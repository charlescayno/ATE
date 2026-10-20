"""Simulation check for the Manual Control 4-meter grid, total efficiency and CCH discharge.

Run: .\\conda_env\\python.exe scripts\\verify_pml_grid_discharge.py
"""
import os
import runpy
import sys
import time
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
os.environ["PI_ATE_SIMULATION"] = "1"
os.environ["PI_ATE_AUTO_CONFIRM"] = "1"

OUT = sys.__stdout__
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    OUT.write(f"{'PASS' if cond else 'FAIL'}  {name}{('  -> ' + str(detail)) if detail and not cond else ''}\n")
    OUT.flush()


class FakeMeter:
    def __init__(self, v, i, p, pf=0.95):
        self._voltage, self._current, self._power, self._pf = v, i, p, pf
        self.polls = 0

    def update_basic_params(self):
        self.polls += 1


class FakeLoad:
    def __init__(self, name, log, mode='CCL', status='1', cc=2.5):
        self.name, self.log, self.state = name, log, {'mode': mode, 'status': status, 'cc_l1': cc}
        self.channel = 1

    def _rec(self, *a):
        self.log.append((self.name,) + a)

    def snapshot_state(self):
        self._rec('snapshot'); return dict(self.state)

    def restore_state(self, s):
        self._rec('restore', s['mode'], s['cc_l1'], s['status']); self.state = dict(s)

    def set_cc_high(self, a):
        self._rec('cch', a)

    def turn_on(self):
        self._rec('on')

    def turn_off(self):
        self._rec('off')

    def short_on(self):
        self._rec('SHORT')

    def reset_values(self):
        self._rec('reset')

    @property
    def cc(self):
        return 0

    @cc.setter
    def cc(self, v):
        self._rec('AUTO_RANGE_CC', v)


def wait_until(app, cond, timeout_s=5.0):
    t0 = time.time()
    while not cond() and time.time() - t0 < timeout_s:
        app.processEvents()
        time.sleep(0.01)
    return cond()


def test_pure():
    from page_controls.pml_grid import compute_efficiency
    total, eff, shares = compute_efficiency(20.0, {1: 10.0, 2: 5.0})
    check("eff: 2 meters sum Pout", abs(total - 15) < 1e-9 and abs(eff - 75) < 1e-9, (total, eff))
    check("eff: share per meter", abs(shares[1] - 66.666) < 0.01 and abs(shares[2] - 33.333) < 0.01, shares)
    total, eff, shares = compute_efficiency(20.0, {1: 18.0})
    check("eff: single meter unchanged", abs(eff - 90) < 1e-9 and abs(shares[1] - 100) < 1e-9)
    check("eff: Pin 0 -> None", compute_efficiency(0.0, {1: 1.0})[1] is None)
    check("eff: no meters -> None", compute_efficiency(20.0, {}) == (None, None, {}))


def test_driver_commands():
    from equipment.electronic_load import ElectronicLoadModule
    cmds = []
    st = {'MODE': 'CCL', 'LOAD': '1', 'L1': '2.5'}

    def write(cmd):
        cmds.append(cmd)
        if cmd == 'MODE?': return st['MODE']
        if cmd == 'LOAD?': return st['LOAD']
        if cmd == 'CURR:STAT:L1?': return st['L1']
        k, _, v = cmd.partition(' ')
        if k == 'MODE': st['MODE'] = v
        if k == 'LOAD': st['LOAD'] = '1' if v == 'ON' else '0'
        if k == 'CURR:STAT:L1': st['L1'] = v

    ld = object.__new__(ElectronicLoadModule)
    ld.write, ld.channel, ld.device_id = write, 1, 'FAKE'
    ld.prog_func = SimpleNamespace(channel='CHAN', mode='MODE', load='LOAD', current_static='CURR:STAT')
    ld._active_level, ld._cc, ld.active_channel_status = '1', 2.5, '1'
    snap = ld.snapshot_state()
    check("driver: snapshot reads mode/status/L1", snap['mode'] == 'CCL' and snap['status'] == '1' and snap['cc_l1'] == 2.5, snap)
    cmds.clear()
    ld.set_cc_high(1.0)
    check("driver: set_cc_high -> LOAD OFF, MODE CCH, L1 1.0", cmds == ['CHAN 1', 'LOAD OFF', 'MODE CCH', 'CURR:STAT:L1 1.0'], cmds)
    ld.turn_on(); ld.turn_off()
    cmds.clear()
    ld.restore_state(snap)
    check("driver: restore -> MODE CCL, L1 2.5, LOAD ON", 'MODE CCL' in cmds and 'CURR:STAT:L1 2.5' in cmds and st['LOAD'] == '1'
          and cmds.index('MODE CCL') < cmds.index('CURR:STAT:L1 2.5'), cmds)


