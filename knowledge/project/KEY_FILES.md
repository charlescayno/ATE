# Key files

## Entry points

| File | Role |
|------|------|
| `main.py` | App bootstrap, simulation flag, MainWindow |
| `run.bat` / `run_simulation.bat` / `run_hardware.bat` | Windows launchers |
| `psu_tests/tests.py` | TestPlan, TestItem orchestration |
| `psu_tests/test_type.py` | **TestTypes** registry |
| `equipment/handler.py` | EquipmentHandler, detect/connect |
| `page_controls/add_test.py` | Add Tests UI, soak/line/load, poll timing gear |
| `page_controls/equipment_setup.py` | Bench assignment |
| `psu_tests/definitions.py` | SoakTime, TestData, TestConditions, settings |

## Power meters (WT500)

| File | Role |
|------|------|
| `equipment/definitions.py` | `760202` → `PowerMeterWT500` |
| `equipment/power_meter_specs.py` | `PowerMeterWT500`, INTEGRATE/NUMERIC SCPI |
| `equipment/power_meter.py` | Facade: `integration_settings`, `gather_data` delegation |
| `page_controls/manual_pm_range.py` | WT500 fixed range UI |

## 2-port / waveform / poll

| File | Role |
|------|------|
| `psu_tests/test_efficiency_2port.py` | Dual-port efficiency base, `setup_equipment` integration |
| `psu_tests/test_efficiency_2port_waveform.py` | Scope capture per point |
| `psu_tests/test_steady_state_poll_2port_waveform.py` | Timed poll rows + effective integration |

## Verify scripts

| File | Role |
|------|------|
| `scripts/test_poll_timing_headless.py` | No Qt; defaults + AST checks |
| `scripts/verify_steady_state_poll_2port_waveform.py` | Simulated poll test run |
