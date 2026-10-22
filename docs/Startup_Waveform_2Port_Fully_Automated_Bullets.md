# Startup Waveform 2 Port — fully automated (bullet summary)

## What “fully automated” means in PI ATE

- **User Prompts** set to **None (Fully Automated)** on the waveform test gear.
- That turns **off** the pre-test oscilloscope OK dialog and the **per-capture review** (Proceed / Recapture / Skip / Stop).
- It does **not** by itself remove the bulk-cap **OK** warning or the **Yes/No** charge/capture dialogs.
- For a **hands-off** run (simulation, CI, smoke scripts), also set **`PI_ATE_AUTO_CONFIRM=1`** (or `--auto-confirm` on the hardware smoke script) so those OK/Yes prompts auto-accept.

---

## Once at the start of the test

- **Optional:** run configured **output discharge pulses** on the DUT (if discharge count &gt; 0).
- **Bulk cap:** operator normally confirms discharge via OK dialog — **skipped** when `PI_ATE_AUTO_CONFIRM=1`.
- **Scope setup reminder** (load `.DFL`, probes, trigger channel): **skipped** in fully automated (no Pre-Test prompts).
- **Apply scope setup** to the oscilloscope automatically (labels, measurements, cursors as configured).

---

## For each input voltage (Vin) in the plan

- Turn **HMP aux DC OFF** so the bulk capacitor is **disconnected from the DUT**.
- **Charge step:** normally Yes/No — “charge bulk to this Vin?” — **auto Yes** with `PI_ATE_AUTO_CONFIRM=1`.
- If **Yes:** keep HMP OFF and **ramp or set** the line supply to that Vin (DC bulk ramp on Magna when applicable; AC sets frequency too).
- If **No:** **skip all load points** at that Vin (only matters when an operator clicks No).

---

## For each load point (Ch1 / Ch2) at that Vin

- **Set electronic loads** to the programmed Ch1 and Ch2 currents (dual-load mode, e.g. Option A).
- **Scope RUN SINGLE** — arm single-shot before the startup event.
- **Capture prompt:** normally Yes/No — “start startup capture?” — **auto Yes** with `PI_ATE_AUTO_CONFIRM=1`.
- **HMP aux DC ON** — connects bulk cap to DUT; **startup/inrush** happens here.
- **Wait** at least the **capture timeout** (default **10 s**, adjustable in advanced params).
- **Scope STOP** after the wait.
- **Per-capture review:** **skipped** in fully automated — no recapture loop from the UI.
- **Screenshot** saved as startup PNG (`*_SUW.png`), scope measurements read from the scope.
- **Scope RUN** (leave continuous mode), **HMP OFF** after capture.
- **Settle time**, then **measure efficiency** (power meters / loads) and **write Excel rows** (data + scope columns).
- **Post-capture delay**, then next load point.

---

## Between Vin blocks and at end

- After all loads at one Vin: **blank row** and **export** that Vin block to the workbook.
- After all Vin steps: **optional final discharge pulses**.
- **Format sheet**, **link/embed waveforms** on the SUW waveforms sheet when configured.

---

## What you do not get in fully automated mode

- No “check scope before we start” OK (unless you switch User Prompts to include **Pre-Test**).
- No operator review after each capture (unless you include **Per-Capture** in User Prompts).
- No **Recapture** path in practice (review is what offers Recapture).

---

## Bench / equipment assumptions (unchanged)

- **HMP** (e.g. HMP2030/4040) must be **Aux DC** in Equipment Setup; primary input is **not** the HMP.
- **Auto Find Trigger** is off for startup; trigger channel is fixed per plan.
- Efficiency is still measured **after HMP OFF** following each capture (same as interactive mode).

---

## Quick reference: interactive vs fully automated + auto-confirm

| Step | Per-Capture Only (default) | None (Fully Automated) + `PI_ATE_AUTO_CONFIRM=1` |
|------|----------------------------|--------------------------------------------------|
| Bulk discharge OK | Shown | Skipped |
| Scope pre-test OK | Skipped (default) | Skipped |
| Yes/No charge bulk | Shown | Auto Yes |
| Yes/No start capture | Shown | Auto Yes |
| Review capture | Shown | Skipped |
| HMP ON/OFF, wait, PNG, efficiency | Automatic | Automatic |

---

## See also

- [Full flowcharts — fully automated](./Startup_Waveform_2Port_Sequence_Fully_Automated.md)
- [Interactive sequence](./Startup_Waveform_2Port_Test_Sequence.md)
