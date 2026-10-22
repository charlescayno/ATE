"""Manual Control load power meter grid.

Replaces the CH1-CH4 load power meter tabs with a 2x2 grid of compact tiles,
a total strip (Pin | Sum Pout | Total Eff) and a per-meter settings dialog
(voltage/current range, integration, averaging, mode) opened from a gear button.
Also hosts the non-blocking output discharge sequencer used by Manual Control.
"""
from PySide2.QtCore import Qt, QTimer
from PySide2.QtGui import QFont
from PySide2.QtWidgets import (QDialog, QFrame, QGridLayout, QHBoxLayout, QLabel,
                               QPushButton, QSizePolicy, QToolButton, QVBoxLayout, QWidget)

from page_controls import manual_control_theme as mc_theme

CHANNELS = (1, 2, 3, 4)
PIN_LIMIT_W = 10e3

GEAR_STYLE = mc_theme.gear_style()
DIALOG_STYLE = mc_theme.dialog_style()
STRIP_STYLE = mc_theme.strip_style()


def _sfx(n: int) -> str:
    return "" if n == 1 else f"_{n}"


def pml_widgets(ui, n: int) -> dict:
    s = _sfx(n)
    return {
        'tile': getattr(ui, f"frame_manual_control_pml{s}"),
        'layout': getattr(ui, f"verticalLayout_19{s}"),
        'title': getattr(ui, f"label_load_power_meter{s}"),
        'display': getattr(ui, f"frame_pml_display{s}"),
        'select': getattr(ui, "frame_pml_display_select" if n == 1 else f"frame_pml_display{s}_select"),
        'control': getattr(ui, f"frame_pml_control{s}"),
        'labels': [getattr(ui, f"label_pml_display_{c}{s}") for c in "abcd"],
        'cbx': [getattr(ui, f"cbx_pml_display_{c}{s}") for c in "abcd"],
    }


def compute_efficiency(pin_W, pouts_W: dict):
    """Return (sum_pout_W, total_eff_pct, share_pct_by_channel) for the readable load meters."""
    if not pouts_W:
        return None, None, {}
    total = sum(pouts_W.values())
    eff = total / pin_W * 100 if (pin_W is not None and 0 < pin_W < PIN_LIMIT_W) else None
    shares = {n: p / total * 100 for n, p in pouts_W.items()} if total > 0 else {}
    return total, eff, shares


class PmlSettingsDialog(QDialog):
    def __init__(self, parent, n: int, control_frame: QFrame):
        super().__init__(parent)
        self.setWindowTitle(f"Load Power Meter CH{n} Settings")
        self.setStyleSheet(DIALOG_STYLE)
        lay = QVBoxLayout(self)
        control_frame.setParent(self)
        lay.addWidget(control_frame)
        control_frame.show()
        btn = QPushButton("Close", self)
        btn.clicked.connect(self.close)
        lay.addWidget(btn, 0, Qt.AlignRight)


