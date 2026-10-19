# Expected UI — "Efficiency 2 Port (Waveform)"

These are text mockups of what the new test will look like, based on the confirmed plan. Exact spacing and colours will follow the existing dark theme, and the real widgets reuse what Efficiency 2 Port and Steady-State already show. Default values come from the two existing tests and can be changed.

---

## 1. Add Tests page: test selection and general options

```
┌─ Add Tests ──────────────────────────────────────────────────────────────────┐
│ Test Type: [ Efficiency 2 Port (Waveform)                              ▼ ]   │
│                                                                              │
│ Unit ID: [ 00   ]                       ← now shown (Unit ID bug fixed)      │
│                                                                              │
│ ☐ USB-PD Device                          Coupling: [ AC ▼ ]                  │
│ Load Type: [ CC ▼ ]   ☑ Use E-Load Data   Load Direction: [ High to Low ▼ ]  │
│                                                                              │
│ ( "Measure Scope Ripple" checkbox is hidden: scope capture is always on )    │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Line Voltage Range and Load Current Range pages

These are the same as Efficiency 2 Port today: line-range preset or custom, and a load-range preset (default LOAD_EFF: 100/75/50/25/10 %). The load range table is editable, and the Soak Time settings are unchanged.

```
┌─ Line Voltage Range ──────────┐   ┌─ Load Current Range ─────────────────────┐
│ Preset: [ UNIVERSAL ▼ ]       │   │ Preset: [ LOAD_EFF ▼ ]  (unlocked)       │
│  90 VAC  60 Hz                │   │  Load %  |  Ch1 Iout (A)                 │
│ 115 VAC  60 Hz                │   │  100     |  5.00                         │
│ 230 VAC  50 Hz                │   │   75     |  3.75                         │
│ 265 VAC  50 Hz                │   │   50     |  2.50   ...                   │
└───────────────────────────────┘   └──────────────────────────────────────────┘
```

---

## 3. Settings panel (page 3): Output 1, Output 2, Scope and Trigger

This panel combines the "Output 1 / Output 2 Settings" layout from Efficiency 2 Port with the scope channel matrix and trigger settings from Steady-State.

```
┌─ Output 1 Settings ──────────────────────────────────────────────────────────┐
│ Nominal Vout 1 (V) [ 5    ]        Nominal Iout 1 (A) [ 5    ]               │
├─ Output 2 Settings ──────────────────────────────────────────────────────────┤
│ Nominal Vout 2 (V)   [ 12   ]      Nominal Iout 2 (A)   [ 2    ]             │
│ Fixed Aux Load (A)   [ 0    ]      Port 2 Loads (%)     [ 100, 50, 0 ]       │
│ Dual Load Mode       [ Option A: Proportional Sync (Both Ports 100%->10%) ▼ ]│
├─ Scope & Trigger Settings  (i) ──────────────────────────────────────────────┤
│  Scope channels (name + ⚙ per-channel measurements / derating / cursor):     │
│   ☑ CH1: [ Primary Vds ] ⚙         ☑ CH2: [ Ids         ] ⚙                  │
│   ☐ CH3: [             ] ⚙         ☐ CH4: [             ] ⚙                  │
│                                                                              │
│ Trigger Channel (1-4) [ 1    ]     Trigger Delta          [ 3    ]           │
│ Settle Time (s)       [ 1    ]     Discharge Pulses       [ 2    ]           │
│ Ambient Temp (°C)     [ 25   ]     Post-Capture Delay (s) [ 1    ]           │
│                                                                              │
│ Embed in Excel        [ Yes                     ▼ ]                          │
│ User Prompts          [ Pre-Test & Per-Capture  ▼ ]                          │
│ Auto Find Trigger     [ No                      ▼ ]                          │
└──────────────────────────────────────────────────────────────────────────────┘
```

How the panel's slots are used:

| Slot | Field |
|---|---|
| Text field 1 | Nominal Vout 2 (V) |
| Text field 2 | Nominal Iout 2 (A) |
| Text field 3 | Fixed Aux Load (A) |
| Text field 4 | Port 2 Loads (%) |
| Text field 5 | Trigger Delta |
| Text field 6 | Settle Time (s) |
| Text field 7 | Discharge Pulses |
| Text field 8 | Ambient Temp (°C) |
| Text field 9 | Post-Capture Delay (s) |
| Text field 10 | **Trigger Channel (1–4)**, which used to be a dropdown |
| Dropdown 1 | Dual Load Mode |
| Dropdown 2 | Embed in Excel |
| Dropdown 3 | User Prompts |
| Dropdown 4 | Auto Find Trigger |

**As built:** the panel heading reads "Output 2 / Scope & Trigger Settings". The scope channel matrix sits below the dropdowns (grid row 8), with the Dual Load Mode description just above it (row 7). The (i) FAQ button is not included in this version; it is still available on Steady-State.

---

## 4. Test list entry (Test Plan / Run page)

```
Efficiency 2 Port (Waveform): Ch1: 5V, 5A | Ch2: 12V, 2A
Mode: Option A: Proportional Sync
Trigger: CH1 (Delta: 3V) | Prompts: Pre-Test & Per-Capture
Status: Capturing waveform...        Upcoming: Capture Waveform
IN PROGRESS: 0:42:10, 35%
Line Range: UNIVERSAL, Load Range: LOAD_EFF, Coupling: AC
Load Measurement: Electronic Load
```

---

## 5. Pop-ups during the run

**Before the test starts** (when User Prompts includes "Pre-Test"):

```
┌─ Oscilloscope Setup Verification ───────────────────────────┐
│ Unit ID: 00 | Ambient Temp: 25°C                            │
│ Ch1: 5 V / 5 A    Ch2: 12 V / 2 A    Mode: Option A         │
│ 1. Load the correct .DFL file into the oscilloscope.        │
│ 2. Probe Configuration: CH1: Primary Vds, CH2: Ids          │
│ 3. Trigger Channel: CH1 (Delta: 3 V)                        │
│                                                [   OK   ]   │
└─────────────────────────────────────────────────────────────┘
```

**At each load point** (when User Prompts includes "Per-Capture"). By the time this appears, the efficiency for this point has already been measured:

```
┌─ Capture Waveform (115 VAC, Ch1 100% / Ch2 100%) ───────────┐
│ Operating Point: 115 VAC | Ch1 5 A | Ch2 2 A                │
│ Efficiency: 89.42 %   Pin: 55.9 W   Po_Total: 50.0 W        │
│ Trigger Level: CH1 @ 412.50 V                               │
│ Live Measurements:                                          │
│   Primary Vds Max: 455.2                                    │
│   Primary Vds Derating (%): 70.03                           │
│   Ids Max: 1.84                                             │
│                                                             │
│ [Capture & Proceed] [Recapture / Retrigger] [Skip] [Stop]   │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Test Results page

