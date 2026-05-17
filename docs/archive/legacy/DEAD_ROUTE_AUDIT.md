# DEAD ROUTE AUDIT — PHASE1-H3

**Date:** 2026-05-16 · **Authority:** [`../product/ACTIVE_SURFACE_MAP.md`](../product/ACTIVE_SURFACE_MAP.md)

---

## Removed from app registration

| Route | Module | Reason |
|-------|--------|--------|
| `/chat` | `chat_component.py` | LLM chat room — not Phase 1 surface |
| `/story` | `story_page.py` | Story upload / cloud narrative — Phase 2+ |
| `/unlocks` | `unlocks_page.py` | Unlock / monetization progression — not Phase 1 |

**Preserved reference copies:** `docs/archive/dead_routes/`

---

## Active routes (unchanged)

`/`, `/profile`, `/quiz`, `/target`, `/insight`, `/match`, `/login`

---

## Redirect / compatibility changes

| Before | After |
|--------|-------|
| Login → `/story` when no custom vector | Login → `/profile` |
| Nav linked story/unlocks (historical) | Nav: core loop + login only |

---

## Internal-only (no public route)

| Item | Notes |
|------|-------|
| `SessionState.guard_protected_routes` | Still used by `/match` on_load |
| Cloud `db_service` | Account paths only; not marketed in Phase 1 face |

---

## Regression impact

- `test_remove_premature_sns_layer_v1.py` — reads archived `story_page` reference
- `test_core_flows.py` — HTTP smoke for dead routes removed when `REGRESSION_HTTP=1`
