# Manual control — where things live

## Open in Cursor (this workspace)

Your PI ATE clone is **`C:\Users\Charles\ATE`**. Open that folder in Cursor (**File → Open Folder**) if `@` and search should target ATE, not `charles-1`.

| What | Path |
|------|------|
| **Repo root (PI ATE)** | `C:\Users\Charles\ATE` |
| Default launcher (simulation) | `C:\Users\Charles\ATE\run.bat` → calls `run_simulation.bat` |
| Simulation launcher | `C:\Users\Charles\ATE\run_simulation.bat` |
| Physical bench launcher | `C:\Users\Charles\ATE\run_hardware.bat` |
| Oscilloscope panel (code) | `C:\Users\Charles\ATE\page_controls\manual_scope_panel.py` |
| Manual page handler (+ E-STOP, sim banner) | `C:\Users\Charles\ATE\page_controls\manual_control.py` |
| PML / discharge sequencer | `C:\Users\Charles\ATE\page_controls\pml_grid.py` |
| E-load grid | `C:\Users\Charles\ATE\page_controls\eload_grid.py` |
| Doc (scope + E-STOP) | `C:\Users\Charles\ATE\docs\Manual_Control_Scope_ESTOP.md` |
| Doc (less crowded layout) | `C:\Users\Charles\ATE\docs\Manual_Control_Less_Crowded.md` |
| Doc (this index) | `C:\Users\Charles\ATE\docs\Manual_Control_File_Locations.md` |
| UI mockup PNG | `C:\Users\Charles\ATE\docs\manual_control_ui_mockup.png` |
| Scope verify script | `C:\Users\Charles\ATE\scripts\verify_manual_control_scope_estop.py` |
| GitHub remote | `https://github.com/charlescayno/ATE` |

**In Cursor:** `Ctrl+P` → paste a path above, or use **File → Open File**.

## Run the app (see the real UI)

```bat
C:\Users\Charles\ATE\run.bat
REM or explicitly:
C:\Users\Charles\ATE\run_simulation.bat
```

Home → **Manual Equipment Control**. **Simulation banner** (when virtual bench) at top; **E-STOP** top-right; **oscilloscope** at bottom (Run / Run Single / Stop on the right).

## Captured PNGs from “Capture waveform”

Default folder (created on first capture):

`C:\Users\Charles\Documents\PI_ATE\manual_waveforms`

Filename comes from the **PNG filename** field on the scope panel (default `manual_capture.png`).

## Notes in `charles-1` repo

If you were browsing `C:\Users\Charles\charles-1`, that is a **different** git repo. PI ATE code changes are under **`C:\Users\Charles\ATE`** only until you copy or commit from there.
