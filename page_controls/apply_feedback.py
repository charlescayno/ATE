"""Brief green 'Applied' flash on Manual Control action buttons."""
from __future__ import annotations

from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QPushButton

from page_controls import manual_control_theme as mc_theme

APPLY_FEEDBACK_MS = 500


def flash_apply_button(
    btn: QPushButton | None,
    *,
    ok_text: str = "Applied",
    restore_text: str | None = None,
    base_style: str | None = None,
) -> None:
    if btn is None:
        return
    label = restore_text if restore_text is not None else btn.text()
    style = base_style
    if style is None:
        style = btn.property("_mc_apply_base_style")
    if not style:
        style = btn.styleSheet()
        btn.setProperty("_mc_apply_base_style", style)
    btn.setText(ok_text)
    btn.setStyleSheet(mc_theme.apply_ok_button_style())
    btn.setEnabled(False)

    def restore() -> None:
        btn.setText(label)
        btn.setStyleSheet(style)
        btn.setEnabled(True)

    QTimer.singleShot(APPLY_FEEDBACK_MS, restore)
