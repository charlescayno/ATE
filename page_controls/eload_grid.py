"""Manual Control electronic load grid.

Replaces the CH1-CH4 e-load tabs with a 2x2 grid of compact tiles. Slew settings
move into a per-channel dialog opened from a gear button, the output discharge
controls sit in the grid header, and USB PD Sink becomes a collapsible panel.
One EloadChannel controller drives every channel, including the fixed-range
Chroma modes (CCL/CCH/CCDL/CCDH/CRL/CRH).
"""
from PySide2.QtCore import Qt
from PySide2.QtGui import QDoubleValidator
from PySide2.QtWidgets import (QDialog, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QSizePolicy, QToolButton, QVBoxLayout, QWidget)

from equipment.eload_specs import ELoadTypes, EloadStatus
from psu_tests.definitions import MessageType
from ui.ui_styles import Style

CHANNELS = (1, 2, 3, 4)

TILE_STYLE = "QFrame#{name}{{border: 2px solid black; border-radius: 10px; background-color: rgb(29,34,44);}}"
TILE_ON_STYLE = "QFrame#{name}{{border: 2px solid rgb(85,170,85); border-radius: 10px; background-color: rgb(29,34,44);}}"
UNASSIGNED_STYLE = "QFrame#{name}{{border: 2px dashed rgb(70,70,70); border-radius: 10px; background-color: rgb(36,38,44);}}"
HEADER_STYLE = ("QFrame#frame_eload_grid_header{border: 2px solid black; border-radius: 10px; background-color: rgb(29,34,44);}"
                "QLabel{border:none; color: rgb(220,220,220);} QCheckBox{color: white;}")
GEAR_STYLE = ("QToolButton{border:none; color: rgb(180,180,180); font-size: 16px;}"
              "QToolButton:hover{color: white;} QToolButton:disabled{color: rgb(71,71,71);}")
DIALOG_STYLE = ("QDialog{background-color: rgb(40,44,52);} QLabel{color: rgb(210,210,210);}"
                "QPushButton#btn_eload_dialog_close{color: white; background-color: rgb(52,59,72); border: 1px solid rgb(80,90,110);"
                " border-radius: 5px; padding: 4px 14px;}")
TOGGLE_STYLE = ("QToolButton{color: rgb(200,200,200); background-color: rgb(39,44,54); border: 1px solid rgb(63,70,87);"
                " border-radius: 6px; font-weight: bold;} QToolButton:hover{background-color: rgb(52,59,72);}")


def _sfx(n):
    return "" if n == 1 else f"_{n}"


def eload_widgets(handler, n):
    ui, s = handler.ui, _sfx(n)

    def w(name):
        widget = getattr(ui, name, None)
        return widget if widget is not None else getattr(handler, name)

    return {
        'tile': w(f"frame_manual_control_eload{s}"),
        'title': w(f"label_manual_control_eload{s}"),
        'contents': w(f"frame_manual_control_eload{s}_contents"),
        'top': w(f"frame_manual_control_eload{s}_top"),
        'level': w(f"frame_manual_control_eload{s}_level"),
        'slew': w(f"frame_manual_control_eload{s}_slew"),
        'bottom': w(f"frame_manual_control_eload{s}_bottom"),
        'b_frame': w(f"frame_manual_control_eload{s}_b"),
        'mode': w(f"cbx_manual_control_eload_type{s}"),
        'swap': w(f"btn_manual_control_eload_a_b_swap{s}"),
        'a_label': w(f"label_manual_control_eload{s}_a"),
        'b_label': w(f"label_manual_control_eload{s}_b"),
        'a_edit': w(f"lineedit_manual_control_eload_a_level{s}"),
        'b_edit': w(f"lineedit_manual_control_eload_b_level{s}"),
        'a_unit': w(f"label_manual_control_eload{s}_a_level_unit"),
        'b_unit': w(f"label_manual_control_eload{s}_b_level_unit"),
        'set_a': w(f"btn_manual_control_eload_set_A{s}"),
        'set_b': w(f"btn_manual_control_eload_set_B{s}"),
        'set_slew': w(f"btn_manual_control_eload_set_slew{s}"),
        'rise_label': w(f"label_manual_control_electronic_load_rise{s}"),
        'fall_label': w(f"label_manual_control_electronic_load_fall{s}"),
        'rise_edit': w(f"lineedit_manual_control_eload_slew_rise{s}"),
        'fall_edit': w(f"lineedit_manual_control_eload_slew_fall{s}"),
        'rise_unit': w(f"label_manual_control_eload{s}_slew_rise_unit"),
        'fall_unit': w(f"label_manual_control_eload{s}_slew_fall_unit"),
        'rise_max': w(f"btn_manual_control_eload_slew_rise_max{s}"),
        'fall_max': w(f"btn_manual_control_eload_slew_fall_max{s}"),
        'on': w(f"btn_manual_control_eload_turn_on{s}"),
        'off': w(f"btn_manual_control_eload_turn_off{s}"),
    }


