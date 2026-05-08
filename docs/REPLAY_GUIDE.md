# Replay guide — HOKU315

本文件描述 **incident replay** 與 **regression replay** 如何配合 [`debug_evidence/`](../debug_evidence/README.md)、[`ai/replay/replay_incident.py`](../ai/replay/replay_incident.py)（或根目錄 `replay/` shim）與 AI incident 流程（見 [`AI_PATCH_FLOW.md`](AI_PATCH_FLOW.md)）。

---

## 1. 為何需要 replay

- **Incident replay**：在同一組輸入（向量、RPC body、Network 紀錄）下重現問題，驗證根因假設。  
- **Regression replay**：修正後用相同 fixture／測試指令再跑一遍，避免 HOTFIX 回流。

目前 **`replay_incident.py` 為 mock skeleton**：只讀檔、列出將重放的項目，**不呼叫 PostgREST**、**不改資料庫**。

---

## 2. Incident replay 流程（建議順序）

1. **Observe**：使用者／監控觀察到異常（見 `DEBUG_GUIDE.md`）。  
2. **Evidence**：`python scripts/create_incident.py short-slug` 建立目錄；補齊 `console.txt`、`network.json`、`backend.txt`、`rpc.sql`。  
3. **Runtime snapshot（可選）**：`python scripts/collect_runtime.py short-slug` 寫入 `runtime_collect.json`、`env_redacted.json`、`vector_payload.json`、`rpc_payload.json`、`traceback_snippet.txt`。  
4. **Mock replay**：  

```powershell
python -m ai.replay.replay_incident --incident debug_evidence/YYYY-MM-DD-short-slug
```

5. **Live replay（未來）**：在隔離環境或 SQL Editor 依 `rpc.sql`／`network.json` 重播；須遵守 `DEBUG_POLICY.md`（禁止未佐證直接改 production SQL）。

---

## 3. Incident folder 約定

| 檔案 | Mock replay 用途 |
|------|------------------|
| `rpc_payload.json` | 模擬 RPC 請求本體 |
| `vector_payload.json` | 模擬向量輸入校驗 |
| `network.json` | 模擬 DevTools 層級重播 |
| `state_snapshot.json` | （選用）未來還原 Reflex state |

---

## 4. Regression replay

- **目標**：每次 AI 或人工 patch 合併前，跑 **`python -m tests.run_all_tests`** 與（未來）`tests/regression/` 內專項案例。  
- **做法**：將與事故相關的最小重現步驟／資料記入 regression README 與 incident `root_cause.md` 的「驗證」段落。  
- 詳見 [`tests/regression/README.md`](../tests/regression/README.md)。

---

## 5. 相關文件

- [`docs/AI_PATCH_FLOW.md`](AI_PATCH_FLOW.md) — 端到端 AI patch 節點  
- [`ai/diagnosis/root_cause_engine.py`](../ai/diagnosis/root_cause_engine.py) — 根因分類 skeleton  
