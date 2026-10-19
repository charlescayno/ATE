# Efficiency 2 Port (Waveform) — Expected Output

**Implementation:** `psu_tests/test_efficiency_2port_waveform.py` (`EfficiencyWaveformTest_2Port`, a subclass of `EfficiencyTest_2Port`).
**Verification:** `scripts/verify_efficiency_2port_waveform.py` runs Option A and Option B against the simulated equipment and checks the workbook.

## Where results appear

| Location | Path / UI |
|---|---|
| Excel file | `{output folder}/Efficiency 2 Port (Waveform) Test {Vout}V.xlsx` |
| Data worksheet | `Eff2PWF_{AC\|DC}_{Vout}V_{Iout}A` |
| Waveforms worksheet | `Eff2P_WF_Waveforms` (only when Embed in Excel = Yes) |
| Screenshots | `{output folder}/waveforms/{UnitID}_{Vin}V{AC\|DC}_Ch1_{I1}A_Ch2_{I2}A.png` |
| In-app | Test Results: same columns as Excel A–S, then the scope columns. The T–X limits block is Excel only. |

## Data worksheet layout

- **Row 1:** test title.
- **Row 2:** Unit ID, ambient temperature, Ch1 and Ch2 nominals, dual-load mode, probe setup, trigger channel.
- **Row 4:** merged section titles:

| Columns | Section |
|---|---|
| A–S | Same as Efficiency 2 Port (Load Condition … Total Power & Efficiency) |
| T–X | Average Efficiency Limits |
| Y onward | Oscilloscope Measurements |

- **Row 5:** column headers.
  - **A–S:** Ch1 Load, Ch2 Load, V(AC/DC) (rms), Freq, Vin, Iin, Pin, PF, %THD, Vo1, Io1, Po1, %V Reg 1, Vo2, Io2, Po2, %V Reg 2, Po_Total, Efficiency (%).
  - **T–X:** Avg_Eff, DOE6 Limit, COC5 T2 Limit, COC5_T2_10%, Pass/Fail.
  - **Y onward:** `Trig Ch`, `Trig Level (V)`, one column per configured scope measurement, then `Waveform File`.
- **Rows 6+:** one row per load point. Each line-voltage block is followed by one blank row. As in Efficiency 2 Port, only the first block has the header row.

Which scope measurement columns appear depends on the channel matrix:

- Each enabled channel adds `{name} {Max|Min|Mean|RMS|Pk-Pk}` for each measurement selected under its ⚙ button. If none are selected, it adds `{name} Max`.
- A channel with a derating limit adds `{name} Derating (%)` after its Max column.
- A channel with its cursor enabled adds `{name} dX`, `{name} Fsw (kHz)` and `{name} dY`.

**Example with the defaults** (CH1 "Primary Vds" with a 650 V derating limit, CH2 "Ids"):
`Trig Ch | Trig Level (V) | Primary Vds Max | Primary Vds Derating (%) | Ids Max | Waveform File`

## Per-point behaviour

1. Set both loads, soak, then wait the settle time.
2. Measure efficiency (Pin, Po1, Po2, Po_Total, efficiency, %V Reg 1 and 2).
3. Capture the waveform. Find the trigger first if Auto Find Trigger is on. Show the prompt if User Prompts includes "Per-Capture".
   - **Capture & Proceed:** saves the screenshot and records the measurements.
   - **Recapture / Retrigger:** re-triggers at the same point. The efficiency reading is kept.
   - **Skip Point:** keeps the efficiency row. The scope cells show `N/A` and the waveform file is blank.
   - **Stop Test:** stops the test.
4. Wait the post-capture delay.

At the end of the test, the outputs are discharged Discharge Pulses times, and the screenshots are embedded if Embed in Excel is Yes.

## Plots (Test Results)

Efficiency vs Load, Channel 1 Regulation, Channel 2 Regulation, and Max Vds vs Input Voltage. The Vds plot has one series per load pair, plus a derating-limit line when a limit is set.
