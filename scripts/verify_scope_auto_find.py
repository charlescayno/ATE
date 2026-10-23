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


class _SequenceScope:
    """Wrap simulated scope and record key auto-find call order."""

    def __init__(self, inner):
        self._inner = inner
        self.events = []

    def __getattr__(self, name):
        return getattr(self._inner, name)

    def edge_trigger(self, channel, level, edge="POS"):
        self.events.append(("edge_trigger", float(level)))
        return self._inner.edge_trigger(channel, level, edge)

    def trigger_mode(self, mode):
        self.events.append(("trigger_mode", mode))
        return self._inner.trigger_mode(mode)

    def set_trigger_mode(self, mode):
        self.events.append(("trigger_mode", mode))
        return self._inner.set_trigger_mode(mode)

    def run_single(self):
        self.events.append(("run_single", None))
        return self._inner.run_single()

    def get_measure(self, channel):
        self.events.append(("get_measure", channel))
        return self._inner.get_measure(channel)


def _check_sequence(events):
    """edge 0 -> AUTO -> run_single -> get_measure -> NORM -> sweep edge @ Max."""
    if len(events) < 5:
        return False, events
    if events[0] != ("edge_trigger", 0.0):
        return False, events
    auto_idx = next((i for i, e in enumerate(events) if e == ("trigger_mode", "AUTO")), None)
    if auto_idx is None:
        return False, events
    if events[auto_idx + 1] != ("run_single", None):
        return False, events
    if events[auto_idx + 2][0] != "get_measure":
        return False, events
    norm_idx = next((i for i, e in enumerate(events) if e == ("trigger_mode", "NORM")), None)
    if norm_idx is None or norm_idx <= auto_idx + 2:
        return False, events
    max_edge = events[norm_idx + 1]
    if max_edge[0] != "edge_trigger" or max_edge[1] <= 0:
        return False, events
    return True, events


def main():
    from PySide2.QtWidgets import QApplication
    from equipment.scope_auto_trigger import AutoFindTriggerSettings, find_trigger_level
    from equipment.simulated_handler import SimulatedEquipmentHandler, VirtualCircuitState

    state = VirtualCircuitState()
    state.vin = 48.0
    inner = SimulatedEquipmentHandler(parent=None).oscilloscope
    inner.state = state
    scope = _SequenceScope(inner)
    cfg = AutoFindTriggerSettings(
        trigger_delta=2.0,
        auto_settle_s=0.01,
        step_settle_s=0.01,
        final_settle_s=0.01,
        max_steps=20,
    )
    level = find_trigger_level(scope, 1, "POS", cfg)
    check("algo: returns numeric level", isinstance(level, float) and level > 0, level)
    ok_seq, ev = _check_sequence(scope.events)
    check("algo: call sequence (0V, AUTO, run_single, measure, NORM, sweep)", ok_seq, ev)

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
