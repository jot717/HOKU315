# PHASE2-A — Persistence Architecture Review v1

**Sprint type:** Review + hardening assessment only (no product behavior changes)  
**Date:** 2026-05-17  
**Scope:** Completed PHASE2-A local-first persistence foundation  
**Authority:** [`../../active/product/ROADMAP.md`](../../active/product/ROADMAP.md) · [`../../active/governance/SSOT_HIERARCHY.md`](../../active/governance/SSOT_HIERARCHY.md)

---

## Executive summary

| Item | Result |
|------|--------|
| **Final assessment** | **WARN** (approved to plan PHASE2-B with conditions) |
| **Architecture score** | **82 / 100** |
| **PHASE2-A boundaries respected** | Yes |
| **PHASE2-B blockers** | None critical; 4 hardening recommendations before cloud adapter |

PHASE2-A successfully centralizes product JSON persistence behind `PersistenceBackend` + `LocalJsonBackend`. Automated regression (5 tests) and UAT (12 tests) provide strong local stability signals. Gaps are schema normalization parity, non-atomic writes, and two ops-side shadow write paths—not fundamental design flaws.

---

## 1. Architecture strengths

1. **Single port pattern** — All five product entities route through `get_backend().read/write`; no store-level direct `Path.open` after refactor.
2. **Stable entity registry** — `entities.py` maps canonical keys → one file each; duplicate-path test passes in UAT.
3. **Fail-fast cloud guard** — `HOKU_PERSISTENCE_BACKEND` rejects non-`local` values at registry boundary.
4. **Test injection** — `use_backend()` fixes import-binding issue; UAT isolation prevents repo `runtime_state/` pollution.
5. **Public API preserved** — `load_profile`, `save_target_profile`, `append_history`, etc. unchanged for `fox_quiz` / engines.
6. **Documentation chain** — `RUNTIME_STATE_SCHEMA.md`, `ROADMAP` PHASE2-A slice, `ACTIVE_SURFACE_MAP` aligned.
7. **Separation from cloud vectors** — `db_service.upsert_user_vector` remains account/match path, not mixed into JSON port (intentional Phase 1 boundary).

---

## 2. Identified risks

| ID | Risk | Severity | Area |
|----|------|----------|------|
| R1 | `profile_store` does not normalize/validate on load (unlike `target_profile_store`) | Medium | Schema |
| R2 | No atomic write (crash mid-`json.dump` can corrupt file) | Medium | Durability |
| R3 | `runtime_sanity_check.py` writes `session_history` / `local_session` directly, bypassing port | Low | Shadow path |
| R4 | Global `_backend` singleton — concurrent requests share one backend instance | Low | Runtime |
| R5 | Legacy `.gitignore` entry `runtime_state/profile.json` (unused entity key) | Low | Drift |
| R6 | `SessionState` Supabase tokens in `rx.LocalStorage` parallel to JSON port | Medium (2-B) | Auth coupling |
| R7 | No schema `version` field in JSON blobs for forward migration | Medium | Migration |
| R8 | `load_profile` returns raw disk dict without coercion if file exists but invalid | Medium | Schema |

---

## 3. Schema durability analysis

| Entity | Owner module | Normalize on read | Default on missing | Timestamp fields |
|--------|--------------|-------------------|--------------------|------------------|
| `user_profile` | `profile_store` | **No** | Yes (writes default) | None |
| `target_profile` | `target_profile_store` | **Yes** (`normalize_target_profile`) | Yes | N/A |
| `fox_memory` | `fox_memory_store` | Partial merge with `DEFAULT_MEMORY` | Yes | `updated_at` (engine sets) |
| `session_history` | `session_history` | Row sanitize (strings only) | `[]` | None |
| `local_session` | `app_binding/persistence` | Dict check on load | `{}` | None |

**Field naming:** Consistent snake_case within each entity; cross-entity names differ by design (profile vs target).

**Nullable handling:** Target coerces lists/sliders; profile trusts file contents.

**Merge behavior:** Target partial save merges with `DEFAULT_TARGET`; profile overwrites full blob on save.

**Backward compatibility:** Old JSON without new target fields is healed by `normalize_target_profile`. Profile JSON with extra keys is preserved on round-trip (no strip).

**Serialization:** Deterministic `indent=2`, `ensure_ascii=False` in `LocalJsonBackend.write`.

---

## 4. Backend boundary analysis

```
fox_quiz / engines
    → store modules (profile, target, memory, session, app_binding)
        → registry.get_backend()
            → PersistenceBackend.read/write
                → LocalJsonBackend → runtime_state/*.json
```

| Boundary | Status |
|----------|--------|
| Stores → port | **Correct** |
| Port → disk | **Correct** (single implementation) |
| Ops sanity → disk | **Partial bypass** (R3) |
| UI Reflex state | In-memory; persisted via store APIs only |
| Auth tokens | **Outside port** (`SessionState` LocalStorage) — acceptable for 2-A, must stay separate in 2-B |

