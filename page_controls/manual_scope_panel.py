"""Oscilloscope controls at bottom of Manual Equipment Control page."""
from __future__ import annotations

import os
import re
from typing import TYPE_CHECKING

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from equipment.oscilloscope_specs import LeCroyOscilloscope, RohdeSchwarzOscilloscope, TriggerMode
from equipment.scope_auto_trigger import AutoFindTriggerSettings, find_trigger_level
from page_controls import manual_control_theme as mc_theme
from page_controls.scope_auto_find_dialog import ScopeAutoFindSettingsDialog
from psu_tests.definitions import MessageType

if TYPE_CHECKING:
    from page_controls.manual_control import ManualControlPageHandler

PANEL_STYLE = mc_theme.scope_panel_style()

TRIGGER_MODES = ("Auto", "Normal", "Freerun")
TRIGGER_CHANNELS = ("CH1", "CH2", "CH3", "CH4")
TRIGGER_EDGES = ("Rising", "Falling", "Either")
TRIGGER_EDGE_SCPI = {"Rising": "POS", "Falling": "NEG", "Either": "EITH"}


class TriggerLevelEdit(QLineEdit):
    """Trigger level field — mouse wheel adjusts volts (WheelFocus, like legacy scope UI)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFocusPolicy(Qt.WheelFocus)
        self.setToolTip(
            "Scroll to change level (V). Ctrl: fine 0.01 V · Shift: coarse 1 V · default 0.1 V"
        )
        self._wheel_apply_callback = None

    def set_wheel_apply_callback(self, callback):
        self._wheel_apply_callback = callback

    def _step_for_event(self, event) -> float:
        mods = event.modifiers()
        if mods & Qt.ControlModifier:
            return 0.01
        if mods & Qt.ShiftModifier:
            return 1.0
        return 0.1

    def wheelEvent(self, event):
        delta_y = event.angleDelta().y()
        if delta_y == 0:
            return
        step = self._step_for_event(event)
        try:
            val = float(self.text().strip())
        except ValueError:
            val = 0.0
        val += step if delta_y > 0 else -step
        val = max(-50.0, min(50.0, val))
        text = f"{val:.4f}".rstrip("0").rstrip(".")
        self.setText(text)
        event.accept()
        if self._wheel_apply_callback is not None:
            self._wheel_apply_callback()


class ManualScopePanel:
    def __init__(self, handler: "ManualControlPageHandler"):
        self.handler = handler
        self.ui = handler.ui
        self._default_capture_dir = os.path.join(
            os.path.expanduser("~"), "Documents", "PI_ATE", "manual_waveforms")
        self.auto_find_settings = AutoFindTriggerSettings()
        self._auto_find_running = False
        self._build()
        self._bind()

    def _build(self):
        ui = self.ui
        page = ui.page_manual_control
        frame = QFrame(page)
        frame.setObjectName("frame_manual_control_oscilloscope")
        frame.setStyleSheet(PANEL_STYLE)
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        outer = QVBoxLayout(frame)
        outer.setContentsMargins(8, 6, 8, 8)
        outer.setSpacing(4)

        btn_style = ui.btn_manual_control_ac_source_turn_on.styleSheet()
        compact = btn_style + " QPushButton { min-height: 24px; max-height: 26px; padding: 2px 10px; font-size: 10px; }"
        lbl_style = "color: rgb(190,190,190); font-size: 10px; border: none;"

        self.header_widget = QWidget(frame)
        header = QHBoxLayout(self.header_widget)
        header.setContentsMargins(0, 0, 0, 0)
        self.btn_collapse = QToolButton(self.header_widget)
        self.btn_collapse.setCheckable(True)
        self.btn_collapse.setChecked(True)
        self.btn_collapse.setText("▼")
        self.btn_collapse.setToolTip("Collapse / expand oscilloscope panel")
        self.btn_collapse.setStyleSheet(mc_theme.gear_style())
        header.addWidget(self.btn_collapse)
        title = QLabel("OSCILLOSCOPE", self.header_widget)
        title.setStyleSheet(mc_theme.section_title_style())
        title.setFont(mc_theme.label_font(11))
        header.addWidget(title)
        self.label_status = QLabel("—", self.header_widget)
        self.label_status.setStyleSheet(
            f"color:{mc_theme.TEXT_MUTED}; border:none; font-family:{mc_theme.FONT_TELEMETRY};"
            f" font-size:10px; font-weight:600;")
        header.addWidget(self.label_status)
        header.addStretch(1)

        self.btn_run = QPushButton("Run", self.header_widget)
        self.btn_run_single = QPushButton("Run Single", self.header_widget)
        self.btn_stop = QPushButton("Stop", self.header_widget)
        for btn in (self.btn_run, self.btn_run_single, self.btn_stop):
            btn.setStyleSheet(compact)
            header.addWidget(btn)
        outer.addWidget(self.header_widget)

        self.body = QWidget(frame)
        body_l = QVBoxLayout(self.body)
        body_l.setContentsMargins(4, 0, 0, 0)
        body_l.setSpacing(4)

        trig_row = QHBoxLayout()
        trig_row.setSpacing(6)
        for text, widget_factory in (
            ("Mode", lambda: self._make_combo("cbx_manual_control_scope_trigger_mode", TRIGGER_MODES)),
            ("Source", lambda: self._make_combo("cbx_manual_control_scope_trigger_channel", TRIGGER_CHANNELS)),
            ("Edge", lambda: self._make_combo("cbx_manual_control_scope_trigger_edge", TRIGGER_EDGES)),
        ):
            trig_row.addWidget(QLabel(text, self.body))
            w = widget_factory()
            trig_row.addWidget(w)
        self.cbx_trigger_mode = self.body.findChild(QComboBox, "cbx_manual_control_scope_trigger_mode")
        self.cbx_trigger_channel = self.body.findChild(QComboBox, "cbx_manual_control_scope_trigger_channel")
        self.cbx_trigger_edge = self.body.findChild(QComboBox, "cbx_manual_control_scope_trigger_edge")

        trig_row.addWidget(QLabel("Level (V)", self.body))
        self.lineedit_trigger_level = TriggerLevelEdit(self.body)
        self.lineedit_trigger_level.setObjectName("lineedit_manual_control_scope_trigger_level")
        self.lineedit_trigger_level.setText("0.0")
        self.lineedit_trigger_level.setMaximumWidth(72)
        trig_row.addWidget(self.lineedit_trigger_level)
        self.btn_apply_trigger = QPushButton("Apply trigger", self.body)
        self.btn_apply_trigger.setStyleSheet(compact)
        trig_row.addWidget(self.btn_apply_trigger)
        self.btn_auto_find_trigger = QPushButton("Auto find", self.body)
        self.btn_auto_find_trigger.setObjectName("btn_manual_control_scope_auto_find_trigger")
        self.btn_auto_find_trigger.setToolTip(
            "Sweep trigger level on the selected source (same algorithm as waveform tests)")
        self.btn_auto_find_trigger.setStyleSheet(compact)
        trig_row.addWidget(self.btn_auto_find_trigger)
        self.btn_auto_find_settings = QToolButton(self.body)
        self.btn_auto_find_settings.setObjectName("btn_manual_control_scope_auto_find_settings")
        self.btn_auto_find_settings.setText("⚙")
        self.btn_auto_find_settings.setToolTip("Auto-find trigger delta and settle times")
        self.btn_auto_find_settings.setStyleSheet(mc_theme.gear_style())
        self.btn_auto_find_settings.setCursor(Qt.PointingHandCursor)
        trig_row.addWidget(self.btn_auto_find_settings)
        trig_row.addStretch(1)
        body_l.addLayout(trig_row)

        cap_row = QHBoxLayout()
        cap_row.setSpacing(6)
        cap_row.addWidget(QLabel("PNG file", self.body))
        self.lineedit_filename = QLineEdit(self.body)
        self.lineedit_filename.setObjectName("lineedit_manual_control_scope_filename")
        self.lineedit_filename.setText("manual_capture.png")
        cap_row.addWidget(self.lineedit_filename, 1)
        self.btn_capture = QPushButton("Capture waveform", self.body)
        self.btn_capture.setObjectName("btn_manual_control_scope_capture")
        self.btn_capture.setStyleSheet(compact)
        cap_row.addWidget(self.btn_capture)
        body_l.addLayout(cap_row)

        self.label_capture_path = QLabel("", self.body)
        self.label_capture_path.setWordWrap(True)
        self.label_capture_path.setStyleSheet("color: rgb(130,140,160); font-size: 9px; border: none;")
        body_l.addWidget(self.label_capture_path)
        for lbl in self.body.findChildren(QLabel):
            lbl.setStyleSheet(lbl_style)

        outer.addWidget(self.body)
        self.btn_apply_mode = self.btn_apply_trigger
        self.btn_apply_level = self.btn_apply_trigger

        ui.verticalLayout_12.addWidget(frame, 0)
        ui.frame_manual_control_oscilloscope = frame

        ui.btn_manual_control_scope_run = self.btn_run
        ui.btn_manual_control_scope_run_single = self.btn_run_single
        ui.btn_manual_control_scope_stop = self.btn_stop
        ui.label_manual_control_scope_status = self.label_status
        ui.btn_manual_control_scope_capture = self.btn_capture
        ui.cbx_manual_control_scope_trigger_mode = self.cbx_trigger_mode
        ui.cbx_manual_control_scope_trigger_channel = self.cbx_trigger_channel
        ui.cbx_manual_control_scope_trigger_edge = self.cbx_trigger_edge
        ui.lineedit_manual_control_scope_trigger_level = self.lineedit_trigger_level
        ui.lineedit_manual_control_scope_filename = self.lineedit_filename
        ui.btn_manual_control_scope_auto_find_trigger = self.btn_auto_find_trigger
        ui.btn_manual_control_scope_auto_find_settings = self.btn_auto_find_settings

    def _make_combo(self, name: str, items):
        cbx = QComboBox(self.body)
        cbx.setObjectName(name)
        cbx.addItems(items)
        cbx.setMaximumWidth(100)
        return cbx

    def _bind(self):
        self.btn_run.clicked.connect(self.run_continuous)
        self.btn_run_single.clicked.connect(self.run_single)
        self.btn_stop.clicked.connect(self.stop)
        self.btn_apply_trigger.clicked.connect(self._apply_trigger_mode_and_level)
        self.lineedit_trigger_level.set_wheel_apply_callback(
            self._apply_trigger_from_wheel)
        self.btn_auto_find_trigger.clicked.connect(self.auto_find_trigger)
        self.btn_auto_find_settings.clicked.connect(self._open_auto_find_settings)
        self.btn_capture.clicked.connect(self.capture_waveform)
        self.btn_collapse.toggled.connect(self._set_body_visible)
        self._set_body_visible(True)

    def _set_body_visible(self, expanded: bool):
        self.body.setVisible(expanded)
        self.btn_collapse.setText("▼" if expanded else "▶")
        for w in (
            self.btn_capture,
            self.lineedit_filename,
            self.label_capture_path,
            self.btn_apply_trigger,
            self.btn_auto_find_trigger,
            self.btn_auto_find_settings,
            self.lineedit_trigger_level,
            self.cbx_trigger_mode,
            self.cbx_trigger_channel,
            self.cbx_trigger_edge,
        ):
            w.setVisible(expanded)
        frame = self.ui.frame_manual_control_oscilloscope
        if expanded:
            frame.setMaximumHeight(16777215)
            frame.setMinimumHeight(0)
        else:
            frame.setMaximumHeight(self.header_widget.sizeHint().height() + 20)

    def _apply_trigger_mode_and_level(self):
        # edge_trigger() drivers force NORM briefly; re-apply mode after edge setup.
        self.apply_edge_trigger()
        self.apply_trigger_mode()

    def _apply_trigger_from_wheel(self):
        """Live edge update while scrolling level (skip full mode re-apply)."""
        if self._auto_find_running:
            return
        self.apply_edge_trigger()

    def get_scope(self):
        return self.handler.get_oscilloscope()

    def _set_status(self, text: str, color: str):
        self.label_status.setText(text)
        self.label_status.setStyleSheet(f"font-weight: bold; color: {color}; padding-left: 8px;")

    def refresh_controls(self):
        ok = self.get_scope() is not None and getattr(self.handler, "oscilloscope_accessible", True)
        for w in (
            self.btn_run,
            self.btn_run_single,
            self.btn_stop,
            self.btn_apply_trigger,
            self.btn_auto_find_trigger,
            self.btn_auto_find_settings,
            self.btn_capture,
            self.cbx_trigger_mode,
            self.cbx_trigger_channel,
            self.cbx_trigger_edge,
            self.lineedit_trigger_level,
            self.lineedit_filename,
        ):
            w.setEnabled(ok and not self._auto_find_running)
        if not ok:
            self._set_status("Not assigned", "rgb(140,140,140)")
            self.label_capture_path.setText("")

    def _mark_scope_failed(self, exc: Exception, action: str):
        print(f"[SCOPE] {action} failed: {exc}")
        self.handler.oscilloscope_accessible = False
        self.refresh_controls()

    def run_continuous(self):
        scope = self.get_scope()
        if scope is None:
            return
        try:
            scope.run()
            self._set_status("RUN", "rgb(85,255,127)")
        except Exception as exc:
            self._mark_scope_failed(exc, "Run")

    def run_single(self):
        scope = self.get_scope()
        if scope is None:
            return
        try:
            scope.run_single()
            self._set_status("SINGLE", "rgb(255,220,85)")
        except Exception as exc:
            self._mark_scope_failed(exc, "Run Single")

    def stop(self):
        scope = self.get_scope()
        if scope is None:
            return
        try:
            scope.stop()
            self._set_status("STOP", "rgb(255,120,120)")
        except Exception as exc:
            self._mark_scope_failed(exc, "Stop")

    def _trigger_channel_index(self) -> int:
        text = self.cbx_trigger_channel.currentText().strip().upper()
        m = re.search(r"(\d)", text)
        return int(m.group(1)) if m else 1

    def _trigger_edge_scpi(self) -> str:
        label = self.cbx_trigger_edge.currentText().strip()
        return TRIGGER_EDGE_SCPI.get(label, "POS")

    def apply_trigger_mode(self):
        scope = self.get_scope()
        if scope is None:
            return
        ui_mode = self.cbx_trigger_mode.currentText()
        try:
            if isinstance(scope, LeCroyOscilloscope):
                lc_map = {
                    "Auto": TriggerMode.AUTO,
                    "Normal": TriggerMode.NORMAL,
                    "Freerun": TriggerMode.FREERUN,
                }
                scope.set_trigger_mode(lc_map.get(ui_mode, TriggerMode.AUTO))
            elif isinstance(scope, RohdeSchwarzOscilloscope):
                rs_map = {"Auto": "AUTO", "Normal": "NORM", "Freerun": "FREerun"}
                scope.set_trigger_mode(rs_map.get(ui_mode, "AUTO"))
            elif hasattr(scope, "trigger_mode"):
                rs_map = {"Auto": "AUTO", "Normal": "NORM", "Freerun": "FREerun"}
                scope.trigger_mode(rs_map.get(ui_mode, "AUTO"))
            else:
                print("[SCOPE] Trigger mode not supported for this scope class")
                return
            self._set_status(f"MODE {ui_mode.upper()}", "rgb(200,200,255)")
        except Exception as exc:
            self._mark_scope_failed(exc, "Apply trigger mode")

    def apply_edge_trigger(self):
        scope = self.get_scope()
        if scope is None:
            return
        try:
            ch = self._trigger_channel_index()
            level = float(self.lineedit_trigger_level.text().strip())
        except ValueError:
            self.handler.parent.msg_box_info(
                title="Oscilloscope",
                message="Enter a numeric trigger level (volts).",
                message_type=MessageType.INFO,
            )
            return
        edge = self._trigger_edge_scpi()
        edge_label = self.cbx_trigger_edge.currentText()
        try:
            if hasattr(scope, "edge_trigger"):
                scope.edge_trigger(ch, level, edge)
            elif hasattr(scope, "write"):
                scope.write(f"TRIG1:SOUR CHAN{ch}")
                scope.write("TRIG1:TYPE EDGE")
                if hasattr(scope, "trigger_level"):
                    scope.trigger_level(ch, level)
                elif hasattr(scope, "set_trigger_level"):
                    scope.set_trigger_level(level)
                else:
                    scope.write(f"TRIG1:LEV{ch} {level}")
                scope.write(f"TRIG1:EDGE:SLOP {edge}")
            elif hasattr(scope, "trigger_level"):
                scope.trigger_level(ch, level)
            elif hasattr(scope, "set_trigger_level"):
                scope.set_trigger_level(level)
            else:
                print("[SCOPE] Edge trigger not supported for this scope class")
                return
            self._set_status(
                f"EDGE CH{ch} {edge_label} {level:g} V",
                "rgb(200,200,255)",
            )
        except Exception as exc:
            self._mark_scope_failed(exc, "Apply edge trigger")

    def apply_trigger_level(self):
        """Backward-compatible alias for edge trigger + mode."""
        self.apply_edge_trigger()
        self.apply_trigger_mode()

    def _open_auto_find_settings(self):
        dlg = ScopeAutoFindSettingsDialog(self.handler.parent, self.auto_find_settings)
        if dlg.exec_() == QDialog.Accepted:
            dlg.apply_to_settings()

    def _pump_events(self):
        app = QApplication.instance()
        if app is not None:
            app.processEvents()

    def auto_find_trigger(self):
        scope = self.get_scope()
        if scope is None or self._auto_find_running:
            return
        if not hasattr(scope, "get_measure") or not hasattr(scope, "edge_trigger"):
            self.handler.parent.msg_box_info(
                title="Oscilloscope",
                message="Auto-find requires a scope with measurements and edge trigger support.",
                message_type=MessageType.INFO,
            )
            return

        ch = self._trigger_channel_index()
        edge = self._trigger_edge_scpi()
        self._auto_find_running = True
        self.refresh_controls()
        self._set_status("AUTO FIND…", "rgb(255,220,85)")

        def on_progress(msg: str):
            self._set_status(msg[:48], "rgb(255,220,85)")
            self._pump_events()

        try:
            level = find_trigger_level(
                scope,
                ch,
                edge,
                self.auto_find_settings,
                pump_events=self._pump_events,
                on_progress=on_progress,
            )
            self.lineedit_trigger_level.setText(f"{level:g}")
            self.apply_edge_trigger()
            self.apply_trigger_mode()
            self._set_status(f"AUTO CH{ch} {level:g} V", "rgb(85,255,127)")
        except Exception as exc:
            self._mark_scope_failed(exc, "Auto find trigger")
        finally:
            self._auto_find_running = False
            self.refresh_controls()

    def _sanitize_filename(self, name: str) -> str:
        name = (name or "").strip()
        if not name:
            name = "manual_capture.png"
        if not name.lower().endswith(".png"):
            name += ".png"
        name = re.sub(r'[<>:"/\\|?*]', "_", name)
        return name

    def _unique_filename(self, directory: str, filename: str) -> str:
        """If path exists, append _1, _2, ... before the extension."""
        full = os.path.join(directory, filename)
        if not os.path.exists(full):
            return filename
        stem, ext = os.path.splitext(filename)
        for n in range(1, 10000):
            candidate = f"{stem}_{n}{ext}"
            if not os.path.exists(os.path.join(directory, candidate)):
                return candidate
        raise OSError(f"Too many files matching {filename} in {directory}")

    def capture_waveform(self):
        scope = self.get_scope()
        if scope is None:
            return
        filename = self._sanitize_filename(self.lineedit_filename.text())
        out_dir = self._default_capture_dir
        try:
            os.makedirs(out_dir, exist_ok=True)
        except OSError as exc:
            print(f"[SCOPE] Cannot create folder {out_dir}: {exc}")
            out_dir = os.path.expanduser("~")
        path = out_dir
        filename = self._unique_filename(path, filename)
        try:
            scope.get_screenshot(filename, path)
            full = os.path.join(path, filename)
            self.label_capture_path.setText(f"Saved: {full}")
            self._set_status("CAPTURED", "rgb(85,255,127)")
            print(f"[SCOPE] Capture saved: {full}")
        except Exception as exc:
            self.label_capture_path.setText(f"Capture failed: {exc}")
            self._mark_scope_failed(exc, "Capture")

    def dialog_state_widgets(self):
        return [
            self.cbx_trigger_mode,
            self.cbx_trigger_channel,
            self.cbx_trigger_edge,
            self.lineedit_trigger_level,
            self.lineedit_filename,
        ]
