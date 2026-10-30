# Design details

## TestData.gather_data (Pin / Pout)

Location: `psu_tests/definitions.py`.

- Reads Vin, Iin, PF as snapshots.  
- If integration timer > 0 and load PM active: `synchronous_integration()` for Pin + Pout (load 1).  
- Else if integrate: source-only integration path.  
- Timer 0 → instantaneous `power` property.

## Steady-State Poll Waveform 2 Port

Class: `SteadyStatePollWaveformTest_2Port` extends `EfficiencyWaveformTest_2Port`.

Default scope (Add Test → new poll item): **CH1** `VDS_PRI`, **MAXimum**, derating **1700 V**; CH2–4 off (`POLL_DEFAULT_SCOPE_CHANNELS` in `test_steady_state_poll_2port_waveform.py`).

Per load point (each sample):

1. Integrate Pin for **soak integration time** (not poll wait).  
2. `_measure_poll_readings()` → **`capture_waveform_at_point()`** (unique `_S{n}` PNG).  
3. Excel row → wait **`poll_interval_s`** → repeat for **N** samples.

I2C param indices: **10** poll wait between samples (s), **11** samples per load point (legacy: values ≥ 60 treated as old duration in s), **12** fan cooling (1 = HMP aux CH2 12 V / 4 A ON for the test).

Fan path uses `dc_source_aux` HMP (`prefer_hmp_as_aux()`), same as startup/smoke scripts; `setup_equipment()` applies preflight; `run()` `finally` turns CH2 OFF when fan was enabled.

## PowerMeterWT500 integration SCPI

- Preset 4 → WH on numeric item 25.  
- `INTEGRATE:TIMER h,m,s` → START → poll STATE? until TIM/RES.  
- `get_integrated_power`: Wh → average W over window.
- Terminal telemetry (`equipment/power_meter.py`): **Starting integration (interval … s)** and **Integration stopped after interval …** on the facade `start_integration` / `poll_integration_status` path (used by tests and poll Pin reads).

## Page controllers — poll UI

- Hidden line edits synced to I2C params; visible when poll test selected (`_apply_poll_timing_visibility`).  
- Flow text: `page_controls/test_sequence_flow_text.py`.

## Settings persistence

- User JSON under `%USERPROFILE%/Documents/PI_ATE/` (see `user_settings/save_load.py`).  
- Windows-oriented paths; cloud/Linux tests set `USERPROFILE` for imports.
