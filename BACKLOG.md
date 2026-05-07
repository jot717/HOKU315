# HOKU315 BACKLOG

**Workflow（AI-native）**：衝刺計畫見 [`SPRINT_PLAN.md`](SPRINT_PLAN.md)、日誌見 [`SPRINT_LOG.md`](SPRINT_LOG.md)；配對牆驗收見 [`TEST_CHECKLIST.md`](TEST_CHECKLIST.md)；資料庫套用軌跡見 [`sql/DEPLOY_LOG.md`](sql/DEPLOY_LOG.md)。產品治理仍依根目錄 **`DEVELOPMENT_CONSTITUTION.md`**。

狀態約定：`[TODO]` · `[WIP]` · `[DONE]` · **`[REMOVED/INTERNAL_ONLY]`**。

---

## P0 — STABILIZATION

穩定基底與聯調護欄（持續維護，不視為「新功能」）。

- **Supabase / PostgREST**：`PGRST205`／schema cache 暖機；RPC 簽名與部署版本與 `sql/match_logic.sql` 對齊記錄於 `sql/DEPLOY_LOG.md`。
- **`malformed array literal` 迴歸防線**：RPC 僅傳 pgvector literal、`profiles.vector` 為單一來源；見 **HOTFIX ARCHIVE** 與 `TEST_CHECKLIST.md`。
- **Reflex runtime**：禁止在事件處理器中違反 async／`ImmutableStateError` 模式（背景任務見歷史 HOTFIX）。
- **環境**：`python-dotenv`、`.env` 與金鑰載入一致；依賴見凍結後之 `requirements.txt`（含 `reflex==0.9.2`、`supabase`、`postgrest`、`python-dotenv`）。
- **前后端契約**：`get_safe_matches` 回傳欄位與 `match_wall` 渲染鍵一致，避免 RPC／UI mismatch（見 `TEST_CHECKLIST.md`）。
- **測試閘門**：一鍵 `python -m tests.run_all_tests`；無雲端時 SKIP、exit 0。

---

## P1 — CORE FEATURES

目前已交付或可驗證之主線（MVP 1–2）。

- **`[DONE]` Task 1–4**：20 維維度與 `fox_logic`；測驗 UI；`db_service` 向量寫入；`user_memories`／RAG Lite／`llm_gateway`。
- **`[REMOVED/INTERNAL_ONLY]` Task 5**：`/chat` 產品面廢止，僅歷史／內部過渡保留。
- **`[DONE]` Task 6／6.5**：Auth、Story、Storage、Session、`ensure_user_profile`、受保護路由。
- **`[DONE]` Task 7**：配對牆、`get_safe_matches`、`match_wall`、`tests/test_hater_logic.py`。
- **`[DONE]` Task 7.5**：Navbar、`/`→`/match`、`/quiz`、登入依向量分流至 `/story` 或 `/match`。
- **`[WIP]` Task 9**：支付解鎖、`user_unlocks`、`create_unlock`、配對牆解鎖 dialog（含 `MOCK_UNLOCK`）。
- **`[TODO]` Task 8**：已解鎖對象之 AI 防雷報告（結構化輸出、付費價值）。

**Sprint 對齊**：本週以 [`SPRINT_PLAN.md`](SPRINT_PLAN.md) — **match wall 完整 demo** 為準，逐項勾選並於 [`SPRINT_LOG.md`](SPRINT_LOG.md) 留痕。

---

## P2 — GROWTH

產品化與規模化（規劃中，待 P1 收口後展開）。

- 真 LLM 攻略批次／on-demand API（與 Task 8 綑綁）。
- 觀測與成本：支付、生成成本紀錄。
- 向量記憶僅作畫像與攻略上下文（不驱动前台對話主流程）。

---

## P3 — FUTURE

- E2E（例如 Playwright）可選。
- 進階變現與營運實驗（待主線 Milestone 明確後再拆）。

---

## HOTFIX ARCHIVE

此區僅封存已發生之緊急修復與根因類項，避免與進行中需求混線。**不再於此區新增條目時，應同步寫入 `SPRINT_LOG` 或對應 Task DEV LOG。**

### malformed array literal／vector／RPC

