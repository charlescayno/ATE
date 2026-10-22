# Power Integrations Automated Test Equipment (PI ATE)

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![UI: PySide2](https://img.shields.io/badge/GUI-PySide2-green.svg)](https://pypi.org/project/PySide2/)

A Python-based automated testing and validation suite designed for Power Integrations power supply designs. PI ATE automates bench instrument control, data acquisition, USB-PD profile sequencing, and real-time data plotting.

**Repository:** [github.com/charlescayno/ATE](https://github.com/charlescayno/ATE)

---

## Table of Contents
1. [Key Features](#key-features)
2. [Supported Tests](#supported-tests)
3. [Supported Instruments](#supported-instruments)
4. [Quick Start](#quick-start)
5. [Installation & Setup](#installation--setup)
6. [Manual Equipment Control](#manual-equipment-control)
7. [VS Code Configuration](#vs-code-configuration)
8. [Architecture & System Design](architecture.md)
9. [Project Structure](#project-structure)
10. [Troubleshooting](#troubleshooting)

---

## Key Features

* **Automated Test Sequencing**: Create, re-order, queue, and execute multi-condition test plans.
* **USB-PD / PPS Support**: Automatic detection and testing across fixed PDOs and Augmented PPS ranges using hardware sink controllers.
* **Interactive Data & Plots**: Real-time graphing (Efficiency, Voltage/Current curves) and dynamic data tables with export capabilities.
* **Dual Logging**: Console output and persistent execution logging (`app_log.txt`) for diagnostics and traceability.
* **Instrument Abstraction Layer**: Resilient SCPI communication with automatic retries and safe data conversion.
* **Manual Equipment Control**: Direct control of DC/AC sources, up to four electronic load channels, and live power meter readouts from the bench tab.
* **Persistent Manual Control UI**: Input fields on the Manual Equipment Control tab are saved to `manual_control_settings.json` and restored on the next launch.

---

## Supported Tests

* **Efficiency Test**: Measures active input power, output power, and calculates efficiency across load/line steps.
* **Load Regulation**: Sweeps output current while monitoring output voltage stability and ripple.
* **Line Regulation**: Evaluates regulation performance over varying AC input voltages.
* **No-Load / Standby Power**: Measures low-power standby consumption with power meter integration.
* **CV/CC Characterization**: Maps constant voltage and constant current transitions.
* **Input Harmonics**: Measures current harmonics and THD according to regulatory standards (e.g., IEC 61000-3-2).
* **Input Line Ramp**: Automated AC voltage slew rate and brown-in/brown-out testing.
* **Transients & Dynamic Load**: Step-load response and transient overshoot/undershoot measurement.

---

## Supported Instruments

* **Power Meters**: Yokogawa WT210, WT310, WT310E, WT500, Chroma 66200 Series.
* **AC Power Sources**: Chroma 61500 / 61600 Series, Keysight / Agilent AC Sources.
* **Electronic Loads**: Chroma 6310 / 6314 / 63600 Series, Keysight N3300 Series.
* **USB-PD Sinks / Controllers**: Cypress CY4500, PI STM32 EPR Sink Controller.

---

## Quick Start

### 1. Launching the Application
If your environment is already set up, double-click (both start **virtual simulation**):
```bat
run.bat
run_simulation.bat
```
For the physical bench (GPIB / Anaconda env), use `run_hardware.bat`.

From a terminal (without activating conda manually):
```bat
conda run -p .\conda_env python main.py
```

Or activate the project environment and run:
```bat
setup\activate_env.bat
python main.py
```

---

## Manual Equipment Control

The **Manual Equipment Control** tab (`page_controls/manual_control.py`) is for interactive bench work outside automated test plans.

| Area | Behavior |
|------|----------|
| **Electronic load** | Channels 1–4 support Load ON / Load OFF with consistent styling and SCPI control when roles are assigned in Equipment Setup. |
| **DC source ramping** | Long voltage ramps temporarily pause GPIB polling so VISA timeouts are less likely during slow slews. |
| **Power meters (PML / PMS)** | Live V, A, W, and efficiency update when the mapped instrument is connected and responding. |
| **Settings file** | `manual_control_settings.json` in the project root stores line edits, combo indices, and checkboxes under the manual control page. Delete this file to reset to UI defaults. |

Configure hardware roles (Source, PML 1–4, Electronic Load 1–4, etc.) on the **Equipment Setup** tab before using manual control. Unassigned or disconnected power meter load slots show **None** on the displays and may leave related dropdowns empty until a device is mapped and online.

---

## Installation & Setup

### Option A: Automatic Setup (Fresh Install)
Run the automated setup script to create the conda environment, install dependencies, and configure required DLLs:
```bat
setup.bat
```

### Option B: Update Existing Setup
If you already have the conda environment created and only need to update packages:
```bat
install_dependencies.bat
```

### Option C: Manual Conda Setup
1. Open Anaconda Prompt / PowerShell.
2. Create and activate a Python 3.10 environment:
   ```bash
   conda create -p ./conda_env python=3.10 -y
   conda activate ./conda_env
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## VS Code Configuration

### 1. Select Python Interpreter
1. Press `Ctrl + Shift + P` in VS Code.
2. Type and select `Python: Select Interpreter`.
3. Choose `./conda_env/python.exe` (or your Anaconda Python 3.10 path).

### 2. Debugging Configuration (`launch.json`)
To enable smooth debugging without stepping into external libraries, add the following to `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Main.py",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "justMyCode": false
        }
    ]
}
```

---

## Project Structure

```
├── main.py                       # Application entry point and main window event loop
├── run.bat                       # Default launcher → simulation (calls run_simulation.bat)
├── run_simulation.bat            # Virtual bench (conda_env + PI_ATE_SIMULATION=1)
├── run_hardware.bat              # Physical bench (setup/activate_env.bat + main.py)
├── setup.bat                     # Automated fresh install script
├── install_dependencies.bat      # Updates packages in existing environment
├── requirements.txt              # Python package dependencies
├── conda_env/                    # Local conda environment (created by setup)
├── manual_control_settings.json  # Auto-saved Manual Equipment Control UI state (runtime)
├── app_log.txt                   # DualLogger stdout/stderr capture (runtime)
│
├── equipment/               # Instrument drivers (AC Source, E-Load, Power Meter)
│   ├── equipment.py         # VISA I/O decorator and base hardware classes
│   ├── power_meter_specs.py # Yokogawa & Chroma SCPI drivers
│   └── handler.py           # Equipment discovery and session manager
│
├── page_controls/           # UI Controller logic per page
│   ├── add_test.py          # Test plan builder and execution service
│   ├── test_results.py      # Results table and interactive plot handler
│   ├── manual_control.py    # Direct bench instrument manual control
│   └── equipment_setup.py   # Hardware connection and port configuration
│
├── psu_tests/               # Test definitions, routines, and worker threads
│   ├── tests.py             # TestPlan and TestItem queue manager
│   ├── test_efficiency.py   # Efficiency test routine
│   ├── test_load_reg.py     # Load regulation test routine
│   └── ...                  # Other test modules
│
├── plotter/                 # Data structures and PyQtGraph plotting utilities
├── sink_controllers/        # USB-PD and PPS sink controller communication
└── ui/                      # Qt Designer UI definitions and icon resources
```

---

## Troubleshooting

* **PowerShell Execution Policy Error**:
  If PowerShell blocks the activation script:
  ```powershell
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
* **VISA / Instrument Not Found**:
  * Ensure [NI-VISA](https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html) runtime is installed.
  * Verify USB / GPIB / RS232 connections and check device addresses in **Equipment Setup**.
* **Power meter load shows "None" or empty dropdowns**:
  * Assign the instrument to the correct **Power Meter Load** role in Equipment Setup and confirm the session opens without VISA errors.
  * Efficiency reads **None** when input power is zero or either meter reading is invalid.
* **Manual control values wrong after upgrade**:
  * Remove or edit `manual_control_settings.json` if widget names changed between releases.
* **Logs & Error Details**:
  * All stdout, stderr, and uncaught exceptions are automatically captured in `app_log.txt` in the root folder.
