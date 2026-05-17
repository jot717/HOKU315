# PHASE1-H7 — SSOT HIERARCHY CONSOLIDATION REPORT

Governance-only sprint. No product features implemented.

---

## 1. SSOT hierarchy summary

```
PRODUCT_MASTER (identity + flow)
    └── ROADMAP (PHASE1–7 law)
            └── MASTER_BACKLOG (ACTIVE/COMPLETED)
                    └── backlog/archive BACKLOG + SPRINT slices
                            └── IMPLEMENT → REGRESSION → UAT → DONE → ARCHIVE
```

Boot: `START_NEW_SPRINT.md` → load `SSOT_HIERARCHY.md` before coding.

---

## 2. Authority ownership map

| Responsibility | Owner |
|----------------|--------|
| Product identity | `docs/active/product/PRODUCT_MASTER.md` |
| Phase boundaries | `docs/active/product/ROADMAP.md` |
| Signal / match law | `SIGNAL_SYSTEM.md`, `MATCH_SYSTEM.md` |
| Planning index | `docs/active/governance/MASTER_BACKLOG.md` |
| Authority precedence | `docs/active/governance/SSOT_HIERARCHY.md` |
| AI boot | `docs/active/governance/START_NEW_SPRINT.md` |
| Engineering P0/P1 | Root `BACKLOG.md` |
| Sprint history | `SPRINT_LOG.md` + archive full log |
| Historical only | `docs/archive/`, `backlog/archive/` |

---

## 3. Governance conflicts resolved

| Conflict | Resolution |
|----------|------------|
| `FOX_ROADMAP.md` vs `ROADMAP.md` | Active law = `ROADMAP.md` only; FOX in archive |
| `BACKLOG.md` linked dead `FOX_ROADMAP` | Fixed to `ROADMAP.md` |
| Phase table duplicated in PRODUCT_MASTER + ROADMAP | Master = summary; ROADMAP = PHASE1–7 detail |
| `PHASE1-H*` vs product PHASE2 | Documented naming split in ROADMAP + SSOT_HIERARCHY |
| `AI_CONTEXT_PRIORITY` vs boot order | Marked supplemental; START_NEW_SPRINT + SSOT_HIERARCHY win |
| MASTER_BACKLOG duplicated phase text | Points to ROADMAP only |

---

## 4. Impacted files

- `docs/active/product/ROADMAP.md` (rewritten)
- `docs/active/product/PRODUCT_MASTER.md`
- `docs/active/product/AI_DEVELOPMENT_CONSTITUTION.md`
- `docs/active/governance/SSOT_HIERARCHY.md` (new)
- `docs/active/governance/START_NEW_SPRINT.md`
- `docs/active/governance/MASTER_BACKLOG.md`
- `docs/active/governance/REPO_GOVERNANCE_RULES.md`
- `docs/active/governance/AI_CONTEXT_PRIORITY.md`
- `docs/active/governance/AI_TASK_TEMPLATE.md`
- `docs/active/governance/GOVERNANCE_CHECKLIST.md`
- `docs/active/governance/README.md`
- `docs/README.md`
- `BACKLOG.md` (broken link fix)
- `tests/regression/test_ssot_hierarchy_v1.py` (new)

---

## 5. Regression risks

- Tests referencing `FOX_ROADMAP` in active path may fail — active file removed by design.
- `test_ai_development_discipline_v1` load-order assertions may need updates if boot steps change.
- Long `BACKLOG.md` body still contains historical phase names; not rewritten (out of scope).

---

## 6. Recommended canonical workflow

1. Load `START_NEW_SPRINT.md` chain including `SSOT_HIERARCHY.md` and `ROADMAP.md`.
2. Confirm ACTIVE row in `MASTER_BACKLOG.md` matches intended **product** phase.
3. Create or use `backlog/archive/BACKLOG_*` + `SPRINT_*` for the slice.
4. Implement against `docs/active/` only.
5. Run `check_all_flows.py`, `reflex_compile_gate.py`, `pytest tests/regression/`.
6. UAT per `docs/active/uat/`.
7. Mark COMPLETED in MASTER_BACKLOG; append `SPRINT_LOG.md`; archive slice.

---

## 7. Validation

- `python ops/flow/check_all_flows.py`
- `python ops/env/reflex_compile_gate.py`
- `pytest tests/regression/test_ssot_hierarchy_v1.py tests/regression/test_ai_development_discipline_v1.py -v`
