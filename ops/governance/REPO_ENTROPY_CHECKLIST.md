# REPO ENTROPY CHECKLIST

Run before merging governance or doc-heavy sprints.

---

## Root

- [ ] Root contains **only** `README.md`, `BACKLOG.md`, `SPRINT_LOG.md` (plus code/config)
- [ ] No new root `.md` files

---

## Active docs

- [ ] `docs/active/product/` has **exactly 8** SSOT files (see product README)
- [ ] `docs/active/uat/` has **at most 2** release UAT files
- [ ] No product law in `docs/active/product/` except pointer README

---

## Archive

- [ ] No loose `.md` at `docs/archive/` root (except README)
- [ ] Archive buckets: `product/`, `uat/`, `hotfix/`, `legacy/`, `dead_routes/`, `root_legacy/`
- [ ] Active docs do not markdown-link `docs/archive/` as authority

---

## Systems

- [ ] No second onboarding, signal, match, or UX narrative
- [ ] No parallel roadmap/constitution outside active product folder
- [ ] Sprint slices only in `backlog/` or `backlog/archive/`

---

## Regression

```bash
python ops/flow/check_all_flows.py
python -m pytest tests/regression/test_phase1h4_md_highway_v1.py -v --tb=short
```

**Law:** [`../../docs/active/product/AI_DEVELOPMENT_CONSTITUTION.md`](../../docs/active/product/AI_DEVELOPMENT_CONSTITUTION.md)
