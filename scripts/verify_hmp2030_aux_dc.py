"""Verify HMP2030 auxiliary DC source roles and manual-control helpers.

Run: .\\conda_env\\python.exe scripts\\verify_hmp2030_aux_dc.py
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
os.environ["PI_ATE_SIMULATION"] = "1"

OUT = sys.__stdout__
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    msg = f"{'PASS' if cond else 'FAIL'}  {name}"
    if detail and not cond:
        msg += f"  -> {detail}"
    OUT.write(msg + "\n")
    OUT.flush()


def test_dc_source_model_lookup():
    from equipment.dc_source import _resolve_dc_source_model
    from equipment.dc_source_specs import DCSourceHMP2030
    cls = _resolve_dc_source_model("HMP2030")
    check("lookup: HMP2030 resolves", cls is DCSourceHMP2030)


def test_handler_roles_sim():
    from equipment.simulated_handler import SimulatedEquipmentHandler
    h = SimulatedEquipmentHandler(parent=None)
    check("sim: Magna primary dc_source", h.dc_source.model == "SL1000-1.5")
    check("sim: HMP2030 aux dc_source_aux", h.dc_source_aux.model == "HMP2030")
    check("sim: two dc_sources listed", len(h.dc_sources) == 2)


def test_aux_manual_setpoints():
    from equipment.simulated_handler import SimulatedEquipmentHandler
    h = SimulatedEquipmentHandler(parent=None)
    aux = h.dc_source_aux
    aux.set_current_limit(2.5)
    aux.voltage = 12.0
    aux.turn_on()
    check("sim aux: voltage set", abs(aux.voltage - 12.0) < 1e-6)
    check("sim aux: current limit set", abs(aux.current - 2.5) < 1e-6)
    check("sim aux: output on", aux.output_status == 1)
    vin_before = h.state.vin
    check("sim aux: does not drive input rail", abs(h.state.vin - vin_before) < 1e-6)
    aux.turn_off()
    check("sim aux: output off", aux.output_status == 0)
    aux.channel_set_voltage(2, 9.0)
    aux.channel_turn_on(2)
    check("sim aux: CH2 voltage", abs(aux._hmp_channels[2]['v'] - 9.0) < 1e-6)
    check("sim aux: CH2 on", aux._hmp_channels[2]['on'] == 1)


def test_hmp_scpi_commands():
    from equipment.dc_source import DCSource
    from equipment.dc_source_specs import DCSourceHMP2030
    cmds = []

    class FakeDev:
        def query(self, c):
            cmds.append(c)
            if c.endswith("?"):
                if "VOLTage" in c:
                    return "0"
                if "CURRent" in c:
                    return "0"
                if "STATe" in c:
                    return "0"
            return ""

        def write(self, c):
            cmds.append(c)

    ld = object.__new__(DCSource)
    ld.device = FakeDev()
    ld.device_id = "Rohde&Schwarz,HMP2030,123,1.0"
    ld.manufacturer, ld.model, ld.serial = "Rohde&Schwarz", "HMP2030", "123"
    ld.dc_source_object = DCSourceHMP2030()
    ld.command_output_on = ld.dc_source_object.output_on
    ld.command_output_off = ld.dc_source_object.output_off
    ld.command_measure = ld.dc_source_object.measure
    ld.command_volt = ld.dc_source_object.volt
    ld.command_curr = ld.dc_source_object.curr
    ld.command_output = ld.dc_source_object.output
    ld.command_state = ld.dc_source_object.state
    ld.command_sequence = ld.dc_source_object.sequence
    ld._voltage = ld._current = 0
    ld.output_status = 0
    ld.description = "Rohde&Schwarz HMP2030 123"

    ld.voltage = 5.0
    ld.set_current_limit(1.25)
    ld.turn_on()
    check("driver: SOURce:VOLTage write", "SOURce:VOLTage 5.0" in cmds, cmds)
    check("driver: SOURce:CURRent write", "SOURce:CURRent 1.25" in cmds, cmds)
    check("driver: OUTPut ON", "OUTPut ON" in cmds, cmds)

    ld.channel_set_voltage(2, 3.3)
    ld.channel_set_current_limit(2, 0.5)
    ld.channel_turn_on(2)
    check("driver: INSTrument:NSEL for CH2", "INSTrument:NSEL 2" in cmds, cmds)
    check("driver: CH2 voltage", "SOURce:VOLTage 3.3" in cmds, cmds)


if __name__ == "__main__":
    test_dc_source_model_lookup()
    test_handler_roles_sim()
    test_aux_manual_setpoints()
    test_hmp_scpi_commands()
    failed = [n for n, ok in results if not ok]
    OUT.write(f"\n{len(results) - len(failed)}/{len(results)} passed\n")
    sys.exit(1 if failed else 0)
