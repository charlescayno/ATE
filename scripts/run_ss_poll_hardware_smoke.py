"""Steady-State Poll Waveform 2 Port on real GPIB (screenshot / TST-326 bench defaults).

Usage (repo root, conda env):
  python scripts/run_ss_poll_hardware_smoke.py --auto-confirm
  python scripts/run_ss_poll_hardware_smoke.py --auto-confirm --poll-interval 30 --poll-samples 3
"""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path[:] = [str(ROOT)] + [
    p for p in sys.path[1:]
    if p and "PI_ATE_Marketing_Release" not in p.replace("/", os.sep)
]
os.chdir(ROOT)

if os.environ.get("PI_ATE_SIMULATION") == "1":
    print("[ERROR] Unset PI_ATE_SIMULATION for hardware run.", flush=True)
    sys.exit(2)

from PySide2.QtCore import Qt, QThread, QTimer  # noqa: E402
from PySide2.QtWidgets import QApplication, QLabel, QMainWindow, QMessageBox, QVBoxLayout, QWidget  # noqa: E402

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
from psu_tests.test_steady_state_poll_2port_waveform import SteadyStatePollWaveformTest_2Port  # noqa: E402
from psu_tests.test_type import TestTypes  # noqa: E402

POLL = SteadyStatePollWaveformTest_2Port
OPTION_C = "Option C: Fixed Aux / Swept Main (Port 2 Fixed Load)"


