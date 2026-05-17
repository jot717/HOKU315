# HOKU315 開發憲法（DEVELOPMENT_CONSTITUTION）

本文件為本專案之開發原則，與 `BACKLOG.md` 搭配使用；變更架構或流程時應同步修訂本文。**可執行流程與閘門**以 [`ops/process/RULES.md`](ops/process/RULES.md) 為準（見文末「執行說明」）。

---

## 第一章：架構與階層

### 1.1 全棧 Python 化

採用 **Reflex + Supabase** 架構：前端與互動邏輯以 Reflex 為主，後端資料與驗證以 Supabase（PostgreSQL、Auth、RPC 等）為主，盡量維持技術棧單一、可維護。

### 1.2 AI 切換層

所有 **LLM 調用** 必須封裝在**獨立的類別（或模組）**中，對外暴露穩定介面（例如：產生文案、評分、摘要），**禁止**在 UI 或業務流程中散落裸 API 呼叫。

該層須支援 **DeepSeek、Claude** 等供應商之**一鍵切換**（設定檔或環境變數切換實作，不得硬編唯一廠商）。

### 1.3 資料層

所有 **資料庫操作**（查詢、更新、RPC、向量寫入等）必須透過專案根目錄之 **`db_service.py`** 進行；其他模組不得直接建立第二套 Supabase 客戶端繞過該層（測試替身與 Mock 除外，且須在測試中明確標註）。

---

## 第二章：需求導向開發

嚴禁「隨興寫 code」。

任何功能或重構在動工前，須具備：

- **需求說明**（可為簡短規格、Issue 描述或本 repo 內之需求段落）；且  
- **`BACKLOG.md` 中可對應之項目**（狀態與驗收條件清楚）。

未完成上述文件化步驟之工作，不得合併為「已完成」之交付。

---

## 第三章：測試驅動

每個 **`BACKLOG.md` 項目**在標示完成前，必須：

1. 建立**對應之測試腳本**（命名慣例：`test_xxx.py` 或專案約定之測試路徑）；  
2. 在**終端機**執行並 **Debug 通過**（無未處理之失敗斷言或執行期錯誤）；  
3. 將測試如何執行（指令或簡述）保留在該 Backlog 項目之備註或 PR 說明中，便於重現。

「完成」之定義：**功能符合需求 + 測試可重現通過**。

---

## 附錄：環境鎖定與工作區

- **工作區根目錄**：以 **`HOKU315`（JOT717）專案根目錄** 為 Cursor 工作區根，路徑、匯入與腳本預設工作目錄皆以此為準。  
- **正式測試**：置於 **`tests/`**，自根目錄執行 `python -m tests.<模組>`（見 `README.md`）。  
- **歸檔**：階段性、非正式流程之腳本置於 **`archive/`**（側邊欄預設隱藏，見 `.vscode/settings.json`）。  
- **編譯產物**：Python 之 `__pycache__`、`.pyc` 由版本庫忽略並在編輯器中隱藏（見 `.gitignore`、`.vscode/settings.json`），避免干擾檔案樹與 diff。

---

## 執行說明（EXECUTION NOTE）

本文為**理念與原則層**之治理說明；**實際可執行規則**（流程、閘門、腳本）以下列為準：

- [`ops/process/RULES.md`](ops/process/RULES.md)
- [`ops/hooks/`](ops/hooks/)（如 `check_process.py`、`check_regression.sh` / `check_regression.ps1`）

This is **conceptual governance only**.  
All execution rules are enforced in:

- `ops/process/RULES.md`
- `ops/hooks/*`

---

*文件版本：初版*
