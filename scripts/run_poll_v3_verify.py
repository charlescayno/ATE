"""Run poll v3 checks: static + full verify when Qt works."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def static_checks() -> list[str]:
    errors: list[str] = []
    poll_py = (ROOT / "psu_tests" / "test_steady_state_poll_2port_waveform.py").read_text(
        encoding="utf-8"
    )
    defs_py = (ROOT / "psu_tests" / "definitions.py").read_text(encoding="utf-8")
    add_py = (ROOT / "page_controls" / "add_test.py").read_text(encoding="utf-8")

    def req(name: str, ok: bool, detail: str = ""):
        if ok:
            print(f"OK  {name}")
        else:
            print(f"FAIL {name} {detail}")
            errors.append(name)

    req("integrate before read helper", "_integrate_source_pin_before_read" in poll_py)
    acquire = poll_py.split("def _acquire_operating_point")[1].split("def _link_capture")[0]
    req("integrate called in acquire", "_integrate_source_pin_before_read(" in acquire)
    req("no idle wait in acquire", "_wait_for_scheduled_poll_sample(" not in acquire)
    req("effective uses poll param", "poll_interval_s" in poll_py.split("effective_integration_s")[1][:400])
    req("gather flag", "source_pin_integration_done" in defs_py)
    req("UI label", "Pin integration per sample (s)" in add_py)
    req("ETA n * per only", "return n * per" in poll_py)
    return errors


def run_full_verify() -> tuple[int, str]:
    env = os.environ.copy()
    env["PI_ATE_AUTO_CONFIRM"] = "1"
    env.setdefault("QT_QPA_PLATFORM", "offscreen")
    cmd = [sys.executable, str(ROOT / "scripts" / "verify_steady_state_poll_2port_waveform.py")]
    proc = subprocess.run(
        cmd,
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out


def main() -> int:
    os.chdir(ROOT)
    print("=== Poll v3 static checks ===")
    errors = static_checks()
    print("\n=== Full simulated verify ===")
    code, out = run_full_verify()
    if out.strip():
        print(out)
    else:
        print(f"(no output, exit code {code})")
    if code == 0:
        print("OK full verify")
    else:
        errors.append(f"full verify exit {code}")
    if errors:
        print(f"\nFAILED: {len(errors)}")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("\nALL PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
