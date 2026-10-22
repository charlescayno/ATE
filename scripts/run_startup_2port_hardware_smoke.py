"""Minimal Startup Waveform 2 Port on real GPIB (smoke: 1 Vin, 1 load point).

Usage (from repo root, conda env active):
  python scripts/run_startup_2port_hardware_smoke.py
  python scripts/run_startup_2port_hardware_smoke.py --auto-confirm   # skip Yes/No (bench still moves)

Watch the PI ATE message boxes on your desktop.
"""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

if os.environ.get("PI_ATE_SIMULATION") == "1":
    print("[ERROR] Unset PI_ATE_SIMULATION for hardware run.")
    sys.exit(2)

from PySide2.QtCore import Qt, QThread, QTimer  # noqa: E402
from PySide2.QtWidgets import (  # noqa: E402
    QApplication,
    QLabel,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from equipment.handler import EquipmentHandler  # noqa: E402
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
from psu_tests.test_object_imports import MessageType  # noqa: E402
from psu_tests.test_startup_2port_waveform import StartupWaveformTest_2Port  # noqa: E402
from psu_tests.test_type import TestTypes  # noqa: E402


class BenchHost(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PI ATE — Startup 2 Port hardware smoke")
        self.run_settings = {"debug": False}
        self.equipment = None
        self._test_thread = None

        central = QWidget()
        layout = QVBoxLayout(central)
        self.status_label = QLabel(
            "Starting…\n\n"
            "If this window stays empty, GPIB scan is still running or a prompt is "
            "behind this window — try Alt+Tab for “Bulk Capacitor” / Yes-No dialogs."
        )
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        self.setCentralWidget(central)
        self.resize(520, 160)

        self.msg_box = QMessageBox(self)
        self._top_flags = self.msg_box.windowFlags() | Qt.WindowStaysOnTopHint

    def set_status(self, text: str):
        self.status_label.setText(text)
        QApplication.processEvents()

    def init_equipment(self):
        self.set_status("Scanning GPIB and assigning roles (1–3 min if addresses are busy)…")
        print("[INFO] Scanning GPIB / assigning equipment roles...", flush=True)
        self.equipment = EquipmentHandler(self)
        aux = getattr(self.equipment, "dc_source_aux", None)
        prim = getattr(self.equipment, "dc_source", None)
        scope = getattr(self.equipment, "oscilloscope", None)
        lines = [
            "Equipment ready. Test starting — respond to pop-up prompts.",
            f"Primary DC: {getattr(prim, 'description', None)}",
            f"Aux DC:     {getattr(aux, 'description', None)}",
            f"Scope:      {getattr(scope, 'description', None)}",
        ]
        self.set_status("\n".join(lines))
        print(f"  dc_source:     {getattr(prim, 'description', None)}", flush=True)
        print(f"  dc_source_aux: {getattr(aux, 'description', None)}", flush=True)
        print(f"  oscilloscope:  {getattr(scope, 'description', None)}", flush=True)

    def msg_box_info(self, title, message, message_type):
        match message_type:
            case MessageType.WARNING:
                self.msg_box.setIcon(QMessageBox.Warning)
            case MessageType.ABORT:
                self.msg_box.setIcon(QMessageBox.Critical)
            case _:
                self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.setTextFormat(Qt.RichText)
        self.msg_box.setText(message)
        self.msg_box.setWindowTitle(title)
        self.msg_box.setStandardButtons(QMessageBox.Ok)
        self.msg_box.setWindowFlags(self._top_flags)
        self.msg_box.raise_()
        self.msg_box.activateWindow()
        self.msg_box.exec_()

    def msg_box_pick(self, title, message):
        self.msg_box.setTextFormat(Qt.RichText)
        self.msg_box.setIcon(QMessageBox.Warning)
        self.msg_box.setText(message)
        self.msg_box.setWindowTitle(title)
        self.msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.msg_box.setWindowFlags(self._top_flags)
        self.msg_box.raise_()
        self.msg_box.activateWindow()
        return self.msg_box.exec_()


class _TestItem:
    def __init__(self, parent, conditions):
        self.parent = parent
        self.test_type_index = TestTypes.index(StartupWaveformTest_2Port)
        self.test_conditions = conditions


def _build_conditions(*, vin_v: float, coupling: str) -> TestConditions:
    mode = "Option A: Proportional Sync (Both Ports 100% -> 10%)"
    freq = 60 if coupling.upper() == "AC" else 0
    return TestConditions(
        name=StartupWaveformTest_2Port.title,
        nominal_output_voltage_V=5,
        nominal_load_current_A=4.5,
        max_load_current_A=4.5,
        line_range=LineRange(name="SMOKE", vin_freq=[[vin_v, freq]], custom=True),
        load_range=LoadRange(name="SMOKE", load_range_pct=[100], custom=True),
        soak_time=SoakTime(name="SMOKE", initial=1, line=1, load=1, integration=1),
        general_options=GeneralOptions(coupling=coupling),
        usbpd_options=USBPDOptions(),
        i2c_test_parameters=I2CTestParameters(
            params=[12.0, 2.0, 0.0, "100", 1.0, 1.0, 0, 25.0, 1, 0, 10.0],
            cbx_params=[mode, "Yes", "None (Fully Automated)", "No"],
        ),
        unit_id="SMOKE",
        ambient_temp=25.0,
        scope_channels={
            1: {"enabled": True, "name": "Primary Vds", "derating": 650, "measurements": ["MAXimum"]},
            2: {"enabled": True, "name": "Ids", "measurements": ["MAXimum"]},
            3: {"enabled": False, "name": ""},
            4: {"enabled": False, "name": ""},
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--auto-confirm",
        action="store_true",
        help="PI_ATE_AUTO_CONFIRM=1 (auto Yes; still drives real hardware)",
    )
    parser.add_argument("--vin", type=float, default=400.0, help="Input voltage setpoint (default 400 for Magna DC)")
    parser.add_argument(
        "--coupling",
        choices=["DC", "AC"],
        default="DC",
        help="DC uses Magna/HVDC; AC needs an AC source in Setup",
    )
    args = parser.parse_args()
    if args.auto_confirm:
        os.environ["PI_ATE_AUTO_CONFIRM"] = "1"

    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass

    app = QApplication.instance() or QApplication(sys.argv)
    host = BenchHost()
    host.show()
    host.raise_()
    host.activateWindow()

    out = os.path.join(tempfile.gettempdir(), "pi_ate_startup_smoke")
    os.makedirs(out, exist_ok=True)
    final_status = {"value": None}

    def preflight() -> str | None:
        eq = host.equipment
        from equipment.dc_source import is_magna_hvdc

        if args.coupling.upper() == "AC" and getattr(eq, "ac_source", None) is None:
            return "No AC source — use --coupling DC for Magna-only bench, or assign AC in Setup."
        if args.coupling.upper() == "DC" and getattr(eq, "dc_source", None) is None:
            return "No DC source (Magna) assigned."
        if args.coupling.upper() == "DC" and not is_magna_hvdc(eq.dc_source):
            print("[WARN] Primary DC is not Magna HVDC; bulk-cap ramp behavior may differ.", flush=True)
        if getattr(eq, "dc_source_aux", None) is None:
            return "No aux DC (HMP) — assign HMP2030 as Aux DC in Equipment Setup."
        try:
            eq.check_scope_availability(get_default=True)
        except Exception:
            pass
        if getattr(eq, "oscilloscope", None) is None:
            return (
                "No oscilloscope — connect scope (GPIB/USB) and assign in Setup, "
                "or close other apps holding the scope address."
            )
        return None

    def start_test_thread():
        err = preflight()
        if err:
            host.set_status(f"Cannot start:\n{err}")
            print(f"[ERROR] {err}", flush=True)
            QTimer.singleShot(100, app.quit)
            return

        item = _TestItem(host, _build_conditions(vin_v=args.vin, coupling=args.coupling))
        test = StartupWaveformTest_2Port(item)
        test.output_folder_path = out

        thread = QThread()
        host._test_thread = thread
        test.moveToThread(thread)

        def on_message(title, message, message_type):
            host.msg_box_info(title, message, message_type)
            test.message_closed = True

        test.message.connect(on_message)

        def on_status(status):
            final_status["value"] = status
            print(f"[STATUS] {status}", flush=True)
            host.set_status(f"Test status: {status}\nOutput: {out}")
            if status in (
                TestStatus.COMPLETE,
                TestStatus.STOPPED,
                TestStatus.FAILED,
                TestStatus.SKIPPED,
            ):
                thread.quit()

        test.status_update.connect(on_status)
        thread.started.connect(test.run)
        thread.finished.connect(app.quit)

        print(
            f"[INFO] Startup smoke: {args.vin:g} V {args.coupling}, 100% load, 1 point.",
            flush=True,
        )
        print(f"[INFO] Output folder: {out}", flush=True)
        thread.start()

    def bootstrap():
        try:
            host.init_equipment()
        except Exception as exc:
            host.set_status(f"Equipment init failed:\n{exc}")
            print(f"[ERROR] {exc}", flush=True)
            QTimer.singleShot(100, app.quit)
            return
        start_test_thread()

    QTimer.singleShot(0, bootstrap)
    code = app.exec_()
    status = final_status["value"]
    if status == TestStatus.COMPLETE:
        print(f"[OK] Complete. Workbook under {out}")
        return 0
    print(f"[FAIL] Ended with status {status!r}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
