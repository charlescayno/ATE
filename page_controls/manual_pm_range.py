"""Apply Manual Control power-meter voltage/current range combos to hardware."""
from __future__ import annotations

import re
from typing import TYPE_CHECKING, Literal, Optional

from page_controls import pml_grid

if TYPE_CHECKING:
    from page_controls.manual_control import ManualControlPageHandler

RangeKind = Literal["voltage", "current"]

_UNIT_SCALE = {
    "V": 1.0,
    "MV": 1e-3,
    "KV": 1e3,
    "UA": 1e-6,
    "MA": 1e-3,
    "A": 1.0,
}

# WT500 ranges at crest factor 3.
WT500_VOLTAGE_RANGES = (15, 30, 60, 100, 150, 300, 600, 1000)
WT500_CURRENT_RANGES = (0.5, 1, 2, 5, 10, 20, 40)


def _parse_range_value(text: str) -> Optional[float]:
    raw = (text or "").strip().upper().replace(" ", "")
    if not raw or raw == "AUTO":
        return None
    m = re.match(r"^([\d.]+)\s*(MV|KV|MA|UA|V|A)?$", raw)
    if not m:
        return None
    val = float(m.group(1))
    unit = m.group(2) or ("V" if "V" in raw else "A" if "A" in raw else "V")
    return val * _UNIT_SCALE.get(unit, 1.0)


def _normalize_combo_items(handler: "ManualControlPageHandler") -> None:
    ui = handler.ui
    pairs = [
        (ui.cbx_pms_voltage_range, "300V"),
        (ui.cbx_pms_current_range, "20A"),
        (ui.cbx_pml_voltage_range, "300V"),
        (ui.cbx_pml_current_range, "20A"),
    ]
    for n in pml_grid.CHANNELS:
        if n == 1:
            continue
        sfx = f"_{n}"
        pairs.append((getattr(ui, f"cbx_pml_voltage_range{sfx}"), "300V"))
        pairs.append((getattr(ui, f"cbx_pml_current_range{sfx}"), "20A"))
    for combo, fixed in pairs:
        if combo.count() >= 2 and "10MA" in combo.itemText(1).upper().replace(" ", ""):
            combo.setItemText(1, fixed)


def _pm_for_channel(handler: "ManualControlPageHandler", channel):
    if channel == "source":
        return getattr(handler, "power_meter_source", None)
    n = int(channel)
    if n == 1:
        return getattr(handler, "power_meter_load", None) or getattr(
            handler.equipment, "power_meter_load_1", None
        )
    return getattr(handler.equipment, f"power_meter_load_{n}", None)


def apply_range_combo(
    handler: "ManualControlPageHandler",
    channel,
    combo,
    kind: RangeKind,
) -> None:
    pm = _pm_for_channel(handler, channel)
    if pm is None or _is_poll_skipped(pm):
        return
    text = combo.currentText().strip()
    label = "WT500/PM" if channel == "source" else f"load PM {channel}"
    if _supports_fixed_range(pm) and combo.currentIndex() > 0:
        value = _parse_range_value(text)
        if value is None:
            return
        try:
            if kind == "voltage":
                actual = pm.set_fixed_voltage_range(value)
            else:
                actual = pm.set_fixed_current_range(value)
        except Exception as exc:
            print(f"[Manual Control] {label} {kind} range: {exc}")
            return
        if actual is not None and abs(actual - value) > 1e-6:
            print(f"[Manual Control] {label} {kind} range: asked {text}, meter reports {actual:g}")
            _select_range(combo, False, actual, "V" if kind == "voltage" else "A")
        return
    try:
        if combo.currentIndex() == 0 or text.upper() == "AUTO":
            if kind == "voltage":
                pm.voltage_auto_range_enable(True)
            else:
                pm.current_auto_range_enable(True)
            return
        value = _parse_range_value(text)
        if value is None:
            pm.auto_range_enable(True)
            return
        if kind == "voltage":
            pm.voltage_auto_range_enable(False)
            pm.set_voltage_range(value)
        else:
            pm.current_auto_range_enable(False)
            pm.set_current_range(value)
    except Exception as exc:
        print(f"[Manual Control] {label} {kind} range: {exc}")


def _channel_range_combos(handler: "ManualControlPageHandler"):
    ui = handler.ui
    rows = [("source", ui.cbx_pms_voltage_range, ui.cbx_pms_current_range)]
    for n in pml_grid.CHANNELS:
        sfx = pml_grid._sfx(n)
        rows.append(
            (
                n,
                getattr(ui, f"cbx_pml_voltage_range{sfx}"),
                getattr(ui, f"cbx_pml_current_range{sfx}"),
            )
        )
    return rows


