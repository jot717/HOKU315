# HOKU315 需求清單（BACKLOG）

狀態：`[TODO]` 未開始 · `[WIP]` 進行中 · `[DONE]` 已完成 · **`[REMOVED/INTERNAL_ONLY]`** 已自產品面下架（僅歷史／後台或程式相容保留，禁止再當作對外功能交付）

每項 **`[DONE]`**（或 MVP 2 各 Task 收口）前須滿足《開發憲法》第三章：**對應測試腳本** + 終端機驗證通過。

**目前**：**MVP 1** — **Task 1–Task 4 為 `[DONE]`**；**Task 5 為 `[REMOVED/INTERNAL_ONLY]`**（見該節）。整合驗收可執行 **`python -m tests.run_all_tests`**（無 Supabase 時雲端段 SKIP，exit 0）。**MVP 2：北極狐壁壘商業化** — **Task 6、6.5 為 `[DONE]`**（Auth／Session 自動化／stories／Storage）；**Task 7–Task 9 為 `[TODO]`**。

---

### 《開發憲法》交付節奏（MVP 2 每個 Task 必循）

1. **設計**：前後端與 **SQL／HTTP 接口** 定稿（可於本檔或 PR 描述留存）。  
2. **開發**：依設計實作，不留下一次性腳本於根目錄。  
3. **測試**：**獨立模組** `tests/test_<feature>.py`，可重複執行；無金鑰／無雲端時 **SKIP + exit 0**（與現有專案慣例一致），必要 E2E 則明訂環境變數。  
4. **交付**：更新本 BACKLOG 狀態、README 片段（若對外可見行為變更）。

**禁止**：根目錄與專案內任意位置堆置臨時垃圾檔；所有自動化測試集中在 **`tests/`**。

---

### MVP 2 憲法宣告（避雷 × 測試 × 產品形態）

1. **測試義務**：MVP 2 **每一個 Task（6–9）必須對應至少一個** `tests/` 內可重複執行之腳本（名稱於 Task 內訂明；可沿用／擴充既有檔名）。  
2. **避雷邏輯形態**：所有「避雷／不合適對象」處理必須是 **「靜默過濾 + 數據呈現」** — 後端完成向量與規則運算，前端以 **看板、計數、卡片狀態、解鎖旗標** 等展示；**嚴禁**再以即時 **聊天室、對話氣泡、問答式客服** 作為核心價值載體（與 Task 5 撤銷一致）。  
3. **LLM／攻略**：若產出文字，僅限 **結構化攻略、摘要、付費後解鎖內容**，不得回到「自由對話主流程」。
4. **Session／Auth（憲法級，Task 6.5 起）**：**嚴禁**在產品 UI 要求使用者手動貼上 Access Token。所有需 JWT 之功能（Story、配對牆、付費流等）**僅能**依賴 **`SessionState` 經登入自動取得並持久化之 session**（`rx.LocalStorage` 等）；未登入訪問受保護路由（如 **`/story`**、**`/match`**）一律 **重導向 `/login`**。

---

## [DONE] Task 1：20 維社交地雷維度定義與 `fox_logic.py` 實作

- **目標**：定義 20 維「社交地雷」語意維度，並在 `fox_logic.py` 中實作維度計算／映射邏輯（供測驗與向量管線使用）。  
- **驗收**：`fox_logic.SOCIAL_MINE_DIMENSIONS` / `generate_vector`；測試 `python -m tests.test_fox_logic`（與 `db_service._DIM`、`pg_vector_literal` 相容）已通過。

---

## [DONE] Task 2：Reflex 前端「狐狸性向測驗」組件（20 題滑桿介面）

- **目標**：以 Reflex 建立「狐狸性向測驗」UI，共 20 題，每題以滑桿（slider）操作。  
- **驗收**：`fox_quiz/fox_quiz.py` + `rxconfig.py`；自動化煙霧測試 `python -m tests.test_fox_quiz_smoke`。  
- **手動 UI 檢查清單**（啟動 `reflex run` 或 `python -m reflex run` 後）：  
  1. 首頁顯示標題「狐狸性向測驗」與 20 張題卡（題號 1–20）。  
  2. 每題可拖曳滑桿 0–1，放開後數值應保留（可改多題後捲動回第一題確認）。  
  3. 點「產生結果向量」後出現綠色提示，文案含「已產生 20 維向量」與前 5 維預覽。  
