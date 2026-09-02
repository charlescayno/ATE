import os

from datetime import datetime

import openpyxl

from PySide2.QtCore import (QThread, QObject, Signal, Slot,QTimer)

from psu_tests.definitions import (
    MessageType, LineRange, LineSettings, LineRamp, LineRampSettings, LoadRange,
    LoadSettings, SoakTime, SoaktimeSettings, USBPDOptions,
    GeneralOptions, I2CTestParameters, TestConditions,TestStatus)

from psu_tests.ui_definitions import *

from equipment.handler import *

# Import classes for different test types
from psu_tests.test_load_reg import LoadRegulationTest
from psu_tests.test_line_reg import LineRegulationTest
from psu_tests.test_efficiency import EfficiencyTest
from psu_tests.test_no_load import NoLoadPowerTest
from psu_tests.test_cvcc import CVCCTest
from psu_tests.test_transients import TransientsTest
from psu_tests.test_input_harmonics import InputHarmonicsTest
from psu_tests.test_input_line_ramp import InputLineRampTest
from psu_tests.test_i2c_cv_sweep import I2C_CVSweepTest
from psu_tests.test_file_template import TemplateTest
from psu_tests.test_type import TestTypes, get_test_title_list, get_test_title, get_test_type
from pd.pd_types import SUPPLY_TYPE

from plotter.plotter import PlotSeries, PlottableObject, PlotType, DataTable


class TestItem():
    def __init__(self,
            # parent: MainWindow,
            parent,
            test_type_index:int,
            test_conditions:TestConditions,
            *args, **kwargs):
        # Make the parent's objects such as the equipment, USB PD sink, etc
        # available to the TestItem object
        self.parent = parent

        # Type of test. See TEST_TYPE class
        self.test_type_index = test_type_index

        # Test conditions object
        self.test_conditions = test_conditions

        # Test progress in percent
        self.test_progress:int = 0 
        self.status = TestStatus.IN_QUEUE

        # TODO: Add test equipment requirements for checking later
        self.test_requirements = []

        self.test_routine_thread = None

        self.generate_test_object()

        # Test data related objects
        self.plottables:list[PlottableObject] = list()
        self.test_data_table:DataTable = None 
        
        # Only those with True will appear on the TestResultsPage
        self.with_test_data = False  
        
    @Slot(str,str,MessageType)
    def popup_message(self, title:str='', message:str='',message_type:MessageType = MessageType.INFO):
        self.parent.msg_box_info(title,message,message_type)
        self.worker.message_closed = True

        
    def generate_test_object(self):
        """ Convert the test item into a TestObject that is appropriate
        """
        # Use the test_type_index to get a class from the TestTypes list
        test_class:TemplateTest = TestTypes[self.test_type_index]
        # Create an instance of the selected class using the current TestItem parameters
        self.test_object:TemplateTest = test_class(self)

    @Slot(int)
    def update_progress(self, progress_pct):
        # print(f'Test is {progress_pct}% done')
        self.progress_pct = progress_pct
        self.test_object.progress_pct = progress_pct

    @Slot(int)
    def update_estimated_time(self, estimated_time):
        self.test_object.estimated_time_s = estimated_time
        # print(f'Estimated time(s) {estimated_time}')

    @Slot(TestStatus)
    def update_object_status(self, status):
        self.test_object.status = status
        if status == TestStatus.COMPLETE:
            self.test_routine_thread.quit()
        elif status == TestStatus.STOPPED:
            self.test_routine_thread.exit(1)
        elif status == TestStatus.FAILED:
            self.test_routine_thread.exit(-1)
        elif status == TestStatus.SKIPPED:
            self.test_routine_thread.exit(2)

    @Slot(list)
    def update_test_data(self, test_data):
        """Slot to receive the test data sent by the test object thread.
        This information will be used by the TestResults page handler to 
        show the plot and test data"""
        self.with_test_data = True

        self.plottables:list[PlottableObject] = test_data[0]
        self.test_data_table:DataTable = test_data[1]

    def update_status(self):
        
        def item_status():
            self.test_routine_thread = None
            self.status = self.test_object.status    
    
        if not self.test_object.status in [TestStatus.IN_PROGRESS, TestStatus.IN_QUEUE]:
            self.test_routine_thread.deleteLater()
        
        QTimer.singleShot(1000,item_status)

    def run(self):
        """ Run the test object of the TestItem Object
        """
        self.status = TestStatus.IN_PROGRESS
        self.worker:TemplateTest = self.test_object

        # Move the worker to the separate thread
        self.worker.moveToThread(self.test_routine_thread)

        # Connect basic Signals
        self.test_routine_thread.started.connect(self.worker.run)
        self.test_routine_thread.finished.connect(self.update_status)
        # self.worker.finished.connect(self.test_routine_thread.quit)
        # self.worker.finished.connect(self.worker.deleteLater)
        
        # Connect signals to defined slots
        self.worker.status_update.connect(self.update_object_status)
        self.worker.estimated_time.connect(self.update_estimated_time)
        self.worker.progress.connect(self.update_progress)
        self.worker.message.connect(self.popup_message)
        
        try:
            self.worker.test_data_update.connect(self.update_test_data)
        except:
            print("Add test data update for this test")

        # Start the thread to run the TestObject
        self.test_routine_thread.start()
    
    def get_dict(self)->dict:
        """Return a dictionary containing the details of the TestItem object."""
        
        d = self.test_object.get_dict()
        return d
        
