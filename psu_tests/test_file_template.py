from psu_tests.test_object_imports import *

class TemplateTest(QObject):
    """
    File for test class template
    """
    
    title = "Template"
    short_title = "Template"
    
    # General UI Definitions
    ui_definitions = General_UI_Definitions()
    ui_definitions.stack_page_1 = StackWidget1Pages.LineVoltageRange
    ui_definitions.stack_page_2 = StackWidget2Pages.LoadCurrentRange
    ui_definitions.stack_page_3 = StackWidget3Pages.USBPD_Options

    ui_definitions.usb_pd_device_toggle_visible = True
    ui_definitions.nominal_iout_visible = True
    ui_definitions.nominal_vout_visible = True
    ui_definitions.nominal_vout_enable = True

    ui_definitions.measure_ripple_visible = True
    ui_definitions.load_type_visible = True

    
    # General UI Update Definitions
    ui_update = General_UI_Update_Definitions()
    ui_update.line_settings_update = True
    ui_update.load_settings_update = True
    ui_update.soaktime_settings_update = True
    ui_update.cvcc_settings_update = False
    ui_update.line_ramp_settings_update = False
    ui_update.nominal_output_settings_update = True
    ui_update.usbpd_options_update = True
    ui_update.tracking_pdo_request_update = True
    ui_update.measure_ripple_update = True
    ui_update.load_direction_update = True
    ui_update.eload_type_update = True
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
            temp_ui_def.usbpd_tracking_pdo_chk_visible = True
            temp_ui_def.usbpd_getsourcecaps_btn_visible = True
            temp_ui_def.nominal_vout_visible = False
            temp_ui_def.nominal_vout_enable = False
            temp_ui_def.add_test_button_2_txt = 'Test All Fixed PDO'
            temp_ui_def.add_test_button_2_visible = True
            return temp_ui_def
        
        # else, return the base definition
        else:
            return self.ui_definitions
        
    @classmethod
    def get_ui_update_definitions(self):
        """Return a UI u[date definition."""
        return self.ui_update

    tc_default = TestConditions(
        name = title,
        nominal_output_voltage_V=5,
        nominal_load_current_A=5,
        max_load_current_A = 5,
        line_range= LineSettings.UNIVERSAL,
        load_range= LoadSettings.LOAD_10_PCT_STEP,
        soak_time= SoaktimeSettings.SOAK_LOAD_REG,
        general_options = GeneralOptions(),
        usbpd_options = USBPDOptions(),
        line_ramp_settings = LineRamp(),
        i2c_test_parameters= I2CTestParameters())
    
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
        self.total_time, self.total_steps = self.estimate_remaining(0,0, vin_delays=True)
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
            self.ac_source_eload_discharge_sequence()
            print("Test Stopped")
            self.status_update.emit(TestStatus.STOPPED)
            
        
        except TestSkipped as e:
            # If the test is skipped through the UI
            self.cleanup_usbpd_pps_operation()
            self.ac_source_eload_discharge_sequence()
            print("Test Skipped")
            self.status_update.emit(TestStatus.SKIPPED)
            
        
        except Exception as e:
            # If there is an unhandled error inside the loop
            print(traceback.format_exc())
            self.cleanup_usbpd_pps_operation()
            if self.usbpd_test:
                self.usbpd_sink.usb_pd_initialize()
            self.ac_source_eload_discharge_sequence()
            print("Test Failed")
            self.status_update.emit(TestStatus.FAILED)
            

        else:
            # If all goes well
            # Emit a status_update signal to signal that the test is complete
            self.cleanup_usbpd_pps_operation()
            self.ac_source_eload_discharge_sequence()
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
        
        self.total_time, self.total_steps = self.estimate_remaining(0,0, vin_delays=True)
        self.status_report(0, 0, vin_delays=True)
        if self.usbpd_test:
            self.ac_source_eload_discharge_sequence()
        # Loop through each line input level
        for self.vin_index, self.vin_freq in enumerate(self.vin_list): 
        
            # Extract the values from the vin_freq
            self.ac_source.set_voltage_with_coupling(voltage= self.vin_freq[0], coupling= self.coupling)  
            if self.coupling == AC_SOURCE_COUPLING.AC:
                self.ac_source.frequency = self.vin_freq[1]
            self.source_vout = self.vin_freq[0]
            
            # Set the parameter for displaying the set output voltage
            self.test_data.vin_set_V = self.vin_freq[0]
            self.test_data.ac_freq_Hz = self.vin_freq[1]

            # Turn on the AC source with the current parameters
            self.ac_source.turn_on()

            # Sleep for a short time to allow the power supply to stabilize 
            sleep(2)

            # If the power supply is for USBPD, request the PDO for the test condition
            if self.usbpd_test:
                if(self.usbpd_sink.usb_pd_initialize()):
                    self.usb_pd_request(vout_V=self.vout_V, 
                        iout_A=self.i_rated_A)
                else:
                    raise ConnectionError("No USB-PD Source Connected")
                    
            
            # Set the e-load to the maximum load level to be tested and turn it on
            # self.electronic_load.reset_values()
            self.electronic_load.set_load(self.vout_V,max(self.iout_list_A),self.eload_type)
            self.electronic_load.turn_on()
            
            sleep(2)
            # Correct the ac source output, limit to 1V
            self.correct_source_output()

            # Do the initial soak if it is the first input voltage on the list
            if self.vin_index == 0:
                soak.do_initial_soak()
            # Or the soak per line if it is not
            else:
                soak.do_soak_per_line()

            # Create a new data series for the plottable objects  
            self.create_new_plot_series()
            
            # Loop through each load current level
            for iout_index, iout_level in enumerate(self.iout_list_A):
                # print("Entered inner loop")                 
                self.status_report(self.vin_index, iout_index, vin_delays=False)
                # print("Status report sent")
                # Trim the trailing zeros
                iout_A = float(f'{round(iout_level,6):g}')
                # print("Iout float")
                # If USB PD device and tracking_pdo_request_is set
                # request the PDO current the same as the load  
                if self.tracking_pdo_requests: 
                    # print("Entered Tracking PDO request")
                    # Get previous load current 
                    if iout_index == 0:
                        iout_previous_A = 0
                    else:
                        iout_previous_A = self.iout_list_A[iout_index]
                        
                    # If next current is higher than the previous 
                    # request new PDO current first before updating the e-load current              
                    if iout_A > iout_previous_A:
                        self.usb_pd_request(vout_V=self.vout_V, 
                            iout_A=iout_A) 
                        self.electronic_load.set_load(self.vout_V,iout_A,self.eload_type)
                        self.electronic_load.turn_on()
                    else:
                        self.electronic_load.set_load(self.vout_V,iout_A,self.eload_type)
                        self.electronic_load.turn_on()
                        self.usb_pd_request(vout_V=self.vout_V, 
                            iout_A=iout_A)
                else:
                    # print("Set eload")
                    self.electronic_load.set_load(self.vout_V,iout_A,self.eload_type)
                    self.electronic_load.turn_on()
                    
                if iout_A == 0:
                    # print("Off load")
                    self.electronic_load.turn_off()
                
                if iout_A < 0.05:
                    self.power_meter_load.set_current_range(0.05)
                else:
                        self.power_meter_load.current_auto_range_enable()
                
                # Sleep for a short time to allow the power meters to select the appropriate range
                sleep(2)

                # Correct the ac source output, limit to 1V
                self.correct_source_output()
                
                # Sleep for the soak time before measuring
                soak.do_soak_per_load()
                # print("Load soak done")

                # If ripple is to be measured, run the scope
                # TODO: Verify if working
                if self.measure_ripple:
                    # print("Measure ripple started")
                    self.oscilloscope.stop()
                    waveform_filename = (f"{self.short_title}_{self.vin_freq[0]:g}V{self.coupling}"
                                         f"_{self.vout_V:g}V_{iout_A:g}A.png")
                    self.oscilloscope.get_screenshot(waveform_filename, self.waveform_filepath) #capture waveform of output voltage with AC coupling
                    output_ripple_V = self.oscilloscope.get_measure(1)
                    self.test_data.output_ripple_mV = output_ripple_V * 1000
                    self.oscilloscope.run()
                    sleep(1)
                
                # TODO: Synchronize the integration
                # Gather the data from the equipment
                self.test_data.gather_data(coupling=self.coupling)
                # print("Gathered data")
                self.output_dataframe.loc[len(self.output_dataframe)]\
                    = self.process_data_row()
                # print("Dataframe")
                
                # Update the data for the results page
                self.update_output_data()
                # print("Output data for results page")
                
            # Discharge sequence
            self.ac_source_eload_discharge_sequence()
            
            # Add a blank row
            self.test_data_table.add_blank_row()
            
            # Get anchor
            if self.vin_index > 0:
                anchor = f"B{5+1+self.vin_index*(len(self.iout_list_A)+4)}"
            else:
                anchor = "B5"

            #export data to excel per line input
            # TODO: Consistency of 'Test Data' text needed
            export_to_excel(
                self.output_dataframe, self.output_folder_path, 
                self.data_filename, self.sheet_name, anchor) 
            # Clear data list for next loop 
            self.output_dataframe=self.output_dataframe[0:0]
    
    # TODO: Place in sink controller
    def usb_pd_request(self, vout_V:float, iout_A:float):
        
        # If fixed PDO
        if self.usbpd_options.pdo_type == SUPPLY_TYPE.FIXED:
            self.usbpd_sink.fpdo_request(vbus_V=vout_V, 
                                            iout_max_A=iout_A)
        # If augmented PDO
        elif self.usbpd_options.pdo_type == SUPPLY_TYPE.AUGMENTED:
            
            # If PPS
            if self.usbpd_options.augmented_type == AUGMENTED_TYPE.SPR_PPS:
                self.usbpd_sink.pps_request(vout_V=vout_V,
                                        iout_max_A=iout_A)
            # IF EPR AVS
            elif self.usbpd_options.augmented_type == AUGMENTED_TYPE.EPR_AVS:
                self.usbpd_sink.epr_avs_request(vout_V=vout_V,
                                        iout_max_A=iout_A)
            # IF SPR AVS
            elif self.usbpd_options.augmented_type == AUGMENTED_TYPE.SPR_AVS:
                self.usbpd_sink.spr_avs_request(vout_V=vout_V,
                                        iout_max_A=iout_A)
    
    def cleanup_usbpd_pps_operation(self):
        if self.usbpd_test:
            if self.usbpd_options.augmented_type == AUGMENTED_TYPE.SPR_PPS:
                self.usbpd_sink.pps_thread_cleanup()
                sleep(0.5)
                
    def ac_source_eload_discharge_sequence(self):
        self.equipment.input_supply_eload_discharge_sequence(self.i_max_A/3,coupling=self.coupling)

    def correct_source_output(self):
        
        # Read vin until steady
        for i in range(10):
            vin = self.power_meter_source.voltage
            # If read value is None, repeat read
            if vin is None:
                continue
            break
        
        offset = min(1,self.vin_freq[0] - self.power_meter_source.voltage)
        self.source_vout += offset

        self.ac_source.set_voltage_with_coupling(voltage=self.source_vout, coupling= self.coupling)
        self.ac_source.turn_on()      
    
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
            
        text = f"{self.title}: {round(self.vout_V,3):g}V, {round(self.i_max_A,3):g}A\n" 
        
        if self.usbpd_test:
            match self.usbpd_options.pdo_type:
                case SUPPLY_TYPE.FIXED:
                    if self.vout_V <= PD_SPECS.USBPD_MAX_SPR_FIXED_VOLTAGE_V:
                        supply_type = 'Fixed PDO: SPR'
                    else:
                        supply_type = 'Fixed PDO: EPR'
                case SUPPLY_TYPE.AUGMENTED:
                    match self.usbpd_options.augmented_type:
                        case AUGMENTED_TYPE.SPR_PPS:
                            supply_type = 'Augmented PDO: SPR PPS'
                        case AUGMENTED_TYPE.EPR_AVS:
                            supply_type = 'Augmented PDO: EPR AVS'
                        case AUGMENTED_TYPE.SPR_AVS:
                            supply_type = 'Augmented PDO: SPR AVS'
        else:
            supply_type = 'Non USB-PD'
        text += f"Supply type: {supply_type}\n"    
        if self.status in [TestStatus.STOPPED, TestStatus.FAILED, TestStatus.COMPLETE, TestStatus.SKIPPED]:
            text += f"{self.status}\n"
        else:
            text += f"{self.status}: {self.estimated_time_txt}, {self.progress_txt}\n"
            
        text += f"Line Range: {self.line_range.name}, Load Range: {self.load_range_pct.name}, Coupling: {self.coupling}\n"
        
        if self.tracking_pdo_requests:
            text += "Current Request Tracking: Enabled\n"
        else:
            text += "Current Request Tracking: Disabled\n"
            
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
        self.tracking_pdo_requests:bool = self.usbpd_options.tracking_pdo_request

        # General PSU Test Options
        self.general_options:GeneralOptions = self.test_conditions.general_options
        self.measure_ripple:bool = self.general_options.measure_ripple
        self.eload_type:str = self.general_options.eload_type
        self.use_eload_data:bool = self.general_options.use_eload_data
        self.load_direction:str = self.general_options.load_direction
        self.coupling:str = self.general_options.coupling

        # Nominal settings
        self.nominal_load_current_A:float = self.test_conditions.nominal_load_current_A
        self.nominal_output_voltage_V:float = self.test_conditions.nominal_output_voltage_V

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
        self.ac_source = self.equipment.ac_source
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

        self.power_meter_source.integration_settings(
            mode="NORMAL", timer_s=self.soak_time.integration_time)
        self.power_meter_load.integration_settings(
            mode="NORMAL", timer_s=self.soak_time.integration_time)
        self.power_meter_load.stop_integration()
        self.power_meter_source.stop_integration()
        self.power_meter_load.reset_integration()
        self.power_meter_source.reset_integration()

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
        self.output_dataframe = dataframe_from_headers(self.header_list)
        
        if not os.path.exists(self.output_folder_path):
            os.mkdir(self.output_folder_path)
        self.data_filename = f"{self.title} Test {self.vout_V:g}V"
        self.data_file_path = f'{self.output_folder_path}/{self.data_filename}.xlsx'
        
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
        self.sheet_name = (f"{self.short_title}_{self.coupling}_"
                           f"{round(self.vout_V,3):g}V_{round(self.i_max_A,3):g}A")
        
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
        self.ws.merge_cells('I4:L4')
        self.ws['I4'] = 'Ouput Measurement'
        self.ws['I4'].alignment = Alignment(horizontal='center')
        self.wb.save(self.data_file_path)
        self.wb.close()

    def define_data_header(self):
        """Defines the data header for the excel file."""  
        header_list = [
            f'V{self.coupling} (rms)','Freq (Hz)','Vin (rms)','Iin (mA)',
            'Pin (W)','PF','%THD','Vo (V)','Io (A)','Po (W)',
            '%V Reg','Efficiency','V Reg(5%)']

        if self.measure_ripple:
            header_list.append('PTP (mV)')
        return header_list

    def process_data_row(self):
        """Create a row of data from the test data"""
        # if self.coupling == 'DC':
        #     self.test_data.ac_freq_Hz = 0
        data_row = [
            self.test_data.vin_set_V, self.test_data.ac_freq_Hz, self.test_data.vin_V, 
            self.test_data.iin_mA,self.test_data.pin_W, self.test_data.PF, self.test_data.thd_pct, 
            self.test_data.vout_V, self.test_data.iout_A, self.test_data.pout_W, self.test_data.vreg_pct,
            self.test_data.eff_pct,self.test_data.vreg_passfail]
        if self.measure_ripple:
            data_row.append(self.test_data.output_ripple_mV)
            
        return data_row

    ###########################################################################
    #                       TEST CONDITIONS FUNCTIONS                         #
    ###########################################################################
    def prepare_test_conditions(self):
        """Prepare the list of conditions to be used."""
        test_conditions = self.test_conditions
        
        # Generate a list of the input line voltage
        self.vin_list = test_conditions.line_range.vin_freq
        
        # Nominal levels
        self.i_max_A = test_conditions.nominal_load_current_A
        self.vout_V = test_conditions.nominal_output_voltage_V
        self.i_rated_A = test_conditions.max_load_current_A
        
        #Generate a list of the load percent list
        self.load_pct_list = test_conditions.load_range.check_load_direction(self.general_options.load_direction)
        
        # Generate a list of output current using the load percent list
        self.iout_list_A = [load_pct * self.i_max_A/100 \
             for load_pct in self.load_pct_list] 

    ###########################################################################
    #                       TEST TIME ESTIMATION FUNCTIONS                    #
    ###########################################################################
    # Signals for reporting
    def status_report(self, vin_index, load_index, vin_delays):
        """Compute the remaining steps and time. 
        Emit signals containing the computed info."""
        remaining_time_s, remaining_steps = self.estimate_remaining(
            vin_index, load_index, vin_delays)
        percent_completion = round((1 - remaining_steps/self.total_steps)*100,0)

        self.estimated_time.emit(remaining_time_s)
        self.progress.emit(percent_completion)

    def estimate_remaining(self, vin_index_t, iout_index_t, vin_delays:bool = True):
        """Estimate the remaining time and steps using the inputs."""
        soak = self.soak_time

        remaining_time_s = 0
        remaining_steps = 0
        iout_index = 0
        vin_index = 0
        start_adding_time = False

        def add_time(t,add_step:bool = False):
            """Add the input time only when the index passed the input."""
            nonlocal remaining_steps
            nonlocal remaining_time_s
            nonlocal start_adding_time
            nonlocal vin_index
            nonlocal vin_index_t
            nonlocal iout_index
            nonlocal iout_index_t
            nonlocal vin_delays

            # Only add time if the index
            if not start_adding_time:
                if vin_index == vin_index_t:
                    if iout_index == iout_index_t:
                        start_adding_time = True
                        vin_delays = True
            
            if start_adding_time:
                remaining_time_s += t
                if add_step:
                    remaining_steps += 1

            return remaining_steps, remaining_time_s

        add_time(1)
        # Emulate the test loop to estimate the time and number of steps
        for vin_index, _ in enumerate(self.vin_list): 
            
            if vin_delays:
                # Sleep for a short time to allow the power supply to stabilize 
                add_time(2)

                # If the power supply is for USBPD, request the PDO for the test condition
                if self.usbpd_test:
                    add_time(1)
                # Do the initial soak if it is the first input voltage on the list
                if vin_index == 0:
                    add_time(soak.initial_soak)
                # Or the soak per line if it is not
                else:
                    add_time(soak.soak_per_line)
            
            # Loop through each load current level
            for iout_index, _ in enumerate(self.iout_list_A):                 
                if self.tracking_pdo_requests: 
                    add_time(1)
                add_time(2,True)
                # Sleep for the soak time before measuring
                add_time(soak.soak_per_load)
                add_time(soak.integration_time)
                add_time(1.7)
                if self.measure_ripple:
                    add_time(1)
               
        add_time(3)
        
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

        generate_plots_LoadReg(
            vout = self.vout_V,
            iout = max(self.iout_list_A),
            num_step = len(self.load_pct_list),
            vin_step = len(self.vin_list),
            coupling = self.coupling,
            wb = self.wb,
            sheet_name = self.sheet_name,
            wb_filepath = self.data_file_path,
            usb_pd_flag = self.usbpd_options.usbpd_test)
        
        generate_plots_LoadvEff(
            vout = self.vout_V,
            iout = max(self.iout_list_A),
            num_step = len(self.load_pct_list),
            vin_step = len(self.vin_list),
            coupling = self.coupling,
            wb = self.wb,
            sheet_name = self.sheet_name,
            wb_filepath = self.data_file_path)

        if self.measure_ripple:
            generate_plots_LoadvRipple(
                vout = self.vout_V,
                iout = max(self.iout_list_A),
                num_step = len(self.load_pct_list),
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
        self.load_vs_efficiency_plot = PlottableObject(
            title="Efficiency vs Load",
            type=PlotType.LINE,
            x_label="Load Current (A)",
            y_label="Efficiency (%)",
            x_range=(0, self.i_max_A),
            y_range=(80, 100),
            plot_series_list=[])
        
        nom_vout_V = self.vout_V
        self.load_reg_plot = PlottableObject(
            title="Load Regulation",
            type=PlotType.LINE,
            x_label="Load Current (A)",
            y_label="Output Voltage (V)",
            x_range=(0, self.i_max_A),
            y_range=(nom_vout_V*0.9, nom_vout_V*1.1),
            plot_series_list=[])
        
        if self.measure_ripple:
            self.load_vs_ripple_plot = PlottableObject(
                title="Ripple vs Load",
                type=PlotType.LINE,
                x_label="Load Current (A)",
                y_label="Output Ripple (mV)",
                x_range=(0, self.i_max_A),
                y_range=(0, 500),
                plot_series_list=[])

        self.test_data_table = DataTable(
            header=self.header_list, data=[])

        self.with_data = True
        
    def create_new_plot_series(self):
        """Create a new data series for each plottable object
        with the current input voltage as name."""
        self.load_vs_efficiency_plot.add_plot_series(
            name=f'{self.vin_list[self.vin_index][0]:3g} V',
            x_values=[],
            y_values=[])

        self.load_reg_plot.add_plot_series(
            name=f'{self.vin_list[self.vin_index][0]:3g} V',
            x_values=[],
            y_values=[])
        
        if self.measure_ripple:
            self.load_vs_ripple_plot.add_plot_series(
                name=f'{self.vin_list[self.vin_index][0]:3g} V',
                x_values=[],
                y_values=[])

    def update_output_data(self):
        """Update the plots and numeric data
        Emit a signal containing the processed info"""

        td = self.test_data

        # Plottable objects processing
        plottables = []

        self.load_vs_efficiency_plot.append_plot_data(
            plot_index=self.vin_index,
            x=td.iout_A,
            y=td.eff_pct)
        plottables.append(self.load_vs_efficiency_plot)
        
        self.load_reg_plot.append_plot_data(
            plot_index=self.vin_index,
            x=td.iout_A,
            y=td.vout_V)
        plottables.append(self.load_reg_plot)
        
        if self.measure_ripple:
            self.load_vs_ripple_plot.append_plot_data(
                plot_index=self.vin_index,
                x=td.iout_A,
                y=td.output_ripple_mV)
            plottables.append(self.load_vs_ripple_plot)
            
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
            'LOAD_RANGE_name':                     self.test_conditions.load_range.name,
            'LOAD_RANGE_load_range_pct':           self.test_conditions.load_range.load_range_pct,
            'LOAD_RANGE_custom':                   self.test_conditions.load_range.custom,
            'SOAK_TIME_name':                      self.test_conditions.soak_time.name,
            'SOAK_TIME_initial_soak':              self.test_conditions.soak_time.initial_soak,
            'SOAK_TIME_soak_per_line':             self.test_conditions.soak_time.soak_per_line,
            'SOAK_TIME_soak_per_load':             self.test_conditions.soak_time.soak_per_load,
            'SOAK_TIME_integration_time':          self.test_conditions.soak_time.integration_time,
            'SOAK_TIME_custom':                    self.test_conditions.soak_time.custom,
            'GENERAL_OPTIONS_measure_ripple':      self.test_conditions.general_options.measure_ripple,
            'GENERAL_OPTIONS_use_eload_data':      self.test_conditions.general_options.use_eload_data,
            'GENERAL_OPTIONS_eload_type':          self.test_conditions.general_options.eload_type,
            'GENERAL_OPTIONS_load_direction':      self.test_conditions.general_options.load_direction,
            'GENERAL_OPTIONS_coupling':            self.test_conditions.general_options.coupling,
            'USBPD_OPTIONS_usbpd_test':            self.test_conditions.usbpd_options.usbpd_test,
            'USBPD_OPTIONS_tracking_pdo_request':  self.test_conditions.usbpd_options.tracking_pdo_request,
            'USBPD_OPTIONS_pdo_type':              self.test_conditions.usbpd_options.pdo_type,
            'USBPD_OPTIONS_augmented_type':        self.test_conditions.usbpd_options.augmented_type,
            'NAME':                                self.test_conditions.name}
        return d
    
    @staticmethod
    def extract_test_condition(test_item_dict:dict)->dict:
        test_object_class = TemplateTest
        new_test_conditions = TestConditions(
            nominal_output_voltage_V=test_item_dict['NOMINAL_OUTPUT_VOLTAGE_V'],
            nominal_load_current_A=test_item_dict['NOMINAL_LOAD_CURRENT_A'],
            max_load_current_A=test_item_dict['MAX_LOAD_CURRENT_A'],
            line_range=LineRange(
                name = test_item_dict['LINE_RANGE_name'],
                vin_freq = test_item_dict['LINE_RANGE_vin_freq'],
                custom = test_item_dict['LINE_RANGE_custom']),
            load_range=LoadRange(
                name = test_item_dict['LOAD_RANGE_name'],
                load_range_pct = test_item_dict['LOAD_RANGE_load_range_pct'],
                custom = test_item_dict['LOAD_RANGE_custom']),
            soak_time=SoakTime(
                name = test_item_dict['SOAK_TIME_name'],
                initial= test_item_dict['SOAK_TIME_initial_soak'],
                line= test_item_dict['SOAK_TIME_soak_per_line'],
                load= test_item_dict['SOAK_TIME_soak_per_load'],
                integration= test_item_dict['SOAK_TIME_integration_time']),
            general_options=GeneralOptions(
                measure_ripple=test_item_dict['GENERAL_OPTIONS_measure_ripple'],
                use_eload_data=test_item_dict['GENERAL_OPTIONS_use_eload_data'],
                eload_type=test_item_dict['GENERAL_OPTIONS_eload_type'],
                load_direction=test_item_dict['GENERAL_OPTIONS_load_direction'],
                coupling=test_item_dict['GENERAL_OPTIONS_coupling']),
            usbpd_options=USBPDOptions(
                usbpd_test=test_item_dict['USBPD_OPTIONS_usbpd_test'],
                tracking_pdo_request=test_item_dict['USBPD_OPTIONS_tracking_pdo_request'],
                pdo_type=test_item_dict['USBPD_OPTIONS_pdo_type'],
                augmented_type=test_item_dict['USBPD_OPTIONS_augmented_type']),
            line_ramp_settings=test_object_class.tc_default.line_ramp_settings,
            i2c_test_parameters=test_object_class.tc_default.i2c_test_parameters,
            name=test_item_dict['NAME'])
        return new_test_conditions
    