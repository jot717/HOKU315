# FOX MEMORY SYSTEM v1

## GOAL

Give the Arctic Fox **short-term local memory** of the user’s recent observation runs—rule-based only—so the product feels more like **companionship** than a one-shot tool.

## SCOPE

* `runtime_state/fox_memory.json` persistence
* `remember_insight()` rule engine (score bands)
* guardian / diary UI (`fox_memory_card`)
* AppState fields + refresh on load / after new insight

## NON-GOALS

* embeddings, vector DB, LLM memory orchestration
* backend / flow / auth rewrites

## STATUS

ACTIVE
