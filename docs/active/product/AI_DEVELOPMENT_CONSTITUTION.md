# AI DEVELOPMENT CONSTITUTION

**Highest-priority implementation rule file for humans and AI agents.**

**Authority chain:** this file -> [`PRODUCT_MASTER.md`](PRODUCT_MASTER.md) -> domain SSOT -> code.

---

## Section A - Single source of truth

**Only these files may define product logic** (all under `docs/active/product/`):

| File | Scope |
|------|--------|
| [`PRODUCT_MASTER.md`](PRODUCT_MASTER.md) | Identity, flow, systems |
| [`SIGNAL_SYSTEM.md`](SIGNAL_SYSTEM.md) | Signal pipeline |
| [`MATCH_SYSTEM.md`](MATCH_SYSTEM.md) | Match / social energy |
| [`ROADMAP.md`](ROADMAP.md) | Phases 1-5 |
| [`../../../backlog/MASTER_BACKLOG.md`](../../../backlog/MASTER_BACKLOG.md) | Sprint index |
| [`../uat/UAT_MASTER_GUIDE.md`](../uat/UAT_MASTER_GUIDE.md) | Acceptance |

**All other docs:** reference-only or `docs/archive/`.

---

## Section B - No second system rule

Forbidden: second signal/match/onboarding/memory/UX narrative; shadow backlog; parallel constitutions.

Required: extend existing runtime and update SSOT in place.

---

## Section C - Phase enforcement

| Phase | Allowed |
|-------|---------|
| **1** | Manual / local rule-based intelligence |
| **2** | Persistence, account memory |
| **3** | SNS import (gated) |
| **4** | Social graph intelligence |
| **5** | AI-scale inference |

No phase leakage in Phase 1 face.

---

## Section D - Document creation rules

Do not create new constitution/roadmap/architecture docs unless SSOT cannot hold the change.

Default: update files in `docs/active/product/`.

Ontology annex: `docs/archive/product/` - link once from SSOT.

---

## Section E - AI implementation workflow

Every sprint must state: PHASE, GOAL, NON-GOALS, PRODUCT/UX/GOVERNANCE impact, FILES UPDATED/ARCHIVED, REGRESSION, COMMIT FORMAT.

---

## Section F - Repo entropy rule

On duplicate meaning or archive cited as law: stop feature work, normalize, re-run governance regression.

See [`../governance/GOVERNANCE_CHECKLIST.md`](../governance/GOVERNANCE_CHECKLIST.md) and [`ACTIVE_SURFACE_MAP.md`](ACTIVE_SURFACE_MAP.md).

---

## Section G - No parallel systems

Never create second onboarding, signal model, match engine, UX philosophy, or product identity.

---

## Section H - Physical entropy rule

Before new folder, route, doc category, or runtime system: check [`ACTIVE_SURFACE_MAP.md`](ACTIVE_SURFACE_MAP.md), extend canonical systems.

---

## Section I - Markdown highway rules

| Rule | Detail |
|------|--------|
| **No root markdown** | Never create `.md` in repo root except `README.md`, `BACKLOG.md`, `SPRINT_LOG.md` |
| **Active only** | Product/UAT law only under `docs/active/` |
| **No parallel constitutions** | One AI constitution (this file) |
| **Sprint docs** | Backlog/sprint slices only in `backlog/` or `backlog/archive/` |
| **Category required** | Every new doc must land in `docs/active/<category>/` or `docs/archive/<bucket>/` |
| **Archive ban** | `docs/archive/` never referenced for runtime planning or SSOT links |

Navigation: [`../../README.md`](../../README.md) -> [`../README.md`](../README.md).
