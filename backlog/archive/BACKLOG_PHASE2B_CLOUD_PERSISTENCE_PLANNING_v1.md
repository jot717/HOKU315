# BACKLOG — PHASE2-B Cloud Persistence Planning v1

**Type:** Planning only — no Supabase implementation.

**Canonical plan:** [`docs/active/governance/PHASE2B_CLOUD_PERSISTENCE_PLAN.md`](../../docs/active/governance/PHASE2B_CLOUD_PERSISTENCE_PLAN.md)

## Objective

Define local/cloud ownership, sync, conflict, auth, dual-write, failure, and anti-desync rules before adapter code.

## Done when

- [x] `PHASE2B_CLOUD_PERSISTENCE_PLAN.md` published
- [x] ROADMAP PHASE2-B planning slice updated
- [x] Regression guard for plan sections
- [x] MASTER_BACKLOG reflects planning COMPLETE; impl FUTURE

## Out of scope

Supabase adapter, DDL, realtime, SNS, new routes, migration runner execution.

## Next sprint

`PHASE2-B-IMPL` — implement `CloudPersistenceBackend` + `DualWriteBackend` per plan §10–12.

## Sprint

[`SPRINT_PHASE2B_CLOUD_PERSISTENCE_PLANNING_v1.md`](SPRINT_PHASE2B_CLOUD_PERSISTENCE_PLANNING_v1.md)
