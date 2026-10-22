import os
import time

from psu_tests.test_object_imports import *
from psu_tests.test_efficiency_2port_waveform import EfficiencyWaveformTest_2Port
from psu_tests.test_startup_2port_waveform import _StartupYesNoHelper


class StartupWaveformTest_ACTurnOn(EfficiencyWaveformTest_2Port):
    """
    DER-1113-style startup: discharge, arm scope (RUN SINGLE), AC/input ON, soak,
    discharge again, operator confirms capture, then STOP + PNG + Excel.

    No HMP bulk-cap connect — startup event is turning the input supply on at Vin.
    """

    title = "Startup Waveform AC Turn-On (DER-1113)"
    short_title = "SU_WF_AC"
    PNG_SUFFIX = "_SUAC"

    PRE_AC_ON_S = 1.0
    POST_AC_ON_S = 3.0

    tc_default = None

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
        if len(params) > 6:
            params[6] = 2.0
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
            f"SUAC {self._line_vin_filename_part()} {self.vout_V:g}V "
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

    def _ask_yes_no(self, title: str, message: str) -> bool:
        if os.environ.get('PI_ATE_AUTO_CONFIRM') == '1':
            return True
        try:
            from PySide2.QtWidgets import QApplication
            app = QApplication.instance()
            if app is None:
                return True
            helper = getattr(self, '_startup_yes_no_helper', None)
            if helper is None:
                helper = _StartupYesNoHelper()
                helper.moveToThread(app.thread())
                self._startup_yes_no_helper = helper
            helper._main_window = getattr(self, 'parent', None)
            helper.result = True
            helper.show_sig.emit(title, message)
            return helper.result
        except Exception as exc:
            print(f"[Warning] Yes/No prompt failed: {exc}")
        return True

    def _turn_input_on_at_vin(self, vin_set: float, vin_freq_row):
        self.input_supply.set_voltage_with_coupling(voltage=vin_set, coupling=self.coupling)
        if self.coupling == AC_SOURCE_COUPLING.AC:
            self.input_supply.frequency = vin_freq_row[1]
        self.input_supply.turn_on()
        self.source_vout = vin_set
        self.test_data.vin_set_V = vin_set
        self.test_data.ac_freq_Hz = vin_freq_row[1]

    def _prompt_confirm_save_capture(self, vin_set: float, i1_A: float, i2_A: float) -> bool:
        coupling_label = "DC" if str(self.coupling).upper() == "DC" else "AC"
        msg = (
            "<b>Startup AC turn-on</b><br><br>"
            "Review the capture on the oscilloscope, then save.<br><br>"
            f"Input: <b>{vin_set:g} V {coupling_label}</b><br>"
            f"Ch1 {i1_A:g} A ({self.current_ch1_lbl}) | "
            f"Ch2 {i2_A:g} A ({self.current_ch2_lbl})<br><br>"
            "<b>Yes</b> — STOP scope and save PNG.<br>"
            "<b>No</b> — skip this point."
        )
        return self._ask_yes_no("Save Startup Waveform", msg)

    def _startup_png_filename(self, vin_set, i1_A, i2_A) -> str:
        prefix = f"{self.unit_id}_" if self.unit_id else ""
        pwr = self._dual_port_power_filename_part(i1_A=i1_A, i2_A=i2_A, png_suffix=True)
        return (
            f"{prefix}{vin_set:g}V{self.coupling}_Ch1_{i1_A:g}A_Ch2_{i2_A:g}A"
            f"{pwr}{self.PNG_SUFFIX}.png")

    def capture_ac_turnon_at_point(self, vin_set, vin_freq_row, i1_A, i2_A) -> list:
        """DER-1113 sequence per (Vin, load) point."""
        n_meas = len(self.scope_measurement_labels)
        trig_level = self._read_trigger_level()
        pulses = max(1, int(self.discharge_pulses)) if self.discharge_pulses else 2

        while True:
            if self.reapply_scope_before_capture:
                self.apply_scope_setup()

            self.update_status_log("Discharging output...", upcoming="Set loads")
            self.discharge_output(pulses)

            self.update_status_log(
                f"Setting Loads Ch1 {i1_A:g} A / Ch2 {i2_A:g} A", upcoming="RUN SINGLE")
            self._set_loads(i1_A, i2_A)

            self.update_status_log("Arming oscilloscope (RUN SINGLE)...", upcoming="Input ON")
            self.oscilloscope.run_single()

            sleep(self.PRE_AC_ON_S)

            self.update_status_log(
                f"Input ON — {vin_set:g} V{self.coupling} (startup event)",
                upcoming=f"Soak {self.POST_AC_ON_S:g} s")
            self._turn_input_on_at_vin(vin_set, vin_freq_row)

            sleep(self.POST_AC_ON_S)

            self.update_status_log("Discharging output...", upcoming="Confirm save")
            self.discharge_output(pulses)

            if not self._prompt_confirm_save_capture(vin_set, i1_A, i2_A):
                print(f"[SKIP] Save declined at {vin_set:g} V, Ch1 {i1_A:g} A, Ch2 {i2_A:g} A")
                self.oscilloscope.run()
                row = [f"CH{self.trigger_channel}", "N/A"] + ["N/A"] * n_meas
                if not self.embed_images:
                    row.append("")
                return row

            self.update_status_log("Stopping scope and saving PNG...", upcoming="Excel row")
            try:
                self.oscilloscope.stop()
            except Exception as exc:
                print(f"[Warning] scope.stop: {exc}")
            meas = self.query_active_scope_measurements()

            if self.prompt_before_capture:
                meas_str = "".join(f"{k}: {v}<br>" for k, v in meas.items()) or "No active measurements found.<br>"
                message = (
                    f"<b>Operating Point:</b> {vin_set:g} V{self.coupling} | "
                    f"Ch1 {i1_A:g} A ({self.current_ch1_lbl}) | Ch2 {i2_A:g} A ({self.current_ch2_lbl})<br>"
                    f"<b>Unit ID:</b> {self.unit_id}<br>"
                    f"<b>Trigger Level:</b> CH{self.trigger_channel} @ {trig_level:.2f} V<br>"
                    f"<b>Live Measurements:</b><br>{meas_str}<br>"
                    "Review the startup waveform, then choose an action:"
                )
                action = self.request_capture_action(
                    f"Startup Capture ({vin_set:g} V, Ch1 {self.current_ch1_lbl} / Ch2 {self.current_ch2_lbl})",
                    message)
                if action == "RECAPTURE":
                    print(f"[RECAPTURE] Re-run DER sequence at {vin_set} V, Ch1 {i1_A} A, Ch2 {i2_A} A")
                    try:
                        self.input_supply.turn_off()
                    except Exception:
                        pass
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

        if self.prompt_before_start:
            prompt_msg = (
                "<b>================== OSCILLOSCOPE SETUP REMINDER ==================</b><br>"
                f"Unit ID: {self.unit_id} | Ambient Temp: {self.ambient_temp:g}\u00b0C<br>"
                f"Ch1: {self.vout_V:g} V / {self.i_max_A:g} A &nbsp; "
                f"Ch2: {self.vout_2_V:g} V / {self.i_max_2_A:g} A &nbsp; Mode: {self.dual_load_mode}<br><br>"
                "1. Load the correct startup .DFL file into the oscilloscope.<br>"
                f"2. Probe Configuration: {self.probe_setup}<br>"
                f"3. Trigger Channel: CH{self.trigger_channel} (fixed — Auto Find Trigger off)<br>"
                "4. Typical probes: CH1 Primary Vds, CH2 Ids (DER-1113).<br>"
                "<b>=================================================================</b><br><br>"
                "Click OK once setup is complete to proceed."
            )
            self.create_message_popup("Oscilloscope Setup Verification", prompt_msg, MessageType.INFO)

        self.apply_scope_setup()

        self.total_time, self.total_steps = self.estimate_remaining(0, 0, vin_delays=False)
        self.status_report(0, 0, vin_delays=False)

        for self.vin_index, self.vin_freq in enumerate(self.vin_list):
            vin_set = self.vin_freq[0]
            self.create_new_plot_series()

            for load_index, (i1_A, i2_A, ch1_lbl, ch2_lbl) in enumerate(self.load_pairs):
                if test_control_flags.get('StopTest', False):
                    raise TestStopped
                if test_control_flags.get('SkipTest', False):
                    raise TestSkipped

                self.status_report(self.vin_index, load_index, vin_delays=False)
                self.current_ch1_lbl = ch1_lbl
                self.current_ch2_lbl = ch2_lbl
                self.current_load_index = load_index

                scope_row = self.capture_ac_turnon_at_point(vin_set, self.vin_freq, i1_A, i2_A)

                sleep(self.settle_time)
                self.update_status_log("Measuring efficiency...", upcoming="Save row")
                self._measure_efficiency(i2_A)

                self.output_dataframe.loc[len(self.output_dataframe)] = self.process_data_row()
                self.scope_dataframe.loc[len(self.scope_dataframe)] = scope_row
                self.current_scope_row = scope_row
                self.update_output_data()

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
        pulses = max(1, int(self.discharge_pulses)) if self.discharge_pulses else 2
        per_point = (
            pulses * 1.5 * 2
            + 1 + self.PRE_AC_ON_S + self.POST_AC_ON_S
            + 1 + self.settle_time + 1.5 + self.post_capture_delay
        )

        def add_time(t, add_step=False):
            nonlocal remaining_time_s, remaining_steps, start_adding_time
            if not start_adding_time and vin_index == vin_index_t and load_index == load_index_t:
                start_adding_time = True
            if start_adding_time:
                remaining_time_s += t
                if add_step:
                    remaining_steps += 1

        for vin_index, _ in enumerate(self.vin_list):
            load_index = 0
            for load_index, _ in enumerate(self.load_pairs):
                add_time(per_point, True)
            add_time(1)

        add_time(self.discharge_pulses * 1.5)
        return remaining_time_s, remaining_steps

    @staticmethod
    def extract_test_condition(test_item_dict: dict) -> TestConditions:
        tc = EfficiencyWaveformTest_2Port.extract_test_condition(test_item_dict)
        if tc.name == StartupWaveformTest_ACTurnOn.title or 'DER-1113' in (tc.name or ''):
            tc.name = StartupWaveformTest_ACTurnOn.title
        saved = test_item_dict.get('SCOPE_CHANNELS') or {}
        default = StartupWaveformTest_ACTurnOn.tc_default.scope_channels
        tc.scope_channels = {
            ch: saved.get(ch, saved.get(str(ch), default[ch])) for ch in (1, 2, 3, 4)
        }
        return tc


StartupWaveformTest_ACTurnOn.tc_default = StartupWaveformTest_ACTurnOn._build_tc_default()
