# Standard Python Library Imports
from time import sleep
import datetime
import traceback
import os
import math
from copy import copy

# Third-Party Imports
from PySide2.QtCore import (QObject, Signal, Slot)
import pandas as pd
import openpyxl
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import PatternFill, Font as CellFont, Alignment, Border, Side
from openpyxl.utils import get_column_letter
try:
    from openpyxl.drawing.image import Image as OpenpyxlImage
except ImportError:
    OpenpyxlImage = None

# Local Imports
from psu_tests.test_object_imports import *
from equipment.handler import AC_SOURCE_COUPLING

# Re-alias Font after test_object_imports wildcard import (data_process shadows Font with openpyxl.drawing.text.Font)
Font = CellFont


class CapturePromptHelper(QObject):
    show_prompt_sig = Signal(str, str)
    def __init__(self):
        super().__init__()
        self.result = "CAPTURE"
        from PySide2.QtCore import Qt
        self.show_prompt_sig.connect(self.show_dialog, Qt.BlockingQueuedConnection)

    @Slot(str, str)
    def show_dialog(self, title, message):
        from PySide2.QtWidgets import QMessageBox
        from PySide2.QtCore import Qt
        msg_box = QMessageBox()
        msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowStaysOnTopHint)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Question)

        btn_capture = msg_box.addButton("Capture & Proceed", QMessageBox.AcceptRole)
        btn_recapture = msg_box.addButton("Recapture / Retrigger", QMessageBox.ActionRole)
        btn_skip = msg_box.addButton("Skip Point", QMessageBox.DestructiveRole)
        btn_stop = msg_box.addButton("Stop Test", QMessageBox.RejectRole)
        msg_box.setDefaultButton(btn_capture)

        msg_box.exec_()
        clicked = msg_box.clickedButton()
        if clicked == btn_capture:
            self.result = "CAPTURE"
        elif clicked == btn_recapture:
            self.result = "RECAPTURE"
        elif clicked == btn_skip:
            self.result = "SKIP"
        elif clicked == btn_stop:
            self.result = "STOP"
        else:
            self.result = "CAPTURE"

