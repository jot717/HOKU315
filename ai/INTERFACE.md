# AI ENGINEERING LAYER INTERFACE

## Entry Points

- **INCIDENT**:
  - **`scripts/collect_runtime.py`**
  - **purpose**: capture runtime failure data

- **REPLAY**:
  - **`ai/replay/replay_incident.py`** (or root `replay/` shim)
  - **purpose**: reproduce incident (mock / offline)

- **DIAGNOSE**:
  - **`ai/diagnosis/root_cause_engine.py`**
  - **purpose**: classify error type

- **SUGGEST**:
  - **`ai/suggestion/suggest_engine.py`**
  - **purpose**: propose fix strategy

- **SELF-HEAL**:
  - **`ai/self_heal/*`**
  - **purpose**: controlled patch generation + regression check

## RULE

AI layer **must NOT** depend on product business logic or UI implementation.

See also [`REPO_ARCHITECTURE.md`](../REPO_ARCHITECTURE.md), [`ARCHITECTURE_CONTRACT.md`](../ARCHITECTURE_CONTRACT.md).
