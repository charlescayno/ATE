import os
import time

from psu_tests.test_object_imports import *
from psu_tests.test_efficiency_2port_waveform import EfficiencyWaveformTest_2Port


class StartupWaveformTest_2Port(EfficiencyWaveformTest_2Port):
    """
    Startup Waveform 2 Port: scope capture on input switch / startup event at each (Vin, load) point.
    """

    title = "Startup Waveform 2 Port"
    short_title = "SU_WF_2P"
    STARTUP_CAPTURE_TIMEOUT_S = 7.0
    PNG_SUFFIX = "_SUW"

    tc_default = None  # set after class body

    i2c_ui_definitions = EfficiencyWaveformTest_2Port.i2c_ui_definitions

    @classmethod
    def _build_tc_default(cls):
        tc = EfficiencyWaveformTest_2Port.tc_default
        i2c = tc.i2c_test_parameters
        cbx = list(getattr(i2c, 'cbx_param', []) or [])
        if len(cbx) > 3:
            cbx[3] = "No"
        if len(cbx) > 2:
            cbx[2] = "Per-Capture Only"
        params = list(getattr(i2c, 'param', []) or [])
        if len(params) > 4:
            params[4] = 1.0
        return TestConditions(
            name=cls.title,
            nominal_output_voltage_V=tc.nominal_output_voltage_V,
            nominal_load_current_A=tc.nominal_load_current_A,
            max_load_current_A=tc.max_load_current_A,
            line_range=tc.line_range,
            load_range=tc.load_range,
            soak_time=tc.soak_time,
            general_options=tc.general_options,
            usbpd_options=tc.usbpd_options,
            line_ramp_settings=tc.line_ramp_settings,
            i2c_test_parameters=I2CTestParameters(
                params=params,
                cbx_params=cbx,
            ),
            unit_id=tc.unit_id,
            ambient_temp=tc.ambient_temp,
            scope_channels=dict(tc.scope_channels),
        )

    def unpack_test_item(self):
        super().unpack_test_item()
        self.auto_find_trigger = False

    def build_detailed_output_basename(self) -> str:
        return (
            f"SUW {self._line_vin_filename_part()} {self.vout_V:g}V "
            f"{self._dual_port_power_filename_part()} {self._scope_names_filename_part()}"
        )

    def setup_data_file(self):
        super().setup_data_file()
        desired = (
            f"{self.short_title}_{self.coupling}_{round(self.vout_V, 3):g}V_"
            f"{round(self.i_max_A, 3):g}A")
        if self.sheet_name == desired:
            return
        ws = self.wb[self.sheet_name]
        ws.title = desired
        self.sheet_name = desired
        self.wb.save(self.data_file_path)
        self.wb.close()
        self.wb = openpyxl.load_workbook(self.data_file_path)
        self.ws = self.wb[self.sheet_name]

    def _prompt_bulk_cap_discharge_to_input(self):
        msg = (
            "<b>Discharge outputs to input bulk capacitor</b><br><br>"
            "Follow bench procedure to discharge the DUT outputs into the "
            "<b>input bulk capacitor</b> as required for startup testing.<br><br>"
            "Click OK when complete."
        )
        self.create_message_popup("Bulk Capacitor — Output Discharge", msg, MessageType.WARNING)

    def _prompt_bulk_cap_disconnect(self):
        msg = (
            "<b>Disconnect input bulk capacitor</b><br><br>"
            "Disengage the bulk capacitor from the DUT input path before the first startup capture.<br><br>"
            "Click OK when the bulk cap is disconnected."
        )
        self.create_message_popup("Bulk Capacitor — Disconnect", msg, MessageType.WARNING)

    def _prompt_input_switch(self, vin_set: float):
        coupling_label = "DC" if str(self.coupling).upper() == "DC" else "AC"
        msg = (
            "<b>WARNING — HIGH VOLTAGE</b><br><br>"
            f"Input supply is at <b>{vin_set:g} V {coupling_label}</b>. "
            "The DUT input must stay isolated until you intentionally close the input switch.<br><br>"
            "Use proper PPE and bench safety practice. Confirm the setup matches the test plan, "
            "then close the input switch to capture startup.<br><br>"
            "Click OK after the switch is closed."
        )
        self.create_message_popup("Close Input Switch (HV)", msg, MessageType.WARNING)

    def _wait_for_scope_capture(self, vin_set: float, i1_A: float, i2_A: float) -> bool:
        if os.environ.get('PI_ATE_AUTO_CONFIRM') == '1':
            sleep(0.05)
            try:
                self.oscilloscope.stop()
            except Exception:
                pass
            return True

        deadline = time.monotonic() + self.STARTUP_CAPTURE_TIMEOUT_S
        while time.monotonic() < deadline:
            if test_control_flags.get('StopTest', False):
                raise TestStopped
            if test_control_flags.get('SkipTest', False):
                raise TestSkipped
            try:
                status = int(self.oscilloscope.trigger_status())
                if status >= 1:
                    try:
                        self.oscilloscope.stop()
                    except Exception:
                        pass
                    return True
            except (TypeError, ValueError):
                try:
                    self.oscilloscope.stop()
                except Exception:
                    pass
                return True
            except Exception as exc:
                print(f"[Warning] trigger_status poll: {exc}")
            sleep(0.1)

        try:
            self.oscilloscope.stop()
        except Exception:
            pass
        print(
            f"[TIMEOUT] No scope capture within {self.STARTUP_CAPTURE_TIMEOUT_S:g} s at "
            f"{vin_set:g} V, Ch1 {i1_A:g} A, Ch2 {i2_A:g} A")
        return False

    def _apply_vin_setpoint(self, vin_set: float, vin_freq_row):
        self.update_status_log(f"Setting Input {vin_set:g} V{self.coupling}", upcoming="Arm scope")
        if self._bulk_cap_ramp_applies():
            self._bulk_cap_ramp_to_voltage(vin_set)
        else:
            self.input_supply.set_voltage_with_coupling(voltage=vin_set, coupling=self.coupling)
            self.input_supply.turn_on()
        if self.coupling == AC_SOURCE_COUPLING.AC:
            self.input_supply.frequency = vin_freq_row[1]
        self.source_vout = vin_set
        self.test_data.vin_set_V = vin_set
        self.test_data.ac_freq_Hz = vin_freq_row[1]

    def _startup_png_filename(self, vin_set, i1_A, i2_A) -> str:
        prefix = f"{self.unit_id}_" if self.unit_id else ""
        pwr = self._dual_port_power_filename_part(i1_A=i1_A, i2_A=i2_A, png_suffix=True)
        return (
            f"{prefix}{vin_set:g}V{self.coupling}_Ch1_{i1_A:g}A_Ch2_{i2_A:g}A"
            f"{pwr}{self.PNG_SUFFIX}.png")

    def capture_startup_at_point(self, vin_set, i1_A, i2_A) -> list:
        """Arm, switch prompt, acquisition wait, review prompt, screenshot."""
        n_meas = len(self.scope_measurement_labels)
        trig_level = self._read_trigger_level()

        while True:
            if self.reapply_scope_before_capture:
                self.apply_scope_setup()
            self.update_status_log("Arming oscilloscope (single)...", upcoming="Set loads")
            self.oscilloscope.run_single()

            self._set_loads(i1_A, i2_A)
            self.update_status_log("Waiting for input switch...", upcoming="Acquisition")
            self._prompt_input_switch(vin_set)

            self.update_status_log("Waiting for scope acquisition...", upcoming="Review capture")
            self._wait_for_scope_capture(vin_set, i1_A, i2_A)
            meas = self.query_active_scope_measurements()

            if self.prompt_before_capture:
                timeout_note = ""
                meas_str = "".join(f"{k}: {v}<br>" for k, v in meas.items()) or "No active measurements found.<br>"
                message = (
                    f"<b>Operating Point:</b> {vin_set:g} V{self.coupling} | "
                    f"Ch1 {i1_A:g} A ({self.current_ch1_lbl}) | Ch2 {i2_A:g} A ({self.current_ch2_lbl})<br>"
                    f"<b>Unit ID:</b> {self.unit_id}<br>"
                    f"<b>Trigger Level:</b> CH{self.trigger_channel} @ {trig_level:.2f} V<br>"
                    f"{timeout_note}<br>"
                    f"<b>Live Measurements:</b><br>{meas_str}<br>"
                    "Review the startup waveform on the oscilloscope, then choose an action:"
                )
                action = self.request_capture_action(
                    f"Startup Capture ({vin_set:g} V, Ch1 {self.current_ch1_lbl} / Ch2 {self.current_ch2_lbl})",
                    message)
                if action == "RECAPTURE":
                    print(f"[RECAPTURE] Re-arm at {vin_set} V, Ch1 {i1_A} A, Ch2 {i2_A} A")
                    continue
                if action == "STOP":
                    raise TestStopped
                if action == "SKIP":
                    print(f"[SKIP] Capture skipped at {vin_set} V, Ch1 {i1_A} A, Ch2 {i2_A} A")
                    self.oscilloscope.run()
                    row = [f"CH{self.trigger_channel}", "N/A"] + ["N/A"] * n_meas
                    if not self.embed_images:
                        row.append("")
                    return row

            img_filename = self._startup_png_filename(vin_set, i1_A, i2_A)
            img_path = os.path.join(self.waveform_filepath, img_filename)
            try:
                self.oscilloscope.get_screenshot(img_filename, self.waveform_filepath)
            except Exception as e:
                print(f"[Warning] Failed to capture oscilloscope screenshot {img_filename}: {e}")
            self.oscilloscope.run()

            self.captured_records.append({
                'vin': vin_set, 'i1': i1_A, 'i2': i2_A,
                'ch1_lbl': self.current_ch1_lbl, 'ch2_lbl': self.current_ch2_lbl,
                'eff': getattr(self, 'eff_total_pct', 0.0), 'path': img_path, 'measurements': meas,
            })

            row = [f"CH{self.trigger_channel}", round(trig_level, 2)]
            for label in self.scope_measurement_labels:
                val = meas.get(label)
                row.append(val if val is not None else "N/A")
            if not self.embed_images:
                row.append(img_path)
            return row

    def test_loop(self):
        if self.discharge_pulses > 0:
            self.discharge_output(self.discharge_pulses)

        self._prompt_bulk_cap_discharge_to_input()

        if self.prompt_before_start:
            prompt_msg = (
                "<b>================== OSCILLOSCOPE SETUP REMINDER ==================</b><br>"
                f"Unit ID: {self.unit_id} | Ambient Temp: {self.ambient_temp:g}\u00b0C<br>"
                f"Ch1: {self.vout_V:g} V / {self.i_max_A:g} A &nbsp; "
                f"Ch2: {self.vout_2_V:g} V / {self.i_max_2_A:g} A &nbsp; Mode: {self.dual_load_mode}<br><br>"
                "1. Load the correct startup .DFL file into the oscilloscope.<br>"
                f"2. Probe Configuration: {self.probe_setup}<br>"
                f"3. Trigger Channel: CH{self.trigger_channel} (fixed — Auto Find Trigger off)<br>"
                "<b>=================================================================</b><br><br>"
                "Click OK once setup is complete to proceed."
            )
            self.create_message_popup("Oscilloscope Setup Verification", prompt_msg, MessageType.INFO)

        self.apply_scope_setup()

        self.total_time, self.total_steps = self.estimate_remaining(0, 0, vin_delays=True)
        self.status_report(0, 0, vin_delays=True)

        first_point = True

        for self.vin_index, self.vin_freq in enumerate(self.vin_list):
            vin_set = self.vin_freq[0]
            self.create_new_plot_series()

            if self.power_meter_load:
                self.power_meter_load.auto_range_enable()
            if self.power_meter_load_2:
                self.power_meter_load_2.auto_range_enable()
            if self.power_meter_source:
                self.power_meter_source.current_auto_range_enable()

            for load_index, (i1_A, i2_A, ch1_lbl, ch2_lbl) in enumerate(self.load_pairs):
                if test_control_flags.get('StopTest', False):
                    raise TestStopped
                if test_control_flags.get('SkipTest', False):
                    raise TestSkipped

                self.status_report(self.vin_index, load_index, vin_delays=False)
                self.current_ch1_lbl = ch1_lbl
                self.current_ch2_lbl = ch2_lbl
                self.current_load_index = load_index

                if first_point:
                    self._prompt_bulk_cap_disconnect()
                    first_point = False

                self.update_status_log("Discharging unit...", upcoming="Input ramp")
                if self.usbpd_test:
                    self.input_supply_eload_discharge_sequence()
                else:
                    self.input_supply_eload_discharge_sequence()

                self._apply_vin_setpoint(vin_set, self.vin_freq)

                self.update_status_log(
                    f"Setting Loads Ch1 {i1_A:g} A / Ch2 {i2_A:g} A", upcoming="Startup capture")
                scope_row = self.capture_startup_at_point(vin_set, i1_A, i2_A)

                sleep(self.settle_time)
                self.update_status_log("Measuring efficiency...", upcoming="Save row")
                self._measure_efficiency(i2_A)

                self.output_dataframe.loc[len(self.output_dataframe)] = self.process_data_row()
                self.scope_dataframe.loc[len(self.scope_dataframe)] = scope_row
                self.current_scope_row = scope_row
                self.update_output_data()

                if self.power_meter_load:
                    self.power_meter_load.auto_range_enable()
                if self.power_meter_load_2:
                    self.power_meter_load_2.auto_range_enable()
                if self.power_meter_source:
                    self.power_meter_source.current_auto_range_enable()

                sleep(self.post_capture_delay)

            self.test_data_table.add_blank_row()
            self._export_line_block()

        if self.discharge_pulses > 0:
            self.discharge_output(self.discharge_pulses)
        self._apply_main_sheet_number_formats()
        if self.embed_images:
            self._link_capture_main_sheet_rows()
            self.embed_waveforms_in_excel()

    def estimate_remaining(self, vin_index_t, load_index_t, vin_delays: bool = True):
        remaining_time_s = 0
        remaining_steps = 0
        start_adding_time = False
        vin_index = 0
        load_index = 0

        def add_time(t, add_step=False):
            nonlocal remaining_time_s, remaining_steps, start_adding_time
            if not start_adding_time and vin_index == vin_index_t and load_index == load_index_t:
                start_adding_time = True
            if start_adding_time:
                remaining_time_s += t
                if add_step:
                    remaining_steps += 1

        ramp_s = lambda v: float(v) / self.BULK_CAP_RAMP_V_PER_S + 0.5

        for vin_index, vin_row in enumerate(self.vin_list):
            load_index = 0
            for load_index, _ in enumerate(self.load_pairs):
                if self._bulk_cap_ramp_in_queue_estimate():
                    add_time(ramp_s(vin_row[0]))
                else:
                    add_time(2)
                add_time(1, True)
                add_time(2)
                add_time(self.STARTUP_CAPTURE_TIMEOUT_S)
                add_time(2)
                add_time(self.settle_time)
                add_time(1.5)
                add_time(self.post_capture_delay)
            add_time(1)

        add_time(self.discharge_pulses * 1.5)
        return remaining_time_s, remaining_steps

    @staticmethod
    def extract_test_condition(test_item_dict: dict) -> TestConditions:
        tc = EfficiencyWaveformTest_2Port.extract_test_condition(test_item_dict)
        if tc.name == StartupWaveformTest_2Port.title or 'Startup Waveform' in (tc.name or ''):
            tc.name = StartupWaveformTest_2Port.title
        saved = test_item_dict.get('SCOPE_CHANNELS') or {}
        default = StartupWaveformTest_2Port.tc_default.scope_channels
        tc.scope_channels = {
            ch: saved.get(ch, saved.get(str(ch), default[ch])) for ch in (1, 2, 3, 4)
        }
        return tc


StartupWaveformTest_2Port.tc_default = StartupWaveformTest_2Port._build_tc_default()
