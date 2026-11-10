# Design decisions

## WT500 error 844: guarded INTEGRATE:STOP (2026-10-30)

**Decision:** Yokogawa drivers query `INTEGRATE:STATE?` before `INTEGRATE:STOP`; skip STOP when state is STOP/TIM/RES/RESET/OFF. Poll setup no longer calls stop/reset after `integration_settings()`.

**Rationale:** Idle or post-TimeUp STOP caused front-panel error 844 during Steady-State Poll Waveform 2 Port setup and between samples.

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

## Rdson Measurements test type (2026-11)

**Decision:** New test type Rdson Measurements (RdsonMeasurementTest_2Port, psu_tests/test_rdson_measurements.py) subclasses SteadyStatePollWaveformTest_2Port and reuses its poll flow/params (10/11/12). Per sample it additionally reads RTO6 **Cursor 1..4** via oscilloscope.get_cursor(n) and writes **Cursor Result n Y1/Y2/dX/dY** columns (off cursors = N/A). No Rdson math; cursors are set up by the operator on the scope (Vds = CH1, Ids = CH2).

**Affected:** psu_tests/test_rdson_measurements.py, psu_tests/test_type.py, page_controls/add_test.py (POLL_WAVEFORM_TITLES), page_controls/test_sequence_flow_text.py, scripts/verify_rdson_measurements.py.


## Rdson Measurements: cursor assignment + Rds math (2026-11)

**Decision:** Cursors are assigned C1 = VDS #1, C2 = IDS #1, C3 = VDS #2, C4 = IDS #2 (pairs 1+2, 3+4). Per sample: Rds1 = C1.Y1/C2.Y1, Rds2 = C1.Y2/C2.Y2, Rds3 = C3.Y1/C4.Y1, Rds4 = C3.Y2/C4.Y2, Rds_avg = mean of the four (ohm, V/A). Any missing cursor or Ids ~ 0 gives N/A for that term and for Rds_avg. Supersedes the earlier 'no Rdson math' decision. Workbook name prefix is `OUTPUT_PREFIX` (RDSON; poll stays SSP).


## Poll/Rdson: 'No integration' option (2026-11)

**Decision:** I2C param **13** (`NO_INTEGRATION_PARAM_INDEX`, default 0) turns Pin integration off for `SteadyStatePollWaveformTest_2Port` and `RdsonMeasurementTest_2Port`. Param 10 then means **Time interval per sample (s)**: an idle gap *after the previous sample finished* (scope + Excel row) before the next one; none before the first sample of a load point. Pin = instantaneous read with WT500 averaging (timer 0). Excel: Time Integration Start/End = Time Sampled; metadata shows 'Time interval per sample (s)' and 'Pin integration (s)' = Off. GUI: checkbox in the poll timing frame relabels the field.

## Rdson Measurements defaults (2026-11)

**Decision:** `RdsonMeasurementTest_2Port.tc_default` now mirrors the bench plan `ATE_test_plan_without fan.json`: Vout1 48 V / Iout1 2 A (max 2 A), line Custom 860 V / 50 Hz DC, Full Load, soak TST-326, Option C with Vout2 20 V / Iout2 0.1 A / Fixed Aux 0.1 A, interval 30 s, 30 samples, fan off, **no integration on**, prompts None (Fully Automated), Auto Find Trigger No, CH1 VDS (derating 1700 V) / CH2 IDS, cursors off. Verified in `scripts/verify_rdson_measurements.py`.

- **Rdson fast capture:** Rdson sets `reapply_scope_before_capture=False` (scope setup applied once at start; per-sample relabel cost ~1 s/channel) and overrides `_wait_for_single_acquisition` to poll `ACQ:CURR?` (max 1 s, 50 ms steps) instead of fixed `sleep(1)`. Base hook defaults to `sleep(1)`; other tests unchanged. Hardware-unverified.
