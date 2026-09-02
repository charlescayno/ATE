from psu_tests.test_object_imports import *

class InputLineRampTest(BaseTestObject):
    """
    The Input Line Ramp test sweeps the line input at a given slew rate    
    """
    title = "Input Line Ramp"
    
    # General UI Definitions
    ui_definitions = General_UI_Definitions()
    ui_definitions.stack_page_1 = StackWidget1Pages.LineRamp
    ui_definitions.stack_page_2 = StackWidget2Pages.EmptyPage
    ui_definitions.stack_page_3 = StackWidget3Pages.USBPD_Options

    ui_definitions.usb_pd_device_toggle_visible = True
    ui_definitions.nominal_iout_visible = True
    ui_definitions.nominal_vout_visible = True
    ui_definitions.nominal_vout_enable = True
    ui_definitions.load_type_visible = True

        
    # General UI Update Definitions
    ui_update = General_UI_Update_Definitions()
    ui_update.line_settings_update = False
    ui_update.load_settings_update = False
    ui_update.soaktime_settings_update = False
    ui_update.cvcc_settings_update = False
    ui_update.line_ramp_settings_update = True
    ui_update.nominal_output_settings_update = True
    ui_update.usbpd_options_update = True
    ui_update.tracking_pdo_request_update = False
    ui_update.measure_ripple_update = False
    ui_update.load_direction_update = False
    ui_update.eload_type_update = True
    ui_update.use_eload_data_update = True
    ui_update.coupling_update = False
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
        max_load_current_A=5,
        line_range= LineSettings.UNIVERSAL,
        load_range= LoadSettings.LOAD_SINGLE_VALUE_100_PCT,
        soak_time= SoaktimeSettings.SOAK_INPUT_HARMONICS,
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
        self.total_time, self.total_steps = self.estimate_remaining(0, initial_delays = True)
        self.estimated_time_s = self.total_time
        self.message_closed = False

    def run(self):
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
            # If there is an unhandled error inside the loop
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
            #self.plot_charts()
            self.cleanup_usbpd_pps_operation()
            self.input_supply_eload_discharge_sequence()
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
        
    def with_waveform_capture(self):
        if self.test_conditions.general_options.measure_ripple:
            return True
        else:
            return False
        
    def test_loop(self):
        global test_control_flags
        self.total_time, self.total_steps = self.estimate_remaining(0, initial_delays = True)
        self.status_report(0, initial_delays=True)
        if self.usbpd_test:
            self.input_supply_eload_discharge_sequence()
        self.input_supply.set_voltage_with_coupling(voltage= self.vin_list[0][0], coupling= self.coupling)  
        
        if self.coupling == AC_SOURCE_COUPLING.AC:
            self.input_supply.frequency = self.freq
        
        self.input_supply.ac_slew_rate = 9.9e37    
        self.input_supply.dc_slew_rate = 9.9e37   
        self.input_supply.freq_slew_rate = 9.9e37   
        
        # Turn on the AC source with the current parameters
        self.input_supply.turn_on()
        
        # Sleep for a short time to allow the power supply to stabilize 
        sleep(3)
        

        self.electronic_load.set_load(self.vout_V,self.i_max_A,self.eload_type)
        self.electronic_load.turn_on()
        
        if self.i_max_A < 0.05:
            if self.power_meter_load:
                self.power_meter_load.set_current_range(0.05)
        else:
            if self.power_meter_load:
                self.power_meter_load.current_auto_range_enable()
            
        # Sleep for a short time to allow the power supply to stabilize 
        sleep(2)
        
        # Loop through each line input level
        for vin_index, vin_slew in enumerate(self.vin_list):
            
            self.status_report(vin_index, initial_delays = False)
            self.input_supply.set_voltage_with_coupling(voltage= vin_slew[0], coupling= self.coupling)  
            self.input_supply.turn_on()
            sleep(2)
            
            if self.coupling == 'DC':
                self.input_supply.dc_slew_rate = vin_slew[1]

            else:
                self.input_supply.ac_slew_rate = vin_slew[1]  
            
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
                self.usb_pd_request(vout_V=self.vout_V, 
                    iout_A=self.i_rated_A)
            
            if vin_index < len(self.vin_list) - 1:
                vin_next = (self.vin_list[vin_index+1])[0]
                
            else:   
                vin_next = vin_slew[0]
                 
            vin = vin_slew[0]
            
            self.input_supply.set_voltage_with_coupling(voltage= vin_next, coupling= self.coupling)  
            
            self.input_supply.turn_on()
                
            #print('slope start')
            while (abs(vin_next - vin) >= (vin_next*0.01)):
                sleep(1)
                vin = self.power_meter_source.voltage
                # print(vin)
                if test_control_flags['StopTest'] == True:
                    raise TestStopped
                if test_control_flags['SkipTest'] == True:
                    raise TestSkipped
                
            self.test_data.gather_data(measure_thd=False, coupling=self.coupling,usb_pd=self.usbpd_test)    
            self.output_dataframe.loc[len(self.output_dataframe)]\
                = self.process_data_row()
            
        # Get anchor        
        anchor = f"B{5}"
            
        # export data to excel per line input
        # TODO: Consistency of 'Test Data' text needed
        export_to_excel(
            self.output_dataframe, self.output_folder_path, 
            self.data_filename, self.sheet_name, anchor) 
        # Clear data list for next loop 
        self.output_dataframe=self.output_dataframe[0:0]
        
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
                
    def input_supply_eload_discharge_sequence(self):
        self.equipment.input_supply_eload_discharge_sequence(self.i_max_A/3,coupling=self.coupling)

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
            
        text += f"Line Range: {self.line_ramp_settings.name}, Coupling: {self.coupling}\n"
        
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

        # Type of test. See TEST_TYPE class
        self.test_type_index = test_item.test_type_index

        # Test Conditions Object
        self.test_conditions:TestConditions = test_item.test_conditions

        # USBPD Options
        self.usbpd_options:USBPDOptions = self.test_conditions.usbpd_options
        self.usbpd_test:bool = self.usbpd_options.usbpd_test

        # General PSU Test Options
        self.general_options = self.test_conditions.general_options
        self.eload_type:str = self.general_options.eload_type
        self.use_eload_data:bool = self.general_options.use_eload_data
        
        # Input Line Ramp Settings
        self.line_ramp_settings:LineRamp = self.test_conditions.line_ramp_settings

        # Nominal settings
        self.nominal_load_current_A:float = self.test_conditions.nominal_load_current_A
        self.nominal_output_voltage_V:float = self.test_conditions.nominal_output_voltage_V

        # Test progress in percent
        self.test_progress:float = 0 
        self.test_complete:bool = False
    
    @timeit
    def setup_equipment(self):
        """Set up the assignment and initialization of equipment"""
        self.input_supply = self.equipment.ac_source
        self.power_meter_source = self.equipment.power_meter_source
        self.power_meter_load = self.equipment.power_meter_load_1
        self.electronic_load = self.equipment.electronic_load_1
        self.usbpd_sink = self.equipment.usbpd_sink
        self.oscilloscope = self.equipment.oscilloscope

        
        if self.power_meter_load is not None:
            self.power_meter_load.integration_settings(
                mode="NORMAL", timer_s=0)
            self.power_meter_load.stop_integration()
            self.power_meter_load.reset_integration()

        if self.power_meter_source is not None:
            self.power_meter_source.integration_settings(
                mode="NORMAL", timer_s=0)
            self.power_meter_source.stop_integration()
            self.power_meter_source.reset_integration()

        if self.electronic_load is not None:
            self.electronic_load.reset_values()
        



        # TODO: Set base settings such as coupling, averaging, rates
    
    @timeit
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
        self.data_filename = f"{self.title} Test"
        self.data_file_path = f'{self.output_folder_path}/{self.data_filename}.xlsx'
        
        # Check if workbook exists
        if not os.path.exists(self.data_file_path):     
            self.wb:Workbook = openpyxl.Workbook()
            self.wb.save(self.data_file_path)
            self.wb.close()
            
        # Open the workbook    
        self.wb:Workbook = openpyxl.load_workbook(self.data_file_path)
        
        # Prepare the sheet name
        self.sheet_name = f"LineRamp_{self.line_ramp_settings.name}_{self.line_ramp_settings.coupling}_{self.vout_V:g}V_{self.i_max_A:g}A"
        
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
        
        # Generate line ramp settings
        self.vin_list = self.line_ramp_settings.vin_slew
        self.freq = self.line_ramp_settings.freq
        self.coupling = self.line_ramp_settings.coupling
        
        # Nominal levels
        self.i_max_A = test_conditions.nominal_load_current_A
        self.vout_V = test_conditions.nominal_output_voltage_V
        self.i_rated_A = test_conditions.max_load_current_A

        
    def define_data_header(self):
        """Defines the data header for the excel file."""  
        header_list = [
            f'V{self.coupling} (rms)','Freq (Hz)','Vin (rms)','Iin (mA)',
            'Pin (W)','PF','%THD','Vo (V)','Io (A)','Po (W)',
            '%V Reg','Efficiency','V Reg(5%)']
        
        return header_list
    
    def process_data_row(self):
        """Create a row of data from the test data"""
        data_row = [self.test_data.vin_set_V, self.test_data.ac_freq_Hz, self.test_data.vin_V, 
            self.test_data.iin_mA,self.test_data.pin_W, self.test_data.PF, self.test_data.thd_pct, 
            self.test_data.vout_V, self.test_data.iout_A, self.test_data.pout_W, self.test_data.vreg_pct,
            self.test_data.eff_pct,self.test_data.vreg_passfail]
            
        return data_row

    # Signals for reporting
    def status_report(self, vin_index,initial_delays):
                
        remaining_time_s, remaining_steps = self.estimate_remaining(vin_index,initial_delays)
        percent_completion = round((1 - remaining_steps/self.total_steps)*100,0)

        self.estimated_time.emit(remaining_time_s)
        self.progress.emit(percent_completion)

    def estimate_remaining(self, vin_index_t, initial_delays:bool = True):

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
        
        if initial_delays:
            # Startup sequence
            add_time(3)

            add_time(3)
            
            add_time(3)
            
        for vin_index, vin_slew in enumerate(self.vin_list):
            
            add_time(2,True) 
            
            # Time is the slew rate mutliplied by the difference between the initial and final voltage
            if vin_index < len(self.vin_list) - 1: 
                add_time(abs((1/vin_slew[1])*(vin_slew[0] - (self.vin_list[vin_index+1])[0]*0.99)))
            add_time(0.7)
                
        add_time(3)
        
        return remaining_time_s, remaining_steps
    
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
            usb_pd_flag = self.usbpd_options.usbpd_test)

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
    #      Test Item Dictionary creation for saving/loading test items        #
    ###########################################################################
    def get_dict(self)->dict:
        d = {'TEST_TYPE_INDEX':                    self.test_type_index, 
            'NOMINAL_OUTPUT_VOLTAGE_V':            self.test_conditions.nominal_output_voltage_V,
            'NOMINAL_LOAD_CURRENT_A':              self.test_conditions.nominal_load_current_A,
            'MAX_LOAD_CURRENT_A':                  self.test_conditions.max_load_current_A,
            'GENERAL_OPTIONS_measure_ripple':      self.test_conditions.general_options.measure_ripple,
            'GENERAL_OPTIONS_use_eload_data':      self.test_conditions.general_options.use_eload_data,
            'GENERAL_OPTIONS_eload_type':          self.test_conditions.general_options.eload_type,
            'GENERAL_OPTIONS_load_direction':      self.test_conditions.general_options.load_direction,
            'USBPD_OPTIONS_usbpd_test':            self.test_conditions.usbpd_options.usbpd_test,
            'USBPD_OPTIONS_tracking_pdo_request':  self.test_conditions.usbpd_options.tracking_pdo_request,
            'USBPD_OPTIONS_pdo_type':              self.test_conditions.usbpd_options.pdo_type,
            'USBPD_OPTIONS_augmented_type':        self.test_conditions.usbpd_options.augmented_type,
            'LINE_RAMP_SETTINGS_name':             self.test_conditions.line_ramp_settings.name,
            'LINE_RAMP_SETTINGS_vin_slew':         self.test_conditions.line_ramp_settings.vin_slew,
            'LINE_RAMP_SETTINGS_freq':             self.test_conditions.line_ramp_settings.freq,
            'LINE_RAMP_SETTINGS_coupling':         self.test_conditions.line_ramp_settings.coupling,
            'LINE_RAMP_SETTINGS_custom':           self.test_conditions.line_ramp_settings.custom,
            'NAME':                                self.test_conditions.name}
        return d
    
    @staticmethod
    def extract_test_condition(test_item_dict:dict)->dict:
        test_object_class = InputLineRampTest
        new_test_conditions = TestConditions(
            nominal_output_voltage_V=test_item_dict['NOMINAL_OUTPUT_VOLTAGE_V'],
            nominal_load_current_A=test_item_dict['NOMINAL_LOAD_CURRENT_A'],
            max_load_current_A=test_item_dict['MAX_LOAD_CURRENT_A'],
            line_range=test_object_class.tc_default.line_range,
            load_range=test_object_class.tc_default.load_range,
            soak_time=test_object_class.tc_default.soak_time,
            general_options=GeneralOptions(
                measure_ripple=test_item_dict['GENERAL_OPTIONS_measure_ripple'],
                use_eload_data=test_item_dict['GENERAL_OPTIONS_use_eload_data'],
                eload_type=test_item_dict['GENERAL_OPTIONS_eload_type'],
                load_direction=test_item_dict['GENERAL_OPTIONS_load_direction']),
            usbpd_options=USBPDOptions(
                usbpd_test=test_item_dict['USBPD_OPTIONS_usbpd_test'],
                tracking_pdo_request=test_item_dict['USBPD_OPTIONS_tracking_pdo_request'],
                pdo_type=test_item_dict['USBPD_OPTIONS_pdo_type'],
                augmented_type=test_item_dict['USBPD_OPTIONS_augmented_type']),
            line_ramp_settings=LineRamp(
                name = test_item_dict['LINE_RAMP_SETTINGS_name'],
                vin_slew = test_item_dict['LINE_RAMP_SETTINGS_vin_slew'],
                freq = test_item_dict['LINE_RAMP_SETTINGS_freq'],
                coupling = test_item_dict['LINE_RAMP_SETTINGS_coupling'],
                custom = test_item_dict['LINE_RAMP_SETTINGS_custom']),
            i2c_test_parameters = test_object_class.tc_default.i2c_test_parameters,
            name=test_item_dict['NAME'])
        return new_test_conditions    

    