# ACTIVE SURFACE MAP — Phase 1

**Physical law for routes, docs, state, UI, and tests.**  
Before adding folders, routes, or docs, check this file and extend canonical systems only.

Authority: [`PRODUCT_MASTER.md`](PRODUCT_MASTER.md) · [`AI_DEVELOPMENT_CONSTITUTION.md`](AI_DEVELOPMENT_CONSTITUTION.md)

---

## Active routes

Only these routes are official Phase 1 routes:

| Route | Purpose |
|-------|---------|
| `/` | Home — guest vs account entry |
| `/profile` | Signal profile setup |
| `/quiz` | Signal questionnaire |
| `/target` | Target observation |
| `/insight` | Interaction pressure analysis |
| `/match` | Social energy match wall |
| `/login` | Account utility (optional) |

**All other routes are deprecated or internal-only** (see `ops/uat/DEAD_ROUTE_AUDIT.md`).

---

## Active product docs

Only these files are authoritative for product identity:

| File | Role |
|------|------|
| [`PRODUCT_MASTER.md`](PRODUCT_MASTER.md) | Identity, flow, systems |
| [`SIGNAL_SYSTEM.md`](SIGNAL_SYSTEM.md) | Signal pipeline |
| [`MATCH_SYSTEM.md`](MATCH_SYSTEM.md) | Match / social energy |
| [`ROADMAP.md`](ROADMAP.md) | Phases 1–5 |
| [`AI_DEVELOPMENT_CONSTITUTION.md`](AI_DEVELOPMENT_CONSTITUTION.md) | AI implementation law |
| [`REPO_GOVERNANCE_RULES.md`](REPO_GOVERNANCE_RULES.md) | Doc locations |
| [`CANONICAL_TERMINOLOGY.md`](CANONICAL_TERMINOLOGY.md) | UX copy |
| [`ACTIVE_SURFACE_MAP.md`](ACTIVE_SURFACE_MAP.md) | This map |

Process helpers (checklist, context priority): `docs/archive/phase1_legacy/` — not product identity.

No other product doc may redefine product identity.

---

## Active UX flow

```
/profile → /quiz → /target → /insight → /match
```

Home (`/`) precedes the loop. `/login` is optional utility.

---

## Active state systems

| State | Module |
|-------|--------|
| `AppState` | `fox_quiz/state/app_state.py` |
| `ProfileState` | `fox_quiz/state/profile_state.py` |
| `TargetState` | `fox_quiz/state/target_state.py` |
| `MatchWallState` | `fox_quiz/match_wall.py` |
| `SessionState` | `fox_quiz/session_state.py` |
| `QuizState` | `fox_quiz/fox_quiz.py` (questionnaire only) |

---

## Active UI surfaces

| Surface | Location |
|---------|----------|
| Profile setup | `fox_quiz/ui/profile_page.py` |
| Signal quiz | `fox_quiz/fox_quiz.py` (`quiz_page`) |
| Target observation | `fox_quiz/ui/pages/target_page.py` |
| Insight analysis | `fox_quiz/ui/insight_panel.py` |
| Match credibility | `fox_quiz/match_wall.py` |
| Fox observer block | `insight_panel` — max one block |
| World shell | `world_container`, `floating_snow` (layout only) |

**Not active:** legacy guardian stacks, story-first onboarding, unlock progression UX, dead components (see `ops/uat/DEAD_COMPONENT_AUDIT.md`).

---

## Active test categories

| Category | Location |
|----------|----------|
| governance | `tests/regression/test_phase1*h*` |
| flow | `tests/regression/test_*flow*` |
| runtime | `tests/regression/test_*engine*` |
| compile | `tests/regression/test_*compile*` |
| signal | `tests/regression/test_signal*` |
| match | `tests/regression/test_*match*` |
| insight | `tests/regression/test_*insight*`, phase1d |

Future layout: `tests/README_TEST_STRUCTURE.md`
