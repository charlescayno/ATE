"""Rdson Measurements: steady-state poll waveform 2 port + RTO6 cursor results 1-4.

Same flow as Steady-State Poll Waveform 2 Port (integrate Pin -> meters -> scope
capture -> Excel row, repeated N samples per load point). In addition, every
sample records the RTO6 Cursor 1..4 results (Y1, Y2, dX, dY) and computes RDS(on).

Cursor assignment (operator sets these up on the scope; the test only reads them):
    Cursor 1 = Sampled VDS voltage #1      Cursor 2 = Sampled IDS current #1
    Cursor 3 = Sampled VDS voltage #2      Cursor 4 = Sampled IDS current #2
Pair #1 = Cursor 1 + 2, Pair #2 = Cursor 3 + 4.

    Rds1 = Cursor1.Y1 / Cursor2.Y1
    Rds2 = Cursor1.Y2 / Cursor2.Y2
    Rds3 = Cursor3.Y1 / Cursor4.Y1
    Rds4 = Cursor3.Y2 / Cursor4.Y2
    Rds_avg = (Rds1 + Rds2 + Rds3 + Rds4) / 4      (ohms: V / A)
"""
from copy import deepcopy

from psu_tests.test_steady_state_poll_2port_waveform import SteadyStatePollWaveformTest_2Port


