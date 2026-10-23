# Manual Equipment Control — oscilloscope & E-STOP

## Layout

- **E-STOP** — top-right of the page header (all outputs off).
- **Oscilloscope** — full-width panel **below** all equipment (meters, source, loads, USB PD).

## Oscilloscope panel

| Control | Action |
|---------|--------|
| **Run** | Continuous acquisition |
| **Run Single** | Single-shot |
| **Stop** | Stop acquisition |
| **Trigger mode** + **Apply mode** | Auto / Normal / Freerun (R&S SCPI or LeCroy VBS) |
| **Trigger source** + **Trigger level (V)** + **Apply level** | Edge trigger on CH1–CH4 |
| **PNG filename** | Name for capture (`.png` added if missing) |
| **Capture waveform** | **Stop** acquisition, then `get_screenshot()` → `Documents\PI_ATE\manual_waveforms\` (if the name exists, saves as `name_1.png`, `name_2.png`, …) |

Filename and trigger settings are saved in `manual_control_settings.json` with other manual page fields.

## Code

- `page_controls/manual_scope_panel.py` — bottom panel UI and scope actions
- `page_controls/manual_control.py` — E-STOP toolbar, delegates to `scope_panel`

## Verify

```bat
set PI_ATE_SIMULATION=1
python scripts\verify_manual_control_scope_estop.py
```
(run in PI ATE conda env with PySide2)
