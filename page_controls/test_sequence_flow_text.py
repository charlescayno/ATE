"""High-level test sequence copy for Add Test flow (➜) dialog."""

STEADY_STATE_WAVEFORM_2PORT_TITLE = "Steady-State Waveform 2 Port"
STEADY_STATE_POLL_WAVEFORM_2PORT_TITLE = "Steady-State Poll Waveform 2 Port"
STARTUP_WAVEFORM_2PORT_TITLE = "Startup Waveform 2 Port"
STARTUP_WAVEFORM_AC_TURNON_TITLE = "Startup Waveform AC Turn-On (DER-1113)"
EFFICIENCY_2PORT_WAVEFORM_LEGACY_TITLE = "Efficiency 2 Port (Waveform)"

FLOW_TITLES = (
    STEADY_STATE_WAVEFORM_2PORT_TITLE,
    STEADY_STATE_POLL_WAVEFORM_2PORT_TITLE,
    EFFICIENCY_2PORT_WAVEFORM_LEGACY_TITLE,
    STARTUP_WAVEFORM_2PORT_TITLE,
    STARTUP_WAVEFORM_AC_TURNON_TITLE,
)


def _step(active: bool, label: str) -> str:
    if active:
        return label
    return f"(skipped — not in User Prompts) {label}"


def _user_prompts_flags(user_prompts: str) -> tuple[bool, bool]:
    text = (user_prompts or "").strip()
    pre = "Pre-Test" in text
    per = "Per-Capture" in text
    return pre, per


def build_startup_flow_text(
    *,
    user_prompts: str = "Per-Capture Only",
    capture_timeout_s: float = 10.0,
    dual_load_mode: str = "",
    discharge_pulses: int = 0,
) -> str:
    pre_test, per_capture = _user_prompts_flags(user_prompts)
    mode_note = dual_load_mode.strip() or "Dual Load Mode"
    lines = [
        "STARTUP WAVEFORM 2 PORT — SEQUENCE",
        f"Dual Load Mode: {mode_note}",
        f"User Prompts: {user_prompts.strip() or '(default)'}",
        f"Capture Timeout: {capture_timeout_s:g} s (gear → advanced)",
        "",
        "=== ONCE AT TEST START ===",
        _step(discharge_pulses > 0, f"[AUTO] Output discharge pulses (×{discharge_pulses})"),
        "  →",
        "[USER] OK — Discharge DUT outputs to input bulk cap",
        "  →",
        _step(pre_test, "[USER] OK — Oscilloscope setup reminder"),
        "  →",
        "[AUTO] Apply scope setup",
        "",
        "=== EACH Vin STEP (before load points) ===",
        "[AUTO] HMP aux DC OFF (bulk cap disconnected from DUT)",
        "  →",
        "[USER] Yes/No — Start charging bulk cap to this Vin?",
        "  → [AUTO] If Yes: HMP OFF + ramp / set input voltage",
        "  → [AUTO] If No: skip all load points at this Vin",
        "",
        "=== EACH LOAD POINT AT THIS Vin — REPEAT ===",
        "[AUTO] Set e-loads (Ch1 / Ch2)",
        "  →",
        "[AUTO] Scope RUN SINGLE",
        "  →",
        "[USER] Yes/No — Start startup waveform capture?",
        "  → [AUTO] If Yes: HMP aux DC ON",
        "  →",
        f"[AUTO] Wait minimum {capture_timeout_s:g} s, then scope STOP",
        "  →",
        _step(per_capture, "[USER] Review capture (Proceed / Recapture / Skip / Stop)"),
        "  →",
        "[AUTO] Screenshot + scope row + efficiency + Excel + HMP OFF",
        "",
        "=== RECAPTURE ===",
        "HMP OFF → RUN SINGLE → Yes/No capture → HMP ON → wait → STOP → review",
        "",
        "=== END OF TEST ===",
        _step(discharge_pulses > 0, "[AUTO] Final discharge pulses"),
        "  →",
        "[AUTO] Save workbook + SUW waveforms sheet",
        "",
        "Notes: Bulk-cap discharge (OK) runs once at start. Charge and capture use Yes/No.",
        "HMP requires Aux DC = HMP in Equipment Setup.",
    ]
    return "\n".join(lines)


