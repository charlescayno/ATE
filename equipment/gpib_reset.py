"""Reset every detected GPIB instrument without stopping on one failure."""
from __future__ import annotations

from equipment.safety_shutdown import turn_all_outputs_off


def _unique(items):
    seen = set()
    for item in items:
        if item is None or id(item) in seen:
            continue
        seen.add(id(item))
        yield item


def _resource_name(instrument) -> str:
    address = getattr(instrument, "address", "")
    if address:
        return str(address)
    device = getattr(instrument, "device", None)
    return str(getattr(device, "resource_name", "") or "")


def _all_detected_instruments(equipment):
    instruments = []
    for list_name in (
        "ac_sources",
        "dc_sources",
        "e_loads",
        "power_meters",
        "oscilloscopes",
    ):
        instruments.extend(getattr(equipment, list_name, []) or [])
    return _unique(instruments)


def reset_all_gpib(equipment, log_prefix="[GPIB RESET]"):
    """Reset all GPIB instruments and leave every source/load output OFF."""
    turn_all_outputs_off(equipment, log_prefix)
    reset_count = 0
    skipped_count = 0
    failures = []

    for instrument in _all_detected_instruments(equipment):
        resource = _resource_name(instrument)
        if resource and not resource.upper().startswith("GPIB"):
            continue
        label = resource or getattr(instrument, "device_id", repr(instrument))
        try:
            reset = getattr(instrument, "reset", None)
            if callable(reset):
                reset()
            else:
                write = getattr(instrument, "write", None)
                if not callable(write):
                    skipped_count += 1
                    print(f"{log_prefix} {label}: reset unsupported")
                    continue
                write("*RST")
            reset_count += 1
            print(f"{log_prefix} {label}: reset complete")
        except Exception as exc:
            failures.append((label, exc))
            print(f"{log_prefix} {label}: reset failed: {exc}")

    # Some instruments briefly alter output state during *RST.
    turn_all_outputs_off(equipment, log_prefix)
    print(
        f"{log_prefix} Finished: {reset_count} reset, "
        f"{skipped_count} unsupported, {len(failures)} failed."
    )
    return reset_count, skipped_count, failures
