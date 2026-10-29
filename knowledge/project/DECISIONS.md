# Design decisions

## Poll test: effective integration (2026)

**Decision:** For `SteadyStatePollWaveformTest_2Port` only, WT500 integration timer = **`max(soak.integration_time, poll_interval_s)`**, applied in `setup_equipment()` after parent setup.

**Rationale:** TST-326 soak integration defaults to 0; poll interval alone should still enable integrated Pin. Avoids mismatch when operators set 5 min poll but forget soak integration field.

**Tradeoffs:** Load PM ch1 integrates in sync with source via `synchronous_integration()`; ch2 remains instantaneous. Stop does not interrupt `poll_integration_status()` mid-window.

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
