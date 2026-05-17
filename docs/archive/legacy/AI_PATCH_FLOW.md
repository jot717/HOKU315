# AI patch flow — Observe → Deploy

本流程約束 **AI／人工協作修復** 時的責任分界：自動化僅輔助 **Observe／Evidence／Replay／Diagnose／Suggest**；**合併與部署**須經人類審核與測試閘門。

```
Observe
  → Evidence
  → Replay
  → Diagnose
  → Suggest
  → Human Review
  → Regression Test
  → Deploy
```

---

## Observe

- 從使用者回報、監控、或開發時 `reflex run`／瀏覽器 Console 察覺異常。  
- 不急于改 code：先記錄現象與發生路徑（路由、操作步驟）。

---

## Evidence

- 依 [`ops/debug/DEBUG_GUIDE.md`](../ops/debug/DEBUG_GUIDE.md) 收集 Console／Network／Backend／SQL。  
- 建立標準目錄：`python scripts/create_incident.py short-slug`。  
- 可選：`python scripts/collect_runtime.py short-slug` 補齊 runtime／環境（已脫敏）與 payload 占位檔。

---

## Replay

- **Mock**：`python -m ai.replay.replay_incident --incident debug_evidence/YYYY-MM-DD-short-slug`（見 [`REPLAY_GUIDE.md`](REPLAY_GUIDE.md)；亦可 `python replay/replay_incident.py` shim）。  
- **Live**：僅在符合 [`ops/debug/DEBUG_POLICY.md`](../ops/debug/DEBUG_POLICY.md) 的前提下於安全環境重播。

---

## Diagnose

- 使用 taxonomy：`ai/taxonomy/error_taxonomy.yaml`。  
- 執行 skeleton 分類器：

```powershell
python -m ai.diagnosis.root_cause_engine --incident debug_evidence/YYYY-MM-DD-short-slug
```

輸出為 **排序後的假設**，需由開發者確認。

---

## Suggest

- 產生 patch 脈絡：`python scripts/generate_patch_context.py --incident ...` → `patch_context.md`。  
- 將 `patch_context.md`、事故檔案與下列 prompt 模板一併餵給 AI（或人工撰寫 patch）：  
  - `ai/prompt_templates/hotfix_prompt.md`  
  - `ai/prompt_templates/sql_patch_prompt.md`  
  - `ai/prompt_templates/runtime_bug_prompt.md`
- **Self-healing v1（SAFE MODE）**：taxonomy → 待審 JSON：`python -m ai.self_heal.suggest_bridge STATE_DESYNC`；見 [`ai/self_heal/README.md`](../ai/self_heal/README.md)、[`BACKLOG.md`](../BACKLOG.md) **SELF-HEALING SYSTEM v1**。

---

## Human Review

- 禁止未經 review 直接套用 AI 產生的 SQL／production 變更。  
- 對照 `BACKLOG.md` **HOTFIX ARCHIVE** 與 `sql/DEPLOY_LOG.md`。

---

## Regression Test

- **`pytest tests/regression/`**（閘門；見 [`BACKLOG.md`](../BACKLOG.md) **REGRESSION GATE**、[`tests/regression/README.md`](../tests/regression/README.md)、CI **`.github/workflows/regression.yml`**）。  
- **`python -m tests.run_all_tests`**（亦由 regression 中的 gate 間接必跑）。  
- 將驗證步驟寫回 incident `root_cause.md`。

---

## Deploy

- 僅在 review 與 regression 通過後部署；並更新 `BACKLOG.md`、`SPRINT_LOG.md`、`sql/DEPLOY_LOG.md`（若涉及 SQL）。

---

## Patch policy（占位）

正式規則將擴充於 **`ai/patch_policy/`**（見該目錄 README）。現階段仍以 **`ops/debug/DEBUG_POLICY.md`** 為準。
