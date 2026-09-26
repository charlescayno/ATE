import os
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class ScrollScaleEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.steps = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0]
    def wheelEvent(self, event):
        try:
            val = float(self.text())
            idx = min(range(len(self.steps)), key=lambda i: abs(self.steps[i]-val))
            if event.angleDelta().y() > 0:
                idx = min(len(self.steps)-1, idx+1)
            else:
                idx = max(0, idx-1)
            self.setText(str(self.steps[idx]))
            self.returnPressed.emit()
        except ValueError:
            pass

class OscilloscopeControlPageHandler:
    def __init__(self, parent):
        self.parent = parent
        self.ui = parent.ui
        self.equipment = parent.equipment

        self.setup_ui()
        self.connect_signals()
        
        self.poll_timer = QTimer(self.parent)
        self.poll_timer.timeout.connect(self.poll_measurements)
        self.polling_active = False

    def setup_ui(self):
        page = self.ui.page_oscilloscope_control
        
        # CLEAR LAYOUT IF EXISTS (for reloading)
        if page.layout():
            QWidget().setLayout(page.layout())

        self.main_layout = QVBoxLayout(page)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)

        # TITLE LABEL
        self.label_title = QLabel("MANUAL OSCILLOSCOPE CONTROL (RTO6)")
        font_title = QFont()
        font_title.setPointSize(12)
        font_title.setBold(True)
        self.label_title.setFont(font_title)
        self.label_title.setStyleSheet("color: rgb(210, 210, 210);")
        self.main_layout.addWidget(self.label_title)

        # TOP BAR (Acquisition & Display)
        self.frame_top = QFrame(page)
        self.frame_top.setStyleSheet("QFrame { background-color: rgb(39, 44, 54); border-radius: 5px; } QLabel { color: white; }")
        self.layout_top = QHBoxLayout(self.frame_top)
        
        self.btn_run_cont = QPushButton("Run Continuous")
        self.btn_run_single = QPushButton("Run Single")
        self.btn_stop = QPushButton("Stop")
        
        for btn in [self.btn_run_cont, self.btn_run_single, self.btn_stop]:
            btn.setMinimumHeight(35)
            btn.setStyleSheet("""
                QPushButton { background-color: rgb(52, 59, 72); border-radius: 5px; border: 2px solid rgb(52, 59, 72); color: white; padding: 5px 15px; }
                QPushButton:hover { background-color: rgb(57, 65, 80); }
                QPushButton:pressed { background-color: rgb(35, 40, 49); }
            """)
            self.layout_top.addWidget(btn)
            
        self.label_status = QLabel("Status: WAIT")
        self.label_status.setStyleSheet("color: #FFA500; font-weight: bold; padding: 0 15px;")
        self.layout_top.addWidget(self.label_status)
        
        # Display Persistence
        self.layout_top.addSpacing(20)
        self.layout_top.addWidget(QLabel("Persistence:"))
        self.cb_pers_state = QComboBox()
        self.cb_pers_state.addItems(["OFF", "ON"])
        self.cb_pers_state.setStyleSheet("QComboBox { background-color: rgb(27, 29, 35); color: white; border-radius: 3px; padding: 2px; }")
        self.layout_top.addWidget(self.cb_pers_state)
        
        self.cb_pers_time = QComboBox()
        self.cb_pers_time.addItems(["Auto", "50ms", "100ms", "500ms", "1s", "Infinite"])
        self.cb_pers_time.setStyleSheet("QComboBox { background-color: rgb(27, 29, 35); color: white; border-radius: 3px; padding: 2px; }")
        self.layout_top.addWidget(self.cb_pers_time)
        
        self.btn_apply_disp = QPushButton("Apply Disp")
        self.btn_apply_disp.setStyleSheet("QPushButton { background-color: rgb(52, 59, 72); border-radius: 5px; color: white; padding: 5px; }")
        self.layout_top.addWidget(self.btn_apply_disp)
        
        self.layout_top.addStretch()
        self.main_layout.addWidget(self.frame_top)

        # MIDDLE SECTION (Horizontal Layout)
        self.layout_middle = QHBoxLayout()
        self.main_layout.addLayout(self.layout_middle)

        # 1. VERTICAL TABS
        self.tab_vertical = QTabWidget()
        self.tab_vertical.setStyleSheet("""
            QTabWidget::pane { border: 1px solid rgb(52, 59, 72); background: rgb(39, 44, 54); border-radius: 5px; }
            QTabBar::tab { background: rgb(39, 44, 54); color: rgb(210, 210, 210); padding: 8px 15px; margin-right: 2px; border-top-left-radius: 4px; border-top-right-radius: 4px; }
            QTabBar::tab:selected { background: rgb(52, 59, 72); border: 1px solid rgb(52, 59, 72); border-bottom-color: rgb(52, 59, 72); }
            QLabel { color: rgb(210, 210, 210); border: none; }
            QLineEdit, QComboBox { background-color: rgb(27, 29, 35); border-radius: 5px; border: 2px solid rgb(27, 29, 35); color: white; padding: 5px; }
            QLineEdit:hover, QComboBox:hover { border: 2px solid rgb(64, 71, 88); }
        """)
        
        self.ch_widgets = {}
        for ch in range(1, 5):
            tab = QWidget()
            layout = QGridLayout(tab)
            
            # State
            layout.addWidget(QLabel(f"CH{ch} State:"), 0, 0)
            cb_state = QComboBox()
            cb_state.addItems(["OFF", "ON"])
            layout.addWidget(cb_state, 0, 1)
            
            # Label
            layout.addWidget(QLabel("Label:"), 1, 0)
            le_label = QLineEdit(f"CH{ch}")
            layout.addWidget(le_label, 1, 1)
            
            # Color
            layout.addWidget(QLabel("Color:"), 2, 0)
            btn_color = QPushButton("Pick Color")
            btn_color.setStyleSheet("background-color: rgb(80, 80, 80); color: white; border-radius: 3px;")
            layout.addWidget(btn_color, 2, 1)
            
            # Scale
            layout.addWidget(QLabel("Scale (V or A/div):\n(Scroll to change)"), 3, 0)
            le_scale = ScrollScaleEdit("1.0")
            layout.addWidget(le_scale, 3, 1)
            
            # Offset
            layout.addWidget(QLabel("Offset:"), 4, 0)
            le_offset = QLineEdit("0.0")
            layout.addWidget(le_offset, 4, 1)
            
            # Coupling
            layout.addWidget(QLabel("Coupling:"), 5, 0)
            cb_coupling = QComboBox()
            cb_coupling.addItems(["DC", "AC", "DC50", "AC50"])
            layout.addWidget(cb_coupling, 5, 1)
            
            btn_apply = QPushButton(f"Apply CH{ch}")
            btn_apply.setStyleSheet("QPushButton { background-color: rgb(52, 59, 72); border-radius: 5px; padding: 5px; color: white; } QPushButton:hover { background-color: rgb(57, 65, 80); }")
            layout.addWidget(btn_apply, 6, 0, 1, 2)
            layout.setRowStretch(7, 1)
            
            self.ch_widgets[ch] = {
                'state': cb_state, 'label': le_label, 'color_btn': btn_color, 'color_val': None,
                'scale': le_scale, 'offset': le_offset, 'coupling': cb_coupling, 'apply': btn_apply
            }
            
            self.tab_vertical.addTab(tab, f"CH{ch}")
            
        self.layout_middle.addWidget(self.tab_vertical, stretch=1)

        # 2. HORIZONTAL, TRIGGER & ZOOM
        self.frame_htz = QFrame()
        self.frame_htz.setStyleSheet("QFrame { background-color: rgb(39, 44, 54); border-radius: 5px; } QLabel { color: white; border: none; } QLineEdit, QComboBox { background-color: rgb(27, 29, 35); color: white; border-radius: 5px; padding: 5px; }")
        self.layout_htz = QVBoxLayout(self.frame_htz)
        
        lbl_ht_title = QLabel("HORIZONTAL & TRIGGER")
        lbl_ht_title.setFont(font_title)
        self.layout_htz.addWidget(lbl_ht_title)
        
        grid_ht = QGridLayout()
        grid_ht.addWidget(QLabel("Time/Div (s):"), 0, 0)
        self.le_timebase = ScrollScaleEdit("0.001")
        grid_ht.addWidget(self.le_timebase, 0, 1)
        
        grid_ht.addWidget(QLabel("Delay (s):"), 1, 0)
        self.le_delay = QLineEdit("0.0")
        grid_ht.addWidget(self.le_delay, 1, 1)
        
        grid_ht.addWidget(QLabel("Trig Source:"), 2, 0)
        self.cb_trig_source = QComboBox()
        self.cb_trig_source.addItems(["CH1", "CH2", "CH3", "CH4", "EXT"])
        grid_ht.addWidget(self.cb_trig_source, 2, 1)
        
        grid_ht.addWidget(QLabel("Trig Level:"), 3, 0)
        self.le_trig_level = QLineEdit("1.0")
        grid_ht.addWidget(self.le_trig_level, 3, 1)
        
        grid_ht.addWidget(QLabel("Trig Edge:"), 4, 0)
        self.cb_trig_edge = QComboBox()
        self.cb_trig_edge.addItems(["POS", "NEG", "EITH"])
        grid_ht.addWidget(self.cb_trig_edge, 4, 1)
        
        self.btn_apply_ht = QPushButton("Apply Horiz/Trig")
        self.btn_apply_ht.setStyleSheet("QPushButton { background-color: rgb(52, 59, 72); border-radius: 5px; padding: 5px; color: white; }")
        grid_ht.addWidget(self.btn_apply_ht, 5, 0, 1, 2)
        self.layout_htz.addLayout(grid_ht)
        
        # Zoom Section
        self.layout_htz.addSpacing(10)
        lbl_zoom_title = QLabel("ZOOM CONTROLS")
        lbl_zoom_title.setFont(font_title)
        self.layout_htz.addWidget(lbl_zoom_title)
        
        grid_zoom = QGridLayout()
        grid_zoom.addWidget(QLabel("Zoom State:"), 0, 0)
        self.cb_zoom_state = QComboBox()
        self.cb_zoom_state.addItems(["OFF", "ON"])
        grid_zoom.addWidget(self.cb_zoom_state, 0, 1)
        
        grid_zoom.addWidget(QLabel("Zoom Scale (s):"), 1, 0)
        self.le_zoom_scale = ScrollScaleEdit("0.0001")
        grid_zoom.addWidget(self.le_zoom_scale, 1, 1)
        
        grid_zoom.addWidget(QLabel("Zoom Pos (s):"), 2, 0)
        self.le_zoom_pos = QLineEdit("0.0")
        grid_zoom.addWidget(self.le_zoom_pos, 2, 1)
        
        self.btn_apply_zoom = QPushButton("Apply Zoom")
        self.btn_apply_zoom.setStyleSheet("QPushButton { background-color: rgb(52, 59, 72); border-radius: 5px; padding: 5px; color: white; }")
        grid_zoom.addWidget(self.btn_apply_zoom, 3, 0, 1, 2)
        
        self.layout_htz.addLayout(grid_zoom)
        self.layout_htz.addStretch()
        self.layout_middle.addWidget(self.frame_htz, stretch=1)

        # BOTTOM SECTION (Measurements & Cursors)
        self.layout_bottom = QHBoxLayout()
        self.main_layout.addLayout(self.layout_bottom)

        # Measurements (8 slots)
        self.frame_meas = QFrame()
        self.frame_meas.setStyleSheet("QFrame { background-color: rgb(39, 44, 54); border-radius: 5px; } QLabel { color: white; border: none; } QComboBox { background-color: rgb(27, 29, 35); color: white; border-radius: 5px; padding: 2px; }")
        self.layout_meas = QVBoxLayout(self.frame_meas)
        
        meas_top = QHBoxLayout()
        lbl_meas_title = QLabel("MEASUREMENTS (1-8)")
        lbl_meas_title.setFont(font_title)
        meas_top.addWidget(lbl_meas_title)
        self.btn_poll_meas = QPushButton("Start Polling")
        self.btn_poll_meas.setCheckable(True)
        self.btn_poll_meas.setStyleSheet("QPushButton { background-color: rgb(52, 59, 72); color: white; padding: 5px; border-radius: 5px; } QPushButton:checked { background-color: #008000; }")
        meas_top.addWidget(self.btn_poll_meas)
        meas_top.addStretch()
        self.layout_meas.addLayout(meas_top)

        grid_meas = QGridLayout()
        self.meas_widgets = []
        for i in range(8):
            cb_src = QComboBox()
            cb_src.addItems(["CH1", "CH2", "CH3", "CH4"])
            cb_type = QComboBox()
            cb_type.addItems(["OFF", "VPP", "VMAX", "VMIN", "MEAN", "RMS", "FREQ", "RISETIME", "FALLTIME", "PDELTA"])
            lbl_res = QLabel("---")
            lbl_res.setStyleSheet("font-size: 14px; font-weight: bold; color: #00FF00;")
            lbl_res.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            row = i % 4
            col_offset = (i // 4) * 4
            
            grid_meas.addWidget(QLabel(f"M{i+1}:"), row, col_offset + 0)
            grid_meas.addWidget(cb_src, row, col_offset + 1)
            grid_meas.addWidget(cb_type, row, col_offset + 2)
            grid_meas.addWidget(lbl_res, row, col_offset + 3)
            
            self.meas_widgets.append({'src': cb_src, 'type': cb_type, 'res': lbl_res})
            
        self.layout_meas.addLayout(grid_meas)
        self.layout_bottom.addWidget(self.frame_meas, stretch=2)

        # Cursors
        self.frame_curs = QFrame()
        self.frame_curs.setStyleSheet("QFrame { background-color: rgb(39, 44, 54); border-radius: 5px; } QLabel { color: white; border: none; } QLineEdit, QComboBox { background-color: rgb(27, 29, 35); color: white; border-radius: 5px; padding: 5px; }")
        self.layout_curs = QVBoxLayout(self.frame_curs)
        lbl_curs_title = QLabel("MULTI-CURSORS")
        lbl_curs_title.setFont(font_title)
        self.layout_curs.addWidget(lbl_curs_title)

        grid_curs = QGridLayout()
        
        grid_curs.addWidget(QLabel("Cursor Set:"), 0, 0)
        self.cb_curs_set = QComboBox()
        self.cb_curs_set.addItems(["Cursor 1", "Cursor 2", "Cursor 3", "Cursor 4"])
        grid_curs.addWidget(self.cb_curs_set, 0, 1)

        grid_curs.addWidget(QLabel("State:"), 1, 0)
        self.cb_curs_state = QComboBox()
        self.cb_curs_state.addItems(["OFF", "ON"])
        grid_curs.addWidget(self.cb_curs_state, 1, 1)

        grid_curs.addWidget(QLabel("Source:"), 2, 0)
        self.cb_curs_src = QComboBox()
        self.cb_curs_src.addItems(["CH1", "CH2", "CH3", "CH4"])
        grid_curs.addWidget(self.cb_curs_src, 2, 1)

        grid_curs.addWidget(QLabel("Pos 1:"), 3, 0)
        self.le_curs1 = QLineEdit("0.0")
        grid_curs.addWidget(self.le_curs1, 3, 1)

        grid_curs.addWidget(QLabel("Pos 2:"), 4, 0)
        self.le_curs2 = QLineEdit("0.0")
        grid_curs.addWidget(self.le_curs2, 4, 1)
        
        self.btn_apply_curs = QPushButton("Apply Cursor")
        self.btn_apply_curs.setStyleSheet("QPushButton { background-color: rgb(52, 59, 72); border-radius: 5px; padding: 5px; color: white; }")
        grid_curs.addWidget(self.btn_apply_curs, 5, 0, 1, 2)

        self.lbl_curs_delta = QLabel("Delta: ---")
        self.lbl_curs_delta.setStyleSheet("font-size: 14px; font-weight: bold; color: #00FFFF;")
        grid_curs.addWidget(self.lbl_curs_delta, 6, 0, 1, 2)

        self.layout_curs.addLayout(grid_curs)
        self.layout_curs.addStretch()
        self.layout_bottom.addWidget(self.frame_curs, stretch=1)

    def connect_signals(self):
        self.btn_run_cont.clicked.connect(lambda: self.set_run_state("RUN"))
        self.btn_run_single.clicked.connect(lambda: self.set_run_state("SING"))
        self.btn_stop.clicked.connect(lambda: self.set_run_state("STOP"))
        self.btn_apply_disp.clicked.connect(self.apply_display)
        
        for ch, widgets in self.ch_widgets.items():
            widgets['apply'].clicked.connect(lambda _, c=ch: self.apply_channel(c))
            widgets['color_btn'].clicked.connect(lambda _, c=ch: self.pick_color(c))
            widgets['scale'].returnPressed.connect(lambda _, c=ch: self.apply_channel(c))
            
        self.btn_apply_ht.clicked.connect(self.apply_ht)
        self.le_timebase.returnPressed.connect(self.apply_ht)
        
        self.btn_apply_zoom.clicked.connect(self.apply_zoom)
        self.le_zoom_scale.returnPressed.connect(self.apply_zoom)
        
        self.btn_apply_curs.clicked.connect(self.apply_cursors)
        self.btn_poll_meas.toggled.connect(self.toggle_polling)

    def get_scope(self):
        if not self.equipment: return None
        return getattr(self.equipment, 'oscilloscope', None)

    def pick_color(self, ch):
        color = QColorDialog.getColor()
        if color.isValid():
            self.ch_widgets[ch]['color_btn'].setStyleSheet(f"background-color: {color.name()}; color: white; border-radius: 3px;")
            self.ch_widgets[ch]['color_val'] = color.name()

    def set_run_state(self, state):
        scope = self.get_scope()
        if scope:
            try:
                if state == "RUN":
                    scope.write("RUN")
                    self.label_status.setText("Status: RUN")
                    self.label_status.setStyleSheet("color: #00FF00; font-weight: bold; padding: 0 15px;")
                elif state == "SING":
                    scope.write("SING")
                    self.label_status.setText("Status: SINGLE")
                    self.label_status.setStyleSheet("color: #FFFF00; font-weight: bold; padding: 0 15px;")
                elif state == "STOP":
                    scope.write("STOP")
                    self.label_status.setText("Status: STOP")
                    self.label_status.setStyleSheet("color: #FF0000; font-weight: bold; padding: 0 15px;")
            except Exception as e:
                print(f"Error setting run state: {e}")

    def apply_display(self):
        scope = self.get_scope()
        if not scope: return
        try:
            state = self.cb_pers_state.currentText()
            time_val = self.cb_pers_time.currentText()
            scope.write(f"DISP:PERS:STAT {'ON' if state=='ON' else 'OFF'}")
            if state == "ON":
                if time_val == "Infinite":
                    scope.write("DISP:PERS:TIME INF")
                elif time_val == "Auto":
                    scope.write("DISP:PERS:TIME AUTO")
                else:
                    t = time_val.replace('ms', 'e-3').replace('s', '')
                    scope.write(f"DISP:PERS:TIME {t}")
        except Exception as e:
            pass

    def apply_channel(self, ch):
        scope = self.get_scope()
        if not scope: return
        w = self.ch_widgets[ch]
        state = w['state'].currentText()
        label = w['label'].text()
        scale = w['scale'].text()
        offset = w['offset'].text()
        coupling = w['coupling'].currentText()
        color = w['color_val']
        
        try:
            scope.write(f"CHAN{ch}:STAT {'ON' if state=='ON' else 'OFF'}")
            scope.write(f"CHAN{ch}:SCAL {scale}")
            scope.write(f"CHAN{ch}:OFFS {offset}")
            scope.write(f"CHAN{ch}:COUP {coupling}")
            
            if label:
                scope.write(f"CHAN{ch}:LAB '{label}'")
                scope.write(f"CHAN{ch}:LAB:STAT ON")
                
            if color:
                color = color.lstrip('#')
                r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
                scope.write(f"DISP:CMAP:TRAC{ch}:COL {r},{g},{b}")
        except Exception as e:
            pass

    def apply_ht(self):
        scope = self.get_scope()
        if not scope: return
        try:
            scope.write(f"TIM:SCAL {self.le_timebase.text()}")
            scope.write(f"TIM:POS {self.le_delay.text()}")
            scope.write(f"TRIG:A:SOUR {self.cb_trig_source.currentText()}")
            scope.write(f"TRIG:A:LEV{self.cb_trig_source.currentText()[-1] if 'CH' in self.cb_trig_source.currentText() else '1'} {self.le_trig_level.text()}")
            scope.write(f"TRIG:A:EDGE:SLOP {self.cb_trig_edge.currentText()}")
        except Exception as e:
            pass

    def apply_zoom(self):
        scope = self.get_scope()
        if not scope: return
        try:
            state = self.cb_zoom_state.currentText()
            scope.write(f"ZOOM:STAT {'ON' if state=='ON' else 'OFF'}")
            if state == "ON":
                scope.write(f"ZOOM:SCAL {self.le_zoom_scale.text()}")
                scope.write(f"ZOOM:POS {self.le_zoom_pos.text()}")
        except Exception as e:
            pass

    def apply_cursors(self):
        scope = self.get_scope()
        if not scope: return
        try:
            c_set = self.cb_curs_set.currentIndex() + 1 
            state = self.cb_curs_state.currentText()
            scope.write(f"CURS{c_set}:STAT {'ON' if state=='ON' else 'OFF'}")
            if state == "ON":
                src = self.cb_curs_src.currentText()
                scope.write(f"CURS{c_set}:SOUR {src}")
                scope.write(f"CURS{c_set}:X1P {self.le_curs1.text()}")
                scope.write(f"CURS{c_set}:X2P {self.le_curs2.text()}")
                
                try:
                    delta = scope.query(f"CURS{c_set}:XDEL?")
                    self.lbl_curs_delta.setText(f"C{c_set} Delta: {float(delta):.4e}")
                except:
                    pass
        except Exception as e:
            pass

    def toggle_polling(self, checked):
        if checked:
            self.btn_poll_meas.setText("Stop Polling")
            self.poll_timer.start(1000)
        else:
            self.btn_poll_meas.setText("Start Polling")
            self.poll_timer.stop()

    def poll_measurements(self):
        scope = self.get_scope()
        if not scope: return
        
        for i, w in enumerate(self.meas_widgets):
            m_type = w['type'].currentText()
            m_src = w['src'].currentText()
            idx = i + 1
            
            if m_type == "OFF":
                w['res'].setText("---")
                continue
                
            try:
                scope.write(f"MEAS{idx}:SOUR {m_src}")
                scope.write(f"MEAS{idx}:MAIN {m_type}")
                scope.write(f"MEAS{idx}:ON")
                
                res = scope.query(f"MEAS{idx}:RES:ACT?")
                val = float(res)
                if abs(val) > 1000 or (abs(val) < 0.01 and val != 0):
                    w['res'].setText(f"{val:.3e}")
                else:
                    w['res'].setText(f"{val:.4f}")
            except:
                w['res'].setText("ERR")
