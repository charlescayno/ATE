"""Verify Manual Equipment Control has no scope panel and retains E-STOP."""
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
            "btn_manual_control_pm_auto_range",
            "btn_manual_control_reset_all_gpib",
        ):
            if not hasattr(ui, name):
                errors.append(f"missing ui.{name}")

        if getattr(mc, "scope_panel", None) is not None:
            errors.append("scope_panel should not be created on Manual Equipment Control")
        if hasattr(ui, "frame_manual_control_oscilloscope"):
            errors.append("manual oscilloscope frame should not exist")

        scroll = getattr(ui, "scroll_manual_control_equipment", None)
        if scroll is None or scroll.widget() is None:
            errors.append("equipment scroll area missing")
        elif ui.verticalLayout_12.indexOf(ui.frame_manual_control_lower) >= 0:
            errors.append("lower equipment frame should live inside scroll area, not main layout")

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
    print("OK Manual Control scope section removed + E-STOP retained")
    return 0


if __name__ == "__main__":
    sys.exit(main())
