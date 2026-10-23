# Manual Equipment Control — E-STOP

## Layout

- **E-STOP** — top-right of the page header (all outputs off).

## Oscilloscope controls

The oscilloscope section was removed from Manual Equipment Control. Use the
dedicated **Oscilloscope** page or an automated waveform test for scope setup,
triggering, and capture.

## Code

- `page_controls/manual_control.py` — Manual Control layout and E-STOP toolbar
- `page_controls/oscilloscope_control.py` — dedicated Oscilloscope page

## Verify

```bat
set PI_ATE_SIMULATION=1
python scripts\verify_manual_control_scope_estop.py
```
(run in PI ATE conda env with PySide2)
