# STATE SANITIZATION — RUNTIME UAT (v1)

**TYPE:** Stability hotfix — Reflex state + hydration.  
**Refs:** [`backlog/BACKLOG_STATE_SANITIZATION_HOTFIX_v1.md`](../../backlog/BACKLOG_STATE_SANITIZATION_HOTFIX_v1.md)

## Manual checks (pass)

* `reflex run` — open `/`, `/profile`, `/target`, `/insight` without console **socket** crash loops.
* No repeated **hydration** redlines when toggling insight empty ↔ result.
* Sliders on `/target` moved quickly do not blank the page.

## Regression (automated)

* `pytest tests/regression/test_state_sanitization_hotfix_v1.py`
* Full suite: `pytest tests/regression/ -v --tb=short`

## Fail criteria

* New product behavior or routes added under this sprint name.
