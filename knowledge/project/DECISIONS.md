# Design decisions

## Poll test: effective integration (2026)

**Decision:** For `SteadyStatePollWaveformTest_2Port` only, WT500 integration timer = **`max(soak.integration_time, poll_interval_s)`**, applied in `setup_equipment()` after parent setup.

**Rationale:** TST-326 soak integration defaults to 0; poll interval alone should still enable integrated Pin. Avoids mismatch when operators set 5 min poll but forget soak integration field.

**Tradeoffs:** Only **source** PM uses the poll timer in `_configure_poll_power_meter_integration()`; load PMs stay at timer 0 (instant P). Stop does not interrupt `poll_integration_status()` mid-window.

## 2-port load PMs: no integration (2026-10)

**Decision:** **Load PM Ch1 and Ch2** on 2-port tests use **timer 0** at setup. Models **WT310** and **WT310E** are in `INTEGRATION_DISABLED_MODELS` (`start_integration()` no-op; `gather_data_load()` never integrates).

**Rationale:** Only the **source** PM integrates for Pin on poll; load Pout is instant. Avoids GPIB timeouts from load-side `INTEGRATE:*` SCPI.

## Poll test UI defaults (2026-10)

**Decision:** `SteadyStatePollWaveformTest_2Port` default **User Prompts** = `None (Fully Automated)`; **Auto Find Trigger** = `No`.

## TestTypes order

**Decision:** Dual-port / waveform tests listed first in `TestTypes` for Add Tests dropdown grouping.

**Rationale:** Saved plans use index + title resolution (`resolve_test_type_index` legacy map).

## WT500 fixed range

**Decision:** WT500 does not force AUTO at connect; user/manual range UI (`manual_pm_range.py`).

**Rationale:** Avoid clipping; efficiency tests may force source AUTO before measure when OL risk.

## Knowledge folder

**Decision:** Maintain `knowledge/project/*.md` as agent-first index; long-form stays in `architecture.md` / README.

**Rationale:** Lower token use vs loading full architecture every chat.

---

When adding decisions: date, decision, rationale, affected files.
