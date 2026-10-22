"""SpaceX-inspired mission-control styling for Manual Equipment Control.

Principles: near-black canvas, flat panels, thin dividers, monospace telemetry,
ALL-CAPS section labels, minimal chrome, clear abort (red) / nominal (green) states.
"""
from __future__ import annotations

from PySide2.QtGui import QFont

# Palette (ground-control / telemetry)
BG_VOID = "#0a0a0c"
BG_PANEL = "#111114"
BG_TILE = "#141418"
BG_TILE_OFF = "#101012"
LINE = "#2a2a32"
LINE_DIM = "#1e1e24"
TEXT = "#e8e8ec"
TEXT_MUTED = "#7a7a88"
TEXT_LABEL = "#9a9aa8"
ACCENT = "#ffffff"
GO = "#4ade80"
WARN = "#fbbf24"
ABORT = "#dc2626"
ABORT_HOVER = "#ef4444"
SIM = "#93c5fd"

FONT_UI = '"Segoe UI", "Helvetica Neue", Arial, sans-serif'
FONT_TELEMETRY = '"Consolas", "Cascadia Mono", "Courier New", monospace'


def telemetry_font(point_size: int = 15, bold: bool = True) -> QFont:
    f = QFont("Consolas", point_size)
    f.setStyleHint(QFont.Monospace)
    f.setBold(bold)
    return f


def label_font(point_size: int = 10, bold: bool = True) -> QFont:
    f = QFont("Segoe UI", point_size)
    f.setBold(bold)
    f.setLetterSpacing(QFont.PercentageSpacing, 108)
    return f


def tile_style(object_name: str, *, assigned: bool = True, active: bool = False) -> str:
    bg = BG_TILE if assigned else BG_TILE_OFF
    border = f"border-left: 3px solid {GO};" if active else ""
    bottom = f"border-bottom: 1px solid {LINE};" if assigned else f"border-bottom: 1px dashed {LINE_DIM};"
    return (
        f"QFrame#{object_name}{{background-color:{bg}; border:none; {border} {bottom}}}"
    )


def strip_style() -> str:
    return (
        f"QFrame{{border:none; background:transparent; border-bottom:1px solid {LINE};}}"
        f"QLabel{{border:none; color:{TEXT}; font-family:{FONT_UI};}}"
    )


def header_bar_style(object_name: str = "label_manual_control") -> str:
    return (
        f"QFrame#{object_name}{{background-color:{BG_PANEL}; border:none;"
        f" border-bottom:1px solid {LINE};}}"
    )


def page_title_style() -> str:
    return (
        f"color:{ACCENT}; border:none; font-family:{FONT_UI}; font-size:13px;"
        f" font-weight:700; letter-spacing:2px;"
    )


def sim_banner_style() -> str:
    return (
        f"color:{SIM}; border:none; font-family:{FONT_UI}; font-size:10px;"
        f" font-weight:600; letter-spacing:1px;"
    )


def estop_style() -> str:
    return (
        f"QPushButton{{min-height:28px; max-height:32px; padding:4px 16px;"
        f" font-family:{FONT_UI}; font-size:11px; font-weight:700; letter-spacing:1px;"
        f" color:{ACCENT}; background-color:{ABORT}; border:1px solid {ABORT_HOVER};"
        f" border-radius:2px;}}"
        f" QPushButton:hover{{background-color:{ABORT_HOVER};}}"
        f" QPushButton:pressed{{background-color:#991b1b;}}"
    )


def flat_panel_style() -> str:
    return f"QFrame{{border:none; background-color:{BG_PANEL};}}"


def scope_panel_style(object_name: str = "frame_manual_control_oscilloscope") -> str:
    return (
        f"QFrame#{object_name}{{border:none; border-top:1px solid {LINE};"
        f" background-color:{BG_PANEL};}}"
        f" QLabel{{color:{TEXT_LABEL}; border:none; font-family:{FONT_UI}; font-size:10px;}}"
        f" QLineEdit, QComboBox{{background-color:{BG_VOID}; color:{TEXT};"
        f" font-family:{FONT_TELEMETRY}; border:1px solid {LINE}; border-radius:2px;"
        f" padding:2px 6px; min-height:22px;}}"
        f" QComboBox::drop-down{{border:none;}}"
    )


