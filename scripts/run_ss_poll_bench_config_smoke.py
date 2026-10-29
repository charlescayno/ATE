"""Run Steady-State Poll 2 Port with TST-326-style bench settings (simulation first).

Screenshot-aligned defaults:
  750 VDC custom line, 48 V / 4.5 A CH1, 20 V / 0.1 A CH2 (Option C),
  initial soak 5 s, CH1 VDS_PRI, poll interval/duration from env or 60 s / 120 s.
"""
from __future__ import annotations

import os
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path[:] = [str(ROOT)] + [
    p for p in sys.path[1:]
    if p and "PI_ATE_Marketing_Release" not in p.replace("/", os.sep)
]
os.chdir(ROOT)
os.environ.setdefault("PI_ATE_AUTO_CONFIRM", "1")

# Fast sim unless PI_ATE_POLL_REAL_SLEEP=1
if os.environ.get("PI_ATE_POLL_REAL_SLEEP", "").strip() not in ("1", "yes", "true"):
    time.sleep = lambda _s: None  # noqa: A001

from PySide2.QtWidgets import QApplication  # noqa: E402

app = QApplication.instance() or QApplication(sys.argv)

from psu_tests.definitions import (  # noqa: E402
    GeneralOptions,
    I2CTestParameters,
    LineRange,
    LoadRange,
    SoakTime,
    TestConditions,
    TestStatus,
    USBPDOptions,
)
from psu_tests.test_steady_state_poll_2port_waveform import SteadyStatePollWaveformTest_2Port  # noqa: E402
from psu_tests.test_type import TestTypes  # noqa: E402
from equipment.simulated_handler import SimulatedEquipmentHandler  # noqa: E402

POLL = SteadyStatePollWaveformTest_2Port
OPTION_C = "Option C: Fixed Aux / Swept Main (Port 2 Fixed Load)"


def _float_env(name: str, default: float) -> float:
    try:
        return float(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


class FakeParent:
    def __init__(self):
        self.run_settings = {"debug": False}
        self.equipment = SimulatedEquipmentHandler(self)


class FakeItem:
    def __init__(self, parent, conditions):
        self.parent = parent
        self.test_type_index = TestTypes.index(POLL)
        self.test_conditions = conditions


def build_conditions() -> TestConditions:
    poll_iv = _float_env("PI_ATE_POLL_INTERVAL_S", 30.0)
    poll_n = _float_env("PI_ATE_POLL_SAMPLES", 3.0)
    params = [20.0, 0.1, 0.1, 0.0, 1.0, 1.0, 2.0, 25.0, 1.0, 1.0, poll_iv, poll_n]
    scope = dict(POLL.POLL_DEFAULT_SCOPE_CHANNELS)
    return TestConditions(
        name=POLL.title,
        nominal_output_voltage_V=48.0,
        nominal_load_current_A=4.5,
        max_load_current_A=4.5,
        line_range=LineRange(name="750VDC", vin_freq=[[750, 0]], custom=True),
        load_range=LoadRange(name="100pct", load_range_pct=[100], custom=True),
        soak_time=SoakTime(name="bench", initial=5, line=0, load=0, integration=0),
        general_options=GeneralOptions(
            measure_ripple=False,
            use_eload_data=False,
            eload_type="CC",
            load_direction="Downward",
            coupling="DC",
        ),
        usbpd_options=USBPDOptions(),
        i2c_test_parameters=I2CTestParameters(
            params=params,
            cbx_params=[OPTION_C, "Yes", "None (Fully Automated)", "No"],
        ),
        unit_id="TST-326",
        ambient_temp=25.0,
        scope_channels=scope,
    )


def main() -> int:
    statuses: list = []
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as out_dir:
        test = POLL(FakeItem(FakeParent(), build_conditions()))
        test.status_update.connect(statuses.append)
        test.output_folder_path = out_dir
        print(f"[SMOKE] Output: {out_dir}")
        print(f"[SMOKE] Poll wait={test.poll_interval_s}s samples={test.poll_samples_n}")
        print(f"[SMOKE] Samples per point: {test._sample_count()}")
        try:
            test.run()
        except Exception as exc:
            print(f"[SMOKE] FAIL run raised: {type(exc).__name__}: {exc}")
            return 1
        if TestStatus.COMPLETE not in statuses:
            print(f"[SMOKE] FAIL statuses: {statuses}")
            return 1
        if not test.captured_records:
            errors.append("no captured_records")
        if not os.path.isfile(test.data_file_path):
            errors.append(f"missing workbook {test.data_file_path}")
        n = test.captured_records[0].get("n_samples") if test.captured_records else 0
        expected = test._sample_count()
        if n != expected:
            errors.append(f"n_samples {n} != expected {expected}")
        if errors:
            print("[SMOKE] FAIL", "; ".join(errors))
            return 1
        print(f"[SMOKE] PASS complete — {test.data_filename}, samples={n}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
