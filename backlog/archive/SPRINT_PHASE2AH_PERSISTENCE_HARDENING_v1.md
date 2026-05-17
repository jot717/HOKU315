# SPRINT — PHASE2-AH Persistence Hardening v1

## GOAL

Harden local persistence per architecture review (R1/R2/R3/R7).

## DELIVERABLES

- `product/persistence/runtime/schema.py`
- Atomic `LocalJsonBackend.write`
- Store normalization parity + session envelope
- Ops sanity via stores only
- Tests: regression + UAT expansion
- Report: `docs/archive/reviews/PHASE2AH_PERSISTENCE_HARDENING_REPORT_v1.md`

## REGRESSION

```bash
pytest tests/regression/test_phase2ah_persistence_hardening_v1.py -v --tb=short
pytest tests/uat/ -v --tb=short
```

## COMMIT

`fix(persistence): PHASE2AH persistence hardening v1`
