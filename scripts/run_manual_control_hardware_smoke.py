"""Exercise Manual Equipment Control against the real bench (safe DC cap).

Requires assigned equipment and GPIB. Uses PI_ATE_MANUAL_DC_MAX_V (default 10 V here).
"""
from __future__ import annotations

import os
import sys
import tempfile
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
os.environ.setdefault("PI_ATE_AUTO_CONFIRM", "1")
os.environ.setdefault("PI_ATE_MANUAL_DC_MAX_V", "10")

# Real hardware only
os.environ.pop("PI_ATE_SIMULATION", None)
if "--hardware" not in sys.argv and "-hw" not in sys.argv:
    sys.argv.append("--hardware")

errors: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    tag = "OK" if ok else "FAIL"
    print(f"{tag}  {name}" + (f"  {detail}" if detail and not ok else ""))
    if not ok:
        errors.append(f"{name}: {detail}" if detail else name)


def pump(app, mc, cycles: int = 15, delay_s: float = 0.05) -> None:
    for _ in range(cycles):
        app.processEvents()
        try:
            mc.update_service()
        except Exception:
            pass
        time.sleep(delay_s)


def safe_call(name: str, fn) -> None:
    try:
        fn()
        check(name, True)
    except Exception as exc:
        check(name, False, f"{type(exc).__name__}: {exc}")
        traceback.print_exc()


def main() -> int:
    print("[SMOKE] starting manual control hardware smoke…", flush=True)
    from PySide2.QtWidgets import QApplication

    app = QApplication.instance() or QApplication(sys.argv)

    import runpy

    g = runpy.run_path(str(ROOT / "main.py"), run_name="__mc_hw__")
    win = g["MainWindow"]()
    mc = win.manual_control_handler
    ui = mc.ui
    eq = win.equipment

    print(f"[SMOKE] PI_ATE_MANUAL_DC_MAX_V={os.environ.get('PI_ATE_MANUAL_DC_MAX_V')}")
    print(f"[SMOKE] simulation={getattr(win, 'is_simulation_mode', False)}")

    if getattr(win, "is_simulation_mode", False):
        check("hardware mode", False, "bench fell back to simulation; use --hardware or assign GPIB")
        return 1

    safe_call("manual_control.start", mc.start)
    pump(app, mc, 10)

    safe_call("refresh_equipment_readings", mc.refresh_equipment_readings)
    pump(app, mc, 5)

    if hasattr(ui, "chkbox_manual_control_live_poll"):
        safe_call(
            "live_poll toggle on",
            lambda: ui.chkbox_manual_control_live_poll.setChecked(True),
        )
        pump(app, mc, 8)
        safe_call(
            "live_poll toggle off",
            lambda: ui.chkbox_manual_control_live_poll.setChecked(False),
        )
        pump(app, mc, 3)

    safe_call("PM auto range", mc.reset_all_power_meters_auto_range)
    pump(app, mc, 10)

    # Presets (temp file via save/load)
    preset_name = "_smoke_mc_temp"
    if mc.cbx_manual_preset.findText(preset_name) < 0:
        mc.cbx_manual_preset.addItem(preset_name)
    mc.cbx_manual_preset.setCurrentText(preset_name)

    safe_call("preset save", mc.save_session_preset)
    safe_call("preset load", mc.load_session_preset)

    # Line input — DC/Magna only above 0; cap enforced by env
    src = getattr(mc, "ac_source", None)
    is_dc_magna = src is not None and __import__(
        "equipment.dc_source", fromlist=["is_magna_hvdc"]
    ).is_magna_hvdc(src)

    ui.lineedit_manual_control_ac_source_voltage.setText("5")
    pump(app, mc, 2)

    if is_dc_magna:
        safe_call("DC voltage clamp rejects >10 V", lambda: _test_dc_clamp(mc, app))
        ui.lineedit_manual_control_ac_source_voltage.setText("5")
        pump(app, mc, 2)
        safe_call(
            "source OFF (before ON)",
            lambda: mc.set_acsource_flags(
                __import__("equipment.ac_source", fromlist=["AC_SOURCE_REQUEST"]).AC_SOURCE_REQUEST.OFF
            ),
        )
        pump(app, mc, 8)
        safe_call(
            "source ON @ 5 V DC",
            lambda: mc.set_acsource_flags(
                __import__("equipment.ac_source", fromlist=["AC_SOURCE_REQUEST"]).AC_SOURCE_REQUEST.ON
            ),
        )
        pump(app, mc, 40)
        safe_call(
            "source OFF",
            lambda: mc.set_acsource_flags(
                __import__("equipment.ac_source", fromlist=["AC_SOURCE_REQUEST"]).AC_SOURCE_REQUEST.OFF
            ),
        )
        pump(app, mc, 15)
    else:
        print("[SMOKE] skip source ON/OFF (not Magna HVDC line input)")

    ui.chkbox_manual_control_auto_discharge.setChecked(False)
    safe_call("discharge button", mc.discharge_output_manual)
    pump(app, mc, 20)

    # E-load channels (minimal — set 0 A / OFF only)
    from page_controls import eload_grid

    for n in eload_grid.CHANNELS:
        ld = getattr(eq, f"electronic_load_{n}", None)
        if ld is None:
            continue
        ch = mc.eload_grid.channels.get(n)
        if ch is None:
            continue
        w = ch.w
        safe_call(f"eload {n} set A=0", lambda c=ch: c.w["a_edit"].setText("0"))
        safe_call(f"eload {n} Set A", lambda c=ch: c.set_level(1))
        pump(app, mc, 5)
        safe_call(f"eload {n} OFF", lambda c=ch: c.turn_off())
        pump(app, mc, 5)

    # Aux DC — apply only, no output ON if unassigned
    if getattr(mc, "dc_source_aux_accessible", False) and mc.dc_source_aux is not None:
        widgets = getattr(mc, "hmp_aux_channel_widgets", {})
        if 1 in widgets:
            widgets[1]["le_v"].setText("3.3")
            widgets[1]["le_i"].setText("0.1")
            safe_call("aux DC apply CH1", lambda: mc.aux_dc_apply_settings(1))
            pump(app, mc, 5)

    safe_call("E-STOP", mc.emergency_stop_all)
    pump(app, mc, 10)

    if os.environ.get("PI_ATE_SMOKE_RESET_GPIB", "").strip().lower() in ("1", "yes", "true"):
        safe_call("reset all GPIB", mc.reset_all_gpib_equipment)
        pump(app, mc, 15)
    else:
        print("[SMOKE] skip reset all GPIB (set PI_ATE_SMOKE_RESET_GPIB=1 to include)")

    safe_call("manual_control.stop", mc.stop)

    if errors:
        print(f"\n{len(errors)} failure(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("\nOK Manual Equipment Control hardware smoke")
    return 0


def _test_dc_clamp(mc, app) -> None:
    from equipment.ac_source import AC_SOURCE_REQUEST

    mc.ui.lineedit_manual_control_ac_source_voltage.setText("48")
    mc.set_acsource_flags(AC_SOURCE_REQUEST.ON)
    for _ in range(30):
        app.processEvents()
        mc.update_service()
        time.sleep(0.05)
    mc.set_acsource_flags(AC_SOURCE_REQUEST.OFF)
    for _ in range(10):
        app.processEvents()
        mc.update_service()
        time.sleep(0.05)
    # Should not throw; clamp is logged in ac_source_power_on


if __name__ == "__main__":
    sys.exit(main())
