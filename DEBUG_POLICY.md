# AI PATCH POLICY

本檔約束 **P0 HOTFIX** 與 **AI-assisted patch** 的允許範圍，與 [**`DEBUG_GUIDE.md`**](DEBUG_GUIDE.md)、[**`debug_evidence/README.md`**](debug_evidence/README.md) 並行使用：**先有證據**，再最小修正。

---

## P0 HOTFIX — **禁止**

在未封存 **`debug_evidence/YYYY-MM-DD-…`** 證據且未完成 **`DEBUG_GUIDE.md`** 所述分层判定前，**禁止**：

* rename function（大規模重新命名／公開 API 改名）  
* rename state（跨元件／全域 State 欄位改名）  
* 改 **`route`**（`/match`、`/story`、`/login` 等）  
* 改 **RPC signature**（函式參數名／順序／型別／REST contract），除非 **`sql/DEPLOY_LOG.md`** 已記載並已於 DB 部署  
* **大規模 refactor**（與根因無關之重構）  
* **改 schema**（資料表結構、欄位語意替換）未經明確設計與 deploy log  

---

## P0 HOTFIX — **允許**

下列在未扭曲產品契約前提下通常允許：

* **小範圍 patch**（單一函式／單一元件／單一路径修正）  
* **logging**（例如 `DEBUG_VECTOR`、結構化錯誤摘要）  
* **fallback**（已知環境差異：例如 RPC 簽名過渡、retry）  
* **null／empty handling**  
* **guard**（早退、權限／token 檢查）  
* **runtime fix**（hydration、nested DOM、`ImmutableState` 等對應最小 UI／事件修正）  

---

## 事故結案檢查

1. **`debug_evidence/…`** 內是否具備 `console.txt`／`network.json`／`backend.txt`／`rpc.sql`（若有涉 RPC／SQL）／`root_cause.md`（視嚴重度至少後者 + 其一）  
2. [**`BACKLOG.md`**](BACKLOG.md) **HOTFIX ARCHIVE** 是否摘要連結至該資料夾路徑  
3. [**`SPRINT_LOG.md`**](SPRINT_LOG.md) 是否記錄 DONE／BLOCKER  
