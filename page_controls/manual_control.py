
from sre_parse import State
import time

from enum import Enum
from PyQt5.QtCore import QCoreApplication

from numpy import source

from misc_functions.misc_functions import RepeatedTimer

from PySide2 import QtGui
from PySide2.QtGui import QValidator, QIntValidator, QDoubleValidator
from PySide2.QtCore import QTimer

from pyvisa.errors import VisaIOError

from functools import wraps

from equipment.handler import EquipmentHandler
from equipment.ac_source import *
from equipment.power_meter import *
from equipment.electronic_load import *
import inject_ui
from page_controls import pml_grid, eload_grid
from equipment.eload_specs import ELoadTypes

from user_settings.save_load import (write_to_default_config, read_from_default_config) 
from user_settings.keys import *
from misc_functions.misc_functions import *
from psu_tests.definitions import MessageType


from pd.protocol import *
from pd.pd_types import *

from sink_controllers.definitions import *
from sink_controllers.exceptions import *
from sink_controllers.epr_sink_control import STM32SinkController
from sink_controllers.pi_epr_sink import PISinkController
from sink_controllers.pat_tool import PDSinkController

from ui.ui_styles import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import MainWindow, Ui_MainWindow


class MANUAL_CONTROL_SETTINGS():
    GPIB_UPDATE_INTERVAL_MS = 500
    USBPD_UPDATE_INTERVAL_MS = 200
    UI_UPDATE_INTERVAL_MS = 500
    UPDATE_INTERVAL_MS = 500

class EQUIPMENT_ADDRESS():
    POWER_METER_SOURCE = 2
    POWER_METER_LOAD = 1
    E_LOAD = 8
    AC_SOURCE = 5

class REQUEST_TYPE():
    PD = 0
    UI = 1

class PD_REQUEST():
    RDO = 0
    EPR_ENTRY = 1
    EPR_EXIT = 2

class AC_SOURCE_REQUEST:
    NO_REQUEST = 0
    ON = 1
    OFF = 2

class UI_REQUEST():
    UPDATE_PDO_LIST = 0
    PARAM_TEXT_UPDATE = 1
    
    ########################################################################
    #                Equipment Error Handling Wrappers                     #
    ########################################################################
def power_meter_load_access(f):
    """Error handling wrapper for accessing load power meter."""
    def wrapper(*args):
        self:ManualControlPageHandler = args[0]
        # Perform the wrapped function only if the equipment is accessbile
        if self.power_meter_load_accessible:
            try:
                return f(*args)
            except (AttributeError, VisaIOError, TypeError):
                # If there is an encountered exception,
                # Set the equipment as not accessible
                self.ui_power_meter_load_update_fail()
                self.power_meter_load_accessible = False
                # Change its frame to red to indicate not accessible
                self.ui.frame_manual_control_pml.setStyleSheet(Style.red_frame)
                self.ui.frame_manual_control_pml.setEnabled(False)
    return wrapper

def power_meter_source_access(f):
    """Error handling wrapper for accessing source power meter."""
    def wrapper(*args):
        # Perform the wrapped function only if the equipment is accessbile
        self:ManualControlPageHandler = args[0]
        if self.power_meter_source_accessible:
            try:
                return f(*args)
            except (AttributeError, VisaIOError, TypeError):
                # If there is an encountered exception,
                # Set the equipment as not accessible
                self.ui_power_meter_source_update_fail()
                self.power_meter_source_accessible = False
                # Change its frame to red to indicate not accessible
                self.ui.frame_manual_control_pms.setStyleSheet(Style.red_frame)
                self.ui.frame_manual_control_pms.setEnabled(False)
    return wrapper

def ac_source_access(f):
    """Error handling wrapper for accessing ac source."""
    def wrapper(*args):
        # Perform the wrapped function only if the equipment is accessbile
        self:ManualControlPageHandler = args[0]
        if self.ac_source_accessible:
            try:
                return f(*args)
            except (AttributeError, VisaIOError, TypeError):
                # If there is an encountered exception,
                # Set the equipment as not accessible
                self.ac_source_accessible = False
                self.ui.frame_manual_control_ac_source\
                    .setStyleSheet(Style.red_frame)
                self.ui.frame_manual_control_ac_source\
                    .setEnabled(False)
    return wrapper

def eload_access(f):
    """Error handling wrapper for accessing electronic load."""
    def wrapper(*args):
        # Perform the wrapped function only if the equipment is accessbile
        self:ManualControlPageHandler = args[0]
        if self.electronic_load_accessible:
            try:
                return f(*args)
            except (AttributeError, VisaIOError, TypeError):
                # If there is an encountered exception,
                # Set the equipment as not accessible
                self.electronic_load_accessible = False
                self.ui.frame_manual_control_eload.setStyleSheet(Style.red_frame)
                self.ui.frame_manual_control_eload.setEnabled(False)
    return wrapper

# Handles the logic for the Manual Equipment Control page

def power_meter_load_2_access(f):
    def wrapper(*args):
        self = args[0]
        if self.power_meter_load_2_accessible:
            try:
                return f(*args)
            except Exception:
                self.ui_power_meter_load_2_update_fail()
                self.power_meter_load_2_accessible = False
    return wrapper

def eload_2_access(f):
    def wrapper(*args):
        self = args[0]
        if self.electronic_load_2_accessible:
            try:
                return f(*args)
            except Exception:
                self.electronic_load_2_accessible = False
                self.ui.frame_manual_control_eload_2.setStyleSheet(Style.red_frame)
                self.ui.frame_manual_control_eload_2.setEnabled(False)
    return wrapper


def power_meter_load_3_access(f):
    def wrapper(*args):
        self = args[0]
        if self.power_meter_load_3_accessible:
            try:
                return f(*args)
            except Exception:
                self.ui_power_meter_load_3_update_fail()
                self.power_meter_load_3_accessible = False
    return wrapper

def eload_3_access(f):
    def wrapper(*args):
        self = args[0]
        if self.electronic_load_3_accessible:
            try:
                return f(*args)
            except Exception:
                self.electronic_load_3_accessible = False
                self.ui.frame_manual_control_eload_3.setStyleSheet(Style.red_frame)
                self.ui.frame_manual_control_eload_3.setEnabled(False)
    return wrapper


def power_meter_load_4_access(f):
    def wrapper(*args):
        self = args[0]
        if self.power_meter_load_4_accessible:
            try:
                return f(*args)
            except Exception:
                self.ui_power_meter_load_4_update_fail()
                self.power_meter_load_4_accessible = False
    return wrapper

def eload_4_access(f):
    def wrapper(*args):
        self = args[0]
        if self.electronic_load_4_accessible:
            try:
                return f(*args)
            except Exception:
                self.electronic_load_4_accessible = False
                self.ui.frame_manual_control_eload_4.setStyleSheet(Style.red_frame)
                self.ui.frame_manual_control_eload_4.setEnabled(False)
    return wrapper
