# DEAD COMPONENT AUDIT — PHASE1-H3

**Date:** 2026-05-16 · **Authority:** [`../product/ACTIVE_SURFACE_MAP.md`](../product/ACTIVE_SURFACE_MAP.md)

---

## Removed from `fox_quiz/ui/components/`

| Component | Reason |
|-----------|--------|
| `hero_insight.py` | Legacy guardian hero / compatibility index |
| `insight_cards.py` | Duplicate insight stack |
| `signal_scan_banner.py` | Guardian scan immersion (pre–signal-first) |
| `compatibility_meter.py` | Dating-score-style meter |
| `signal_guard_card.py` | Standalone guard card (insight uses inline sections) |
| `session_history.py` | Unused UI list (history via `AppState` only) |
| `fox_message_card.py` | Unused fox card stack |
| `fox_avatar.py` | Unused avatar widget (chat route removed) |

**Reference copies:** `docs/archive/dead_components_reference/`

---

## Active retained components

| Component | Used by |
|-----------|---------|
| `world_container.py` | Home, profile, target, insight shell |
| `floating_snow.py` | `world_container` |
| `warning_signal_chip.py` | (support; may be used by archived guard card tests) |

**Active insight UX:** `fox_quiz/ui/insight_panel.py` — pressure, weakness, fit, avoid, single fox observer.

---

## Active pages (not components)

- `home_page.py`, `profile_page.py`, `target_page.py`, `app_page.py`, `match_wall.py`, `login_page.py`, `nav_bar.py`

---

## Engine note

`product/guard/runtime/signal_guard_engine.py` remains **runtime** for `AppState` risk merge — not a second UX surface.
