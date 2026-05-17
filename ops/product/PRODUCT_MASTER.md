# PRODUCT MASTER — Single Source of Truth

**All product, UAT, and backlog docs must reference this file.**  
Governance: [`REPO_GOVERNANCE_RULES.md`](REPO_GOVERNANCE_RULES.md) · Backlog index: [`../../backlog/MASTER_BACKLOG.md`](../../backlog/MASTER_BACKLOG.md) · UAT index: [`../uat/UAT_MASTER_GUIDE.md`](../uat/UAT_MASTER_GUIDE.md)

---

## What HOKU315 is

An **AI-native social signal analysis** product that helps users understand:

- **How social interactions drain energy** (rhythm, reply pressure, emotional pacing)
- **Which interaction shapes to avoid** (rule-based pressure patterns)
- **Which peer rhythms are lighter** for their current signal profile (social energy compatibility)

**Core model:** [`SOCIAL_ENERGY_MODEL.md`](SOCIAL_ENERGY_MODEL.md) · **Match archetypes:** [`MATCH_ARCHETYPE_SYSTEM.md`](MATCH_ARCHETYPE_SYSTEM.md)

---

## What HOKU315 is NOT

- Not a dating app or “compatibility score” SKU
- Not personality typing (MBTI, attachment labels as identity)
- Not therapy, healing, or clinical diagnosis
- Not astrology or fate-based matching
- Not SNS-connected in **Phase 1 face** (no OAuth/graph copy in primary UX)

---

## Core product loop (Phase 1)

| Step | Route | Purpose |
|------|-------|---------|
| 1 | `/profile` | Local signal profile (name, interests, stress) |
| 2 | `/quiz` | 20-dimension sensitivity vector |
| 3 | `/target` | Named observation target (local JSON) |
| 4 | `/insight` | Rule-based interaction pressure + rhythm analysis |
| 5 | `/match` | Social energy compatibility cards (when account + data) |

Detail: [`PHASE1_PRODUCT_FLOW.md`](PHASE1_PRODUCT_FLOW.md) · Pages: [`PAGE_PURPOSE_SYSTEM.md`](PAGE_PURPOSE_SYSTEM.md)

---

## Guest vs account

| Mode | Who | Persistence | Product promise |
|------|-----|-------------|-----------------|
| **Guest（訪客）** | No login | Local JSON / session on device; **no** cross-device guarantee | “Analyze my signals now” |
| **Account（帳號）** | Email login | Cloud profile, vector, stories, match wall; longitudinal memory | “Save trends across time” |

Phase boundary: [`PHASE_BOUNDARY_SYSTEM.md`](PHASE_BOUNDARY_SYSTEM.md)  
Future SNS: [`../../docs/deprecated/future_sns_layer/README.md`](../../docs/deprecated/future_sns_layer/README.md)

**UI entry:** `/` explains both modes; `/login` is optional utility, not the product story.

---

## Fox role

- **Observer** — names interaction shape and pacing (max **one** block per insight page)
- **Not** therapist, life coach, emotional healer, or mascot spam

Constitutions: [`UX_INTELLIGENCE_CONSTITUTION.md`](UX_INTELLIGENCE_CONSTITUTION.md) · [`MATCH_CREDIBILITY_CONSTITUTION.md`](MATCH_CREDIBILITY_CONSTITUTION.md) · [`SOCIAL_CAUSALITY_RULES.md`](SOCIAL_CAUSALITY_RULES.md)

---

## Signal system (rule-based)

| Layer | Doc | Code |
|-------|-----|------|
| Constitution | [`SIGNAL_SYSTEM_CONSTITUTION.md`](SIGNAL_SYSTEM_CONSTITUTION.md) | — |
| Profile schema | [`SIGNAL_PROFILE_SCHEMA.md`](SIGNAL_PROFILE_SCHEMA.md) | `product/profile/` |
| Flow | [`SIGNAL_FLOW_ARCHITECTURE.md`](SIGNAL_FLOW_ARCHITECTURE.md) | `product/app_binding/` |
| Inference | [`SIGNAL_INTELLIGENCE_CONSTITUTION.md`](SIGNAL_INTELLIGENCE_CONSTITUTION.md) | `signal_inference_engine.py` |
| Pressure ontology | [`INTERACTION_PRESSURE_ONTOLOGY.md`](INTERACTION_PRESSURE_ONTOLOGY.md) | `ux_intelligence_engine.py` |
| Target | [`TARGET_SIGNAL_CONSTITUTION.md`](TARGET_SIGNAL_CONSTITUTION.md) | `product/target/` |
| Relationship sim | [`RELATIONSHIP_INTELLIGENCE_CONSTITUTION.md`](RELATIONSHIP_INTELLIGENCE_CONSTITUTION.md) | `relationship_simulation_engine.py` |

---

## Social energy & match credibility

- Energy model: [`SOCIAL_ENERGY_MODEL.md`](SOCIAL_ENERGY_MODEL.md)
- Match rhythm engine: `product/match/runtime/match_rhythm_engine.py`
- UX intelligence: `product/signal/runtime/ux_intelligence_engine.py`

---

## Phase boundaries

| Phase | User-facing scope |
|-------|-------------------|
| **1** | Local signal + questionnaire + target + rule insight + energy-oriented match copy |
| **2** | Account persistence, cross-device backup (utility framing) |
| **3** | SNS import, external graph, interaction ingestion (gated; not in Phase 1 UI) |

Full rules: [`PHASE_BOUNDARY_SYSTEM.md`](PHASE_BOUNDARY_SYSTEM.md)

---

## Roadmap & direction

- North star: [`CORE_PRODUCT_REALIGNMENT.md`](CORE_PRODUCT_REALIGNMENT.md) · [`SOCIAL_SIGNAL_ARCHITECTURE.md`](SOCIAL_SIGNAL_ARCHITECTURE.md)
- Phased delivery: [`FOX_ROADMAP.md`](FOX_ROADMAP.md)
- Positioning: [`SIGNAL_FIRST_PRODUCT_POSITION.md`](SIGNAL_FIRST_PRODUCT_POSITION.md)

---

## Memory model

- Fox memory store: `product/memory/runtime/fox_memory_store.py`
- Session history: `product/session/runtime/session_history.py`
- Local runtime state: `runtime_state/` (see `ops/env/RUNTIME_STATE_SCHEMA.md`)

---

## Engineering constitution

- Root: [`../../DEVELOPMENT_CONSTITUTION.md`](../../DEVELOPMENT_CONSTITUTION.md)
- Architecture: [`../../ARCHITECTURE_CONTRACT.md`](../../ARCHITECTURE_CONTRACT.md)
- Environment: [`../env/STARTUP_GUIDE.md`](../env/STARTUP_GUIDE.md)

---

## Document index

See [`README.md`](README.md) for active vs archived product docs.
