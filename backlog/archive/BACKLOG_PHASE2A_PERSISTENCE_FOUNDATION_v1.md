# BACKLOG — PHASE2-A Persistence Foundation v1

**Product phase:** PHASE2 ([`ROADMAP.md`](../../docs/active/product/ROADMAP.md))  
**Authority:** [`PRODUCT_MASTER.md`](../../docs/active/product/PRODUCT_MASTER.md)

## Objective

Introduce a single persistence port (`PersistenceBackend`) over existing `runtime_state/` JSON files so later cloud adapters (2-B+) plug in without rewriting product stores.

## Done when

- [x] `product/persistence/runtime/` with entities, `LocalJsonBackend`, `get_backend()`
- [x] Profile, target, fox memory, session history, local session use backend
- [x] `HOKU_PERSISTENCE_BACKEND=local` only (unsupported modes fail fast)
- [x] Regression `test_phase2a_persistence_foundation_v1.py`
- [x] ROADMAP PHASE2-A slice + MASTER_BACKLOG ACTIVE row
- [ ] PHASE2-B cloud adapter (separate backlog)

## Out of scope

Supabase wiring, auth UX, cross-device sync UI, SNS, new routes, Phase 1 marketing copy changes.

## Sprint

[`SPRINT_PHASE2A_PERSISTENCE_FOUNDATION_v1.md`](SPRINT_PHASE2A_PERSISTENCE_FOUNDATION_v1.md)
