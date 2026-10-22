"""SpaceX-inspired mission-control styling for Manual Equipment Control.

Principles: near-black canvas, flat panels, thin dividers, monospace telemetry,
ALL-CAPS section labels, minimal chrome, clear abort (red) / nominal (green) states.
"""
from __future__ import annotations

import re

from PySide2.QtGui import QFont

_ELOAD_SECTION = re.compile(r"^label_manual_control_eload(_\d+)?$")
_LOAD_PM_SECTION = re.compile(r"^label_load_power_meter(_\d+)?$")

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

# Readable mission-control sizes (Manual Equipment Control)
PT_UI = 11
PT_SECTION = 11
PT_TELEMETRY = 18
PT_TELEMETRY_STRIP = 14
PT_INPUT = 12
PT_COMBO = 12
PT_FIELD = 10


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


def input_font(point_size: int = 10, bold: bool = False) -> QFont:
    f = QFont("Consolas", point_size)
    f.setStyleHint(QFont.Monospace)
    f.setBold(bold)
    return f


def field_label_style() -> str:
    return (
        f"color:{TEXT_LABEL}; border:none; font-family:{FONT_UI}; font-size:9px;"
        f" font-weight:600;"
    )


def input_style() -> str:
    return (
        f"background-color:{BG_VOID}; color:{TEXT}; font-family:{FONT_TELEMETRY};"
        f" font-size:11px; border:1px solid {LINE}; border-radius:2px; padding:2px 4px;"
    )


def compact_button_style() -> str:
    return (
        f"background-color:{BG_TILE}; color:{TEXT}; border:1px solid {LINE};"
        f" border-radius:2px; padding:2px 6px; font-family:{FONT_UI}; font-size:10px;"
        f" font-weight:600; min-height:22px; max-height:26px;"
    )


def aux_output_button_style(*, on: bool) -> str:
    """Single HMP channel output toggle — green when ON, muted when OFF."""
    if on:
        return (
            f"QPushButton{{background-color:#14532d; color:{GO}; border:1px solid {GO};"
            f" border-radius:2px; padding:2px 10px; font-family:{FONT_TELEMETRY};"
            f" font-size:11px; font-weight:700; min-height:22px; max-height:26px;"
            f" min-width:44px;}}"
            f" QPushButton:hover{{background-color:#166534;}}"
            f" QPushButton:pressed{{background-color:#15803d;}}"
        )
    return (
        f"QPushButton{{background-color:{BG_TILE}; color:{TEXT_MUTED}; border:1px solid {LINE};"
        f" border-radius:2px; padding:2px 10px; font-family:{FONT_TELEMETRY};"
        f" font-size:11px; font-weight:700; min-height:22px; max-height:26px;"
        f" min-width:44px;}}"
        f" QPushButton:hover{{border-color:{TEXT_MUTED}; color:{TEXT};}}"
    )


def _is_telemetry_label(name: str) -> bool:
    if not name:
        return False
    if "_display_" in name:
        return True
    if name.startswith("label_pml_total_") and name != "label_pml_total_eff":
        return True
    if "label_manual_control_dc_aux_status_ch" in name:
        return True
    return False


def _is_section_title(name: str) -> bool:
    if name in (
        "label_manual_control_ac_source",
        "label_manual_control_dc_source_aux",
        "label_source_power_meter",
        "label_2",
    ):
        return True
    if _LOAD_PM_SECTION.match(name) or _ELOAD_SECTION.match(name):
        return True
    return False


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


def hmp_aux_panel_style() -> str:
    return (
        f"QFrame#frame_manual_control_dc_source_aux{{background-color:{BG_PANEL};"
        f" border:none; border-top:1px solid {LINE};}}"
    )