def _is_poll_skipped(pm) -> bool:
    return getattr(pm, "is_poll_skipped", lambda: False)()


def _supports_fixed_range(pm) -> bool:
    return getattr(pm, "supports_fixed_range", lambda: False)()


def _range_label(value: float, unit: str) -> str:
    return f"{value:g} {unit}"


def _set_range_items(combo, values, unit: str) -> None:
    labels = ["AUTO"] + [_range_label(v, unit) for v in values]
    if [combo.itemText(i) for i in range(combo.count())] == labels:
        return
    combo.blockSignals(True)
    try:
        combo.clear()
        combo.addItems(labels)
    finally:
        combo.blockSignals(False)


def _select_range(combo, auto: bool, value, unit: str) -> None:
    """Show the meter's state in the combo without sending anything."""
    idx = 0
    if not auto and value:
        idx = -1
        for i in range(1, combo.count()):
            v = _parse_range_value(combo.itemText(i))
            if v is not None and abs(v - value) < 1e-6:
                idx = i
                break
    combo.blockSignals(True)
    try:
        if idx < 0:
            combo.addItem(_range_label(value, unit))
            idx = combo.count() - 1
        combo.setCurrentIndex(idx)
    finally:
        combo.blockSignals(False)


def sync_from_meters(handler: "ManualControlPageHandler") -> None:
    """Page entry: fill WT500 range lists and show the meter's actual range (queries only)."""
    for channel, vbx, cbx in _channel_range_combos(handler):
        pm = _pm_for_channel(handler, channel)
        if pm is None or _is_poll_skipped(pm) or not _supports_fixed_range(pm):
            continue
        _set_range_items(vbx, WT500_VOLTAGE_RANGES, "V")
        _set_range_items(cbx, WT500_CURRENT_RANGES, "A")
        state = pm.read_range_state()
        if state is None:
            continue
        v_auto, v_range, i_auto, i_range = state
        _select_range(vbx, v_auto, v_range, "V")
        _select_range(cbx, i_auto, i_range, "A")


def _all_assigned_power_meters(handler: "ManualControlPageHandler"):
    eq = handler.equipment
    candidates = [
        getattr(handler, "power_meter_source", None),
        getattr(handler, "power_meter_load", None),
        getattr(eq, "power_meter_source", None),
    ]
    for i in range(1, 7):
        candidates.append(getattr(eq, f"power_meter_load_{i}", None))
    seen: set[int] = set()
    unique = []
    for pm in candidates:
        if pm is None:
            continue
        key = id(pm)
        if key in seen:
            continue
        seen.add(key)
        unique.append(pm)
    return unique


def set_ui_combos_auto(handler: "ManualControlPageHandler") -> None:
    for _channel, vbx, cbx in _channel_range_combos(handler):
        for combo in (vbx, cbx):
            combo.blockSignals(True)
            try:
                if combo.count() > 0:
                    combo.setCurrentIndex(0)
            finally:
                combo.blockSignals(False)


def reset_all_to_auto_range(handler: "ManualControlPageHandler") -> None:
    """Hardware AUTO on every assigned PM; sync gear-dialog combos to AUTO."""
    count = 0
    for pm in _all_assigned_power_meters(handler):
        if _is_poll_skipped(pm):
            continue
        try:
            pm.auto_range_enable(True)
            count += 1
        except Exception as exc:
            dev = getattr(pm, "device_id", None) or getattr(pm, "model", "?")
            print(f"[Manual Control] PM auto range reset ({dev}): {exc}")
    set_ui_combos_auto(handler)
    handler.save_manual_settings()
    print(f"[Manual Control] Reset {count} power meter(s) to AUTO voltage/current range.")


def wire(handler: "ManualControlPageHandler") -> None:
    _normalize_combo_items(handler)
    for channel, vbx, cbx in _channel_range_combos(handler):

        def on_v(_idx, ch=channel, c=vbx, h=handler):
            apply_range_combo(h, ch, c, "voltage")
            h.save_manual_settings()

        def on_i(_idx, ch=channel, c=cbx, h=handler):
            apply_range_combo(h, ch, c, "current")
            h.save_manual_settings()

        vbx.currentIndexChanged.connect(on_v)
        cbx.currentIndexChanged.connect(on_i)
