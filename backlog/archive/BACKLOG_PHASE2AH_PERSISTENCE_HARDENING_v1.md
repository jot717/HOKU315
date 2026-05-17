# BACKLOG — PHASE2-AH Persistence Hardening v1

**Authority:** [`docs/archive/reviews/PHASE2A_PERSISTENCE_ARCHITECTURE_REVIEW_v1.md`](../../docs/archive/reviews/PHASE2A_PERSISTENCE_ARCHITECTURE_REVIEW_v1.md)

## Objective

Resolve review risks R1, R2, R3, R7 before PHASE2-B.

## Done when

- [x] Profile normalization parity (`normalize_profile`)
- [x] Atomic JSON writes in `LocalJsonBackend`
- [x] `runtime_sanity_check` routes fixes through stores
- [x] `schema_version` on all entities + session envelope
- [x] Regression `test_phase2ah_persistence_hardening_v1.py`
- [x] UAT hardening cases added

## Out of scope

Supabase, sync, realtime, SNS, migration engine.

## Sprint

[`SPRINT_PHASE2AH_PERSISTENCE_HARDENING_v1.md`](SPRINT_PHASE2AH_PERSISTENCE_HARDENING_v1.md)
