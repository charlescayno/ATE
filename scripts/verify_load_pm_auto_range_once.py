"""ensure_auto_range_on: no RANGE MAX, no AUTO writes when already on, slow-query timeout restored."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from equipment.power_meter import PowerMeter  # noqa: E402


class FakeDevice:
    resource_name = "GPIB0::20::INSTR"

    def __init__(self, v_auto=True, i_auto=True):
        self.timeout = 500
        self.v_auto = v_auto
        self.i_auto = i_auto
        self.writes: list[str] = []
        self.query_timeouts: dict[str, int] = {}

    def write(self, cmd):
        self.writes.append(cmd)
        if cmd.startswith("INPUT:VOLTAGE:AUTO "):
            self.v_auto = cmd.endswith("ON")
        if cmd.startswith("INPUT:CURRENT:AUTO "):
            self.i_auto = cmd.endswith("ON")

    def query(self, cmd):
        self.query_timeouts[cmd] = self.timeout
        if cmd == "INPUT:VOLTAGE:AUTO?":
            return "1" if self.v_auto else "0"
        if cmd == "INPUT:CURRENT:AUTO?":
            return "1" if self.i_auto else "0"
        if cmd == "MEASURE:AVERAGING:STATE?":
            return "0"
        if cmd.endswith("RANGE?"):
            return "1.0E+00"
        return "0"

    def read(self):
        return ""


failures = 0


def check(name, ok, detail=""):
    global failures
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if not ok else ""))
    if not ok:
        failures += 1


dev = FakeDevice()
pm = PowerMeter(dev, "YOKOGAWA,WT310E,C3TB07044E,F1.02")
dev.writes.clear()
check("already AUTO: returns True", pm.ensure_auto_range_on(settle_s=0) is True)
check("already AUTO: no writes", dev.writes == [], dev.writes)
check("slow query timeout 3 s", dev.query_timeouts.get("INPUT:CURRENT:AUTO?") == 3000, dev.query_timeouts)
check("timeout restored after slow query", dev.timeout == pm.power_meter_object.POWER_METER_TIMEOUT_MS, dev.timeout)

dev.v_auto = dev.i_auto = False
dev.writes.clear()
check("AUTO off: turned on", pm.ensure_auto_range_on(settle_s=0) is True)
check("AUTO off: never RANGE MAX", not any("RANGE MAX" in w for w in dev.writes), dev.writes)
check("AUTO off: AUTO ON once each",
      dev.writes.count("INPUT:VOLTAGE:AUTO ON") == 1 and dev.writes.count("INPUT:CURRENT:AUTO ON") == 1,
      dev.writes)
check("valid STOP header", "INTEGRATION:STOP" not in dev.writes, dev.writes)

check("power meter VISA timeout 3 s", dev.timeout == 3000 or pm.power_meter_object.device.timeout == 3000,
      dev.timeout)

pm.power_meter_object._integration_time = 60
orig_query = dev.query
dev.query = lambda cmd: "748.3E+00" if cmd == "INTEGRATE:TIMER?" else orig_query(cmd)
check("stale TIMER? reply ignored", pm.get_integration_timer() == 60, pm.get_integration_timer())
dev.query = lambda cmd: "0,1,0" if cmd == "INTEGRATE:TIMER?" else orig_query(cmd)
check("h,m,s TIMER? parsed", pm.get_integration_timer() == 60, pm.get_integration_timer())

print("\nAll checks passed." if not failures else f"\n{failures} check(s) FAILED")
sys.exit(1 if failures else 0)
