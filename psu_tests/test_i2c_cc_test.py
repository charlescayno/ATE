from psu_tests.test_object_imports import *

class I2C_CCTest(BaseTestObject):
    """
    The CC test is similar to a CVCC Test with specific conditions on the loop speed registers

    """
    title = "I2C CC"
    short_title = "CC"
    i2c_test = True

    # General UI Definitions
    ui_definitions = General_UI_Definitions()
    ui_definitions.stack_page_1 = StackWidget1Pages.LineVoltageRange
    ui_definitions.stack_page_2 = StackWidget2Pages.CVCCSettings
    ui_definitions.stack_page_3 = StackWidget3Pages.I2C_Options
    ui_definitions.multiple_cvcc_setpoints_enable = True
    ui_definitions.use_eload_data_toggle_visible = True
    
    # I2C UI definitions
    i2c_ui_definitions = I2C_UI_Definitions()
    # Line Edits
    i2c_ui_definitions.add_lineedit(label='Rsense (mΩ)', param_index=1)
    i2c_ui_definitions.add_lineedit(label='SR ZVS On',param_index=9)
    i2c_ui_definitions.add_lineedit(label='SR ZVS Delay',param_index=10)
    i2c_ui_definitions.add_lineedit(label='CC Offset',param_index=2)
    # Checkbox
    i2c_ui_definitions.add_cbx(label="SR ZVS?", contents=['Yes', 'No'], param_index=1)
    i2c_ui_definitions.add_cbx(label="Initial Mode", contents=['CCM', 'DCM'], param_index=2)
    i2c_ui_definitions.add_cbx(label="CC Offset Dir", contents=['Add', 'Subtract'], param_index=3)
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
    ui_update.measure_ripple_update = True
    ui_update.load_direction_update = False
    ui_update.eload_type_update = False
    ui_update.use_eload_data_update = False
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
        self.i2c_ui_definitions.add_lineedit(label='Rsense (mΩ)', param_index=1)
        self.i2c_ui_definitions.add_lineedit(label='SR ZVS On',param_index=9)
        self.i2c_ui_definitions.add_lineedit(label='SR ZVS Delay',param_index=10)
        self.i2c_ui_definitions.add_lineedit(label='CC Offset',param_index=2)
        # Checkbox
        self.i2c_ui_definitions.add_cbx(label="SR ZVS?", contents=['Yes', 'No'], param_index=1)
        self.i2c_ui_definitions.add_cbx(label="Initial Mode", contents=['CCM', 'DCM'], param_index=2)
        self.i2c_ui_definitions.add_cbx(label="CC Offset Dir", contents=['Add', 'Subtract'], param_index=3)
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
        self.setup_cv_cc_load_steps()
        self.total_time, self.total_steps = self.estimate_remaining(0, True, True, True)
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
        
        self.total_time, self.total_steps = self.estimate_remaining(0, True, True, True)
        self.status_report(0,True,True,True) 
        self.input_supply_eload_discharge_sequence()
        self.i2c_controller.update_rsense(self.rsense_mohm)
        
        temp_filepaths = []
        
        # Loop through each line input level
        for self.vin_index, self.vin_freq in enumerate(self.vin_list):
            # print(f"\tVin = {vin_freq[0]}V")
            self.exit_condition = ""
            self.status_report(self.vin_index,True,True,True) 
            
            self.prepare_excel_header(self.vin_index, self.column_step)
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

            self.power_meter_load.auto_range_enable()
            self.power_meter_source.current_auto_range_enable()
            self.electronic_load.reset_values()
            # Set the e-load to the minimum load level to be tested and turn it on
            self.electronic_load.set_load(self.vout_V,0,self.eload_type)
            self.electronic_load.turn_on()
            
            sleep(2)
            # Send necessary I2C commands
            self.i2c_initialize()
            sleep(1)
            self.i2c_controller.cv(self.vout_V)

            self.i2c_controller.cc(iout_A=self.i_max_A, offset=self.cc_offset)
            self.i2c_controller.cvo(self.i2c_commands.CVO_RESP_NR,
                self.i2c_commands.CVO_TIMER_8MS,False)
            
            # Turn the e-load off
            self.electronic_load.turn_off()
            
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
            
            self.omf = self.i2c_controller.read_omf()
            
            self.i2c_controller.write_2bytes_from_input(self.LS1_reg,self.LS1_DEF_LSB,self.LS1_DEF_MSB)
            self.i2c_controller.write_2bytes_from_input(self.LS2_reg,self.LS2_CV_LSB,self.LS2_CV_MSB)
            
            self.test_data.gather_data_load(integrate=False)
            
            self.status_report(self.vin_index,False,True,True)
            self.cv_region_sweep()
            
            self.status_report(self.vin_index,False,False,True)
            self.cc_region_sweep()

            # Add a blank row
            self.test_data_table.add_blank_row()
            
            self.output_dataframe=self.output_dataframe[0:0]
            
            # Set the output to 5V and let the output caps discharge
            # before turning off the eload to prevent Eload CRL OV
            sleep(1.6)
            self.i2c_initialize()
            self.i2c_controller.cv(vout_V=5)
            sleep(0.1)
            self.input_supply.turn_off()

            sleep(2)

            self.electronic_load.turn_off()
            
        
        self.export(temp_filepaths)

        # print(f"Exited test loop: {self.sheet_name}")
    
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
    
    def cv_region_sweep(self):
        """Sweep in CV region"""
        soak = self.soak_time
        # print("Entered CV loop")   
        # Loop through each load current level for the CV or CP region
        for iout_index, iout_level in enumerate(self.CV_range):
            # Trim the trailing zeros
            iout_A = float(f'{round(iout_level,6):g}')
            
            if iout_A == 0:
                eload_voltage = self.electronic_load.voltage
                self.electronic_load.set_load(eload_voltage,iout_A,self.eload_type)
                cr = self.min_cr
            else:
                # Get equivalent load resistance
                eload_voltage = self.electronic_load.voltage
                cr = round(eload_voltage/iout_A,6)
                self.electronic_load.set_load(eload_voltage,iout_A,self.eload_type)
                self.electronic_load.turn_on()
            
            if iout_A < 0.05:
                self.power_meter_load.set_current_range(0.05)
            else:
                    self.power_meter_load.current_auto_range_enable()
                        
            
            # Sleep for the soak time before measuring
            soak.do_soak_per_load()
            # Gather the data from the equipment
            if (self.power_meter_load._current_auto_range_status):
                self.power_meter_load.auto_range_enable(False)
                sleep(1)
            if (self.power_meter_source._current_auto_range_status):
                self.power_meter_source.current_auto_range_enable(False)
                sleep(1)
            self.test_data.gather_data_load(integrate=False)
            self.output_dataframe.loc[len(self.output_dataframe)]\
                = self.process_data_row_load()

            if self.test_data.vout_V < self.uva_thresh:
                print(self.test_data.vout_V)
                self.exit_condition = "Power supply shut down during CV region"
                raise Exception(self.exit_condition) 
            
            data_row = self.process_data_row_load()
            
            if self.measure_ripple:
                output_ripple_V = self.oscilloscope.get_measure(1)
                self.test_data.output_ripple_mV = round(output_ripple_V * 1000,1)

            self.write_textfile_row(self.wr, self.txt_file, data_row)
            
            # Update the data for the results page
            self.update_output_data()
            self.min_cr = cr
            
            self.power_meter_load.auto_range_enable()
            self.power_meter_source.current_auto_range_enable()

            try:
                self.omf = self.i2c_controller.read_omf()
            except Exception as e:
                # print("OMF readback failed \n")
                raise(e)
            else:
                match self.omf:
                    case self.i2c_defaults.OMF_CC_MODE:
                        if (self.vout_V >= self.vout_ls2_limit_V) and (self.i_max_A <= self.iout_ls2_limit_A):
                            # Write custom loop speed 2 setting
                            self.i2c_controller.write_2bytes_from_input(self.LS2_reg,self.LS2_LOW_CC_LSB,self.LS2_LOW_CC_MSB)
                        else:
                            self.i2c_controller.write_2bytes_from_input(self.LS2_reg,self.LS2_CC_LSB,self.LS2_CC_MSB)

                        self.cc_current_start_A = self.test_data.iout_A
                        self.cc_voltage_start_V = self.test_data.vout_V
                        # Break out of the CV loop
                        break
                    case _:
                        pass

    def cc_region_sweep(self):
        # Loop through all vout step
        # Change load according to Vout level
        
        """Sweep in CC region"""
        soak = self.soak_time
        # print("\t\tEntered CC loop")

        for vout_index, vout_level in enumerate(self.CC_range):
            self.cc_current_end_A = self.test_data.iout_A
            self.cc_voltage_end_V = self.test_data.vout_V
            v_cable = self.test_data.vout_V - self.electronic_load.voltage
            r_cable = v_cable / self.test_data.iout_A

            cr = round(vout_level/self.test_data.iout_A,6)
            cr_eload = cr - r_cable  
            if cr_eload >= self.min_cr:
                continue
            vout_V = self.electronic_load.voltage
            self.electronic_load.set_load(vout_V,vout_V/cr_eload,self.eload_type)
            self.electronic_load.turn_on()

            soak.do_soak_per_load()
            
            if (self.power_meter_load._current_auto_range_status):
                self.power_meter_load.auto_range_enable(False)
                sleep(1)
            if (self.power_meter_source._current_auto_range_status):
                self.power_meter_source.current_auto_range_enable(False)
                sleep(1)
            

            # Gather the data from the equipment
            self.test_data.gather_data_load(integrate=False)

            self.power_meter_load.auto_range_enable()
            self.power_meter_source.current_auto_range_enable()
            
            if not self.cc_data_valid():
                # print([self.test_data.vout_V, self.test_data.iout_A, self.test_data.pout_W])
                # Set eload to CRH to prevent OVP when load is turned off
                self.electronic_load.set_load(self.vout_V, 0.1, self.eload_type)
                break

            self.output_dataframe.loc[len(self.output_dataframe)]\
                = self.process_data_row_load()

            data_row = self.process_data_row_load()

            if self.measure_ripple:
                output_ripple_V = self.oscilloscope.get_measure(1)
                self.test_data.output_ripple_mV = round(output_ripple_V * 1000,1)

            self.write_textfile_row(self.wr, self.txt_file, data_row)
            
            # Update the data for the results page
            self.update_output_data()    
            self.min_cr = cr            
            try:
                self.omf = self.i2c_controller.read_omf()
            except:
                self.omf = self.i2c_defaults.OMF_CC_MODE
            
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
            
        text += f"Line Range: {self.line_range.name}, Coupling: {self.coupling}\n"
        
        if self.use_eload_data:
            text += "Load Measurement: Electonic Load"
        else:
            text += "Load Measurement: Power Meter"
        
        # text += f"\n {self.exit_condition}"
            
        self.test_list_text = text

    def unpack_test_item(self):
        """Extract the needed information from the TestItem object"""

        test_item = self.test_item

        self.parent:MainWindow = test_item.parent
        self.equipment:EquipmentHandler = self.parent.equipment

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
        self.measure_ripple:bool = self.general_options.measure_ripple
        
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
        
        self.power_meter_load.integration_settings(
            mode="NORMAL", timer_s=0)
        self.power_meter_source.integration_settings(
            mode="NORMAL", timer_s=0)
        self.power_meter_load.stop_integration()
        self.power_meter_source.stop_integration()
        self.power_meter_load.reset_integration()
        self.power_meter_source.reset_integration()

        if self.measure_ripple:
            # self.oscilloscope.setup_ripple(y_scale=0.5)
            # self.initialize_scope_settings()
            pass
        
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
        # self.i2c_controller.set_smbus_config()
        self.electronic_load.turn_off()
        self.electronic_load.reset_values()
    
    def setup_data_file(self):
        """Set up the the data frame to be used for output 
        as well as the excel Workbook"""
        self.test_data = TestData()
        
        self.test_data.use_eload_data = False
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
        self.data_file_name_ext = f'{self.data_filename}.xlsx'
        self.data_file_path = f'{self.output_folder_path}/{self.data_file_name_ext}'
        
        # Check if workbook exists
        if not os.path.exists(self.data_file_path):     
            self.wb:Workbook = openpyxl.Workbook()
            self.wb.save(self.data_file_path)
            self.wb.close()
        
        # Open the workbook    
        self.wb:Workbook = openpyxl.load_workbook(self.data_file_path)
        
        # Prepare the sheet name
        self.sheet_name = f"CC_{self.coupling}_{self.vout_V:g}V_{self.i_max_A:g}A"
        
        sheet_list = self.wb.sheetnames  
        if self.sheet_name in sheet_list:
            # Clear existing sheet of the test item
            clear_sheet(self.output_folder_path,
                    self.data_filename ,self.sheet_name)
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
        
        # Rsense
        self.rsense_mohm = self.i2c_test_conditions.param[1-1]
        
        # Calibration Offset
        self.cc_offset_dir = self.i2c_test_conditions.cbx_param[3-1]
        self.cc_offset = self.i2c_test_conditions.param[2-1]
        if self.cc_offset_dir == "Add":
            self.cc_offset = int(self.cc_offset)
        else:
            self.cc_offset = 0-int(self.cc_offset)

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
        
        self.i_max_A = self.nominal_load_current_A
        self.vout_V = self.nominal_output_voltage_V
        
        # Indicator for CV setpoint for Custom Loop Speed 2 setting
        self.vout_ls2_limit_V = 11
        
        # Indicator for CC setpoint for Custom Loop Speed 2 setting
        self.iout_ls2_limit_A = 1
        
        # Loop Speed Text
        self.ls2_text = intlist_to_hex_str([self.i2c_commands.LOOPSPEED_2_MSB_DEFAULT, self.i2c_commands.LOOPSPEED_2_LSB_DEFAULT])

        # Make all voltages in spec with Inno5Pro resolution
        trim_to_spec(self.nominal_output_voltage_V,
                     self.i2c_params.CV_RESOLUTION_MV/1000)
        
        self.eload_type = 'CR'
        
        # Set sink Rsense to the defined Rsense value,
        self.i2c_controller.update_rsense(self.rsense_mohm)
        
        # Loop Speed registers and default values
        self.LS1_reg = self.i2c_controller.registers.LOOPSPEED_1_REG
        self.LS2_reg = self.i2c_controller.registers.LOOPSPEED_2_REG
        
        # Default value for Loop Speed 1
        self.LS1_DEF_LSB = self.i2c_controller.commands.LOOPSPEED_1_LSB_DEFAULT
        self.LS1_DEF_MSB = self.i2c_controller.commands.LOOPSPEED_1_MSB_DEFAULT
        
        # Default value for Loop Speed 2 at CV
        self.LS2_CV_LSB = self.i2c_controller.commands.VST_LOOPSPEED_2_LSB
        self.LS2_CV_MSB = self.i2c_controller.commands.VST_LOOPSPEED_2_MSB
        
        # Default value for Loop Speed 2 at CC
        self.LS2_CC_LSB = self.i2c_controller.commands.LOOPSPEED_2_LSB_DEFAULT
        self.LS2_CC_MSB = self.i2c_controller.commands.LOOPSPEED_2_MSB_DEFAULT
        
        # Default value for Loop Speed 2 at CC for CV > 11 V and CC < 1 A
        self.LS2_LOW_CC_LSB = self.i2c_controller.commands.CLT_LOOPSPEED_2_LSB
        self.LS2_LOW_CC_MSB = self.i2c_controller.commands.CLT_LOOPSPEED_2_MSB
        
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
        cell2.value = 'Output Measurement'
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
    
    def define_data_header(self):
        """Defines the data header for the excel file."""  
        header_list = [
            f'V{self.coupling} (rms)','Freq (Hz)','Io CC (LSB)','Io CC (A)',
            'Io readback (LSB)','Io readback (A)', 'OMF',
            'Io eload(A)','Vo (V)','Io (A)','Po (W)',
            'LoopSpeed2']
        
        if self.measure_ripple:
            header_list.append('Vout_pp (mV)')
        
        self.column_step = len(header_list)+1
        
        return header_list
    
    def process_data_row_load(self):
        """Create a row of load data from the test data"""

        self.read_iout_cc_bits = "ERR"
        self.read_iout_ave_bits = "ERR"
        self.read_omf_txt = "ERR"
        self.read_vout_inst = "ERR"
        
        self.i2c_readback()

        td = self.test_data
        iout_eload:float = round(self.electronic_load.current,6)
        
        iout_cc_A = round(self.read_iout_cc_bits*((self.i2c_params.IS_MAX_MV/self.rsense_mohm)/self.i2c_params.CC_MAX_COUNT),6)
        iout_readback_A = round(self.read_iout_ave_bits*((self.i2c_params.IS_MAX_MV/self.rsense_mohm)/self.i2c_params.CC_MAX_COUNT),6) 
        loop_speed = self.i2c_controller.read_loop_speed_2_byte()

        data_row = [
             td.vin_set_V, td.ac_freq_Hz, self.read_iout_cc_bits, iout_cc_A,
             self.read_iout_ave_bits, iout_readback_A, self.read_omf_txt,
             iout_eload, td.vout_V, td.iout_A, td.pout_W,
             loop_speed]
        if self.measure_ripple:
            data_row.append(td.output_ripple_mV)
        return data_row

    def setup_cv_cc_load_steps(self):
        """Define the load setpoints for CV, CP and CC region"""
        
        # Get iout range for CV region
        # Make the iout step when searching for CC threshold 1/2 of an LSB
        inno = self.i2c_params
        cc_search_step = inno.IS_MAX_MV/inno.CC_MAX_COUNT/self.rsense_mohm/2
        self.CV_range = np.concatenate(
            [np.linspace(0, self.i_max_A*0.9, 10), # 0% to 90% with 10% steps
             np.arange(self.i_max_A*0.91, self.i_max_A*1.4, cc_search_step)])

        self.define_cc_range()
    
    def define_cc_range(self):
        # Initial CC range using estimated knee point voltage
        tmp = np.concatenate([
            np.around(np.arange(self.vout_V-0.25, 6, -0.25),3),       # 0.5V steps for Vout>6V
            np.around(np.arange(6-0.1, 4, -0.1),3),                 # 0.1V steps for 6V to 4V
            np.around(np.arange(4-0.05, self.uva_thresh, -0.05),3)  # 50mV steps for 4V to UV level
        ])
        # Remove the Vout values above the typical
        cc_range_v = []
        for v in tmp:
            if v < self.vout_V:
                cc_range_v.append(v)
                
        self.CC_range = cc_range_v
    
    # Signals for reporting
    def status_report(self, vin_index, vin_delay = False,
                      cv_delay = False, cc_delay = False):
        """Compute the remaining steps and time. 
        Emit signals containing the computed info."""
        remaining_time_s, remaining_steps = self.estimate_remaining(
            vin_index, vin_delay, cv_delay, cc_delay)
        percent_completion = round((1 - remaining_steps/self.total_steps)*100,0)

        self.estimated_time.emit(remaining_time_s)
        self.progress.emit(percent_completion)

    def estimate_remaining(self, vin_index_t, vin_delay:bool = False,
                           cv_delay:bool = False, cc_delay:bool = False):
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
            
        self.oscilloscope.channel_settings(
            state=ch1_enable, channel=1, scale=ch1_scale, 
            position=ch1_position, label=ch1_label, color=ch1_color,
            rel_x_position=ch1_rel_x_position,
            rel_y_position=ch1_rel_y_position, 
            bandwidth=ch1_bw, 
            coupling=ch1_coupling, 
            offset=ch1_offset)
            
        self.oscilloscope.channel_settings(
            state=ch2_enable, channel=2, scale=ch2_scale, 
            position=ch2_position, label=ch2_label, color=ch2_color, 
            rel_x_position=ch2_rel_x_position,
            rel_y_position=ch2_rel_y_position, 
            bandwidth=ch2_bw, 
            coupling=ch2_coupling, 
            offset=ch2_offset)
        
        self.oscilloscope.channel_settings(
            state=ch3_enable, channel=3, scale=ch3_scale, 
            position=ch3_position, label=ch3_label, color=ch3_color, 
            rel_x_position=ch3_rel_x_position,
            rel_y_position=ch3_rel_y_position, 
            bandwidth=ch3_bw, 
            coupling=ch3_coupling, 
            offset=ch3_offset)
        
        self.oscilloscope.channel_settings(
            state=ch4_enable, channel=4, scale=ch4_scale, 
            position=ch4_position, label=ch4_label, color=ch4_color, 
            rel_x_position=ch4_rel_x_position,
            rel_y_position=ch4_rel_y_position, 
            bandwidth=ch4_bw, 
            coupling=ch4_coupling, 
            offset=ch4_offset)
        
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
            col_vout=col_vout,
            cc_current_start_A=self.cc_current_start_A,
            cc_voltage_start_V=self.cc_voltage_start_V,
            cc_current_end_A=self.cc_current_end_A,
            cc_voltage_end_V=self.cc_voltage_end_V,
            x_axis_wide_range=False)

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
        test_object_class = I2C_CCTest
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