class RdsonMeasurementTest_2Port(SteadyStatePollWaveformTest_2Port):
    title = "Rdson Measurements"
    short_title = "RDSON_2P"
    PNG_SUFFIX = "_RDSON"
    OUTPUT_PREFIX = "RDSON"

    # Fast capture: scope setup is applied once at test start (not per sample),
    # and the post-single wait polls for acquisition done instead of sleeping 1 s.
    reapply_scope_before_capture = False
    POLL_SCOPE_CAPTURE_GUESS_S = 1.0
    SCHEDULED_INTERVAL = True  # interval = time between acquisitions (no integration)
    TIMING_DIAG_CSV = True     # per-sample timing CSV next to the workbook (<name>_timing.csv)
    ACQ_WAIT_MAX_S = 5.0  # max wait for the single-shot trigger

    def _wait_for_single_acquisition(self):
        """Block on *OPC? until the single acquisition completes (max ACQ_WAIT_MAX_S).

        Returns immediately when the scope is simulated (no VISA device). On timeout
        (no trigger) a warning is printed and capture continues, so the sample is
        flagged in the log rather than silently stale. Stop/Skip is honored afterwards.
        """
        from time import monotonic
        device = getattr(self.oscilloscope, 'device', None)
        query = getattr(device, 'query', None)
        if query is None:
            return
        t0 = monotonic()
        old_timeout = getattr(device, 'timeout', None)
        status = "done"
        try:
            device.timeout = int(self.ACQ_WAIT_MAX_S * 1000)
            query('*OPC?')
        except Exception as exc:
            status = f"TIMEOUT/ERROR ({exc.__class__.__name__}) - no trigger? capture may be stale"
        finally:
            if old_timeout is not None:
                try:
                    device.timeout = old_timeout
                except Exception:
                    pass
        print(f"[TIMING] acquisition wait {monotonic() - t0:.3f} s ({status})")

    CURSOR_SETS = (1, 2, 3, 4)
    # (column suffix, key returned by oscilloscope.get_cursor)
    CURSOR_FIELDS = (
        ("Y1", "y1 position"),
        ("Y2", "y2 position"),
        ("dX", "delta x"),
        ("dY", "delta y"),
    )
    # (column label, (vds cursor, vds field), (ids cursor, ids field))
    RDS_TERMS = (
        ("Rds1 (ohm)", (1, "Y1"), (2, "Y1")),
        ("Rds2 (ohm)", (1, "Y2"), (2, "Y2")),
        ("Rds3 (ohm)", (3, "Y1"), (4, "Y1")),
        ("Rds4 (ohm)", (3, "Y2"), (4, "Y2")),
    )
    RDS_AVG_LABEL = "Rds_avg (ohm)"

    POLL_DEFAULT_SCOPE_CHANNELS = {
        1: {'enabled': True, 'name': 'VDS', 'measurements': ['MAXimum'],
            'derating': 1700.0, 'cursor': {'enabled': False, 'type': 'VERTical'}},
        2: {'enabled': True, 'name': 'IDS', 'measurements': ['MAXimum'],
            'derating': None, 'cursor': {'enabled': False, 'type': 'VERTical'}},
        3: {'enabled': False, 'name': '', 'measurements': [], 'derating': None, 'cursor': {}},
        4: {'enabled': False, 'name': '', 'measurements': [], 'derating': None, 'cursor': {}},
    }

    tc_default = None

    CURSOR_NOTE = (
        "Cursor Assignment Required for RDS(on) Measurement: "
        "Cursor 1 = Sampled VDS Voltage #1, Cursor 2 = Sampled IDS Current #1, "
        "Cursor 3 = Sampled VDS Voltage #2, Cursor 4 = Sampled IDS Current #2 "
        "(Pair #1 = Cursor 1+2, Pair #2 = Cursor 3+4). "
        "Rds1 = C1.Y1/C2.Y1, Rds2 = C1.Y2/C2.Y2, Rds3 = C3.Y1/C4.Y1, Rds4 = C3.Y2/C4.Y2, "
        "Rds_avg = (Rds1+Rds2+Rds3+Rds4)/4. "
        "Place the cursors at valid VDS and IDS sampling points within the conduction interval; "
        "incorrect assignment or placement gives inaccurate RDS(on). "
        "Cursors that are off record N/A."
    )

    @classmethod
    def cursor_column_labels(cls) -> list:
        cols = [
            f"Cursor Result {n} {suffix}"
            for n in cls.CURSOR_SETS
            for suffix, _ in cls.CURSOR_FIELDS
        ]
        cols += [label for label, _, _ in cls.RDS_TERMS]
        cols.append(cls.RDS_AVG_LABEL)
        return cols

    # Minimum time interval per sample (s): scope capture + meters take ~1.4 s on a direct
    # LAN (HiSLIP), ~25 s on a slow routed network. Warn only; the value is not enforced.
    MIN_INTERVAL_S = 5.0

    @classmethod
    def interval_warning(cls, interval_s, no_integration=True):
        """Warning text when the interval is below the recommended minimum, else ''."""
        if not no_integration:
            return ""
        try:
            interval_s = float(interval_s)
        except (TypeError, ValueError):
            return ""
        if interval_s < cls.MIN_INTERVAL_S:
            return (f"Time interval per sample {interval_s:g} s is below the recommended "
                    f"minimum of {cls.MIN_INTERVAL_S:g} s (scope capture + meter read take "
                    f"~1.4 s on a direct LAN, more on slow networks). Samples may be spaced further apart than set.")
        return ""

    def setup_equipment(self):
        super().setup_equipment()
        warn = self.interval_warning(getattr(self, 'poll_interval_s', None),
                                     getattr(self, 'no_integration', False))
        if warn:
            print(f"[WARNING] {warn}")
            try:
                self.update_status_log(warn, upcoming="Prepare test")
            except Exception:
                pass
        print(f"[RDSON] {self.CURSOR_NOTE}")
        try:
            self.update_status_log(
                "Reminder: assign cursors 1-4 (C1 VDS#1, C2 IDS#1, C3 VDS#2, C4 IDS#2)",
                upcoming="Prepare test")
        except Exception:
            pass

    def update_test_list_text(self):
        super().update_test_list_text()
        if self.CURSOR_NOTE not in self.test_list_text:
            self.test_list_text += "\n" + self.CURSOR_NOTE

    def define_scope_header(self):
        super().define_scope_header()
        labels = list(self.scope_measurement_labels)
        for col in self.cursor_column_labels():
            if col not in labels:
                labels.append(col)
        self.scope_measurement_labels = labels
        scope_cols = ['Trig Ch', 'Trig Level (V)'] + labels
        if not getattr(self, 'embed_images', True):
            scope_cols.append('Waveform File')
        return scope_cols

    @staticmethod
    def _to_float(raw):
        try:
            return float(str(raw).strip())
        except (TypeError, ValueError):
            return None

    @classmethod
    def compute_rds(cls, raw: dict) -> dict:
        """raw: {(cursor_n, field): float|None}. Returns Rds1..4 and Rds_avg (None -> 'N/A')."""
        out = {}
        vals = []
        for label, (vc, vf), (ic, i_f) in cls.RDS_TERMS:
            v = raw.get((vc, vf))
            i = raw.get((ic, i_f))
            if v is None or i is None or abs(i) < 1e-12:
                out[label] = "N/A"
                vals.append(None)
            else:
                r = v / i
                out[label] = round(r, 6)
                vals.append(r)
        if all(x is not None for x in vals):
            out[cls.RDS_AVG_LABEL] = round(sum(vals) / len(vals), 6)
        else:
            out[cls.RDS_AVG_LABEL] = "N/A"
        return out

    def _read_cursor_batch(self):
        """Batched cursor read. After the first sample only Y1P/Y2P are read (8 items);
        on/off state and dX are cached from the first sample and dY = Y2 - Y1 is computed
        locally. Bench CSV showed ~0.35 s per SCPI query and 11-16 s for the cursor step:
        the real scope class (RohdeSchwarzOscilloscope in equipment/oscilloscope_specs.py)
        had no get_cursors_fast, so the 32-query per-field fallback ran. Per-sample numbers
        go to <workbook>_timing.csv."""
        from time import perf_counter
        scope = self.oscilloscope
        static = getattr(self, '_cursor_static', None)
        t0 = perf_counter()
        try:
            return self._read_cursor_batch_inner(scope, static)
        finally:
            self._diag_cursor_read_s = perf_counter() - t0

    def _read_cursor_batch_inner(self, scope, static):
        if static is None:
            self._diag_cursor_items = len(self.CURSOR_SETS) * 5
            full = scope.get_cursors_fast(self.CURSOR_SETS)
            self._cursor_static = {
                n: (None if rec is None else {"delta x": rec.get("delta x")})
                for n, rec in full.items()}
            return full
        on = [n for n in self.CURSOR_SETS if static.get(n) is not None]
        self._diag_cursor_items = len(on) * 2
        quick = scope.get_cursors_fast(on, fields=("y1 position", "y2 position")) if on else {}
        out = {}
        for n in self.CURSOR_SETS:
            rec = quick.get(n)
            if static.get(n) is None or rec is None:
                out[n] = None
                continue
            rec = dict(rec)
            rec["delta x"] = static[n]["delta x"]
            y1, y2 = self._to_float(rec.get("y1 position")), self._to_float(rec.get("y2 position"))
            rec["delta y"] = (y2 - y1) if (y1 is not None and y2 is not None) else None
            out[n] = rec
        return out

    def query_cursor_results(self) -> dict:
        """Read Cursor 1..4 from the scope and compute Rds; unavailable values are 'N/A'."""
        out = {}
        raw = {}
        batch = None
        if hasattr(self.oscilloscope, 'get_cursors_fast') and not getattr(self, '_cursor_batch_failed', False):
            try:
                batch = self._read_cursor_batch()
            except Exception as exc:
                self._cursor_batch_failed = True
                print(f"[Warning] Batched cursor query failed, using per-field queries: {exc}")
        for n in self.CURSOR_SETS:
            cur = None
            if batch is not None:
                cur = batch.get(n)
            else:
                try:
                    cur = self.oscilloscope.get_cursor(cursor=n)
                except Exception as exc:
                    print(f"[Warning] Cursor Result {n} query: {exc}")
            for suffix, key in self.CURSOR_FIELDS:
                val = self._to_float((cur or {}).get(key))
                raw[(n, suffix)] = val
                out[f"Cursor Result {n} {suffix}"] = round(val, 6) if val is not None else "N/A"
        out.update(self.compute_rds(raw))
        return out

    def _get_scope_measure_items(self):
        """Query only enabled channels (not all 8); ARN ON is sent once."""
        scope = self.oscilloscope
        items = []
        raw_ok = hasattr(scope, 'write') and not getattr(self, '_meas_fast_failed', False)
        for ch, data in sorted(self.scope_channels.items()):
            if not data.get('enabled'):
                continue
            labels = values = None
            try:
                if raw_ok:
                    from time import perf_counter
                    ta = perf_counter()
                    if not getattr(self, '_arn_set', False):
                        scope.write(f'MEAS{ch}:ARN ON')
                    tb = perf_counter()
                    reply = scope.write(f'MEAS{ch}:ARES?')
                    print(f"[TIMING] MEAS{ch}: ARN ON {tb - ta:.2f} s | ARES? {perf_counter() - tb:.2f} s")
                    labels, values = [], []
                    for part in str(reply).split(','):
                        lbl, val = part.split(':')
                        labels.append(lbl.strip())
                        values.append(float(val.strip()))
                else:
                    labels, values = scope.get_measure(ch)
            except Exception as exc:
                if raw_ok:
                    self._meas_fast_failed = True
                    print(f"[Warning] Fast measurement query failed, using get_measure: {exc}")
                try:
                    labels, values = scope.get_measure(ch)
                except Exception:
                    labels = values = None
            items.append({"channel": ch, "labels": labels, "values": values})
        if raw_ok:
            self._arn_set = True
        return items

    def query_active_scope_measurements(self) -> dict:
        from time import perf_counter
        diag = getattr(self, '_diag_meas', None)
        if diag is None:
            diag = self._diag_meas = {}
        scope = self.oscilloscope
        # Probe: does the scope still look busy right after STOP? (*OPC? round trip)
        if self.TIMING_DIAG_CSV and hasattr(scope, 'write'):
            tp = perf_counter()
            try:
                scope.write('*OPC?')
            except Exception:
                pass
            diag["stop_opc_probe_s"] = perf_counter() - tp
        t0 = perf_counter()
        meas = super().query_active_scope_measurements()
        t1 = perf_counter()
        meas.update(self.query_cursor_results())
        t2 = perf_counter()
        diag["channel_meas_s"] = t1 - t0
        diag["cursor_read_s"] = getattr(self, '_diag_cursor_read_s', t2 - t1)
        diag["cursor_items"] = getattr(self, '_diag_cursor_items', "")
        # Probe: repeat one cursor query right after the batch. If this is fast, the
        # first cursor query pays the cost (scope recalculation), not each item.
        if self.TIMING_DIAG_CSV and hasattr(scope, 'write'):
            tp = perf_counter()
            try:
                scope.write('CURS1:Y1P?')
            except Exception:
                pass
            diag["cursor_repeat_probe_s"] = perf_counter() - tp
        print(f"[TIMING] measure detail: channel measurements {t1 - t0:.2f} s "
              f"| cursors+Rds {t2 - t1:.2f} s")
        return meas

    @classmethod
    def _build_rdson_tc_default(cls):
        """Defaults taken from the bench test plan 'ATE_test_plan_without fan.json'."""
        from psu_tests.definitions import (
            TestConditions, LineRange, LoadSettings, SoaktimeSettings,
            GeneralOptions, USBPDOptions, LineRamp, I2CTestParameters)
        # Param indices: 0-2 Vout2 / Iout2 / Fixed Aux, 3-9 hidden advanced
        # (trigger delta, settle, discharge pulses, ambient, post-capture, trigger ch),
        # 10 = time interval per sample, 11 = samples per load point,
        # 12 = fan cooling (off), 13 = no integration (on)
        params = [20.0, 0.1, 0.1, 0.0, 1.0, 1.0, 2.0, 25.0, 1.0, 1.0,
                  30.0, 30.0, 0.0, 1.0]
        return TestConditions(
            name=cls.title,
            nominal_output_voltage_V=48.0,
            nominal_load_current_A=2.0,
            max_load_current_A=2.0,
            line_range=LineRange(name="Custom", vin_freq=[[860.0, 50.0]], custom=False),
            load_range=LoadSettings.LOAD_SINGLE_VALUE_100_PCT,
            soak_time=SoaktimeSettings.TST_326,
            general_options=GeneralOptions(
                measure_ripple=False,
                use_eload_data=False,
                eload_type='CC',
                load_direction='Downward',
                coupling='DC',
            ),
            usbpd_options=USBPDOptions(),
            line_ramp_settings=LineRamp(),
            i2c_test_parameters=I2CTestParameters(
                params=params,
                cbx_params=[
                    "Option C: Fixed Aux / Swept Main (Port 2 Fixed Load)",
                    "Yes",
                    "None (Fully Automated)",
                    "No",
                ]),
            unit_id="00",
            ambient_temp=25.0,
            scope_channels=deepcopy(cls.POLL_DEFAULT_SCOPE_CHANNELS),
        )


RdsonMeasurementTest_2Port.tc_default = RdsonMeasurementTest_2Port._build_rdson_tc_default()
