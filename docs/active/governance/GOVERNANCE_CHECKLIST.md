# GOVERNANCE CHECKLIST

Pre-sprint checks. Law: [`../product/AI_DEVELOPMENT_CONSTITUTION.md`](../product/AI_DEVELOPMENT_CONSTITUTION.md)

- [ ] Violates [`PRODUCT_MASTER.md`](../product/PRODUCT_MASTER.md)?
- [ ] Creates a second system?
- [ ] Leaks a future phase?
- [ ] Creates duplicate docs outside `docs/active/`?
- [ ] Increases repo entropy?
- [ ] Needs archive cleanup?
- [ ] Breaks [`CANONICAL_TERMINOLOGY.md`](../product/CANONICAL_TERMINOLOGY.md)?
- [ ] Creates UX confusion (second flow)?

Entropy: [`../../../ops/governance/REPO_ENTROPY_CHECKLIST.md`](../../../ops/governance/REPO_ENTROPY_CHECKLIST.md)

```bash
python ops/flow/check_all_flows.py
python -m pytest tests/regression/test_phase1h4_md_highway_v1.py -v --tb=short
```
