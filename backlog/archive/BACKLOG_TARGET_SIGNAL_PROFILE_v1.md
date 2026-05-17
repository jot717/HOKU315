# BACKLOG — TARGET SIGNAL PROFILE v1

## STATUS

ACTIVE

## TYPE

CORE PRODUCT LOOP FIX (named **target** + local JSON + insight integration)

## GOAL

Remove loop fragmentation: user signal profile + **target observation entity** + relationship simulation + guardian copy + memory, aligned to **HOME → PROFILE → TARGET → INSIGHT**.

## DELIVERABLES

* [`docs/active/product/TARGET_SIGNAL_CONSTITUTION.md`](../docs/active/product/TARGET_SIGNAL_CONSTITUTION.md)
* [`docs/active/product/TARGET_ANALYSIS_FLOW.md`](../docs/active/product/TARGET_ANALYSIS_FLOW.md)
* [`docs/active/product/TARGET_PROFILE_SCHEMA.md`](../docs/active/product/TARGET_PROFILE_SCHEMA.md)
* [`product/target/runtime/target_profile_store.py`](../product/target/runtime/target_profile_store.py)
* [`fox_quiz/ui/pages/target_page.py`](../fox_quiz/ui/pages/target_page.py) — route `/target`
* Insight simplification + target-aware guardian strings
* [`docs/active/uat/TARGET_SIGNAL_PROFILE_UAT.md`](../docs/active/uat/TARGET_SIGNAL_PROFILE_UAT.md)
* Regression: `tests/regression/test_target_signal_profile_v1.py`

## NON-GOALS

SNS APIs, embeddings, vector DB, auth, Supabase, multi-user systems, backend rewrite.

## SPRINT

[`SPRINT_TARGET_SIGNAL_PROFILE_v1.md`](SPRINT_TARGET_SIGNAL_PROFILE_v1.md)
