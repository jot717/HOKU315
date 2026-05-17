# BACKLOG — PHASE1 product flow recovery v1

## Objective

Restore **one** clear user path and signal-first positioning without backend, auth, or vector changes.

## Locked flow

HOME → `/profile` → `/quiz` → `/target` → `/insight` → `/match`

## Deliverables

- [x] Home, profile, quiz, target, insight, match copy and structure  
- [x] Nav cleanup (core six + login)  
- [x] Docs: `docs/active/product/PHASE1_PRODUCT_FLOW.md`, `PAGE_PURPOSE_SYSTEM.md`, `SIGNAL_FIRST_PRODUCT_POSITION.md`  
- [x] UAT: `docs/active/uat/PHASE1_PRODUCT_FLOW_UAT.md`  
- [x] Deprecation record: `docs/deprecated/` + `README.md`  
- [x] Regression: `pytest tests/regression/`; `python ops/flow/check_all_flows.py`

## Out of scope

Backend rewrite, embeddings, agents, new routes, SNS APIs.

## References

- Sprint: [`SPRINT_PHASE1_PRODUCT_FLOW_RECOVERY_v1.md`](SPRINT_PHASE1_PRODUCT_FLOW_RECOVERY_v1.md)