class PmlGrid:
    def __init__(self, handler):
        self.handler = handler
        self.ui = handler.ui
        self.widgets = {n: pml_widgets(self.ui, n) for n in CHANNELS}
        self.dialogs = {}
        self.gears = {}
        self.assigned = {n: True for n in CHANNELS}
        self._build()

    def _build(self):
        ui = self.ui
        tabs = ui.tabWidget_pml
        upper = ui.horizontalLayout_9
        idx = upper.indexOf(tabs)
        while tabs.count():
            tabs.removeTab(0)
        upper.removeWidget(tabs)
        tabs.hide()

        container = QWidget(ui.frame_manual_control_upper)
        container.setObjectName("widget_pml_grid")
        v = QVBoxLayout(container)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(2)
        v.addWidget(self._build_strip(container))

        grid = QGridLayout()
        grid.setSpacing(4)
        grid.setContentsMargins(0, 0, 0, 0)
        for n in CHANNELS:
            self._compact_tile(n)
            grid.addWidget(self.widgets[n]['tile'], (n - 1) // 2, (n - 1) % 2)
            self.widgets[n]['tile'].show()
        for col in range(2):
            grid.setColumnStretch(col, 0)
        for row in range(2):
            grid.setRowStretch(row, 0)
        v.addLayout(grid, 0)

        container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        upper.insertWidget(idx, container, 0)
        upper.setStretch(idx, 0)
        ui.widget_pml_grid = container

    def _build_strip(self, parent):
        strip = QFrame(parent)
        strip.setObjectName("frame_pml_total")
        strip.setStyleSheet(STRIP_STYLE)
        strip.setMaximumHeight(36)
        h = QHBoxLayout(strip)
        h.setContentsMargins(4, 0, 4, 2)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_pin = QLabel("Pin: None", strip)
        self.label_pout = QLabel("ΣPout: None", strip)
        self.label_eff = QLabel("Total Eff: None", strip)
        for lbl in (self.label_pin, self.label_pout, self.label_eff):
            lbl.setFont(font)
            lbl.setAlignment(Qt.AlignCenter)
            h.addWidget(lbl, 1)
        self.label_eff.setStyleSheet("color: rgb(85, 255, 127);")
        self.ui.label_pml_total_pin = self.label_pin
        self.ui.label_pml_total_pout = self.label_pout
        self.ui.label_pml_total_eff = self.label_eff
        return strip

    def _compact_tile(self, n):
        w = self.widgets[n]
        tile = w['tile']
        tile.setMinimumSize(0, 0)
        tile.setMaximumWidth(520)
        tile.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        tile.setStyleSheet(mc_theme.tile_style(tile.objectName(), assigned=True))

        # Header: title + gear
        w['layout'].removeWidget(w['title'])
        header = QWidget(tile)
        hl = QHBoxLayout(header)
        hl.setContentsMargins(4, 0, 4, 0)
        w['title'].setParent(header)
        w['title'].setText(f"LOAD PM CH{n}")
        w['title'].setStyleSheet(mc_theme.section_title_style())
        w['title'].setFont(mc_theme.label_font(10))
        hl.addWidget(w['title'], 1)
        gear = QToolButton(header)
        gear.setObjectName(f"btn_pml_settings{_sfx(n)}")
        gear.setText("⚙")
        gear.setToolTip(f"CH{n} range / integration / averaging / mode settings")
        gear.setStyleSheet(GEAR_STYLE)
        gear.setCursor(Qt.PointingHandCursor)
        gear.clicked.connect(lambda _=False, ch=n: self.open_settings(ch))
        hl.addWidget(gear)
        w['layout'].insertWidget(0, header)
        w['layout'].setContentsMargins(4, 2, 4, 4)
        w['layout'].setSpacing(1)
        self.gears[n] = gear
        setattr(self.ui, f"btn_pml_settings{_sfx(n)}", gear)

        # Readouts: smaller rows so the 2x2 grid fits
        w['display'].setMinimumSize(0, 0)
        w['display'].setMaximumWidth(16777215)
        for lbl in w['labels']:
            lbl.setFont(mc_theme.telemetry_font(15))
            lbl.setStyleSheet(mc_theme.telemetry_label_style())
            lbl.setMinimumHeight(24)
            lbl.setMaximumHeight(30)
        w['select'].setMaximumWidth(78)
        for cbx in w['cbx']:
            cbx.setMinimumHeight(24)
            cbx.setMaximumHeight(30)

        # Settings move into the gear dialog
        self.dialogs[n] = PmlSettingsDialog(self.handler.parent, n, w['control'])

    def open_settings(self, n):
        dlg = self.dialogs[n]
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()

    def dialog_state_widgets(self):
        """Widgets moved out of page_manual_control that still need save/restore."""
        from PySide2.QtWidgets import QCheckBox, QComboBox, QLineEdit
        found = []
        for dlg in self.dialogs.values():
            for t in (QLineEdit, QComboBox, QCheckBox):
                found += [x for x in dlg.findChildren(t) if x.objectName()]
        return found

    def set_assigned(self, n, assigned: bool):
        self.assigned[n] = assigned
        w = self.widgets[n]
        tile = w['tile']
        if assigned:
            tile.setStyleSheet(mc_theme.tile_style(tile.objectName(), assigned=True))
            w['title'].setText(f"LOAD PM CH{n}")
            tile.setEnabled(True)
        else:
            tile.setStyleSheet(mc_theme.tile_style(tile.objectName(), assigned=False))
            w['title'].setText(f"LOAD PM CH{n} - Not assigned")
            for lbl in w['labels']:
                lbl.setText('—')
            tile.setEnabled(False)
            tile.hide()
            self.dialogs[n].hide()
        if assigned:
            tile.show()

    def set_share(self, n, share_pct):
        self.widgets[n]['labels'][3].setText('None' if share_pct is None else f'{share_pct:.1f}% Share')

    def set_totals(self, pin_W, sum_pout_W, eff_pct, count):
        self.label_pin.setText("Pin: None" if pin_W is None or not (0 <= pin_W < PIN_LIMIT_W) else f"Pin: {pin_W:.2f} W")
        self.label_pout.setText("ΣPout: None" if sum_pout_W is None else f"ΣPout: {sum_pout_W:.2f} W ({count} PM)")
        self.label_eff.setText("Total Eff: None" if eff_pct is None else f"Total Eff: {eff_pct:.2f}%")


class DischargeSequencer:
    """Non-blocking CCH output discharge: snapshot loads, pulse ON/OFF, then restore."""

    def __init__(self, parent, get_loads, on_done=None, pulses=2, on_ms=1000, off_ms=1000):
        self.get_loads = get_loads
        self.on_done = on_done
        self.pulses = pulses
        self.on_ms = on_ms
        self.off_ms = off_ms
        self.timer = QTimer(parent)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._step)
        self.running = False
        self.log = []

    def _emit(self, msg):
        self.log.append(msg)
        print(f"[DISCHARGE] {msg}")

    def start(self, current_A: float, reason: str = ""):
        if self.running:
            return False
        loads = self.get_loads()
        if not loads:
            self._emit(f"skipped ({reason}): no electronic load assigned")
            return False
        self.current_A = current_A
        self.loads = loads
        self.snapshots = {}
        for name, ld in loads:
            try:
                self.snapshots[name] = ld.snapshot_state()
            except Exception as e:
                self._emit(f"{name}: snapshot failed ({e})")
        self.steps = []
        for _ in range(self.pulses):
            self.steps += [('on', self.on_ms), ('off', self.off_ms)]
        self.steps.append(('restore', 0))
        self.running = True
        self._emit(f"start ({reason}): {len(loads)} load(s), CCH {current_A} A, {self.pulses}x {self.on_ms}/{self.off_ms} ms")
        self._step()
        return True

    def _step(self):
        if not self.steps:
            self.running = False
            self._emit("done")
            if self.on_done:
                self.on_done()
            return
        action, hold_ms = self.steps.pop(0)
        for name, ld in self.loads:
            try:
                if action == 'on':
                    ld.set_cc_high(self.current_A)
                    ld.turn_on()
                elif action == 'off':
                    ld.turn_off()
                elif action == 'restore' and name in self.snapshots:
                    ld.restore_state(self.snapshots[name])
            except Exception as e:
                self._emit(f"{name}: {action} failed ({e})")
        self._emit(action)
        self.timer.start(hold_ms)

    def cancel(self):
        """Abort an in-progress discharge sequence (e.g. manual E-STOP)."""
        if self.timer.isActive():
            self.timer.stop()
        self.steps = []
        loads = getattr(self, 'loads', None) or []
        for name, ld in loads:
            try:
                ld.turn_off()
            except Exception as e:
                self._emit(f"{name}: cancel off failed ({e})")
        if self.running:
            self._emit("cancelled")
        self.running = False
