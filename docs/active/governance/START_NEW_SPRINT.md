# START NEW SPRINT

## PURPOSE

This file is the mandatory AI boot sequence.

Before ANY implementation:

1. Load README.md
2. Load docs/README.md
3. Load PRODUCT_MASTER.md
4. Load AI_DEVELOPMENT_CONSTITUTION.md
5. Load GOVERNANCE_CHECKLIST.md
6. Load MASTER_BACKLOG.md

Never skip this order.

---

# AI CONTEXT LOAD ORDER

README.md
→ docs/README.md
→ docs/active/product/PRODUCT_MASTER.md
→ docs/active/product/AI_DEVELOPMENT_CONSTITUTION.md
→ docs/active/governance/GOVERNANCE_CHECKLIST.md
→ docs/active/governance/MASTER_BACKLOG.md

---

# IMPLEMENTATION FLOW

BACKLOG
→ SPRINT
→ IMPLEMENT
→ REGRESSION
→ UAT
→ DONE
→ ARCHIVE

Never skip phases.

---

# FORBIDDEN AI BEHAVIORS

## DO NOT:

* create parallel constitutions
* create v2/v3 architecture docs
* create duplicate roadmap files
* create temporary migration systems
* use archive as implementation truth
* create root markdown files
* generate speculative future systems
* mix PHASE2/3/4 implementations
* create second onboarding flow
* create second product identity
* bypass regression
* bypass UAT
* leave temporary debug systems

---

# REPO DISCIPLINE

## ROOT

Root is entry only.

Allowed:

* README.md
* BACKLOG.md
* SPRINT_LOG.md
* requirements.txt
* scripts/config

No other markdown allowed.

---

# DOCS

## ACTIVE

# docs/active/

single source of truth

## ARCHIVE

# docs/archive/

historical only

Never use archive as active implementation context.

---

# OPS

# ops/

executable operations only

No product truth inside ops.

---

# PRODUCT TRUTH

Only extend:

* PRODUCT_MASTER.md
* SIGNAL_SYSTEM.md
* MATCH_SYSTEM.md
* ROADMAP.md

Never create parallel systems.

---

# PHASE BOUNDARIES

PHASE1:
local intelligence only

PHASE2:
persistence layer

PHASE3:
SNS integration

PHASE4:
graph intelligence

PHASE5:
AI scaling

Never implement future phases early.
