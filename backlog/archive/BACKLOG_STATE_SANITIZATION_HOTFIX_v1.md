# BACKLOG — STATE SANITIZATION HOTFIX v1

## STATUS

ACTIVE

## TYPE

RUNTIME STABILITY HOTFIX (Reflex hydration / socket sync — **no new features**)

## GOAL

Stabilize frontend runtime: `@rx.var` outputs JSON-safe primitives only, list fields are `list[str]` where required, session/history payloads sanitized, event handlers tolerate `None` / empty slider events, removed dead computed vars.

## DELIVERABLES

* Code: `fox_quiz/state/app_state.py`, `target_state.py`, `profile_state.py`, `product/session/runtime/session_history.py`, `fox_quiz/ui/components/session_history.py`
* [`docs/active/uat/STATE_SANITIZATION_RUNTIME_UAT.md`](../docs/active/uat/STATE_SANITIZATION_RUNTIME_UAT.md)
* Regression: `tests/regression/test_state_sanitization_hotfix_v1.py`

## NON-GOALS

New routes, product features, backend rewrites, auth, SNS.

## SPRINT

[`SPRINT_STATE_SANITIZATION_HOTFIX_v1.md`](SPRINT_STATE_SANITIZATION_HOTFIX_v1.md)