- **[DONE] 修復：滑桿即時互動性（Hotfix）**：`on_change` + `default_value`（移除 `value` 直綁）、`set_score_at` 支援 list/float、微分去重與 `throttle(32)`；壓測 `python -m tests.test_ui_event`。  
- **[DONE] Task 2.5：UI 體驗深度優化**：受控 `value` 綁定 `scores[i]` + `on_change`（`throttle(48)`）、滑桿主題色、結果區織光四維均值與霜鎧狐文案；壓測含 20 維同輪更新（仍僅 `tests/test_ui_event.py`）。

---

## [DONE] Task 3：向量寫入測試（將測驗結果透過 `db_service` 存入 Supabase）

- **目標**：將測驗產出之 20 維向量經 **`db_service.py`** 寫入 Supabase（`profiles` / `mine_vector`）。  
- **驗收**：`python -m tests.test_vector_persistence`（有有效 `DB_TEST_PROFILE_ID` 與 profile 時做讀寫斷言；否則 SKIP exit 0）；`fox_quiz` 之 `submit_quiz` 背景呼叫 `update_user_vector` 並於 UI 顯示成功／錯誤；`db_service.get_user_vector` / `parse_vector_value` 供讀回與測試。

---

## [DONE] Task 4：記憶聯調（`user_memories` + RAG Lite + `llm_gateway` 注入）

- **目標**：`db_service.insert_user_memory` / `match_user_memories` 與 `sql/user_memories.sql` 對齊；`LLMGateway.build_minefield_system_block` 合併 profile 與向量記憶；測試 `python -m tests.test_ai_memory`（無雲端或表未建時 SKIP，exit 0）。  
- **驗收**：PostgREST schema 暖機重試（`PGRST205` 等）已內建於 `db_service`；整合路徑可穩定通過。  
- **MVP 2 備註**：上述 **RAG／注入能力保留於後台與攻略生成鏈**，**不得**再綁定已撤銷之對話室主流程（見 Task 5）。

---

## [REMOVED/INTERNAL_ONLY] Task 5：Reflex 對話介面與個性化 LLM 整合（歷史）

- **原目標（已作廢）**：`/chat` 對話視窗、`build_chat_messages`、RAG 提示與規則式回覆等「對話式」體驗。  
- **現行決議**：  
  - **徹底廢除 `/chat` 作為產品介面**（不得再以「聊天室」作為 MVP 2 價值交付）。  
  - **相關邏輯轉入後台／非互動管線**（例如：向量記憶、攻略文案生成、批處理），由 Task 6–9 與憲法宣告規範之 **數據與解鎖** 形態承接。  
  - **嚴禁**產出 **答非所問、仿客服對話** 的聊天 UI；若程式庫中仍有路由或元件，僅允許作為 **INTERNAL_ONLY** 過渡，直至完全移除或改寫為非對話模組。  
- **驗收（歷史）**：曾以 `fox_quiz/chat_component.py`、`route="/chat"`、`reflex compile` 通過為紀錄；**不再作為 MVP 2 驗收依據**。

---

## MVP 2：北極狐壁壘商業化（戰術清單）

**主軸**：測驗向量 → **靜默避雷過濾** → **配對牆／攔截可視化** → **付費解鎖深度內容** → **端到端變現驗收**。  
**與 Task 5 切斷**：本 MVP **不以對話室為載體**；價值展現在 **儀表、計數、卡片、解鎖狀態與攻略交付**。  
**Session**：見 Task 6.5 — 全線功能依自動 Session，禁止手動 Token UI。

---

### [DONE] Task 6：Auth 與故事發布基礎

