# AI TASK TEMPLATE

FOLLOW:

README.md
→ docs/README.md
→ docs/active/product/PRODUCT_MASTER.md
→ docs/active/product/AI_DEVELOPMENT_CONSTITUTION.md
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
[REPLACE HERE]

DELIVERABLES:
[REPLACE HERE]

NON-GOALS:
[REPLACE HERE]

VALIDATION:

* python ops/flow/check_all_flows.py
* python ops/env/reflex_compile_gate.py
* pytest tests/regression/ -v --tb=short
