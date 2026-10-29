# Features

## Test types (active — `TestTypes` in `test_type.py`)

1. Steady-State Waveform 2 Port  
2. **Steady-State Poll Waveform 2 Port** — scope once + timed PM/scope rows  
3. Startup Waveform 2 Port  
4. Startup Waveform AC Turn-On (DER-1113)  
5. Efficiency 2 Port / 3 Port  
6. Load Regulation, Line Regulation, Efficiency  
7. No Load Input Power, CVCC  
8. Input Harmonics, Input Line Ramp  
9. Steady-State Waveform Capture (Vds/Ids)

Many I2C / Transients / Light Load classes exist but are **commented out** of `TestTypes`.

## Instruments (see README)

- PM: WT210/310/310E/**WT500** (`760202`), Chroma  
- AC/DC sources, Chroma/Kesight loads, USB-PD sinks, scope

## Poll test (feature summary)

- Params: poll interval (s), poll duration (s) on I2C param slots 10–11.  
- Defaults: **300 s** interval, **1200 s** duration (5 samples/point).  
- Default scope: **CH1** `VDS_PRI`, MAXimum, **1700 V** derating (CH2–4 off).  
- **Effective integration** = `max(soak.integration_time, poll_interval_s)` for WT500 timers (this test only).

## Manual control

- Live PM poll; integration timer temporarily set to 0 during fast poll (restored after).  
- Settings persisted (`manual_control_settings.json`).
- Magna HVDC line input: DC SOURCE UI (ramp, current limit) when primary role is Magna or AC role is unset and DC Source is Magna.  
- Equipment poll/init faults log to terminal as `[MANUAL_CONTROL] <role> (<fn>): …` (also in `app_log.txt`).

## USB-PD

- Optional PDO/PPS sequencing via sink controllers when enabled in test conditions.
