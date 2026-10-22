"""Run Startup Waveform AC Turn-On (DER-1113) headless against simulated equipment."""
import os
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
os.environ['PI_ATE_AUTO_CONFIRM'] = '1'
time.sleep = lambda _s: None

from PySide2.QtWidgets import QApplication  # noqa: E402

app = QApplication.instance() or QApplication(sys.argv)

import openpyxl  # noqa: E402
from psu_tests.definitions import (  # noqa: E402
    TestConditions, LineRange, LoadRange, SoakTime,
    GeneralOptions, USBPDOptions, I2CTestParameters, TestStatus)
from psu_tests.test_type import TestTypes  # noqa: E402
from psu_tests.test_startup_ac_turnon_waveform import StartupWaveformTest_ACTurnOn  # noqa: E402
from equipment.simulated_handler import SimulatedEquipmentHandler  # noqa: E402

MODES = {
    'A': "Option A: Proportional Sync (Both Ports 100% -> 10%)",
}


class FakeParent:
    def __init__(self):
        self.run_settings = {'debug': False}
        self.equipment = SimulatedEquipmentHandler(self)


class FakeItem:
    def __init__(self, parent, conditions):
        self.parent = parent
        self.test_type_index = TestTypes.index(StartupWaveformTest_ACTurnOn)
        self.test_conditions = conditions


def run_case(mode_key: str, out_dir: str) -> list:
    vin = [[180, 50], [230, 50]]
    loads = [100, 50]
    conditions = TestConditions(
        name=StartupWaveformTest_ACTurnOn.title,
        nominal_output_voltage_V=5, nominal_load_current_A=5, max_load_current_A=5,
        line_range=LineRange(name='TEST', vin_freq=vin, custom=True),
        load_range=LoadRange(name='TEST', load_range_pct=loads, custom=True),
        soak_time=SoakTime(name='VERIFY_SOAK', initial=2, line=3, load=4, integration=1),
        general_options=GeneralOptions(coupling='AC'),
        usbpd_options=USBPDOptions(),
        i2c_test_parameters=I2CTestParameters(
            params=[12.0, 2.0, 0.0, "100, 50", 3.0, 0, 2, 25.0, 0, 2],
            cbx_params=[MODES[mode_key], 'Yes', 'None (Fully Automated)', 'No']),
        unit_id='U7', ambient_temp=25.0,
        scope_channels={
            1: {'enabled': True, 'name': 'Primary Vds', 'derating': 650, 'measurements': ['MAXimum']},
            2: {'enabled': True, 'name': 'Ids', 'measurements': ['MAXimum']},
            3: {'enabled': False, 'name': ''},
            4: {'enabled': False, 'name': ''},
        })

    statuses = []
    test = StartupWaveformTest_ACTurnOn(FakeItem(FakeParent(), conditions))
    test.status_update.connect(statuses.append)
    test.output_folder_path = os.path.join(out_dir, f"mode_{mode_key}")
    test.run()

    errors = []
    if TestStatus.COMPLETE not in statuses:
        return [f"mode {mode_key}: test did not complete, statuses={statuses}"]

    if not test.sheet_name.startswith('SU_WF_AC_'):
        errors.append(f"mode {mode_key}: sheet name {test.sheet_name!r}")
    pngs = [rec.get('path') for rec in getattr(test, 'captured_records', []) if rec.get('path')]
    if not pngs:
        errors.append(f"mode {mode_key}: no PNG captures recorded")
    if pngs and not all(p.endswith('_SUAC.png') for p in pngs):
        errors.append(f"mode {mode_key}: unexpected PNG suffix in {pngs!r}")
    return errors


def main():
    errors = []
    with tempfile.TemporaryDirectory() as tmp:
        for key in MODES:
            errors.extend(run_case(key, tmp))
    if errors:
        print("FAIL")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("OK")


if __name__ == '__main__':
    main()
