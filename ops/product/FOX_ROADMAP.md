# FOX ROADMAP — AI-NATIVE SNS GUARDIAN PLATFORM

The **fox** is the **guardian persona and UX layer**; roadmap phases below prioritize **social signal intelligence**, **SNS-backed protection**, and **interaction risk** over standalone “insight app” positioning. Guardian world UX remains the **delivery shell** for alerts and clarity, not a substitute for the core moat.

### Rule-based signal intelligence (v1)

Shipped: `collect_signal_profile_for_inference` + `infer_signal_risks` in [`product/signal/runtime/signal_inference_engine.py`](../../product/signal/runtime/signal_inference_engine.py) — **combination rules** over profile, 20-D mine vector, memory, and bound-flow score; outputs ontology-aligned risks, **HIGH/MEDIUM/LOW** priority, and short guardian strings merged in [`fox_quiz/state/app_state.py`](../../fox_quiz/state/app_state.py). See [`SIGNAL_INTELLIGENCE_CONSTITUTION.md`](SIGNAL_INTELLIGENCE_CONSTITUTION.md).

### Relationship signal simulation (v1)

Shipped: synthetic **interaction archetypes** + overlap simulation in [`product/signal/runtime/relationship_simulation_engine.py`](../../product/signal/runtime/relationship_simulation_engine.py) — `generate_relationship_archetype` + `simulate_relationship_risk` (rule-based only); guardian copy shifts toward **interaction exhaustion** framing; optional fox-memory tags via `record_relationship_simulation_memory` in [`product/memory/runtime/fox_memory_engine.py`](../../product/memory/runtime/fox_memory_engine.py). See [`RELATIONSHIP_INTELLIGENCE_CONSTITUTION.md`](RELATIONSHIP_INTELLIGENCE_CONSTITUTION.md), [`RELATIONSHIP_ARCHETYPE_MODEL.md`](RELATIONSHIP_ARCHETYPE_MODEL.md), [`INTERACTION_SIGNAL_ONTOLOGY.md`](INTERACTION_SIGNAL_ONTOLOGY.md).

### Signal system consolidation (v1)

Phase 1 delivery is documented as **one signal architecture**: canonical **Signal Profile Setup** on **`/profile`**, optional **signal questions** on **`/quiz`** (20 sliders), **Guardian Observation** on **`/insight`**, and **signal memory** in `runtime_state/` — **no duplicate onboarding route**. See [`SIGNAL_SYSTEM_CONSTITUTION.md`](SIGNAL_SYSTEM_CONSTITUTION.md), [`SIGNAL_FLOW_ARCHITECTURE.md`](SIGNAL_FLOW_ARCHITECTURE.md), [`SIGNAL_PROFILE_SCHEMA.md`](SIGNAL_PROFILE_SCHEMA.md).

---

## PHASE 1 — Guardian UX MVP

**Goal:** Ship a credible **guardian-first** experience that can later plug in real SNS intelligence.

* Fox presence, tone, and navigation that explain **protection**, not therapy or scoring
* Profile + local / demo signal path aligned to **risk and drain** language
* Insight / observation flows that preview **interaction risk** framing (without over-claiming data the product does not yet ingest)

**Success:** Users understand **what class of product** this is (social protection + signals), not a generic AI report app.

---

## PHASE 2 — Persistent Identity + Auth + Cloud Profile

**Goal:** Durable user identity for **cross-device** and **cloud-backed** social graph work later.

* Auth, session, and cloud profile
* Consent and data-control surfaces required before SNS connect
* Foundation for syncing **dangerous interaction memory** and preferences

---

## PHASE 3 — SNS Ingestion + Signal Intelligence

**Goal:** Turn **real social inputs** (where policy allows) into structured signals.

* Opt-in connectors (per [`SOCIAL_SIGNAL_ARCHITECTURE.md`](SOCIAL_SIGNAL_ARCHITECTURE.md))
* Embeddings / vector memory for **longitudinal** patterns
* Hater-adjacent and **drain** pattern detection aligned to [`HATER_SIGNAL_MODEL.md`](HATER_SIGNAL_MODEL.md) (implementation follows policy review)

---

## PHASE 4 — Social Graph + Guardian Network

**Goal:** **Relationship- and graph-aware** protection, not single-thread chat analysis.

* Safe circles, high-friction zone awareness, repeat-actor memory
* Network-scale alerts (e.g. coordinated negativity) where product scope allows
* Community and trust primitives that support **guardian network** positioning

---

## PHASE 5 — Monetization + Premium Protection

**Goal:** Paid tiers for **deeper signal depth**, not vanity scores.

* Premium filtering, advanced alerts, priority ingestion limits
* Clear separation from “dating premium” or “compatibility unlock” framing

---

## PHASE 6 — AI Signal Scale Layer

**Goal:** Cost, latency, and safety at scale once **retention on real social value** is proven.

* Infra scaling, realtime paths, caching, vector and policy optimization
* Evaluation harnesses for **harm reduction** and false-positive management

---

## ALIGNMENT

* **North star:** [`CORE_PRODUCT_REALIGNMENT.md`](CORE_PRODUCT_REALIGNMENT.md)
* **Deprecated language:** [`DEPRECATED_PRODUCT_LANGUAGE.md`](DEPRECATED_PRODUCT_LANGUAGE.md)
* **Direction reset narrative:** [`../uat/PRODUCT_DIRECTION_RESET_NOTES.md`](../uat/PRODUCT_DIRECTION_RESET_NOTES.md)
