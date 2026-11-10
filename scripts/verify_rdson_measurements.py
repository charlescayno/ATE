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
        self.batch_calls = 0
        self.measure_queries = []
        self.arn_count = 0

    def get_cursors_fast(self, cursors=(1, 2, 3, 4)):
        self.batch_calls += 1
        if self.bad:
            raise ValueError("bad reply")
        self.cursor_queries += 1
        out = {}
        for n in cursors:
            if n in self.off:
                out[n] = None
                continue
            y1, y2 = CURSORS[n]
            out[n] = {"y1 position": str(y1), "y2 position": str(y2),
                      "delta x": "1e-6", "delta y": str(y2 - y1)}
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


def main():
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
