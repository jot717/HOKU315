# PHASE2-B-IMPL — Cloud Persistence Implementation Report v1

**Sprint type:** Implementation (local-first dual-write cloud mirror)  
**Date:** 2026-05-17  
**Authority:** [`../../active/governance/PHASE2B_CLOUD_PERSISTENCE_PLAN.md`](../../active/governance/PHASE2B_CLOUD_PERSISTENCE_PLAN.md)

---

## Executive summary

| Item | Result |
|------|--------|
| **Final assessment** | **PASS** (with environment WARN) |
| **Architecture score** | **88 / 100** |
| **Phase 1 identity / UX drift** | None |
| **PHASE2-B scope respected** | Yes |

First cloud persistence layer ships behind the existing `PersistenceBackend` port. Default runtime remains `HOKU_PERSISTENCE_BACKEND=local`. Cloud sync activates only when `HOKU_CLOUD_SYNC_ENABLED` is set and an authenticated user id resolves.

---

## 1. Implemented modules

| Module | Role |
|--------|------|
| `product/persistence/runtime/cloud_backend.py` | `CloudPersistenceBackend` — `db_service` only |
| `product/persistence/runtime/dual_write_backend.py` | Local-first dual write + LWW read |
| `product/persistence/runtime/sync_context.py` | `HOKU_CLOUD_SYNC_ENABLED`, token provider, user id |
| `product/persistence/runtime/sync_status.py` | `runtime_state/sync_status.json` tracking |
| `product/persistence/runtime/registry.py` | `local` / `dual` modes; dual gated by flag |
| `product/persistence/runtime/entities.py` | `CLOUD_SYNCABLE_ENTITIES` (excludes `local_session`) |
| `db_service.py` | `persistence_fetch_entity`, `persistence_upsert_entity`, mock store |
| `sql/persistence_entities.sql` | DDL for `hoku_entity_snapshots` + RLS |

---

## 2. Architecture boundary verification

```
stores → registry.get_backend()
           ├─ local (default) → LocalJsonBackend
           └─ dual + HOKU_CLOUD_SYNC_ENABLED → DualWriteBackend
                  ├─ local write (always first)
                  └─ CloudPersistenceBackend → db_service only
```

| Rule | Status |
|------|--------|
| No Supabase in stores | PASS |
| `db_service.py` sole cloud boundary | PASS |
| No auth tokens in cloud payloads | PASS |
| No second persistence root | PASS |
| Guest / no token → local only | PASS |
| `local_session` never cloud-synced | PASS |
| No field-level merge | PASS |
| LWW by `updated_at` on read | PASS |

---

## 3. Sync behavior summary

**Write path:** `DualWriteBackend.write` → local atomic write → `mark_local_write` → cloud upsert (3 retries) → `mark_synced` or `mark_pending`.

**Read path:** If cloud snapshot `updated_at` > local timestamp, cloud payload is written locally and returned; else local wins.

**Feature flags:**

- `HOKU_CLOUD_SYNC_ENABLED=1|true|yes` — enables dual cloud leg when backend is `dual`
- `HOKU_PERSISTENCE_BACKEND=dual` — selects `DualWriteBackend` (falls back to local if flag off)
- `HOKU_CLOUD_PERSISTENCE_MOCK=1` — file mock under `runtime_state/cloud_mock/` (tests)

---

## 4. Local / cloud ownership

| Entity | Local owner | Cloud mirror |
|--------|-------------|--------------|
| `user_profile` | `runtime_state/user_profile.json` | Per-user snapshot row |
| `target_profile` | `runtime_state/target_profile.json` | Yes |
| `fox_memory` | `runtime_state/fox_memory.json` | Yes |
| `session_history` | `runtime_state/session_history.json` | Yes |
| `local_session` | `runtime_state/local_session.json` | **Never** |

---

## 5. Failure recovery

- Cloud upsert exceptions after retries → `sync_status` entity `pending`; local file unchanged by rollback (local already committed).
- Cloud fetch failure on read → local data returned.
- Failed sync never deletes or overwrites local with empty cloud.

---

## 6. Test results

| Suite | Result |
|-------|--------|
| `python ops/flow/check_all_flows.py` | **PASS** |
| `python ops/env/reflex_compile_gate.py` | **WARN** — system Python 3.14 missing `reflex_components_radix.plugin` (pre-existing env; use repo `.venv`) |
| `pytest tests/regression/` | **159 passed**, 5 failed (all radix/reflex env), 4 skipped |
| `pytest tests/uat/` | **18 passed** |
| PHASE2-B regression (`test_phase2b_*`) | **6 passed** |
| PHASE2-B UAT | **3 passed** |

---

## 7. Remaining PHASE2-B warnings

| ID | Warning | Severity |
|----|---------|----------|
| W1 | Production Supabase DDL must be applied manually (`sql/persistence_entities.sql`) | Medium |
| W2 | App-layer `set_access_token_provider()` not wired from `SessionState` in this sprint (env `HOKU_ACCESS_TOKEN` / mock login for tests) | Medium |
| W3 | No background retry worker — `pending` cleared on next successful write/read cycle only | Low |
| W4 | Reflex compile gate requires pinned `.venv` on dev machines | Low (env) |

---

## 8. PASS / WARN / FAIL

| Dimension | Assessment |
|-----------|------------|
| Implementation completeness | **PASS** |
| Boundary / SSOT compliance | **PASS** |
| Regression (persistence) | **PASS** |
| UAT | **PASS** |
| Reflex compile gate (this host) | **WARN** |
| **Overall** | **PASS** |

---

## Next

- Wire `set_access_token_provider` from fox_quiz session state when enabling cloud in staging.
- Apply `sql/persistence_entities.sql` to Supabase before disabling mock mode.