- **目標（已收口）**  
  - **`stories`** 表與 **`profiles`／真實 `user.id`** 綁定；Auth 與 **`SessionState.access_token`** 一致。  
  - **Storage 實傳**：`db_service.upload_to_supabase_storage` → bucket **`stories`**，路徑嚴格 **`{user_id}/{filename}`**。  
  - **SQL**：`sql/stories.sql` 含 **`storage.buckets`** 初始化與 **Storage RLS**（僅讀寫自己 UUID 前綴資料夾，防繞過前端直鏈原圖）。  
  - **SQL**：`sql/profiles_rls.sql` — **`profiles`** 之 **SELECT／INSERT／UPDATE** 限 **`auth.uid() = id`**（修正聯調 **42501**，並支撐 **`ensure_user_profile`**）。  
  - **後端**：`db_service.ensure_user_profile(access_token)` — **UPSERT + ignore_duplicates**，預設向量全 **0.5**，避免 **`stories`** **23503**。  
  - **UI**：`fox_quiz/story_page.py` — **先 Storage 成功，再寫入 DB**（**不再**含手動貼 Token；見 Task 6.5）；異步 state 見 **[HOTFIX-001]**。  
- **測試**  
  - `tests/test_story_auth.py`：DB 寫入與路徑規範。  
  - `tests/test_story_storage.py`：**1×1 PNG** 上傳並 **list** 驗證物件存在。  

---

### [DONE] Task 6.5：Supabase 真實 Auth 整合與去 Token 化

- **目標**  
  - **廢除**手動填寫 Access Token 的產品 UI；技術債清理：**已自 `fox_quiz/story_page.py` 移除** access_token 輸入框（見 HOTFIX LOG：去 Token 化查核）。  
  - **Email／密碼登入與註冊**：`fox_quiz/login_page.py`，成功後由 `db_service.auth_sign_in_email_password` / `auth_sign_up_email_password` 取得 token，並呼叫 **`ensure_user_profile`** 與 **`profiles`**／Auth 對齊。  
  - **Session 自動化**：`fox_quiz/session_state.py` 使用 **`rx.LocalStorage`**（鍵 `hok315_supabase_access` / `hok315_supabase_refresh`）持久化 **`access_token`**、**`refresh_token`**。  
  - **路由保護**：未登入或 token 無效時，**`/story`**、**`/match`** 於 **`on_load`** 執行 **`SessionState.guard_protected_routes`** → **`rx.redirect("/login")`**。  
  - **聯調前置**：部署須執行 **`sql/profiles_rls.sql`**（與 **[HOTFIX-002]**），避免 **42501／23503** 全鏈路崩潰。  
- **驗收**  
  - `python -m tests.test_auth_flow`：模組匯入／State 欄位煙霧；可選整合：設定 **`AUTH_TEST_EMAIL`**、**`AUTH_TEST_PASSWORD`**（連同 `SUPABASE_URL`、`SUPABASE_KEY`）時驗證登入 → token → `user_id_from_access_token`。  
  - `reflex compile` 通過。  

---

### [DONE] Task 7：北極狐配對牆與「攔截可視化」

- **目標**  
  - 後端 **`sql/match_logic.sql`**：RPC **`get_safe_matches(current_uid uuid)`** 已落地（`distance >= 1.2` 排除、`distance >= 0.7` 標記 `is_blurred=true`、回傳衝突最大維度 index/label 與 `blocked_count`）。  
  - 擴充 **`fox_quiz/match_wall.py`**：**配對牆** UI 已接上 RPC，並於 `/match` `on_load` 自動載入。  
  - **首頁（或配對牆主視圖）必須包含看板**：**「已攔截地雷對象總數」**（數字儀表，邏輯來自後端靜默過濾結果之聚合）。  
  - **憲法**：僅使用 **`SessionState`** 自動 session；**禁止**手動輸入 token。  
- **卡片機制（價值展現）**  
  - **照片**：預設 **高斯模糊**（CSS／等效）。  
  - **動態標註攔截原因**：例如 **「第 14 維度衝突」**（維度索引／標籤須與 `fox_logic` 維度定義可追溯對齊）。  
- **測試（必備）**  
  - `tests/test_hater_logic.py`：**給定向量對**可重現過濾／標記結果（含離線門檻與可選 RPC 欄位檢查）。  
  - `tests/test_match_wall_smoke.py`（建議新增）：Reflex 模組匯入、`match_wall` 狀態與看板欄位存在性（不強制啟動瀏覽器）。

---

### [TODO] Task 8：深度質料解鎖與付費牆