- **FIX — `get_safe_matches` RPC vector parsing**：舊版 `string_to_array`／`::text` 與 pgvector `"[...]"` 衝突；改為原生 `vector <-> vector`／正確字面量傳参。
- **FIX — `mine_vector` 廢止**：統一 `profiles.vector`；種子／`db_service` 欄位預設與文案對齊。
- **FIX — RPC 傳入 vector 格式**：禁止 CSV；統一 `to_pgvector`／`"[...]"`；呼叫前可比對 `DEBUG_VECTOR` 輸出。
- **HOTFIX-005（歷史）**：RPC 曾以 `vec::text`／`float8[]` 繞過下標限制；已由 pgvector 原生路徑取代（歷史紀錄保留）。

### Reflex runtime（async／State）

- **HOTFIX-001**：`ImmutableStateError`／Story 上傳改非 background、`async with self`。
- **HOTFIX-003**：測驗 `generate_result` async、`upsert_user_vector`、Story `DEBUG_URL`。
- **HOTFIX-004**：Story 公開網址除錯與 `rx.image` 優化。
- Task 2 軌跡：**滑桿互動**，`tests/test_ui_event`。

### dotenv／PostgREST／後端耐受

- **HOTFIX-002**：`profiles` RLS、`ensure_user_profile`、42501／23503 與 `sql/profiles_rls.sql`。
- **db_service**：`_retry_on_stale_schema`、`PGRST205`／`PGRST204` 重試。
- **`get_matches`／RPC 過渡相容**：部署端曾存在 `get_safe_matches(match_threshold, query_vector)` 舊簽名之提示；以 deploy log 區分環境版本。

### frontend／backend mismatch

- **`get_safe_matches` 回傳欄位演進**：曾有 `matched_user_id`／`blocked_count`／衝突維度與現行 `user_id`／`distance`／`is_blurred`；整合測試與 **`TEST_CHECKLIST.md`** 需對齊。
- **seed 外鍵**：`profiles.id` 須對 `auth.users`；**`seed_test_users.py`** 改 JWT `sub`（見歷史 FIX）。

### HOTFIX LOG（全文歸檔）

<details>
<summary>展開：[HOTFIX-001]～[HOTFIX-004]、變更紀錄中 2026-05-05 所列 HOTFIX（與前文不重複細節可略）</summary>

- **[HOTFIX-001]**（2026-05-05）Story：`submit_story` 非背景 async、`async with self`、`rx.window_alert`。
- **[HOTFIX-002]**（2026-05-05）`sql/profiles_rls.sql`、`ensure_user_profile` UPSERT、`login_page`／`story_page` 對齊。
- **[HOTFIX-003]**（2026-05-05）測驗 async、`upsert_user_vector`、`DEBUG_URL`。
- **[HOTFIX-004]**（2026-05-05）Story 公開網址除錯、圖片渲染。

⚠️ **憲法級提醒**：禁止在事件處理器對 State 的非同步非法寫入；一律使用 Reflex 建議之 context manager 模式。
</details>

---

## DEV LOG

**原則**：Task 級交付節奏仍依《開發憲法》：設計 → 開發 → `tests/test_<feature>.py` → 更新本 BACKLOG／衝刺文件。

### 編年摘要（搬移自原「變更紀錄」）

| 日期 | 摘要 |
|------|------|
| 初版 | Task 1–3 |
| 產品化衝刺 | README、`run_all_tests`、`llm_gateway`、`test_db_connection` SKIP |
| MVP 2 規劃 | Task 6–9、憲法交付節奏 |
| Task 6 開發 | `sql/stories.sql`、`db_service`、 `/story`、`session_state`、測試擴充 |
| MVP 2 重整 | Task 5 `REMOVED/INTERNAL_ONLY`；北極狐壁壘主線 |
| Task 6／6.5 `[DONE]` | Storage、RLS、去 Token 化、`guard_protected_routes` |
| 2026-05-06 | Navbar、`/`→`/match`、`user_unlocks`、`create_unlock`、Task 8 獨立條目、`seed_test_users.py`＋PyJWT |

### Task 級筆記（精簡保留）

- **Task 7**：`get_safe_matches`、`match_wall`、攔截看板；RPC／卡片／Storage URL 串接；`tests/test_hater_logic.py`。
- **Task 7.5**：`nav_bar.py`、`login_page` 向量分流、`RootRedirectState`、說明並列於 **SPRINT** 類文件。
- **Task 9**（進行中）：解鎖 dialog、占位 `/unlocks`；**Task 8**（待開始）：結構化攻略與付費價值。

### 結構調整（本檔）

- **2026-05-08**：BACKLOG 由「連續 HOTFIX 混編」改為 **P0–P3 + HOTFIX ARCHIVE + DEV LOG**；衝刺與測試清單外掛獨立 markdown，以降低 AI 協作與交付混線。
