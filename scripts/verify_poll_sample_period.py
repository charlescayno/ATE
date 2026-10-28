"""Real-clock check: Time Sampled spacing tracks Poll Interval (simulated reads)."""
import datetime
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from psu_tests.definitions import test_control_flags
from psu_tests.test_steady_state_poll_2port_waveform import SteadyStatePollWaveformTest_2Port

POLL = SteadyStatePollWaveformTest_2Port
INTERVAL_S = 1.0
READ_S = 0.12
N = 4
TOL = 0.35


class TimingProbe(POLL):
    """Exercise wait + read scheduling without bench hardware."""

    def __init__(self):
        self.poll_prev_sampled_dt = None
        self._poll_repeat_read_duration_s = READ_S
        self.poll_row_sampled_dt = None
        self.stamps = []

    def _raise_if_abort(self, *_args):
        return

    def _simulate_read(self):
        time.sleep(READ_S)
        self._poll_repeat_read_duration_s = READ_S

    def run_ticks(self):
        test_control_flags['StopTest'] = False
        test_control_flags['SkipTest'] = False
        interval = INTERVAL_S
        for sample in range(N):
            if sample == 0:
                self.poll_point_start_dt = datetime.datetime.now()
            else:
                self._wait_for_scheduled_poll_sample(interval, 0, 0)
                self._simulate_read()
            self.poll_row_sampled_dt = datetime.datetime.now()
            self.stamps.append(self.poll_row_sampled_dt)
            self.poll_prev_sampled_dt = self.poll_row_sampled_dt


def main() -> int:
    probe = TimingProbe()
    t0 = time.perf_counter()
    probe.run_ticks()
    elapsed = time.perf_counter() - t0

    gaps = []
    for i in range(1, len(probe.stamps)):
        gaps.append((probe.stamps[i] - probe.stamps[i - 1]).total_seconds())

    ok_gaps = all(abs(g - INTERVAL_S) <= TOL for g in gaps)
    expect_min = (N - 1) * (INTERVAL_S - READ_S) + READ_S * N
    ok_total = elapsed >= expect_min * 0.85

    print(f"Poll interval setting: {INTERVAL_S:g} s (simulated read {READ_S:g} s)")
    print(f"Time Sampled gaps (s): {[round(g, 3) for g in gaps]}")
    print(f"Total elapsed: {elapsed:.3f} s")

    if ok_gaps and ok_total:
        print("OK  poll sample period spacing")
        return 0
    print("FAIL poll sample period spacing", ok_gaps, ok_total)
    return 1


if __name__ == "__main__":
    sys.exit(main())
