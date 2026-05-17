# SPRINT — MATCH WALL compile hotfix v1

**Goal:** Restore safe Reflex compile for `/match` grid.

## Tasks

1. Move distance thresholds into `enrich_match_row_for_ui()` (Python `float` domain).
2. Replace `_match_card` branching with `compat_bucket` / `risk_bucket` + `rx.cond`.
3. Document in `docs/active/uat/MATCH_WALL_COMPILE_HOTFIX.md`.
4. Add `tests/regression/test_match_wall_compile_hotfix_v1.py`.

## Verify

```powershell
python ops\env\reflex_compile_gate.py
pytest tests\regression\test_match_wall_compile_hotfix_v1.py -v
```
