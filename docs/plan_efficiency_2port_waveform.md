# Plan: new combined test — Efficiency 2 Port + Steady-State Waveform Capture

**Status:** implemented in `psu_tests/test_efficiency_2port_waveform.py` (see the "Decisions" section at the end). Verify with `scripts/verify_efficiency_2port_waveform.py`.

## Goal

Add a new test, working name **"Efficiency 2 Port + Waveform Capture"**. At every line voltage and load step it does two things:

1. Takes the full dual-output efficiency measurement, the same as **Efficiency 2 Port**.
2. Captures the scope waveform at that same point, the same as **Steady-State Waveform Capture**: optional auto-trigger sweep, an optional operator prompt (Capture / Recapture / Skip / Stop), a PNG screenshot, and the readings from the active scope measurement slots.

Neither existing test is replaced. Both stay exactly as they are.

---

## What each test brings

| Feature | Efficiency 2 Port | Steady-State | Combined test |
|---|---|---|---|
| Line × load sweep | yes | yes | yes |
| Two outputs (two electronic loads, Port 2 settings, dual-load modes A/B/C) | yes | no | yes |
| Pin / PF / THD, Po1 / Po2 / Po_Total, efficiency, %V Reg 1 and 2 | yes | single-output only | yes (2-port version) |
| Average-efficiency limits block (T–X) | yes | no | yes |
| USB-PD source support | yes | no | yes (left as is from Efficiency 2 Port) |
| 4-channel scope matrix (names, measurements, derating, cursors) | no | yes | yes |
| Trigger channel, auto-find trigger, trigger delta | no | yes | yes |
| Operator prompts (before the test and/or before each capture) | no | yes | yes |
| Screenshot per point plus a Waveforms worksheet with embedded images | no | yes | yes |
| Unit ID, ambient temperature, settle time, discharge pulses, post-capture delay | no | yes | yes |
| Plots | Efficiency vs Load, Ch1 Reg, Ch2 Reg | Max Vds vs Vin | all four |

---

## Order of steps at each load point

1. Set both loads (Ch1 / Ch2 from the dual-load mode), then auto-range the power meters.
2. Correct the source voltage, soak per load, then wait the settle time.
3. **Efficiency measurement first:** lock the power meter ranges, gather Port 1 and Port 2 data, and compute Po_Total and efficiency.
4. **Then the scope capture:** auto-find the trigger (if enabled), run a single acquisition, stop, read the measurements, and show the operator prompt (if enabled).
   - **Recapture** re-triggers at the same point. The efficiency numbers are kept.
   - **Skip** keeps the efficiency row and leaves the scope cells empty (`N/A`).
   - **Stop** ends the test.
5. Save the screenshot, write the row, update the plots, wait the post-capture delay, and restore auto-range.

The efficiency reading comes first so that a long operator prompt can't stretch or affect the power-meter integration window. The unit stays at the same operating point the whole time, so the scope still sees steady state.

---

## Output layout (Excel and Test Results)

**Recommended:** one row per load point, with the scope columns **added to the right** of the existing 2-port table:

- **A–S:** unchanged Efficiency 2 Port columns (Ch1 Load … Efficiency (%)).
- **T–X:** Average Efficiency Limits, unchanged.
- **Y onward:** `Trig Ch`, `Trig Level (V)`, then one column per configured scope measurement (e.g. `Primary Vds Max`, `Primary Vds Derating (%)`, `Ids Max`, cursor `dX` / `Fsw (kHz)` / `dY`), then `Waveform File`.
- Row 4 gets a merged section title **"Oscilloscope Measurements"** over Y onward.
- In Test Results the same columns follow S. T–X stays Excel-only, as it is today.
- A **Waveforms** worksheet holds the embedded screenshots, captioned with Vin, Ch1/Ch2 load and the measurements, when "Embed in Excel" is set to Yes.

**Alternative:** put the scope readings in a separate sub-table below each line-voltage block. That is how the scope option just added to Efficiency 2 Port works. Each row stays shorter, but the scope data no longer lines up with its efficiency row.

---

## Add Test panel: settings slots

The shared settings panel has **10 text fields and 4 dropdowns**. Combining both tests needs:

