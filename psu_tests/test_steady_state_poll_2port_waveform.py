"""Steady-state 2-port waveform test that polls meters for a timed window."""
import datetime
import math
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
    are read again after Poll Interval (idle gap since the previous read finished)
    until Poll Duration has elapsed.
    Each sample is its own Excel row (Sample, Elapsed, Time Start/End, Time Sampled).
    Default window is 5 min between samples for 20 min per load point. Stop at any time keeps the rows
    already taken and writes them to the Excel file.
    """

    title = "Steady-State Poll Waveform 2 Port"
    short_title = "SS_POLL_2P"
    PNG_SUFFIX = "_SSP"
    POLL_COLUMNS = (
        "Sample",
        "Elapsed (s)",
        "Time Start",
        "Time End",
        "Time Sampled",
        "Interval (s)",
    )
    POLL_DATETIME_EXCEL_FMT = "yyyy-mm-dd hh:mm:ss"
    POLL_INTERVAL_PARAM_INDEX = 10
    POLL_DURATION_PARAM_INDEX = 11
    POLL_INTERVAL_DEFAULT_S = 300.0
    POLL_READ_DURATION_GUESS_S = 0.75
    POLL_DURATION_DEFAULT_S = 20 * 60.0
    POLL_DEFAULT_SCOPE_CHANNELS = {
        1: {
            'enabled': True,
            'name': 'VDS_PRI',
            'measurements': ['MAXimum'],
            'derating': 1700.0,
            'cursor': {'enabled': False, 'type': 'VERTical'},
        },
        2: {'enabled': False, 'name': '', 'measurements': [], 'derating': None, 'cursor': {}},
        3: {'enabled': False, 'name': '', 'measurements': [], 'derating': None, 'cursor': {}},
        4: {'enabled': False, 'name': '', 'measurements': [], 'derating': None, 'cursor': {}},
    }

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
            scope_channels=deepcopy(cls.POLL_DEFAULT_SCOPE_CHANNELS),
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

    @staticmethod
    def effective_integration_s(soak_integration_s, poll_interval_s) -> float:
        """Integrate Pin/Pout for max(soak integration, poll interval) on this test only."""
        try:
            soak = float(soak_integration_s or 0)
        except (TypeError, ValueError):
            soak = 0.0
        try:
            poll = float(poll_interval_s or 0)
        except (TypeError, ValueError):
            poll = 0.0
        if soak < 0:
            soak = 0.0
        if poll < 0:
            poll = 0.0
        return max(soak, poll)

    def _effective_integration_s(self) -> float:
        return self.effective_integration_s(
            getattr(self.soak_time, 'integration_time', 0),
            getattr(self, 'poll_interval_s', 0),
        )

    def _configure_poll_power_meter_integration(self):
        timer_s = self._effective_integration_s()
        for pm in (
            self.power_meter_source,
            self.power_meter_load,
            self.power_meter_load_2,
        ):
            if pm is None:
                continue
            pm.integration_settings(mode="NORMAL", timer_s=timer_s)
            pm.stop_integration()
            pm.reset_integration()

    def setup_equipment(self):
        super().setup_equipment()
        self._configure_poll_power_meter_integration()
        eff = self._effective_integration_s()
        if eff > 0:
            soak = float(getattr(self.soak_time, 'integration_time', 0) or 0)
            print(
                f"[POLL] Power meter integration: {eff:g} s "
                f"(max of soak integration {soak:g} s, "
                f"poll interval {float(self.poll_interval_s):g} s)"
            )

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
        self.poll_point_start_dt = None
        self.poll_point_end_dt = None
        self.poll_row_sampled_dt = None
        self.poll_prev_sampled_dt = None
        self._poll_repeat_read_duration_s = self.POLL_READ_DURATION_GUESS_S

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
        if (
            self.poll_row_sampled_dt is not None
            and self.poll_prev_sampled_dt is not None
        ):
            interval_s = round(
                (self.poll_row_sampled_dt - self.poll_prev_sampled_dt).total_seconds(),
                2,
            )
        else:
            interval_s = 0.0
        return row + [
            int(self.poll_sample_index),
            round(float(self.poll_elapsed_s), 2),
            self.poll_point_start_dt,
            self.poll_point_end_dt,
            self.poll_row_sampled_dt,
            interval_s,
        ]

    def _poll_first_excel_col(self) -> int:
        return self.scope_excel_col() - len(self.POLL_COLUMNS)

    @staticmethod
    def _excel_num_format_for_header(header: str) -> str:
        if header == 'Sample':
            return '0'
        if header in ('Elapsed (s)', 'Interval (s)'):
            return '#,##0.00'
        if header in ('Time Start', 'Time End', 'Time Sampled'):
            return SteadyStatePollWaveformTest_2Port.POLL_DATETIME_EXCEL_FMT
        return EfficiencyWaveformTest_2Port._excel_num_format_for_header(header)

    def _write_run_metadata_rows(self, ws):
        super()._write_run_metadata_rows(ws)
        rows = (
            (2, "Poll interval (s)", self.poll_interval_s),
            (3, "Poll duration (s)", self.poll_duration_s),
            (4, "Samples per point", self._sample_count()),
            (5, "Effective integration (s)", self._effective_integration_s()),
        )
        for row, label, value in rows:
            ws[f"D{row}"] = label
            ws[f"E{row}"] = value
            ws[f"D{row}"].font = CellFont(bold=True, size=10, color="1F497D")
            ws[f"E{row}"].font = CellFont(size=10)

    def _write_excel_section_header_row(self, ws, row: int):
        super()._write_excel_section_header_row(ws, row)
        from openpyxl.utils import get_column_letter
        first_col = self._poll_first_excel_col()
        last_col = self.scope_excel_col() - 1
        first_letter = get_column_letter(first_col)
        last_letter = get_column_letter(last_col)
        ws.merge_cells(f"{first_letter}{row}:{last_letter}{row}")
        cell = ws[f"{first_letter}{row}"]
        cell.value = "Timed Poll"
        self._style_excel_section_title_cell(cell)

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

    def _wait_for_scheduled_poll_sample(
            self, interval_s, records_before, rows_at_start):
        """Start the next read so Time Sampled is ~interval_s after the previous."""
        if self.poll_prev_sampled_dt is None:
            return
        gap = float(interval_s)
        slack = float(getattr(self, '_poll_repeat_read_duration_s',
                              self.POLL_READ_DURATION_GUESS_S))
        slack = min(max(slack, 0.05), gap * 0.9)
        target_start = (
            self.poll_prev_sampled_dt
            + datetime.timedelta(seconds=gap - slack)
        )
        while datetime.datetime.now() < target_start:
            self._raise_if_abort(records_before, rows_at_start)
            remaining = (target_start - datetime.datetime.now()).total_seconds()
            self._wait_or_stop(min(0.25, max(remaining, 0.0)),
                               records_before, rows_at_start)

    def _measure_poll_readings(self, i2_A):
        """PM reads for poll samples without re-sending AUTO range every tick."""
        self.test_data.gather_data(
            coupling=self.coupling,
            usb_pd=self.usbpd_test,
            stable_source_pin=True,
        )
        if self.power_meter_load_2 or self.electronic_load_2:
            self.test_data_2.gather_data_load(
                integrate=False, force_use_eload_data=self.use_eload_data)
            self.test_data_2.vreg_pct = (
                ((self.test_data_2.vout_V - self.vout_2_V) / self.vout_2_V) * 100
                if self.vout_2_V else 0)
        else:
            self.test_data_2.vout_V = self.vout_2_V
            self.test_data_2.iout_A = i2_A
            self.test_data_2.pout_W = self.vout_2_V * i2_A
            self.test_data_2.vreg_pct = 0.0

        self.po_total_W = self.test_data.pout_W + self.test_data_2.pout_W
        self.eff_total_pct = (
            (self.po_total_W / self.test_data.pin_W * 100)
            if self.test_data.pin_W > 0 else 0)

    def _extra_acquire_time_s(self) -> float:
        n = self._sample_count()
        if n <= 1:
            return 0.0
        integ = self._effective_integration_s()
        return (n - 1) * (float(self.poll_interval_s) + integ + 0.3)

    def _append_measurement_row(self, scope_row):
        super()._append_measurement_row(scope_row)
        if self.poll_row_sampled_dt is not None:
            self.poll_prev_sampled_dt = self.poll_row_sampled_dt

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
        self.poll_prev_sampled_dt = None
        self._poll_repeat_read_duration_s = self.POLL_READ_DURATION_GUESS_S
        trig_level = None
        img_path = ""
        self.ensure_load_power_meters_auto_range()
        self.prepare_load_power_meters_for_poll_output()
        self.prepare_source_power_meter_for_poll_input()
        try:
            for sample in range(n):
                self._raise_if_abort(records_before, rows_at_start)
                self.poll_sample_index = sample + 1
                self.poll_elapsed_s = sample * interval
                if sample == 0:
                    self.poll_point_start_dt = datetime.datetime.now()
                    self.poll_point_end_dt = (
                        self.poll_point_start_dt
                        + datetime.timedelta(seconds=float(self.poll_duration_s))
                    )
                    self.update_status_log(
                        f"Poll sample 1/{n}", upcoming="Capture Waveform")
                    self._measure_poll_readings(i2_A)
                    scope_row = self.capture_waveform_at_point(vin_set, i1_A, i2_A)
                    if len(scope_row) > 1 and scope_row[1] == "N/A":
                        self._append_measurement_row(scope_row)
                        return
                    trig_level = scope_row[1] if len(scope_row) > 1 else None
                    if not self.embed_images and scope_row:
                        img_path = scope_row[-1]
                else:
                    self.update_status_log(
                        f"Poll sample {sample + 1}/{n} "
                        f"(~{interval:g} s period)",
                        upcoming="Read meters")
                    self._wait_for_scheduled_poll_sample(
                        interval, records_before, rows_at_start)
                    read_t0 = datetime.datetime.now()
                    self._measure_poll_readings(i2_A)
                    meas = self.query_active_scope_measurements()
                    scope_row = self._scope_row_from_measurements(
                        meas, trig_level, img_path)
                    read_t1 = datetime.datetime.now()
                    self._poll_repeat_read_duration_s = max(
                        0.05,
                        (read_t1 - read_t0).total_seconds(),
                    )
                self.poll_row_sampled_dt = datetime.datetime.now()
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
            f"Poll: ~{self.poll_interval_s:g} s between Time Sampled rows for {duration_txt} "
            f"({self._sample_count()} samples per point). "
            "Stop keeps rows already saved to Excel."
        )
        if note not in self.test_list_text:
            self.test_list_text += "\n" + note


SteadyStatePollWaveformTest_2Port.tc_default = SteadyStatePollWaveformTest_2Port._build_tc_default()
