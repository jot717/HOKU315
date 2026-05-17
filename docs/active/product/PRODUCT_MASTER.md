# PRODUCT MASTER - Single Source of Truth

**All product, UAT, and backlog docs must reference this file.**

AI: [`AI_DEVELOPMENT_CONSTITUTION.md`](AI_DEVELOPMENT_CONSTITUTION.md) · Checklist: [`../governance/GOVERNANCE_CHECKLIST.md`](../governance/GOVERNANCE_CHECKLIST.md) · Backlog: [`../governance/MASTER_BACKLOG.md`](../governance/MASTER_BACKLOG.md) · UAT: [`../uat/UAT_MASTER_GUIDE.md`](../uat/UAT_MASTER_GUIDE.md)

---

## Official product identity

**HOKU315 = AI social signal intelligence system**

Helps users identify **dangerous / high-drain interaction patterns** through rule-based social signal and energy analysis.

**Core value:** Interaction pressure, rhythm mismatch, and social energy cost - not dating scores or therapy.

### What HOKU315 is NOT

- Not a therapy app or emotional healing AI
- Not an AI companion or life coach SKU
- Not a dating score or compatibility-percent product
- Not a personality analyzer (MBTI, attachment labels as identity)
- Not SNS-connected in **Phase 1 face**

Terminology: [`CANONICAL_TERMINOLOGY.md`](CANONICAL_TERMINOLOGY.md)

---

## Official user flow

**No second flow allowed.**

```
/ -> /profile -> /quiz -> /target -> /insight -> /match
```

| Step | Route | Purpose |
|------|-------|---------|
| Home | `/` | Guest vs account entry |
| Signal profile | `/profile` | Local signal profile |
| Mine questionnaire | `/quiz` | Sensitivity vector |
| Target observation | `/target` | Named target (local) |
| Guardian observation | `/insight` | Interaction pressure + rhythm |
| Match wall | `/match` | Social energy compatibility |

Detail: [`SIGNAL_SYSTEM.md`](SIGNAL_SYSTEM.md) · [`MATCH_SYSTEM.md`](MATCH_SYSTEM.md) · [`../uat/PHASE1_PRODUCT_FLOW_UAT.md`](../uat/PHASE1_PRODUCT_FLOW_UAT.md)

---

## Official systems (only)

| System | SSOT / code |
|--------|-------------|
| Signal system | [`SIGNAL_SYSTEM.md`](SIGNAL_SYSTEM.md) |
| Interaction pressure | `ux_intelligence_engine.py` |
| Social energy | `match_rhythm_engine.py` |
| Match credibility | `fox_quiz/match_wall.py` |
| Persistence | Phase 2 |
| SNS intelligence | Phase 3+ |

---

## Guest vs account

| Mode | Promise |
|------|---------|
| **Guest** | Analyze signals now (local JSON) |
| **Account** | Save trends across time |

`/login` is optional utility. Phases: [`ROADMAP.md`](ROADMAP.md)

---

## Fox role

- **北極狐觀察** - one observer block on `/insight` max
- Not therapy guidance

---

## AI DEVELOPMENT DISCIPLINE

All implementation must follow:

[`docs/active/governance/START_NEW_SPRINT.md`](../governance/START_NEW_SPRINT.md)

---

## Phase boundaries

**Canonical detail:** [`ROADMAP.md`](ROADMAP.md) (PHASE1–PHASE7). Summary only:

| Phase | Scope |
|-------|--------|
| **1** | Local rule-based intelligence (**current face**) |
| **2–7** | Persistence → SNS → graph → AI scale → automation → platform |

Do not infer phases from `docs/archive/`. Governance sprints (`PHASE1-H*`) are not product phases.

---

## Engineering (non-product SSOT)

- [`../governance/DEVELOPMENT_CONSTITUTION.md`](../governance/DEVELOPMENT_CONSTITUTION.md)
- [`../governance/ARCHITECTURE_CONTRACT.md`](../governance/ARCHITECTURE_CONTRACT.md)

Historical annex: `docs/archive/product/` (reference only).
