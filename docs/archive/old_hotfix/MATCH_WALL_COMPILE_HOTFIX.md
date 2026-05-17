# MATCH WALL — Compile hotfix (PHASE1 maintenance)

**Date:** 2026-05-16  
**Scope:** `fox_quiz/match_wall.py` + rendering rules for `rx.foreach`.

## Root cause

`rx.foreach(MatchWallState.matches, _match_card)` passes **each dict field as a reactive Var**.  
Using **Python numeric comparison** in the render path, e.g. `distance <= 0.35`, produces operands like `ObjectItemOperation` vs `float`, which raises:

```text
TypeError: '<=' not supported between instances of 'ObjectItemOperation' and 'float'
```

This is a **Reflex / reactive collection** limitation: UI lambdas must not treat foreach item fields as plain Python numbers for ordering or threshold checks.

## Fix pattern

1. **Compute thresholds in plain Python** when building state (e.g. in `load_match_wall` / `_load()`), using `float(...)` on the server/thread side.
2. Store **string buckets** (`"h" | "m" | "l"`) or other **discrete tokens** on each row dict.
3. In `_match_card`, use **`rx.cond(item["bucket"] == "h", ...)`** (or equivalent) **only** — no `distance <= 0.35` in the foreach renderer.

Helper: `enrich_match_row_for_ui()` in `match_wall.py`.

## Forbidden in `rx.foreach` render callbacks

- `field <= literal_float` / `field <` / `>` / `>=` where `field` comes from the foreach item.
- Any **native Python numeric ordering** on reactive item fields.

## Safe patterns

- Precompute **`compat_bucket`**, **`risk_bucket`**, **`emotion_line`**, **`distance_str`**, etc. before assigning `MatchWallState.matches`.
- **`rx.cond`** / **`rx.match`** on **string or enum-like** fields that were set in Python.
- Comparisons on **`SessionState`** fields or top-level `rx.State` vars outside foreach item accessors follow normal Reflex rules; still avoid mixing untested numeric compares on Var if the compiler complains.

## Validation

- `python -m reflex compile` (or `ops/env/reflex_compile_gate.py`) succeeds.
- `/match` grid renders after login when RPC returns rows.

## References

- Code: `fox_quiz/match_wall.py`
- Regression: `tests/regression/test_match_wall_compile_hotfix_v1.py`
