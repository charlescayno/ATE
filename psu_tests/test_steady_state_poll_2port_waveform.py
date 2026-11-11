"""Steady-state 2-port waveform test that polls meters for a timed window."""
import datetime
import math
import os
import time
from copy import deepcopy
from time import sleep

import openpyxl
from openpyxl.styles import Font as CellFont

from psu_tests.definitions import TestConditions, I2CTestParameters, test_control_flags, TestFailed
from psu_tests.test_object_imports import TestStopped, TestSkipped
from psu_tests.test_efficiency_2port_waveform import EfficiencyWaveformTest_2Port


class SteadyStatePollWaveformTest_2Port(EfficiencyWaveformTest_2Port):
    """
    Steady-State Poll Waveform 2 Port.

    Same line/load sweep and one scope screenshot per point as Steady-State
    Waveform 2 Port. Each sample: integrate Pin (param 10) → meters → scope capture (PNG)
    → Excel row → repeat for N samples. Next sample integration starts after previous scope finishes.
    """

    title = "Steady-State Poll Waveform 2 Port"
    short_title = "SS_POLL_2P"
    PNG_SUFFIX = "_SSP"
    OUTPUT_PREFIX = "SSP"  # leading token of the detailed output file name
    POLL_COLUMNS = (
        "Sample",
        "Elapsed (s)",
        "Time Start",
        "Time End",
        "Time Sampled",
        "Time Integration Start",
        "Time Integration End",
        "Interval (s)",
    )
    POLL_DATETIME_EXCEL_FMT = "yyyy-mm-dd hh:mm:ss"
    POLL_INTERVAL_PARAM_INDEX = 10
    POLL_SAMPLES_PARAM_INDEX = 11
    POLL_DURATION_PARAM_INDEX = 11  # legacy alias (stored value is sample count)
    FAN_COOLING_PARAM_INDEX = 12
    NO_INTEGRATION_PARAM_INDEX = 13  # 1 = no Pin integration; param 10 becomes time interval per sample
    FAN_COOLING_VOLTAGE_V = 12.0
    FAN_COOLING_CURRENT_A = 4.0
    HMP_FAN_CHANNEL = 2
    POLL_INTERVAL_DEFAULT_S = 30.0
    POLL_READ_DURATION_GUESS_S = 0.75
    POLL_SAMPLES_DEFAULT = 3
    POLL_DURATION_DEFAULT_S = 20 * 60.0  # legacy duration for migration only
    LEGACY_POLL_DURATION_MIN_S = 1e5  # legacy duration migration effectively off: 1200 = 1200 samples
    POLL_SCOPE_CAPTURE_GUESS_S = 12.0
    # True: in No-integration mode the interval is the time between scope acquisitions
    # (idle wait is computed from the previous acquisition). False: wait after the capture.
    SCHEDULED_INTERVAL = False
    PRE_ACQ_GUESS_S = 3.0  # meter read + trigger/run_single/wait before the first schedule
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
        while len(params) <= cls.POLL_SAMPLES_PARAM_INDEX:
            params.append(0.0)
        params[cls.POLL_INTERVAL_PARAM_INDEX] = cls.POLL_INTERVAL_DEFAULT_S
        params[cls.POLL_SAMPLES_PARAM_INDEX] = float(cls.POLL_SAMPLES_DEFAULT)
        while len(params) <= cls.FAN_COOLING_PARAM_INDEX:
            params.append(0.0)
        params[cls.FAN_COOLING_PARAM_INDEX] = 0.0
        while len(params) <= cls.NO_INTEGRATION_PARAM_INDEX:
            params.append(0.0)
        params[cls.NO_INTEGRATION_PARAM_INDEX] = 0.0
        cbx = list(getattr(i2c, 'cbx_param', []) or [])
        while len(cbx) < 4:
            cbx.append('')
        if not str(cbx[0]).strip():
            cbx[0] = "Option C: Fixed Aux / Swept Main (Port 2 Fixed Load)"
        cbx[2] = "None (Fully Automated)"
        cbx[3] = "No"
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
        return int(getattr(self, 'poll_samples_n', self.POLL_SAMPLES_DEFAULT))

    @classmethod
    def read_samples_per_point(cls, params, poll_interval_s=None) -> int:
        """Param 11 = sample count; values >= LEGACY_POLL_DURATION_MIN_S are old duration (s)."""
        interval = poll_interval_s
        if interval is None:
            interval = cls._read_poll_param(
                params, cls.POLL_INTERVAL_PARAM_INDEX, cls.POLL_INTERVAL_DEFAULT_S)
        raw = cls._read_poll_param(
            params, cls.POLL_SAMPLES_PARAM_INDEX, float(cls.POLL_SAMPLES_DEFAULT))
        if raw >= cls.LEGACY_POLL_DURATION_MIN_S and interval > 0:
            return cls.sample_count_for(interval, raw)
        return max(1, int(round(raw)))

    @staticmethod
    def effective_integration_s(soak_integration_s, poll_interval_s=None) -> float:
        """Pin integration window = poll param 10 (soak integration ignored for poll Pin)."""
        del soak_integration_s
        try:
            t = float(poll_interval_s or 0)
        except (TypeError, ValueError):
            t = 0.0
        if t < 0:
            t = 0.0
        return t

    @classmethod
    def no_integration_from_params(cls, params) -> bool:
        return cls._read_poll_param(params, cls.NO_INTEGRATION_PARAM_INDEX, 0.0) >= 0.5

    def _effective_integration_s(self) -> float:
        if getattr(self, 'no_integration', False):
            return 0.0
        return self.effective_integration_s(
            0,
            getattr(self, 'poll_interval_s', self.POLL_INTERVAL_DEFAULT_S),
        )

    def _configure_poll_power_meter_integration(self):
        timer_s = self._effective_integration_s()
        for pm, use_poll_timer in (
            (self.power_meter_source, True),
            (self.power_meter_load, False),
            (self.power_meter_load_2, False),
        ):
            if pm is None:
                continue
            t = timer_s if use_poll_timer else 0
            if not use_poll_timer and getattr(pm, 'integration_disabled', lambda: False)():
                t = 0
            pm.integration_settings(mode="NORMAL", timer_s=t)

    @classmethod
    def fan_cooling_enabled_from_params(cls, params) -> bool:
        raw = cls._read_poll_param(params, cls.FAN_COOLING_PARAM_INDEX, 0.0)
        return raw >= 0.5

    def _hmp_for_fan_cooling(self):
        eq = self.equipment
        if hasattr(eq, 'prefer_hmp_as_aux'):
            eq.prefer_hmp_as_aux()
        aux = getattr(eq, 'dc_source_aux', None)
        if aux is not None and aux.is_hmp_series():
            return aux
        primary = getattr(eq, 'dc_source', None)
        input_supply = getattr(self, 'input_supply', None)
        for dc in getattr(eq, 'dc_sources', []) or []:
            if dc is None or not dc.is_hmp_series():
                continue
            if dc is input_supply or dc is primary:
                continue
            return dc
        return None

    def _apply_hmp_fan_cooling_preflight(self):
        """Before test loop: fan ON when enabled, else ensure HMP CH2 is OFF."""
        self._fan_cooling_active = False
        hmp = self._hmp_for_fan_cooling()
        ch = self.HMP_FAN_CHANNEL
        if self.enable_fan_cooling:
            if hmp is None:
                raise TestFailed(
                    "Enable Fan Cooling is checked but no HMP aux DC is assigned "
                    "(Equipment Setup → Aux DC → HMP2030)."
                )
            v, a = self.FAN_COOLING_VOLTAGE_V, self.FAN_COOLING_CURRENT_A
            self.update_status_log(
                f"HMP CH{ch} fan cooling: {v:g} V, {a:g} A limit, output ON",
                upcoming="Prepare test",
            )
            hmp.channel_set_voltage(ch, v)
            hmp.channel_set_current_limit(ch, a)
            hmp.channel_turn_on(ch)
            self._fan_cooling_active = True
            print(
                f"[POLL] Fan cooling ON — {getattr(hmp, 'description', hmp)} "
                f"CH{ch} {v:g} V / {a:g} A"
            )
        elif hmp is not None:
            hmp.channel_turn_off(ch)
            print(f"[POLL] Fan cooling disabled — HMP CH{ch} output OFF")

    def _shutdown_hmp_fan_cooling(self):
        hmp = self._hmp_for_fan_cooling()
        if hmp is None:
            return
        ch = self.HMP_FAN_CHANNEL
        hmp.channel_turn_off(ch)
        self._fan_cooling_active = False
        print(f"[POLL] Fan cooling OFF — HMP CH{ch} output OFF")

    def run(self):
        try:
            super().run()
        finally:
            if getattr(self, '_fan_cooling_active', False):
                self._shutdown_hmp_fan_cooling()

    def setup_equipment(self):
        super().setup_equipment()
        self._apply_hmp_fan_cooling_preflight()
        self._configure_poll_power_meter_integration()
        eff = self._effective_integration_s()
        if eff > 0:
            print(
                f"[POLL] Pin integration per sample: {eff:g} s "
                f"(I2C param {self.POLL_INTERVAL_PARAM_INDEX})"
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
        self.no_integration = self.no_integration_from_params(params)
        self.poll_samples_n = self.read_samples_per_point(params, self.poll_interval_s)
        self.poll_sample_index = 1
        self.poll_elapsed_s = 0.0
        self.poll_point_start_dt = None
        self.poll_point_end_dt = None
        self.poll_row_sampled_dt = None
        self.poll_integ_start_dt = None
        self.poll_integ_end_dt = None
        self.poll_prev_sampled_dt = None
        self._poll_repeat_read_duration_s = self.POLL_READ_DURATION_GUESS_S
        self.enable_fan_cooling = self.fan_cooling_enabled_from_params(params)
        self._fan_cooling_active = False

    def build_detailed_output_basename(self) -> str:
        return (
            f"{self.OUTPUT_PREFIX} {self._line_vin_filename_part()} {self.vout_V:g}V "
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
        integ_start = self.poll_integ_start_dt
        integ_end = self.poll_integ_end_dt
        if getattr(self, 'no_integration', False):
            # No integration: integration start/end columns carry the sample time
            integ_start = integ_end = self.poll_row_sampled_dt
        return row + [
            int(self.poll_sample_index),
            round(float(self.poll_elapsed_s), 2),
            self.poll_point_start_dt,
            self.poll_point_end_dt,
            self.poll_row_sampled_dt,
            integ_start,
            integ_end,
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
        if header in (
            'Time Start',
            'Time End',
            'Time Sampled',
            'Time Integration Start',
            'Time Integration End',
        ):
            return SteadyStatePollWaveformTest_2Port.POLL_DATETIME_EXCEL_FMT
        return EfficiencyWaveformTest_2Port._excel_num_format_for_header(header)

    def _write_run_metadata_rows(self, ws):
        super()._write_run_metadata_rows(ws)
        no_integ = getattr(self, 'no_integration', False)
        rows = (
            (2, "Time interval per sample (s)" if no_integ
             else "Pin integration per sample (s)", self.poll_interval_s),
            (3, "Samples per load point", self._sample_count()),
            (4, "Pin integration (s)", "Off" if no_integ
             else self._effective_integration_s()),
            (5, "Est. poll window (s)", round(self._estimated_poll_point_duration_s(), 1)),
            (6, "Fan cooling (HMP CH2)", "Yes" if self.enable_fan_cooling else "No"),
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
        """One scope PNG per poll sample; linking is 1:1 (no n_samples blob on first capture)."""
        return

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
        """Idle wait after previous Time Sampled before the next integration starts."""
        if self.poll_prev_sampled_dt is None:
            return
        gap = max(0.0, float(interval_s))
        if gap <= 0:
            return
        target_start = (
            self.poll_prev_sampled_dt + datetime.timedelta(seconds=gap)
        )
        while datetime.datetime.now() < target_start:
            self._raise_if_abort(records_before, rows_at_start)
            remaining = (target_start - datetime.datetime.now()).total_seconds()
            self._wait_or_stop(min(0.25, max(remaining, 0.0)),
                               records_before, rows_at_start)

    def prepare_source_power_meter_for_poll_input(self):
        """Once per load point: set source timer from Pin integration per sample (param 10)."""
        pm = self.power_meter_source
        if pm is not None and hasattr(pm, '_stop_and_reset_integration'):
            pm._stop_and_reset_integration()
        self.ensure_source_power_meter_auto_range(settle_s=0)
        if pm is None:
            return
        integ = self._effective_integration_s()
        if integ >= 1.0:
            sec = max(1, int(round(integ)))
            pm.integration_settings(mode='NORMAL', timer_s=sec, reset=True)
            try:
                pm.enable_averaging(False)
            except Exception:
                pass
        else:
            try:
                pm.integration_settings(mode='NORMAL', timer_s=0, reset=True)
            except Exception:
                pass
            try:
                pm.enable_averaging(True)
            except Exception:
                pass

    TIMING_DIAG_CSV = False  # write <workbook>_timing.csv with per-sample timing diagnostics
    TIMING_DIAG_FIELDS = (
        "sample", "vin_V", "i1_A", "i2_A", "acquisition_time", "spacing_s", "target_interval_s",
        "idle_wait_s", "behind_s", "pre_acq_s", "meter_read_s", "capture_total_s",
        "trigger_read_s", "run_single_s", "acq_wait_s", "stop_s", "measure_cursors_s",
        "screenshot_s", "run_s", "stop_opc_probe_s", "channel_meas_s", "cursor_read_s",
        "cursor_items", "cursor_repeat_probe_s", "row_record_s")

    def _timing_diag_path(self):
        base = getattr(self, 'data_file_path', None)
        if not base:
            return None
        return os.path.splitext(base)[0] + "_timing.csv"

    def _write_timing_diag_row(self, vin_set, i1_A, i2_A, sampled_dt, t_int,
                               capture_total_s=0.0, row_record_s=0.0):
        """Append one per-sample timing row (seconds) to <workbook>_timing.csv."""
        path = self._timing_diag_path()
        if not path:
            return
        steps = getattr(self, '_last_capture_steps', None) or {}
        meas = getattr(self, '_diag_meas', None) or {}
        prev = getattr(self, '_diag_prev_acq', None)
        spacing = (sampled_dt - prev).total_seconds() if prev is not None else ""
        self._diag_prev_acq = sampled_dt

        def r(v):
            return round(v, 3) if isinstance(v, (int, float)) else (v if v is not None else "")
        rec = {
            "sample": self.poll_sample_index, "vin_V": vin_set, "i1_A": i1_A, "i2_A": i2_A,
            "acquisition_time": sampled_dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            "spacing_s": r(spacing), "target_interval_s": t_int,
            "idle_wait_s": r(getattr(self, '_diag_idle_wait_s', "")),
            "behind_s": r(getattr(self, '_diag_behind_s', "")),
            "pre_acq_s": r(getattr(self, '_poll_pre_acq_s', "")),
            "meter_read_s": r(getattr(self, '_diag_meter_read_s', "")),
            "capture_total_s": r(capture_total_s),
            "row_record_s": r(row_record_s),
        }
        for key in ("trigger_read_s", "run_single_s", "acq_wait_s", "stop_s",
                    "measure_cursors_s", "screenshot_s", "run_s"):
            rec[key] = r(steps.get(key, ""))
        for key in ("stop_opc_probe_s", "channel_meas_s", "cursor_read_s",
                    "cursor_items", "cursor_repeat_probe_s"):
            rec[key] = r(meas.get(key, ""))
        self._diag_idle_wait_s = ""
        self._diag_behind_s = ""
        try:
            import csv
            new_file = not os.path.exists(path)
            with open(path, "a", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=self.TIMING_DIAG_FIELDS)
                if new_file:
                    w.writeheader()
                w.writerow(rec)
        except Exception as exc:
            print(f"[Warning] Could not write timing diagnostics CSV: {exc}")

    @staticmethod
    def scheduled_wait_s(now, prev_acq, interval_s, pre_s):
        """(idle wait s, seconds behind schedule) so the next acquisition lands at
        prev_acq + interval, given pre_s of work (meters + trigger) before it."""
        target = prev_acq + datetime.timedelta(seconds=float(interval_s))
        start_at = target - datetime.timedelta(seconds=float(pre_s))
        wait = max(0.0, (start_at - now).total_seconds())
        behind = max(0.0, (now + datetime.timedelta(seconds=float(pre_s)) - target).total_seconds())
        return wait, behind

    def _scheduled_poll_wait(self, interval_s, n, records_before, rows_at_start):
        prev = getattr(self, '_poll_last_acq_dt', None)
        if prev is None:
            self._wait_or_stop(interval_s, records_before, rows_at_start)
            return
        pre = getattr(self, '_poll_pre_acq_s', None)
        if pre is None:
            pre = self.PRE_ACQ_GUESS_S
        wait, behind = self.scheduled_wait_s(datetime.datetime.now(), prev, interval_s, pre)
        self._diag_idle_wait_s = wait
        self._diag_behind_s = behind
        if behind > 0.5:
            print(f"[WARNING] Poll sample {self.poll_sample_index}: behind schedule by "
                  f"{behind:.1f} s (interval {interval_s:g} s is shorter than the work per sample)")
        self.update_status_log(
            f"Poll sample {self.poll_sample_index}/{n}: idle {wait:.1f} s "
            f"(acquisition every {interval_s:g} s)",
            upcoming="Read meters")
        print(f"[TIMING] scheduled idle wait {wait:.1f} s (pre-acquisition work ~{pre:.1f} s)")
        # Deadline-based wait (no drift from summing many short sleeps)
        deadline = datetime.datetime.now() + datetime.timedelta(seconds=wait)
        while True:
            self._raise_if_abort(records_before, rows_at_start)
            remaining = (deadline - datetime.datetime.now()).total_seconds()
            if remaining <= 0:
                break
            sleep(min(0.25, remaining))

    def _poll_per_sample_overhead_s(self) -> float:
        return max(
            float(getattr(self, '_poll_repeat_read_duration_s', self.POLL_READ_DURATION_GUESS_S)),
            self.POLL_READ_DURATION_GUESS_S,
        ) + self.POLL_SCOPE_CAPTURE_GUESS_S

    def _estimated_poll_point_duration_s(self) -> float:
        return self.estimate_point_duration_s(
            self.poll_interval_s,
            self._sample_count(),
            getattr(self, 'no_integration', False),
            read_s=getattr(self, '_poll_repeat_read_duration_s', None),
        )

    @classmethod
    def estimate_point_duration_s(cls, interval_s, samples_n, no_integration=False,
                                  read_s=None) -> float:
        """Estimated seconds per load point (also used by the Add Test GUI)."""
        try:
            n = int(samples_n)
            interval = max(float(interval_s or 0), 0.0)
        except (TypeError, ValueError):
            return 0.0
        if n <= 0:
            return 0.0
        integ = 0.0 if no_integration else interval
        read = max(float(read_s or 0), cls.POLL_READ_DURATION_GUESS_S)
        if no_integration and cls.SCHEDULED_INTERVAL:
            # Interval = time between acquisitions; never shorter than the work per sample
            overhead = read + cls.POLL_SCOPE_CAPTURE_GUESS_S
            return overhead + max(n - 1, 0) * max(interval, overhead)
        total = n * (integ + read + cls.POLL_SCOPE_CAPTURE_GUESS_S)
        if no_integration:
            # idle gap between samples (not before the first)
            total += max(n - 1, 0) * interval
        return total

    def _integrate_source_pin_before_read(self, records_before, rows_at_start):
        """Integrate Pin for T_int before meter read; honors Stop in 0.25 s slices."""
        self.poll_integ_start_dt = None
        self.poll_integ_end_dt = None
        integ = self._effective_integration_s()
        if integ < 1.0:
            return
        pm = self.power_meter_source
        if pm is None:
            return
        self._raise_if_abort(records_before, rows_at_start)
        self.poll_integ_start_dt = datetime.datetime.now()
        pm.start_integration()
        deadline = time.time() + float(integ)
        pmo = getattr(pm, 'power_meter_object', None)
        while time.time() < deadline:
            self._raise_if_abort(records_before, rows_at_start)
            if pmo is not None and hasattr(pmo, 'check_integration_status'):
                try:
                    pmo.check_integration_status()
                except Exception:
                    pass
                if getattr(pmo, '_integration_done', False):
                    self.poll_integ_end_dt = datetime.datetime.now()
                    return
            remaining = deadline - time.time()
            if remaining <= 0:
                break
            sleep(min(0.25, remaining))
        self.poll_integ_end_dt = datetime.datetime.now()

    def _measure_poll_readings(self, i2_A):
        """PM reads for poll samples without re-sending AUTO range every tick."""
        pin_done = self._effective_integration_s() >= 1.0
        self.test_data.gather_data(
            coupling=self.coupling,
            usb_pd=self.usbpd_test,
            stable_source_pin=True,
            source_pin_integration_done=pin_done,
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
        return self._estimated_poll_point_duration_s()

    def _append_measurement_row(self, scope_row):
        super()._append_measurement_row(scope_row)
        t_end = time.perf_counter()
        t_cap = getattr(self, '_timing_last_capture_end', None)
        if t_cap is not None:
            print(f"[TIMING] sample {getattr(self, 'poll_sample_index', '?')}: "
                  f"after capture -> row recorded (dataframe + log + UI update) "
                  f"{t_end - t_cap:.3f} s")
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
        t_int = float(self.poll_interval_s or 0)
        records_before = len(self.captured_records)
        rows_at_start = len(self.output_dataframe)
        self.poll_prev_sampled_dt = None
        self._poll_last_acq_dt = None
        self._poll_pre_acq_s = None
        self._diag_prev_acq = None
        self._poll_repeat_read_duration_s = self.POLL_READ_DURATION_GUESS_S
        self.prepare_load_power_meters_for_poll_output()
        self.prepare_source_power_meter_for_poll_input()
        try:
            for sample in range(n):
                self._raise_if_abort(records_before, rows_at_start)
                self.poll_sample_index = sample + 1
                no_integ = getattr(self, 'no_integration', False)
                self.poll_elapsed_s = sample * t_int
                if sample == 0:
                    self.poll_point_start_dt = datetime.datetime.now()
                    self.poll_point_end_dt = (
                        self.poll_point_start_dt
                        + datetime.timedelta(seconds=self._estimated_poll_point_duration_s())
                    )
                elif no_integ and t_int > 0 and self.SCHEDULED_INTERVAL:
                    self._scheduled_poll_wait(t_int, n, records_before, rows_at_start)
                elif no_integ and t_int > 0:
                    # Idle gap after the previous sample finished (scope + Excel row)
                    self.update_status_log(
                        f"Poll sample {self.poll_sample_index}/{n}: "
                        f"waiting {t_int:g} s interval",
                        upcoming="Read meters")
                    self._wait_or_stop(t_int, records_before, rows_at_start)
                if no_integ and sample > 0 and self.poll_point_start_dt is not None:
                    self.poll_elapsed_s = (
                        datetime.datetime.now() - self.poll_point_start_dt
                    ).total_seconds()
                self._poll_sample_start_dt = datetime.datetime.now()
                self.update_status_log(
                    f"Poll sample {self.poll_sample_index}/{n} "
                    + ("(no integration, instantaneous Pin)" if no_integ
                       else f"(Pin integrate {self._effective_integration_s():g} s)"),
                    upcoming="Read meters")
                self._integrate_source_pin_before_read(
                    records_before, rows_at_start)
                read_t0 = datetime.datetime.now()
                self.update_status_log(
                    f"Poll sample {self.poll_sample_index}/{n}",
                    upcoming="Capture Waveform")
                _m0 = time.perf_counter()
                self._measure_poll_readings(i2_A)
                self._diag_meter_read_s = time.perf_counter() - _m0
                self._poll_waveform_filename_tag = f"_S{self.poll_sample_index}"
                cap_t0 = time.perf_counter()
                self._last_capture_steps = {}
                self._diag_meas = {}
                self.last_acquisition_dt = None
                scope_row = self.capture_waveform_at_point(vin_set, i1_A, i2_A)
                self._timing_last_capture_end = time.perf_counter()
                print(f"[TIMING] sample {self.poll_sample_index}/{n}: "
                      f"capture waveform took {self._timing_last_capture_end - cap_t0:.3f} s")
                read_t1 = datetime.datetime.now()
                self._poll_repeat_read_duration_s = max(
                    0.05,
                    (read_t1 - read_t0).total_seconds(),
                )
                sampled_dt = datetime.datetime.now()
                if no_integ:
                    # Time Sampled = moment the scope acquired the waveform (not end of capture)
                    sampled_dt = getattr(self, 'last_acquisition_dt', None) or sampled_dt
                    if sample == 0 or getattr(self, '_poll_first_acq_dt', None) is None:
                        self._poll_first_acq_dt = sampled_dt
                    self.poll_elapsed_s = (sampled_dt - self._poll_first_acq_dt).total_seconds()
                    if self.SCHEDULED_INTERVAL:
                        prev_acq = getattr(self, '_poll_last_acq_dt', None)
                        if prev_acq is not None:
                            print(f"[TIMING] acquisition spacing "
                                  f"{(sampled_dt - prev_acq).total_seconds():.2f} s "
                                  f"(target {t_int:g} s)")
                        self._poll_last_acq_dt = sampled_dt
                        start = getattr(self, '_poll_sample_start_dt', None)
                        if start is not None:
                            self._poll_pre_acq_s = max(0.0, (sampled_dt - start).total_seconds())
                if len(scope_row) > 1 and scope_row[1] == "N/A":
                    self.poll_row_sampled_dt = sampled_dt
                    self._append_measurement_row(scope_row)
                    if 'NO TRIGGER' in str(scope_row[0]):
                        continue  # missed trigger: keep polling the remaining samples
                    return
                self.poll_row_sampled_dt = sampled_dt
                _r0 = time.perf_counter()
                self._append_measurement_row(scope_row)
                if self.TIMING_DIAG_CSV:
                    self._write_timing_diag_row(
                        vin_set, i1_A, i2_A, sampled_dt, t_int,
                        capture_total_s=self._timing_last_capture_end - cap_t0,
                        row_record_s=time.perf_counter() - _r0)
        except (TestStopped, TestSkipped):
            self._note_partial_capture(records_before, rows_at_start)
            raise

    def _export_line_block(self):
        t0 = time.perf_counter()
        t_cap = getattr(self, '_timing_last_capture_end', None)
        try:
            return super()._export_line_block()
        finally:
            t1 = time.perf_counter()
            msg = f"[TIMING] Excel export of Vin block (rows -> workbook) took {t1 - t0:.3f} s"
            if t_cap is not None:
                msg += f"; last capture -> Excel written {t1 - t_cap:.3f} s"
            print(msg)

    def embed_waveforms_in_excel(self):
        t0 = time.perf_counter()
        try:
            return super().embed_waveforms_in_excel()
        finally:
            print(f"[TIMING] Embedding {len(getattr(self, 'captured_records', []) or [])} "
                  f"waveform images in Excel took {time.perf_counter() - t0:.3f} s")

    def _link_capture_main_sheet_rows(self):
        """One embedded PNG per poll sample → one main sheet row per capture record."""
        super()._link_capture_main_sheet_rows()

    def update_test_list_text(self):
        super().update_test_list_text()
        fan = (
            f"HMP CH{self.HMP_FAN_CHANNEL} fan {self.FAN_COOLING_VOLTAGE_V:g} V / "
            f"{self.FAN_COOLING_CURRENT_A:g} A."
            if self.enable_fan_cooling
            else ""
        )
        if getattr(self, 'no_integration', False) and self.SCHEDULED_INTERVAL:
            timing = (
                f"{self.poll_interval_s:g} s between scope acquisitions, no Pin integration "
                f"(read, scope, row, idle). ")
        elif getattr(self, 'no_integration', False):
            timing = (
                f"{self.poll_interval_s:g} s time interval per sample, no Pin integration "
                f"(read, scope, row, wait). ")
        else:
            timing = (
                f"{self.poll_interval_s:g} s Pin integration per sample "
                f"(integrate, read, scope, row). ")
        note = (
            f"Poll: {self._sample_count()} samples/load point, "
            f"{timing}"
            f"{fan} "
            "Stop keeps rows already saved to Excel."
        ).replace("  ", " ")
        if note not in self.test_list_text:
            self.test_list_text += "\n" + note


SteadyStatePollWaveformTest_2Port.tc_default = SteadyStatePollWaveformTest_2Port._build_tc_default()