class ManualControlPageHandler():
    def __init__(self, parent):

        # Get a link from the parent
        self.parent:MainWindow = parent

        # Let the handler control the ui
        self.ui:Ui_MainWindow = parent.ui

        # Inject multi-channel UI components
        inject_ui.inject_ui(self)
        self.pml_grid = pml_grid.PmlGrid(self)
        self.pml_pout_W = {n: None for n in pml_grid.CHANNELS}

        # Bind UI elements to functionss
        self.bind_ui_elements()
        self.eload_grid = eload_grid.EloadGrid(self)

        # Use the equipment from the parent
        self.equipment:EquipmentHandler = parent.equipment

        self.setup_update_timer()
        self.discharge = pml_grid.DischargeSequencer(self.parent, self.get_discharge_loads)
        # Initializations
        self.epr_mode_enabled = False


        # USBPD Request Flags
        self.request_epr_entry_flag = False
        self.request_epr_exit_flag = False
        self.request_pdo_flag = False
        self.previous_source_caps_bytes = []

        # GPIB Equipment Flags
        self.ac_source_request = AC_SOURCE_REQUEST.NO_REQUEST
        self.power_meter_source_request_flag = False
        self.power_meter_load_request_flag = False
        self.eload_request_flag = False

        # UI  Flags
        self.update_pdo_list_flag = False
        self.update_param_text_flag = False
        self.source_caps_listed = False
        self.setup_state_saving()
    
    def bind_ui_elements(self):
        from PySide2.QtGui import QDoubleValidator
        self.validator = QDoubleValidator(0, 16777215, 6)

        # Channel 3 binds

        self.ui.lineedit_manual_control_eload_a_level_2.setValidator(self.validator)
        self.ui.lineedit_manual_control_eload_slew_rise_2.setValidator(self.validator)
        self.ui.lineedit_manual_control_eload_b_level_2.setValidator(self.validator)
        self.ui.lineedit_manual_control_eload_slew_fall_2.setValidator(self.validator)

        self.ui.lineedit_manual_control_eload_a_level_3.setValidator(self.validator)
        self.ui.lineedit_manual_control_eload_slew_rise_3.setValidator(self.validator)
        self.ui.lineedit_manual_control_eload_b_level_3.setValidator(self.validator)
        self.ui.lineedit_manual_control_eload_slew_fall_3.setValidator(self.validator)

        from PySide2.QtWidgets import QCheckBox, QLabel, QLineEdit, QSpacerItem, QSizePolicy
        from PySide2.QtCore import Qt
        # Create DC Source Ramp controls
        self.ui.chkbox_manual_control_dc_source_ramp_enable = QCheckBox(self.ui.frame_manual_control_ac_source_params)
        self.ui.chkbox_manual_control_dc_source_ramp_enable.setObjectName(u"chkbox_manual_control_dc_source_ramp_enable")
        self.ui.chkbox_manual_control_dc_source_ramp_enable.setText("Enable Ramp")
        self.ui.chkbox_manual_control_dc_source_ramp_enable.setStyleSheet("color: white;")
        self.ui.chkbox_manual_control_dc_source_ramp_enable.setVisible(False)
        self.ui.gridLayout_3.addWidget(self.ui.chkbox_manual_control_dc_source_ramp_enable, 3, 0, 1, 2)
        
        self.ui.label_manual_control_dc_source_slew_rate = QLabel(self.ui.frame_manual_control_ac_source_params)
        self.ui.label_manual_control_dc_source_slew_rate.setText("Slew Rate (V/s)")
        self.ui.label_manual_control_dc_source_slew_rate.setVisible(False)
        self.ui.gridLayout_3.addWidget(self.ui.label_manual_control_dc_source_slew_rate, 4, 0, 1, 1)

        self.ui.lineedit_manual_control_dc_source_slew_rate = QLineEdit(self.ui.frame_manual_control_ac_source_params)
        self.ui.lineedit_manual_control_dc_source_slew_rate.setText("1.0")
        self.ui.lineedit_manual_control_dc_source_slew_rate.setStyleSheet(self.ui.lineedit_manual_control_ac_source_voltage.styleSheet())
        self.ui.lineedit_manual_control_dc_source_slew_rate.setVisible(False)
        self.ui.label_manual_control_dc_source_estimated_time = QLabel(self.ui.frame_manual_control_ac_source_params)
        self.ui.label_manual_control_dc_source_estimated_time.setText("Estimated Time: N/A")
        self.ui.label_manual_control_dc_source_estimated_time.setStyleSheet("color: white; border: none; padding-top: 5px;")
        self.ui.label_manual_control_dc_source_estimated_time.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.ui.label_manual_control_dc_source_estimated_time.setVisible(False)
        self.ui.gridLayout_3.addWidget(self.ui.lineedit_manual_control_dc_source_slew_rate, 4, 1, 1, 1)
        self.ui.gridLayout_3.addWidget(self.ui.label_manual_control_dc_source_estimated_time, 5, 0, 1, 2)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.ui.gridLayout_3.addItem(spacer, 6, 0, 1, 2)

        # Output discharge controls (CCH pulse on every assigned e-load)
        params = self.ui.frame_manual_control_ac_source_params
        self.ui.chkbox_manual_control_auto_discharge = QCheckBox(params)
        self.ui.chkbox_manual_control_auto_discharge.setText("Auto-discharge on source OFF")
        self.ui.chkbox_manual_control_auto_discharge.setStyleSheet("color: white;")
        self.ui.chkbox_manual_control_auto_discharge.setChecked(True)
        self.ui.gridLayout_3.addWidget(self.ui.chkbox_manual_control_auto_discharge, 7, 0, 1, 2)
        self.ui.label_manual_control_discharge_current = QLabel(params)
        self.ui.label_manual_control_discharge_current.setText("Discharge CCH (A)")
        self.ui.gridLayout_3.addWidget(self.ui.label_manual_control_discharge_current, 8, 0, 1, 1)
        self.ui.lineedit_manual_control_discharge_current = QLineEdit(params)
        self.ui.lineedit_manual_control_discharge_current.setText("1.0")
        self.ui.lineedit_manual_control_discharge_current.setValidator(self.validator)
        self.ui.lineedit_manual_control_discharge_current.setStyleSheet(self.ui.lineedit_manual_control_ac_source_voltage.styleSheet())
        self.ui.gridLayout_3.addWidget(self.ui.lineedit_manual_control_discharge_current, 8, 1, 1, 1)
        from PySide2.QtWidgets import QPushButton
        self.ui.btn_manual_control_discharge = QPushButton(params)
        self.ui.btn_manual_control_discharge.setText("Discharge")
        self.ui.btn_manual_control_discharge.setMinimumHeight(32)
        self.ui.btn_manual_control_discharge.setStyleSheet(self.ui.btn_manual_control_ac_source_turn_off.styleSheet())
        self.ui.btn_manual_control_discharge.clicked.connect(self.discharge_output_manual)
        self.ui.gridLayout_3.addWidget(self.ui.btn_manual_control_discharge, 9, 0, 1, 2)
        self.ui.lineedit_manual_control_dc_source_slew_rate.textChanged.connect(self.update_estimated_ramp_time)
        self.ui.lineedit_manual_control_ac_source_voltage.textChanged.connect(self.update_estimated_ramp_time)

        # Setup Equipment
        self.ui.btn_manual_control_setup_equipment.clicked.\
            connect(self.initialize_gpib_equipment)
        
        # Link UI buttons to controls
        self.ui.btn_usbpdsink_request.clicked.\
            connect(lambda: self.set_pd_flags(PD_REQUEST.RDO))

        # Link EPR Mode button to EPR Mode toggle
        self.ui.btn_usbpdsink_epr_entry.clicked.\
            connect(lambda: self.set_pd_flags(PD_REQUEST.EPR_ENTRY))
        self.ui.btn_usbpdsink_epr_exit.clicked.\
            connect(lambda: self.set_pd_flags(PD_REQUEST.EPR_EXIT))

        # UI modifications can only be done in the main thread
        # Link Request Parameter change to listwidget update
        self.ui.list_usbpdsink_sourcecaps.currentItemChanged.\
            connect(lambda: self.set_ui_flags(UI_REQUEST.PARAM_TEXT_UPDATE))
        

        # Link AC Source Buttons
        self.ui.btn_manual_control_ac_source_turn_on.clicked.\
            connect(lambda: self.set_acsource_flags(AC_SOURCE_REQUEST.ON))
        self.ui.btn_manual_control_ac_source_turn_off.clicked.\
            connect(lambda: self.set_acsource_flags(AC_SOURCE_REQUEST.OFF))
        self.ui.chkbox_manual_control_ac_source_coupling.clicked.connect(self.update_ac_source_coupling)
        
        # Set validator for lineedits
        self.validator = QDoubleValidator(0, 16777215, 6)
        
        self.ui.lineedit_manual_control_ac_source_voltage.setValidator(self.validator)
        self.ui.lineedit_manual_control_ac_source_frequency.setValidator(self.validator)
        self.ui.lineedit_manual_control_eload_a_level.setValidator(self.validator)
        self.ui.lineedit_manual_control_eload_slew_rise.setValidator(self.validator)
        self.ui.lineedit_manual_control_eload_b_level.setValidator(self.validator)
        self.ui.lineedit_manual_control_eload_slew_fall.setValidator(self.validator)
        self.ui.lineedit_manual_usbpd_request_param1.setValidator(self.validator)
        self.ui.lineedit_manual_usbpd_request_param2.setValidator(self.validator)

    def set_pd_flags(self, flag_code:int):
        match flag_code:
            case PD_REQUEST.RDO:
                self.request_pdo_flag = True
            case PD_REQUEST.EPR_ENTRY:
                self.request_epr_entry_flag = True
            case PD_REQUEST.EPR_EXIT:
                self.request_epr_exit_flag = True

    def set_ui_flags(self, flag_code:int):
        match flag_code:
            case UI_REQUEST.PARAM_TEXT_UPDATE:
                self.update_param_text_flag = True
            case UI_REQUEST.UPDATE_PDO_LIST:
                self.update_pdo_list_flag = True
        
    def set_acsource_flags (self, flag_code:int):
        self.ac_source_request = flag_code

    def setup_update_timer(self):
        self.update_timer = QTimer(self.parent)
        self.update_timer.timeout.connect(self.update_service)

    def start(self):
        """ Start the manual control handler
        """

        # Use the USB PD sink defined by the handler
        # self.usbpd_sink:SinkController = self.parent.usbpd_sink
        # self.equipment.usbpd_sink.find_sink_controller_device()
        # Use the handler defined equipment roles
        self.initialize_gpib_equipment()
        self.initialize_usbpd()
        sleep(0.1)
        self.update_timer.start(MANUAL_CONTROL_SETTINGS.UPDATE_INTERVAL_MS)

    
    def stop(self):
        self.update_timer.stop()
        if self.power_meter_source is not None:
            try:
                self.power_meter_source.set_integration_timer(timer_s=self.power_meter_source_integ_timer)
            except Exception as e:
                print('Power meter source integration timer error')
            
        if self.power_meter_load is not None:
            try: 
                self.power_meter_load.set_integration_timer(timer_s=self.power_meter_load_integ_timer)
            except Exception as e:
                print('Power meter sload integration timer error')
        if self.usbpd_sink is not None:
            if self.usbpd_sink.status == SINK_STATE.USBPD_SOURCE_CONNECTED:
                self.usbpd_sink.pps_thread_cleanup()
            self.usbpd_sink.close()

    def update_service(self):
        self.usbpd_update()
        self.gpib_update()
        self.ui_update()

    ########################################################################
    #                          USBPD Functions START                       #
    ########################################################################
    
    # def setup_ui_update_timer(self):
    #     self.ui_update_timer = QTimer(self.parent)
    #     self.ui_update_timer.timeout.connect(self.ui_update)
        

    # def start_ui_update_timer(self):
    #     self.ui_update_timer.start(MANUAL_CONTROL_SETTINGS.UI_UPDATE_INTERVAL_MS)

    # def stop_ui_update_timer(self):
    #     self.ui_update_timer.stop()

    def ui_update(self):
        self.ui_powermeter_update()
        self.ui_usbpd_update()
        self.ui_acsource_update()
        self.ui_eload_update()
    
    def ui_powermeter_update(self):
        self.ui_power_meter_load_2_update()
        self.ui_power_meter_load_3_update()
        self.ui_power_meter_load_4_update()
        self.ui_power_meter_source_update()
        self.ui_power_meter_load_update()
        self.ui_pml_total_update()

    def ui_pml_total_update(self):
        accessible = {n: getattr(self, 'power_meter_load_accessible' if n == 1 else f'power_meter_load_{n}_accessible', False)
                      for n in pml_grid.CHANNELS}
        pouts = {n: p for n, p in self.pml_pout_W.items() if accessible[n] and p is not None}
        pin = getattr(self, 'Pin_W', None) if getattr(self, 'power_meter_source_accessible', False) else None
        total, eff, shares = pml_grid.compute_efficiency(pin, pouts)
        for n in pml_grid.CHANNELS:
            if accessible[n]:
                self.pml_grid.set_share(n, shares.get(n))
        self.pml_grid.set_totals(pin, total, eff, len(pouts))

    @power_meter_source_access
    def ui_power_meter_source_update(self):
        # Source power meter display
        # Set arbitrary limit to validate result (10k)
        voltage = self.power_meter_source._voltage
        if voltage < 10e3:
            self.ui.label_pms_display_a.setText(f'{voltage:.2f} V')
        current = self.power_meter_source._current
        if current < 10e3:
            self.ui.label_pms_display_b.setText(f'{current:.2f} A')
        self.Pin_W = self.power_meter_source._power
        if self.Pin_W < 10e3:
            self.ui.label_pms_display_c.setText(f'{self.Pin_W:.2f} W')
        pf = self.power_meter_source._pf*100
        if ((pf >= 0) & (pf <= 100)):
            self.ui.label_pms_display_d.setText(f'{pf:.2f}% PF')
        else:
            self.ui.label_pms_display_d.setText('None') 

    @power_meter_load_access
    def ui_power_meter_load_update(self):
        # Load power meter display
        # Set arbitrary limit to validate result (10k)
        voltage = self.power_meter_load._voltage
        if voltage < 10e3:
            self.ui.label_pml_display_a.setText(f'{voltage:.2f} V')
        current = self.power_meter_load._current
        if current < 10e3:
            self.ui.label_pml_display_b.setText(f'{current:.2f} A')
        pout_W = self.power_meter_load._power
        self.pml_pout_W[1] = pout_W if pout_W < 10e3 else None
        if pout_W < 10e3:
            self.ui.label_pml_display_c.setText(f'{pout_W:.2f} W')
            
    def ui_power_meter_load_update_fail(self):
        self.pml_pout_W[1] = None
        self.ui.label_pml_display_a.setText('None')
        self.ui.label_pml_display_b.setText('None')
        self.ui.label_pml_display_c.setText('None')
        self.ui.label_pml_display_d.setText('None')
    
    def ui_power_meter_source_update_fail(self):
        self.Pin_W = None
        self.ui.label_pms_display_a.setText('None')
        self.ui.label_pms_display_b.setText('None')
        self.ui.label_pms_display_c.setText('None')
        self.ui.label_pms_display_d.setText('None')
            
    def ui_usbpd_update(self):
        if self.update_param_text_flag:
            self.ui_request_params_text_update()
            self.update_param_text_flag = False
        
        if self.update_pdo_list_flag:
           self.ui_update_pdo_list()
           self.update_pdo_list_flag = False

    def ui_acsource_update(self):
        pass
    def ui_eload_update(self):
        self.eload_grid.refresh_status()


    ########################################################################
    #                          USBPD UI UPDATE Functions                   #
    ########################################################################
    def ui_request_params_text_update(self):
        current_row = self.ui.list_usbpdsink_sourcecaps.currentRow()
        # If none is selected, just end function
        if current_row == -1:
            return

        received_source_caps = self.usbpd_sink.received_source_caps
        # Get index of currently selected PDO
        selected_pdo:SourceCap = received_source_caps[current_row]

        # If PDO is fixed, Change label to max current
        # Set text boxes values to PDO max current 
        if selected_pdo.supply_type == SUPPLY_TYPE.FIXED:
            self.ui.label_usbpdsink_request_param1.setText("Maximum Current (mA)")
            max_current_string = str(selected_pdo.max_current_mA)
            self.ui.lineedit_manual_usbpd_request_param1.setText(max_current_string)
            self.ui.lineedit_manual_usbpd_request_param2.setText(max_current_string)
        # If PDO is augmented, change label to max voltage
        # Set text boxes to max voltage and max pps current
        elif selected_pdo.supply_type == SUPPLY_TYPE.AUGMENTED:
            
            self.ui.label_usbpdsink_request_param1.setText("Output Voltage (mV)")
            max_voltage_string = str(selected_pdo.max_voltage_mV)
            self.ui.lineedit_manual_usbpd_request_param1.setText(max_voltage_string)
                
            # The processing of max current for AVS is different from PPS
            # If augmented type is AVS, use the PDP to get the max current
            if selected_pdo.augmented_type == AUGMENTED_TYPE.EPR_AVS:
                max_current_value = round(selected_pdo.pd_power_W/(selected_pdo.max_voltage_mV/1e6))
                max_current_string = str(max_current_value)
                self.ui.lineedit_manual_usbpd_request_param2.setText(max_current_string)

            # If augmented type is PPS, directly use the max current parameter
            elif selected_pdo.augmented_type == AUGMENTED_TYPE.SPR_PPS:
                max_current_string = str(selected_pdo.max_current_mA)
                self.ui.lineedit_manual_usbpd_request_param2.setText(max_current_string)

            elif selected_pdo.augmented_type == AUGMENTED_TYPE.SPR_AVS:
                max_current_string = str(selected_pdo.max_current_mA)
                self.ui.lineedit_manual_usbpd_request_param2.setText(max_current_string)

    def ui_update_pdo_list(self):

        selected_row = self.ui.list_usbpdsink_sourcecaps.currentRow()
        self.ui.list_usbpdsink_sourcecaps.clear()
        
        if self.usbpd_sink.source_cap_count == 0:
            self.source_caps_listed = False
            self.ui.list_usbpdsink_sourcecaps.setCurrentRow(-1)
            return
        else:
            for source_cap in self.usbpd_sink.received_source_caps:
                self.ui.list_usbpdsink_sourcecaps.addItem(source_cap.text)
            self.source_caps_listed = True
            self.ui.list_usbpdsink_sourcecaps.setCurrentRow(selected_row)

    
    def usbpd_retain_selection(self):
        """Prevent deselection of items during usbpd_update"""
        pass

    ########################################################################
    #                          USBPD Functions START                       #
    ########################################################################

    def initialize_usbpd(self):
        """Initialize the USBPD settings for the Manual Control Handler"""
        # self.ui.list_usbpdsink_sourcecaps.clear()

        self.usbpd_sink = self.equipment.usbpd_sink
        if self.usbpd_sink is not None:
            self.usbpd_sink.get_status(serial_number=self.usbpd_sink.serial_number)

        # Flag to check if source caps need update
        # self.source_caps_listed = False

    def usbpd_update(self):
        """USB related processing that will run on timer. 
        Requests are only handled if a USBPD source is connected"""

        if self.usbpd_sink is None:
            return
        
        # Get the status
        usbpd_status = self.usbpd_sink.get_status(serial_number=self.usbpd_sink.serial_number)
        
        # Update Sink Status Text
        if usbpd_status == SINK_STATE.SINK_DISCONNECTED:
            self.ui.label_usbpdsink_status.setText('Sink Disconnected')
            self.ui.label_usbpdsink_status.setStyleSheet('color: red')
        else:
            self.ui.label_usbpdsink_status.setText('Sink Connected')
            self.ui.label_usbpdsink_status.setStyleSheet('color: green')
        if usbpd_status != SINK_STATE.USBPD_SOURCE_CONNECTED:
            # If source cap changes while Type C cable is disconnected, 
            # there is likely a power supply previously connected
            if self.source_caps_changed() | (self.usbpd_sink.source_caps_bytes != []):
                self.source_caps_listed = False
                self.update_pdo_list_flag = True
                self.usbpd_sink.pps_thread_cleanup()
                
                # Update USB-PD Status Text
                self.ui.label_usbpdsink_connection_status.setText('No PD Contract')
                self.ui.label_usbpdsink_connection_status.setStyleSheet('color: red')
        else:
            # Update the PDO list only if there are changes to source caps
            if (self.source_caps_listed == False) | (self.usbpd_sink.source_caps_bytes == []) | self.source_caps_changed():
                self.update_pdo_list_flag = True
                # Cleanup PPS thread if there are any
                self.usbpd_sink.pps_thread_cleanup()
                if (self.source_caps_listed == False):
                    self.usbpd_sink.vdm_initialize()
                
                # Update USB-PD Status Text
                if type(self.usbpd_sink) in [PISinkController, STM32SinkController,PDSinkController]:
                        if self.usbpd_sink.CC1_status:
                            self.ui.label_usbpdsink_connection_status.setText('USB-PD Source Connected | CC1')
                        else:
                            self.ui.label_usbpdsink_connection_status.setText('USB-PD Source Connected | CC2')
                else:
                    self.ui.label_usbpdsink_connection_status.setText('USB-PD Source Connected')
                self.ui.label_usbpdsink_connection_status.setStyleSheet('color: green')
            self.usbpd_sink.set_dfp_state()
            self.process_requests()
    
    def source_caps_changed(self)->bool:
        """Check if there are changes in the source caps"""
        
        source_caps_changed = True
        if self.previous_source_caps_bytes == self.usbpd_sink.source_caps_bytes:
            source_caps_changed = False
        
        # Store the source caps
        self.previous_source_caps_bytes = self.usbpd_sink.source_caps_bytes
        
        return source_caps_changed
        

    def process_requests(self):
        if self.request_pdo_flag:
            self.request_pdo_flag = False
            self.service_pdo_request()
        if self.request_epr_entry_flag:
            self.request_epr_entry_flag = False
            self.epr_entry()
        if self.request_epr_exit_flag:
            self.request_epr_exit_flag = False
            self.epr_exit()
            
   
    def service_pdo_request(self):
        # TODO: Checking of inputs
        # Get index of selected PDO
        list_widget_row = self.ui.list_usbpdsink_sourcecaps.currentRow()
        
        # If selected item is outside source cap list
        if (list_widget_row >= len(self.usbpd_sink.received_source_caps)) or (list_widget_row < 0):
            self.ui.list_usbpdsink_sourcecaps.setCurrentRow(-1)
            return 
        # If no PDO is selected, exit function
        if list_widget_row is None:
            return

        # Check if PDO is Fixed or Augmented
        source_cap:SourceCap = self.usbpd_sink.received_source_caps[list_widget_row]
        object_position = source_cap.object_position
        pdo_supply_type = source_cap.supply_type
        
        if self.ui.chkbox_manual_control_no_usb_suspend.isChecked():
            no_usb_suspend = 1
        else:
            no_usb_suspend = 0
        if self.ui.chkbox_manual_control_usb_comm_capable.isChecked():
            usb_comm_capable = 1
        else:
            usb_comm_capable = 0
        if self.ui.chkbox_manual_control_capability_mismatch.isChecked():
            cap_mismatch = 1
        else:
            cap_mismatch = 0
        if self.ui.chkbox_manual_control_enable_giveback.isChecked():
            give_back = 1
        else:
            give_back = 0

        if pdo_supply_type == SUPPLY_TYPE.FIXED:
            pdo_voltage_V = source_cap.voltage_mV/1000
            ilim_text_input = self.ui.lineedit_manual_usbpd_request_param2.text()
            ilim_request = int(ilim_text_input)/1000
            
            self.usbpd_sink.fpdo_request(iout_max_A=ilim_request, vbus_V=pdo_voltage_V,object_position=object_position,\
                no_usb_suspend=no_usb_suspend,usb_comm_capable=usb_comm_capable,cap_mismatch=cap_mismatch,give_back=give_back)
        elif pdo_supply_type == SUPPLY_TYPE.AUGMENTED:
            vout_text_input = self.ui.lineedit_manual_usbpd_request_param1.text()
            ilim_text_input = self.ui.lineedit_manual_usbpd_request_param2.text()

            vout_request = int(vout_text_input)/1000
            ilim_request = int(ilim_text_input)/1000
            
            pdo_augmented_type = source_cap.augmented_type

            match pdo_augmented_type:
                case AUGMENTED_TYPE.SPR_PPS:
                    self.usbpd_sink.pps_request(vout_V=vout_request, iout_max_A=ilim_request,object_position=object_position,\
                        no_usb_suspend=no_usb_suspend,usb_comm_capable=usb_comm_capable,cap_mismatch=cap_mismatch)

                case AUGMENTED_TYPE.EPR_AVS:
                    self.usbpd_sink.epr_avs_request(vout_V=vout_request, iout_max_A=ilim_request,object_position=object_position,\
                        no_usb_suspend=no_usb_suspend,usb_comm_capable=usb_comm_capable,cap_mismatch=cap_mismatch)
                    
                case AUGMENTED_TYPE.SPR_AVS:
                    self.usbpd_sink.spr_avs_request(vout_V=vout_request, iout_max_A=ilim_request,object_position=object_position,\
                        no_usb_suspend=no_usb_suspend,usb_comm_capable=usb_comm_capable,cap_mismatch=cap_mismatch)
                
                case _:
                    pass
        # Deselect the row to prevent issues
        # self.ui.list_usbpdsink_sourcecaps.setCurrentRow(-1)

    ####################################
    #       UI Updates
    ####################################
        
    
    ####################################
    #       EPR Mode
    ####################################

    def epr_entry(self):
        self.ui.list_usbpdsink_sourcecaps.setCurrentRow(-1)
        self.usbpd_sink.epr_entry()
        self.update_pdo_list_flag = True
    
    def epr_exit(self):
        self.ui.list_usbpdsink_sourcecaps.setCurrentRow(-1)
        self.usbpd_sink.epr_exit()
        self.update_pdo_list_flag = True




    ########################################################################
    #                          USBPD Functions END                         #
    ########################################################################
    
    
    ########################################################################
    #                     Equipment Functions Start                        #
    ########################################################################

    def initialize_gpib_equipment(self):
        """ Use the equipment roles that are defined in the handler"""

        self.ac_source_accessible = True
        self.power_meter_load_accessible = True
        self.power_meter_load_2_accessible = True
        self.power_meter_load_3_accessible = True
        self.power_meter_load_4_accessible = True
        self.power_meter_source_accessible = True
        self.electronic_load_accessible = True
        self.electronic_load_2_accessible = True
        self.electronic_load_3_accessible = True
        self.electronic_load_4_accessible = True

        self.ac_source = None
        self.power_meter_load = None
        self.power_meter_source = None
        self.electronic_load = None

        self.initialize_equipment_ui_frames()
        self.refresh_pml_assignment()
        self.refresh_eload_assignment()

        # TODO: Add a way to configure which equipment is to be used in the GUI
        # Currently the equipment used are based on address order
        self.initialize_ac_source()
        self.initialize_eload()
        self.initialize_power_meter_source()
        self.initialize_power_meter_load()

    
    def gpib_update(self):
        # Update the AC source (which handles DC software ramping as well)
        self.ac_source_update()
        
        # If we are actively software-ramping the DC source, skip polling other
        # equipment on the GPIB bus to avoid VisaIOError timeouts from bus flooding.
        if getattr(self, 'is_ramping', False):
            return
            
        self.power_meter_load_update()
        self.power_meter_load_2_update()
        self.power_meter_load_3_update()
        self.power_meter_load_4_update()
        
        self.power_meter_source_update()
        
        self.eload_update()
        if hasattr(self, 'eload_2_update'): self.eload_2_update()
        if hasattr(self, 'eload_3_update'): self.eload_3_update()
        if hasattr(self, 'eload_4_update'): self.eload_4_update()

    def refresh_pml_assignment(self):
        """Grey out load power meter tiles that have no meter assigned in Equipment Setup."""
        for n in pml_grid.CHANNELS:
            assigned = getattr(self.equipment, f'power_meter_load_{n}', None) is not None
            self.pml_grid.set_assigned(n, assigned)
            if not assigned:
                setattr(self, 'power_meter_load_accessible' if n == 1 else f'power_meter_load_{n}_accessible', False)
                self.pml_pout_W[n] = None

    def refresh_eload_assignment(self):
        """Grey out e-load tiles with no load assigned; fill the mode list of the assigned ones."""
        for n in eload_grid.CHANNELS:
            assigned = getattr(self.equipment, f'electronic_load_{n}', None) is not None
            if not assigned:
                setattr(self, 'electronic_load_accessible' if n == 1 else f'electronic_load_{n}_accessible', False)
            self.eload_grid.set_assigned(n, assigned)

    @power_meter_load_2_access
    def power_meter_load_2_update(self):
        self.equipment.power_meter_load_2.update_basic_params()

    @power_meter_load_3_access
    def power_meter_load_3_update(self):
        self.equipment.power_meter_load_3.update_basic_params()

    @power_meter_load_4_access
    def power_meter_load_4_update(self):
        self.equipment.power_meter_load_4.update_basic_params()

    def get_discharge_loads(self):
        loads = []
        for n in (1, 2, 3, 4):
            ld = getattr(self.equipment, f'electronic_load_{n}', None)
            if ld is not None:
                loads.append((f'E-Load CH{n}', ld))
        return loads

    def discharge_current_A(self):
        try:
            return max(0.0, float(self.ui.lineedit_manual_control_discharge_current.text()))
        except ValueError:
            return 1.0

    def start_output_discharge(self, reason: str):
        self.discharge.start(self.discharge_current_A(), reason)

    def discharge_output_manual(self):
        self.is_ramping = False
        source = getattr(self, 'ac_source', None)
        if source is not None:
            try:
                source.turn_off()
            except Exception as e:
                print(f"[DISCHARGE] source OFF failed: {e}")
        self.start_output_discharge("Discharge button")

    def initialize_equipment_ui_frames(self):
        """Set the frames of the equipment to normal"""
        ui = self.ui

        ac_source_frame = ui.frame_manual_control_ac_source
        eload_frame = ui.frame_manual_control_eload
        pml_frame  = ui.frame_manual_control_pml
        pms_frame  = ui.frame_manual_control_pms
        
        ac_source_frame.setEnabled(True)
        eload_frame.setEnabled(True)
        pml_frame.setEnabled(True)
        pms_frame.setEnabled(True)

        ac_source_frame.setStyleSheet(Style.normal_frame)
        eload_frame.setStyleSheet(Style.normal_frame)
        pml_frame.setStyleSheet(Style.normal_frame)
        pms_frame.setStyleSheet(Style.normal_frame)


    ########################################################################
    #                  Equipment Initialization Functions                  #
    ########################################################################
    @ac_source_access
    def initialize_ac_source(self):
        self.ac_source = self.equipment.ac_source
        
        # Reset UI back to default (AC Source) just in case it was previously set to DC Source
        self.ui.label_manual_control_ac_source.setText("AC SOURCE")
        self.ui.label_manual_control_ac_source_frequency.setVisible(True)
        self.ui.lineedit_manual_control_ac_source_frequency.setVisible(True)
        self.ui.chkbox_manual_control_ac_source_coupling.setVisible(True)
        self.ui.label_manual_control_ac_source_frequency.setEnabled(True)
        self.ui.lineedit_manual_control_ac_source_frequency.setEnabled(True)

        self.ui.chkbox_manual_control_dc_source_ramp_enable.setVisible(False)
        self.ui.label_manual_control_dc_source_slew_rate.setVisible(False)
        self.ui.lineedit_manual_control_dc_source_slew_rate.setVisible(False)
        self.ui.label_manual_control_dc_source_estimated_time.setVisible(False)
        
        if hasattr(self.equipment, 'dc_source') and self.equipment.dc_source is not None:
            if 'SL1000' in self.equipment.dc_source.model or 'Magna-Power' in getattr(self.equipment.dc_source, 'manufacturer', ''):
                self.ac_source = self.equipment.dc_source
                # Modify UI for DC Source
                self.ui.label_manual_control_ac_source.setText("DC SOURCE")
                self.ui.label_manual_control_ac_source_frequency.setVisible(False)
                self.ui.lineedit_manual_control_ac_source_frequency.setVisible(False)
                self.ui.chkbox_manual_control_ac_source_coupling.setChecked(True)
                self.ui.chkbox_manual_control_ac_source_coupling.setVisible(False)
                self.ui.label_manual_control_ac_source_frequency.setEnabled(False)
                self.ui.lineedit_manual_control_ac_source_frequency.setEnabled(False)
                self.ac_source.coupling = AC_SOURCE_COUPLING.DC

                self.ui.chkbox_manual_control_dc_source_ramp_enable.setVisible(True)
                self.ui.label_manual_control_dc_source_slew_rate.setVisible(True)
                self.ui.lineedit_manual_control_dc_source_slew_rate.setVisible(True)
                self.ui.label_manual_control_dc_source_estimated_time.setVisible(True)

    @eload_access
    def initialize_eload(self):
        self.electronic_load:ElectronicLoadModule = self.equipment.electronic_load_1
        self.electronic_load.set_active_level(1)
    
    @power_meter_source_access
    def initialize_power_meter_source(self):
        self.power_meter_source = self.equipment.power_meter_source
        self.power_meter_source_integ_timer = self.power_meter_source.get_integration_timer()
        self.power_meter_source.set_integration_timer(timer_s=0)


    @power_meter_load_access
    def initialize_power_meter_load(self):
        self.power_meter_load = self.equipment.power_meter_load_1
        self.power_meter_load_integ_timer = self.power_meter_load.get_integration_timer()
        self.power_meter_load.set_integration_timer(timer_s=0)


    ########################################################################
    #                  Equipment Update Functions                          #
    ########################################################################
    @power_meter_load_access
    def power_meter_load_update(self):
        """ Update power meter parameters
        
        Wrapped with error handling
        """
        self.power_meter_load.update_basic_params()

    @power_meter_source_access
    def power_meter_source_update(self):
        """ Update power meter parameters
        
        Wrapped with error handling
        """
        self.power_meter_source.update_basic_params()

    @ac_source_access
    def ac_source_update(self):
        """ Update AC source, do request.
        
        Wrapped with error handling"""
        # Do the request
        if not self.ac_source_request == AC_SOURCE_REQUEST.NO_REQUEST:
            self.ac_source_request_service()    
            self.ac_source_request = AC_SOURCE_REQUEST.NO_REQUEST
            
        # Software ramp execution
        if getattr(self, 'is_ramping', False):
            try:
                if self.current_ramp_voltage < self.target_ramp_voltage:
                    self.current_ramp_voltage += self.ramp_step_v
                    if self.current_ramp_voltage >= self.target_ramp_voltage:
                        self.current_ramp_voltage = self.target_ramp_voltage
                        self.is_ramping = False
                elif self.current_ramp_voltage > self.target_ramp_voltage:
                    self.current_ramp_voltage -= self.ramp_step_v
                    if self.current_ramp_voltage <= self.target_ramp_voltage:
                        self.current_ramp_voltage = self.target_ramp_voltage
                        self.is_ramping = False
                self.ac_source.set_voltage_with_coupling(voltage=self.current_ramp_voltage, coupling=self.ac_source.coupling)
                
                # Throttle log to once per second
                current_time = time.time()
                if current_time - getattr(self, 'last_ramp_log_time', 0.0) >= 1.0 or not self.is_ramping:
                    print(f"[DC_SOURCE] Ramping Output: {self.current_ramp_voltage:.2f} V / {self.target_ramp_voltage:.2f} V")
                    self.last_ramp_log_time = current_time
            except Exception as e:
                print(f"[ERROR] Exception during software ramp: {str(e)}")
                self.is_ramping = False

        # Indicate the state of the AC source output by changing the frame color
        self.ac_source.update_status()
        if self.ac_source.output_status == AC_SOURCE_STATUS.ON:
                self.ui.frame_manual_control_ac_source_buttons.setStyleSheet(Style.green_frame)
        else:
            self.ui.frame_manual_control_ac_source_buttons.setStyleSheet(Style.red_frame)
    
    @eload_access
    def eload_update(self):
        """ Update eload
        
        Currently used only for pinging eload
        """
        self.electronic_load.get_id()


    ########################################################################
