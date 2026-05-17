# EXECUTION GATE v1

Companion to [`../process/RULES.md`](../process/RULES.md). This layer states **what “valid” means** for a feature moving through the lifecycle; lightweight scripts live in this directory.

---

## PURPOSE

Force all product development to follow an explicit lifecycle before work is treated as **valid / mergeable**.

---

## RULE

**No feature can move forward** (as “ready to ship” or “definitionally complete”) unless:

```text
BACKLOG → SPRINT → IMPLEMENT → REGRESSION → DONE
```

- **BACKLOG**: spec file under `backlog/BACKLOG_<FEATURE>.md` (or equivalent traceability in root `BACKLOG.md`).
- **SPRINT**: sprint spec under `backlog/SPRINT_<FEATURE>.md` (or sprint section in `SPRINT_LOG.md` / `docs/archive/root_legacy/SPRINT_PLAN.md`).
- **IMPLEMENT**: code or integration exists in the repo (human / review judgment; not fully automatable here).
- **REGRESSION**: `pytest tests/regression/` passes (or `python scripts/run_regression.py`).
- **DONE**: recorded in [`SPRINT_LOG.md`](../../SPRINT_LOG.md) (and item closed in [`BACKLOG.md`](../../BACKLOG.md) as appropriate).

---

## VALIDATION LOGIC

| Step | Minimum signal |
|------|----------------|
| BACKLOG | `backlog/BACKLOG_<FEATURE>.md` present (when using feature-ID files) |
| SPRINT | `backlog/SPRINT_<FEATURE>.md` present |
| IMPLEMENT | Not checked by `check_flow.py` alone — requires review |
| REGRESSION | CI / local regression pass |
| DONE | Logged in `SPRINT_LOG.md` |

---

## BLOCKING RULE

If any **required** step for your team’s definition is missing, the feature is **not valid** for “done” until remediated.

---

## Scripts

```powershell
python ops/gate/check_flow.py --feature MATCH_FLOW_v1
```

Checks only **backlog + sprint file presence** for the given feature ID (convention: `backlog/BACKLOG_<FEATURE>.md`, `backlog/SPRINT_<FEATURE>.md`).