def build_startup_ac_turnon_flow_text(
    *,
    user_prompts: str = "Per-Capture Only",
    dual_load_mode: str = "",
    discharge_pulses: int = 2,
    pre_ac_on_s: float = 1.0,
    post_ac_on_s: float = 3.0,
) -> str:
    pre_test, per_capture = _user_prompts_flags(user_prompts)
    mode_note = dual_load_mode.strip() or "Dual Load Mode"
    lines = [
        "STARTUP WAVEFORM AC TURN-ON (DER-1113) — SEQUENCE",
        f"Dual Load Mode: {mode_note}",
        f"User Prompts: {user_prompts.strip() or '(default)'}",
        f"Pre-Input Delay: {pre_ac_on_s:g} s | Post-Input Soak: {post_ac_on_s:g} s",
        "",
        "=== ONCE AT TEST START ===",
        _step(discharge_pulses > 0, f"[AUTO] Output discharge pulses (×{discharge_pulses})"),
        "  →",
        _step(pre_test, "[USER] OK — Oscilloscope setup reminder"),
        "  →",
        "[AUTO] Apply scope setup",
        "",
        "=== EACH LOAD POINT (Vin × Ch1/Ch2 load) — REPEAT ===",
        "[AUTO] Discharge output (input OFF)",
        "  →",
        "[AUTO] Set e-loads (Ch1 / Ch2)",
        "  →",
        "[AUTO] Scope RUN SINGLE",
        "  →",
        f"[AUTO] Wait {pre_ac_on_s:g} s",
        "  →",
        "[AUTO] Input supply ON at Vin (AC/DC per plan) — startup event",
        "  →",
        f"[AUTO] Wait {post_ac_on_s:g} s",
        "  →",
        "[AUTO] Discharge output again",
        "  →",
        "[USER] Yes/No — Review scope and save PNG?",
        "  →",
        "[AUTO] Scope STOP + screenshot (_SUAC.png)",
        "  →",
        _step(per_capture, "[USER] Review capture (Proceed / Recapture / Skip / Stop)"),
        "  →",
        "[AUTO] Efficiency + Excel row",
        "",
        "=== RECAPTURE ===",
        "Full DER sequence repeats from discharge (no HMP).",
        "",
        "=== END OF TEST ===",
        _step(discharge_pulses > 0, "[AUTO] Final discharge pulses"),
        "  →",
        "[AUTO] Save workbook + SUAC waveforms sheet",
        "",
        "Notes: Matches legacy DER-1113 Primary Vds/Ids startup (AC turn-on, not bulk-cap HMP connect).",
    ]
    return "\n".join(lines)


def build_steady_state_flow_text(
    *,
    user_prompts: str = "Pre-Test & Per-Capture",
    dual_load_mode: str = "",
) -> str:
    pre_test, per_capture = _user_prompts_flags(user_prompts)
    mode_note = dual_load_mode.strip() or "Dual Load Mode"
    lines = [
        "STEADY-STATE WAVEFORM 2 PORT — SEQUENCE",
        f"Dual Load Mode: {mode_note}",
        f"User Prompts: {user_prompts.strip() or '(default)'}",
        "",
        "=== ONCE AT TEST START ===",
        _step(pre_test, "[USER] OK — Oscilloscope setup reminder"),
        "  →",
        "[AUTO] Apply scope setup",
        "  →",
        "[AUTO] Discharge / confirm discharge resistor (as configured)",
        "",
        "=== EACH Vin STEP ===",
        "[AUTO] Set / ramp input Vin",
        "  →",
        "[AUTO] Initial or line soak",
        "  →",
        "=== EACH LOAD POINT AT THIS Vin ===",
        "[AUTO] Set loads",
        "  →",
        "[AUTO] Load soak",
        "  →",
        "[AUTO] Measure efficiency",
        "  →",
        "[AUTO] Scope RUN SINGLE + capture",
        "  →",
        _step(per_capture, "[USER] Optional per-capture review"),
        "  →",
        "[AUTO] Save Excel row + waveform PNG",
        "",
        "=== END OF TEST ===",
        "[AUTO] Discharge output",
        "  →",
        "[AUTO] Save workbook + SSW waveforms sheet",
    ]
    return "\n".join(lines)


