# SIGNAL INFERENCE MODEL (v1)

**STATUS:** Human-readable **correlation rules** only (implemented as Python conditionals).  
**NOT:** ML, embeddings, vector DB, LLM chains.

Rules consume the bundle from `collect_signal_profile_for_inference()`:

* `profile` — `activity` (1–10 stress proxy), `interests`, `name`
* `mine_vector` — 20-D clamped values aligned to [`fox_logic.SOCIAL_MINE_DIMENSIONS`](../../fox_logic.py)
* `memory` — `recent_patterns`, `recent_warnings`
* `insight_state` — optional English `activity_analysis` string for tension cue
* `match_score` — optional demo bound-flow score (low → extra exhaustion nudge)

---

## RULE EXAMPLES (DOCUMENTARY)

### IF high social fatigue + high response anxiety → attention_drain_risk ↑

* **Operationalization:** `activity/10` elevated **and** high `reply_latency_anxiety` + `dm_pace_sensitivity` in mine vector.
* **Output:** bumps `attention_drain_risk`, surfaces guardian line about刷新/訊息流.

### IF avoids confrontation + sensitive to passive aggression → silent pressure vulnerability ↑

* **Operationalization:** `emotional_tone_deaf`, `silence_discomfort`, `backhanded_praise` combination.
* **Output:** bumps `passive_aggression_risk` / `manipulation_sensitivity`.

### IF fears exclusion + overthinks replies → ghosting_sensitivity ↑

* **Operationalization:** `reply_latency_anxiety` + `dm_pace_sensitivity` with moderate `activity`.
* **Output:** bumps `ghosting_sensitivity`, ghosting-specific guardian hint.

Additional combinations (life-stage comparison + humblebrag → `social_comparison_risk` / `approval_dependency_risk`; group stress + interruption → `overexposure_risk`; boundary + cling → `unstable_relationship_risk`) are implemented alongside these exemplars.

---

## PRIORITY MODEL

After per-type scores in `[0,1]`:

* **HIGH** — top score ≥ 0.72 **or** three or more types ≥ 0.55  
* **MEDIUM** — top ≥ 0.48 **or** second ≥ 0.45  
* **LOW** — otherwise  

Guardian UI merges this with legacy `evaluate_signal_risk` level via **max rank** so the user always sees the **stricter** of the two when they disagree.

---

## SOURCE OF TRUTH

Code: [`product/signal/runtime/signal_inference_engine.py`](../../product/signal/runtime/signal_inference_engine.py)  
Ontology labels: [`SIGNAL_RISK_ONTOLOGY.md`](SIGNAL_RISK_ONTOLOGY.md)