class BenchHost(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PI ATE — SS Poll 2 Port hardware smoke")
        self.run_settings = {"debug": False}
        self.equipment = None
        self._test_thread = None
        central = QWidget()
        layout = QVBoxLayout(central)
        self.status_label = QLabel("Starting GPIB scan…")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        self.setCentralWidget(central)
        self.resize(560, 180)
        self.msg_box = QMessageBox(self)
        self._top_flags = self.msg_box.windowFlags() | Qt.WindowStaysOnTopHint

    def set_status(self, text: str):
        self.status_label.setText(text)
        QApplication.processEvents()

    def init_equipment(self):
        self.set_status("Scanning GPIB / assigning roles (may take 1–3 min)…")
        print("[INFO] Scanning GPIB / assigning equipment roles...", flush=True)
        self.equipment = EquipmentHandler(self)
        scope_ok = False
        for attempt in range(1, 4):
            print(f"[INFO] Oscilloscope connect attempt {attempt}/3…", flush=True)
            if self.equipment.check_scope_availability(get_default=True):
                scope_ok = True
                break
            import time
            time.sleep(2.0)
        if not scope_ok:
            print(
                "[WARN] Oscilloscope not reachable (Equipment Setup LAN address). "
                "Poll test requires scope for waveform capture.",
                flush=True,
            )
        lines = [
            "Equipment ready — poll test starting.",
            f"Primary DC: {getattr(self.equipment.dc_source, 'description', None)}",
            f"Source PM:  {getattr(self.equipment.power_meter_source, 'description', None)}",
            f"Load PM 1:  {getattr(self.equipment.power_meter_load_1, 'description', None)}",
            f"Scope:      {getattr(self.equipment.oscilloscope, 'description', None)}",
        ]
        self.set_status("\n".join(lines))
        for ln in lines[1:]:
            print(f"  {ln.strip()}", flush=True)

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
        self.msg_box.exec_()


class _TestItem:
    def __init__(self, parent, conditions):
        self.parent = parent
        self.test_type_index = TestTypes.index(POLL)
        self.test_conditions = conditions


def _build_conditions(args) -> TestConditions:
    params = [
        20.0, 0.1, 0.1, 0.0, 1.0, 1.0, 2.0, 25.0, 1.0, 1.0,
        float(args.poll_interval),
        float(args.poll_samples if args.poll_duration is None else args.poll_duration),
    ]
    scope = dict(POLL.POLL_DEFAULT_SCOPE_CHANNELS)
    return TestConditions(
        name=POLL.title,
        nominal_output_voltage_V=48.0,
        nominal_load_current_A=4.5,
        max_load_current_A=4.5,
        line_range=LineRange(name="750VDC", vin_freq=[[750.0, 0]], custom=True),
        load_range=LoadRange(name="100pct", load_range_pct=[100], custom=True),
        soak_time=SoakTime(
            name="bench",
            initial=args.initial_soak,
            line=0,
            load=args.load_soak,
            integration=0,
        ),
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
        unit_id=args.unit_id,
        ambient_temp=25.0,
        scope_channels=scope,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--auto-confirm", action="store_true")
    parser.add_argument("--poll-interval", type=float, default=30.0,
                        help="Wait between samples (s)")
    parser.add_argument("--poll-samples", type=float, default=3.0,
                        help="Samples per load point")
    parser.add_argument("--poll-duration", type=float, default=None,
                        help="Legacy: duration (s) → converted to sample count if >= 60")
    parser.add_argument("--initial-soak", type=float, default=5.0)
    parser.add_argument("--load-soak", type=float, default=5.0)
    parser.add_argument("--unit-id", default="TST-326")
    parser.add_argument("--hmp-ch2-v", type=float, default=12.0)
    parser.add_argument("--hmp-ch2-a", type=float, default=4.0)
    parser.add_argument("--skip-hmp-ch2", action="store_true")
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
    out = os.path.join(tempfile.gettempdir(), "pi_ate_ss_poll_smoke")
    os.makedirs(out, exist_ok=True)
    final_status = {"value": None}

    def preflight() -> str | None:
        eq = host.equipment
        if getattr(eq, "dc_source", None) is None:
            return "No primary DC source assigned."
        if getattr(eq, "power_meter_source", None) is None:
            return "No source power meter assigned."
        if getattr(eq, "power_meter_load_1", None) is None:
            return "No load power meter CH1 assigned."
        try:
            eq.check_scope_availability(get_default=True)
        except Exception:
            pass
        if getattr(eq, "oscilloscope", None) is None:
            return "No oscilloscope assigned."
        return None

    def setup_hmp_aux_channel_2() -> str | None:
        if args.skip_hmp_ch2:
            print("[INFO] Skipping HMP CH2 setup (--skip-hmp-ch2)", flush=True)
            return None
        eq = host.equipment
        aux = getattr(eq, "dc_source_aux", None)
        if aux is None:
            return (
                "No Aux DC assigned. Equipment Setup → Aux DC → HMP2030, "
                "or run with --skip-hmp-ch2 if bias is already on."
            )
        if not aux.is_hmp_series():
            return f"Aux DC is not HMP: {getattr(aux, 'description', aux)}"
        v, a = float(args.hmp_ch2_v), float(args.hmp_ch2_a)
        print(
            f"[INFO] HMP aux {aux.description}: CH2 → {v:g} V, {a:g} A limit, output ON",
            flush=True,
        )
        aux.channel_set_voltage(2, v)
        aux.channel_set_current_limit(2, a)
        aux.channel_turn_on(2)
        st = aux.channel_update_status(2)
        print(f"[INFO] HMP CH2 output status after ON: {st}", flush=True)
        return None

    def start_test_thread():
        err = setup_hmp_aux_channel_2()
        if err:
            host.set_status(f"Cannot start:\n{err}")
            print(f"[ERROR] {err}", flush=True)
            QTimer.singleShot(100, app.quit)
            return
        err = preflight()
        if err:
            host.set_status(f"Cannot start:\n{err}")
            print(f"[ERROR] {err}", flush=True)
            QTimer.singleShot(100, app.quit)
            return

        item = _TestItem(host, _build_conditions(args))
        test = POLL(item)
        test.output_folder_path = out
        n = test._sample_count()
        print(
            f"[INFO] SS Poll: 750 VDC, 48 V / 4.5 A + 20 V / 0.1 A, "
            f"poll wait {args.poll_interval:g}s, {n} samples/point",
            flush=True,
        )
        print(f"[INFO] Output: {out}", flush=True)

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
            host.set_status(f"Status: {status}\n{out}")
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
        print(f"[OK] Complete. Workbook under {out}", flush=True)
        return 0
    print(f"[FAIL] Ended with status {status!r}", flush=True)
    return 1


if __name__ == "__main__":
    sys.exit(main())
