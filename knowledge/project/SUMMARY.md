# PI ATE — Project summary

**Name:** Power Integrations Automated Test Equipment (PI ATE)  
**Purpose:** Desktop app to automate bench characterization of AC-DC / DC-DC supplies (efficiency, regulation, harmonics, USB-PD, scope capture).  
**Stack:** Python 3.10, PySide2, PyVISA, PyQtGraph, pandas/openpyxl.  
**Platform:** Windows bench (GPIB/VISA); optional **simulation** (`main.py -s`, `run_simulation.bat`).  
**Repo:** [github.com/charlescayno/ATE](https://github.com/charlescayno/ATE)

## Core user flows

1. **Equipment Setup** — detect/bind AC source, loads, Yokogawa PMs (e.g. WT500 `760202`), scope, USB-PD sink.  
2. **Add Tests** — queue TestItems (type + line/load/soak/USB-PD/I2C options).  
3. **Run** — TestPlan runs each TestObject on a worker thread; live plots + Excel export.  
4. **Manual Equipment Control** — direct instrument control + PM polling.

## Authority docs in repo

- **`knowledge/project/WORKFLOW.md`** — how agents devs work (docs first, no full-repo scan)  
- `README.md` — features, instruments, quick start  
- `architecture.md`, `threading_architecture.md` — extended architecture (read only when WORKFLOW/ARCHITECTURE point here)  
- `knowledge/project/*` — agent-optimized index (this tree)

## Session memory (agent store)

Recent feature handoffs may live in agent store `pi-ate-steady-state-poll-2port.md` (poll + WT500 integration).
