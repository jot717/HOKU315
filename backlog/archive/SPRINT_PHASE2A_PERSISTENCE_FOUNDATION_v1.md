# SPRINT — PHASE2-A Persistence Foundation v1

## GOAL

Persistence port + local JSON backend; refactor stores; no Phase 1 UX drift.

## NON-GOALS

Cloud adapter, login changes, SNS, new routes.

## FILES

| Area | Path |
|------|------|
| Port | `product/persistence/runtime/` |
| Stores | `profile_store`, `target_profile_store`, `fox_memory_store`, `session_history`, `app_binding/persistence` |
| Law | `docs/active/product/ROADMAP.md` (PHASE2-A) |
| Schema | `docs/active/env/RUNTIME_STATE_SCHEMA.md` |
| Test | `tests/regression/test_phase2a_persistence_foundation_v1.py` |

## REGRESSION

```bash
python ops/flow/check_all_flows.py
python ops/env/reflex_compile_gate.py
pytest tests/regression/test_phase2a_persistence_foundation_v1.py -v --tb=short
```

## COMMIT

`feat(persistence): PHASE2A persistence foundation v1`
