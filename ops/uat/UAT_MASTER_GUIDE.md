# UAT MASTER GUIDE

**Official acceptance path for Phase 1.** Product truth: [`../product/PRODUCT_MASTER.md`](../product/PRODUCT_MASTER.md)

---

## Canonical user journey (30-second understanding)

1. Land on **`/`** — choose **訪客** (start now) or **帳號** (save trends).
2. **`/profile`** — signal profile.
3. **`/quiz`** — sensitivity vector.
4. **`/target`** — observation target (optional but recommended).
5. **`/insight`** — interaction pressure analysis (one fox observer block).
6. **`/match`** — social energy cards (requires login + backend data).

---

## Official UAT flow (release gate)

### A. Guest path (no login)

| # | Route | Pass criteria |
|---|-------|----------------|
| A1 | `/` | Guest vs account explained; CTA clear |
| A2 | `/profile` | Save profile; success message |
| A3 | `/quiz` | Sliders work; result without API shame copy |
| A4 | `/target` | Target saves locally |
| A5 | `/insight` | Analysis runs; causal copy; **one** fox block |
| A6 | — | No SNS/token/sync-failure banners on above routes |

### B. Account path (login)

| # | Route | Pass criteria |
|---|-------|----------------|
| B1 | `/login` | Register/login; calm errors |
| B2 | `/match` | Cards show rhythm, reply pressure, energy safety, scenario |
| B3 | `/story` | Optional legacy upload path still works if enabled |

### C. Regression (automated)

```bash
python ops/flow/check_all_flows.py
pytest tests/regression/ -v --tb=short
python ops/env/reflex_compile_gate.py
```

---

## Regression categories

| Category | Tests / docs |
|----------|----------------|
| Governance | `test_phase1g_governance_consolidation_v1.py` |
| Phase1-D UX | `test_phase1d_ux_intelligence_v1.py` |
| Phase1-F match | `test_phase1f_match_credibility_v1.py` |
| SNS layer removed | `test_remove_premature_sns_layer_v1.py` |
| Match compile | `test_match_wall_compile_hotfix_v1.py` |
| Environment | `test_phase1e_environment_lockdown_v1.py` |
| Core flows | `test_core_flow.py`, `test_flow_integration.py` |

---

## Release blockers

- Any **failed** `tests/regression/` (except documented SKIP for cloud credentials)
- `reflex_compile_gate.py` not OK
- Phase 1 routes show therapy/diagnosis/dating-score-primary copy
- Multiple fox blocks on `/insight`
- `rx.foreach` float compares in card renderers

---

## Phase acceptance rules

| Phase | Acceptance |
|-------|------------|
| **1 face** | Guest journey complete without login; copy = signal/energy not SNS |
| **1-D** | Insight/match causal copy; ontology + engine tests green |
| **1-F** | Match cards = social energy model fields |
| **1-G** | `PRODUCT_MASTER` + this guide + `MASTER_BACKLOG` exist; home/login clear |
| **2** | Account persistence UAT (future) |
| **3** | SNS consent UAT (future) |

---

## Active UAT scripts

| Doc | When to use |
|-----|-------------|
| [`PHASE1_PRODUCT_FLOW_UAT.md`](PHASE1_PRODUCT_FLOW_UAT.md) | Full journey wording |

Phase-specific and domain UAT (historical): `docs/archive/uat/` — not release gate.

---

## Governance regression

`tests/regression/test_phase1h2_ai_governance_reset_v1.py` — active doc limits, SSOT files, terminology.
