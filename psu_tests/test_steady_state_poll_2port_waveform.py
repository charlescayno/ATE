"""Steady-state 2-port waveform test that polls meters for a timed window."""
import math
import numbers
from copy import deepcopy
from time import sleep

import openpyxl
from openpyxl.styles import Font as CellFont

from psu_tests.definitions import TestConditions, I2CTestParameters, test_control_flags
from psu_tests.test_object_imports import TestStopped, TestSkipped
from psu_tests.test_efficiency_2port_waveform import EfficiencyWaveformTest_2Port


class SteadyStatePollWaveformTest_2Port(EfficiencyWaveformTest_2Port):
    """
    Steady-State Poll Waveform 2 Port.

    Same line/load sweep and one scope screenshot per point as Steady-State
    Waveform 2 Port. After the screenshot, power-meter and scope measurements
    are read again every Poll Interval until Poll Duration has elapsed.
    Each sample is its own Excel row (Sample, Elapsed).
    Default window is 5 s for 15 minutes. Stop at any time keeps the rows
    already taken and writes them to the Excel file.
    """

    title = "Steady-State Poll Waveform 2 Port"
    short_title = "SS_POLL_2P"
    PNG_SUFFIX = "_SSP"
    POLL_COLUMNS = ("Sample", "Elapsed (s)")
    POLL_INTERVAL_PARAM_INDEX = 10
    POLL_DURATION_PARAM_INDEX = 11
    POLL_INTERVAL_DEFAULT_S = 5.0
    POLL_DURATION_DEFAULT_S = 15 * 60.0

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
            scope_channels=deepcopy(tc.scope_channels),
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

    @staticmethod
    def _poll_grid_line(cells, widths) -> str:
        padded = [str(cell).ljust(width) for cell, width in zip(cells, widths)]
        return "| " + " | ".join(padded) + " |"

    @staticmethod
    def _poll_sep_line(widths) -> str:
        return "|" + "|".join("-" * (width + 2) for width in widths) + "|"

    def _print_poll_table_row(self):
        """Print the latest Excel row as one row of a console table."""
        headers = [str(h) for h in (list(self.header_list) + list(self.scope_header_list))]
        data = getattr(getattr(self, "test_data_table", None), "data", None) or []
        if not headers or not data:
            return
        row = list(data[-1])
        if len(row) < len(headers):
            row.extend([""] * (len(headers) - len(row)))
        texts = [self._poll_cell_text(value) for value in row[:len(headers)]]
        new_point = int(getattr(self, "poll_sample_index", 1) or 1) == 1
        if new_point or not getattr(self, "_poll_table_widths", None):
            self._poll_table_widths = [
                max(len(header), len(text)) for header, text in zip(headers, texts)]
            print("[POLL TABLE]", flush=True)
            print(self._poll_grid_line(headers, self._poll_table_widths), flush=True)
            print(self._poll_sep_line(self._poll_table_widths), flush=True)
        print(self._poll_grid_line(texts, self._poll_table_widths), flush=True)

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
            (3, "Poll duration (s)", self.poll_duration_s),
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
        if len(getattr(self, 'captured_records', []) or []) <= records_before:
            return
        taken = len(self.output_dataframe) - rows_at_start
        if taken > 0:
            self.captured_records[records_before]['n_samples'] = taken

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
        n = self._sample_count()
        if n <= 1:
            return 0.0
        integ = float(getattr(self.soak_time, 'integration_time', 0) or 0)
        return (n - 1) * (float(self.poll_interval_s) + integ + 0.3)

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

    def _acquire_operating_point(self, vin_set, i1_A, i2_A):
        n = self._sample_count()
        interval = float(self.poll_interval_s) if n > 1 else 0.0
        records_before = len(self.captured_records)
        rows_at_start = len(self.output_dataframe)
        trig_level = None
        img_path = ""
        try:
            for sample in range(n):
                self._raise_if_abort(records_before, rows_at_start)
                self.poll_sample_index = sample + 1
                self.poll_elapsed_s = sample * interval
                if sample == 0:
                    self.update_status_log(
                        f"Poll sample 1/{n}", upcoming="Capture Waveform")
                    self._measure_efficiency(i2_A)
                    scope_row = self.capture_waveform_at_point(vin_set, i1_A, i2_A)
                    if len(scope_row) > 1 and scope_row[1] == "N/A":
                        self._append_measurement_row(scope_row)
                        return
                    trig_level = scope_row[1] if len(scope_row) > 1 else None
                    if not self.embed_images and scope_row:
                        img_path = scope_row[-1]
                else:
                    self.update_status_log(
                        f"Poll sample {sample + 1}/{n} after {interval:g} s",
                        upcoming="Read meters")
                    self._wait_or_stop(interval, records_before, rows_at_start)
                    self._measure_efficiency(i2_A)
                    meas = self.query_active_scope_measurements()
                    scope_row = self._scope_row_from_measurements(meas, trig_level, img_path)
                self._append_measurement_row(scope_row)
        except (TestStopped, TestSkipped):
            self._note_partial_capture(records_before, rows_at_start)
            raise
        if len(self.captured_records) > records_before:
            self.captured_records[records_before]['n_samples'] = (
                len(self.output_dataframe) - rows_at_start)

    def _link_capture_main_sheet_rows(self):
        row = self.excel_first_data_row + 1
        for rec in self.captured_records:
            rec['main_sheet_row'] = row
            row += int(rec.get('n_samples') or 1)

    def update_test_list_text(self):
        super().update_test_list_text()
        duration_s = float(self.poll_duration_s)
        if duration_s >= 60 and abs(duration_s % 60) < 1e-6:
            duration_txt = f"{duration_s / 60:g} min"
        else:
            duration_txt = f"{duration_s:g} s"
        note = (
            f"Poll: every {self.poll_interval_s:g} s for {duration_txt} "
            f"({self._sample_count()} samples per point). "
            "Stop keeps rows already saved to Excel."
        )
        if note not in self.test_list_text:
            self.test_list_text += "\n" + note


SteadyStatePollWaveformTest_2Port.tc_default = SteadyStatePollWaveformTest_2Port._build_tc_default()
