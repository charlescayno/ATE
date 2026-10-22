"""Gear dialog: auto-find trigger tuning (delta, settle times)."""
from PySide2.QtCore import Qt
from PySide2.QtGui import QDoubleValidator, QIntValidator
from PySide2.QtWidgets import (
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from equipment.scope_auto_trigger import AutoFindTriggerSettings
from page_controls import manual_control_theme as mc_theme


class ScopeAutoFindSettingsDialog(QDialog):
    def __init__(self, parent, settings: AutoFindTriggerSettings):
        super().__init__(parent)
        self.setWindowTitle("Auto-find trigger")
        self.setStyleSheet(mc_theme.dialog_style())
        self.setMinimumWidth(340)
        self._settings = settings

        root = QVBoxLayout(self)
        hint = QLabel(
            "Sweep trigger level using the selected source channel and edge. "
            "Increase delta for faster/coarser search; adjust settle times for noisy signals.",
            self,
        )
        hint.setWordWrap(True)
        hint.setStyleSheet(mc_theme.field_label_style() + " border:none;")
        root.addWidget(hint)

        form = QFormLayout()
        dbl = QDoubleValidator(0.001, 100.0, 6, self)
        dbl.setNotation(QDoubleValidator.StandardNotation)
        int_v = QIntValidator(1, 100, self)

        self.le_delta = QLineEdit(self)
        self.le_delta.setValidator(dbl)
        self.le_auto_settle = QLineEdit(self)
        self.le_auto_settle.setValidator(dbl)
        self.le_step_settle = QLineEdit(self)
        self.le_step_settle.setValidator(dbl)
        self.le_final_settle = QLineEdit(self)
        self.le_final_settle.setValidator(dbl)
        self.le_max_steps = QLineEdit(self)
        self.le_max_steps.setValidator(int_v)

        form.addRow("Trigger delta (V):", self.le_delta)
        form.addRow("Auto / NORM settle (s):", self.le_auto_settle)
        form.addRow("Step settle (s):", self.le_step_settle)
        form.addRow("Final settle (s):", self.le_final_settle)
        form.addRow("Max steps:", self.le_max_steps)
        root.addLayout(form)

        btn_row = QPushButton("Close", self)
        btn_row.clicked.connect(self._accept_and_save)
        btn_row.setStyleSheet(mc_theme.compact_button_style())
        root.addWidget(btn_row, 0, Qt.AlignRight)

        self._load_from_settings()

    def _accept_and_save(self):
        self.apply_to_settings()
        self.accept()

    def _load_from_settings(self):
        s = self._settings
        self.le_delta.setText(f"{s.trigger_delta:g}")
        self.le_auto_settle.setText(f"{s.auto_settle_s:g}")
        self.le_step_settle.setText(f"{s.step_settle_s:g}")
        self.le_final_settle.setText(f"{s.final_settle_s:g}")
        self.le_max_steps.setText(str(s.max_steps))

    def apply_to_settings(self) -> AutoFindTriggerSettings:
        s = self._settings

        def _f(le, default):
            try:
                return float(le.text().strip())
            except ValueError:
                return default

        s.trigger_delta = _f(self.le_delta, s.trigger_delta)
        s.auto_settle_s = _f(self.le_auto_settle, s.auto_settle_s)
        s.step_settle_s = _f(self.le_step_settle, s.step_settle_s)
        s.final_settle_s = _f(self.le_final_settle, s.final_settle_s)
        try:
            s.max_steps = int(self.le_max_steps.text().strip())
        except ValueError:
            pass
        return s
