import os
import json
from copy import copy
from time import sleep

from app.app_modules import *

from page_controls.manual_control import ManualControlPageHandler
from sink_controllers.epr_sink_control import *
from sink_controllers.definitions import * 
from sink_controllers.pi_epr_sink import *

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (
    QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QTimer,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent, Signal, Slot, QThread)
from PySide2.QtGui import (
    QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase,
    QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, 
    QRadialGradient,QIntValidator,QDoubleValidator)
from PySide2.QtWidgets import *

import numpy as np

from pyvisa import VisaIOError

from equipment.ac_source import ACSource
from equipment.electronic_load import ElectronicLoadModule
from equipment.handler import EquipmentHandler

from psu_tests.tests import (TestItem, TestPlan,)

from psu_tests.definitions import (
    MessageType, LineSettings, LineRange, LoadSettings, LoadRange, LineRamp, LineRampSettings, SoakTime, SoaktimeSettings, TestStatus,
    CVCCSettings,TestConditionSettings, I2CTestParameters, test_control_flags)
from psu_tests.test_file_template import TemplateTest
from psu_tests.test_type import *

from misc_functions.misc_functions import *

import user_settings.save_load as configs
from user_settings.keys import SaveFileKeys


from psu_tests.definitions import (USBPDOptions, GeneralOptions, TestConditions)
from psu_tests.ui_definitions import *

from page_controls.definitions import (StackWidget1Pages, StackWidget2Pages)

from pd.pd_types import PD_SPECS, SourceCap


from ui.ui_styles import *

from main import MainWindow, Ui_MainWindow

TEST_PLAN_UPDATE_TIMER = 200

class InputError(Exception):
    pass

# TODO: if output folder path is blank, replace it with desktop
class AddTestPageHandler(QObject):

    stop_test_thread = Signal()

    def __init__(self, parent:MainWindow) -> None:
        super().__init__()
        self.parent:MainWindow = parent
        self.ui:Ui_MainWindow = parent.ui
        self.equipment:EquipmentHandler = parent.equipment

        self.test_plan:TestPlan = parent.test_plan
        self.line_settings:LineSettings = parent.line_settings
        self.load_settings:LoadSettings = parent.load_settings
        self.line_ramp_settings:LineRampSettings = parent.line_ramp_settings
        self.soaktime_settings:SoaktimeSettings = parent.soaktime_settings
        self.test_condition_settings:TestConditionSettings = parent.test_condition_settings
        # Objects for combo box selected ranges
        self.selected_line_range:LineRange
        self.selected_load_range:LoadRange
        self.selected_soaktime: SoakTime
        # Thread object container
        self.test_routine_thread:QThread = None
        self.get_source_caps_thread:QThread = None

        # 
        self.test_type_index = 0
        self.item_selected = False
        self.ongoing_load_range_update = False
        self.test_item_selection_item_changed_flag = False
        self.test_item_selection_changed_flag = False
        self.test_item_click_flag = False
        self.soak_time_selection_changed = False
        
        self.i2c_tests_names = [x.title for x in I2C_TestTypes]
        self.inno_family_update_ready = False
        
        
        self.bind_ui_elements()
        self.initialize_ui_states()
        self.setup_testplan_update_timer()

    def start(self):
        self.setup_equipment()

    def setup_equipment(self):
        self.ac_source:ACSource = self.equipment.ac_source
        self.usbpd_sink = self.equipment.usbpd_sink
        self.electronic_load = self.equipment.electronic_load_1
        
    def bind_ui_elements(self):
        self.bind_page_buttons()
        self.bind_ui_change_events()

    def bind_page_buttons(self):
        # Bind Open Folder Button
        self.ui.btn_add_tests_output_folder_location.clicked.connect(
            self.select_output_directory)
        
        # Bind open explorer button
        self.ui.btn_add_tests_open_output_folder.clicked.connect(
            self.open_output_directory)

        # Bind GET SOURCE CAPS Button
        self.ui.btn_add_tests_usbpd_get_source_caps.clicked.connect(
            self.get_source_caps)
        
        # Bind Add Test Button
        self.ui.btn_add_tests_option_1.clicked.connect(
            self.add_single_test)

        # Bind TEST ALL FIXED SOURCE Button
        self.ui.btn_add_tests_option_2.clicked.connect(
            self.test_all_fixed_pdos)

        # Bind Save Plan Button
        self.ui.btn_add_tests_save_test_plan.clicked.connect(
            self.save_test_plan)
        
        # Bind Load Plan Button
        self.ui.btn_add_tests_load_test_plan.clicked.connect(
            self.load_test_plan)
        
        # Bind Move Up Button
        self.ui.btn_add_tests_test_item_move_up.clicked.connect( 
            self.move_up_selected_test)

        # Bind Move Down Button
        self.ui.btn_add_tests_test_item_move_down.clicked.connect( 
            self.move_down_selected_test)
        
        # Bind Move to Top Button
        self.ui.btn_add_tests_test_item_move_top.clicked.connect( 
            self.move_top_selected_test)
        
        # Bind Move to Bottom Button
        self.ui.btn_add_tests_test_item_move_bottom.clicked.connect( 
            self.move_bottom_selected_test)
        
        # Bind Restart Selected Test Button
        self.ui.btn_add_tests_restart_selected_test.clicked.connect(
            self.restart_selected_test)
        
         # Bind Update Selected Test Button
        self.ui.btn_add_tests_update_selected_test.clicked.connect(
            self.update_selected_test)
        
        # Bind Remove Selected Test Button
        self.ui.btn_add_tests_remove_selected_test.clicked.connect(
            self.remove_test)
        
        # Bind Skip Selected Test Button
        self.ui.btn_add_tests_skip_selected_test.clicked.connect(
            self.skip_selected_test)
        
        # Bind Restart All Test Button
        self.ui.btn_add_tests_restart_all_test.clicked.connect(
            self.restart_all_test)
        
        # Bind Clear Test List Button
        self.ui.btn_add_tests_clear_all_test.clicked.connect(
            self.clear_test)

        # Bind RUN TESTS Button
        self.ui.btn_add_tests_run.clicked.connect(
            self.run_tests)
        
        # Bind STOP TEST Button
        self.ui.btn_add_tests_stop.clicked.connect(
            self.stop_tests)

        # Bindings for modifying line settings
        self.ui.btn_add_tests_line_range_add_setting.clicked.connect(
            self.custom_line_setting_add_entry)
        self.ui.btn_add_tests_line_range_remove_setting.clicked.connect(
            self.custom_line_setting_remove_entry)
        self.ui.btn_add_tests_line_range_duplicate_setting.clicked.connect(
            self.custom_line_setting_duplicate_entry)
        
        # Bindings for modifying line ramp settings
        self.ui.btn_add_tests_line_ramp_add_setting.clicked.connect(
            self.custom_line_ramp_setting_add_entry)
        self.ui.btn_add_tests_line_ramp_remove_setting.clicked.connect(
            self.custom_line_ramp_setting_remove_entry)
        self.ui.btn_add_tests_line_ramp_duplicate_setting.clicked.connect(
            self.custom_line_ramp_setting_duplicate_entry)

        # Bindings for modifying load settings
        self.ui.btn_add_tests_load_range_add_setting.clicked.connect(
            self.custom_load_setting_add_entry)
        self.ui.btn_add_tests_load_range_remove_setting.clicked.connect(
            self.custom_load_setting_remove_entry)
        self.ui.btn_add_tests_load_range_duplicate_setting.clicked.connect(
            self.custom_load_setting_duplicate_entry)
        
        # Bindings for modifying soaktime settings
        self.ui.btn_add_tests_timing_params_add_setting.clicked.connect(
            self.custom_timing_params_add_entry)
        self.ui.btn_add_tests_timing_params_remove_setting.clicked.connect(
            self.custom_timing_params_remove_entry)
        self.ui.btn_add_tests_timing_params_duplicate_setting.clicked.connect(
            self.custom_timing_params_duplicate_entry)

        # Bindings for adding/removing entries in Line/Load ranges
        self.ui.btn_add_tests_line_range_add.clicked.connect(
            self.custom_line_range_add_entry)
        self.ui.btn_add_tests_line_ramp_add.clicked.connect(
            self.custom_line_ramp_add_entry)
        self.ui.btn_add_tests_load_range_add.clicked.connect(
            self.custom_load_range_add_entry)
        self.ui.btn_add_tests_line_range_remove.clicked.connect(
            self.custom_line_range_remove_entry)
        self.ui.btn_add_tests_line_ramp_remove.clicked.connect(
            self.custom_line_ramp_remove_entry)
        self.ui.btn_add_tests_load_range_remove.clicked.connect(
            self.custom_load_range_remove_entry)
        self.ui.btn_add_tests_line_range_clear.clicked.connect(   
            self.custom_line_range_clear_entry)
        self.ui.btn_add_tests_line_ramp_clear.clicked.connect(   
            self.custom_line_ramp_clear_entry)
        self.ui.btn_add_tests_load_range_clear.clicked.connect(    
            self.custom_load_range_clear_entry)

    def bind_ui_change_events(self):
        # Bind Line range combo box to list widget update
        self.ui.cbx_add_tests_line_range_type.currentIndexChanged.connect(\
            self.update_line_range_table)

         # Bind Line ramp setting combo box to list widget update
        self.ui.cbx_add_tests_line_ramp_type.currentIndexChanged.connect(\
            self.update_line_ramp_table)
        
        # Bind load range combo box to list widget update
        self.ui.cbx_add_tests_load_range_type.currentIndexChanged.connect(\
            self.update_load_range_table)
        #Bind soaktime combo box to list widget update
        self.ui.cbx_add_tests_timing_params.currentIndexChanged.connect(\
            self.update_soaktime_list)
        # The testtype combobox is controlling two stacked widgets 
        # which will display the necessaryinput fields 
        # for the selected text
        self.ui.cbx_add_tests_testtype.currentIndexChanged.connect(
            self.test_type_index_changed)
        
        # The USBPD Device? checkbox controls which ui items are displayed 
        self.ui.chkbox_add_tests_usbpd_device.stateChanged.connect(
            self.usbpd_dev_toggle_changed)

        # Select results folder shows the combo box for the results folder
        # Results folder is used instead of creating a new one
        self.ui.chkbox_add_tests_results_folder.stateChanged.connect(
            self.results_folder_toggle_changed)

        self.ui.cbx_add_tests_results_folder.currentIndexChanged.connect(
            self.result_folder_cbx_changed)

        self.ui.chkbox_add_tests_cvcc_multi_setpoints.stateChanged.connect(
            self.cvcc_multi_setpoints_toggle_changed)
    
        # Bindings for test list interaction
        self.ui.table_add_tests_test_list.itemClicked.connect(
            self.test_item_clicked)
        self.ui.table_add_tests_test_list.itemSelectionChanged.connect(
            self.test_item_selection_changed)
        self.ui.table_add_tests_test_list.itemChanged.connect(
             self.test_item_selected_item_changed)
        
        self.ui.lineedit_add_tests_nominal_output_current.textChanged.connect(
            self.update_load_range_table)
        self.ui.lineedit_add_tests_nominal_output_voltage.textChanged.connect(
            self.update_load_range_table)
        
        self.ui.table_add_tests_source_caps.itemSelectionChanged.connect(
            self.source_caps_table_selected)
        
        # For when soaktime setting fields are changed
        self.ui.lineedit_add_tests_testtime_param1.textChanged.connect(
            self.update_initial_soak_setting)
        self.ui.lineedit_add_tests_testtime_param2.textChanged.connect(
            self.update_soak_per_line_setting)
        self.ui.lineedit_add_tests_testtime_param3.textChanged.connect(
            self.update_soak_per_load_setting)
        self.ui.lineedit_add_tests_testtime_param4.textChanged.connect(
            self.update_integration_time_setting)
        
        self.ui.widget_toggle_add_tests_line_range_coupling.stateChanged.connect(
            self.line_range_coupling_toggle_changed)
        self.ui.widget_toggle_add_tests_line_ramp_coupling.stateChanged.connect(
            self.input_line_ramp_coupling_toggle_changed)
        
