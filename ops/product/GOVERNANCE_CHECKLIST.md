# GOVERNANCE CHECKLIST

Run **before** any sprint implementation. If any box is **yes** to a stop condition, halt and normalize first.

---

## Pre-sprint checks

- [ ] Does this violate [`PRODUCT_MASTER.md`](PRODUCT_MASTER.md) (identity, flow, systems)?
- [ ] Does this create a **second system** (signal, match, onboarding, memory, UX narrative)?
- [ ] Does this **leak a future phase** (SNS, graph AI, LLM inference in Phase 1 face)?
- [ ] Does this create **duplicate docs** instead of updating SSOT?
- [ ] Does this increase **repo entropy** (overlapping terms, parallel constitutions)?
- [ ] Does this require **archive cleanup** (active doc count > limits)?
- [ ] Does this break [`CANONICAL_TERMINOLOGY.md`](CANONICAL_TERMINOLOGY.md)?
- [ ] Does this create **UX confusion** (second flow, second onboarding)?

**If any stop condition:** do not merge feature work until governance regression passes.

---

## Post-change verification

```bash
python ops/flow/check_all_flows.py
pytest tests/regression/test_phase1h2_ai_governance_reset_v1.py -v --tb=short
pytest tests/regression/ -v --tb=short
python ops/env/reflex_compile_gate.py
```

---

## Active doc limits

| Area | Max active files | Location |
|------|------------------|----------|
| Product SSOT + governance | **< 10** | `ops/product/*.md` (excl. README) |
| UAT | **< 5** | `ops/uat/*.md` (excl. README) |
| Backlog sources | **2** | `backlog/MASTER_BACKLOG.md`, `SPRINT_LOG.md` |

Archive: `docs/archive/` — historical only; see `docs/archive/README.md`.
