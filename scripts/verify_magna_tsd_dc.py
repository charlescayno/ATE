"""Verify Magna TSD2000-2.5 DC source registration and Magna HVDC detection.

Run: .\\conda_env\\python.exe scripts\\verify_magna_tsd_dc.py
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
os.environ["PI_ATE_SIMULATION"] = "1"

OUT = sys.__stdout__
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    msg = f"{'PASS' if cond else 'FAIL'}  {name}"
    if detail and not cond:
        msg += f"  -> {detail}"
    OUT.write(msg + "\n")
    OUT.flush()


def test_tsd_model_lookup():
    from equipment.dc_source import _resolve_dc_source_model
    from equipment.dc_source_specs import DCSourceMagnaPower

    cls = _resolve_dc_source_model("TSD2000-2.5")
    check("lookup: TSD2000-2.5 resolves", cls is DCSourceMagnaPower)


def test_is_magna_hvdc():
    from equipment.dc_source import DCSource, is_magna_hvdc
    from equipment.dc_source_specs import DCSourceMagnaPower

    class FakeDev:
        def query(self, c):
            if "?" in c:
                return "0"
            return ""

        def write(self, c):
            pass

        def close(self):
            pass

    def make_magna(model):
        dc = object.__new__(DCSource)
        dc.device = FakeDev()
        dc.device_id = f"Magna-Power Electronics Inc.,{model},S/N:1,F/W:9.0"
        dc.manufacturer = "Magna-Power Electronics Inc."
        dc.model = model
        dc.serial = "S/N:1"
        dc.unpack_dc_source_specs()
        dc._voltage = dc._current = 0
        dc.output_status = 0
        dc.description = f"Magna {model}"
        return dc

    tsd = make_magna("TSD2000-2.5")
    sl = make_magna("SL1000-1.5")
    check("is_magna_hvdc: TSD2000-2.5", is_magna_hvdc(tsd))
    check("is_magna_hvdc: SL1000-1.5", is_magna_hvdc(sl))
    check("is_magna_hvdc: TSD uses Magna SCPI", tsd.command_output_on == "OUTP:START")

    hmp = object.__new__(DCSource)
    hmp.manufacturer = "Rohde&Schwarz"
    hmp.model = "HMP2030"
    check("is_magna_hvdc: HMP false", not is_magna_hvdc(hmp))


def test_handler_magna_role():
    from equipment.handler import EquipmentHandler
    from equipment.dc_source import DCSource

    class FakeDev:
        def query(self, c):
            return "0" if "?" in c else ""

        def write(self, c):
            pass

        def close(self):
            pass

    h = object.__new__(EquipmentHandler)
    tsd = object.__new__(DCSource)
    tsd.device = FakeDev()
    tsd.device_id = "Magna-Power Electronics Inc.,TSD2000-2.5,S/N:1,F/W:9.0"
    tsd.manufacturer = "Magna-Power Electronics Inc."
    tsd.model = "TSD2000-2.5"
    tsd.serial = "S/N:1"
    tsd.unpack_dc_source_specs()
    tsd._voltage = tsd._current = 0
    tsd.output_status = 0
    tsd.description = "Magna TSD"
    check("handler: _is_magna_dc TSD", EquipmentHandler._is_magna_dc(tsd))


def test_discharge_check():
    from equipment.dc_source import is_magna_hvdc

    class Supply:
        manufacturer = "Magna-Power Electronics Inc."
        model = "TSD2000-2.5"

    check("discharge path: Magna TSD input_supply", is_magna_hvdc(Supply()))


if __name__ == "__main__":
    test_tsd_model_lookup()
    test_is_magna_hvdc()
    test_handler_magna_role()
    test_discharge_check()
    failed = [n for n, ok in results if not ok]
    OUT.write(f"\n{len(results) - len(failed)}/{len(results)} passed\n")
    sys.exit(1 if failed else 0)
