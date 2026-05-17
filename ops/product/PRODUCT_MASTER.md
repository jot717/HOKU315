# PRODUCT MASTER  ESingle Source of Truth

**All product, UAT, and backlog docs must reference this file.**  
AI implementation: [`AI_DEVELOPMENT_CONSTITUTION.md`](AI_DEVELOPMENT_CONSTITUTION.md) · Governance: [`GOVERNANCE_CHECKLIST.md`](GOVERNANCE_CHECKLIST.md) · Backlog: [`../../backlog/MASTER_BACKLOG.md`](../../backlog/MASTER_BACKLOG.md) · UAT: [`../uat/UAT_MASTER_GUIDE.md`](../uat/UAT_MASTER_GUIDE.md)

---

## Official product identity

**HOKU315 = AI social signal intelligence system**

Helps users identify **dangerous / high-drain interaction patterns** through rule-based social signal and energy analysis.

**Core value:** Understand interaction pressure, rhythm mismatch, and social energy cost  Enot who to date or how to heal.

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
/  ↁE /profile  ↁE /quiz  ↁE /target  ↁE /insight  ↁE /match
```

| Step | Route | Purpose |
|------|-------|---------|
| Home | `/` | Guest vs account entry (no second onboarding) |
| Signal profile | `/profile` | Local signal profile |
| Mine questionnaire | `/quiz` | Sensitivity vector |
| Target observation | `/target` | Named target (local) |
| Guardian observation | `/insight` | Interaction pressure + rhythm |
| Match wall | `/match` | Social energy compatibility |

Detail: [`SIGNAL_SYSTEM.md`](SIGNAL_SYSTEM.md) · Match: [`MATCH_SYSTEM.md`](MATCH_SYSTEM.md) · UAT: [`../uat/PHASE1_PRODUCT_FLOW_UAT.md`](../uat/PHASE1_PRODUCT_FLOW_UAT.md)

---

## Official systems (only)

| System | SSOT / code |
|--------|-------------|
| Signal system | [`SIGNAL_SYSTEM.md`](SIGNAL_SYSTEM.md) · `product/signal/`, `product/profile/`, `product/target/` |
| Interaction pressure system | `ux_intelligence_engine.py` · archive annex |
| Social energy system | `match_rhythm_engine.py` · [`MATCH_SYSTEM.md`](MATCH_SYSTEM.md) |
| Match credibility system | `fox_quiz/match_wall.py` · [`MATCH_SYSTEM.md`](MATCH_SYSTEM.md) |
| Persistence layer | Phase 2  Eaccount/cloud utility |
| SNS intelligence layer | Phase 3+  Egated |

**Forbidden:** second signal system, second match narrative, second onboarding, second memory law in active docs.

---

## Guest vs account

| Mode | Persistence | Promise |
|------|-------------|---------|
| **Guest** | Local JSON on device | Analyze signals now |
| **Account** | Cloud profile, match wall, history | Save trends across time |

`/login` is optional utility. Phase rules: [`ROADMAP.md`](ROADMAP.md)

---

## Fox role

- **北極狐觀寁E*  Eone observer block on `/insight` max
- Not therapy guidance, not emotional healing copy

---

## Phase boundaries

| Phase | Scope |
|-------|--------|
| **1** | Manual / local rule-based intelligence (current face) |
| **2** | Persistence & memory |
| **3** | SNS import |
| **4** | Social graph intelligence |
| **5** | AI-scale inference |

Full phased delivery: [`ROADMAP.md`](ROADMAP.md) · No phase leakage in primary UX.

---

## Engineering (non-product SSOT)

- [`../../DEVELOPMENT_CONSTITUTION.md`](../../DEVELOPMENT_CONSTITUTION.md)
- [`../../ARCHITECTURE_CONTRACT.md`](../../ARCHITECTURE_CONTRACT.md)

Historical technical annex: `docs/archive/phase1_legacy/` (reference only).
