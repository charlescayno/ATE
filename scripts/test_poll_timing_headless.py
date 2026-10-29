"""Headless checks for Steady-State Poll defaults (no Qt/GPIB imports).

Run from repo root: python scripts/test_poll_timing_headless.py
"""
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLL_PY = ROOT / "psu_tests" / "test_steady_state_poll_2port_waveform.py"
FLOW_PY = ROOT / "page_controls" / "test_sequence_flow_text.py"


def _class_constant(module_path: Path, class_name: str, const_name: str):
    tree = ast.parse(module_path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Name) and target.id == const_name:
                            return eval(compile(ast.Expression(item.value), "<ast>", "eval"))
    raise KeyError(f"{class_name}.{const_name} in {module_path}")


def sample_count_for(interval_s, duration_s) -> int:
    import math

    interval = float(interval_s)
    duration = float(duration_s)
    if interval <= 0 or duration <= 0:
        return 1
    return int(math.floor((duration + 1e-9) / interval)) + 1


def effective_integration_s(soak_integration_s, poll_interval_s) -> float:
    soak = float(soak_integration_s or 0)
    poll = float(poll_interval_s or 0)
    return max(max(soak, 0), max(poll, 0))


def main() -> int:
    errors = []

    def check(label: str, ok: bool, detail=""):
        if ok:
            print(f"OK  {label}")
        else:
            print(f"FAIL {label} {detail}")
            errors.append(label)

    interval = _class_constant(POLL_PY, "SteadyStatePollWaveformTest_2Port", "POLL_INTERVAL_DEFAULT_S")
    duration = _class_constant(POLL_PY, "SteadyStatePollWaveformTest_2Port", "POLL_DURATION_DEFAULT_S")

    check("poll interval default 300 s", interval == 300.0, interval)
    check("poll duration default 1200 s", duration == 1200.0, duration)
    check("5 samples per point", sample_count_for(interval, duration) == 5)
    check("effective integration 0+300", effective_integration_s(0, interval) == 300.0)

    src = POLL_PY.read_text(encoding="utf-8")
    check("effective_integration_s in poll test", "def effective_integration_s" in src)
    check("setup_equipment override", "def setup_equipment(self):" in src)
    check("_configure_poll_power_meter_integration", "_configure_poll_power_meter_integration" in src)

    flow = FLOW_PY.read_text(encoding="utf-8")
    check("flow imports poll class", "SteadyStatePollWaveformTest_2Port" in flow)
    check("verify expects 300/1200", "300.0" in (ROOT / "scripts" / "verify_steady_state_poll_2port_waveform.py").read_text())

    scope = _class_constant(
        POLL_PY, "SteadyStatePollWaveformTest_2Port", "POLL_DEFAULT_SCOPE_CHANNELS",
    )
    ch1 = scope[1]
    check("scope CH1 enabled", ch1.get("enabled") is True)
    check("scope CH1 VDS_PRI", ch1.get("name") == "VDS_PRI")
    check("scope CH1 derating 1700 V", ch1.get("derating") == 1700.0)
    check("scope CH1 MAXimum", ch1.get("measurements") == ["MAXimum"])

    if errors:
        print(f"\n{len(errors)} failed")
        return 1
    print("\nPASS poll timing + scope defaults (headless, AST)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
