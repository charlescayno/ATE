from psu_tests.test_object_imports import *

class I2C_LineRegTest(BaseTestObject):
    """
    The line regulation test sweeps the line input
    """
    title = "I2C LineReg"
    short_title = "LineReg"
    i2c_test = True

    # General UI Definitions
    ui_definitions = General_UI_Definitions()
    ui_definitions.stack_page_1 = StackWidget1Pages.LineVoltageRange
    ui_definitions.stack_page_2 = StackWidget2Pages.LoadCurrentRange
    ui_definitions.stack_page_3 = StackWidget3Pages.I2C_Options

    ui_definitions.measure_ripple_visible = True
    ui_definitions.load_type_visible = True

    # I2C UI definitions
    i2c_ui_definitions = I2C_UI_Definitions()
    # Line Edits
    i2c_ui_definitions.add_lineedit(label='Nominal Vout (V)', param_index=1)
    i2c_ui_definitions.add_lineedit(label='Nominal Iout (A)', param_index=2)

    i2c_ui_definitions.add_lineedit(label='SR ZVS On',param_index=9)
    i2c_ui_definitions.add_lineedit(label='SR ZVS Delay',param_index=10)
    # Combo box
    i2c_ui_definitions.add_cbx(label="SR ZVS?", contents=['Yes', 'No'], param_index=1)
    i2c_ui_definitions.add_cbx(label="Initial Mode", contents=['CCM', 'DCM'], param_index=2)
    i2c_ui_definitions.add_cbx(label="Inno-Pro Family", contents=InnoProFamilyList, param_index=4)
        
    # General UI Update Definitions
    ui_update = General_UI_Update_Definitions()
    ui_update.line_settings_update = True
    ui_update.load_settings_update = True
    ui_update.soaktime_settings_update = True
    ui_update.cvcc_settings_update = False
    ui_update.line_ramp_settings_update = False
    ui_update.nominal_output_settings_update = True
    ui_update.usbpd_options_update = False
    ui_update.tracking_pdo_request_update = False
    ui_update.measure_ripple_update = True
    ui_update.load_direction_update = True
    ui_update.eload_type_update = True
    ui_update.use_eload_data_update = True
    ui_update.i2c_params_update = True
    
    @classmethod
    def get_ui_definitions(self, flags:UIChangeFlags = UIChangeFlags()):
        """Return a UI definition based on the UIChangeFlags object."""
        temp_ui_def = copy(self.ui_definitions)

        return self.ui_definitions

    @classmethod
    def get_ui_update_definitions(self):
        """Return a UI update definition."""
        return self.ui_update
    
    @classmethod
    def set_i2c_ui_definitions(self):
        """Set default I2C UI definitions"""
        # I2C UI definitions
        self.i2c_ui_definitions = I2C_UI_Definitions()
        # Line Edits
        self.i2c_ui_definitions.add_lineedit(label='Nominal Vout (V)', param_index=1)
        self.i2c_ui_definitions.add_lineedit(label='Nominal Iout (A)', param_index=2)

        self.i2c_ui_definitions.add_lineedit(label='SR ZVS On',param_index=9)
        self.i2c_ui_definitions.add_lineedit(label='SR ZVS Delay',param_index=10)
        # Combo box
        self.i2c_ui_definitions.add_cbx(label="SR ZVS?", contents=['Yes', 'No'], param_index=1)
        self.i2c_ui_definitions.add_cbx(label="Initial Mode", contents=['CCM', 'DCM'], param_index=2)
        self.i2c_ui_definitions.add_cbx(label="Inno-Pro Family", contents=InnoProFamilyList, param_index=4)
    
    @classmethod
    def update_i2c_ui_definitions(self,inno_family:InnoProFamily.Inno5Pro):
        match inno_family:
            case InnoProFamily.Inno5Pro:
                self.set_i2c_ui_definitions()
                return self.i2c_ui_definitions
            case InnoProFamily.Inno4Pro:
                self.i2c_ui_definitions.sub_lineedit(param_index=9)
                self.i2c_ui_definitions.sub_lineedit(param_index=10)
                self.i2c_ui_definitions.sub_cbx(param_index=1)
                return self.i2c_ui_definitions
    
    tc_default = TestConditions(
        name = title,
        nominal_output_voltage_V=5,
        nominal_load_current_A=5,
        max_load_current_A =5,
        line_range= LineSettings.UNIVERSAL_EXT,
        load_range= LoadSettings.LOAD_100_50_PCT,
        soak_time= SoaktimeSettings.SOAK_LINE_REG,
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
        self.total_time, self.total_steps = self.estimate_remaining(0,0,iout_delays = True, initial_delays = True)
        self.estimated_time_s = self.total_time

        self.with_data = False
        self.message_closed = False
    
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
        if self.test_conditions.general_options.measure_ripple:
            return True
        else:
            return False

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
            self.input_supply_eload_discharge_sequence()
            print("Test Stopped")
            self.i2c_controller.close()
            self.status_update.emit(TestStatus.STOPPED)
        
        except TestSkipped as e:
            # If the test is skipped while running
            self.input_supply_eload_discharge_sequence()
            print("Test Skipped")
            self.i2c_controller.close()
            self.status_update.emit(TestStatus.SKIPPED)

        except Exception as e:
            # If there is an unhandled error inside the loop
            print(traceback.format_exc())
            self.input_supply_eload_discharge_sequence()
            print("Test Failed")
            self.i2c_controller.close()
            self.status_update.emit(TestStatus.FAILED)

        else:
            # If all goes well
            # Emit a status_update signal to signal that the test is complete
            self.input_supply_eload_discharge_sequence()
            self.plot_charts()
            self.estimated_time_s = 0
            self.i2c_controller.close()
            self.status_update.emit(TestStatus.COMPLETE)

    def i2c_initialize(self):
        i2c = self.i2c_commands
        self.i2c_controller.watchdog(self.i2c_commands.WATCHDOG_OFF)
        self.i2c_controller.fast_vi(self.i2c_commands.FASTVI_LIMIT_DIS)
        self.i2c_controller.ova(30, self.i2c_commands.OVA_RESP_NR)
        self.i2c_controller.uva(3, self.i2c_commands.UVA_RESP_NR, self.i2c_commands.UVA_TIMER_16MS)
        # self.i2c_controller.loop_option(self.i2c_commands.LOOP_OPTION1_LSB, self.i2c_commands.LOOP_OPTION1_MSB)
        self.i2c_controller.cvo(response=i2c.CVO_RESP_NR,timer=i2c.CVO_TIMER_64MS, cvo_en=i2c.CVO_CV_ONLY_MODE)
        self.i2c_controller.vben(self.i2c_commands.VBEN_ON)
        
        match self.innopro_family:
            case InnoProFamily.Inno5Pro:
                if self.sr_zvs_enable == 'Yes':
                    self.i2c_controller.sr_zvs(sr_zvs_en=True, fwd_valley_switch_en=True, 
                                            on_time_count=self.sr_zvs_on_count, delay_time_count=self.sr_zvs_del_count)
                else:
                    self.i2c_controller.sr_zvs(sr_zvs_en=False, fwd_valley_switch_en=False, 
                                            on_time_count=0, delay_time_count=2)
                if self.ccm_dcm_initial == "DCM":
                    self.i2c_controller.dcm_only(enable=True)
                else:
                    self.i2c_controller.dcm_only(enable=False)
                    
                self.i2c_controller.fwd_peak(
                    pre_shift_ns=self.i2c_commands.FWD_PEAK_PRESHIFT_150NS,
                    window_pct=self.i2c_commands.FWD_PEAK_WINDOW_15_35_PCT,
                    fwd_peak_en=self.i2c_commands.FWD_PEAK_ENABLE)
                
                # self.i2c_controller.sr_disable(
                #     sr_on_protection_en=True,
                #     sr_zvs_on_protection_en=True,
                #     protection_threshold_mV=self.i2c_commands.SR_PROTECTION_THRESHOLD_200MV,
                #     bit4_en=False,
                #     bit5_en=False,
                #     unwanted_pulse_protection_en=True,
                #     unwanted_pulse_protection_count=1)
                    
            case InnoProFamily.Inno4Pro:
                if self.ccm_dcm_initial == "DCM":
                    self.i2c_controller.dcm_only(enable=True)
                else:
                    self.i2c_controller.dcm_only(enable=False)

                self.i2c_controller.fwd_peak(
                    pre_shift_ns=self.i2c_commands.FWD_PEAK_PRESHIFT_90NS,
                    window_pct=self.i2c_commands.FWD_PEAK_WINDOW_15_35_PCT,
                    fwd_peak_en=self.i2c_commands.FWD_PEAK_ENABLE)

        self.i2c_controller.cv(self.vout_V)

    def test_loop(self):
        soak = self.soak_time

        self.total_time, self.total_steps = self.estimate_remaining(
            0,0,iout_delays = True, initial_delays = True)
        self.status_report(0, 0,iout_delays=True,initial_delays=True)
        self.input_supply_eload_discharge_sequence()
        # Startup sequence
        if self.coupling == AC_SOURCE_COUPLING.AC:
            self.input_supply.frequency = (self.vin_list[0])[1]
        self.input_supply.set_voltage_with_coupling(
            voltage= (self.vin_list[0])[0], coupling= self.coupling)
        self.source_vout = (self.vin_list[0])[0] 

        # Turn on the AC source with the current parameters
        self.input_supply.turn_on()
        
        # Sleep for a short time to allow the power supply to stabilize 
        sleep(3)
        
            # Send necessary I2C commands
        self.i2c_initialize()
        
        # Sleep for a short time to allow the power supply to stabilize 
        sleep(2)

        # Loop through each load current level
        for self.iout_index, iout_level in enumerate(self.iout_list_A):
            # Trim the trailing zeros
            iout_A = float(f'{round(iout_level,6):g}')
            self.load_pct = self.load_pct_list[self.iout_index]
            
            self.electronic_load.set_load(self.vout_V,iout_A,self.eload_type)
            self.electronic_load.turn_on()
            
            if iout_A < 0.05:
                if self.power_meter_load:
                    self.power_meter_load.set_current_range(0.05)
            else:
                if self.power_meter_load:
                    self.power_meter_load.current_auto_range_enable()

            # Sleep for a short time to allow the power supply to stabilize
            soak.do_soak_per_load()

            # Create a new data series for the plottable objects            
            self.create_new_plot_series()

            # Loop through each line input level
            for vin_index, self.vin_freq in enumerate(self.vin_list):
                self.status_report(vin_index, self.iout_index,iout_delays = False, initial_delays = False)
                
                # Extract the values from the self.vin_freq
                self.input_supply.set_voltage_with_coupling(
                    voltage= self.vin_freq[0], coupling= self.coupling)
                if self.coupling == AC_SOURCE_COUPLING.AC:
                    self.input_supply.frequency = self.vin_freq[1]
                
                # Set the parameter for displaying the set output voltage
                self.test_data.vin_set_V = self.vin_freq[0]
                self.test_data.ac_freq_Hz = self.vin_freq[1]
                self.source_vout = self.vin_freq[0]
                
                # Turn on the AC source with the current parameters
                self.input_supply.turn_on()   
                
                # Wait for a short time after the first input voltage application
                if vin_index == 0:
                    sleep(2)
                    
                # Correct the ac source output, limit to 1V
                self.correct_source_output()            
                
                # Do the initial soak if it is the first input voltage on the list
                if vin_index == 0:
                    soak.do_initial_soak()
                # Or the soak per line if it is not
                else:
                    soak.do_soak_per_line()

                # If ripple is to be measured, run the scope
                # TODO: Verify if working
                if self.measure_ripple:
                    self.oscilloscope.stop()
                    waveform_filename = f"{self.short_title}_{self.vin_freq[0]:g}V{self.coupling}_{self.vout_V:g}V_{iout_A:g}A_{self.dcm_text}_{self.sr_zvs_text}.png"
                    self.oscilloscope.get_screenshot(waveform_filename, self.waveform_filepath) #capture waveform of output voltage with AC coupling
                
                    output_ripple_V = self.oscilloscope.get_measure(1)
                    
                    self.test_data.output_ripple_mV = output_ripple_V * 1000
                    self.oscilloscope.run()
                    sleep(1)
                
                if self.power_meter_load and getattr(self.power_meter_load, '_current_auto_range_status', False):
                    self.power_meter_load.auto_range_enable(False)
                    sleep(1)
                if self.power_meter_source and getattr(self.power_meter_source, '_current_auto_range_status', False):
                    self.power_meter_source.current_auto_range_enable(False)
                    sleep(1)
                # TODO: Synchronize the integration
                # Gather the data from the equipment
                self.test_data.gather_data(coupling = self.coupling)
                
                self.output_dataframe.loc[len(self.output_dataframe)]\
                    = self.process_data_row()
                
                # Update the data for the results page
                self.update_output_data()

            # Get anchor        
            if self.iout_index > 0:
                anchor = f"A{5+1+self.iout_index*(len(self.vin_list)+4)}"
            else:
                anchor = "A5"
                
            if self.power_meter_load:
                self.power_meter_load.auto_range_enable()
            if self.power_meter_source:
                self.power_meter_source.current_auto_range_enable()
            # Add a blank row
            self.test_data_table.add_blank_row()

            # export data to excel per line input
            # TODO: Consistency of 'Test Data' text needed
            export_to_excel(
                self.output_dataframe, self.output_folder_path, 
                self.data_filename, self.sheet_name, anchor) 
            # Clear data list for next loop 
            self.output_dataframe=self.output_dataframe[0:0]

                
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
        
        text = f"{self.title}: {round(self.vout_V,3):g}V, {round(self.i_max_A,3):g}A\n" 
        text += f"Family: {self.innopro_family}, "
        match self.innopro_family:
            case InnoProFamily.Inno5Pro:
                text += f"Operation: {self.dcm_text} {self.sr_zvs_text}\n"
            case InnoProFamily.Inno4Pro:
                text += f"Operation: {self.dcm_text}\n"
        
        if self.status in [TestStatus.STOPPED, TestStatus.FAILED, TestStatus.COMPLETE, TestStatus.SKIPPED]:
            text += f"{self.status}\n"
        else:
            text += f"{self.status}: {self.estimated_time_txt}, {self.progress_txt}\n"
            
        text += f"Line Range: {self.line_range.name}, Load Range: {self.load_range_pct.name}, Coupling: {self.coupling}\n"
        
            
        if self.measure_ripple:
            text += "Output Ripple Measurement: Enabled\n"
        else:
            text += "Output Ripple Measurement: Disabled\n"
        
        if self.use_eload_data:
            text += "Load Measurement: Electonic Load"
        else:
            text += "Load Measurement: Power Meter"
            
        self.test_list_text = text

    def unpack_test_item(self):
        """Extract the needed information from the TestItem object"""

        test_item = self.test_item

        self.parent:MainWindow = test_item.parent
        self.equipment:EquipmentHandler = self.parent.equipment
        self.i2c_controller = self.equipment.i2c_controller
        # Type of test. See TEST_TYPE class
        self.test_type_index = test_item.test_type_index

        # Test Conditions Object
        self.test_conditions:TestConditions = test_item.test_conditions

        # General PSU Test Options
        self.general_options:GeneralOptions = self.test_conditions.general_options
        self.measure_ripple:bool = self.general_options.measure_ripple
        self.eload_type:str = self.general_options.eload_type
        self.use_eload_data:bool = self.general_options.use_eload_data
        self.load_direction:str = self.general_options.load_direction
        self.coupling:str = self.general_options.coupling

        self.i2c_test_conditions = self.test_conditions.i2c_test_parameters
        
        # Inno-pro Family
        self.innopro_family = self.i2c_test_conditions.cbx_param[4-1]
        
        # Update controller based on Inno-Pro Family
        self.i2c_controller.update_controller(self.innopro_family)
        
        self.i2c_commands = self.i2c_controller.commands
        self.i2c_params = self.i2c_controller.params
        self.i2c_defaults = self.i2c_controller.defaults

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
            # self.oscilloscope.setup_ripple()
            pass

        if self.power_meter_load is not None:
            self.power_meter_load.integration_settings(
                mode="NORMAL", timer_s=self.soak_time.integration_time)
            self.power_meter_load.stop_integration()
            self.power_meter_load.reset_integration()

        if self.power_meter_source is not None:
            self.power_meter_source.integration_settings(
                mode="NORMAL", timer_s=self.soak_time.integration_time)
            self.power_meter_source.stop_integration()
            self.power_meter_source.reset_integration()
        
        # TODO: Set base settings such as coupling, averaging, rates
        # I2C controller object
        self.i2c_controller:pat_tool.InnoProI2CControllerContainer \
            = self.equipment.i2c_controller
            
        # Update controller based on Inno-Pro Family
        self.i2c_controller.update_controller(self.innopro_family)
        
        self.i2c_commands = self.i2c_controller.commands
        self.i2c_params = self.i2c_controller.params
        self.i2c_defaults = self.i2c_controller.defaults
        
        self.i2c_controller.close()
        self.i2c_controller.reset()

        self.electronic_load.turn_off()
        self.electronic_load.reset_values()
    
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
        match self.innopro_family:
            case InnoProFamily.Inno5Pro:
                self.data_filename = f'{self.title} Test {self.vout_V:g}V {self.dcm_text} {self.sr_zvs_text} {self.innopro_family}'
            case InnoProFamily.Inno4Pro:
                self.data_filename = f'{self.title} Test {self.vout_V:g}V {self.dcm_text} {self.innopro_family}'
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

    def prepare_test_conditions(self):
        """Prepare the list of conditions to be used."""
        test_conditions = self.test_conditions
        
        # Generate a list of the input line voltage
        self.vin_list = test_conditions.line_range.vin_freq
        
        # Nominal output settings
        self.nominal_output_voltage_V = self.i2c_test_conditions.param[0]
        self.nominal_load_current_A = round(self.i2c_test_conditions.param[1],6)
        
        # CDC setpoint
        self.cdc_mV = self.i2c_test_conditions.param[2]

        # SR-ZVS & DCM Only
        match self.innopro_family:
            case InnoProFamily.Inno5Pro:
                self.sr_zvs_enable = self.i2c_test_conditions.cbx_param[1-1]
                self.ccm_dcm_initial = self.i2c_test_conditions.cbx_param[2-1]
                self.sr_zvs_on_count = self.i2c_test_conditions.param[9-1]
                self.sr_zvs_del_count = self.i2c_test_conditions.param[10-1]
                
                if self.sr_zvs_enable == 'Yes':
                    self.sr_zvs_text = 'SR-ZVS'
                else:
                    self.sr_zvs_text = 'QR'
                if self.ccm_dcm_initial == "DCM":
                    self.dcm_text = 'DCM Only'
                else:
                    self.dcm_text = 'CCM Allowed'
                    
            case InnoProFamily.Inno4Pro:
                self.ccm_dcm_initial = self.i2c_test_conditions.cbx_param[2-1]
                
                if self.ccm_dcm_initial == "DCM":
                    self.dcm_text = 'DCM Only'
                else:
                    self.dcm_text = 'CCM Allowed'

        
        self.i_max_A = self.nominal_load_current_A
        self.vout_V = self.nominal_output_voltage_V
        
        # Make all voltages in spec with Inno5Pro resolution

        trim_to_spec(self.vout_V,self.i2c_params.CV_RESOLUTION_MV/1000)
        
        self.test_conditions.nominal_output_voltage_V = self.vout_V
        self.test_conditions.nominal_load_current_A = self.i_max_A
        self.test_conditions.max_load_current_A = self.i_max_A
        
        #Generate a list of the load percent list
        self.load_pct_list = test_conditions.load_range.check_load_direction(self.general_options.load_direction)
        
        # Generate a list of output current using the load percent list
        self.iout_list_A = [load_pct * self.i_max_A/100 \
             for load_pct in self.load_pct_list]
        
    def define_data_header(self):
        """Defines the data header for the excel file."""  
        header_list = [
            'Load',f'V{self.coupling} (rms)','Freq (Hz)',
            'Vin (rms)','Iin (mA)',
            'Pin (W)','PF','%THD','Vo (V)','Io (A)','Po (W)',
            '%V Reg','Efficiency','V Reg(5%)']

        if self.measure_ripple:
            header_list.append('PTP (mV)')
        return header_list
    
    def process_data_row(self):
        """Create a row of data from the test data"""
        td = self.test_data
        data_row = [
            self.load_pct, td.vin_set_V, td.ac_freq_Hz, td.vin_V, 
            td.iin_mA,td.pin_W, td.PF, td.thd_pct, 
            td.vout_V, td.iout_A, td.pout_W, td.vreg_pct,
            td.eff_pct,td.vreg_passfail]
        if self.measure_ripple:
            data_row.append(td.output_ripple_mV)
            
        return data_row

    # Signals for reporting
    def status_report(self, vin_index, load_index, iout_delays,initial_delays):
                
        remaining_time_s, remaining_steps = self.estimate_remaining(vin_index, load_index, iout_delays,initial_delays)
        percent_completion = round((1 - remaining_steps/self.total_steps)*100,0)

        self.estimated_time.emit(remaining_time_s)
        self.progress.emit(percent_completion)

    def estimate_remaining(self, vin_index_t, iout_index_t, iout_delays:bool = True, initial_delays:bool = True):

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
            nonlocal iout_index_t
            nonlocal iout_delays

            # Only add time if the index
            if not start_adding_time:
                if iout_index == iout_index_t:
                    if vin_index == vin_index_t:
                        start_adding_time = True
                        iout_delays = True            
            if start_adding_time:
                remaining_time_s += t
                if add_step:
                    remaining_steps += 1

            return remaining_steps, remaining_time_s
        
        if initial_delays:
            # Startup sequence
            add_time(3)
            add_time(3)
            add_time(3)
            
        for iout_index, _ in enumerate(self.iout_list_A):
            
            if iout_delays:
                add_time(soak.soak_per_load)
        
            for vin_index, _ in enumerate(self.vin_list):
                
                add_time(2,True) 
                
                # Do the initial soak if it is the first input voltage on the list
                if vin_index == 0:
                    add_time(soak.initial_soak)
                # Or the soak per line if it is not
                else:
                    add_time(soak.soak_per_line)            

                    # Sleep for the soak time before measuring
                add_time(soak.integration_time)
                add_time(1.7)
                if self.measure_ripple:
                    add_time(1)
                
        add_time(3)
        
        return remaining_time_s, remaining_steps
    
    def plot_charts(self):
        """Add a Chart on the output workbook for this test item."""
        self.wb = openpyxl.load_workbook(self.data_file_path)

        generate_plots_LineReg(
            vout = self.vout_V,
            iout = self.i_max_A,
            num_step = len(self.load_pct_list),
            vin_step = len(self.vin_list),
            coupling = self.coupling,
            wb = self.wb,
            sheet_name = self.sheet_name,
            wb_filepath = self.data_file_path,
            usb_pd_flag = False)

        generate_plots_LinevEff(
            vout = self.vout_V,
            iout = self.i_max_A,
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

        vin_min = 10000
        vin_max = 0

        vin_list = [vin[0] for vin in self.vin_list]
        vin_min, vin_max = min(vin_list), max(vin_list)

        # Plottable Objects
        self.efficiency_vs_line_plot = PlottableObject(
            title="Efficiency vs Line",
            type=PlotType.LINE,
            x_label="Line Voltage (V)",
            y_label="Efficiency (%)",
            x_range=(vin_min, vin_max),
            y_range=(80, 100),
            plot_series_list=[])
        
        nom_vout_V = self.vout_V
        self.line_reg_plot = PlottableObject(
            title="Line Regulation",
            type=PlotType.LINE,
            x_label="Line Voltage (V)",
            y_label="Output Voltage (V)",
            x_range=(vin_min, vin_max),
            y_range=(nom_vout_V*0.9, nom_vout_V*1.1),
            plot_series_list=[])
        
        if self.measure_ripple:
            self.ripple_vs_line_plot = PlottableObject(
                title="Ripple vs Line",
                type=PlotType.LINE,
            x_label="Line Voltage (V)",
                y_label="Output Ripple (mV)",
            x_range=(vin_min, vin_max),
                y_range=(0, 500),
                plot_series_list=[])

        self.test_data_table = DataTable(
            header=self.header_list, data=[])

        self.with_data = True

    def create_new_plot_series(self):
        """Create a new data series for each plottable object
        with the current input voltage as name."""
        self.efficiency_vs_line_plot.add_plot_series(
            name=f'{self.iout_list_A[self.iout_index]:3g} A',
            x_values=[],
            y_values=[])

        self.line_reg_plot.add_plot_series(
            name=f'{self.iout_list_A[self.iout_index]:3g} A',
            x_values=[],
            y_values=[])
        
        if self.measure_ripple:
            self.ripple_vs_line_plot.add_plot_series(
            name=f'{self.iout_list_A[self.iout_index]:3g} A',
                x_values=[],
                y_values=[])

    def update_output_data(self):
        """Update the plots and numeric data
        Emit a signal containing the processed info"""

        td = self.test_data

        # Plottable objects processing
        plottables = []

        self.efficiency_vs_line_plot.append_plot_data(
            plot_index=self.iout_index,
            x=td.vin_set_V,
            y=td.eff_pct)
        plottables.append(self.efficiency_vs_line_plot)
        
        self.line_reg_plot.append_plot_data(
            plot_index=self.iout_index,
            x=td.vin_set_V,
            y=td.vout_V)
        plottables.append(self.line_reg_plot)
        
        if self.measure_ripple:
            self.ripple_vs_line_plot.append_plot_data(
                plot_index=self.iout_index,
                x=td.vin_set_V,
                y=td.output_ripple_mV)
            plottables.append(self.ripple_vs_line_plot)
            
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
            'I2C_PARAMS':                          self.test_conditions.i2c_test_parameters.param,
            'I2C_CBX_PARAMS':                      self.test_conditions.i2c_test_parameters.cbx_param,
            'NAME':                                self.test_conditions.name}
        return d
    
    @staticmethod
    def extract_test_condition(test_item_dict:dict)->dict:
        test_object_class = I2C_LineRegTest
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
            usbpd_options=test_object_class.tc_default.usbpd_options,
            line_ramp_settings= test_object_class.tc_default.line_ramp_settings,
            i2c_test_parameters=I2CTestParameters(
                params = test_item_dict['I2C_PARAMS'],
                cbx_params = test_item_dict['I2C_CBX_PARAMS']),
            name=test_item_dict['NAME'])
        return new_test_conditions
    