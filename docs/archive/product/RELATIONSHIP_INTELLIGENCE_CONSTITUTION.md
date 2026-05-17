# RELATIONSHIP INTELLIGENCE CONSTITUTION (v1)

**STATUS:** ACTIVE  
**TYPE:** Relationship / **interaction** intelligence foundation — **synthetic** archetypes only (no real SNS, no multi-user graph in this sprint)

This complements [`SIGNAL_INTELLIGENCE_CONSTITUTION.md`](SIGNAL_INTELLIGENCE_CONSTITUTION.md) but shifts the lens from **solo signal** to **interaction-shaped risk**.

---

## CORE PURPOSE

The system exists to:

* detect **dangerous interaction styles** (patterns of behavior in exchanges, not moral labels on people)
* **simulate** social risk exposure using **archetypes** + user signal overlap
* identify **emotional exhaustion** sources that come from **how others interact**
* identify **unsafe relationship patterns** (instability, extraction, passive hostility, etc.)
* help users **avoid destructive social loops** through guardian framing

The system does **not**:

* judge humans morally as “bad people”
* classify individuals into permanent villain types
* simulate **psychology diagnosis** or clinical assessment
* produce **dating compatibility scores**

---

## CORE PRINCIPLE

The system analyzes **interaction patterns**.

It does **not** measure **human worth**.

Copy must default to: **「有些人習慣用某種節奏互動，可能會這樣耗你」** — not **「你很脆弱」**.

---

## IMPLEMENTATION GUARDRAILS (v1)

* **Rule-based** archetypes in [`product/signal/runtime/relationship_simulation_engine.py`](../../product/signal/runtime/relationship_simulation_engine.py)
* Overlap with user `risk_scores` from [`infer_signal_risks`](../../product/signal/runtime/signal_inference_engine.py) — transparent, tunable thresholds
* **Fox memory** may record recurring **interaction-pattern tags** (not real identities)

---

## RELATED DOCS

* [`RELATIONSHIP_ARCHETYPE_MODEL.md`](RELATIONSHIP_ARCHETYPE_MODEL.md)  
* [`INTERACTION_SIGNAL_ONTOLOGY.md`](INTERACTION_SIGNAL_ONTOLOGY.md)  
* [`docs/active/uat/RELATIONSHIP_SIGNAL_SIMULATION_UAT.md`](../uat/RELATIONSHIP_SIGNAL_SIMULATION_UAT.md)
