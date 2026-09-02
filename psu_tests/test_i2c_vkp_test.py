from psu_tests.test_object_imports import *

class I2C_VKPTest(BaseTestObject):
    """
    The VKP test is similar to a CVCC Test with constant power (CP) range between the CV and CC range

    """
    title = "I2C VKP"
    i2c_test = True

    # General UI Definitions
    ui_definitions = General_UI_Definitions()
    ui_definitions.stack_page_1 = StackWidget1Pages.LineVoltageRange
    ui_definitions.stack_page_2 = StackWidget2Pages.CVCCSettings
    ui_definitions.stack_page_3 = StackWidget3Pages.I2C_Options
    ui_definitions.multiple_cvcc_setpoints_enable = True
    
    # I2C UI definitions
    i2c_ui_definitions = I2C_UI_Definitions()
    # Line Edits
    i2c_ui_definitions.add_lineedit(label='VKP (V)', param_index=1)
    i2c_ui_definitions.add_lineedit(label='Rsense (mΩ)', param_index=2)
    # Checkbox
    i2c_ui_definitions.add_cbx(label="SR ZVS?", contents=['Yes', 'No'], param_index=1)
    i2c_ui_definitions.add_cbx(label="Initial Mode", contents=['CCM', 'DCM'], param_index=2)
    i2c_ui_definitions.add_lineedit(label='SR ZVS On',param_index=9)
    i2c_ui_definitions.add_lineedit(label='SR ZVS Delay',param_index=10)
    i2c_ui_definitions.add_cbx(label="Inno-Pro Family", contents=InnoProFamilyList, param_index=4)

    
    # General UI Update Definitions
    ui_update = General_UI_Update_Definitions()
    ui_update.line_settings_update = True
    ui_update.load_settings_update = False
    ui_update.soaktime_settings_update = True
    ui_update.cvcc_settings_update = True
    ui_update.line_ramp_settings_update = False
    ui_update.nominal_output_settings_update = False
    ui_update.usbpd_options_update = False
    ui_update.tracking_pdo_request_update = False
    ui_update.measure_ripple_update = False
    ui_update.load_direction_update = False
    ui_update.eload_type_update = False
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
        self.i2c_ui_definitions.add_lineedit(label='VKP (V)', param_index=1)
        self.i2c_ui_definitions.add_lineedit(label='Rsense (mΩ)', param_index=2)
        # Checkbox
        self.i2c_ui_definitions.add_cbx(label="SR ZVS?", contents=['Yes', 'No'], param_index=1)
        self.i2c_ui_definitions.add_cbx(label="Initial Mode", contents=['CCM', 'DCM'], param_index=2)
        self.i2c_ui_definitions.add_lineedit(label='SR ZVS On',param_index=9)
        self.i2c_ui_definitions.add_lineedit(label='SR ZVS Delay',param_index=10)
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
        self.setup_cv_cp_cc_load_steps()
        self.total_time, self.total_steps = self.estimate_remaining(0, True, True, True, True)
        self.estimated_time_s = self.total_time

        self.message_closed = False
        self.with_data = False

        self.exit_condition = ""  
        
    def with_waveform_capture(self):
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
        self.i2c_controller.watchdog(self.i2c_commands.WATCHDOG_OFF)
        self.i2c_controller.fast_vi(self.i2c_commands.FASTVI_LIMIT_DIS)
        self.i2c_controller.ova(30, self.i2c_commands.OVA_RESP_NR)
        self.i2c_controller.uva(self.uva_thresh, self.i2c_commands.UVA_RESP_AR, self.i2c_commands.UVA_TIMER_16MS)
        self.i2c_controller.cvo(self.i2c_commands.CVO_RESP_NR,self.i2c_commands.CVO_TIMER_8MS,cvo_en=False)
        # self.i2c_controller.loop_option(self.i2c_commands.LOOP_OPTION1_LSB, self.i2c_commands.LOOP_OPTION1_MSB)
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

    def test_loop(self):
        
        soak = self.soak_time
        
        self.total_time, self.total_steps = self.estimate_remaining(0, True, True, True, True)
        self.status_report(0,True,True,True,True) 
        self.input_supply_eload_discharge_sequence()
        self.i2c_controller.update_rsense(self.rsense_mohm)
        
        
        temp_filepaths = []
        # Loop through each line input level
        for self.vin_index, self.vin_freq in enumerate(self.vin_list):
            self.status_report(self.vin_index,True,True,True,True) 
            
            self.prepare_excel_header(self.vin_index, self.column_step)
            # Extract the values from the self.vin_freq
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
            self.electronic_load.reset_values()
            # Set the e-load to the minimum load level to be tested and turn it on
            self.electronic_load.set_load(self.vout_V,0,self.eload_type)
            self.electronic_load.turn_on()
            
            sleep(2)

            # Send necessary I2C commands
            self.i2c_initialize()
            sleep(1)
            self.i2c_controller.vkp(self.vkp_V)  
            self.i2c_controller.cc(self.i_max_A)
            self.i2c_controller.cv(self.vout_V)
            
            sleep(1)
            
            # Set the e-load to the minimum load level to be tested and turn it on
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

            # Create a new data series for the plottable objects  
            self.create_new_plot_series()
            
            temp_file_path = f"{self.temp_folder_path}/{self.title} {self.vin_freq[0]}V.csv"
            self.txt_file = open(temp_file_path,'w', newline='')
            self.wr = csv.writer(self.txt_file, quoting=csv.QUOTE_ALL)
            self.wr.writerow(self.header_list)
            temp_filepaths.append(temp_file_path)
            
            self.status_report(self.vin_index,False,True,True,True)
            self.cv_region_sweep(self.CV_range)
            
            self.status_report(self.vin_index,False,False,True,True)
            self.cp_region_sweep(self.CP_range)
            
            self.status_report(self.vin_index,False,False,False,True)
            self.cc_region_sweep(self.CC_range)

            # Add a blank row
            self.test_data_table.add_blank_row()
            
            self.output_dataframe=self.output_dataframe[0:0]

            # Set the output to 5V and let the output caps discharge
            # before turning off the eload to prevent Eload CRL OV
            self.i2c_controller.cv(vout_V=5)
            sleep(0.1)

            self.electronic_load.turn_off()
        
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
    
    def cv_region_sweep(self, iout_range):
        """Sweep in CV region"""
        soak = self.soak_time
        # print("Entered CV loop")   
        # Loop through each load current level for the CV or CP region
        for iout_index, iout_level in enumerate(iout_range):
            # Trim the trailing zeros
            iout_A = float(f'{round(iout_level,6):g}')
            
            if iout_A == 0:
                self.electronic_load.turn_off()
                cr = self.min_cr
            else:
                # Get eauivalent load resistance
                cr = round(self.vout_V/iout_A,6)
                self.electronic_load.set_load(self.vout_V,iout_A,self.eload_type)
                self.electronic_load.turn_on()
            
            if iout_A < 0.05:
                if self.power_meter_load:
                    self.power_meter_load.set_current_range(0.05)
            else:
                if self.power_meter_load:
                    self.power_meter_load.current_auto_range_enable()
            
            # Sleep for the soak time before measuring
            soak.do_soak_per_load()
            # Gather the data from the equipment
            if self.power_meter_load and getattr(self.power_meter_load, '_current_auto_range_status', False):
                self.power_meter_load.auto_range_enable(False)
                sleep(1)
            if self.power_meter_source and getattr(self.power_meter_source, '_current_auto_range_status', False):
                self.power_meter_source.current_auto_range_enable(False)
                sleep(1)
            self.test_data.gather_data_load(integrate=False)
            self.output_dataframe.loc[len(self.output_dataframe)]\
                = self.process_data_row_load()
            
            data_row = self.process_data_row_load()
            
            self.write_textfile_row(self.wr, self.txt_file, data_row)
            
            # Update the data for the results page
            self.update_output_data()
            self.min_cr = cr
            
            if self.power_meter_load:
                self.power_meter_load.auto_range_enable()
            if self.power_meter_source:
                self.power_meter_source.current_auto_range_enable()

            self.ccm_dcm_decision()
    
    def cp_region_sweep(self, iout_range):
        """Sweep in CP region"""
        soak = self.soak_time
        # print("Entered CP loop")
        # Loop through each load current level for the CV or CP region
        for iout_index, iout_level in enumerate(iout_range):
            # Trim the trailing zeros
            iout_A = float(f'{round(iout_level,6):g}')
            
            # Get voltage based on the constant power condition and the current
            vout_V = self.p_max_W/iout_A
            
            # Get eauivalent load resistance
            cr = round(vout_V/iout_A,6)

            if cr > self.min_cr:
                continue
            self.electronic_load.set_load(vout_V,iout_A,self.eload_type)
            self.electronic_load.turn_on()
            
            # Sleep for a short time to allow the power meters to select the appropriate range
            # sleep(2)
            
            # Sleep for the soak time before measuring
            soak.do_soak_per_load()

            if self.test_data.pout_W < 1:
                raise Exception("PSU restarted during CP region.")
            if self.power_meter_load and getattr(self.power_meter_load, '_current_auto_range_status', False):
                self.power_meter_load.auto_range_enable(False)
                sleep(1)
            if self.power_meter_source and getattr(self.power_meter_source, '_current_auto_range_status', False):
                self.power_meter_source.current_auto_range_enable(False)
                sleep(1)
            
            # Gather the data from the equipment
            self.test_data.gather_data_load(integrate=False)
            self.output_dataframe.loc[len(self.output_dataframe)]\
                = self.process_data_row_load()
            
            data_row = self.process_data_row_load()
            
            self.write_textfile_row(self.wr, self.txt_file, data_row)
            
            # Update the data for the results page
            self.update_output_data()
            self.min_cr = cr
            
            if self.power_meter_load:
                self.power_meter_load.auto_range_enable()
            if self.power_meter_source:
                self.power_meter_source.current_auto_range_enable()

            self.ccm_dcm_decision()

            inn = self.i2c_defaults
            if self.read_omf_txt[:2] == inn.OMF_TEXT[inn.OMF_CC_MODE]:
                self.define_cc_range(vkp = self.test_data.vout_V)
                return
                
    def cc_region_sweep(self, rout_range):
        """Sweep in CC region"""
        soak = self.soak_time
        # print("Entered CC loop") 
        # Loop through each load current level for the CV or CP region
        for rout_index, rout_level in enumerate(rout_range):
            cr = round(rout_level,6)
            if cr >= self.min_cr:
                continue
            vout_V = self.electronic_load.voltage
            self.electronic_load.set_load(vout_V,vout_V/cr,self.eload_type)
            self.electronic_load.turn_on()
            
            # Sleep for a short time to allow the power meters to select the appropriate range
            # sleep(2)
            
            # Sleep for the soak time before measuring
            soak.do_soak_per_load()
            
            if self.power_meter_load and getattr(self.power_meter_load, '_current_auto_range_status', False):
                self.power_meter_load.auto_range_enable(False)
                sleep(1)
            if self.power_meter_source and getattr(self.power_meter_source, '_current_auto_range_status', False):
                self.power_meter_source.current_auto_range_enable(False)
                sleep(1)
            

            # Gather the data from the equipment
            self.test_data.gather_data_load(integrate=False)

            if self.power_meter_load:
                self.power_meter_load.auto_range_enable()
            if self.power_meter_source:
                self.power_meter_source.current_auto_range_enable()
            
            if not self.cc_data_valid():
                # print([self.test_data.vout_V, self.test_data.iout_A, self.test_data.pout_W])
                self.electronic_load.set_load(self.vout_V, 0.1, self.eload_type)
                break
            
            self.output_dataframe.loc[len(self.output_dataframe)]\
                = self.process_data_row_load()
                
            data_row = self.process_data_row_load()
            
            self.write_textfile_row(self.wr, self.txt_file, data_row)
            
            # Update the data for the results page
            self.update_output_data()    
            self.min_cr = cr

            self.ccm_dcm_decision()

    def ccm_dcm_decision(self):
        if self.test_data.vout_V < 5:
            self.i2c_controller.dcm_only(enable=False)
            
    def cc_data_valid(self)->bool:
        """Returns True if CC data is still valid.
        
        Causes of invalid data:
        1. Iout measured is greater than maximum specified current
        2. Any of the measured voltage, current, or power is zero
        3. Output voltage measured increased from previous measurement
        """
        td = self.test_data
        cond1 = abs((td.iout_A - self.i_max_A)/self.i_max_A) > 0.2 # 20% max dev
        cond2 = 0 in [td.vout_V, td.iout_A, td.pout_W]
        cond3 = td.vout_V \
            > (self.output_dataframe['Vo (V)'].tail(1).values * 1.05)
        cond4 = td.vout_V <= self.uva_thresh
        # Return false if any of the conditions is true
        # print(f'cond1: {cond1}, cond2: {cond2}, cond3: {cond3}')

        cc_exit = (cond1 | cond2 | cond3 | cond4)

        if cc_exit:
            if cond1:
                self.exit_condition += "\t\tIout measured outside specifed tolerance\n"
            if cond2:
                self.exit_condition += "\t\tZero value measurement\n"
            if cond3:
                self.exit_condition += "\t\tVout increased from previous loading condition\n"
            if cond4:
                self.exit_condition += "\t\tReached UV threshold\n"
            
            # print(f"CC Exit: {self.exit_condition}")

        return not cc_exit

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
        
        text = f"{self.title}: {self.vout_V:g} V, {self.i_max_A:g} A\n" 
        text += f"VKP: {self.vkp_V:g} V, Family: {self.innopro_family}, "
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

        # List of load percentage
        self.load_range_pct:LoadRange = self.test_conditions.load_range
        
        self.soak_time:SoakTime = self.test_conditions.soak_time
        
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
        self.min_cr = self.electronic_load.crh_max_r
        
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
        self.test_data.vout_nom_V = self.vout_V
        self.test_data.source_power_meter = self.power_meter_source
        self.test_data.load_power_meter = self.power_meter_load
        self.test_data.electronic_load = self.electronic_load

        # Prepare output dataframe
        self.header_list = self.define_data_header()
        # self.output_dataframe = dataframe_from_headers(self.header_list)
        
        if not os.path.exists(self.output_folder_path):
            os.mkdir(self.output_folder_path)
        match self.innopro_family:
            case InnoProFamily.Inno5Pro:
                self.data_filename = f'{self.title} Test {self.vout_V:g}V {self.dcm_text} {self.sr_zvs_text} {self.innopro_family}'
            case InnoProFamily.Inno4Pro:
                self.data_filename = f'{self.title} Test {self.vout_V:g}V {self.dcm_text} {self.innopro_family}'
        self.data_file_path = f'{self.output_folder_path}/{self.data_filename}.xlsx'
        
        # Check if workbook exists
        if not os.path.exists(self.data_file_path):     
            self.wb:Workbook = openpyxl.Workbook()
            self.wb.save(self.data_file_path)
            self.wb.close()
            
        # Open the workbook    
        self.wb:Workbook = openpyxl.load_workbook(self.data_file_path)
        
        # Prepare the sheet name
        self.sheet_name = f"VKP_{self.coupling}_{self.vout_V:g}V_{self.i_max_A:g}A_{self.vkp_V:g}V"
        
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
    
    def prepare_test_conditions(self):
        """Prepare the list of conditions to be used."""
        tc = self.test_conditions
        
        # Generate a list of the input line voltage
        self.vin_list = tc.line_range.vin_freq
                
        # Nominal output settings
        self.nominal_output_voltage_V = tc.nominal_output_voltage_V
        self.nominal_load_current_A = tc.nominal_load_current_A
        
        # VKP setpoint
        self.vkp_V = self.i2c_test_conditions.param[0]
        
        # Rsense
        self.rsense_mohm = self.i2c_test_conditions.param[1]

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


        # Max Current based on rsense
        self.i_max_rsense_A = (self.i2c_params.IS_MAX_MV/self.rsense_mohm)
        
        # CP setpoint
        self.p_max_W = self.vkp_V*self.i_max_rsense_A
        
        self.i_max_A = self.nominal_load_current_A
        self.vout_V = self.nominal_output_voltage_V
        
        # Make all voltages in spec with Inno5Pro resolution
        self.vout_V = math.floor(int(self.vout_V*1000)/self.i2c_params.CV_RESOLUTION_MV)*self.i2c_params.CV_RESOLUTION_MV/1000
        self.vkp_V  = math.floor(int(self.vkp_V*1000)/self.i2c_params.VKP_RESOLUTION_MV)*self.i2c_params.VKP_RESOLUTION_MV/1000
        
        self.eload_type = 'CR'
        
        # Set sink Rsense to the defined Rsense value,
        self.i2c_controller.update_rsense(self.rsense_mohm)
        
        # Fixed UV Setting
        self.uva_thresh = 3
    
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
        
    def define_data_header(self):
        """Defines the data header for the excel file."""  
        header_list = [
            f'V{self.coupling} (rms)','Freq (Hz)','Io CC (LSB)','Io CC (A)',
            'Io I2C (LSB)','Io I2C (A)', 'OMF',
            'Vout I2C (V)', 'Pout I2C (W)',
            'Io eload(A)','Vo (V)','Io (A)','Po (W)']
        
        self.column_step = len(header_list)+1
        return header_list
    
    # TODO: Update with better way
    def i2c_readback(self):
        for i in range(0,5):
            if self.read_iout_cc_bits == "ERR":
                try:
                    self.read_iout_cc_bits = self.i2c_controller.read_cc()
                except:
                    pass
            
            if self.read_iout_ave_bits == "ERR":
                try:
                    self.read_iout_ave_bits = self.i2c_controller.read_iout_average()
                except:
                    pass
            
            if self.read_omf_txt == "ERR":
                try:
                    self.read_omf_txt = self.i2c_controller.read_omf_txt()
                except:
                    pass
            
            if self.read_vout_inst == "ERR":
                try:
                    self.read_vout_inst = self.i2c_controller.read_vout_v()
                except:
                    pass
            
            sleep(0.01)



    def process_data_row_load(self):
        """Create a row of data from the test data"""

        self.read_iout_cc_bits = "ERR"
        self.read_iout_ave_bits = "ERR"
        self.read_omf_txt = "ERR"
        self.read_vout_inst = "ERR"

        self.i2c_readback()
        # TODO: CLEAN UP
        td = self.test_data

        iout_eload:float = round(self.electronic_load.current,6)
        
        iout_cc_A = round(self.read_iout_cc_bits*((self.i2c_params.IS_MAX_MV/self.rsense_mohm)/self.i2c_params.CC_MAX_COUNT),6)
        iout_readback_A = round(self.read_iout_ave_bits*((self.i2c_params.IS_MAX_MV/self.rsense_mohm)/self.i2c_params.CC_MAX_COUNT),6) 
        pout_read = round(self.read_vout_inst * iout_readback_A,2)

        data_row = [
             td.vin_set_V, td.ac_freq_Hz, self.read_iout_cc_bits, iout_cc_A,
             self.read_iout_ave_bits, iout_readback_A, self.read_omf_txt,
             self.read_vout_inst, pout_read,
             iout_eload, td.vout_V, td.iout_A, td.pout_W]
        return data_row
    
    # def process_data_row_load(self):
    #     """Create a row of load data from the test data"""
    #     td = self.test_data
    #     data_row = [
    #          td.vin_set_V, td.ac_freq_Hz, None, None,None, None, None, td.vout_V, td.iout_A, 
    #         td.pout_W, td.vreg_pct, None,td.vreg_passfail]
    
    #     return data_row

    def setup_cv_cp_cc_load_steps(self):
        """Define the load setpoints for CV, CP and CC region"""
        self.Vrange_a = []
        self.Vrange_b = []
        self.Vrange_c = []
        
        # Knee point between CV and CP region
        self.iout_CP_A = self.p_max_W / self.vout_V
        
        # If knee point is greater than the nominal load current
        if self.iout_CP_A > self.i_max_A:
            self.iout_CP_A = self.i_max_A
            vkp_temp = self.vout_V
            self.CP_range =[]
        else:
            inno = self.i2c_params
            # Make the CP step 1/3 of an LSB to show staircase behavior
            cp_iout_step = inno.IS_MAX_MV/inno.CC_MAX_COUNT/self.rsense_mohm/3
            self.CP_range = np.arange(
                self.iout_CP_A*0.91, 
                self.i_max_A*1.05, 
                cp_iout_step)
            vkp_temp = self.p_max_W/(self.i_max_A*1.05)
        
        # Get iout range for CV region
        self.CV_range = np.linspace(0, self.iout_CP_A*0.9, 10)

        self.define_cc_range(vkp_temp)

    def define_cc_range(self, vkp):
        # Initial CC range using estimated knee point voltage
        # Target down to 1V and rely on UV to end the test
        cc_range_v = np.concatenate([
            np.around(np.arange(vkp-0.5, 6, -0.5),3),
            np.around(np.arange(6-0.1, 4, -0.1),3),
            np.around(np.arange(4-0.05, 1, -0.05),3)
        ])
        tmp = []

        # Clean up the CC range. Ensure target is below the knee point
        for vout in cc_range_v:
            if vout < vkp:
                # Take the resistance value from the voltage target
                tmp.append(vout/self.i_max_A)

        self.CC_range = tmp

    def clean_up_cp_range(self, min_step=0.001):
        """ Return a range of Iout that is increasing
        """

        tmp = [self.CP_range[0]]

        # Make sure that the current range for CP is increasing
        # And the minimum iout step is at least 1mA
        i_min = self.CP_range[0]
        for iout in self.CP_range:
            if (iout-i_min)>=min_step:
                tmp.append(iout)
                i_min = iout
        
        self.CP_range = tmp

    # Signals for reporting
    def status_report(self, vin_index, vin_delay = False,
                      cv_delay = False, cp_delay= False, cc_delay = False):
        """Compute the remaining steps and time. 
        Emit signals containing the computed info."""
        remaining_time_s, remaining_steps = self.estimate_remaining(
            vin_index, vin_delay, cv_delay,cp_delay, cc_delay)
        percent_completion = round((1 - remaining_steps/self.total_steps)*100,0)

        self.estimated_time.emit(remaining_time_s)
        self.progress.emit(percent_completion)

    def estimate_remaining(self, vin_index_t, vin_delay:bool = False,
                           cv_delay:bool = False, cp_delay:bool = False, cc_delay:bool = False):
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
            nonlocal vin_delay
            nonlocal cv_delay
            nonlocal cp_delay
            nonlocal cc_delay

            # Only add time if the index
            if not start_adding_time:
                if vin_index == vin_index_t:
                        start_adding_time = True
                        vin_delay = True
                        cv_delay = True
                        cp_delay = True
                        cc_delay = True
            
            if start_adding_time:
                remaining_time_s += t
                if add_step:
                    remaining_steps += 1

            return remaining_steps, remaining_time_s
        
        add_time(1)
        # Emulate the test loop to estimate the time and number of steps
        for vin_index, _ in enumerate(self.vin_list): 
            
            if vin_delay:
                # Sleep for a short time to allow the power supply to stabilize 
                add_time(2)

                # Send necessary I2C commands
                add_time(2)
                # Do the initial soak if it is the first input voltage on the list
                if vin_index == 0:
                    add_time(soak.initial_soak)
                # Or the soak per line if it is not
                else:
                    add_time(soak.soak_per_line)
            
            if cv_delay:
            # Loop through each load current level
                for iout_index, _ in enumerate(self.CV_range):                 
                    add_time(0,True)
                    # Sleep for the soak time before measuring
                    add_time(soak.soak_per_load)
                    add_time(soak.integration_time)
                    add_time(0.1)
            if cp_delay:
                for iout_index, _ in enumerate(self.CP_range):                 
                    add_time(0,True)
                    # Sleep for the soak time before measuring
                    add_time(soak.soak_per_load)
                    add_time(soak.integration_time)
                    add_time(0.1)
            if cc_delay:
                for iout_index, _ in enumerate(self.CC_range):                 
                    add_time(0,True)
                    # Sleep for the soak time before measuring
                    add_time(soak.soak_per_load)
                    add_time(soak.integration_time)
                    add_time(0.1)
                
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
            title=f"CVCPCC {nom_vout_V:g}V {iout_cc_A:g}A VKP: {self.vkp_V}V",
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
        test_data_row = self.process_data_row_load()
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
            'I2C_PARAMS':                          self.test_conditions.i2c_test_parameters.param,
            'I2C_CBX_PARAMS':                      self.test_conditions.i2c_test_parameters.cbx_param,
            'NAME':                                self.test_conditions.name}
        return d
    
    @staticmethod
    def extract_test_condition(test_item_dict:dict)->dict:
        test_object_class = I2C_VKPTest
        new_test_conditions = TestConditions(
            nominal_output_voltage_V=test_item_dict['NOMINAL_OUTPUT_VOLTAGE_V'],
            nominal_load_current_A=test_item_dict['NOMINAL_LOAD_CURRENT_A'],
            max_load_current_A=test_item_dict['MAX_LOAD_CURRENT_A'],
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
                measure_ripple=test_item_dict['GENERAL_OPTIONS_measure_ripple'],
                use_eload_data=test_item_dict['GENERAL_OPTIONS_use_eload_data'],
                eload_type=test_object_class.tc_default.general_options.eload_type,
                load_direction=test_object_class.tc_default.general_options.load_direction,
                coupling=test_item_dict['GENERAL_OPTIONS_coupling']),
            usbpd_options=test_object_class.tc_default.usbpd_options,
            line_ramp_settings=test_object_class.tc_default.line_ramp_settings,
            i2c_test_parameters=I2CTestParameters(
                params = test_item_dict['I2C_PARAMS'],
                cbx_params = test_item_dict['I2C_CBX_PARAMS']),
            name=test_item_dict['NAME'])
        return new_test_conditions