def gear_style() -> str:
    return (
        f"QToolButton{{border:none; color:{TEXT_MUTED}; font-size:15px;}}"
        f" QToolButton:hover{{color:{ACCENT};}}"
        f" QToolButton:disabled{{color:#404048;}}"
    )


def dialog_style() -> str:
    return (
        f"QDialog{{background-color:{BG_PANEL};}}"
        f" QLabel{{color:{TEXT}; font-family:{FONT_UI};}}"
        f" QPushButton{{color:{TEXT}; background-color:{BG_TILE}; border:1px solid {LINE};"
        f" border-radius:2px; padding:4px 14px; font-family:{FONT_UI};}}"
        f" QPushButton:hover{{background-color:#1c1c22; border-color:{TEXT_MUTED};}}"
    )


def header_strip_style(object_name: str) -> str:
    return (
        f"QFrame#{object_name}{{border:none; background:transparent;"
        f" border-bottom:1px solid {LINE};}}"
        f" QLabel{{border:none; color:{TEXT}; font-family:{FONT_UI};}}"
        f" QCheckBox{{color:{TEXT}; font-family:{FONT_UI}; font-size:10px;}}"
    )


def telemetry_label_style(*, accent: bool = False) -> str:
    color = GO if accent else TEXT
    return f"color:{color}; border:none; font-family:{FONT_TELEMETRY};"


def section_title_style() -> str:
    return (
        f"color:{TEXT_MUTED}; border:none; font-family:{FONT_UI}; font-size:10px;"
        f" font-weight:600; letter-spacing:1px;"
    )


def page_stylesheet() -> str:
    return (
        f"QWidget#page_manual_control{{background-color:{BG_VOID};}}"
        f" QScrollArea{{background-color:{BG_VOID}; border:none;}}"
        f" QWidget#widget_manual_control_equipment_scroll{{background-color:{BG_VOID};}}"
        f" QLabel{{color:{TEXT_LABEL};}}"
        f" QLineEdit, QComboBox, QSpinBox{{background-color:{BG_VOID}; color:{TEXT};"
        f" border:1px solid {LINE}; border-radius:2px; padding:2px 4px;}}"
        f" QPushButton{{background-color:{BG_TILE}; color:{TEXT}; border:1px solid {LINE};"
        f" border-radius:2px; padding:4px 10px; font-family:{FONT_UI}; font-size:10px;}}"
        f" QPushButton:hover{{border-color:{TEXT_MUTED}; background-color:#1a1a20;}}"
        f" QCheckBox{{color:{TEXT}; spacing:4px;}}"
    )


def apply_page_theme(handler) -> None:
    """Apply mission-control palette to the manual control page and key widgets."""
    ui = handler.ui
    ui.page_manual_control.setStyleSheet(page_stylesheet())
    scroll = getattr(ui, "scroll_manual_control_equipment", None)
    if scroll is not None:
        scroll.setStyleSheet(f"QScrollArea{{background:{BG_VOID}; border:none;}}")
        scroll.viewport().setStyleSheet(f"background:{BG_VOID};")

    title = getattr(ui, "label_2", None)
    if title is not None:
        title.setStyleSheet(page_title_style())

    sim = getattr(ui, "label_manual_control_simulation_banner", None)
    if sim is not None:
        sim.setStyleSheet(sim_banner_style())

    estop = getattr(handler, "btn_estop", None)
    if estop is not None:
        estop.setStyleSheet(estop_style())

    header = ui.label_manual_control
    header.setStyleSheet(header_bar_style(header.objectName()))

    for name in (
        "label_source_power_meter",
        "label_manual_control_ac_source",
        "label_manual_control_dc_source_aux",
    ):
        lbl = getattr(ui, name, None)
        if lbl is not None:
            lbl.setStyleSheet(section_title_style())

    eff = getattr(ui, "label_pml_total_eff", None)
    if eff is not None:
        eff.setStyleSheet(f"color:{GO}; border:none; font-weight:700;")

    from PySide2.QtWidgets import QLabel

    for lbl in ui.page_manual_control.findChildren(QLabel):
        name = lbl.objectName() or ""
        if "label_pms_display_" in name or "label_pml_display_" in name:
            lbl.setFont(telemetry_font(14))
            lbl.setStyleSheet(telemetry_label_style())
            lbl.setMaximumHeight(32)
            lbl.setMinimumHeight(24)
