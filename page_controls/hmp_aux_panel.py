"""Manual Control — HMP2030 auxiliary DC (3-channel card layout)."""
from __future__ import annotations

from functools import partial

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from equipment.dc_source import HMP_MANUAL_CHANNEL_COUNT
from page_controls import manual_control_theme as mc_theme
from page_controls.mc_value_box import make_value_box


class HmpAuxPanel:
    """Stacked channel cards: badge · V/I setpoints · Apply · OUT toggle."""

    def __init__(self, handler):
        self.handler = handler
        self.ui = handler.ui
        self.channel_widgets: dict = {}

    def install(self):
        ui = self.ui
        handler = self.handler
        frame = QFrame(ui.frame_manual_control_lower)
        frame.setObjectName("frame_manual_control_dc_source_aux")
        frame.setStyleSheet(mc_theme.hmp_aux_panel_style())
        frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        outer = QVBoxLayout(frame)
        outer.setContentsMargins(6, 6, 6, 4)
        outer.setSpacing(6)

        head = QWidget(frame)
        head_lay = QHBoxLayout(head)
        head_lay.setContentsMargins(0, 0, 0, 0)
        head_lay.setSpacing(6)
        title = QLabel("AUX DC", head)
        title.setObjectName("label_manual_control_dc_source_aux")
        title.setStyleSheet(mc_theme.section_title_style())
        title.setFont(mc_theme.label_font(10))
        sub = QLabel("HMP · bias rails", head)
        sub.setStyleSheet(mc_theme.field_label_style() + " border:none;")
        sub.setFont(mc_theme.label_font(9, bold=False))
        head_lay.addWidget(title, 0, Qt.AlignLeft | Qt.AlignVCenter)
        head_lay.addWidget(sub, 0, Qt.AlignLeft | Qt.AlignVCenter)
        head_lay.addStretch(1)
        outer.addWidget(head)

        btn_apply_style = mc_theme.hmp_aux_apply_button_style()
        row_h = 26

        for ch in range(1, HMP_MANUAL_CHANNEL_COUNT + 1):
            tile = QFrame(frame)
            tile.setObjectName(f"frame_hmp_aux_ch{ch}")
            tile.setStyleSheet(mc_theme.hmp_aux_channel_tile_style(ch))
            row = QHBoxLayout(tile)
            row.setContentsMargins(6, 4, 6, 4)
            row.setSpacing(8)

            badge = QLabel(f"CH{ch}", tile)
            badge.setAlignment(Qt.AlignCenter)
            badge.setFixedWidth(36)
            badge.setStyleSheet(
                f"color:{mc_theme.TEXT}; border:none; font-family:{mc_theme.FONT_TELEMETRY};"
                f" font-size:12px; font-weight:700;"
            )
            row.addWidget(badge, 0, Qt.AlignVCenter)

            v_wrap, le_v, _ = make_value_box(
                tile,
                unit="V",
                object_name=f"lineedit_manual_control_dc_aux_voltage_ch{ch}",
                default_text="0",
                validator=handler.validator,
                row_height=row_h,
            )
            i_wrap, le_i, _ = make_value_box(
                tile,
                unit="A",
                object_name=f"lineedit_manual_control_dc_aux_current_ch{ch}",
                default_text="1.0",
                validator=handler.validator,
                row_height=row_h,
            )
            row.addWidget(v_wrap, 1)
            row.addWidget(i_wrap, 1)

            actions = QWidget(tile)
            al = QVBoxLayout(actions)
            al.setContentsMargins(0, 0, 0, 0)
            al.setSpacing(3)
            btn_apply = QPushButton("Apply", actions)
            btn_apply.setObjectName(f"btn_manual_control_dc_aux_apply_ch{ch}")
            btn_apply.setStyleSheet(btn_apply_style)
            btn_apply.setFixedHeight(row_h)
            btn_apply.setToolTip("Apply V / I for this channel")
            btn_out = QPushButton("OFF", actions)
            btn_out.setObjectName(f"btn_manual_control_dc_aux_output_ch{ch}")
            btn_out.setCheckable(True)
            btn_out.setChecked(False)
            btn_out.setFixedHeight(row_h)
            btn_out.setToolTip("Toggle channel output")
            btn_out.setStyleSheet(mc_theme.aux_output_button_style(on=False))
            btn_out.setFont(mc_theme.telemetry_font(11))
            al.addWidget(btn_apply)
            al.addWidget(btn_out)
            row.addWidget(actions, 0, Qt.AlignTop)

            btn_apply.clicked.connect(partial(handler.aux_dc_apply_settings, ch))
            btn_out.toggled.connect(partial(handler._aux_dc_output_toggled, ch))

            self.channel_widgets[ch] = {
                "le_v": le_v,
                "le_i": le_i,
                "btn_apply": btn_apply,
                "apply_style": btn_apply_style,
                "output_btn": btn_out,
                "status": btn_out,
            }
            outer.addWidget(tile)

        w1 = self.channel_widgets[1]
        ui.lineedit_manual_control_dc_aux_voltage = w1["le_v"]
        ui.lineedit_manual_control_dc_aux_current = w1["le_i"]
        ui.label_manual_control_dc_aux_status = w1["output_btn"]
        ui.frame_manual_control_dc_aux_buttons = w1["output_btn"]
        ui.btn_manual_control_dc_aux_apply = frame.findChild(
            QPushButton, "btn_manual_control_dc_aux_apply_ch1"
        )
        ui.btn_manual_control_dc_aux_output = w1["output_btn"]
        ui.btn_manual_control_dc_aux_turn_on = w1["output_btn"]
        ui.btn_manual_control_dc_aux_turn_off = w1["output_btn"]

        ui.frame_manual_control_dc_source_aux = frame
        frame.setVisible(False)
        handler.hmp_aux_channel_widgets = self.channel_widgets
