"""Assert Steady-State Waveform 2 Port tc_default matches TST-326 test plan."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from psu_tests.definitions import TestConditionSettings  # noqa: E402 — anchor psu_tests to this repo
from psu_tests.test_type import TestTypes, get_test_title_list  # noqa: E402
from psu_tests.test_efficiency_2port_waveform import EfficiencyWaveformTest_2Port  # noqa: E402


def main() -> int:
    errors = []
    if TestTypes[0] is not EfficiencyWaveformTest_2Port:
        errors.append(f"TestTypes[0] = {TestTypes[0].title!r}, expected waveform")
    if get_test_title_list()[0] != EfficiencyWaveformTest_2Port.title:
        errors.append("Waveform is not first in test type dropdown list")

    tc = EfficiencyWaveformTest_2Port.tc_default
    checks = [
        (tc.nominal_output_voltage_V == 48.0, "nominal V 48"),
        (tc.nominal_load_current_A == 3.0, "nominal I 3"),
        (tc.line_range.name == "TST-326 HVDC", "line range name"),
        (tc.line_range.vin_freq == [[750.0, 50.0], [800.0, 50.0], [860.0, 50.0]], "vin list"),
        (tc.load_range.name == "Full Load", "load range"),
        (tc.soak_time.name == "TST-326", "soak name"),
        (tc.soak_time.initial_soak == 5.0, "initial soak"),
        (tc.general_options.coupling == "DC", "DC coupling"),
        (tc.scope_channels[1]["name"] == "VDS_SR", "scope CH1 name"),
        (tc.scope_channels[1]["derating"] == 150.0, "derating"),
        (str(tc.i2c_test_parameters.cbx_param[0]).startswith("Option C"), "Option C mode"),
    ]
    for ok, label in checks:
        if not ok:
            errors.append(f"tc_default: {label}")

    idx = TestTypes.index(EfficiencyWaveformTest_2Port)
    wf = TestConditionSettings().test_condition_list[idx]
    if wf.line_range is not tc.line_range:
        errors.append("TestConditionSettings line_range not shared with tc_default")

    if errors:
        print("FAIL")
        for e in errors:
            print(" ", e)
        return 1
    print("OK TST-326 Steady-State Waveform 2 Port defaults")
    return 0


if __name__ == "__main__":
    sys.exit(main())
