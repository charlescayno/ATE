"""Simulation check for the Manual Control e-load 2x2 grid and fixed-range Chroma modes.

Run: .\\conda_env\\python.exe scripts\\verify_eload_grid.py
"""
import json
import os
import runpy
import sys
import tempfile
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
    msg = f"{'PASS' if cond else 'FAIL'}  {name}"
    if detail and not cond:
        msg += f"  -> {detail}"
    OUT.write(msg.encode('ascii', 'replace').decode() + "\n")
    OUT.flush()


def test_specs_and_driver():
    from equipment import eload_specs as es
    from equipment.electronic_load import ElectronicLoadModule

    modes = es.fixed_range_modes(es.Chroma63103A)
    check("specs: 63103A adds CCL/CCH/CCDL/CCDH/CRL/CRH", modes == ['CCL', 'CCH', 'CCDL', 'CCDH', 'CRL', 'CRH'], modes)
    check("specs: no dynamic modes when CCD not supported", 'CCDL' not in es.fixed_range_modes(es.EloadModuleBaseClass))

    cmds, st = [], {'MODE': 'CCH', 'LOAD': '1'}

    def write(cmd):
        cmds.append(cmd)
        if cmd == 'MODE?': return st['MODE']
        if cmd == 'LOAD?': return st['LOAD']
        k, _, v = cmd.partition(' ')
        if k == 'MODE': st['MODE'] = v
        if k == 'LOAD': st['LOAD'] = '1' if v == 'ON' else '0'

    ld = object.__new__(ElectronicLoadModule)
    ld.write, ld.channel, ld.device_id = write, 1, 'FAKE'
    ld.prog_func = SimpleNamespace(channel='CHAN', mode='MODE', load='LOAD', current_static='CURR:STAT',
                                   current_dynamic='CURR:DYN', resistance='RES', rise='RISE', fall='FALL')
    ld.ccl_max_a, ld.cch_max_a = 6.0, 60.0
    ld.crl_min_r, ld.crl_max_r, ld.crh_min_r, ld.crh_max_r = 0.025, 100.0, 1.25, 5000.0
    ld.ccd_t_min_s, ld.ccd_t_max_s = 25e-6, 50.0
    ld._active_level, ld._cc = '1', 0

    ld.set_fixed_mode('CCL', 2.0, 1)
    check("driver: CCL from CCH (ON) -> OFF, MODE CCL, L1, ON",
          cmds == ['CHAN 1', 'LOAD?', 'MODE?', 'LOAD OFF', 'MODE CCL', 'CURR:STAT:L1 2.0', 'LOAD ON', 'LOAD?'], cmds)
    cmds.clear()
    ld.set_fixed_mode('CCL', 3.0, 2)
    check("driver: same mode -> no MODE write, L2 set", 'MODE CCL' not in cmds and 'CURR:STAT:L2 3.0' in cmds
          and 'LOAD OFF' not in cmds, cmds)
    cmds.clear()
    try:
        ld.set_fixed_mode('CCL', 7.0)
        raised = False
    except ValueError as e:
        raised = 'CCH' in str(e)
    check("driver: CCL over range raises with CCH hint, nothing sent", raised and not cmds, cmds)
    cmds.clear()
    ld.set_fixed_mode('CRH', 100.0)
    check("driver: CRH writes RES:L1", 'MODE CRH' in cmds and 'RES:L1 100.0' in cmds, cmds)
    cmds.clear()
    ld.set_dynamic('CCDH', 10.0, 20.0, 5, 15, 0.15, 'MAX')
    expected = ['MODE CCDH', 'CURR:DYN:L1 10.0', 'CURR:DYN:L2 20.0', 'CURR:DYN:RISE 0.15', 'CURR:DYN:FALL MAX',
                'CURR:DYN:T1 5mS', 'CURR:DYN:T2 15mS']
    check("driver: CCDH dynamic sequence with mS suffix", all(c in cmds for c in expected)
          and cmds.index('MODE CCDH') < cmds.index('CURR:DYN:L1 10.0'), cmds)
    cmds.clear()
    try:
        ld.set_dynamic('CCDL', 1.0, 2.0, 0.0, 10)
        raised = False
    except ValueError:
        raised = True
    check("driver: dynamic T1 below minimum rejected", raised and not cmds, cmds)


def wait(app, n=5):
    for _ in range(n):
        app.processEvents()