#                         Equipment Functions Start                        #
    ########################################################################

    def ac_source_request_service(self):
        match self.ac_source_request:
            case AC_SOURCE_REQUEST.NO_REQUEST:
                return
            case AC_SOURCE_REQUEST.ON:
                self.ac_source_power_on()
            case AC_SOURCE_REQUEST.OFF:
                self.is_ramping = False
                self.ac_source.turn_off()
                if self.ui.chkbox_manual_control_auto_discharge.isChecked():
                    self.start_output_discharge("source OFF")

    def ac_source_power_on(self):
        if (self.ui.lineedit_manual_control_ac_source_voltage.text() == ''):
            self.parent.msg_box_info(
                title="AC Source Error",
                message=f"Please enter the input voltage.",
                message_type = MessageType.INFO
                )
            return
    
        vin_V = rounded_float(self.ui.lineedit_manual_control_ac_source_voltage.text())
        self.update_ac_source_coupling()
        
        if self.ac_source.coupling == AC_SOURCE_COUPLING.AC:    
            if (self.ui.lineedit_manual_control_ac_source_frequency.text() == ''):
                if vin_V >= 180:
                    freq = 50
                else:
                    freq = 60
                self.ui.lineedit_manual_control_ac_source_frequency.setText(f'{freq:g}')
            else:
                freq = rounded_float(self.ui.lineedit_manual_control_ac_source_frequency.text())
            self.ac_source.frequency = freq
        elif 'Magna-Power' in getattr(self.ac_source, 'manufacturer', '') or 'SL1000' in getattr(self.ac_source, 'model', ''):
            # Prompt user to disengage discharge resistor
            res = self.parent.msg_box_pick(
                title="Discharge Resistor Check",
                message="<h2>⚠️ ATTENTION</h2><br><span style='font-size: 14pt; font-weight: bold;'>Is the discharge resistor disengaged?</span><br><br><span style='font-size: 12pt; color: #cc0000;'>Please disengage it before powering up.</span>"
            )
            if res != 1024: # QMessageBox.Ok
                return
            
            # Apply Slew rate if enabled
            if hasattr(self.ui, 'chkbox_manual_control_dc_source_ramp_enable') and self.ui.chkbox_manual_control_dc_source_ramp_enable.isChecked():
                slew_rate = self.ui.lineedit_manual_control_dc_source_slew_rate.text()
                if slew_rate != '':
                    if hasattr(self.ac_source, 'set_slew_rate'):
                        self.ac_source.set_slew_rate(slew_rate)
                    else:
                        # Magna-Power SL-series doesn't natively support VOLT:SLEW, so we must software ramp.
                        interval_s = MANUAL_CONTROL_SETTINGS.UPDATE_INTERVAL_MS / 1000.0
                        self.ramp_step_v = float(slew_rate) * interval_s
                        try:
                            self.current_ramp_voltage = float(self.ac_source.voltage)
                        except (ValueError, TypeError, AttributeError):
                            self.current_ramp_voltage = 0.0
                        self.target_ramp_voltage = float(vin_V)
                        
                        # Only enable ramping if we actually have distance to cover
                        if abs(self.target_ramp_voltage - self.current_ramp_voltage) > self.ramp_step_v:
                            self.is_ramping = True
                            self.ac_source.set_voltage_with_coupling(voltage=self.current_ramp_voltage, coupling=self.ac_source.coupling)
                            self.ac_source.turn_on()
                            return
        
        self.ac_source.set_voltage_with_coupling(voltage= vin_V, coupling= self.ac_source.coupling) 
        self.ac_source.turn_on() 
        
    def update_ac_source_coupling(self):
        if self.ui.chkbox_manual_control_ac_source_coupling.isChecked():
            self.ui.chkbox_manual_control_ac_source_coupling.setText(QCoreApplication.translate("MainWindow", 'DC', None))
            self.ui.lineedit_manual_control_ac_source_frequency.setEnabled(False)
            self.ui.label_manual_control_ac_source_frequency.setEnabled(False)
            self.ac_source.coupling = AC_SOURCE_COUPLING.DC
        else:
            self.ui.chkbox_manual_control_ac_source_coupling.setText(QCoreApplication.translate("MainWindow", 'AC', None))
            self.ui.lineedit_manual_control_ac_source_frequency.setEnabled(True)
            self.ui.label_manual_control_ac_source_frequency.setEnabled(True)
            self.ac_source.coupling = AC_SOURCE_COUPLING.AC
        

    def update_estimated_ramp_time(self):
        try:
            target_voltage = float(self.ui.lineedit_manual_control_ac_source_voltage.text())
            slew_rate = float(self.ui.lineedit_manual_control_dc_source_slew_rate.text())
            if slew_rate > 0:
                time_s = target_voltage / slew_rate
                self.ui.label_manual_control_dc_source_estimated_time.setText(f"Estimated Time: {time_s:.2f} s")
            else:
                self.ui.label_manual_control_dc_source_estimated_time.setText("Estimated Time: N/A")
        except ValueError:
            self.ui.label_manual_control_dc_source_estimated_time.setText("Estimated Time: N/A")

    # Electronic Load Functions
    @eload_2_access
    def eload_2_update(self):
        """ Update eload
        
        Currently used only for pinging eload
        """
        self.equipment.electronic_load_2.get_id()


    ########################################################################
