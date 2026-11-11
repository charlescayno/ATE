"""Headless check for Rdson Measurements (cursor results 1-4 + Rds math)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psu_tests.definitions  # noqa: F401  (import order avoids circular import)
from psu_tests.test_rdson_measurements import RdsonMeasurementTest_2Port as T
from psu_tests.test_type import TestTypes

# cursor -> (Y1, Y2)
CURSORS = {1: (1.0, 2.0), 2: (10.0, 10.0), 3: (3.0, 4.0), 4: (10.0, 20.0)}


class FakeScope:
    def __init__(self, off=()):
        self.off = off

    def get_measure_all(self):
        return []

    def get_measure(self, ch):
        return ['MAX'], [1.0]

    def get_cursor(self, cursor=1):
        if cursor in self.off:
            return None
        y1, y2 = CURSORS[cursor]
        return {"y1 position": str(y1), "y2 position": str(y2),
                "delta x": "1e-6", "delta y": str(y2 - y1)}


class BatchScope(FakeScope):
    """Fake scope exposing write() and get_cursors_fast() like the real one."""
    def __init__(self, off=(), bad=False):
        super().__init__(off)
        self.bad = bad
        self.cursor_queries = 0
        self.field_log = []
        self.batch_calls = 0
        self.measure_queries = []
        self.arn_count = 0

    def get_cursors_fast(self, cursors=(1, 2, 3, 4), fields=None):
        self.batch_calls += 1
        if self.bad:
            raise ValueError("bad reply")
        self.cursor_queries += 1
        self.field_log.append((tuple(cursors), fields))
        out = {}
        for n in cursors:
            if fields is None and n in self.off:
                out[n] = None
                continue
            y1, y2 = CURSORS[n]
            rec = {"y1 position": str(y1), "y2 position": str(y2),
                   "delta x": "1e-6", "delta y": str(y2 - y1)}
            if fields is not None:
                rec = {k: v for k, v in rec.items() if k in fields}
            out[n] = rec
        return out

    def write(self, cmd):
        if cmd.endswith("ARN ON"):
            self.arn_count += 1
            return None
        if cmd.endswith(":ARES?"):
            self.measure_queries.append(cmd.split(":")[0])
            return "Max:1.5"
        raise AssertionError(cmd)


def make(scope):
    t = T.__new__(T)
    t.scope_channels = T.POLL_DEFAULT_SCOPE_CHANNELS
    t.embed_images = True
    t.oscilloscope = scope
    return t


def check_no_trigger():
    """No trigger: re-arm once, then N/A row flagged NO TRIGGER; stop after 3 in a row."""
    from psu_tests.definitions import TestStopped

    class Dev:
        def __init__(self, trig):
            self.trig, self.timeout, self.cleared = trig, 2000, 0

        def query(self, cmd):
            if cmd == '*OPC?' and not self.trig[0]:
                raise TimeoutError("visa timeout")
            return "1"

        def clear(self):
            self.cleared += 1

    class Scope:
        def __init__(self, trig):
            self.device, self.log = Dev(trig), []

        def run_single(self): self.log.append("single")
        def stop(self): self.log.append("stop")
        def run(self): self.log.append("run")
        def get_screenshot(self, *a): self.log.append("shot")

    def mk(trig):
        t = T.__new__(T)
        t.oscilloscope = Scope(trig)
        t.scope_measurement_labels = ["VDS Max", "IDS Max"]
        t.auto_find_trigger, t.embed_images, t.trigger_channel = False, True, 1
        t.prompt_before_capture, t.captured_records = False, []
        t.update_status_log = lambda *a, **k: None
        t._read_trigger_level = lambda: 3.76
        t.query_active_scope_measurements = lambda: {"VDS Max": 4.0, "IDS Max": 3.0}
        t.vout_V, t.vout_2_V, t.i_max_A, t.i_max_2_A = 48.0, 20.0, 2.0, 0.1
        t.waveform_filepath, t.unit_id, t.coupling = ".", "", "DC"
        t.current_ch1_lbl, t.current_ch2_lbl, t.eff_total_pct = "100%", "0.1A", 88.0
        return t

    assert T.NO_TRIGGER_RETRIES == 1 and T.NO_TRIGGER_MAX_CONSECUTIVE == 0
    trig = [False]
    t = mk(trig)
    row = t.capture_waveform_at_point(860, 2, 0.1)
    assert row == ["CH1 (NO TRIGGER)", "N/A", "N/A", "N/A"], row
    assert t.oscilloscope.log.count("single") == 2 and t.oscilloscope.log[-1] == "run"
    assert t.oscilloscope.device.cleared == 2 and t._no_trigger_streak == 1
    trig[0] = True  # trigger returns: normal row, streak reset
    row = t.capture_waveform_at_point(860, 2, 0.1)
    assert row[0] == "CH1" and row[1] == 3.76 and t._no_trigger_streak == 0, row
    trig[0] = False
    for _ in range(5):
        row = t.capture_waveform_at_point(860, 2, 0.1)
        assert row[1] == "N/A"
    assert t._no_trigger_streak == 5  # never stops; keeps polling


def main():
    check_no_trigger()
    assert T in TestTypes, "not registered"
    assert T.tc_default is not None and T.tc_default.name == "Rdson Measurements"
    tc = T.tc_default
    p = [float(x) for x in tc.i2c_test_parameters.param]
    assert (tc.nominal_output_voltage_V, tc.nominal_load_current_A, tc.max_load_current_A) == (48.0, 2.0, 2.0)
    assert tc.line_range.vin_freq == [[860.0, 50.0]] and tc.general_options.coupling == 'DC'
    assert tc.load_range.load_range_pct == [100] and tc.soak_time.name == "TST-326"
    assert p[:3] == [20.0, 0.1, 0.1] and p[10] == 30.0 and p[11] == 30.0 and p[12] == 0.0 and p[13] == 1.0
    assert tc.scope_channels[1]['derating'] == 1700.0 and tc.scope_channels[2]['name'] == 'IDS'
    assert list(tc.i2c_test_parameters.cbx_param)[2:] == ["None (Fully Automated)", "No"]
    t = make(FakeScope())
    cols = t.define_scope_header()
    for n in (1, 2, 3, 4):
        for s in ("Y1", "Y2", "dX", "dY"):
            assert f"Cursor Result {n} {s}" in cols, (n, s)
    for c in ("Rds1 (ohm)", "Rds2 (ohm)", "Rds3 (ohm)", "Rds4 (ohm)", "Rds_avg (ohm)"):
        assert c in cols, c
    meas = t.query_active_scope_measurements()
    # Rds1=1/10, Rds2=2/10, Rds3=3/10, Rds4=4/20
    assert meas["Rds1 (ohm)"] == 0.1
    assert meas["Rds2 (ohm)"] == 0.2
    assert meas["Rds3 (ohm)"] == 0.3
    assert meas["Rds4 (ohm)"] == 0.2
    assert meas["Rds_avg (ohm)"] == 0.2, meas["Rds_avg (ohm)"]
    # cursor 3 off -> Rds3/Rds4/avg N/A
    meas = make(FakeScope(off=(3,))).query_active_scope_measurements()
    assert meas["Cursor Result 3 Y1"] == "N/A"
    assert meas["Rds3 (ohm)"] == "N/A" and meas["Rds_avg (ohm)"] == "N/A"
    assert meas["Rds1 (ohm)"] == 0.1

    # batched path: same Rds as per-field path, one write for all cursors
    fast = BatchScope()
    meas = make(fast).query_active_scope_measurements()
    assert fast.cursor_queries == 1 and fast.measure_queries == ["MEAS1", "MEAS2"], (fast.cursor_queries, fast.measure_queries)
    assert meas["Rds_avg (ohm)"] == 0.2 and meas["Rds1 (ohm)"] == 0.1
    assert fast.arn_count == 2
    # cursor 3 off in batch -> N/A
    meas = make(BatchScope(off=(3,))).query_active_scope_measurements()
    assert meas["Rds3 (ohm)"] == "N/A" and meas["Rds_avg (ohm)"] == "N/A"
    # 2nd sample reads only Y1/Y2 of the cursors that were on; dY computed locally, dX cached
    fast2 = BatchScope(off=(3,))
    t2 = make(fast2)
    t2.query_active_scope_measurements()
    m2 = t2.query_active_scope_measurements()
    assert fast2.field_log[1] == ((1, 2, 4), ("y1 position", "y2 position")), fast2.field_log
    assert m2["Cursor Result 1 dY"] == 1.0 and m2["Cursor Result 1 dX"] == 1e-06
    assert m2["Cursor Result 3 Y1"] == "N/A" and m2["Rds_avg (ohm)"] == "N/A"
    assert m2["Rds1 (ohm)"] == 0.1
    # scheduled interval: idle wait = prev acquisition + interval - pre-acquisition work - now
    import datetime as _dt
    t0 = _dt.datetime(2026, 1, 1, 12, 0, 0)
    w, b = T.scheduled_wait_s(t0 + _dt.timedelta(seconds=12.75), t0, 30.0, 3.1)
    assert abs(w - 14.15) < 1e-6 and b == 0.0, (w, b)
    w, b = T.scheduled_wait_s(t0 + _dt.timedelta(seconds=28.0), t0, 30.0, 3.1)
    assert w == 0.0 and abs(b - 1.1) < 1e-6, (w, b)
    assert T.SCHEDULED_INTERVAL is True
    # estimate: interval is between acquisitions, never shorter than the work per sample
    overhead = T.POLL_READ_DURATION_GUESS_S + T.POLL_SCOPE_CAPTURE_GUESS_S
    assert abs(T.estimate_point_duration_s(30, 4, True) - (overhead + 3 * 30)) < 1e-6
    assert abs(T.estimate_point_duration_s(1, 4, True) - (overhead + 3 * overhead)) < 1e-6
    # the REAL scope class (RohdeSchwarzOscilloscope) must provide get_cursors_fast
    from equipment.oscilloscope_specs import RohdeSchwarzOscilloscope as RTO
    assert hasattr(RTO, 'get_cursors_fast')
    rto = RTO.__new__(RTO)
    sent = []

    def fake_write(cmd):
        sent.append(cmd)
        assert cmd.count("?") == cmd.count(";:") + 1  # one message, all queries
        vals = []
        for q in cmd.split(";:"):
            n = int(q.split(":")[0].replace("CURS", ""))
            f = q.split(":")[1].rstrip("?")
            vals.append({"STAT": "0" if n == 3 else "1", "Y1P": str(CURSORS[n][0]),
                         "Y2P": str(CURSORS[n][1]), "XDEL": "1e-6", "YDEL": "9"}[f])
        return ";".join(vals)
    rto.write = fake_write
    full = rto.get_cursors_fast((1, 2, 3, 4))
    assert len(sent) == 1 and full[3] is None and full[1]["y2 position"] == "2.0"
    quick = rto.get_cursors_fast((1, 2, 4), fields=("y1 position", "y2 position"))
    assert len(sent) == 2 and list(quick[1].keys()) == ["y1 position", "y2 position"]
    assert sent[1].count("?") == 6
    rto.write = lambda cmd: "1;2;3"
    try:
        rto.get_cursors_fast((1, 2))
        raise AssertionError("expected ValueError")
    except ValueError:
        pass
    # timing diagnostics CSV
    import csv, tempfile
    assert T.TIMING_DIAG_CSV is True
    with tempfile.TemporaryDirectory() as d:
        td = make(BatchScope())
        td.data_file_path = os.path.join(d, "RDSON_x.xlsx")
        td.poll_sample_index = 1
        td._last_capture_steps = {"trigger_read_s": 0.33, "screenshot_s": 3.9}
        td._diag_meas = {"cursor_read_s": 11.0, "cursor_items": 8, "cursor_repeat_probe_s": 0.3}
        s1 = _dt.datetime(2026, 1, 1, 12, 0, 0)
        td._write_timing_diag_row(860, 2, 0.1, s1, 30.0, capture_total_s=17.7, row_record_s=0.05)
        td.poll_sample_index = 2
        td._write_timing_diag_row(860, 2, 0.1, s1 + _dt.timedelta(seconds=30.1), 30.0,
                                  capture_total_s=17.9, row_record_s=0.04)
        path = os.path.join(d, "RDSON_x_timing.csv")
        rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
        assert len(rows) == 2 and list(rows[0].keys()) == list(T.TIMING_DIAG_FIELDS)
        assert rows[0]["spacing_s"] == "" and rows[1]["spacing_s"] == "30.1"
        assert rows[0]["screenshot_s"] == "3.9" and rows[0]["cursor_read_s"] == "11.0"
        assert rows[1]["sample"] == "2" and rows[0]["capture_total_s"] == "17.7"
    # compact terminal block
    hdr = ["VDC (rms)", "Po_Total (W)", "Vo1 (V)", "Io1 (A)", "Vo2 (V)", "Io2 (A)",
           "Efficiency (%)", "Rds1 (ohm)", "Rds2 (ohm)", "Rds3 (ohm)", "Rds4 (ohm)",
           "Rds_avg (ohm)", "VDS Max", "IDS Max"]
    vals = [860, 97.66, 47.93, 2.0, 20.19, 0.11, 86.42, .67, .68, .67, .67, .67, 4.01, 3.28]
    blk = T.format_terminal_block(hdr, vals).split("\n")
    assert blk[0] == "[RDSON][860V][97.7W]", blk[0]
    assert "OUT:   47.93V/2.00A + 20.19V/0.11A" in blk and "EFF:   86.42%" in blk
    assert "RDS:   0.67ohm, 0.68ohm, 0.67ohm, 0.67ohm (Avg=0.67ohm)" in blk
    assert "PEAKS: Vds=4.01V, Ids=3.28A" in blk
    # minimum interval warning (warn only, 30 s)
    assert T.MIN_INTERVAL_S == 5.0
    assert T.interval_warning(6) == "" and T.interval_warning(30) == ""
    assert "below the recommended minimum of 5 s" in T.interval_warning(4)
    assert T.interval_warning(20, no_integration=False) == ""
    assert T.interval_warning("abc") == ""
    # malformed batch reply -> fallback to per-field get_cursor, flagged once
    bad = BatchScope(bad=True)
    t = make(bad)
    meas = t.query_active_scope_measurements()
    assert meas["Rds_avg (ohm)"] == 0.2 and t._cursor_batch_failed
    t.query_active_scope_measurements()
    assert bad.batch_calls == 1
    print("OK:", len(cols), "scope columns")


if __name__ == "__main__":
    main()
