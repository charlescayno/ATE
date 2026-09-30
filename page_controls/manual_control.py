
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
        self.ui.frame_manual_control_eload_2.setVisible(True)
        self.ui.frame_manual_control_eload_4.setVisible(False)
        self.ui.frame_manual_control_pml_3.setVisible(False)
        self.ui.frame_manual_control_pml_4.setVisible(False)

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
        self.setup_state_saving()
    

    def setup_state_saving(self):
        import json
        import os
        from PySide2.QtWidgets import QLineEdit, QComboBox, QCheckBox
        self.settings_file = "manual_control_settings.json"
        
        self.state_widgets = []
        for t in (QLineEdit, QComboBox, QCheckBox):
            for widget in self.ui.page_manual_control.findChildren(t):
                obj_name = widget.objectName()
                if not obj_name: continue
                self.state_widgets.append(widget)
                
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
            obj_name = widget.objectName()
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
                obj_name = widget.objectName()
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
