"""WT500 error 844: INTEGRATE:STOP must not be sent when integration is idle (STOP/TIM/RES)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from equipment.power_meter_specs import PowerMeterBaseClass  # noqa: E402


class FakeDevice:
    resource_name = "GPIB0::7::INSTR"

    def __init__(self, state: str = "STOP"):
        self.timeout = 3000
        self.state = state.upper()
        self.writes: list[str] = []

    def write(self, cmd):
        self.writes.append(cmd)

    def query(self, cmd):
        if cmd == "INTEGRATE:STATE?":
            return self.state
        if cmd == "INTEGRATE:TIMER?":
            return "0, 1, 0"
        return "0"

    def read(self):
        return ""


failures = 0


def check(name, ok, detail=""):
    global failures
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if not ok else ""))
    if not ok:
        failures += 1


def driver_for(state: str) -> PowerMeterBaseClass:
    dev = FakeDevice(state)
    drv = PowerMeterBaseClass(dev, "YOKOGAWA,WT500,123,F1.00")
    drv._integration_time = 60
    return drv


for idle in ("STOP", "TIM", "RES", "RESET", "OFF"):
    drv = driver_for(idle)
    drv.device.writes.clear()
    drv.stop_integration()
    check(
        f"idle {idle}: no INTEGRATE:STOP",
        "INTEGRATE:STOP" not in drv.device.writes,
        drv.device.writes,
    )

drv = driver_for("RUN")
drv.device.writes.clear()
drv.stop_integration()
check("RUN: sends INTEGRATE:STOP", "INTEGRATE:STOP" in drv.device.writes, drv.device.writes)

drv = driver_for("STOP")
drv.device.writes.clear()
drv._stop_and_reset_integration()
check(
    "_stop_and_reset idle: STOP skipped, RESET sent",
    drv.device.writes == ["INTEGRATE:RESET"],
    drv.device.writes,
)

if failures:
    print(f"\n{failures} failure(s)")
    sys.exit(1)
print("\nOK integration stop idle guard")