class TestPlan():
    """ A container class for the list of tests that will be done
    
    Methods:
    add_test_item
    remove_test_item
    reorder_test_item
    run_test_items
    get_test_equipment_requirements

    """
    def __init__(self, parent):

        # Make the parent's objects such as the equipment, USB PD sink, etc
        # available to the TestPlan object
        self.parent = parent

        # List of all the tests to be performed
        self.test_items:list[TestItem] = []

        # Output folder that is shared across the tests
        self.output_folder_path = None

        self.status = TestStatus.IN_QUEUE
        self.progress: int = 0

        self.test_routine_thread = QThread()
        self.line_settings=LineSettings()
        self.load_settings=LoadSettings()
        self.soaktime_settings=SoaktimeSettings()


    def add_test_item(self, test_item:TestItem, *args, **kwargs):
        test_item.parent = self.parent
        self.test_items.append(test_item)

    # Test item preparation related methods

    def prepare_test_items(self):
        """Prepare the test items for the test."""
        # Distribute the necessary values
        self.distribute_necessary_values()

    def generate_output_folder_name(self):
        """Generate a test output using the current date and time"""
        
        date_time = datetime.now()
        # TODO: Fix time
        dt_formatted = date_time.strftime('%Y-%m-%d_%H-%M-%S')

        # Check if TestObject needs waveform capture
        with_waveform_capture = False
        for test_item in self.test_items:
            with_waveform_capture = test_item.test_object.with_waveform_capture()
        
        # Set the folder name according to the need of waveform capture
        if with_waveform_capture:
            return f'Test_Data_and_Waveforms_{dt_formatted}'
        else:
            return f'Test_Data_{dt_formatted}'

    def distribute_necessary_values(self):
        """"""
        for test_item in self.test_items:
            # Distribute folder and file paths
            test_item.test_object.output_folder_path = self.output_folder_path
    
    # Test Loop related methods

    def update_loop(self):
        """Processes the test plan when the test is running"""
        self.update_status()

        if self.status == TestStatus.IN_QUEUE:
            self.run_1st_test_in_queue()
    
    def update_status(self):
        """Check all test item and get the status of the test list
        """
        
        # Removed as stop status only applies when stop button is pressed
        # stopped_flag = False

        
        # Get status of all test items
        test_item_status_list = [x.status for x in self.test_items]
        if (TestStatus.IN_PROGRESS not in test_item_status_list) and (TestStatus.IN_QUEUE not in test_item_status_list):
            self.status = TestStatus.COMPLETE
            return self.status
        
        if (TestStatus.IN_PROGRESS in test_item_status_list):
            self.status = TestStatus.IN_PROGRESS
            return self.status
            
        if (TestStatus.IN_QUEUE in test_item_status_list):
            self.status = TestStatus.IN_QUEUE
            return self.status

    def run_1st_test_in_queue(self):
        """Loop through the test items and run the first item 
        with the status set to IN_QUEUE"""
        for test_item in self.test_items:
            if (test_item.status == TestStatus.IN_QUEUE):
                test_item.run()
                return
            
    def add_dict_to_test_plan(self, test_item_dict:dict):
        """Add the test_item to the list"""
        
        name=test_item_dict['NAME']
        test_names = get_test_title_list()
        test_type:TemplateTest = TestTypes[test_names.index(name)]
        new_test_conditions:TestConditions = test_type.extract_test_condition(test_item_dict=test_item_dict)
        
        # Update line settings list, load settings list, and soaktime settings list
        
        self.line_settings.add_dict_to_range_list(new_test_conditions.line_range.get_dict())
        self.load_settings.add_dict_to_range_list(new_test_conditions.load_range.get_dict())
        self.soaktime_settings.add_dict_to_soaktime_list(new_test_conditions.soak_time.get_dict())
        
        # Handling if any of the created test conditions settings are not found in the respective list, set it to Custom setting
        
        # Line settings list check
        line_settings_names = [x.name for x in self.line_settings.line_range_list]
        # If new line settting name not in list of names
        if new_test_conditions.line_range.name not in line_settings_names:
            new_test_conditions.line_range.name = "Custom"
            new_test_conditions.line_range.custom =False
        # If new line range does not mach respective line range in the list
        elif (not new_test_conditions.line_range.vin_freq == self.line_settings.line_range_list[line_settings_names.index(new_test_conditions.line_range.name)].vin_freq):
            new_test_conditions.line_range.name = "Custom"
            new_test_conditions.line_range.custom =True
        
        # Load settings list check        
        load_settings_names = [x.name for x in LoadSettings().load_range_list]
        # If new load settting name not in list of names
        if new_test_conditions.load_range.name not in load_settings_names:
            new_test_conditions.load_range.name = "Custom"
            new_test_conditions.load_range.custom =True
        # If new load range does not mach respective load range in the list
        elif (not new_test_conditions.load_range.load_range_pct == self.load_settings.load_range_list[load_settings_names.index(new_test_conditions.load_range.name)].load_range_pct):
            new_test_conditions.load_range.name = "Custom"
            new_test_conditions.load_range.custom =True
        
        
        # Soaktime settings list check
        soaktime_settings_names = [x.name for x in SoaktimeSettings().soaktime_list]
        # If new soaktime settting name not in list of names
        if new_test_conditions.soak_time.name not in soaktime_settings_names:
            new_test_conditions.soak_time.name = "Custom"
            new_test_conditions.soak_time.custom =True
        # If new soaktime setting does not mach respective soaktime setting in the list
        elif (not new_test_conditions.soak_time.initial_soak == self.soaktime_settings.soaktime_list[soaktime_settings_names.index(new_test_conditions.soak_time.name)].initial_soak) or \
            (not new_test_conditions.soak_time.soak_per_line == self.soaktime_settings.soaktime_list[soaktime_settings_names.index(new_test_conditions.soak_time.name)].soak_per_line) or \
            (not new_test_conditions.soak_time.soak_per_load == self.soaktime_settings.soaktime_list[soaktime_settings_names.index(new_test_conditions.soak_time.name)].soak_per_load) or \
            (not new_test_conditions.soak_time.integration_time == self.soaktime_settings.soaktime_list[soaktime_settings_names.index(new_test_conditions.soak_time.name)].integration_time):
            new_test_conditions.soak_time.name = "Custom"
            new_test_conditions.soak_time.custom =True
            
        # Create new test item
        new_test_item = TestItem(self.parent,test_type_index=test_item_dict['TEST_TYPE_INDEX'],test_conditions=new_test_conditions)
        # Add test item to test list
        self.add_test_item(new_test_item)
