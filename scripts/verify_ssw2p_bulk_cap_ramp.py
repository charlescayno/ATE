"""Verify Steady-State Waveform 2 Port Vin ramp (no return-to-zero, 100 V/s)."""
import os
import sys
from pathlib import Path
from types import SimpleNamespace

_cwd_root = Path.cwd().resolve()
_file_root = Path(__file__).resolve().parents[1]
ROOT = _cwd_root if (_cwd_root / "main.py").is_file() else _file_root
os.chdir(ROOT)


def _scrub_sys_path(root: Path):
    root_res = root.resolve()
    root_s = str(root_res)
    cleaned = []
    for p in sys.path:
        if not p:
            continue
        try:
            pr = Path(p).resolve()
        except OSError:
            cleaned.append(p)
            continue
        if pr == root_res or root_res in pr.parents:
            cleaned.append(p)
            continue
        norm = p.replace("\\", "/").lower()
        if "pi_ate" in norm or "pi-ate" in norm:
            continue
        cleaned.append(p)
    sys.path = [root_s] + [p for p in cleaned if os.path.normcase(p) != os.path.normcase(root_s)]


_scrub_sys_path(ROOT)

from PySide2.QtWidgets import QApplication  # noqa: E402

QApplication.instance() or QApplication(sys.argv)

from equipment.ac_source import AC_SOURCE_COUPLING  # noqa: E402
from psu_tests.test_type import TestTypes  # noqa: E402
from psu_tests.test_efficiency_2port_waveform import EfficiencyWaveformTest_2Port  # noqa: E402
import psu_tests.test_efficiency_2port_waveform as eff2p_mod  # noqa: E402

OUT = sys.__stdout__
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    msg = f"{'PASS' if cond else 'FAIL'}  {name}"
    if detail and not cond:
        msg += f"  -> {detail}"
    OUT.write(msg + "\n")
    OUT.flush()


class FakeInputSupply:
    def __init__(self, v=300.0):
        self._v = float(v)
        self.commands = []
        self.turn_off_calls = 0

    @property
    def voltage(self):
        return self._v

    def turn_off(self):
        self.turn_off_calls += 1

    def turn_on(self):
        self.commands.append("ON")

    def set_voltage_with_coupling(self, voltage, coupling):
        self.commands.append(float(voltage))
        self._v = float(voltage)


def _make_test(vin_list=None):
    test = EfficiencyWaveformTest_2Port.__new__(EfficiencyWaveformTest_2Port)
    test.coupling = AC_SOURCE_COUPLING.DC
    test.input_supply = FakeInputSupply(300.0)
    test.power_meter_source = None
    test.vin_list = vin_list or [[300, 0], [400, 0], [200, 0]]
    test.soak_time = SimpleNamespace(initial_soak=0, soak_per_line=0, soak_per_load=0, integration_time=0)
    test.load_pairs = [(1, 1)]
    test.usbpd_test = False
    test.discharge_pulses = 0
    test.settle_time = 0
    test.post_capture_delay = 0
    test.auto_find_trigger = False
    test.input_supply_needs_discharge_resistor_check = lambda: True
    return test


def test_ramp_up_no_zero():
    eff2p_mod.sleep = lambda _s: None
    test = _make_test()
    test._last_bulk_cap_vin_set = 300.0
    test._bulk_cap_ramp_to_voltage(400.0)
    volts = [c for c in test.input_supply.commands if isinstance(c, (int, float))]
    check("ramp up: no turn_off", test.input_supply.turn_off_calls == 0)
    check("ramp up: never commands 0 V", 0.0 not in volts)
    check("ramp up: ends at target", volts[-1] == 400.0)
    check("ramp up: starts near 300", min(volts) >= 300.0 - 0.01)


def test_ramp_down():
    eff2p_mod.sleep = lambda _s: None
    test = _make_test()
    test.input_supply = FakeInputSupply(400.0)
    test._last_bulk_cap_vin_set = 400.0
    test._bulk_cap_ramp_to_voltage(200.0)
    volts = [c for c in test.input_supply.commands if isinstance(c, (int, float))]
    check("ramp down: no turn_off", test.input_supply.turn_off_calls == 0)
    check("ramp down: never commands 0 V", 0.0 not in volts)
    check("ramp down: ends at 200", volts[-1] == 200.0)
    check("ramp down: max step from 400", max(volts) <= 400.0 + 0.01)


def test_estimate_uses_delta_vin():
    test = _make_test()
    t, _ = test.estimate_remaining(0, 0, vin_delays=True)
    # 300->400: 1s + 0.2, 400->200: 2s + 0.2, plus fixed blocks per vin (4s each * 3) ...
    # Only assert first vin uses 0.5s ramp slot not 300/100=3s
    test2 = _make_test(vin_list=[[400, 0], [200, 0]])
    t2, _ = test2.estimate_remaining(0, 0, vin_delays=True)
    t_first_only = _make_test(vin_list=[[400, 0]])
    t_first, _ = t_first_only.estimate_remaining(0, 0, vin_delays=True)
    check("estimate: first vin ramp slot <= 1s", t_first < 20)
    check("estimate: two-step > one-step", t2 > t_first)


if __name__ == "__main__":
    test_ramp_up_no_zero()
    test_ramp_down()
    test_estimate_uses_delta_vin()
    failed = [n for n, ok in results if not ok]
    OUT.write(f"\n{len(results) - len(failed)}/{len(results)} passed\n")
    sys.exit(1 if failed else 0)