# TODO: Open the current directory
    def select_output_directory(self):
        """Opens a prompt to select the directory for the outputs"""

        username = os.getlogin()
        default_path = os.path.join('C:\\','users', username, 'Desktop') 

        dialog = QtWidgets.QFileDialog()

        output_folder_path = dialog.getExistingDirectory(
            self.parent, 'Select Results Directory', default_path)

        if not output_folder_path == '':
            self.ui.lineedit_add_tests_output_folder_location.\
                setText(output_folder_path)

            self.output_folder_path     = output_folder_path

            # Save the selected folder as the default
            configs.write_to_default_config(
                key=SaveFileKeys.OUTPUT_FOLDER_PATH,
                value= self.output_folder_path)

        self.results_folder_toggle_changed()

    def open_output_directory(self):
        """Open the output directory using an explorer window"""
        # If the results folder checkbox is checked, open the result folder
        # If not, use the parent folder
        res_folder_en = self.ui.chkbox_add_tests_results_folder.checkState()
        if res_folder_en:
            parent_folder_path = self.ui.lineedit_add_tests_output_folder_location.text()
            results_folder = self.ui.cbx_add_tests_results_folder.currentText()
            folder_path = f'{parent_folder_path}/{results_folder}'
        else:
            folder_path = self.ui.lineedit_add_tests_output_folder_location.text()

        # Open the folder using explorer window
        if os.path.exists(folder_path):
            os.startfile(f'{folder_path}')

    def initialize_ui_states(self):
        self.item_selected = True
        # Initialize Test Type List
        self.intitialize_test_types_list()

        # Initialize Line Settings List
        self.initialize_ui_element_settings()
        self.item_selected = False
        
        # Run the routine to hide the usbpd ui elements
        self.usbpd_dev_toggle_changed()

        self.update_cbx_line_voltage_range()
        self.update_cbx_load_range()
        self.update_cbx_line_voltage_ramp()
        self.update_line_range_table()
        self.update_cbx_soaktime_settings()
        self.load_default_configs()



    def initialize_ui_element_settings(self):
        ui = self.ui

        # Set the resize mode of the tableviews
        ui.table_add_tests_line_range.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        ui.table_add_tests_line_ramp.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        ui.table_add_tests_load_range.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        ui.table_add_tests_source_caps.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        
        # Set the widths of the tableview columns 
        ui.table_add_tests_source_caps.setColumnWidth(0, 50)
        ui.table_add_tests_source_caps.setColumnWidth(1, 50)
        ui.table_add_tests_source_caps.setColumnWidth(3, 50)
        ui.table_add_tests_source_caps.setColumnWidth(4, 50)
        ui.table_add_tests_test_list.setColumnWidth(0,50)

        # Show the headers of the table widgets
        ui.table_add_tests_test_list.horizontalHeader().setVisible(True)
        ui.table_add_tests_source_caps.horizontalHeader().setVisible(True)
        ui.table_add_tests_line_range.horizontalHeader().setVisible(True)
        ui.table_add_tests_line_ramp.horizontalHeader().setVisible(True)
        ui.table_add_tests_load_range.horizontalHeader().setVisible(True)
        
        # Hide the lineedit_add_tests_line_range_voltage_2 (only for spacing)
        ui.lineedit_add_tests_line_range_voltage_2.setVisible(False)

        # Initialize USBPD checkbox as unchecked to hide USBPD options
        ui.chkbox_add_tests_usbpd_device.setChecked(False)

        # Initialize CVCC Multiple setpoints as false
        ui.chkbox_add_tests_cvcc_multi_setpoints.setChecked(False)

        # Initialize AC Source Coupling as AC
        # Start from true to ensure that the *.changed event will trigger
        ui.widget_toggle_add_tests_line_range_coupling.setChecked(True)
        ui.widget_toggle_add_tests_line_ramp_coupling.setChecked(True)
        ui.widget_toggle_add_tests_line_range_coupling.setChecked(False)
        ui.widget_toggle_add_tests_line_ramp_coupling.setChecked(False)

        # Hide the combo box for results folder
        ui.frame_add_tests_results_folder.setVisible(False)

        # Clear the test list display at startup
        ui.table_add_tests_test_list.setRowCount(0)
        self.item_selected = False

        # For setting size policies of hidden fields
        add_setretainsize_policy(ui.table_add_tests_source_caps)
        add_setretainsize_policy(ui.frame_add_tests_nominal_output_voltage)
        add_setretainsize_policy(ui.frame_add_tests_nominal_output_current)
        add_setretainsize_policy(ui.frame_add_tests_timing_params)
        add_setretainsize_policy(ui.frame_add_tests_eload_type)
        add_setretainsize_policy(ui.chkbox_add_tests_measure_scope_ripple)
        add_setretainsize_policy(ui.chkbox_add_tests_eload_measurement)
        add_setretainsize_policy(ui.chkbox_add_tests_proportional_current_request)
        add_setretainsize_policy(ui.btn_add_tests_option_1)
        add_setretainsize_policy(ui.btn_add_tests_option_2)
        add_setretainsize_policy(ui.lineedit_add_tests_line_range_voltage_2)
        add_setretainsize_policy(ui.frame_add_tests_line_range_coupling)
 
        # Initialize validator settings
        self.validator = QDoubleValidator(0, 16777215, 6)
        
        ui.lineedit_add_tests_line_range_voltage.setValidator(self.validator)
        ui.lineedit_add_tests_line_range_frequency.setValidator(self.validator)
        
        ui.lineedit_add_tests_load_range_percent.setValidator(self.validator)
        
        ui.lineedit_add_tests_testtime_param1.setValidator(self.validator)
        ui.lineedit_add_tests_testtime_param2.setValidator(self.validator)
        ui.lineedit_add_tests_testtime_param3.setValidator(self.validator)
        ui.lineedit_add_tests_testtime_param4.setValidator(self.validator)
        
        ui.lineedit_add_tests_nominal_output_voltage.setValidator(self.validator)
        ui.lineedit_add_tests_nominal_output_current.setValidator(self.validator)
        
        ui.lineedit_add_tests_cvcc_nom_voltage.setValidator(self.validator)
        ui.lineedit_add_tests_cvcc_max_current.setValidator(self.validator)
        ui.lineedit_add_tests_cvcc_min_current.setValidator(self.validator)
        ui.lineedit_add_tests_cvcc_step_size.setValidator(self.validator)
        
        ui.lineedit_add_tests_line_ramp_voltage.setValidator(self.validator)
        ui.lineedit_add_tests_line_ramp_slew_rate.setValidator(self.validator)
        ui.lineedit_add_tests_line_ramp_frequency.setValidator(self.validator)

        self.define_i2c_ui_elements()
    

    def define_i2c_ui_elements(self):
        ui = self.ui
        self.i2c_ui_lineedit_frames = [
            ui.frame_add_tests_i2c_param_1,
            ui.frame_add_tests_i2c_param_2,
            ui.frame_add_tests_i2c_param_3,
            ui.frame_add_tests_i2c_param_4,
            ui.frame_add_tests_i2c_param_5,
            ui.frame_add_tests_i2c_param_6,
            ui.frame_add_tests_i2c_param_7,
            ui.frame_add_tests_i2c_param_8,
            ui.frame_add_tests_i2c_param_9,
            ui.frame_add_tests_i2c_param_10,
        ]

        self.i2c_ui_lineedit_labels = [
            ui.label_add_tests_i2c_param_1,
            ui.label_add_tests_i2c_param_2,
            ui.label_add_tests_i2c_param_3,
            ui.label_add_tests_i2c_param_4,
            ui.label_add_tests_i2c_param_5,
            ui.label_add_tests_i2c_param_6,
            ui.label_add_tests_i2c_param_7,
            ui.label_add_tests_i2c_param_8,
            ui.label_add_tests_i2c_param_9,
            ui.label_add_tests_i2c_param_10,
        ]

        self.i2c_ui_lineedits = [
            ui.lineedit_add_tests_i2c_param_1,
            ui.lineedit_add_tests_i2c_param_2,
            ui.lineedit_add_tests_i2c_param_3,
            ui.lineedit_add_tests_i2c_param_4,
            ui.lineedit_add_tests_i2c_param_5,
            ui.lineedit_add_tests_i2c_param_6,
            ui.lineedit_add_tests_i2c_param_7,
            ui.lineedit_add_tests_i2c_param_8,
            ui.lineedit_add_tests_i2c_param_9,
            ui.lineedit_add_tests_i2c_param_10,
        ]
        
        self.i2c_ui_combo_boxes = [
            ui.cbx_add_tests_i2c_cbxparam_1,
            ui.cbx_add_tests_i2c_cbxparam_2,
            ui.cbx_add_tests_i2c_cbxparam_3,
            ui.cbx_add_tests_i2c_cbxparam_4,
        ]

        self.i2c_ui_cbx_frames = [
            ui.frame_add_tests_i2c_cbxparam_1,
            ui.frame_add_tests_i2c_cbxparam_2,
            ui.frame_add_tests_i2c_cbxparam_3,
            ui.frame_add_tests_i2c_cbxparam_4,
        ]
        
        self.i2c_ui_cbx_labels = [
            ui.label_add_tests_i2c_cbxparam_1,
            ui.label_add_tests_i2c_cbxparam_2,
            ui.label_add_tests_i2c_cbxparam_3,
            ui.label_add_tests_i2c_cbxparam_4,
        ]
        
        for frame in self.i2c_ui_lineedit_frames:
            add_setretainsize_policy(frame)
        
        # for label in self.i2c_ui_lineedit_labels:
        #     label.setSizePolicy(sp_horizontal_min_expanding)

        for frame in self.i2c_ui_cbx_frames:
            add_setretainsize_policy(frame)
            
        # for label in self.i2c_ui_cbx_labels:
        #     label.setSizePolicy(sp_horizontal_min_expanding)

        for line in self.i2c_ui_lineedits:
            line.setValidator(self.validator)

        self.ui.cbx_add_tests_i2c_cbxparam_4.currentIndexChanged.connect(self.update_i2c_ui_on_inno_family_change)

    def intitialize_test_types_list(self):
        """ Initialize the values of the combobox for test type selection
        """

        # Get the list of titles from the TestTypes list
        test_title_list = get_test_title_list()

        # Add all of the items of the list to the combobox entries
        self.ui.cbx_add_tests_testtype.addItems(test_title_list)

            
    def update_cbx_line_voltage_range(self):
        """ Initialize the contents of the line voltage range combo box
        and the line range table widget
        """
        # Get the names of the line ranges in the line settings object
        self.line_settings_names = \
            [x.name for x in self.line_settings.line_range_list]
        
        # Add that list of names to the combo box
        self.ui.cbx_add_tests_line_range_type.clear()
        self.ui.cbx_add_tests_line_range_type.addItems(self.line_settings_names)
        
    def update_cbx_line_voltage_ramp(self):
        """ Initialize the contents of the line voltage range combo box
        and the line range table widget
        """
        # Get the names of the line ranges in the line settings object
        self.line_ramp_settings_names = \
            [x.name for x in self.line_ramp_settings.line_ramp_list]
        
        # Add that list of names to the combo box
        self.ui.cbx_add_tests_line_ramp_type.clear()
        self.ui.cbx_add_tests_line_ramp_type.addItems(self.line_ramp_settings_names)
    
    def update_cbx_load_range(self):
        
        """ Initialize the contents of the load range combo box
        and the load range table widget
        """
        # Get the names of the load ranges in the line settings object
        self.load_settings_names = \
            [x.name for x in self.load_settings.load_range_list]
        self.load_direction_names = ['Downward','Upward']
        self.load_settings_mode_names = ['CC','CR']
        
        
        # Add that list of names to the combo box

        self.ui.cbx_add_tests_load_range_direction.clear()
        self.ui.cbx_add_tests_load_range_eload_type.clear()
        
        self.ui.cbx_add_tests_load_range_direction.addItems(self.load_direction_names)
        self.ui.cbx_add_tests_load_range_eload_type.addItems(self.load_settings_mode_names)

        
        for load_setting_index, load_setting_name in enumerate(self.load_settings_names):
            current_name  = self.ui.cbx_add_tests_load_range_type.itemText(load_setting_index)
            if current_name == '':
                self.ui.cbx_add_tests_load_range_type.addItem(load_setting_name)
            else:
                self.ui.cbx_add_tests_load_range_type.setItemText(load_setting_index,load_setting_name)
        
        self.ui.cbx_add_tests_load_range_type.setMaxCount(len(self.load_settings_names))
        self.ui.cbx_add_tests_load_range_type.setMaxCount(2147483647)
            
    
    def update_cbx_soaktime_settings(self):
        """ Initialize the contents of the soaktime settings combo box
        and the soaktime table widget
        """
        # Get the names of the line ranges in the line settings object
        self.soaktime_settings_names = \
            [x.name for x in self.soaktime_settings.soaktime_list]
        
        # Add that list of names to the combo box
        self.ui.cbx_add_tests_timing_params.clear()
        self.ui.cbx_add_tests_timing_params.addItems(self.soaktime_settings_names)

        
    def update_line_range_table(self):
        """Update the line range UI when the combo box value changes."""
        # Get index of selected line voltage range
        line_range_index = \
            self.ui.cbx_add_tests_line_range_type.currentIndex()
        
        # Get the contents of the selected line setting
        self.selected_line_range:LineRange = \
            self.line_settings.line_range_list[line_range_index]
        
        # Get the number of elements
        line_range_num_elements = len(self.selected_line_range.vin_freq)

        # Clear the contents of the table
        self.ui.table_add_tests_line_range.clearContents()

        # Set the number of rows equal to the number of vin and freq
        self.ui.table_add_tests_line_range.\
            setRowCount(line_range_num_elements)

        # Go through the line range and set the values of the table
        for i, item in enumerate(self.selected_line_range.vin_freq):
            self.ui.table_add_tests_line_range.setItem(
                i, 0, QtWidgets.QTableWidgetItem(f'{round(item[0],3):g}'))
            if not self.ui.widget_toggle_add_tests_line_range_coupling.isChecked():
                self.ui.table_add_tests_line_range.setItem(
                    i, 1, QtWidgets.QTableWidgetItem(f'{round(item[1],3):g}'))
    
        # Only enable the add/remove entry function if 
        # the line range is CUSTOM
        if self.selected_line_range.custom == True & (not self.selected_line_range.name == 'Custom'):
            self.ui.frame_add_tests_line_range_buttons.setEnabled(True)
            self.ui.lineedit_add_tests_line_range_voltage.setEnabled(True)
            self.ui.lineedit_add_tests_line_range_frequency.setEnabled(True)
            self.ui.btn_add_tests_line_range_remove_setting.setEnabled(True)
        elif self.selected_line_range.name == 'Custom':
            self.ui.frame_add_tests_line_range_buttons.setEnabled(True) 
            self.ui.lineedit_add_tests_line_range_voltage.setEnabled(True)
            self.ui.lineedit_add_tests_line_range_frequency.setEnabled(True)
            self.ui.btn_add_tests_line_range_remove_setting.setEnabled(False)   
        else:
            self.ui.frame_add_tests_line_range_buttons.setEnabled(False) 
            self.ui.lineedit_add_tests_line_range_voltage.setEnabled(False)
            self.ui.lineedit_add_tests_line_range_frequency.setEnabled(False)
            self.ui.btn_add_tests_line_range_remove_setting.setEnabled(False)   
            
    
    def update_line_ramp_table(self):
        """Update the line range UI when the combo box value changes."""
        # Get index of selected line voltage range
        line_ramp_index = \
            self.ui.cbx_add_tests_line_ramp_type.currentIndex()
        
        # Get the contents of the selected line setting
        self.selected_line_ramp:LineRamp = \
            self.line_ramp_settings.line_ramp_list[line_ramp_index]
        
        # Get the number of elements
        line_ramp_num_elements = len(self.selected_line_ramp.vin_slew)

        # Clear the contents of the table
        self.ui.table_add_tests_line_ramp.clearContents()

        # Set the number of rows equal to the number of vin and freq
        self.ui.table_add_tests_line_ramp.\
            setRowCount(line_ramp_num_elements)

        # Go through the line range and set the values of the table
        for i, item in enumerate(self.selected_line_ramp.vin_slew):
            self.ui.table_add_tests_line_ramp.setItem(
                i, 0, QtWidgets.QTableWidgetItem(f'{round(item[0],3):g}'))
            self.ui.table_add_tests_line_ramp.setItem(
                i, 1, QtWidgets.QTableWidgetItem(f'{round(item[1],3):g}'))
    
        # Only enable the add/remove entry function if 
        # the line range is CUSTOM
        if self.selected_line_ramp.custom == True & (not self.selected_line_ramp.name == 'Custom'):
            self.ui.frame_add_tests_line_ramp_buttons.setEnabled(True)
            self.ui.lineedit_add_tests_line_ramp_voltage.setEnabled(True)
            self.ui.lineedit_add_tests_line_ramp_slew_rate.setEnabled(True)
            self.ui.btn_add_tests_line_ramp_remove_setting.setEnabled(True)
        elif self.selected_line_ramp.name == 'Custom':
            self.ui.frame_add_tests_line_ramp_buttons.setEnabled(True)
            self.ui.lineedit_add_tests_line_ramp_voltage.setEnabled(True)
            self.ui.lineedit_add_tests_line_ramp_slew_rate.setEnabled(True) 
            self.ui.btn_add_tests_line_ramp_remove_setting.setEnabled(False)   
        else:
            self.ui.lineedit_add_tests_line_ramp_voltage.setEnabled(False)
            self.ui.lineedit_add_tests_line_ramp_slew_rate.setEnabled(False)
            self.ui.frame_add_tests_line_ramp_buttons.setEnabled(False) 
            self.ui.btn_add_tests_line_ramp_remove_setting.setEnabled(False)   

    def update_load_range_table(self):
        if self.ongoing_load_range_update:
            return
        # Get index of selected load voltage range
        load_range_index = \
            self.ui.cbx_add_tests_load_range_type.currentIndex()

        # Get the contents of the selected load setting
        self.selected_load_range:LoadRange = \
            self.load_settings.load_range_list[load_range_index]
            
        # Clear the contents of the table
        self.ui.table_add_tests_load_range.clearContents()   
        
        # Change column header depending on test type
        if TestTypes[self.test_type_index] in [LightLoad]:
            self.ui.table_add_tests_load_range.setHorizontalHeaderLabels(['Output Power (W)', 'Load Current (A)'])
            self.ui.label_add_tests_soak_per_load_4.setText('Output Power (W)')
        else:
            self.ui.table_add_tests_load_range.setHorizontalHeaderLabels(['Load Percentage', 'Load Current (A)'])
            self.ui.label_add_tests_soak_per_load_4.setText('Load Percentage')

        # Get load current and check whether usb pd is enabled
        usbpd_check_state = self.ui.chkbox_add_tests_usbpd_device.checkState()
        
        if is_numeric(self.ui.lineedit_add_tests_nominal_output_voltage.text()) and (not usbpd_check_state):
            nominal_output_voltage_V = rounded_float(self.ui.lineedit_add_tests_nominal_output_voltage.text())
            output_voltage_available = True
        elif usbpd_check_state:
            if not hasattr(self, 'usbpd_source_caps'):
                output_voltage_available = False
            else:
                selection_index = self.ui.table_add_tests_source_caps.currentRow()
                if (not selection_index == -1) and (selection_index < len(self.usbpd_source_caps)):
                    source_cap = self.usbpd_source_caps[selection_index]
                    if source_cap.supply_type == SUPPLY_TYPE.AUGMENTED:
                        if is_numeric(self.ui.lineedit_add_tests_nominal_output_voltage.text()):
                            nominal_output_voltage_V = rounded_float(self.ui.lineedit_add_tests_nominal_output_voltage.text())
                            output_voltage_available = True
                        else:
                            output_voltage_available = False
                    else:
                        nominal_output_voltage_V = source_cap.voltage_mV/1000 
                        output_voltage_available = True              
                else:
                    output_voltage_available = False
        else:
            output_voltage_available = False
        
        if is_numeric(self.ui.lineedit_add_tests_nominal_output_current.text()):
            nominal_load_current_A = rounded_float(self.ui.lineedit_add_tests_nominal_output_current.text())
            load_current_available = True
        elif usbpd_check_state:
            if not hasattr(self, 'usbpd_source_caps'):
                load_current_available = False
            else:
                selection_index = self.ui.table_add_tests_source_caps.currentRow()
                if (not selection_index == -1) and (selection_index < len(self.usbpd_source_caps)):
                    load_current_available = True
                    source_cap = self.usbpd_source_caps[selection_index]
                    nominal_load_current_A = source_cap.max_current_mA/1000
                else:
                    load_current_available = False
        else:
            load_current_available = False
               
        # If test type is input harmonics test and the load range has more than one item
        if (TestTypes[self.test_type_index] in [InputHarmonicsTest]) & (len(self.selected_load_range.load_range_pct) > 1) & (not(self.item_selected)):
            self.parent.msg_box_info(
                            title="Load Range Info",
                            message=f"For {TestTypes[self.test_type_index].title} Test, only 1 load setting can be set",
                            message_type = MessageType.INFO
                        )
            if self.selected_load_range.name == 'Custom':
                while len(self.selected_load_range.load_range_pct) > 1:
                    self.selected_load_range.load_range_pct.pop()
            else:
                load_range_index_default = self.load_settings.load_range_list.index(
                    (self.test_condition_settings.test_condition_list[self.test_type_index]).load_range)
                self.ongoing_load_range_update = True
                self.ui.cbx_add_tests_load_range_type.setCurrentIndex(load_range_index_default)
                self.ongoing_load_range_update = False
                
                # Update the selected load setting
                self.selected_load_range = \
                    self.load_settings.load_range_list[load_range_index_default]
            

            
        # If test type is efficiency test and the load range is not for the efficiency test   
        if (TestTypes[self.test_type_index] == EfficiencyTest) & (not self.selected_load_range.name == 'Efficiency Test' ) & (not(self.item_selected)):
            self.parent.msg_box_info(
                            title="Load Range Info",
                            message=f"For {TestTypes[self.test_type_index].title} Test, only the expected load percentages can be selected (100%, 75%, 50%, 25%, 10%)",
                            message_type = MessageType.INFO
                        )
            load_range_index_default = self.load_settings.load_range_list.index(
                (self.test_condition_settings.test_condition_list[self.test_type_index]).load_range)
            self.ongoing_load_range_update = True
            self.ui.cbx_add_tests_load_range_type.setCurrentIndex(load_range_index_default)
            self.ongoing_load_range_update = False
            
            # Update the selected load setting
            self.selected_load_range = \
                self.load_settings.load_range_list[load_range_index_default]
            
        # Get the number of elements
        load_range_num_elements = \
            len(self.selected_load_range.load_range_pct)

        # Set the number of rows equal to the number of load steps
        self.ui.table_add_tests_load_range\
            .setRowCount(load_range_num_elements)
        
        # Go through the load range and set the values of the table
        for i, item in enumerate(self.selected_load_range.load_range_pct):
            
            self.ui.table_add_tests_load_range.setItem(
                i, 0, QtWidgets.QTableWidgetItem(f'{round(item,6):g}'))
            
            if TestTypes[self.test_type_index] in [LightLoad]:
                if output_voltage_available:
                    self.ui.table_add_tests_load_range.setItem(
                        i, 1, QtWidgets.QTableWidgetItem(f'{round(item/nominal_output_voltage_V,6):g}'))
            else:
                 if load_current_available:   
                    self.ui.table_add_tests_load_range.setItem(
                        i, 1, QtWidgets.QTableWidgetItem(f'{round(nominal_load_current_A*item/100,6):g}'))
            
        self.ui.frame_add_tests_load_range_params_options.setEnabled(True)
        # Only enable the add/remove entry function if 
        # the line range is CUSTOM
        if self.selected_load_range.custom == True & (not self.selected_load_range.name == 'Custom'):
            self.ui.lineedit_add_tests_load_range_percent.setEnabled(True)
            self.ui.frame_add_tests_load_range_buttons.setEnabled(True)
            self.ui.btn_add_tests_load_range_remove_setting.setEnabled(True)
        elif self.selected_load_range.name == 'Custom':
            self.ui.lineedit_add_tests_load_range_percent.setEnabled(True)
            self.ui.frame_add_tests_load_range_buttons.setEnabled(True)   
            self.ui.btn_add_tests_load_range_remove_setting.setEnabled(False)
        else:
            self.ui.lineedit_add_tests_load_range_percent.setEnabled(False)
            self.ui.frame_add_tests_load_range_buttons.setEnabled(False)   
            self.ui.btn_add_tests_load_range_remove_setting.setEnabled(False)
            
    def update_soaktime_list(self):
        self.soak_time_selection_changed = True
        # Get index of selected soaktime setting
        soak_time_index = \
            self.ui.cbx_add_tests_timing_params.currentIndex()
        
        # Get the contents of the selected soaktime setting
        self.selected_soaktime:SoakTime = \
            self.soaktime_settings.soaktime_list[soak_time_index]
        
        # Clear the contents of the table
        self.ui.lineedit_add_tests_testtime_param1.setText(
            f"{self.selected_soaktime.initial_soak:g}")
        self.ui.lineedit_add_tests_testtime_param2.setText(
            f"{self.selected_soaktime.soak_per_line:g}")
        self.ui.lineedit_add_tests_testtime_param3.setText(
            f"{self.selected_soaktime.soak_per_load:g}")
        self.ui.lineedit_add_tests_testtime_param4.setText(
            f"{self.selected_soaktime.integration_time:g}")
        
        if self.selected_soaktime.custom == True & (not self.selected_soaktime.name == 'Custom'):
            self.ui.lineedit_add_tests_testtime_param1.setEnabled(True)
            self.ui.lineedit_add_tests_testtime_param2.setEnabled(True)
            self.ui.lineedit_add_tests_testtime_param3.setEnabled(True)
            self.ui.lineedit_add_tests_testtime_param4.setEnabled(True)
            self.ui.btn_add_tests_timing_params_remove_setting.setEnabled(True)
        elif self.selected_soaktime.name == 'Custom':
            self.ui.lineedit_add_tests_testtime_param1.setEnabled(True)
            self.ui.lineedit_add_tests_testtime_param2.setEnabled(True)
            self.ui.lineedit_add_tests_testtime_param3.setEnabled(True)
            self.ui.lineedit_add_tests_testtime_param4.setEnabled(True)  
            self.ui.btn_add_tests_timing_params_remove_setting.setEnabled(False)
        else:
            self.ui.lineedit_add_tests_testtime_param1.setEnabled(False)
            self.ui.lineedit_add_tests_testtime_param2.setEnabled(False)
            self.ui.lineedit_add_tests_testtime_param3.setEnabled(False)
            self.ui.lineedit_add_tests_testtime_param4.setEnabled(False)  
            self.ui.btn_add_tests_timing_params_remove_setting.setEnabled(False)
            
        self.soak_time_selection_changed = False
    
    ###########################################################################
    #               CUSTOM SETTING MODIFICATION FUNCTIONS
    ###########################################################################
    # LINE SETTINGS
    def custom_line_setting_add_entry(self)->None:
        """Add a custom line setting and store it to the user file."""
        name = self.parent.msg_box_input(
            title="Add Line Range",
            message="Name for new line range")
        
        # Ignore if blank
        if name == '' or name==None:
            return
        # Loop through the current settings names
        # Check if it has a match and return early if it does
        for line_range in self.line_settings.line_range_list:
            if line_range.name == name:
                self.parent.msg_box_info(
                    title="Add Line Range Error",
                    message=f"Line range with the name [{name}] already exists",
                    message_type = MessageType.INFO
                    )
                return
        
        # Create a new linerange object and store it in the file
        new_line_range = LineRange(name, [], custom=True)
        self.line_settings.add_line_range(new_line_range)
        self.line_settings.write_user_settings()
        # Update the combo box
        self.update_cbx_line_voltage_range()

        # Select the last item which is the newly created line range
        lr_count = len(self.line_settings.line_range_list)
        self.ui.cbx_add_tests_line_range_type.setCurrentIndex(lr_count-1)


    def custom_line_setting_duplicate_entry(self)->None:
        """Add a custom line setting from the currently selected
        line setting and store it to the user file."""
        # Get a text input for the name
        name = self.parent.msg_box_input(
            title="Duplicate Line Range",
            message="Name for new line range")
        # Ignore if blank
        if name == '' or name==None:
            return
        # Loop through the current settings names
        # Check if it has a match and return early if it does
        for line_range in self.line_settings.line_range_list:
            if line_range.name == name:
                self.parent.msg_box_info(
                    title="Add Line Range Error",
                    message=f"Line range with the name [{name}] already exists",
                    message_type = MessageType.INFO
                    )
                return
        # Get the index of the currently selected line setting
        selected_index = self.ui.cbx_add_tests_line_range_type.currentIndex()
        selected_line_range = self.line_settings.line_range_list[selected_index]
        # Create a new object from the selected linerange 
        # but with different name
        new_line_range = LineRange(
            name = name, 
            vin_freq=copy(selected_line_range.vin_freq),
            custom=True)
        # Store the created linerange to the file
        self.line_settings.add_line_range(new_line_range)
        self.line_settings.write_user_settings()
        # Update the combo box
        self.update_cbx_line_voltage_range()

        # Select the last item which is the newly created line range
        lr_count = len(self.line_settings.line_range_list)
        self.ui.cbx_add_tests_line_range_type.setCurrentIndex(lr_count-1)

    def custom_line_setting_remove_entry(self)->None:
        """Remove selected custom line setting and remove it from the user file."""
        # Get the index of the currently selected line setting
        selected_index = self.ui.cbx_add_tests_line_range_type.currentIndex()
        # Check if selected setting is custom before removing
        if self.line_settings.line_range_list[selected_index].custom == True:
            # Remove that entry from the list
            self.line_settings.line_range_list.pop(selected_index)
        # Write the contents of the line settings to the file
        self.line_settings.write_user_settings()
        # Update the combo box
        self.update_cbx_line_voltage_range()
        
    ###########################################################################    
    # LINE RAMP SETTINGS
    def custom_line_ramp_setting_add_entry(self)->None:
        """Add a custom line ramp setting and store it to the user file."""
        name = self.parent.msg_box_input(
            title="Add Line Ramp Setting",
            message="Name for new line ramp setting")
        
        # Ignore if blank
        if name == '' or name==None:
            return
        # Loop through the current settings names
        # Check if it has a match and return early if it does
        for line_ramp in self.line_ramp_settings.line_ramp_list:
            if line_ramp.name == name:
                self.parent.msg_box_info(
                    title="Add Line Ramp Setting Error",
                    message=f"Line ramp setting with the name [{name}] already exists",
                    message_type = MessageType.INFO
                    )
                return
        
        # Create a new linerange object and store it in the file
        new_line_ramp = LineRamp(name, custom=True)
        self.line_ramp_settings.add_line_ramp_setting(new_line_ramp)
        self.line_ramp_settings.write_user_settings()
        # Update the combo box
        self.update_cbx_line_voltage_ramp()

        # Select the last item which is the newly created line range
        lr_count = len(self.line_ramp_settings.line_ramp_list)
        self.ui.cbx_add_tests_line_ramp_type.setCurrentIndex(lr_count-1)


    def custom_line_ramp_setting_duplicate_entry(self)->None:
        """Add a custom line setting from the currently selected
        line setting and store it to the user file."""
        # Get a text input for the name
        name = self.parent.msg_box_input(
            title="Duplicate Line Ramp Setting",
            message="Name for new line ramp setting")
        # Ignore if blank
        if name == '' or name==None:
            return
        # Loop through the current settings names
        # Check if it has a match and return early if it does
        for line_ramp in self.line_ramp_settings.line_ramp_list:
            if line_ramp.name == name:
                self.parent.msg_box_info(
                    title="Add Line Ramp Setting Error",
                    message=f"Line ramp setting with the name [{name}] already exists",
                    message_type = MessageType.INFO
                    )
                return
        # Get the index of the currently selected line ramp setting
        selected_index = self.ui.cbx_add_tests_line_ramp_type.currentIndex()
        selected_line_ramp = self.line_ramp_settings.line_ramp_list[selected_index]
        
        # Create a new object from the selected lineramp 
        # but with different name
        new_line_ramp = LineRamp(
            name = name, 
            vin_slew = copy(selected_line_ramp.vin_slew),
            freq = copy(selected_line_ramp.freq),
            coupling = copy(selected_line_ramp.coupling),
            custom=True)
        
        # Store the created lineramp to the file
        self.line_ramp_settings.add_line_ramp_setting(new_line_ramp)
        self.line_ramp_settings.write_user_settings()
        # Update the combo box
        self.update_cbx_line_voltage_ramp()

        # Select the last item which is the newly created line range
        lr_count = len(self.line_ramp_settings.line_ramp_list)
        self.ui.cbx_add_tests_line_ramp_type.setCurrentIndex(lr_count-1)

    def custom_line_ramp_setting_remove_entry(self)->None:
        """Remove selected custom line setting and remove it from the user file."""
        # Get the index of the currently selected line ramp setting
        selected_index = self.ui.cbx_add_tests_line_ramp_type.currentIndex()
        # Check if selected setting is custom before removing
        if self.line_ramp_settings.line_ramp_list[selected_index].custom == True:
            # Remove that entry from the list
            self.line_ramp_settings.line_ramp_list.pop(selected_index)
        # Write the contents of the line settings to the file
        self.line_ramp_settings.write_user_settings()
        # Update the combo box
        self.update_cbx_line_voltage_ramp()

    ###########################################################################
    # LOAD SETTINGS
    def custom_load_setting_add_entry(self)->None:
        """Add a custom load setting and store it to the user file."""
        name = self.parent.msg_box_input(
            title="Add Load Range",
            message="Name for new load range")
        
        # Ignore if blank
        if name == '' or name==None:
            return
        # Loop through the current settings names
        # Check if it has a match and return early if it does
        for load_range in self.load_settings.load_range_list:
            if load_range.name == name:
                self.parent.msg_box_info(
                    title="Add Load Range Error",
                    message=f"Load range with the name [{name}] already exists",
                    message_type = MessageType.INFO
                    )
                return
        
        # Create a new LoadRange object and store it in the file
        new_load_range = LoadRange(name, [], custom=True)
        self.load_settings.add_load_range(new_load_range)
        self.load_settings.write_user_settings()
        # Update the combo box
        self.update_cbx_load_range()

        # Select the last item which is the newly created line range
        lr_count = len(self.load_settings.load_range_list)
        self.ui.cbx_add_tests_load_range_type.setCurrentIndex(lr_count-1)

    def custom_load_setting_duplicate_entry(self)->None:
        """Add a custom load setting from the currently selected
        load setting and store it to the user file."""
        # Get a text input for the name
        name = self.parent.msg_box_input(
            title="Duplicate Load Range",
            message="Name for new load range")
        # Ignore if blank
        if name == '' or name==None:
            return
        # Loop through the current settings names
        # Check if it has a match and return early if it does
        for load_range in self.load_settings.load_range_list:
            if load_range.name == name:
                self.parent.msg_box_info(
                    title="Add Load Range Error",
                    message=f"Load range with the name [{name}] already exists",
                    message_type = MessageType.INFO
                    )
                return
        # Create a new object from the selected LoadRange 
        # but with different name
        new_load_range = LoadRange(
            name = name, 
            load_range_pct=copy(self.selected_load_range.load_range_pct),
            custom=True)
        # Store the created LoadRange to the file
        self.load_settings.add_load_range(new_load_range)
        self.load_settings.write_user_settings()
        # Update the combo box
        self.update_cbx_load_range()

        # Select the last item which is the newly created load range
        lr_count = len(self.load_settings.load_range_list)
        self.ui.cbx_add_tests_load_range_type.setCurrentIndex(lr_count-1)

    def custom_load_setting_remove_entry(self)->None:
        """Remove selected custom load setting and remove it from the user file."""
        # Get the index of the currently selected load setting
        selected_index = self.ui.cbx_add_tests_load_range_type.currentIndex()
        # Check if selected setting is custom before removing
        if self.load_settings.load_range_list[selected_index].custom == True:
            # Remove that entry from the list
            self.load_settings.load_range_list.pop(selected_index)
        # Write the contents of the load settings to the file
        self.load_settings.write_user_settings()
        # Update the combo box
        self.update_cbx_load_range()

    ###########################################################################
    # TIMING PARAMETERS
    def custom_timing_params_add_entry(self)->None:
        """Add a custom soaktime setting and store it to the user file."""
        name = self.parent.msg_box_input(
            title="Add Soak Time Setting",
            message="Name for new soak time setting")
        # Ignore if blank
        if name == '' or name==None:
            return
        # Loop through the current settings names
        # Check if it has a match and return early if it does
        for soaktime_setting in self.soaktime_settings.soaktime_list:
            if soaktime_setting.name == name:
                self.parent.msg_box_info(
                    title="Add Line Range Error",
                    message=f"Soak time setting with the name [{name}] already exists",
                    message_type = MessageType.INFO
                    )
                return
        # Create a new linerange object and store it in the file
        new_soaktime_setting = SoakTime(name=name,initial=0,line=0,load=0,integration=0,custom=True)
        self.soaktime_settings.add_soaktime(new_soaktime_setting)
        self.soaktime_settings.write_user_settings()
        # Update the combo box
        self.update_cbx_soaktime_settings()

        # Select the last item which is the newly created line range
        st_count = len(self.soaktime_settings.soaktime_list)
        self.ui.cbx_add_tests_timing_params.setCurrentIndex(st_count-1)

    def custom_timing_params_duplicate_entry(self)->None:
        """Add a custom soaktime setting from the currently selected
        soaktime setting and store it to the user file."""
        name = self.parent.msg_box_input(
            title="Add Soak Time Setting",
            message="Name for new soak time setting")
        # Ignore if blank
        if name == '' or name==None:
            return
        # Loop through the current settings names
        # Check if it has a match and return early if it does
        for soaktime_setting in self.soaktime_settings.soaktime_list:
            if soaktime_setting.name == name:
                self.parent.msg_box_info(
                    title="Add Line Range Error",
                    message=f"Soak time setting with the name [{name}] already exists",
                    message_type = MessageType.INFO
                    )
                return
        # Create a new object from the selected LoadRange 
        # but with different name
        new_soaktime_setting = SoakTime(
            name = name, 
            initial=copy(self.selected_soaktime.initial_soak),
            line=copy(self.selected_soaktime.soak_per_line),
            load=copy(self.selected_soaktime.soak_per_load),
            integration=copy(self.selected_soaktime.integration_time),
            custom=True)
        # Store the created LoadRange to the file
        self.soaktime_settings.add_soaktime(new_soaktime_setting)
        self.soaktime_settings.write_user_settings()
        # Update the combo box
        self.update_cbx_soaktime_settings()

        # Select the last item which is the newly created load range
        lr_count = len(self.soaktime_settings.soaktime_list)
        self.ui.cbx_add_tests_timing_params.setCurrentIndex(lr_count-1)

    def custom_timing_params_remove_entry(self)->None:
        """Remove selected custom soaktime setting and remove it from the user file."""
        # Get the index of the currently selected load setting
        selected_index = self.ui.cbx_add_tests_timing_params.currentIndex()
        # Check if selected setting is custom before removing
        if self.soaktime_settings.soaktime_list[selected_index].custom == True:
            # Remove that entry from the list
            self.soaktime_settings.soaktime_list.pop(selected_index)
        # Write the contents of the load settings to the file
        self.soaktime_settings.write_user_settings()
        # Update the combo box
        self.update_cbx_soaktime_settings()

    ###########################################################################
    #               CUSTOM SETTING ENTRIES MODIFICATION FUNCTIONS
    ###########################################################################

    def custom_line_range_add_entry(self)->None:
        """Add an entry for the custom line range"""
        # Get the current selected Line Range

        # Get the text from the lineedits
        vin_txt = self.ui.lineedit_add_tests_line_range_voltage.text()
        freq_txt = self.ui.lineedit_add_tests_line_range_frequency.text()

        # If no inputs, ignore
        if vin_txt == '' and freq_txt == '':
            return
        
        # If only freq has input, exit        
        if vin_txt == '' and  is_numeric(freq_txt):
            self.parent.msg_box_info(
                title = "Input Error!",
                message = "Please enter the input voltage",
                message_type = MessageType.INFO
            )
            return
        # If only vin has input, auto select recommended frequency     
        if is_numeric(vin_txt) and  freq_txt == '':
            vin = round(float(vin_txt),2)
            if vin >= 180:
                freq = 50
            else:
                freq = 60
            self.ui.lineedit_add_tests_line_range_frequency.setText(f'{freq}')
            freq_txt = self.ui.lineedit_add_tests_line_range_frequency.text()
        
        # If the inputs are not valid, exit
        if (not is_numeric(vin_txt)) or (not is_numeric(freq_txt)):  
            self.parent.msg_box_info(
                title = "Input Error!",
                message = "Please enter numeric inputs.",
                message_type = MessageType.INFO
            )
            return
            
        else:
            vin = round(float(vin_txt),2)
            freq = round(float(freq_txt),2)
            if self.selected_line_range.custom:
                # Add the value pair to the selected range
                self.selected_line_range.add_vin_freq(vin, freq)
                
                # Update the list
                self.update_line_range_table()

            self.line_settings.write_user_settings()
            
            self.ui.lineedit_add_tests_line_range_voltage.clear()
            self.ui.lineedit_add_tests_line_range_frequency.clear()
    
    def custom_line_ramp_add_entry(self)->None:
        """Add an entry for the custom line ramp setting"""
        # Get the current selected Line Range

        # Get the text from the lineedits
        vin_txt = self.ui.lineedit_add_tests_line_ramp_voltage.text()
        slew_rate_txt = self.ui.lineedit_add_tests_line_ramp_slew_rate.text()

        # If no inputs, ignore
        if vin_txt == '' and slew_rate_txt == '':
            return
        
        # If only freq has input, exit        
        if vin_txt == '' and  is_numeric(slew_rate_txt):
            self.parent.msg_box_info(
                title = "Input Error!",
                message = "Please enter the input voltage",
                message_type = MessageType.INFO
            )
            return
        # If only vin has input, auto select recommended frequency     
        if is_numeric(vin_txt) and  slew_rate_txt == '':
            vin = round(float(vin_txt),2)
            slew_rate = 1e30
            self.ui.lineedit_add_tests_line_ramp_slew_rate.setText(f'{slew_rate}')
            slew_rate_txt = self.ui.lineedit_add_tests_line_ramp_slew_rate.text()
        
        # If the inputs are not valid, exit
        if (not is_numeric(vin_txt)) or (not is_numeric(slew_rate_txt)):  
            self.parent.msg_box_info(
                title = "Input Error!",
                message = "Please enter numeric inputs.",
                message_type = MessageType.INFO
            )
            return
            
        else:
            vin = round(float(vin_txt),2)
            slew_rate = round(float(slew_rate_txt),2)
            # Add the value pair to the selected range
            if self.selected_line_ramp.custom:
                self.selected_line_ramp.add_vin_slew(vin, slew_rate)
                
                # Update the list
                self.update_line_ramp_table()

            self.line_ramp_settings.write_user_settings()
            
            self.ui.lineedit_add_tests_line_ramp_voltage.clear()
            self.ui.lineedit_add_tests_line_ramp_slew_rate.clear()
            

    def custom_load_range_add_entry(self)->None:
        """Add an entry for the custom line range"""
        load_pct_txt = self.ui.lineedit_add_tests_load_range_percent.text()

        # If the inputs are valid, process the inputs
        if is_numeric(load_pct_txt):
            load_pct = round(float(load_pct_txt),4)
            
            if self.selected_load_range.custom: 
                # Add the value pair to the range
                self.selected_load_range.add_load_pct(load_pct)
                # Update the list
                self.update_load_range_table()

            self.load_settings.write_user_settings()
            
            self.ui.lineedit_add_tests_load_range_percent.clear()
            self.ui.lineedit_add_tests_load_range_percent.setFocus()
            
        # If the inputs are not valid, show a message
        else:
            self.parent.msg_box_info(
                title = "Input Error!",
                message = "Please enter numeric inputs.",
                message_type = MessageType.INFO
            )
    
    def custom_line_range_remove_entry(self)->None:
        """Remove the selected item from the custom line range."""
        selection_index = self.ui.table_add_tests_line_range.currentRow()
        
        # If there is a selection, 
        if not selection_index == -1:
            # remove that selection from the list
            if self.selected_line_range.custom:
                self.selected_line_range.delete_vin_freq(selection_index)
                self.update_line_range_table()
            # and update the saved config
            self.line_settings.write_user_settings()
    
    def custom_line_ramp_remove_entry(self)->None:
        """Remove the selected item from the custom line ramp setting."""
        selection_index = self.ui.table_add_tests_line_ramp.currentRow()
        
        # If there is a selection, 
        if not selection_index == -1:
            # remove that selection from the list
            if self.selected_line_ramp.custom:
                self.selected_line_ramp.delete_vin_slew(selection_index)
                self.update_line_ramp_table()
            # and update the saved config
            self.line_ramp_settings.write_user_settings()

    def custom_load_range_remove_entry(self)->None:
        """Remove the selected item from the custom load range."""
        selection_index = self.ui.table_add_tests_load_range.currentRow()
        
        # If there is a selection, 
        if not selection_index == -1:
            # remove that selection from the list
            if self.selected_load_range.custom:
                self.selected_load_range.delete_load_pct(selection_index)
                self.update_load_range_table()
            # and update the saved config
            self.line_settings.write_user_settings()

    def custom_line_range_clear_entry(self)->None:
        """Remove the all items from the custom line range."""
        # Clear the object's contents
        if self.selected_line_range.custom:
            self.selected_line_range.vin_freq.clear()
        # Update the display
        self.update_line_range_table()
        # and store the new value
        self.line_settings.write_user_settings()
        
    def custom_line_ramp_clear_entry(self)->None:
        """Remove the all items from the custom line ramp setting."""
        # Clear the object's contents
        if self.selected_line_ramp.custom:
            self.selected_line_ramp.vin_slew.clear()
        # Update the display
        self.update_line_ramp_table()
        # and store the new value
        self.line_ramp_settings.write_user_settings()

    def custom_load_range_clear_entry(self)->None:
        """Remove the all items from the custom line range."""
        # Clear the object's contents
        if self.selected_load_range.custom:
            self.selected_load_range.load_range_pct.clear()
        # Update the display
        self.update_load_range_table()
        # and store the new value
        self.load_settings.write_user_settings()
        
    def update_initial_soak_setting(self):
        if self.soak_time_selection_changed:
            return
        self.selected_soaktime.initial_soak = rounded_float(
            self.ui.lineedit_add_tests_testtime_param1.text())
        self.soaktime_settings.write_user_settings()
        
    def update_soak_per_line_setting(self):
        if self.soak_time_selection_changed:
            return
        self.selected_soaktime.soak_per_line = rounded_float(
            self.ui.lineedit_add_tests_testtime_param2.text())
        self.soaktime_settings.write_user_settings()
        
    def update_soak_per_load_setting(self):
        if self.soak_time_selection_changed:
            return
        self.selected_soaktime.soak_per_load= rounded_float(
            self.ui.lineedit_add_tests_testtime_param3.text())
        self.soaktime_settings.write_user_settings()
        
    def update_integration_time_setting(self):
        if self.soak_time_selection_changed:
            return
        self.selected_soaktime.integration_time = rounded_float(
            self.ui.lineedit_add_tests_testtime_param4.text())
        self.soaktime_settings.write_user_settings()

    # Default configs processing
    def load_default_configs(self):
        """Load default configs of the page from the default config file."""
    
        def load_default_output_folder():
            """Load the output folder location and update the UI"""
            self.parent_folder_path = configs.read_from_default_config(
                key=SaveFileKeys.OUTPUT_FOLDER_PATH, default_value='')
            self.ui.lineedit_add_tests_output_folder_location.setText(
                self.parent_folder_path)
        
        def load_result_folder_toggle():
            toggle_checked = configs.read_from_default_config(
                key=SaveFileKeys.RESULT_FOLDER_TOGGLE, default_value=False)
            # toggle_checked = False
            self.ui.chkbox_add_tests_results_folder.setChecked(toggle_checked)
            return toggle_checked
        
        def load_result_folder():
            """Load the results folder value into the UI."""
            result_folder = configs.read_from_default_config(
                key=SaveFileKeys.RESULT_FOLDER, default_value='')
            result_folder_path = f'{self.parent_folder_path}/{result_folder}'
            if os.path.exists(result_folder_path):
                self.folder_name = result_folder
            self.select_current_run_results_folder()

        # OUTPUT FOLDER RELATED CONFIGS
        # Load the output folder value first 
        load_default_output_folder()
        # Load the result folder toggle value
        results_folder_toggle = load_result_folder_toggle()
        # If result folder toggle is checked,
        # load the result folder to the combo box
        if results_folder_toggle:
            load_result_folder()   

        # Read from the user settings
        self.line_settings.read_user_settings()
        self.update_cbx_line_voltage_range()

        self.load_settings.read_user_settings()
        self.update_cbx_load_range()
        
        self.soaktime_settings.read_user_settings()
        self.update_cbx_soaktime_settings()
        
        self.line_ramp_settings.read_user_settings()
        self.update_cbx_line_voltage_ramp()


    def test_type_index_changed(self):
        """ Change the UI elements as needed by the selected test.
        """

        # Get the index to be used for determining the test object type
        self.test_type_index = self.ui.cbx_add_tests_testtype.currentIndex()
        
        # Get the list of titles from the TestTypes list
      

        # Depending on the value of the combo box, display the 
        # UI pages needed by the test
        self.selected_test_class = TestTypes[self.test_type_index]

        
        self.select_stack_page_per_test()
        self.set_ui_states()
        self.update_test_conditions_default()
        self.update_load_range_table()
          
    
    
    def select_stack_page_per_test(self):
        """Change the page displayed on the stacked widgets
        depending on the selected test"""
        test_class:TemplateTest = self.selected_test_class
        ui_def:General_UI_Definitions = test_class.get_ui_definitions()

        self.ui.stackedwidget_add_tests_params_top.setCurrentIndex(
            ui_def.stack_page_1)
        self.ui.stackedwidget_add_tests_params_bot.setCurrentIndex(
            ui_def.stack_page_2)
        self.ui.stackedwidget_add_tests_middle.setCurrentIndex(
            ui_def.stack_page_3)

        # If test is an i2c test or has i2c_ui_definitions, change the i2c page stuff
        if (test_class.title in self.i2c_tests_names) or hasattr(test_class, 'i2c_ui_definitions'):
            self.set_i2c_page_ui_settings()
    
    def update_i2c_ui_on_inno_family_change(self):
        if self.inno_family_update_ready & (self.selected_test_class in InnoPro_TestTypes):
            self.inno_family_update_ready = False
            tc:TemplateTest = self.selected_test_class
            tc_ui:I2C_UI_Definitions = tc.i2c_ui_definitions
            tc_ui = tc.update_i2c_ui_definitions(self.ui.cbx_add_tests_i2c_cbxparam_4.currentText())
            cbx_index = self.ui.cbx_add_tests_i2c_cbxparam_4.currentIndex()
            self.update_i2c_page_ui_settings(tc_ui)
            self.ui.cbx_add_tests_i2c_cbxparam_4.setCurrentIndex(cbx_index)
            self.inno_family_update_ready = True
        
    def set_i2c_page_ui_settings(self):
        self.inno_family_update_ready = False
        tc:TemplateTest = self.selected_test_class
        if (self.selected_test_class in InnoPro_TestTypes):
            tc.set_i2c_ui_definitions()
        tc_ui:I2C_UI_Definitions = tc.i2c_ui_definitions
        self.update_i2c_page_ui_settings(tc_ui)
        self.inno_family_update_ready = True
    
    def update_i2c_page_ui_settings(self,tc_ui):
        ui = self.ui
        # Line edits
        le_ui_frames = self.i2c_ui_lineedit_frames
        le_ui_labels = self.i2c_ui_lineedit_labels
        le_vis_flags = tc_ui.lineedit_visibility_flags
        le_texts = tc_ui.lineedit_label_texts

        for frame, label in zip(le_ui_frames, le_ui_labels):
            frame.setVisible(False)
            label.setText('')

        for frame, label, flag, text in \
            zip(le_ui_frames, le_ui_labels, le_vis_flags, le_texts):
            # Loop through the UI and settings until the setting is undefined
            frame.setVisible(flag)
            label.setText(text)
        

        # Combo boxes
        cbx_frames = self.i2c_ui_cbx_frames
        cbx_labels = self.i2c_ui_cbx_labels
        cbx_list = self.i2c_ui_combo_boxes
        cbx_texts = tc_ui.cbx_label_texts
        cbx_contents = tc_ui.cbx_contents
        cbx_vis_flags = tc_ui.cbx_visibility_flags

        for frame, label in zip(cbx_frames, cbx_labels):
            frame.setVisible(False)
            label.setText('')

        for frame, label, text, cbx, flag, content in \
            zip(cbx_frames, cbx_labels, cbx_texts, cbx_list, cbx_vis_flags, cbx_contents):
            frame.setVisible(flag)
            label.setText(text)
            cbx.setMaximumWidth(16777215)
            cbx.clear()
            if not content is None:
                cbx.addItems(content)

    def set_ui_states(self):
        """Change the state of the UI depending on 
        the selected test type"""
        ui:Ui_MainWindow = self.ui
        # TODO: Update template based on Load Reg and include I2C/ other future options
        test_class:TemplateTest = TestTypes[self.test_type_index]
        
        # Define the flags that may change the UI
        ui_change_flags = UIChangeFlags()
        ui_change_flags.usb_pd_device_toggle_checked = self.ui.chkbox_add_tests_usbpd_device.checkState()

        # Get the UI definition from the selected test class
        ui_def:General_UI_Definitions = test_class.get_ui_definitions(flags=ui_change_flags)

        # Update the UI based on the received UI definition

        # Frames Visibility
        ui.frame_add_tests_timing_params.setVisible(ui_def.test_time_params_frame_visible)

        # Test Time Parameters
        ui.label_add_tests_testtime_param1.setText(ui_def.test_time_param1_label)
        ui.label_add_tests_testtime_param2.setText(ui_def.test_time_param2_label)
        ui.label_add_tests_testtime_param3.setText(ui_def.test_time_param3_label)
        ui.label_add_tests_testtime_param4.setText(ui_def.test_time_param4_label)
        ui.label_add_tests_testtime_param1.setVisible(ui_def.test_time_param1_visible)
        ui.label_add_tests_testtime_param2.setVisible(ui_def.test_time_param2_visible)
        ui.label_add_tests_testtime_param3.setVisible(ui_def.test_time_param3_visible)
        ui.label_add_tests_testtime_param4.setVisible(ui_def.test_time_param4_visible)
        ui.lineedit_add_tests_testtime_param1.setVisible(ui_def.test_time_param1_visible)
        ui.lineedit_add_tests_testtime_param2.setVisible(ui_def.test_time_param2_visible)
        ui.lineedit_add_tests_testtime_param3.setVisible(ui_def.test_time_param3_visible)
        ui.lineedit_add_tests_testtime_param4.setVisible(ui_def.test_time_param4_visible)

        # USBPD Settings
        # USBPD Device Toggle
        ui.chkbox_add_tests_usbpd_device.setVisible(ui_def.usb_pd_device_toggle_visible)
        if hasattr(self, 'usbpd_source_caps') & (not ui.table_add_tests_source_caps.currentRow() == -1) & ui.chkbox_add_tests_usbpd_device.isChecked():
            selection_index = ui.table_add_tests_source_caps.currentRow()
            source_caps_list = self.usbpd_source_caps
            source_cap:SourceCap = source_caps_list[selection_index]
            if (source_cap.supply_type == SUPPLY_TYPE.AUGMENTED) & (self.selected_test_class not in CVCC_TestTypes):
                ui_def.nominal_vout_visible = True 
                ui_def.nominal_vout_enable = True
            else:
                ui_def.nominal_vout_visible = False 
                ui_def.nominal_vout_enable = False
        
        # Nominal output current and voltage
        ui.frame_add_tests_nominal_output_current.setVisible(ui_def.nominal_iout_visible)
        ui.frame_add_tests_nominal_output_voltage.setVisible(ui_def.nominal_vout_visible)
        ui.frame_add_tests_nominal_output_voltage.setEnabled(ui_def.nominal_vout_enable)
        # Source caps table and button toggle
        ui.table_add_tests_source_caps.setVisible(ui_def.usbpd_sourcecaps_table_visible)
        ui.btn_add_tests_usbpd_get_source_caps.setVisible(ui_def.usbpd_getsourcecaps_btn_visible)  
        # Tracking PDO Requests
        ui.chkbox_add_tests_proportional_current_request.setVisible(ui_def.usbpd_tracking_pdo_chk_visible)
        
        # General Options
        ui.frame_add_tests_eload_type.setVisible(ui_def.load_type_visible)
        ui.chkbox_add_tests_measure_scope_ripple.setVisible(ui_def.measure_ripple_visible)
        ui.chkbox_add_tests_eload_measurement.setVisible(ui_def.use_eload_data_toggle_visible)
        ui.frame_add_tests_line_range_coupling.setVisible(ui_def.coupling_visible)
        
        # Load Range options
        ui.cbx_add_tests_load_range_type.setEnabled(ui_def.load_range_selection_enabled)
        ui.cbx_add_tests_load_range_direction.setEnabled(ui_def.load_direction_cbx_enabled)
        ui.label_add_tests_soak_per_load_2.setEnabled(ui_def.load_direction_cbx_enabled)
        
        # Add Test Buttons
        # Button 1 
        ui.btn_add_tests_option_1.setVisible(ui_def.add_test_button_1_visible)
        ui.btn_add_tests_option_1.setText(ui_def.add_test_button_1_txt)
        # Button 2
        ui.btn_add_tests_option_2.setVisible(ui_def.add_test_button_2_visible)
        ui.btn_add_tests_option_2.setText(ui_def.add_test_button_2_txt)
                  
        # CVCC multiple setpoints button
        self.ui.chkbox_add_tests_cvcc_multi_setpoints.setEnabled(ui_def.multiple_cvcc_setpoints_enable)
        self.ui.chkbox_add_tests_cvcc_multi_setpoints.setChecked(ui_def.multiple_cvcc_setpoints_enable)
        
        # I2C parameters
        
    def update_test_list_control_buttons_state(self):
        """Update ui button status for test item control"""
        
        if self.test_plan.status == TestStatus.IN_PROGRESS:
            self.ui.btn_add_tests_usbpd_get_source_caps.setEnabled(False)
        if self.test_plan.status in [TestStatus.STOPPED, TestStatus.COMPLETE]:
            self.ui.btn_add_tests_usbpd_get_source_caps.setEnabled(True)
            self.ui.btn_add_tests_run.setEnabled(True)
            
        test_item_index = self.ui.table_add_tests_test_list.currentRow()
        if test_item_index >= len(self.test_plan.test_items):
            test_item_index = len(self.test_plan.test_items) - 1
        if test_item_index < 0:
            return
        test_item = self.test_plan.test_items[test_item_index]

        if self.test_plan.status == TestStatus.IN_PROGRESS:
            self.ui.btn_add_tests_usbpd_get_source_caps.setEnabled(False)
            if test_item.status == TestStatus.IN_PROGRESS:
                self.ui.btn_add_tests_restart_selected_test.setEnabled(False)
                self.ui.btn_add_tests_remove_selected_test.setEnabled(False)
                self.ui.btn_add_tests_update_selected_test.setEnabled(False)
                self.ui.btn_add_tests_test_item_move_up.setEnabled(False)
                self.ui.btn_add_tests_test_item_move_down.setEnabled(False)
                self.ui.btn_add_tests_test_item_move_top.setEnabled(False)
                self.ui.btn_add_tests_test_item_move_bottom.setEnabled(False)
                
            else:
                self.ui.btn_add_tests_restart_selected_test.setEnabled(True)
                self.ui.btn_add_tests_remove_selected_test.setEnabled(True)
                self.ui.btn_add_tests_update_selected_test.setEnabled(True)
                if test_item.status == TestStatus.IN_QUEUE:
                    self.ui.btn_add_tests_test_item_move_up.setEnabled(True)
                    self.ui.btn_add_tests_test_item_move_down.setEnabled(True)
                    self.ui.btn_add_tests_test_item_move_top.setEnabled(True)
                    self.ui.btn_add_tests_test_item_move_bottom.setEnabled(True)
                else:
                    self.ui.btn_add_tests_test_item_move_up.setEnabled(False)
                    self.ui.btn_add_tests_test_item_move_down.setEnabled(False)
                    self.ui.btn_add_tests_test_item_move_top.setEnabled(False)
                    self.ui.btn_add_tests_test_item_move_bottom.setEnabled(False)
                    
        else:
                self.ui.btn_add_tests_restart_selected_test.setEnabled(True)
                self.ui.btn_add_tests_remove_selected_test.setEnabled(True)
                self.ui.btn_add_tests_update_selected_test.setEnabled(True)
                self.ui.btn_add_tests_test_item_move_up.setEnabled(True)
                self.ui.btn_add_tests_test_item_move_down.setEnabled(True)
                self.ui.btn_add_tests_test_item_move_top.setEnabled(True)
                self.ui.btn_add_tests_test_item_move_bottom.setEnabled(True)
                
        if test_item.status not in [TestStatus.IN_PROGRESS, TestStatus.IN_QUEUE]:
            self.ui.btn_add_tests_skip_selected_test.setEnabled(False)
        else:
            self.ui.btn_add_tests_skip_selected_test.setEnabled(True)
    def test_item_clicked(self):

        self.test_item_click_flag = True
        self.test_item_selected()
        
    def test_item_selection_changed(self):

        # sleep(0.05)
        if (not self.test_item_selection_item_changed_flag) and (not self.test_item_click_flag):
            self.test_item_selection_changed_flag = True
            self.test_item_selected()
        else:
            self.test_item_selection_changed_flag = False
                
    def test_item_selected_item_changed(self):
        
        if self.test_item_selection_item_changed_flag:
            self.test_item_selected()
    
    def test_item_selected(self):
        '''Update slected test conditions and test buttons when a test item is selected or changed'''
        
        # If no flags raised
        if not (self.test_item_click_flag or self.test_item_selection_changed_flag or self.test_item_selection_item_changed_flag):
            return
        self.test_item_selection_item_changed_flag = False
        self.test_item_selection_changed_flag = False
        self.test_item_click_flag = False
        self.ui.table_add_tests_test_list.setEnabled(False)
        
        test_item_index = self.ui.table_add_tests_test_list.currentRow()
        if (not test_item_index == -1) and (len(self.test_plan.test_items) > 0) and (test_item_index < len(self.test_plan.test_items)):
            
            self.item_selected = True
            
            # Get necessary indices and values and update test conditions in the depending on the test item selected
            
            # Test type settings
            self.selected_test_item = self.test_plan.test_items[test_item_index]
            self.ui.cbx_add_tests_testtype.setCurrentIndex(self.selected_test_item.test_type_index)
            
            selected_test_conditions = self.selected_test_item.test_conditions
            
            test_type_index = self.selected_test_item.test_type_index

            test_type:TemplateTest = TestTypes[test_type_index]
            
            ui_update_def = test_type.get_ui_update_definitions()
            
            line_settings_update = ui_update_def.line_settings_update
            load_settings_update = ui_update_def.load_settings_update
            soaktime_settings_update = ui_update_def.soaktime_settings_update
            cvcc_settings_update = ui_update_def.cvcc_settings_update
            line_ramp_settings_update = ui_update_def.line_ramp_settings_update
            nominal_output_settings_update = ui_update_def.nominal_output_settings_update
            usbpd_options_update = ui_update_def.usbpd_options_update
            tracking_pdo_request_update = ui_update_def.tracking_pdo_request_update
            measure_ripple_update = ui_update_def.measure_ripple_update
            load_direction_update = ui_update_def.load_direction_update
            eload_type_update = ui_update_def.eload_type_update
            use_eload_data_update = ui_update_def.use_eload_data_update
            coupling_update = ui_update_def.coupling_update
            i2c_params_update = ui_update_def.i2c_params_update
            
            if line_settings_update:
                # Line range settings
                if selected_test_conditions.line_range.name not in self.line_settings_names:
                    self.parent.msg_box_info('Line Range Error','Selected Line Range Settings unavailable. Setting line range to Custom',MessageType.INFO)
                    selected_test_conditions.line_range.name = LineSettings.CUSTOM.name
                    self.update_test_list_details()
                line_range_index = self.line_settings_names.index(selected_test_conditions.line_range.name)
                self.ui.cbx_add_tests_line_range_type.setCurrentIndex(line_range_index)
                
                # If custom range, write the values into the line range table. Else, clear table
                if selected_test_conditions.line_range.name ==  LineSettings.CUSTOM.name:
                    custom_line_range = LineRange(name='Dummy',vin_freq=copy(selected_test_conditions.line_range.vin_freq),custom=True)
                    self.custom_line_range_clear_entry()
                    self.line_settings.line_range_list[line_range_index].vin_freq = copy(custom_line_range.vin_freq)
                    self.update_line_range_table()
                else:
                    self.line_settings.line_range_list[self.line_settings_names.index(LineSettings.CUSTOM.name)].vin_freq.clear()
            
            if soaktime_settings_update:
                # Soaktime settings  
                if selected_test_conditions.soak_time.name not in self.soaktime_settings_names:
                    self.parent.msg_box_info('Soak Time Settings Error','Selected Soak Time Settings unavailable. Setting soak time setting to Custom',MessageType.INFO)
                    selected_test_conditions.soak_time.name = SoaktimeSettings.SOAK_CUSTOM.name
                    self.update_test_list_details()                
                soaktime_index = self.soaktime_settings_names.index(selected_test_conditions.soak_time.name)
                self.ui.cbx_add_tests_timing_params.setCurrentIndex(soaktime_index)
                
                # If custom range, write the values into the corresponding fields
                if selected_test_conditions.soak_time.name == SoaktimeSettings.SOAK_CUSTOM.name:
                    self.ui.lineedit_add_tests_testtime_param1.setText(f'{round(selected_test_conditions.soak_time.initial_soak,3):g}')
                    self.ui.lineedit_add_tests_testtime_param2.setText(f'{round(selected_test_conditions.soak_time.soak_per_line,3):g}')
                    self.ui.lineedit_add_tests_testtime_param3.setText(f'{round(selected_test_conditions.soak_time.soak_per_load,3):g}')
                    self.ui.lineedit_add_tests_testtime_param4.setText(f'{round(selected_test_conditions.soak_time.integration_time,3):g}')
            
            if load_settings_update:
                # Load range settings
                if selected_test_conditions.load_range.name not in self.load_settings_names:
                    self.parent.msg_box_info('Load Range Error','Selected Load Range Settings unavailable. Setting load range to Custom',MessageType.INFO)
                    selected_test_conditions.load_range.name = LoadSettings.LOAD_CUSTOM.name
                    self.update_test_list_details()
                load_range_index = self.load_settings_names.index(selected_test_conditions.load_range.name)
                self.ui.cbx_add_tests_load_range_type.setCurrentIndex(load_range_index)
                
                # If custom range, write the values into the load range table. Else, clear table
                if selected_test_conditions.load_range.name == LoadSettings.LOAD_CUSTOM.name:
                    custom_load_range = LoadRange(name='Dummy',load_range_pct=copy(selected_test_conditions.load_range.load_range_pct),custom=True)
                    self.custom_load_range_clear_entry()
                    self.load_settings.load_range_list[load_range_index].load_range_pct = copy(custom_load_range.load_range_pct)
                    self.update_load_range_table()
                    
                else:
                    self.load_settings.load_range_list[self.load_settings_names.index(LoadSettings.LOAD_CUSTOM.name)].load_range_pct.clear()
            
            if line_ramp_settings_update:
                # Line ramp settings
                if selected_test_conditions.line_ramp_settings.name not in self.line_ramp_settings_names:
                    self.parent.msg_box_info('Load Range Error','Selected Load Range Settings unavailable. Setting line ramp setting to Custom',MessageType.INFO)
                    selected_test_conditions.line_ramp_settings.name = LineRampSettings.RAMP_CUSTOM.name
                    self.update_test_list_details()
                line_ramp_index = self.line_ramp_settings_names.index(selected_test_conditions.line_ramp_settings.name)
                self.ui.cbx_add_tests_line_ramp_type.setCurrentIndex(line_ramp_index)
                freq = selected_test_conditions.line_ramp_settings.freq
                coupling = selected_test_conditions.line_ramp_settings.coupling
                
                # If custom range, write the values into the line ramp table. Else, clear table
                if selected_test_conditions.line_ramp_settings.name ==  LineRampSettings.RAMP_CUSTOM.name:
                    custom_line_ramp = LineRamp(name='Dummy',vin_slew=copy(selected_test_conditions.line_ramp_settings.vin_slew), freq = freq, coupling = coupling,custom=True)
                    self.custom_line_ramp_clear_entry()
                    self.line_ramp_settings.line_ramp_list[line_ramp_index].vin_slew = copy(custom_line_ramp.vin_slew)
                    self.update_line_ramp_table()

                else:
                    self.line_ramp_settings.line_ramp_list[self.line_ramp_settings_names.index(LineRampSettings.RAMP_CUSTOM.name)].vin_slew.clear()
                
                if coupling == 'DC':
                    coupling_toggle = True
                    self.ui.lineedit_add_tests_line_ramp_frequency.setText(f'')
                else:
                    coupling_toggle = False
                    self.ui.lineedit_add_tests_line_ramp_frequency.setText(f'{freq:g}')
                self.ui.widget_toggle_add_tests_line_ramp_coupling.setChecked(coupling_toggle)
            
            # Other tests conditions
            
            if load_direction_update:
                direction_index = self.load_direction_names.index(selected_test_conditions.general_options.load_direction)
                self.ui.cbx_add_tests_load_range_direction.setCurrentIndex(direction_index)
                
            if eload_type_update:
                eload_type_index = self.load_settings_mode_names.index(selected_test_conditions.general_options.eload_type)
                self.ui.cbx_add_tests_load_range_eload_type.setCurrentIndex(eload_type_index)
                    
            if measure_ripple_update:
                measure_ripple_state = selected_test_conditions.general_options.measure_ripple
                self.ui.chkbox_add_tests_measure_scope_ripple.setChecked(measure_ripple_state)
                    
            if coupling_update:
                coupling = selected_test_conditions.general_options.coupling
                if coupling == 'DC':
                    coupling_toggle = True
                else:
                    coupling_toggle = False
                self.ui.widget_toggle_add_tests_line_range_coupling.setChecked(coupling_toggle)
                

            usb_pd_enabled_state = selected_test_conditions.usbpd_options.usbpd_test
            if usbpd_options_update:
                self.ui.chkbox_add_tests_usbpd_device.setChecked(usb_pd_enabled_state)                
                if tracking_pdo_request_update:
                    usb_pd_tracking_state = selected_test_conditions.usbpd_options.tracking_pdo_request
                    self.ui.chkbox_add_tests_proportional_current_request.setChecked(usb_pd_tracking_state)
                
            
            if use_eload_data_update:
                use_eload_data_state = selected_test_conditions.general_options.use_eload_data
                self.ui.chkbox_add_tests_eload_measurement.setChecked(use_eload_data_state)
            
            if i2c_params_update:
                if test_type in InnoPro_TestTypes:
                    inno_pro_cbx = self.i2c_ui_combo_boxes[3]
                    inno_pro_family = selected_test_conditions.i2c_test_parameters.cbx_param[3]
                    cbx_option_index = test_type.i2c_ui_definitions.cbx_contents[3].index(inno_pro_family)
                    inno_pro_cbx.setCurrentIndex(cbx_option_index)
                    
                if hasattr(selected_test_conditions, 'i2c_test_parameters') and selected_test_conditions.i2c_test_parameters:
                    for line_index, line in enumerate(self.i2c_ui_lineedits):
                        if line_index < len(selected_test_conditions.i2c_test_parameters.param):
                            val = selected_test_conditions.i2c_test_parameters.param[line_index]
                            line.setText(f'{val:g}' if (val != 0 and val != '') else '')

                    for cbx_index, cbx in enumerate(self.i2c_ui_combo_boxes):
                        if cbx_index < len(selected_test_conditions.i2c_test_parameters.cbx_param):
                            val = str(selected_test_conditions.i2c_test_parameters.cbx_param[cbx_index])
                            if val == '' or val == '0':
                                continue
                            cbx_names = [cbx.itemText(i) for i in range(cbx.count())]
                            if val in cbx_names:
                                cbx.setCurrentIndex(cbx_names.index(val))
                    
                    
            if nominal_output_settings_update:
                # Nominal output settings
                nominal_output_voltage = selected_test_conditions.nominal_output_voltage_V
                nominal_output_current = selected_test_conditions.nominal_load_current_A
                
                # If USB PD
                if usb_pd_enabled_state:
                
                    # Check if source caps have been requested
                    if not hasattr(self, 'usbpd_source_caps'):
                        pass
                    
                    else:
                        # Get list of all source caps, fixed pdo, pps objects, and avs objects
                        source_caps:list[SourceCap] = self.usbpd_source_caps
                        fixed_source_caps:list[SourceCap] = self.usbpd_fixed_source_caps
                        pps_source_caps:list[SourceCap] = self.usbpd_pps_source_caps
                        epr_avs_source_caps:list[SourceCap] = self.usbpd_epr_avs_source_caps
                        spr_avs_source_caps:list[SourceCap] = self.usbpd_spr_avs_source_caps
                        # Get voltage and current values for all fixed PDOs
                        fixed_source_caps_voltage_V = [x.voltage_mV/1000 for x in fixed_source_caps]
                        
                        fixed_source_caps_current_A = [x.max_current_mA/1000 for x in fixed_source_caps]
                        
                        # If using FPDO and not supported by any FPDO
                        if (nominal_output_voltage not in fixed_source_caps_voltage_V) and \
                            (selected_test_conditions.usbpd_options.pdo_type == SUPPLY_TYPE.FIXED):
                            self.parent.msg_box_info(
                                title="Test Item Warning",
                                message=f"Nominal Voltage Settings not found in source capabilities",
                                message_type=MessageType.WARNING
                            )
                            
                        # If using PPS or AVS
                        elif selected_test_conditions.usbpd_options.pdo_type == SUPPLY_TYPE.AUGMENTED:
                            source_cap_index_V = -1
                            
                            # Check capability of each PPS object
                            if  selected_test_conditions.usbpd_options.augmented_type == AUGMENTED_TYPE.SPR_PPS:
                                for source_cap_pps in pps_source_caps:
                                    if (nominal_output_voltage >= round(source_cap_pps.min_voltage_mV/1000,3)) and \
                                        (nominal_output_voltage <= round(source_cap_pps.max_voltage_mV/1000,3)):
                                        source_cap_index_V = source_caps.index(source_cap_pps)
                                        break
                                        
                            # Check capability of each EPR AVS object
                            elif selected_test_conditions.usbpd_options.augmented_type == AUGMENTED_TYPE.EPR_AVS:
                                for source_cap_avs in epr_avs_source_caps:
                                    if (nominal_output_voltage >= round(source_cap_avs.min_voltage_mV/1000,3)) and \
                                        (nominal_output_voltage <= round(source_cap_avs.max_voltage_mV/1000,3)):
                                        source_cap_index_V = source_caps.index(source_cap_avs)
                                        break
                                    
                            # Check capability of each SPR AVS object
                            elif selected_test_conditions.usbpd_options.augmented_type == AUGMENTED_TYPE.SPR_AVS:
                                for source_cap_avs in spr_avs_source_caps:
                                    if (nominal_output_voltage >= round(source_cap_avs.min_voltage_mV/1000,3)) and \
                                        (nominal_output_voltage <= round(source_cap_avs.max_voltage_mV/1000,3)):
                                        source_cap_index_V = source_caps.index(source_cap_avs)
                                        break
                                        
                            # If not supported by any PPS or AVS object
                            if source_cap_index_V == -1:
                                self.parent.msg_box_info(
                                title="Test Item Warning",
                                message=f"Nominal Voltage Settings not found in source capabilities",
                                message_type = MessageType.WARNING
                                )
                            
                            # Update selection on source caps table and nominal voltage field          
                            self.ui.table_add_tests_source_caps.setCurrentIndex(self.ui.table_add_tests_source_caps.model().index(source_cap_index_V,0))
                            self.ui.lineedit_add_tests_nominal_output_voltage.setText(f'{round(nominal_output_voltage,3):g}')
                            
                        # If supported by a fixed PDO and is using FPDO
                        elif (nominal_output_voltage in fixed_source_caps_voltage_V) and \
                            (selected_test_conditions.usbpd_options.pdo_type == SUPPLY_TYPE.FIXED):
                            source_cap_index_V = -1
                            for fixed_source_cap in fixed_source_caps:
                                if (nominal_output_voltage*1000) == fixed_source_cap.voltage_mV:
                                    source_cap_index_V = source_caps.index(fixed_source_cap)
                                    break
                            
                            if source_cap_index_V == -1:
                                self.parent.msg_box_info(
                                title="Test Item Warning",
                                message=f"Nominal Voltage Settings not found in source capabilities",
                                message_type = MessageType.WARNING
                                )
                            
                            # If  FPDO does not support the nominal current
                            elif  source_caps[source_cap_index_V].max_current_mA < (nominal_output_current*1000):
                                self.parent.msg_box_info(
                                    title="Test Item Warning",
                                    message=f"Fixed PDO for {round(nominal_output_voltage,3):g} V does not support nominal load current",
                                    message_type = MessageType.WARNING
                                )
                            else:
                                # Update source cap table to select the corresponding PDO
                                self.ui.table_add_tests_source_caps.setCurrentIndex(self.ui.table_add_tests_source_caps.model().index(source_cap_index_V,0))
                                
                # If non USB PD
                else:
                    
                    # Update nominal voltage field
                    self.ui.lineedit_add_tests_nominal_output_voltage.setText(f'{round(nominal_output_voltage,3):g}')
                    
                # Update nominal current field    
                self.ui.lineedit_add_tests_nominal_output_current.setText(f'{round(nominal_output_current,6):g}')
            
            
            # Update fields for nominal values for CVCC Test        
            if cvcc_settings_update:
                # Nominal output settings
                nominal_output_voltage = selected_test_conditions.nominal_output_voltage_V
                nominal_output_current = selected_test_conditions.nominal_load_current_A

                # If USB PD
                if usb_pd_enabled_state:
                    
                    # Check if source caps have been requested
                    if not hasattr(self, 'usbpd_source_caps'):
                        pass
                    else:
                        
                        # Get list of all source caps and pps source caps
                        source_caps:list[SourceCap] = self.usbpd_source_caps
                        pps_source_caps:list[SourceCap] = self.usbpd_pps_source_caps
            
                        source_cap_index_V = -1
                        # Check capability of each PPS object
                        for source_cap_pps in pps_source_caps:
                            if (selected_test_conditions.nominal_output_voltage_V >= round(source_cap_pps.min_voltage_mV/1000,3)) and (selected_test_conditions.nominal_output_voltage_V <= round(source_cap_pps.max_voltage_mV/1000,3)):
                                source_cap_index_V = source_caps.index(source_cap_pps)

                        # If not supported by any PPS object
                        if source_cap_index_V == -1:
                            self.parent.msg_box_info(
                            title="Test Item Warning",
                            message=f"Nominal Voltage Settings not found in source capabilities",
                            message_type = MessageType.WARNING
                            )
                        else:
                            # Update source cap table to select the corresponding PDO
                            self.ui.table_add_tests_source_caps.setCurrentIndex(self.ui.table_add_tests_source_caps.model().index(source_cap_index_V,0))
                
                # Set multi setpoint option to false when selecting a cvcc test item to prevent creatng multiple tests out of one selection
                self.ui.chkbox_add_tests_cvcc_multi_setpoints.setChecked(False)
                
                # Update nominal voltage and current field
                self.ui.lineedit_add_tests_cvcc_nom_voltage.setText(f'{round(nominal_output_voltage,3):g}')
                self.ui.lineedit_add_tests_cvcc_max_current.setText(f'{round(nominal_output_current,6):g}')
                
            # Test conditions update done
            self.item_selected = False
        
        self.ui.table_add_tests_test_list.setEnabled(True)
        
        self.update_test_list_control_buttons_state()

    def update_test_conditions_default(self):
        """Update default test conditions based on selected test type"""
        if not self.item_selected:
            line_range_index = self.line_settings.line_range_list.index(
                (self.test_condition_settings.test_condition_list[self.test_type_index]).line_range)
            load_range_index = self.load_settings.load_range_list.index(
                (self.test_condition_settings.test_condition_list[self.test_type_index]).load_range)
            soaktime_index = self.soaktime_settings.soaktime_list.index(
                (self.test_condition_settings.test_condition_list[self.test_type_index]).soak_time)
            coupling_state = self.test_condition_settings.test_condition_list[self.test_type_index]\
                .general_options.coupling
            measure_ripple_state = self.test_condition_settings.test_condition_list[self.test_type_index]\
                .general_options.measure_ripple
            usb_pd_tracking_state = self.test_condition_settings.test_condition_list[self.test_type_index]\
                .usbpd_options.tracking_pdo_request
            
            self.ui.cbx_add_tests_line_range_type.setCurrentIndex(line_range_index)
            self.ui.cbx_add_tests_load_range_type.setCurrentIndex(load_range_index)
            self.ui.cbx_add_tests_timing_params.setCurrentIndex(soaktime_index)
            self.ui.chkbox_add_tests_measure_scope_ripple.setChecked(measure_ripple_state)
            if coupling_state == 'DC':
                self.ui.widget_toggle_add_tests_line_range_coupling.setChecked(True)
            else:
                self.ui.widget_toggle_add_tests_line_range_coupling.setChecked(False)
            self.ui.chkbox_add_tests_eload_measurement.setChecked(False)
            self.ui.cbx_add_tests_load_range_direction.setCurrentIndex(0)
            self.ui.cbx_add_tests_load_range_eload_type.setCurrentIndex(0)
            self.ui.chkbox_add_tests_proportional_current_request.setChecked(usb_pd_tracking_state)
            
            self.ui.lineedit_add_tests_cvcc_nom_voltage.setText('5')
            self.ui.lineedit_add_tests_cvcc_max_current.setText('5')
            self.ui.lineedit_add_tests_cvcc_min_current.setText('1')
            self.ui.lineedit_add_tests_cvcc_step_size.setText('0.5')
            
            self.ui.lineedit_add_tests_nominal_output_voltage.setText('')
            self.ui.lineedit_add_tests_nominal_output_current.setText('')
            
            if hasattr(self.selected_test_class, 'i2c_ui_definitions'):
                default_i2c = getattr(self.selected_test_class.tc_default, 'i2c_test_parameters', None)
                if default_i2c:
                    for idx, line in enumerate(self.i2c_ui_lineedits):
                        if idx < len(default_i2c.param) and default_i2c.param[idx] != 0:
                            line.setText(f"{default_i2c.param[idx]:g}")
                        else:
                            line.setText('')
                    for idx, cbx in enumerate(self.i2c_ui_combo_boxes):
                        if idx < len(default_i2c.cbx_param) and default_i2c.cbx_param[idx] != 0 and default_i2c.cbx_param[idx] != '':
                            cbx_item = str(default_i2c.cbx_param[idx])
                            cbx_names = [cbx.itemText(i) for i in range(cbx.count())]
                            if cbx_item in cbx_names:
                                cbx.setCurrentIndex(cbx_names.index(cbx_item))
                else:
                    for line in self.i2c_ui_lineedits:
                        line.setText('')
            else:
                for line in self.i2c_ui_lineedits:
                    line.setText('')

    
    def usbpd_dev_toggle_changed(self):
        self.set_ui_states()
        
        # Update load range table
        self.update_load_range_table()
    
    def results_folder_toggle_changed(self):
        """Hide or show the result folder combo box depending on chekbox state
        Save the UI state on the configs"""
        # Check the state fo the checkbox
        checkbox_state = self.ui.chkbox_add_tests_results_folder.isChecked()

        # Show the combo box if the check box is checked
        self.ui.frame_add_tests_results_folder.setVisible(checkbox_state)

        # Update the items on the results folder combo box
        subfolders = self.get_parent_dir_subfolders()
        
        self.ui.cbx_add_tests_results_folder.clear()
        self.ui.cbx_add_tests_results_folder.addItems(subfolders)

        # Save the state of the UI
        configs.write_to_default_config(
            key=SaveFileKeys.RESULT_FOLDER_TOGGLE,value=checkbox_state)

    def result_folder_cbx_changed(self):
        """Save the folder selected"""
        folder = self.ui.cbx_add_tests_results_folder.currentText()
        configs.write_to_default_config(
            key=SaveFileKeys.RESULT_FOLDER, value=folder)

    def select_current_run_results_folder(self):
        """Force the results folder toggle to true and select the current output folder."""
        # TODO: Fix later
        return
        self.ui.chkbox_add_tests_results_folder.setChecked(True)
        self.results_folder_toggle_changed()

        folder_index = self.subfolders.index(self.folder_name)
        self.ui.cbx_add_tests_results_folder.setCurrentIndex(folder_index)

    def cvcc_multi_setpoints_toggle_changed(self):
        # Check the state fo the checkbox
        checkbox_state = self.ui.chkbox_add_tests_cvcc_multi_setpoints.isChecked()

        # Show the min current and step size if checkbox is ticked, hide if not
        self.ui.label_add_tests_cvcc_min_current.setEnabled(checkbox_state)
        self.ui.label_add_tests_cvcc_step_size.setEnabled(checkbox_state)
        self.ui.lineedit_add_tests_cvcc_min_current.setEnabled(checkbox_state)
        self.ui.lineedit_add_tests_cvcc_step_size.setEnabled(checkbox_state)
        
    def input_line_ramp_coupling_toggle_changed(self):
        """Update enabled state of frequency input on Input Line Ramp settings depending on coupling"""
        widget = self.ui.widget_toggle_add_tests_line_ramp_coupling
        if widget.isChecked():
            widget.setText("Coupling: DC")
            self.ui.lineedit_add_tests_line_ramp_frequency.setEnabled(False)
        else:
            widget.setText("Coupling: AC")
            self.ui.lineedit_add_tests_line_ramp_frequency.setEnabled(True)
    
    def line_range_coupling_toggle_changed(self):
        widget = self.ui.widget_toggle_add_tests_line_range_coupling

        if widget.isChecked():
            widget.setText("Coupling: DC")
        else:
            widget.setText("Coupling: AC")
        self.update_line_range_table()

    def get_parent_dir_subfolders(self):
        """Return the list of folders inside the parent folder"""
        parent_folder_path = self.ui.lineedit_add_tests_output_folder_location.text()
        
        subfolders = []
        if os.path.exists(parent_folder_path):

            for file in os.listdir(parent_folder_path):
                path = os.path.join(parent_folder_path, file)
                if os.path.isdir(path):
                    subfolders.append(file)
        self.subfolders = subfolders
        self.parent_folder_path = parent_folder_path
        return subfolders

    
    # Get Source Caps Related Functions

    @Slot(str)
    def slot_print(self, txt):
        """Print the state of the thread on the GetSourceCaps button."""
        self.ui.btn_add_tests_usbpd_get_source_caps.setText(txt)

    @Slot(list)
    def receive_source_caps(self, received_caps_list):
        """Process the received source caps from the thread."""
        self.usbpd_source_caps = received_caps_list[0]
        self.usbpd_fixed_source_caps = received_caps_list[1]
        self.usbpd_pps_source_caps = received_caps_list[2]
        self.usbpd_epr_avs_source_caps = received_caps_list[3]
        self.usbpd_spr_avs_source_caps = received_caps_list[4]
        # Update the contents of the source caps UI 
        self.update_source_caps_ui()
        # If no source caps received, show message
        message  = "Test routine finished but there are no source caps received.\n"
        message += "Please check USB PD power supply connection."
        if len(self.usbpd_source_caps) == 0:
            self.parent.msg_box_info("Get Source Caps Error", message, MessageType.INFO)

    @Slot()
    def source_caps_worker_done(self):
        """Run the methods needed after the worker finishes."""
        # Clean up the thread that run the process
        self.get_source_caps_thread_exit()
        
    @Slot()    
    def source_caps_thread_cleanup(self):
        self.get_source_caps_worker.deleteLater()
        self.get_source_caps_thread.deleteLater()
        # Method to be run by the timer below
        def clear_source_cap_thread_object():
            self.get_source_caps_thread = None

            # Revert the button text to default
            self.ui.btn_add_tests_usbpd_get_source_caps.setText("Get Source Cap")

            # Enable the buttton for Get Source Caps and RUN TESTS
            self.ui.btn_add_tests_usbpd_get_source_caps.setEnabled(True)
            self.ui.btn_add_tests_run.setEnabled(True)
        
        # Run a timer that will clear the thread object
            # after 5 seconds
        QTimer.singleShot(5000, clear_source_cap_thread_object)
        

    @Slot()
    def get_source_caps_exception(self):
        """Run in case the GetSourceCaps thread encountered an exception."""
        # Clean up the thread that run the process
        self.get_source_caps_thread_exit()
        # Show a message for the error
        message  = "Encountered an error while running routine.\n"
        message += "Please check AC source and Sink Controller connection."
        self.parent.msg_box_info("Get Source Caps Error", message, MessageType.INFO)
        # Clear the source caps table
        self.ui.table_add_tests_source_caps.clearContents()

    def get_source_caps(self):
        """Create a thread that will run a GetSourceCaps routine"""

        # User Prompt
        message = "This routine will turn on the connected AC source with 115Vac.\n"
        message += "Ensure that the setup is ready to prevent accidents."
        response = self.parent.msg_box_pick("Get Source Caps", message)

        # Proceed only if response is OK
        if not (response == QMessageBox.Ok):
            return

        # Disable button
        get_source_caps_button = self.ui.btn_add_tests_usbpd_get_source_caps
        get_source_caps_button.setEnabled(False)
        self.ui.btn_add_tests_run.setEnabled(False)

        # Check if the AC source and Sink Controller are ready
        # If one is not connected, re-enable button and return prematurely
        if not self.sink_controller_and_ac_source_ready():
            get_source_caps_button.setEnabled(True)
            self.ui.btn_add_tests_run.setEnabled(True)
            self.ui.table_add_tests_source_caps.clearContents()
            return

        # Create a thread object
        self.get_source_caps_thread = QThread()
        # Create the worker object
        self.get_source_caps_worker = GetSourceCapsWorker(
            self.ac_source, self.usbpd_sink, self.electronic_load)
        # Move worker to the thread
        self.get_source_caps_worker.moveToThread(self.get_source_caps_thread)
        # Connect signals and slots for the thread
        self.get_source_caps_thread.started.connect(self.get_source_caps_worker.run)
        # Connect signals and slots for the worker
        self.get_source_caps_worker.state.connect(self.slot_print)
        self.get_source_caps_worker.received_caps.connect(self.receive_source_caps)
        # Connect signal for failed test
        self.get_source_caps_worker.failed.connect(self.get_source_caps_exception)
        # Connections for thread cleanup
        self.get_source_caps_worker.finished.connect(self.source_caps_worker_done)
        self.get_source_caps_thread.finished.connect(self.source_caps_thread_cleanup)    
        
        sleep(1)
        # Start the thread
        self.get_source_caps_thread.start()
        
    
    def sink_controller_and_ac_source_ready(self)->bool:
        """Check if AC source and USB PD sink are ready."""
        source_present = True
        sink_controller_present = True
        
        # Update the GPIB equipment 
        self.equipment.update_accessible_visa_equipment()
        self.equipment.initialize_equipment_role_assigment()
        self.setup_equipment()

        # Check if ac source is detected
        try:
            self.ac_source.update_status()
        except (VisaIOError, AttributeError):
            source_present = False

        # Check if sink controller is detected
        try:
            self.usbpd_sink.ping_sink_controller_device()
            if  self.usbpd_sink.status == SINK_STATE.SINK_DISCONNECTED:
                sink_controller_present = False
        except:
            sink_controller_present = False
        
        # If only source is not present
        if not source_present:
            self.parent.msg_box_info(
                title="Get Source Caps Error",
                message="AC source not detected.",
                message_type = MessageType.WARNING
            )
            return False
        # If only sink controller is not present
        if not sink_controller_present:
            self.parent.msg_box_info(
                title="Get Source Caps Error",
                message="USBPD sink controller not detected.",
                message_type = MessageType.WARNING
            )
            return False
        # If both are not present
        if not sink_controller_present and not source_present:
            self.parent.msg_box_info(
                title="Get Source Caps Error",
                message="AC source and USBPD sink controller not detected.",
                message_type = MessageType.WARNING
            )
            return False
        # If there are no issues, return true
        return True

    def get_source_caps_thread_exit(self):
        """Clean up the thread that run the Get Source Caps routine."""
        self.ui.btn_add_tests_usbpd_get_source_caps.setText("Cleaning up thread")
        # Quit the thread to prepare it for deletion
        if self.get_source_caps_thread is not None:
            self.get_source_caps_thread.quit()
            
    def update_source_caps_ui(self):
        # Clear the table
        self.ui.table_add_tests_source_caps.clearContents()

        # Received source caps
        source_caps_list = self.usbpd_source_caps

        # Set table widget row count equal to the number of source caps
        self.ui.table_add_tests_source_caps\
            .setRowCount(len(source_caps_list))


        for row, source_cap in enumerate(source_caps_list):
            source_cap:SourceCap = source_cap
            object_position_txt:str = str(source_cap.object_position)

            pdo_type_txt:str = source_cap.pdo_type_text
            
            # TODO: change implementation if pdo is not input
            # Text for source cap Vout depending on source cap type
            if source_cap.supply_type == SUPPLY_TYPE.FIXED:
                voltage_text = f'{source_cap.voltage_mV / 1000:g} V'
            elif pdo_type_txt == "SPR AVS":
                if source_cap.max_current_high_range_mA == 0:
                    voltage_text = f'{source_cap.min_voltage_mV / 1000:g} V '
                    voltage_text += f'to {source_cap.max_voltage_mV/1000:g} V'
                elif source_cap.max_current_low_range_mA == source_cap.max_current_high_range_mA:
                    voltage_text = f'{source_cap.min_voltage_mV / 1000:g} V '
                    voltage_text += f'to {source_cap.max_voltage_mV/1000:g} V'
                else:
                    voltage_text = f'{source_cap.min_voltage_mV / 1000:g} V '
                    voltage_text += f'to {PD_SPECS.USBPD_MAX_SPR_AVS_LOW_VOLTAGE_V:g} V\n'
                    voltage_text += f'{PD_SPECS.USBPD_MAX_SPR_AVS_LOW_VOLTAGE_V:g} V '
                    voltage_text += f'to {source_cap.max_voltage_mV / 1000:g} V'
            else:
                voltage_text = f'{source_cap.min_voltage_mV / 1000:g} V '
                voltage_text += f'to {source_cap.max_voltage_mV / 1000:g} V'
                
            if pdo_type_txt == "EPR AVS":
                current_text = f'{source_cap.max_current_mA/1000:g} A'
            elif pdo_type_txt == "SPR AVS":
                if source_cap.max_current_high_range_mA == 0:
                    current_text =f'{source_cap.max_current_low_range_mA / 1000:g} A'
                elif source_cap.max_current_low_range_mA == source_cap.max_current_high_range_mA:
                    current_text =f'{source_cap.max_current_low_range_mA / 1000:g} A'
                else:
                    current_text = f'{source_cap.max_current_low_range_mA / 1000:g} A\n{source_cap.max_current_high_range_mA / 1000:g} A'
            else:
                current_text = f'{source_cap.max_current_mA/1000:g} A'
            
            if pdo_type_txt == "EPR AVS":
                power_text = f'{source_cap.pd_power_W} W' 
            elif pdo_type_txt == "SPR AVS":
                power_text =  f'{round(source_cap.max_voltage_mV / 1000 * source_cap.max_current_high_range_mA/1000,6):g} W'
            elif source_cap.supply_type == SUPPLY_TYPE.FIXED:
                power_text =  f'{round(source_cap.voltage_mV / 1000 * source_cap.max_current_mA/1000,3):g} W'
            else:
                power_text =  f'{round(source_cap.max_voltage_mV / 1000 * source_cap.max_current_mA/1000,3):g} W'
            
            self.ui.table_add_tests_source_caps.setItem(
                row, 0, QtWidgets.QTableWidgetItem(object_position_txt))
            self.ui.table_add_tests_source_caps.setItem(
                row, 1, QtWidgets.QTableWidgetItem(pdo_type_txt))
            self.ui.table_add_tests_source_caps.setItem(
                row, 2, QtWidgets.QTableWidgetItem(voltage_text))
            self.ui.table_add_tests_source_caps.setItem(
                row, 3, QtWidgets.QTableWidgetItem(current_text))
            self.ui.table_add_tests_source_caps.setItem(
                row, 4, QtWidgets.QTableWidgetItem(power_text))
            
    def source_caps_table_selected(self):
        self.set_ui_states()
        self.update_load_range_table()
        
    # Routine for the 1st add test button
    # Normally for single test
    def add_single_test(self):
        """ Add a single"""
        test_type = TestTypes[self.test_type_index]
        current_len = len(self.test_plan.test_items)
        match test_type.title:
            # Special Cases
            case CVCCTest.title:
                self.add_cvcc_test()

            case NoLoadPowerTest.title:
                self.add_no_load_power_test()
            
            case test_type.title if test_type.title in self.i2c_tests_names:
                self.add_i2c_test()
                
            # Default case
            case _:
                if self.ui.chkbox_add_tests_usbpd_device.isChecked():
                    self.test_single_pdo()
                else:
                    self.test_non_pdo()
                    
        # Check if adding single test was successful            
        if len(self.test_plan.test_items) > 0:
            if len(self.test_plan.test_items) > current_len:
                selection_index = len(self.test_plan.test_items) - 1
                self.ui.table_add_tests_test_list.setCurrentIndex(self.ui.table_add_tests_test_list.model().index(selection_index,0))


    # def process_cvcc_settings(self):
    #     ui:Ui_MainWindow = self.ui

    #     cvcc_settings = CVCCSettings()
        
    #     cvcc_settings.multiple_setpoints = ui.chkbox_add_tests_cvcc_multi_setpoints.checkState()
        
    #     if cvcc_settings.multiple_setpoints:
    #         if (not is_numeric(self.ui.lineedit_add_tests_cvcc_nom_voltage.text())) or \
    #             (not is_numeric(self.ui.lineedit_add_tests_cvcc_max_current.text())) or \
    #             (not is_numeric(self.ui.lineedit_add_tests_cvcc_min_current.text())) or \
    #             (not is_numeric(self.ui.lineedit_add_tests_cvcc_step_size.text())):
    #             self.parent.msg_box_info(
    #                 title = "Input Error!",
    #                 message = "Please enter numeric inputs.",
    #                 message_type = MessageType.INFO
    #             )
    #             raise InputError("CVCC: Inputs are not numeric")
    #     else:
    #         if (not is_numeric(self.ui.lineedit_add_tests_cvcc_nom_voltage.text())) or \
    #             (not is_numeric(self.ui.lineedit_add_tests_cvcc_max_current.text())):
    #             self.parent.msg_box_info(
    #                 title = "Input Error!",
    #                 message = "Please enter numeric inputs.",
    #                 message_type = MessageType.INFO
    #             )
    #             raise InputError("CVCC: Inputs are not numeric")
        
    #     cvcc_settings.nom_vout_V = rounded_float(ui.lineedit_add_tests_cvcc_nom_voltage.text())
    #     cvcc_settings.max_current_A = rounded_float(ui.lineedit_add_tests_cvcc_max_current.text())
        
    #     return cvcc_settings

    def get_i2c_parameters_from_ui(self):
        """Return an I2CTestParameters object created from the UI inputs."""
        params = []
        cbx_params = []
        for line in self.i2c_ui_lineedits:
            val = line.text()

            if (val == '') or (not is_numeric(val)):
                params.append(0)
            elif is_numeric(val):
                params.append(float(val))
        for cbx in self.i2c_ui_combo_boxes:
            val = cbx.currentText()

            cbx_params.append(val)

        i2c_test_parameters = I2CTestParameters(params, cbx_params)
        return i2c_test_parameters

    def get_timing_params_from_ui(self):
        """Return a SoakTime object created from the UI inputs"""

        # Timing Settings
        initial_soak_time_s:float \
            = rounded_float(
                self.ui.lineedit_add_tests_testtime_param1.text())
        soak_time_per_line_s:float \
            = rounded_float(
                self.ui.lineedit_add_tests_testtime_param2.text())
        soak_time_per_load_s:float \
            = rounded_float(
                self.ui.lineedit_add_tests_testtime_param3.text())
        integration_time_s:float \
            = rounded_float(
                self.ui.lineedit_add_tests_testtime_param4.text())
        soak_time = SoakTime(
            self.selected_soaktime.name,initial_soak_time_s, 
            soak_time_per_line_s,soak_time_per_load_s, integration_time_s)
        
        return soak_time

    def get_general_options_from_ui(self):
        """Return a GeneralOptions object created from the UI inputs"""
        
        # General Options
        general_options = GeneralOptions()
        general_options.measure_ripple:bool = \
            self.ui.chkbox_add_tests_measure_scope_ripple.isChecked()
        general_options.use_eload_data:bool = \
            self.ui.chkbox_add_tests_eload_measurement.isChecked()
        general_options.eload_type:str = \
            self.ui.cbx_add_tests_load_range_eload_type.currentText()
        general_options.load_direction:str  =\
            self.ui.cbx_add_tests_load_range_direction.currentText()
        if self.selected_test_class.title == InputLineRampTest.title:
            if self.ui.widget_toggle_add_tests_line_ramp_coupling.isChecked():
                general_options.coupling:str = 'DC'
            else:
                general_options.coupling:str = 'AC'
        else:
            if self.ui.widget_toggle_add_tests_line_range_coupling.isChecked():
                general_options.coupling:str = 'DC'
            else:
                general_options.coupling:str = 'AC'
        return general_options
       
    def get_usbpd_options_from_ui(self, source_cap:SourceCap = None):
        """Return a USBPDOptions object created from the UI inputs and selected source cap"""
        
        # USBPD Options
        usbpd_options = USBPDOptions()
        usbpd_options.usbpd_test:bool = \
            self.ui.chkbox_add_tests_usbpd_device.isChecked()
        usbpd_options.tracking_pdo_request:bool = \
            self.ui.chkbox_add_tests_proportional_current_request.isChecked()
            
        if source_cap is not None:
            usbpd_options.pdo_type:SUPPLY_TYPE = \
                source_cap.supply_type
            
            # Update augmented type if selected object is PPS or AVS
            if usbpd_options.pdo_type == SUPPLY_TYPE.AUGMENTED:
                usbpd_options.augmented_type = source_cap.augmented_type
        return usbpd_options
    
    def process_cvcc_inputs(self):
        # Check first if inputs are valid
        if (self.ui.lineedit_add_tests_cvcc_nom_voltage.text() == '') and \
            (self.ui.lineedit_add_tests_cvcc_max_current.text() == '') and \
             (self.ui.lineedit_add_tests_cvcc_min_current.text() == '') and \
            (self.ui.lineedit_add_tests_cvcc_step_size.text() == ''):
            return False
        
        cvcc_settings = CVCCSettings()
        
        cvcc_settings.multiple_setpoints = self.ui.chkbox_add_tests_cvcc_multi_setpoints.checkState()
        
        if cvcc_settings.multiple_setpoints:
            if (not is_numeric(self.ui.lineedit_add_tests_cvcc_nom_voltage.text())) or \
                (not is_numeric(self.ui.lineedit_add_tests_cvcc_max_current.text())) or \
                (not is_numeric(self.ui.lineedit_add_tests_cvcc_min_current.text())) or \
                (not is_numeric(self.ui.lineedit_add_tests_cvcc_step_size.text())):
                self.parent.msg_box_info(
                    title = "Input Error!",
                    message = "Please enter numeric inputs.",
                    message_type = MessageType.INFO
                )
                return False

            cvcc_settings.nom_vout_V = rounded_float(self.ui.lineedit_add_tests_cvcc_nom_voltage.text())
            cvcc_settings.max_current_A = rounded_float(self.ui.lineedit_add_tests_cvcc_max_current.text())
            cvcc_settings.min_current_A = rounded_float(self.ui.lineedit_add_tests_cvcc_min_current.text())
            cvcc_settings.step_size_A = rounded_float(self.ui.lineedit_add_tests_cvcc_step_size.text())
            
            if cvcc_settings.max_current_A < cvcc_settings.min_current_A:
                self.parent.msg_box_info(
                    title="Test Item Error!",
                    message=f"Entered maximum output current is not greater than the minimum output current",
                    message_type = MessageType.WARNING
                )
                return False
        else:
            if (not is_numeric(self.ui.lineedit_add_tests_cvcc_nom_voltage.text())) or \
                (not is_numeric(self.ui.lineedit_add_tests_cvcc_max_current.text())):
                self.parent.msg_box_info(
                    title = "Input Error!",
                    message = "Please enter numeric inputs.",
                    message_type = MessageType.INFO
                )
                return False
            
            cvcc_settings.nom_vout_V = rounded_float(self.ui.lineedit_add_tests_cvcc_nom_voltage.text())
            cvcc_settings.max_current_A = rounded_float(self.ui.lineedit_add_tests_cvcc_max_current.text())
            
        return True


    # TODO: Add expected UV range
    def add_cvcc_test(self):
        
        if not self.process_cvcc_inputs():
            return
        
        ui:Ui_MainWindow = self.ui

        test_type_index = self.test_type_index

        # USBPD Options
        usbpd_options = self.get_usbpd_options_from_ui()
        
        # General Options
        general_options = self.get_general_options_from_ui()

        # Test Condition Ranges
        load_range_pct= LoadRange(name = self.selected_load_range.name,load_range_pct= copy(self.selected_load_range.load_range_pct))
        
        line_range= LineRange(name = self.selected_line_range.name, vin_freq = copy(self.selected_line_range.vin_freq))

        # CVCC Test Settings
        cvcc_settings = CVCCSettings()
        
        cvcc_settings.multiple_setpoints = ui.chkbox_add_tests_cvcc_multi_setpoints.checkState()
        
        cvcc_settings.nom_vout_V = rounded_float(ui.lineedit_add_tests_cvcc_nom_voltage.text())
        cvcc_settings.max_current_A = rounded_float(ui.lineedit_add_tests_cvcc_max_current.text())
        
        if usbpd_options.usbpd_test:
                                                
            # If source caps list not available
            if not hasattr(self, 'usbpd_source_caps'):
                self.parent.msg_box_info(
                    title="Test Item Error!",
                    message=f"No source capabilities found. Consider getting source capabilities again",
                    message_type = MessageType.WARNING
                )
                return 
            
            usbpd_options.pdo_type:SUPPLY_TYPE = SUPPLY_TYPE.AUGMENTED
            
            # Input curent range and step checking
            if (cvcc_settings.max_current_A > PD_SPECS.USBPD_MAX_REQ_CURRENT_A):
                self.parent.msg_box_info(
                    title="Test Item Error!",
                    message=f"Entered maximum output current is higher than the maximum allowable PPS request current. Output current is set to {PD_SPECS.USBPD_MAX_REQ_CURRENT_A:g} A",
                    message_type = MessageType.WARNING
                )
                cvcc_settings.max_current_A = PD_SPECS.USBPD_MAX_REQ_CURRENT_A
                
            if (cvcc_settings.max_current_A < PD_SPECS.USBPD_MIN_REQ_CURRENT_A):
                self.parent.msg_box_info(
                    title="Test Item Error!",
                    message=f"Entered maximum output current is lower than the minimum allowable PPS request current. Output current is set to {PD_SPECS.USBPD_MIN_REQ_CURRENT_A:g} A",
                    message_type = MessageType.WARNING
                )
                cvcc_settings.max_current_A = PD_SPECS.USBPD_MIN_REQ_CURRENT_A
                           
            if cvcc_settings.multiple_setpoints:
                
                cvcc_settings.min_current_A = rounded_float(ui.lineedit_add_tests_cvcc_min_current.text())
                cvcc_settings.step_size_A = rounded_float(ui.lineedit_add_tests_cvcc_step_size.text())
            
                if (cvcc_settings.min_current_A < PD_SPECS.USBPD_MIN_REQ_CURRENT_A):
                    self.parent.msg_box_info(
                        title="Test Item Error!",
                        message=f"Entered minimum output current is lower than the minimum allowable PPS request current. Output current is set to {PD_SPECS.USBPD_MIN_REQ_CURRENT_A:g} A",
                        message_type = MessageType.WARNING
                    )
                    cvcc_settings.min_current_A = PD_SPECS.USBPD_MIN_REQ_CURRENT_A
                
                if cvcc_settings.max_current_A < cvcc_settings.min_current_A:
                    self.parent.msg_box_info(
                        title="Test Item Error!",
                        message=f"Entered maximum output current is not greater than the minimum output current",
                        message_type = MessageType.WARNING
                    )
                    return
                if cvcc_settings.step_size_A < round(PD_SPECS.USBPD_STEP_SPR_CURRENT_MA/1000,6):
                    self.parent.msg_box_info(
                        title="Test Item Error!",
                        message=f"Entered current step size is lower than the nominal current step size for USB PD. Current step size is set to {PD_SPECS.USBPD_STEP_SPR_CURRENT_MA} mA",
                        message_type = MessageType.WARNING
                    )
                    cvcc_settings.step_size_A = round(PD_SPECS.USBPD_STEP_SPR_CURRENT_MA/1000,6)    
                    
            # Get list of all source caps
            source_caps:list[SourceCap] = self.usbpd_source_caps
            pps_source_caps:list[SourceCap] = self.usbpd_pps_source_caps
            
            # If no PPS object detected    
            if len(pps_source_caps) < 1:
                self.parent.msg_box_info(
                title="Test Item Warning",
                message=f"No PPS object detected. Consider requesting the source capabilities again",
                message_type = MessageType.WARNING
                )
                return
            source_cap_index_V = -1
            # Check capability of each PPS object
            for source_cap_pps in pps_source_caps:
                if (cvcc_settings.nom_vout_V >= round(source_cap_pps.min_voltage_mV/1000,3)) and (cvcc_settings.nom_vout_V <= round(source_cap_pps.max_voltage_mV/1000,3)):
                    source_cap_index_V = source_caps.index(source_cap_pps)

            # If not supported by any PPS object
            if source_cap_index_V == -1:
                self.parent.msg_box_info(
                title="Test Item Warning",
                message=f"Nominal Voltage Settings not supported by any PPS object",
                message_type = MessageType.WARNING
                )
                return    
            
            usbpd_options.augmented_type = AUGMENTED_TYPE.SPR_PPS
            max_load_current_A = round(source_caps[source_cap_index_V].max_current_mA/1000,6)
        else:
            max_load_current_A = cvcc_settings.max_current_A
                    
        cvcc_settings.process_inputs()
                
        # Timing Settings
        soak_time = self.get_timing_params_from_ui()

        # Loop through the setpoints and create a test for each
        for iout in cvcc_settings.iout_setpoints:
            
            # Prepare the test conditions object
            test_conditions = TestConditions(
            nominal_output_voltage_V = cvcc_settings.nom_vout_V,
            nominal_load_current_A = iout,
            max_load_current_A = max_load_current_A,
            line_range = line_range,    
            load_range = load_range_pct,
            soak_time = soak_time,
            usbpd_options = usbpd_options,
            general_options = general_options,
            cvcc_settings = cvcc_settings,
            name=TestTypes[test_type_index].title
            )

            # Create a test object for the iout setpoint
            new_test_item = TestItem(parent = self.parent,
            test_type_index = test_type_index,
            test_conditions = test_conditions)

            # Add the new test item to the test plan 
            self.test_plan.add_test_item(new_test_item)
        
        # Update the test list after processing all set points
        self.update_test_list_details()
        
    def add_no_load_power_test(self):

        test_type_index = self.test_type_index

        # Test Condition Ranges
        line_range:LineRange = self.selected_line_range
        # Add a dummy load range
        load_range = LoadRange(name="dummy", load_range_pct=[])

        # Timing Settings
        soak_time = self.get_timing_params_from_ui()
        
        # General options
        general_options = self.get_general_options_from_ui()
        

        # Prepare the test conditions object
        test_conditions = TestConditions(
        nominal_output_voltage_V = 0,
        nominal_load_current_A = 0,
        max_load_current_A = 0,
        line_range = line_range,    
        load_range = load_range,
        soak_time = soak_time,
        general_options = general_options,
        name=TestTypes[test_type_index].title
        )

        # Create a test object for the iout setpoint
        new_test_item = TestItem(parent = self.parent,
        test_type_index = test_type_index,
        test_conditions = test_conditions)

        # Add the new test item to the test plan 
        self.test_plan.add_test_item(new_test_item)
    
        # Update the test list after processing all set points
        self.update_test_list_details()   

    def test_single_pdo(self):
        # TODO: Merge with multiple test request, need parameter
        
        # Check first if inputs are valid     
        
        if not hasattr(self, 'usbpd_source_caps'):
            self.parent.msg_box_info(
                title="Test Item Error!",
                message=f"No source capabilities found. Consider requesting the source capabilities again",
                message_type = MessageType.WARNING
            )
            return

        source_caps:list[SourceCap] = self.usbpd_source_caps

        # Create TestItem object
 
        test_type_index = self.test_type_index
        
        # Get the index of the selected PDO
        # Do not proceed if nothing is selected
        
        selection_index = self.ui.table_add_tests_source_caps.currentRow()
    
        if (selection_index == -1):
            self.parent.msg_box_info(
                title="Test Item Error!",
                message=f"Please choose a supported Power Delivery Object (PDO)",
                message_type = MessageType.WARNING
            )
            return
        if (selection_index >= len(source_caps)):
            self.parent.msg_box_info(
                title="Test Item Error!",
                message=f"Selected Power Delivery Object (PDO) is not in the Source Capabilities",
                message_type = MessageType.WARNING
            )
            return
        supply_type = source_caps[selection_index].supply_type
                
        # If selected object is APDO
        if supply_type == SUPPLY_TYPE.AUGMENTED:
            if (self.ui.lineedit_add_tests_nominal_output_voltage.text() == '') and \
                (self.ui.lineedit_add_tests_nominal_output_current.text() == ''):
                return
            
            # Check if nominal voltage and nominal curent values are valid
            
            if (self.ui.lineedit_add_tests_nominal_output_voltage.text() == '') and \
                (not self.ui.lineedit_add_tests_nominal_output_current.text() == ''):
                self.parent.msg_box_info(
                    title = "Input Error!",
                    message=f"Please type in the nominal output voltage",
                    message_type = MessageType.INFO
                )
                return
            
            if (not self.ui.lineedit_add_tests_nominal_output_voltage.text() == '') and \
                (self.ui.lineedit_add_tests_nominal_output_current.text() == ''):
                self.parent.msg_box_info(
                    title = "Input Error!",
                    message=f"Please type in the nominal output current",
                    message_type = MessageType.INFO
                )
                return
            
            source_cap:SourceCap = source_caps[selection_index]
            nominal_output_voltage_V = rounded_float(self.ui.lineedit_add_tests_nominal_output_voltage.text())
            
            # Check if nominal voltage is within the APDO voltage specs
            
            if nominal_output_voltage_V < round(source_cap.min_voltage_mV / 1000,3):
                self.parent.msg_box_info(
                    title = "Input Error!",
                    message = f"Entered voltage is higher than the maximum allowable voltage request of the APDO. Output voltage is set to {round(source_cap.min_voltage_mV / 1000,3):g} V",
                    message_type = MessageType.INFO
                )
                nominal_output_voltage_V = round(source_cap.min_voltage_mV / 1000,3)
                
            elif nominal_output_voltage_V > round(source_cap.max_voltage_mV / 1000,3):
                self.parent.msg_box_info(
                    title = "Input Error!",
                    message = f"Entered voltage is lower than the minimum allowable voltage request of the APDO. Output voltage is set to {round(source_cap.max_voltage_mV / 1000,3):g} V",
                    message_type = MessageType.INFO
                )
                nominal_output_voltage_V = round(source_cap.max_voltage_mV / 1000,3)
                
            nominal_load_current_A = rounded_float(self.ui.lineedit_add_tests_nominal_output_current.text())
                
            # Check if nominal current is supported by object
            
            if nominal_load_current_A > round(source_cap.max_current_mA/1000,6):
                self.parent.msg_box_info(
                title="Test Item Error!",
                message=f"Entered nominal output current is higher than the maximum allowable current request of the APDO. Output current is set to {round(source_cap.max_current_mA / 1000,6)} A",
                message_type = MessageType.WARNING
            )
                nominal_load_current_A = round(source_cap.max_current_mA/1000,6)
            
            elif nominal_load_current_A < PD_SPECS.USBPD_MIN_REQ_CURRENT_A:
                self.parent.msg_box_info(
                title="Test Item Error!",
                message=f"Entered nominal output current is lower than the minimum allowable current request of the APDO. Output current is set to {PD_SPECS.USBPD_MIN_REQ_CURRENT_A} A",
                message_type = MessageType.WARNING
            )
                nominal_load_current_A = PD_SPECS.USBPD_MIN_REQ_CURRENT_A
        
        # If selected object is Fixed PDO
        elif supply_type == SUPPLY_TYPE.FIXED:
            source_cap:SourceCap = source_caps[selection_index]
            nominal_output_voltage_V =source_cap.voltage_mV/1000
            
            # Nominal output parameters
            if not self.ui.lineedit_add_tests_nominal_output_current.text() == '':
                if rounded_float(self.ui.lineedit_add_tests_nominal_output_current.text()) > round(source_cap.max_current_mA/1000,6):
                    self.parent.msg_box_info(
                        title="Test Item Error!",
                        message=f"Entered nominal output current exceeds the rated source capability. Output current is set to {round(source_cap.max_current_mA/1000,6):g} A",
                        message_type = MessageType.WARNING
                    )
                    nominal_load_current_A = round(source_cap.max_current_mA/1000,6)
                else:
                    nominal_load_current_A = rounded_float(self.ui.lineedit_add_tests_nominal_output_current.text())
            else:
                nominal_load_current_A = round(source_cap.max_current_mA/1000,6)
                
        # If not FPDO or APDO
        else:
            self.parent.msg_box_info(
                title = "Input Error!",
                message = f"Selected object is not a Fixed PDO or an Augmented PDO",
                message_type = MessageType.WARNING
            )
            return
        
        # Get the source cap to add
        source_cap = source_caps[selection_index]
        
        # USBPD Options
        usbpd_options = self.get_usbpd_options_from_ui(source_cap)

        # General Options
        general_options = self.get_general_options_from_ui()

        # Test Condition Ranges
        load_range_pct= LoadRange(name = self.selected_load_range.name,load_range_pct= copy(self.selected_load_range.load_range_pct))
        
        line_range= LineRange(name = self.selected_line_range.name, vin_freq = copy(self.selected_line_range.vin_freq))

        # Timing Settings
        soak_time = self.get_timing_params_from_ui()
        
        max_load_current_A = nominal_load_current_A
        
        # Add a TestItem object to the TestList for each fixed PDO
        # Reverse the order of the source caps to be added 
        # so that the first to be tested is the highest load
        
        if TestTypes[test_type_index].title == InputLineRampTest.title:
        
            # Check coupling toggle switch (Enabled for DC)
            if self.ui.widget_toggle_add_tests_line_ramp_coupling.isChecked():
                coupling = 'DC'
                freq = 0
            else:
                coupling = 'AC'
                if (self.ui.lineedit_add_tests_line_ramp_frequency.text() == ''):
                    self.parent.msg_box_info(
                        title = "Input Error!",
                        message = "Please enter the expected line frequency",
                        message_type = MessageType.INFO
                        )
                    return
                else:
                    freq = rounded_float(self.ui.lineedit_add_tests_line_ramp_frequency.text())    
                            
            line_ramp_settings = LineRamp(
                name = copy(self.selected_line_ramp.name),
                vin_slew = copy(self.selected_line_ramp.vin_slew),
                coupling = coupling,
                freq = freq,
                custom = copy(self.selected_line_ramp.custom)         
            )
            
            test_conditions = TestConditions(
                nominal_output_voltage_V = nominal_output_voltage_V,
                nominal_load_current_A = nominal_load_current_A,
                max_load_current_A = max_load_current_A,
                line_range = line_range,
                load_range = load_range_pct,
                soak_time = soak_time,
                general_options = general_options,
                usbpd_options = usbpd_options,
                line_ramp_settings = line_ramp_settings,
                name=TestTypes[test_type_index].title
            )
            
        else:
            i2c_test_parameters = self.get_i2c_parameters_from_ui() if hasattr(TestTypes[test_type_index], 'i2c_ui_definitions') else I2CTestParameters()
            test_conditions = TestConditions(
                nominal_output_voltage_V = nominal_output_voltage_V,
                nominal_load_current_A = nominal_load_current_A,
                max_load_current_A = max_load_current_A,
                line_range = line_range,
                load_range = load_range_pct,
                soak_time = soak_time,
                general_options = general_options,
                usbpd_options = usbpd_options,
                i2c_test_parameters = i2c_test_parameters,
                name=TestTypes[test_type_index].title
            )
        
        new_test_item = TestItem(parent = self.parent,
            test_type_index = test_type_index,
            test_conditions = test_conditions)
        
        self.ui.table_add_tests_source_caps.clearSelection()
        # Add the new test item to the test plan 
        self.test_plan.add_test_item(new_test_item)
        

        self.update_test_list_details()
        

        
    def test_non_pdo(self):
        # Check first if inputs are valid
        # Input the nominal output voltage and current
        
        if (self.ui.lineedit_add_tests_nominal_output_voltage.text() == '') and \
            (self.ui.lineedit_add_tests_nominal_output_current.text() == ''):
            self.parent.msg_box_info(
                title = "Input Error!",
                message=f"Please type in the nominal output voltage and current",
                message_type = MessageType.INFO
            )
            return
        
        if (self.ui.lineedit_add_tests_nominal_output_voltage.text() == '') and \
            (not self.ui.lineedit_add_tests_nominal_output_current.text() == ''):
            self.parent.msg_box_info(
                title = "Input Error!",
                message=f"Please type in the nominal output voltage",
                message_type = MessageType.INFO
            )
            return
        
        if (not self.ui.lineedit_add_tests_nominal_output_voltage.text() == '') and \
            (self.ui.lineedit_add_tests_nominal_output_current.text() == ''):
            self.parent.msg_box_info(
                title = "Input Error!",
                message=f"Please type in the nominal output current",
                message_type = MessageType.INFO
            )
            return
        
        
        if (not is_numeric(self.ui.lineedit_add_tests_nominal_output_voltage.text())) or \
            (not is_numeric(self.ui.lineedit_add_tests_nominal_output_current.text())):
            self.parent.msg_box_info(
                title = "Input Error!",
                message = "Please enter numeric inputs.",
                message_type = MessageType.INFO
            )
            return
        
        # Test Type

        # TODO: Sanitize inputs or set up error handling
        # Take the inputs from the ui
 
        test_type_index = self.test_type_index
        
        # General Options
        general_options = self.get_general_options_from_ui()

        # Test Condition Ranges
        load_range_pct= LoadRange(name = self.selected_load_range.name,load_range_pct= copy(self.selected_load_range.load_range_pct))
        
        line_range= LineRange(name = self.selected_line_range.name, vin_freq = copy(self.selected_line_range.vin_freq))

        # Timing Settings
        soak_time = self.get_timing_params_from_ui()
        
        
        # Nominal output parameters
        nominal_output_voltage_V = rounded_float(self.ui.lineedit_add_tests_nominal_output_voltage.text())
        nominal_load_current_A = rounded_float(self.ui.lineedit_add_tests_nominal_output_current.text())
        
        match TestTypes[test_type_index].title:
            case InputLineRampTest.title:
                # Check coupling toggle switch (Enabled for DC)
                if self.ui.widget_toggle_add_tests_line_ramp_coupling.isChecked():
                    coupling = 'DC'
                    freq = 0
                else:
                    coupling = 'AC'
                    if (self.ui.lineedit_add_tests_line_ramp_frequency.text() == ''):
                        self.parent.msg_box_info(
                            title = "Input Error!",
                            message = "Please enter the expected line frequency",
                            message_type = MessageType.INFO
                            )
                        return
                    else:
                        freq = rounded_float(self.ui.lineedit_add_tests_line_ramp_frequency.text())    
                                
                line_ramp_settings = LineRamp(
                    name = copy(self.selected_line_ramp.name),
                    vin_slew = copy(self.selected_line_ramp.vin_slew),
                    coupling = coupling,
                    freq = freq,
                    custom = copy(self.selected_line_ramp.custom)         
                )
                
                test_conditions = TestConditions(
                    nominal_output_voltage_V = nominal_output_voltage_V,
                    nominal_load_current_A = nominal_load_current_A,
                    max_load_current_A = nominal_load_current_A,
                    line_range = line_range,
                    load_range = load_range_pct,
                    soak_time = soak_time,
                    general_options = general_options,
                    line_ramp_settings = line_ramp_settings,
                    name=TestTypes[test_type_index].title
                )
        
            case _:
                i2c_test_parameters = self.get_i2c_parameters_from_ui() if hasattr(TestTypes[test_type_index], 'i2c_ui_definitions') else I2CTestParameters()
                test_conditions = TestConditions(
                    nominal_output_voltage_V = nominal_output_voltage_V,
                    nominal_load_current_A = nominal_load_current_A,
                    max_load_current_A = nominal_load_current_A,
                    line_range = line_range,
                    load_range = load_range_pct,
                    soak_time = soak_time,
                    general_options = general_options,
                    i2c_test_parameters = i2c_test_parameters,
                    name=TestTypes[test_type_index].title
                )
        
        new_test_item = TestItem(parent = self.parent,
            test_type_index = test_type_index,
            test_conditions = test_conditions)

        # Add the new test item to the test plan 
        self.test_plan.add_test_item(new_test_item)
        

        self.update_test_list_details()

        
    def add_i2c_test(self):

        ui:Ui_MainWindow = self.ui

        test_type_index = self.test_type_index
        try:
            # Test Condition Ranges
            line_range = LineRange(
                name = self.selected_line_range.name,
                vin_freq = copy(self.selected_line_range.vin_freq))
            
             # Test Condition Ranges
            load_range_pct= LoadRange(
                name = self.selected_load_range.name,
                load_range_pct= copy(self.selected_load_range.load_range_pct))

            i2c_test_parameters = self.get_i2c_parameters_from_ui()

            soak_time = self.get_timing_params_from_ui()
            
            general_options = self.get_general_options_from_ui()
            
        except InputError as e:
            print(e)
        
        if TestTypes[test_type_index] in CVCC_TestTypes:
            if not self.process_cvcc_inputs():
                return

            # CVCC Test Settings
            cvcc_settings = CVCCSettings()
            
            cvcc_settings.multiple_setpoints = ui.chkbox_add_tests_cvcc_multi_setpoints.checkState()
            
            cvcc_settings.nom_vout_V = rounded_float(ui.lineedit_add_tests_cvcc_nom_voltage.text())
            cvcc_settings.max_current_A = rounded_float(ui.lineedit_add_tests_cvcc_max_current.text())
            if cvcc_settings.multiple_setpoints:
            
                cvcc_settings.min_current_A = rounded_float(ui.lineedit_add_tests_cvcc_min_current.text())
                cvcc_settings.step_size_A = rounded_float(ui.lineedit_add_tests_cvcc_step_size.text())
            
            cvcc_settings.process_inputs()
            
             # Loop through the setpoints and create a test for each
            for iout in cvcc_settings.iout_setpoints:
                
                # Prepare the test conditions object
                test_conditions = TestConditions(
                nominal_output_voltage_V = cvcc_settings.nom_vout_V,
                nominal_load_current_A = iout,
                max_load_current_A = cvcc_settings.max_current_A,
                line_range = line_range,    
                load_range = load_range_pct,
                soak_time = soak_time,
                general_options = general_options,
                cvcc_settings = cvcc_settings,
                i2c_test_parameters = i2c_test_parameters,
                name=TestTypes[test_type_index].title
                )

                # Create a test object for the iout setpoint
                new_test_item = TestItem(parent = self.parent,
                test_type_index = test_type_index,
                test_conditions = test_conditions)

                # Add the new test item to the test plan 
                self.test_plan.add_test_item(new_test_item)
        else:
            test_conditions = TestConditions(
            nominal_output_voltage_V = 5,
            nominal_load_current_A = 5,
            max_load_current_A = 5,
            line_range = line_range,
            load_range = load_range_pct,
            soak_time = soak_time,
            general_options = general_options,
            i2c_test_parameters = i2c_test_parameters,
            name=TestTypes[test_type_index].title,
            )

            # Create a test object for the iout setpoint
            new_test_item = TestItem(parent = self.parent,
            test_type_index = test_type_index,
            test_conditions = test_conditions)

            # Add the new test item to the test plan 
            self.test_plan.add_test_item(new_test_item)
        
        # Update the test list after processing all set points
        self.update_test_list_details()

    def test_all_fixed_pdos(self):
        """
        Take all of the Fixed Supply PDOs and add them to the test list
        with the PDO voltage and max current parameters used for the
        nominal voltage and current setting


        """
        # Check first if inputs are valid
        if (not is_numeric(self.ui.lineedit_add_tests_nominal_output_current.text())) and \
            (not self.ui.lineedit_add_tests_nominal_output_current.text() == ''):
            self.parent.msg_box_info(
                title = "Input Error!",
                message = "Please enter numeric inputs.",
                message_type = MessageType.INFO
            )
            return
        
        if not hasattr(self, 'usbpd_fixed_source_caps'):
            self.parent.msg_box_info(
                title="Test Item Error!",
                message=f"No fixed source capabilities found. Consider requesting the source capabilities again",
                message_type = MessageType.WARNING
            )
            return
        

        fixed_source_caps = self.usbpd_sink.fs_list

        # Create TestItem object from fixed PDO
        # Input the voltage list, current list,
        # Test Type

        # TODO: Sanitize inputs or set up error handling
        # Take the inputs from the ui
 
        test_type_index = self.test_type_index

        # USBPD Options
        usbpd_options = self.get_usbpd_options_from_ui()

        # General Options
        general_options = self.get_general_options_from_ui()

        # Test Condition Ranges
        load_range_pct= LoadRange(name = self.selected_load_range.name,load_range_pct= copy(self.selected_load_range.load_range_pct))
        
        line_range= LineRange(name = self.selected_line_range.name, vin_freq = copy(self.selected_line_range.vin_freq))

        # Timing Settings
        soak_time = self.get_timing_params_from_ui()
        
        # Add a TestItem object to the TestList for each fixed PDO
        # Reverse the order of the source caps to be added 
        # so that the first to be tested is the highest load
        source_caps_to_add = reversed(fixed_source_caps)
        
        for source_cap in source_caps_to_add:
            source_cap:SourceCap = source_cap
            
            usbpd_options.pdo_type:SUPPLY_TYPE = \
            source_cap.supply_type
            
            # Nominal output parameters
            nominal_output_voltage_V =source_cap.voltage_mV/1000
            if not self.ui.lineedit_add_tests_nominal_output_current.text() == '':
                if rounded_float(self.ui.lineedit_add_tests_nominal_output_current.text()) > round(source_cap.max_current_mA/1000,6):
                    self.parent.msg_box_info(
                        title="Test Item Error!",
                        message=f"Entered nominal output current exceeds the rated source capability. Output current is set to {round(source_cap.max_current_mA/1000,6):g} A",
                        message_type = MessageType.WARNING
                    )
                    nominal_load_current_A = round(source_cap.max_current_mA/1000,6)
                else:
                    nominal_load_current_A = rounded_float(self.ui.lineedit_add_tests_nominal_output_current.text())
            else:
                nominal_load_current_A = round(source_cap.max_current_mA/1000,6)
            
            match TestTypes[test_type_index].title:
                case InputLineRampTest.title:    
                    # Check coupling toggle switch (Enabled for DC)
                    if self.ui.widget_toggle_add_tests_line_ramp_coupling.isChecked():
                        coupling = 'DC'
                        freq = 0
                    else:
                        coupling = 'AC'
                        if (self.ui.lineedit_add_tests_line_ramp_frequency.text() == ''):
                            self.parent.msg_box_info(
                                title = "Input Error!",
                                message = "Please enter the expected line frequency",
                                message_type = MessageType.INFO
                                )
                            return
                        else:
                            freq = rounded_float(self.ui.lineedit_add_tests_line_ramp_frequency.text())    
                                    
                    line_ramp_settings = LineRamp(
                        name = copy(self.selected_line_ramp.name),
                        vin_slew = copy(self.selected_line_ramp.vin_slew),
                        coupling = coupling,
                        freq = freq,
                        custom = copy(self.selected_line_ramp.custom)         
                    )
                    
                    test_conditions = TestConditions(
                        nominal_output_voltage_V = nominal_output_voltage_V,
                        nominal_load_current_A = nominal_load_current_A,
                        max_load_current_A = round(source_cap.max_current_mA/1000,6),
                        line_range = line_range,
                        load_range = load_range_pct,
                        soak_time = soak_time,
                        general_options = general_options,
                        usbpd_options = usbpd_options,
                        line_ramp_settings = line_ramp_settings,
                        name=TestTypes[test_type_index].title
                    )

                case _:
                    test_conditions = TestConditions(
                        nominal_output_voltage_V = nominal_output_voltage_V,
                        nominal_load_current_A = nominal_load_current_A,
                        max_load_current_A = round(source_cap.max_current_mA/1000,6),
                        line_range = line_range,
                        load_range = load_range_pct,
                        soak_time = soak_time,
                        general_options = general_options,
                        usbpd_options = usbpd_options,
                        name=TestTypes[test_type_index].title
                    )

            new_test_item = TestItem(parent = self.parent,
                test_type_index = test_type_index,
                test_conditions = test_conditions)

            # Add the new test item to the test plan 
            self.test_plan.add_test_item(new_test_item)
        

        self.update_test_list_details()

    def get_selected_pdo_index(self):
        return self.ui.table_add_tests_source_caps.currentRow()
  
    def update_test_list_details(self):
        """Takes information from the TestPlan and 
        updates the details of the test list"""

        # Get the selected row before clearing the table
        # Clear the contents of the test list table

        # Use the test plan
        test_plan = self.test_plan

        for test_item_index,test_item in enumerate(test_plan.test_items):
            # Add a row to the table for the current item
            current_row_count = self.ui.table_add_tests_test_list.rowCount()
            if current_row_count <= test_item_index:
                self.ui.table_add_tests_test_list\
                    .setRowCount(current_row_count+1)

            # Get the details text from the test object
            test_object = test_item.test_object
            test_object.update_test_list_text()
            details_text = test_item.test_object.test_list_text

            # Add the details to the table
            self.ui.table_add_tests_test_list.setItem(
                test_item_index, 0, 
                QtWidgets.QTableWidgetItem(str(test_item_index+1)))
            self.ui.table_add_tests_test_list.setItem(
                test_item_index, 1, 
                QtWidgets.QTableWidgetItem(details_text))
        
        if self.ui.table_add_tests_test_list.rowCount() > len(test_plan.test_items):
            self.ui.table_add_tests_test_list.setRowCount(len(test_plan.test_items))
        
        # Backup test list to a .json file each time the test list is updated
        
        if len(self.test_plan.test_items) == 0:
            return
        
        obj_list = []
        for test_item in self.test_plan.test_items:
            d = test_item.get_dict()
            obj_list.append(d)
        
        # Backup test list to a .json file each time the test list is updated
        with open(configs.test_items_filepath, 'w') as test_list_file:
            json.dump(obj_list, test_list_file, indent=2)
        

    # TODO: Overwrite for waveforms
    def run_tests(self):
        """ Process the necessary requirements then start the timer
        which will update the test plan in a loop
        """
        # Disable the RUN button
        self.ui.btn_add_tests_run.setEnabled(False)

        # Do logical checks first
        if self.usbpd_sink is not None:
            if self.usbpd_sink.open_status:
                self.usbpd_sink.close()

        # Get output folder path
        self.output_folder_path = self.get_output_folder_path()
        self.test_plan.output_folder_path = self.output_folder_path
        self.test_plan.status = TestStatus.IN_QUEUE
        # Start the timer which will do the test plan update for running test
        self.test_plan_update_timer.start(TEST_PLAN_UPDATE_TIMER)

        # Select the results folder for the current run
        self.select_current_run_results_folder()

    def get_output_folder_path(self):
        
        if not self.ui.chkbox_add_tests_results_folder.checkState():
            
            self.folder_name = self.test_plan.generate_output_folder_name()

        else:
            self.folder_name = self.ui.cbx_add_tests_results_folder.currentText()

        path = f'{self.parent_folder_path}/{self.folder_name}'

        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def setup_testplan_update_timer(self):
        """Setup the timer that will run the update loop for both the
        test list ui and TestPlan."""
        self.test_plan_update_timer = QTimer(self.parent)
        self.test_plan_update_timer.timeout.connect(self.test_plan_update_service)
    
    def test_plan_update_service(self):
        global test_control_flags
        """Process the test loop for the test plan and update the UI 
        while test is running."""
        
        # Dug out from inside the method to prevent garbage collection
        # from deleting the thread

        test_plan = self.test_plan
        test_plan.update_status()

        # Stop the timer if the tests are stopped
        if test_plan.status == TestStatus.STOPPED:
            self.test_plan_update_timer.stop()
            
            
        # If the TestPlan is in Queue, run the first TestItem that is in Queue
        elif test_plan.status == TestStatus.IN_QUEUE:
            for test_item_index, test_item in enumerate(test_plan.test_items):
                if test_item.status == TestStatus.IN_QUEUE:

                    # Global flag for stopping test accessible by worker thread
                    test_control_flags['StopTest'] = False
                    test_control_flags['SkipTest'] = False
                    self.test_routine_thread = QThread()
                    self.test_routine_thread.finished.connect(self.test_routine_thread_cleanup)
                    test_item.test_routine_thread = self.test_routine_thread

                    # Bind thread to parent to prevent it from expiring unexpectedly
                    self.parent.test_routine_thread = self.test_routine_thread 

                    # Regenerate test object to disconnect the worker from thread
                    test_item.generate_test_object()

                    test_object = test_item.test_object
                    test_object.output_folder_path = self.output_folder_path
                    test_item.run()
                    self.ui.table_add_tests_test_list.setCurrentIndex(self.ui.table_add_tests_test_list.model().index(test_item_index,0))
                    break  
            
        elif test_plan.status == TestStatus.COMPLETE:
            # If the tests have completed, stop the update timer
            self.test_routine_thread = None
            self.parent.test_routine_thread = None
            self.test_plan_update_timer.stop()
            self.update_test_list_control_buttons_state()
            self.parent.msg_box_info('Test Info','Test Complete',MessageType.INFO)
            

        for test_item in test_plan.test_items:
            if test_item.test_object.status == TestStatus.IN_PROGRESS:
                if test_item.test_object.estimated_time_s >= 0.2:
                    test_item.test_object.estimated_time_s -= 0.2
                else:
                    test_item.test_object.estimated_time_s = 0


        # Update the test list on each run of this loop
        self.update_test_list_details()
        
        self.update_test_list_control_buttons_state()


