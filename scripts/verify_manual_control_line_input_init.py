"""Verify Manual Control line-input init: Magna DC UI vs AC UI."""
import os
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
os.environ["PI_ATE_SIMULATION"] = "1"

errors = []


def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  -> {detail}" if detail and not ok else ""))
    if not ok:
        errors.append(name)


def main() -> int:
    from PySide2.QtWidgets import QApplication

    app = QApplication.instance() or QApplication(sys.argv)
    g = runpy.run_path(str(ROOT / "main.py"), run_name="__mc_init__")
    win = g["MainWindow"]()
    mc = win.manual_control_handler
    eq = win.equipment
    ui = mc.ui

    eq.ac_source = None
    eq.dc_source = eq.dc_sources[0]
    mc.ac_source_accessible = True
    mc.initialize_ac_source()

    check("Magna-only: ac_source bound", mc.ac_source is eq.dc_source)
    check("Magna-only: DC SOURCE label", ui.label_manual_control_ac_source.text() == "DC SOURCE")
    check(
        "Magna-only: ramp controls not hidden",
        not ui.chkbox_manual_control_dc_source_ramp_enable.isHidden(),
    )
    check("Magna-only: frame enabled", ui.frame_manual_control_ac_source.isEnabled())

    eq.ac_source = eq.ac_sources[0]
    eq.dc_source = eq.dc_sources[0]
    mc.ac_source_accessible = True
    mc.initialize_ac_source()
    check("AC assigned: AC SOURCE label", ui.label_manual_control_ac_source.text() == "AC SOURCE")
    check(
        "AC assigned: ramp hidden",
        ui.chkbox_manual_control_dc_source_ramp_enable.isHidden()
        or not ui.chkbox_manual_control_dc_source_ramp_enable.isVisible(),
    )

    if errors:
        print(f"\n{len(errors)} check(s) failed.")
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
