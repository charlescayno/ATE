# Testing

## Tiers

| Tier | What | Where |
|------|------|--------|
| Headless | Constants, AST, no Qt | `scripts/test_poll_timing_headless.py` |
| Simulated Qt | Full poll test, mocked sleep | `scripts/verify_steady_state_poll_2port_waveform.py` |
| Hardware smoke | GPIB bench | `scripts/run_startup_2port_hardware_smoke.py`, manual |
| WT500 range | Fake device | `scripts/verify_wt500_fixed_range.py` |

## Requirements

- **Windows + PI ATE conda env** (PySide2, pyvisa, pandas, openpyxl) for full verify.  
- Linux CI/cloud often lacks conda env; PySide2 may segfault without display.

## Agent verification rule

Run headless or targeted script before claiming done (`always-verify-code` user skill).

## After code changes (poll / defaults)

1. `python scripts/test_poll_timing_headless.py`  
2. `python scripts/verify_steady_state_poll_2port_waveform.py` (Windows env)  
3. Optional: one simulated point in UI (`run_simulation.bat`)

## Updating tests when defaults change

- Adjust expected values in `verify_steady_state_poll_2port_waveform.py`.  
- Keep `test_type.py` registration checks if order matters.