#                         Equipment Functions Start                        #
    ########################################################################

    @power_meter_load_2_access
    def ui_power_meter_load_2_update(self):
        # Load power meter display
        # Set arbitrary limit to validate result (10k)
        voltage = self.equipment.power_meter_load_2._voltage
        if voltage < 10e3:
            self.ui.label_pml_display_a_2.setText(f'{voltage:.2f} V')
        current = self.equipment.power_meter_load_2._current
        if current < 10e3:
            self.ui.label_pml_display_b_2.setText(f'{current:.2f} A')
        pout_W = self.equipment.power_meter_load_2._power
        self.pml_pout_W[2] = pout_W if pout_W < 10e3 else None
        if pout_W < 10e3:
            self.ui.label_pml_display_c_2.setText(f'{pout_W:.2f} W')
            
    def ui_power_meter_load_2_update_fail(self):
        self.pml_pout_W[2] = None
        self.ui.label_pml_display_a_2.setText('None')
        self.ui.label_pml_display_b_2.setText('None')
        self.ui.label_pml_display_c_2.setText('None')
        self.ui.label_pml_display_d_2.setText('None')
    
    @eload_3_access
    def eload_3_update(self):
        """ Update eload
        
        Currently used only for pinging eload
        """
        self.equipment.electronic_load_3.get_id()


    ########################################################################
