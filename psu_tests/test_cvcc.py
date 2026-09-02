from psu_tests.test_object_imports import *

class CVCCTest(BaseTestObject):
    """
    The CVCC test sweeps the load until unit restarts
    """
    
    title = "CVCC"
    short_title = "CVCC"

    # General UI Definitions
    ui_definitions = General_UI_Definitions()
    ui_definitions.stack_page_1 = StackWidget1Pages.LineVoltageRange
    ui_definitions.stack_page_2 = StackWidget2Pages.CVCCSettings
    ui_definitions.stack_page_3 = StackWidget3Pages.USBPD_Options

    ui_definitions.usb_pd_device_toggle_visible = True
    ui_definitions.nominal_iout_visible = False
    ui_definitions.nominal_vout_visible = False
    ui_definitions.nominal_vout_enable = False
    ui_definitions.measure_ripple_visible = True

    ui_definitions.load_type_visible = False
        
    # General UI Update Definitions
    ui_update = General_UI_Update_Definitions()
    ui_update.line_settings_update = True
    ui_update.load_settings_update = False
    ui_update.soaktime_settings_update = True
    ui_update.cvcc_settings_update = True
    ui_update.line_ramp_settings_update = False
    ui_update.nominal_output_settings_update = False
    ui_update.usbpd_options_update = True
    ui_update.tracking_pdo_request_update = False
    ui_update.measure_ripple_update = True
    ui_update.load_direction_update = False
    ui_update.eload_type_update = False
    ui_update.use_eload_data_update = True
    ui_update.i2c_params_update = False

    @classmethod
    def get_ui_definitions(self, flags:UIChangeFlags = UIChangeFlags()):
        """Return a UI definition based on the UIChangeFlags object."""
        temp_ui_def = copy(self.ui_definitions)

        # If the USB PD device toggle is checked, 
        # modify the ui definition to be returned
        if flags.usb_pd_device_toggle_checked:
            temp_ui_def.usbpd_sourcecaps_table_visible = True
            temp_ui_def.usbpd_getsourcecaps_btn_visible = True
            temp_ui_def.multiple_cvcc_setpoints_enable = True
            return temp_ui_def
        
        # else, return the base definition
        else:
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
        soak_time= SoaktimeSettings.SOAK_CVCC,
        general_options = GeneralOptions(),
        usbpd_options = USBPDOptions(),
        line_ramp_settings = LineRamp(),
        i2c_test_parameters = I2CTestParameters())
    
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
        self.setup_cv_cc_load_steps()
        self.message_closed = False
        
        # Compute the estimated time during init to update display
        self.total_time, self.total_steps = self.estimate_remaining(
            0, vin_delay= True, cv_delay = True, cc_delay = True)
        self.estimated_time_s = self.total_time

        self.with_data = False
        self.message_closed = False
      
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
            self.status_update.emit(TestStatus.IN_PROGRESS)

            # Assign equipment and initialize settings
            self.setup_equipment()

            self.prepare_test_conditions()

            # Prepare the data container
            self.setup_data_file()
            self.test_loop()
        except TestStopped as e:
            # If the test is stopped through the UI
            self.cleanup_usbpd_pps_operation()
            self.input_supply_eload_discharge_sequence()
            print("Test Stopped")
            self.status_update.emit(TestStatus.STOPPED)
            
        
        except TestSkipped as e:
            # If the test is skipped through the UI
            self.cleanup_usbpd_pps_operation()
            self.input_supply_eload_discharge_sequence()
            print("Test Skipped")
            self.status_update.emit(TestStatus.SKIPPED)
            
        
        except Exception as e:
            # If there is an unhandled error inside the loop
            print(traceback.format_exc())
            self.cleanup_usbpd_pps_operation()
            if self.usbpd_test:
                self.usbpd_sink.usb_pd_initialize()
            self.input_supply_eload_discharge_sequence()
            print("Test Failed")
            self.status_update.emit(TestStatus.FAILED)
            

        else:
            # If all goes well
            # Emit a status_update signal to signal that the test is complete
            self.cleanup_usbpd_pps_operation()
            self.input_supply_eload_discharge_sequence()
            self.plot_charts()
            self.estimated_time_s = 0
            self.status_update.emit(TestStatus.COMPLETE)
    
    def create_message_popup(self,title:str,message:str,message_type:MessageType):
        self.message.emit(title,message, message_type)
        while self.message_closed == False:
            sleep(0.5)
            if test_control_flags['StopTest'] == True:
                raise TestStopped
            if test_control_flags['SkipTest'] == True:
                raise TestSkipped
        self.message_closed = False   

    def test_loop(self):
        soak = self.soak_time
        
        self.total_time, self.total_steps = self.estimate_remaining(
            0, vin_delay= True, cv_delay = True, cc_delay = True)
        self.status_report(0, vin_delay= True, cv_delay = True, cc_delay = True)
        if self.usbpd_test:
            self.input_supply_eload_discharge_sequence()
        # Loop through each line input level
        for self.vin_index, self.vin_freq in enumerate(self.vin_list): 

            # Initialize excel columns per line input level
            self.wb = load_workbook(self.data_file_path)
            
            self.prepare_sheet_formatting()
            self.output_dataframe = dataframe_from_headers(self.header_list)
            # Extract the values from the vin_freq
            self.input_supply.set_voltage_with_coupling(voltage= self.vin_freq[0], coupling= self.coupling) 
            if self.coupling == AC_SOURCE_COUPLING.AC:
                self.input_supply.frequency = self.vin_freq[1]
            self.source_vout = self.vin_freq[0]
            
            # Set the parameter for displaying the set output voltage
            self.test_data.vin_set_V = self.vin_freq[0]
            self.test_data.ac_freq_Hz = self.vin_freq[1]

            # Turn on the AC source with the current parameters
            self.input_supply.turn_on()

            if self.power_meter_load:
                self.power_meter_load.auto_range_enable()
            if self.power_meter_source:
                self.power_meter_source.current_auto_range_enable()

            # Sleep for a short time to allow the power supply to stabilize 
            sleep(2)

            # If the power supply is for USBPD, request the PDO for the test condition
            if self.usbpd_test:
                usbpd_init_ok = False
                counter = 0
                while not usbpd_init_ok:
                    usbpd_init_ok = self.usbpd_sink.usb_pd_initialize()
                    sleep(0.2)
                    counter += 1
                    if counter == 20:
                        raise ConnectionError("No USB-PD Source Connected")
                counter = 0
                while self.usbpd_sink.source_cap_count == 0:
                    self.usbpd_sink.get_status(serial_number=self.usbpd_sink.serial_number)
                    counter += 1
                    sleep(0.2)
                    if counter == 20:
                        raise ConnectionError("Unable to Get Source Capabilities")
                sleep(1)
                self.usbpd_sink.pps_request(
                    vout_V=self.vout_V,
                    iout_max_A=self.i_max_A)
            
            # Set the e-load to the minimum load level to be tested and turn it on
            self.electronic_load.reset_values()
            self.electronic_load.set_load(self.vout_V,0,self.eload_type)
            self.electronic_load.turn_on()
            
            # Sleep for a short time to allow the power supply to stabilize 
            sleep(2)
            # Correct the ac source output, limit to 1V
            self.correct_source_output()

            # Do the initial soak if it is the first input voltage on the list
            if self.vin_index == 0:
                soak.do_initial_soak()
            # Or the soak per line if it is not
            else:
                soak.do_soak_per_line()
            
            # TODO: Synchronize the integration
            # Gather the data from the equipment
            self.test_data.gather_data(integrate=False, coupling=self.coupling,usb_pd=self.usbpd_test)
            
            self.output_dataframe.loc[len(self.output_dataframe)]\
                = self.process_data_row()
                
            self.status_report(self.vin_index, cv_delay = True, cc_delay = True)    
            
            # Create a new data series for the plottable objects            
            self.create_new_plot_series()

            # Start CVCC loadstep loops
            # TODO: Simplify CVCC ranges
            # For CV region, Iout from 10% to 90% of set current
            self.status_report(self.vin_index,False,True,True)
            self.cv_region_sweep(self.CV_range,self.vin_freq)
            
            self.status_report(self.vin_index,False,False,True)
            self.cc_region_sweep(self.CC_range,self.vin_freq)
                        
            anchor = f"{get_column_letter(2+self.vin_index*self.column_step)}5"
            
            # export data to excel per line input
            export_to_excel(
                self.output_dataframe, self.output_folder_path,
                self.data_filename,self.sheet_name,anchor)
            # Clear data list for next loop 
            self.output_dataframe=self.output_dataframe[0:0]        
            
            # Discharge sequence for USB-PD tests
            if self.usbpd_test:
                self.cleanup_usbpd_pps_operation()
                self.input_supply_eload_discharge_sequence()
                
            sleep(3)        

    def cv_region_sweep(self, iout_range, vin_freq):
        """Sweep in CV region"""
        soak = self.soak_time

        for i_step in iout_range:
            if i_step == 0:
                self.electronic_load.turn_off()
                cr = self.min_cr
            else:
                cr = round(self.vout_V/i_step,6)
                self.electronic_load.set_load(self.vout_V,i_step,self.eload_type)
                self.electronic_load.turn_on()  
            
            if i_step < 0.05:
                if self.power_meter_load:
                    self.power_meter_load.set_current_range(0.05)
            else:
                if self.power_meter_load:
                    self.power_meter_load.current_auto_range_enable()
                    
            # Correct the ac source output, limit to 1V
            self.correct_source_output()
                        
            soak.do_soak_per_load()
            
            if self.measure_ripple:
                # print("Measure ripple started")
                self.oscilloscope.stop()
                waveform_filename = f"{vin_freq[0]:g}_V{self.coupling}_{self.vout_V:g}V_{i_step:g}A_CV.png"
                self.oscilloscope.get_screenshot(waveform_filename, self.waveform_filepath) #capture waveform of output voltage with AC coupling
                _, output_ripple_V = self.oscilloscope.get_measure(1)
                self.test_data.output_ripple_mV = output_ripple_V[0] * 1000
                self.oscilloscope.run()
                sleep(1)

            if self.power_meter_load and getattr(self.power_meter_load, '_current_auto_range_status', False):
                self.power_meter_load.auto_range_enable(False)
                sleep(1)
            if self.power_meter_source and getattr(self.power_meter_source, '_current_auto_range_status', False):
                self.power_meter_source.current_auto_range_enable(False)
                sleep(1)
            self.test_data.gather_data_load(integrate=False,usb_pd=self.usbpd_test)
            self.output_dataframe.loc[len(self.output_dataframe)]\
                = self.process_data_row_load()
            
            # Update the data for the results page
            self.update_output_data()
            self.min_cr = cr

            if self.power_meter_load:
                self.power_meter_load.auto_range_enable()
            if self.power_meter_source:
                self.power_meter_source.current_auto_range_enable()

    def cc_region_sweep(self, rout_range, vin_freq):
        """Sweep in CC region"""
        
        soak = self.soak_time
        for rout in rout_range:
            cr = round(rout,6)

            if cr > self.min_cr:
                continue
            vout_V = self.electronic_load.voltage
            self.electronic_load.set_load(vout_V,vout_V/cr,self.eload_type)
            self.electronic_load.turn_on()
            
            if vout_V/cr < 0.05:
                if self.power_meter_load:
                    self.power_meter_load.set_current_range(0.05)
            elif vout_V/cr <= 4.9:
                if self.power_meter_load:
                    self.power_meter_load.set_current_range(5)
            else:
                if self.power_meter_load:
                    self.power_meter_load.current_auto_range_enable()

            # Correct the ac source output, limit to 1V
            self.correct_source_output()
            soak.do_soak_per_load()
            
            if self.power_meter_load and getattr(self.power_meter_load, '_current_auto_range_status', False):
                self.power_meter_load.auto_range_enable(False)
                sleep(1)
            if self.power_meter_source and getattr(self.power_meter_source, '_current_auto_range_status', False):
                self.power_meter_source.current_auto_range_enable(False)
                sleep(1)
            
            if self.use_eload_data or self.power_meter_load is None:
                vout_V = self.electronic_load.voltage
            else:
                vout_V = self.power_meter_load.voltage
            
            if self.measure_ripple:
                # print("Measure ripple started")
                self.oscilloscope.stop()
                waveform_filename = f"{vin_freq[0]}_V{self.coupling}_{vout_V}V_{self.i_max_A}A_CC.png"
                self.oscilloscope.get_screenshot(waveform_filename, self.waveform_filepath) #capture waveform of output voltage with AC coupling
                output_ripple_V = self.oscilloscope.get_measure(1)
                self.test_data.output_ripple_mV = output_ripple_V * 1000
                self.oscilloscope.run()
                sleep(1)

            self.test_data.gather_data_load(integrate=False,usb_pd=self.usbpd_test)
            if self.power_meter_load:
                self.power_meter_load.auto_range_enable()
            if self.power_meter_source:
                self.power_meter_source.current_auto_range_enable()
            if not self.cc_data_valid():
                break

            self.output_dataframe.loc[len(self.output_dataframe)]\
                = self.process_data_row_load()

            # Update the data for the results page
            self.update_output_data()

            self.min_cr = cr

    def cc_data_valid(self)->bool:
        """Returns True if CC data is still valid.
        
        Causes of invalid data:
        1. Iout measured is greater than maximum specified current
        2. Any of the measured voltage, current, or power is zero
        3. Output voltage measured increased from previous measurement
        """
        td = self.test_data
        cond1 = abs(td.iout_A - self.i_max_A) > 0.5
        cond2 = 0 in [td.vout_V, td.iout_A]
        cond3 = td.vout_V \
            > (self.output_dataframe['Vo (V)'].tail(1).values* 1.03)
        cond4 = td.vout_V <= 2
        # Return false if any of the conditions is true
        return not (cond1 | cond2 | cond3 | cond4)
        

    def cleanup_usbpd_pps_operation(self):
        if self.usbpd_test:
            if self.usbpd_options.augmented_type == AUGMENTED_TYPE.SPR_PPS:
                self.usbpd_sink.pps_thread_cleanup()
                sleep(0.5)
                
    def input_supply_eload_discharge_sequence(self):
        self.equipment.input_supply_eload_discharge_sequence(self.i_max_A/3,coupling=self.coupling)

    def correct_source_output(self):
        """Remove the offset in the measured input by adjusting the source voltage"""
        # Read VIN until steady
        for i in range(10):
            vin = self.power_meter_source.voltage
            # If read value is None, repeat read
            if vin is None:
                continue
            break
        
        if vin is None:
            offset = 0
        else:
            offset = min(1, self.vin_freq[0] - vin)
        self.source_vout += offset
        self.input_supply.set_voltage_with_coupling(voltage=self.source_vout, coupling=self.coupling)
        self.input_supply.turn_on()

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
        
        text =  (f"{self.title}: {round(self.vout_V,3):g}V, "
                f"{round(self.i_max_A,3):g}A\n")
        
        if self.usbpd_test:
            supply_type = 'Augmented PDO: SPR PPS'
        else:
            supply_type = 'Non USB-PD'
            
        text += f"Supply type: {supply_type}\n"  
        
        if self.status in \
            [TestStatus.STOPPED, TestStatus.FAILED, TestStatus.COMPLETE, TestStatus.SKIPPED]:
            text += f"{self.status}\n"
        else:
            text += (f"{self.status}: {self.estimated_time_txt}, {self.progress_txt}\n")
        text += f"Line Range: {self.line_range.name}, Coupling: {self.coupling}\n"
        
        if self.measure_ripple:
            text += "Output Ripple Measurement: Enabled\n"
        else:
            text += "Output Ripple Measurement: Disabled\n"
        
        if self.use_eload_data:
            text += "Load Measurement: Electonic Load"
        else:
            text += "Load Measurement: Power Meter"
            
        self.test_list_text = text

    def with_waveform_capture(self):
        if self.test_conditions.general_options.measure_ripple:
            return True
        else:
            return False

    def unpack_test_item(self):
        """Extract the needed information from the TestItem object"""

        test_item = self.test_item

        self.parent:MainWindow = test_item.parent
        self.equipment:EquipmentHandler = self.parent.equipment

        # Type of test. See TEST_TYPE class
        self.test_type_index = test_item.test_type_index

        # Test Conditions Object
        self.test_conditions:TestConditions = test_item.test_conditions

        # USBPD Options
        self.usbpd_options:USBPDOptions = self.test_conditions.usbpd_options
        self.usbpd_test:bool = self.usbpd_options.usbpd_test
        self.tracking_pdo_requests:bool \
            = self.usbpd_options.tracking_pdo_request

        # General PSU Test Options
        self.general_options:GeneralOptions = self.test_conditions.general_options
        self.measure_ripple:bool = self.general_options.measure_ripple
        self.use_eload_data:bool = self.general_options.use_eload_data
        self.coupling:str = self.general_options.coupling

        # Nominal settings
        self.nominal_load_current_A:float \
            = self.test_conditions.nominal_load_current_A
        self.nominal_output_voltage_V:float \
            = self.test_conditions.nominal_output_voltage_V
        

        # List of input voltage and frequency
        self.line_range:LineRange = self.test_conditions.line_range

        # List of load percentage
        self.load_range_pct:LoadRange = self.test_conditions.load_range
        
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
        self.power_meter_load = self.equipment.power_meter_load_1
        self.electronic_load = self.equipment.electronic_load_1
        self.usbpd_sink = self.equipment.usbpd_sink
        self.oscilloscope = self.equipment.oscilloscope
        if self.measure_ripple:
            # self.initialize_scope_settings()
            # self.oscilloscope.run()
            # self.oscilloscope.setup_ripple()
            pass

        if self.power_meter_source is not None:
            self.power_meter_source.integration_settings(
                mode="NORMAL", timer_s=self.soak_time.integration_time)
            self.power_meter_source.stop_integration()
            self.power_meter_source.reset_integration()

        if self.power_meter_load is not None:
            self.power_meter_load.integration_settings(
                mode="NORMAL", timer_s=self.soak_time.integration_time)
            self.power_meter_load.stop_integration()
            self.power_meter_load.reset_integration()

        if self.electronic_load is not None:
            self.electronic_load.reset_values()

    ###########################################################################
    #                       DATA FILE SETUP FUNCTIONS                         #
    ###########################################################################
    # TODO: Set base settings such as coupling, averaging, rates
    def setup_data_file(self):
        """Set up the the data frame to be used for output 
        as well as the excel Workbook"""
        self.test_data = TestData()
        self.test_data.vout_nom_V = self.vout_V
        self.test_data.use_eload_data = self.use_eload_data
        self.test_data.source_power_meter = self.power_meter_source
        self.test_data.load_power_meter = self.power_meter_load
        self.test_data.electronic_load = self.electronic_load

        # Prepare output dataframe
        self.header_list = self.define_data_header()
        

        if not os.path.exists(self.output_folder_path):
            os.mkdir(self.output_folder_path)
        self.data_filename = f"{self.title} Test {self.vout_V:g}V"
        self.data_file_path \
            = f'{self.output_folder_path}/{self.data_filename}.xlsx'
            
        self.waveform_filepath = f'{self.output_folder_path}/waveforms' 
        if self.measure_ripple and not os.path.exists(self.waveform_filepath):
            os.mkdir(self.waveform_filepath)
        
        # Check if workbook exists
        if not os.path.exists(self.data_file_path):     
            self.wb:Workbook = openpyxl.Workbook()
            self.wb.save(self.data_file_path)
            self.wb.close()
            
        # Open the workbook    
        self.wb:Workbook = openpyxl.load_workbook(self.data_file_path)
        
        # Prepare the sheet name
        self.sheet_name \
            = f"CVCC_{self.coupling}_{round(self.vout_V,3):g}V_{round(self.i_max_A,3):g}A"

        sheet_list = self.wb.sheetnames  
        if self.sheet_name in sheet_list:
            # Clear existing sheet of the test item
            clear_sheet(self.output_folder_path,
                    self.data_filename,self.sheet_name)
            self.wb:Workbook = openpyxl.load_workbook(self.data_file_path)
            self.ws:Worksheet = self.wb[self.sheet_name]
        else:
            # Create a worksheet 
            self.ws:Worksheet = self.wb.create_sheet(title=self.sheet_name)

        self.wb.save(self.data_file_path)
        self.wb.close()
        
        # Create the plottables and data table for the results viewer
        self.define_output_data_objects()

    def prepare_sheet_formatting(self):
        """Merge the cells for the header.""" 
        self.ws:Worksheet= self.wb[self.sheet_name]       
        self.ws.merge_cells(
            f'{get_column_letter(2+self.vin_index*self.column_step)}4:'
            f'{get_column_letter(3+self.vin_index*self.column_step)}4')
        self.ws[f'{get_column_letter(2+self.vin_index*self.column_step)}4'] = 'Input'
        self.ws[f'{get_column_letter(2+self.vin_index*self.column_step)}4'].alignment \
            = Alignment(horizontal='center')
        self.ws.merge_cells(f'{get_column_letter(4+self.vin_index*self.column_step)}4:'
                            f'{get_column_letter(8+self.vin_index*self.column_step)}4')
        self.ws[f'{get_column_letter(4+self.vin_index*self.column_step)}4'] \
            = 'Input Measurement'
        self.ws[f'{get_column_letter(4+self.vin_index*self.column_step)}4'].alignment \
            = Alignment(horizontal='center')
        self.ws.merge_cells(f'{get_column_letter(9+self.vin_index*self.column_step)}4:'
                            f'{get_column_letter(12+self.vin_index*self.column_step)}4')
        self.ws.merge_cells(f'{get_column_letter(9+self.vin_index*self.column_step)}4:'
                            f'{get_column_letter(12+self.vin_index*self.column_step)}4')
        self.ws[f'{get_column_letter(9+self.vin_index*self.column_step)}4'] \
            = 'Output Measurement'
        self.ws[f'{get_column_letter(9+self.vin_index*self.column_step)}4'].alignment \
            = Alignment(horizontal='center')
        
        self.wb.save(self.data_file_path)
        self.wb.close()
        
        # Add header to output dataframe
        self.output_dataframe = dataframe_from_headers(self.header_list)

    def prepare_test_conditions(self):
        """Prepare the list of conditions to be used."""
        self.min_cr = 100000
        
        test_conditions = self.test_conditions
        
        self.eload_type = 'CR'
        
        # Generate a list of the input line voltage
        self.vin_list = test_conditions.line_range.vin_freq
        
        # Nominal levels
        self.i_max_A = test_conditions.nominal_load_current_A
        self.vout_V = test_conditions.nominal_output_voltage_V
        self.i_rated_A = test_conditions.max_load_current_A

        # Set up the target voltages in CC region
        self.setup_cv_cc_load_steps()
        
    def define_data_header(self):
        """Defines the data header for the excel file."""  
        header_list = [
            f'V{self.coupling} (rms)','Freq (Hz)','Vin (rms)','Iin (mA)',
            'Pin (W)','PF','%THD','Vo (V)','Io (A)','Po (W)',
            '%V Reg','Efficiency','V Reg(5%)']
        
        if self.measure_ripple:
            header_list.append('PTP (mV)')
        
        self.column_step = len(header_list)+1

        return header_list
    
    def process_data_row(self):
        """Create a row of data from the test data"""
        # TODO: CLEAN UP
        td = self.test_data
        data_row = [
            td.vin_set_V, td.ac_freq_Hz, td.vin_V, 
            td.iin_mA,td.pin_W, td.PF, td.thd_pct, 
            td.vout_V, td.iout_A, td.pout_W, td.vreg_pct,
            td.eff_pct,td.vreg_passfail]
        
        if self.measure_ripple:
            data_row.append(self.test_data.output_ripple_mV)
        
            
        return data_row
    def process_data_row_load(self):
        """Create a row of load data from the test data"""
        td = self.test_data
        data_row = [
            td.vin_set_V, td.ac_freq_Hz, None, None,None, None, None, td.vout_V, td.iout_A, 
            td.pout_W, td.vreg_pct, None,td.vreg_passfail]
        
        if self.measure_ripple:
            data_row.append(self.test_data.output_ripple_mV)
    
        return data_row
    
    def setup_cv_cc_load_steps(self):
        """Define the levels of output voltage in CC which will be measured"""
        self.Vrange_a = []
        self.Vrange_b = []
        self.Vrange_c = []
        
        # Get iout range for CV region
        self.CV_range = np.concatenate(
            [np.linspace(0, self.i_max_A*0.9, 10), np.linspace(self.i_max_A*0.91, self.i_max_A*1.05, 15)])

        if self.vout_V >= 8:
            self.Vrange_a = np.around(np.arange(self.vout_V-0.5, 8, -0.5), 3)
            self.Vrange_b = np.around(np.arange(8-0.1, 6, -0.1), 3)
            self.Vrange_c = np.around(np.arange(6-0.05, 2, -0.05), 3)
            self.CC_range = np.concatenate([self.Vrange_a, self.Vrange_b, self.Vrange_c])
        if (self.vout_V >= 6) & (self.vout_V < 8):
            self.Vrange_b = np.around(np.arange(self.vout_V-0.1, 6, -0.1), 3)
            self.Vrange_c = np.around(np.arange(6-0.05, 2, -0.05), 3)
            self.CC_range = np.concatenate([self.Vrange_b, self.Vrange_c])
        if (self.vout_V >= 2) & (self.vout_V < 6):
            self.Vrange_c = np.around(np.arange(self.vout_V-0.05, 2, -0.05), 3)
            self.CC_range = self.Vrange_c
            
        # For CC region, range is defined by r instead of i for convenience    
        self.CC_range = [x/ self.i_max_A for x in self.CC_range]           
    
    def status_report(self, vin_index_t, vin_delay = False,
                      cv_delay = False, cc_delay = False):
                
        remaining_time_s, remaining_steps \
            = self.estimate_remaining(
                vin_index_t, vin_delay, cv_delay,
                cc_delay)
                
        percent_completion = round((1-remaining_steps/self.total_steps)*100,0)

        self.estimated_time.emit(remaining_time_s)
        self.progress.emit(percent_completion)

    def estimate_remaining(
            self, vin_index_t, vin_delay = False, cv_delay = False, 
            cc_delay = False):

        soak = self.soak_time

        remaining_time_s = 0
        remaining_steps = 0
        iout_index = 0
        vin_index = 0
        start_adding_time = False

        def add_time(t,add_step:bool = False):
            nonlocal remaining_steps
            nonlocal remaining_time_s
            nonlocal start_adding_time
            nonlocal vin_index
            nonlocal vin_index_t
            nonlocal iout_index
            nonlocal vin_delay
            nonlocal cv_delay
            nonlocal cc_delay

            # Only add time if the index
            if not start_adding_time:
                if vin_index == vin_index_t:
                    start_adding_time = True
                    vin_delay = True
                    cv_delay = True
                    cc_delay = True
            
            if start_adding_time:
                remaining_time_s += t
                if add_step:
                    remaining_steps += 1                   

            return remaining_steps, remaining_time_s
        
        add_time(1)
        for vin_index, _ in enumerate(self.vin_list): 
            
            if vin_delay:
                # Delays to stabilize output
                add_time(6)
                # Initial soak or line soak
                if vin_index == 0:
                    add_time(soak.initial_soak)
                else:
                    add_time(soak.soak_per_line)
                # Measurement Delay
                add_time(0.1)
                
            if cv_delay:
                # For CV region
                for i_step in self.CV_range:
                    add_time(soak.soak_per_load)
                    add_time(soak.integration_time)
                    add_time(0.1,True)
                    if self.measure_ripple:
                        add_time(1)
            
            if cc_delay:
                # For CC region  
                for rout in self.CC_range:
                    add_time(soak.soak_per_load)
                    add_time(soak.integration_time)
                    add_time(0.1,True)
                    if self.measure_ripple:
                        add_time(1)
            
            add_time(8)
        
        return remaining_time_s, remaining_steps
    
    ###########################################################################
    #                       SCOPE SETUP                                       #
    ###########################################################################
    def initialize_scope_settings(self):
        """Define scope settings"""
    
        #trig_channel = 1
        #trig_level = 4.5
        #trig_edge = 'POS'
        
        time_position = 30
        time_scale = 0.01

        """ZOOM SETTINGS"""
        zoom_enable = False
        zoom_pos = 30.4
        zoom_rel_scale = 2
        zoom_vert_scale = 100

        """
        MEASUREMENT SETTINGS OPTIONS: "MAX,MIN,RMS,MEAN,PDELta"
        """

        ch1_enable = 'ON'
        ch2_enable = 'OFF'
        ch3_enable = 'OFF'
        ch4_enable = 'OFF'

        """CHANNEL 1"""
        ch1_scale = 0.1
        ch1_position = 0
        ch1_bw = 500
        ch1_rel_x_position = 20
        ch1_rel_y_position = 0
        ch1_offset = 0
        ch1_label = "VOUT"
        ch1_measure = "PDEL"
        ch1_color = "YELLOW"
        ch1_coupling = "AC"

        """CHANNEL 2"""
        ch2_scale = 0.2
        ch2_position = 0
        ch2_bw = 500
        ch2_rel_x_position = 40
        ch2_rel_y_position = 0
        ch2_offset = 5
        ch2_label = "VBUS_OUT"
        ch2_measure = "MAX,MIN"
        ch2_color = "LIGHT_BLUE"
        ch2_coupling = "DCLimit"

        """CHANNEL 3"""
        ch3_scale = 1
        ch3_position = -4
        ch3_bw = 500
        ch3_rel_x_position = 60
        ch3_rel_y_position = 0
        ch3_offset = 0
        ch3_label = "PRI_IDS"
        ch3_measure = "MAX,RMS"
        ch3_color = "PINK"
        ch3_coupling = "DCLimit"

        """CHANNEL 4"""
        ch4_scale = 5
        ch4_position = -5
        ch4_bw = 20
        ch4_rel_x_position = 80
        ch4_rel_y_position = 0
        ch4_offset = 0
        ch4_label = "VOUT"
        ch4_measure = "MAX,MIN"
        ch4_color = "GREEN"
        ch4_coupling = "DCLimit"
        ch4_offset = 10
        
        self.oscilloscope.remove_zoom()
        if zoom_enable:
            self.oscilloscope.add_zoom(rel_pos=zoom_pos, rel_scale=zoom_rel_scale,vert_scale=zoom_vert_scale)
            
        self.oscilloscope.channel_settings(state=ch1_enable, channel=1, scale=ch1_scale, position=ch1_position, label=ch1_label,
                                color=ch1_color, rel_x_position=ch1_rel_x_position,rel_y_position=ch1_rel_y_position, bandwidth=ch1_bw, coupling=ch1_coupling, offset=ch1_offset)
            
        self.oscilloscope.channel_settings(state=ch2_enable, channel=2, scale=ch2_scale, position=ch2_position, label=ch2_label,
                                color=ch2_color, rel_x_position=ch2_rel_x_position,rel_y_position=ch2_rel_y_position, bandwidth=ch2_bw, coupling=ch2_coupling, offset=ch2_offset)
        
        self.oscilloscope.channel_settings(state=ch3_enable, channel=3, scale=ch3_scale, position=ch3_position, label=ch3_label,
                                color=ch3_color, rel_x_position=ch3_rel_x_position,rel_y_position=ch3_rel_y_position, bandwidth=ch3_bw, coupling=ch3_coupling, offset=ch3_offset)
        
        self.oscilloscope.channel_settings(state=ch4_enable, channel=4, scale=ch4_scale, position=ch4_position, label=ch4_label,
                                color=ch4_color, rel_x_position=ch4_rel_x_position,rel_y_position=ch4_rel_y_position, bandwidth=ch4_bw, coupling=ch4_coupling, offset=ch4_offset)
        
        if ch1_enable != 'OFF': self.oscilloscope.measure(1, ch1_measure)
        if ch2_enable != 'OFF': self.oscilloscope.measure(2, ch2_measure)
        if ch3_enable != 'OFF': self.oscilloscope.measure(3, ch3_measure)
        if ch4_enable != 'OFF': self.oscilloscope.measure(4, ch4_measure)

        self.oscilloscope.record_length(50E6)
        self.oscilloscope.time_position(time_position)
        self.oscilloscope.time_scale(time_scale)

        
        #trigger_channel = trig_channel
        #trigger_level = trig_level
        #trigger_edge = trig_edge
        self.oscilloscope.trigger_mode("AUTO")
        
    ###########################################################################
    #                       PLOTTING                                          #
    ###########################################################################
    
    def plot_charts(self):
        """Add a Chart on the output workbook for this test item."""
        self.wb = openpyxl.load_workbook(self.data_file_path)

        col_vout = self.header_list.index('Vo (V)')
        col_iout = self.header_list.index('Io (A)')
        
        cvcc_plot = CVCCPlot(
            vout_v=self.vout_V, 
            iout_a=self.i_max_A, 
            vin_step=self.vin_list,
            coupling=self.coupling,
            num_step=500, sheet_name=self.sheet_name,
            wb_filepath=self.data_file_path,
            column_step=self.column_step,
            col_iout=col_iout,
            col_vout=col_vout)

        cvcc_plot.generate()

    ###########################################################################
    #               Output Data Processing for Test Results Page              #
    ###########################################################################
    def define_output_data_objects(self):
        """Define the objects that will be viewable in the test results page"""

        vin_min = 10000
        vin_max = 0
        nom_vout_V = self.vout_V
        iout_cc_A = self.i_max_A

        # Plottable Objects
        self.cvcc_plot = PlottableObject(
            title=f"CVCC {nom_vout_V:g}V {iout_cc_A:g}A",
            type=PlotType.LINE,
            x_label="Output Current (A)",
            y_label="Output Voltage",
            x_range=(0, iout_cc_A+.2),
            y_range=(0, nom_vout_V+2),
            plot_series_list=[])
        
        self.test_data_table = DataTable(
            header=self.header_list, data=[])

        self.with_data = True

    def create_new_plot_series(self):
        """Create a new data series for each plottable object
        with the current input voltage as name."""
        self.cvcc_plot.add_plot_series(
            name=f'{self.vin_list[self.vin_index][0]:3g} V',
            x_values=[],
            y_values=[])

    def update_output_data(self):
        """Update the plots and numeric data
        Emit a signal containing the processed info"""

        td = self.test_data

        # Plottable objects processing
        plottables = []

        self.cvcc_plot.append_plot_data(
            plot_index=self.vin_index,
            x=td.iout_A,
            y=td.vout_V)
        plottables.append(self.cvcc_plot)
        
        # Test Data Table Processing
        test_data_row = self.process_data_row()
        self.test_data_table.add_data_row(test_data_row)      

        self.test_data_update.emit([plottables, self.test_data_table])
        
    
    ###########################################################################
    #      Test Item Dictionary creation for saving/loading test items        #
    ###########################################################################
    
    def get_dict(self)->dict:
        d = {'TEST_TYPE_INDEX':                    self.test_type_index, 
            'NOMINAL_OUTPUT_VOLTAGE_V':            self.test_conditions.nominal_output_voltage_V,
            'NOMINAL_LOAD_CURRENT_A':              self.test_conditions.nominal_load_current_A,
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
            'GENERAL_OPTIONS_measure_ripple':      self.test_conditions.general_options.measure_ripple,
            'GENERAL_OPTIONS_use_eload_data':      self.test_conditions.general_options.use_eload_data,
            'GENERAL_OPTIONS_coupling':            self.test_conditions.general_options.coupling,
            'USBPD_OPTIONS_usbpd_test':            self.test_conditions.usbpd_options.usbpd_test,
            'USBPD_OPTIONS_tracking_pdo_request':  self.test_conditions.usbpd_options.tracking_pdo_request,
            'USBPD_OPTIONS_pdo_type':              self.test_conditions.usbpd_options.pdo_type,
            'USBPD_OPTIONS_augmented_type':        self.test_conditions.usbpd_options.augmented_type,
            'NAME':                                self.test_conditions.name}
        return d
    
    @staticmethod
    def extract_test_condition(test_item_dict:dict)->dict:
        test_object_class = CVCCTest
        new_test_conditions = TestConditions(
            nominal_output_voltage_V=test_item_dict['NOMINAL_OUTPUT_VOLTAGE_V'],
            nominal_load_current_A=test_item_dict['NOMINAL_LOAD_CURRENT_A'],
            max_load_current_A=test_item_dict['MAX_LOAD_CURRENT_A'],
            line_range=LineRange(
                name = test_item_dict['LINE_RANGE_name'],
                vin_freq = test_item_dict['LINE_RANGE_vin_freq'],
                custom = test_item_dict['LINE_RANGE_custom']),
            load_range=CVCCTest.tc_default.load_range,
            soak_time=SoakTime(
                name = test_item_dict['SOAK_TIME_name'],
                initial= test_item_dict['SOAK_TIME_initial_soak'],
                line= test_item_dict['SOAK_TIME_soak_per_line'],
                load= test_item_dict['SOAK_TIME_soak_per_load'],
                integration= test_item_dict['SOAK_TIME_integration_time']),
            general_options=GeneralOptions(
                measure_ripple=test_item_dict['GENERAL_OPTIONS_measure_ripple'],
                use_eload_data=test_item_dict['GENERAL_OPTIONS_use_eload_data'],
                eload_type=CVCCTest.tc_default.general_options.eload_type,
                load_direction=CVCCTest.tc_default.general_options.load_direction,
                coupling=test_item_dict['GENERAL_OPTIONS_coupling']),
            usbpd_options=USBPDOptions(
                usbpd_test=test_item_dict['USBPD_OPTIONS_usbpd_test'],
                tracking_pdo_request=test_item_dict['USBPD_OPTIONS_tracking_pdo_request'],
                pdo_type=test_item_dict['USBPD_OPTIONS_pdo_type'],
                augmented_type=test_item_dict['USBPD_OPTIONS_augmented_type']),
            line_ramp_settings= CVCCTest.tc_default.line_ramp_settings,
            i2c_test_parameters=CVCCTest.tc_default.i2c_test_parameters,
            name=test_item_dict['NAME'])
        return new_test_conditions