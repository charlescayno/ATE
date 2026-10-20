"""Advanced scope / timing settings for Steady-State Waveform 2 Port — opened from a gear button."""
from PySide2.QtCore import Qt
from PySide2.QtGui import QDoubleValidator
from PySide2.QtWidgets import (
    QComboBox, QDialog, QDialogButtonBox, QFormLayout, QLabel, QLineEdit, QVBoxLayout,
)

DIALOG_STYLE = (
    "QDialog{background-color: rgb(40,44,52);}"
    "QLabel{color: rgb(210,210,210);}"
    "QLineEdit, QComboBox{color: white; background-color: rgb(52,59,72); border: 1px solid rgb(80,90,110);"
    " border-radius: 4px; padding: 4px; min-height: 24px;}"
    "QPushButton{color: white; background-color: rgb(52,59,72); border: 1px solid rgb(80,90,110);"
    " border-radius: 5px; padding: 4px 14px;}"
    "QPushButton:hover{background-color: rgb(61,70,86);}"
)


def _enabled_trigger_channels(scope_channels: dict) -> list[int]:
    if not scope_channels:
        return [1, 2, 3, 4]
    enabled = []
    for ch in (1, 2, 3, 4):
        data = scope_channels.get(ch) or scope_channels.get(str(ch)) or {}
        if data.get('enabled', ch <= 2):
            enabled.append(ch)
    return enabled or [1]


class Eff2PWaveformAdvancedDialog(QDialog):
    """Edits hidden i2c lineedits 5–10 (and optional ambient on test conditions)."""

    PARAM_INDICES = {
        'trigger_delta': 4,
        'settle_time': 5,
        'discharge_pulses': 6,
        'ambient_temp': 7,
        'post_capture_delay': 8,
        'trigger_channel': 9,
    }

    def __init__(self, parent, lineedits, scope_channels=None, ambient_lineedit=None):
        super().__init__(parent)
        self.lineedits = lineedits
        self.ambient_lineedit = ambient_lineedit
        self.setWindowTitle("Scope & timing (advanced)")
        self.setStyleSheet(DIALOG_STYLE)
        self.setMinimumWidth(360)

        form = QFormLayout()
        validator = QDoubleValidator(-1e6, 1e6, 6, self)
        validator.setNotation(QDoubleValidator.StandardNotation)

        self.le_trigger_delta = QLineEdit(self)
        self.le_settle = QLineEdit(self)
        self.le_discharge = QLineEdit(self)
        self.le_ambient = QLineEdit(self)
        self.le_post_delay = QLineEdit(self)
        self.cbx_trigger = QComboBox(self)

        for le in (self.le_trigger_delta, self.le_settle, self.le_discharge, self.le_ambient, self.le_post_delay):
            le.setValidator(validator)

        chs = _enabled_trigger_channels(scope_channels or {})
        self.cbx_trigger.addItems([f"CH{n}" for n in chs])

        form.addRow("Trigger Delta (V):", self.le_trigger_delta)
        form.addRow("Settle Time (s):", self.le_settle)
        form.addRow("Discharge Pulses:", self.le_discharge)
        form.addRow("Ambient Temp (°C):", self.le_ambient)
        form.addRow("Post-Capture Delay (s):", self.le_post_delay)
        form.addRow("Trigger Channel:", self.cbx_trigger)

        hint = QLabel(
            "Stop Test always runs a safety discharge at 1.0 A CCH "
            "(≥2 pulses, or more if Discharge Pulses is higher)."
        )
        hint.setWordWrap(True)
        hint.setStyleSheet("color: rgb(150, 170, 190); font-size: 11px;")

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        root = QVBoxLayout(self)
        root.addLayout(form)
        root.addWidget(hint)
        root.addWidget(buttons)

        self._load_from_lineedits()

    def _load_from_lineedits(self):
        def txt(idx, default=""):
            if idx < len(self.lineedits):
                t = self.lineedits[idx].text().strip()
                return t if t else default
            return default

        self.le_trigger_delta.setText(txt(self.PARAM_INDICES['trigger_delta'], "0.5"))
        self.le_settle.setText(txt(self.PARAM_INDICES['settle_time'], "1.0"))
        self.le_discharge.setText(txt(self.PARAM_INDICES['discharge_pulses'], "2"))
        amb = txt(self.PARAM_INDICES['ambient_temp'], "25")
        if self.ambient_lineedit and self.ambient_lineedit.text().strip():
            amb = self.ambient_lineedit.text().strip()
        self.le_ambient.setText(amb)
        self.le_post_delay.setText(txt(self.PARAM_INDICES['post_capture_delay'], "1.0"))

        ch_txt = txt(self.PARAM_INDICES['trigger_channel'], "1")
        try:
            ch_num = int(float(ch_txt))
        except (ValueError, TypeError):
            ch_num = 1
        want = f"CH{ch_num}"
        idx = self.cbx_trigger.findText(want)
        self.cbx_trigger.setCurrentIndex(idx if idx >= 0 else 0)

    def apply_to_lineedits(self):
        def set_txt(idx, value):
            if idx < len(self.lineedits):
                self.lineedits[idx].setText(str(value))

        set_txt(self.PARAM_INDICES['trigger_delta'], self.le_trigger_delta.text().strip() or "0.5")
        set_txt(self.PARAM_INDICES['settle_time'], self.le_settle.text().strip() or "1.0")
        set_txt(self.PARAM_INDICES['discharge_pulses'], self.le_discharge.text().strip() or "0")
        amb = self.le_ambient.text().strip() or "25"
        set_txt(self.PARAM_INDICES['ambient_temp'], amb)
        if self.ambient_lineedit is not None:
            self.ambient_lineedit.setText(amb)
        set_txt(self.PARAM_INDICES['post_capture_delay'], self.le_post_delay.text().strip() or "1.0")
        ch = self.cbx_trigger.currentText().replace("CH", "")
        set_txt(self.PARAM_INDICES['trigger_channel'], ch or "1")
