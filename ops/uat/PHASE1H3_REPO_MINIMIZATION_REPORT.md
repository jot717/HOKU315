# PHASE1-H3 — PHYSICAL REPO MINIMIZATION REPORT

**Sprint:** Physical repo minimization v1 · **No product features**

---

## BEFORE

| Metric | State |
|--------|--------|
| Registered routes | 10 (`/`, `/quiz`, `/login`, `/chat`, `/story`, `/match`, `/unlocks`, `/insight`, `/profile`, `/target`) |
| Archive layout | Loose `docs/archive/product/`, `docs/archive/uat/`, plus `docs/deprecated/` scatter |
| Active product docs | 9–10 + governance helpers |
| Active UAT | 2 release + scattered references |
| WIP in product root | `product/shell/`, experimental `match_engine.py`, CI draft |
| `runtime_state/` | Live JSON dumps committed or present |
| Dead UI components | 8 unused widgets in `fox_quiz/ui/components/` |
| Ambiguous routes | `/story`, `/chat`, `/unlocks` still registered |

---

## AFTER

| Metric | State |
|--------|--------|
| **Active routes** | 7 — see [`ACTIVE_SURFACE_MAP.md`](../product/ACTIVE_SURFACE_MAP.md) |
| **Archive buckets** | `phase1_legacy/` (37), `old_uat/` (9), `old_hotfix/` (3); root = README only |
| **Dead route refs** | `docs/archive/dead_routes_reference/` |
| **Dead components** | `docs/archive/dead_components_reference/` |
| **WIP** | `wip/app_shell/`, `experimental_match/`, `workflow/`, `prototypes/` |
| **runtime_state** | `.gitkeep` + `templates/sample_*.json` only (tracked) |
| **Audits** | [`DEAD_ROUTE_AUDIT.md`](DEAD_ROUTE_AUDIT.md), [`DEAD_COMPONENT_AUDIT.md`](DEAD_COMPONENT_AUDIT.md) |

### Removed routes

`/chat`, `/story`, `/unlocks` — unregistered; modules archived.

### Removed / archived components

`hero_insight`, `insight_cards`, `signal_scan_banner`, `compatibility_meter`, `signal_guard_card`, `session_history`, `fox_message_card`, `fox_avatar`.

### Login redirect

No custom vector → `/profile` (was `/story`).

---

## FINAL ACTIVE PRODUCT

**HOKU315 = AI Social Signal Intelligence System**

**Core loop:**  
`profile` → `quiz` → `target` → `insight` → `match`

**Fox role:** Observer / narration layer only (one block on insight).

**Phase boundaries:**

| Phase | Scope |
|-------|--------|
| P1 | Local rule-based intelligence (current face) |
| P2 | Persistence |
| P3 | SNS import |
| P4 | Social graph |
| P5 | AI-scale inference |

---

## Validation

```bash
python ops/flow/check_all_flows.py
python -m pytest tests/regression/test_phase1h3_repo_minimization_v1.py -v --tb=short
python -m pytest tests/regression/ -v --tb=short
python ops/env/reflex_compile_gate.py
```

Use project `.venv` for full compile gate when `reflex-components-radix` is installed.
