# Manual Equipment Control UI — what can be improved

Based on `page_controls/manual_control.py`, `eload_grid.py`, `pml_grid.py`, and the generated `ui/ui_main.py` page. Bullets are ordered roughly **impact first**, then polish.

---

## Startup / bulk-cap workflow (align with SU_WF_2P tests)

- Add a **Startup bench** strip or preset: **HMP all OFF → ramp primary DC to Vin → RUN SINGLE reminder → HMP connect** so manual control mirrors `StartupWaveformTest_2Port` without running a full test.
- Show **roles from Equipment Setup** on each tile (Primary DC, Aux HMP, PML CH1, etc.) so operators know which box maps to startup vs steady-state.
- One-click **“Disconnect DUT from bulk (HMP OFF)”** and **“Connect bulk to DUT (HMP ON)”** for the assigned Aux HMP, not only per-channel Set/On/Off.
- Optional **linked ramp**: use the same **V/s** and skip logic as test code (`BULK_CAP_RAMP_V_PER_S`) when turning primary DC on, so manual and automated ramps match.
- After primary **OFF**, surface **bulk discharge** state (discharge resistor engaged?, auto-discharge running?) in one status line — Magna already prompts on ON; make OFF/discharge symmetric and visible.

---

## Safety and operator errors

- **Magna discharge resistor** is only confirmed on **DC ON**; add the same class of guard on **ramp start** and when **HMP ON** connects bulk to DUT (configurable “I confirm bench is safe”).
- **Auto-discharge on source OFF** is easy to miss; show a short **toast/status** when discharge sequencer starts (`DischargeSequencer`) and which e-load channels are pulsing.
- **Confirm high energy** before applying high Vin or high load (thresholds from test plan or user settings).
- **E-stop / All OFF** button: primary DC off, all HMP channels off, all e-loads off, cancel ramp — one obvious control.

---

## Live feedback (gaps today)

- `ui_acsource_update()` is **empty** — show **measured/set Vin**, **freq**, **coupling**, and **ramping** (`is_ramping`, current vs target V) on the DC/AC source panel.
- HMP Aux shows **ON/OFF** only — add **readback V/I** per channel when the driver supports it (even if slower poll rate).
- E-load tiles rely on **ping via `get_id()`**; show **actual I/V/P** and **CC/CV state** on the tile (not only in gear dialog).
- When a GPIB error greys out a tile, show **why** (last SCPI error, timeout) and a **Retry** button instead of permanent disable until page restart.

---

## Equipment assignment and discoverability

- **Setup Equipment** entry on manual page is **hidden** (`frame_manual_control_setup_equipment.hide()`) — restore a compact **“Open Setup Equipment”** or **role summary + edit** so bench changes do not require leaving manual control.
- Code still has **TODO: configure which equipment in GUI** — manual page should reflect **Equipment Setup roles only**, never hard-coded GPIB order (`EQUIPMENT_ADDRESS` looks legacy/unused).
- On page **Start**, show a **checklist**: missing Aux HMP when startup tests are in queue, unassigned PML for 2-port mode, etc.

---

## Layout and density

- Lower row stacks **DC + Aux HMP + e-load grid + USB PD** — on laptop screens this is crowded; consider **tabs or collapsible sections** (eload grid already collapses USB PD; extend pattern to PML grid and Aux HMP).
- **Aux HMP** under DC is good (`verify_aux_dc_ui_layout.py`); add **collapse** when Aux is unassigned to reclaim vertical space.
- PML **2×2 grid + total efficiency strip** is strong — add **pin label** on source meter tile to match “Sum Pout | Total Eff” story for 2-port debugging.

---

## Polling and performance

- Single **500 ms** timer hits **all** meters, loads, and source; during **software ramp**, other GPIB is skipped (good) — document that in UI (“Ramping — meters paused”).
- Allow **slow / fast poll** toggle or pause polling when manual page is not visible (save GPIB bandwidth for running tests).
- Reduce duplicate **Visa** traffic: e-load updates mostly `get_id()` — poll **status only** on an interval, full measurements when tile is expanded or ON.

---

## USB PD sink panel

- **PDO request** path has **TODO: input validation** — validate mA/mV against selected PDO limits before `fpdo_request` / `pps_request`.
- Status strings are good (connected / contract); add **active RDO summary** (V, A, PPS vs Fixed) when contracted.
- Collapsible panel helps; default **collapsed when no sink hardware** to reduce noise.

---

## Settings and consistency

- `manual_control_settings.json` saves widgets on the page — **scope** path (cwd vs Documents) should match other PI ATE configs; consider **user profile folder** like `Documents/PI_ATE/`.
- Persist **discharge current**, **auto-discharge**, **ramp enable/slew** alongside e-load/PML gear dialog settings.
- **Per-bench profiles** (name + JSON) for different DUT families.

---

## Code health (enables future UI work)

- Remove stray **PyQt5** import (`QCoreApplication` from PyQt5) — project is **PySide2**; reduces confusion and install clutter.
- Unify **error wrappers** (`power_meter_load_2_access` etc.) so all channels grey/red consistently and call shared **mark_unavailable(reason)**.
- Split **manual_control.py** (~1600 lines) — USB PD, source/ramp, aux HMP already partially extracted (`eload_grid`, `pml_grid`); move **AC/DC source** and **discharge** into modules for easier testing.

---

## Nice-to-have

- **Oscilloscope** deep link: “Open scope remote” or show trigger/run state if LAN scope API exists (manual page is the natural home for bench prep).
- **Copy bench state** to clipboard (Vin, loads, HMP CH states) for lab notes.
- **Keyboard shortcuts**: source ON/OFF, discharge, HMP toggle when manual page focused.
- Light **simulation banner** when `PI_ATE_SIMULATION=1` on manual page.

---

## Already in good shape (keep building on)

- **PmlGrid** / **EloadGrid**: 2×2 tiles, gear dialogs, unassigned dashed tiles, total efficiency strip.
- **Magna software ramp** with estimated time and bus quiet during ramp.
- **Multi-channel HMP Aux** panel stacked under DC source.
- **JSON state restore** for line edits and checkboxes on the page.
- **Output discharge sequencer** integrated with source OFF and manual Discharge button.

---

## Suggested first slices (if you implement)

1. Live **DC source readback + ramp progress** on the source panel.  
2. **Retry** on GPIB failure + **All OFF**.  
3. **Startup bench** macro (HMP OFF / ramp / HMP ON) tied to Equipment Setup roles.  
4. Re-show **Setup Equipment** shortcut on manual page.
