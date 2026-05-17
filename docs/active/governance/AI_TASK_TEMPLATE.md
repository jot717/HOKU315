# AI TASK TEMPLATE

FOLLOW:

README.md
→ docs/README.md
→ docs/active/governance/SSOT_HIERARCHY.md
→ docs/active/product/PRODUCT_MASTER.md
→ docs/active/product/AI_DEVELOPMENT_CONSTITUTION.md
→ docs/active/product/ROADMAP.md
→ docs/active/governance/GOVERNANCE_CHECKLIST.md
→ docs/active/governance/MASTER_BACKLOG.md
→ START_NEW_SPRINT.md

RULES:

* SSOT only
* no parallel systems
* no duplicate docs
* no phase drift
* no speculative architecture
* backlog → sprint → implement → regression → uat → done
* archive immediately after completion

CURRENT TARGET:
**PHASE2-A Persistence Architecture Review v1** (COMPLETE — see archive review)

DELIVERABLES:

* `docs/archive/reviews/PHASE2A_PERSISTENCE_ARCHITECTURE_REVIEW_v1.md`
* Scorecard, ownership map, PHASE2-B risk analysis
* Validation gates run (regression + UAT)

NON-GOALS:

* Cloud / Supabase / sync / realtime implementation
* Product behavior changes
* PHASE2-B adapter code

VALIDATION:

* python ops/flow/check_all_flows.py
* python ops/env/reflex_compile_gate.py
* pytest tests/regression/ -v --tb=short
* pytest tests/uat/ -v --tb=short
