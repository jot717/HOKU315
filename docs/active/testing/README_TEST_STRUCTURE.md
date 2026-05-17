# Test structure — migration plan

**Phase 1-H3:** No regression files deleted. This document defines future layout and anti-entropy rules.

---

## Target layout

```
tests/
  governance/     # SSOT, active surface, doc limits
  flow/           # Route registration, journey order
  runtime/        # Engines (signal, match, guard, memory)
  compile/        # Reflex page build / foreach safety
  signal/         # Profile, target, inference
  match/          # Match wall, rhythm engine
  insight/        # UX intelligence, insight panel
```

**Today:** Most tests live in `tests/regression/` with category prefixes in filenames.

---

## Deprecated phase-slice tests (keep until migrated)

| Pattern | Status |
|---------|--------|
| `test_phase1d_*` | Keep — encodes UX intelligence contract |
| `test_phase1f_*` | Keep — match credibility |
| `test_phase1g_*`, `test_phase1h2_*` | Governance |
| `test_fox_immersion_*` | Partially obsolete UI; archive components removed |
| `test_fox_signal_guard_*` | Engine + archived card reference |

**WIP tests quarantined:** `wip/prototypes/test_app_shell_replacement.py`, `test_match_flow.py`

---

## Migration plan

1. **H3** — Document structure (this file); quarantine WIP tests  
2. **H4** — Copy (not move) governance tests → `tests/governance/`  
3. **H5** — Split `tests/regression/` by category; keep shim imports one release  
4. **H6** — Delete empty `tests/regression/` after CI updated  

---

## Anti-entropy rules

- New tests must map to an **active category** in [`ACTIVE_SURFACE_MAP.md`](../docs/active/product/ACTIVE_SURFACE_MAP.md)
- Do not add tests that require dead routes (`/story`, `/chat`, `/unlocks`) without archived reference imports
- Governance tests run on every doc-only sprint
- Compile tests require project `.venv` (`reflex-components-radix`)

---

## Commands

```bash
python ops/flow/check_all_flows.py
python -m pytest tests/regression/ -v --tb=short
python ops/env/reflex_compile_gate.py
```