def _parse_slew(text):
    text = text.strip().upper()
    return "MAX" if text == "MAX" else round(float(text) / 1000, 6)


class EloadChannel:
    """Button/combobox logic for one e-load channel (replaces the per-channel copies)."""

    def __init__(self, handler, n, widgets):
        self.handler, self.n, self.w = handler, n, widgets

    # -- helpers ---------------------------------------------------------
    @property
    def load(self):
        return getattr(self.handler.equipment, f'electronic_load_{self.n}', None)

    @property
    def flag(self):
        return 'electronic_load_accessible' if self.n == 1 else f'electronic_load_{self.n}_accessible'

    def accessible(self):
        return getattr(self.handler, self.flag, False) and self.load is not None

    @property
    def mode(self):
        return self.w['mode'].currentText()

    def _run(self, fn):
        if not self.accessible():
            return
        try:
            fn()
        except ValueError as e:
            self.handler.parent.msg_box_info(title=f"E-Load CH{self.n}", message=str(e),
                                             message_type=MessageType.INFO)
        except Exception as e:
            print(f"[E_LOAD] CH{self.n} error: {e}")
            setattr(self.handler, self.flag, False)
            self.w['tile'].setStyleSheet(Style.red_frame)
            self.w['tile'].setEnabled(False)

    def _vout(self):
        vout_V = self.load.voltage
        return self.load.crh_max_v if abs(vout_V) < 0.5 else vout_V

    # -- actions ---------------------------------------------------------
    def turn_on(self):
        self._run(lambda: self.load.turn_on())

    def turn_off(self):
        self._run(lambda: self.load.turn_off())

    def set_level(self, level_no):
        def do():
            mode = self.mode
            value = round(float((self.w['a_edit'] if level_no == 1 else self.w['b_edit']).text()), 6)
            if mode in ELoadTypes.DYNAMIC_CC:
                return self._apply_dynamic()
            if mode in ELoadTypes.FIXED_CC + ELoadTypes.FIXED_CR:
                self.load.set_active_level(level_no)
                return self.load.set_fixed_mode(mode, value, level_no)
            vout_V = self._vout()
            match mode:
                case ELoadTypes.CC:
                    iout_A = value
                case ELoadTypes.CR:
                    iout_A = 0 if value == 0 else vout_V / value
                case ELoadTypes.CP:
                    iout_A = value / vout_V
                case ELoadTypes.CV:
                    vout_V, iout_A = value, None
                case _:
                    return
            self.load.set_active_level(level_no)
            self.load.set_load(vout_V=vout_V, iout_A=iout_A, mode=mode)
        self._run(do)

    def set_slew(self):
        def do():
            mode = self.mode
            if mode in ELoadTypes.DYNAMIC_CC:
                return self._apply_dynamic()
            rise, fall = _parse_slew(self.w['rise_edit'].text()), _parse_slew(self.w['fall_edit'].text())
            if mode in (ELoadTypes.CC,) + ELoadTypes.FIXED_CC:
                self.load.set_cc_static_slew(rise, fall)
            elif mode in (ELoadTypes.CR,) + ELoadTypes.FIXED_CR:
                self.load.set_cr_slew(rise, fall)
        self._run(do)

    def apply_dynamic(self):
        self._run(self._apply_dynamic)

    def _apply_dynamic(self):
        self.load.set_dynamic(self.mode,
                              round(float(self.w['a_edit'].text()), 6),
                              round(float(self.w['b_edit'].text()), 6),
                              float(self.t1_edit.text()), float(self.t2_edit.text()),
                              _parse_slew(self.w['rise_edit'].text()), _parse_slew(self.w['fall_edit'].text()))

    def swap(self):
        if self.mode in ELoadTypes.DYNAMIC_CC or not self.accessible():
            return
        self.set_level(2 if self.load._active_level == '1' else 1)

    def set_max(self, edit):
        edit.setText("MAX")

    # -- UI state --------------------------------------------------------
    def populate_modes(self):
        load = self.load
        if load is None:
            return
        cbx = self.w['mode']
        previous = cbx.currentText()
        cbx.blockSignals(True)
        cbx.clear()
        cbx.addItems(list(load.load_modes))
        if previous in load.load_modes:
            cbx.setCurrentText(previous)
        cbx.blockSignals(False)
        self.update_settings()

    def update_settings(self):
        w, mode, load = self.w, self.mode, self.load
        dynamic = mode in ELoadTypes.DYNAMIC_CC
        w['rise_label'].setText('Rise')
        w['rise_unit'].setText('mA / µs')
        w['fall_unit'].setText('mA / µs')
        w['rise_edit'].setText('150')
        w['fall_edit'].setText('150')
        w['a_label'].setText('L1' if dynamic else 'Level A')
        w['b_label'].setText('L2' if dynamic else 'Level B')
        multi = bool(getattr(load, 'multi_channel', False))
        w['b_frame'].setVisible(dynamic or not multi)
        w['swap'].setEnabled(not dynamic)
        self.dynamic_row.setVisible(dynamic)
        w['set_a'].setVisible(not dynamic)
        w['set_b'].setVisible(not dynamic)

        unit = {'CC': 'A', 'CR': 'Ω', 'CV': 'V', 'CP': 'W', 'LED': 'V'}.get(mode)
        if mode in ELoadTypes.FIXED_CC + ELoadTypes.DYNAMIC_CC:
            unit = 'A'
        elif mode in ELoadTypes.FIXED_CR:
            unit = 'Ω'
        if unit:
            w['a_unit'].setText(unit)
            w['b_unit'].setText(unit)

        rise_on = fall_on = True
        if mode in (ELoadTypes.CR,) + ELoadTypes.FIXED_CR and load is not None and not load.cr_slew_available:
            rise_on = fall_on = False
        elif mode == ELoadTypes.CV:
            w['rise_unit'].setText('A')
            w['rise_label'].setText('Limit')
            fall_on = False
        elif mode == ELoadTypes.CP and load is not None:
            u = 'A / µs' if load.cp_slew_unit[0] == 'A' else 'W / µs'
            w['rise_unit'].setText(u)
            w['fall_unit'].setText(u)
            w['rise_edit'].setText('0.15')
            w['fall_edit'].setText('0.15')
        for key in ('rise_label', 'rise_edit', 'rise_unit'):
            w[key].setEnabled(rise_on)
        for key in ('fall_label', 'fall_edit', 'fall_unit'):
            w[key].setEnabled(fall_on)

    def refresh_status(self):
        load, tile = self.load, self.w['tile']
        if load is None or not getattr(self.handler, self.flag, False):
            return
        on = str(getattr(load, 'active_channel_status', '0')) == EloadStatus.ON
        level = getattr(load, '_active_level', '1')
        mode = getattr(load, 'active_channel_mode', '') or ''
        self.status.setText(f"● ON  {mode} L{level}" if on else f"○ OFF  {mode}")
        self.status.setStyleSheet("color: rgb(85,255,127);" if on else "color: rgb(140,140,140);")
        style = (TILE_ON_STYLE if on else TILE_STYLE).format(name=tile.objectName())
        if tile.styleSheet() != style:
            tile.setStyleSheet(style)


