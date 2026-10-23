"""Auto-find trigger level (sweep until edge trigger stops arming).

Sequence:
  1. edge_trigger(ch, 0 V, POS)
  2. AUTO
  3. run_single()
  4. get_measure(ch) -> Max seed
  5. NORM
  6. sweep: edge @ Max, run_single, raise level until not triggering, back off one delta
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


def waveform_test_auto_find_settings(trigger_delta: float = 0.5) -> AutoFindTriggerSettings:
    """Default settle times for PSU waveform tests (Eff 2P, Steady-State Capture, etc.)."""
    return AutoFindTriggerSettings(
        trigger_delta=trigger_delta,
        auto_settle_s=1.0,
        step_settle_s=0.5,
        final_settle_s=6.0,
    )


def find_trigger_for_waveform_test(
    scope,
    channel: int,
    trigger_delta: float = 0.5,
    edge: str = "POS",
    *,
    pump_events: Optional[Callable[[], None]] = None,
    on_progress: Optional[Callable[[str], None]] = None,
    check_abort: Optional[Callable[[], None]] = None,
) -> float:
    """Auto-find for Add Test waveform runs and any test that mirrors FIND_TRIGGER."""
    return find_trigger_level(
        scope,
        channel,
        edge,
        waveform_test_auto_find_settings(trigger_delta),
        pump_events=pump_events,
        on_progress=on_progress,
        check_abort=check_abort,
    )


def find_trigger_level(
    scope,
    channel: int,
    edge: str = "POS",
    settings: Optional[AutoFindTriggerSettings] = None,
    *,
    pump_events: Optional[Callable[[], None]] = None,
    on_progress: Optional[Callable[[str], None]] = None,
    check_abort: Optional[Callable[[], None]] = None,
) -> float:
    """Raise trigger level until acquisition stops triggering; back off one delta step."""
    cfg = settings or AutoFindTriggerSettings()

    def progress(msg: str):
        if on_progress:
            on_progress(msg)

    try:
        scope.edge_trigger(channel, 0.0, edge)
        progress(f"Priming CH{channel} edge @ 0 V")
        _set_trigger_mode(scope, "AUTO")
        scope.run_single()
        _sleep(cfg.auto_settle_s, pump_events)

        max_value = _read_channel_max(scope, channel)
        progress(f"Baseline Max CH{channel}: {max_value:g} V")

        _set_trigger_mode(scope, "NORM")

        trigger_level = max_value
        scope.edge_trigger(channel, trigger_level, edge)
        progress(f"Sweep start CH{channel} @ {trigger_level:g} V")

        scope.run_single()
        _sleep(cfg.auto_settle_s, pump_events)
        trigger_status = scope.trigger_status()

        steps = 0
        while trigger_status == 1 and steps < cfg.max_steps:
            if check_abort:
                check_abort()
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
