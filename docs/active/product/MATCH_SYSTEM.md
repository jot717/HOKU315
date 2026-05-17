# MATCH SYSTEM - Single Source of Truth

> **Authority:** [`PRODUCT_MASTER.md`](PRODUCT_MASTER.md)
> **Implementation:** `product/match/runtime/`, `fox_quiz/match_wall.py`

**Social energy compatibility** - not dating score, not personality match.

---

## Scope

| Surface | Route | Runtime |
|---------|-------|---------|
| Match wall | `/match` | `match_rhythm_engine.py`, `enrich_match_row_for_ui` |
| Bound flow score | `/insight` (demo) | `product/app_binding/`, MVP scoring |

Requires **account mode** for live peer rows from backend; guest may see redirect to `/login`.

---

## Core rules

1. Cards show rhythm, reply pressure, emotional pacing, energy safety, exhaustion point, scenario - precomputed in Python.
2. Match archetypes - content in archive; engine: `generate_match_credibility_bundle`.
3. Energy model - annex in `docs/archive/product/`.
4. Use canonical terminology per `CANONICAL_TERMINOLOGY.md`.

---

## Historical technical annex

`docs/archive/product/` - match credibility constitution, archetype tables, social energy model.

---

## Phase boundaries

Phase 1: rule-based peer inference. Phase 3+: SNS graph - not in Phase 1 UI.
