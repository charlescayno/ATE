"""Verify WT500 V/I range stays fixed: no AUTO at connect, page entry or polling; AUTO only on user request."""
import os
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
os.environ["PI_ATE_SIMULATION"] = "1"
os.environ["PI_ATE_AUTO_CONFIRM"] = "1"

import equipment.power_meter_specs as specs

specs.sleep = lambda *_: None

errors = []


def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  -> {detail}" if detail and not ok else ""))
    if not ok:
        errors.append(name)


class FakeWT500Device:
    """Tracks AUTO / RANGE state like the meter; records every write."""

    resource_name = "GPIB0::5::INSTR"
    timeout = 0

    def __init__(self, v_range=300.0, i_range=5.0, v_auto=False, i_auto=False, max_current=40.0):
        self.v_range, self.i_range = v_range, i_range
        self.v_auto, self.i_auto = v_auto, i_auto
        self.max_current = max_current
        self.writes = []

    def write(self, cmd):
        self.writes.append(cmd)
        key, _, arg = cmd.partition(" ")
        if key == "INPUT:VOLTAGE:AUTO":
            self.v_auto = arg == "ON"
        elif key == "INPUT:CURRENT:AUTO":
            self.i_auto = arg == "ON"
        elif key == "INPUT:VOLTAGE:RANGE":
            self.v_range = 1000.0 if arg == "MAX" else float(arg.rstrip("V"))
        elif key == "INPUT:CURRENT:RANGE":
            self.i_range = self.max_current if arg == "MAX" else min(float(arg.rstrip("A")), self.max_current)

    def query(self, cmd):
        return {
            "INPUT:VOLTAGE:AUTO?": "1" if self.v_auto else "0",
            "INPUT:CURRENT:AUTO?": "1" if self.i_auto else "0",
            "INPUT:VOLTAGE:RANGE?": f"{self.v_range:E}",
            "INPUT:CURRENT:RANGE?": f"{self.i_range:E}",
            "MEASURE:AVERAGING:STATE?": "0",
            "NUMERIC:NORMAL:VALUE? 1": "230.0",
        }.get(cmd, "0")

    def read(self):
        return ""

    def auto_on_writes(self):
        return [w for w in self.writes if "AUTO ON" in w]

    def range_writes(self):
        return [w for w in self.writes if "RANGE" in w or "AUTO" in w]


def make_wt500(**kw):
    from equipment.power_meter import PowerMeter

    dev = FakeWT500Device(**kw)
    return PowerMeter(dev, "YOKOGAWA,760202,FAKE01,1.0"), dev


def check_connect_and_wrapper():
    pm, dev = make_wt500(v_range=300.0, i_range=5.0)
    check("connect: no AUTO ON sent", not dev.auto_on_writes(), dev.auto_on_writes())
    check("connect: range untouched", (dev.v_range, dev.i_range, dev.v_auto, dev.i_auto) == (300.0, 5.0, False, False))
    check("WT500 supports fixed range", pm.supports_fixed_range())

    dev.writes.clear()
    actual = pm.set_fixed_voltage_range(150)
    check("fixed V: AUTO OFF + RANGE only", dev.writes == ["INPUT:VOLTAGE:AUTO OFF", "INPUT:VOLTAGE:RANGE 150V"], dev.writes)
    check("fixed V: readback returned", actual == 150.0, actual)
    check("read_range_state", pm.read_range_state() == (False, 150.0, False, 5.0), pm.read_range_state())

    dev.writes.clear()
    for _ in range(3):
        pm.poll_basic_params()
    check("polling sends no range/auto commands", not dev.range_writes(), dev.range_writes())

    dev.writes.clear()
    pm.auto_range_enable(False)
    check(
        "auto off for both restores V and I range",
        "INPUT:VOLTAGE:RANGE 150.0V" in dev.writes and "INPUT:CURRENT:RANGE 5.0A" in dev.writes,
        dev.writes,
    )


def check_manual_control():
    from PySide2.QtWidgets import QApplication
    import page_controls.manual_pm_range as mpr

    app = QApplication.instance() or QApplication(sys.argv)
    g = runpy.run_path(str(ROOT / "main.py"), run_name="__wt500_range__")
    win = g["MainWindow"]()
    mc = win.manual_control_handler
    ui = mc.ui

    src, src_dev = make_wt500(v_range=300.0, i_range=5.0, i_auto=True)
    load, load_dev = make_wt500(v_range=60.0, i_range=2.0, max_current=10.0)
    mc.power_meter_source = src
    win.equipment.power_meter_load_2 = load
    src_dev.writes.clear()
    load_dev.writes.clear()

    mpr.sync_from_meters(mc)
    vbx, cbx = ui.cbx_pms_voltage_range, ui.cbx_pms_current_range
    lv, lc = ui.cbx_pml_voltage_range_2, ui.cbx_pml_current_range_2
    check("entry: WT500 V list", [vbx.itemText(i) for i in range(vbx.count())] == ["AUTO"] + [f"{v:g} V" for v in mpr.WT500_VOLTAGE_RANGES])
    check("entry: WT500 I list", [cbx.itemText(i) for i in range(cbx.count())] == ["AUTO"] + [f"{v:g} A" for v in mpr.WT500_CURRENT_RANGES])
    check("entry: source shows meter state (300 V / AUTO)", (vbx.currentText(), cbx.currentText()) == ("300 V", "AUTO"), (vbx.currentText(), cbx.currentText()))
    check("entry: load CH2 shows meter state (60 V / 2 A)", (lv.currentText(), lc.currentText()) == ("60 V", "2 A"), (lv.currentText(), lc.currentText()))
    check("entry: nothing written to meters", not src_dev.writes and not load_dev.writes, src_dev.writes + load_dev.writes)

    vbx.setCurrentText("600 V")
    check("change V: AUTO OFF + 600V only", src_dev.writes == ["INPUT:VOLTAGE:AUTO OFF", "INPUT:VOLTAGE:RANGE 600V"], src_dev.writes)
    src_dev.writes.clear()
    cbx.setCurrentText("10 A")
    check("change I from AUTO: AUTO OFF + 10A", src_dev.writes == ["INPUT:CURRENT:AUTO OFF", "INPUT:CURRENT:RANGE 10A"], src_dev.writes)
    check("change I: meter now fixed", not src_dev.i_auto and src_dev.i_range == 10.0)

    load_dev.writes.clear()
    lc.setCurrentText("40 A")
    check("rejected range: combo shows meter readback", lc.currentText() == "10 A", lc.currentText())

    src_dev.writes.clear()
    mpr.sync_from_meters(mc)
    check("re-entry keeps fixed range, no writes", (vbx.currentText(), cbx.currentText()) == ("600 V", "10 A") and not src_dev.writes)

    vbx.setCurrentIndex(0)
    check("AUTO selected: AUTO ON sent for voltage only", src_dev.auto_on_writes() == ["INPUT:VOLTAGE:AUTO ON"], src_dev.auto_on_writes())

    src_dev.writes.clear()
    load_dev.writes.clear()
    mc.reset_all_power_meters_auto_range()
    check("PM Auto Range: source V+I AUTO ON", src_dev.v_auto and src_dev.i_auto)
    check("PM Auto Range: load V+I AUTO ON", load_dev.v_auto and load_dev.i_auto)
    check("PM Auto Range: each AUTO ON sent once", len(src_dev.auto_on_writes()) == 2, src_dev.auto_on_writes())
    app.processEvents()


def main() -> int:
    check_connect_and_wrapper()
    check_manual_control()
    if errors:
        print(f"\n{len(errors)} check(s) failed.")
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
