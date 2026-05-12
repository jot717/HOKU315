# BACKLOG — SIGNAL SYSTEM CONSOLIDATION v1

## STATUS

ACTIVE

## TYPE

SIGNAL ARCHITECTURE CONSOLIDATION (docs + terminology + light UX; **SAFE MODE**)

## GOAL

Unify **existing** profile, quiz sliders, insight, memory, and signal wording under **one coherent signal architecture** — **no** duplicate onboarding system, **no** SNS/vector/auth implementation.

## DELIVERABLES

* [`ops/product/SIGNAL_SYSTEM_CONSTITUTION.md`](../ops/product/SIGNAL_SYSTEM_CONSTITUTION.md)
* [`ops/product/SIGNAL_PROFILE_SCHEMA.md`](../ops/product/SIGNAL_PROFILE_SCHEMA.md)
* [`ops/product/SIGNAL_FLOW_ARCHITECTURE.md`](../ops/product/SIGNAL_FLOW_ARCHITECTURE.md)
* [`ops/product/SIGNAL_INPUT_AUDIT.md`](../ops/product/SIGNAL_INPUT_AUDIT.md)
* [`ops/product/SIGNAL_STATE_MAPPING.md`](../ops/product/SIGNAL_STATE_MAPPING.md)
* [`ops/uat/SIGNAL_SYSTEM_CONSOLIDATION_UAT.md`](../uat/SIGNAL_SYSTEM_CONSOLIDATION_UAT.md)
* Home + profile (+ optional quiz intro) copy alignment
* [`GUARDIAN_UX_CONSTITUTION.md`](../product/GUARDIAN_UX_CONSTITUTION.md) — SIGNAL-FIRST section
* [`FOX_ROADMAP.md`](../product/FOX_ROADMAP.md) — consolidation pointer
* Regression: `tests/regression/test_signal_system_consolidation_v1.py`

## NON-GOALS

* New Supabase tables, SNS APIs, embeddings pipeline, social graph implementation, auth rewrites

## SPRINT

[`SPRINT_SIGNAL_SYSTEM_CONSOLIDATION_v1.md`](SPRINT_SIGNAL_SYSTEM_CONSOLIDATION_v1.md)
