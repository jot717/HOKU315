# PHASE1-D UX INTELLIGENCE UAT

**TYPE:** Rule-based social pressure copy (no LLM / no therapy)

## Preconditions

- `/profile` saved
- `/quiz` sliders moved (optional but improves inference)
- `/target` named (optional; improves target-specific lines)

## Manual checks

### `/insight`

- [ ] After「開始分析」, copy explains **why interaction drains you** (causal, not label-only).
- [ ] Rhythm section describes **conflict or mismatch**, not only archetype name.
- [ ]「適合你的社交類型」reads as **why this fit is lighter**, not generic compatibility.
- [ ]「建議避免」names **interaction shape**, not insults toward a person.
- [ ] **Exactly one** fox/observer block; no second fox monologue elsewhere on page.
- [ ] No therapy/diagnosis wording (see `SOCIAL_CAUSALITY_RULES.md`).

### `/match`

- [ ] Each card shows **lighter interaction**, **pressure reduced**, **rhythm**, **fatigue avoided**, **one scenario**.
- [ ] High-distance cards still feel believable (not "great vibes" only).
- [ ] Blurred cards explain caution without API/token errors.

### Regression

```bash
python ops/flow/check_all_flows.py
pytest tests/regression/test_phase1d_ux_intelligence_v1.py -v
pytest tests/regression/ -v --tb=short
python ops/env/reflex_compile_gate.py
```

## Pass criteria

- Outputs feel observational and **social-causal**.
- Less template phrasing than pre-Phase1-D.
- Fox presence **reduced** (one block) but **more specific**.
