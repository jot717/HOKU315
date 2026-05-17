# MASTER BACKLOG

**Canonical phase index.** Detail slices live in `backlog/archive/` after completion.  
Product truth: [`ops/product/PRODUCT_MASTER.md`](../ops/product/PRODUCT_MASTER.md) · P0/P1 engineering: [`../BACKLOG.md`](../BACKLOG.md)

---

## ACTIVE

| Phase | Status | Summary | UAT |
|-------|--------|---------|-----|
| **APP SHELL REPLACEMENT v1** | WIP / planned | Shell routing & product surface alignment | TBD |
| **PHASE2 persistence** | FUTURE | Account memory, cross-device backup (utility) | — |
| **PHASE3 SNS** | FUTURE | Opt-in graph ingestion | — |

---

## COMPLETED (Phase 1 family)

Each row = **one canonical entry**. Sprint files: `backlog/archive/BACKLOG_*` / `SPRINT_*`.

| Phase | Summary | Key docs |
|-------|---------|----------|
| **PHASE1-G Governance v1** | Product master, backlog/UAT governance, guest/login clarity | `PRODUCT_MASTER.md`, `MASTER_BACKLOG.md`, `UAT_MASTER_GUIDE.md` |
| **PHASE1-F Match credibility v1** | Social energy match cards, rhythm engine | `MATCH_ARCHETYPE_SYSTEM.md`, `match_rhythm_engine.py` |
| **PHASE1-D UX intelligence v1** | Interaction pressure copy, insight upgrade | `ux_intelligence_engine.py`, `INTERACTION_PRESSURE_ONTOLOGY.md` |
| **PHASE1-E Environment lockdown v1** | Python/Reflex pin, compile gate | `ops/env/STARTUP_GUIDE.md` |
| **PHASE1 Product flow recovery v1** | Signal-first journey, nav, insight | `PHASE1_PRODUCT_FLOW.md` |
| **Premature SNS layer removal v1** | No API/token noise in Phase 1 UI | `PHASE_BOUNDARY_SYSTEM.md` |
| **Match wall compile hotfix v1** | `rx.foreach` precompute | `MATCH_WALL_COMPILE_HOTFIX` (archived UAT) |
| **State sanitization hotfix v1** | Reflex state safety | archive |
| **Target signal profile v1** | `/target` entity | `TARGET_SIGNAL_CONSTITUTION.md` |
| **Relationship signal simulation v1** | Archetypes + overlap | `RELATIONSHIP_INTELLIGENCE_CONSTITUTION.md` |
| **Signal intelligence engine v1** | `infer_signal_risks` | `SIGNAL_INTELLIGENCE_CONSTITUTION.md` |
| **Signal system consolidation v1** | Unified signal architecture | `SIGNAL_SYSTEM_CONSTITUTION.md` |
| **Product core realignment v1** | Guardian network direction lock | `CORE_PRODUCT_REALIGNMENT.md` |
| **PHASE1 UAT flow fix v2** | Onboarding clarity | `PHASE1_UAT_SCRIPT.md` |
| **FLOW / MATCH / UNLOCK / INSIGHT v1** | Core product modules | `product/*/README.md` |

---

## ARCHIVED

- All `backlog/archive/BACKLOG_*.md` and `SPRINT_*.md` — historical scope/DoD
- Drift reports: `docs/deprecated/archive/product/`
- Superseded UAT: `docs/deprecated/archive/uat/`

---

## BLOCKED

| Item | Blocker |
|------|---------|
| Real SNS ingestion | Phase 3; consent + infra |
| Production Stripe unlock | P1 Task 9; not Phase 1 governance scope |

---

## FUTURE PHASES

| Phase | Scope |
|-------|--------|
| **2** | Longitudinal memory, account utility, cloud backup UX |
| **3** | SNS import, external graph, interaction ingestion |
| **4+** | See [`ops/product/FOX_ROADMAP.md`](../ops/product/FOX_ROADMAP.md) |

---

## How to add work

1. Add **one row** here (ACTIVE).
2. Create `BACKLOG_<slug>_v1.md` + `SPRINT_<slug>_v1.md` if slice detail needed.
3. Link from `PRODUCT_MASTER.md` only if it changes product truth.
4. On complete → move slice to `backlog/archive/`, move row to COMPLETED.