- **目標**  
  - **點擊解鎖**流程：狀態機（鎖定／已解鎖）、錯誤與重試策略。  
  - **解鎖後內容**：  
    - **清晰照片**（非模糊）。  
    - **AI 生成的「地雷對抗攻略」**（結構化短文／條目式，非聊天室往返）。  
  - **Stripe**：支付 **預留接口**（Checkout／Session／Webhook 占位與環境變數），確保 **變現路徑可串接**。  
  - **憲法**：付費與解鎖 API 僅帶 **自動 session** 之 JWT；**禁止**要求使用者貼 token。  
- **價值展現**  
  - 使用者為 **可驗證的增量資訊** 付費（清晰影像 + 攻略），而非為「聊天回合」付費。  
- **測試（必備）**  
  - `tests/test_unlock_content.py`（建議）：解鎖旗標、攻略欄位 mock／離線斷言。  
  - `tests/test_stripe_placeholder.py`（建議）：Webhook／session 建立 mock，無真金鑰時 SKIP exit 0。

---

### [TODO] Task 9：全量變現流（User Flow）驗收

- **目標**  
  - 從 **登入（自動 session）→ 測驗 → 配對／攔截可視化 → 付費解鎖** 的 **完整商業鏈條** 驗收。  
  - 涵蓋 **SKIP 規則**、**E2E 必要環境變數**、以及 **失敗場景**（無 Auth、無支付、無網路）之可重現行為。  
  - **憲法**：全鏈 **不得**出現手動 Access Token 輸入；登入態僅來自 **Task 6.5** 管線。  
- **測試（必備）**  
  - `tests/test_mvp2_monetization_flow.py`（或等價命名）：可為 **分段 scenario** 或 **單檔多步驟**，須寫入 `tests/` 並可由 **`python -m tests.run_all_tests`** 或文件化之一鍵指令執行。  
- **價值展現**  
  - 證明產品敘事為 **避雷決策 + 可視化 + 變現**，而非對話體驗。

---

## 下一階段建議（產品化之後）

1. **真 LLM 串接**：攻略生成走 **批次／on-demand 非對話 API**，輸出結構化內容；與 Task 8 解鎖捆綁。  
2. **向量記憶**：僅作為 **使用者畫像與攻略上下文**，不驅動前台聊天主流程。  
3. **Auth、配對、變現**：以 **MVP 2：北極狐壁壘商業化**（Task 6–9）為唯一主線。  
4. **觀測與成本**：記錄支付與生成成本；`user_memories` 索引見 `sql/user_memories.sql` 註解。  
5. **E2E**：Playwright 等可選；**Task 9** 為憲法級商業鏈條驗收口。

---

## 變更紀錄

| 日期 | 說明 |
|------|------|
| 初版 | 建立 Task 1–3 |
| 產品化衝刺 | README 快速啟動／數據流圖、`run_all_tests`、`llm_gateway` 五種語氣、`test_db_connection` 離線 SKIP |
| MVP 2 規劃 | 新增 Task 6–9（北極狐壁壘與變現管線）、憲法交付節奏；Task 6 `stories`／Auth 設計提案（待確認後開發） |
| Task 6 開發 | `sql/stories.sql`、`db_service` Auth／stories API、`/story` UI、`session_state`、`tests/test_story_auth`、`run_all_tests` 擴充；Task 6 標 `[WIP]` |
| MVP 2 戰術重整 | Task 5 標 `[REMOVED/INTERNAL_ONLY]`（廢 `/chat` 產品面）；MVP 2 更名「北極狐壁壘商業化」；Task 6–9 細化配對牆／攔截看板／付費攻略／全鏈驗收；憲法宣告（靜默過濾 + 數據呈現、每 Task 必備 tests） |
| Task 6 收尾 | Storage `upload_to_supabase_storage`、`sql/stories.sql` bucket+RLS、`story_page` 先傳後寫 DB、`tests/test_story_storage.py`；Task 6 `[DONE]` |
| Task 6.5／憲法 | `login_page`、`SessionState` LocalStorage、`guard_protected_routes` + `/login` 重導向、`/match` 占位保護、移除 `story_page` 手動 Token UI、`tests/test_auth_flow`；Task 7–9 註記「僅自動 session」 |
| 2026-05-05 | **[HOTFIX-001]** `story_page`：`submit_story` 改為非背景 async 事件、`async with self` 與 `uploading`／`rx.window_alert`（見 HOTFIX LOG） |
| 2026-05-05 | **[HOTFIX-002]** `profiles` 自動同步（後續擴充：`ensure_user_profile` UPSERT + `sql/profiles_rls.sql`，見 HOTFIX LOG） |
| 2026-05-05 | **系統全鏈路穩定性**：profiles RLS（42501）、Story FK（23503）、Reflex State（見 HOTFIX LOG 詳述）；Task 6／6.5 維持 **`[DONE]`** |
| 2026-05-05 | **[HOTFIX-003]** 測驗主流程 async 化（`generate_result`）+ `upsert_user_vector` 強制寫庫 + Story 成功輸出 `DEBUG_URL` |

