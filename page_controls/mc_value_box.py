"""Compact setpoint field: optional caption + numeric entry + unit inside one bordered box."""
from __future__ import annotations

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QWidget

from page_controls import manual_control_theme as mc_theme


def make_value_box(
    parent: QWidget,
    *,
    unit: str,
    object_name: str,
    default_text: str,
    validator,
    caption: str | None = None,
    row_height: int = 26,
    edit_font_pt: int = 12,
    unit_font_pt: int = 11,
    caption_font_pt: int = 10,
    max_width: int | None = None,
) -> tuple[QFrame, QLineEdit, QLabel]:
    """Return (frame, line_edit, unit_label). Unit is separate so callers can change V ↔ A."""
    box = QFrame(parent)
    box.setStyleSheet(mc_theme.hmp_aux_value_box_style())
    hl = QHBoxLayout(box)
    hl.setContentsMargins(6, 0, 4, 0)
    hl.setSpacing(4)

    if caption:
        cap = QLabel(caption, box)
        cap.setStyleSheet(mc_theme.hmp_aux_caption_style())
        cap.setFont(mc_theme.label_font(caption_font_pt, bold=False))
        hl.addWidget(cap, 0, Qt.AlignVCenter)

    le = QLineEdit(box)
    le.setObjectName(object_name)
    le.setText(default_text)
    le.setFixedHeight(row_height)
    le.setValidator(validator)
    le.setStyleSheet(mc_theme.hmp_aux_value_edit_style())
    le.setFont(mc_theme.input_font(edit_font_pt))

    unit_lbl = QLabel(unit, box)
    unit_lbl.setStyleSheet(mc_theme.hmp_aux_value_unit_style())
    unit_lbl.setFont(mc_theme.input_font(unit_font_pt, bold=True))

    hl.addWidget(le, 1)
    hl.addWidget(unit_lbl, 0, Qt.AlignVCenter)

    if max_width is not None:
        box.setMaximumWidth(max_width)

    return box, le, unit_lbl