#                         Equipment Functions Start                        #
    ########################################################################

    @power_meter_load_3_access
    def ui_power_meter_load_3_update(self):
        # Load power meter display
        # Set arbitrary limit to validate result (10k)
        voltage = self.equipment.power_meter_load_3._voltage
        if voltage < 10e3:
            self.ui.label_pml_display_a_3.setText(f'{voltage:.2f} V')
        current = self.equipment.power_meter_load_3._current
        if current < 10e3:
            self.ui.label_pml_display_b_3.setText(f'{current:.2f} A')
        pout_W = self.equipment.power_meter_load_3._power
        self.pml_pout_W[3] = pout_W if pout_W < 10e3 else None
        if pout_W < 10e3:
            self.ui.label_pml_display_c_3.setText(f'{pout_W:.2f} W')
            
    def ui_power_meter_load_3_update_fail(self):
        self.pml_pout_W[3] = None
        self.ui.label_pml_display_a_3.setText('None')
        self.ui.label_pml_display_b_3.setText('None')
        self.ui.label_pml_display_c_3.setText('None')
        self.ui.label_pml_display_d_3.setText('None')
    
    @eload_4_access
    def eload_4_update(self):
        """ Update eload
        
        Currently used only for pinging eload
        """
        self.equipment.electronic_load_4.get_id()


    ########################################################################