def test_ui():
    from PySide2.QtWidgets import QApplication
    app = QApplication.instance() or QApplication(sys.argv)
    g = runpy.run_path(str(ROOT / "main.py"), run_name="__smoke__")
    window = g["MainWindow"]()
    mc = window.manual_control_handler
    mc.settings_file = os.path.join(tempfile.gettempdir(), "pi_ate_verify_manual_settings.json")
    messages = []
    window.msg_box_info = lambda title, message, message_type=None: messages.append(message)
    window.msg_box_pick = lambda *a, **k: 1024
    window.resize(1600, 950)
    window.show()
    ui = window.ui
    ui.stackedWidget.setCurrentWidget(ui.page_manual_control)
    wait(app)
    grid = mc.eload_grid
    ch = grid.channels

    check("ui: e-load tabs removed", ui.tabWidget_eload.count() == 0 and not ui.tabWidget_eload.isVisible())
    check("ui: all 4 e-load tiles visible", all(ch[n].w['tile'].isVisible() for n in (1, 2, 3, 4)))
    check("ui: slew frames moved into gear dialogs", all(ch[n].w['slew'].parent() is grid.dialogs[n] for n in (1, 2, 3, 4)))
    grid.gears[3].click(); wait(app)
    check("ui: gear opens CH3 slew dialog", grid.dialogs[3].isVisible())
    grid.dialogs[3].close()
    check("ui: USB PD Sink collapsed by default", not ui.frame_manual_control_usb_pd_sink.isVisible())
    ui.btn_manual_control_usb_pd_toggle.click(); wait(app)
    expanded = ui.frame_manual_control_usb_pd_sink.isVisible()
    ui.btn_manual_control_usb_pd_toggle.click(); wait(app)
    check("ui: USB PD toggle expands and collapses", expanded and not ui.frame_manual_control_usb_pd_sink.isVisible())
    header = ui.widget_eload_grid.findChild(type(ui.frame_manual_control_lower), "frame_eload_grid_header")
    check("ui: discharge controls moved into e-load header",
          header is not None and ui.btn_manual_control_discharge.parent() is header
          and ui.chkbox_manual_control_auto_discharge.parent() is header)

    mc.initialize_gpib_equipment(); wait(app)
    mc.update_timer.stop()
    items = [ch[2].w['mode'].itemText(i) for i in range(ch[2].w['mode'].count())]
    check("modes: auto modes kept first, fixed-range appended",
          items[:5] == ['CC', 'CR', 'CV', 'CP', 'LED'] and items[5:] == ['CCL', 'CCH', 'CCDL', 'CCDH', 'CRL', 'CRH'], items)
    check("modes: populated on all 4 tiles", all(ch[n].w['mode'].count() == 11 for n in (1, 2, 3, 4)))

    # CH4 buttons are wired now
    ld4 = mc.equipment.electronic_load_4
    ch[4].w['mode'].setCurrentText('CC')
    ch[4].w['a_edit'].setText('1.5')
    ch[4].w['set_a'].click()
    ch[4].w['on'].click(); wait(app)
    mc.ui_eload_update()
    check("CH4: Set A + Load ON reach electronic_load_4", ld4._ch['iout'] == 1.5 and ld4._ch['load_on'])
    check("CH4: status shows ON and tile border green", 'ON' in ch[4].status.text()
          and '85,170,85' in ch[4].w['tile'].styleSheet(), (ch[4].status.text(), ch[4].w['tile'].styleSheet()))
    ch[4].w['off'].click(); mc.ui_eload_update()
    check("CH4: Load OFF", not ld4._ch['load_on'] and 'OFF' in ch[4].status.text())

    # Fixed-range CC on CH2
    ld2 = mc.equipment.electronic_load_2
    ch[1].w['rise_edit'].setText('77')
    ch[2].w['mode'].setCurrentText('CCL'); wait(app)
    check("CH2: mode change leaves CH1 slew field alone", ch[1].w['rise_edit'].text() == '77', ch[1].w['rise_edit'].text())
    ch[2].w['a_edit'].setText('2.5')
    ch[2].w['set_a'].click()
    check("CH2: CCL Set A -> set_fixed_mode('CCL', 2.5, 1)", ld2.mode_log[-1:] == [('fixed', 'CCL', 2.5, 1)], ld2.mode_log)
    n_log = len(ld2.mode_log)
    ch[2].w['a_edit'].setText('7')
    ch[2].w['set_a'].click()
    check("CH2: CCL 7 A rejected with message, nothing sent", len(ld2.mode_log) == n_log and messages
          and 'CCH' in messages[-1], messages)
    check("CH2: tile still usable after range error", mc.electronic_load_2_accessible and ch[2].w['tile'].isEnabled())

    # CRH
    ch[2].w['mode'].setCurrentText('CRH'); wait(app)
    check("CH2: CRH unit is ohms", ch[2].w['a_unit'].text() == 'Ω', ch[2].w['a_unit'].text())
    ch[2].w['b_edit'].setText('100')
    ch[2].w['set_b'].click()
    check("CH2: CRH Set B -> level 2", ld2.mode_log[-1] == ('fixed', 'CRH', 100.0, 2), ld2.mode_log[-1])

    # Dynamic CCDH
    ch[2].w['mode'].setCurrentText('CCDH'); wait(app)
    check("CH2: CCDH shows T1/T2 row and L1/L2 captions, hides Set A/B",
          ch[2].dynamic_row.isVisible() and ch[2].w['a_label'].text() == 'L1' and not ch[2].w['set_a'].isVisible()
          and not ch[2].w['swap'].isEnabled())
    ch[2].w['a_edit'].setText('10'); ch[2].w['b_edit'].setText('20')
    ch[2].t1_edit.setText('5'); ch[2].t2_edit.setText('15')
    ch[2].apply_btn.click()
    check("CH2: Apply sends dynamic L1/L2/T1/T2 + slew",
          ld2.mode_log[-1] == ('dynamic', 'CCDH', 10.0, 20.0, 5.0, 15.0, 0.15, 0.15), ld2.mode_log[-1])

    # CP no longer raises on CH2-4 (old merged-decorator bug)
    ch[3].w['mode'].setCurrentText('CP'); wait(app)
    check("CH3: CP mode selectable without error", ch[3].w['rise_unit'].text() == 'W / µs' and mc.electronic_load_3_accessible)

    # Unassigned tile
    mc.equipment.electronic_load_4 = None
    mc.initialize_gpib_equipment(); wait(app)
    mc.update_timer.stop()
    check("CH4: unassigned tile greyed", not ch[4].w['tile'].isEnabled() and 'Not assigned' in ch[4].w['title'].text()
          and not mc.electronic_load_4_accessible)
    mc.equipment.electronic_load_4 = ld4

    # Save/restore includes dialog widgets with unique keys
    ch[2].w['rise_edit'].setText('123')
    ch[1].w['rise_edit'].setText('77')
    mc.save_manual_settings()
    saved = json.load(open(mc.settings_file, encoding='utf-8'))
    check("save: CH2 dialog slew saved under its own key",
          saved.get('lineedit_manual_control_eload_slew_rise_2') == '123'
          and saved.get('lineedit_manual_control_eload_slew_rise') == '77',
          {k: v for k, v in saved.items() if 'slew_rise' in k})
    ch[2].w['rise_edit'].setText('0')
    mc.load_manual_settings()
    check("restore: CH2 dialog slew restored", ch[2].w['rise_edit'].text() == '123', ch[2].w['rise_edit'].text())
    check("save: PML gear dialog widgets included",
          any(k.startswith('cbx_pml_voltage_range') for k in saved), [k for k in saved if 'pml' in k][:5])

    # Discharge restore round-trips a fixed-range mode
    ld2.set_fixed_mode('CCL', 2.0); ld2.turn_on()
    mc.discharge.on_ms = mc.discharge.off_ms = 30
    mc.ui.chkbox_manual_control_auto_discharge.setChecked(True)
    mc.ac_source_request = 2
    mc.ac_source_request_service()
    import time
    t0 = time.time()
    while mc.discharge.running and time.time() - t0 < 5:
        app.processEvents(); time.sleep(0.01)
    check("discharge: CH2 back to CCL 2.0 A and ON after CCH pulses",
          ld2.active_channel_mode == 'CCL' and ld2._ch['iout'] == 2.0 and ld2._ch['load_on'],
          (ld2.active_channel_mode, ld2._ch['iout'], ld2._ch['load_on']))

    window.grab().save(str(ROOT / "scripts" / "verify_eload_grid.png"))
    window.close()


if __name__ == "__main__":
    test_specs_and_driver()
    test_ui()
    failed = [n for n, ok in results if not ok]
    OUT.write(f"\n{len(results) - len(failed)}/{len(results)} passed\n")
    sys.exit(1 if failed else 0)
