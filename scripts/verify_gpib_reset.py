"""Verify Reset All GPIB resets GPIB devices only and leaves outputs OFF."""
import os
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))


class FakeInstrument:
    def __init__(self, address, *, reset_supported=True):
        self.address = address
        self.reset_calls = 0
        self.off_calls = 0
        if not reset_supported:
            self.reset = None

    def reset(self):
        self.reset_calls += 1

    def turn_off(self):
        self.off_calls += 1

    def stop(self):
        pass


def main() -> int:
    from equipment.gpib_reset import reset_all_gpib

    ac = FakeInstrument("GPIB0::1::INSTR")
    dc = FakeInstrument("GPIB0::30::INSTR")
    load = FakeInstrument("GPIB0::8::INSTR")
    meter = FakeInstrument("GPIB0::12::INSTR")
    scope = FakeInstrument("TCPIP::192.168.1.100::INSTR")
    equipment = SimpleNamespace(
        ac_sources=[ac],
        dc_sources=[dc],
        e_loads=[load],
        power_meters=[meter],
        oscilloscopes=[scope],
        ac_source=ac,
        dc_source=dc,
        dc_source_aux=None,
        oscilloscope=scope,
        **{f"electronic_load_{n}": load if n == 1 else None for n in range(1, 7)},
    )

    reset_count, skipped_count, failures = reset_all_gpib(equipment, "[VERIFY]")
    errors = []
    if (reset_count, skipped_count, len(failures)) != (4, 0, 0):
        errors.append(
            f"unexpected result: reset={reset_count}, skipped={skipped_count}, "
            f"failed={len(failures)}"
        )
    if any(device.reset_calls != 1 for device in (ac, dc, load, meter)):
        errors.append("not every GPIB device was reset exactly once")
    if scope.reset_calls:
        errors.append("TCPIP oscilloscope should not be reset by Reset All GPIB")
    if any(device.off_calls < 2 for device in (ac, dc, load)):
        errors.append("outputs were not forced OFF before and after reset")

    if errors:
        print("FAIL Reset All GPIB")
        for error in errors:
            print(f"  {error}")
        return 1
    print("OK Reset All GPIB resets GPIB devices and leaves outputs OFF")
    return 0


if __name__ == "__main__":
    sys.exit(main())
