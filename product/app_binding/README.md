# APP FLOW BINDING v1

## PURPOSE

Bridge FLOW INTEGRATION runtime
into future fox_quiz UI/state layer.

---

## CURRENT STATUS

SAFE MODE:

- local state binding
- runtime orchestration
- local persistence
- `runtime/flow_binding.execute_bound_flow` → orchestrator + `persist_session`

PARTIAL:

- demo UI at `/insight` (`fox_quiz/ui`, `fox_quiz/state/app_state.py`)

NOT YET:

- Production wiring from match_wall / real profiles
- live authenticated session binding

---

## MODULES

- `runtime/persistence.py`
- `runtime/flow_binding.py`

---

## RESPONSIBILITIES

- runtime state synchronization
- session persistence
- integration preparation