**Protocol adequacy for PHASE2-B:** `read(entity) / write(entity, data)` is sufficient for a `SupabaseBackend` adapter if entity keys remain stable. Recommend adding optional `exists()` / `delete()` in 2-B design doc only—not required for 2-A.

---

## 5. Migration readiness

| Criterion | Status | Notes |
|-----------|--------|-------|
| Stable entity keys | **Ready** | Five keys in `entities.py` |
| Adapter swap via registry | **Ready** | `use_backend` / env hook pattern |
| Schema versioning | **Not ready** | No `schema_version` in JSON |
| Atomic migration scripts | **Not ready** | No migration runner |
| Template samples | **Ready** | `runtime_state/templates/*.json` |
| Dual-write strategy | **Not defined** | Required for 2-B planning |

**Migration readiness status:** **YELLOW** — port is ready; data contract needs version stamps and profile normalization before cloud dual-write.

---

## 6. Cleanup guarantees

| Mechanism | Guarantee |
|-----------|-----------|
| UAT `conftest` autouse | Unlinks repo `runtime_state/*.json` after each UAT test |
| Regression `conftest` autouse | Same artifact cleanup in regression suite |
| H3 test `test_runtime_templates_only` | Repo must not retain live JSON (only templates) |
| `.gitignore` | Prevents committing machine-local JSON |

**Determinism:** **PASS** under pytest. Manual dev runs may leave JSON in `runtime_state/` (expected).

---

## 7. Persistence ownership map

| Entity key | Canonical owner (logic) | Disk file | Write path | Read path |
|------------|-------------------------|-----------|------------|-----------|
| `user_profile` | `profile_store` | `runtime_state/user_profile.json` | `save_profile` → backend.write | `load_profile` → backend.read |
| `target_profile` | `target_profile_store` | `runtime_state/target_profile.json` | `save_target_profile` (normalized) | `load_target_profile` (normalized) |
| `fox_memory` | `fox_memory_store` / `fox_memory_engine` | `runtime_state/fox_memory.json` | `save_fox_memory` | `load_fox_memory` |
| `session_history` | `session_history` | `runtime_state/session_history.json` | `append_history` | `load_history` |
| `local_session` | `app_binding/persistence` | `runtime_state/local_session.json` | `persist_session` | `load_session` |

**Runtime owners:** Reflex states (`ProfileState`, `TargetState`, `AppState`) call store APIs on events—not disk directly.

**Non-port persistence (documented exceptions):**

| Surface | Storage | Phase |
|---------|---------|-------|
| `SessionState.access_token` / `refresh_token` | Browser LocalStorage | 2-B auth utility |
| `db_service` vectors / RPC | Supabase | Phase 1 match (account path) |
| `runtime_sanity_check` emergency fix | Direct JSON for history/session only | Ops |

---

## 8. State lifecycle boundaries

```
[missing file] --load()--> default seed --save()--> disk JSON
[disk JSON] --load()--> domain store --mutate--> save() --> overwrite disk
[corrupt JSON] --sanity_check--> fix via store APIs OR direct ops write (history/session)
```

**Lifecycle rules:**

- First load creates file for profile/target/fox_memory via save-default pattern.
- Session history returns `[]` if missing (no auto-create until append).
- Local session returns `{}` if missing.
- No explicit delete/TTL API (history capped at 20 rows in logic only).

---

## 9. Anti-drift evaluation

| Check | Result |
|-------|--------|
| Parallel product persistence systems | **None found** in `product/` |
| Duplicate JSON per entity | **Prevented** (ENTITY_PATHS unique) |
| Hidden temp state files | **None** (no `.bak` writers) |
| PHASE3 SNS in persistence layer | **None** |
| Speculative architecture docs in active | **None added** |
| Onboarding flow drift | **None** (routes unchanged) |
| Archive used as law | **Not in code paths** |

**Governance validation:** PHASE2-A scope respected in code and active docs. No PHASE2-B implementation detected.

---

## 10. Duplicate system audit

| Path | Verdict |
|------|---------|
| `product/persistence/runtime/*` | **Canonical** |
| Store modules | **Canonical** (via port) |
| `ops/env/runtime_sanity_check.py` direct `json.dump` for history/session | **Shadow** (ops-only; R3) |
| `fox_quiz/session_state.py` LocalStorage | **Separate concern** (auth tokens) |
| `db_service.py` | **Separate concern** (remote DB) |
| `runtime_state/profile.json` | **Legacy gitignore only** — no code reference (R5) |

---

## 11. PHASE2-B risk analysis

