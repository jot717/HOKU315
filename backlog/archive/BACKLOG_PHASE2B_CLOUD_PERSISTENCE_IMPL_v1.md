# BACKLOG — PHASE2-B Cloud Persistence Implementation v1

**Type:** Implementation — cloud mirror behind persistence port.

**Authority:** [`docs/active/governance/PHASE2B_CLOUD_PERSISTENCE_PLAN.md`](../../docs/active/governance/PHASE2B_CLOUD_PERSISTENCE_PLAN.md)

**Report:** [`docs/archive/reviews/PHASE2B_CLOUD_PERSISTENCE_IMPL_REPORT_v1.md`](../../docs/archive/reviews/PHASE2B_CLOUD_PERSISTENCE_IMPL_REPORT_v1.md)

## Objective

Implement `CloudPersistenceBackend`, `DualWriteBackend`, feature-flagged sync, sync status, and LWW conflict handling without Phase 1 UX drift.

## Done when

- [x] `CloudPersistenceBackend` + `DualWriteBackend`
- [x] `HOKU_CLOUD_SYNC_ENABLED` gating
- [x] `db_service` persistence fetch/upsert + mock mode
- [x] `sync_status.json` tracking
- [x] Regression + UAT coverage
- [x] Implementation report archived

## Out of scope

Realtime sync, SNS, graph/vector, embeddings, new routes, onboarding changes, background workers.

## Sprint

[`SPRINT_PHASE2B_CLOUD_PERSISTENCE_IMPL_v1.md`](SPRINT_PHASE2B_CLOUD_PERSISTENCE_IMPL_v1.md)
