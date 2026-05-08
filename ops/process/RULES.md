# PROCESS ENFORCEMENT RULES v1

Workflow guardrails for AI-native development. See [`ARCHITECTURE_CONTRACT.md`](../../ARCHITECTURE_CONTRACT.md), [`BACKLOG.md`](../../BACKLOG.md), [`SPRINT_LOG.md`](../../SPRINT_LOG.md).

---

## RULE 1 — BACKLOG FIRST

No feature can be implemented without a **BACKLOG** entry.

Suggested item shape: [`backlog_template.md`](backlog_template.md)

- id  
- goal  
- scope  
- dependency  
- status: planned  

---

## RULE 2 — SPRINT REQUIRED

No BACKLOG item should be **executed as planned work** without being tied to a **sprint** (e.g. [`SPRINT_PLAN.md`](../../SPRINT_PLAN.md) / sprint section in log).

Sprint shape: [`sprint_template.md`](sprint_template.md)

- sprint id  
- goal  
- tasks  
- done / blockers  

---

## RULE 3 — REGRESSION GATE

No feature is considered **DONE** unless:

```text
pytest tests/regression/
```

passes (see **REGRESSION GATE** in [`BACKLOG.md`](../../BACKLOG.md); wrapper `python scripts/run_regression.py`).

---

## RULE 4 — LOG EVERYTHING

Every sprint should update **[`SPRINT_LOG.md`](../../SPRINT_LOG.md)** (DONE / BLOCKER / NEXT).

---

## RULE 5 — NO DIRECT FEATURE COMMIT

All work should **map** to:

```text
BACKLOG → SPRINT → IMPLEMENT → TEST → LOG
```

---

## Light checks

From repo root:

```powershell
python ops/hooks/check_process.py
```

Regression gate (same as CI intent):

```powershell
python scripts/run_regression.py
```

On Unix / Git Bash: [`ops/hooks/check_regression.sh`](../hooks/check_regression.sh)
