# Efficiency 2 Port — Expected table output

This is what you should see in **Test Results** and in the Excel worksheet (`Efficiency 2 Port Test {Vout}V.xlsx`).

---

## Part 1 — Main efficiency table (always)

The table has **19 data columns** (Excel **A through S**). The top row of the block is the column header row.

| # | Column | Header (typical) | What you see |
|---|--------|------------------|--------------|
| 1 | A | Ch1 Load | Load label for port 1, e.g. `100%`, `75%`, `50%` |
| 2 | B | Ch2 Load | Port 2 label — matches mode (e.g. `100%`, `50%`, or `0.5A` for fixed aux) |
| 3 | C | VDC (rms) or VAC (rms) | Input setpoint for this line-voltage step |
| 4 | D | Freq (Hz) | Line frequency |
| 5 | E | Vin (rms) | Measured input voltage |
| 6 | F | Iin (mA) | Measured input current |
| 7 | G | Pin (W) | Measured input power |
| 8 | H | PF | Power factor |
| 9 | I | %THD | THD |
| 10 | J | Vo1 (V) | Port 1 output voltage |
| 11 | K | Io1 (A) | Port 1 output current |
| 12 | L | Po1 (W) | Port 1 output power |
| 13 | M | %V Reg 1 | Port 1 regulation vs nominal Vout1 |
| 14 | N | Vo2 (V) | Port 2 output voltage |
| 15 | O | Io2 (A) | Port 2 output current |
| 16 | P | Po2 (W) | Port 2 output power |
| 17 | Q | %V Reg 2 | Port 2 regulation vs nominal Vout2 |
| 18 | R | Po_Total (W) | Po1 + Po2 |
| 19 | S | Efficiency (%) | (Po_Total / Pin) × 100 |

**Row count:** one row per load step in the sweep (often 5 rows for 100% → 10%), repeated for each line voltage in your line range.

**Example data row** (numbers are illustrative):

| Ch1 Load | Ch2 Load | VDC (rms) | Freq | Vin | Iin (mA) | Pin (W) | PF | %THD | Vo1 | Io1 | Po1 | %V Reg 1 | Vo2 | Io2 | Po2 | %V Reg 2 | Po_Total | Efficiency (%) |
|----------|----------|-----------|------|-----|----------|---------|----|------|-----|-----|-----|----------|-----|-----|-----|----------|----------|----------------|
| 100% | 100% | 750 | 50.00 | 750.4 | 208 | 155.6 | 0.99 | 0.000 | 47.612 | 3.00 | 142.83 | -0.81 | 12.00 | 2.00 | 24.00 | 0.00 | 166.83 | 93.08 |

**Sanity checks:**

- **R** ≈ **L** + **P**
- **S** ≈ **R** / **G** × 100

---

## Part 2 — Regulatory columns (Excel only, same row as main data)

Starting at column **T** on the **same row** as the main header/data (not in columns N–Q):

| Col | Header | Notes |
|-----|--------|--------|
| T | Avg_Eff | May be empty until 2-port regulatory logic fills it |
| U | DOE6 Limit | |
| V | COC5 T2 Limit | |
| W | COC5_T2_10% | |
| X | Pass/Fail | |

In **Test Results**, you usually only see columns **A–S**; the T–X block is mainly in Excel.

---

## Part 3 — Between line-voltage blocks

After all load rows for one input voltage (e.g. 750 VDC):

- **Blank row** (empty cells across the efficiency columns)

Then either the next line-voltage block starts (same 19 headers + data rows), or (if scope is enabled) the oscilloscope block below.

---

## Part 4 — Oscilloscope sub-table (optional)

Only when **Measure Scope Ripple** is enabled and the scope returns measurements.

**Layout (below the efficiency block for that Vin):**

1. Blank row  
2. One row: first cell **Oscilloscope Measurements** (title)  
3. Header row for the scope sub-table  
4. One data row per load step where scope read succeeded (same order as the efficiency rows above)

**Scope sub-table columns:**

| Column | Content |
|--------|---------|
| Ch1 Load | Same label as column A for that step |
| Ch2 Load | Same label as column B for that step |
| *(dynamic)* | One column per active scope measurement, named like `CH1 Pk-Pk`, `CH1 Max`, `CH2 RMS`, … depending on your scope MEAS setup |

**Example** (if CH1 Pk-Pk and CH2 Max are configured):

| Ch1 Load | Ch2 Load | CH1 Pk-Pk | CH2 Max |
|----------|----------|-----------|---------|
| 100% | 100% | 0.042 | 12.05 |
| 75% | 75% | 0.038 | 12.04 |
| 50% | 50% | 0.035 | 12.03 |
| 25% | 25% | 0.031 | 12.02 |
| 10% | 10% | 0.028 | 12.01 |

If a load step returns no measurements, that step may have **no** scope row (efficiency row still present).

In **Test Results**, the scope title and scope headers appear as **extra rows** under the efficiency data; the widget’s top header row still lists the 19 efficiency columns, so scope columns may extend to the right on those lower rows.

---

## Full vertical picture (one line voltage, scope on)

```
[Header: 19 efficiency columns A–S]
[100% / 100%  … efficiency data …]
[75%  / 75%   …]
…
[10%  / 10%   …]
[blank row]
Oscilloscope Measurements
Ch1 Load | Ch2 Load | CH1 Pk-Pk | CH2 Max | …
100%     | 100%     | 0.042     | 12.05   | …
…
[blank row]                    ← before next Vin block
[Header + efficiency rows for next Vin]
…
```

---

## What is *not* in the main table

- **Vo2 / Io2 / Po2 / %V Reg 2** must stay in **N–Q** — not regulatory limit text.
- Scope values are **not** mixed into columns A–S; they live in the **separate block below** each Vin section (when enabled).

---

**See also:** `docs/efficiency_2port_expected_output.md` (full spec and troubleshooting).
