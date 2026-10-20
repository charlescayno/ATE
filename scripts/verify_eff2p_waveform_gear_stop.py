"""UI gear visibility + stop-test discharge for Efficiency 2 Port (Waveform)."""
import os
import runpy
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from PySide2.QtWidgets import QApplication  # noqa: E402

app = QApplication.instance() or QApplication(sys.argv)

from psu_tests.definitions import TestStatus  # noqa: E402
from psu_tests.test_efficiency_2port_waveform import EfficiencyWaveformTest_2Port  # noqa: E402
from psu_tests.test_type import TestTypes  # noqa: E402
from page_controls.add_test import EFFICIENCY_2PORT_WAVEFORM_TITLE  # noqa: E402

errors = []


def check(name, ok, detail=""):
    if ok:
        print(f"OK  {name}")
    else:
        print(f"FAIL {name} {detail}")
        errors.append(name)


def test_ui_gear():
    g = runpy.run_path(str(ROOT / "main.py"), run_name="__gear_ui__")
    window = g["MainWindow"]()
    window.show()
    window.ui.stackedWidget.setCurrentWidget(window.ui.page_add_tests)
    app.processEvents()
    add = window.add_test_pagehandler
    idx = next(i for i, t in enumerate(TestTypes) if t.title == EFFICIENCY_2PORT_WAVEFORM_TITLE)
    add.ui.cbx_add_tests_testtype.setCurrentIndex(idx)
    add.test_type_index_changed()
    app.processEvents()

    hidden = all(not add.i2c_ui_lineedit_frames[i].isVisible() for i in range(4, 10))
    check("ui: advanced lineedits 5-10 hidden", hidden)
    gear_ok = hasattr(add, 'frame_eff2p_advanced_gear') and add.frame_eff2p_advanced_gear.isVisibleTo(add.ui.frame_add_tests_i2c)
    check("ui: gear row visible", gear_ok)
    scope_ok = hasattr(add, 'frame_scope_channels') and add.frame_scope_channels.isVisibleTo(add.ui.frame_add_tests_i2c)
    check("ui: scope channels visible", scope_ok)

    add.i2c_ui_lineedits[4].setText("0.75")
    dlg = __import__('page_controls.eff2p_waveform_advanced', fromlist=['Eff2PWaveformAdvancedDialog']).Eff2PWaveformAdvancedDialog(
        window, add.i2c_ui_lineedits, scope_channels=add.get_scope_channels_from_ui())
    dlg.le_trigger_delta.setText("1.25")
    dlg.apply_to_lineedits()
    check("ui: dialog writes trigger delta", add.i2c_ui_lineedits[4].text() == "1.25")


def test_stop_discharge():
    log = []

    class FakeLoad:
        def set_cc_high(self, a):
            log.append(('cch', float(a)))

        def turn_on(self):
            log.append(('on',))

        def turn_off(self):
            log.append(('off',))

        def reset_values(self):
            log.append(('reset',))

    import psu_tests.test_efficiency_2port_waveform as ew_mod

    ew_mod.sleep = lambda _s: None
    t = EfficiencyWaveformTest_2Port.__new__(EfficiencyWaveformTest_2Port)
    t.electronic_load = FakeLoad()
    t.electronic_load_2 = FakeLoad()
    t.discharge_pulses = 0
    t.input_supply = SimpleNamespace(turn_off=lambda: log.append(('src', 'off')))
    t.safe_output_discharge(reason="test")
    cch = [x[1] for x in log if x[0] == 'cch']
    check("stop: uses 1.0 A CCH", cch and all(v == 1.0 for v in cch), cch)
    check("stop: at least 2 pulses per load", cch.count(1.0) >= 4, log)


def test_run_stopped():
    import psu_tests.test_efficiency_2port_waveform as ew_mod
    from psu_tests.definitions import TestConditions, LineRange, LoadRange, SoakTime, GeneralOptions, USBPDOptions, I2CTestParameters
    from equipment.simulated_handler import SimulatedEquipmentHandler

    ew_mod.sleep = lambda _s: None
    discharged = []

    class Parent:
        run_settings = {'debug': False}
        equipment = None

    class Item:
        parent = Parent()
        test_type_index = TestTypes.index(EfficiencyWaveformTest_2Port)
        test_conditions = TestConditions(
            name=EfficiencyWaveformTest_2Port.title,
            nominal_output_voltage_V=5, nominal_load_current_A=5, max_load_current_A=5,
            line_range=LineRange(name='T', vin_freq=[[115, 60]], custom=True),
            load_range=LoadRange(name='T', load_range_pct=[100], custom=True),
            soak_time=SoakTime(name='T', initial=0, line=0, load=0, integration=0),
            general_options=GeneralOptions(coupling='AC'),
            usbpd_options=USBPDOptions(),
            i2c_test_parameters=I2CTestParameters(
                params=[12.0, 2.0, 0.0, "100", 0.5, 1.0, 0, 25.0, 1.0, 1.0],
                cbx_params=[EfficiencyWaveformTest_2Port.tc_default.i2c_test_parameters.cbx_param[0],
                            'Yes', 'None (Fully Automated)', 'No']),
            unit_id='T', ambient_temp=25.0,
            scope_channels=EfficiencyWaveformTest_2Port.tc_default.scope_channels)

    Parent.equipment = SimulatedEquipmentHandler(Parent())
    item = Item()
    test = EfficiencyWaveformTest_2Port(item)
    orig = test.test_loop

    from psu_tests.definitions import TestStopped

    def stop_loop():
        test.safe_output_discharge = lambda reason="": discharged.append(reason)
        raise TestStopped

    test.test_loop = stop_loop
    test.setup_equipment = lambda: None
    test.prepare_test_conditions = lambda: test.unpack_test_item()
    test.setup_data_file = lambda: None
    test.cleanup_usbpd_pps_operation = lambda: None
    test.input_supply_eload_discharge_sequence = lambda: log.append('input_discharge')
    log = []
    statuses = []
    test.status_update.connect(statuses.append)
    test.run()
    check("run: STOPPED status", TestStatus.STOPPED in statuses, statuses)
    check("run: safe discharge on stop", discharged == ['stopped'], discharged)


if __name__ == '__main__':
    test_ui_gear()
    test_stop_discharge()
    test_run_stopped()
    if errors:
        print(f"\n{len(errors)} failure(s)")
        sys.exit(1)
    print("\nAll checks passed.")
