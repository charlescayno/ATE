"""Smoke-test test sequence flow copy for waveform 2-port tests."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from page_controls.test_sequence_flow_text import (  # noqa: E402
    STARTUP_WAVEFORM_2PORT_TITLE,
    STEADY_STATE_WAVEFORM_2PORT_TITLE,
    build_flow_text_for_title,
)
def main() -> int:
    errors = []
    su = build_flow_text_for_title(
        STARTUP_WAVEFORM_2PORT_TITLE,
        user_prompts="Per-Capture Only",
        capture_timeout_s=10.0,
        dual_load_mode="Option A",
        discharge_pulses=2,
    )
    ssw = build_flow_text_for_title(
        STEADY_STATE_WAVEFORM_2PORT_TITLE,
        user_prompts="None (Fully Automated)",
        dual_load_mode="Option C",
    )
    for name, text, needles in (
        ("startup", su, ("RUN SINGLE", "HMP", "10 s", "→", "Option A")),
        ("steady-state", ssw, ("soak", "RUN SINGLE", "Option C", "→")),
    ):
        if not text:
            errors.append(f"{name}: empty")
            continue
        for n in needles:
            if n not in text:
                errors.append(f"{name}: missing {n!r}")

    skipped = build_flow_text_for_title(
        STARTUP_WAVEFORM_2PORT_TITLE,
        user_prompts="None (Fully Automated)",
    )
    if skipped and "skipped" not in skipped.lower():
        errors.append("startup fully automated should mark skipped USER steps")

    if errors:
        print("FAIL")
        for e in errors:
            print(" ", e)
        return 1
    print("OK test sequence flow text")
    return 0


if __name__ == "__main__":
    sys.exit(main())
