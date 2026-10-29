"""Turn ON/OFF must run with Live poll off (immediate ac_source_update)."""
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


def main() -> int:
    from PySide2.QtWidgets import QApplication
    from page_controls import manual_control as mc_mod

    app = QApplication.instance() or QApplication(sys.argv)
    g = runpy.run_path(str(ROOT / "main.py"), run_name="__mc_onoff__")
    win = g["MainWindow"]()
    mc = win.manual_control_handler
    eq = win.equipment
    ui = mc.ui

    eq.ac_source = None
    eq.dc_source = eq.dc_sources[0]
    src = eq.dc_source
    mc.ac_source = src
    mc.ac_source_accessible = True
    mc._gpib_init_ready = True
    mc._apply_manual_line_input_dc_ui()
    setattr(src, "coupling", mc_mod.AC_SOURCE_COUPLING.DC)

    ui.lineedit_manual_control_ac_source_voltage.setText("48")
    ui.lineedit_manual_control_dc_source_current_limit.setText("0.8")
    ui.chkbox_manual_control_dc_source_ramp_enable.setChecked(False)

    calls = {"on": 0, "off": 0}
    orig_on = src.turn_on
    orig_off = src.turn_off

    def turn_on():
        calls["on"] += 1
        return orig_on()

    def turn_off():
        calls["off"] += 1
        return orig_off()

    src.turn_on = turn_on
    src.turn_off = turn_off

    mc.live_poll_enabled = False
    mc._apply_live_poll_timer()
    check("timer stopped when live poll off", not mc.update_timer.isActive())

    mc.ac_source_request = mc_mod.AC_SOURCE_REQUEST.NO_REQUEST
    mc.set_acsource_flags(mc_mod.AC_SOURCE_REQUEST.ON)
    check("Turn ON calls turn_on immediately", calls["on"] == 1, calls)
    check("request cleared after ON", mc.ac_source_request == mc_mod.AC_SOURCE_REQUEST.NO_REQUEST)

    mc.set_acsource_flags(mc_mod.AC_SOURCE_REQUEST.OFF)
    check("Turn OFF calls turn_off immediately", calls["off"] == 1, calls)

    if errors:
        print(f"\n{len(errors)} check(s) failed.")
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
