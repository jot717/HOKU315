# BACKLOG — MATCH WALL compile hotfix v1

## Problem

Reflex compile/runtime failure: numeric compare on foreach item `distance` in `_match_card`.

## Fix

Precompute UI fields in `enrich_match_row_for_ui()` during `load_match_wall`; foreach renderer uses buckets + `rx.cond` only.

## Done when

- [x] No `distance </<=/>/>=` in `_match_card` / foreach render path
- [x] UAT doc + regression test
- [x] `reflex compile` green on policy venv

## Sprint

[`SPRINT_MATCH_WALL_COMPILE_HOTFIX_v1.md`](SPRINT_MATCH_WALL_COMPILE_HOTFIX_v1.md)
