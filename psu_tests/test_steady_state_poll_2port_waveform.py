"""Steady-state 2-port waveform test that polls meters for a timed window."""
import math
import numbers
import os
from copy import deepcopy
from time import sleep

import openpyxl
from openpyxl.styles import Font as CellFont

from psu_tests.definitions import TestConditions, I2CTestParameters, TestStatus, test_control_flags
from psu_tests.test_object_imports import TestStopped, TestSkipped
from psu_tests.test_efficiency_2port_waveform import EfficiencyWaveformTest_2Port


class SteadyStatePollWaveformTest_2Port(EfficiencyWaveformTest_2Port):
    """
    Steady-State Poll Waveform 2 Port.

    Same line/load sweep as Steady-State Waveform 2 Port. Every poll sample
    reads the meters and Vds, then stops the scope, saves that waveform, and
    returns the scope to Normal so the next interval can capture again.
    Each sample is its own Excel row (Sample, Elapsed).
    Default window is 5 s for 5 minutes. Stop at any time keeps the rows
    already taken and writes them to the Excel file.
    """

    title = "Steady-State Poll Waveform 2 Port"
    short_title = "SS_POLL_2P"
    PNG_SUFFIX = "_SSP"
    POLL_COLUMNS = ("Sample", "Elapsed (s)")
    POLL_INTERVAL_PARAM_INDEX = 10
    POLL_DURATION_PARAM_INDEX = 11
    POLL_INTERVAL_DEFAULT_S = 5.0
    POLL_DURATION_DEFAULT_S = 5 * 60.0
    # One console row must fit a normal terminal. Extra columns wrap under it.
    POLL_CONSOLE_WIDTH = 100
    POLL_PIPE_COLUMNS = (
        "Sample", "Elapsed (s)", "Vin (rms)", "Iin (mA)", "Pin (W)",
        "Vo1 (V)", "Io1 (A)", "Po1 (W)", "Vo2 (V)", "Io2 (A)", "Po2 (W)",
        "Efficiency (%)",
    )

    i2c_ui_definitions = EfficiencyWaveformTest_2Port.i2c_ui_definitions
    tc_default = None

    @classmethod
    def _build_tc_default(cls):
        tc = EfficiencyWaveformTest_2Port.tc_default
        i2c = tc.i2c_test_parameters
        params = list(getattr(i2c, 'param', []) or [])
        while len(params) <= cls.POLL_DURATION_PARAM_INDEX:
            params.append(0.0)
        params[cls.POLL_INTERVAL_PARAM_INDEX] = cls.POLL_INTERVAL_DEFAULT_S
        params[cls.POLL_DURATION_PARAM_INDEX] = cls.POLL_DURATION_DEFAULT_S
        scope_channels = deepcopy(tc.scope_channels)
        ch1 = dict(scope_channels.get(1) or {})
        ch1['enabled'] = True
        ch1['name'] = 'VDS_PRI'
        ch1['measurements'] = ['MAXimum']
        ch1['derating'] = 1700.0
        scope_channels[1] = ch1
        ch2 = dict(scope_channels.get(2) or {})
        if ch2.get('name') == 'VDS_PRI':
            ch2['name'] = 'VDS_SR'
            ch2['enabled'] = False
            scope_channels[2] = ch2
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
                cbx_params=list(getattr(i2c, 'cbx_param', []) or []),
            ),
            unit_id=tc.unit_id,
            ambient_temp=tc.ambient_temp,
            scope_channels=scope_channels,
        )

    @staticmethod
    def sample_count_for(interval_s, duration_s) -> int:
        """Samples at t=0, t=interval, ... while t <= duration. At least one."""
        try:
            interval = float(interval_s)
            duration = float(duration_s)
        except (TypeError, ValueError):
            return 1
        if interval <= 0 or duration <= 0:
            return 1
        return int(math.floor((duration + 1e-9) / interval)) + 1

    def _sample_count(self) -> int:
        return self.sample_count_for(self.poll_interval_s, self.poll_duration_s)

    @classmethod
    def _read_poll_param(cls, params, index, default) -> float:
        try:
            if params and len(params) > index and str(params[index]).strip() != '':
                val = float(params[index])
                if val < 0:
                    return default
                return val
        except (TypeError, ValueError):
            pass
        return default

    def unpack_test_item(self):
        super().unpack_test_item()
        i2c = getattr(self.test_conditions, 'i2c_test_parameters', None)
        params = list(getattr(i2c, 'param', []) or [])
        self.poll_interval_s = self._read_poll_param(
            params, self.POLL_INTERVAL_PARAM_INDEX, self.POLL_INTERVAL_DEFAULT_S)
        self.poll_duration_s = self._read_poll_param(
            params, self.POLL_DURATION_PARAM_INDEX, self.POLL_DURATION_DEFAULT_S)
        self.poll_sample_index = 1
        self.poll_elapsed_s = 0.0

    def build_detailed_output_basename(self) -> str:
        return (
            f"SSP {self._line_vin_filename_part()} {self.vout_V:g}V "
            f"{self._dual_port_power_filename_part()} {self._scope_names_filename_part()}"
        )

    def define_data_header(self):
        return list(super().define_data_header()) + list(self.POLL_COLUMNS)

    def scope_excel_col(self) -> int:
        return super().scope_excel_col() + len(self.POLL_COLUMNS)

    def process_data_row(self):
        row = super().process_data_row()
        return row + [int(self.poll_sample_index), round(float(self.poll_elapsed_s), 2)]

    @staticmethod
    def _poll_cell_text(value) -> str:
        if value is None:
            return ""
        if isinstance(value, bool):
            return str(value)
        if isinstance(value, numbers.Integral):
            return str(int(value))
        if isinstance(value, numbers.Real):
            return f"{float(value):.2f}"
        return str(value)

    def _poll_console_omit(self, header: str) -> bool:
        """Columns already shown on the sample banner, or a long file path."""
        if header in ("Ch1 Load", "Ch2 Load", "Freq (Hz)", "Waveform File"):
            return True
        return header == f"V{getattr(self, 'coupling', 'AC')} (rms)"

    @staticmethod
    def _poll_col_widths(headers, by_name):
        return [max(len(header), len(by_name.get(header, "")), 1) for header in headers]

    @classmethod
    def _poll_grid_width(cls, headers, by_name) -> int:
        if not headers:
            return 0
        widths = cls._poll_col_widths(headers, by_name)
        return sum(widths) + 3 * len(widths) + 1

    @staticmethod
    def _poll_grid_line(cells, widths, align_right=False) -> str:
        padded = []
        for cell, width in zip(cells, widths):
            text = str(cell)
            padded.append(text.rjust(width) if align_right else text.ljust(width))
        return "| " + " | ".join(padded) + " |"

    @staticmethod
    def _poll_sep_line(widths) -> str:
        return "|" + "|".join("-" * (width + 2) for width in widths) + "|"

    def _poll_console_columns(self, headers, by_name):
        columns = [h for h in self.POLL_PIPE_COLUMNS if h in by_name]
        columns += [h for h in headers if h not in columns and not self._poll_console_omit(h)]
        return columns

    def _poll_column_bands(self, columns, by_name):
        """Split columns so each grid line fits the console."""
        bands = []
        current = []
        for header in columns:
            trial = current + [header]
            if current and self._poll_grid_width(trial, by_name) > self.POLL_CONSOLE_WIDTH:
                bands.append(current)
                current = [header]
            else:
                current = trial
        if current:
            bands.append(current)
        return bands

    def _print_wrapped(self, text, indent=""):
        width = self.POLL_CONSOLE_WIDTH
        pending = text
        while pending:
            room = width - len(indent)
            if len(pending) <= room:
                print(indent + pending, flush=True)
                return
            cut = pending.rfind(" ", 0, room + 1)
            if cut <= 0:
                cut = max(1, room)
            print(indent + pending[:cut].rstrip(), flush=True)
            pending = pending[cut:].lstrip()
            indent = "  "

    def _print_poll_banner(self, by_name):
        count = self._sample_count()
        index = int(getattr(self, "poll_sample_index", 1) or 1)
        elapsed = by_name.get("Elapsed (s)", "")
        ch1 = by_name.get("Ch1 Load", "")
        ch2 = by_name.get("Ch2 Load", "")
        freq = by_name.get("Freq (Hz)", "")
        vin_set = by_name.get(f"V{getattr(self, 'coupling', 'AC')} (rms)", "")
        parts = [f"[POLL] {index}/{count}  t={elapsed} s", f"Ch1 {ch1}", f"Ch2 {ch2}"]
        if vin_set:
            parts.append(f"set {vin_set} {getattr(self, 'coupling', 'AC')}")
        if freq:
            parts.append(f"{freq} Hz")
        self._print_wrapped("   ".join(parts))

    def _print_poll_table_row(self):
        """Print the latest sample as a short table, then the remaining columns."""
        headers = [str(h) for h in (list(self.header_list) + list(self.scope_header_list))]
        data = getattr(getattr(self, "test_data_table", None), "data", None) or []
        if not headers or not data:
            return
        row = list(data[-1])
        if len(row) < len(headers):
            row.extend([""] * (len(headers) - len(row)))
        by_name = {
            header: self._poll_cell_text(value)
            for header, value in zip(headers, row[:len(headers)])
        }
        if int(getattr(self, "poll_sample_index", 1) or 1) == 1:
            print("[POLL TABLE]", flush=True)
        self._print_poll_banner(by_name)
        columns = self._poll_console_columns(headers, by_name)
        for band in self._poll_column_bands(columns, by_name):
            widths = self._poll_col_widths(band, by_name)
            print(self._poll_grid_line(band, widths), flush=True)
            print(self._poll_sep_line(widths), flush=True)
            print(self._poll_grid_line(
                [by_name[h] for h in band], widths, align_right=True), flush=True)
        print(flush=True)

    def update_output_data(self):
        super().update_output_data()
        self._print_poll_table_row()

    @staticmethod
    def _excel_num_format_for_header(header: str) -> str:
        if header == 'Sample':
            return '0'
        if header == 'Elapsed (s)':
            return '#,##0.00'
        return EfficiencyWaveformTest_2Port._excel_num_format_for_header(header)

    def _write_run_metadata_rows(self, ws):
        super()._write_run_metadata_rows(ws)
        rows = (
            (2, "Poll interval (s)", self.poll_interval_s),
            (3, "Poll duration (min)", self.poll_duration_s / 60.0),
            (4, "Samples per point", self._sample_count()),
        )
        for row, label, value in rows:
            ws[f"D{row}"] = label
            ws[f"E{row}"] = value
            ws[f"D{row}"].font = CellFont(bold=True, size=10, color="1F497D")
            ws[f"E{row}"].font = CellFont(size=10)

    def _write_excel_section_header_row(self, ws, row: int):
        super()._write_excel_section_header_row(ws, row)
        ws.merge_cells(f"T{row}:U{row}")
        ws[f"T{row}"] = "Timed Poll"
        self._style_excel_section_title_cell(ws[f"T{row}"])

    def setup_data_file(self):
        super().setup_data_file()
        desired = (
            f"{self.short_title}_{self.coupling}_{round(self.vout_V, 3):g}V_"
            f"{round(self.i_max_A, 3):g}A")
        if len(desired) > 31:
            desired = desired[:31]
        if self.sheet_name == desired:
            return
        ws = self.wb[self.sheet_name]
        ws.title = desired
        self.sheet_name = desired
        self.wb.save(self.data_file_path)
        self.wb.close()
        self.wb = openpyxl.load_workbook(self.data_file_path)
        self.ws = self.wb[self.sheet_name]

    def test_loop(self):
        try:
            super().test_loop()
        except (TestStopped, TestSkipped):
            self._save_collected_rows()
            raise

    def _save_collected_rows(self):
        """Write samples already taken when the operator stops or skips."""
        try:
            df = getattr(self, 'output_dataframe', None)
            if df is not None and len(df) > 1 and getattr(self, 'data_file_path', None):
                self._export_line_block()
            if getattr(self, 'data_file_path', None):
                self._apply_main_sheet_number_formats()
            if getattr(self, 'embed_images', False) and getattr(self, 'captured_records', None):
                self._link_capture_main_sheet_rows()
                self.embed_waveforms_in_excel()
            path = getattr(self, 'data_file_path', None)
            if path:
                print(f"[POLL] Partial results saved to {path}")
        except Exception as exc:
            print(f"[Warning] Could not save partial poll workbook: {exc}")

    def _note_partial_capture(self, records_before, rows_at_start):
        for rec in (getattr(self, 'captured_records', []) or [])[records_before:]:
            rec['n_samples'] = 1

    def _raise_if_abort(self, records_before, rows_at_start):
        stop = test_control_flags.get('StopTest', False)
        skip = test_control_flags.get('SkipTest', False)
        if not stop and not skip:
            return
        self._note_partial_capture(records_before, rows_at_start)
        if stop:
            raise TestStopped
        raise TestSkipped

    def _wait_or_stop(self, seconds, records_before, rows_at_start):
        """Sleep in short slices so Stop is honored during the poll interval."""
        remaining = float(seconds)
        while remaining > 1e-9:
            self._raise_if_abort(records_before, rows_at_start)
            chunk = min(0.25, remaining)
            sleep(chunk)
            remaining -= chunk

    def _extra_acquire_time_s(self) -> float:
        """Scheduled waits after sample 1. Each later sample sleeps the poll interval."""
        n = self._sample_count()
        if n <= 1:
            return 0.0
        return (n - 1) * float(self.poll_interval_s)

    @staticmethod
    def _format_estimate(seconds) -> str:
        total = int(round(float(seconds or 0)))
        if total < 0:
            total = 0
        hours, rem = divmod(total, 3600)
        minutes, secs = divmod(rem, 60)
        parts = []
        if hours:
            parts.append(f"{hours} h")
        if minutes or hours:
            parts.append(f"{minutes} min")
        parts.append(f"{secs} s")
        return " ".join(parts)

    @classmethod
    def preview_total_s(
        cls,
        vin_list,
        n_loads,
        initial_soak,
        line_soak,
        load_soak,
        integration_s,
        settle_s,
        post_capture_s,
        auto_find,
        discharge_pulses,
        poll_interval_s,
        poll_duration_s,
        coupling_dc=True,
        usbpd=False,
    ) -> float:
        """Same queue total as estimate_remaining, for the Add Tests preview."""
        n_samples = cls.sample_count_for(poll_interval_s, poll_duration_s)
        extra = 0.0 if n_samples <= 1 else (n_samples - 1) * float(poll_interval_s)
        n_loads = max(1, int(n_loads or 1))
        vins = list(vin_list or [[0, 0]])
        total = 0.0
        ramp = float(cls.BULK_CAP_RAMP_V_PER_S)
        for index, row in enumerate(vins):
            if coupling_dc:
                v_set = float(row[0])
                if index == 0:
                    total += 0.5
                else:
                    v_prev = float(vins[index - 1][0])
                    total += abs(v_set - v_prev) / ramp + 0.2
            total += 4
            if usbpd:
                total += 1
            total += float(initial_soak if index == 0 else line_soak)
            for _ in range(n_loads):
                total += 2
                total += float(load_soak)
                total += float(settle_s)
                total += float(integration_s)
                total += 1.7
                total += 12 if auto_find else 2
                total += extra
                total += float(post_capture_s)
            total += 3
        total += float(discharge_pulses) * 1.5
        return total

    def _scope_row_from_measurements(self, meas: dict, trig_level, img_path: str = "") -> list:
        try:
            level = round(float(trig_level), 2)
        except (TypeError, ValueError):
            level = 0.0
        row = [f"CH{self.trigger_channel}", level]
        for label in self.scope_measurement_labels:
            val = meas.get(label)
            row.append(val if val is not None else "N/A")
        if not self.embed_images:
            row.append(img_path or "")
        return row

    def _mark_scope(self, action: str):
        actions = getattr(self, "_poll_scope_actions", None)
        if actions is None:
            actions = []
            self._poll_scope_actions = actions
        actions.append(action)

    def _resume_scope_normal(self):
        """Leave the scope acquiring in Normal so the next interval has a new waveform."""
        scope = self.oscilloscope
        self._mark_scope("NORM")
        if hasattr(scope, "trigger_mode"):
            scope.trigger_mode("NORM")
        elif hasattr(scope, "set_trigger_mode"):
            scope.set_trigger_mode("NORM")
        self._mark_scope("run")
        scope.run()

    def _save_poll_screenshot(self, vin_set, i1_A, i2_A) -> str:
        prefix = f"{self.unit_id}_" if self.unit_id else ""
        pwr = self._dual_port_power_filename_part(i1_A=i1_A, i2_A=i2_A, png_suffix=True)
        png_suffix = getattr(self, "PNG_SUFFIX", "") or ""
        sample = int(getattr(self, "poll_sample_index", 1) or 1)
        elapsed = float(getattr(self, "poll_elapsed_s", 0.0) or 0.0)
        img_filename = (
            f"{prefix}{vin_set:g}V{self.coupling}_Ch1_{i1_A:g}A_Ch2_{i2_A:g}A"
            f"{pwr}_s{sample}_t{elapsed:g}s{png_suffix}.png")
        img_path = os.path.join(self.waveform_filepath, img_filename)
        self._mark_scope("screenshot")
        try:
            self.oscilloscope.get_screenshot(img_filename, self.waveform_filepath)
        except Exception as exc:
            print(f"[Warning] Failed to capture oscilloscope screenshot {img_filename}: {exc}")
        return img_path

    def _capture_poll_waveform(self, vin_set, i1_A, i2_A, records_before, rows_at_start) -> list:
        """Stop, read Vds, save the waveform, then return the scope to Normal."""
        n_meas = len(self.scope_measurement_labels)
        while True:
            self._raise_if_abort(records_before, rows_at_start)
            self.update_status_log("Scope stop", upcoming="Measure Vds")
            self._mark_scope("stop")
            self.oscilloscope.stop()
            self._mark_scope("measure")
            meas = self.query_active_scope_measurements()
            trig_level = self._read_trigger_level()
            if self.prompt_before_capture and int(self.poll_sample_index) == 1:
                meas_str = "".join(
                    f"{key}: {val}<br>" for key, val in meas.items()) or "No active measurements found.<br>"
                message = (
                    f"<b>Operating Point:</b> {vin_set:g} V{self.coupling} | "
                    f"Ch1 {i1_A:g} A ({self.current_ch1_lbl}) | Ch2 {i2_A:g} A ({self.current_ch2_lbl})<br>"
                    f"<b>Sample:</b> {int(self.poll_sample_index)} &nbsp; "
                    f"<b>Elapsed:</b> {float(self.poll_elapsed_s):g} s<br>"
                    f"<b>Live Measurements:</b><br>{meas_str}<br>"
                    "The scope is stopped. Capture this waveform, or choose another action:"
                )
                action = self.request_capture_action(
                    f"Capture Waveform ({vin_set:g} V, sample {int(self.poll_sample_index)})",
                    message)
                if action == "RECAPTURE":
                    self._resume_scope_normal()
                    continue
                if action == "STOP":
                    raise TestStopped
                if action == "SKIP":
                    self._resume_scope_normal()
                    row = [f"CH{self.trigger_channel}", "N/A"] + ["N/A"] * n_meas
                    if not self.embed_images:
                        row.append("")
                    return row
            img_path = self._save_poll_screenshot(vin_set, i1_A, i2_A)
            self.captured_records.append({
                'vin': vin_set, 'i1': i1_A, 'i2': i2_A,
                'ch1_lbl': f"{self.current_ch1_lbl} t={float(self.poll_elapsed_s):g}s",
                'ch2_lbl': self.current_ch2_lbl,
                'eff': self.eff_total_pct, 'path': img_path, 'measurements': meas,
                'n_samples': 1,
            })
            self._resume_scope_normal()
            return self._scope_row_from_measurements(meas, trig_level, img_path)

    def _acquire_operating_point(self, vin_set, i1_A, i2_A):
        n = self._sample_count()
        interval = float(self.poll_interval_s) if n > 1 else 0.0
        records_before = len(self.captured_records)
        rows_at_start = len(self.output_dataframe)
        if getattr(self, "_poll_scope_actions", None) is None:
            self._poll_scope_actions = []
        try:
            for sample in range(n):
                self._raise_if_abort(records_before, rows_at_start)
                self.poll_sample_index = sample + 1
                self.poll_elapsed_s = sample * interval
                if sample == 0:
                    self.update_status_log(
                        f"Poll sample 1/{n}", upcoming="Measure Vds")
                    self._measure_efficiency(i2_A)
                    if self.auto_find_trigger:
                        self.update_status_log(
                            "Sweeping Trigger Level...", upcoming="Scope stop")
                        self.find_trigger(
                            channel=self.trigger_channel, trigger_delta=self.trigger_delta)
                else:
                    self.update_status_log(
                        f"Poll sample {sample + 1}/{n} after {interval:g} s",
                        upcoming="Measure Vds")
                    self._wait_or_stop(interval, records_before, rows_at_start)
                    self._measure_efficiency(i2_A)
                scope_row = self._capture_poll_waveform(
                    vin_set, i1_A, i2_A, records_before, rows_at_start)
                self._append_measurement_row(scope_row)
                if len(scope_row) > 1 and scope_row[1] == "N/A":
                    return
        except (TestStopped, TestSkipped):
            self._note_partial_capture(records_before, rows_at_start)
            raise
        self._note_partial_capture(records_before, rows_at_start)

    def _link_capture_main_sheet_rows(self):
        row = self.excel_first_data_row + 1
        for rec in self.captured_records:
            rec['main_sheet_row'] = row
            row += int(rec.get('n_samples') or 1)

    def update_test_list_text(self):
        if self.status == TestStatus.IN_QUEUE:
            self.total_time, self.total_steps = self.estimate_remaining(0, 0, vin_delays=True)
            self.estimated_time_s = self.total_time
        super().update_test_list_text()
        shown_s = self.estimated_time_s if self.status == TestStatus.IN_PROGRESS else self.total_time
        label = "Estimated time remaining" if self.status == TestStatus.IN_PROGRESS else "Estimated time"
        prog = getattr(self, 'progress_txt', '') or '0%'
        estimate_line = f"{self.status}: {label}: {self._format_estimate(shown_s)}, {prog}"
        lines = []
        replaced = False
        for line in self.test_list_text.split("\n"):
            if line.startswith("Poll:"):
                continue
            if line.startswith(f"{TestStatus.IN_QUEUE}:") or line.startswith(f"{TestStatus.IN_PROGRESS}:"):
                lines.append(estimate_line)
                replaced = True
            else:
                lines.append(line)
        if not replaced and self.status in (TestStatus.IN_QUEUE, TestStatus.IN_PROGRESS):
            lines.append(estimate_line)
        duration_txt = f"{float(self.poll_duration_s) / 60.0:g} min"
        note = (
            f"Poll: every {self.poll_interval_s:g} s for {duration_txt} "
            f"({self._sample_count()} samples per point). "
            "Each sample stops the scope, saves the waveform, then returns the scope to Normal. "
            "Stop keeps rows already saved to Excel."
        )
        self.test_list_text = "\n".join(lines)
        if note not in self.test_list_text:
            self.test_list_text += "\n" + note


SteadyStatePollWaveformTest_2Port.tc_default = SteadyStatePollWaveformTest_2Port._build_tc_default()
