# Product layer — match

**Logical ownership**: match wall UI、配對 RPC 呼叫與相關 state。

**目前實作位置**（Reflex app 模組未搬移，避免破壞 `fox_quiz`／`rxconfig`）：

- `fox_quiz/match_wall.py`
- `fox_quiz/fox_quiz.py`（`/match` route）
- `db_service.py`（`get_safe_matches` 等）

此目錄為 **REPO LAYERING v1** 之分類占位；新增程式碼時優先放在對應既有檔案或與維護者約定之結構。
