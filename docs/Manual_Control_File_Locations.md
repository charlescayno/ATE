# Manual control — where things live

## Open in Cursor (this workspace)

Your PI ATE clone is **`C:\Users\Charles\ATE`**. Open that folder in Cursor (**File → Open Folder**) if `@` and search should target ATE, not `charles-1`.

| What | Path |
|------|------|
| Oscilloscope panel (code) | `C:\Users\Charles\ATE\page_controls\manual_scope_panel.py` |
| Manual page handler | `C:\Users\Charles\ATE\page_controls\manual_control.py` |
| Doc (scope + E-STOP) | `C:\Users\Charles\ATE\docs\Manual_Control_Scope_ESTOP.md` |
| UI mockup PNG | `C:\Users\Charles\ATE\docs\manual_control_ui_mockup.png` |

**In Cursor:** `Ctrl+P` → paste a path above, or use **File → Open File**.

## Run the app (see the real UI)

```bat
C:\Users\Charles\ATE\run.bat
```

Home → **Manual Equipment Control**. Oscilloscope block is at the **bottom**; **E-STOP** is top-right of the header.

## Captured PNGs from “Capture waveform”

Default folder (created on first capture):

`C:\Users\Charles\Documents\PI_ATE\manual_waveforms`

Filename comes from the **PNG filename** field on the scope panel (default `manual_capture.png`).

## Notes in `charles-1` repo

If you were browsing `C:\Users\Charles\charles-1`, that is a **different** git repo. PI ATE code changes are under **`C:\Users\Charles\ATE`** only until you copy or commit from there.
