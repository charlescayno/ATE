"""Auto-find trigger level (sweep until edge trigger stops arming).

Algorithm matches psu_tests find_trigger (Efficiency 2P waveform / Vds steady state).
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from time import sleep
from typing import Callable, Optional


@dataclass
class AutoFindTriggerSettings:
    trigger_delta: float = 0.5
    max_steps: int = 30
    auto_settle_s: float = 1.0
    step_settle_s: float = 0.5
    final_settle_s: float = 6.0


def _sleep(seconds: float, pump_events: Optional[Callable[[], None]] = None):
    if seconds <= 0:
        return
    if pump_events is None:
        sleep(seconds)
        return
    import time as _time

    deadline = _time.time() + seconds
    while _time.time() < deadline:
        pump_events()
        _time.sleep(min(0.05, max(0.0, deadline - _time.time())))


def _set_trigger_mode(scope, mode: str):
    if hasattr(scope, "trigger_mode"):
        scope.trigger_mode(mode)
    elif hasattr(scope, "set_trigger_mode"):
        scope.set_trigger_mode(mode)


def _read_channel_max(scope, channel: int) -> float:
    labels, values = scope.get_measure(channel)
    try:
        max_value = float(values[0]) if values and values[0] is not None else 10.0
        if math.isnan(max_value):
            max_value = 10.0
    except (ValueError, TypeError):
        max_value = 10.0
    return float(f"{max_value:.4f}")


def find_trigger_level(
    scope,
    channel: int,
    edge: str = "POS",
    settings: Optional[AutoFindTriggerSettings] = None,
    *,
    pump_events: Optional[Callable[[], None]] = None,
    on_progress: Optional[Callable[[str], None]] = None,
) -> float:
    """Raise trigger level until acquisition stops triggering; back off one delta step."""
    cfg = settings or AutoFindTriggerSettings()

    def progress(msg: str):
        if on_progress:
            on_progress(msg)

    scope.run_single()
    _set_trigger_mode(scope, "AUTO")
    _sleep(cfg.auto_settle_s, pump_events)
    _set_trigger_mode(scope, "NORM")

    try:
        max_value = _read_channel_max(scope, channel)
        trigger_level = max_value
        scope.edge_trigger(channel, trigger_level, edge)
        progress(f"Start CH{channel} @ {trigger_level:g} V")

        scope.run_single()
        _sleep(cfg.auto_settle_s, pump_events)
        trigger_status = scope.trigger_status()

        steps = 0
        while trigger_status == 1 and steps < cfg.max_steps:
            steps += 1
            trigger_level += cfg.trigger_delta
            scope.edge_trigger(channel, trigger_level, edge)
            progress(f"Step {steps}: {trigger_level:g} V")
            scope.run_single()
            _sleep(cfg.step_settle_s, pump_events)
            trigger_status = scope.trigger_status()

        trigger_level -= cfg.trigger_delta
        scope.edge_trigger(channel, trigger_level, edge)
        progress(f"Locked CH{channel} @ {trigger_level:g} V")
        _sleep(cfg.final_settle_s, pump_events)
        return trigger_level
    except Exception as exc:
        print(f"[Warning] find_trigger_level error on CH{channel}: {exc}")
        return 10.0