| Setting | Type | From |
|---|---|---|
| Nominal Vout 2 (V) | text | Efficiency 2 Port |
| Nominal Iout 2 (A) | text | Efficiency 2 Port |
| Fixed Aux Load (A) | text | Efficiency 2 Port |
| Port 2 Loads (%) | text | Efficiency 2 Port |
| Trigger Delta | text | Steady-State |
| Settle Time (s) | text | Steady-State |
| Discharge Pulses | text | Steady-State |
| Ambient Temp (°C) | text | Steady-State |
| Post-Capture Delay (s) | text | Steady-State |
| Dual Load Mode | dropdown | Efficiency 2 Port |
| Trigger Channel | dropdown | Steady-State |
| Embed in Excel | dropdown | Steady-State |
| User Prompts | dropdown | Steady-State |
| Auto Find Trigger | dropdown | Steady-State |

That is **9 text fields (fits)** and **5 dropdowns (one too many)**. One of them has to change. Options:

- **A (recommended):** make **Trigger Channel** a text field (1–4), validated and defaulting to 1. It uses the 10th text field.
- **B:** always embed the images in Excel and drop the "Embed in Excel" dropdown.
- **C:** merge "Auto Find Trigger" into "User Prompts" as extra choices. This makes the dropdown confusing.

The panel also has to show these at the same time:

- Output 1 nominal Vout / Iout (as Efficiency 2 Port does today)
- The 4-channel scope matrix and the Unit ID field (as Steady-State does today)

---

## Code changes (once approved)

1. **New file `psu_tests/test_efficiency_2port_waveform.py`**
   - Class `EfficiencyWaveformTest_2Port`, subclassing `EfficiencyTest_2Port`, so dual-load mode, the efficiency math, the Excel layout and USB-PD come along unchanged.
   - Override `unpack_test_item`, `setup_equipment` (oscilloscope required), `define_data_header`, `process_data_row`, `prepare_sheet_formatting`, `define_output_data_objects`, `test_loop`, `estimate_remaining`, `update_test_list_text`, `get_dict`, `extract_test_condition`, and `with_waveform_capture` (always on).
   - Turn off the scope sub-table option inherited from Efficiency 2 Port, so scope data isn't written twice.
2. **Shared scope helpers.** Move `find_trigger`, `query_active_scope_measurements`, `request_capture_action` / `CapturePromptHelper`, `embed_waveforms_in_excel`, `discharge_output` and the scope-setup routine into a small mixin, `psu_tests/scope_capture_mixin.py`. Steady-State and the new test both use it. Steady-State behaves exactly as before; only where the code lives changes.
   - Alternative that doesn't touch Steady-State: copy those methods into the new file. It's faster but leaves two copies to maintain.
3. **`psu_tests/test_type.py`:** import the new class and add it to the **end** of `TestTypes`. Saved test plans store tests by list position, so adding it anywhere else would shift existing saved plans to the wrong tests.
4. **`page_controls/add_test.py`:** add the new title wherever the code checks for "Efficiency 2 Port" or "Steady-State Waveform Capture", so the Output 1 nominal fields, the scope matrix, the Scope FAQ button, Unit ID and the defaults/reset all appear. This also fixes an existing bug: the Unit ID field checks for class name `TestVdsIdsSteadyState`, but the class is actually named `VdsIdsSteadyStateTest`, so the Unit ID field never appears even for Steady-State today.
5. **Docs:** add `docs/efficiency_2port_waveform_expected_output.md` describing the columns.

---

## How I'll check it

- Compile all touched files with `py_compile`.
- Use the simulated equipment handler (`equipment/simulated_handler.py`) to run Option A and Option B sweeps with prompts set to "None (Fully Automated)". Then confirm:
  - the row count matches line steps × load pairs,
  - the scope columns line up with the headers,
  - the Waveforms sheet is created,
  - no columns overlap across line-voltage blocks.
- Smoke-test the app: open Add Test, select the new test, and confirm all panels show and the settings save and reload through a saved test plan.
- Re-run plain Efficiency 2 Port and Steady-State to confirm nothing changed.

---

## Decisions (confirmed by user)

1. **Output layout:** scope columns go **to the right on the same row** (Y onward, after the T–X limits block).
2. **Fifth dropdown:** **Trigger Channel becomes a text field** (1–4, default 1). The four dropdowns are Dual Load Mode, Embed in Excel, User Prompts and Auto Find Trigger.
3. **Shared code:** **copy** the scope helpers into the new test file. `test_vds_ids_steady_state.py` is not touched.
4. **Name:** **"Efficiency 2 Port (Waveform)"**.

Because the helpers are copied rather than shared, change 2 under "Code changes" does not apply. The Unit ID bug fix in `add_test.py` (change 4) still affects Steady-State, since it's in the shared Add Test page. I'll include it unless you'd rather keep that separate.
