from psu_tests.test_object_imports import *

#for harmonic order 2,3,5,7...39, for harmonic order 2, %limit is 30*PF
ClassC_percent_limit = [
    0, 2, 30, 10, 7, 5, 3, 3, 3, 3, 
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3] 
#for harmonic order ,3,5,7...39, limit is Pin*element of list
ClassD_mA_limit = [
    0, 0, 3.4, 1.9, 1, 0.5, 0.35, 0.29, 
    0.25, 0.22, 0.2, 0.18, 0.16, 0.15,
    0.14, 0.13, 0.12, 0.11, 0.11, 0.1, 0.09] 

class InputHarmonicsTest(BaseTestObject):
    """
    The Input Harmonics test computes the harmonic content for a specific load
    and voltage until unit restarts
    """
    title = "Input Harmonics"
    short_title = "InHarm"

    # General UI Definitions
    ui_definitions = General_UI_Definitions()
    ui_definitions.stack_page_1 = StackWidget1Pages.LineVoltageRange
    ui_definitions.stack_page_2 = StackWidget2Pages.LoadCurrentRange
    ui_definitions.stack_page_3 = StackWidget3Pages.USBPD_Options

    ui_definitions.usb_pd_device_toggle_visible = True
    ui_definitions.nominal_iout_visible = True
    ui_definitions.nominal_vout_visible = True
    ui_definitions.nominal_vout_enable = True
    ui_definitions.coupling_visible = False

    ui_definitions.load_type_visible = True
    ui_definitions.load_direction_cbx_enabled = False
        
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
    ui_update.measure_ripple_update = False
    ui_update.load_direction_update = False
    ui_update.eload_type_update = True
    ui_update.use_eload_data_update = True
    ui_update.coupling_update = True
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
        """Return a UI update definition."""
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
        self.total_time, self.total_steps = self.estimate_remaining(0)
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

    def with_waveform_capture(self):
        return False

    def test_loop(self):
        soak = self.soak_time

        self.total_time, self.total_steps = self.estimate_remaining(0)
        self.status_report(0)
        if self.usbpd_test:
            self.input_supply_eload_discharge_sequence()
        # Loop through each line input level
        for self.vin_index, self.vin_freq in enumerate(self.vin_list): 
            self.status_report(self.vin_index)
            # Extract the values from the self.vin_freq
            self.input_supply.set_voltage_with_coupling(voltage= self.vin_freq[0], coupling= self.coupling)  
            if self.coupling == AC_SOURCE_COUPLING.AC:
                self.input_supply.frequency = self.vin_freq[1]
            
            # Set the parameter for displaying the set output voltage
            self.test_data.vin_set_V = self.vin_freq[0]
            self.test_data.ac_freq_Hz = self.vin_freq[1]
            self.source_vout = self.vin_freq[0]

            # Turn on the AC source with the current parameters
            self.input_supply.turn_on()

            if self.power_meter_load:
                self.power_meter_load.auto_range_enable()
            if self.power_meter_source:
                self.power_meter_source.current_auto_range_enable()

            # Sleep for a short time to allow the power supply to stabilize 
            sleep(3)

            # If the power supply is for USBPD, 
            # request the PDO for the test condition
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
                if self.tracking_pdo_requests:
                    self.usb_pd_request(vout_V=self.vout_V, 
                        iout_A=self.i_out_A)
                else:
                    self.usb_pd_request(vout_V=self.vout_V, 
                        iout_A=self.i_rated_A)         
            
            # Set the e-load to the maximum load level to be tested 
            # and turn it on
            self.electronic_load.set_load(
                self.vout_V,self.i_out_A,self.eload_type)
            self.electronic_load.turn_on()
            
            if self.i_out_A < 0.05:
                if self.power_meter_load:
                    self.power_meter_load.set_current_range(0.05)
            else:
                if self.power_meter_load:
                    self.power_meter_load.current_auto_range_enable()
            
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
            
            # Gather the data from the equipment            
            if self.power_meter_load and getattr(self.power_meter_load, '_current_auto_range_status', False):
                self.power_meter_load.auto_range_enable(False)
                sleep(1)
            if self.power_meter_source and getattr(self.power_meter_source, '_current_auto_range_status', False):
                self.power_meter_source.current_auto_range_enable(False)
                sleep(1)
            
            self.test_data.gather_data(coupling=self.coupling,usb_pd=self.usbpd_test)
            
            self.output_dataframe.loc[len(self.output_dataframe)]\
                = self.process_data_row()
            #Get harmonic components
            self.harmonics_mA, self.harmonics_percent \
                = self.power_meter_source.get_harmonics()
            if self.power_meter_load:
                self.power_meter_load.auto_range_enable()
            if self.power_meter_source:
                self.power_meter_source.current_auto_range_enable()
                
            #Create harmonics table
            self.harmonics_list = self.create_harmonics_table()

            # Get anchor
            anchor = f"B{5+self.vin_index*(2+2+len(ClassC_percent_limit)+4+1)}"
            harmonics_anchor = f"B{9+self.vin_index*(len(ClassC_percent_limit)+4+2+2+1)}"
            
            # export data to excel per line input
            # TODO: Consistency of 'Test Data' text needed
            export_to_excel(
                self.output_dataframe, self.output_folder_path, 
                self.data_filename,self.sheet_name, anchor)
            export_to_excel(
                self.harmonics_list,self.output_folder_path, 
                self.data_filename,self.sheet_name, harmonics_anchor)
            
            # Clear data list for next loop
            self.output_dataframe=self.output_dataframe[0:0]
            self.harmonics_list = self.harmonics_list[0:0]
            self.output_dataframe.loc[len(self.output_dataframe)] = self.header_list
            self.harmonics_list.loc[len(self.harmonics_list)] = self.harmonics_header_list
            
    def create_harmonics_table(self):
        h_pct = self.harmonics_percent
        h_mA = self.harmonics_mA
        h_list = self.harmonics_list

        
        for order in range(len(h_mA)):
            #1st order
            if (order+1==1): 
                # print([order+1, h_mA[order],None,None,None,None])
                h_list.loc[len(h_list)] \
                    = [order+1, h_mA[order],None,None,None,None]

            #2nd order
            elif (order+1==2): 
                if (h_pct[order] <= ClassC_percent_limit[order]):
                    harmonics_stat = 'PASS'
                else:
                    harmonics_stat = 'FAIL'
                h_list.loc[len(h_list)] \
                    = [order+1, h_mA[order],h_pct[order],None,
                       ClassC_percent_limit[order],harmonics_stat]
            #3rd order
            elif (order+1==3):  
                if (h_pct[order] \
                    <= ClassC_percent_limit[order]*self.test_data.PF) \
                        & (h_mA[order] <= ClassD_mA_limit[order]*self.test_data.pin_W):
                    harmonics_stat = 'PASS'
                else:
                    harmonics_stat = 'FAIL'
                h_list.loc[len(h_list)]\
                    = [order+1, h_mA[order],h_pct[order],
                       ClassD_mA_limit[order]*self.test_data.pin_W,
                       ClassC_percent_limit[order]*self.test_data.PF,
                       harmonics_stat]

            #odd harmonics starting at 5th order
            elif ((order+1)%2 != 0) & (order+1> 3) & (order + 1 < 40): 
                if (h_pct[order] \
                    <= ClassC_percent_limit[2+round((order+1-3)/2)]) & (h_mA[order] <= ClassD_mA_limit[2+round((order+1-3)/2)] * self.test_data.pin_W):
                    harmonics_stat = 'PASS'
                else:
                    harmonics_stat = 'FAIL'
                h_list.loc[len(h_list)]= [order+1, h_mA[order],h_pct[order],ClassD_mA_limit[2+round((order+1-3)/2)]*self.test_data.pin_W,ClassC_percent_limit[2+round((order+1-3)/2)],harmonics_stat]
        
        return h_list

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
            
        text += f"Line Range: {self.line_range.name}, Load Range: {self.load_range_pct.name}\n"

        if self.tracking_pdo_requests:
            text += "Current Request Tracking: Enabled\n"
        else:
            text += "Current Request Tracking: Disabled\n"
        
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
        self.tracking_pdo_requests:bool = self.usbpd_options.tracking_pdo_request
        
        # General PSU Test Options
        self.general_options:GeneralOptions = self.test_conditions.general_options
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
        self.input_supply = self.equipment.ac_source
        self.power_meter_source = self.equipment.power_meter_source
        self.power_meter_load = self.equipment.power_meter_load_1
        self.electronic_load = self.equipment.electronic_load_1
        self.usbpd_sink = self.equipment.usbpd_sink
        self.oscilloscope = self.equipment.oscilloscope

        
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

        if self.electronic_load is not None:
            self.electronic_load.reset_values()

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
        self.harmonics_header_list = ['nth order','mA content', '%% content', 'ma Limit', '%% Limit', 'Remarks'] 
        self.harmonics_list=dataframe_from_headers(self.harmonics_header_list)
        
        if not os.path.exists(self.output_folder_path):
            os.mkdir(self.output_folder_path)
        self.data_filename = f"{self.title} Test {self.vout_V:g}V"
        self.data_file_path = f'{self.output_folder_path}/{self.data_filename}.xlsx'
        
        # Check if workbook exists
        if not os.path.exists(self.data_file_path):     
            self.wb:Workbook = openpyxl.Workbook()
            self.wb.save(self.data_file_path)
            self.wb.close()
            
        # Open the workbook    
        self.wb:Workbook = openpyxl.load_workbook(self.data_file_path)
        
        # Prepare the sheet name
        self.sheet_name = f"Input_Harmonics_{self.coupling}_{round(self.vout_V,3):g}V_{round(self.i_out_A,3):g}A"

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
        # self.define_output_data_objects()
        
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
        
        # Nominal levels
        self.i_max_A = test_conditions.nominal_load_current_A
        self.vout_V = test_conditions.nominal_output_voltage_V
        self.i_rated_A = test_conditions.max_load_current_A
        
        #Generate a list of the load percent list
        self.load_pct_list = test_conditions.load_range.check_load_direction(self.general_options.load_direction)
        
        # Generate a list of output current using the load percent list
        self.iout_list_A = [load_pct * self.i_max_A/100 \
             for load_pct in self.load_pct_list] 
        
        self.i_out_A = self.iout_list_A[0]
        
    def define_data_header(self):
        """Defines the data header for the excel file."""  
        header_list = [
            f'V{self.coupling} (rms)','Freq (Hz)','Vin (rms)','Iin (mA)',
            'Pin (W)','PF','%THD','Vo (V)','Io (A)','Po (W)',
            '%V Reg','Efficiency','V Reg(5%)']
        return header_list
    
    def process_data_row(self):
        """Create a row of data from the test data"""
        data_row = [
            self.test_data.vin_set_V, self.test_data.ac_freq_Hz, self.test_data.vin_V, 
            self.test_data.iin_mA,self.test_data.pin_W, self.test_data.PF, self.test_data.thd_pct, 
            self.test_data.vout_V, self.test_data.iout_A, self.test_data.pout_W, self.test_data.vreg_pct,
            self.test_data.eff_pct,self.test_data.vreg_passfail]           
        return data_row
    
     # Signals for reporting
    def status_report(self, vin_index):
                
        remaining_time_s, remaining_steps = self.estimate_remaining(vin_index)
        percent_completion = round((1 - remaining_steps/self.total_steps)*100,0)

        self.estimated_time.emit(remaining_time_s)
        self.progress.emit(percent_completion)

    def estimate_remaining(self, vin_index_t):

        soak = self.soak_time

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

            # Only add time if the index
            if not start_adding_time:
                if vin_index == vin_index_t:
                    start_adding_time = True
            
            if start_adding_time:
                remaining_time_s += t
                if add_step:
                    remaining_steps += 1

            return remaining_steps, remaining_time_s
        
        add_time(1)
        for vin_index, _ in enumerate(self.vin_list):
            
            add_time(3,True) 
            
            if self.usbpd_test:     
                add_time(2)
            
            # Do the initial soak if it is the first input voltage on the list
            if vin_index == 0:
                add_time(soak.initial_soak)
            # Or the soak per line if it is not
            else:
                add_time(soak.soak_per_line)            

            # Sleep for the soak time before measuring
            add_time(soak.integration_time)
            add_time(1.7)
            add_time(4)
                
        add_time(3)
        
        return remaining_time_s, remaining_steps
    
    def plot_charts(self):
        """Add a Chart on the output workbook for this test item."""
        self.wb = openpyxl.load_workbook(self.data_file_path)

        generate_plots_InputHarmonics(
            vout = self.vout_V,
            iout = self.i_out_A,
            vin_step = len(self.vin_list),
            wb = self.wb,
            sheet_name = self.sheet_name,
            wb_filepath = self.data_file_path,)
        
        self.wb.close()
        
    
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
            'USBPD_OPTIONS_usbpd_test':            self.test_conditions.usbpd_options.usbpd_test,
            'USBPD_OPTIONS_tracking_pdo_request':  self.test_conditions.usbpd_options.tracking_pdo_request,
            'USBPD_OPTIONS_pdo_type':              self.test_conditions.usbpd_options.pdo_type,
            'USBPD_OPTIONS_augmented_type':        self.test_conditions.usbpd_options.augmented_type,
            'NAME':                                self.test_conditions.name}
        return d
    
    @staticmethod
    def extract_test_condition(test_item_dict:dict)->dict:
        test_object_class = InputHarmonicsTest
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
                coupling=test_object_class.tc_default.general_options.coupling),
            usbpd_options=USBPDOptions(
                usbpd_test=test_item_dict['USBPD_OPTIONS_usbpd_test'],
                tracking_pdo_request=test_item_dict['USBPD_OPTIONS_tracking_pdo_request'],
                pdo_type=test_item_dict['USBPD_OPTIONS_pdo_type'],
                augmented_type=test_item_dict['USBPD_OPTIONS_augmented_type']),
            line_ramp_settings=test_object_class.tc_default.line_ramp_settings,
            i2c_test_parameters=test_object_class.tc_default.i2c_test_parameters,
            name=test_item_dict['NAME'])
        return new_test_conditions