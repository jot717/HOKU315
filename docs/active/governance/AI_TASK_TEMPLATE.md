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
**PHASE2-B Cloud Persistence Planning v1** (COMPLETE — see plan)

DELIVERABLES:

* `docs/active/governance/PHASE2B_CLOUD_PERSISTENCE_PLAN.md`
* ROADMAP PHASE2-B planning slice
* `backlog/archive/BACKLOG_PHASE2B_CLOUD_PERSISTENCE_PLANNING_v1.md`
* `tests/regression/test_phase2b_cloud_persistence_planning_v1.py`

NON-GOALS:

* Supabase adapter implementation
* Realtime / SNS / graph / embeddings expansion
* Auth UX redesign
* New product routes

VALIDATION:

* python ops/flow/check_all_flows.py
* pytest tests/regression/test_phase2b_cloud_persistence_planning_v1.py -v --tb=short
