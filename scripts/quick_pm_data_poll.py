"""Quick power-meter poll (source + load 1/2). Use --sim when GPIB PMs are offline.

  python scripts/quick_pm_data_poll.py --sim --samples 3 --interval 2
  python scripts/quick_pm_data_poll.py --samples 5 --interval 5
"""
from __future__ import annotations

import argparse
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from PySide2.QtWidgets import QApplication  # noqa: E402

from equipment.ac_source import AC_SOURCE_COUPLING  # noqa: E402
from equipment.power_meter import PowerMeter  # noqa: E402
from psu_tests.definitions import TestData  # noqa: E402

import pyvisa  # noqa: E402


def _prime_sim_bench(eq) -> None:
    st = getattr(eq, "state", None)
    if st is None:
        return
    st.ac_on = True
    st.vin = 380.0
    st.loads[1].update({"load_on": True, "iout": 2.0, "target_vout": 48.0})
    st.loads[2].update({"load_on": True, "iout": 1.0, "target_vout": 12.0})


def _is_power_meter_idn(idn: str) -> bool:
    u = (idn or "").upper()
    return "YOKOGAWA" in u and any(m in u for m in ("WT310", "760202", "WT500", "WT180"))


def _discover_power_meters(timeout_ms: int = 3000) -> list[tuple[str, str, PowerMeter]]:
    rm = pyvisa.ResourceManager()
    found: list[tuple[str, str, PowerMeter]] = []
    for resource_txt in rm.list_resources():
        if "GPIB" not in resource_txt:
            continue
        try:
            dev = rm.open_resource(resource_txt)
            dev.timeout = timeout_ms
            idn = dev.query("*IDN?").strip()
        except pyvisa.VisaIOError:
            continue
        if not _is_power_meter_idn(idn):
            try:
                dev.close()
            except Exception:
                pass
            continue
        pm = PowerMeter(dev, idn)
        found.append((resource_txt, idn, pm))
    return found


def _run_pm_only_poll(samples: int, interval: float) -> int:
    print("[INFO] PM-only poll (skips full bench scan / e-load init)", flush=True)
    meters = _discover_power_meters()
    if not meters:
        print("[FAIL] No Yokogawa power meters answered on GPIB.", flush=True)
        return 1
    for addr, idn, pm in meters:
        print(f"  {addr}: {idn}  ({pm.description})", flush=True)
    print(f"\n[INFO] {samples} sample(s), {interval:g} s apart\n", flush=True)
    hdr = " # | " + " | ".join(f"{m[2].description[:22]:>22}" for m in meters)
    print(hdr, flush=True)
    print("   | " + " | ".join("V      I      P" for _ in meters), flush=True)
    for i in range(samples):
        if i > 0:
            time.sleep(max(0.0, interval))
        cells = []
        for _addr, _idn, pm in meters:
            try:
                pm.poll_basic_params()
                cells.append(f"{pm._voltage:>5.2f} {pm._current:>5.3f} {pm._power:>6.1f}")
            except Exception:
                cells.append(f"{'—':>5} {'—':>5} {'—':>6}")
        print(f"{i + 1:2d} | " + " | ".join(f"{c:>22}" for c in cells), flush=True)
    print("\nOK  PM-only poll finished", flush=True)
    return 0


def _label(pm) -> str:
    if pm is None:
        return "— (not assigned)"
    return getattr(pm, "description", None) or type(pm).__name__


