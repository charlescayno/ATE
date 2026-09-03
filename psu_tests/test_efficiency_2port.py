from psu_tests.test_object_imports import *

class EfficiencyTest_2Port(BaseTestObject):
    """
    The efficiency test for 2-Port / Dual Output supplies.
    Supports Option A (Proportional Sync), Option B (Cross-Regulation Matrix),
    and Option C (Fixed Aux / Swept Main).
    """

    title = "Efficiency 2 Port"

    # General UI Definitions
    ui_definitions = General_UI_Definitions()
    ui_definitions.stack_page_1 = StackWidget1Pages.LineVoltageRange
    ui_definitions.stack_page_2 = StackWidget2Pages.LoadCurrentRange
    ui_definitions.stack_page_3 = StackWidget3Pages.I2C_Options

    ui_definitions.usb_pd_device_toggle_visible = True
    ui_definitions.nominal_iout_visible = True
    ui_definitions.nominal_vout_visible = True
    ui_definitions.nominal_vout_enable = True  
    
    ui_definitions.load_type_visible = True
    ui_definitions.load_direction_cbx_enabled = False
    ui_definitions.load_range_selection_enabled = False
        
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
    ui_update.load_direction_update = True
    ui_update.eload_type_update = True
    ui_update.use_eload_data_update = True
    ui_update.i2c_params_update = True

    i2c_ui_definitions = I2C_UI_Definitions()
    i2c_ui_definitions.add_lineedit("Nominal Vout 2 (V)", 1)
    i2c_ui_definitions.add_lineedit("Nominal Iout 2 (A)", 2)
    i2c_ui_definitions.add_lineedit("Fixed Aux Load (A)", 3)
    i2c_ui_definitions.add_lineedit("Port 2 Loads (%)", 4)
    i2c_ui_definitions.add_cbx("Dual Load Mode", [
        "Option A: Proportional Sync (Both Ports 100% -> 10%)",
        "Option B: Cross-Reg Matrix (Port 2 at Specified % Loads)",
        "Option C: Fixed Aux / Swept Main (Port 2 Fixed Load)"
    ], 1)

    @classmethod
    def get_ui_definitions(self, flags:UIChangeFlags = UIChangeFlags()):
        """Return a UI definition based on the UIChangeFlags object."""
        temp_ui_def = copy(self.ui_definitions)

        if flags.usb_pd_device_toggle_checked:
            temp_ui_def.usbpd_sourcecaps_table_visible = True
            temp_ui_def.usbpd_tracking_pdo_chk_visible = True
            temp_ui_def.usbpd_getsourcecaps_btn_visible = True
            temp_ui_def.nominal_vout_visible = False
            temp_ui_def.nominal_vout_enable = False
            temp_ui_def.add_test_button_2_txt = 'Test All Fixed PDO'
            temp_ui_def.add_test_button_2_visible = True
            return temp_ui_def
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
        load_range= LoadSettings.LOAD_EFF,
        soak_time= SoaktimeSettings.SOAK_EFF,
        general_options = GeneralOptions(),
        usbpd_options = USBPDOptions(),
        line_ramp_settings = LineRamp(),
        i2c_test_parameters = I2CTestParameters(params=[12.0, 2.0, 0.0, "100, 50, 0"], cbx_params=["Option A: Proportional Sync (Both Ports 100% -> 10%)"]))

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
        self.total_time, self.total_steps = self.estimate_remaining(0, 0, vin_delays=True)
        self.estimated_time_s = self.total_time
        self.message_closed = False

        self.with_data = False
        self.update_test_list_text()

    def with_waveform_capture(self):
        return False

    def run(self):
        """ Run the test for this TestObject
        This method will be run on a separate thread to prevent UI freezing
        """
        if self.parent.run_settings['debug']:
            debugpy.debug_this_thread()
        global test_control_flags

        try:
            self.status_update.emit(TestStatus.IN_PROGRESS)
            self.setup_equipment()
            self.prepare_test_conditions()
            self.setup_data_file()
            self.test_loop()
        except TestStopped:
            self.cleanup_usbpd_pps_operation()
            self.input_supply_eload_discharge_sequence()
            print("Test Stopped")
            self.status_update.emit(TestStatus.STOPPED)
        except TestSkipped:
            self.cleanup_usbpd_pps_operation()
            self.input_supply_eload_discharge_sequence()
            print("Test Skipped")
            self.status_update.emit(TestStatus.SKIPPED)
        except Exception:
            print(traceback.format_exc())
            with open('error_log.txt', 'a') as f:
                f.write(traceback.format_exc() + '\n')
            self.cleanup_usbpd_pps_operation()
            if self.usbpd_test and self.usbpd_sink:
                self.usbpd_sink.usb_pd_initialize()
            self.input_supply_eload_discharge_sequence()
            print("Test Failed")
            self.status_update.emit(TestStatus.FAILED)
        else:
            self.cleanup_usbpd_pps_operation()
            self.input_supply_eload_discharge_sequence()
            self.estimated_time_s = 0
            self.status_update.emit(TestStatus.COMPLETE)
            
    def create_message_popup(self, title:str, message:str, message_type:MessageType):
        self.message.emit(title, message, message_type)
        while not self.message_closed:
            sleep(0.5)
            if test_control_flags['StopTest']:
                raise TestStopped
            if test_control_flags['SkipTest']:
                raise TestSkipped
        self.message_closed = False   
       
    def test_loop(self):
        soak = self.soak_time
        
        self.total_time, self.total_steps = self.estimate_remaining(0, 0, vin_delays=True)
        self.status_report(0, 0, vin_delays=True)
        if self.usbpd_test:
            self.input_supply_eload_discharge_sequence()
        
        # Loop through each line input level
        for self.vin_index, self.vin_freq in enumerate(self.vin_list): 
            self.input_supply.set_voltage_with_coupling(voltage=self.vin_freq[0], coupling=self.coupling)  
            if self.coupling == AC_SOURCE_COUPLING.AC:
                self.input_supply.frequency = self.vin_freq[1]
            self.source_vout = self.vin_freq[0]
            
            self.test_data.vin_set_V = self.vin_freq[0]
            self.test_data.ac_freq_Hz = self.vin_freq[1]
            
            self.create_new_plot_series()

            self.input_supply.turn_on()

            if self.power_meter_load:
                self.power_meter_load.auto_range_enable()
            if self.power_meter_load_2:
                self.power_meter_load_2.auto_range_enable()
            if self.power_meter_source:
                self.power_meter_source.current_auto_range_enable()

            sleep(2)

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
                self.usb_pd_request(vout_V=self.vout_V, iout_A=self.i_rated_A)
            
            # Initial load setting
            init_i1 = self.load_pairs[0][0] if len(self.load_pairs) > 0 else 0
            init_i2 = self.load_pairs[0][1] if len(self.load_pairs) > 0 else 0
            self.electronic_load.set_load(self.vout_V, init_i1, self.eload_type)
            if self.electronic_load_2 is not None:
                self.electronic_load_2.set_load(self.vout_2_V, init_i2, self.eload_type)
            
            if init_i1 > 0:
                self.electronic_load.turn_on()
            else:
                self.electronic_load.turn_off()

            if self.electronic_load_2 is not None:
                if init_i2 > 0:
                    self.electronic_load_2.turn_on()
                else:
                    self.electronic_load_2.turn_off()
            
            sleep(2)
            self.correct_source_output()

            if self.vin_index == 0:
                soak.do_initial_soak()
            else:
                soak.do_soak_per_line()
            
            # Loop through each load current level pair
            for load_index, (i1_A, i2_A, ch1_lbl, ch2_lbl) in enumerate(self.load_pairs):
                self.status_report(self.vin_index, load_index, vin_delays=False)
                
                self.current_ch1_lbl = ch1_lbl
                self.current_ch2_lbl = ch2_lbl

                self.electronic_load.set_load(self.vout_V, i1_A, self.eload_type)
                if self.electronic_load_2 is not None:
                    self.electronic_load_2.set_load(self.vout_2_V, i2_A, self.eload_type)
                
                if i1_A > 0:
                    self.electronic_load.turn_on()
                else:
                    self.electronic_load.turn_off()
                
                if self.electronic_load_2 is not None:
                    if i2_A > 0:
                        self.electronic_load_2.turn_on()
                    else:
                        self.electronic_load_2.turn_off()

                if self.power_meter_load is not None:
                    if i1_A < 0.05:
                        self.power_meter_load.set_current_range(0.05)
                    else:
                        self.power_meter_load.current_auto_range_enable()
                
                if self.power_meter_load_2 is not None:
                    if i2_A < 0.05:
                        self.power_meter_load_2.set_current_range(0.05)
                    else:
                        self.power_meter_load_2.current_auto_range_enable()

                sleep(2)
                self.correct_source_output()
                soak.do_soak_per_load()
                
                if self.power_meter_load and getattr(self.power_meter_load, '_current_auto_range_status', False):
                    self.power_meter_load.auto_range_enable(False)
                    sleep(0.5)
                if self.power_meter_load_2 and getattr(self.power_meter_load_2, '_current_auto_range_status', False):
                    self.power_meter_load_2.auto_range_enable(False)
                    sleep(0.5)
                if self.power_meter_source and getattr(self.power_meter_source, '_current_auto_range_status', False):
                    self.power_meter_source.current_auto_range_enable(False)
                    sleep(0.5)
                
                self.test_data.gather_data(coupling=self.coupling, usb_pd=self.usbpd_test)
                if self.power_meter_load_2 or self.electronic_load_2:
                    self.test_data_2.gather_data_load(integrate=False, force_use_eload_data=self.use_eload_data)
                    self.test_data_2.vreg_pct = ((self.test_data_2.vout_V - self.vout_2_V) / self.vout_2_V) * 100 if self.vout_2_V else 0
                else:
                    self.test_data_2.vout_V = self.vout_2_V
                    self.test_data_2.iout_A = i2_A
                    self.test_data_2.pout_W = self.vout_2_V * i2_A
                    self.test_data_2.vreg_pct = 0.0

                self.po_total_W = self.test_data.pout_W + self.test_data_2.pout_W
                self.eff_total_pct = (self.po_total_W / self.test_data.pin_W * 100) if self.test_data.pin_W > 0 else 0
                
                self.output_dataframe.loc[len(self.output_dataframe)] = self.process_data_row() 
                self.update_output_data()

                if self.power_meter_load:
                    self.power_meter_load.auto_range_enable()
                if self.power_meter_load_2:
                    self.power_meter_load_2.auto_range_enable()
                if self.power_meter_source:
                    self.power_meter_source.current_auto_range_enable()
            
            self.test_data_table.add_blank_row()
            
            if self.vin_index > 0:
                anchor = f"A{5+1+self.vin_index*(len(self.load_pairs)+1)}"
                eff_anchor = f"N{5+1+self.vin_index*(len(self.load_pairs)+1)}"
            else:
                anchor = "A5"
                eff_anchor = "N5"

            export_to_excel(
                self.output_dataframe, self.output_folder_path, 
                self.data_filename, self.sheet_name, anchor)
            
            export_to_excel(
                self.efficiency_dataframe, self.output_folder_path, 
                self.data_filename, self.sheet_name, eff_anchor)
             
            self.output_dataframe = self.output_dataframe[0:0]
            self.efficiency_dataframe = self.efficiency_dataframe[0:0]
            
            if self.usbpd_test:
                self.input_supply_eload_discharge_sequence()
                
            sleep(3)
        
    def usb_pd_request(self, vout_V:float, iout_A:float):
        if self.usbpd_options.pdo_type == SUPPLY_TYPE.FIXED:
            self.usbpd_sink.fpdo_request(vbus_V=vout_V, iout_max_A=iout_A)
        elif self.usbpd_options.pdo_type == SUPPLY_TYPE.AUGMENTED:
            if self.usbpd_options.augmented_type == AUGMENTED_TYPE.SPR_PPS:
                self.usbpd_sink.pps_request(vout_V=vout_V, iout_max_A=iout_A)
            elif self.usbpd_options.augmented_type == AUGMENTED_TYPE.EPR_AVS:
                self.usbpd_sink.epr_avs_request(vout_V=vout_V, iout_max_A=iout_A)
            elif self.usbpd_options.augmented_type == AUGMENTED_TYPE.SPR_AVS:
                self.usbpd_sink.spr_avs_request(vout_V=vout_V, iout_max_A=iout_A)
                
    def cleanup_usbpd_pps_operation(self):
        if self.usbpd_test:
            if self.usbpd_options.augmented_type == AUGMENTED_TYPE.SPR_PPS:
                self.usbpd_sink.pps_thread_cleanup()
                sleep(0.5)        
    
    def input_supply_eload_discharge_sequence(self):
        self.equipment.input_supply_eload_discharge_sequence(self.i_max_A/3, coupling=self.coupling)
        if self.electronic_load_2 is not None:
            self.electronic_load_2.turn_off()
    
    def correct_source_output(self):
        """Remove the offset in the measured input by adjusting the source voltage"""
        vin = None
        for _ in range(10):
            vin = self.power_meter_source.voltage
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
        if self.status == TestStatus.COMPLETE:
            self.estimated_time_txt = ''
            self.progress_txt = '100'
        elif self.status in [TestStatus.STOPPED, TestStatus.SKIPPED]:
            self.estimated_time_txt = ''
            self.progress_txt = ''
        else:
            self.estimated_time_txt = f'{datetime.timedelta(seconds=round(self.estimated_time_s,0))}'
            self.progress_txt = str(self.progress_pct)
            
        if not self.progress_txt == '':
            self.progress_txt += '%'
        
        text = f"{self.title}: Ch1: {round(self.vout_V,3):g}V, {round(self.i_max_A,3):g}A | Ch2: {round(self.vout_2_V,3):g}V, {round(self.i_max_2_A,3):g}A\n" 
        text += f"Mode: {self.dual_load_mode}\n"
        
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

        self.test_type_index = test_item.test_type_index
        self.test_conditions:TestConditions = test_item.test_conditions

        self.usbpd_options:USBPDOptions = self.test_conditions.usbpd_options
        self.usbpd_test:bool = self.usbpd_options.usbpd_test
        self.tracking_pdo_requests:bool = self.usbpd_options.tracking_pdo_request

        self.general_options:GeneralOptions = self.test_conditions.general_options
        self.eload_type:str = self.general_options.eload_type
        self.use_eload_data:bool = self.general_options.use_eload_data
        self.coupling:str = self.general_options.coupling

        self.nominal_load_current_A:float = self.test_conditions.nominal_load_current_A
        self.nominal_output_voltage_V:float = self.test_conditions.nominal_output_voltage_V
        self.vout_V:float = self.nominal_output_voltage_V
        self.i_max_A:float = self.nominal_load_current_A

        self.line_range:LineRange = self.test_conditions.line_range
        self.load_range_pct:LoadRange = self.test_conditions.load_range
        self.soak_time:SoakTime = self.test_conditions.soak_time

        # I2C / Dual Port Parameters
        self.i2c_test_parameters = getattr(self.test_conditions, 'i2c_test_parameters', None)
        if self.i2c_test_parameters:
            self.vout_2_V = float(self.i2c_test_parameters.param[0]) if (len(self.i2c_test_parameters.param) > 0 and self.i2c_test_parameters.param[0]) else 12.0
            self.i_max_2_A = float(self.i2c_test_parameters.param[1]) if (len(self.i2c_test_parameters.param) > 1 and self.i2c_test_parameters.param[1]) else 2.0
            self.fixed_aux_A = float(self.i2c_test_parameters.param[2]) if (len(self.i2c_test_parameters.param) > 2 and self.i2c_test_parameters.param[2]) else 0.0
            cross_reg_raw = self.i2c_test_parameters.param[3] if len(self.i2c_test_parameters.param) > 3 else "100, 50, 0"
            try:
                self.cross_reg_pct2_list = [float(x.strip().rstrip('%')) for x in str(cross_reg_raw).split(',') if x.strip()]
                if not self.cross_reg_pct2_list:
                    self.cross_reg_pct2_list = [100.0, 50.0, 0.0]
            except Exception:
                self.cross_reg_pct2_list = [100.0, 50.0, 0.0]
            cbx_mode = str(self.i2c_test_parameters.cbx_param[0]) if len(self.i2c_test_parameters.cbx_param) > 0 else ""
            if "Option B" in cbx_mode:
                self.dual_load_mode = "Option B: Cross-Reg Matrix"
            elif "Option C" in cbx_mode:
                self.dual_load_mode = "Option C: Fixed Aux/Swept Main"
            else:
                self.dual_load_mode = "Option A: Proportional Sync"
        else:
            self.vout_2_V = 12.0
            self.i_max_2_A = 2.0
            self.fixed_aux_A = 0.0
            self.cross_reg_pct2_list = [100.0, 50.0, 0.0]
            self.dual_load_mode = "Option A: Proportional Sync"

        self.test_progress:float = 0 
        self.test_complete:bool = False
    
    def setup_equipment(self):
        """Set up the assignment and initialization of equipment"""
        self.ac_source = self.equipment.ac_source
        self.dc_source = self.equipment.dc_source
        if (self.dc_source is not None) and (self.coupling == AC_SOURCE_COUPLING.DC):
            self.input_supply = self.dc_source
        else:
            if self.ac_source is not None:
                self.input_supply = self.ac_source
            else:
                raise ConnectionError("No Input Supply Connected")
        self.power_meter_source = self.equipment.power_meter_source
        self.power_meter_load = self.equipment.power_meter_load_1
        self.power_meter_load_2 = self.equipment.power_meter_load_2
        self.electronic_load = self.equipment.electronic_load_1
        self.electronic_load_2 = self.equipment.electronic_load_2
        self.usbpd_sink = self.equipment.usbpd_sink
        self.oscilloscope = self.equipment.oscilloscope

        if self.power_meter_load is not None:
            self.power_meter_load.integration_settings(
                mode="NORMAL", timer_s=self.soak_time.integration_time)
            self.power_meter_load.stop_integration()
            self.power_meter_load.reset_integration()

        if self.power_meter_load_2 is not None:
            self.power_meter_load_2.integration_settings(
                mode="NORMAL", timer_s=self.soak_time.integration_time)
            self.power_meter_load_2.stop_integration()
            self.power_meter_load_2.reset_integration()

        if self.power_meter_source is not None:
            self.power_meter_source.integration_settings(
                mode="NORMAL", timer_s=self.soak_time.integration_time)
            self.power_meter_source.stop_integration()
            self.power_meter_source.reset_integration()

        if self.electronic_load is not None:
            self.electronic_load.reset_values()

        if self.electronic_load_2 is not None:
            self.electronic_load_2.reset_values()

    def setup_data_file(self):
        """Set up the data frame to be used for output 
        as well as the excel Workbook"""
        self.test_data = TestData()
        self.test_data.vout_nom_V = self.vout_V
        self.test_data.use_eload_data = self.use_eload_data
        self.test_data.source_power_meter = self.power_meter_source
        self.test_data.load_power_meter = self.power_meter_load
        self.test_data.electronic_load = self.electronic_load

        self.test_data_2 = TestData()
        self.test_data_2.vout_nom_V = self.vout_2_V
        self.test_data_2.use_eload_data = self.use_eload_data
        self.test_data_2.load_power_meter = self.power_meter_load_2
        self.test_data_2.electronic_load = self.electronic_load_2

        # Prepare output and efficiency dataframe
        self.header_list = self.define_data_header()
        self.output_dataframe = dataframe_from_headers(self.header_list)
        self.efficiency_header = ['Avg_Eff','DOE6 Limit', 'COC5 T2 Limit', 'COC5_T2_10%','Pass/Fail']
        self.efficiency_dataframe = dataframe_from_headers(self.efficiency_header)
        
        if not os.path.exists(self.output_folder_path):
            os.mkdir(self.output_folder_path)
        self.data_filename = f'{self.title} Test {self.vout_V:g}V'
        self.data_file_path = f'{self.output_folder_path}/{self.data_filename}.xlsx'
        
        # Check if workbook exists
        if not os.path.exists(self.data_file_path):     
            self.wb:Workbook = openpyxl.Workbook()
            self.wb.save(self.data_file_path)
            self.wb.close()
            
        # Open the workbook    
        self.wb:Workbook = openpyxl.load_workbook(self.data_file_path)
        
        # Prepare the sheet name
        self.sheet_name = f"AveEff_{self.coupling}_{round(self.vout_V,3):g}V_{round(self.i_max_A,3):g}A"

        sheet_list = self.wb.sheetnames  
        if self.sheet_name in sheet_list:
            clear_sheet(self.output_folder_path, self.data_filename, self.sheet_name)
            self.wb:Workbook = openpyxl.load_workbook(self.data_file_path)
            self.ws:Worksheet = self.wb[self.sheet_name]
        else:
            self.ws:Worksheet = self.wb.create_sheet(title=self.sheet_name)

        self.prepare_sheet_formatting()
        self.define_output_data_objects()
        
    def prepare_sheet_formatting(self):
        """Merge the cells for the header."""
        self.ws.merge_cells('A4:B4')
        self.ws['A4'] = 'Load Condition'
        self.ws['A4'].alignment = Alignment(horizontal='center')
        self.ws.merge_cells('C4:D4')
        self.ws['C4'] = 'Input Set'
        self.ws['C4'].alignment = Alignment(horizontal='center')
        self.ws.merge_cells('E4:I4')
        self.ws['E4'] = 'Input Measurement'
        self.ws['E4'].alignment = Alignment(horizontal='center')
        self.ws.merge_cells('J4:M4')
        self.ws['J4'] = 'Output 1 Measurement'
        self.ws['J4'].alignment = Alignment(horizontal='center')
        self.ws.merge_cells('N4:Q4')
        self.ws['N4'] = 'Output 2 Measurement'
        self.ws['N4'].alignment = Alignment(horizontal='center')
        self.ws.merge_cells('R4:S4')
        self.ws['R4'] = 'Total Power & Efficiency'
        self.ws['R4'].alignment = Alignment(horizontal='center')
        self.wb.save(self.data_file_path)
        self.wb.close()

    def prepare_test_conditions(self):
        """Prepare the list of conditions to be used."""
        test_conditions = self.test_conditions
        
        self.vin_list = test_conditions.line_range.vin_freq
        
        self.i_max_A = test_conditions.nominal_load_current_A
        self.vout_V = test_conditions.nominal_output_voltage_V
        self.i_rated_A = test_conditions.max_load_current_A

        # I2C / Dual Port Parameters
        self.i2c_test_parameters = getattr(test_conditions, 'i2c_test_parameters', None)
        if self.i2c_test_parameters:
            self.vout_2_V = float(self.i2c_test_parameters.param[0]) if (len(self.i2c_test_parameters.param) > 0 and self.i2c_test_parameters.param[0]) else 12.0
            self.i_max_2_A = float(self.i2c_test_parameters.param[1]) if (len(self.i2c_test_parameters.param) > 1 and self.i2c_test_parameters.param[1]) else 2.0
            self.fixed_aux_A = float(self.i2c_test_parameters.param[2]) if (len(self.i2c_test_parameters.param) > 2 and self.i2c_test_parameters.param[2]) else 0.0
            cross_reg_raw = self.i2c_test_parameters.param[3] if len(self.i2c_test_parameters.param) > 3 else "100, 50, 0"
            try:
                self.cross_reg_pct2_list = [float(x.strip().rstrip('%')) for x in str(cross_reg_raw).split(',') if x.strip()]
                if not self.cross_reg_pct2_list:
                    self.cross_reg_pct2_list = [100.0, 50.0, 0.0]
            except Exception:
                self.cross_reg_pct2_list = [100.0, 50.0, 0.0]
            cbx_mode = str(self.i2c_test_parameters.cbx_param[0]) if len(self.i2c_test_parameters.cbx_param) > 0 else ""
            if "Option B" in cbx_mode:
                self.dual_load_mode = "Option B: Cross-Reg Matrix"
            elif "Option C" in cbx_mode:
                self.dual_load_mode = "Option C: Fixed Aux/Swept Main"
            else:
                self.dual_load_mode = "Option A: Proportional Sync"
        else:
            self.vout_2_V = 12.0
            self.i_max_2_A = 2.0
            self.fixed_aux_A = 0.0
            self.cross_reg_pct2_list = [100.0, 50.0, 0.0]
            self.dual_load_mode = "Option A: Proportional Sync"
        
        self.load_pct_list = test_conditions.load_range.check_load_direction(self.general_options.load_direction)

        self.load_pairs = []
        if "Option A" in self.dual_load_mode:
            for pct in self.load_pct_list:
                i1 = (pct / 100.0) * self.i_max_A
                i2 = (pct / 100.0) * self.i_max_2_A
                self.load_pairs.append((i1, i2, f"{pct}%", f"{pct}%"))
        elif "Option B" in self.dual_load_mode:
            for pct2 in self.cross_reg_pct2_list:
                i2 = (pct2 / 100.0) * self.i_max_2_A
                for pct1 in self.load_pct_list:
                    i1 = (pct1 / 100.0) * self.i_max_A
                    self.load_pairs.append((i1, i2, f"{pct1}%", f"{pct2:g}%"))
        elif "Option C" in self.dual_load_mode:
            for pct in self.load_pct_list:
                i1 = (pct / 100.0) * self.i_max_A
                self.load_pairs.append((i1, self.fixed_aux_A, f"{pct}%", f"{round(self.fixed_aux_A, 3):g}A"))
        else:
            for pct in self.load_pct_list:
                i1 = (pct / 100.0) * self.i_max_A
                i2 = (pct / 100.0) * self.i_max_2_A
                self.load_pairs.append((i1, i2, f"{pct}%", f"{pct}%"))
        
        self.iout_list_A = [p[0] for p in self.load_pairs]

    def define_data_header(self):
        header_list = [
            'Ch1 Load', 'Ch2 Load', f'V{self.coupling} (rms)', 'Freq (Hz)', 'Vin (rms)', 'Iin (mA)',
            'Pin (W)', 'PF', '%THD', 'Vo1 (V)', 'Io1 (A)', 'Po1 (W)',
            '%V Reg 1', 'Vo2 (V)', 'Io2 (A)', 'Po2 (W)', '%V Reg 2',
            'Po_Total (W)', 'Efficiency (%)']
        return header_list

    def process_data_row(self):
        data_row = [
            self.current_ch1_lbl, self.current_ch2_lbl, self.test_data.vin_set_V, self.test_data.ac_freq_Hz, 
            self.test_data.vin_V, self.test_data.iin_mA, self.test_data.pin_W, self.test_data.PF, self.test_data.thd_pct, 
            self.test_data.vout_V, self.test_data.iout_A, self.test_data.pout_W, self.test_data.vreg_pct,
            self.test_data_2.vout_V, self.test_data_2.iout_A, self.test_data_2.pout_W, self.test_data_2.vreg_pct,
            self.po_total_W, self.eff_total_pct]
        return data_row
    
    def status_report(self, vin_index, load_index, vin_delays):
        remaining_time_s, remaining_steps = self.estimate_remaining(vin_index, load_index, vin_delays)
        percent_completion = round((1 - remaining_steps/self.total_steps)*100,0) if self.total_steps else 0

        self.estimated_time.emit(remaining_time_s)
        self.progress.emit(percent_completion)

    def estimate_remaining(self, vin_index_t, load_index_t, vin_delays:bool = True):
        soak = self.soak_time

        remaining_time_s = 0
        remaining_steps = 0
        load_index = 0
        vin_index = 0
        start_adding_time = False

        def add_time(t, add_step:bool = False):
            nonlocal remaining_steps
            nonlocal remaining_time_s
            nonlocal start_adding_time
            nonlocal vin_index
            nonlocal vin_index_t
            nonlocal load_index
            nonlocal load_index_t
            nonlocal vin_delays

            if not start_adding_time:
                if vin_index == vin_index_t:
                    if load_index == load_index_t:
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
                add_time(2)
                if self.usbpd_test:
                    add_time(1)
                if vin_index == 0:
                    add_time(soak.initial_soak)
                else:
                    add_time(soak.soak_per_line)
            
            for load_index, _ in enumerate(self.load_pairs):                 
                if self.tracking_pdo_requests: 
                    add_time(1)
                add_time(2, True)
                add_time(soak.soak_per_load)
                add_time(soak.integration_time)
                add_time(1.7)

            add_time(3)
        
        return remaining_time_s, remaining_steps

    def create_eff_table(self):
        try:
            generate_table_AveEff(
                vin_step = len(self.vin_list),
                coupling = self.coupling,
                sheet_name = self.sheet_name,
                wb_filepath = self.data_file_path)
        except Exception:
            pass
        
    ###########################################################################
    #               Output Data Processing for Test Results Page              #
    ###########################################################################
    def define_output_data_objects(self):
        """Define the objects that will be viewable in the test results page"""
        self.load_vs_efficiency_plot = PlottableObject(
            title="Efficiency vs Load",
            type=PlotType.LINE,
            x_label="Ch1 Load Current (A)",
            y_label="Efficiency (%)",
            x_range=(0, self.nominal_load_current_A),
            y_range=(80, 100),
            plot_series_list=[])
        
        self.ch1_vreg_plot = PlottableObject(
            title="Channel 1 Regulation",
            type=PlotType.LINE,
            x_label="Ch1 Current (A)",
            y_label="Ch1 Voltage (V)",
            x_range=(0, self.nominal_load_current_A),
            y_range=(0, self.vout_V * 1.1),
            plot_series_list=[])

        self.ch2_vreg_plot = PlottableObject(
            title="Channel 2 Regulation",
            type=PlotType.LINE,
            x_label="Ch2 Current (A)",
            y_label="Ch2 Voltage (V)",
            x_range=(0, self.i_max_2_A),
            y_range=(0, self.vout_2_V * 1.1),
            plot_series_list=[])
        
        self.test_data_table = DataTable(
            header=self.header_list, data=[])

        self.with_data = True
        
    def create_new_plot_series(self):
        """Create a new data series for each plottable object
        with the current input voltage as name."""
        series_name = f'{self.vin_list[self.vin_index][0]:3g} V'
        self.load_vs_efficiency_plot.add_plot_series(
            name=series_name,
            x_values=[],
            y_values=[])
        self.ch1_vreg_plot.add_plot_series(
            name=series_name,
            x_values=[],
            y_values=[])
        self.ch2_vreg_plot.add_plot_series(
            name=series_name,
            x_values=[],
            y_values=[])

    def update_output_data(self):
        """Update the plots and numeric data
        Emit a signal containing the processed info"""
        td1 = self.test_data
        td2 = self.test_data_2

        plottables = []

        self.load_vs_efficiency_plot.append_plot_data(
            plot_index=self.vin_index,
            x=td1.iout_A,
            y=self.eff_total_pct)
        plottables.append(self.load_vs_efficiency_plot)

        self.ch1_vreg_plot.append_plot_data(
            plot_index=self.vin_index,
            x=td1.iout_A,
            y=td1.vout_V)
        plottables.append(self.ch1_vreg_plot)

        self.ch2_vreg_plot.append_plot_data(
            plot_index=self.vin_index,
            x=td2.iout_A,
            y=td2.vout_V)
        plottables.append(self.ch2_vreg_plot)
            
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
            'I2C_PARAMS':                          getattr(self.test_conditions.i2c_test_parameters, 'param', [0]*10),
            'I2C_CBX_PARAMS':                      getattr(self.test_conditions.i2c_test_parameters, 'cbx_param', [0]*4),
            'NAME':                                self.test_conditions.name}
        return d
    
    @staticmethod
    def extract_test_condition(test_item_dict:dict)->dict:
        test_object_class = EfficiencyTest_2Port
        i2c_params = test_item_dict.get('I2C_PARAMS', [0]*10)
        i2c_cbx_params = test_item_dict.get('I2C_CBX_PARAMS', [0]*4)
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
            i2c_test_parameters=I2CTestParameters(params=i2c_params, cbx_params=i2c_cbx_params),
            name=test_item_dict['NAME'])
        return new_test_conditions