def hmp_aux_channel_tile_style(channel: int) -> str:
    accent = {1: GO, 2: SIM, 3: WARN}.get(channel, LINE)
    return (
        f"QFrame#frame_hmp_aux_ch{channel}{{background-color:{BG_TILE}; border:none;"
        f" border-left:3px solid {accent}; border-radius:2px;}}"
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


def safety_dialog_style() -> str:
    return (
        f"QDialog{{background-color:{BG_PANEL}; font-family:{FONT_UI}; border:1px solid {LINE};}}"
    )


def safety_dialog_tag_style() -> str:
    return (
        f"color:{WARN}; border:none; font-family:{FONT_UI}; font-size:10px;"
        f" font-weight:700; letter-spacing:3px;"
    )


def safety_dialog_title_style() -> str:
    return (
        f"color:{ACCENT}; border:none; font-family:{FONT_UI}; font-size:16px;"
        f" font-weight:700; letter-spacing:0.5px;"
    )


def safety_dialog_question_style() -> str:
    return (
        f"color:{TEXT}; border:none; font-family:{FONT_UI}; font-size:13px;"
        f" font-weight:600;"
    )


def safety_dialog_detail_style() -> str:
    return (
        f"color:{TEXT_MUTED}; border:none; font-family:{FONT_UI}; font-size:11px;"
        f" line-height:140%;"
    )


def safety_dialog_confirm_button_style() -> str:
    return (
        f"QPushButton{{min-height:32px; padding:6px 18px; font-family:{FONT_UI};"
        f" font-size:11px; font-weight:700; letter-spacing:0.5px; color:{BG_VOID};"
        f" background-color:{GO}; border:1px solid {GO}; border-radius:2px;}}"
        f" QPushButton:hover{{background-color:#6ee7a0; border-color:#6ee7a0;}}"
        f" QPushButton:pressed{{background-color:#22c55e;}}"
    )


def safety_dialog_cancel_button_style() -> str:
    return (
        f"QPushButton{{min-height:32px; padding:6px 18px; font-family:{FONT_UI};"
        f" font-size:11px; font-weight:600; color:{TEXT}; background-color:{BG_TILE};"
        f" border:1px solid {LINE}; border-radius:2px; margin-right:8px;}}"
        f" QPushButton:hover{{background-color:#1c1c22; border-color:{TEXT_MUTED};}}"
    )


def dialog_style() -> str:
    return (
        f"QDialog{{background-color:{BG_PANEL}; font-family:{FONT_UI};}}"
        f" QLabel{{color:{TEXT}; font-family:{FONT_UI}; font-size:10px;}}"
        f" QLineEdit, QComboBox, QSpinBox{{background-color:{BG_VOID}; color:{TEXT};"
        f" font-family:{FONT_TELEMETRY}; font-size:11px; border:1px solid {LINE};"
        f" border-radius:2px; padding:2px 4px;}}"
        f" QPushButton{{color:{TEXT}; background-color:{BG_TILE}; border:1px solid {LINE};"
        f" border-radius:2px; padding:4px 14px; font-family:{FONT_UI}; font-size:10px;"
        f" font-weight:600;}}"
        f" QPushButton:hover{{background-color:#1c1c22; border-color:{TEXT_MUTED};}}"
    )


def header_strip_style(object_name: str) -> str:
    return (
        f"QFrame#{object_name}{{border:none; background:transparent;"
        f" border-bottom:1px solid {LINE};}}"
        f" QLabel{{border:none; color:{TEXT}; font-family:{FONT_UI};}}"
        f" QCheckBox{{color:{TEXT}; font-family:{FONT_UI}; font-size:10px;}}"
    )


def telemetry_label_style(*, accent: bool = False, point_size: int = PT_TELEMETRY) -> str:
    color = GO if accent else TEXT
    return (
        f"color:{color}; border:none; font-family:{FONT_TELEMETRY};"
        f" font-size:{point_size}px; font-weight:600;"
    )


def section_title_style() -> str:
    return (
        f"color:{TEXT_MUTED}; border:none; font-family:{FONT_UI}; font-size:{PT_SECTION}px;"
        f" font-weight:600; letter-spacing:1px;"
    )


def page_stylesheet() -> str:
    return (
        f"QWidget#page_manual_control{{background-color:{BG_VOID}; font-family:{FONT_UI};"
        f" font-size:{PT_UI}px;}}"
        f" QScrollArea{{background-color:{BG_VOID}; border:none;}}"
        f" QWidget#widget_manual_control_equipment_scroll{{background-color:{BG_VOID};}}"
        f" QLabel{{color:{TEXT_LABEL}; font-family:{FONT_UI}; font-size:{PT_UI}px;}}"
        f" QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox{{background-color:{BG_VOID};"
        f" color:{TEXT}; font-family:{FONT_TELEMETRY}; font-size:{PT_INPUT}px;"
        f" border:1px solid {LINE}; border-radius:2px; padding:3px 6px; min-height:26px;}}"
        f" QComboBox QAbstractItemView{{background-color:{BG_PANEL}; color:{TEXT};"
        f" font-family:{FONT_TELEMETRY}; selection-background-color:#1c1c22;}}"
        f" QPushButton{{background-color:{BG_TILE}; color:{TEXT}; border:1px solid {LINE};"
        f" border-radius:2px; padding:4px 10px; font-family:{FONT_UI}; font-size:{PT_UI}px;"
        f" font-weight:600; min-height:26px;}}"
        f" QPushButton:hover{{border-color:{TEXT_MUTED}; background-color:#1a1a20;}}"
        f" QCheckBox{{color:{TEXT}; spacing:4px; font-family:{FONT_UI}; font-size:{PT_UI}px;}}"
        f" QToolButton{{font-family:{FONT_UI};}}"
    )


def apply_page_fonts(handler) -> None:
    """Set QFont on manual-control widgets so legacy .ui font roles do not win."""
    from PySide2.QtWidgets import (
        QCheckBox,
        QComboBox,
        QDoubleSpinBox,
        QLabel,
        QLineEdit,
        QPushButton,
        QSpinBox,
        QWidget,
    )

    ui = handler.ui
    roots = [ui.page_manual_control]
    for panel_name in ("pml_grid", "pms_panel", "eload_grid", "scope_panel"):
        panel = getattr(handler, panel_name, None)
        if panel is None:
            continue
        dlg = getattr(panel, "dialog", None)
        if dlg is not None:
            roots.append(dlg)
        dialogs = getattr(panel, "dialogs", None)
        if isinstance(dialogs, dict):
            roots.extend(dialogs.values())

    seen = set()

    def walk(root: QWidget):
        if root is None or id(root) in seen:
            return
        seen.add(id(root))

        for lbl in root.findChildren(QLabel):
            name = lbl.objectName() or ""
            if _is_telemetry_label(name):
                if name.startswith("label_pml_total_"):
                    lbl.setFont(telemetry_font(PT_TELEMETRY_STRIP))
                    lbl.setStyleSheet(
                        telemetry_label_style(
                            accent="total_eff" in name, point_size=PT_TELEMETRY_STRIP
                        )
                    )
                else:
                    lbl.setFont(telemetry_font(PT_TELEMETRY))
                    if "total_eff" not in name:
                        lbl.setStyleSheet(telemetry_label_style())
            elif _is_section_title(name):
                lbl.setFont(label_font(PT_SECTION))
                if name != "label_2":
                    lbl.setStyleSheet(section_title_style())
            elif name.startswith("label_"):
                lbl.setFont(label_font(PT_FIELD, bold=False))

        for w in root.findChildren(QLineEdit):
            w.setFont(input_font(PT_INPUT))
        for w in root.findChildren(QComboBox):
            w.setFont(input_font(PT_COMBO))
        for spin_type in (QSpinBox, QDoubleSpinBox):
            for w in root.findChildren(spin_type):
                w.setFont(input_font(PT_COMBO))
        for w in root.findChildren(QPushButton):
            if w.objectName() == "btn_manual_control_estop":
                continue
            w.setFont(label_font(PT_UI, bold=True))
        for w in root.findChildren(QCheckBox):
            w.setFont(label_font(PT_UI, bold=False))

    ui.page_manual_control.setFont(label_font(PT_UI, bold=False))
    for r in roots:
        walk(r)

    eff = getattr(ui, "label_pml_total_eff", None)
    if eff is not None:
        eff.setFont(telemetry_font(PT_TELEMETRY_STRIP, bold=True))
        eff.setStyleSheet(
            telemetry_label_style(accent=True, point_size=PT_TELEMETRY_STRIP)
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

    apply_page_fonts(handler)

    from PySide2.QtWidgets import QLabel

    for lbl in ui.page_manual_control.findChildren(QLabel):
        name = lbl.objectName() or ""
        if "label_pms_display_" in name or "label_pml_display_" in name:
            lbl.setMaximumHeight(40)
            lbl.setMinimumHeight(30)


def remove_display_select_column(select_frame):
    """Remove legacy per-row PM display selector combos (chevron column)."""
    from PySide2.QtWidgets import QFrame

    if not isinstance(select_frame, QFrame):
        return
    select_frame.hide()
    parent = select_frame.parentWidget()
    if parent is not None:
        lay = parent.layout()
        if lay is not None:
            lay.removeWidget(select_frame)
