# GOVERNANCE CHECKLIST

Pre-sprint checks. Law: [`../product/AI_DEVELOPMENT_CONSTITUTION.md`](../product/AI_DEVELOPMENT_CONSTITUTION.md)

- [ ] Violates [`PRODUCT_MASTER.md`](../product/PRODUCT_MASTER.md)?
- [ ] Creates a second system?
- [ ] Leaks a future phase?
- [ ] Creates duplicate docs outside `docs/active/`?
- [ ] Adds markdown to repo root?
- [ ] Puts product truth in `ops/`?
- [ ] Breaks [`CANONICAL_TERMINOLOGY.md`](../product/CANONICAL_TERMINOLOGY.md)?
- [ ] START_NEW_SPRINT loaded
- [ ] PRODUCT_MASTER loaded
- [ ] MASTER_BACKLOG loaded
- [ ] no archive context used
- [ ] no duplicate docs created
- [ ] phase boundary respected

Entropy: [`REPO_ENTROPY_CHECKLIST.md`](REPO_ENTROPY_CHECKLIST.md)

```bash
python ops/flow/check_all_flows.py
python -m pytest tests/regression/test_ai_development_discipline_v1.py -v --tb=short
```
