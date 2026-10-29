"""Verify TestData._reconcile_load_vout fixes zero/nan Vo for Excel."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

from equipment.power_meter_specs import parse_float_response  # noqa: E402
from psu_tests.definitions import TestData  # noqa: E402

errors = []


def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  -> {detail}" if detail and not ok else ""))
    if not ok:
        errors.append(name)


class FakePM:
    def __init__(self, v, i=None, p=None):
        self._v = v
        self._i = i
        self._p = p

    @property
    def voltage(self):
        return self._v

    @property
    def current(self):
        return self._i if self._i is not None else 0.0

    @property
    def power(self):
        return self._p if self._p is not None else 0.0

    def get_integration_timer(self):
        return 0


def test_parse_nan():
    check("parse nan string", parse_float_response("nan", -1.0) == -1.0)
    check("parse float nan", parse_float_response(float("nan"), 0.0) == 0.0)


def test_p_over_i():
    td = TestData()
    td.vout_nom_V = 48.0
    td.load_power_meter = None
    td.vout_V = 0.0
    td.iout_A = 1.0
    td.pout_W = 48.1
    td._reconcile_load_vout()
    check("Vo from P/I when U=0", abs(td.vout_V - 48.1) < 0.01, td.vout_V)


def test_eload_zero_pm_wins():
    td = TestData()
    td.vout_nom_V = 48.0
    td.load_power_meter = FakePM(47.95)
    td.vout_V = 0.0
    td.iout_A = 2.0
    td.pout_W = 95.0
    td._reconcile_load_vout()
    check("PM U when e-load V=0", abs(td.vout_V - 47.95) < 0.01, td.vout_V)


def test_stable_source_pin_uses_averaging_when_no_timer():
    from psu_tests.definitions import TestData

    class Src:
        integration_calls = []
        avg_on = False
        _integration_time = 0

        def get_integration_timer(self):
            return 0

        @property
        def voltage(self):
            return 750.0

        @property
        def current(self):
            return 0.1

        @property
        def pf(self):
            return 1.0

        @property
        def power(self):
            return 73.0

        def enable_averaging(self, en=True):
            self.avg_on = bool(en)

        def start_integration(self):
            self.integration_calls.append('start')

        def poll_integration_status(self):
            pass

        def get_integrated_power(self, reset=True):
            return 99.0

    td = TestData()
    td.vout_nom_V = 48.0
    td.source_power_meter = Src()
    td.load_power_meter = None
    td.use_eload_data = True
    td.electronic_load = type('E', (), {'voltage': 48.0, 'current': 1.0})()
    td.gather_data(coupling='DC', measure_thd=False, stable_source_pin=True)
    check('poll Pin uses averaging path', td.source_power_meter.avg_on)
    check('Pin from source', abs(td.pin_W - 73.0) < 0.01, td.pin_W)
    check('no integration when timer 0', not td.source_power_meter.integration_calls)


def test_stable_source_pin_reads_vin_after_integration():
    from psu_tests.definitions import TestData

    class Src:
        _integration_time = 60
        read_order = []

        def get_integration_timer(self):
            return 60

        @property
        def voltage(self):
            self.read_order.append("v")
            return 750.0

        @property
        def current(self):
            self.read_order.append("i")
            return 0.05

        @property
        def pf(self):
            return 0.99

        @property
        def power(self):
            return 0.0

        def enable_averaging(self, en=True):
            pass

        def start_integration(self):
            self.read_order.append("start")

        def poll_integration_status(self):
            self.read_order.append("poll_done")

        def get_integrated_power(self, reset=True):
            self.read_order.append("pin")
            return 250.0

    td = TestData()
    td.vout_nom_V = 48.0
    td.source_power_meter = Src()
    td.load_power_meter = FakePM(48.0, i=4.5, p=215.0)
    td.use_eload_data = False
    td.gather_data(coupling="DC", measure_thd=False, stable_source_pin=True)
    check("Vin after integration", abs(td.vin_V - 750.0) < 0.01, td.vin_V)
    check("Pin integrated", abs(td.pin_W - 250.0) < 0.01, td.pin_W)
    check("Iin mA scaled", abs(td.iin_mA - 50.0) < 0.01, td.iin_mA)
    order = td.source_power_meter.read_order
    check("poll before Vin read", order.index("poll_done") < order.index("v"), order)


def test_gather_data_load_path():
    td = TestData()
    td.vout_nom_V = 20.0
    td.use_eload_data = False
    td.load_power_meter = FakePM(0.0, i=1.0, p=20.25)
    td.vout_V = td.load_power_meter.voltage
    td.iout_A = td.load_power_meter.current
    td.pout_W = td.load_power_meter.power
    td._reconcile_load_vout()
    check("load path reconcile", abs(td.vout_V - 20.25) < 0.05, td.vout_V)


if __name__ == "__main__":
    test_parse_nan()
    test_p_over_i()
    test_eload_zero_pm_wins()
    test_stable_source_pin_uses_averaging_when_no_timer()
    test_stable_source_pin_reads_vin_after_integration()
    test_gather_data_load_path()
    if errors:
        print(f"\n{len(errors)} failed")
        sys.exit(1)
    print("\nOK  verify_vout_reconcile")
