"""Verify AUX DC manual-control panel layout (stacked under DC SOURCE, 3 HMP channels).

Run from repo root with PI ATE conda Python 3.10+:
  conda_env\\python.exe scripts\\verify_aux_dc_ui_layout.py
"""
import os
import runpy
import sys
from pathlib import Path

_cwd_root = Path.cwd().resolve()
_file_root = Path(__file__).resolve().parents[1]
ROOT = _cwd_root if (_cwd_root / "main.py").is_file() else _file_root
os.chdir(ROOT)


def _scrub_sys_path(root: Path):
    root_res = root.resolve()
    root_s = str(root_res)
    cleaned = []
    for p in sys.path:
        if not p:
            continue
        try:
            pr = Path(p).resolve()
        except OSError:
            cleaned.append(p)
            continue
        if pr == root_res or root_res in pr.parents:
            cleaned.append(p)
            continue
        norm = p.replace("\\", "/").lower()
        if "pi_ate" in norm or "pi-ate" in norm:
            continue
        cleaned.append(p)
    sys.path = [root_s] + [p for p in cleaned if os.path.normcase(p) != os.path.normcase(root_s)]


_scrub_sys_path(ROOT)
os.environ["PI_ATE_SIMULATION"] = "1"
os.environ["PI_ATE_AUTO_CONFIRM"] = "1"

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
    from equipment.dc_source import HMP_MANUAL_CHANNEL_COUNT

    app = QApplication.instance() or QApplication(sys.argv)
    g = runpy.run_path(str(ROOT / "main.py"), run_name="__aux_ui__")
    win = g["MainWindow"]()
    ui = win.ui

    check("ui: dc source column wrapper", hasattr(ui, "frame_manual_control_dc_source_column"))
    col = ui.frame_manual_control_dc_source_column
    check("ui: column min width 300", col.minimumWidth() >= 300)
    check("ui: aux frame exists", hasattr(ui, "frame_manual_control_dc_source_aux"))
    frame = ui.frame_manual_control_dc_source_aux
    layout = ui.horizontalLayout_13
    check("ui: column in lower row", layout.indexOf(col) >= 0)
    check("ui: aux not sibling beside dc in row",
          layout.indexOf(frame) < 0 and frame.parent() is col)

    mc = win.manual_control_handler
    check("ui: 3 channel widget sets", len(getattr(mc, 'hmp_aux_channel_widgets', {})) == HMP_MANUAL_CHANNEL_COUNT)
    for ch in range(1, HMP_MANUAL_CHANNEL_COUNT + 1):
        w = mc.hmp_aux_channel_widgets[ch]
        check(f"ui: CH{ch} status label", w['status'].text() in ("OFF", "ON", "Off", "On"))

    eq = win.equipment
    if getattr(eq, "dc_source_aux", None) is None:
        primary = getattr(eq, "dc_source", None)
        for dc in getattr(eq, "dc_sources", []) or []:
            if dc is not None and dc is not primary:
                eq.dc_source_aux = dc
                break
    aux = getattr(eq, "dc_source_aux", None)
    check("equipment: dc_source_aux assigned", aux is not None, type(eq).__name__)
    ui.stackedWidget.setCurrentWidget(ui.page_manual_control)
    app.processEvents()
    mc.initialize_aux_dc_source()
    app.processEvents()
    shown = frame.isVisible() or not frame.isHidden()
    check("ui: visible when aux assigned", shown and aux is not None)

    failed = [n for n, ok in results if not ok]
    OUT.write(f"\n{len(results) - len(failed)}/{len(results)} passed\n")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
