# Run PI ATE in simulation (no GPIB bench)

**Yes.** Simulation uses `SimulatedEquipmentHandler` — no real instruments.

## Easiest (this clone)

Double-click or from a cmd prompt:

```bat
cd /d C:\Users\Charles\ATE
run_simulation.bat
```

Same as:

```bat
set PI_ATE_SIMULATION=1
python main.py -s
```

(but `python` must be the **PI ATE conda env**, not base Anaconda.)

## Conda env on your PC

| Location | Status |
|----------|--------|
| `C:\Users\Charles\ATE\conda_env\` | **Missing** in this clone |
| `C:\Users\Charles\.gemini\antigravity\scratch\ATE\conda_env\` | **Present** — `run_simulation.bat` uses this as fallback |

To make `run.bat` work without fallback, copy the whole `conda_env` folder into `C:\Users\Charles\ATE\`, or recreate the env from project docs.

## CLI flags (`main.py`)

- `-s` or `--simulation` — force simulation
- `-hw` or `--hardware` — force real GPIB scan (no auto-fallback to sim)

If you start **without** `-s` and **no** hardware is found, the app **auto-enables** simulation anyway.

## Quick test (no GUI window)

```bat
cd /d C:\Users\Charles\ATE
set PI_ATE_SIMULATION=1
C:\Users\Charles\.gemini\antigravity\scratch\ATE\conda_env\python.exe scripts\verify_manual_control_scope_estop.py
```

Should print: `OK manual control scope panel + E-STOP`

## In the GUI

After `run_simulation.bat`: open **Manual Equipment Control** — simulated meters/loads/scope respond without bench hardware.

Captures still go to: `C:\Users\Charles\Documents\PI_ATE\manual_waveforms\`
