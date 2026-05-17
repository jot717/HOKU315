# Product layer — match

**Logical ownership**: match wall UI、配對 RPC 呼叫與相關 state。

**MATCH FLOW v1（init + runtime helper）**

| 文件 | 內容 |
|------|------|
| [`state_model.md`](state_model.md) | USER_STATE / MATCH_STATE |
| [`match_logic.md`](match_logic.md) | 規則式分數草案 |
| [`product_flow.md`](product_flow.md) | 使用者流程 |
| [`runtime/match_engine.py`](runtime/match_engine.py) | rule-based scoring engine（MVP） |
| [`runtime/match_flow.py`](runtime/match_flow.py) | runtime helper：`run_match(user_a, user_b)` |

**Backlog／Sprint**：[`backlog/archive/BACKLOG_MATCH_FLOW_v1.md`](../../backlog/archive/BACKLOG_MATCH_FLOW_v1.md)、[`backlog/archive/SPRINT_MATCH_FLOW_v1.md`](../../backlog/archive/SPRINT_MATCH_FLOW_v1.md) · Index：[`backlog/MASTER_BACKLOG.md`](../../backlog/MASTER_BACKLOG.md)

**目前實作位置**（Reflex app 模組未搬移，避免破壞 `fox_quiz`／`rxconfig`）：

- `fox_quiz/match_wall.py`
- `fox_quiz/fox_quiz.py`（`/match` route）
- `db_service.py`（`get_safe_matches` 等）

此目錄為 **REPO LAYERING v1** 之分類占位；新增程式碼時優先放在對應既有檔案或與維護者約定之結構。
