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


def main() -> int:
    errors = []

    def check(label: str, ok: bool, detail=""):
        if ok:
            print(f"OK  {label}")
        else:
            print(f"FAIL {label} {detail}")
            errors.append(label)

    interval = _class_constant(POLL_PY, "SteadyStatePollWaveformTest_2Port", "POLL_INTERVAL_DEFAULT_S")
    samples = _class_constant(POLL_PY, "SteadyStatePollWaveformTest_2Port", "POLL_SAMPLES_DEFAULT")

    check("poll wait default 30 s", interval == 30.0, interval)
    check("poll samples default 3", samples == 3, samples)

    src = POLL_PY.read_text(encoding="utf-8")
    check("effective_integration_s in poll test", "def effective_integration_s" in src)
    check("read_samples_per_point", "def read_samples_per_point" in src)
    check("prepare_source override", "def prepare_source_power_meter_for_poll_input(self):" in src)

    flow = FLOW_PY.read_text(encoding="utf-8")
    check("flow imports poll class", "SteadyStatePollWaveformTest_2Port" in flow)
    check("verify expects 30/3 defaults", "30.0" in (ROOT / "scripts" / "verify_steady_state_poll_2port_waveform.py").read_text())

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