| Contamination point | Risk | Mitigation for 2-B planning |
|--------------------|------|------------------------------|
| `get_backend()` env switch | Adapter replaces local; stores unchanged | Implement `SupabaseBackend` behind same protocol |
| `SessionState` tokens | Auth coupled to browser, not port | Keep tokens out of `PersistenceBackend`; optional `AuthSession` adapter |
| `db_service` vector writes | Dual truth (JSON profile vs Supabase vector) | Define **source of truth** per field in 2-B spec |
| Sync without versioning | Corruption on merge | Add `schema_version` + migration id |
| Cache in Reflex state | Stale UI after disk sync | Event-driven reload from stores post-sync |
| Sanity check bypass | Ops fixes diverge from app | Route fixes through `get_backend()` in 2-B hardening |
| Realtime subscriptions | Out of scope drift | Explicit non-goal in 2-B backlog |

**Sync corruption risk:** **Medium** until versioned merge rules exist.  
**Auth coupling risk:** **Medium** — tokens already isolated from JSON port (good).

---

## 12. Technical debt findings

1. Add `normalize_profile()` symmetric to target (or shared validator module).
2. Add atomic write helper (`write temp + replace`) in `LocalJsonBackend`.
3. Route `runtime_sanity_check` session/history fixes through store APIs.
4. Remove or document `runtime_state/profile.json` gitignore legacy.
5. Add optional `schema_version: 1` to each entity in 2-B prep (no migration yet).
6. Remove unused `import os` in `backend.py` (cosmetic).

---

## 13. Recommendations (cleanup / hardening)

**Before PHASE2-B implementation:**

1. **P0 (planning):** Write `BACKLOG_PHASE2B_CLOUD_PERSISTENCE_v1.md` with explicit non-goals (no realtime, no SNS).
2. **P1 (hardening):** Profile normalization parity + schema version field.
3. **P1 (hardening):** Atomic local writes.
4. **P2:** Unify sanity check with persistence port.
5. **P2:** Document dual-truth matrix: local JSON vs Supabase vector vs auth tokens.

**Do not start:** sync engine, Supabase adapter, or auth UX changes until P1 hardening accepted or waived in backlog.

---

## 14. Architecture scorecard

| Dimension | Score (0–10) | Weight | Weighted |
|-----------|--------------|--------|----------|
| Schema durability | 7 | 20% | 1.4 |
| Backend abstraction | 9 | 20% | 1.8 |
| Ownership clarity | 9 | 15% | 1.35 |
| Test coverage (reg+uat) | 9 | 15% | 1.35 |
| Migration readiness | 6 | 15% | 0.9 |
| Anti-drift / governance | 9 | 10% | 0.9 |
| PHASE2-B isolation | 8 | 5% | 0.4 |
| **Total** | | | **8.2 → 82%** |

---

## 15. PHASE2-B blockers

| Blocker | Critical? |
|---------|-----------|
| None — planning may proceed | No |

**Conditions (WARN):**

- Acknowledge R1/R2/R6/R7 in PHASE2-B backlog non-goals and acceptance criteria.
- Do not implement cloud adapter until product owner accepts migration/version plan.

---

## 16. Approved boundaries for next phase (PHASE2-B)

**Allowed:**

- New `PersistenceBackend` implementation (e.g. Supabase) selected by env
- Dual-write / read-through design **documented** before code
- Auth utility wiring **without** changing Phase 1 face copy
- Store APIs unchanged

**Forbidden:**

- SNS / graph / vector expansion beyond existing match RPC
- Realtime sync / websocket state
- New onboarding routes
- Second JSON root or parallel `profile.json`
- Archive-driven schema inference

---

## 17. Validation results (review sprint)

| Gate | Result |
|------|--------|
| `python ops/flow/check_all_flows.py` | PASSED |
| `python ops/env/reflex_compile_gate.py` | OK |
| `pytest tests/regression/ -v --tb=short` | 151 passed, 3 skipped |
| `pytest tests/uat/ -v --tb=short` | 12 passed |

---

## 18. Final assessment

**PASS / WARN / FAIL:** **WARN**

- **PASS** for PHASE2-A completion and local-first stability.
- **WARN** for migration/versioning and profile normalization before cloud work.
- **Not FAIL** — no architectural reversal required.

---

## References reviewed

- `product/persistence/runtime/` (entities, backend, registry)
- `product/profile/runtime/profile_store.py`
- `product/target/runtime/target_profile_store.py`
- `product/memory/runtime/fox_memory_store.py`
- `product/session/runtime/session_history.py`
- `product/app_binding/runtime/persistence.py`
- `ops/env/runtime_sanity_check.py`
- `tests/regression/test_phase2a_persistence_foundation_v1.py`
- `tests/uat/test_phase2a_persistence_uat.py`
- `docs/active/env/RUNTIME_STATE_SCHEMA.md`
