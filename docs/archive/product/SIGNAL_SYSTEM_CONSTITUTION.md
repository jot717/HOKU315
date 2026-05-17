# SIGNAL SYSTEM CONSTITUTION (v1)

**STATUS:** ACTIVE  
**TYPE:** System consolidation — **one coherent signal architecture** across existing surfaces

This document **locks how the repo already works** and forbids parallel “new onboarding” systems. It complements [`SIGNAL_FLOW_ARCHITECTURE.md`](SIGNAL_FLOW_ARCHITECTURE.md), [`SIGNAL_PROFILE_SCHEMA.md`](SIGNAL_PROFILE_SCHEMA.md), and [`SIGNAL_FIRST_PRODUCT_POSITION.md`](SIGNAL_FIRST_PRODUCT_POSITION.md) (archived guardian-UX spec: [`docs/deprecated/GUARDIAN_UX_CONSTITUTION.md`](../../docs/deprecated/GUARDIAN_UX_CONSTITUTION.md)).

---

## Core rule: no duplicate onboarding

* **Do not** add a second onboarding route, wizard, or “first-run” flow that duplicates `/profile` or `/quiz`.
* **Do** treat **`/profile`** as the **canonical Signal Profile Setup** entry for name, interests, and stress/activity (1–10).
* **Do** treat **`/quiz`** (20 sliders, `SOCIAL_MINE_DIMENSIONS`) as the **optional deep signal questionnaire** — same product story, different depth.
* **Do** treat **`/insight`** as **Guardian Observation** over bound flow output + local memory — not a separate product silo.

---

## Single mental model

Users are building a **signal profile** (what drains them, what pressures them, how they tolerate interaction), **not** a personality typing profile.

Interpreter copy (including legacy “guardian” tone in some engines) exists to **explain signals**; it must not **replace** the signal pipeline story (see **Signal-first UX law** in [`SIGNAL_FIRST_PRODUCT_POSITION.md`](SIGNAL_FIRST_PRODUCT_POSITION.md)).

---

## Canonical artifacts (existing)

| Artifact | Role |
|----------|------|
| `runtime_state/user_profile.json` | Persisted **signal profile** slice (name, interests, activity) |
| `runtime_state/fox_memory.json` | **Signal memory** — recent patterns / warnings for guardian continuity |
| Session / insight payloads | **Observation outputs** from bound flow + formatters |
| `SOCIAL_MINE_DIMENSIONS` + quiz sliders | **High-dimensional mine sensitivity** (vector-backed when logged in) |

---

## Consolidation vs new direction

This constitution is **normalization and alignment** of existing pieces. It is **not** a new product pivot. For north-star product language, see [`CORE_PRODUCT_REALIGNMENT.md`](CORE_PRODUCT_REALIGNMENT.md).

---

## References

* [`SIGNAL_INPUT_AUDIT.md`](SIGNAL_INPUT_AUDIT.md) — what exists, overlaps, drift  
* [`SIGNAL_STATE_MAPPING.md`](SIGNAL_STATE_MAPPING.md) — state → canonical signal meaning  
* [`SIGNAL_PROFILE_SCHEMA.md`](SIGNAL_PROFILE_SCHEMA.md) — future unified JSON shape  
* [`SIGNAL_FLOW_ARCHITECTURE.md`](SIGNAL_FLOW_ARCHITECTURE.md) — end-to-end flow
