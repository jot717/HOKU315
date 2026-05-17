# ROADMAP — Canonical Product Phases (PHASE1–PHASE7)

**Authority:** [`PRODUCT_MASTER.md`](PRODUCT_MASTER.md) owns identity and user flow. **This file** owns phase boundaries, mission, scope, and non-goals.

**Planning index:** [`../governance/MASTER_BACKLOG.md`](../governance/MASTER_BACKLOG.md)  
**SSOT chain:** [`../governance/SSOT_HIERARCHY.md`](../governance/SSOT_HIERARCHY.md)

---

## Phase authority hierarchy

| Layer | Owner | Role |
|-------|--------|------|
| Product identity & flow | `PRODUCT_MASTER.md` | What HOKU315 is; official routes |
| Phase boundaries | **`ROADMAP.md` (this file)** | PHASE1–PHASE7 mission / scope / non-goals |
| Domain systems | `SIGNAL_SYSTEM.md`, `MATCH_SYSTEM.md` | Signal and match law within active phase |
| Sprint index | `MASTER_BACKLOG.md` | ACTIVE / COMPLETED rows; links to archive slices |
| Engineering P0/P1 | Root `BACKLOG.md` | Stabilization tasks only — not product phase law |
| Execution boot | `START_NEW_SPRINT.md` | Mandatory AI load order before any sprint |

**Forbidden:** Inferring phases from `docs/archive/product/FOX_ROADMAP.md`, `PHASE_BOUNDARY_SYSTEM.md`, or any archived roadmap. Archive is historical narrative only.

---

## Naming: product phase vs governance sprint

| Term | Meaning | Example |
|------|---------|---------|
| **PHASE1–PHASE7** | Product delivery phases (this file) | PHASE2 = persistence |
| **PHASE1-H*** | Governance / stabilization sprints inside Phase 1 face | PHASE1-H6 = AI discipline |

Do not treat `PHASE1-H6` as product PHASE6.

---

## PHASE1 — Local signal intelligence (CURRENT FACE)

**Status:** ACTIVE (face shipped; H-sprints continue stabilization)

**Mission:** Rule-based social signal and interaction-energy analysis on device. One canonical user journey.

**Scope:**

- Routes: `/` → `/profile` → `/quiz` → `/target` → `/insight` → `/match`
- Guest + optional account (local JSON); login as utility only
- Fox observer block on `/insight` only
- Engines: `ux_intelligence_engine`, `match_rhythm_engine`, local `runtime_state/`

**Non-goals:**

- Cloud persistence as product headline
- SNS OAuth, graph import, or “connect Facebook” copy
- Therapy / dating-score / MBTI-as-identity positioning
- PHASE2+ capabilities in default UX

**Authority:** Implement only what `PRODUCT_MASTER.md` + Phase 1 systems allow.

---

## PHASE2 — Persistence & memory

**Status:** ACTIVE (foundation in progress)

**Mission:** Longitudinal memory, account-backed profiles, cross-device continuity.

**Scope:**

- Durable profile / target / session history
- Auth and backup as **utility**, not new product identity
- Migration from local JSON templates

**Non-goals:**

- SNS surfaces or external graph UI
- Replacing Phase 1 rule engines with ML inference
- Second onboarding flow

### PHASE2-A — Persistence foundation v1

**Status:** COMPLETED

**Mission:** One persistence port over existing `runtime_state/` JSON; no UX or cloud headline changes.

**Scope:**

- `product/persistence/runtime/` — entity keys, `PersistenceBackend`, `LocalJsonBackend`, `get_backend()`
- All runtime stores route through backend (`profile`, `target`, `fox_memory`, `session_history`, `local_session`)
- Env: `HOKU_PERSISTENCE_BACKEND=local` (default; only supported value in 2-A)

**Non-goals:**

- Supabase / cloud adapter (PHASE2-B+)
- Login or account UX changes
- New routes or Phase 1 copy changes
- SNS or graph persistence

**Code SSOT:** `product/persistence/runtime/entities.py` · Schema: [`../env/RUNTIME_STATE_SCHEMA.md`](../env/RUNTIME_STATE_SCHEMA.md)

---

## PHASE3 — SNS import

**Status:** FUTURE

**Mission:** Consent-based connection to user-chosen external surfaces.

**Scope:**

- Opt-in ingestion pipelines (policy-bound)
- External signal adapters behind explicit user action

**Non-goals:**

- Default-connected accounts in Phase 1/2 routes
- Graph-wide scraping without consent
- Product rebrand to “social network app”

---

## PHASE4 — Social graph intelligence

**Status:** FUTURE

**Mission:** Graph-aware guardian signals across opted-in network.

**Scope:**

- Relationship graph as signal input (not dating graph)
- Network-level drain / pressure patterns

**Non-goals:**

- Public social feed or messaging product
- Compatibility-percent leaderboard

---

## PHASE5 — AI-scale inference

**Status:** FUTURE

**Mission:** Scalable inference **after** signal ontology and energy model are stable in Phases 1–4.

**Scope:**

- Model-served inference behind existing signal contracts
- Performance and cost controls at product boundary

**Non-goals:**

- Phase 1 copy promising “AI companion” or open-ended chat SKU
- Bypassing `SIGNAL_SYSTEM.md` / `MATCH_SYSTEM.md` contracts

---

## PHASE6 — Guardian automation & trust

**Status:** FUTURE

**Mission:** Proactive guardian operations—timely re-analysis, alerts, and trust surfaces—without changing core identity.

**Scope:**

- Scheduled / event-driven re-evaluation of signal state
- User-visible alert and trust UX (still signal-first)
- Audit-friendly product behavior documentation

**Non-goals:**

- Autonomous agent that replaces user judgment
- New primary routes that bypass `/profile` → `/match` chain
- Compliance/legal SSOT (belongs in governance/env, not product identity)

---

## PHASE7 — Platform & ecosystem

**Status:** FUTURE

**Mission:** Controlled extensibility for partners and platform consumers.

**Scope:**

- Versioned public APIs for signal outputs (read-only by default)
- Partner adapter contracts aligned with Phase 3–5 boundaries

**Non-goals:**

- Open marketplace of unreviewed third-party “personalities”
- Second product identity or white-label fork inside repo
- Parallel roadmap or constitution files

---

## Canonical flow: roadmap → planning → execution

```
ROADMAP.md (phase law)
    → MASTER_BACKLOG.md (ACTIVE row + optional backlog/archive slice)
        → backlog/archive/BACKLOG_<slug>_v1.md + SPRINT_<slug>_v1.md
            → IMPLEMENT (code + docs/active only)
                → REGRESSION (tests/regression/)
                    → UAT (docs/active/uat/)
                        → DONE (MASTER_BACKLOG COMPLETED + SPRINT_LOG)
                            → ARCHIVE (docs/archive/, backlog/archive/)
```

Never skip a step. Never plan from archive.

---

## Archive rule (phases)

| Source | Use |
|--------|-----|
| `docs/active/product/ROADMAP.md` | **Only** canonical phase definitions |
| `docs/archive/product/FOX_ROADMAP.md` | Historical; do not extend or cite as law |
| `docs/archive/product/PHASE_BOUNDARY_SYSTEM.md` | Superseded by this file |

When archive and active disagree, **active wins**.
