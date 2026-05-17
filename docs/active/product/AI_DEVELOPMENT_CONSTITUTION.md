# AI DEVELOPMENT CONSTITUTION

**Highest-priority implementation rule file for humans and AI agents.**

**Authority chain:** this file -> [`PRODUCT_MASTER.md`](PRODUCT_MASTER.md) -> code.

---

## AI CONTEXT LOAD ORDER

1. [`../../../README.md`](../../../README.md)
2. [`../../README.md`](../../README.md)
3. [`PRODUCT_MASTER.md`](PRODUCT_MASTER.md)
4. [`AI_DEVELOPMENT_CONSTITUTION.md`](AI_DEVELOPMENT_CONSTITUTION.md)
5. [`ACTIVE_SURFACE_MAP.md`](ACTIVE_SURFACE_MAP.md)

**AI MUST IGNORE** (unless explicitly requested):

- `docs/archive/`
- `docs/deprecated/`
- Old sprint docs outside `backlog/archive/`
- Legacy UAT and hotfix reports
- `docs/archive/legacy/sprint_history/`

---

## Section A - Single source of truth

Product logic only in `docs/active/product/`:

| File | Scope |
|------|--------|
| `PRODUCT_MASTER.md` | Identity, flow, systems |
| `SIGNAL_SYSTEM.md` | Signal pipeline |
| `MATCH_SYSTEM.md` | Match / social energy |
| `ROADMAP.md` | Phases 1-5 |
| `../governance/MASTER_BACKLOG.md` | Sprint index |
| `../uat/UAT_MASTER_GUIDE.md` | Acceptance |

---

## Section B - No second system rule

Forbidden: parallel signal/match/onboarding/memory/UX systems; shadow backlog.

---

## Section C - Phase enforcement

Phase 1 = local rules only. Phases 2-5 gated. No leakage in Phase 1 face.

---

## Section D - Document creation rules

- **Never** create markdown in repository root (except `README`, `BACKLOG`, `SPRINT_LOG`)
- **Never** create parallel constitutions
- **Never** create temporary sprint md outside `backlog/` or `backlog/archive/`
- **All** new docs require category under `docs/active/<category>/` or `docs/archive/<bucket>/`
- **Active** docs only under `docs/active/`
- **Archive** docs never referenced for runtime planning

Default: update SSOT files in place.

---

## Section E - Sprint workflow

Every sprint: PHASE, GOAL, NON-GOALS, impacts, FILES UPDATED/ARCHIVED, REGRESSION, COMMIT FORMAT.

---

## Section F - Repo entropy rule

On duplicate meaning: stop, normalize, re-run governance tests.

See [`../governance/GOVERNANCE_CHECKLIST.md`](../governance/GOVERNANCE_CHECKLIST.md) and [`ACTIVE_SURFACE_MAP.md`](ACTIVE_SURFACE_MAP.md).

---

## Section G - No parallel systems

Never create second onboarding, signal model, match engine, UX philosophy, or product identity.

---

## Section H - Physical entropy rule

Before new folder/route/doc/system: check `ACTIVE_SURFACE_MAP.md`, extend canonical code.

---

## Section I - Markdown highway

| Rule | Detail |
|------|--------|
| Root | Lobby only - no knowledge content |
| `docs/active/` | Only knowledge layer |
| `docs/archive/` | Historical graveyard |
| `ops/` | Executable factory only (`env`, `flow`, `debug`, `testing`) |

Governance: [`../governance/`](../governance/)