#                         Equipment Functions Start                        #
    ########################################################################

    @power_meter_load_4_access
    def ui_power_meter_load_4_update(self):
        # Load power meter display
        # Set arbitrary limit to validate result (10k)
        voltage = self.equipment.power_meter_load_4._voltage
        if voltage < 10e3:
            self.ui.label_pml_display_a_4.setText(f'{voltage:.2f} V')
        current = self.equipment.power_meter_load_4._current
        if current < 10e3:
            self.ui.label_pml_display_b_4.setText(f'{current:.2f} A')
        pout_W = self.equipment.power_meter_load_4._power
        self.pml_pout_W[4] = pout_W if pout_W < 10e3 else None
        if pout_W < 10e3:
            self.ui.label_pml_display_c_4.setText(f'{pout_W:.2f} W')
            
    def ui_power_meter_load_4_update_fail(self):
        self.pml_pout_W[4] = None
        self.ui.label_pml_display_a_4.setText('None')
        self.ui.label_pml_display_b_4.setText('None')
        self.ui.label_pml_display_c_4.setText('None')
        self.ui.label_pml_display_d_4.setText('None')
    

    def setup_state_saving(self):
        import json
        import os
        from PySide2.QtWidgets import QLineEdit, QComboBox, QCheckBox
        self.settings_file = "manual_control_settings.json"
        
        self.state_widgets = []
        self.state_keys = {}
        names = {}
        for owner in (self, self.ui):
            for attr, value in vars(owner).items():
                if isinstance(value, (QLineEdit, QComboBox, QCheckBox)):
                    names.setdefault(id(value), attr)
        candidates = []
        for t in (QLineEdit, QComboBox, QCheckBox):
            candidates += self.ui.page_manual_control.findChildren(t)
        candidates += self.pml_grid.dialog_state_widgets() + self.eload_grid.dialog_state_widgets()
        for widget in candidates:
                obj_name = widget.objectName()
                if not obj_name or widget in self.state_widgets: continue
                self.state_widgets.append(widget)
                self.state_keys[id(widget)] = names.get(id(widget), obj_name)
                
                if isinstance(widget, QLineEdit):
                    widget.editingFinished.connect(self.save_manual_settings)
                elif isinstance(widget, QComboBox):
                    widget.currentIndexChanged.connect(self.save_manual_settings)
                elif isinstance(widget, QCheckBox):
                    widget.toggled.connect(self.save_manual_settings)
                
        self.load_manual_settings()

    def save_manual_settings(self, *args):
        import json
        from PySide2.QtWidgets import QLineEdit, QComboBox, QCheckBox
        state = {}
        for widget in self.state_widgets:
            obj_name = self.state_keys.get(id(widget), widget.objectName())
            if isinstance(widget, QLineEdit):
                state[obj_name] = widget.text()
            elif isinstance(widget, QComboBox):
                state[obj_name] = widget.currentIndex()
            elif isinstance(widget, QCheckBox):
                state[obj_name] = widget.isChecked()
                
        try:
            with open(self.settings_file, "w", encoding='utf-8') as f:
                json.dump(state, f, indent=4)
        except Exception as e:
            print(f"Failed to save manual settings: {e}")

    def load_manual_settings(self):
        import json
        import os
        from PySide2.QtWidgets import QLineEdit, QComboBox, QCheckBox
        if not os.path.exists(self.settings_file):
            return
            
        try:
            with open(self.settings_file, "r", encoding='utf-8') as f:
                state = json.load(f)
                
            for widget in self.state_widgets:
                obj_name = self.state_keys.get(id(widget), widget.objectName())
                if obj_name in state:
                    val = state[obj_name]
                    widget.blockSignals(True)
                    if isinstance(widget, QLineEdit):
                        widget.setText(str(val))
                    elif isinstance(widget, QComboBox):
                        widget.setCurrentIndex(int(val))
                    elif isinstance(widget, QCheckBox):
                        widget.setChecked(bool(val))
                    widget.blockSignals(False)
        except Exception as e:
            print(f"Failed to load manual settings: {e}")
