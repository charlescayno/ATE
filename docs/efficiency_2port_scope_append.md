# Efficiency 2 Port — Oscilloscope data appended after the main table

## What changed

**Efficiency 2 Port** can now capture oscilloscope measurements at each load step and append them **below** the main efficiency table (columns A–S) for each line-voltage block, in both Excel and the Test Results table.

**File:** `psu_tests/test_efficiency_2port.py`  
**Docs:** `docs/efficiency_2port_expected_output.md` (new section)

## How to use

1. On **Add Tests**, enable **Measure Scope Ripple** (General Options).
2. Connect and configure the oscilloscope **MEAS** slots as you do for load regulation tests.
3. Run **Efficiency 2 Port** from the Marketing Release folder (`run.bat`).

Per load step (after soak):

- Scope **stop** → optional **PNG** in the run waveform folder → read measurements → scope **run**.

Per line voltage (after the usual Excel export at A and T):

- One **blank** row
- Row title: **Oscilloscope Measurements**
- Sub-table: **Ch1 Load**, **Ch2 Load**, plus dynamic columns (e.g. `CH1 Pk-Pk`, `CH2 Max`) from active MEAS slots

Multi–line-voltage sheets advance a **row cursor** so scope blocks do not overlap the next Vin section.

## Test Results UI

After each line-voltage block, the results table shows the same pattern: blank row → title row → scope header row → scope data rows (efficiency columns stay in the top header; scope uses extra columns as needed).

## Notes

- Scope capture runs only when the checkbox is on **and** `self.oscilloscope` is connected.
- Empty measurement dicts are skipped (no scope row for that step).
- Time estimate adds ~2.5 s per load step when scope measurement is enabled.
