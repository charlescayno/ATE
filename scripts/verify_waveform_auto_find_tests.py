"""Smoke-test shared waveform auto-find (used by Eff 2P + Steady-State Capture find_trigger())."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from equipment.scope_auto_trigger import find_trigger_for_waveform_test
from equipment.simulated_handler import SimulatedEquipmentHandler, VirtualCircuitState
from scripts.verify_scope_auto_find import _SequenceScope, _check_sequence


def _scope(vin: float = 115.0):
    state = VirtualCircuitState()
    state.vin = vin
    inner = SimulatedEquipmentHandler(parent=None).oscilloscope
    inner.state = state
    return _SequenceScope(inner)


def main():
    errors = []
    scope = _scope()
    lvl = find_trigger_for_waveform_test(scope, 1, 2.0)
    ok, ev = _check_sequence(scope.events)
    if not ok:
        errors.append(f"CH1 sequence: {ev}")
    if not (isinstance(lvl, float) and lvl > 0):
        errors.append(f"CH1 level: {lvl}")

    if errors:
        for e in errors:
            print("FAIL", e)
        return 1
    print("OK find_trigger_for_waveform_test (Eff 2P + Steady-State Capture delegate here)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
