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
**PHASE3 SNS** (FUTURE — see ROADMAP)

LAST COMPLETED:
**PHASE2-B-IMPL Cloud Persistence v1** — see `PHASE2B_CLOUD_PERSISTENCE_IMPL_REPORT_v1.md`

NON-GOALS (PHASE2-B closed):

* Realtime sync, SNS, graph/vector, embeddings, new routes, onboarding drift

VALIDATION:

* python ops/flow/check_all_flows.py
* pytest tests/regression/test_phase2b_cloud_persistence_planning_v1.py -v --tb=short
