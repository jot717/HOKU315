# REPO GOVERNANCE RULES

**Authority chain:** `DEVELOPMENT_CONSTITUTION.md` → [`PRODUCT_MASTER.md`](PRODUCT_MASTER.md) → domain constitutions → sprint archives.

---

## Where docs live

| Type | Location | Index |
|------|----------|--------|
| Product truth | `ops/product/` | [`PRODUCT_MASTER.md`](PRODUCT_MASTER.md), [`README.md`](README.md) |
| UAT | `ops/uat/` | [`UAT_MASTER_GUIDE.md`](../uat/UAT_MASTER_GUIDE.md) |
| Backlog | `backlog/` | [`MASTER_BACKLOG.md`](../../backlog/MASTER_BACKLOG.md) |
| Deprecated / history | `docs/deprecated/` | [`docs/deprecated/README.md`](../../docs/deprecated/README.md) |
| Drift / audit archive | `docs/deprecated/archive/` | [`archive/README.md`](../../docs/deprecated/archive/README.md) |
| Sprint slices (historical) | `backlog/archive/` | linked from `MASTER_BACKLOG.md` |
| Env / runtime | `ops/env/` | `STARTUP_GUIDE.md` |

---

## Active vs archive vs deprecated

- **Active** — Current phase law; linked from `PRODUCT_MASTER.md`.
- **Archive** — Completed sprint backlog/UAT/drift reports; **read-only** history.
- **Deprecated** — Superseded product language or UX specs; do not implement from these without explicit revival.

**When to archive:** Sprint marked COMPLETED in `MASTER_BACKLOG.md`; or doc superseded by `PRODUCT_MASTER` / a newer constitution.

**Do not delete** archived history; move and link.

---

## Sprint naming

- Backlog: `BACKLOG_<SLUG>_v1.md`
- Sprint: `SPRINT_<SLUG>_v1.md`
- Commit: `feat|fix|chore(scope): HUMAN TITLE v1` aligned with sprint slug

After completion → move slice files to `backlog/archive/`; keep **one** canonical row in `MASTER_BACKLOG.md`.

---

## Forbidden governance anti-patterns

- Duplicate “constitutions” that contradict `PRODUCT_MASTER.md`
- Orphan docs (no link from `PRODUCT_MASTER`, README, or `MASTER_BACKLOG`)
- Shadow backlog systems (only `MASTER_BACKLOG.md` + root `BACKLOG.md` P0/P1 index)
- New intelligence features smuggled into governance-only sprints

---

## Code ↔ doc coupling

- New product routes → update `PAGE_PURPOSE_SYSTEM.md` + `PRODUCT_MASTER` loop table
- New rule engines → ontology/constitution + regression test under `tests/regression/`
- UI copy → Phase 1 safe (no SNS/token therapy); see `PHASE_BOUNDARY_SYSTEM.md`
