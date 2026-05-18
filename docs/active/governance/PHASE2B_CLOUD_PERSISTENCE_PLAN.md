# PHASE2-B — Cloud Persistence Plan v1

**Status:** PLANNING COMPLETE — **no implementation in this slice**  
**Authority:** [`../product/ROADMAP.md`](../product/ROADMAP.md) · Prior work: [`../../archive/reviews/PHASE2AH_PERSISTENCE_HARDENING_REPORT_v1.md`](../../archive/reviews/PHASE2AH_PERSISTENCE_HARDENING_REPORT_v1.md)  
**Implementation gate:** Separate sprint `PHASE2-B-IMPL` — not started until this plan is accepted.

---

## 1. Mission (planning only)

Define cloud persistence **boundaries** before any Supabase adapter code:

- Local vs cloud ownership
- Sync rules
- Conflict rules
- Auth boundaries
- Dual-write behavior
- Failure handling
- Anti-desync rules

**Explicit non-goals (this phase):**

- Supabase adapter implementation
- Realtime subscriptions / websockets
- SNS import (PHASE3)
- Graph / vector expansion beyond existing match RPC
- New onboarding routes or Phase 1 face copy changes
- Migration engine execution

---

## 2. Architecture context (completed foundation)

| Layer | Current state |
|-------|----------------|
| Port | `PersistenceBackend` + `LocalJsonBackend` |
| Entities | `user_profile`, `target_profile`, `fox_memory`, `session_history`, `local_session` |
| Schema | `schema_version: 1` on dict entities; session envelope `{schema_version, items}` |
| Writes | Atomic temp + replace (local) |
| Auth tokens | `SessionState` → browser LocalStorage (outside port) |
| Match vectors | `db_service.py` → Supabase RPC (existing; **not** JSON port) |

---

## 3. Local vs cloud ownership map

### 3.1 Source of truth by mode

| Mode | Profile / target / fox_memory / session / flow | Match vectors |
|------|-----------------------------------------------|---------------|
| **Guest (no account)** | **Local only** (`runtime_state/`) | Not available (match wall requires login) |
| **Account (logged in)** | **Cloud authoritative** after first successful sync | **Cloud authoritative** (existing `db_service`) |
| **Offline / cloud down** | **Local read-only cache**; writes queue or fail per policy below | Use last known RPC result; no silent write |

### 3.2 Field ownership (account mode)

| Data | Local JSON port | Cloud (Supabase tables) | Notes |
|------|-----------------|-------------------------|-------|
| Signal profile fields | Cache + offline queue | **Authoritative** when synced | Same shape as `normalize_profile()` |
| Target profile | Cache + offline queue | **Authoritative** when synced | Same shape as `normalize_target_profile()` |
| Fox memory | Cache + offline queue | **Authoritative** when synced | Rule tags only; no LLM blobs |
| Session history | Cache + offline queue | **Authoritative** when synced | Envelope `schema_version` + `items` |
| Flow binding (`local_session`) | **Local only** | Not mirrored | Device/session UX state |
| Auth tokens | **Never in JSON port** | Supabase Auth session | `SessionState` LocalStorage only |
| User vector / match RPC | **Never in JSON port** | **Authoritative** | Stays in `db_service.py` |

### 3.3 Anti-duplication rule

**One canonical owner per field.** Cloud tables must not introduce parallel keys for data already in JSON entities without a migration plan. Vectors remain in `profiles.vector` (or agreed table) — not duplicated inside profile JSON on cloud.

---

## 4. Auth boundaries

| Concern | Owner | Rule |
|---------|-------|------|
| Login / logout UX | `fox_quiz` + `SessionState` | Utility only; no product rebrand |
| Access / refresh tokens | Browser LocalStorage | **Never** written by `PersistenceBackend` |
| Supabase client | `db_service.py` only | No second client in stores or UI |
| Persistence port | Account-gated cloud adapter | Adapter receives **user id** from session layer; does not store tokens |
| Guest | No cloud adapter calls | `HOKU_PERSISTENCE_BACKEND=local` only |

**Gate:** Cloud backend activates only when `SessionState` has valid session **and** user opts in to sync (default on for account users after login — configurable flag in implementation sprint, not in Phase 1 face copy).

---

## 5. Dual-write behavior (implementation spec)

### 5.1 Phased rollout (recommended)

| Stage | Behavior |
|-------|----------|
| **B0 (planning)** | Local only — current production |
| **B1** | `dual_write_local_first` — write local atomically, then async cloud upsert |
| **B2** | `cloud_read_through` — on login, pull cloud → normalize → merge into local cache |
| **B3** | `cloud_authoritative` — reads prefer cloud when online; local is cache |

**Default for first implementation:** **B1 + B2** (no B3 until UAT passes).

### 5.2 Write sequence (account + online)

```
1. normalize_* (store layer — unchanged public API)
2. LocalJsonBackend.write (always — cache)
3. If account + online: CloudBackend.upsert(entity, payload)
4. On cloud failure: mark entity sync_state=pending; do not roll back local
```

**Rationale:** Local-first preserves Phase 1 guest behavior and offline resilience; cloud is backup/sync layer for accounts.

### 5.3 Read sequence (account + online)

