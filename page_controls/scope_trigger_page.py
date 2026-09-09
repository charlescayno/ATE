import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *

class ScopeSettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QGridLayout(self)

        # General Data
        gb_general = QGroupBox('General Data')
        form_general = QFormLayout(gb_general)
        self.le_unit_id = QLineEdit()
        self.le_ambient_temp = QLineEdit()
        form_general.addRow('Unit ID:', self.le_unit_id)
        form_general.addRow('Ambient Temp (C):', self.le_ambient_temp)
        main_layout.addWidget(gb_general, 0, 0)

        # Scope Channels
        gb_scope = QGroupBox('Scope Channels')
        grid_scope = QGridLayout(gb_scope)
        self.chk_ch1 = QCheckBox('CH1 Name:')
        self.le_ch1_name = QLineEdit()
        self.chk_ch2 = QCheckBox('CH2 Name:')
        self.le_ch2_name = QLineEdit()
        self.chk_ch3 = QCheckBox('CH3 Name:')
        self.le_ch3_name = QLineEdit()
        self.chk_ch4 = QCheckBox('CH4 Name:')
        self.le_ch4_name = QLineEdit()
        grid_scope.addWidget(self.chk_ch1, 0, 0); grid_scope.addWidget(self.le_ch1_name, 0, 1)
        grid_scope.addWidget(self.chk_ch2, 1, 0); grid_scope.addWidget(self.le_ch2_name, 1, 1)
        grid_scope.addWidget(self.chk_ch3, 2, 0); grid_scope.addWidget(self.le_ch3_name, 2, 1)
        grid_scope.addWidget(self.chk_ch4, 3, 0); grid_scope.addWidget(self.le_ch4_name, 3, 1)
        main_layout.addWidget(gb_scope, 0, 1)

        # Trigger Controls
        gb_trigger = QGroupBox('Trigger Controls')
        form_trigger = QFormLayout(gb_trigger)
        self.cbx_trigger_channel = QComboBox()
        self.cbx_trigger_channel.addItems(['CH1', 'CH2', 'CH3', 'CH4'])
        self.le_trigger_delta = QLineEdit()
        self.cbx_auto_find = QComboBox()
        self.cbx_auto_find.addItems(['Yes', 'No'])
        self.le_settle_time = QLineEdit()
        self.le_post_capture_delay = QLineEdit()
        form_trigger.addRow('Trigger Channel:', self.cbx_trigger_channel)
        form_trigger.addRow('Trigger Delta:', self.le_trigger_delta)
        form_trigger.addRow('Auto Find Trigger:', self.cbx_auto_find)
        form_trigger.addRow('Settle Time (s):', self.le_settle_time)
        form_trigger.addRow('Post-Capture Delay (s):', self.le_post_capture_delay)
        main_layout.addWidget(gb_trigger, 1, 0)

        # Execution Options
        gb_exec = QGroupBox('Execution Options')
        form_exec = QFormLayout(gb_exec)
        self.le_discharge_pulses = QLineEdit()
        self.cbx_user_prompts = QComboBox()
        self.cbx_user_prompts.addItems(['Pre-Test Only', 'Pre-Test & Per-Capture', 'Per-Capture Only', 'None (Fully Automated)'])
        self.cbx_embed_excel = QComboBox()
        self.cbx_embed_excel.addItems(['Yes', 'No'])
        form_exec.addRow('Discharge Pulses:', self.le_discharge_pulses)
        form_exec.addRow('User Prompts:', self.cbx_user_prompts)
        form_exec.addRow('Embed in Excel:', self.cbx_embed_excel)
        main_layout.addWidget(gb_exec, 1, 1)
