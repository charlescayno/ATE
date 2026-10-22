"""Mission-control styled safety confirmation dialogs."""
import os

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from page_controls import manual_control_theme as mc


def confirm_discharge_resistor_disengaged(parent) -> bool:
    """Return True if the operator confirms the discharge resistor is disengaged."""
    if os.environ.get("PI_ATE_AUTO_CONFIRM") == "1":
        return True
    return DischargeResistorDialog(parent).exec_() == QDialog.Accepted


class DischargeResistorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Discharge Resistor Check")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setStyleSheet(mc.safety_dialog_style())
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        accent = QWidget(self)
        accent.setFixedWidth(4)
        accent.setStyleSheet(f"background-color:{mc.WARN};")
        root.addWidget(accent)

        body = QVBoxLayout()
        body.setContentsMargins(24, 22, 24, 20)
        body.setSpacing(10)

        tag = QLabel("SAFETY CHECK")
        tag.setStyleSheet(mc.safety_dialog_tag_style())
        body.addWidget(tag)

        title = QLabel("Discharge resistor must be disengaged")
        title.setWordWrap(True)
        title.setStyleSheet(mc.safety_dialog_title_style())
        body.addWidget(title)

        question = QLabel(
            "Is the discharge resistor fully disconnected from the DUT?"
        )
        question.setWordWrap(True)
        question.setStyleSheet(mc.safety_dialog_question_style())
        body.addWidget(question)

        detail = QLabel(
            "Do not enable the DC source until the bench is safe. "
            "Confirm only after you have physically removed or switched out "
            "the discharge path."
        )
        detail.setWordWrap(True)
        detail.setStyleSheet(mc.safety_dialog_detail_style())
        body.addWidget(detail)

        body.addSpacing(10)
        btn_row = QHBoxLayout()
        btn_row.addStretch(1)
        cancel = QPushButton("Cancel")
        cancel.setStyleSheet(mc.safety_dialog_cancel_button_style())
        cancel.clicked.connect(self.reject)
        confirm = QPushButton("Disengaged — continue")
        confirm.setStyleSheet(mc.safety_dialog_confirm_button_style())
        confirm.setDefault(True)
        confirm.setAutoDefault(True)
        confirm.clicked.connect(self.accept)
        btn_row.addWidget(cancel)
        btn_row.addWidget(confirm)
        body.addLayout(btn_row)

        wrap = QWidget(self)
        wrap.setLayout(body)
        root.addWidget(wrap, 1)
