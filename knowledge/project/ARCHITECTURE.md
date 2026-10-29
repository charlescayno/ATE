# Architecture

See also `architecture.md` and `threading_architecture.md` in repo root.

## Layers

| Layer | Location | Role |
|-------|----------|------|
| UI | `ui/`, `main.py` | Qt widgets, dark theme |
| Page controllers | `page_controls/` | Bridge UI → engine & equipment |
| Test engine | `psu_tests/` | TestTypes, TestItem, TestObject workers |
| Data / plots | `plotter/`, `data_process/` | Tables, PyQtGraph |
| HAL | `equipment/` | VISA, model-specific SCPI (`*_specs.py`) |
| USB-PD | `sink_controllers/`, `pd/` | Sink profiles, PDO/PPS |

## Runtime flow

```text
MainWindow → TestPlan → TestItem.run() → QThread + TestObject.run()
  → setup_equipment() → test_loop() → signals → UI plots / Excel
EquipmentHandler holds connected instrument instances (source, loads, PMs, scope).
```

## Threading

- UI thread must not block on SCPI.  
- Worker object pattern: `TestObject` in `QThread`, cross-thread signals (`Qt.QueuedConnection`).  
- Cooperative stop: `test_control_flags` (`StopTest`, `SkipTest`).

## Test registration

- `psu_tests/test_type.py` → `TestTypes` list defines Add Tests dropdown order and index stability (`resolve_test_type_index` for legacy titles).

## Simulation

- `equipment/simulated_handler.py` — virtual bench when GPIB absent or `-s`.
