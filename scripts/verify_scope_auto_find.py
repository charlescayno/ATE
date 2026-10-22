"""Verify manual scope auto-find trigger (sim) + gear settings dialog."""
import os
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
os.environ["PI_ATE_SIMULATION"] = "1"

OUT = sys.__stdout__
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    msg = f"{'PASS' if cond else 'FAIL'}  {name}"
    if detail and not cond:
        msg += f"  -> {detail}"
    OUT.write(msg + "\n")
    OUT.flush()


def main():
    from PySide2.QtWidgets import QApplication
    from equipment.scope_auto_trigger import AutoFindTriggerSettings, find_trigger_level
    from equipment.simulated_handler import SimulatedEquipmentHandler, VirtualCircuitState

    state = VirtualCircuitState()
    state.vin = 48.0
    scope = SimulatedEquipmentHandler(parent=None).oscilloscope
    scope.state = state
    cfg = AutoFindTriggerSettings(
        trigger_delta=2.0,
        auto_settle_s=0.01,
        step_settle_s=0.01,
        final_settle_s=0.01,
        max_steps=20,
    )
    level = find_trigger_level(scope, 1, "POS", cfg)
    check("algo: returns numeric level", isinstance(level, float) and level > 0, level)

    app = QApplication.instance() or QApplication(sys.argv)
    g = runpy.run_path(str(ROOT / "main.py"), run_name="__scope_af__")
    win = g["MainWindow"]()
    ui = win.ui
    mc = win.manual_control_handler
    sp = mc.scope_panel

    check("ui: auto find button", hasattr(ui, "btn_manual_control_scope_auto_find_trigger"))
    check("ui: auto find gear", hasattr(ui, "btn_manual_control_scope_auto_find_settings"))

    sp.auto_find_settings = AutoFindTriggerSettings(
        trigger_delta=5.0,
        auto_settle_s=0.01,
        step_settle_s=0.01,
        final_settle_s=0.01,
    )
    ui.stackedWidget.setCurrentWidget(ui.page_manual_control)
    app.processEvents()
    sp.auto_find_trigger()
    app.processEvents()
    lvl_text = ui.lineedit_manual_control_scope_trigger_level.text()
    check("ui: level field updated after auto find", lvl_text not in ("", "0.0"), lvl_text)

    passed = sum(1 for _, ok in results if ok)
    OUT.write(f"\n{passed}/{len(results)} passed\n")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