#####################################################################|######|
#       Test List Control Buttons
#####################################################################|######|

    # Save test list to a .json file
    def save_test_plan(self):
        """"Save the test list to a .json file"""
        username = os.getlogin()
        default_path = self.parent_folder_path

        # Create dialog window for file selection
        dialog = QtWidgets.QFileDialog()
        default_filename = 'ATE_test_plan'
        test_plan_save_path, path_file_type = dialog.getSaveFileName(
             self.parent, "Save Test Plan Data", f'{default_path}\{default_filename}.json', "JSON Source File (*.json)")
        
        # Handling of file input
        if test_plan_save_path == '':
            return
        if not ((test_plan_save_path.split('.'))[-1]).lower() == 'json':
            test_plan_save_path = test_plan_save_path + '.json'
        obj_list = []
        for test_item in self.test_plan.test_items:
            d = test_item.get_dict()
            obj_list.append(d)
        
        with open(test_plan_save_path, 'w') as test_list_file:
            json.dump(obj_list, test_list_file, indent=2)
    
    # Load test list from a .json file    
    def load_test_plan(self):
        """"Load the test list from a .json file"""
        username = os.getlogin()
        default_path = self.parent_folder_path

        # Create dialog window for file selection
        dialog = QtWidgets.QFileDialog()
        test_plan_load_path, path_file_type = dialog.getOpenFileName(
            self.parent, 'Select Test Plan', default_path, "JSON Source File (*.json)")

        # Handling of file input
        if test_plan_load_path == '':
            return
        while not ((test_plan_load_path.split('.'))[-1]).lower() == 'json':
            self.parent.msg_box_info(
                title="Load Test Plan",
                message=f"Incorrect file type. File type must be "".json""",
                message_type = MessageType.WARNING
                )
            default_path = test_plan_load_path.replace(test_plan_load_path.split('\\')[-1],'')
            test_plan_load_path, path_file_type = dialog.getOpenFileName(
                self.parent, 'Select Test Plan', default_path, "JSON Source File (*.json)")
            if test_plan_load_path == '':
                return

        with open(test_plan_load_path, "r") as test_list_file:
            test_item_list = json.load(test_list_file)
        
        # Go through each test item
        for test_item in test_item_list:
            self.test_plan.add_dict_to_test_plan(test_item)
        self.update_test_list_details()
        
    # Move up selected test item
    def move_up_selected_test(self):
        """Move up selected test in the queue"""
        selection_index = self.ui.table_add_tests_test_list.currentRow()

        if selection_index == -1 or selection_index == 0:
            return
        
        if self.test_plan.status == TestStatus.IN_PROGRESS:
            if not self.test_plan.test_items[selection_index].status == TestStatus.IN_QUEUE:
                return  
        
        new_test_item:TestItem = self.test_plan.test_items[selection_index]
        self.test_plan.test_items.pop(selection_index)
        self.test_plan.test_items.insert(selection_index-1,new_test_item)
        
        self.ui.table_add_tests_test_list.setCurrentIndex(self.ui.table_add_tests_test_list.model().index(selection_index-1,0))
        self.test_item_selection_item_changed_flag = True
        self.update_test_list_details()
        
        
    # Move down selected test item
    def move_down_selected_test(self):
        """Move up selected test in the queue"""
        selection_index = self.ui.table_add_tests_test_list.currentRow()

        if selection_index == -1 or selection_index == len(self.test_plan.test_items)-1:
            return
        
        if self.test_plan.status == TestStatus.IN_PROGRESS:
            
            if not self.test_plan.test_items[selection_index].status == TestStatus.IN_QUEUE:
                return
        
        new_test_item:TestItem = self.test_plan.test_items[selection_index]
        self.test_plan.test_items.pop(selection_index)
        self.test_plan.test_items.insert(selection_index+1,new_test_item)
        
        self.ui.table_add_tests_test_list.setCurrentIndex(self.ui.table_add_tests_test_list.model().index(selection_index+1,0))
        self.test_item_selection_item_changed_flag = True
        self.update_test_list_details()
    
    # Move selected test item to top
    def move_top_selected_test(self):
        """Move up selected test in the queue"""
        selection_index = self.ui.table_add_tests_test_list.currentRow()

        if selection_index == -1 or selection_index == 0:
            return
        
        top_index = 0
        
        if self.test_plan.status == TestStatus.IN_PROGRESS:
            
            if not self.test_plan.test_items[selection_index].status == TestStatus.IN_QUEUE:
                return            
        
        new_test_item:TestItem = self.test_plan.test_items[selection_index]
        self.test_plan.test_items.pop(selection_index)
        self.test_plan.test_items.insert(top_index,new_test_item)
        
        self.ui.table_add_tests_test_list.setCurrentIndex(self.ui.table_add_tests_test_list.model().index(top_index,0))
        self.test_item_selection_item_changed_flag = True
        self.update_test_list_details()
    
    # Move selected test item to bottom    
    def move_bottom_selected_test(self):
        """Move up selected test in the queue"""
        selection_index = self.ui.table_add_tests_test_list.currentRow()

        if selection_index == -1 or selection_index == len(self.test_plan.test_items) - 1:
            return
        
        bottom_index = len(self.test_plan.test_items) - 1
        
        if self.test_plan.status == TestStatus.IN_PROGRESS:
            
            if not self.test_plan.test_items[selection_index].status == TestStatus.IN_QUEUE:
                return
        new_test_item:TestItem = self.test_plan.test_items[selection_index]
        self.test_plan.test_items.pop(selection_index)
        self.test_plan.test_items.append(new_test_item)
        
        self.ui.table_add_tests_test_list.setCurrentIndex(self.ui.table_add_tests_test_list.model().index(bottom_index,0))
        self.test_item_selection_item_changed_flag = True
        self.update_test_list_details()

    # Restart Selected Test
    def restart_selected_test(self):
        selection_index = self.ui.table_add_tests_test_list.currentRow()

        if selection_index == -1:
            return
        
        if self.test_plan.test_items[selection_index].status == TestStatus.IN_PROGRESS:
            return
        
        self.test_plan.test_items[selection_index].status = TestStatus.IN_QUEUE
        self.test_plan.test_items[selection_index].test_object.status = TestStatus.IN_QUEUE
        self.test_plan.test_items[selection_index].test_object.estimated_time_s = self.test_plan.test_items[selection_index].test_object.total_time

        self.update_test_list_details()
        self.update_test_list_control_buttons_state()
           
    # Update Selected Test
    def update_selected_test(self):
        selection_index = self.ui.table_add_tests_test_list.currentRow()

        if selection_index == -1:
            return
        
        test_item = self.test_plan.test_items[selection_index]
        if test_item.status == TestStatus.IN_PROGRESS:
            return
        original_test_list_length = len(self.test_plan.test_items)
        
        if self.ui.chkbox_add_tests_cvcc_multi_setpoints.isChecked():
            self.ui.chkbox_add_tests_cvcc_multi_setpoints.setChecked(False)
        
        if test_item.test_object.i2c_test:
            self.add_i2c_test()
        else:
            self.add_single_test()
        
        # If test list length stayed the same, no new test is added
        if len(self.test_plan.test_items) == original_test_list_length:
            return
        
        new_test_item:TestItem = self.test_plan.test_items[original_test_list_length]
        self.test_plan.test_items.pop(original_test_list_length)
        self.test_plan.test_items.pop(selection_index)
        self.test_plan.test_items.insert(selection_index,new_test_item)
        
        
        self.ui.table_add_tests_test_list.setCurrentIndex(self.ui.table_add_tests_test_list.model().index(selection_index,0))
        self.update_test_list_details()
        self.update_test_list_control_buttons_state()
    
    # Remove selected test item
    def remove_test(self):
        """Removes the selected test from the test plan."""
        selection_index = self.ui.table_add_tests_test_list.currentRow()

        if selection_index == -1:
            return
        
        if self.test_plan.test_items[selection_index].status == TestStatus.IN_PROGRESS:
            return
        current_len = len(self.test_plan.test_items)
        self.test_plan.test_items.pop(selection_index)
        if selection_index < current_len - 1:
            self.test_item_selection_item_changed_flag = True
        else:
            self.test_item_selection_changed_flag = True
        self.update_test_list_details()
        self.update_test_list_control_buttons_state()
        
        
    # Skip Selected Test
    def skip_selected_test(self):
        
        global test_control_flags
        
        selection_index = self.ui.table_add_tests_test_list.currentRow()

        if selection_index == -1:
            return
        
        if self.test_plan.test_items[selection_index].status in [TestStatus.IN_QUEUE]:
            self.test_plan.test_items[selection_index].status = TestStatus.SKIPPED
            self.test_plan.test_items[selection_index].test_object.status = TestStatus.SKIPPED                
            
        elif (self.test_plan.status in [TestStatus.IN_QUEUE, TestStatus.IN_PROGRESS]) and (self.test_plan.test_items[selection_index].status == TestStatus.IN_PROGRESS):
            test_control_flags['SkipTest'] = True
            self.test_plan_update_timer.stop()
            self.test_plan.test_items[selection_index].update_object_status(TestStatus.SKIPPED)
                
            self.test_plan.status = TestStatus.SKIPPED
            QTimer.singleShot(1000,self.test_plan_update_timer.start(TEST_PLAN_UPDATE_TIMER))        
            
        self.update_test_list_details()
        if selection_index < len( self.test_plan.test_items) - 1:  
            self.ui.table_add_tests_test_list.setCurrentIndex(self.ui.table_add_tests_test_list.model().index(selection_index+1,0))
        else: 
            self.update_test_list_control_buttons_state()
        
    
    def clear_test(self):
        """Removes all the test items from the test plan."""
        
        if self.test_plan.status == TestStatus.IN_PROGRESS:
            # Remove test item prior to item in progress
            while not self.test_plan.test_items[0].status == TestStatus.IN_PROGRESS:
                self.test_plan.test_items.pop(0)
                if len(self.test_plan.test_items) == 0:
                    break
                
            # Remove test item after item in progress
            for index in range(len(self.test_plan.test_items)-1):
                self.test_plan.test_items.pop(1)
            
        else:                    
            self.test_plan.test_items.clear()

        self.update_test_list_details()  
        self.update_test_list_control_buttons_state()      
    
    def restart_all_test(self):
        '''Restart all tests not in queue'''
        
        for index in range(len(self.test_plan.test_items)):
            if not ((self.test_plan.test_items[index].status == TestStatus.IN_PROGRESS) or (self.test_plan.test_items[index].status == TestStatus.IN_QUEUE)):
                self.test_plan.test_items[index].status = TestStatus.IN_QUEUE
                self.test_plan.test_items[index].test_object.status = TestStatus.IN_QUEUE
                self.test_plan.test_items[index].test_object.estimated_time_s = self.test_plan.test_items[index].test_object.total_time
            
        self.update_test_list_details()
        self.update_test_list_control_buttons_state()

    # TODO: Separate test object loop into smaller functions
    # So that threads can be stopped
    def stop_tests(self):
        if not self.test_plan_update_timer.isActive():
            return
        # Stop the current thread to prevent status change

        # Stop the test plan update timer to prevent unexpected update
        self.test_plan_update_timer.stop()
        
        global test_control_flags
        test_control_flags['StopTest'] = True

        # Update the test list details after 5s
        QTimer.singleShot(5000, self.update_test_list_details)
        
        for test_item in self.test_plan.test_items:
            if test_item.status in [TestStatus.IN_PROGRESS, TestStatus.IN_QUEUE]:
                test_item.status = TestStatus.STOPPED
                test_item.test_object.status = TestStatus.STOPPED
        
        self.test_plan.status = TestStatus.STOPPED
        
        # Quit previous test thread
        if self.test_routine_thread is not None:
            if self.test_routine_thread.isRunning():
                self.test_routine_thread.quit()
                
        self.update_test_list_control_buttons_state()
        self.parent.msg_box_info('Test Info','Test Stopped',MessageType.INFO)
            
            
    def test_routine_thread_cleanup(self):
        def set_objects_to_none():        
            self.test_routine_thread = None
            self.parent.test_routine_thread = None
        QTimer.singleShot(1000, set_objects_to_none)

