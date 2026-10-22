# Manual Equipment Control — less crowded

## Why it felt crowded

One screen was trying to show **everything at once**:

- Source PM + **4** load PM tiles (each with range/integration UI in gear dialogs, but tiles still large)
- DC source + HMP aux + **4** e-load tiles + USB PD
- Oscilloscope at the bottom **below the fold** on a laptop

## Changes just made (restart simulation to see)

1. **Scroll area** — Meters, source, and loads scroll; **header (E-STOP) and oscilloscope stay pinned** on the page.
2. **Hide unassigned channels** — PML CH3/4 and E-LOAD CH3/4 **hidden** when not in Equipment Setup (2-port benches use less grid space).
3. **Compact oscilloscope panel** — One header row (collapse + Run / Run Single / Stop + status); trigger and capture on **two** short rows; **▼** collapses details to a single bar.

## What you can do in the UI

| Action | Effect |
|--------|--------|
| Scroll the middle section | See all equipment without losing scope |
| **▼** on oscilloscope | Collapse trigger/filename rows; keep Run/Stop in header |
| USB **◂** strip | Keep USB PD collapsed unless you need it |
| Gear **⚙** on PM/e-load | Ranges and slew live in dialogs, not on the tile |

## Optional next steps (not coded yet)

- **Tabs:** “Bench” vs “Scope only” full-width scope page
- **2-port layout preset:** Only CH1/CH2 tiles + hide CH3/4 labels entirely in grid
- **Smaller default window** sections with `QSplitter` drag resize
- Move **source PM** ranges entirely into gear (like PML grid already does for loads)

## Try it

```bat
C:\Users\Charles\ATE\run_simulation.bat
```

Open **Manual Equipment Control** and scroll the center; scope should stay visible at the bottom.
