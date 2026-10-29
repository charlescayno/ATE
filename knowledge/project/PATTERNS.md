# Patterns and conventions

## Equipment / SCPI

- Model classes in `equipment/*_specs.py`; registry in `equipment/definitions.py`.  
- `Equipment` + `@visa_io` retry decorator on facade methods (`equipment/equipment.py`).  
- `PowerMeter` delegates to `power_meter_object` by IDN model string.

## Tests

- Each test: class with `title`, `tc_default`, `unpack_test_item`, `setup_equipment`, `test_loop`, Excel helpers.  
- Register in `TestTypes` in `test_type.py` (order affects saved `TEST_TYPE_INDEX`).  
- Measurements often via `TestData.gather_data(integrate=True)` in `psu_tests/definitions.py`.  
- Soak: `SoakTime` (initial, per line, per load, **integration_time**).

## UI

- Page controllers attach to `MainWindow` widgets; avoid logic in generated `ui/ui_main.py` when possible.  
- Advanced options: gear dialogs (e.g. poll interval/duration in `add_test.py` I2C param indices 10–11).

## Git / agent (user)

- Feature branches: `cursor/<name>-ccf6` for cloud agent.  
- Touch `run.bat` mtime after PI ATE tasks on Windows clone (`always-touch-run-bat`).

## Token / docs

- Prefer `knowledge/project/*.md` + narrow file reads over whole-repo search.  
- Update `DECISIONS.md` when behavior changes materially.
