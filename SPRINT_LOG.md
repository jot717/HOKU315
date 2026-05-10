# Sprint Log

## YYYY-MM-DD

### DONE

### BLOCKER

### NEXT

---

## 2026-05-08

### DONE

* remove `.states` runtime tracking（`git rm -r --cached .states` + `.gitignore`）

### BLOCKER

### NEXT

* UAT /match loading
* console error cleanup
* verify unlock flow

---

## 2026-05-09

### DONE

* 修復 Reflex nested p hydration warning（`rx.callout`／`rx.text` 調整：`fox_quiz.py`、`match_wall.py`、`login`／`story`／`unlocks`）

* Console hydration warning 清除（需本機 `/match`、`/quiz` 自驗）

### BLOCKER

### NEXT

* 驗證 /match console clean

* 驗證 unlock modal 無 hydration error

---

## 2026-05-10

### DONE

* 建立 **`DEBUG_GUIDE.md`**

* 建立標準除錯證據流（Console／Network／Backend／SQL／優先級／禁止事項）

* 建立 HOTFIX workflow（證據 → 分層 → 修正 → UAT → BACKLOG／SPRINT_LOG／TEST_CHECKLIST）

### BLOCKER

### NEXT

* MATCH FLOW UAT

* RPC response verification

* console clean verification

---

## 2026-05-11

### DONE

* 建立 **`debug_evidence/`** 與 **`debug_evidence/README.md`**（事故目錄、`console.txt`／`network.json`／`backend.txt`／`rpc.sql`／`root_cause.md` 規格）

* 建立 **`DEBUG_POLICY.md`**（P0 HOTFIX 禁止／允許事項）

* 建立 root cause evidence workflow（串接 **`DEBUG_GUIDE.md`** §6–§7）

### BLOCKER

### NEXT

* MATCH FLOW evidence collection

* RPC evidence collection

* runtime incident archive

---

## 2026-05-12

### DONE

* 建立 **Incident Template Generator**（`scripts/create_incident.py`）

### NEXT

* 第一個真實事故演練

* MATCH FLOW incident archive

---

## 2026-05-13

### DONE

* 建立 **AI INCIDENT SYSTEM v1 skeleton**（`ai/`、`replay/`、`docs/`、`tests/regression/`、`scripts/collect_runtime.py`、`scripts/generate_patch_context.py`）

* 建立 **AI-NATIVE REPO LAYERING v1**（[`REPO_ARCHITECTURE.md`](REPO_ARCHITECTURE.md)、`product/`、`ops/`、`ai/replay/`、`ai/incident/README.md`；`scripts`/`tests`/`docs` 仍於 repo 根目錄以相容 pytest／CI）

* **INTERFACE STABILIZATION v1**：[`ARCHITECTURE_CONTRACT.md`](ARCHITECTURE_CONTRACT.md)、`product/INTERFACE.md`、`ai/INTERFACE.md`、`ops/INTERFACE.md`

* **PROCESS ENFORCEMENT v1**：[`ops/process/RULES.md`](ops/process/RULES.md)、`ops/hooks/check_process.py`

### NEXT

* replay runtime incident

* regression baseline

* root cause classification

---

## SPRINT 2026-W02 — MATCH FLOW v1

**STATUS**: ACTIVE

**GOAL**:

- implement minimal match system

詳見 [`backlog/SPRINT_MATCH_FLOW_v1.md`](backlog/SPRINT_MATCH_FLOW_v1.md)。

---

## PROCESS ENFORCEMENT ACTIVE

All development must follow:

`BACKLOG → SPRINT → IMPLEMENT → TEST → LOG`

Rules: [`ops/process/RULES.md`](ops/process/RULES.md).

---

## SPRINT 2026-W03 — UNLOCK FLOW v1

STATUS: ACTIVE

GOAL:

- implement unlock insight system

- remove chat-first direction

---

## FLOW CONSISTENCY SYSTEM v1

STATUS: ACTIVE

GOAL:

- standardize product flow architecture

- prevent flow drift

---

## SPRINT 2026-W04 — INSIGHT ENGINE v1

STATUS: ACTIVE

---

## SPRINT 2026-W05 — FLOW INTEGRATION v1

STATUS: ACTIVE

---

## SPRINT 2026-W07 — APP UI INTEGRATION v1

STATUS: ACTIVE

---

## SPRINT 2026-W08 — INSIGHT EXPERIENCE v1

STATUS: ACTIVE

---

## SPRINT 2026-W04 — USER PROFILE SYSTEM v1

STATUS: ACTIVE
