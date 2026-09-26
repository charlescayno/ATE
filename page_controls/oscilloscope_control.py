import os
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class OscilloscopeControlPageHandler:
    def __init__(self, parent):
        self.parent = parent
        self.ui = parent.ui
        self.equipment = parent.equipment

        self.setup_ui()
        self.connect_signals()
        
        # Timer for polling measurements
        self.poll_timer = QTimer(self.parent)
        self.poll_timer.timeout.connect(self.poll_measurements)
        self.polling_active = False

    def setup_ui(self):
        page = self.ui.page_oscilloscope_control
        
        # Main Layout
        self.main_layout = QVBoxLayout(page)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # TITLE LABEL
        self.label_title = QLabel("MANUAL OSCILLOSCOPE CONTROL (RTO6)")
        font_title = QFont()
        font_title.setPointSize(12)
        font_title.setBold(True)
        self.label_title.setFont(font_title)
        self.label_title.setStyleSheet("color: rgb(210, 210, 210);")
        self.main_layout.addWidget(self.label_title)

        # TOP BAR (Acquisition Controls)
        self.frame_top = QFrame(page)
        self.frame_top.setStyleSheet("QFrame { background-color: rgb(39, 44, 54); border-radius: 5px; }")
        self.layout_top = QHBoxLayout(self.frame_top)
        
        self.btn_run_cont = QPushButton("Run Continuous")
        self.btn_run_single = QPushButton("Run Single")
        self.btn_stop = QPushButton("Stop")
        
        for btn in [self.btn_run_cont, self.btn_run_single, self.btn_stop]:
            btn.setMinimumHeight(40)
            btn.setStyleSheet("""
                QPushButton { background-color: rgb(52, 59, 72); border-radius: 5px; border: 2px solid rgb(52, 59, 72); color: white; padding: 5px; }
                QPushButton:hover { background-color: rgb(57, 65, 80); border: 2px solid rgb(61, 70, 86); }
                QPushButton:pressed { background-color: rgb(35, 40, 49); border: 2px solid rgb(43, 50, 61); }
            """)
            self.layout_top.addWidget(btn)
            
        self.label_status = QLabel("Status: WAIT")
        self.label_status.setStyleSheet("color: #FFA500; font-weight: bold;")
        self.layout_top.addWidget(self.label_status)
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
            lbl_state = QLabel(f"CH{ch} State:")
            cb_state = QComboBox()
            cb_state.addItems(["OFF", "ON"])
            layout.addWidget(lbl_state, 0, 0)
            layout.addWidget(cb_state, 0, 1)
            
            # Scale
            lbl_scale = QLabel("Scale (V/div):")
            le_scale = QLineEdit("1.0")
            layout.addWidget(lbl_scale, 1, 0)
            layout.addWidget(le_scale, 1, 1)
            
            # Offset
            lbl_offset = QLabel("Offset (V):")
            le_offset = QLineEdit("0.0")
            layout.addWidget(lbl_offset, 2, 0)
            layout.addWidget(le_offset, 2, 1)
            
            # Coupling
            lbl_coupling = QLabel("Coupling:")
            cb_coupling = QComboBox()
            cb_coupling.addItems(["DC", "AC", "DC50", "AC50"])
            layout.addWidget(lbl_coupling, 3, 0)
            layout.addWidget(cb_coupling, 3, 1)
            
            btn_apply = QPushButton(f"Apply CH{ch}")
            btn_apply.setStyleSheet("""
                QPushButton { background-color: rgb(52, 59, 72); border-radius: 5px; padding: 5px; color: white; }
                QPushButton:hover { background-color: rgb(57, 65, 80); }
            """)
            layout.addWidget(btn_apply, 4, 0, 1, 2)
            layout.setRowStretch(5, 1)
            
            self.ch_widgets[ch] = {
                'state': cb_state, 'scale': le_scale, 
                'offset': le_offset, 'coupling': cb_coupling,
                'apply': btn_apply
            }
            
            self.tab_vertical.addTab(tab, f"CH{ch}")
            
        self.layout_middle.addWidget(self.tab_vertical, stretch=1)

        # 2. HORIZONTAL & TRIGGER
        self.frame_ht = QFrame()
        self.frame_ht.setStyleSheet("QFrame { background-color: rgb(39, 44, 54); border-radius: 5px; } QLabel { color: white; border: none; } QLineEdit, QComboBox { background-color: rgb(27, 29, 35); color: white; border-radius: 5px; padding: 5px; }")
        self.layout_ht = QVBoxLayout(self.frame_ht)
        
        lbl_ht_title = QLabel("HORIZONTAL & TRIGGER")
        lbl_ht_title.setFont(font_title)
        self.layout_ht.addWidget(lbl_ht_title)
        
        grid_ht = QGridLayout()
        # Timebase
        grid_ht.addWidget(QLabel("Time/Div (s):"), 0, 0)
        self.le_timebase = QLineEdit("0.001")
        grid_ht.addWidget(self.le_timebase, 0, 1)
        
        # Delay
        grid_ht.addWidget(QLabel("Delay (s):"), 1, 0)
        self.le_delay = QLineEdit("0.0")
        grid_ht.addWidget(self.le_delay, 1, 1)
        
        # Source
        grid_ht.addWidget(QLabel("Trig Source:"), 2, 0)
        self.cb_trig_source = QComboBox()
        self.cb_trig_source.addItems(["CH1", "CH2", "CH3", "CH4", "EXT"])
        grid_ht.addWidget(self.cb_trig_source, 2, 1)
        
        # Level
        grid_ht.addWidget(QLabel("Trig Level (V):"), 3, 0)
        self.le_trig_level = QLineEdit("1.0")
        grid_ht.addWidget(self.le_trig_level, 3, 1)
        
        # Edge
        grid_ht.addWidget(QLabel("Trig Edge:"), 4, 0)
        self.cb_trig_edge = QComboBox()
        self.cb_trig_edge.addItems(["POS", "NEG", "EITH"])
        grid_ht.addWidget(self.cb_trig_edge, 4, 1)
        
        self.btn_apply_ht = QPushButton("Apply Horiz/Trig")
        self.btn_apply_ht.setStyleSheet("QPushButton { background-color: rgb(52, 59, 72); border-radius: 5px; padding: 5px; color: white; }")
        grid_ht.addWidget(self.btn_apply_ht, 5, 0, 1, 2)
        
        self.layout_ht.addLayout(grid_ht)
        self.layout_ht.addStretch()
        self.layout_middle.addWidget(self.frame_ht, stretch=1)

        # BOTTOM SECTION (Measurements & Cursors)
        self.layout_bottom = QHBoxLayout()
        self.main_layout.addLayout(self.layout_bottom)

        # Measurements
        self.frame_meas = QFrame()
        self.frame_meas.setStyleSheet("QFrame { background-color: rgb(39, 44, 54); border-radius: 5px; } QLabel { color: white; border: none; } QComboBox { background-color: rgb(27, 29, 35); color: white; border-radius: 5px; padding: 2px; }")
        self.layout_meas = QVBoxLayout(self.frame_meas)
        
        # Top bar of measurements
        meas_top = QHBoxLayout()
        lbl_meas_title = QLabel("MEASUREMENTS")
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
        for i in range(4):
            cb_src = QComboBox()
            cb_src.addItems(["CH1", "CH2", "CH3", "CH4"])
            cb_type = QComboBox()
            cb_type.addItems(["OFF", "VPP", "VMAX", "VMIN", "MEAN", "RMS", "FREQ", "RISETIME"])
            lbl_res = QLabel("---")
            lbl_res.setStyleSheet("font-size: 16px; font-weight: bold; color: #00FF00;")
            lbl_res.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            grid_meas.addWidget(QLabel(f"M{i+1}:"), i, 0)
            grid_meas.addWidget(cb_src, i, 1)
            grid_meas.addWidget(cb_type, i, 2)
            grid_meas.addWidget(lbl_res, i, 3)
            
            self.meas_widgets.append({'src': cb_src, 'type': cb_type, 'res': lbl_res})
            
        self.layout_meas.addLayout(grid_meas)
        self.layout_bottom.addWidget(self.frame_meas, stretch=1)

        # Cursors
        self.frame_curs = QFrame()
        self.frame_curs.setStyleSheet("QFrame { background-color: rgb(39, 44, 54); border-radius: 5px; } QLabel { color: white; border: none; } QLineEdit, QComboBox { background-color: rgb(27, 29, 35); color: white; border-radius: 5px; padding: 5px; }")
        self.layout_curs = QVBoxLayout(self.frame_curs)
        lbl_curs_title = QLabel("CURSORS")
        lbl_curs_title.setFont(font_title)
        self.layout_curs.addWidget(lbl_curs_title)

        grid_curs = QGridLayout()
        self.cb_curs_state = QComboBox()
        self.cb_curs_state.addItems(["OFF", "ON"])
        grid_curs.addWidget(QLabel("State:"), 0, 0)
        grid_curs.addWidget(self.cb_curs_state, 0, 1)

        self.cb_curs_src = QComboBox()
        self.cb_curs_src.addItems(["CH1", "CH2", "CH3", "CH4"])
        grid_curs.addWidget(QLabel("Source:"), 1, 0)
        grid_curs.addWidget(self.cb_curs_src, 1, 1)

        self.le_curs1 = QLineEdit("0.0")
        grid_curs.addWidget(QLabel("Pos 1:"), 2, 0)
        grid_curs.addWidget(self.le_curs1, 2, 1)

        self.le_curs2 = QLineEdit("0.0")
        grid_curs.addWidget(QLabel("Pos 2:"), 3, 0)
        grid_curs.addWidget(self.le_curs2, 3, 1)
        
        self.btn_apply_curs = QPushButton("Apply Cursors")
        self.btn_apply_curs.setStyleSheet("QPushButton { background-color: rgb(52, 59, 72); border-radius: 5px; padding: 5px; color: white; }")
        grid_curs.addWidget(self.btn_apply_curs, 4, 0, 1, 2)

        self.lbl_curs_delta = QLabel("Delta: ---")
        self.lbl_curs_delta.setStyleSheet("font-size: 14px; font-weight: bold; color: #00FFFF;")
        grid_curs.addWidget(self.lbl_curs_delta, 5, 0, 1, 2)

        self.layout_curs.addLayout(grid_curs)
        self.layout_curs.addStretch()
        self.layout_bottom.addWidget(self.frame_curs, stretch=1)
        
        # Push everything up
        self.main_layout.addStretch()

    def connect_signals(self):
        self.btn_run_cont.clicked.connect(lambda: self.set_run_state("RUN"))
        self.btn_run_single.clicked.connect(lambda: self.set_run_state("SING"))
        self.btn_stop.clicked.connect(lambda: self.set_run_state("STOP"))
        
        for ch, widgets in self.ch_widgets.items():
            widgets['apply'].clicked.connect(lambda _, c=ch: self.apply_channel(c))
            
        self.btn_apply_ht.clicked.connect(self.apply_ht)
        self.btn_apply_curs.clicked.connect(self.apply_cursors)
        
        self.btn_poll_meas.toggled.connect(self.toggle_polling)

    def get_scope(self):
        # Helper to get the oscilloscope safely
        if not self.equipment: return None
        return getattr(self.equipment, 'oscilloscope', None)

    def set_run_state(self, state):
        scope = self.get_scope()
        if scope:
            try:
                if state == "RUN":
                    scope.write("RUN")
                    self.label_status.setText("Status: RUN")
                    self.label_status.setStyleSheet("color: #00FF00; font-weight: bold;")
                elif state == "SING":
                    scope.write("SING")
                    self.label_status.setText("Status: SINGLE")
                    self.label_status.setStyleSheet("color: #FFFF00; font-weight: bold;")
                elif state == "STOP":
                    scope.write("STOP")
                    self.label_status.setText("Status: STOP")
                    self.label_status.setStyleSheet("color: #FF0000; font-weight: bold;")
            except Exception as e:
                print(f"Error setting run state: {e}")

    def apply_channel(self, ch):
        scope = self.get_scope()
        if not scope: return
        w = self.ch_widgets[ch]
        state = w['state'].currentText()
        scale = w['scale'].text()
        offset = w['offset'].text()
        coupling = w['coupling'].currentText()
        
        try:
            scope.write(f"CHAN{ch}:STAT {'ON' if state=='ON' else 'OFF'}")
            scope.write(f"CHAN{ch}:SCAL {scale}")
            scope.write(f"CHAN{ch}:OFFS {offset}")
            scope.write(f"CHAN{ch}:COUP {coupling}")
        except Exception as e:
            print(f"Error applying CH{ch}: {e}")

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
            print(f"Error applying Horiz/Trig: {e}")

    def apply_cursors(self):
        scope = self.get_scope()
        if not scope: return
        try:
            state = self.cb_curs_state.currentText()
            scope.write(f"CURS:STAT {'ON' if state=='ON' else 'OFF'}")
            if state == "ON":
                src = self.cb_curs_src.currentText()
                scope.write(f"CURS:SOUR {src}")
                scope.write(f"CURS:X1P {self.le_curs1.text()}")
                scope.write(f"CURS:X2P {self.le_curs2.text()}")
                # Try to read delta back
                try:
                    delta = scope.query("CURS:XDEL?")
                    self.lbl_curs_delta.setText(f"Delta: {float(delta):.4e}")
                except:
                    pass
        except Exception as e:
            print(f"Error applying Cursors: {e}")

    def toggle_polling(self, checked):
        if checked:
            self.btn_poll_meas.setText("Stop Polling")
            self.poll_timer.start(1000) # 1 sec interval
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
                # Setup measurement if not already
                scope.write(f"MEAS{idx}:SOUR {m_src}")
                scope.write(f"MEAS{idx}:MAIN {m_type}")
                scope.write(f"MEAS{idx}:ON")
                
                # Query result
                res = scope.query(f"MEAS{idx}:RES:ACT?")
                val = float(res)
                # Format nicely
                if abs(val) > 1000 or (abs(val) < 0.01 and val != 0):
                    w['res'].setText(f"{val:.3e}")
                else:
                    w['res'].setText(f"{val:.4f}")
            except Exception as e:
                w['res'].setText("ERR")
                # print(f"Error polling M{idx}: {e}")