def build_poll_flow_text(
    *,
    user_prompts: str = "Per-Capture Only",
    dual_load_mode: str = "",
    poll_interval_s: float = 1.0,
    poll_duration_s: float = 10.0,
    sample_count: int = 11,
) -> str:
    pre_test, per_capture = _user_prompts_flags(user_prompts)
    mode_note = dual_load_mode.strip() or "Dual Load Mode"
    lines = [
        "STEADY-STATE POLL WAVEFORM 2 PORT — SEQUENCE",
        f"Dual Load Mode: {mode_note}",
        f"User Prompts: {user_prompts.strip() or '(default)'}",
        f"Poll: every {poll_interval_s:g} s for {poll_duration_s:g} s "
        f"({sample_count} samples per load point, gear → advanced)",
        "",
        "=== ONCE AT TEST START ===",
        _step(pre_test, "[USER] OK — Oscilloscope setup reminder"),
        "  →",
        "[AUTO] Apply scope setup",
        "",
        "=== EACH Vin STEP ===",
        "[AUTO] Set / ramp input Vin",
        "  →",
        "[AUTO] Initial or line soak",
        "",
        "=== EACH LOAD POINT AT THIS Vin ===",
        "[AUTO] Set loads + load soak",
        "  →",
        "[AUTO] Sample 1: efficiency + scope RUN SINGLE + screenshot",
        "  →",
        _step(per_capture, "[USER] Optional per-capture review (sample 1 only)"),
        "  →",
        f"[AUTO] Further samples every {poll_interval_s:g} s until {poll_duration_s:g} s",
        "  →",
        "[AUTO] Each sample: power meters + scope measurements → Excel row",
        "",
        "=== END OF TEST ===",
        "[AUTO] Discharge output",
        "  →",
        "[AUTO] Save workbook + SS_POLL_2P waveforms sheet (one image per load point)",
    ]
    return "\n".join(lines)


def build_flow_text_for_title(
    title: str,
    *,
    user_prompts: str = "",
    capture_timeout_s: float = 10.0,
    dual_load_mode: str = "",
    discharge_pulses: int = 0,
    poll_interval_s: float = 1.0,
    poll_duration_s: float = 10.0,
    sample_count: int = 11,
) -> str | None:
    if title == STEADY_STATE_POLL_WAVEFORM_2PORT_TITLE:
        return build_poll_flow_text(
            user_prompts=user_prompts,
            dual_load_mode=dual_load_mode,
            poll_interval_s=poll_interval_s,
            poll_duration_s=poll_duration_s,
            sample_count=sample_count,
        )
    if title == STARTUP_WAVEFORM_2PORT_TITLE:
        return build_startup_flow_text(
            user_prompts=user_prompts,
            capture_timeout_s=capture_timeout_s,
            dual_load_mode=dual_load_mode,
            discharge_pulses=discharge_pulses,
        )
    if title == STARTUP_WAVEFORM_AC_TURNON_TITLE:
        return build_startup_ac_turnon_flow_text(
            user_prompts=user_prompts,
            dual_load_mode=dual_load_mode,
            discharge_pulses=discharge_pulses or 2,
        )
    if title in (STEADY_STATE_WAVEFORM_2PORT_TITLE, EFFICIENCY_2PORT_WAVEFORM_LEGACY_TITLE):
        return build_steady_state_flow_text(
            user_prompts=user_prompts,
            dual_load_mode=dual_load_mode,
        )
    return None
