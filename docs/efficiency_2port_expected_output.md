# Efficiency 2 Port — Expected Output

This document describes the **intended** table layout for the **Efficiency 2 Port** test after the Excel export fix (regulatory summary at column **T**, not **N**).

**Implementation reference:** `psu_tests/test_efficiency_2port.py` (`define_data_header`, `prepare_sheet_formatting`, `process_data_row`).

---

## Where results appear

| Location | Path / UI |
|----------|-----------|
| In-app | **Test Results** tab → data table for the running/completed test |
| Excel file | `{output folder}/Efficiency 2 Port Test {Vout}V.xlsx` |
| Worksheet | `AveEff_{AC\|DC}_{Vout}V_{Iout}A` (example: `AveEff_DC_48V_5A`) |

---

## Excel row 4 — section headers (merged cells)

| Excel columns | Section title |
|---------------|---------------|
| A–B | Load Condition |
| C–D | Input Set |
| E–I | Input Measurement |
| J–M | Output 1 Measurement |
| **N–Q** | **Output 2 Measurement** |
| R–S | Total Power & Efficiency |
| T–X | Average Efficiency Limits |

---

## Row 5+ — data column headers (19 columns, A through S)

These headers are used in **Test Results** and in the Excel data block starting at **A5**.

| Col | Header | Description |
|-----|--------|-------------|
| A | Ch1 Load | Port 1 load step label (e.g. `100%`, `75%`) |
| B | Ch2 Load | Port 2 load step label (depends on dual-load mode) |
| C | VDC (rms) or VAC (rms) | Input voltage setpoint for the line step |
| D | Freq (Hz) | AC frequency (or as configured) |
| E | Vin (rms) | Measured input voltage |
| F | Iin (mA) | Measured input current |
| G | Pin (W) | Measured input power |
| H | PF | Power factor |
| I | %THD | Total harmonic distortion |
| J | Vo1 (V) | Port 1 output voltage |
| K | Io1 (A) | Port 1 output current |
| L | Po1 (W) | Port 1 output power |
| M | %V Reg 1 | Port 1 voltage regulation vs nominal Vout 1 |
| **N** | **Vo2 (V)** | **Port 2 output voltage** |
| **O** | **Io2 (A)** | **Port 2 output current** |
| **P** | **Po2 (W)** | **Port 2 output power** |
| **Q** | **%V Reg 2** | **Port 2 voltage regulation vs nominal Vout 2** |
| R | Po_Total (W) | Po1 + Po2 |
| S | Efficiency (%) | (Po_Total / Pin) × 100 |

**Important:** Columns **N–Q** must show **Vo2 / Io2 / Po2 / %V Reg 2** only. They must **not** show `Avg_Eff`, `DOE6 Limit`, or `Pass/Fail` (those belong under **T–X**).

---

## Regulatory summary block (columns T–X, anchor T5)

Written by a separate export starting at **T5** (same row as the data block for each line-voltage section):

| Col | Header |
|-----|--------|
| T | Avg_Eff |
| U | DOE6 Limit |
| V | COC5 T2 Limit |
| W | COC5_T2_10% |
| X | Pass/Fail |

Population of this block may be sparse compared to single-port Efficiency until 2-port regulatory row logic is fully implemented; measurement columns **A–S** should still be complete.

---

## Example row (illustrative — Option A proportional sync, 100% / 100%)

Nominals example: Vout1 = 48 V, Iout1 = 5 A, Vout2 = 12 V, Iout2 = 2 A, DC input 750 V. **Your numbers will differ** with hardware and settings.

| Ch1 Load | Ch2 Load | VDC (rms) | Freq | Vin | Iin (mA) | Pin (W) | PF | %THD | Vo1 (V) | Io1 (A) | Po1 (W) | %V Reg 1 | Vo2 (V) | Io2 (A) | Po2 (W) | %V Reg 2 | Po_Total (W) | Efficiency (%) |
|----------|----------|-----------|------|-----|----------|---------|----|------|---------|---------|---------|----------|---------|---------|---------|----------|--------------|----------------|
| 100% | 100% | 750 | 50.00 | 750.4 | 208 | 155.6 | 0.99 | 0.000 | 47.612 | 3.00 | 142.83 | -0.81 | 12.00 | 2.00 | 24.00 | 0.00 | 166.83 | 93.08 |

Check: **Po_Total ≈ Po1 + Po2**, **Efficiency ≈ Po_Total / Pin × 100**.

---

## Load step rows

- One **data row per entry** in the configured load range (default efficiency steps: 100%, 75%, 50%, 25%, 10%) combined with the **dual load mode**:
  - **Option A — Proportional sync:** Ch1 and Ch2 percentages track together.
  - **Option B — Cross-reg matrix:** Ch2 fixed per matrix step; Ch1 sweeps load range.
  - **Option C — Fixed aux:** Ch2 shows fixed aux current (e.g. `0.5A`); Ch1 sweeps load range.
- The test repeats the load sweep for **each line voltage** in the selected line range.
- A **blank row** is inserted between line-voltage blocks in the exported sheet / results table.

---

## Oscilloscope measurements (optional, below each line-voltage block)

When **Measure Scope Ripple** is enabled on Add Tests (General Options) and an oscilloscope is connected:

1. After each load step soak, the scope is stopped, optional PNG screenshots are saved under the run waveform folder, and active **MEAS** slots are read via `get_measure_all()` (with per-channel fallback).
2. After the main **A–S** efficiency table and **T–X** summary for that line voltage, a **blank row**, then a titled block **Oscilloscope Measurements**, then a sub-table:
   - Fixed columns: **Ch1 Load**, **Ch2 Load**
   - Dynamic columns: one per active measurement (e.g. `CH1 Pk-Pk`, `CH2 Max`, …) depending on scope setup
3. The same sub-table is appended in **Test Results** (title + header as rows under the efficiency data).
4. Multi–line-voltage runs use a running Excel row cursor so scope blocks do not overwrite the next line-voltage section.

---

## Dual-load mode — Ch2 Load column examples

| Mode | Ch1 Load (example) | Ch2 Load (example) |
|------|--------------------|--------------------|
| Option A | 100% | 100% |
| Option A | 50% | 50% |
| Option B | 100% | 50% |
| Option C | 100% | 0.5A (fixed aux) |

Port 2 nominal values come from **Nominal Vout 2 (V)** and **Nominal Iout 2 (A)** on the Add Test page (I2C/dual-port parameters).

---

## Related plots (Test Results)

| Plot | X axis | Y axis |
|------|--------|--------|
| Efficiency vs Load | Ch1 load current (A) | Efficiency (%) |
| Channel 1 Regulation | Ch1 current (A) | Ch1 voltage (V) |
| Channel 2 Regulation | Ch2 current (A) | Ch2 voltage (V) |

---

## Troubleshooting misaligned columns

If **Output 2** shows limit columns instead of **Vo2 / Io2 / Po2**:

1. Confirm you are on code with **efficiency summary anchor `T5`** (not `N5`) in `test_efficiency_2port.py`.
2. Re-run the test or use a **new** worksheet; old sheets keep the previous layout.
3. Launch from: `run.bat` in the Marketing Release project folder.

---

*PI ATE — Power Integrations Automated Test Equipment*
