# SSOT HIERARCHY

**Purpose:** Single authority map for roadmap → planning → sprint → execution.  
**Boot:** [`START_NEW_SPRINT.md`](START_NEW_SPRINT.md) · **Phases:** [`../product/ROADMAP.md`](../product/ROADMAP.md)

---

## Product SSOT

**Location:** `docs/active/product/` (7 files + README)

| File | Owns |
|------|------|
| [`PRODUCT_MASTER.md`](../product/PRODUCT_MASTER.md) | Identity, official flow, system table |
| [`SIGNAL_SYSTEM.md`](../product/SIGNAL_SYSTEM.md) | Signal pipeline law |
| [`MATCH_SYSTEM.md`](../product/MATCH_SYSTEM.md) | Match / social energy law |
| [`ROADMAP.md`](../product/ROADMAP.md) | **PHASE1–PHASE7** boundaries only |
| [`AI_DEVELOPMENT_CONSTITUTION.md`](../product/AI_DEVELOPMENT_CONSTITUTION.md) | AI implementation rules |
| [`CANONICAL_TERMINOLOGY.md`](../product/CANONICAL_TERMINOLOGY.md) | Wording law |
| [`ACTIVE_SURFACE_MAP.md`](../product/ACTIVE_SURFACE_MAP.md) | Routes / components / folders |

**Rule:** Extend these files in place. No parallel product constitutions.

---

## Governance SSOT

**Location:** `docs/active/governance/`

| File | Owns |
|------|------|
| [`START_NEW_SPRINT.md`](START_NEW_SPRINT.md) | Mandatory context load + execution chain |
| [`SSOT_HIERARCHY.md`](SSOT_HIERARCHY.md) | **This file** — authority precedence |
| [`MASTER_BACKLOG.md`](MASTER_BACKLOG.md) | Phase/sprint index (ACTIVE / COMPLETED) |
| [`REPO_GOVERNANCE_RULES.md`](REPO_GOVERNANCE_RULES.md) | Where doc types live |
| [`GOVERNANCE_CHECKLIST.md`](GOVERNANCE_CHECKLIST.md) | Pre-sprint gates |
| [`REPO_ENTROPY_CHECKLIST.md`](REPO_ENTROPY_CHECKLIST.md) | Physical repo entropy |
| [`DEVELOPMENT_CONSTITUTION.md`](DEVELOPMENT_CONSTITUTION.md) | Engineering principles |
| [`ARCHITECTURE_CONTRACT.md`](ARCHITECTURE_CONTRACT.md) | Interface contracts |
| [`REPO_ARCHITECTURE.md`](REPO_ARCHITECTURE.md) | Repo layering |
| [`AI_TASK_TEMPLATE.md`](AI_TASK_TEMPLATE.md) | Per-sprint task shell |
| [`PHASE2B_CLOUD_PERSISTENCE_PLAN.md`](PHASE2B_CLOUD_PERSISTENCE_PLAN.md) | PHASE2-B cloud boundaries (planning; pre-impl) |

**Supplemental (not precedence law):** [`AI_CONTEXT_PRIORITY.md`](AI_CONTEXT_PRIORITY.md) — load hints only; if conflict, use this file + `START_NEW_SPRINT.md`.

---

## Planning SSOT

| Document | Owns | Does not own |
|----------|------|----------------|
| [`ROADMAP.md`](../product/ROADMAP.md) | PHASE1–7 mission, scope, non-goals | Sprint task lists |
| [`MASTER_BACKLOG.md`](MASTER_BACKLOG.md) | Which phase/sprint is ACTIVE or COMPLETED | Product identity |
| Root [`BACKLOG.md`](../../../BACKLOG.md) | P0/P1 engineering stabilization index | Product phases, UAT law |
| `backlog/archive/BACKLOG_<slug>_v1.md` | Slice detail for one initiative | Global phase boundaries |

**Rule:** New product phase work starts with a ROADMAP check, then one MASTER_BACKLOG ACTIVE row.

---

## Sprint SSOT

| Artifact | Owns |
|----------|------|
| `backlog/archive/SPRINT_<slug>_v1.md` | Sprint goal, non-goals, deliverables for one slice |
| Root [`SPRINT_LOG.md`](../../../SPRINT_LOG.md) | Recent execution summary (pointer) |
| [`docs/archive/legacy/sprint_history/SPRINT_LOG_FULL.md`](../archive/legacy/sprint_history/SPRINT_LOG_FULL.md) | Full historical log |

**Rule:** No active sprint plans in `docs/archive/` or repo root (except `SPRINT_LOG` index).

**Naming:** `PHASE1-H*` = governance sprint; `PHASE2` in MASTER_BACKLOG = product phase from ROADMAP.

---

## Execution SSOT

| Stage | Authority | Validation |
|-------|-----------|------------|
| Boot | `START_NEW_SPRINT.md` load order | `GOVERNANCE_CHECKLIST.md` |
| Implement | `AI_DEVELOPMENT_CONSTITUTION.md` + domain SSOT | Code review vs `ACTIVE_SURFACE_MAP.md` |
| Regression | `tests/regression/` | `pytest tests/regression/` |
| UAT | `docs/active/uat/UAT_MASTER_GUIDE.md` | Phase-appropriate UAT doc |
| Ops gates | `ops/flow/`, `ops/env/` | `check_all_flows.py`, `reflex_compile_gate.py` |

**Rule:** `ops/` holds executables only — no product truth.

---

## Archive rules

| Zone | Role |
|------|------|
| `docs/archive/` | Read-only history |
| `backlog/archive/` | Completed BACKLOG/SPRINT slices |
| `docs/deprecated/` | Retired paths (pointer only) |

**Forbidden:**

- Loading archive as implementation context
- Creating ACTIVE planning rows only in archive
- Duplicating ROADMAP phase text into new active files

---

## Authority precedence rules

When documents conflict, apply top-down:

1. [`PRODUCT_MASTER.md`](../product/PRODUCT_MASTER.md) — identity & flow  
2. [`ROADMAP.md`](../product/ROADMAP.md) — phase boundaries  
3. [`AI_DEVELOPMENT_CONSTITUTION.md`](../product/AI_DEVELOPMENT_CONSTITUTION.md) — AI behavior  
4. Domain SSOT (`SIGNAL_SYSTEM`, `MATCH_SYSTEM`, terminology, surface map)  
5. [`SSOT_HIERARCHY.md`](SSOT_HIERARCHY.md) — ownership map (this file)  
6. [`MASTER_BACKLOG.md`](MASTER_BACKLOG.md) — what is ACTIVE now  
7. Sprint slice (`backlog/archive/BACKLOG_*`, `SPRINT_*`)  
8. Root `BACKLOG.md` — engineering tasks only  
9. Archive / deprecated — **never** overrides 1–8  

---

## Minimized duplicates (resolved)

| Was ambiguous | Resolution |
|---------------|------------|
| `FOX_ROADMAP.md` vs `ROADMAP.md` | Only `docs/active/product/ROADMAP.md` is law |
| `AI_CONTEXT_PRIORITY` vs `START_NEW_SPRINT` | Boot order = `START_NEW_SPRINT`; priority file is supplemental |
| `PRODUCT_MASTER` phase table vs `ROADMAP` | Table in master = summary; detail = `ROADMAP.md` |
| `PHASE1-H*` vs `PHASE2` product | H = governance sprint; digit = product phase |
| Root `BACKLOG.md` vs `MASTER_BACKLOG` | Master = canonical index; root = P0/P1 engineering |
