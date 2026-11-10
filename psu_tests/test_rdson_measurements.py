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
            'derating': None, 'cursor': {'enabled': False, 'type': 'VERTical'}},
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

    def setup_equipment(self):
        super().setup_equipment()
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

    def query_cursor_results(self) -> dict:
        """Read Cursor 1..4 from the scope and compute Rds; unavailable values are 'N/A'."""
        out = {}
        raw = {}
        for n in self.CURSOR_SETS:
            cur = None
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

    def query_active_scope_measurements(self) -> dict:
        meas = super().query_active_scope_measurements()
        meas.update(self.query_cursor_results())
        return meas

    @classmethod
    def _build_rdson_tc_default(cls):
        tc = cls._build_tc_default()
        tc.name = cls.title
        tc.scope_channels = deepcopy(cls.POLL_DEFAULT_SCOPE_CHANNELS)
        return tc


RdsonMeasurementTest_2Port.tc_default = RdsonMeasurementTest_2Port._build_rdson_tc_default()
