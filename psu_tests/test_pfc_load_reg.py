from psu_tests.test_object_imports import *
    
class PFC_LoadRegTest(BaseTestObject):
    """
    The CDC test is similar to a Load Regulation test with just the CDC register changed

    """
    title = "PFC LoadReg"
    short_title = "LoadReg"
    i2c_test = False

    # General UI Definitions
    ui_definitions = General_UI_Definitions()
    ui_definitions.stack_page_1 = StackWidget1Pages.LineVoltageRange
    ui_definitions.stack_page_2 = StackWidget2Pages.LoadCurrentRange
    ui_definitions.stack_page_3 = StackWidget3Pages.I2C_Options

    # ui_definitions.load_type_visible = True # Force Eload type to CR
    ui_definitions.measure_ripple_visible = True
    
    # I2C UI definitions
    i2c_ui_definitions = I2C_UI_Definitions()
    # Line Edits
    i2c_ui_definitions.add_lineedit(label='Low Line Vout (V)', param_index=1)
    i2c_ui_definitions.add_lineedit(label='High Line Vout (V)', param_index=2)

    i2c_ui_definitions.add_lineedit(label='Output Power (W)', param_index=4)
    # Combo box
    i2c_ui_definitions.add_cbx(label="Boost Follower?", contents=['Yes', 'No'], param_index=1)
    
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
        load_range= LoadSettings.LOAD_10_PCT_STEP,
        soak_time= SoaktimeSettings.SOAK_LOAD_REG,
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
            self.input_supply_eload_discharge_sequence()
            print("Test Stopped")
            self.status_update.emit(TestStatus.STOPPED)
        
        except TestSkipped as e:
            # If there is an unhandled error inside the loop
            self.input_supply_eload_discharge_sequence()
            print("Test Skipped")
            self.status_update.emit(TestStatus.SKIPPED)

        except Exception as e:
            print(traceback.format_exc())
            # If there is an unhandled error inside the loop
            self.input_supply_eload_discharge_sequence()
            print("Test Failed")
            self.status_update.emit(TestStatus.FAILED)

        else:
            # If all goes well
            # Emit a status_update signal to signal that the test is complete

            self.input_supply_eload_discharge_sequence()

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
        self.input_supply_eload_discharge_sequence()
        
        temp_filepaths = []
        
        # Loop through each line input level
        for self.vin_index, self.vin_freq in enumerate(self.vin_list):
        
            # Set eload to approximate half load
            init_iout = self.output_power/self.vout_V * 0.5
            self.electronic_load.set_load(self.vout_V, init_iout, self.eload_type)

            # Extract the values from the vin_freq
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

            if self.power_meter_load:
                self.power_meter_load.auto_range_enable()
            if self.power_meter_source:
                self.power_meter_source.current_auto_range_enable()

            # Sleep for a short time to allow the power supply to stabilize 
            sleep(2)

            

            # Get initial output voltage while loaded
            self.test_data.get_eload_meas()
            iout_max = min(self.output_power/self.test_data.vout_V, self.allowable_iout)
            self.electronic_load.set_load(self.test_data.vout_V,iout_max,self.eload_type)
            self.electronic_load.turn_on()
            sleep(1)
            self.test_data.get_eload_meas()
            iout_max = min(self.output_power/self.test_data.vout_V, self.allowable_iout)
            self.seek_pout(self.test_data.vout_V, iout_max, 0.002)
            # Prepare iout list depending on output with boost follower
            self.iout_list_A = [load_pct * iout_max/100 \
                for load_pct in self.load_pct_list]

            # Correct the ac source output, limit to 1V
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
            
            # Loop through each load current level
            for iout_index, iout_level in enumerate(self.iout_list_A):
                # print("Entered inner loop")                 
                self.status_report(self.vin_index, iout_index, vin_delays=False)
                # print("Status report sent")
                # Trim the trailing zeros
                iout_A = float(f'{round(iout_level,6):g}')
                # print("Iout float")

                # print("Set eload")
                # Added due to eload inaccuracy
                self.seek_pout(self.test_data.vout_V, iout_level, 0.002)

                # Correct the ac source output, limit to 1V
                self.correct_source_output()
                    
                if iout_A == 0:
                    # print("Off load")
                    self.electronic_load.turn_off()
                
                # Sleep for the soak time before measuring
                soak.do_soak_per_load()
                # print("Load soak done")

                # Gather the data from the equipment
                self.test_data.gather_data(coupling=self.coupling)
                
                # If ripple is to be measured, run the scope
                # TODO: Verify if working
                if self.measure_ripple:
                    # print("Measure ripple started")
                    self.oscilloscope.stop()
                    self.oscilloscope.run_single()
                    sleep(0.5)
                    waveform_filename = f"{self.vin_freq[0]:g}V{self.coupling}_{self.vout_V:g}V_{iout_A:g}A.png"
                    self.oscilloscope.get_screenshot(waveform_filename, self.waveform_filepath) #capture waveform of output voltage with AC coupling
                    output_ripple_V = self.oscilloscope.get_measure(1)
                    self.test_data.output_ripple_mV = output_ripple_V * 1000
                    self.oscilloscope.run()
                    # sleep(1)
                
                # print("Gathered data")
                self.output_dataframe.loc[len(self.output_dataframe)]\
                    = self.process_data_row()
                # print("Dataframe")
                
                data_row = self.process_data_row()
                
                self.write_textfile_row(wr, txt_file, data_row)
                
                # Update the data for the results page
                self.update_output_data()
                # print("Output data for results page")

                if self.power_meter_load:
                    self.power_meter_load.auto_range_enable()
                if self.power_meter_source:
                    self.power_meter_source.current_auto_range_enable()
                
               
            
            # Add a blank row
            self.test_data_table.add_blank_row()
            
            self.output_dataframe=self.output_dataframe[0:0]
        
        self.export(temp_filepaths)
        
        self.plot_charts()
    
    def seek_pout(self, vout, iout, iout_res):

        td = self.test_data
        set_load = iout
        for i in range(0,20):
            td.get_eload_meas()
            # Above Pout but limit with resolution
            pout_eload = td.iout_A * td.vout_V
            if abs(td.iout_A - iout) < iout_res:
                # Prefer having slightly higher than slightly less load
                # But also ok with 0.5 W difference with target
                if (td.iout_A - iout) > 0 or abs(pout_eload-self.output_power)<0.5:
                    return
            elif td.iout_A < iout:
                set_load = set_load + iout_res
            elif td.iout_A > iout:
                set_load = set_load - iout_res
            self.electronic_load.set_load(vout, set_load, self.eload_type)
            sleep(1)

    def correct_source_output(self):

        offset = min(1,self.vin_freq[0] - self.power_meter_source.voltage)
        self.source_vout += offset

        self.input_supply.set_voltage_with_coupling(voltage=self.source_vout, coupling= self.coupling)
        self.input_supply.turn_on()

    def write_textfile_row(self, writer, file, row):
        writer.writerow(row)
        file.flush()

    def export(self, csv_filepaths):
        """Get the CSV files and place them in excel"""
        for i, filepath in enumerate(csv_filepaths):
            df = pd.read_csv(filepath)

            anchor = f"B{6+i*(len(self.iout_list_A)+4)}"
            export_to_excel(
                df, self.output_folder_path, 
                self.data_filename, self.sheet_name, anchor) 
                # Clear data list for next loop 
                
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
        text = f"{self.title}: {self.vout_V:g} V, {self.output_power:g} W\n" 
        text += f"CDC: {self.cdc_mV:g} mV, Operation: \n"
        
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
        self.test_conditions = test_item.test_conditions
        
        # General PSU Test Options
        self.general_options:GeneralOptions = self.test_conditions.general_options
        self.measure_ripple:bool = self.general_options.measure_ripple
        self.eload_type:str = self.general_options.eload_type
        self.use_eload_data:bool = self.general_options.use_eload_data
        self.load_direction:str = self.general_options.load_direction
        self.coupling:str = self.general_options.coupling
        
        self.i2c_test_conditions = self.test_conditions.i2c_test_parameters

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
        self.input_supply = self.equipment.ac_source
        self.power_meter_source = self.equipment.power_meter_source
        self.power_meter_load = self.equipment.power_meter_load_1
        self.electronic_load = self.equipment.electronic_load_1
        self.oscilloscope = self.equipment.oscilloscope
        if self.measure_ripple:
            # self.oscilloscope.setup_ripple()
            # self.initialize_scope_settings()
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
        
        if self.electronic_load is not None:
            self.electronic_load.turn_off()
            self.electronic_load.reset_values()
    
    def setup_data_file(self):
        """Set up the the data frame to be used for output 
        as well as the excel Workbook"""
        self.test_data = TestData()
        
        self.test_data.use_eload_data = self.use_eload_data
        self.test_data.vout_nom_V = self.vout_V
        self.test_data.use_eload_data = self.use_eload_data
        self.test_data.source_power_meter = self.power_meter_source
        self.test_data.load_power_meter = self.power_meter_load
        self.test_data.electronic_load = self.electronic_load

        # Prepare output dataframe
        self.header_list = self.define_data_header()
        # self.output_dataframe = dataframe_from_headers(self.header_list)
        
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
        self.sheet_name = f"{self.short_title}_{self.coupling}_{self.vout_V:g}V_{self.output_power:g}W_{self.cdc_mV:g}mV"
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
        
        # Create a temp folder in the test results folder to store 
        # txt files for dumping output data quickly
        # These files will then be converted later to excel
        self.temp_folder_path = f'{self.output_folder_path}/temp'

        if not os.path.exists(self.temp_folder_path):
            os.mkdir(self.temp_folder_path)
    
    def prepare_test_conditions(self):
        """Prepare the list of conditions to be used."""
        tc = self.test_conditions
        
        # Force eload to operate in CR
        self.eload_type = 'CR'

        # Generate a list of the input line voltage
        self.vin_list = tc.line_range.vin_freq
        
        # Nominal output settings
        self.nominal_output_voltage_V = self.i2c_test_conditions.param[0]
        self.nominal_load_current_A = round(self.i2c_test_conditions.param[1],6)
        
        # CDC setpoint
        self.cdc_mV = self.i2c_test_conditions.param[2]

        # PFC Settings
        self.vout_low_line = self.i2c_test_conditions.param[1-1]
        self.vout_high_line = self.i2c_test_conditions.param[2-1]
        self.bf_threshold = self.i2c_test_conditions.param[3-1]
        self.output_power = self.i2c_test_conditions.param[4-1]
        self.allowable_iout = self.output_power / self.vout_low_line*1.15
        
        self.is_boost_follower = self.i2c_test_conditions.cbx_param[1-1]
        
        self.i_max_A = self.output_power / self.vout_low_line
        self.vout_V = self.nominal_output_voltage_V
        

        self.test_conditions.nominal_output_voltage_V = self.vout_V
        self.test_conditions.nominal_load_current_A = self.i_max_A
        self.test_conditions.max_load_current_A = self.i_max_A
        
        #Generate a list of the load percent list
        self.load_pct_list = tc.load_range.check_load_direction(self.load_direction)
        
        # Generate a list of output current using the load percent list
        self.iout_list_A = [load_pct * self.nominal_load_current_A/100 \
             for load_pct in self.load_pct_list] 

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
        self.output_dataframe = dataframe_from_headers(self.header_list)
        anchor = "B5"
        export_to_excel(
                self.output_dataframe, self.output_folder_path, 
                self.data_filename, self.sheet_name, anchor) 
        
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
        td = self.test_data
        data_row = [
            td.vin_set_V, td.ac_freq_Hz, td.vin_V, 
            td.iin_mA,td.pin_W, td.PF, td.thd_pct, 
            td.vout_V, td.iout_A, td.pout_W, td.vreg_pct,
            td.eff_pct,td.vreg_passfail]
        
        if self.measure_ripple:
            data_row.append(self.test_data.output_ripple_mV)
            
        return data_row

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

                # Send necessary I2C commands
                add_time(2)
                # Do the initial soak if it is the first input voltage on the list
                if vin_index == 0:
                    add_time(soak.initial_soak)
                # Or the soak per line if it is not
                else:
                    add_time(soak.soak_per_line)
            
            # Loop through each load current level
            for iout_index, _ in enumerate(self.iout_list_A):                 
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
            usb_pd_flag = False)
        
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
        test_object_class = PFC_LoadRegTest
        new_test_conditions = TestConditions(
            nominal_output_voltage_V=test_object_class.tc_default.nominal_output_voltage_V,
            nominal_load_current_A=test_object_class.tc_default.nominal_load_current_A,
            max_load_current_A=test_object_class.tc_default.max_load_current_A,
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
            line_ramp_settings=test_object_class.tc_default.line_ramp_settings,
            i2c_test_parameters=I2CTestParameters(
                params = test_item_dict['I2C_PARAMS'],
                cbx_params = test_item_dict['I2C_CBX_PARAMS']),
            name=test_item_dict['NAME'])
        return new_test_conditions