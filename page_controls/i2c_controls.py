from typing import TYPE_CHECKING

from asyncio import sleep


import os
import json
import debugpy

from app.app_modules import *

from equipment.handler import EquipmentHandler
from equipment.ac_source import *
from equipment.power_meter import *
from equipment.electronic_load import *
from equipment.eload_specs import ELoadTypes

from sink_controllers import pat_tool
from sink_controllers.pat_tool import SMBUS_STATE, InnoProI2CControllerContainer

from functools import wraps

import user_settings.save_load as configs

from user_settings.save_load import (write_to_default_config, read_from_default_config) 
from user_settings.keys import *
from sink_controllers.pat_tool import I2CWriteError
from misc_functions.misc_functions import *
from psu_tests.definitions import MessageType
from page_controls.definitions import StackWidgetI2CControlsPages, I2CCommandObject
from sink_controllers.definitions import *

from ui.ui_styles import *

from dll.SLABHIDtoSMBUS import (HID_SMBUS_S0, HID_SMBUS_S1)

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (
    QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QTimer,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent, Signal, Slot, QThread)
from PySide2.QtGui import (
    QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase,
    QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, 
    QRadialGradient,QIntValidator,QDoubleValidator)
from PySide2.QtWidgets import *

import threading

if TYPE_CHECKING:
    from main import MainWindow, Ui_MainWindow


# Indicate the availability of the AC source output by changing something in the ui
red_frame = "QFrame{border:2px solid red;	border-radius: 5px;};"
green_frame = "QFrame{border:2px solid green;	border-radius: 5px;};"
UPDATE_INTERVAL_MS = 500

def i2c_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self:I2CControlsPageHandler = args[0]
        try:
            if self.message_type.currentText() == InnoPro_MessageType.I2C:
                if self.i2c_controller is not None:
                    if self.usbpd_sink is not None:
                        try:
                            self.usbpd_sink.close()
                        except Exception as e:
                            print(e)
                    self.i2c_controller.reset()
                    # Prompt user if SMBUS is not connected
                    if not self.i2c_controller.connection_status == SMBUS_STATE.CONNECTED:
                        if self.i2c_command_list_thread_running:
                            self.i2c_command_worker.update_popup_status(True)
                        self.message_popup.emit(True)
                        self.parent.msg_box_info(
                            title="I2C Control",
                            message="TST-058 not connected",
                            message_type=MessageType.INFO)
                        if self.i2c_command_list_thread_running:
                            self.i2c_command_worker.update_popup_status(False)
                        self.message_popup.emit(False)
                        return None
                else:
                    if self.i2c_command_list_thread_running:
                        self.i2c_command_worker.update_popup_status(True)
                    self.message_popup.emit(True)
                    self.parent.msg_box_info(
                        title="I2C Control",
                        message="TST-058 not connected",
                        message_type=MessageType.INFO)
                    if self.i2c_command_list_thread_running:
                        self.i2c_command_worker.update_popup_status(False)
                    self.message_popup.emit(False)
                    return None
            elif self.message_type.currentText() in InnoProMessageUVDMList:
                if self.usbpd_sink is not None:
                    sink_status = self.usbpd_sink.get_status()
                    if not sink_status == SINK_STATE.USBPD_SOURCE_CONNECTED:
                        if self.i2c_command_list_thread_running:
                            self.i2c_command_worker.update_popup_status(True)
                        self.message_popup.emit(True)
                        self.parent.msg_box_info(
                            title="I2C Control",
                            message="USB-PD Sink/Source not connected",
                            message_type=MessageType.INFO)
                        if self.i2c_command_list_thread_running:
                            self.i2c_command_worker.update_popup_status(False)
                        self.message_popup.emit(False)
                        return None
                else:
                    if self.i2c_command_list_thread_running:
                        self.i2c_command_worker.update_popup_status(True)
                    self.message_popup.emit(True)
                    self.parent.msg_box_info(
                        title="I2C Control",
                        message="USB-PD Sink not connected",
                        message_type=MessageType.INFO)
                    if self.i2c_command_list_thread_running:
                        self.i2c_command_worker.update_popup_status(False)
                    self.message_popup.emit(False)
                    return None
            else:
                pass   
                result = None            
        except:
            if self.message_type.currentText() == InnoPro_MessageType.I2C:
                if self.i2c_command_list_thread_running:
                    self.i2c_command_worker.update_popup_status(True)
                self.message_popup.emit(True)
                self.parent.msg_box_info(
                        title="I2C Control",
                        message="TST-058 not connected",
                        message_type=MessageType.INFO)
                if self.i2c_command_list_thread_running:
                        self.i2c_command_worker.update_popup_status(False)
                self.message_popup.emit(False)
                return None
            elif self.message_type.currentText() in InnoProMessageUVDMList:
                if self.i2c_command_list_thread_running:
                    self.i2c_command_worker.update_popup_status(True)
                self.message_popup.emit(True)
                self.parent.msg_box_info(
                        title="I2C Control",
                        message="USB-PD Sink/Source not connected",
                        message_type=MessageType.INFO)
                if self.i2c_command_list_thread_running:
                        self.i2c_command_worker.update_popup_status(False)
                self.message_popup.emit(False)
                return None
            else:
                pass
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(e)
        if (self.i2c_controller is not None) and (self.message_type.currentText() == InnoPro_MessageType.I2C):
            try:
                self.i2c_controller.close()
            except Exception as e:
                print(e)
        return result
    return wrapper

