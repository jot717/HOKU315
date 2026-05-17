# PHASE1-F MATCH CREDIBILITY UAT

## Preconditions

- `/profile`, `/quiz` completed (improves inference)
- Optional `/target` for insight weakness overlap line

## `/match`

- [ ] Each card shows **互動節奏**, **回覆壓力**, **情緒步調**, **社交電量安全度**, **可能耗盡點**, **互動情境**
- [ ] No primary "dating score" or vague "high compatibility" without mechanism
- [ ] Blurred cards explain caution without API/token noise
- [ ] Copy references **rhythm / energy / pressure**, not personality typing

## `/insight`

- [ ] **你的節奏弱點** section links weakness ↔ interaction type (causal, not "you are sensitive")
- [ ] Still **one** 北極狐觀察 block only
- [ ] No therapy/diagnosis wording

## Regression

```bash
python ops/flow/check_all_flows.py
pytest tests/regression/test_phase1f_match_credibility_v1.py -v
pytest tests/regression/ -v --tb=short
python ops/env/reflex_compile_gate.py
```

## Pass

- Match feels believable and energy-oriented  
- Less template feeling vs pre-Phase1-F  
- Fox restrained  
