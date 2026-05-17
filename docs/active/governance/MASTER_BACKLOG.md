# MASTER BACKLOG

**Canonical planning index.** Phase law: [`../product/ROADMAP.md`](../product/ROADMAP.md) · Authority map: [`SSOT_HIERARCHY.md`](SSOT_HIERARCHY.md) · Detail slices: `backlog/archive/` after completion.

Product truth: [`../product/PRODUCT_MASTER.md`](../product/PRODUCT_MASTER.md) · Boot: [`START_NEW_SPRINT.md`](START_NEW_SPRINT.md) · Engineering P0/P1: [`../../../BACKLOG.md`](../../../BACKLOG.md)

---

## ACTIVE

| Phase | Status | Summary | UAT |
|-------|--------|---------|-----|
| **PHASE2-B cloud persistence** | FUTURE | Supabase adapter behind same port (utility); see `docs/archive/reviews/PHASE2A_*` | - |
| **PHASE3 SNS** | FUTURE | Opt-in graph ingestion | - |

---

## COMPLETED (Phase 1 family)

| Phase | Summary | Key docs |
|-------|---------|----------|
| **PHASE2-A Persistence architecture review v1** | Review scorecard WARN; ownership map; 2-B risks | `docs/archive/reviews/PHASE2A_PERSISTENCE_ARCHITECTURE_REVIEW_v1.md` |
| **PHASE2-A Persistence foundation v1** | `PersistenceBackend`, local JSON port, store refactor | `product/persistence/runtime/` |
| **PHASE1-H7 SSOT hierarchy v1** | `SSOT_HIERARCHY.md`, ROADMAP PHASE1–7, authority chain | `SSOT_HIERARCHY.md` |
| **PHASE1-H6 AI development discipline v1** | `START_NEW_SPRINT.md`, `AI_TASK_TEMPLATE.md`, regression guard | `START_NEW_SPRINT.md` |
| **PHASE1-H5 Root consolidation v1** | Root lobby, governance layer in `docs/active/governance/` | `docs/README.md` |
| **PHASE1-H4 MD highway v1** | `docs/active/` SSOT, archive buckets | `docs/active/product/` |
| **PHASE1-H3 Repo minimization v1** | Active surface map, dead routes, WIP quarantine | `ACTIVE_SURFACE_MAP.md` |
| **PHASE1-H2 AI governance reset v1** | SSOT consolidation, AI constitution | `AI_DEVELOPMENT_CONSTITUTION.md` |
| **PHASE1-G Governance v1** | Product master, guest/login clarity | `PRODUCT_MASTER.md` |
| **PHASE1-F Match credibility v1** | Social energy match cards | `match_rhythm_engine.py` |
| **PHASE1-D UX intelligence v1** | Interaction pressure copy | `ux_intelligence_engine.py` |
| **PHASE1-E Environment lockdown v1** | Python/Reflex pin, compile gate | `docs/active/env/STARTUP_GUIDE.md` |
| **PHASE1 Product flow recovery v1** | Signal-first journey | `PHASE1_PRODUCT_FLOW_UAT.md` |

Full rows: see `backlog/archive/` and [`../archive/legacy/sprint_history/SPRINT_LOG_FULL.md`](../archive/legacy/sprint_history/SPRINT_LOG_FULL.md).

---

## ARCHIVED

- `backlog/archive/BACKLOG_*` and `SPRINT_*`
- `docs/archive/product/`, `docs/archive/uat/`, `docs/archive/hotfix/`

---

## FUTURE PRODUCT PHASES

All phase definitions: [`../product/ROADMAP.md`](../product/ROADMAP.md) only. Do not duplicate here.

| Phase | Status |
|-------|--------|
| **2** | Persistence & memory |
| **3** | SNS import |
| **4** | Social graph intelligence |
| **5** | AI-scale inference |
| **6** | Guardian automation & trust |
| **7** | Platform & ecosystem |

---

## How to add work

1. One row in ACTIVE.
2. Optional `backlog/archive/BACKLOG_<slug>_v1.md` + `SPRINT_<slug>_v1.md`.
3. On complete: move slice to `backlog/archive/`, row to COMPLETED.
