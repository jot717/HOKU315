# ACTIVE SURFACE MAP - Phase 1

**Physical law for routes, docs, state, UI, and tests.**

Authority: [`PRODUCT_MASTER.md`](PRODUCT_MASTER.md) · [`AI_DEVELOPMENT_CONSTITUTION.md`](AI_DEVELOPMENT_CONSTITUTION.md)

---

## Active routes

| Route | Purpose |
|-------|---------|
| `/` | Home |
| `/profile` | Signal profile |
| `/quiz` | Questionnaire |
| `/target` | Target observation |
| `/insight` | Interaction analysis |
| `/match` | Match wall |
| `/login` | Account utility |

All other routes: deprecated (see `docs/archive/legacy/DEAD_ROUTE_AUDIT.md`).

---

## Active product docs

Only files in `docs/active/product/` (8 SSOT files). See [`README.md`](README.md).

---

## Active UX flow

`/profile` -> `/quiz` -> `/target` -> `/insight` -> `/match`

---

## Active state systems

`AppState`, `ProfileState`, `TargetState`, `MatchWallState`, `SessionState`, `QuizState`

**Persistence (Phase 2-A):** `product/persistence/runtime/` — all `runtime_state/` JSON via `LocalJsonBackend`

---

## Active UI surfaces

profile setup, signal quiz, target observation, insight analysis, match credibility, fox observer (one block on insight)

---

## Active test categories

governance, runtime, flow, compile, signal, match, insight

See [`../testing/README_TEST_STRUCTURE.md`](../testing/README_TEST_STRUCTURE.md).