def _read_row(eq, use_eload: bool) -> dict:
    td1 = TestData()
    td1.use_eload_data = use_eload
    td1.vout_nom_V = 48.0
    td1.source_power_meter = eq.power_meter_source
    td1.load_power_meter = eq.power_meter_load_1
    td1.electronic_load = getattr(eq, "electronic_load_1", None)

    td2 = TestData()
    td2.use_eload_data = use_eload
    td2.vout_nom_V = 20.0
    td2.load_power_meter = eq.power_meter_load_2
    td2.electronic_load = getattr(eq, "electronic_load_2", None)

    td1.gather_data(coupling=AC_SOURCE_COUPLING.DC, usb_pd=False, measure_thd=False)
    td2.gather_data_load(integrate=False, force_use_eload_data=use_eload)
    return {
        "vin": td1.vin_V,
        "pin": td1.pin_W,
        "vo1": td1.vout_V,
        "io1": td1.iout_A,
        "po1": td1.pout_W,
        "vo2": td2.vout_V,
        "io2": td2.iout_A,
        "po2": td2.pout_W,
    }


def _init_equipment(sim: bool):
    host = type("Host", (), {"run_settings": {"debug": False}})()
    if sim:
        os.environ["PI_ATE_SIMULATION"] = "1"
        from equipment.simulated_handler import SimulatedEquipmentHandler  # noqa: E402

        print("[INFO] Simulation mode (no GPIB required)", flush=True)
        eq = SimulatedEquipmentHandler(host)
        _prime_sim_bench(eq)
        return eq

    if os.environ.get("PI_ATE_SIMULATION") == "1":
        os.environ.pop("PI_ATE_SIMULATION", None)
    from equipment.handler import EquipmentHandler  # noqa: E402

    print("[INFO] Scanning GPIB / assigning roles…", flush=True)
    return EquipmentHandler(host)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sim", action="store_true", help="Simulated PMs (no GPIB)")
    parser.add_argument(
        "--pm-only",
        action="store_true",
        help="Poll Yokogawa PMs on GPIB only (no e-load / full EquipmentHandler)",
    )
    parser.add_argument("--samples", type=int, default=3)
    parser.add_argument("--interval", type=float, default=2.0)
    parser.add_argument("--use-eload", action="store_true", help="Vo from e-load instead of load PM")
    args = parser.parse_args()

    if args.pm_only and not args.sim:
        return _run_pm_only_poll(args.samples, args.interval)

    app = QApplication.instance() or QApplication(sys.argv)
    eq = _init_equipment(args.sim)

    roles = (
        ("Source PM", eq.power_meter_source),
        ("Load 1 PM", eq.power_meter_load_1),
        ("Load 2 PM", eq.power_meter_load_2),
    )
    for name, pm in roles:
        print(f"  {name}: {_label(pm)}", flush=True)

    missing = [n for n, pm in roles if pm is None]
    if missing and not args.sim:
        print(
            f"[WARN] Not assigned: {', '.join(missing)} — "
            "readings may be 0. Use --sim for demo data or fix Equipment Setup.",
            flush=True,
        )

    mode = "e-load" if args.use_eload else "load PM"
    print(
        f"[INFO] Polling {args.samples} sample(s), {args.interval:g} s apart, Vo via {mode}\n",
        flush=True,
    )
    print(
        " # |     Vin |    Pin |    Vo1 |   Io1 |   Po1 |    Vo2 |   Io2 |   Po2",
        flush=True,
    )

    for i in range(args.samples):
        if i > 0:
            time.sleep(max(0.0, args.interval))
        r = _read_row(eq, args.use_eload)
        print(
            f"{i + 1:2d} | {r['vin']!s:>7} | {r['pin']!s:>6} | "
            f"{r['vo1']!s:>6} | {r['io1']!s:>5} | {r['po1']!s:>5} | "
            f"{r['vo2']!s:>6} | {r['io2']!s:>5} | {r['po2']!s:>5}",
            flush=True,
        )

    ok = any(
        (r := _read_row(eq, args.use_eload)) and (
            (r.get("vo1") or 0) > 0.1 or (r.get("vin") or 0) > 1
        )
        for _ in [0]
    )
    if args.sim or ok:
        print("\nOK  quick PM data poll finished", flush=True)
        return 0
    print(
        "\nFAIL all Vo/Vin ~0 — connect PMs and roles, or run with --sim",
        flush=True,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