---

## HOTFIX LOG

⚠️ 警告：『禁止在任何事件處理器中使用非同步直接賦值，必須使用上下文管理器。』

Task 6 與 Task 6.5 狀態：**`[DONE]`**（含下列修復後之交付節奏）。

---

### [HOTFIX-001] ImmutableState／異步 UI 鎖死（Story 上傳）

**日期**：2026-05-05  

**背景與診斷（Task 6.5 聯調）**  

- Reflex 在 **`@rx.event(background=True)`** 背景任務中對 **`StoryState`** 的直接賦值會觸發 **`ImmutableStateError`**（於 **`StateProxy`** 路徑非法寫入）。  
- 表象：**前端紅字／例外串流**、部分環境 **按鈕卡住／事件未完成**，使用者誤判為「Token／網路」問題。

**修正範圍（應用層）**  

| 層級 | 作法 |
|------|------|
| **`story_page.py`** | **`submit_story`** 改為 **`async def` + `@rx.event`（非 background）**；凡 **`uploading`**、**`status_msg`** 等 state，一律 **`async with self:`** 區塊內更新。 |
| **`story_page.py`** | **`on_image_drop`**：在 **`await` 讀檔結束後**，以 **`async with self:`** 寫入 **`image_basename`**／**`pending_image_b64`**／**`upload_hint`**。 |
| **UX** | **`uploading`** + 按鈕 **`disabled`**／文案「上傳中…」；失敗時 **`return rx.window_alert(...)`** 並 **`uploading=False`**。 |

**驗收**  

- `python -m reflex compile` 通過。  
- 手動：`/story` 上傳儲存不中斷、無 **`ImmutableStateError`**。  

---

### [HOTFIX-002] RLS **42501**、FK **23503** 與 Profile 自動同步（資料層 + 後端）

**日期**：2026-05-05  

**背景與診斷（Task 6.5 聯調）**  

1. **42501（RLS）**：`public.profiles` 若 **未開放 authenticated 對「自己的列」INSERT／UPDATE**，後端以使用者 JWT 呼叫 **`ensure_*`** 會被拒絕，新用戶無法自建 profile。  
2. **23503（FK）**：`stories.user_id` **REFERENCES profiles(id)**；profile 列不存在時，Story INSERT 失敗。  
3. 與 [HOTFIX-001] 疊加時，易誤判為單一前端問題；需 **SQL + 後端 + 前端雙重保險** 一併收口。

**修正範圍（資料庫）**  

| 檔案 | 作法 |
|------|------|
| **`sql/profiles_rls.sql`**（新增） | **`ENABLE ROW LEVEL SECURITY`**；**`profiles_select_own`**（`USING auth.uid() = id`）、**`profiles_insert_own`**（**`WITH CHECK (auth.uid() = id)`**）、**`profiles_update_own`**（**USING + WITH CHECK**）；並 **`GRANT SELECT, INSERT, UPDATE … TO authenticated`**。 |
| **`sql/stories.sql`**（註解） | 提示先跑 **`profiles_rls.sql`**；既有 **`stories_insert_own`** 等 policy 維持 **`auth.uid() = user_id`**，對 **已驗證用戶** 開放 INSERT。 |

**修正範圍（後端 `db_service.py`）**  

