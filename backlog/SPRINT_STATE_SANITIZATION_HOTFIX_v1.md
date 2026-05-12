# SPRINT — STATE SANITIZATION HOTFIX v1

## STATUS

ACTIVE

## DEFINITION OF DONE

* AppState `@rx.var` methods return only `str`, `int`, `float`, or `bool` (no dict/tuple/list-of-dict from vars)
* String list fields coerced via `_str_list`; `flow_result` / `insight_state` guarded when loading session or bound flow
* Session history rows normalized to string-only dicts on load/append
* Target/profile `on_change` handlers null-safe; slider handlers ignore empty updates
* `python ops/flow/check_all_flows.py` + `pytest tests/regression/` pass

## OUT OF SCOPE

Feature work, new pages, architecture redesign.