class GetSourceCapsWorker(QObject):
    """This class is a thread worker to run the GetSourceCaps function"""
    failed = Signal()
    finished = Signal()
    state = Signal(str)
    received_caps = Signal(list)

    def __init__(self, ac_source:ACSource, usbpd_sink:PISinkController|STM32SinkController, electronic_load:ElectronicLoadModule):
        super().__init__()
        self.ac_source = ac_source
        self.usbpd_sink = usbpd_sink
        self.electronic_load = electronic_load

    def run(self):
        """Run the routine for getting the source caps."""     
        # The whole routine is checked for error.
        # The main thread will do the handling
        try:
            self.ac_source_eload_discharge_sequence()
            self.state.emit('Discharing power supply')
            sleep(2)
            self.state.emit('Turning on source')
            self.ac_source.voltage = 115
            self.ac_source.turn_on()
            sleep(1)
            self.state.emit('Getting Source Caps')
            self.usbpd_sink.usb_pd_initialize()
            sleep(2)
            counter = 0
            while self.usbpd_sink.source_cap_count == 0:
                self.usbpd_sink.get_status(serial_number=self.usbpd_sink.serial_number)
                counter += 1
                if counter == 20:
                    break
                sleep(0.5)
            if self.usbpd_sink.epr_capable:
                self.state.emit('Getting Source Caps')
                self.usbpd_sink.epr_entry()
                sleep(3)
            self.usbpd_sink.get_source_caps()
            sleep(3)           
            # Return both the list received and fixed source caps.
            usbpd_source_caps = self.usbpd_sink.received_source_caps
            usbpd_fixed_source_caps = self.usbpd_sink.fs_list
            usbpd_pps_source_caps = self.usbpd_sink.pps_list
            usbpd_epr_avs_source_caps = self.usbpd_sink.epr_avs_list
            usbpd_spr_avs_source_caps = self.usbpd_sink.spr_avs_list
            # Turn off the source and emit a 'finished' signal
            self.ac_source.turn_off()
            self.state.emit('Turning off source')
            sleep(0.5)
            self.state.emit('Get Source Caps')
            self.received_caps.emit([usbpd_source_caps, usbpd_fixed_source_caps,usbpd_pps_source_caps,usbpd_epr_avs_source_caps,usbpd_spr_avs_source_caps])
            self.finished.emit()
        except:
            self.failed.emit()
        finally:
            self.ac_source_eload_discharge_sequence()
        
    def ac_source_eload_discharge_sequence(self):
        self.electronic_load.cc = 0.5
        self.electronic_load.turn_on()
        self.ac_source.turn_off()
        self.ac_source.coupling = 'AC'
        self.ac_source.offset = 0
        self.ac_source.ac_slew_rate = 9.9e37
        self.ac_source.dc_slew_rate = 9.9e37
        self.ac_source.freq_slew_rate = 9.9e37
        sleep(3)
        self.electronic_load.turn_off()  
        self.electronic_load.reset_values()    