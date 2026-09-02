
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
class ManualControlPageHandler():
    def __init__(self, parent):

        # Get a link from the parent
        self.parent:MainWindow = parent

        # Let the handler control the ui
        self.ui:Ui_MainWindow = parent.ui

        # Bind UI elements to functionss
        self.bind_ui_elements()

        # Use the equipment from the parent
        self.equipment:EquipmentHandler = parent.equipment

        self.setup_update_timer()
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
    
    def bind_ui_elements(self):
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
        
        # E-Load Buttons       
        self.ui.btn_manual_control_eload_turn_on.clicked.connect(
                self.eload_turn_on)
        self.ui.btn_manual_control_eload_set_A.clicked.connect(
            self.eload_set_level_A)
        self.ui.btn_manual_control_eload_set_B.clicked.connect(
            self.eload_set_level_B)
        self.ui.btn_manual_control_eload_set_slew.clicked.connect(
            self.eload_set_slew)
        self.ui.btn_manual_control_eload_turn_off.clicked.connect(
            self.eload_turn_off)
        self.ui.btn_manual_control_eload_a_b_swap.clicked.connect(
            self.eload_swap_active_level)
        self.ui.cbx_manual_control_eload_type.currentIndexChanged.connect(
            self.update_eload_settings)
        

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
        self.ui_power_meter_source_update()
        self.ui_power_meter_load_update()

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
        self.Pout_W = self.power_meter_load._power
        if self.Pout_W < 10e3:
            self.ui.label_pml_display_c.setText(f'{self.Pout_W:.2f} W')
        if (self.Pin_W > 0) and (self.Pout_W < 10e3) and (self.Pin_W < 10e3):
            eff = self.Pout_W/self.Pin_W*100
            self.ui.label_pml_display_d.setText(f'{eff:.2f}% Eff')
        else:
            self.ui.label_pml_display_d.setText('None')
            
    def ui_power_meter_load_update_fail(self):
        self.ui.label_pml_display_a.setText('None')
        self.ui.label_pml_display_b.setText('None')
        self.ui.label_pml_display_c.setText('None')
        self.ui.label_pml_display_d.setText('None')
    
    def ui_power_meter_source_update_fail(self):
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
        pass


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
        self.power_meter_source_accessible = True
        self.electronic_load_accessible = True

        self.ac_source = None
        self.power_meter_load = None
        self.power_meter_source = None
        self.electronic_load = None

        self.initialize_equipment_ui_frames()

        # TODO: Add a way to configure which equipment is to be used in the GUI
        # Currently the equipment used are based on address order
        self.initialize_ac_source()
        self.initialize_eload()
        self.initialize_power_meter_source()
        self.initialize_power_meter_load()

    
    def gpib_update(self):
        self.power_meter_load_update()
        self.power_meter_source_update()
        self.ac_source_update()
        self.eload_update()
    
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

    @eload_access
    def initialize_eload(self):
        self.electronic_load:ElectronicLoadModule = self.equipment.electronic_load_1
        self.electronic_load.set_active_level(1)
        self.update_eload_modes_cbx()
    
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
                self.ac_source.turn_off()

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
        
    # Electronic Load Functions
    @eload_access
    def update_eload_modes_cbx(self):
        """Populate the eload modes based on the current Eload model"""
        modes = self.electronic_load.load_modes

        self.ui.cbx_manual_control_eload_type.clear()
        self.ui.cbx_manual_control_eload_type.addItems(modes)

        # If the eload is multi channel, the A/B button is not available
        if self.electronic_load.multi_channel:
            self.ui.frame_manual_control_eload_b.setVisible(False)
        else:
            self.ui.frame_manual_control_eload_b.setVisible(True)

    @eload_access
    def eload_turn_off(self):
        """Turn off the electronic load."""
        self.electronic_load.turn_off()

    @eload_access
    def eload_turn_on(self):
        """Turn on the electronic load"""
        self.electronic_load.turn_on()

    @eload_access
    def eload_set_level_A(self):
        # Take the inputs first
        try:
            load_mode = self.ui.cbx_manual_control_eload_type.currentText()

            load_a_level_txt = self.ui.lineedit_manual_control_eload_a_level.text()
        
            load_a_level = round(float(load_a_level_txt),6)
            
            vout_V = self.electronic_load.voltage
            if abs(vout_V) < 0.5:
                vout_V = self.electronic_load.crh_max_v
                
        except Exception as e:
            print(e)
            return        
        
        match load_mode:
            case ELoadTypes.CC:
                iout_a_A = load_a_level
            case ELoadTypes.CR:
                # If input is 0, assume no input (open circuit, max cr) instead of short circuit
                if load_a_level == 0:
                    iout_a_A = 0
                else:
                    iout_a_A = vout_V/load_a_level
            case ELoadTypes.CP:
                iout_a_A = load_a_level/vout_V
            case ELoadTypes.CV:
                vout_V = load_a_level
                iout_a_A = None
            case _:
                return
        self.electronic_load.set_active_level(1)
        self.electronic_load.set_load(vout_V=vout_V, iout_A=iout_a_A, mode=load_mode)
        
    @eload_access                 
    def eload_set_level_B(self):
        # Take the inputs first
        try:
            load_mode = self.ui.cbx_manual_control_eload_type.currentText()

            load_b_level_txt = self.ui.lineedit_manual_control_eload_b_level.text()
            
            load_b_level = round(float(load_b_level_txt),6)
            
            vout_V = self.electronic_load.voltage
            if abs(vout_V) < 0.5:
                vout_V = self.electronic_load.crh_max_v
                
        except Exception as e:
            print(e)
            return 
        
        match load_mode:
            case ELoadTypes.CC:
                iout_b_A = load_b_level
            case ELoadTypes.CR:
                # If input is 0, assume no input (open circuit, max cr) instead of short circuit
                if load_b_level == 0:
                    iout_b_A = 0
                else:
                    iout_b_A = vout_V/load_b_level
            case ELoadTypes.CP:
                iout_b_A = load_b_level/vout_V
            case ELoadTypes.CV:
                vout_V = load_b_level
                iout_b_A = None
            case _:
                return
        self.electronic_load.set_active_level(2)
        self.electronic_load.set_load(vout_V=vout_V, iout_A=iout_b_A, mode=load_mode)
   
    @eload_access   
    def eload_set_slew(self):
        # Take the inputs first
        try:
            load_mode = self.ui.cbx_manual_control_eload_type.currentText()

            load_rise_txt = self.ui.lineedit_manual_control_eload_slew_rise.text()
            load_fall_txt = self.ui.lineedit_manual_control_eload_slew_fall.text()
            
            load_rise = round(float(load_rise_txt)/1000,6)
            load_fall = round(float(load_fall_txt)/1000,6)
            
        except Exception as e:
            print(e)
            return 

        match load_mode:
            case ELoadTypes.CC:
                self.electronic_load.set_cc_static_slew(load_rise,load_fall)
            case ELoadTypes.CR:
                self.electronic_load.set_cr_slew(load_rise,load_fall)
          
    @eload_access   
    def eload_swap_active_level(self):
        vout_V = self.electronic_load.voltage
        if abs(vout_V) < 0.5:
            vout_V = self.electronic_load.crh_max_v
        if self.electronic_load._active_level == '1':
            self.eload_set_level_B()
        else:
            self.eload_set_level_A()
        
        # self.electronic_load.get_active_level()
        # load_mode = self.ui.cbx_manual_control_eload_type.currentText()
        # vout_V = self.electronic_load.voltage
        # if abs(vout_V) < 0.5:
        #     vout_V = self.electronic_load.crh_max_v
        # match load_mode:
        #     case ELoadTypes.CC:
        #         if self.electronic_load._active_level == '1':
        #             self.electronic_load.set_active_level(2)
        #             self.electronic_load.set_load(vout_V=vout_V, iout_A=self.electronic_load.cc_static_l2, mode=load_mode)
        #         else:
        #             self.electronic_load.set_active_level(1)
        #             self.electronic_load.set_load(vout_V=vout_V, iout_A=self.electronic_load.cc_static_l1, mode=load_mode)
        #     case ELoadTypes.CR:
        #         if self.electronic_load._active_level == '1':
        #             self.electronic_load.set_active_level(2)
        #             self.electronic_load.set_load(vout_V=vout_V, iout_A=(vout_V/self.electronic_load.cr_l2), mode=load_mode)
        #         else:
        #             self.electronic_load.set_active_level(1)
        #             self.electronic_load.set_load(vout_V=vout_V, iout_A=(vout_V/self.electronic_load.cr_l1), mode=load_mode)
    
    def update_eload_settings(self):
        self.ui.label_manual_control_electronic_load_rise.setText('Rise')
        self.ui.label_manual_control_eload_slew_rise_unit.setText('mA / µs')
        self.ui.label_manual_control_eload_slew_fall_unit.setText('mA / µs')
        self.ui.lineedit_manual_control_eload_slew_rise.setText('150')
        self.ui.lineedit_manual_control_eload_slew_fall.setText('150')
        
        if self.ui.cbx_manual_control_eload_type.currentText() == ELoadTypes.CC:
            self.ui.label_manual_control_eload_a_level_unit.setText('A')
            self.ui.label_manual_control_eload_b_level_unit.setText('A')
            self.ui.label_manual_control_electronic_load_rise.setEnabled(True)
            self.ui.lineedit_manual_control_eload_slew_rise.setEnabled(True)
            self.ui.label_manual_control_eload_slew_rise_unit.setEnabled(True)
            self.ui.label_manual_control_electronic_load_fall.setEnabled(True)
            self.ui.lineedit_manual_control_eload_slew_fall.setEnabled(True)
            self.ui.label_manual_control_eload_slew_fall_unit.setEnabled(True)
        elif self.ui.cbx_manual_control_eload_type.currentText() == ELoadTypes.CR:
            self.ui.label_manual_control_eload_a_level_unit.setText('Ω')
            self.ui.label_manual_control_eload_b_level_unit.setText('Ω')
            if not self.electronic_load.cr_slew_available:
                self.ui.label_manual_control_electronic_load_rise.setEnabled(False)
                self.ui.lineedit_manual_control_eload_slew_rise.setEnabled(False)
                self.ui.label_manual_control_eload_slew_rise_unit.setEnabled(False)
                self.ui.label_manual_control_electronic_load_fall.setEnabled(False)
                self.ui.lineedit_manual_control_eload_slew_fall.setEnabled(False)
                self.ui.label_manual_control_eload_slew_fall_unit.setEnabled(False)
            else:
                self.ui.label_manual_control_electronic_load_rise.setEnabled(True)
                self.ui.lineedit_manual_control_eload_slew_rise.setEnabled(True)
                self.ui.label_manual_control_eload_slew_rise_unit.setEnabled(True)
                self.ui.label_manual_control_electronic_load_fall.setEnabled(True)
                self.ui.lineedit_manual_control_eload_slew_fall.setEnabled(True)
                self.ui.label_manual_control_eload_slew_fall_unit.setEnabled(True)
        elif self.ui.cbx_manual_control_eload_type.currentText() == ELoadTypes.CV:
            self.ui.label_manual_control_eload_a_level_unit.setText('V')
            self.ui.label_manual_control_eload_b_level_unit.setText('V')
            self.ui.label_manual_control_electronic_load_rise.setEnabled(True)
            self.ui.lineedit_manual_control_eload_slew_rise.setEnabled(True)
            self.ui.label_manual_control_eload_slew_rise_unit.setEnabled(True)
            self.ui.label_manual_control_eload_slew_rise_unit.setText('A')
            self.ui.label_manual_control_electronic_load_rise.setText('Limit')
            self.ui.label_manual_control_electronic_load_fall.setEnabled(False)
            self.ui.lineedit_manual_control_eload_slew_fall.setEnabled(False)
            self.ui.label_manual_control_eload_slew_fall_unit.setEnabled(False)
        elif self.ui.cbx_manual_control_eload_type.currentText() == ELoadTypes.CP:
            self.ui.label_manual_control_eload_a_level_unit.setText('W')
            self.ui.label_manual_control_eload_b_level_unit.setText('W')
            if self.electronic_load.cp_slew_unit[0] ==  'A':
                self.ui.label_manual_control_eload_slew_rise_unit.setText('A / µs')
                self.ui.label_manual_control_eload_slew_fall_unit.setText('A / µs')
            else:
                self.ui.label_manual_control_eload_slew_rise_unit.setText('W / µs')
                self.ui.label_manual_control_eload_slew_fall_unit.setText('W / µs')
            self.ui.lineedit_manual_control_eload_slew_rise.setText('0.15')
            self.ui.lineedit_manual_control_eload_slew_fall.setText('0.15')
            self.ui.label_manual_control_electronic_load_rise.setEnabled(True)
            self.ui.lineedit_manual_control_eload_slew_rise.setEnabled(True)
            self.ui.label_manual_control_eload_slew_rise_unit.setEnabled(True)
            self.ui.label_manual_control_electronic_load_fall.setEnabled(True)
            self.ui.lineedit_manual_control_eload_slew_fall.setEnabled(True)
            self.ui.label_manual_control_eload_slew_fall_unit.setEnabled(True)