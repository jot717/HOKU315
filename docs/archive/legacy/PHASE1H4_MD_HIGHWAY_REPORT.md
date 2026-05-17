# PHASE1-H4 - MD HIGHWAY RESTRUCTURE REPORT

**Sprint:** Markdown highway v1 · **Commit:** `chore(repo): PHASE1H4 MD HIGHWAY RESTRUCTURE v1`

---

## BEFORE (H3 end state)

| Metric | Approx |
|--------|--------|
| Root `.md` files | 10+ (README, BACKLOG, SPRINT_LOG, constitution, debug, test, architecture, sprint plan) |
| Active product location | `ops/product/` (9 files) |
| Active UAT location | `ops/uat/` (2 + audit reports) |
| Archive layout | `phase1_legacy/`, `old_uat/`, `old_hotfix/` buckets |
| AI navigation | Multiple entry points (root + ops + docs) |

---

## AFTER

| Metric | Value |
|--------|-------|
| Root `.md` files | **3** (`README.md`, `BACKLOG.md`, `SPRINT_LOG.md`) |
| Active product SSOT | **8** in `docs/active/product/` |
| Active UAT | **2** in `docs/active/uat/` |
| Active governance | `docs/active/governance/GOVERNANCE_CHECKLIST.md` |
| Active env | `docs/active/env/` |
| Archive buckets | `product/`, `uat/`, `hotfix/`, `legacy/`, `dead_routes/`, `root_legacy/` |
| Engineering law | `ops/governance/`, `ops/debug/`, `ops/testing/` |

**Reduction:** root markdown ~70% fewer files (10 -> 3).

---

## Active surface map

| Area | Path |
|------|------|
| Product law | `docs/active/product/PRODUCT_MASTER.md` |
| Surface map | `docs/active/product/ACTIVE_SURFACE_MAP.md` |
| UAT gate | `docs/active/uat/UAT_MASTER_GUIDE.md` |
| Navigation | `docs/README.md` -> `docs/active/README.md` |

---

## Archive map

| Bucket | Role |
|--------|------|
| `docs/archive/product/` | Legacy constitutions |
| `docs/archive/uat/` | Phase UAT scripts |
| `docs/archive/hotfix/` | Hotfix audits |
| `docs/archive/legacy/` | Drift, H3/H4 reports, dead components |
| `docs/archive/dead_routes/` | Removed routes |
| `docs/archive/root_legacy/` | Former root `SPRINT_PLAN.md` |

---

## Navigation flow (AI)

```
README.md (10s product pitch)
  -> docs/README.md
    -> docs/active/README.md
      -> docs/active/product/PRODUCT_MASTER.md
      -> docs/active/product/AI_DEVELOPMENT_CONSTITUTION.md
```

**Forbidden:** new root markdown; product docs outside `docs/active/product/`.

---

## Final active product

**HOKU315** = AI Social Signal Intelligence System

**Loop:** profile -> quiz -> target -> insight -> match

**Fox:** observer only (one block on insight)

**Phases:** P1 local | P2 persistence | P3 SNS | P4 graph | P5 AI scale

---

## Validation

```bash
python ops/flow/check_all_flows.py
python -m pytest tests/regression/test_phase1h4_md_highway_v1.py -v --tb=short
```
