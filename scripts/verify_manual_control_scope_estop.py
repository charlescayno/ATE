"""Verify scope panel + E-STOP on Manual Equipment Control."""
import os
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
os.environ["PI_ATE_SIMULATION"] = "1"
os.environ["PI_ATE_AUTO_CONFIRM"] = "1"

_SETTINGS = ROOT / "manual_control_settings.json"


def main() -> int:
    from PySide2.QtWidgets import QApplication

    app = QApplication.instance() or QApplication(sys.argv)
    settings_backup = None
    if _SETTINGS.exists():
        settings_backup = ROOT / "manual_control_settings.json.verify_bak"
        if settings_backup.exists():
            settings_backup.unlink()
        _SETTINGS.rename(settings_backup)
    errors = []
    try:
        g = runpy.run_path(str(ROOT / "main.py"), run_name="__mc_scope__")
        win = g["MainWindow"]()
        mc = win.manual_control_handler
        ui = win.ui

        for name in (
            "btn_manual_control_estop",
            "frame_manual_control_oscilloscope",
            "btn_manual_control_scope_run",
            "btn_manual_control_scope_run_single",
            "btn_manual_control_scope_stop",
            "btn_manual_control_scope_capture",
            "cbx_manual_control_scope_trigger_mode",
            "cbx_manual_control_scope_trigger_edge",
            "lineedit_manual_control_scope_trigger_level",
            "lineedit_manual_control_scope_filename",
            "btn_manual_control_scope_auto_find_trigger",
            "btn_manual_control_scope_auto_find_settings",
        ):
            if not hasattr(ui, name):
                errors.append(f"missing ui.{name}")

        layout = ui.verticalLayout_12
        scroll = getattr(ui, "scroll_manual_control_equipment", None)
        osc_idx = layout.indexOf(ui.frame_manual_control_oscilloscope)
        scroll_idx = layout.indexOf(scroll) if scroll is not None else -1
        if osc_idx < 0 or scroll_idx < 0 or osc_idx <= scroll_idx:
            errors.append("oscilloscope panel should be below equipment scroll area")
        if scroll is None or scroll.widget() is None:
            errors.append("equipment scroll area missing")
        elif layout.indexOf(ui.frame_manual_control_lower) >= 0:
            errors.append("lower equipment frame should live inside scroll area, not main layout")

        sp = mc.scope_panel
        sp.run_single()
        if ui.label_manual_control_scope_status.text() != "SINGLE":
            errors.append("run_single status")
        sp.run_continuous()
        sp.stop()
        if ui.cbx_manual_control_scope_trigger_edge.currentText() != "Rising":
            errors.append("default trigger edge should be Rising")
        ui.cbx_manual_control_scope_trigger_edge.setCurrentText("Falling")
        sp.apply_edge_trigger()
        sp.apply_trigger_mode()
        sp.capture_waveform()
        if "Saved:" not in sp.label_capture_path.text() and "Capture failed" not in sp.label_capture_path.text():
            errors.append("capture path label")

        mc.emergency_stop_all()

        if not hasattr(mc.discharge, "cancel"):
            errors.append("DischargeSequencer.cancel missing")
    finally:
        if settings_backup and settings_backup.exists():
            if _SETTINGS.exists():
                _SETTINGS.unlink()
            settings_backup.rename(_SETTINGS)

    if errors:
        print("FAIL")
        for e in errors:
            print(" ", e)
        return 1
    print("OK manual control scope panel + E-STOP")
    return 0


if __name__ == "__main__":
    sys.exit(main())