class EloadSettingsDialog(QDialog):
    def __init__(self, parent, n, slew_frame):
        super().__init__(parent)
        self.setWindowTitle(f"Electronic Load CH{n} Slew Settings")
        self.setStyleSheet(DIALOG_STYLE)
        lay = QVBoxLayout(self)
        slew_frame.setParent(self)
        lay.addWidget(slew_frame)
        slew_frame.show()
        btn = QPushButton("Close", self)
        btn.setObjectName("btn_eload_dialog_close")
        btn.clicked.connect(self.close)
        lay.addWidget(btn, 0, Qt.AlignRight)


class EloadGrid:
    def __init__(self, handler):
        self.handler = handler
        self.ui = handler.ui
        self.channels = {n: EloadChannel(handler, n, eload_widgets(handler, n)) for n in CHANNELS}
        self.dialogs = {}
        self.gears = {}
        self.validator = QDoubleValidator(0, 16777215, 6)
        self._build()
        self._bind()

    # -- layout ----------------------------------------------------------
    def _build(self):
        ui = self.ui
        lower = ui.horizontalLayout_13
        tabs = ui.tabWidget_eload
        idx = lower.indexOf(tabs)
        while tabs.count():
            tabs.removeTab(0)
        lower.removeWidget(tabs)
        tabs.hide()

        container = QWidget(ui.frame_manual_control_lower)
        container.setObjectName("widget_eload_grid")
        v = QVBoxLayout(container)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(6)
        v.addWidget(self._build_header(container))
        grid = QGridLayout()
        grid.setSpacing(6)
        for n in CHANNELS:
            self._compact_tile(n)
            tile = self.channels[n].w['tile']
            grid.addWidget(tile, (n - 1) // 2, (n - 1) % 2)
            tile.show()
        v.addLayout(grid, 1)
        lower.insertWidget(idx, container, 3)
        ui.widget_eload_grid = container
        self._make_usb_pd_collapsible()

    def _build_header(self, parent):
        ui = self.ui
        header = QFrame(parent)
        header.setObjectName("frame_eload_grid_header")
        header.setStyleSheet(HEADER_STYLE)
        header.setMaximumHeight(46)
        h = QHBoxLayout(header)
        h.setContentsMargins(10, 2, 10, 2)
        title = QLabel("ELECTRONIC LOAD", header)
        title.setStyleSheet("font-weight: bold;")
        h.addWidget(title)
        h.addStretch(1)
        # Discharge controls move here from the source panel: they act on the e-loads
        grid3 = ui.gridLayout_3
        for wname in ("chkbox_manual_control_auto_discharge", "label_manual_control_discharge_current",
                      "lineedit_manual_control_discharge_current", "btn_manual_control_discharge"):
            widget = getattr(ui, wname)
            grid3.removeWidget(widget)
            widget.setParent(header)
            h.addWidget(widget)
        ui.lineedit_manual_control_discharge_current.setMaximumWidth(60)
        ui.btn_manual_control_discharge.setMinimumHeight(28)
        ui.btn_manual_control_discharge.setMinimumWidth(90)
        return header

    def _compact_tile(self, n):
        ch = self.channels[n]
        w = ch.w
        tile = w['tile']
        tile.setMinimumSize(0, 0)
        tile.setStyleSheet(TILE_STYLE.format(name=tile.objectName()))

        # Header: title, status, gear
        layout = tile.layout()
        layout.removeWidget(w['title'])
        header = QWidget(tile)
        hl = QHBoxLayout(header)
        hl.setContentsMargins(4, 0, 4, 0)
        w['title'].setParent(header)
        w['title'].setText(f"E-LOAD CH{n}")
        hl.addWidget(w['title'])
        ch.status = QLabel("○ OFF", header)
        ch.status.setStyleSheet("color: rgb(140,140,140);")
        hl.addWidget(ch.status, 1, Qt.AlignRight)
        gear = QToolButton(header)
        gear.setObjectName(f"btn_eload_settings{_sfx(n)}")
        gear.setText("⚙")
        gear.setToolTip(f"CH{n} slew rate settings")
        gear.setStyleSheet(GEAR_STYLE)
        gear.setCursor(Qt.PointingHandCursor)
        gear.clicked.connect(lambda _=False, c=n: self.open_settings(c))
        hl.addWidget(gear)
        layout.insertWidget(0, header)
        layout.setContentsMargins(6, 4, 6, 6)
        layout.setSpacing(2)
        self.gears[n] = gear
        setattr(self.ui, f"btn_eload_settings{_sfx(n)}", gear)

        # Dynamic CC timing row (shown only for CCDL/CCDH)
        row = QWidget(w['level'])
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 0, 0, 0)
        edit_style = w['a_edit'].styleSheet()
        ch.t1_edit, ch.t2_edit = QLineEdit("10", row), QLineEdit("10", row)
        for label, edit in (("T1", ch.t1_edit), ("T2", ch.t2_edit)):
            lbl = QLabel(label, row)
            lbl.setStyleSheet("color: white;")
            rl.addWidget(lbl)
            edit.setValidator(self.validator)
            edit.setStyleSheet(edit_style)
            edit.setMaximumWidth(70)
            rl.addWidget(edit)
            unit = QLabel("ms", row)
            unit.setStyleSheet("color: white;")
            rl.addWidget(unit)
        ch.t1_edit.setObjectName(f"lineedit_manual_control_eload_dyn_t1{_sfx(n)}")
        ch.t2_edit.setObjectName(f"lineedit_manual_control_eload_dyn_t2{_sfx(n)}")
        ch.apply_btn = QPushButton("Apply", row)
        ch.apply_btn.setObjectName(f"btn_manual_control_eload_dyn_apply{_sfx(n)}")
        ch.apply_btn.setStyleSheet(w['set_a'].styleSheet())
        ch.apply_btn.setMinimumHeight(28)
        rl.addWidget(ch.apply_btn)
        w['level'].layout().addWidget(row)
        ch.dynamic_row = row
        row.setVisible(False)

        # Compact the nested frames so all rows fit in a quarter of the lower row
        tile.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        nested = [w['contents'], w['top'], w['level'].parentWidget(), w['level'],
                  w['a_edit'].parentWidget(), w['b_frame'], w['bottom']]
        for frame in nested:
            frame.setMinimumHeight(0)
            if frame.layout() is not None:
                frame.layout().setContentsMargins(2, 1, 2, 1)
                frame.layout().setSpacing(4)

        # Compact the fixed-size widgets
        for key in ('on', 'off'):
            w[key].setMinimumSize(60, 30)
        for key in ('a_edit', 'b_edit', 'set_a', 'set_b', 'swap', 'mode'):
            w[key].setMinimumHeight(26)
            w[key].setMaximumHeight(32)

        # Slew settings move into the gear dialog
        self.dialogs[n] = EloadSettingsDialog(self.handler.parent, n, w['slew'])

    def _make_usb_pd_collapsible(self):
        ui = self.ui
        lower = ui.horizontalLayout_13
        frame = ui.frame_manual_control_usb_pd_sink
        idx = lower.indexOf(frame)
        toggle = QToolButton(ui.frame_manual_control_lower)
        toggle.setObjectName("btn_manual_control_usb_pd_toggle")
        toggle.setCheckable(True)
        toggle.setStyleSheet(TOGGLE_STYLE)
        toggle.setMinimumWidth(28)
        toggle.setMaximumWidth(28)
        toggle.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        toggle.toggled.connect(self.set_usb_pd_expanded)
        lower.insertWidget(idx, toggle)
        ui.btn_manual_control_usb_pd_toggle = toggle
        self.usb_pd_toggle = toggle
        self.set_usb_pd_expanded(False)

    def set_usb_pd_expanded(self, expanded):
        self.ui.frame_manual_control_usb_pd_sink.setVisible(expanded)
        self.usb_pd_toggle.setText("▸\nU\nS\nB\n\nP\nD" if expanded else "◂\nU\nS\nB\n\nP\nD")
        self.usb_pd_toggle.setToolTip("Hide USB PD Sink" if expanded else "Show USB PD Sink")
        if self.usb_pd_toggle.isChecked() != expanded:
            self.usb_pd_toggle.setChecked(expanded)

    # -- bindings --------------------------------------------------------
    def _bind(self):
        for n, ch in self.channels.items():
            w = ch.w
            w['on'].clicked.connect(ch.turn_on)
            w['off'].clicked.connect(ch.turn_off)
            w['set_a'].clicked.connect(lambda _=False, c=ch: c.set_level(1))
            w['set_b'].clicked.connect(lambda _=False, c=ch: c.set_level(2))
            w['set_slew'].clicked.connect(ch.set_slew)
            w['swap'].clicked.connect(ch.swap)
            w['rise_max'].clicked.connect(lambda _=False, c=ch: c.set_max(c.w['rise_edit']))
            w['fall_max'].clicked.connect(lambda _=False, c=ch: c.set_max(c.w['fall_edit']))
            w['mode'].currentIndexChanged.connect(lambda _=0, c=ch: c.update_settings())
            ch.apply_btn.clicked.connect(ch.apply_dynamic)
            for key in ('a_edit', 'b_edit'):
                w[key].setValidator(self.validator)

    def open_settings(self, n):
        dlg = self.dialogs[n]
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()

    def dialog_state_widgets(self):
        """Widgets moved out of page_manual_control that still need save/restore."""
        from PySide2.QtWidgets import QComboBox, QCheckBox
        found = []
        for dlg in self.dialogs.values():
            for t in (QLineEdit, QComboBox, QCheckBox):
                found += [x for x in dlg.findChildren(t) if x.objectName()]
        return found

    # -- assignment / status --------------------------------------------
    def set_assigned(self, n, assigned):
        ch = self.channels[n]
        tile = ch.w['tile']
        if assigned:
            tile.setEnabled(True)
            tile.setStyleSheet(TILE_STYLE.format(name=tile.objectName()))
            ch.w['title'].setText(f"E-LOAD CH{n}")
            ch.populate_modes()
        else:
            tile.setEnabled(False)
            tile.setStyleSheet(UNASSIGNED_STYLE.format(name=tile.objectName()))
            ch.w['title'].setText(f"E-LOAD CH{n} - Not assigned")
            ch.status.setText("")
            self.dialogs[n].hide()

    def refresh_status(self):
        for ch in self.channels.values():
            ch.refresh_status()