```
1. If guest or backend=local: load from local only
2. If account + online: fetch cloud → normalize → compare schema_version
3. If cloud newer: write through to local cache (atomic)
4. If cloud missing: push local snapshot to cloud (first sync)
5. Return normalized dict to callers (same API)
```

---

## 6. Sync rules

| Rule ID | Rule |
|---------|------|
| S1 | Sync unit = one **entity key** (`user_profile`, etc.), not partial fields |
| S2 | Every cloud row includes `schema_version`, `user_id`, `updated_at` (ISO UTC) |
| S3 | Local file `updated_at` optional in 2-B impl; if absent, use file mtime for conflict |
| S4 | Sync runs on: login, explicit save events, app background interval (≥ 60s, implementation detail) |
| S5 | No sync for `local_session` |
| S6 | `flow_binding` never blocks signal profile save |
| S7 | First login migration: local snapshot uploaded once if cloud empty |
| S8 | Logout clears tokens only — **does not** delete local cache (guest can continue) |

---

## 7. Conflict rules

| Scenario | Resolution |
|----------|------------|
| Same `schema_version`, cloud `updated_at` > local | **Cloud wins** → overwrite local cache |
| Same version, local newer | **Push local → cloud** |
| `schema_version` cloud > local | **Cloud wins** after migration transform (future) |
| `schema_version` local > cloud | **Reject cloud**; push local (dev-only flag for emergency) |
| Divergent edits both newer (clock skew) | **Cloud wins** if account mode; log conflict metric |
| Guest | **Local only** — no conflict possible |
| Corrupt local JSON | Local heal (2-AH) then push clean snapshot |

**No automatic merge of list fields** (e.g. `interests`, `recent_patterns`) in v1 — entity-level last-write-wins.

---

## 8. Failure handling

| Failure | Behavior |
|---------|----------|
| Cloud unreachable on read | Serve local cache; surface optional subtle status (not Phase 1 banner) |
| Cloud unreachable on write | Local write succeeds; queue `sync_pending` in local metadata file or entity wrapper |
| Auth expired | Stop cloud calls; local cache remains; redirect to login on protected routes only |
| Schema validation fail | Do not upload; run normalize locally; ops/sanity pattern |
| Partial cloud write | Retry with backoff (3x); then mark pending |
| RPC/vector fail | Existing `db_service` behavior — independent of JSON port |

**Fail-closed:** Invalid cloud payload never overwrites good local cache without validation.

---

## 9. Anti-desync rules

| ID | Rule |
|----|------|
| A1 | UI Reflex state must **reload from stores** after sync, not hold shadow copies |
| A2 | No direct `runtime_state/` access outside `PersistenceBackend` |
| A3 | No Supabase calls inside store modules |
| A4 | `db_service` must not read/write JSON entity files |
| A5 | Single `get_backend()` — cloud adapter composed inside registry, not parallel singleton |
| A6 | Environment: `HOKU_PERSISTENCE_BACKEND=local|cloud|dual` (plan only; impl validates) |
| A7 | Regression + UAT must cover dual-write and offline paths before B3 |
| A8 | Feature flag `HOKU_CLOUD_SYNC_ENABLED` default off until impl sprint UAT passes |

---

## 10. Proposed cloud adapter interface (spec only)

```python
class CloudPersistenceBackend:
    """Implements PersistenceBackend for Supabase tables — NOT IMPLEMENTED."""

    def read(self, entity: str) -> Any | None: ...
    def write(self, entity: str, data: Any) -> None: ...

class DualWriteBackend:
    """Composes LocalJsonBackend + CloudPersistenceBackend per rules §5–7."""

    def read(self, entity: str) -> Any | None: ...
    def write(self, entity: str, data: Any) -> None: ...
```

**Table naming (proposal):** `user_profiles`, `target_profiles`, `fox_memories`, `session_histories` — keyed by `user_id`. Exact DDL in implementation sprint.

---

## 11. PHASE3+ contamination guard

| System | PHASE2-B may touch | Forbidden |
|--------|-------------------|-----------|
| SNS OAuth | No | PHASE3 |
| Graph ingestion | No | PHASE3–4 |
| Embeddings pipeline | No new | Existing match RPC only |
| Realtime channels | No | PHASE2-B |
| New routes | No | PHASE1 face |

---

## 12. Implementation acceptance criteria (future sprint)

Before marking PHASE2-B impl COMPLETED:

- [ ] `DualWriteBackend` behind `get_backend()` when `dual` mode
- [ ] All five entities sync per §3–7
- [ ] Auth tokens remain outside port
- [ ] Regression + UAT for offline, conflict, corrupt JSON, pending queue
- [ ] No Phase 1 copy advertising cloud/SNS
- [ ] `MASTER_BACKLOG` updated; plan archived if superseded

---

## 13. Planning verdict

| Item | Status |
|------|--------|
| Boundaries defined | **Yes** |
| Ready for implementation sprint | **Yes** |
| Blockers | **None** |
| Recommendation | **Proceed to PHASE2-B-IMPL** when prioritized in MASTER_BACKLOG |

---

## References

- `product/persistence/runtime/`
- `docs/active/env/RUNTIME_STATE_SCHEMA.md`
- `fox_quiz/session_state.py`
- `db_service.py` (vectors/RPC — separate concern)
