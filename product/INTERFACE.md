# PRODUCT LAYER INTERFACE

## Entry Points

- **MATCH**:
  - **entry**: `fox_quiz` (match logic inside app)
  - **purpose**: generate user compatibility results

- **UNLOCK**:
  - **entry**: `fox_quiz` (unlock flow)
  - **purpose**: unlock interaction between users

- **CHAT**:
  - **entry**: `fox_quiz` (chat module)
  - **purpose**: messaging after unlock

## RULE

Product layer **must NOT** directly import AI modules (`ai/*`).

See also [`ops/governance/REPO_ARCHITECTURE.md`](../ops/governance/REPO_ARCHITECTURE.md), [`ops/governance/ARCHITECTURE_CONTRACT.md`](../ops/governance/ARCHITECTURE_CONTRACT.md).
