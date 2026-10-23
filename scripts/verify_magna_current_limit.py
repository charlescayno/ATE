"""Verify Manual Control sends the Magna current limit before Output ON."""
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


class FakeMagna:
    manufacturer = "Magna-Power Electronics Inc."
    model = "TSD2000-2.5"
    description = "Fake TSD2000-2.5"

    def __init__(self):
        self.coupling = None
        self.calls = []

    def set_current_limit(self, a):
        self.calls.append(("ilim", a))

    def set_voltage_with_coupling(self, voltage, coupling):
        self.calls.append(("volt", voltage))

    def turn_on(self):
        self.calls.append(("on",))

    @property
    def voltage(self):
        return 0.0


def main() -> int:
    from PySide2.QtWidgets import QApplication
    import page_controls.safety_dialog as safety

    safety.confirm_discharge_resistor_disengaged = lambda *_: True
    app = QApplication.instance() or QApplication(sys.argv)
    g = runpy.run_path(str(ROOT / "main.py"), run_name="__magna_ilim__")
    win = g["MainWindow"]()
    mc = win.manual_control_handler
    ui = mc.ui
    msgs = []
    mc.parent.msg_box_info = lambda **kw: msgs.append(kw)

    magna = FakeMagna()
    mc.ac_source = magna
    mc._apply_manual_line_input_dc_ui()
    field = ui.lineedit_manual_control_dc_source_current_limit
    check("DC mode shows Current Limit field", not field.isHidden())
    ui.chkbox_manual_control_dc_source_ramp_enable.setChecked(False)
    ui.lineedit_manual_control_ac_source_voltage.setText("750")

    field.setText("")
    mc.ac_source_power_on()
    check("blank field: model max 2.5 A sent before ON", magna.calls == [("ilim", 2.5), ("volt", 750.0), ("on",)], magna.calls)

    magna.calls.clear()
    field.setText("1.2")
    mc.ac_source_power_on()
    check("1.2 A sent before ON", magna.calls[:1] == [("ilim", 1.2)] and magna.calls[-1] == ("on",), magna.calls)

    magna.calls.clear()
    field.setText("5")
    mc.ac_source_power_on()
    check("above model max: no output ON", ("on",) not in magna.calls, magna.calls)
    check("above model max: user warned", len(msgs) == 1, msgs)

    magna.calls.clear()
    field.setText("0.8")
    field.editingFinished.emit()
    check("editing field applies limit immediately", magna.calls == [("ilim", 0.8)], magna.calls)

    mc._apply_manual_line_input_ac_ui()
    check("AC mode hides Current Limit field", field.isHidden())
    app.processEvents()

    if errors:
        print(f"\n{len(errors)} check(s) failed.")
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
