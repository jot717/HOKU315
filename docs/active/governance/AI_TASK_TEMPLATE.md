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
**PHASE2-A Persistence Foundation v1**

DELIVERABLES:

* `product/persistence/runtime/` — `PersistenceBackend`, `LocalJsonBackend`, entity registry, `get_backend()`
* Runtime stores refactored to use persistence port (profile, target, fox_memory, session_history, local_session)
* `ROADMAP.md` PHASE2-A slice documented
* `backlog/archive/BACKLOG_PHASE2A_PERSISTENCE_FOUNDATION_v1.md` + `SPRINT_PHASE2A_*`
* `tests/regression/test_phase2a_persistence_foundation_v1.py`
* `RUNTIME_STATE_SCHEMA.md` — Phase 2-A backend note

NON-GOALS:

* Supabase / cloud persistence adapter
* Auth redesign or login UX changes
* SNS, graph, or PHASE3+ features
* New root markdown or parallel roadmap files
* Phase 1 face copy advertising cloud sync

VALIDATION:

* python ops/flow/check_all_flows.py
* python ops/env/reflex_compile_gate.py
* pytest tests/regression/test_phase2a_persistence_foundation_v1.py -v --tb=short
* pytest tests/regression/ -v --tb=short
