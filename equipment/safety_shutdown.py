"""Best-effort emergency shutdown for all bench outputs."""
from __future__ import annotations


def _unique(items):
    seen = set()
    for item in items:
        if item is None or id(item) in seen:
            continue
        seen.add(id(item))
        yield item


def turn_all_outputs_off(equipment, log_prefix="[STOP TEST]"):
    """Turn off every detected/assigned source and electronic load.

    Each device is attempted independently so one VISA error cannot prevent
    the remaining bench equipment from being switched off.
    """
    failures = []

    ac_sources = list(getattr(equipment, "ac_sources", []) or [])
    ac_sources.append(getattr(equipment, "ac_source", None))
    for source in _unique(ac_sources):
        try:
            source.turn_off()
        except Exception as exc:
            failures.append(("AC source", exc))

    dc_sources = list(getattr(equipment, "dc_sources", []) or [])
    dc_sources.extend(
        (
            getattr(equipment, "dc_source", None),
            getattr(equipment, "dc_source_aux", None),
        )
    )
    for source in _unique(dc_sources):
        try:
            if getattr(source, "is_hmp_series", lambda: False)():
                for channel in range(1, 4):
                    try:
                        source.channel_turn_off(channel)
                    except Exception as exc:
                        failures.append((f"HMP channel {channel}", exc))
            source.turn_off()
        except Exception as exc:
            failures.append(("DC source", exc))

    loads = list(getattr(equipment, "e_loads", []) or [])
    loads.extend(
        getattr(equipment, f"electronic_load_{channel}", None)
        for channel in range(1, 7)
    )
    for load in _unique(loads):
        try:
            load.turn_off()
        except Exception as exc:
            failures.append(("electronic load", exc))

    scope = getattr(equipment, "oscilloscope", None)
    if scope is not None:
        try:
            scope.stop()
        except Exception as exc:
            failures.append(("oscilloscope", exc))

    if failures:
        for name, exc in failures:
            print(f"{log_prefix} {name} OFF failed: {exc}")
    else:
        print(f"{log_prefix} All sources and loads are OFF; scope is stopped.")
    return failures