- **`ensure_user_profile(access_token)`**（主入口）：以 **`upsert(..., on_conflict=id, ignore_duplicates=True)`** 原子補列 — **無列則插入** `{ id, mine_vector=全 0.5×20 }`；**已存在則不覆寫向量**（避免沖掉測驗寫入）。  
- **`ensure_profile_exists`**：保留為 **別名**，呼叫 **`ensure_user_profile`**。

**修正範圍（應用層）**  

| 檔案 | 作法 |
|------|------|
| **`login_page.py`** | 登入／註冊成功取得 token 後 **`ensure_user_profile(token)`**（與 Auth 瞬間對齊）。 |
| **`story_page.py`** | **無手動 Token 輸入框**（去 Token 化已物理移除）；**儲存前雙重呼叫**：解碼圖片後 **`ensure_user_profile`** 一次；**`create_story` 前**再 **`ensure_user_profile`** 一次（防競態／缺列）。 |

**驗收（UAT）**  

- 於 Supabase 執行 **`sql/profiles_rls.sql`**（及既有 **`sql/stories.sql`**）。  
- 註冊全新帳號 → **不做測驗** → **`/story`** 上傳圖片 → **Storage + stories** 成功，無 **42501／23503**。  

---

### [HOTFIX-003] 測驗事件 Async 全鏈路修補 + 寫庫保證 + Story Debug URL

**日期**：2026-05-05  

**背景與診斷**  

- 測驗事件於舊流程中以背景事件執行，歷次聯調已多次出現 `ImmutableStateError` 模式（跨頁面重現）。
- `generate_result` 路徑缺乏「必然寫庫」保證時，可能只在前端得到結果文案，造成資料與 UI 脫節。

**修正範圍（應用層 + 服務層）**  

| 檔案 | 作法 |
|------|------|
| **`fox_quiz/fox_quiz.py`** | 新增並切換主事件為 **`generate_result`（`async def`）**；事件內 state 更新全以 **`async with self:`** 寫入。保留 `submit_quiz` 為相容別名。 |
| **`db_service.py`** | 新增 **`upsert_user_vector(access_token, user_vector)`**，以 JWT + UPSERT（`on_conflict=id`）保證向量資料實際落地（存在更新，不存在建立）。 |
| **`fox_quiz/fox_quiz.py`** | 測驗送出時先 `ensure_user_profile(token)`，再 `upsert_user_vector(token, vec)`，避免「只前端計算未落庫」。 |
| **`fox_quiz/story_page.py`** | Story 成功回調增加 `print(f\"DEBUG_URL: {public_url}\")`，直接在 terminal 輸出檔案網址供 UAT-02 調試。 |

---

### [HOTFIX-004] story_page.py 實體網址輸出與 UI 渲染優化
**日期**：2026-05-05  
**背景**：UAT-02 需要快速驗證 Storage 上傳是否成功，且原有 `img` 元件在部分瀏覽器緩存下顯示異常。  
**修正**：在 `create_story` 成功後於終端機輸出 `DEBUG_URL`，並優化前端 `rx.image` 的 src 處理邏輯。

---

### [HOTFIX-005] RPC 向量解析語法修復 (Cast vs Subscript)
**日期**：2026-05-05  
**背景與診斷**：  
- 在 Task 7 實作 `get_safe_matches` RPC 時，嘗試直接對 `vector` 類型使用 `[gs]` 下標取值導致 SQL ERROR `42804: cannot subscript type vector`。  
- Supabase 環境未安裝 `vector_to_float8_array` 擴充函數，導致轉換失敗（ERROR `42883`）。  
**修正範圍（SQL）**：  
- 修改 `sql/match_logic.sql`，改用原生 PostgreSQL 強制轉型：`cast(trim(both '[]' from vec::text) as float8[])`。  
- 此做法將向量轉為標準 float8 陣列，確保 `generate_series` 能正確比對 20 維度衝突。  
**驗收**：Supabase SQL Editor 執行成功，`get_safe_matches` 可正確回傳 `conflict_dim_label`。

**驗收（UAT-02）**  

- 啟動 `reflex run`，完成一次測驗送出，確認資料庫 profiles 向量已更新（UPSERT）。
- 於 `/story` 成功上傳後，終端機應可見 `DEBUG_URL: ...` 輸出。
