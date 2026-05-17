# SIGNAL INTELLIGENCE CONSTITUTION (v1)

**STATUS:** ACTIVE  
**TYPE:** Rule-based signal intelligence — **first real intelligence layer** in this repo (no LLM, embeddings, vector search, or agents in this sprint)

This document binds **how** the engine may reason: **combinations of signals**, transparent rules, and guardian-safe outputs.

---

## CORE PURPOSE

The engine exists to:

* detect **dangerous interaction patterns** (as assistive signals, not clinical facts)
* identify **emotional exhaustion risk** from pace and exposure proxies
* identify **hater-sensitive** or **pile-on–sensitive** environments from mine-vector + profile stress
* detect **manipulation pressure** (ambiguity, plausible deniability, baiting rhythms — rule sketches)
* detect **attention-drain risk** (reply anxiety + DM pace + notification load proxies)
* help **guardian systems explain danger** in short, human language

The engine does **not**:

* diagnose psychology or medical conditions
* evaluate personality as a “type”
* simulate therapy or replace professional care
* generate mystical or opaque “AI knowing you” prose

---

## INTELLIGENCE PRINCIPLE

The engine interprets **signal combinations** (profile stress, 20-D mine vector bands, optional match/insight text, memory tags).

It does **not** treat **single isolated answers** as destiny: thresholds fire only when **multiple** inputs align (see [`SIGNAL_INFERENCE_MODEL.md`](SIGNAL_INFERENCE_MODEL.md)).

---

## EXAMPLES (CONCEPT → RULE SHAPE)

| Combination (conceptual) | Inferred pressure |
|--------------------------|-------------------|
| High social fatigue (activity) + high fear of exclusion (reply/DM mines) | **attention_drain_risk** ↑ |
| Avoids confrontation (silence / tone mines) + hates passive aggression (backhand / tone) | **passive_aggression_risk** / **silent pressure** sensitivity ↑ |
| Fears exclusion (reply anxiety) + overthinks replies (DM pace) | **ghosting_sensitivity** ↑ |

Exact thresholds live in [`product/signal/runtime/signal_inference_engine.py`](../../product/signal/runtime/signal_inference_engine.py) and may be tuned in SAFE MODE.

---

## OUTPUT CONTRACT

Downstream guardian UI must:

* show **highest danger first** (priority HIGH / MEDIUM / LOW)
* keep copy **short** and **actionable**
* never imply **therapy** or **psychological scoring**

Cross-read: [`SIGNAL_RISK_ONTOLOGY.md`](SIGNAL_RISK_ONTOLOGY.md), [`SIGNAL_SYSTEM_CONSTITUTION.md`](SIGNAL_SYSTEM_CONSTITUTION.md).
