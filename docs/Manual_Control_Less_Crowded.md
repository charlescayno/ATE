# Manual Equipment Control — less crowded

## Why it felt crowded

One screen was trying to show **everything at once**:

- Source PM + **4** load PM tiles (each with range/integration UI in gear dialogs, but tiles still large)
- DC source + HMP aux + **4** e-load tiles + USB PD
- Oscilloscope at the bottom **below the fold** on a laptop

## Changes (restart simulation to see)

1. **Scroll area** — Meters, source, and loads scroll; **header (E-STOP) and oscilloscope stay pinned** on the page.
2. **Hide unassigned channels** — PML CH3/4 and E-LOAD CH3/4 **hidden** when not in Equipment Setup (2-port benches use less grid space).
3. **Compact oscilloscope panel** — One header row (collapse + Run / Run Single / Stop + status); trigger and capture on **two** short rows; **▼** collapses details to a single bar.
4. **Flat layout (no box containers)** — Removed thick rounded borders on PM/e-load tiles and section frames; tiles use **content height** (no stretch-to-fill empty space). Header is one title row + optional SIM line (no overlapping 50px clip).
5. **Mission-control theme** (`page_controls/manual_control_theme.py`) — SpaceX-inspired: near-black canvas, monospace telemetry, thin dividers, flat 2px buttons, green nominal / red E-STOP.

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

### Simulation demo numbers

On entering Manual Control in simulation, the virtual bench defaults to **115 VAC**, **5 V @ 3 A** (load PM CH1) and **5 V @ 2 A** (CH2) so **Pin / ΣPout / Total Eff** and all meter readouts show realistic values. Set `PI_ATE_SIM_DEMO=0` before launch to skip this seed.
