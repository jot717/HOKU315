# PREMATURE SNS / API LAYER AUDIT (Phase1 UX)

**Scope:** Phase1 product is **local signal analysis + questionnaire + target observation + rule-based inference**. End users must not see **SNS**, **OAuth**, **Graph API**, **paste token**, **sync failure to cloud**, or **user-id parse** troubleshooting in primary flows.

**Date:** 2026-05-16

## Summary

| Area | Finding | Action (this hotfix) |
|------|---------|----------------------|
| Quiz result | Shamed users for "not logged in", showed `MOCK_LOGIN_USER_ID`, `[同步失敗]`, raw backend errors, "雲端脈絡" | Local-first success copy; optional cloud upsert errors softened; no red error callout for cloud |
| Login page | Copy named vendor auth + "token 存於裝置" | Neutral account / Phase2 backup wording |
| Story page | JWT, `user_id/`, Storage/RLS dump in UI, `DEBUG_URL` | Plain user copy; generic errors; remove debug print |
| Chat (deprecated route) | Message told users to paste token / env MOCK | Redirect-style guidance via login |
| Match wall | Load errors echoed exception (could leak token vocabulary) | Generic load failure string |
| Session state | Module doc named Supabase + Token | Doc points to Phase2 + deprecated SNS note |
| `db_service.py`, tests, scripts | Legitimate use of `access_token` for Phase2/E2E | **Keep** — backend/E2E only, not Phase1 face |

## File-by-file

### `fox_quiz/fox_quiz.py`

- **Reason:** Quiz `generate_result` mixed **login requirement**, **env MOCK hints**, and **`[同步失敗]`** with PostgREST text into `result_preview`.
- **Behavior (before):** User saw API/sync failure framing even when local vector math succeeded.
- **Change:** **Remove / hide** API shame strings; always present fox + Phase1 path; cloud upsert failure = soft footnote only.

### `fox_quiz/login_page.py`

- **Reason:** Subtitle explicitly described Supabase + token persistence.
- **Behavior (before):** Implied backend plumbing is the product.
- **Change:** **Hide** vendor/token wording; generic account messaging. Profile ensure failures: generic message (no RLS essay in UI).

### `fox_quiz/story_page.py`

- **Reason:** Onboarding text referenced JWT, paths with `user_id`, Storage RLS; status used "同步 profiles" and Storage failures.
- **Behavior (before):** Reads as infra debugging.
- **Change:** **Remove / hide** from visible UI; errors generic.

### `fox_quiz/chat_component.py`

- **Reason:** System bubble mentioned `access_token` and `MOCK_LOGIN_USER_ID`.
- **Behavior (before):** Developer onboarding leak.
- **Change:** **Remove** literal token/env strings from UI.

### `fox_quiz/match_wall.py`

- **Reason:** `error_msg = f"…{e}"` could surface backend vocabulary.
- **Behavior (before):** Risk of confusing Phase1 user.
- **Change:** **Hide** exception text in banner; generic retry message.

### `fox_quiz/session_state.py`

- **Reason:** Top-level doc said "Supabase" + "手動貼 Token".
- **Change:** **Rephrase** docs; fields **kept** (still required for `/login`, `/match`, `/story` when cloud paths run). **Phase-later:** true SNS OAuth fields would live in a dedicated Phase3 module, not Reflex session naming.

### `fox_quiz/ui/insight_panel.py`, `fox_quiz/ui/profile_page.py`

- **Reason:** Audited for token/sync strings.
- **Behavior:** No user-facing access_token/oauth/sync-failed copy found.
- **Change:** None required.

### `db_service.py`, `tests/*`, `seed_test_users.py`, `README.md`

- **Reason:** Technical use of tokens and user id resolution.
- **Behavior:** Correct for Phase2/backend.
- **Change:** **Keep**; not shown in Phase1 primary UI after this hotfix.

### Product docs (`ops/product/*`, `BACKLOG.md`)

- **Reason:** Roadmap mentions SNS / social graph as **future** north star.
- **Behavior:** Strategic docs, not runtime UI.
- **Change:** **Phase-later** language remains; **no** requirement to delete roadmap. **Rule:** Do not surface this language inside Phase1 pages (see `ops/product/PHASE_BOUNDARY_SYSTEM.md`).

## Forbidden patterns (Phase1 UI)

- Python numeric compares on reactive foreach items (separate hotfix) — N/A here.
- User-visible: `access_token`, `OAuth`, `sync failed` / `同步失敗`, `graph api`, `social graph`, `paste token`, `MOCK_LOGIN`, `JWT` (in onboarding), `user_id/` path tutorials, raw Storage/RLS errors.

## Safe patterns

- Local-first copy: profile → questionnaire → target → insight → match reasoning.
- Errors: short, actionable, no vendor dump.
- Phase2/3 details: `docs/deprecated/future_sns_layer/` and product roadmap docs only.