def send_btn_update(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        error = False
        status = -1
        try:
            status, btn = func(*args, **kwargs)
        except I2CWriteError:
            error = True
        
        if error or not (status == HID_SMBUS_S0.COMPLETE):
            flash_btn_stylesheet(btn, Style.style_button_red)
        else:
            flash_btn_stylesheet(btn, Style.style_button_green)
    return wrapper     
        
from inno_pro.definitions import *
from inno_pro.inno5_pro.ui_definitions import *
from inno_pro.inno5_pro.ui_functions import *
from inno_pro.inno4_pro.ui_definitions import *
from inno_pro.inno4_pro.ui_functions import *

class I2CControlsPageHandler(QObject):
    message_popup = Signal(bool)
    """ Handles the page for setting up I2C controls
    
    """
    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent
        self.ui:Ui_MainWindow = parent.ui
        self.equipment:EquipmentHandler = parent.equipment
        self.innoswitch_family = InnoProFamily.Inno5Pro
        self.i2c_controller = self.equipment.i2c_controller
        self.usbpd_sink = self.equipment.usbpd_sink
        self.parent_folder_path = configs.read_from_default_config(
                key=SaveFileKeys.OUTPUT_FOLDER_PATH, default_value='')
        self.initialize_ui()
        self.initialize_equipment_ui()
        self.initialize_inno_pro_command_list_ui()
        
    def initialize_equipment_ui(self):
        try:
            # Equipment setup
            self.ui.btn_i2c_controls_setup_equipment.clicked.connect(
                self.setup_equipment)
            
             # Bind AC Controls UI
            self.ui.btn_i2c_controls_ac_source_turn_on.clicked.connect(self.ac_source_power_on)
            self.ui.btn_i2c_controls_ac_source_turn_off.clicked.connect(self.ac_source_power_off)
            self.ui.chkbox_i2c_controls_ac_source_coupling.clicked.connect(self.update_ac_source_coupling)
            
            # E-Load Buttons
            self.ui.btn_i2c_controls_eload_turn_on.clicked.connect(
                self.eload_turn_on)
            self.ui.btn_i2c_controls_eload_set_A.clicked.connect(
                self.eload_set_level_A)
            self.ui.btn_i2c_controls_eload_set_B.clicked.connect(
                self.eload_set_level_B)
            self.ui.btn_i2c_controls_eload_set_slew.clicked.connect(
                self.eload_set_slew)
            self.ui.btn_i2c_controls_eload_turn_off.clicked.connect(
                self.eload_turn_off)
            self.ui.btn_i2c_controls_eload_a_b_swap.clicked.connect(
                self.eload_swap_active_level)
            self.ui.cbx_i2c_controls_eload_type.currentIndexChanged.connect(
                self.update_eload_settings)
        except:
            print("Exception while binding equipment controls")
        
        # Set validator for lineedits
        self.validator = QDoubleValidator(0, 16777215, 6)
        
        self.ui.lineedit_i2c_controls_ac_source_voltage.setValidator(self.validator)
        self.ui.lineedit_i2c_controls_ac_source_frequency.setValidator(self.validator)
        self.ui.lineedit_i2c_controls_eload_a_level.setValidator(self.validator)
        self.ui.lineedit_i2c_controls_eload_rise.setValidator(self.validator)
        self.ui.lineedit_i2c_controls_eload_b_level.setValidator(self.validator)
        self.ui.lineedit_i2c_controls_eload_fall.setValidator(self.validator)
        self.ui.lineedit_i2c_controls_command_delay.setValidator(self.validator)
    
    def initialize_ui(self):
        # Bind frames and grid layout
        self.frame_reg1 = self.ui.frame_i2c_controls_reg1
        self.frame_reg2 = self.ui.frame_i2c_controls_reg2
        self.frame_reg3 = self.ui.frame_i2c_controls_reg3
        self.frame_reg4 = self.ui.frame_i2c_controls_reg4
        self.frame_reg5 = self.ui.frame_i2c_controls_reg5
        self.frame_reg6 = self.ui.frame_i2c_controls_reg6
        self.frame_reg7 = self.ui.frame_i2c_controls_reg7
        self.frame_reg8 = self.ui.frame_i2c_controls_reg8
        self.frame_reg9 = self.ui.frame_i2c_controls_reg9
        self.frame_reg10 = self.ui.frame_i2c_controls_reg10
        self.frame_reg11 = self.ui.frame_i2c_controls_reg11
        self.frame_reg12 = self.ui.frame_i2c_controls_reg12
        self.frame_reg13 = self.ui.frame_i2c_controls_reg13
        self.frame_reg14 = self.ui.frame_i2c_controls_reg14
        self.frame_reg15 = self.ui.frame_i2c_controls_reg15
        self.frame_reg16 = self.ui.frame_i2c_controls_reg16
        self.frame_reg17 = self.ui.frame_i2c_controls_reg17
        self.frame_reg18 = self.ui.frame_i2c_controls_reg18
        self.frame_reg19 = self.ui.frame_i2c_controls_reg19
        self.frame_reg20 = self.ui.frame_i2c_controls_reg20
        self.frame_reg21 = self.ui.frame_i2c_controls_reg21
        self.frame_reg22 = self.ui.frame_i2c_controls_reg22
        self.frame_reg23 = self.ui.frame_i2c_controls_reg23
        self.frame_reg24 = self.ui.frame_i2c_controls_reg24
        
        self.frame_reg_list = [
            self.frame_reg1,
            self.frame_reg2,
            self.frame_reg3,
            self.frame_reg4,
            self.frame_reg5,
            self.frame_reg6,
            self.frame_reg7,
            self.frame_reg8,
            self.frame_reg9,
            self.frame_reg10,
            self.frame_reg11,
            self.frame_reg12,
            self.frame_reg13,
            self.frame_reg14,
            self.frame_reg15,
            self.frame_reg16,
            self.frame_reg17,
            self.frame_reg18,
            self.frame_reg19,
            self.frame_reg20,
            self.frame_reg21,
            self.frame_reg22,
            self.frame_reg23,
            self.frame_reg24,
        ]
        # self.frame_reg24 = self.ui.frame_i2c_controls_reg24
        # self.frame_reg25 = self.ui.frame_i2c_controls_reg25

        self.frame_readback_reg_any = self.ui.frame_i2c_controls_readback_reg_any
        self.frame_readback_reg0 = self.ui.frame_i2c_controls_readback_reg0
        self.frame_readback_reg1 = self.ui.frame_i2c_controls_readback_reg1
        self.frame_readback_reg2 = self.ui.frame_i2c_controls_readback_reg2
        self.frame_readback_reg3 = self.ui.frame_i2c_controls_readback_reg3
        self.frame_readback_reg4 = self.ui.frame_i2c_controls_readback_reg4
        self.frame_readback_reg5 = self.ui.frame_i2c_controls_readback_reg5
        self.frame_readback_reg6 = self.ui.frame_i2c_controls_readback_reg6
        self.frame_readback_reg7 = self.ui.frame_i2c_controls_readback_reg7
        self.frame_readback_reg8 = self.ui.frame_i2c_controls_readback_reg8
        self.frame_readback_reg9 = self.ui.frame_i2c_controls_readback_reg9
        self.frame_readback_reg10 = self.ui.frame_i2c_controls_readback_reg10
        self.frame_readback_reg11 = self.ui.frame_i2c_controls_readback_reg11
        self.frame_readback_reg12 = self.ui.frame_i2c_controls_readback_reg12
        self.frame_readback_reg13 = self.ui.frame_i2c_controls_readback_reg13
        self.frame_readback_reg14 = self.ui.frame_i2c_controls_readback_reg14
        self.frame_readback_reg15 = self.ui.frame_i2c_controls_readback_reg15
        self.frame_readback_reg16 = self.ui.frame_i2c_controls_readback_reg16
        self.frame_readback_reg17 = self.ui.frame_i2c_controls_readback_reg17
        self.frame_readback_reg18 = self.ui.frame_i2c_controls_readback_reg18
        self.frame_readback_reg19 = self.ui.frame_i2c_controls_readback_reg19
        self.frame_readback_reg20 = self.ui.frame_i2c_controls_readback_reg20
        self.frame_readback_reg21 = self.ui.frame_i2c_controls_readback_reg21
        self.frame_readback_reg22 = self.ui.frame_i2c_controls_readback_reg22
        self.frame_readback_reg23 = self.ui.frame_i2c_controls_readback_reg23
        self.frame_readback_reg24 = self.ui.frame_i2c_controls_readback_reg24
        
        self.frame_readback_reg_list = [
            self.frame_readback_reg_any,
            self.frame_readback_reg0,
            self.frame_readback_reg1,
            self.frame_readback_reg2,
            self.frame_readback_reg3,
            self.frame_readback_reg4,
            self.frame_readback_reg5,
            self.frame_readback_reg6,
            self.frame_readback_reg7,
            self.frame_readback_reg8,
            self.frame_readback_reg9,
            self.frame_readback_reg10,
            self.frame_readback_reg11,
            self.frame_readback_reg12,
            self.frame_readback_reg13,
            self.frame_readback_reg14,
            self.frame_readback_reg15,
            self.frame_readback_reg16,
            self.frame_readback_reg17,
            self.frame_readback_reg18,
            self.frame_readback_reg19,
            self.frame_readback_reg20,
            self.frame_readback_reg21,
            self.frame_readback_reg22,
            self.frame_readback_reg23,
            self.frame_readback_reg24,
        ]
        
        self.grid_reg1 = self.ui.gridLayout_reg1
        self.grid_reg2 = self.ui.gridLayout_reg2
        self.grid_reg3 = self.ui.gridLayout_reg3
        self.grid_reg4 = self.ui.gridLayout_reg4
        self.grid_reg5 = self.ui.gridLayout_reg5
        self.grid_reg6 = self.ui.gridLayout_reg6
        self.grid_reg7 = self.ui.gridLayout_reg7
        self.grid_reg8 = self.ui.gridLayout_reg8
        self.grid_reg9 = self.ui.gridLayout_reg9
        self.grid_reg10 = self.ui.gridLayout_reg10
        self.grid_reg11 = self.ui.gridLayout_reg11
        self.grid_reg12 = self.ui.gridLayout_reg12
        self.grid_reg13 = self.ui.gridLayout_reg13
        self.grid_reg14 = self.ui.gridLayout_reg14
        self.grid_reg15 = self.ui.gridLayout_reg15
        self.grid_reg16 = self.ui.gridLayout_reg16
        self.grid_reg17 = self.ui.gridLayout_reg17
        self.grid_reg18 = self.ui.gridLayout_reg18
        self.grid_reg19 = self.ui.gridLayout_reg19
        self.grid_reg20 = self.ui.gridLayout_reg20
        self.grid_reg21 = self.ui.gridLayout_reg21
        self.grid_reg22 = self.ui.gridLayout_reg22
        self.grid_reg23 = self.ui.gridLayout_reg23
        self.grid_reg24 = self.ui.gridLayout_reg24
        # self.grid_reg25 = self.ui.gridLayout_reg25
        
        self.grid_reg_list = [
            self.grid_reg1,
            self.grid_reg2,
            self.grid_reg3,
            self.grid_reg4,
            self.grid_reg5,
            self.grid_reg6,
            self.grid_reg7,
            self.grid_reg8,
            self.grid_reg9,
            self.grid_reg10,
            self.grid_reg11,
            self.grid_reg12,
            self.grid_reg13,
            self.grid_reg14,
            self.grid_reg15,
            self.grid_reg16,
            self.grid_reg17,
            self.grid_reg18,
            self.grid_reg19,
            self.grid_reg20,
            self.grid_reg21,
            self.grid_reg22,
            self.grid_reg23,
            self.grid_reg24,
        ]
        self.grid_readback_reg_any = self.ui.gridLayout_readback_reg_any
        self.grid_readback_reg0 = self.ui.gridLayout_readback_reg0
        self.grid_readback_reg1 = self.ui.gridLayout_readback_reg1
        self.grid_readback_reg2 = self.ui.gridLayout_readback_reg2
        self.grid_readback_reg3 = self.ui.gridLayout_readback_reg3
        self.grid_readback_reg4 = self.ui.gridLayout_readback_reg4
        self.grid_readback_reg5 = self.ui.gridLayout_readback_reg5
        self.grid_readback_reg6 = self.ui.gridLayout_readback_reg6
        self.grid_readback_reg7 = self.ui.gridLayout_readback_reg7
        self.grid_readback_reg8 = self.ui.gridLayout_readback_reg8
        self.grid_readback_reg9 = self.ui.gridLayout_readback_reg9
        self.grid_readback_reg10 = self.ui.gridLayout_readback_reg10
        self.grid_readback_reg11 = self.ui.gridLayout_readback_reg11
        self.grid_readback_reg12 = self.ui.gridLayout_readback_reg12
        self.grid_readback_reg13 = self.ui.gridLayout_readback_reg13
        self.grid_readback_reg14 = self.ui.gridLayout_readback_reg14
        self.grid_readback_reg15 = self.ui.gridLayout_readback_reg15
        self.grid_readback_reg16 = self.ui.gridLayout_readback_reg16
        self.grid_readback_reg17 = self.ui.gridLayout_readback_reg17
        self.grid_readback_reg18 = self.ui.gridLayout_readback_reg18
        self.grid_readback_reg19 = self.ui.gridLayout_readback_reg19
        self.grid_readback_reg20 = self.ui.gridLayout_readback_reg20
        self.grid_readback_reg21 = self.ui.gridLayout_readback_reg21
        self.grid_readback_reg22 = self.ui.gridLayout_readback_reg22
        self.grid_readback_reg23 = self.ui.gridLayout_readback_reg23
        self.grid_readback_reg24 = self.ui.gridLayout_readback_reg24

        self.grid_readback_reg_list = [
            self.grid_readback_reg_any,
            self.grid_readback_reg0,
            self.grid_readback_reg1,
            self.grid_readback_reg2,
            self.grid_readback_reg3,
            self.grid_readback_reg4,
            self.grid_readback_reg5,
            self.grid_readback_reg6,
            self.grid_readback_reg7,
            self.grid_readback_reg8,
            self.grid_readback_reg9,
            self.grid_readback_reg10,
            self.grid_readback_reg11,
            self.grid_readback_reg12,
            self.grid_readback_reg13,
            self.grid_readback_reg14,
            self.grid_readback_reg15,
            self.grid_readback_reg16,
            self.grid_readback_reg17,
            self.grid_readback_reg18,
            self.grid_readback_reg19,
            self.grid_readback_reg20,
            self.grid_readback_reg21,
            self.grid_readback_reg22,
            self.grid_readback_reg23,
            self.grid_readback_reg24,
        ]
        self.message_type = self.ui.cbx_i2c_controls_message_type
        self.frame_vben_reg = self.ui.frame_i2c_controls_vben_reg
        self.grid_vben_reg = self.ui.gridLayout_vben_reg
        self.frame_watchdog_reg = self.ui.frame_i2c_controls_watchdog_reg
        self.grid_watchdog_reg = self.ui.gridLayout_watchdog_reg
        self.frame_loop_option_reg = self.ui.frame_i2c_controls_loop_option_reg
        self.grid_loop_option_reg = self.ui.gridLayout_loop_option_reg
        
        self.ui.btn_i2c_controls_registers.clicked.connect(self.select_stack_page_registers)
        self.ui.btn_i2c_controls_readback_registers.clicked.connect(self.select_stack_page_readback_registers)
        
        self.ui.cbx_i2c_controls_inno_pro_family.clear()
        self.ui.cbx_i2c_controls_inno_pro_family.addItems(InnoProFamilyList)
        
        self.ui.cbx_i2c_controls_inno_pro_family.currentIndexChanged.connect(self.setup_inno_pro_registers)
        self.ui.btn_i2c_controls_initialize.clicked.connect(self.i2c_initialize)
        self.ui.btn_i2c_controls_set_nr.clicked.connect(self.i2c_set_nr)
        
        
    def initialize_inno_pro_command_list_ui(self):
        """Initialize the i2c command list UI"""
        self.i2c_command_list_running = False
        self.i2c_command_list:list[I2CCommandObject] = []
        self.i2c_command_list_thread_running = False
        # self.i2c_command_name_list = []
        # self.i2c_command_value_list = []
        # self.i2c_command_extra_params_list = []
        self.ui.btn_i2c_controls_command_save.clicked.connect(self.save_command_list)
        self.ui.btn_i2c_controls_command_load.clicked.connect(self.load_command_list)
        self.ui.btn_i2c_controls_command_add_delay.clicked.connect(self.add_delay_to_command_list)
        self.ui.btn_i2c_controls_command_clear.clicked.connect(self.clear_command_list)
        self.ui.btn_i2c_controls_command_delete.clicked.connect(self.delete_single_from_command_list)
        self.ui.btn_i2c_controls_command_run_all.clicked.connect(self.run_command_list)
        self.ui.btn_i2c_controls_command_run_single.clicked.connect(self.run_single_from_command_list)
        
        self.command_list_delay = self.ui.lineedit_i2c_controls_command_delay
        self.command_list_table = self.ui.table_i2c_controls_command_list
        header = self.command_list_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)   
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
         
    def select_stack_page_registers(self):
        """Change the page displayed on the stacked widgets
        to the registers console"""

        self.ui.stackedWidget_i2c_controls.setCurrentIndex(
            StackWidgetI2CControlsPages.Registers)
    
    def select_stack_page_readback_registers(self):
        """Change the page displayed on the stacked widgets
        to the readback registers console"""

        self.ui.stackedWidget_i2c_controls.setCurrentIndex(
            StackWidgetI2CControlsPages.ReadbackRegisters)
       
    def setup_inno_pro_registers(self):
        self.innoswitch_family = self.ui.cbx_i2c_controls_inno_pro_family.currentText()
        self.clear_all_frames()
        if self.i2c_controller is not None:
            self.i2c_controller.update_controller(self.innoswitch_family)
            
        # List register UIs and register labels    
        self.cmd_reg_list = []
        self.cmd_reg_name_list = []
        
        self.cmd_readback_reg_list = []
        self.cmd_readback_reg_name_list = []
        
        # Bind default/commonly used registers and buttons
        match self.innoswitch_family:
            case InnoProFamily.Inno5Pro:
                
                self.vben_reg = INNO5_VBEN_Reg_UI(self.frame_vben_reg,self.grid_vben_reg)  
                
                
                self.watchdog_reg = INNO5_WATCHDOG_Reg_UI(self.frame_watchdog_reg,self.grid_watchdog_reg)
                self.watchdog_reg.send.clicked.connect(self.send_command_watchdog)
                self.watchdog_reg.queue.clicked.connect(self.queue_command_watchdog)
                
                self.loop_option_reg = INNO5_LOOP_OPTION_Reg_UI(self.frame_loop_option_reg,self.grid_loop_option_reg)
                self.loop_option_reg.send.clicked.connect(self.send_command_loop_option)
                self.loop_option_reg.queue.clicked.connect(self.queue_command_loop_option)
                
                self.cmd_reg_list.append(self.vben_reg)
                self.cmd_reg_name_list.append(self.vben_reg.reg_label)
                
                self.cmd_reg_list.append(self.watchdog_reg)
                self.cmd_reg_name_list.append(self.watchdog_reg.reg_label)
                
                self.cmd_reg_list.append(self.loop_option_reg)
                self.cmd_reg_name_list.append(self.loop_option_reg.reg_label)
                
            case InnoProFamily.Inno4Pro:
                
                self.vben_reg = INNO4_VBEN_Reg_UI(self.frame_vben_reg,self.grid_vben_reg)  
                
                self.watchdog_reg = INNO4_WATCHDOG_Reg_UI(self.frame_watchdog_reg,self.grid_watchdog_reg)
                self.watchdog_reg.send.clicked.connect(self.send_command_watchdog)
                self.watchdog_reg.queue.clicked.connect(self.queue_command_watchdog)
                
                self.loop_option_reg = INNO4_LOOP_OPTION_Reg_UI(self.frame_loop_option_reg,self.grid_loop_option_reg)
                self.loop_option_reg.send.clicked.connect(self.send_command_loop_option)
                self.loop_option_reg.queue.clicked.connect(self.queue_command_loop_option)
                
                self.cmd_reg_list.append(self.vben_reg)
                self.cmd_reg_name_list.append(self.vben_reg.reg_label)
                
                self.cmd_reg_list.append(self.watchdog_reg)
                self.cmd_reg_name_list.append(self.watchdog_reg.reg_label)
                
                self.cmd_reg_list.append(self.loop_option_reg)
                self.cmd_reg_name_list.append(self.loop_option_reg.reg_label)
                
            case _:
                return
        
        self.vben_reg.send.clicked.connect(self.send_command_vben)
        self.vben_reg.queue.clicked.connect(self.queue_command_vben)

        self.setup_inno_pro_command_registers()
        self.setup_inno_pro_readback_registers()
    
    def setup_inno_pro_command_registers(self):
        match self.innoswitch_family:
            case InnoProFamily.Inno5Pro:
                for index, reg in enumerate(INNO5_I2C_COMMAND_REG_LIST):
                    if reg is None:
                        continue
                    self.cmd_reg_list.append(inno5_create_reg_ui(self,self.frame_reg_list[index],self.grid_reg_list[index],reg))
                    self.cmd_reg_name_list.append(reg.reg_label)
            case InnoProFamily.Inno4Pro:
                for index, reg in enumerate(INNO4_I2C_COMMAND_REG_LIST):
                    if reg is None:
                        continue
                    self.cmd_reg_list.append(inno4_create_reg_ui(self,self.frame_reg_list[index],self.grid_reg_list[index],reg))
                    self.cmd_reg_name_list.append(reg.reg_label)
    def setup_inno_pro_readback_registers(self):
        match self.innoswitch_family:
            case InnoProFamily.Inno5Pro:
                for index, reg in enumerate(INNO5_I2C_READBACK_REG_LIST):
                    if reg is None:
                        continue
                    self.cmd_readback_reg_list.append(inno5_create_readback_reg_ui(self,self.frame_readback_reg_list[index],self.grid_readback_reg_list[index],reg))
                    self.cmd_readback_reg_name_list.append(reg.reg_label)
            case InnoProFamily.Inno4Pro:
                for index, reg in enumerate(INNO4_I2C_READBACK_REG_LIST):
                    if reg is None:
                        continue
                    self.cmd_readback_reg_list.append(inno4_create_readback_reg_ui(self,self.frame_readback_reg_list[index],self.grid_readback_reg_list[index],reg))
                    self.cmd_readback_reg_name_list.append(reg.reg_label)
    def start(self):
        self.setup_equipment()
        
        self.setup_update_timer()
        self.update_timer.start(UPDATE_INTERVAL_MS)        
        
    def setup_equipment(self):
        """Set up the assignment and initialization of equipment"""
        self.ac_source:ACSource = self.equipment.ac_source
        if self.ac_source is None:
            self.ui.frame_i2c_controls_ac_source.setEnabled(False)
        else: 
            self.ui.frame_i2c_controls_ac_source.setEnabled(True)     
            
        self.power_meter_source:PowerMeter = self.equipment.power_meter_source
        if self.power_meter_source is None:
            self.power_meter_source_ready = False
            self.ui.frame_i2c_controls_power_meter_source.setEnabled(False)
            self.ui_power_meter_source_update_fail()
        else:
            try:
                self.power_meter_source_ready = True
                self.ui.frame_i2c_controls_power_meter_source.setEnabled(True)
                self.power_meter_source_integ_timer = self.power_meter_source.get_integration_timer()
                self.power_meter_source.set_integration_timer(timer_s=0)
            except Exception as e:
                self.ui.frame_i2c_controls_power_meter_source.setEnabled(False)
                self.power_meter_source_ready = False   
                self.ui_power_meter_source_update_fail()
            
        self.power_meter_load:PowerMeter = self.equipment.power_meter_load_1
        if self.power_meter_load is None:
            self.power_meter_load_ready = False
            self.ui_power_meter_load_update_fail()
            self.ui.frame_i2c_controls_power_meter_load.setEnabled(False)
        else:
            try: 
                self.power_meter_load_ready = True
                self.ui.frame_i2c_controls_power_meter_load.setEnabled(True)
                self.power_meter_load_integ_timer = self.power_meter_load.get_integration_timer()
                self.power_meter_load.set_integration_timer(timer_s=0)
            except Exception as e:
                self.ui.frame_i2c_controls_power_meter_load.setEnabled(False)
                self.power_meter_load_ready = False   
                self.ui_power_meter_source_update_fail()
        
        self.electronic_load:ElectronicLoadModule = self.equipment.electronic_load_1
        if self.electronic_load is None:
            self.ui.frame_i2c_controls_eload.setEnabled(False)
        else:
            self.ui.frame_i2c_controls_eload.setEnabled(True) 
            
        # self.power_meter_load.stop_integration()
        # self.power_meter_source.stop_integration()
        # self.power_meter_load.reset_integration()
        # self.power_meter_source.reset_integration()
        
        # TODO: Set base settings such as coupling, averaging, rates

        # self.parent.equipment_setup_page_handler.check_usbpd_sink_availability()

        self.i2c_controller = self.equipment.i2c_controller
        self.usbpd_sink = self.equipment.usbpd_sink
        self.setup_inno_pro_registers()
   
    def eload_turn_off(self):
        """Turn off the electronic load."""
        try:
            self.electronic_load.turn_off()
        except Exception as e:
            print(e)


    def eload_turn_on(self):
        """Turn on the electronic load"""
        try:
            self.electronic_load.turn_on()
        except Exception as e:
            print(e)
            
    def eload_set_level_A(self):
        # Take the inputs first
        load_mode = self.ui.cbx_i2c_controls_eload_type.currentText()

        load_a_level_txt = self.ui.lineedit_i2c_controls_eload_a_level.text()
        
        try:
            load_a_level = round(float(load_a_level_txt),6)
            
            vout_V = self.electronic_load.voltage
            if abs(vout_V) < 0.5:
                vout_V = self.electronic_load.crh_max_v
            
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
        
        except Exception as e:
            print(e)
                      
    def eload_set_level_B(self):
        # Take the inputs first
        load_mode = self.ui.cbx_i2c_controls_eload_type.currentText()

        load_b_level_txt = self.ui.lineedit_i2c_controls_eload_b_level.text()
        
        try:
            load_b_level = round(float(load_b_level_txt),6)
            
            vout_V = self.electronic_load.voltage
            if abs(vout_V) < 0.5:
                vout_V = self.electronic_load.crh_max_v
            
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
        
        except Exception as e:
            print(e)  
            
        
    def eload_set_slew(self):
        # Take the inputs first
        load_mode = self.ui.cbx_i2c_controls_eload_type.currentText()

        load_rise_txt = self.ui.lineedit_i2c_controls_eload_rise.text()
        load_fall_txt = self.ui.lineedit_i2c_controls_eload_fall.text()
        
        try:
            load_rise = round(float(load_rise_txt)/1000,6)
            load_fall = round(float(load_fall_txt)/1000,6)   

            match load_mode:
                case ELoadTypes.CC:
                    self.electronic_load.set_cc_static_slew(load_rise,load_fall)
                case ELoadTypes.CR:
                    self.electronic_load.set_cr_slew(load_rise,load_fall)
                case ELoadTypes.CP:
                    self.electronic_load.set_cp_slew(load_rise*1000,load_fall*1000)
                case ELoadTypes.CV:
                    self.electronic_load.cv_current = load_rise
        
        except Exception as e:
            print(e)      

    def eload_swap_active_level(self):
        # self.electronic_load.get_active_level()
        # load_mode = self.ui.cbx_i2c_controls_eload_type.currentText()
        vout_V = self.electronic_load.voltage
        if abs(vout_V) < 0.5:
            vout_V = self.electronic_load.crh_max_v
        if self.electronic_load._active_level == '1':
            self.eload_set_level_B()
        else:
            self.eload_set_level_A()
        # match load_mode:
        #     case ELoadTypes.CC:
        #         if self.electronic_load._active_level == '1':
        #             self.eload_set_level_A
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
        #     case ELoadTypes.CP:
        #         if self.electronic_load._active_level == '1':
        #             self.electronic_load.set_active_level(2)
        #             self.electronic_load.set_load(vout_V=vout_V, iout_A=(self.electronic_load.cp_l2/vout_V), mode=load_mode)
        #         else:
        #             self.electronic_load.set_active_level(1)
        #             self.electronic_load.set_load(vout_V=vout_V, iout_A=(self.electronic_load.cp_l1/vout_V), mode=load_mode)
        #     case ELoadTypes.CV:
        #         if self.electronic_load._active_level == '1':
        #             self.electronic_load.set_active_level(2)
        #             self.electronic_load.set_load(vout_V=self.electronic_load.cv_l2, iout_A=self.electronic_load.cv_current, mode=load_mode)
        #         else:
        #             self.electronic_load.set_active_level(1)
        #             self.electronic_load.set_load(vout_V=self.electronic_load.cv_l1, iout_A=self.electronic_load.cv_current, mode=load_mode)

    def update_ac_source_coupling(self):
        if self.ui.chkbox_i2c_controls_ac_source_coupling.isChecked():
            self.ui.chkbox_i2c_controls_ac_source_coupling.setText(QCoreApplication.translate("MainWindow", 'DC', None))
            self.ui.lineedit_i2c_controls_ac_source_frequency.setEnabled(False)
            self.ui.label_i2c_controls_ac_source_frequency.setEnabled(False)
            self.ac_source.coupling = AC_SOURCE_COUPLING.DC
        else:
            self.ui.chkbox_i2c_controls_ac_source_coupling.setText(QCoreApplication.translate("MainWindow", 'AC', None))
            self.ui.lineedit_i2c_controls_ac_source_frequency.setEnabled(True)
            self.ui.label_i2c_controls_ac_source_frequency.setEnabled(True)
            self.ac_source.coupling = AC_SOURCE_COUPLING.AC                
        
    def update_eload_settings(self):
        self.ui.label_i2c_controls_electronic_load_rise.setText('Rise')
        self.ui.label_i2c_controls_eload_rise_unit.setText('mA / µs')
        self.ui.label_i2c_controls_eload_fall_unit.setText('mA / µs')
        self.ui.lineedit_i2c_controls_eload_rise.setText('150')
        self.ui.lineedit_i2c_controls_eload_fall.setText('150')

        if self.ui.cbx_i2c_controls_eload_type.currentText() == ELoadTypes.CC:
            self.ui.label_i2c_controls_eload_a_level_unit.setText('A')
            self.ui.label_i2c_controls_eload_b_level_unit.setText('A')
            self.ui.label_i2c_controls_electronic_load_rise.setEnabled(True)
            self.ui.lineedit_i2c_controls_eload_rise.setEnabled(True)
            self.ui.label_i2c_controls_eload_rise_unit.setEnabled(True)
            self.ui.label_i2c_controls_electronic_load_fall.setEnabled(True)
            self.ui.lineedit_i2c_controls_eload_fall.setEnabled(True)
            self.ui.label_i2c_controls_eload_fall_unit.setEnabled(True)
        elif self.ui.cbx_i2c_controls_eload_type.currentText() == ELoadTypes.CR:
            self.ui.label_i2c_controls_eload_a_level_unit.setText('Ω')
            self.ui.label_i2c_controls_eload_b_level_unit.setText('Ω')
            if not self.electronic_load.cr_slew_available:
                self.ui.label_i2c_controls_electronic_load_rise.setEnabled(False)
                self.ui.lineedit_i2c_controls_eload_rise.setEnabled(False)
                self.ui.label_i2c_controls_eload_rise_unit.setEnabled(False)
                self.ui.label_i2c_controls_electronic_load_fall.setEnabled(False)
                self.ui.lineedit_i2c_controls_eload_fall.setEnabled(False)
                self.ui.label_i2c_controls_eload_fall_unit.setEnabled(False)
            else:
                self.ui.label_i2c_controls_electronic_load_rise.setEnabled(True)
                self.ui.lineedit_i2c_controls_eload_rise.setEnabled(True)
                self.ui.label_i2c_controls_eload_rise_unit.setEnabled(True)
                self.ui.label_i2c_controls_electronic_load_fall.setEnabled(True)
                self.ui.lineedit_i2c_controls_eload_fall.setEnabled(True)
                self.ui.label_i2c_controls_eload_fall_unit.setEnabled(True)
        elif self.ui.cbx_i2c_controls_eload_type.currentText() == ELoadTypes.CV:
            self.ui.label_i2c_controls_eload_a_level_unit.setText('V')
            self.ui.label_i2c_controls_eload_b_level_unit.setText('V')
            self.ui.label_i2c_controls_electronic_load_rise.setEnabled(True)
            self.ui.lineedit_i2c_controls_eload_rise.setEnabled(True)
            self.ui.label_i2c_controls_eload_rise_unit.setEnabled(True)
            self.ui.label_i2c_controls_eload_rise_unit.setText('A')
            self.ui.label_i2c_controls_electronic_load_rise.setText('Limit')
            self.ui.label_i2c_controls_electronic_load_fall.setEnabled(False)
            self.ui.lineedit_i2c_controls_eload_fall.setEnabled(False)
            self.ui.label_i2c_controls_eload_fall_unit.setEnabled(False)
        elif self.ui.cbx_i2c_controls_eload_type.currentText() == ELoadTypes.CP:
            self.ui.label_i2c_controls_eload_a_level_unit.setText('W')
            self.ui.label_i2c_controls_eload_b_level_unit.setText('W')
            if self.electronic_load.cp_slew_unit[0] ==  'A':
                self.ui.label_i2c_controls_eload_rise_unit.setText('A / µs')
                self.ui.label_i2c_controls_eload_fall_unit.setText('A / µs')
            else:
                self.ui.label_i2c_controls_eload_rise_unit.setText('W / µs')
                self.ui.label_i2c_controls_eload_fall_unit.setText('W / µs')
            self.ui.lineedit_i2c_controls_eload_rise.setText('0.15')
            self.ui.lineedit_i2c_controls_eload_fall.setText('0.15')
            self.ui.label_i2c_controls_electronic_load_rise.setEnabled(True)
            self.ui.lineedit_i2c_controls_eload_rise.setEnabled(True)
            self.ui.label_i2c_controls_eload_rise_unit.setEnabled(True)
            self.ui.label_i2c_controls_electronic_load_fall.setEnabled(True)
            self.ui.lineedit_i2c_controls_eload_fall.setEnabled(True)
            self.ui.label_i2c_controls_eload_fall_unit.setEnabled(True)

        
    def ac_source_power_on(self):
        if (self.ui.lineedit_i2c_controls_ac_source_voltage.text() == ''):
            self.parent.msg_box_info(
                title="AC Source Error",
                message=f"Please enter the input voltage.",
                message_type = MessageType.INFO
                )
            return
    
        vin_V = rounded_float(self.ui.lineedit_i2c_controls_ac_source_voltage.text())
        self.update_ac_source_coupling()
        
        if self.ac_source.coupling == AC_SOURCE_COUPLING.AC:    
            if (self.ui.lineedit_i2c_controls_ac_source_frequency.text() == ''):
                if vin_V >= 180:
                    freq = 50
                else:
                    freq = 60
                self.ui.lineedit_i2c_controls_ac_source_frequency.setText(f'{freq:g}')
            else:
                freq = rounded_float(self.ui.lineedit_i2c_controls_ac_source_frequency.text())
            self.ac_source.frequency = freq
            
        self.ac_source.set_voltage_with_coupling(voltage= vin_V, coupling= self.ac_source.coupling) 
        self.ac_source.turn_on() 
        
    def ac_source_power_off(self):
        self.ac_source.turn_off()
        
    def setup_update_timer(self):
        self.update_timer = QTimer(self.parent)
        self.update_timer.timeout.connect(self.update_service)

    def stop(self):
        #print("Stop I2C Controls Page")
        self.update_timer.stop()
        if self.power_meter_source:
            try:
                self.power_meter_source.set_integration_timer(timer_s=self.power_meter_source_integ_timer)
            except Exception as e:
                print('Power meter source integration timer error')
            
        if self.power_meter_load:
            try: 
                self.power_meter_load.set_integration_timer(timer_s=self.power_meter_load_integ_timer)
            except Exception as e:
                print('Power meter sload integration timer error') 
        #self.clear_all_frames()
        if self.usbpd_sink is not None:
            try:
                self.usbpd_sink.close()
            except Exception as e:
                print(e)

    def update_service(self):
        self.update_timer.stop()
        self.gpib_update()
        self.power_meter_ui_update()
        
        self.update_timer.start()
        
    def gpib_update(self):
        if self.power_meter_load is not None:
            self.power_meter_load_update()
        if self.power_meter_source is not None:
            self.power_meter_source_update()
        
    def power_meter_load_update(self):
        """ Update power meter parameters
        
        Wrapped with error handling
        """
        try:
            if self.power_meter_load_ready:
                self.power_meter_load.update_basic_params()
        except Exception as e:
            self.power_meter_load_ready = False
            self.ui_power_meter_load_update_fail()

    def power_meter_source_update(self):
        """ Update power meter parameters
        
        Wrapped with error handling
        """
        try:
            if self.power_meter_source_ready:
                self.power_meter_source.update_basic_params()
        except Exception as e:
            self.power_meter_source_ready = False
            self.ui_power_meter_source_update_fail()

    def power_meter_ui_update(self):
        try:
            if (self.power_meter_source is not None) and (self.power_meter_source_ready):
                self.ui_power_meter_source_update()
        except Exception as e:
            self.power_meter_load_ready = False
            self.ui_power_meter_source_update_fail()
        
        try:
            if (self.power_meter_load is not None) and (self.power_meter_load_ready):
                self.ui_power_meter_load_update()
        except Exception as e:
            self.power_meter_load_ready = False
            self.ui_power_meter_load_update_fail()
    
    def ui_power_meter_source_update(self):
        # Source power meter display
        try:
            # Set arbitrary limit to validate result (10k)
            voltage = self.power_meter_source._voltage
            if voltage < 10e3:
                self.ui.label_i2c_controls_pms_display_a.setText(f'{voltage:.2f} V')
            current = self.power_meter_source._current
            if current < 10e3:
                self.ui.label_i2c_controls_pms_display_b.setText(f'{current:.2f} A')
            self.Pin_W = self.power_meter_source._power
            if self.Pin_W < 10e3:
                self.ui.label_i2c_controls_pms_display_c.setText(f'{self.Pin_W:.2f} W')
            pf = self.power_meter_source._pf*100
            if ((pf >= 0) & (pf <= 100)):
                self.ui.label_i2c_controls_pms_display_d.setText(f'{pf:.2f}% PF')
            else:
               self.ui.label_i2c_controls_pms_display_d.setText('None') 
        except:
            self.ui_power_meter_source_update_fail()
            self.power_meter_source_ready = False

    def ui_power_meter_load_update(self):
        # Load power meter display
        try:
            # Set arbitrary limit to validate result (10k)
            voltage = self.power_meter_load._voltage
            if voltage < 10e3:
                self.ui.label_i2c_controls_pml_display_a.setText(f'{voltage:.2f} V')
            current = self.power_meter_load._current
            if current < 10e3:
                self.ui.label_i2c_controls_pml_display_b.setText(f'{current:.2f} A')
            self.Pout_W = self.power_meter_load._power
            if self.Pout_W < 10e3:
                self.ui.label_i2c_controls_pml_display_c.setText(f'{self.Pout_W:.2f} W')
            if (self.Pin_W > 0) and (self.Pout_W < 10e3) and (self.Pin_W < 10e3):
                eff = self.Pout_W/self.Pin_W*100
                self.ui.label_i2c_controls_pml_display_d.setText(f'{eff:.2f}% Eff')
            else:
                self.ui.label_i2c_controls_pml_display_d.setText('None')
        except:
            self.ui_power_meter_load_update_fail()
            self.power_meter_load_ready = False
    
    def ui_power_meter_load_update_fail(self):
        self.ui.label_i2c_controls_pml_display_a.setText('None')
        self.ui.label_i2c_controls_pml_display_b.setText('None')
        self.ui.label_i2c_controls_pml_display_c.setText('None')
        self.ui.label_i2c_controls_pml_display_d.setText('None')
        
    def ui_power_meter_source_update_fail(self):
        self.ui.label_i2c_controls_pms_display_a.setText('None')
        self.ui.label_i2c_controls_pms_display_b.setText('None')
        self.ui.label_i2c_controls_pms_display_c.setText('None')
        self.ui.label_i2c_controls_pms_display_d.setText('None')
            
    def clear_all_frames(self):
        for i in reversed(range(self.grid_reg1.count())): 
                self.grid_reg1.itemAt(i).widget().deleteLater()
        
        for i in reversed(range(self.grid_reg2.count())): 
                self.grid_reg2.itemAt(i).widget().deleteLater()
                
        for i in reversed(range(self.grid_reg3.count())): 
                self.grid_reg3.itemAt(i).widget().deleteLater()
                
        for i in reversed(range(self.grid_reg4.count())): 
                self.grid_reg4.itemAt(i).widget().deleteLater()
                
        for i in reversed(range(self.grid_reg5.count())): 
                self.grid_reg5.itemAt(i).widget().deleteLater()
                   
        for i in reversed(range(self.grid_reg6.count())): 
                self.grid_reg6.itemAt(i).widget().deleteLater()
                
        for i in reversed(range(self.grid_reg7.count())): 
                self.grid_reg7.itemAt(i).widget().deleteLater()
        
        for i in reversed(range(self.grid_reg8.count())): 
                self.grid_reg8.itemAt(i).widget().deleteLater()
                
        for i in reversed(range(self.grid_reg9.count())): 
                self.grid_reg9.itemAt(i).widget().deleteLater()
                
        for i in reversed(range(self.grid_reg10.count())): 
                self.grid_reg10.itemAt(i).widget().deleteLater()
                
        for i in reversed(range(self.grid_reg11.count())): 
                self.grid_reg11.itemAt(i).widget().deleteLater()
                   
        for i in reversed(range(self.grid_reg12.count())): 
                self.grid_reg12.itemAt(i).widget().deleteLater()
                
        for i in reversed(range(self.grid_reg13.count())): 
                self.grid_reg13.itemAt(i).widget().deleteLater()
                
        for i in reversed(range(self.grid_reg14.count())): 
                self.grid_reg14.itemAt(i).widget().deleteLater()
                
        for i in reversed(range(self.grid_reg15.count())): 
                self.grid_reg15.itemAt(i).widget().deleteLater()
                   
        for i in reversed(range(self.grid_reg16.count())): 
                self.grid_reg16.itemAt(i).widget().deleteLater()
                
        for i in reversed(range(self.grid_reg17.count())): 
                self.grid_reg17.itemAt(i).widget().deleteLater()
        
        for i in reversed(range(self.grid_reg18.count())): 
                self.grid_reg18.itemAt(i).widget().deleteLater()
                
        for i in reversed(range(self.grid_reg19.count())): 
                self.grid_reg19.itemAt(i).widget().deleteLater()
                
        for i in reversed(range(self.grid_reg20.count())): 
                self.grid_reg20.itemAt(i).widget().deleteLater()
                
        for i in reversed(range(self.grid_reg21.count())): 
                self.grid_reg21.itemAt(i).widget().deleteLater()
                   
        for i in reversed(range(self.grid_reg22.count())): 
                self.grid_reg22.itemAt(i).widget().deleteLater()
        
        for i in reversed(range(self.grid_reg23.count())): 
                self.grid_reg23.itemAt(i).widget().deleteLater()
        
        for i in reversed(range(self.grid_reg24.count())): 
                self.grid_reg24.itemAt(i).widget().deleteLater()
        
        for i in reversed(range(self.grid_readback_reg_any.count())): 
                self.grid_readback_reg_any.itemAt(i).widget().deleteLater()
                
        for i in reversed(range(self.grid_readback_reg0.count())): 
                self.grid_readback_reg0.itemAt(i).widget().deleteLater()
                
        for i in reversed(range(self.grid_readback_reg1.count())): 
                self.grid_readback_reg1.itemAt(i).widget().deleteLater()     
        
        for i in reversed(range(self.grid_readback_reg2.count())): 
                self.grid_readback_reg2.itemAt(i).widget().deleteLater()     
                
        for i in reversed(range(self.grid_readback_reg3.count())): 
                self.grid_readback_reg3.itemAt(i).widget().deleteLater()      
        
        for i in reversed(range(self.grid_readback_reg4.count())): 
                self.grid_readback_reg4.itemAt(i).widget().deleteLater()  
        
        for i in reversed(range(self.grid_readback_reg5.count())): 
                self.grid_readback_reg5.itemAt(i).widget().deleteLater()          
        
        for i in reversed(range(self.grid_readback_reg6.count())): 
                self.grid_readback_reg6.itemAt(i).widget().deleteLater()
                
        for i in reversed(range(self.grid_readback_reg7.count())): 
                self.grid_readback_reg7.itemAt(i).widget().deleteLater()     
        
        for i in reversed(range(self.grid_readback_reg8.count())): 
                self.grid_readback_reg8.itemAt(i).widget().deleteLater()     
                
        for i in reversed(range(self.grid_readback_reg9.count())): 
                self.grid_readback_reg9.itemAt(i).widget().deleteLater()      
        
        for i in reversed(range(self.grid_readback_reg10.count())): 
                self.grid_readback_reg10.itemAt(i).widget().deleteLater()  
        
        for i in reversed(range(self.grid_readback_reg11.count())): 
                self.grid_readback_reg11.itemAt(i).widget().deleteLater()      
        
        for i in reversed(range(self.grid_readback_reg12.count())): 
                self.grid_readback_reg12.itemAt(i).widget().deleteLater()     
                
        for i in reversed(range(self.grid_readback_reg13.count())): 
                self.grid_readback_reg13.itemAt(i).widget().deleteLater()      
        
        for i in reversed(range(self.grid_readback_reg14.count())): 
                self.grid_readback_reg14.itemAt(i).widget().deleteLater()  
        
        for i in reversed(range(self.grid_readback_reg15.count())): 
                self.grid_readback_reg15.itemAt(i).widget().deleteLater()          
        
        for i in reversed(range(self.grid_readback_reg16.count())): 
                self.grid_readback_reg16.itemAt(i).widget().deleteLater()
                
        for i in reversed(range(self.grid_readback_reg17.count())): 
                self.grid_readback_reg17.itemAt(i).widget().deleteLater()     
        
        for i in reversed(range(self.grid_readback_reg18.count())): 
                self.grid_readback_reg18.itemAt(i).widget().deleteLater()     
                
        for i in reversed(range(self.grid_readback_reg19.count())): 
                self.grid_readback_reg19.itemAt(i).widget().deleteLater()      
        
        for i in reversed(range(self.grid_readback_reg20.count())): 
                self.grid_readback_reg20.itemAt(i).widget().deleteLater()  
        
        for i in reversed(range(self.grid_readback_reg21.count())): 
                self.grid_readback_reg21.itemAt(i).widget().deleteLater()      
        
        for i in reversed(range(self.grid_readback_reg22.count())): 
                self.grid_readback_reg22.itemAt(i).widget().deleteLater()     
                
        for i in reversed(range(self.grid_readback_reg23.count())): 
                self.grid_readback_reg23.itemAt(i).widget().deleteLater()      
        
        for i in reversed(range(self.grid_readback_reg24.count())): 
                self.grid_readback_reg24.itemAt(i).widget().deleteLater()  
                 
        for i in reversed(range(self.grid_vben_reg.count())): 
                 self.grid_vben_reg.itemAt(i).widget().deleteLater()
                 
        for i in reversed(range(self.grid_watchdog_reg.count())): 
                 self.grid_watchdog_reg.itemAt(i).widget().deleteLater()
                 
        for i in reversed(range(self.grid_loop_option_reg.count())): 
                 self.grid_loop_option_reg.itemAt(i).widget().deleteLater()
    
    # Functions for Common I2C Commands Section
    
    @i2c_access
    @send_btn_update  
    def send_command_vben(self):
        match self.innoswitch_family:
            case InnoProFamily.Inno5Pro:
                return inno5_send_command_write(self,self.vben_reg)
            case InnoProFamily.Inno4Pro:
                return inno4_send_command_write(self,self.vben_reg)
    
    def queue_command_vben(self):
        match self.innoswitch_family:
            case InnoProFamily.Inno5Pro:
                inno5_queue_cmd_fnc(self,self.vben_reg)
            case InnoProFamily.Inno4Pro:
                inno4_queue_cmd_fnc(self,self.vben_reg)

            
    @i2c_access
    @send_btn_update  
    def send_command_watchdog(self):
        match self.innoswitch_family:
            case InnoProFamily.Inno5Pro:
                return inno5_send_command_write(self,self.watchdog_reg)
            case InnoProFamily.Inno4Pro:
                return inno4_send_command_write(self,self.watchdog_reg)
    
    def queue_command_watchdog(self):
        match self.innoswitch_family:
            case InnoProFamily.Inno5Pro:
                inno5_queue_cmd_fnc(self,self.watchdog_reg)
            case InnoProFamily.Inno4Pro:
                inno4_queue_cmd_fnc(self,self.watchdog_reg)
            
    @i2c_access
    @send_btn_update  
    def send_command_loop_option(self):
        match self.innoswitch_family:
            case InnoProFamily.Inno5Pro:
                return inno5_send_command_write(self,self.loop_option_reg)
            case InnoProFamily.Inno4Pro:
                return inno4_send_command_write(self,self.loop_option_reg)
    
    def queue_command_loop_option(self):
        match self.innoswitch_family:
            case InnoProFamily.Inno5Pro:
                inno5_queue_cmd_fnc(self,self.loop_option_reg)
            case InnoProFamily.Inno4Pro:
                inno4_queue_cmd_fnc(self,self.loop_option_reg)
                pass
    @i2c_access
    @send_btn_update  
    def i2c_initialize(self):
        match self.innoswitch_family:
            case InnoProFamily.Inno5Pro:
                return inno5_i2c_initialize(self), self.ui.btn_i2c_controls_initialize
            case InnoProFamily.Inno4Pro:
                return inno4_i2c_initialize(self), self.ui.btn_i2c_controls_initialize
            
    @i2c_access
    @send_btn_update  
    def i2c_set_nr(self):
        match self.innoswitch_family:
            case InnoProFamily.Inno5Pro:
                return inno5_i2c_set_nr(self), self.ui.btn_i2c_controls_set_nr
            case InnoProFamily.Inno4Pro:
                return inno4_i2c_set_nr(self), self.ui.btn_i2c_controls_set_nr
    
    
    # I2C Command List Functions
    
    def save_command_list(self):
        """"Save the command list to a .json file"""
        username = os.getlogin()
        
        default_path = self.parent_folder_path

        # Create dialog window for file selection
        dialog = QtWidgets.QFileDialog()
        default_filename = 'ATE_I2C_Command_List'
        command_list_save_path, path_file_type = dialog.getSaveFileName(
             self.parent, "Save I2C Command List", f'{default_path}\{default_filename}.json', "JSON Source File (*.json)")
        
        # Handling of file input
        if command_list_save_path == '':
            return
        if not ((command_list_save_path.split('.'))[-1]).lower() == 'json':
            command_list_save_path = command_list_save_path + '.json'
        obj_list = []
        for index, command in enumerate(self.i2c_command_list):
            d = command.get_dict()
            obj_list.append(d)
        
        with open(command_list_save_path, 'w') as command_list_file:
            json.dump(obj_list, command_list_file, indent=2)
       
    def load_command_list(self):
        """"Load the command list from a .json file"""
        username = os.getlogin()
        default_path = self.parent_folder_path

        # Create dialog window for file selection
        dialog = QtWidgets.QFileDialog()
        command_list_load_path, path_file_type = dialog.getOpenFileName(
            self.parent, 'Select I2C Command List', default_path, "JSON Source File (*.json)")

        # Handling of file input
        if command_list_load_path == '':
            return
        while not ((command_list_load_path.split('.'))[-1]).lower() == 'json':
            self.parent.msg_box_info(
                title="Load I2C Command List",
                message=f"Incorrect file type. File type must be "".json""",
                message_type = MessageType.WARNING
                )
            default_path = command_list_load_path.replace(command_list_load_path.split('\\')[-1],'')
            command_list_load_path, path_file_type = dialog.getOpenFileName(
                self.parent, 'Load I2C Command List', default_path, "JSON Source File (*.json)")
            if command_list_load_path == '':
                return

        with open(command_list_load_path, "r") as command_list_file:
            command_dict_list = json.load(command_list_file)
        
        # Go through each test item
        for command_dict in command_dict_list:
            self.add_dict_to_command_list(command_dict)
        self.update_i2c_command_list_table()
        
    def get_dict(self,command_name,command_value,command_extra_params)->dict:
        d = {'COMMAND_NAME':            command_name, 
            'COMMAND_VALUE':            command_value,
            'COMMAND_EXTRA_PARAMS':     command_extra_params}
        return d
    
    def add_dict_to_command_list(self,command_dict:dict):
        command = I2CCommandObject()
        command.extract_params_from_dict(command_dict)
        self.i2c_command_list.append(command)
        
    def add_delay_to_command_list(self):
        if self.command_list_delay.text() == '':
            return
        else:
            delay_ms = rounded_float(self.command_list_delay.text())
            command = I2CCommandObject(name='Delay',value=f'{delay_ms:g} ms',extra_params=None) 
            self.i2c_command_list.append(command)

        self.update_i2c_command_list_table()

    def clear_command_list(self):
        self.i2c_command_list.clear()        
        self.update_i2c_command_list_table()
    
    def delete_single_from_command_list(self):
        selection_index = self.command_list_table.currentRow()
        # If there is a selection, 
        if not selection_index == -1:
            self.i2c_command_list.pop(selection_index)
        self.update_i2c_command_list_table()
    
    def run_single_from_command_list(self):
        selection_index = self.command_list_table.currentRow()
        # If there is a selection, 
        if not selection_index == -1:
            try:
                command:I2CCommandObject = self.i2c_command_list[selection_index]
                if command.name == 'Delay':
                    delay_ms = rounded_float(command.value[:-3])
                    sleep(delay_ms/1000)
                elif (command.name[:4].upper()) == 'READ':
                    match self.innoswitch_family:
                        case InnoProFamily.Inno5Pro:
                            inno5_run_queue_command_read(self,command.name,
                                    command.value,command.extra_params)
                        case InnoProFamily.Inno4Pro:
                            inno4_run_queue_command_read(self,command.name,
                                    command.value,command.extra_params)
                else:
                    match self.innoswitch_family:
                        case InnoProFamily.Inno5Pro:
                            inno5_run_queue_command_write(self,command.name,
                                    command.value,command.extra_params)
                        case InnoProFamily.Inno4Pro:
                            inno4_run_queue_command_write(self,command.name,
                                    command.value,command.extra_params)
                self.command_list_table.setCurrentIndex(self.command_list_table.model().index(selection_index+1,0))
            except Exception as e:
                print(e)
    
    def run_command_list(self):
        self.i2c_command_list_running = True
        self.i2c_command_thread = QThread()
        # Bind thread to parent to prevent it from expiring unexpectedly
        self.parent.i2c_command_thread = self.i2c_command_thread 
        self.i2c_command_worker = I2CCommandsWorker(self,self.i2c_command_list,self.command_list_table)
        # Move worker to the thread
        self.i2c_command_worker.moveToThread(self.i2c_command_thread)
        # Connect signals and slots for the thread
        self.i2c_command_thread.started.connect(self.i2c_command_worker.run)
        self.i2c_command_worker.finished.connect(self.i2c_commands_finished)
        self.i2c_command_thread.finished.connect(self.stop_command_list)
        
        sleep(1)
        # Start the thread
        self.i2c_command_list_thread_running = True
        self.i2c_command_thread.start()
        self.update_i2c_commands_ui()
    
    def stop_command_list(self):
        self.i2c_command_list_thread_running = False
        self.i2c_command_worker.deleteLater()
        self.i2c_command_thread.deleteLater()
        def set_objects_to_none():
            self.i2c_command_thread = None
            self.parent.i2c_command_thread = None
            self.i2c_command_list_running = False
            self.update_i2c_commands_ui()
            for thread in threading.enumerate():
                print(thread) 
        if self.i2c_command_thread is not None:
            QTimer.singleShot(3000, set_objects_to_none)
                 
            
    def update_i2c_commands_ui(self):
        if self.i2c_command_list_running:
            self.ui.btn_i2c_controls_command_run_all.setEnabled(False)
            self.ui.btn_i2c_controls_command_run_single.setEnabled(False)
        else:
            self.ui.btn_i2c_controls_command_run_all.setEnabled(True)
            self.ui.btn_i2c_controls_command_run_single.setEnabled(True)
    
    def update_i2c_command_list_table(self):
        self.command_list_table.clearContents()    
        self.command_list_table.setHorizontalHeaderLabels(['Function', 'Value'])
        self.command_list_table.setRowCount(len(self.i2c_command_list))
        for i, command in enumerate(self.i2c_command_list):
            self.command_list_table.setItem(
                i, 0, QtWidgets.QTableWidgetItem(command.name))
            
            self.command_list_table.setItem(
                i, 1, QtWidgets.QTableWidgetItem(command.value))
            
        # Backup command list to a .json file each time the test list is updated
        if len(self.i2c_command_list) == 0:
            return
        
        obj_list = []
        
        for command in self.i2c_command_list:
            d = self.get_dict(command.name,command.value,command.extra_params)
            obj_list.append(d)
            
        with open(configs.i2c_command_list_filepath, 'w') as command_list_file:
            json.dump(obj_list, command_list_file, indent=2)
        
    def i2c_commands_finished(self):
        self.i2c_command_thread.quit()
        
            
