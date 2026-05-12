# SOCIAL SIGNAL ARCHITECTURE (v1)

**STATUS:** Conceptual / future-facing only  
**SCOPE:** Architecture definition — **no implementation commitment** in this document

This describes how an **AI-native SNS guardian network** could ingest, process, and emit protections. Existing shipped systems may only implement a subset (e.g. manual onboarding + local rules); this file is the **north-star map**.

---

## SIGNAL INPUT LAYERS

### 1. Manual onboarding (current / near-term)

* Profile fields (identity, preferences, stress baselines)
* Structured questions and self-reported interests
* Stress patterns and capacity signals (non-clinical, user-declared)

### 2. SNS ingestion (future)

Planned categories of **external signal** (subject to product, legal, and platform policy):

* Instagram
* X (Twitter)
* TikTok
* Threads
* Discord
* LINE
* Contacts and address-book metadata (opt-in)
* Social metadata (followers, blocks, mutes, frequency — as permitted)

Ingestion must remain **user-consented**, **minimally necessary**, and **policy-compliant** per region and platform.

### 3. Interaction patterns (future)

Signals derived from **how** people interact, not only **what** they post:

* Reply speed asymmetry and ghosting patterns
* Passive aggression and indirect hostility
* Emotional drain and one-sided labor in threads
* Attention farming and baiting
* Hater behavior clusters (pile-ons, brigading tone)
* Manipulation loops (gaslight-adjacent rhythms, DARVO-like cycles in public text — conceptual labels only)

---

## SIGNAL PROCESSING (future)

Not implemented by this sprint; intended capabilities:

* Embeddings and semantic similarity over social text and metadata
* Vector memory for longitudinal “same actor, same harm shape” recall
* Relationship scoring (risk of harm / drain, not “romantic fit”)
* Social clustering (circles, cohorts, safe vs high-friction zones)
* Hater ranking and explainable flags for user review
* Dangerous signal detection with human-readable guardian outputs
* Long-term behavioral tracking with decay and user control

---

## OUTPUT (USER-FACING)

Users ultimately receive:

* **Guardian warnings** — what might hurt or drain them soon
* **Danger probability** — calibrated language, not pseudo-science “accuracy”
* **Safe-circle recommendations** — who to lean on, mute, or distance (user agency first)
* **Interaction alerts** — spikes in negativity, pressure, or manipulation-shaped rhythm
* **Emotional exhaustion prevention** — pacing, boundaries, and “stop scrolling” class interventions

All outputs remain **assistive**; the user decides actions. The fox is the **voice** of this layer, not the sole decision maker.
