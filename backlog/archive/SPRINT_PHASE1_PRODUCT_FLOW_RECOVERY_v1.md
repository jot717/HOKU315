# SPRINT — PHASE1 product flow recovery v1

**Type:** SAFE MODE UX + documentation  
**Status:** Complete (when regression + flow check green)

## Stories

1. **Home** — Main title/subtitle, five-step list, two CTAs, footer fox note.  
2. **Profile** — Signal-profile only; explanation box; helpers; success + next to quiz.  
3. **Quiz** — Header, “what we analyze” list, bottom copy + CTA to target.  
4. **Target** — Observation framing + CTA to insight.  
5. **Insight** — Six sections; single fox note; three next actions.  
6. **Match** — Header + cards with compatibility, pressure, rhythm, risk, why.  
7. **Nav** — Six primary labels; drop story/unlock from primary bar.  
8. **Docs + deprecation** — New ops docs; move drifted files to `docs/deprecated/`.

## Verification

```powershell
python ops/flow/check_all_flows.py
pytest tests/regression/ -v --tb=short
```

## Log

Record merge and verification in [`SPRINT_LOG.md`](../SPRINT_LOG.md).