class VdsIdsSteadyStateTest(BaseTestObject):
    """
    Steady-State Waveform Capture Test.
    Sweeps AC Line Voltage and DC Load Current, automatically tunes the
    oscilloscope trigger to capture steady-state switching waveforms, saves
    screenshots, logs peak/max parameters, and embeds waveforms into the Excel report.
    """
    title = "Steady-State Waveform Capture"
    short_title = "SS_Waveform"
    i2c_test = False

    # General UI Definitions
    ui_definitions = General_UI_Definitions()
    ui_definitions.stack_page_1 = StackWidget1Pages.LineVoltageRange
    ui_definitions.stack_page_2 = StackWidget2Pages.LoadCurrentRange
    ui_definitions.stack_page_3 = StackWidget3Pages.I2C_Options

    ui_definitions.test_time_params_frame_visible = True
    ui_definitions.test_time_param1_label = 'Initial Soak (s)'
    ui_definitions.test_time_param2_label = 'Soak Per Line (s)'
    ui_definitions.test_time_param3_label = 'Soak Per Load (s)'

    ui_definitions.nominal_vout_visible = True
    ui_definitions.nominal_vout_enable = True
    ui_definitions.nominal_iout_visible = True
    ui_definitions.load_type_visible = True
    ui_definitions.coupling_visible = True
    ui_definitions.measure_ripple_visible = False
    ui_definitions.use_eload_data_toggle_visible = True
    ui_definitions.load_direction_visible = True

    # Scope & Trigger Parametric UI Definitions
    i2c_ui_definitions = I2C_UI_Definitions()

    # ComboBoxes:
    # 1. Trigger Channel
    i2c_ui_definitions.add_cbx(label="Trigger Channel", contents=['CH1', 'CH2', 'CH3', 'CH4'], param_index=1)
    # 2. Embed in Excel
    i2c_ui_definitions.add_cbx(label="Embed in Excel", contents=['Yes', 'No'], param_index=2)
    # 3. User Prompts
    i2c_ui_definitions.add_cbx(label="User Prompts", contents=[
        'Pre-Test Only',
        'Pre-Test & Per-Capture',
        'Per-Capture Only',
        'None (Fully Automated)'
    ], param_index=3)
    # 4. Auto Find Trigger
    i2c_ui_definitions.add_cbx(label="Auto Find Trigger", contents=['Yes', 'No'], param_index=4)

    # LineEdits:
    # 1. Trigger Delta
    i2c_ui_definitions.add_lineedit(label="Trigger Delta", param_index=1)
    # 2. Settle Time (s)
    i2c_ui_definitions.add_lineedit(label="Settle Time (s)", param_index=2)
    # 3. Discharge Pulses
    i2c_ui_definitions.add_lineedit(label="Discharge Pulses", param_index=3)
    # 4. Ambient Temp (°C)
    i2c_ui_definitions.add_lineedit(label="Ambient Temp (°C)", param_index=4)
    # 5. Post-Capture Delay (s)
    i2c_ui_definitions.add_lineedit(label="Post-Capture Delay (s)", param_index=5)

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
    ui_update.measure_ripple_update = False
    ui_update.load_direction_update = True
    ui_update.eload_type_update = True
    ui_update.use_eload_data_update = True
    ui_update.i2c_params_update = True
    ui_update.coupling_update = True

    @classmethod
    def get_ui_definitions(cls, flags: UIChangeFlags = UIChangeFlags()):
        return cls.ui_definitions

    @classmethod
    def get_ui_update_definitions(cls):
        return cls.ui_update

    # Default Test Conditions
    tc_default = TestConditions(
        name="Steady-State Waveform Capture",
        nominal_output_voltage_V=20.0,
        nominal_load_current_A=5.0,
        max_load_current_A=5.0,
        line_range=LineSettings.UNIVERSAL,
        load_range=LoadSettings.LOAD_25_PCT_STEP,
        soak_time=SoaktimeSettings.SOAK_TEST,
        general_options=GeneralOptions(eload_type='CC', coupling='AC'),
        i2c_test_parameters=I2CTestParameters(
            params=[3.0, 1.0, 2.0, 25.0, 1.0, 0, 0, 0, 0, 0],
            cbx_params=['CH1', 'Yes', 'Pre-Test & Per-Capture', 'No']
        ),
        unit_id="00",
        ambient_temp=25.0,
        scope_channels={
            1: {'enabled': True, 'name': 'Primary Vds'},
            2: {'enabled': True, 'name': 'Ids'},
            3: {'enabled': False, 'name': ''},
            4: {'enabled': False, 'name': ''}
        }
    )

    def __init__(self, test_item):
        super().__init__()
        self.test_item = test_item

        self.ac_source = None
        self.dc_source = None
        self.input_supply = None
        self.power_meter_source = None
        self.power_meter_load = None
        self.electronic_load = None
        self.oscilloscope = None

        self.unpack_test_item()

        self.output_folder_path = None
        self.data_file_path = None
        self.waveform_filepath = None

        self.status = TestStatus.IN_QUEUE
        self.progress_pct = 0
        self.prepare_test_conditions()
        self.total_time, self.total_steps = self.estimate_remaining(0, 0, vin_delays=True)
        self.estimated_time_s = self.total_time

        self.with_data = True
        self.message_closed = False
        self.captured_records = []
        self.update_test_list_text()

    def unpack_test_item(self):
        """Extract information from the TestItem object and scope parameters"""
        test_item = self.test_item
        self.parent = test_item.parent
        self.equipment = self.parent.equipment

        self.test_type_index = test_item.test_type_index
        self.test_conditions: TestConditions = test_item.test_conditions

        self.soak_time: SoakTime = self.test_conditions.soak_time
        self.general_options: GeneralOptions = self.test_conditions.general_options
        self.eload_type: str = self.general_options.eload_type
        self.use_eload_data: bool = self.general_options.use_eload_data
        self.load_direction: str = self.general_options.load_direction
        self.coupling: str = self.general_options.coupling

        self.nominal_output_voltage_V = self.test_conditions.nominal_output_voltage_V
        self.nominal_load_current_A = self.test_conditions.nominal_load_current_A
        self.max_load_current_A = getattr(self.test_conditions, 'max_load_current_A', self.nominal_load_current_A)
        self.unit_id = getattr(self.test_conditions, 'unit_id', 'RE_05')
        
        # Scope Channels (4-channel matrix)
        self.scope_channels = getattr(self.test_conditions, 'scope_channels', None)
        if not self.scope_channels:
            self.scope_channels = {
                1: {'enabled': True, 'name': 'Primary Vds'},
                2: {'enabled': True, 'name': 'Ids'},
                3: {'enabled': False, 'name': ''},
                4: {'enabled': False, 'name': ''}
            }

        # Build dynamic probe setup string from enabled channels
        active_ch_strs = []
        for ch_num, ch_data in sorted(self.scope_channels.items()):
            if ch_data.get('enabled', False):
                name = ch_data.get('name', '').strip()
                active_ch_strs.append(f"CH{ch_num}: {name}" if name else f"CH{ch_num}")
        self.probe_setup = ", ".join(active_ch_strs) if active_ch_strs else "None"

        # Parse Scope & Trigger Parameters from i2c_test_parameters
        i2c_params = getattr(self.test_conditions, 'i2c_test_parameters', None)

        # Trigger Channel (ComboBox 1)
        self.trigger_channel = 1
        if i2c_params and len(i2c_params.cbx_param) > 0 and i2c_params.cbx_param[0]:
            ch_str = str(i2c_params.cbx_param[0]).upper()
            for c in ['1', '2', '3', '4']:
                if c in ch_str:
                    self.trigger_channel = int(c)
                    break

        # Embed Images in Excel, User Prompts Mode, & Auto Find Trigger
        self.embed_images = True
        self.user_prompts = 'Pre-Test & Per-Capture'
        self.auto_find_trigger = False

        if i2c_params and len(i2c_params.cbx_param) >= 4 and i2c_params.cbx_param[1] not in ['Yes', 'No']:
            # Legacy 4-combobox layout: [Trigger, Probe, Embed, Prompts]
            if i2c_params.cbx_param[2]:
                self.embed_images = (str(i2c_params.cbx_param[2]).strip() == 'Yes')
            if i2c_params.cbx_param[3]:
                self.user_prompts = str(i2c_params.cbx_param[3]).strip()
        elif i2c_params and len(i2c_params.cbx_param) >= 2:
            # New layout: [Trigger, Embed, Prompts, Auto Find Trigger]
            if str(i2c_params.cbx_param[1]).strip() in ['Yes', 'No']:
                self.embed_images = (str(i2c_params.cbx_param[1]).strip() == 'Yes')
                if len(i2c_params.cbx_param) > 2 and i2c_params.cbx_param[2]:
                    self.user_prompts = str(i2c_params.cbx_param[2]).strip()
                if len(i2c_params.cbx_param) > 3 and i2c_params.cbx_param[3]:
                    self.auto_find_trigger = (str(i2c_params.cbx_param[3]).strip() == 'Yes')

        self.prompt_before_start = ('Pre-Test' in self.user_prompts)
        self.prompt_before_capture = ('Per-Capture' in self.user_prompts)

        # Trigger Delta (LineEdit 1)
        self.trigger_delta = 0.5
        try:
            if i2c_params and len(i2c_params.param) > 0 and str(i2c_params.param[0]).strip():
                val = float(i2c_params.param[0])
                if val > 0:
                    self.trigger_delta = val
        except (ValueError, TypeError):
            pass

        # Settle Time (LineEdit 2)
        self.settle_time = 1.0
        try:
            if i2c_params and len(i2c_params.param) > 1 and str(i2c_params.param[1]).strip():
                val = float(i2c_params.param[1])
                if val >= 0:
                    self.settle_time = val
        except (ValueError, TypeError):
            pass

        # Discharge Pulses (LineEdit 3)
        self.discharge_pulses = 0
        try:
            if i2c_params and len(i2c_params.param) > 2 and str(i2c_params.param[2]).strip():
                val = int(float(i2c_params.param[2]))
                if val >= 0:
                    self.discharge_pulses = val
        except (ValueError, TypeError):
            pass

        # Ambient Temp (°C) (LineEdit 4)
        self.ambient_temp = 25.0
        try:
            if i2c_params and len(i2c_params.param) > 3 and str(i2c_params.param[3]).strip():
                self.ambient_temp = float(i2c_params.param[3])
            elif hasattr(self.test_conditions, 'ambient_temp'):
                self.ambient_temp = float(self.test_conditions.ambient_temp)
        except (ValueError, TypeError):
            pass

        # Post-Capture Delay (s) (LineEdit 5)
        self.post_capture_delay = 1.0
        try:
            if i2c_params and len(i2c_params.param) > 4 and str(i2c_params.param[4]).strip():
                val = float(i2c_params.param[4])
                if val >= 0:
                    self.post_capture_delay = val
        except (ValueError, TypeError):
            pass

    def setup_equipment(self):
        """Assign equipment and check required instruments are online"""
        self.ac_source = self.equipment.ac_source
        self.dc_source = getattr(self.equipment, 'dc_source', None)

        if (self.dc_source is not None) and (self.coupling == AC_SOURCE_COUPLING.DC):
            self.input_supply = self.dc_source
        else:
            if self.ac_source is not None:
                self.input_supply = self.ac_source
            else:
                raise ConnectionError("No AC Source Connected or Assigned")

        self.power_meter_source = self.equipment.power_meter_source
        self.power_meter_load = self.equipment.power_meter_load_1
        self.electronic_load = self.equipment.electronic_load_1
        self.oscilloscope = self.equipment.oscilloscope

        if self.electronic_load is None:
            raise ConnectionError("No Electronic Load Connected or Assigned. Please check Equipment Setup.")
        if self.oscilloscope is None:
            try:
                if hasattr(self.equipment, 'check_scope_availability'):
                    self.equipment.check_scope_availability(get_default=True)
                    self.oscilloscope = self.equipment.oscilloscope
            except Exception:
                pass
            if self.oscilloscope is None:
                raise ConnectionError("No Oscilloscope Connected or Accessible. Please verify network connection and Oscilloscope IP address in Equipment Setup.")

        self.electronic_load.reset_values()

    def prepare_test_conditions(self):
        """Prepare line and load test lists"""
        test_conditions = self.test_conditions
        self.vin_list = test_conditions.line_range.vin_freq
        self.nominal_load_current_A = test_conditions.nominal_load_current_A
        self.i_max_A = getattr(test_conditions, 'max_load_current_A', self.nominal_load_current_A)
        self.vout_V = test_conditions.nominal_output_voltage_V

        self.load_pct_list = test_conditions.load_range.check_load_direction(self.general_options.load_direction)
        self.iout_list_A = [load_pct * self.nominal_load_current_A / 100 for load_pct in self.load_pct_list]

    def create_message_popup(self, title: str, message: str, message_type: MessageType):
        if getattr(self, '_auto_confirm_prompts', False):
            return
        self.message.emit(title, message, message_type)
        while not self.message_closed:
            sleep(0.5)
            if test_control_flags.get('StopTest', False):
                raise TestStopped
            if test_control_flags.get('SkipTest', False):
                raise TestSkipped
        self.message_closed = False

    def find_trigger(self, channel: int = 1, trigger_delta: float = 0.5) -> float:
        """
        Sweep trigger level to lock onto the highest steady-state peak waveform.
        Matches FIND_TRIGGER algorithm in equipment_settings.py.
        """
        sc = self.oscilloscope
        sc.run_single()
        if hasattr(sc, 'trigger_mode'):
            sc.trigger_mode('AUTO')
        elif hasattr(sc, 'set_trigger_mode'):
            sc.set_trigger_mode('AUTO')
        sleep(1)
        if hasattr(sc, 'trigger_mode'):
            sc.trigger_mode('NORM')
        elif hasattr(sc, 'set_trigger_mode'):
            sc.set_trigger_mode('NORM')

        try:
            # Get initial peak-to-peak measurement value
            labels, values = sc.get_measure(channel)
            if values and len(values) > 0 and values[0] is not None:
                try:
                    max_value = float(values[0])
                    if math.isnan(max_value):
                        max_value = 10.0
                except (ValueError, TypeError):
                    max_value = 10.0
            else:
                max_value = 10.0
            max_value = float(f"{max_value:.4f}")

            trigger_level = max_value
            sc.edge_trigger(channel, trigger_level, 'POS')

            # check if it triggered within 3 seconds
            sc.run_single()
            sleep(1)
            trigger_status = sc.trigger_status()

            # Step up trigger level until it stops triggering (guarded max 30 iterations)
            steps = 0
            max_steps = 30
            while trigger_status == 1 and steps < max_steps:
                steps += 1
                if test_control_flags.get('StopTest', False):
                    raise TestStopped
                if test_control_flags.get('SkipTest', False):
                    raise TestSkipped
                trigger_level += trigger_delta
                sc.edge_trigger(channel, trigger_level, 'POS')
                sc.run_single()
                sleep(0.5)
                trigger_status = sc.trigger_status()

            # Decrease trigger level below to get the maximum trigger possible
            trigger_level -= 1 * trigger_delta
            sc.edge_trigger(channel, trigger_level, 'POS')
            sleep(6)
            return trigger_level
        except (TestStopped, TestSkipped):
            raise
        except Exception as e:
            print(f"[Warning] find_trigger error on CH{channel}: {e}")
            return 10.0

    def discharge_output(self, times: int = 2):
        """Safely discharge converter output using electronic load"""
        if times <= 0:
            return
        if self.ac_source is not None:
            try:
                self.ac_source.turn_off()
            except Exception:
                pass
        if self.electronic_load is not None:
            for _ in range(times):
                if hasattr(self.electronic_load, 'channel') and isinstance(self.electronic_load.channel, (dict, list)):
                    for ch in range(1, len(self.electronic_load.channel) + 1):
                        try:
                            self.electronic_load.channel[ch].short_on()
                            self.electronic_load.channel[ch].turn_on()
                        except Exception:
                            pass
                    sleep(1)
                    for ch in range(1, len(self.electronic_load.channel) + 1):
                        try:
                            self.electronic_load.channel[ch].turn_off()
                            self.electronic_load.channel[ch].short_off()
                        except Exception:
                            pass
                    sleep(0.5)
                else:
                    try:
                        self.electronic_load.cc = self.i_max_A
                        self.electronic_load.turn_on()
                        sleep(1)
                        self.electronic_load.turn_off()
                        sleep(0.5)
                    except Exception:
                        pass
            try:
                self.electronic_load.reset_values()
            except Exception:
                pass

    def input_supply_eload_discharge_sequence(self):
        """ATE standard discharge sequence"""
        if self.equipment is not None:
            self.equipment.input_supply_eload_discharge_sequence(self.i_max_A / 3, coupling=self.coupling)

    def request_capture_action(self, title: str, message: str) -> str:
        """
        Displays confirmation prompt with [Capture & Proceed], [Recapture / Retrigger], [Skip Point], and [Stop Test].
        Returns: 'CAPTURE', 'RECAPTURE', 'SKIP', or 'STOP'.
        """
        if getattr(self, '_auto_confirm_prompts', False) or os.environ.get('PI_ATE_AUTO_CONFIRM') == '1':
            return "CAPTURE"

        try:
            from PySide2.QtWidgets import QApplication
            app = QApplication.instance()
            if app:
                helper = CapturePromptHelper()
                helper.moveToThread(app.thread())
                helper.show_prompt_sig.emit(title, message)
                return helper.result
            return "CAPTURE"
        except Exception as e:
            print(f"Error displaying capture prompt: {e}")
            return "CAPTURE"

    def query_active_scope_measurements(self) -> dict:
        """
        Queries active measurement slots from the oscilloscope.
        Falls back to per-channel peak measurements if active slots are not configured.
        Returns a dict of {measurement_label: value}.
        """
        meas_dict = {}
        try:
            all_meas = self.oscilloscope.get_measure_all()
            if all_meas:
                for item in all_meas:
                    labels = item.get('labels')
                    values = item.get('values')
                    ch_idx = item.get('channel', 1)
                    if labels and values and len(labels) > 0 and len(values) > 0:
                        for lbl, val in zip(labels, values):
                            if val is not None and not (isinstance(val, float) and math.isnan(val)):
                                ch_info = getattr(self, 'scope_channels', {}).get(ch_idx, {})
                                ch_name = ch_info.get('name', f"CH{ch_idx}")
                                col_label = f"{ch_name} {lbl}" if ch_name else f"CH{ch_idx} {lbl}"
                                meas_val = round(float(val), 3)
                                meas_dict[col_label] = meas_val
                                
                                # Derating Calculation
                                if "MAX" in lbl.upper() and ch_info.get('derating') is not None:
                                    derating_limit = ch_info.get('derating')
                                    derating_label = f"{ch_name} Derating (%)" if ch_name else f"CH{ch_idx} Derating (%)"
                                    if derating_limit > 0:
                                        derating_val = (meas_val / derating_limit) * 100
                                        meas_dict[derating_label] = round(derating_val, 2)
                                    else:
                                        meas_dict[derating_label] = 0.0
                                        
        except Exception as e:
            print(f"[Warning] Oscilloscope get_measure_all query: {e}")

        # If no active measurements returned, query each enabled channel for peak/max
        if not meas_dict and hasattr(self, 'scope_channels') and self.scope_channels:
            for ch_num, ch_data in sorted(self.scope_channels.items()):
                if ch_data.get('enabled', False):
                    ch_name = ch_data.get('name', f"CH{ch_num}")
                    try:
                        labels, values = self.oscilloscope.get_measure(ch_num)
                        if values and len(values) > 0 and values[0] is not None:
                            meas_val = round(float(values[0]), 3)
                            meas_dict[f"{ch_name} Max"] = meas_val
                        else:
                            meas_val = 0.0
                            meas_dict[f"{ch_name} Max"] = 0.0
                            
                        # Derating calculation for fallback
                        if ch_data.get('derating') is not None:
                            derating_limit = ch_data.get('derating')
                            derating_label = f"{ch_name} Derating (%)"
                            if derating_limit > 0:
                                meas_dict[derating_label] = round((meas_val / derating_limit) * 100, 2)
                            else:
                                meas_dict[derating_label] = 0.0
                                
                    except Exception:
                        meas_dict[f"{ch_name} Max"] = 0.0
                        if ch_data.get('derating') is not None:
                            meas_dict[f"{ch_name} Derating (%)"] = 0.0

        # Cursor Measurements
        if hasattr(self, 'scope_channels') and self.scope_channels:
            for ch_num, ch_data in sorted(self.scope_channels.items()):
                if ch_data.get('enabled', False) and ch_data.get('cursor', {}).get('enabled'):
                    ch_name = ch_data.get('name', f"CH{ch_num}")
                    try:
                        cursor_vals = self.oscilloscope.get_cursor(cursor=ch_num)
                        if cursor_vals:
                            dx = cursor_vals.get('delta x', 0.0)
                            dy = cursor_vals.get('delta y', 0.0)
                            try: dx = round(float(dx), 6)
                            except: dx = 0.0
                            try: dy = round(float(dy), 3)
                            except: dy = 0.0
                            meas_dict[f"{ch_name} dX"] = dx
                            
                            if dx != 0:
                                fsw_khz = round((1.0 / abs(dx)) / 1000.0, 2)
                                meas_dict[f"{ch_name} Fsw (kHz)"] = fsw_khz
                            else:
                                meas_dict[f"{ch_name} Fsw (kHz)"] = 0.0
                                
                            meas_dict[f"{ch_name} dY"] = dy
                        else:
                            meas_dict[f"{ch_name} dX"] = 0.0
                            meas_dict[f"{ch_name} Fsw (kHz)"] = 0.0
                            meas_dict[f"{ch_name} dY"] = 0.0
                    except Exception as e:
                        print(f"[Warning] Cursor query error on CH{ch_num}: {e}")

        return meas_dict

    def define_data_header(self):
        """Defines the data header for the Excel table and UI table"""
        header_list = [
            'Vin Set (V)', 'Freq (Hz)', 'Vin Meas (V)', 'Iin (mA)', 'Pin (W)', 'PF', '%THD',
            'Vo Set (V)', 'Vo Meas (V)', 'Io (A)', 'Po (W)', 'Efficiency',
            'Trig Ch', 'Trig Level (V)'
        ]
        added_meas = False
        if hasattr(self, 'scope_channels') and self.scope_channels:
            for ch_num, ch_data in sorted(self.scope_channels.items()):
                if ch_data.get('enabled', False):
                    ch_name = ch_data.get('name') or f"CH{ch_num}"
                    header_list.append(f"{ch_name} Max")
                    if ch_data.get('cursor', {}).get('enabled'):
                        header_list.append(f"{ch_name} dX")
                        header_list.append(f"{ch_name} Fsw (kHz)")
                        header_list.append(f"{ch_name} dY")
                    added_meas = True
        if not added_meas:
            header_list.extend(['Vds Max (V)', 'Ids Max (A)'])
        header_list.append('Waveform File')
        return header_list

    def setup_data_file(self):
        """Prepare output folder, Excel workbook, and table containers"""
        self.test_data = TestData()
        self.test_data.vout_nom_V = self.vout_V
        self.test_data.use_eload_data = self.use_eload_data
        self.test_data.source_power_meter = self.power_meter_source
        self.test_data.load_power_meter = self.power_meter_load
        self.test_data.electronic_load = self.electronic_load

        self.header_list = self.define_data_header()
        self.output_dataframe = dataframe_from_headers(self.header_list)

        if not self.output_folder_path:
            self.output_folder_path = getattr(self.test_item, 'output_folder_path', None)
        if not self.output_folder_path:
            self.output_folder_path = getattr(self.parent, 'output_folder_path', None) or os.getcwd()

        if not os.path.exists(self.output_folder_path):
            os.makedirs(self.output_folder_path, exist_ok=True)

        self.data_filename = f"{self.title} Test {self.vout_V:g}V"
        self.data_file_path = f"{self.output_folder_path}/{self.data_filename}.xlsx"

        self.waveform_filepath = f"{self.output_folder_path}/waveforms"
        if not os.path.exists(self.waveform_filepath):
            os.makedirs(self.waveform_filepath, exist_ok=True)

        if not os.path.exists(self.data_file_path):
            wb = openpyxl.Workbook()
            wb.save(self.data_file_path)
            wb.close()

        self.wb = openpyxl.load_workbook(self.data_file_path)
        self.sheet_name = f"{self.short_title}_{self.coupling}_{round(self.vout_V, 3):g}V_{round(self.i_max_A, 3):g}A"

        if self.sheet_name in self.wb.sheetnames:
            clear_sheet(self.output_folder_path, self.data_filename, self.sheet_name)
            self.wb = openpyxl.load_workbook(self.data_file_path)
            self.ws = self.wb[self.sheet_name]
        else:
            self.ws = self.wb.create_sheet(title=self.sheet_name)
            if 'Sheet' in self.wb.sheetnames and len(self.wb.sheetnames) > 1:
                del self.wb['Sheet']

        self.prepare_sheet_formatting()
        self.define_output_data_objects()

    def prepare_sheet_formatting(self):
        """Format the header section of the Excel worksheet"""
        self.ws['B2'] = f"{self.title} Test"
        self.ws['B2'].font = CellFont(size=14, bold=True, color="1F497D")

        info_text = (
            f"Unit ID: {self.unit_id} | Ambient Temp: {self.ambient_temp:g}\u00b0C | "
            f"Nominal Vout: {self.vout_V:g}V | Nominal Iout: {self.nominal_load_current_A:g}A | Max Iout: {self.i_max_A:g}A | Probe Config: {self.probe_setup}"
        )
        self.ws['B3'] = info_text
        self.ws['B3'].font = CellFont(size=10, italic=True)

        # Write Column Headers at Row 5
        for col_idx, header in enumerate(self.header_list, start=2):
            cell = self.ws.cell(row=5, column=col_idx, value=header)
            cell.font = CellFont(bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="2952A3", end_color="2952A3", fill_type="solid")
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        self.wb.save(self.data_file_path)
        self.wb.close()

    def define_output_data_objects(self):
        """Define results page table and plots for live UI monitoring"""
        # Determine maximum X range for the plot
        max_vin = max([v[0] for v in getattr(self, 'vin_list', [])]) if getattr(self, 'vin_list', []) else 265
        
        # Create Plot Object
        self.vds_vs_vin_plot = PlottableObject(
            title="Max Vds vs Input Voltage",
            type=PlotType.LINE,
            x_label="Input Voltage (VAC)",
            y_label="Maximum Vds (V)",
            x_range=(0, max_vin * 1.1),
            y_range=(0, 800), # will auto-scale, starting with a reasonable range
            plot_series_list=[]
        )
        
        # Add a series for each load
        for iout in getattr(self, 'iout_list_A', []):
            self.vds_vs_vin_plot.add_plot_series(
                name=f"Load {iout:g} A",
                x_values=[],
                y_values=[]
            )
            
        # Check if Derating Limit is specified for Primary Vds or CH1
        self.primary_vds_name = "Primary Vds"
        self.derating_limit_v = None
        if hasattr(self, 'scope_channels'):
            for ch, ch_data in self.scope_channels.items():
                if ch_data.get('name') == 'Primary Vds' or ch == 1:
                    self.primary_vds_name = ch_data.get('name', f"CH{ch}")
                    if ch_data.get('derating'):
                        self.derating_limit_v = ch_data.get('derating')
                        break
        
        # Add series for Derating Limit if exists
        if self.derating_limit_v:
            self.vds_vs_vin_plot.add_plot_series(
                name=f"Derating Limit ({self.derating_limit_v} V)",
                x_values=[],
                y_values=[]
            )

        self.test_data_table = DataTable(
            header=self.header_list, data=[]
        )
        self.with_data = True

    def estimate_remaining(self, vin_index_t, iout_index_t, vin_delays: bool = True):
        """Estimate the remaining test execution time in seconds"""
        soak = self.soak_time
        remaining_time_s = 0
        remaining_steps = 0
        vin_index = 0
        iout_index = 0
        start_adding_time = False

        def add_time(t, add_step: bool = False):
            nonlocal remaining_steps, remaining_time_s, start_adding_time
            if not start_adding_time:
                if vin_index == vin_index_t and iout_index == iout_index_t:
                    start_adding_time = True
            if start_adding_time:
                remaining_time_s += t
                if add_step:
                    remaining_steps += 1

        for vin_index, _ in enumerate(self.vin_list):
            if vin_delays:
                add_time(2)
                if vin_index == 0:
                    add_time(soak.initial_soak)
                else:
                    add_time(soak.soak_per_line)

            for iout_index, _ in enumerate(self.iout_list_A):
                add_time(self.settle_time, True)
                add_time(soak.soak_per_load)
                # Scope auto-trigger + capture time (~6s)
                add_time(6)
                # Discharge pulses
                add_time(self.discharge_pulses * 1.5)

        return remaining_time_s, remaining_steps

    def status_report(self, vin_index, load_index, vin_delays):
        """Report ETA and progress percentage to UI"""
        remaining_time_s, remaining_steps = self.estimate_remaining(vin_index, load_index, vin_delays)
        if self.total_steps > 0:
            percent_completion = round((1 - remaining_steps / self.total_steps) * 100, 0)
        else:
            percent_completion = 0
        self.estimated_time.emit(remaining_time_s)
        self.progress.emit(percent_completion)

    def run(self):
        """Run the test routines on a worker thread"""
        if self.parent.run_settings.get('debug', False):
            debugpy.debug_this_thread()

        try:
            self.status_update.emit(TestStatus.IN_PROGRESS)
            self.setup_equipment()
            self.prepare_test_conditions()
            self.setup_data_file()
            self.test_loop()
        except TestStopped:
            self.input_supply_eload_discharge_sequence()
            print("Test Stopped")
            self.status_update.emit(TestStatus.STOPPED)
        except TestSkipped:
            self.input_supply_eload_discharge_sequence()
            print("Test Skipped")
            self.status_update.emit(TestStatus.SKIPPED)
        except Exception as e:
            err_tb = traceback.format_exc()
            print(err_tb)
            self.input_supply_eload_discharge_sequence()
            print("Test Failed")
            err_msg = (
                f"Steady-State Waveform Capture encountered an error:\n\n"
                f"{type(e).__name__}: {str(e)}\n\n"
                "Please check instrument connections and app_log.txt for details."
            )
            try:
                self.create_message_popup("Test Failed", err_msg, MessageType.ABORT)
            except Exception:
                pass
            self.status_update.emit(TestStatus.FAILED)
        else:
            if getattr(self, 'discharge_pulses', 0) > 0:
                self.discharge_output(self.discharge_pulses)
            self.input_supply_eload_discharge_sequence()
            if self.embed_images:
                self.embed_waveforms_in_excel()
            self.estimated_time_s = 0
            self.status_update.emit(TestStatus.COMPLETE)

    def update_status_log(self, msg, upcoming=None):
        self.current_status_log = msg
        self.upcoming_event_log = upcoming
        self.update_test_list_text()
        self.progress.emit(self.progress_pct)

    def test_loop(self):
        """Execute the steady-state capture test"""
        soak = self.soak_time
        self.prepare_test_conditions()

        # Excel Row Counter
        current_excel_row = 6

        # Pre-test Oscilloscope setup prompt
        if self.prompt_before_start:
            prompt_msg = (
                "<b>================== OSCILLOSCOPE SETUP REMINDER ==================</b><br>"
                f"Unit ID: {self.unit_id} | Ambient Temp: {self.ambient_temp:g}\u00b0C<br>"
                f"Nominal Ratings: {self.vout_V:g} V / {self.nominal_load_current_A:g} A (Max: {self.i_max_A:g} A)<br><br>"
                "1. Load the correct .DFL file into the oscilloscope.<br>"
                f"2. Probe Configuration: {self.probe_setup}<br>"
                f"3. Trigger Channel: CH{self.trigger_channel} (Delta: {self.trigger_delta:g} V)<br>"
                "<b>=================================================================</b><br><br>"
                "Click OK once setup is complete to proceed."
            )
            self.create_message_popup("Oscilloscope Setup Verification", prompt_msg, MessageType.INFO)

        # Apply custom scope measurements if supported
        if hasattr(self.oscilloscope, 'set_channel_measurements') and hasattr(self, 'scope_channels') and self.scope_channels:
            custom_meas = {}
            for ch_num, ch_data in self.scope_channels.items():
                if ch_data.get('enabled'):
                    # Set custom channel labels on oscilloscope screen if supported
                    if hasattr(self.oscilloscope, 'channel_label'):
                        ch_name = ch_data.get('name', f"CH{ch_num}")
                        if ch_name:
                            try:
                                self.oscilloscope.channel_label(channel=ch_num, label=ch_name, rel_x_position=50, rel_y_position=50)
                            except Exception as e:
                                print(f"[Warning] Failed to set label '{ch_name}' for CH{ch_num}: {e}")
                                
                    if ch_data.get('measurements'):
                        custom_meas[ch_num] = ch_data.get('measurements')
                        
                    if ch_data.get('cursor', {}).get('enabled'):
                        try:
                            ctype = ch_data['cursor'].get('type', 'VERTical')
                            ctype_short = ctype[:4].upper() if len(ctype)>=4 else 'VERT'
                            if ctype_short == 'HORI': ctype_short = 'HOR'
                            self.oscilloscope.cursor(channel=ch_num, cursor_set=ch_num, type=ctype_short)
                        except Exception as e:
                            print(f"[Warning] Failed to set cursor on CH{ch_num}: {e}")
                        
            if custom_meas:
                try:
                    self.oscilloscope.set_channel_measurements(custom_meas)
                    import time
                    time.sleep(1)
                except Exception as e:
                    print(f"[Warning] Failed to set custom measurements on scope: {e}")

        # Update headers based on actual scope measurements now that setup is complete
        try:
            configured_labels = []
            all_meas = self.oscilloscope.get_measure_all()
            if all_meas:
                for item in all_meas:
                    labels = item.get('labels')
                    ch_idx = item.get('channel', 1)
                    if labels and len(labels) > 0:
                        for lbl in labels:
                            ch_info = getattr(self, 'scope_channels', {}).get(ch_idx, {})
                            ch_name = ch_info.get('name', f"CH{ch_idx}")
                            col_label = f"{ch_name} {lbl}" if ch_name else f"CH{ch_idx} {lbl}"
                            configured_labels.append(col_label)
                            
                            # Add derating column if MAXimum and derating is configured
                            if "MAX" in lbl.upper() and ch_info.get('derating') is not None:
                                derating_label = f"{ch_name} Derating (%)" if ch_name else f"CH{ch_idx} Derating (%)"
                                configured_labels.append(derating_label)
                                
            # Always add cursor labels if configured
            if hasattr(self, 'scope_channels') and self.scope_channels:
                for ch_num, ch_data in sorted(self.scope_channels.items()):
                    if ch_data.get('enabled', False) and ch_data.get('cursor', {}).get('enabled'):
                        ch_name = ch_data.get('name', f"CH{ch_num}")
                        dx_label = f"{ch_name} dX"
                        fsw_label = f"{ch_name} Fsw (kHz)"
                        dy_label = f"{ch_name} dY"
                        if dx_label not in configured_labels:
                            configured_labels.append(dx_label)
                        if fsw_label not in configured_labels:
                            configured_labels.append(fsw_label)
                        if dy_label not in configured_labels:
                            configured_labels.append(dy_label)
            
            if not configured_labels and hasattr(self, 'scope_channels') and self.scope_channels:
                for ch_num, ch_data in sorted(self.scope_channels.items()):
                    if ch_data.get('enabled', False):
                        ch_name = ch_data.get('name', f"CH{ch_num}")
                        configured_labels.append(f"{ch_name} Max")
                        
                        if ch_data.get('derating') is not None:
                            configured_labels.append(f"{ch_name} Derating (%)")
                            
                        if ch_data.get('cursor', {}).get('enabled'):
                            configured_labels.append(f"{ch_name} dX")
                            configured_labels.append(f"{ch_name} dY")
            
            if not configured_labels:
                configured_labels.extend(['Vds Max (V)', 'Ids Max (A)'])
            
            # Rebuild headers
            base_headers = [
                'Vin Set (V)', 'Freq (Hz)', 'Vin Meas (V)', 'Iin (mA)', 'Pin (W)', 'PF', '%THD',
                'Vo Set (V)', 'Vo Meas (V)', 'Io (A)', 'Po (W)', 'Efficiency',
                'Trig Ch', 'Trig Level (V)'
            ]
            self.header_list = base_headers + configured_labels + ['Waveform File']
            
            # Re-write the header row in Excel
            self.wb = openpyxl.load_workbook(self.data_file_path)
            self.ws = self.wb[self.sheet_name]
            for col_idx in range(2, 50): # Clear previous headers
                self.ws.cell(row=5, column=col_idx, value="")
            for col_idx, header in enumerate(self.header_list, start=2):
                cell = self.ws.cell(row=5, column=col_idx, value=header)
                cell.font = CellFont(bold=True, color="FFFFFF")
                cell.fill = PatternFill(start_color="2952A3", end_color="2952A3", fill_type="solid")
                cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            self.wb.save(self.data_file_path)
            self.wb.close()
            
            # Update UI table
            self.test_data_table.header = self.header_list
        except Exception as e:
            print(f"[Warning] Failed to update headers from scope: {e}")


        self.total_time, self.total_steps = self.estimate_remaining(0, 0, vin_delays=True)
        self.status_report(0, 0, vin_delays=True)

        for self.vin_index, self.vin_freq in enumerate(self.vin_list):
            vin_set = self.vin_freq[0]
            freq_set = self.vin_freq[1]

            self.update_status_log(f"Setting Input {vin_set} VAC", upcoming="Initial/Line Soak")

            # Set AC Source
            self.input_supply.set_voltage_with_coupling(voltage=vin_set, coupling=self.coupling)
            if self.coupling == AC_SOURCE_COUPLING.AC:
                self.input_supply.frequency = freq_set
            self.input_supply.turn_on()

            if self.power_meter_load:
                self.power_meter_load.auto_range_enable()
            if self.power_meter_source:
                self.power_meter_source.current_auto_range_enable()

            sleep(2)

            # Set first load current and turn ON load
            iout_first_A = self.iout_list_A[0]
            self.electronic_load.set_load(self.vout_V, iout_first_A, self.eload_type)
            self.electronic_load.turn_on()

            # Line Soak
            if self.vin_index == 0:
                self.update_status_log("Initial Soak...", upcoming=f"Setting Load {self.iout_list_A[0]} A")
                soak.do_initial_soak()
            else:
                self.update_status_log("Line Soak...", upcoming=f"Setting Load {self.iout_list_A[0]} A")
                soak.do_soak_per_line()

            for iout_index, iout_level in enumerate(self.iout_list_A):
                if test_control_flags.get('StopTest', False):
                    raise TestStopped
                if test_control_flags.get('SkipTest', False):
                    raise TestSkipped

                self.status_report(self.vin_index, iout_index, vin_delays=False)
                iout_A = float(f"{round(iout_level, 6):g}")

                self.update_status_log(f"Setting Load {iout_A} A", upcoming="Load Soak")

                # Set Electronic Load
                self.electronic_load.set_load(self.vout_V, iout_A, self.eload_type)
                self.electronic_load.turn_on()
                if iout_A == 0:
                    self.electronic_load.turn_off()

                self.update_status_log(f"Load Soak...", upcoming="Capture/Trigger Sweep")
                soak.do_soak_per_load()
                sleep(self.settle_time)

                # Loop for on-the-fly recapture at this operating point
                while True:
                    # Find optimal scope trigger level if enabled
                    if self.auto_find_trigger:
                        self.update_status_log("Sweeping Trigger Level...", upcoming="Capture Waveform")
                        actual_trig_level = self.find_trigger(channel=self.trigger_channel, trigger_delta=self.trigger_delta)
                    else:
                        if hasattr(self.oscilloscope, 'trigger_level') and callable(getattr(self.oscilloscope, 'trigger_level')):
                            try:
                                actual_trig_level = float(self.oscilloscope.device.query(f'TRIG1:LEV{self.trigger_channel}?'))
                            except Exception:
                                actual_trig_level = 0.0
                        else:
                            actual_trig_level = 0.0

                    self.update_status_log("Capturing waveform...", upcoming="Capture Waveform")
                    
                    # Capture waveform (RUN_SINGLE -> wait -> STOP)
                    self.oscilloscope.run_single()
                    sleep(1)
                    self.oscilloscope.stop()

                    # Query oscilloscope measurements to show in the prompt
                    scope_measurements = self.query_active_scope_measurements()

                    self.update_status_log("Waiting for user prompt...", upcoming="Capture Waveform")

                    if self.prompt_before_capture:
                        # Format scope measurements for the prompt
                        meas_str = ""
                        for label, value in scope_measurements.items():
                            meas_str += f"{label}: {value}<br>"
                        if not meas_str:
                            meas_str = "No active measurements found.<br>"

                        capture_prompt = (
                            f"<b>Oscilloscope Waveform Confirmation:</b><br><br>"
                            f"<b>Operating Point:</b> {vin_set:g} VAC, {iout_A:g} A<br>"
                            f"<b>Unit ID:</b> {self.unit_id}<br>"
                            f"<b>Trigger Level:</b> CH{self.trigger_channel} @ {actual_trig_level:.2f} V<br>"
                            f"<b>Active Channels:</b> {self.probe_setup}<br><br>"
                            f"<b>Live Measurements:</b><br>{meas_str}<br>"
                            "Review waveform on oscilloscope screen.<br>"
                            "Choose an action:"
                        )
                        action = self.request_capture_action(
                            f"Capture Waveform ({vin_set:g} VAC, {iout_A:g} A)",
                            capture_prompt
                        )
                        if action == "RECAPTURE":
                            print(f"[RECAPTURE] Operator requested re-trigger at {vin_set}VAC, {iout_A}A. Retrying...")
                            continue
                        elif action == "SKIP":
                            print(f"[SKIP] Operator skipped capture at {vin_set}VAC, {iout_A}A.")
                            break
                        elif action == "STOP":
                            raise TestStopped

                    # Read input & output power/voltage measurements
                    vin_meas = vin_set
                    iin_mA = 0.0
                    pin_W = 0.0
                    pf = 1.0
                    thd_pct = 0.0
                    if self.power_meter_source is not None:
                        try:
                            vin_meas = self.power_meter_source.voltage or vin_set
                            iin_mA = (self.power_meter_source.current or 0.0) * 1000
                            pin_W = self.power_meter_source.power or 0.0
                            pf = getattr(self.power_meter_source, 'pf', getattr(self.power_meter_source, 'power_factor', 1.0))
                            thd_pct = getattr(self.power_meter_source, 'thd', getattr(self.power_meter_source, 'thd_pct', 0.0))
                        except Exception:
                            pass

                    vo_meas = self.vout_V
                    po_W = self.vout_V * iout_A
                    if self.power_meter_load is not None:
                        try:
                            vo_meas = self.power_meter_load.voltage or self.vout_V
                            po_W = self.power_meter_load.power or (vo_meas * iout_A)
                        except Exception:
                            pass
                            
                    efficiency = (po_W / pin_W * 100.0) if pin_W > 0 else 0.0

                    # Save Screenshot: {unit_id}_{vin}VAC_Io_{iout}A.png
                    prefix = f"{self.unit_id}_" if self.unit_id else ""
                    mode_str = ""
                    img_filename = f"{prefix}{vin_set:g}VAC{mode_str}_Io_{iout_A:g}A.png"
                    img_path = os.path.join(self.waveform_filepath, img_filename)
                    try:
                        self.oscilloscope.get_screenshot(img_filename, self.waveform_filepath)
                    except Exception as e:
                        print(f"[Warning] Failed to capture oscilloscope screenshot {img_filename}: {e}")

                    # Prepare row data
                    row_data = [
                        vin_set, freq_set, round(vin_meas, 2), round(iin_mA, 2),
                        round(pin_W, 3), round(pf, 3), round(thd_pct, 2),
                        self.vout_V, round(vo_meas, 3), iout_A, round(po_W, 3), round(efficiency, 2),
                        f"CH{self.trigger_channel}", round(actual_trig_level, 2)
                    ]

                    # Append measurement values matching headers
                    for h in self.header_list[14:-1]:
                        val = scope_measurements.get(h)
                        if val is None:
                            # Try prefix or channel match
                            for mk, mv in scope_measurements.items():
                                if h.startswith(mk) or mk.startswith(h.split()[0]):
                                    val = mv
                                    break
                        row_data.append(val if val is not None else "N/A")

                    row_data.append(img_filename)

                    # Write row into Excel worksheet
                    self.wb = openpyxl.load_workbook(self.data_file_path)
                    self.ws = self.wb[self.sheet_name]
                    for c_idx, val in enumerate(row_data, start=2):
                        c = self.ws.cell(row=current_excel_row, column=c_idx, value=val)
                        c.alignment = Alignment(horizontal="center")
                    self.wb.save(self.data_file_path)
                    self.wb.close()
                    current_excel_row += 1

                    # Update UI Results Table
                    self.test_data_table.add_data_row(row_data)
                    
                    # Update Plot Data
                    max_vds_col = f"{getattr(self, 'primary_vds_name', 'Primary Vds')} Max"
                    if hasattr(self, 'vds_vs_vin_plot') and max_vds_col in row_data:
                        try:
                            vds_val = float(row_data[max_vds_col])
                            self.vds_vs_vin_plot.append_plot_data(
                                plot_index=iout_index,
                                x=vin_set,
                                y=vds_val
                            )
                            # Append derating limit for this Vin point (only once per Vin)
                            if getattr(self, 'derating_limit_v', None) and iout_index == 0:
                                self.vds_vs_vin_plot.append_plot_data(
                                    plot_index=len(self.iout_list_A),
                                    x=vin_set,
                                    y=self.derating_limit_v
                                )
                        except Exception as e:
                            print(f"[Warning] Failed to append plot data: {e}")

                    self.test_data_update.emit([[self.vds_vs_vin_plot] if hasattr(self, 'vds_vs_vin_plot') else [], self.test_data_table])

                    # Record captured screenshot for embedding
                    self.captured_records.append({
                        'vin': vin_set,
                        'iout': iout_A,
                        'path': img_path,
                        'filename': img_filename,
                        'measurements': scope_measurements
                    })

                    sleep(self.post_capture_delay)
                    break

    def embed_waveforms_in_excel(self):
        """Embed captured waveform images into a dedicated 'Waveforms' worksheet"""
        if OpenpyxlImage is None or not self.captured_records:
            return

        try:
            self.wb = openpyxl.load_workbook(self.data_file_path)
            wf_sheet_name = f"{self.short_title}_Waveforms"

            if wf_sheet_name in self.wb.sheetnames:
                del self.wb[wf_sheet_name]

            ws_wf = self.wb.create_sheet(title=wf_sheet_name)
            ws_wf['B2'] = f"{self.title} - Captured Waveforms"
            ws_wf['B2'].font = CellFont(size=14, bold=True, color="1F497D")

            ws_wf.column_dimensions['B'].width = 45
            ws_wf.column_dimensions['G'].width = 45

            current_row = 4
            for idx, rec in enumerate(self.captured_records):
                img_path = rec['path']
                if not os.path.exists(img_path):
                    continue

                col_letter = 'B' if (idx % 2 == 0) else 'G'
                img_cell = f"{col_letter}{current_row + 1}"
                title_cell = f"{col_letter}{current_row}"

                meas_items = []
                for k, v in rec.get('measurements', {}).items():
                    if v is not None and v != "N/A":
                        meas_items.append(f"{k}: {v}")
                meas_str = (" | " + " | ".join(meas_items)) if meas_items else ""

                ws_wf[title_cell] = f"{rec['vin']:g} VAC, {rec['iout']:g} A{meas_str}"
                ws_wf[title_cell].font = CellFont(bold=True, size=11, color="2952A3")

                img = OpenpyxlImage(img_path)
                img.width = 420
                img.height = 315
                ws_wf.add_image(img, img_cell)

                if idx % 2 == 1 or idx == len(self.captured_records) - 1:
                    current_row += 18

            self.wb.save(self.data_file_path)
            self.wb.close()
        except Exception as e:
            print(f"Error embedding waveforms into Excel: {e}")
            print(traceback.format_exc())

    def with_waveform_capture(self):
        return True

    def update_test_list_text(self):
        """Update the text for the test list UI"""
        if self.status == TestStatus.COMPLETE:
            self.estimated_time_txt = ''
            self.progress_txt = '100%'
        elif self.status in [TestStatus.STOPPED, TestStatus.SKIPPED]:
            self.estimated_time_txt = ''
            self.progress_txt = ''
        else:
            self.estimated_time_txt = f"{datetime.timedelta(seconds=round(self.estimated_time_s, 0))}"
            self.progress_txt = f"{self.progress_pct}%"

        text = f"{self.title}: {round(self.vout_V, 3):g}V, {round(self.i_max_A, 3):g}A\n"
        text += f"Trigger: CH{self.trigger_channel} (Delta: {self.trigger_delta:g}V)\n"
        if getattr(self, 'current_status_log', None):
            text += f"Status: {self.current_status_log}\n"
        if getattr(self, 'upcoming_event_log', None):
            text += f"Upcoming: {self.upcoming_event_log}\n"
            
        if self.status in [TestStatus.COMPLETE, TestStatus.FAILED] and getattr(self, 'output_folder_path', None):
            import os
            output_link = f"<a href='file:///{os.path.abspath(self.output_folder_path).replace(chr(92), '/')}'>Click here to view results folder</a>"
            text += f"{output_link}\n"
        text += f"Estimated Time: {self.estimated_time_txt}  {self.progress_txt}"
        self.test_list_text = text
        return text

    def get_dict(self) -> dict:
        """Create dictionary representation for test serialization"""
        d = {
            'TEST_TYPE_INDEX': self.test_type_index,
            'NOMINAL_OUTPUT_VOLTAGE_V': self.test_conditions.nominal_output_voltage_V,
            'NOMINAL_LOAD_CURRENT_A': self.test_conditions.nominal_load_current_A,
            'MAX_LOAD_CURRENT_A': self.test_conditions.max_load_current_A,
            'UNIT_ID': getattr(self, 'unit_id', getattr(self.test_conditions, 'unit_id', 'RE_05')),
                        'AMBIENT_TEMP': getattr(self, 'ambient_temp', getattr(self.test_conditions, 'ambient_temp', 25.0)),
            'LINE_RANGE_name': self.test_conditions.line_range.name,
            'LINE_RANGE_vin_freq': self.test_conditions.line_range.vin_freq,
            'LINE_RANGE_custom': self.test_conditions.line_range.custom,
            'LOAD_RANGE_name': self.test_conditions.load_range.name,
            'LOAD_RANGE_load_range_pct': self.test_conditions.load_range.load_range_pct,
            'LOAD_RANGE_custom': self.test_conditions.load_range.custom,
            'SOAK_TIME_name': self.test_conditions.soak_time.name,
            'SOAK_TIME_initial_soak': self.test_conditions.soak_time.initial_soak,
            'SOAK_TIME_soak_per_line': self.test_conditions.soak_time.soak_per_line,
            'SOAK_TIME_soak_per_load': self.test_conditions.soak_time.soak_per_load,
            'SOAK_TIME_integration_time': self.test_conditions.soak_time.integration_time,
            'SOAK_TIME_custom': self.test_conditions.soak_time.custom,
            'GENERAL_OPTIONS_measure_ripple': self.general_options.measure_ripple,
            'GENERAL_OPTIONS_eload_type': self.general_options.eload_type,
            'GENERAL_OPTIONS_use_eload_data': self.general_options.use_eload_data,
            'GENERAL_OPTIONS_load_direction': self.general_options.load_direction,
            'GENERAL_OPTIONS_coupling': self.general_options.coupling,
            'I2C_TEST_PARAMETERS_param': self.test_conditions.i2c_test_parameters.param,
            'I2C_TEST_PARAMETERS_cbx_param': self.test_conditions.i2c_test_parameters.cbx_param,
            'I2C_PARAMS': self.test_conditions.i2c_test_parameters.param,
            'I2C_CBX_PARAMS': self.test_conditions.i2c_test_parameters.cbx_param,
            'SCOPE_CHANNELS': getattr(self, 'scope_channels', getattr(self.test_conditions, 'scope_channels', {})),
            'NAME': self.test_conditions.name
        }
        return d

    @staticmethod
    def extract_test_condition(test_item_dict: dict) -> TestConditions:
        test_object_class = VdsIdsSteadyStateTest
        i2c_params = test_item_dict.get('I2C_PARAMS', test_item_dict.get('I2C_TEST_PARAMETERS_param', test_object_class.tc_default.i2c_test_parameters.param))
        i2c_cbx_params = test_item_dict.get('I2C_CBX_PARAMS', test_item_dict.get('I2C_TEST_PARAMETERS_cbx_param', test_object_class.tc_default.i2c_test_parameters.cbx_param))

        new_test_conditions = TestConditions(
            nominal_output_voltage_V=test_item_dict['NOMINAL_OUTPUT_VOLTAGE_V'],
            nominal_load_current_A=test_item_dict['NOMINAL_LOAD_CURRENT_A'],
            max_load_current_A=test_item_dict.get('MAX_LOAD_CURRENT_A', test_item_dict['NOMINAL_LOAD_CURRENT_A']),
            line_range=LineRange(
                name=test_item_dict['LINE_RANGE_name'],
                vin_freq=test_item_dict['LINE_RANGE_vin_freq'],
                custom=test_item_dict['LINE_RANGE_custom']),
            load_range=LoadRange(
                name=test_item_dict['LOAD_RANGE_name'],
                load_range_pct=test_item_dict['LOAD_RANGE_load_range_pct'],
                custom=test_item_dict['LOAD_RANGE_custom']),
            soak_time=SoakTime(
                name=test_item_dict['SOAK_TIME_name'],
                initial=test_item_dict['SOAK_TIME_initial_soak'],
                line=test_item_dict['SOAK_TIME_soak_per_line'],
                load=test_item_dict['SOAK_TIME_soak_per_load'],
                integration=test_item_dict.get('SOAK_TIME_integration_time', 0)),
            general_options=GeneralOptions(
                measure_ripple=test_item_dict.get('GENERAL_OPTIONS_measure_ripple', False),
                use_eload_data=test_item_dict.get('GENERAL_OPTIONS_use_eload_data', True),
                eload_type=test_item_dict.get('GENERAL_OPTIONS_eload_type', 'CC'),
                load_direction=test_item_dict.get('GENERAL_OPTIONS_load_direction', 'Low to High'),
                coupling=test_item_dict.get('GENERAL_OPTIONS_coupling', 'AC')),
            i2c_test_parameters=I2CTestParameters(
                params=i2c_params,
                cbx_params=i2c_cbx_params),
            name=test_item_dict['NAME'],
            unit_id=test_item_dict.get('UNIT_ID', 'RE_05'),
                        ambient_temp=test_item_dict.get('AMBIENT_TEMP', 25.0),
            scope_channels={
                ch: test_item_dict.get('SCOPE_CHANNELS', {}).get(ch, test_item_dict.get('SCOPE_CHANNELS', {}).get(str(ch), {
                    'enabled': (ch in [1, 2]),
                    'name': 'Primary Vds' if ch == 1 else ('Ids' if ch == 2 else '')
                }))
                for ch in [1, 2, 3, 4]
            }
        )
        return new_test_conditions


# Alias for generic waveform capture naming
SteadyStateWaveformCaptureTest = VdsIdsSteadyStateTest

