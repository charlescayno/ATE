# Design decisions

## Poll test: Pin integration per sample (2026-10 v3)

**Decision:** For `SteadyStatePollWaveformTest_2Port`, WT500 **Pin integration = I2C param 10** (`Pin integration per sample (s)`). Soak integration is **not** used for poll Pin. Each sample: **integrate → read → scope → Excel**; sample **k+1** integration starts after sample **k** scope (next loop iteration). No separate idle poll wait. Param **11** = samples per load point (legacy ≥ 60 s = old duration).

**Rationale:** One UI knob for TST-326; avoids idle wait with no integration.

**Tradeoffs:** Load PMs stay timer 0. Long integrate windows use chunked wait + Stop checks in `_integrate_source_pin_before_read()`; read uses `source_pin_integration_done=True` to avoid double integration.

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
