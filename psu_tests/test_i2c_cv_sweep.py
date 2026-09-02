from psu_tests.test_object_imports import *

class I2C_CVSweepTest(BaseTestObject):
    """
    The CV setpoint is sweeped through I2C

    """
    title = "I2C CV Sweep"
    i2c_test = True

    # General UI Definitions
    ui_definitions = General_UI_Definitions()
    ui_definitions.stack_page_1 = StackWidget1Pages.LineVoltageRange
    ui_definitions.stack_page_2 = StackWidget2Pages.EmptyPage
    ui_definitions.stack_page_3 = StackWidget3Pages.I2C_Options

    ui_definitions.test_time_param3_label = 'Soak Per Setpoint (s)'
    ui_definitions.load_type_visible = True

    # I2C UI definitions
    i2c_ui_definitions = I2C_UI_Definitions()
    # Line Edits
    i2c_ui_definitions.add_lineedit(label='Initial Vout (V)', param_index=1)
    i2c_ui_definitions.add_lineedit(label='Final Vout (V)', param_index=2)
    i2c_ui_definitions.add_lineedit(label='Vout Step (V)', param_index=3)
    i2c_ui_definitions.add_lineedit(label='Load Current (A)', param_index=4) 

    i2c_ui_definitions.add_lineedit(label='SR ZVS On',param_index=9)
    i2c_ui_definitions.add_lineedit(label='SR ZVS Delay',param_index=10)
    # Combo box
    i2c_ui_definitions.add_cbx(label="SR ZVS?", contents=['Yes', 'No'], param_index=1)
    i2c_ui_definitions.add_cbx(label="Initial Mode", contents=['CCM', 'DCM'], param_index=2)
    i2c_ui_definitions.add_cbx(label="Inno-Pro Family", contents=InnoProFamilyList, param_index=4)
    
    
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
    ui_update.eload_type_update = True
    ui_update.use_eload_data_update = True
    ui_update.i2c_params_update = True

    @classmethod
    def get_ui_definitions(self, flags:UIChangeFlags = UIChangeFlags()):
        """Return a UI definition based on the UIChangeFlags object."""
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
        self.i2c_ui_definitions.add_lineedit(label='Initial Vout (V)', param_index=1)
        self.i2c_ui_definitions.add_lineedit(label='Final Vout (V)', param_index=2)
        self.i2c_ui_definitions.add_lineedit(label='Vout Step (V)', param_index=3)
        self.i2c_ui_definitions.add_lineedit(label='Load Current (A)', param_index=4) 

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
        max_load_current_A=5,
        line_range= LineSettings.UNIVERSAL,
        load_range= LoadSettings.LOAD_SINGLE_VALUE_100_PCT,
        soak_time= SoaktimeSettings.SOAK_CVCC,
        general_options = GeneralOptions(),
        usbpd_options = USBPDOptions(),
        line_ramp_settings = LineRamp(),
        i2c_test_parameters=I2CTestParameters())
    
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
        self.total_time, self.total_steps = self.estimate_remaining(
            0, 0, vin_delays = True)
        self.estimated_time_s = self.total_time

        self.message_closed = False
        self.with_data = False
        

    
    def with_waveform_capture(self):
        return False

    def run(self):
        if self.parent.run_settings['debug']:
            debugpy.debug_this_thread()
        global test_control_flags
        
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
            print(traceback.format_exc())
            # If there is an unhandled error inside the loop
            self.input_supply_eload_discharge_sequence()
            print("Test Failed")
            self.i2c_controller.close()
            self.status_update.emit(TestStatus.FAILED)

        else:
            # If all goes well
            # Emit a status_update signal to signal that the test is complete
            self.input_supply_eload_discharge_sequence()
            self.plot_charts()
            self.i2c_controller.close()
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
    
    def i2c_initialize(self):
        cmd = self.i2c_commands
        # Reset the registers
        # Not following this sequence may result in high VDS primary stress
        # which may cause the IC to blow up
        
        # Set the CV to the minimum to prevent additional cycle requests if at higher voltage 
        # Enable DCM only to prevent CCM cycles during bleeder enable
        self.i2c_controller.watchdog(cmd.WATCHDOG_OFF)
        
        match self.innopro_family:
            case InnoProFamily.Inno5Pro:
                self.i2c_controller.dcm_only(enable = True)
            case InnoProFamily.Inno4Pro:
                self.i2c_controller.dcm_only(enable = True)
            
        self.i2c_controller.uva(self.uva_thresh, 
                                        cmd.UVA_RESP_NR, 
                                        cmd.UVA_TIMER_16MS)
        self.i2c_controller.ova(threshold_V=30, response=cmd.OVA_RESP_NR)
        self.i2c_controller.cv(vout_V=5)#, autocv=self.i2c_commands.CV_AUTO_UV_OV_ENABLED)
        sleep(1)
        # Enable the bleeder to quickly discharge output
        self.i2c_controller.bleeder(
            bleeder_en=cmd.BLEEDER_ON_AUTO_DIS,
            auto_disable_thresh=cmd.BLEEDER_VOUT4PCT,
            weak_bleeder_en=cmd.WEAK_BLEEDER_ON)
        sleep(1)
        try:            
            self.i2c_controller.vben(cmd.VBEN_OFF_RST)
        except:
            pass
        sleep(1)

        # Reinitialize after reset
        self.i2c_controller.watchdog(cmd.WATCHDOG_OFF)
        self.i2c_controller.fast_vi(cmd.FASTVI_LIMIT_DIS)
        self.i2c_controller.ova(30, cmd.OVA_RESP_NR)
        self.i2c_controller.uva(self.uva_thresh, 
                                        cmd.UVA_RESP_NR, 
                                        cmd.UVA_TIMER_16MS)
        self.i2c_controller.vben(cmd.VBEN_ON)

        self.i2c_controller.cv(vout_V=5)

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

        
    def test_loop(self):
        
        soak = self.soak_time
    
        self.total_time, self.total_steps = self.estimate_remaining(0, 0, vin_delays = True)
        self.status_report(0, 0,vin_delays=True)
        self.input_supply_eload_discharge_sequence()
        temp_filepaths = []
        
        for self.vin_index, self.vin_freq in enumerate(self.vin_list):

            self.prepare_excel_header(self.vin_index, self.column_step)
            
            # Extract the values from the self.vin_freq
            self.input_supply.set_voltage_with_coupling(voltage= self.vin_freq[0], coupling= self.coupling)  
            if self.coupling == AC_SOURCE_COUPLING.AC:
                self.input_supply.frequency = self.vin_freq[1]
            self.source_vout = self.vin_freq[0]
            
            # Set the parameter for displaying the set output voltage
            self.test_data.vin_set_V = self.vin_freq[0]
            self.test_data.ac_freq_Hz = self.vin_freq[1]

            # Create a new data series for the plottable objects  
            self.create_new_plot_series()

            # Turn on the AC source with the current parameters
            self.input_supply.turn_on()

            self.power_meter_load.auto_range_enable()
            self.power_meter_source.current_auto_range_enable()

            # Sleep for a short time to allow the power supply to stabilize 
            sleep(1)

            self.i2c_initialize()
            
            sleep(5)
            # Set the e-load to the maximum load level to be tested and turn it on
            self.electronic_load.reset_values()
            self.electronic_load.set_load(self.vout_min_V,self.iout_A,self.eload_type)
            self.electronic_load.turn_on()
            
            sleep(1)
            
            self.correct_source_output()
            # Do the initial soak if it is the first input voltage on the list
            if self.vin_index == 0:
                soak.do_initial_soak()
            # Or the soak per line if it is not
            else:
                soak.do_soak_per_line()
            
            temp_file_path = f"{self.temp_folder_path}/{self.title} {self.vin_freq[0]}V.csv"
            txt_file = open(temp_file_path,'w', newline='')
            wr = csv.writer(txt_file, quoting=csv.QUOTE_ALL)
            wr.writerow(self.header_list)
            temp_filepaths.append(temp_file_path)

            self.vout_step_meas = 0

            # Loop through each load current level
            for self.vout_index, self.vout_setpoint in enumerate(self.vout_list):
                self.status_report(self.vout_index, self.vin_index, vin_delays=False)
                self.test_data.vout_nom_V = self.vout_setpoint
                self.i2c_controller.cv(vout_V=self.vout_setpoint)
                
                # Set the e-load to the maximum load level to be tested and turn it on
                self.electronic_load.set_load(self.vout_setpoint,self.iout_A,self.eload_type)
                self.electronic_load.turn_on()
                
                if self.iout_A < 0.05:
                    self.power_meter_load.set_current_range(0.05)
                else:
                        self.power_meter_load.current_auto_range_enable()
                
                # Sleep for the soak time before measuring
                soak.do_soak_per_load()

                # Gather the data from the equipment
                self.test_data.gather_data_load(integrate=False)
                self.i2c_read()

                self.cv_error = self.test_data.vreg_pct
                if not self.vout_index == 0: 
                    self.vout_step_meas = self.test_data.vout_V - self.prev_vout_V
                self.prev_vout_V = self.test_data.vout_V
                
                # Process data for excel output
                self.output_dataframe.loc[len(self.output_dataframe)]\
                    = self.process_data_row()
                data_row = self.process_data_row()

                self.write_textfile_row(wr, txt_file, data_row)
            
                # Update the data for the results page
                self.update_output_data()
                # Add a blank row
            
            self.electronic_load.turn_off()
            
            # Clear data list for next loop 
            self.output_dataframe=self.output_dataframe[0:0]

            self.test_data_table.add_blank_row()

        self.export(temp_filepaths)

    def write_textfile_row(self, writer, file, row):
        writer.writerow(row)
        file.flush()

    def export(self, csv_filepaths):
        """Get the CSV files and place them in excel"""
        for i, filepath in enumerate(csv_filepaths):
            df = pd.read_csv(filepath)

            anchor_letter = f'{get_column_letter(2+self.column_step*i)}'  
            anchor = f'{anchor_letter}6'
            export_to_excel(
                df, self.output_folder_path, 
                self.data_filename, self.sheet_name, anchor) 
                # Clear data list for next loop 

    def input_supply_eload_discharge_sequence(self):
        self.equipment.input_supply_eload_discharge_sequence(self.iout_A/3,coupling=self.coupling)

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
        
        text = f"{self.title}: {self.vout_min_V:g} V to {self.vout_max_V:g} V in {self.vout_step_V:g} V steps\n" 
        
        text += f"Load: {self.iout_A:g} A, Family: {self.innopro_family}, "
        match self.innopro_family:
            case InnoProFamily.Inno5Pro:
                text += f"Operation: {self.dcm_text} {self.sr_zvs_text}\n"
            case InnoProFamily.Inno4Pro:
                text += f"Operation: {self.dcm_text}\n"
        
        if self.status in [TestStatus.STOPPED, TestStatus.FAILED, TestStatus.COMPLETE, TestStatus.SKIPPED]:
            text += f"{self.status}\n"
        else:
            text += f"{self.status}: {self.estimated_time_txt}, {self.progress_txt}\n"
            
        text += f"Line Range: {self.line_range.name}, Coupling: {self.coupling}\n"
        
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
        
        # I2C controller object
        self.i2c_controller:pat_tool.InnoProI2CControllerContainer = self.equipment.i2c_controller

        # Test Conditions Object
        self.test_conditions = test_item.test_conditions
        
        # General PSU Test Options
        self.general_options:GeneralOptions = self.test_conditions.general_options
        self.eload_type:str = self.general_options.eload_type
        self.use_eload_data:bool = self.general_options.use_eload_data
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
        self.oscilloscope = self.equipment.oscilloscope
        
        self.power_meter_load.integration_settings(
            mode="NORMAL", timer_s=self.soak_time.integration_time)
        self.power_meter_source.integration_settings(
            mode="NORMAL", timer_s=self.soak_time.integration_time)
        self.power_meter_load.stop_integration()
        self.power_meter_source.stop_integration()
        self.power_meter_load.reset_integration()
        self.power_meter_source.reset_integration()
        
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
        
        self.test_data.use_eload_data = self.use_eload_data
        self.test_data.source_power_meter = self.power_meter_source
        self.test_data.load_power_meter = self.power_meter_load
        self.test_data.electronic_load = self.electronic_load
        self.test_data.vreg_limit_pct = 3

        # Prepare output dataframe
        self.header_list = self.define_data_header()
        # self.output_dataframe = dataframe_from_headers(self.header_list)
        
        if not os.path.exists(self.output_folder_path):
            os.mkdir(self.output_folder_path)
        match self.innopro_family:
            case InnoProFamily.Inno5Pro:
                self.data_filename = f'{self.title} Test {self.dcm_text} {self.sr_zvs_text} {self.innopro_family}'
            case InnoProFamily.Inno4Pro:
                self.data_filename = f'{self.title} Test {self.dcm_text} {self.innopro_family}'
        self.data_file_path = f'{self.output_folder_path}/{self.data_filename}.xlsx'
        
        # Check if workbook exists
        if not os.path.exists(self.data_file_path):     
            self.wb:Workbook = openpyxl.Workbook()
            self.wb.save(self.data_file_path)
            self.wb.close()
            
        # Open the workbook    
        self.wb:Workbook = openpyxl.load_workbook(self.data_file_path)
        
        # Prepare the sheet name, limit to 31 characters
        self.sheet_name = f"CV_{self.coupling}_{self.vout_min_V:g}V-{self.vout_max_V:g}V_{self.vout_step_mV}mV_{self.iout_A:g}A"
        # self.sheet_name = f"CVSweep _{self.iout_A:g}A"

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

        # Create the plottables and data table for the results viewer
        self.define_output_data_objects()
        self.wb.save(self.data_file_path)
        self.wb.close()

        # Create a temp folder in the test results folder to store 
        # txt files for dumping output data quickly
        # These files will then be converted later to excel
        self.temp_folder_path = f'{self.output_folder_path}/temp'

        if not os.path.exists(self.temp_folder_path):
            os.mkdir(self.temp_folder_path)
        
    def prepare_excel_header(self, index, step):
        """Merge the cells for the header."""
        # Open the workbook    
        self.wb:Workbook = openpyxl.load_workbook(self.data_file_path)
        self.ws:Worksheet = self.wb[self.sheet_name]

        offset = index * step
        row = 4
        # B5
        b_col = 2 + offset
        c_col = 3 + offset
        d_col = 4 + offset
        i_col = 9 + offset
        h_col = 8 + offset
        l_col = 12 + offset

        self.ws.merge_cells(start_row=row, end_row=row, start_column = b_col, end_column=c_col)
        
        cell1 = self.ws.cell(row=row, column=b_col)
        cell1.value = 'Input'
        cell1.alignment = Alignment(horizontal='center')
        
        
        self.ws.merge_cells(start_row=row, end_row=row, start_column = d_col, end_column=h_col)
        cell2 = self.ws.cell(row=row, column=d_col)
        cell2.value = 'Input Measurement'
        cell2.alignment = Alignment(horizontal='center')
        
        self.ws.merge_cells(start_row=row, end_row=row, start_column = i_col, end_column=l_col)
        cell3 = self.ws.cell(row=row, column=i_col)
        cell3.value = 'Output Measurement'
        cell3.alignment = Alignment(horizontal='center')

        self.wb.save(self.data_file_path)
        self.wb.close()

        self.output_dataframe = dataframe_from_headers(self.header_list)
        
        anchor = f'{get_column_letter(2+offset)}5'        
        export_to_excel(
                self.output_dataframe, self.output_folder_path, 
                self.data_filename, self.sheet_name, anchor)
    
    
    def prepare_test_conditions(self):
        """Prepare the list of conditions to be used."""
        tc = self.test_conditions
        
        # Generate a list of the input line voltage
        self.vin_list = tc.line_range.vin_freq
        self.vout_min_V = self.i2c_test_conditions.param[0]
        self.vout_max_V = self.i2c_test_conditions.param[1]
        self.vout_step_V = self.i2c_test_conditions.param[2]
        self.vout_step_mV = round(self.vout_step_V*1000,3) 
        self.iout_A = round(self.i2c_test_conditions.param[3],6)
        
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

        # Make all voltages in spec with Inno5Pro resolution
        trim_to_spec(self.vout_step_V, 
                     self.i2c_params.CV_RESOLUTION_MV/1000)
        trim_to_spec(self.vout_max_V, 
                     self.i2c_params.CV_RESOLUTION_MV/1000)
        trim_to_spec(self.vout_min_V,
                     self.i2c_params.CV_RESOLUTION_MV/1000)
        
        self.test_conditions.nominal_load_current_A = self.iout_A
        self.test_conditions.max_load_current_A = self.iout_A
        
        vout_num_step = abs(math.floor((int(self.vout_max_V*1000) \
                        - int(self.vout_min_V*1000)) \
                        /int(self.vout_step_V*1000))) + 1
        self.vout_list = np.linspace(self.vout_min_V, self.vout_max_V, vout_num_step)
        self.vout_list = [round(vout, 3) for vout in self.vout_list]
       
        # Fixed UV Setting
        self.uva_thresh = 2.7

        if self.vout_max_V >= self.vout_min_V:
            self.plot_vout_step_size = self.vout_step_V
        else:
            self.plot_vout_step_size = -self.vout_step_V
        
    def define_data_header(self):
        """Defines the data header for the excel file."""
        vreg_txt = f'V Reg({self.test_data.vreg_limit_pct}%)'
        header_list = [
            'CV Setpoint (V)', f'V{self.coupling} (rms)','Freq (Hz)',
            'Vo (V)','Io (A)','Po (W)',
            'I2C CV Set (V)', 'I2C DAC (V)', 'I2C Vout Ave (V)', 'CDC (mV)', #'I2C Vin_dc(V)',
            '%V Reg',vreg_txt, 'Vout Step(V)', 'Vout Step [50%-200%]']
        # header_list = [
        #     'CV Setpoint (V)', 'Vac (rms)','Freq (Hz)',
        #     'Pin (W)','PF','%THD','Vo (V)','Io (A)','Po (W)',
        #     '%V Reg','Efficiency','V Reg(5%)']

        self.column_step = len(header_list)+1
        return header_list
    
    def process_data_row(self):
        """Create a row of data from the test data"""

        td = self.test_data
        td.vout_nom_V = self.vout_setpoint
        if (self.vout_step_meas >= self.vout_step_V/2) and (self.vout_step_meas < self.vout_step_V*2):
            vout_step_valid = 'PASS'
        else:
            vout_step_valid = 'FAIL'
        data_row = [
            self.vout_setpoint, td.vin_set_V, td.ac_freq_Hz, 
            td.vout_V, td.iout_A, td.pout_W, 
            self.i2c_cv_set, self.i2c_vout_dac, self.i2c_vout_ave, self.i2c_cdc_mV,
            # self.i2c_vin,
            round(td.vreg_pct,2), td.vreg_passfail, self.vout_step_meas,vout_step_valid]

        return data_row
    
    def i2c_read(self):
        self.i2c_cv_set = self.i2c_controller.read_cv_v()
        self.i2c_cc_set = self.i2c_controller.read_cc()
        self.i2c_vout_dac = self.i2c_controller.read_vout_dac_v()
        self.i2c_vout_ave = self.i2c_controller.read_vout_average_v()
        self.i2c_iout_ave = self.i2c_controller.read_iout_average()
        self.i2c_cdc_mV = self.i2c_controller.read_cdc_mv()

        self.i2c_omf = self.i2c_controller.read_omf()

    # Signals for reporting
    def status_report(self, vout_index, vin_index, vin_delays):
                
        remaining_time_s, remaining_steps = self.estimate_remaining(vout_index, vin_index, vin_delays)
        percent_completion = round((1 - remaining_steps/self.total_steps)*100,0)

        self.estimated_time.emit(remaining_time_s)
        self.progress.emit(percent_completion)

    def estimate_remaining(self, vout_index_t, vin_index_t, vin_delays:bool=True):

        soak = self.soak_time

        remaining_time_s = 0
        remaining_steps = 0
        vout_index = 0
        vin_index = 0
        start_adding_time = False
        

        def add_time(t,add_step:bool = False):
            nonlocal remaining_steps
            nonlocal remaining_time_s
            nonlocal start_adding_time
            nonlocal vout_index
            nonlocal vout_index_t
            nonlocal vin_index
            nonlocal vin_index_t
            nonlocal vin_delays

            # Only add time if the index
            if not start_adding_time:
                if vin_index == vin_index_t:
                    if vout_index == vout_index_t:
                        start_adding_time = True
                        vin_delays = True            
            if start_adding_time:
                remaining_time_s += t
                if add_step:
                    remaining_steps += 1

            return remaining_steps, remaining_time_s
        
        add_time(1)
        for vin_index, _ in enumerate(self.vin_list):
            
            if vin_delays:
                add_time(3)
                if vin_index == 0:
                    add_time(soak.initial_soak)
                # Or the soak per line if it is not
                else:
                    add_time(soak.soak_per_line)           
        
            for vout_index, _ in enumerate(self.vout_list):
                
                add_time(1,True) 
                
                add_time(soak.soak_per_load)        

                    # Sleep for the soak time before measuring
                add_time(soak.integration_time)
                add_time(0.1)
                
        add_time(3)
        
        return remaining_time_s, remaining_steps

    def plot_charts(self):
        """Add a Chart on the output workbook for this test item."""
        self.wb = openpyxl.load_workbook(self.data_file_path)

        self.wb.close()

    ###########################################################################
    #               Output Data Processing for Test Results Page              #
    ###########################################################################
    def define_output_data_objects(self):
        """Define the objects that will be viewable in the test results page"""
        # Plottable Objects
        self.cv_vs_vout_plot = PlottableObject(
            title=f"CV Setpoint vs Output Voltage, Load={self.iout_A}A",
            type=PlotType.LINE,
            x_label="CV Setpoint (V)",
            y_label="Output Voltage (V)",
            x_range=(0, self.vout_max_V+1),
            y_range=(0, self.vout_max_V+1),
            plot_series_list=[])

        self.cv_vs_error_plot = PlottableObject(
            title=f"CV Setpoint vs Error, Load={self.iout_A}A",
            type=PlotType.LINE,
            x_label="CV Setpoint (V)",
            y_label="CV Error (%)",
            x_range=(0, self.vout_max_V+1),
            y_range=(-3, 3),
            plot_series_list=[])
        
        self.cvset_vs_cvstep_plot = PlottableObject(
            title=f"CV Setpoint vs CV Step, Load={self.iout_A}A",
            type=PlotType.LINE,
            x_label="CV Setpoint (V)",
            y_label="Vout step (V)",
            x_range=(0, self.vout_max_V+1),
            y_range=(-3*self.vout_step_V, +3*self.vout_step_V),
            plot_series_list=[])
        

        self.test_data_table = DataTable(
            header=self.header_list, data=[])

        self.with_data = True

    def create_new_plot_series(self):
        """Create a new data series for each plottable object
        with the current input voltage as name."""
        pct_lim = self.test_data.vreg_limit_pct
        vin = self.vin_list[self.vin_index][0]

        # CV vs Vout Plot
        if self.vin_index == 0:
            # CV vs Vout Step Plot Limits
            self.cv_vs_vout_plot.add_plot_series(
                name=f'CV Setpoint',
                x_values=[],
                y_values=[],
                format=PlotLineFormatPresets.YELLOW_1PX_SOLID)
            self.cv_vs_vout_plot.add_plot_series(
                name=f'CV +{pct_lim}%',
                x_values=[],
                y_values=[],
                format=PlotLineFormatPresets.RED_1PX_DASH)
            self.cv_vs_vout_plot.add_plot_series(
                name=f'CV -{pct_lim}%',
                x_values=[],
                y_values=[],
                format=PlotLineFormatPresets.RED_1PX_DOT)

            # CV vs Vout Step Plot Limits
            self.cvset_vs_cvstep_plot.add_plot_series(
                name=f'CV Register Step (V)',
                x_values=[],
                y_values=[],
                format=PlotLineFormatPresets.GREEN_1PX_DASH)
            
        # CV vs Vout Plot
        self.cv_vs_vout_plot.add_plot_series(
            name=f'{vin:3g} V',
            x_values=[],
            y_values=[])
        # CV vs Vout Error Plot
        self.cv_vs_error_plot.add_plot_series(
            name=f'{vin:3g} V',
            x_values=[],
            y_values=[])
        # CV vs Vout Step Plot
        self.cvset_vs_cvstep_plot.add_plot_series(
            name=f'{vin:3g} V',
            x_values=[],
            y_values=[])
    
    def update_output_data(self):
        """Update the plots and numeric data
        Emit a signal containing the processed info"""
        td = self.test_data

        # Plottable objects processing
        plottables = []

        pct_lim = self.test_data.vreg_limit_pct
        limit_mult_min = 1 - pct_lim/100
        limit_mult_max = 1 + pct_lim/100
        
        # Add Plot limits only at the start
        if self.vin_index == 0:
            # CV vs Vout Plot Limits
            self.cv_vs_vout_plot.append_plot_data(
                plot_index=0,
                x=self.vout_setpoint,
                y=self.vout_setpoint)
            self.cv_vs_vout_plot.append_plot_data(
                plot_index=1,
                x=self.vout_setpoint,
                y=round(self.vout_setpoint*limit_mult_max,6))
            self.cv_vs_vout_plot.append_plot_data(
                plot_index=2,
                x=self.vout_setpoint,
                y=round(self.vout_setpoint*limit_mult_min,6))
            
            # CV vs Vout Step Plot Limits
            self.cvset_vs_cvstep_plot.append_plot_data(
                plot_index=0,
                x=self.vout_setpoint,
                y=self.plot_vout_step_size)

        # CV vs Vout Plot
        self.cv_vs_vout_plot.append_plot_data(
            plot_index=self.vin_index + 3,
            x=self.vout_setpoint,
            y=td.vout_V)
        plottables.append(self.cv_vs_vout_plot)

        # CV vs Error Plot
        self.cv_vs_error_plot.append_plot_data(
            plot_index=self.vin_index,
            x=self.vout_setpoint,
            y=td.vreg_pct)
        plottables.append(self.cv_vs_error_plot)
        
        # CV vs Vout Step Plot
        # Do not include the 1st sample since 
        # the step measurement requires 2 samples
        if not self.vout_index == 0:
            self.cvset_vs_cvstep_plot.append_plot_data(
                plot_index=self.vin_index+1,
                x=self.vout_setpoint,
                y=self.vout_step_meas)
        plottables.append(self.cvset_vs_cvstep_plot)
        
        # Test Data Table Processing
        test_data_row = self.process_data_row()
        self.test_data_table.add_data_row(test_data_row)      

        self.test_data_update.emit([plottables, self.test_data_table])
        
    ###########################################################################
    #      Test Item Dictionary creation for saving/loading test items        #
    ###########################################################################
    def get_dict(self)->dict:
        d = {'TEST_TYPE_INDEX':                    self.test_type_index,
            'LINE_RANGE_name':                     self.test_conditions.line_range.name,
            'LINE_RANGE_vin_freq':                 self.test_conditions.line_range.vin_freq,
            'LINE_RANGE_custom':                   self.test_conditions.line_range.custom,
            'SOAK_TIME_name':                      self.test_conditions.soak_time.name,
            'SOAK_TIME_initial_soak':              self.test_conditions.soak_time.initial_soak,
            'SOAK_TIME_soak_per_line':             self.test_conditions.soak_time.soak_per_line,
            'SOAK_TIME_soak_per_load':             self.test_conditions.soak_time.soak_per_load,
            'SOAK_TIME_integration_time':          self.test_conditions.soak_time.integration_time,
            'SOAK_TIME_custom':                    self.test_conditions.soak_time.custom,
            'GENERAL_OPTIONS_use_eload_data':      self.test_conditions.general_options.use_eload_data,
            'GENERAL_OPTIONS_eload_type':          self.test_conditions.general_options.eload_type,
            'GENERAL_OPTIONS_coupling':            self.test_conditions.general_options.coupling,
            'I2C_PARAMS':                          self.test_conditions.i2c_test_parameters.param,
            'I2C_CBX_PARAMS':                      self.test_conditions.i2c_test_parameters.cbx_param,
            'NAME':                                self.test_conditions.name}
        return d
    
    @staticmethod
    def extract_test_condition(test_item_dict:dict)->dict:
        test_object_class = I2C_CVSweepTest
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
                use_eload_data=test_item_dict['GENERAL_OPTIONS_use_eload_data'],
                eload_type=test_item_dict['GENERAL_OPTIONS_eload_type'],
                load_direction=test_object_class.tc_default.general_options.load_direction,
                coupling=test_item_dict['GENERAL_OPTIONS_coupling']),
            usbpd_options=test_object_class.tc_default.usbpd_options,
            line_ramp_settings=test_object_class.tc_default.line_ramp_settings,
            i2c_test_parameters=I2CTestParameters(
                params = test_item_dict['I2C_PARAMS'],
                cbx_params = test_item_dict['I2C_CBX_PARAMS']),
            name=test_item_dict['NAME'])
        return new_test_conditions
    