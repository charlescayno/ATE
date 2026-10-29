# Deployment and environment

PI ATE is a **local Windows desktop app**, not a cloud service.

## Environment

- **Python 3.10** conda env (project `conda_env/` or user Anaconda).  
- **PySide2**, **PyVISA**, NI/VISA or compatible stack for GPIB.  
- Setup scripts under `setup/` (e.g. `activate_env.bat`).

## Launch

| Artifact | Use |
|----------|-----|
| `run.bat` | Primary launcher (physical bench) |
| `run_hardware.bat` | Anaconda + GPIB |
| `run_simulation.bat` | No bench |

Cloud Agent VMs may lack conda/GPIB; use simulation or headless scripts only.

## Configuration

- Equipment map: Equipment Setup UI → saved JSON.  
- Defaults: AppData shelve + `Documents/PI_ATE/*.json`.

## Releases

- GitHub repo `charlescayno/ATE`; PRs via cloud agent branch prefix `cursor/*-ccf6`.  
- No automated production deploy documented; distribution is clone + conda + bench.

## Environment builds (Cursor Cloud Agent)

- `.cursor/environment.json` / Builds page for agent VM snapshots; optional for local dev.