def test_psu_discharge():
    import psu_tests.test_vds_ids_steady_state as ss
    import psu_tests.test_efficiency_2port_waveform as ew
    for mod, cls, src_attr in ((ss, ss.VdsIdsSteadyStateTest, 'ac_source'), (ew, ew.EfficiencyWaveformTest_2Port, 'input_supply')):
        log = []
        t = SimpleNamespace(electronic_load=FakeLoad('L1', log), electronic_load_2=None, i_max_A=3.0)
        setattr(t, src_attr, SimpleNamespace(turn_off=lambda: log.append(('src', 'off'))))
        mod.sleep = lambda s: None
        cls.discharge_output(t, 2)
        names = [e[1] for e in log]
        check(f"{mod.__name__.split('.')[-1]}: discharge uses CCH at test current, no SHORT/auto-range",
              names.count('cch') == 2 and all(e[2] == 3.0 for e in log if e[1] == 'cch')
              and 'SHORT' not in names and 'AUTO_RANGE_CC' not in names, log)


def test_ui():
    from PySide2.QtWidgets import QApplication
    app = QApplication.instance() or QApplication(sys.argv)
    g = runpy.run_path(str(ROOT / "main.py"), run_name="__smoke__")
    window = g["MainWindow"]()
    window.show()
    ui = window.ui
    ui.stackedWidget.setCurrentWidget(ui.page_manual_control)
    app.processEvents()
    mc = window.manual_control_handler
    import tempfile
    mc.settings_file = os.path.join(tempfile.gettempdir(), "pi_ate_verify_manual_settings.json")
    grid = mc.pml_grid

    check("ui: tab widget removed from layout", not ui.tabWidget_pml.isVisible() and ui.tabWidget_pml.count() == 0)
    check("ui: all 4 tiles visible at once", all(grid.widgets[n]['tile'].isVisible() for n in (1, 2, 3, 4)))
    check("ui: settings frames moved into gear dialogs",
          all(grid.widgets[n]['control'].parent() is grid.dialogs[n] for n in (1, 2, 3, 4)))
    grid.gears[2].click(); app.processEvents()
    check("ui: gear opens CH2 settings dialog", grid.dialogs[2].isVisible())
    grid.dialogs[2].close()
    check("ui: discharge controls default (auto ON, 1.0 A)",
          ui.chkbox_manual_control_auto_discharge.isChecked() and ui.lineedit_manual_control_discharge_current.text() == '1.0')

    # Assignment: CH3/CH4 unassigned
    mc.equipment.power_meter_load_3 = None
    mc.equipment.power_meter_load_4 = None
    mc.initialize_gpib_equipment()
    app.processEvents()
    t3 = grid.widgets[3]
    check("ui: unassigned CH3 tile greyed", not t3['tile'].isEnabled() and 'Not assigned' in t3['title'].text()
          and not mc.power_meter_load_3_accessible)

    # Efficiency across two load meters
    mc.update_timer.stop()
    mc.power_meter_source = FakeMeter(115.0, 0.2, 20.0)
    mc.power_meter_load = FakeMeter(12.0, 0.833, 10.0)
    mc.equipment.power_meter_load_2 = FakeMeter(5.0, 1.0, 5.0)
    mc.power_meter_source_accessible = mc.power_meter_load_accessible = mc.power_meter_load_2_accessible = True
    mc.is_ramping = False
    mc.power_meter_load_2_update()
    check("poll: load meter 2 now polled", mc.equipment.power_meter_load_2.polls == 1)
    mc.ui_powermeter_update()
    check("ui: total strip Pin/SumPout/Eff", ui.label_pml_total_pin.text() == 'Pin: 20.00 W'
          and ui.label_pml_total_pout.text().startswith('ΣPout: 15.00 W') and ui.label_pml_total_eff.text() == 'Total Eff: 75.00%',
          (ui.label_pml_total_pin.text(), ui.label_pml_total_pout.text(), ui.label_pml_total_eff.text()))
    check("ui: CH1/CH2 share on 4th line", ui.label_pml_display_d.text() == '66.7% Share' and ui.label_pml_display_d_2.text() == '33.3% Share',
          (ui.label_pml_display_d.text(), ui.label_pml_display_d_2.text()))
    check("ui: CH2 Pout shown", ui.label_pml_display_c_2.text() == '5.00 W', ui.label_pml_display_c_2.text())

    # Auto-discharge on source OFF
    log = []
    mc.equipment.electronic_load_1 = FakeLoad('L1', log, mode='CCL', status='1', cc=2.5)
    mc.equipment.electronic_load_2 = FakeLoad('L2', log, mode='CRH', status='0', cc=0.0)
    mc.equipment.electronic_load_3 = None
    mc.equipment.electronic_load_4 = None
    mc.electronic_load_accessible = mc.electronic_load_2_accessible = True
    mc.discharge.on_ms = mc.discharge.off_ms = 50
    mc.ac_source_request = 2  # AC_SOURCE_REQUEST.OFF
    mc.ac_source_request_service()
    done = wait_until(app, lambda: not mc.discharge.running)
    l1 = [e[1:] for e in log if e[0] == 'L1']
    check("discharge: auto-triggered on source OFF and finished", done and l1 and l1[0] == ('snapshot',), l1)
    check("discharge: L1 2x (CCH 1.0 A on, off) then restore",
          l1 == [('snapshot',), ('cch', 1.0), ('on',), ('off',), ('cch', 1.0), ('on',), ('off',), ('restore', 'CCL', 2.5, '1')], l1)
    check("discharge: both assigned loads pulsed, no SHORT/auto-range",
          sum(1 for e in log if e[0] == 'L2' and e[1] == 'cch') == 2 and not any(e[1] in ('SHORT', 'AUTO_RANGE_CC') for e in log))
    check("discharge: L2 restored to previous mode/OFF", ('L2', 'restore', 'CRH', 0.0, '0') in log)

    log.clear()
    ui.chkbox_manual_control_auto_discharge.setChecked(False)
    mc.ac_source_request_service()
    app.processEvents()
    check("discharge: auto OFF -> no discharge", not log and not mc.discharge.running, log)

    ui.lineedit_manual_control_discharge_current.setText('0.5')
    ui.btn_manual_control_discharge.click()
    wait_until(app, lambda: not mc.discharge.running)
    check("discharge: button uses configured current", ('L1', 'cch', 0.5) in log and ('L1', 'restore', 'CCL', 2.5, '1') in log)

    # Simulated e-load path (equipment/simulated_handler.py)
    from equipment.simulated_handler import SimulatedElectronicLoadModule, VirtualCircuitState
    sld = SimulatedElectronicLoadModule(VirtualCircuitState(), 1)
    sld.cc = 2.0; sld.turn_on()
    snap = sld.snapshot_state(); sld.set_cc_high(1.0)
    check("sim e-load: set_cc_high CCH + off", sld.active_channel_mode == 'CCH' and not sld._ch['load_on'])
    sld.restore_state(snap)
    check("sim e-load: restore current + ON", sld._ch['iout'] == 2.0 and sld._ch['load_on'])

    window.grab().save(str(ROOT / "scripts" / "verify_pml_grid.png"))
    window.close()


if __name__ == "__main__":
    test_pure()
    test_driver_commands()
    test_ui()
    test_psu_discharge()  # after main.py import order resolves psu_tests circular imports
    failed = [n for n, ok in results if not ok]
    OUT.write(f"\n{len(results) - len(failed)}/{len(results)} passed\n")
    sys.exit(1 if failed else 0)
