"""Verify simulated Magna DC software slew and source PM readout during ramp.

Run: conda_env\\python.exe scripts\\verify_sim_dc_slew.py
"""
import os
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
os.environ["PI_ATE_SIMULATION"] = "1"
os.environ["PI_ATE_SIM_LINE_INPUT"] = "DC"
os.environ["PI_ATE_SIM_SLEW"] = "1"
os.environ["PI_ATE_SIM_SLEW_VS"] = "8"
os.environ["PI_ATE_AUTO_CONFIRM"] = "1"
os.environ["PI_ATE_SIM_DEMO"] = "1"

OUT = sys.__stdout__
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    line = f"{'PASS' if cond else 'FAIL'}  {name}"
    if detail and not cond:
        line += f"  -> {detail}"
    OUT.write(line + "\n")
    OUT.flush()


def main():
    from PySide2.QtWidgets import QApplication

    app = QApplication.instance() or QApplication(sys.argv)
    g = runpy.run_path(str(ROOT / "main.py"), run_name="__slew__")
    window = g["MainWindow"]()
    window.show()
    ui = window.ui
    ui.stackedWidget.setCurrentWidget(ui.page_manual_control)
    app.processEvents()

    mc = window.manual_control_handler
    mc.start()
    app.processEvents()

    eq = window.equipment
    check("seed: primary DC output OFF at 0 V", eq.dc_source.output_status == 0 and eq.state.vin == 0.0)
    v0 = mc.power_meter_source.voltage
    check("seed: source PM reads ~0 V", v0 < 0.05, v0)

    ui.chkbox_manual_control_dc_source_ramp_enable.setChecked(True)
    ui.lineedit_manual_control_dc_source_slew_rate.setText("8")
    ui.lineedit_manual_control_ac_source_voltage.setText("48")
    app.processEvents()

    from page_controls.manual_control import AC_SOURCE_REQUEST

    mc.set_acsource_flags(AC_SOURCE_REQUEST.ON)
    app.processEvents()
    mc.gpib_update()
    app.processEvents()

    check("ramp: is_ramping after DC ON", getattr(mc, "is_ramping", False))
    check("ramp: output ON while slewing", eq.dc_source.output_status == 1)

    samples = []
    for _ in range(12):
        mc.update_service()
        app.processEvents()
        samples.append(float(mc.power_meter_source.voltage))

    check("ramp: source PM voltage increased", samples[-1] > samples[0] + 0.5, f"{samples[0]:.2f} -> {samples[-1]:.2f}")
    check("ramp: monotonic-ish steps", all(samples[i + 1] >= samples[i] - 0.01 for i in range(len(samples) - 1)), samples)
    check("ramp: reached target or still climbing toward 48 V", samples[-1] >= 4.0, samples[-1])

    for _ in range(40):
        if not getattr(mc, "is_ramping", False):
            break
        mc.update_service()
        app.processEvents()

    v_final = mc.power_meter_source.voltage
    check("ramp: finished near 48 V", abs(v_final - 48.0) < 1.5, v_final)
    check("ramp: is_ramping cleared", not getattr(mc, "is_ramping", False))

    passed = sum(1 for _, ok in results if ok)
    OUT.write(f"\n{passed}/{len(results)} passed\n")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
