# AI DEVELOPMENT CONSTITUTION

**Highest-priority implementation rule file for humans and AI agents.**  
Violations block merge until normalization.

**Authority chain:** This file → [`PRODUCT_MASTER.md`](PRODUCT_MASTER.md) → domain SSOT → code.

---

## Section A — Single source of truth

**Only these files may define product logic:**

| File | Scope |
|------|--------|
| [`PRODUCT_MASTER.md`](PRODUCT_MASTER.md) | Identity, flow, systems, phases |
| [`SIGNAL_SYSTEM.md`](SIGNAL_SYSTEM.md) | Signal profile, quiz, target, inference |
| [`MATCH_SYSTEM.md`](MATCH_SYSTEM.md) | Social energy compatibility, match wall |
| [`ROADMAP.md`](ROADMAP.md) | Phased delivery (Phases 1–5) |
| [`../../backlog/MASTER_BACKLOG.md`](../../backlog/MASTER_BACKLOG.md) | Sprint index |
| [`../uat/UAT_MASTER_GUIDE.md`](../uat/UAT_MASTER_GUIDE.md) | Acceptance |

**All other docs:** reference-only or **historical archive** (`docs/archive/`).  
**Governance helpers (this file, terminology, checklist, context priority):** process only — they do not redefine product logic.

---

## Section B — No second system rule

**Forbidden:**

- Second signal system, insight engine, onboarding, match system, memory layer
- Second UX narrative or terminology system
- Shadow backlog (`BACKLOG.md` slice files except `MASTER_BACKLOG.md` index)
- Parallel constitutions that restate the same rules

**Required:** Extend existing runtime modules and update SSOT docs in place.

---

## Section C — Phase enforcement

| Phase | Allowed |
|-------|---------|
| **1** | Manual / local rule-based intelligence only |
| **2** | Persistence, account memory, cloud backup utility |
| **3** | SNS import (gated; no Phase 1 UI leakage) |
| **4** | Social graph intelligence |
| **5** | AI-scale inference |

No phase leakage in UX, copy, or default routes.

---

## Section D — Document creation rules

**Do not create** new constitution, roadmap, architecture, flow, or phase docs unless SSOT files cannot contain the change.

**Default:** Update `PRODUCT_MASTER.md`, `SIGNAL_SYSTEM.md`, `MATCH_SYSTEM.md`, or `ROADMAP.md`.

New ontologies/schemas → **append to archive annex** under `docs/archive/product/` and link **once** from SSOT.

---

## Section E — AI implementation workflow

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

## Section F — Repo entropy rule

If duplicate meaning, overlapping terminology, archive docs cited as law, or multiple active truths appear:

1. **Stop** feature work  
2. Run normalization (this constitution + [`GOVERNANCE_CHECKLIST.md`](GOVERNANCE_CHECKLIST.md))  
3. Resume only when active doc count and terminology pass regression  

See [`AI_CONTEXT_PRIORITY.md`](AI_CONTEXT_PRIORITY.md) for read order.
