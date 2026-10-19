"""Run Efficiency 2 Port (Waveform) headless against the simulated equipment and check the Excel output."""
import os
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
os.environ['PI_ATE_AUTO_CONFIRM'] = '1'
time.sleep = lambda _s: None  # must run before test modules bind `from time import sleep`

from PySide2.QtWidgets import QApplication  # noqa: E402

app = QApplication.instance() or QApplication(sys.argv)

import openpyxl  # noqa: E402
from psu_tests.definitions import (TestConditions, LineRange, LoadRange, SoakTime,  # noqa: E402
                                   GeneralOptions, USBPDOptions, I2CTestParameters, TestStatus)
from psu_tests.test_type import TestTypes  # noqa: E402
from psu_tests.test_efficiency_2port_waveform import EfficiencyWaveformTest_2Port  # noqa: E402
from equipment.simulated_handler import SimulatedEquipmentHandler  # noqa: E402

MODES = {
    'A': "Option A: Proportional Sync (Both Ports 100% -> 10%)",
    'B': "Option B: Cross-Reg Matrix (Port 2 at Specified % Loads)",
}


class FakeParent:
    def __init__(self):
        self.run_settings = {'debug': False}
        self.equipment = SimulatedEquipmentHandler(self)


class FakeItem:
    def __init__(self, parent, conditions):
        self.parent = parent
        self.test_type_index = TestTypes.index(EfficiencyWaveformTest_2Port)
        self.test_conditions = conditions


def run_case(mode_key: str, out_dir: str) -> list:
    vin = [[115, 60], [230, 50]]
    loads = [100, 50, 10]
    conditions = TestConditions(
        name=EfficiencyWaveformTest_2Port.title,
        nominal_output_voltage_V=5, nominal_load_current_A=5, max_load_current_A=5,
        line_range=LineRange(name='TEST', vin_freq=vin, custom=True),
        load_range=LoadRange(name='TEST', load_range_pct=loads, custom=True),
        soak_time=SoakTime(name='TEST', initial=0, line=0, load=0, integration=0),
        general_options=GeneralOptions(coupling='AC'),
        usbpd_options=USBPDOptions(),
        i2c_test_parameters=I2CTestParameters(
            params=[12.0, 2.0, 0.0, "100, 50", 3.0, 0, 0, 25.0, 0, 2],
            cbx_params=[MODES[mode_key], 'Yes', 'None (Fully Automated)', 'No']),
        unit_id='U7', ambient_temp=25.0,
        scope_channels={1: {'enabled': True, 'name': 'Primary Vds', 'derating': 650},
                        2: {'enabled': True, 'name': 'Ids'},
                        3: {'enabled': False, 'name': ''}, 4: {'enabled': False, 'name': ''}})

    statuses = []
    test = EfficiencyWaveformTest_2Port(FakeItem(FakeParent(), conditions))
    test.status_update.connect(statuses.append)
    test.output_folder_path = os.path.join(out_dir, f"mode_{mode_key}")
    test.run()

    errors = []
    if TestStatus.COMPLETE not in statuses:
        return [f"mode {mode_key}: test did not complete, statuses={statuses}"]

    n_points = len(test.load_pairs)
    wb = openpyxl.load_workbook(test.data_file_path)
    ws = wb[test.sheet_name]
    if ws['Y4'].value != 'Oscilloscope Measurements':
        errors.append(f"mode {mode_key}: Y4 = {ws['Y4'].value!r}")
    if ws['S5'].value != 'Efficiency (%)' or ws['T5'].value != 'Avg_Eff' or ws['Y5'].value != 'Trig Ch':
        errors.append(f"mode {mode_key}: header row S5/T5/Y5 = {ws['S5'].value!r}/{ws['T5'].value!r}/{ws['Y5'].value!r}")
    expected_scope = ['Trig Ch', 'Trig Level (V)', 'Primary Vds Max', 'Primary Vds Derating (%)', 'Ids Max', 'Waveform File']
    got_scope = [ws.cell(row=5, column=25 + i).value for i in range(len(expected_scope))]
    if got_scope != expected_scope:
        errors.append(f"mode {mode_key}: scope headers {got_scope}")

    # Only the first line-voltage block carries the header row (same as Efficiency 2 Port).
    data_start = 6
    for vin_idx in range(len(vin)):
        if ws.cell(row=data_start + n_points, column=1).value not in (None, ''):
            errors.append(f"mode {mode_key}: expected blank separator at row {data_start + n_points}")
        for r in range(data_start, data_start + n_points):
            eff = ws.cell(row=r, column=19).value
            vds = ws.cell(row=r, column=27).value
            img = ws.cell(row=r, column=30).value
            if not isinstance(eff, (int, float)) or not isinstance(vds, (int, float)):
                errors.append(f"mode {mode_key}: row {r} eff={eff!r} vds={vds!r}")
            if ws.cell(row=r, column=25).value != 'CH2':
                errors.append(f"mode {mode_key}: row {r} trigger channel {ws.cell(row=r, column=25).value!r}")
            if not img or not os.path.exists(img):
                errors.append(f"mode {mode_key}: row {r} missing screenshot {img!r}")
        data_start += n_points + 1

    wf_sheet = f"{test.short_title}_Waveforms"
    if wf_sheet not in wb.sheetnames:
        errors.append(f"mode {mode_key}: no {wf_sheet} sheet")
    elif len(wb[wf_sheet]._images) != n_points * len(vin):
        errors.append(f"mode {mode_key}: {len(wb[wf_sheet]._images)} embedded images, expected {n_points * len(vin)}")

    table = test.test_data_table
    if len(table.header) != 19 + len(expected_scope):
        errors.append(f"mode {mode_key}: results table has {len(table.header)} columns")
    data_rows = [r for r in table.data if any(v != '' for v in r)]
    if len(data_rows) != n_points * len(vin):
        errors.append(f"mode {mode_key}: results table has {len(data_rows)} data rows")

    print(f"mode {mode_key}: {n_points} load pairs x {len(vin)} line steps -> {test.data_file_path}")
    return errors


def main() -> int:
    out_dir = tempfile.mkdtemp(prefix="eff2p_wf_")
    errors = run_case('A', out_dir) + run_case('B', out_dir)
    if errors:
        print("FAIL")
        for e in errors:
            print(" ", e)
        return 1
    print("OK Efficiency 2 Port (Waveform) simulated runs passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
