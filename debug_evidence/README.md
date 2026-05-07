# HOKU315 DEBUG EVIDENCE

## 目的

保存每次下列類型事件的**完整、可回放證據**：

* HOTFIX  
* Runtime fail  
* RPC fail  
* SQL fail  
* UAT fail  
* Production incident（若有）

對齊收集流程見根目錄 [**`DEBUG_GUIDE.md`**](../DEBUG_GUIDE.md)；AI／人工 HOTFIX 行為約束見 [**`DEBUG_POLICY.md`**](../DEBUG_POLICY.md)。

---

## 目錄命名規則

每一筆事故獨立一資料夾，建議：

```text
debug_evidence/YYYY-MM-DD-short-slug/
```

範例：

```text
debug_evidence/2026-05-10-match-fail/
```

同一日多起事故時於 slug 區分（例如 `2026-05-10-match-rpc-pgrst202`）。

---

## 建立事故模板

於專案根目錄執行：

```powershell
python scripts/create_incident.py match-fail
```

將建立 `debug_evidence/YYYY-MM-DD-match-fail/`（日期為執行當日），內含 `console.txt`、`network.json`、`backend.txt`、`rpc.sql`、`root_cause.md` 標準檔案。

可選：`--date YYYY-MM-DD` 指定資料夾日期前綴；`--force` 覆寫已存在目錄（謹慎使用）。

---

## 每次事故建議檔案（資產化）

```text
debug_evidence/YYYY-MM-DD-short-slug/
  console.txt
  network.json
  backend.txt
  rpc.sql
  root_cause.md
```

可視需要追加：`screenshots/`（輔助）、`deploy-diff.patch`、`environment.txt`。

---

## 檔案規則

### `console.txt`

**來源**：Browser → DevTools → **Console**

**內容應含**：

* hydration 相關訊息  
* React warning  
* `TypeError`／runtime error  
* 完整紅字堆疊（**複製文字**，勿僅截圖取代）

---

### `network.json`

**來源**：Chrome／Edge DevTools → **Network**，篩選 **`rpc`** 或對應 REST 請求

**內容應涵蓋**（可為 JSON 陣列或多段請求）：

* request payload  
* response body  
* HTTP status code  
* 必要時 timing／failed flag  

※ 若有敏感 token，請脫敏後再提交。

---

### `backend.txt`

**來源**：執行 **`reflex run`**（或 **`python -m reflex run`**）之終端機輸出

**內容應含**：

* `DEBUG_VECTOR = …`（若程式有列印）  
* Python traceback  
* async／state 相關錯誤  
* RPC／HTTP 失敗摘要  

---

### `rpc.sql`

**來源**：Supabase **SQL Editor** 或其它對 DB 之驗證／部署語句

**內容可含**：

* 重現問題之 RPC 測試 SQL  
* 本次 deploy 之相關 DDL／`CREATE OR REPLACE FUNCTION`  
* 驗證用查詢（例如 `\df`、`information_schema` 結果可貼於 `backend.txt` 或本檔註解）

簽名以 repo 內 **`sql/match_logic.sql`** 與 **`sql/DEPLOY_LOG.md`** 為準。

---

### `root_cause.md`

固定段落結構如下：

```markdown
# Root Cause

## 問題

描述現象

## 根因

真正原因

## 修正

修了什麼

## 驗證

如何確認修復成功

## 影響範圍

哪些功能受影響
```

---

## 與其他文件的對應

| 動作 | 同步更新 |
|------|-----------|
| 封存證據 | 本目錄新增事故資料夾 + 檔案 |
| 決策摘要 | [`BACKLOG.md`](../BACKLOG.md) **HOTFIX ARCHIVE** |
| 進度 | [`SPRINT_LOG.md`](../SPRINT_LOG.md) |
| 測試勾選 | [`TEST_CHECKLIST.md`](../TEST_CHECKLIST.md) |
