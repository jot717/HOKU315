# BACKLOG — SIGNAL INTELLIGENCE ENGINE v1

## STATUS

ACTIVE

## TYPE

RULE-BASED SIGNAL INTELLIGENCE (first intelligence layer; **no** LLM / embeddings / vector search / agents)

## GOAL

Interpret **human danger patterns** from existing profile + mine vector + memory + bound-flow signals; drive guardian priority (HIGH/MEDIUM/LOW) and short explanations; tag fox memory when risks repeat.

## DELIVERABLES

* [`ops/product/SIGNAL_INTELLIGENCE_CONSTITUTION.md`](../ops/product/SIGNAL_INTELLIGENCE_CONSTITUTION.md)
* [`ops/product/SIGNAL_RISK_ONTOLOGY.md`](../ops/product/SIGNAL_RISK_ONTOLOGY.md)
* [`ops/product/SIGNAL_INFERENCE_MODEL.md`](../ops/product/SIGNAL_INFERENCE_MODEL.md)
* [`product/signal/runtime/signal_inference_engine.py`](../product/signal/runtime/signal_inference_engine.py) — `infer_signal_risks`, `collect_signal_profile_for_inference`
* [`product/memory/runtime/fox_memory_engine.py`](../product/memory/runtime/fox_memory_engine.py) — `apply_inference_memory_tags`
* Guardian insight integration (`fox_quiz/state/app_state.py`, `fox_quiz/ui/insight_panel.py`)
* [`ops/uat/SIGNAL_INTELLIGENCE_ENGINE_UAT.md`](../ops/uat/SIGNAL_INTELLIGENCE_ENGINE_UAT.md)
* Regression: `tests/regression/test_signal_intelligence_engine_v1.py`

## NON-GOALS

Embeddings, SNS APIs, Supabase schema changes, auth, social graph implementation, LLM reasoning.

## SPRINT

[`SPRINT_SIGNAL_INTELLIGENCE_ENGINE_v1.md`](SPRINT_SIGNAL_INTELLIGENCE_ENGINE_v1.md)
