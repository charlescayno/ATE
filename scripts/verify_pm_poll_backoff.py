"""Verify Manual Control stops polling lazy/locked and unresponsive power meters."""
import os
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
os.environ["PI_ATE_SIMULATION"] = "1"
os.environ["PI_ATE_AUTO_CONFIRM"] = "1"

errors = []


def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  -> {detail}" if detail and not ok else ""))
    if not ok:
        errors.append(name)


class FakeDevice:
    resource_name = "GPIB0::12::INSTR"
    timeout = 0


class DeadMeter:
    """Every read raises, like a VISA timeout."""

    def __init__(self):
        self.reads = []

    def __getattr__(self, name):
        if name in ("voltage", "current", "power", "pf"):
            self.reads.append(name)
            raise TimeoutError("VI_ERROR_TMO")
        raise AttributeError(name)


class LiveMeter:
    voltage = 230.0
    current = 0.5
    power = 100.0
    pf = 0.9


def check_power_meter_class():
    from equipment.power_meter import MAX_FAILED_POLLS, PowerMeter, PowerMeterUnresponsive

    pm = PowerMeter(FakeDevice(), "YOKOGAWA,760202,ASSUMED-GPIB12,0.0", defer_hardware_init=True)
    check("lazy meter is skipped", pm.is_poll_skipped())
    try:
        pm.poll_basic_params()
        check("lazy meter raises on poll", False)
    except PowerMeterUnresponsive:
        check("lazy meter raises on poll", True)

    dead = DeadMeter()
    pm.power_meter_object = dead
    check("opened meter is no longer skipped", not pm.is_poll_skipped())
    pm.poll_basic_params()
    check("1st failed poll keeps polling", pm.failed_polls == 1, pm.failed_polls)
    check("failed poll stops after voltage", "current" not in dead.reads, dead.reads)
    raised = False
    for _ in range(MAX_FAILED_POLLS - 1):
        try:
            pm.poll_basic_params()
        except PowerMeterUnresponsive:
            raised = True
    check(f"raises after {MAX_FAILED_POLLS} failed polls", raised, pm.failed_polls)

    pm.power_meter_object = LiveMeter()
    pm.failed_polls = 1
    pm.poll_basic_params()
    check("successful poll resets failure count", pm.failed_polls == 0, pm.failed_polls)
    check("successful poll reads all values", (pm._voltage, pm._current, pm._power, pm._pf) == (230.0, 0.5, 100.0, 0.9))


def check_manual_control():
    from PySide2.QtWidgets import QApplication
    from equipment.power_meter import PowerMeter

    app = QApplication.instance() or QApplication(sys.argv)
    g = runpy.run_path(str(ROOT / "main.py"), run_name="__pm_backoff__")
    win = g["MainWindow"]()
    mc = win.manual_control_handler

    dead = DeadMeter()
    pm = PowerMeter(FakeDevice(), "YOKOGAWA,760202,ASSUMED-GPIB12,0.0", defer_hardware_init=True)
    pm.power_meter_object = dead
    win.equipment.power_meter_load_2 = pm
    mc.power_meter_load_2_accessible = True

    mc.power_meter_load_2_update()
    check("page: CH2 still polled after 1 failure", mc.power_meter_load_2_accessible)
    mc.power_meter_load_2_update()
    check("page: CH2 polling stopped after 2 failures", not mc.power_meter_load_2_accessible)
    reads_before = len(dead.reads)
    mc.power_meter_load_2_update()
    check("page: stopped meter is not queried again", len(dead.reads) == reads_before)

    lazy = PowerMeter(FakeDevice(), "YOKOGAWA,WT310E,ASSUMED-GPIB7,0.0", defer_hardware_init=True)
    win.equipment.power_meter_source = lazy
    mc.power_meter_source_accessible = True
    mc.initialize_power_meter_source()
    check("page: lazy source meter never initialized/polled", not mc.power_meter_source_accessible)

    import page_controls.manual_pm_range as manual_pm_range
    check("page: no range sync on entry", not hasattr(manual_pm_range, "apply_all_from_ui"))
    app.processEvents()


def main() -> int:
    check_power_meter_class()
    check_manual_control()
    if errors:
        print(f"\n{len(errors)} check(s) failed.")
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
