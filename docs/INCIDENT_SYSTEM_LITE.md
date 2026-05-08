# INCIDENT SYSTEM v1-lite

精簡對照：**A Observation → B Replay (mock) → C Root cause**，與完整 AI Incident / DEBUG 流程並存。

| 階段 | 用途 | 本 repo 實作 |
|------|------|----------------|
| **A Observation** | 留下時間戳與環境快照 | `python scripts/collect_runtime.py <slug>` 會寫入 **`runtime.json`**（`timestamp` / **`env` 已脫敏**，非草稿腳本之明文 `os.environ`）、並保留 `runtime_collect.json` 等檔 |
| **B Replay** | 離線確認「有載入快照」 | `python replay/replay_incident.py debug_evidence/YYYY-MM-DD-<slug>`（位置參數等同 `--incident`）；會列出 `runtime.json` 頂層 keys，其餘仍為 mock |
| **C Root cause** | 對 taxonomy 查表 | `python -m ai.diagnosis.root_cause_engine --error-type STATE_DESYNC`；完整事故仍用 `--incident`／`--scan-latest` |

## 與草稿 bash 的差異（刻意）

- **不**把所有程式換成極簡版：避免遺失 slug／日期目錄規則、`env` 脫敏、以及現有 **五類** taxonomy（HYDRATION／ASYNC 等）。
- **`error_taxonomy.yaml`**：維持單一來源；lite 僅多提供 **`--error-type`** 快速查詢。

## 一行範例

```powershell
python scripts/collect_runtime.py match-fail
python replay/replay_incident.py debug_evidence/2026-05-08-match-fail
python -m ai.diagnosis.root_cause_engine --error-type VECTOR_FORMAT_ERROR
```

完整流程見 [`DEBUG_GUIDE.md`](../DEBUG_GUIDE.md)、[`docs/REPLAY_GUIDE.md`](REPLAY_GUIDE.md)、[`docs/AI_PATCH_FLOW.md`](AI_PATCH_FLOW.md)。
