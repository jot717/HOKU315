# HOKU315 DEBUG GUIDE

本檔為 **Browser／Network／Backend／SQL／優先級／證據流／HOTFIX 流程** 的統一 SOP。  
所有 **HOTFIX、UAT、AI-assisted Debug** 應先依此收集證據，再修改程式或資料庫。

* **證據資產化**：將原始材料寫入 **`debug_evidence/YYYY-MM-DD-slug/`**（見 [`debug_evidence/README.md`](debug_evidence/README.md)）。  
* **Patch 約束**：見 [**`ops/debug/DEBUG_POLICY.md`**](ops/debug/DEBUG_POLICY.md)。  

詳見 [`BACKLOG.md`](BACKLOG.md) **HOTFIX ARCHIVE** 與 [`SPRINT_LOG.md`](SPRINT_LOG.md)。

---

## 1. Browser Console

### 目的

* hydration／CSR mismatch  
* runtime／前端例外  
* React warning  

### 步驟

1. **F12** 開發者工具  
2. 切換 **Console**  
3. 複製**完整紅字** stack／message（**勿僅截圖**，以利搜尋與對照）

### 必查關鍵字

`ERROR`、`TypeError`、`hydration`、`malformed`、`PGRST`、`undefined`、`401`、`403`、`500`

### 範例

`<p> cannot be a descendant of <p>`（nested 段落／元件組合問題）

---

## 2. Network Debug

### 步驟

1. **F12** → **Network**  
2. 篩選 **`rpc`**（或過濾路徑含 `/rest/v1/rpc/`）  
3. 點選 **`get_safe_matches`**（或實際呼叫之 RPC 名稱）

### 需收集

#### Payload（Request JSON）

例如：

```json
{
  "query_vector": "[0.1,0.2,0.3,...]"
}
```

※ pgvector 字串須為 **`[...]`** 括號格式；CSV（無括號）常觸發 `malformed array literal`。

#### Response

例如錯誤：

```json
{
  "message": "malformed array literal"
}
```

### 目的

確認 **frontend → PostgREST → RPC** 參數名與型別是否與部署之函式簽名一致（對照 `sql/match_logic.sql`）。

---

## 3. Backend Log

### 來源

執行 **`reflex run`**（或 **`python -m reflex run`**）之 **終端機標準輸出／錯誤**。

### 需檢查

* **`DEBUG_VECTOR = [...]`**（若程式中有開啟除錯列印）  
* **`Traceback`**  
* RPC／HTTP 失敗訊息  
* async／state 相關錯誤（例如 ImmutableState）

### 範例

```
DEBUG_VECTOR = [0.1,0.1,...]
```

### 禁止

只貼 UI 截圖而**不附** backend／終端機輸出，無法判定資料是否已到達後端。

---

## 4. Supabase SQL RPC Debug

### SQL Editor（直接呼叫資料庫函式）

簽名以 **`sql/match_logic.sql`** 為準。目前 **`get_safe_matches(query_vector vector)`** 時可類似：

```sql
SELECT *
FROM get_safe_matches('[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]'::vector)
LIMIT 5;
```

若環境仍為舊版 **`current_uid uuid`** 等簽名，請依 **`sql/DEPLOY_LOG.md`** 與實際 DB **`information_schema`**／`\df get_safe_matches` 對齊後再測。

### 目的

區分問題來自 **SQL／RPC／pgvector** 或 **前端／PostgREST 參數**。

---

## 5. Debug Priority

### P0 — 功能阻斷

* **`/match` 無法載入**  
* **Auth 失敗**  
* **RPC 失敗**  
* **vector／malformed literal**

### P1 — Runtime

* hydration／SSR mismatch  
* state 與 UI 不一致  
* async／背景事件錯誤  

### P2 — UI

* nested `<p>`、排版間距、版面（不阻斷主流程時降級處理）

---

## 6. 標準除錯證據流

每次 **HOTFIX** 或嚴重 **UAT 失敗**前，應盡力備齊：

### A. Browser Console

完整文字錯誤／warning  

### B. Network Payload／Response

含 **`get_safe_matches`**（或相關）請求與回應 body  

### C. Backend Terminal Log

含 traceback／`DEBUG_VECTOR`／RPC 錯誤  

### D. SQL RPC 測試結果（若涉資料／向量）

於 SQL Editor 可重現與否之一小段結果或錯誤  

### E. 證據資產化（建議 P0／重複事故必做）

將 A–D 之原始輸出依 [**`debug_evidence/README.md`**](debug_evidence/README.md) 存入：

`debug_evidence/YYYY-MM-DD-short-slug/`

並撰寫／更新該目錄之 **`root_cause.md`**（結案後補齊「修正」「驗證」段落）。

### 禁止（在未佐證下）

* 直接大量「試錯式 patch」  
* **未收集證據**即改 production SQL  
* **未驗證 root cause** 即重構大範圍模組  

---

## 7. HOTFIX Workflow

每次 **HOTFIX**（遵守 [**`ops/debug/DEBUG_POLICY.md`**](ops/debug/DEBUG_POLICY.md)）：

1. **收集證據**（§6 A–D，依優先級 P0→P1 聚焦）  
2. **資產化**：建立 **`debug_evidence/YYYY-MM-DD-short-slug/`**，置入 `console.txt`／`network.json`／`backend.txt`／`rpc.sql`（若適用）及 **`root_cause.md`** 草稿／完稿（見 [`debug_evidence/README.md`](debug_evidence/README.md)）  
3. **判定層級**：frontend／backend（Python‧Reflex）／RPC／SQL  
4. **最小修正**並於本地 **`reflex run`** + 對應路由 **UAT**  
5. **更新文件**：  
   * [`BACKLOG.md`](BACKLOG.md) — **HOTFIX ARCHIVE**（含問題／根因／修正／結果；可附證據目錄相對路徑）  
   * [`SPRINT_LOG.md`](SPRINT_LOG.md) — **DONE／BLOCKER／NEXT**  
   * [`ops/testing/TEST_CHECKLIST.md`](ops/testing/TEST_CHECKLIST.md) — 相關勾選項  
6. **建立 incident 資料夾（標準模板）**（若尚未手動建立）：  

```powershell
python scripts/create_incident.py short-slug
```

詳見 [`debug_evidence/README.md`](debug_evidence/README.md) — **建立事故模板**。

