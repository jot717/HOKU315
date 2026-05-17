# AI DEVELOPMENT CONSTITUTION

**Highest-priority implementation rule file for humans and AI agents.**  
Violations block merge until normalization.

**Authority chain:** This file ↁE[`PRODUCT_MASTER.md`](PRODUCT_MASTER.md) ↁEdomain SSOT ↁEcode.

---

## Section A  ESingle source of truth

**Only these files may define product logic:**

| File | Scope |
|------|--------|
| [`PRODUCT_MASTER.md`](PRODUCT_MASTER.md) | Identity, flow, systems, phases |
| [`SIGNAL_SYSTEM.md`](SIGNAL_SYSTEM.md) | Signal profile, quiz, target, inference |
| [`MATCH_SYSTEM.md`](MATCH_SYSTEM.md) | Social energy compatibility, match wall |
| [`ROADMAP.md`](ROADMAP.md) | Phased delivery (Phases 1 E) |
| [`../../backlog/MASTER_BACKLOG.md`](../../backlog/MASTER_BACKLOG.md) | Sprint index |
| [`../uat/UAT_MASTER_GUIDE.md`](../uat/UAT_MASTER_GUIDE.md) | Acceptance |

**All other docs:** reference-only or **historical archive** (`docs/archive/`).  
**Governance helpers (this file, terminology, checklist, context priority):** process only  Ethey do not redefine product logic.

---

## Section B  ENo second system rule

**Forbidden:**

- Second signal system, insight engine, onboarding, match system, memory layer
- Second UX narrative or terminology system
- Shadow backlog (`BACKLOG.md` slice files except `MASTER_BACKLOG.md` index)
- Parallel constitutions that restate the same rules

**Required:** Extend existing runtime modules and update SSOT docs in place.

---

## Section C  EPhase enforcement

| Phase | Allowed |
|-------|---------|
| **1** | Manual / local rule-based intelligence only |
| **2** | Persistence, account memory, cloud backup utility |
| **3** | SNS import (gated; no Phase 1 UI leakage) |
| **4** | Social graph intelligence |
| **5** | AI-scale inference |

No phase leakage in UX, copy, or default routes.

---

## Section D  EDocument creation rules

**Do not create** new constitution, roadmap, architecture, flow, or phase docs unless SSOT files cannot contain the change.

**Default:** Update `PRODUCT_MASTER.md`, `SIGNAL_SYSTEM.md`, `MATCH_SYSTEM.md`, or `ROADMAP.md`.

New ontologies/schemas ↁE**append to archive annex** under `docs/archive/phase1_legacy/` and link **once** from SSOT.

---

## Section E  EAI implementation workflow

Every future sprint must state:

| Field | Required |
|-------|----------|
| PHASE | e.g. 1-H2 governance |
| GOAL | One sentence |
| NON-GOALS | Explicit exclusions |
| PRODUCT IMPACT | SSOT files touched |
| UX IMPACT | Routes/copy |
| GOVERNANCE IMPACT | Archive moves, entropy |
| FILES UPDATED | List |
| FILES ARCHIVED | List |
| REGRESSION | pytest paths |
| COMMIT FORMAT | `type(scope): TITLE vN` |

---

## Section F  ERepo entropy rule

If duplicate meaning, overlapping terminology, archive docs cited as law, or multiple active truths appear:

1. **Stop** feature work  
2. Run normalization (this constitution + [`GOVERNANCE_CHECKLIST.md`](GOVERNANCE_CHECKLIST.md))  
3. Resume only when active doc count and terminology pass regression  

See [`ACTIVE_SURFACE_MAP.md`](ACTIVE_SURFACE_MAP.md) for routes, state, and UI law.

---

## Section G  ENo parallel systems

**Never create:**

- Second onboarding
- Second signal model
- Second match engine
- Second UX philosophy
- Second product identity

**Always** extend canonical systems (`SIGNAL_SYSTEM.md`, `MATCH_SYSTEM.md`, active runtime modules).

---

## Section H  EPhysical entropy rule

Before creating a **new folder**, **route**, **doc category**, or **runtime system**, AI must:

1. Check [`ACTIVE_SURFACE_MAP.md`](ACTIVE_SURFACE_MAP.md)
2. Check existing canonical system (SSOT + code)
3. **Extend** instead of duplicate

If the surface is not on the map, stop and update the map + `PRODUCT_MASTER` in a governance sprint  Edo not ship silently.
