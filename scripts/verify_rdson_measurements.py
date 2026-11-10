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


def make(scope):
    t = T.__new__(T)
    t.scope_channels = T.POLL_DEFAULT_SCOPE_CHANNELS
    t.embed_images = True
    t.oscilloscope = scope
    return t


def main():
    assert T in TestTypes, "not registered"
    assert T.tc_default is not None and T.tc_default.name == "Rdson Measurements"
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
    print("OK:", len(cols), "scope columns")


if __name__ == "__main__":
    main()
