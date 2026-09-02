from psu_tests.test_object_imports import *

class NoLoadPowerTest(BaseTestObject):
    """
    The no load power test measures input power at no load
    """
    title = "No Load Input Power"
    
    # General UI Definitions
    ui_definitions = General_UI_Definitions()
    ui_definitions.stack_page_1 = StackWidget1Pages.LineVoltageRange
    ui_definitions.stack_page_2 = StackWidget2Pages.EmptyPage
    ui_definitions.stack_page_3 = StackWidget3Pages.EmptyPage

    ui_definitions.measure_ripple_visible = False
    ui_definitions.load_type_visible = False
    ui_definitions.use_eload_data_toggle_visible = False
    
    # General UI Update Definitions
    ui_update = General_UI_Update_Definitions()
    ui_update.line_settings_update = True
    ui_update.load_settings_update = False
    ui_update.soaktime_settings_update = True
    ui_update.cvcc_settings_update = False
    ui_update.line_ramp_settings_update = False
    ui_update.nominal_output_settings_update = False
    ui_update.usbpd_options_update = False
    ui_update.tracking_pdo_request_update = False
    ui_update.measure_ripple_update = False
    ui_update.load_direction_update = False
    ui_update.eload_type_update = False
    ui_update.use_eload_data_update = False
    ui_update.i2c_params_update = False

    @classmethod
    def get_ui_definitions(self, flags:UIChangeFlags = UIChangeFlags()):
        """Return a UI definition based on the UIChangeFlags object."""
        return self.ui_definitions
    
    @classmethod
    def get_ui_update_definitions(self):
        """Return a UI update definition."""
        return self.ui_update
    
    tc_default = TestConditions(
        name = title, 
        nominal_output_voltage_V=5,
        nominal_load_current_A=5,
        max_load_current_A=5,
        line_range= LineSettings.UNIVERSAL,
        load_range= LoadSettings.LOAD_SINGLE_VALUE_100_PCT,
        soak_time= SoaktimeSettings.SOAK_NO_LOAD,
        general_options = GeneralOptions(),
        usbpd_options = USBPDOptions(),
        line_ramp_settings = LineRamp())
    
    def __init__(self, test_item):
        super().__init__()
        self.test_item:TestItem = test_item

        # Take the necessary details from the TestItem object        
        self.unpack_test_item()

        # To be passed down by the TestPlan object before running
        self.output_folder_path = None
        self.data_file_path = None
        self.waveform_filepath = None

        # Status
        self.status = TestStatus.IN_QUEUE
        self.progress_pct = 0
        self.prepare_test_conditions()
        self.total_time, self.total_steps = self.estimate_remaining(0)
        self.estimated_time_s = self.total_time
        self.message_closed = False
    
        self.with_data = False

    def run(self):
        """ Run the test for this TestObject

        This method will be run on a separate thread to prevent UI freezing
        """
        if self.parent.run_settings['debug']:
            debugpy.debug_this_thread()
        global test_control_flags


        # Run the loop for the test routines
        try:
            # Emit a status_update signal to signal that the test is in progress
            self.create_message_popup('No Load Input Power Test','Please remove the anything from the output connector and set the power meter to low power setting', MessageType.INFO)  
            
            self.status_update.emit(TestStatus.IN_PROGRESS)

            # Assign equipment and initialize settings
            self.setup_equipment()

            self.prepare_test_conditions()

            # Prepare the data container
            self.setup_data_file()
            
            self.test_loop()
            
            
        except TestStopped as e:
            # If the test is stopped through the UI
            self.input_supply.turn_off()
            print("Test Stopped")
            self.status_update.emit(TestStatus.STOPPED)
            
        except TestSkipped as e:
            # If the test is stopped through the UI
            self.input_supply.turn_off()
            print("Test Skipped")
            self.status_update.emit(TestStatus.SKIPPED)
            
            
        except Exception as e:
            # If there is an unhandled error inside the loop
            print(traceback.format_exc())
            self.input_supply.turn_off()
            print("Test Failed")
            self.status_update.emit(TestStatus.FAILED)
            
        else:
            # If all goes well
            # Emit a status_update signal to signal that the test is complete
            self.plot_charts()
            self.estimated_time_s = 0
            self.create_message_popup('No Load Input Power Test','Test done. Please reconnect the cable and load back to the output connector and set the power meter to high power setting if necessary', MessageType.INFO)            
            self.status_update.emit(TestStatus.COMPLETE)
            # self.test_item.test_routine_thread = None
    
    def create_message_popup(self,title:str,message:str,message_type:MessageType):
        self.message.emit(title,message, message_type)
        while self.message_closed == False:
            sleep(0.5)
            if test_control_flags['StopTest'] == True:
                raise TestStopped
            if test_control_flags['SkipTest'] == True:
                raise TestSkipped
        self.message_closed = False   
    
    def with_waveform_capture(self):
        return False

    def test_loop(self):
        
        soak = self.soak_time
        
        self.total_time, self.total_steps = self.estimate_remaining(0)
        self.status_report(0)
        
        self.create_new_plot_series()

        # Loop through each line input level
        for self.vin_index, vin_freq in enumerate(self.vin_list):
            self.status_report(self.vin_index) 
            
            # Extract the values from the vin_freq
            self.input_supply.set_voltage_with_coupling(voltage= vin_freq[0], coupling= self.coupling)  
            if self.coupling == AC_SOURCE_COUPLING.AC:
                self.input_supply.frequency = vin_freq[1]
            self.source_vout = vin_freq[0]
            
            # Set the parameter for displaying the set output voltage
            self.test_data.vin_set_V = vin_freq[0]
            self.test_data.ac_freq_Hz = vin_freq[1]

            # Turn on the AC source with the current parameters
            self.input_supply.turn_on()

            self.power_meter_source.current_auto_range_enable()
            # Sleep for a short time to allow the power supply to stabilize 
            sleep(2)
            
            # Do the initial soak if it is the first input voltage on the list
            if self.vin_index == 0:
                soak.do_initial_soak()
            # Or the soak per line if it is not
            else:
                soak.do_soak_per_line()
                

            if (self.power_meter_source._current_auto_range_status):
                self.power_meter_source.current_auto_range_enable(False)
                sleep(1)
            # TODO: Synchronize the integration
            # Gather the data from the equipment
            self.test_data.gather_data_source(coupling = self.coupling)

            self.power_meter_source.current_auto_range_enable()
            self.update_output_data()
            
            self.output_dataframe.loc[len(self.output_dataframe)]\
                = self.process_data_row()

        # Get anchor
        anchor = "B5"

        # export data to excel per line input
        # TODO: Consistency of 'Test Data' text needed
        export_to_excel(
            self.output_dataframe, self.output_folder_path, 
            f"{self.title} Test", self.sheet_name, anchor) 
            
        #Discharge sequence
        self.input_supply.turn_off()
    
    def update_test_list_text(self):
        """Update the text for the test list"""
        # If test status is complete, leave the ETA text as blank
        if self.status == TestStatus.COMPLETE:
            self.estimated_time_txt = ''
            self.progress_txt = '100'
        elif self.status in [TestStatus.STOPPED, TestStatus.SKIPPED]:
            self.estimated_time_txt = ''
            self.progress_txt = ''

        # If test status is In Queue or In Progress, process the time
        else:
            self.estimated_time_txt = \
                f'{datetime.timedelta(seconds=round(self.estimated_time_s,0))}'
            self.progress_txt = str(self.progress_pct)

        if not self.progress_txt == '':
            self.progress_txt += '%'
        
        text = f"{self.title}\n" 
        
        if self.status in [TestStatus.STOPPED, TestStatus.FAILED, TestStatus.COMPLETE, TestStatus.SKIPPED]:
            text += f"{self.status}\n"
        else:
            text += f"{self.status}: {self.estimated_time_txt}, {self.progress_txt}\n"
            
        text += f"Line Range: {self.line_range.name}, Coupling: {self.coupling}"

        self.test_list_text = text

    def unpack_test_item(self):
        """Extract the needed information from the TestItem object"""

        test_item = self.test_item

        self.parent:MainWindow = test_item.parent
        self.equipment:EquipmentHandler = self.parent.equipment

        # Type of test. See TEST_TYPE class
        self.test_type_index = test_item.test_type_index

        # Test Conditions Object
        self.test_conditions:TestConditions = test_item.test_conditions

        # General PSU Test Options
        self.general_options:GeneralOptions = self.test_conditions.general_options
        self.coupling:str = self.general_options.coupling

        # List of input voltage and frequency
        self.line_range:LineRange = self.test_conditions.line_range

        
        self.soak_time:SoakTime = self.test_conditions.soak_time

        # Test progress in percent
        self.test_progress:float = 0 
        self.test_complete:bool = False
    
    def setup_equipment(self):
        """Set up the assignment and initialization of equipment"""
        self.ac_source= self.equipment.ac_source
        self.dc_source = self.equipment.dc_source
        if (self.dc_source is not None) and (self.coupling == AC_SOURCE_COUPLING.DC):
            self.input_supply = self.dc_source
        else:
            if(self.ac_source is not None):
                self.input_supply = self.ac_source
            else:
                raise ConnectionError("No Input Supply Connected")
        self.power_meter_source = self.equipment.power_meter_source

        self.power_meter_source.integration_settings(
            mode="NORMAL", timer_s=self.soak_time.integration_time)
        self.power_meter_source.stop_integration()
        self.power_meter_source.reset_integration()



        # TODO: Set base settings such as coupling, averaging, rates

    def setup_data_file(self):
        """Set up the the data frame to be used for output 
        as well as the excel Workbook"""
        self.test_data = TestData()
        self.test_data.source_power_meter = self.power_meter_source

        # Prepare output dataframe
        self.header_list = self.define_data_header()
        self.output_dataframe = dataframe_from_headers(self.header_list)
        
        if not os.path.exists(self.output_folder_path):
            os.mkdir(self.output_folder_path)
        self.data_filename = f'{self.title} Test'
        self.data_file_path = f'{self.output_folder_path}/{self.data_filename}.xlsx'
        
        # Check if workbook exists
        if not os.path.exists(self.data_file_path):     
            self.wb:Workbook = openpyxl.Workbook()
            self.wb.save(self.data_file_path)
            self.wb.close()
            
        # Open the workbook    
        self.wb:Workbook = openpyxl.load_workbook(self.data_file_path)
        
        # Prepare the sheet name
        self.sheet_name = f"NoLoad_{self.coupling}"

        sheet_list = self.wb.sheetnames  
        if self.sheet_name in sheet_list:
            # Clear existing sheet of the test item
            clear_sheet(self.output_folder_path,
                    self.data_filename, self.sheet_name)
            self.wb:Workbook = openpyxl.load_workbook(self.data_file_path)
            self.ws:Worksheet = self.wb[self.sheet_name]
        else:
            # Create a worksheet 
            self.ws:Worksheet = self.wb.create_sheet(title=self.sheet_name)
            
        self.prepare_sheet_formatting()

        # Create the plottables and data table for the results viewer
        self.define_output_data_objects()
        
    def prepare_sheet_formatting(self):
        """Merge the cells for the header."""
        self.ws.merge_cells('B4:C4')
        self.ws['B4'] = 'Input'
        self.ws['B4'].alignment = Alignment(horizontal='center')
        self.ws.merge_cells('D4:H4')
        self.ws['D4'] = 'Input Measurement'
        self.ws['D4'].alignment = Alignment(horizontal='center')
        self.wb.save(self.data_file_path)
        self.wb.close()

    def prepare_test_conditions(self):
        """Prepare the list of conditions to be used."""
        test_conditions = self.test_conditions
        
        # Generate a list of the input line voltage
        self.vin_list = test_conditions.line_range.vin_freq
        
    def define_data_header(self):
        """Defines the data header for the excel file."""  
        header_list = [
            f'V{self.coupling} (rms)','Freq (Hz)','Vin (rms)','Iin (mA)',
            'Pin (mW)']
        return header_list
    
    def process_data_row(self):
        """Create a row of data from the test data"""
        data_row = [
            self.test_data.vin_set_V, self.test_data.ac_freq_Hz, self.test_data.vin_V, 
            self.test_data.iin_mA,self.test_data.pin_W*1000]       
        return data_row
    
    # Signals for reporting
    def status_report(self, vin_index):
                
        remaining_time_s, remaining_steps = self.estimate_remaining(vin_index)
        percent_completion = round((1 - remaining_steps/self.total_steps)*100,0)

        self.estimated_time.emit(remaining_time_s)
        self.progress.emit(percent_completion)
    
    def estimate_remaining(self, vin_index_t):

        soak = self.soak_time

        remaining_time_s = 0
        remaining_steps = 0
        vin_index = 0
        start_adding_time = False

        def add_time(t,add_step:bool = False):
            nonlocal remaining_steps
            nonlocal remaining_time_s
            nonlocal start_adding_time
            nonlocal vin_index
            nonlocal vin_index_t

            # Only add time if the index
            if not start_adding_time:
                if vin_index == vin_index_t:
                    start_adding_time = True
            
            if start_adding_time:
                remaining_time_s += t
                if add_step:
                    remaining_steps += 1

            return remaining_steps, remaining_time_s
        
        for vin_index, _ in enumerate(self.vin_list):
            
            add_time(2,True) 
            
            # Do the initial soak if it is the first input voltage on the list
            if vin_index == 0:
                add_time(soak.initial_soak)
            # Or the soak per line if it is not
            else:
                add_time(soak.soak_per_line)
            add_time(soak.integration_time)
            add_time(1.7)
        
        return remaining_time_s, remaining_steps
    
    def plot_charts(self):
        """Add a Chart on the output workbook for this test item."""
        self.wb = openpyxl.load_workbook(self.data_file_path)

        generate_plots_NoLoad(
            vin_step = len(self.vin_list),
            coupling = self.coupling,
            wb = self.wb,
            sheet_name = self.sheet_name,
            wb_filepath = self.data_file_path)
        
        self.wb.close()

    ###########################################################################
    #               Output Data Processing for Test Results Page              #
    ###########################################################################
    def define_output_data_objects(self):
        """Define the objects that will be viewable in the test results page"""
        # Plottable Objects
        self.input_power_vs_line_plot = PlottableObject(
            title="No-Load Input Power vs Line",
            type=PlotType.LINE,
            x_label="Input Voltage (V)",
            y_label="Input Power (mW)",
            x_range=(0, 265), # TODO: Make this dependent on max input
            y_range=(0, 200),
            plot_series_list=[])

        self.test_data_table = DataTable(
            header=self.header_list, data=[])

        self.with_data = True
        
    def create_new_plot_series(self):
        """Create a new data series for each plottable object
        with the current input voltage as name."""
        self.input_power_vs_line_plot.add_plot_series(
            name=f'No Load Input Power',
            x_values=[],
            y_values=[])

    def update_output_data(self):
        """Update the plots and numeric data
        Emit a signal containing the processed info"""

        td = self.test_data

        # Plottable objects processing
        plottables = []

        self.input_power_vs_line_plot.append_plot_data(
            plot_index=0,
            x=td.vin_set_V,
            y=td.pout_W * 1000)
        plottables.append(self.input_power_vs_line_plot)
        
        # Test Data Table Processing
        test_data_row = self.process_data_row()
        self.test_data_table.add_data_row(test_data_row)      

        self.test_data_update.emit([plottables, self.test_data_table])
    
    ###########################################################################
    #      Test Item Dictionary creation for saving/loading test items        #
    ###########################################################################
    def get_dict(self)->dict:
        d = {'TEST_TYPE_INDEX':                    self.test_type_index, 
            'MAX_LOAD_CURRENT_A':                  self.test_conditions.max_load_current_A,
            'LINE_RANGE_name':                     self.test_conditions.line_range.name,
            'LINE_RANGE_vin_freq':                 self.test_conditions.line_range.vin_freq,
            'LINE_RANGE_custom':                   self.test_conditions.line_range.custom,
            'SOAK_TIME_name':                      self.test_conditions.soak_time.name,
            'SOAK_TIME_initial_soak':              self.test_conditions.soak_time.initial_soak,
            'SOAK_TIME_soak_per_line':             self.test_conditions.soak_time.soak_per_line,
            'SOAK_TIME_soak_per_load':             self.test_conditions.soak_time.soak_per_load,
            'SOAK_TIME_integration_time':          self.test_conditions.soak_time.integration_time,
            'SOAK_TIME_custom':                    self.test_conditions.soak_time.custom,
            'GENERAL_OPTIONS_coupling':            self.test_conditions.general_options.coupling,
            'NAME':                                self.test_conditions.name}
        return d
    @staticmethod
    def extract_test_condition(test_item_dict:dict)->dict:
        test_object_class = NoLoadPowerTest
        new_test_conditions = TestConditions(
            nominal_output_voltage_V=test_object_class.tc_default.nominal_output_voltage_V,
            nominal_load_current_A=test_object_class.tc_default.nominal_load_current_A,
            max_load_current_A=test_object_class.tc_default.max_load_current_A,
            line_range=LineRange(
                name = test_item_dict['LINE_RANGE_name'],
                vin_freq = test_item_dict['LINE_RANGE_vin_freq'],
                custom = test_item_dict['LINE_RANGE_custom']),
            load_range=test_object_class.tc_default.load_range,
            soak_time=SoakTime(
                name = test_item_dict['SOAK_TIME_name'],
                initial= test_item_dict['SOAK_TIME_initial_soak'],
                line= test_item_dict['SOAK_TIME_soak_per_line'],
                load= test_item_dict['SOAK_TIME_soak_per_load'],
                integration= test_item_dict['SOAK_TIME_integration_time']),
            general_options=GeneralOptions(
                measure_ripple=test_object_class.tc_default.general_options.measure_ripple,
                use_eload_data=test_object_class.tc_default.general_options.use_eload_data,
                eload_type=test_object_class.tc_default.general_options.eload_type,
                load_direction=test_object_class.tc_default.general_options.load_direction,
                coupling=test_item_dict['GENERAL_OPTIONS_coupling']),
            usbpd_options=test_object_class.tc_default.usbpd_options,
            line_ramp_settings=test_object_class.tc_default.line_ramp_settings,
            i2c_test_parameters=test_object_class.tc_default.i2c_test_parameters,
            name=test_item_dict['NAME'])
        return new_test_conditions