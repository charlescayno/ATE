"""Manual Control source power meter — compact readouts, settings in gear dialog."""
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QDialog, QFrame, QHBoxLayout, QPushButton, QSizePolicy,
                               QToolButton, QVBoxLayout, QWidget)

from page_controls import manual_control_theme as mc_theme

GEAR_STYLE = mc_theme.gear_style()
DIALOG_STYLE = mc_theme.dialog_style()


class PmsSettingsDialog(QDialog):
    def __init__(self, parent, control_frame: QFrame):
        super().__init__(parent)
        self.setWindowTitle("Source Power Meter Settings")
        self.setStyleSheet(DIALOG_STYLE)
        lay = QVBoxLayout(self)
        control_frame.setParent(self)
        lay.addWidget(control_frame)
        control_frame.show()
        btn = QPushButton("Close", self)
        btn.clicked.connect(self.close)
        lay.addWidget(btn, 0, Qt.AlignRight)


class PmsPanel:
    def __init__(self, handler):
        self.handler = handler
        self.ui = handler.ui
        self.dialog = None
        self.gear = None
        self._build()

    def _build(self):
        ui = self.ui
        tile = ui.frame_manual_control_pms
        tile.setMinimumSize(0, 0)
        tile.setMaximumWidth(560)
        tile.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        tile.setStyleSheet(mc_theme.tile_style(tile.objectName(), assigned=True))

        layout = ui.verticalLayout_17
        layout.removeWidget(ui.label_source_power_meter)

        header = QWidget(tile)
        hl = QHBoxLayout(header)
        hl.setContentsMargins(4, 0, 4, 0)
        ui.label_source_power_meter.setParent(header)
        ui.label_source_power_meter.setText("SOURCE PM")
        ui.label_source_power_meter.setStyleSheet(mc_theme.section_title_style())
        ui.label_source_power_meter.setFont(mc_theme.label_font(mc_theme.PT_SECTION))
        ui.label_source_power_meter.setMaximumHeight(16777215)
        hl.addWidget(ui.label_source_power_meter, 1)

        gear = QToolButton(header)
        gear.setObjectName("btn_pms_settings")
        gear.setText("⚙")
        gear.setToolTip("Range / integration / averaging / mode settings")
        gear.setStyleSheet(GEAR_STYLE)
        gear.setCursor(Qt.PointingHandCursor)
        gear.clicked.connect(self.open_settings)
        hl.addWidget(gear)
        layout.insertWidget(0, header)
        layout.setContentsMargins(4, 2, 4, 4)
        layout.setSpacing(1)
        self.gear = gear
        ui.btn_pms_settings = gear

        contents = ui.frame_pms_contents
        contents.setMinimumHeight(0)
        ui.frame_pms_display.setMinimumSize(0, 0)
        ui.frame_pms_display.setMaximumWidth(16777215)
        ui.frame_pms_display.setStyleSheet("border:none;")
        for lbl in (
            ui.label_pms_display_a,
            ui.label_pms_display_b,
            ui.label_pms_display_c,
            ui.label_pms_display_d,
        ):
            lbl.setFont(mc_theme.telemetry_font(mc_theme.PT_TELEMETRY))
            lbl.setStyleSheet(mc_theme.telemetry_label_style())
            lbl.setMinimumHeight(30)
            lbl.setMaximumHeight(40)
        ui.frame_pms_display_select.setMaximumWidth(92)
        for cbx in (
            ui.cbx_pms_display_a,
            ui.cbx_pms_display_b,
            ui.cbx_pms_display_c,
            ui.cbx_pms_display_d,
        ):
            cbx.setMinimumHeight(28)
            cbx.setMaximumHeight(34)
            cbx.setFont(mc_theme.input_font(mc_theme.PT_COMBO))

        self.dialog = PmsSettingsDialog(self.handler.parent, ui.frame_pms_control)

    def open_settings(self):
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()

    def dialog_state_widgets(self):
        from PySide2.QtWidgets import QCheckBox, QComboBox, QLineEdit

        found = []
        for t in (QLineEdit, QComboBox, QCheckBox):
            found += [x for x in self.dialog.findChildren(t) if x.objectName()]
        return found
