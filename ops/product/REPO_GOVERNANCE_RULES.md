# REPO GOVERNANCE RULES

**Authority chain:** [`AI_DEVELOPMENT_CONSTITUTION.md`](AI_DEVELOPMENT_CONSTITUTION.md) → [`PRODUCT_MASTER.md`](PRODUCT_MASTER.md) → `SIGNAL_SYSTEM.md` / `MATCH_SYSTEM.md` → sprint archives.

---

## Where docs live

| Type | Location | Index |
|------|----------|--------|
| Product SSOT | `ops/product/` (max 9 active `.md` + README) | [`PRODUCT_MASTER.md`](PRODUCT_MASTER.md) |
| UAT | `ops/uat/` (max 2 active `.md` + README) | [`UAT_MASTER_GUIDE.md`](../uat/UAT_MASTER_GUIDE.md) |
| Backlog | `backlog/` | [`MASTER_BACKLOG.md`](../../backlog/MASTER_BACKLOG.md), root `SPRINT_LOG.md` |
| Historical | `docs/archive/` | see `docs/archive/README.md` |
| Deprecated UX | `docs/deprecated/` | read-only |
| Sprint slices (historical) | `backlog/archive/` | linked from `MASTER_BACKLOG.md` |

---

## Active vs archive

- **Active** — Files listed in [`AI_DEVELOPMENT_CONSTITUTION.md`](AI_DEVELOPMENT_CONSTITUTION.md) § A and [`README.md`](README.md).
- **Archive** — `docs/archive/**`, `backlog/archive/**` — **never** define future logic; no links from active docs except “annex” pointer.
- **Deprecated** — Superseded UX specs; do not implement without SSOT update.

**When to archive:** Sprint COMPLETED; doc superseded by SSOT; active count would exceed limits.

---

## Sprint naming

- Backlog: `BACKLOG_<SLUG>_v1.md` → `backlog/archive/` when done
- Sprint: `SPRINT_<SLUG>_v1.md`
- Commit: `feat|fix|chore(scope): HUMAN TITLE v1`

---

## Forbidden anti-patterns

- Duplicate constitutions contradicting `PRODUCT_MASTER.md`
- Second signal/match/onboarding/memory/UX narrative systems
- Shadow backlog (only `MASTER_BACKLOG.md` + `BACKLOG.md` index)
- Phase leakage in Phase 1 face
- Orphan active docs (not in README index)

Pre-sprint: [`GOVERNANCE_CHECKLIST.md`](GOVERNANCE_CHECKLIST.md)

---

## Code ↔ doc coupling

- Routes / flow → update `PRODUCT_MASTER.md` + `SIGNAL_SYSTEM.md` or `MATCH_SYSTEM.md`
- Engines → regression under `tests/regression/`
- Copy → [`CANONICAL_TERMINOLOGY.md`](CANONICAL_TERMINOLOGY.md)
