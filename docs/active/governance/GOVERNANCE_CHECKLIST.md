# GOVERNANCE CHECKLIST

Pre-sprint checks. Law: [`../product/AI_DEVELOPMENT_CONSTITUTION.md`](../product/AI_DEVELOPMENT_CONSTITUTION.md)

- [ ] Violates [`PRODUCT_MASTER.md`](../product/PRODUCT_MASTER.md)?
- [ ] Creates a second system?
- [ ] Leaks a future phase?
- [ ] Creates duplicate docs outside `docs/active/`?
- [ ] Adds markdown to repo root?
- [ ] Puts product truth in `ops/`?
- [ ] Breaks [`CANONICAL_TERMINOLOGY.md`](../product/CANONICAL_TERMINOLOGY.md)?

Entropy: [`REPO_ENTROPY_CHECKLIST.md`](REPO_ENTROPY_CHECKLIST.md)

```bash
python ops/flow/check_all_flows.py
python -m pytest tests/regression/test_phase1h5_root_consolidation_v1.py -v --tb=short
```
