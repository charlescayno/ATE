"""Verify STOP TESTS forces every simulated bench output off."""
import os
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
os.environ["PI_ATE_SIMULATION"] = "1"
os.environ["PI_ATE_AUTO_CONFIRM"] = "1"


def main() -> int:
    from PySide2.QtWidgets import QApplication
    from psu_tests.definitions import test_control_flags

    app = QApplication.instance() or QApplication(sys.argv)
    namespace = runpy.run_path(str(ROOT / "main.py"), run_name="__stop_all_verify__")
    window = namespace["MainWindow"]()
    window.msg_box_info = lambda *_args, **_kwargs: None
    add = window.add_test_pagehandler
    equipment = window.equipment

    for source in getattr(equipment, "ac_sources", []):
        source.turn_on()
    for source in getattr(equipment, "dc_sources", []):
        if getattr(source, "is_hmp_series", lambda: False)():
            for channel in range(1, 4):
                source.channel_turn_on(channel)
        else:
            source.turn_on()
    for load in getattr(equipment, "e_loads", []):
        load.turn_on()

    add.test_plan_update_timer.start(1000)
    add.stop_tests()
    app.processEvents()

    errors = []
    if not test_control_flags.get("StopTest"):
        errors.append("StopTest flag was not set")
    if add.test_plan_update_timer.isActive():
        errors.append("test-plan timer is still active")
    if any(source.state.ac_on for source in getattr(equipment, "ac_sources", [])):
        errors.append("an AC source remains on")
    for source in getattr(equipment, "dc_sources", []):
        if getattr(source, "is_hmp_series", lambda: False)():
            if any(ch["on"] for ch in source._hmp_channels.values()):
                errors.append("an HMP channel remains on")
        elif source.output_status:
            errors.append("a DC source remains on")
    if any(load._ch["load_on"] for load in getattr(equipment, "e_loads", [])):
        errors.append("an electronic load remains on")

    if errors:
        print("FAIL STOP TESTS safety shutdown")
        for error in errors:
            print(f"  {error}")
        return 1
    print("OK STOP TESTS turns off all simulated bench outputs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
