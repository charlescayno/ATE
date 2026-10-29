# Design details

## TestData.gather_data (Pin / Pout)

Location: `psu_tests/definitions.py`.

- Reads Vin, Iin, PF as snapshots.  
- If integration timer > 0 and load PM active: `synchronous_integration()` for Pin + Pout (load 1).  
- Else if integrate: source-only integration path.  
- Timer 0 → instantaneous `power` property.

## Steady-State Poll Waveform 2 Port

Class: `SteadyStatePollWaveformTest_2Port` extends `EfficiencyWaveformTest_2Port`.

Per load point:

1. Sample 1: `_measure_poll_readings()` then scope capture.  
2. Samples 2…N: wait ~`poll_interval_s`, `_measure_poll_readings()`, scope meas refresh, Excel row with poll columns.  
3. `_effective_integration_s()` drives meter programming.

I2C param indices: **10** interval, **11** duration.

## PowerMeterWT500 integration SCPI

- Preset 4 → WH on numeric item 25.  
- `INTEGRATE:TIMER h,m,s` → START → poll STATE? until TIM/RES.  
- `get_integrated_power`: Wh → average W over window.

## Page controllers — poll UI

- Hidden line edits synced to I2C params; visible when poll test selected (`_apply_poll_timing_visibility`).  
- Flow text: `page_controls/test_sequence_flow_text.py`.

## Settings persistence

- User JSON under `%USERPROFILE%/Documents/PI_ATE/` (see `user_settings/save_load.py`).  
- Windows-oriented paths; cloud/Linux tests set `USERPROFILE` for imports.
