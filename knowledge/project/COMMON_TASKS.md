# Common tasks

## Run app

```bat
run.bat              REM hardware / default
run_simulation.bat   REM main.py -s
conda run -p .\conda_env python main.py
```

## Logging

- **Default:** all prints → console + `app_log.txt` (init, GPIB, SCPI, instruments).
- **Quiet console:** `set PI_ATE_MINIMAL_LOG=1` before launch.

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

## Add a feature (knowledge-first)

Follow **`WORKFLOW.md`**. Summary:

1. Read SUMMARY, KEY_FILES, FEATURES, PATTERNS (no repo-wide search).  
2. Edit only files KEY_FILES points to for that subsystem.  
3. Before merge: update FEATURES, DESIGN, DECISIONS, KEY_FILES (+ ARCHITECTURE/TESTING if needed).

## Git sync (cursor feature branch)

Cloud agents may commit locally but fail HTTPS push. On your PC (GitHub auth required):

```bat
scripts\git_sync_cursor_branch.bat
```

Or manually: `git fetch origin` → `git checkout cursor/poll-effective-integration-ccf6` → `git pull --rebase origin cursor/poll-effective-integration-ccf6` → `git push -u origin cursor/poll-effective-integration-ccf6`

Then merge PR #3 on GitHub or continue on the branch.

## Docs for agents

- Knowledge is source of truth for **context**; code is source of truth for **behavior** — sync docs when behavior changes.  
- Session handoff: agent store `pi-ate-*.md` + `DECISIONS.md`.
