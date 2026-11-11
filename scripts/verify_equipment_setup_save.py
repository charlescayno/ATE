"""Headless checks for the equipment setup save/restore path (no instruments needed).

Run: conda_env\\python.exe scripts\\verify_equipment_setup_save.py
"""
import os
import sys
import tempfile
import types

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide2.QtWidgets import QApplication, QComboBox, QFrame, QWidget

app = QApplication([])

import user_settings.save_load as SL
import page_controls.equipment_setup as ES
from equipment.handler import EquipmentHandler

H = ES.EquipmentSetupPageHandler
errors = []


def check(name, cond, info=""):
    print(("OK   " if cond else "FAIL ") + name + (f"  {info}" if info and not cond else ""))
    if not cond:
        errors.append(name)


class Dev:
    def __init__(self, desc, model="", serial=""):
        self.description = desc
        self.model = model
        self.serial = serial


MAGNA = Dev("Magna-Power Electronics Inc.  TSD2000-2.5  S/N:1161-13051", "TSD2000-2.5", "1161-13051")
HMP = Dev("ROHDE&SCHWARZ HMP2030 120321", "HMP2030", "120321")


def aux_combo_fake(dc_sources, aux):
    eq = types.SimpleNamespace(dc_sources=dc_sources, dc_source=MAGNA, dc_source_aux=aux)
    f = types.SimpleNamespace(equipment=eq, parent=QWidget(), ongoing_dc_source_aux_update=False)
    f.ui = types.SimpleNamespace(frame_equip_setup_sources_dcsource_aux=QFrame(),
                                 cbx_equip_setup_sources_dcsource_aux=QComboBox())
    f._ensure_hmp_aux_dc_role = lambda: None
    f._sync_manual_aux_dc_panel = lambda: None
    f.update_dc_source_aux_info = lambda: H.update_dc_source_aux_info(f)
    f.ui.cbx_equip_setup_sources_dcsource_aux.currentIndexChanged.connect(f.update_dc_source_aux_info)
    return f


def test_aux_combo_refresh():
    f = aux_combo_fake([MAGNA, HMP], HMP)
    H.ui_update_dc_source_aux_combo_box(f)
    cbx = f.ui.cbx_equip_setup_sources_dcsource_aux
    check("aux combo shows HMP after refresh", cbx.currentText() == HMP.description, cbx.currentText())
    check("aux role kept after refresh", f.equipment.dc_source_aux is HMP)
    H.ui_update_dc_source_aux_combo_box(f)  # second refresh (called from several places)
    check("aux role kept after 2nd refresh", f.equipment.dc_source_aux is HMP)
    cbx.setCurrentIndex(0)  # operator picks '-'
    check("operator '-' clears aux", f.equipment.dc_source_aux is None)


def test_round_trip(tmp):
    SL.equipment_setup_filepath = os.path.join(tmp, "equipment_setup.json")
    SL.write_to_default_config = lambda *a, **k: None
    cfg = {"ac_source": "", "dc_source": MAGNA.description, "dc_source_aux": HMP.description,
           "oscilloscope_address": "169.254.185.157",
           "power_meters": {"source": "YOKOGAWA 760202 GPIB0::12", "load_1": "YOKOGAWA WT310 GPIB0::7",
                            "load_2": "-", "load_3": "-", "load_4": "-", "load_5": "-"},
           "electronic_loads": {"load_1": "Chroma 6314A 63108A Ch5  GPIB0::8", "load_2": "-",
                                "load_3": "-", "load_4": "-", "load_5": "-", "load_6": "-"},
           "sink_controller": "", "i2c_controller": ""}
    SL.save_equipment_setup(cfg)
    check("saved json equals config", SL.load_equipment_setup() == cfg)

    h = EquipmentHandler.__new__(EquipmentHandler)
    h.ac_sources, h.dc_sources = [], [MAGNA, HMP]
    h.power_meters, h.e_loads = [], []
    h.dc_source = h.dc_source_aux = None
    for name in ("reset_power_meter_roles", "reset_electronic_load_roles"):
        setattr(h, name, lambda: None)
    try:
        h.apply_saved_equipment_roles(SL.load_equipment_setup())
    except Exception as exc:  # roles after DC are not what this test is about
        print("note: apply stopped after DC roles:", type(exc).__name__, exc)
    check("restored primary DC", h.dc_source is MAGNA)
    check("restored Aux DC by description", h.dc_source_aux is HMP)

    # Aux saved, HMP renamed slightly (case/spacing) -> still matched
    renamed = dict(cfg, dc_source_aux="rohde&schwarz hmp2030 120321")
    h.dc_source = h.dc_source_aux = None
    try:
        h.apply_saved_equipment_roles(renamed)
    except Exception:
        pass
    check("Aux matched case-insensitively", h.dc_source_aux is HMP)


def merge_fake(detected_dc, detected_pm=()):
    eq = types.SimpleNamespace(ac_sources=[], dc_sources=detected_dc,
                               power_meters=list(detected_pm), e_loads=[])
    return types.SimpleNamespace(equipment=eq)


def test_offline_merge():
    saved = {"ac_source": "", "dc_source": MAGNA.description, "dc_source_aux": HMP.description,
             "power_meters": {"source": "YOKOGAWA 760202 GPIB0::12", "load_1": "-"},
             "electronic_loads": {"load_1": "Chroma 6314A 63108A Ch5  GPIB0::8"}}
    SL.save_equipment_setup(saved)
    ES.load_equipment_setup = SL.load_equipment_setup
    cur = {"ac_source": "", "dc_source": MAGNA.description, "dc_source_aux": "-",
           "power_meters": {"source": "-", "load_1": "-"},
           "electronic_loads": {"load_1": "-"}}
    # HMP, meter and e-load are switched off (not detected): keep their saved roles
    out = H._keep_saved_roles_for_offline_equipment(merge_fake([MAGNA]), cur)
    check("offline Aux DC keeps saved role", out["dc_source_aux"] == HMP.description, out["dc_source_aux"])
    check("offline power meter keeps saved role", out["power_meters"]["source"] == saved["power_meters"]["source"])
    check("offline e-load keeps saved role",
          out["electronic_loads"]["load_1"] == saved["electronic_loads"]["load_1"])
    # HMP detected but operator set '-': honour the operator
    out = H._keep_saved_roles_for_offline_equipment(merge_fake([MAGNA, HMP]), cur)
    check("detected Aux DC set to '-' is honoured", out["dc_source_aux"] == "-")


def main():
    test_aux_combo_refresh()
    with tempfile.TemporaryDirectory() as tmp:
        test_round_trip(tmp)
        test_offline_merge()
    print("\nFAIL: " + ", ".join(errors) if errors else "\nAll equipment setup checks passed")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
