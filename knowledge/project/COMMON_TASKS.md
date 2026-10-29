# Common tasks

## Run app

```bat
run.bat              REM hardware / default
run_simulation.bat   REM main.py -s
conda run -p .\conda_env python main.py
```

## Add a test to the dropdown

1. Implement class under `psu_tests/test_*.py` with `title`, `tc_default`.  
2. Import and append to `TestTypes` in `psu_tests/test_type.py`.  
3. Wire UI in `page_controls/add_test.py` if special fields needed.

## Change poll defaults / integration

- Edit constants in `psu_tests/test_steady_state_poll_2port_waveform.py`.  
- Update `scripts/verify_steady_state_poll_2port_waveform.py` and run headless script.

## WT500 integration in a test

1. `setup_equipment`: `power_meter_*.integration_settings(NORMAL, timer_s=…)`.  
2. At measure point: `start_integration` → `poll_integration_status` → `get_integrated_power()` or `TestData.gather_data()`.

## Verify without bench

```bat
python scripts\test_poll_timing_headless.py
python scripts\verify_steady_state_poll_2port_waveform.py
```

## Docs for agents

- Refresh `knowledge/project/*.md` when architecture or defaults change.  
- Append session notes to agent store + `DECISIONS.md` for durable rationale.
