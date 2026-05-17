# MATCH SYSTEM — Single Source of Truth

> **Authority:** [`PRODUCT_MASTER.md`](PRODUCT_MASTER.md) · **Implementation:** `product/match/runtime/`, `fox_quiz/match_wall.py`

**Social energy compatibility** — not dating score, not personality match.

---

## Scope

| Surface | Route | Runtime |
|---------|-------|---------|
| Match wall | `/match` | `match_rhythm_engine.py`, `enrich_match_row_for_ui` |
| Bound flow score | `/insight` (demo) | `product/app_binding/`, `match_engine.py` (MVP scoring) |

Requires **account mode** for live peer rows from backend; guest may see redirect to `/login`.

---

## Core rules

1. Cards show **rhythm, reply pressure, emotional pacing, energy safety, exhaustion point, scenario** — precomputed in Python (no float compares in `rx.foreach`).
2. **Match archetypes** — `MATCH_ARCHETYPE_SYSTEM` content in archive; engine: `generate_match_credibility_bundle`.
3. **Energy model** — response debt, carry load, pacing mismatch (`SOCIAL_ENERGY_MODEL` annex in archive).
4. No “相容度：高” vibe-only copy; use 社交電量 / 互動節奏 language per [`CANONICAL_TERMINOLOGY.md`](CANONICAL_TERMINOLOGY.md).

---

## Historical technical annex

`docs/archive/product/` — match credibility constitution, archetype tables, social energy model detail.

---

## Phase boundaries

Phase 1: presentation + rule-based peer shape inference from distance + user inference.  
Phase 3+: SNS-backed graph — **not** in Phase 1 UI.
