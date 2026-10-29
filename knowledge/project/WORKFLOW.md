# Project knowledge workflow (PI ATE)

**Goal:** A new session understands **90%+** of the project from these markdown files and opens **only source files for the current task**.

Knowledge under `knowledge/project/` is the **primary source of context**. Root `README.md` is product overview. Long-form references: `architecture.md`, `threading_architecture.md`.

---

## New session

1. Read `knowledge/project/SUMMARY.md` and `KEY_FILES.md`.
2. Read other knowledge files **only as needed** (see table in `README.md`).
3. **Do not** scan, grep, or explore the entire repository unless the user explicitly asks.
4. If docs and code might disagree, read **only** the files listed in KEY_FILES for that area, then **update knowledge** if code wins.

---

## New feature

1. Read `FEATURES.md`, `PATTERNS.md`, `ARCHITECTURE.md` (and `DESIGN.md` if touching deep behavior).
2. From KEY_FILES + ARCHITECTURE, **list affected modules** — still no whole-repo search.
3. Read **only** those source files (and direct imports if blocked).
4. Implement using existing patterns (`TestTypes`, `PowerMeter` facade, page_controls).
5. **Update knowledge before finishing:**
   - `FEATURES.md` — user-visible / test-type behavior
   - `DESIGN.md` — mechanics, params, constants
   - `DECISIONS.md` — dated decision + rationale
   - `KEY_FILES.md` — new important paths
   - `ARCHITECTURE.md` — only if layers or data flow changed
   - `TESTING.md` — new/changed verify scripts
   - `COMMON_TASKS.md` — new operator or dev steps

6. Optional: agent store `/cursor/stores/self/pi-ate-<topic>.md` for session handoff (`always-session-memory`).

---

## Bug fix

1. Use `KEY_FILES.md` + `FEATURES.md` to locate subsystem.
2. Read **only** files on the failure path.
3. Update knowledge **only** if behavior, architecture, or key paths changed.

---

## Refactoring

1. Scope to impacted modules from ARCHITECTURE + KEY_FILES.
2. Preserve PATTERNS; no drive-by changes.
3. Update `ARCHITECTURE.md`, `KEY_FILES.md`, `PATTERNS.md` if structure or conventions shift.

---

## Context priority

| Priority | Source |
|----------|--------|
| 1 | `knowledge/project/*.md`, root `README.md` |
| 2 | Source files **named in KEY_FILES** for this task |
| 3 | Direct dependencies of those files (single hop) |

**Avoid reading unless task requires it:**

- Whole-repo grep / explore agent on `**/*`
- `ui/ui_main.py` in full, generated UI, `files_rc`, build outputs
- Unrelated `psu_tests/test_*.py`, unrelated equipment drivers
- Vendor / conda env trees

Use **targeted** grep with path + pattern (e.g. `psu_tests/test_steady_state_poll_2port_waveform.py`).

---

## Continuous memory

After substantive work:

- Keep knowledge **concise** (bullets, tables, paths — not pasted code).
- Prefer updating existing sections over new duplicate docs.
- Future sessions should **not** need to re-read the codebase to understand what changed.

---

## Drift policy

If implementation diverges from knowledge: **update knowledge in the same PR/commit** as the code, or note `TODO(doc):` in DECISIONS with file to fix.