class I2CCommandsWorker(QObject):
    """This class is a thread worker for the run_command_list function"""
    finished = Signal()

    def __init__(self, page_handler:I2CControlsPageHandler,i2c_command_list:list[I2CCommandObject],command_list_table):
        super().__init__()
        self.parent = super().parent
        self.i2c_controller = page_handler.i2c_controller
        self.usbpd_sink = page_handler.usbpd_sink
        self.command_list_table = command_list_table
        self.i2c_command_list = i2c_command_list
        self.page_handler = page_handler
        self.popup_status = False
        
    def run(self):
        """Run the routine for executing i2c commands."""     
        # The whole routine is checked for error.
        # The main thread will do the handling
        debugpy.debug_this_thread()
        try:
            self.command_list_table.setCurrentIndex(self.command_list_table.model().index(0,0))
            for index, command in enumerate(self.i2c_command_list):
                while self.popup_status:
                    sleep(0.5)
                self.command_list_table.setCurrentIndex(self.command_list_table.model().index(index,0))
                if command.name == 'Delay':
                    delay_s = rounded_float(command.value[:-3])/1000
                    sleep(delay_s)
                    # QThread.msleep(delay_ms)
                elif (command.name)[:4].upper() == 'READ':
                    match self.page_handler.innoswitch_family:
                        case InnoProFamily.Inno5Pro:
                            inno5_run_queue_command_read(self.page_handler,command.name,
                                command.value,command.extra_params)
                        case InnoProFamily.Inno4Pro:
                            inno4_run_queue_command_read(self.page_handler,command.name,
                                command.value,command.extra_params)
                else:
                    match self.page_handler.innoswitch_family:
                        case InnoProFamily.Inno5Pro:
                            inno5_run_queue_command_write(self.page_handler,command.name,
                                command.value,command.extra_params)
                        case InnoProFamily.Inno4Pro:
                            inno4_run_queue_command_write(self.page_handler,command.name,
                                command.value,command.extra_params)
            self.finished.emit()
            return
        except Exception as e:
            print(e)
            self.finished.emit()
            return
        
    def update_popup_status(self,status):
        self.popup_status = status
            