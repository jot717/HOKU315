# PHASE BOUNDARY SYSTEM

> **Authority:** [`PRODUCT_MASTER.md`](PRODUCT_MASTER.md)

This document separates **what ships in the product face** from **backend and future moat work**. **No later-phase UI or copy may leak into earlier-phase experiences.**

## Phase 1 — Local signal product (current face)

**User belief:** “This system works from **my signal profile** and **the question flow** (plus target observation I enter).”

Includes:

- Local **signal profile** (`/profile`) — name, interests, stress text stored for the experience layer.
- **Questionnaire** (`/quiz`) — slider-derived signal vector and fox summary **without** treating cloud backup as the headline outcome.
- **Target observation** (`/target`) — user-described “other” for overlap analysis.
- **Rule-based inference** (`/insight`) — `infer_signal_risks`, guardian copy, local JSON/session history.
- **Match reasoning surface** (`/match`) — presentation of matches when cloud data exists; **errors must not** imply SNS or third-party APIs.

**Not in Phase 1 face:** OAuth branding, “sync failed”, paste-token workflows, Social Graph / SNS ingestion messaging, Graph API naming, or raw backend identifiers in banners.

## Phase 2 — Persistence, login, account memory

Includes:

- Durable **account** (email/password or equivalent) as a **utility**, not the product story.
- **Cross-device backup** of profile/quiz/vector/story records where implemented.
- Session and token handling **inside** auth flows only; user copy stays calm and non-technical.

**Rule:** Login screens may mention “帳號” but not vendor-specific token tutorials in the default experience.

## Phase 3 — SNS import, external graph, API sync

Includes:

- Consent-based **SNS connect**, **external profile** ingestion, **interaction ingestion**, and **social graph** intelligence.

**Rule:** All Phase 3 features are **behind** explicit product initiation; **no** placeholders (“connect Facebook”) in Phase 1 routes unless the feature is actually shipped and gated.

## Enforcement

- **UI / Reflex:** Primary routes `/`, `/profile`, `/quiz`, `/target`, `/insight`, `/match` — audit for Phase1-safe copy (see `docs/active/uat/PREMATURE_SNS_LAYER_AUDIT.md`).
- **Tests:** Regression asserts removed phrases do not appear in Phase1 page sources (`tests/regression/test_remove_premature_sns_layer_v1.py`).
- **Docs:** Roadmap files (`FOX_ROADMAP.md`, etc.) may describe Phase 3; they are **not** inlined into Phase1 callouts.

## Deprecated / future implementation notes

Technical notes on tokens, Supabase session fields, and future SNS modules: `docs/deprecated/future_sns_layer/README.md`.
