"""Verify Manual Control power-meter range controls and reset-all action."""
import os
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))


class FakePowerMeter:
    def __init__(self):
        self.calls = []

    def auto_range_enable(self, enabled=True):
        self.calls.append(("auto", enabled))

    def voltage_auto_range_enable(self, enabled=True):
        self.calls.append(("v_auto", enabled))

    def current_auto_range_enable(self, enabled=True):
        self.calls.append(("i_auto", enabled))

    def set_voltage_range(self, value):
        self.calls.append(("voltage", value))

    def set_current_range(self, value):
        self.calls.append(("current", value))


def main() -> int:
    from PySide2.QtWidgets import QApplication, QComboBox
    from page_controls import manual_pm_range

    app = QApplication.instance() or QApplication(sys.argv)
    ui = SimpleNamespace()
    for prefix in ("pms", "pml"):
        for kind in ("voltage", "current"):
            combo = QComboBox()
            combo.addItems(["AUTO", "10 mA"])
            setattr(ui, f"cbx_{prefix}_{kind}_range", combo)
    for channel in range(2, 5):
        for kind, fixed in (("voltage", "300V"), ("current", "20A")):
            combo = QComboBox()
            combo.addItems(["AUTO", fixed])
            setattr(ui, f"cbx_pml_{kind}_range_{channel}", combo)

    source = FakePowerMeter()
    loads = [FakePowerMeter() for _ in range(4)]
    equipment = SimpleNamespace(
        power_meter_source=source,
        **{f"power_meter_load_{n}": loads[n - 1] for n in range(1, 5)},
        **{f"power_meter_load_{n}": None for n in range(5, 7)},
    )
    handler = SimpleNamespace(
        ui=ui,
        equipment=equipment,
        power_meter_source=source,
        power_meter_load=loads[0],
        save_manual_settings=lambda: None,
    )

    manual_pm_range.wire(handler)
    errors = []
    if source.calls or any(pm.calls for pm in loads):
        errors.append("wiring the combos must not send range commands")
    if ui.cbx_pms_voltage_range.itemText(1) != "300V":
        errors.append("source voltage fixed-range label")
    if ui.cbx_pms_current_range.itemText(1) != "20A":
        errors.append("source current fixed-range label")

    ui.cbx_pms_voltage_range.setCurrentIndex(1)
    ui.cbx_pms_current_range.setCurrentIndex(1)
    if ("v_auto", False) not in source.calls or ("voltage", 300.0) not in source.calls:
        errors.append("source fixed voltage command")
    if ("i_auto", False) not in source.calls or ("current", 20.0) not in source.calls:
        errors.append("source fixed current command")

    manual_pm_range.reset_all_to_auto_range(handler)
    if any(("auto", True) not in pm.calls for pm in [source] + loads):
        errors.append("reset-all did not reach every assigned power meter")
    if any(
        combo.currentIndex() != 0
        for _channel, v_combo, i_combo in manual_pm_range._channel_range_combos(handler)
        for combo in (v_combo, i_combo)
    ):
        errors.append("reset-all did not set every combo to AUTO")

    if errors:
        print("FAIL Manual Control PM ranges")
        for error in errors:
            print(f"  {error}")
        return 1
    print("OK Manual Control PM ranges and reset-all")
    return 0


if __name__ == "__main__":
    sys.exit(main())