**Plots dropdown:** Efficiency vs Load · Channel 1 Regulation · Channel 2 Regulation · Max Vds vs Input Voltage (with a derating limit line if one is set).

**Data table:** one row per load point. The efficiency columns come first, then the scope columns. The values below are illustrative.

| Ch1 Load | Ch2 Load | VAC (rms) | Freq (Hz) | Vin (rms) | Iin (mA) | Pin (W) | PF | %THD | Vo1 (V) | Io1 (A) | Po1 (W) | %V Reg 1 | Vo2 (V) | Io2 (A) | Po2 (W) | %V Reg 2 | Po_Total (W) | Efficiency (%) | Trig Ch | Trig Level (V) | Primary Vds Max | Primary Vds Derating (%) | Ids Max | Waveform File |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100% | 100% | 115 | 60 | 115.1 | 812 | 55.9 | 0.60 | 95.1 | 4.98 | 5.00 | 24.90 | -0.40 | 11.96 | 2.00 | 23.92 | -0.33 | 48.82 | 87.33 | CH1 | 412.5 | 455.2 | 70.03 | 1.84 | …\waveforms\00_115VAC_Ch1_5A_Ch2_2A.png |
| 75% | 75% | 115 | 60 | 115.1 | 618 | 41.6 | 0.59 | 96.0 | 4.99 | 3.75 | 18.71 | -0.20 | 11.97 | 1.50 | 17.96 | -0.25 | 36.67 | 88.15 | CH1 | 405.0 | 448.9 | 69.06 | 1.41 | … |
| 10% | 10% | 115 | 60 | 115.0 | 98 | 5.6 | 0.45 | 120.3 | 5.01 | 0.50 | 2.51 | 0.20 | 12.02 | 0.20 | 2.40 | 0.17 | 4.91 | 87.68 | CH1 | 380.5 | 421.3 | 64.82 | 0.39 | … |
| *(blank row between line voltages)* | | | | | | | | | | | | | | | | | | | | | | | | |

If a point is **skipped** at the prompt, its efficiency columns are filled in and its scope columns show `N/A`.

Which scope columns appear depends on the channel matrix. Each enabled channel adds its configured measurements (Max, Min, Mean, RMS, Pk-Pk). A channel with a derating limit also adds a `Derating (%)` column, and a channel with its cursor enabled adds `dX`, `Fsw (kHz)` and `dY`.

---

## 7. Excel output

**Workbook:** `Efficiency 2 Port (Waveform) Test {Vout}V.xlsx`

**Data sheet** (row 4 holds the merged section titles; the data headers start at row 5):

```
 A–B             C–D        E–I                 J–M               N–Q               R–S                    T–X                          Y →
┌──────────────┬──────────┬───────────────────┬─────────────────┬─────────────────┬──────────────────────┬────────────────────────────┬──────────────────────────────────────┐
│Load Condition│Input Set │Input Measurement  │Output 1 Meas.   │Output 2 Meas.   │Total Power & Eff.    │Average Efficiency Limits   │Oscilloscope Measurements             │
├──────────────┴──────────┴───────────────────┴─────────────────┴─────────────────┴──────────────────────┴────────────────────────────┴──────────────────────────────────────┤
│Ch1 Load|Ch2 Load|VAC|Freq|Vin|Iin|Pin|PF|%THD|Vo1|Io1|Po1|%VReg1|Vo2|Io2|Po2|%VReg2|Po_Total|Eff%|Avg_Eff|DOE6|COC5 T2|COC5 10%|P/F|Trig Ch|Trig Lvl|Vds Max|Derating%|Ids Max|File│
│ 100%   | 100%   |115|60  |...                                                                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Waveforms sheet** (created when Embed in Excel = Yes). Images are laid out two per row, each with a caption:

```
┌──────────────────────────────────────┐   ┌──────────────────────────────────────┐
│115 VAC, Ch1 5 A / Ch2 2 A | Vds Max: │   │115 VAC, Ch1 3.75 A / Ch2 1.5 A | ... │
│455.2 | Ids Max: 1.84                 │   │                                      │
│ ┌──────────────────────────────────┐ │   │ ┌──────────────────────────────────┐ │
│ │       [scope screenshot]         │ │   │ │       [scope screenshot]         │ │
│ └──────────────────────────────────┘ │   │ └──────────────────────────────────┘ │
└──────────────────────────────────────┘   └──────────────────────────────────────┘
```

**Screenshot file names:** `{UnitID}_{Vin}VAC_Ch1_{I1}A_Ch2_{I2}A.png`, saved in `{output folder}\waveforms\`.
