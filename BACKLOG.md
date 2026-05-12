# HOKU315 BACKLOG

**Workflow（AI-native）**：衝刺計畫見 [`SPRINT_PLAN.md`](SPRINT_PLAN.md)、日誌見 [`SPRINT_LOG.md`](SPRINT_LOG.md)；配對牆驗收見 [`TEST_CHECKLIST.md`](TEST_CHECKLIST.md)；資料庫套用軌跡見 [`sql/DEPLOY_LOG.md`](sql/DEPLOY_LOG.md)；**Debug／UAT 證據收集**見 [**`DEBUG_GUIDE.md`**](DEBUG_GUIDE.md)；**證據資產化目錄**見 [**`debug_evidence/README.md`**](debug_evidence/README.md)；**AI／P0 patch 約束**見 [**`DEBUG_POLICY.md`**](DEBUG_POLICY.md)；**Repo 分層**見 [**`REPO_ARCHITECTURE.md`**](REPO_ARCHITECTURE.md)；**介面契約**見 [**`ARCHITECTURE_CONTRACT.md`**](ARCHITECTURE_CONTRACT.md)；**流程護欄**見 [**`ops/process/RULES.md`**](ops/process/RULES.md)；**治理層級**見 [GOVERNANCE HIERARCHY](#governance-hierarchy)。產品治理仍依根目錄 **`DEVELOPMENT_CONSTITUTION.md`**。

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
- **除錯 SOP**：HOTFIX／UAT 前先依 [**`DEBUG_GUIDE.md`**](DEBUG_GUIDE.md) 收集 Console／Network／Backend／SQL 證據。
- **證據資產化**：嚴重／重複性事故將原始證據封存於 **`debug_evidence/YYYY-MM-DD-slug/`**（見 [`debug_evidence/README.md`](debug_evidence/README.md)）；AI patch 遵守 [**`DEBUG_POLICY.md`**](DEBUG_POLICY.md)。

### Stabilization Sprint (2026-W01)

**Scope**：本 Sprint **僅處理 P0 穩定化**；**禁止**新增 Stripe／coins／成長型功能（見下方 DEV LOG）。

Definition of Done:

* /story 穩定
* /match 穩定
* /unlock 穩定
* 無 malformed array literal
* 無 Reflex runtime mismatch
* 無 package dependency crash
* 無 console error
* Mobile 可正常使用

任務拆解與核銷見 [`SPRINT_PLAN.md`](SPRINT_PLAN.md)；UAT 勾選見 [`TEST_CHECKLIST.md`](TEST_CHECKLIST.md) 之 **MATCH FLOW UAT**；除錯證據流見 [`DEBUG_GUIDE.md`](DEBUG_GUIDE.md)；事故回放目錄見 [`debug_evidence/README.md`](debug_evidence/README.md)。

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

**Sprint 對齊（2026-W01）**：以 [`SPRINT_PLAN.md`](SPRINT_PLAN.md) — **Stabilization**（/story → /match → /unlock）為準；非 P0 項目（Task 8 攻略、Task 9 真實付費串接、成長功能）**暫停至本 Sprint DoD 達成**。每日進度見 [`SPRINT_LOG.md`](SPRINT_LOG.md)。

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

## AI INCIDENT SYSTEM v1

端到端骨架：**Observe → Evidence → Replay → Diagnose → Suggest →（Self-heal 預留）**。流程說明見 [`docs/AI_PATCH_FLOW.md`](docs/AI_PATCH_FLOW.md)、回放見 [`docs/REPLAY_GUIDE.md`](docs/REPLAY_GUIDE.md)。

- **Observe**：異常觀測與路由／操作記錄（對齊 [`DEBUG_GUIDE.md`](DEBUG_GUIDE.md)）。
- **Evidence**：`debug_evidence/`、`scripts/create_incident.py`、`scripts/collect_runtime.py`。
- **Replay**：`ai/replay/replay_incident.py`（現為 mock；尚相容 `python replay/replay_incident.py`）、[`docs/REPLAY_GUIDE.md`](docs/REPLAY_GUIDE.md)。
- **Diagnose**：`ai/taxonomy/error_taxonomy.yaml`、`python -m ai.diagnosis.root_cause_engine`。
- **Suggest**：`scripts/generate_patch_context.py`、`ai/prompt_templates/`；自動化補丁占位：`ai/self_heal/`（見 **[SELF-HEALING SYSTEM v1](#self-healing-system-v1)**）。
- **Patch Policy**：`ai/patch_policy/`（占位）、[`DEBUG_POLICY.md`](DEBUG_POLICY.md)、[`docs/AI_PATCH_FLOW.md`](docs/AI_PATCH_FLOW.md)。

### INCIDENT SYSTEM v1-lite

最小閉環 **Observe → Mock replay → Taxonomy lookup**：見 [`docs/INCIDENT_SYSTEM_LITE.md`](docs/INCIDENT_SYSTEM_LITE.md)（`runtime.json`、`replay_incident.py` 位置參數、`root_cause_engine --error-type`）。

---

## REGRESSION GATE

所有 **deploy／hotfix** 必須通過：

```powershell
pytest tests/regression/
```

未通過 → **禁止部署**。CI 見 [`.github/workflows/regression.yml`](.github/workflows/regression.yml)。細節見 [`tests/regression/README.md`](tests/regression/README.md)。

等同：`python scripts/run_regression.py`（會呼叫 `python -m pytest tests/regression/`）。

---

## SELF-HEALING SYSTEM v1

能力：

- **Suggest → Patch generation**：`ai/suggestion/suggest_engine.py`（taxonomy）、`ai/self_heal/patch_engine.py`、`ai/self_heal/suggest_bridge.py`
- **Manual review patch**：`ai/self_heal/apply_patch.py`（僅列印；不自動改檔）
- **Regression gate（套用前）**：[`tests/regression/`](tests/regression/)，`scripts/run_regression.py`
- **Learning log**：`ai/self_heal/learning_log.py` → `ai/self_heal/logs/fix_log.json`

狀態：

- **SAFE MODE（無自動 deploy／無自動套用程式 diff）**。細見 [`ai/self_heal/README.md`](ai/self_heal/README.md)。

---

## REPO LAYERING v1

完成：

- **PRODUCT／AI／OPS** 邏輯分層與目錄對照（見 [`REPO_ARCHITECTURE.md`](REPO_ARCHITECTURE.md)、[`product/`](product/)、[`ops/`](ops/)、[`ai/incident/README.md`](ai/incident/README.md)）。
- **Replay** 實作歸位 **`ai/replay/`**；根目錄 **`replay/`** 保留 shim。
- **無搬移** `scripts/`、`tests/`、`docs/`（維持 `pytest`、`python -m tests.*` 與 CI 相容）。

---

## INTERFACE STABILIZATION v1

完成：

- **product／ai／ops** 三層入口定義：`product/INTERFACE.md`、`ai/INTERFACE.md`、`ops/INTERFACE.md`
- **不改程式**，僅建立契約層：[`ARCHITECTURE_CONTRACT.md`](ARCHITECTURE_CONTRACT.md)
- **系統邊界**與 [`REPO_ARCHITECTURE.md`](REPO_ARCHITECTURE.md) 對齊

---

## PROCESS ENFORCEMENT v1

System-level rules（詳 [`ops/process/RULES.md`](ops/process/RULES.md)）：

- **BACKLOG** 先於實作規劃新功能／可追蹤條目  
- **SPRINT** 對應可執行衝刺（見 [`SPRINT_PLAN.md`](SPRINT_PLAN.md)、[`SPRINT_LOG.md`](SPRINT_LOG.md)）  
- **REGRESSION** 通過方視為 DONE 門檻之一（`pytest tests/regression/`）  
- 工作流：**BACKLOG → SPRINT → IMPLEMENT → TEST → LOG**  
- 輕量檢查：`python ops/hooks/check_process.py`

---

## MATCH FLOW v1

- **MVP matching system**：規格 [`backlog/BACKLOG_MATCH_FLOW_v1.md`](backlog/BACKLOG_MATCH_FLOW_v1.md)
- **rule-based scoring** 草案：[`product/match/match_logic.md`](product/match/match_logic.md)
- **state / flow**：[`product/match/state_model.md`](product/match/state_model.md)、[`product/match/product_flow.md`](product/match/product_flow.md)
- **Sprint 2026-W02**：[`backlog/SPRINT_MATCH_FLOW_v1.md`](backlog/SPRINT_MATCH_FLOW_v1.md)

---

## HOTFIX ARCHIVE

此區僅封存已發生之緊急修復與根因類項，避免與進行中需求混線。**本 Sprint 內每一筆程式面修復仍須同步更新本節與 [`SPRINT_LOG.md`](SPRINT_LOG.md)。**

### 流程備忘（2026-W01 Stabilization）

- **凍結**：Stripe、coins 商品化、P2 成長功能 — 待 P0 Stabilization Sprint **Definition of Done** 達成後再排入 P1／P2。

### HOTFIX: 建立標準除錯證據流

* **問題**：

  缺少統一 debug workflow，
  導致 HOTFIX 容易失控。

* **修正**：

  建立 **`DEBUG_GUIDE.md`**

* **結果**：

  後續 AI／人工修復可依固定流程進行。

### HOTFIX: 建立 debug evidence 資產化

* **問題**：

  缺少事故證據保存，
  導致 AI 重複修 bug。

* **修正**：

  建立 **`debug_evidence/`**
  與 **`DEBUG_POLICY.md`**

* **結果**：

  每次事故皆可追蹤與回放。

### HOTFIX: Incident Template Generator

* **問題**：

  debug_evidence 仍需手動建立。

* **修正**：

  建立 **`scripts/create_incident.py`**。

* **結果**：

  每次事故可快速標準化建立。

### HOTFIX: 移除 Reflex runtime state 版本追蹤

* **問題**：
  `.states/*.pkl` 被 git 追蹤

* **風險**：
  runtime cache 汙染與跨機器衝突

* **修正**：

  1. `.gitignore` 加入 `.states/`、`*.pkl`
  2. `git rm --cached` 移除版本控制（**不刪除**本地檔案）

* **結果**：
  Reflex runtime state 不再污染 repository

### HOTFIX: Reflex nested p hydration warning

* **問題**：

  React hydration warning：

  `<p> cannot be a descendant of <p>`

* **根本原因**：

  `rx.callout` 與 `rx.text` 同時生成 `<p>`

* **修正**：

  1. 移除 nested `rx.text`（`rx.callout` 改傳字符串 + `white_space` 於 `style`）
  2. 其它易與 Badge／Card／段落上下文衝突之 `rx.text` 改 `as_="span"`

* **結果**：

  hydration warning 消失

  console 恢復正常

### malformed array literal／vector／RPC

- **FIX — `get_safe_matches` RPC vector parsing**：舊版 `string_to_array`／`::text` 與 pgvector `"[...]"` 衝突；改為原生 `vector <-> vector`／正確字面量傳参。
- **FIX — `mine_vector` 廢止**：統一 `profiles.vector`；種子／`db_service` 欄位預設與文案對齊。
- **FIX — RPC 傳入 vector 格式**：禁止 CSV；統一 `to_pgvector`／`"[...]"`；呼叫前可比對 `DEBUG_VECTOR` 輸出。
- **HOTFIX-005（歷史）**：RPC 曾以 `vec::text`／`float8[]` 繞過下標限制；已由 pgvector 原生路徑取代（歷史紀錄保留）。

### Reflex runtime（async／State）

- **HOTFIX（nested `<p>`）**：`fox_quiz/fox_quiz.py` 之 `rx.callout` 改以字串為唯一子內容；`match_wall`／`login`／`story`／`unlocks` 等處對易巢狀段落的 `rx.text` 設 `as_="span"`。詳見上節 **「HOTFIX: Reflex nested p hydration warning」**。
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

### DEV LOG — Stabilization Sprint 啟動

* **原因**：
  近期發生 pgvector / Reflex / package mismatch / runtime crash

* **決策**：
  暫停新功能開發，優先穩定核心流程

* **範圍**：
  /story → /match → /unlock

* **暫停**：
  Stripe / coins / growth feature

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
| 2026-05-08 | **BACKLOG** 分層（P0–P3 + ARCHIVE + DEV LOG）；Workflow 外掛 SPRINT／TEST／`DEPLOY_LOG` |
| 2026-05-08 | **Stabilization Sprint (2026-W01)** 啟動：凍結 Stripe／coins／growth；P0 DoD 見 **P0 — STABILIZATION** |
| 2026-05-09 | **HOTFIX**：Reflex nested `<p>`／`rx.callout` hydration；見 **HOTFIX ARCHIVE** |
| 2026-05-10 | **流程**：建立 **`DEBUG_GUIDE.md`**（標準除錯證據流＋HOTFIX SOP）；見 **HOTFIX ARCHIVE** |
| 2026-05-11 | **資產化**：建立 **`debug_evidence/`**、`DEBUG_POLICY.md`；見 **HOTFIX ARCHIVE** |
| （rolling） | **MATCH FLOW v1** 產品初始化文件：`backlog/`、`product/match/*.md` |

### Task 級筆記（精簡保留）

- **Task 7**：`get_safe_matches`、`match_wall`、攔截看板；RPC／卡片／Storage URL 串接；`tests/test_hater_logic.py`。
- **Task 7.5**：`nav_bar.py`、`login_page` 向量分流、`RootRedirectState`、說明並列於 **SPRINT** 類文件。
- **Task 9**（進行中）：解鎖 dialog、占位 `/unlocks`；**Task 8**（待開始）：結構化攻略與付費價值。

### 結構調整（本檔）

- **2026-05-08**：BACKLOG 由「連續 HOTFIX 混編」改為 **P0–P3 + HOTFIX ARCHIVE + DEV LOG**；衝刺與測試清單外掛獨立 markdown，以降低 AI 協作與交付混線。
- **2026-05-08**：啟動 **Stabilization Sprint (2026-W01)**，`SPRINT_PLAN.md`／`TEST_CHECKLIST.md`（MATCH FLOW UAT）對齊；凍結非 P0 新功能直至 DoD。

---

## GOVERNANCE HIERARCHY

**Constitution → Rules → Hooks**

| 層級 | 角色 |
|------|------|
| **Constitution** | 理念與原則 — [`DEVELOPMENT_CONSTITUTION.md`](DEVELOPMENT_CONSTITUTION.md) |
| **Rules** | 可執行之流程定義 — [`ops/process/RULES.md`](ops/process/RULES.md) |
| **Hooks** | 機械化檢查（檔案存在、回歸指令）— [`ops/hooks/`](ops/hooks/) |

---

## PRODUCT DIRECTION CORRECTION v1

MATCH → UNLOCK → INSIGHT

Deprecated:

MATCH → CHAT

---

## FLOW CONSISTENCY SYSTEM v1

Goal:

Prevent architecture drift between MATCH / UNLOCK / future flows.

Introduced:

- FLOW_CONTRACT
- flow_registry
- shared flow validation

---

## INSIGHT ENGINE v1

Dynamic compatibility insight generation.

---

## FLOW INTEGRATION v1

Unified orchestration for:

MATCH → UNLOCK → INSIGHT

---

## APP FLOW BINDING NOTE

Current phase:

runtime-side integration preparation only.

Actual fox_quiz UI binding

will be implemented in future APP UI INTEGRATION sprint.

---

## APP UI INTEGRATION v1

First clickable insight experience.

---

## INSIGHT EXPERIENCE v1

Emotional AI insight UX layer.

---

## USER PROFILE SYSTEM v1

- local editable profile
- local persistence
- match flow binding

---

## PHASE 1 FINALIZATION

- insight UX v2
- session memory
- UAT system
- phase freeze preparation

---

# APP SHELL REPLACEMENT v1

Consumer-facing product shell replacement initiated.

Legacy engineering/demo shell is being deprecated.

---

## PRODUCT CONSTITUTION ACTIVE

Product direction is governed by:

[`ops/product/PRODUCT_CONSTITUTION.md`](ops/product/PRODUCT_CONSTITUTION.md)

---

## FOX ROADMAP ACTIVE

Product roadmap moved to:

[`ops/product/FOX_ROADMAP.md`](ops/product/FOX_ROADMAP.md)

---

## FOX PRESENCE v1 ACTIVE

Fox guardian tone and narration layer implementation started.

---

## FOX IMMERSION SYSTEM v1 ACTIVE

Immersive guardian world shell (fox presence, signal scan, dream-world layout) — see [`backlog/BACKLOG_FOX_IMMERSION_SYSTEM_v1.md`](backlog/BACKLOG_FOX_IMMERSION_SYSTEM_v1.md).

---

## FOX MEMORY SYSTEM v1 ACTIVE

Local rule-based guardian memory (`runtime_state/fox_memory.json`) — see [`backlog/BACKLOG_FOX_MEMORY_SYSTEM_v1.md`](backlog/BACKLOG_FOX_MEMORY_SYSTEM_v1.md).

---

## FOX SIGNAL GUARD v1 ACTIVE

Signal guard mechanism (risk evaluation + guardian warning card) — see [`backlog/BACKLOG_FOX_SIGNAL_GUARD_v1.md`](backlog/BACKLOG_FOX_SIGNAL_GUARD_v1.md).

---

## PHASE1 UX RESTRUCTURE v1 ACTIVE

**TYPE:** PRODUCT DIRECTION LOCK — guardian hierarchy + copy only (**SAFE MODE**; no backend / DB / auth / vector / pipeline changes).  
**UX law:** [`ops/product/GUARDIAN_UX_CONSTITUTION.md`](ops/product/GUARDIAN_UX_CONSTITUTION.md)  
**UAT:** [`ops/uat/PHASE1_UX_RESTRUCTURE_NOTES.md`](ops/uat/PHASE1_UX_RESTRUCTURE_NOTES.md)  
**Backlog / sprint:** [`backlog/BACKLOG_PHASE1_UX_RESTRUCTURE_v1.md`](backlog/BACKLOG_PHASE1_UX_RESTRUCTURE_v1.md), [`backlog/SPRINT_PHASE1_UX_RESTRUCTURE_v1.md`](backlog/SPRINT_PHASE1_UX_RESTRUCTURE_v1.md)

---

## PRODUCT CORE REALIGNMENT v1 ACTIVE

**TYPE:** PRODUCT REALIGNMENT SPRINT — direction lock (docs + roadmap + deprecated language; **no** removal of guardian UX / fox / insight flow; **no** backend implementation).  
**Core:** AI-native **SNS guardian network** — social signal intelligence, hater / dangerous interaction detection, interaction risk; fox = persona + guardian UX layer.  
**Docs:** [`ops/product/CORE_PRODUCT_REALIGNMENT.md`](ops/product/CORE_PRODUCT_REALIGNMENT.md), [`ops/product/SOCIAL_SIGNAL_ARCHITECTURE.md`](ops/product/SOCIAL_SIGNAL_ARCHITECTURE.md), [`ops/product/HATER_SIGNAL_MODEL.md`](ops/product/HATER_SIGNAL_MODEL.md)  
**UAT:** [`ops/uat/PRODUCT_DIRECTION_RESET_NOTES.md`](ops/uat/PRODUCT_DIRECTION_RESET_NOTES.md)  
**Backlog / sprint:** [`backlog/BACKLOG_PRODUCT_CORE_REALIGNMENT_v1.md`](backlog/BACKLOG_PRODUCT_CORE_REALIGNMENT_v1.md), [`backlog/SPRINT_PRODUCT_CORE_REALIGNMENT_v1.md`](backlog/SPRINT_PRODUCT_CORE_REALIGNMENT_v1.md)

---

## STATE SANITIZATION HOTFIX v1 ACTIVE

**TYPE:** RUNTIME STABILITY HOTFIX — Reflex `@rx.var` / list coercion / session JSON safety; **no** new features or routes.  
**UAT:** [`ops/uat/STATE_SANITIZATION_RUNTIME_UAT.md`](ops/uat/STATE_SANITIZATION_RUNTIME_UAT.md)  
**Backlog / sprint:** [`backlog/BACKLOG_STATE_SANITIZATION_HOTFIX_v1.md`](backlog/BACKLOG_STATE_SANITIZATION_HOTFIX_v1.md), [`backlog/SPRINT_STATE_SANITIZATION_HOTFIX_v1.md`](backlog/SPRINT_STATE_SANITIZATION_HOTFIX_v1.md)

---

## TARGET SIGNAL PROFILE v1 ACTIVE

**TYPE:** CORE PRODUCT LOOP FIX — named **target observation entity** (`/target`) + local JSON + user/target overlap in insight; **no** SNS / vectors / auth.  
**Docs:** [`ops/product/TARGET_SIGNAL_CONSTITUTION.md`](ops/product/TARGET_SIGNAL_CONSTITUTION.md), [`ops/product/TARGET_ANALYSIS_FLOW.md`](ops/product/TARGET_ANALYSIS_FLOW.md), [`ops/product/TARGET_PROFILE_SCHEMA.md`](ops/product/TARGET_PROFILE_SCHEMA.md)  
**UAT:** [`ops/uat/TARGET_SIGNAL_PROFILE_UAT.md`](ops/uat/TARGET_SIGNAL_PROFILE_UAT.md)  
**Backlog / sprint:** [`backlog/BACKLOG_TARGET_SIGNAL_PROFILE_v1.md`](backlog/BACKLOG_TARGET_SIGNAL_PROFILE_v1.md), [`backlog/SPRINT_TARGET_SIGNAL_PROFILE_v1.md`](backlog/SPRINT_TARGET_SIGNAL_PROFILE_v1.md)

---

## RELATIONSHIP SIGNAL SIMULATION v1 ACTIVE

**TYPE:** RELATIONSHIP INTELLIGENCE FOUNDATION — synthetic **interaction archetypes** + overlap simulation; **no** SNS / multi-user / vectors / embeddings.  
**Docs:** [`ops/product/RELATIONSHIP_INTELLIGENCE_CONSTITUTION.md`](ops/product/RELATIONSHIP_INTELLIGENCE_CONSTITUTION.md), [`ops/product/RELATIONSHIP_ARCHETYPE_MODEL.md`](ops/product/RELATIONSHIP_ARCHETYPE_MODEL.md), [`ops/product/INTERACTION_SIGNAL_ONTOLOGY.md`](ops/product/INTERACTION_SIGNAL_ONTOLOGY.md)  
**UAT:** [`ops/uat/RELATIONSHIP_SIGNAL_SIMULATION_UAT.md`](ops/uat/RELATIONSHIP_SIGNAL_SIMULATION_UAT.md)  
**Backlog / sprint:** [`backlog/BACKLOG_RELATIONSHIP_SIGNAL_SIMULATION_v1.md`](backlog/BACKLOG_RELATIONSHIP_SIGNAL_SIMULATION_v1.md), [`backlog/SPRINT_RELATIONSHIP_SIGNAL_SIMULATION_v1.md`](backlog/SPRINT_RELATIONSHIP_SIGNAL_SIMULATION_v1.md)

---

## SIGNAL INTELLIGENCE ENGINE v1 ACTIVE

**TYPE:** RULE-BASED SIGNAL INTELLIGENCE — first interpretive layer (`infer_signal_risks`); **no** LLM / embeddings / vector search / SNS / agents.  
**Docs:** [`ops/product/SIGNAL_INTELLIGENCE_CONSTITUTION.md`](ops/product/SIGNAL_INTELLIGENCE_CONSTITUTION.md), [`ops/product/SIGNAL_RISK_ONTOLOGY.md`](ops/product/SIGNAL_RISK_ONTOLOGY.md), [`ops/product/SIGNAL_INFERENCE_MODEL.md`](ops/product/SIGNAL_INFERENCE_MODEL.md)  
**UAT:** [`ops/uat/SIGNAL_INTELLIGENCE_ENGINE_UAT.md`](ops/uat/SIGNAL_INTELLIGENCE_ENGINE_UAT.md)  
**Backlog / sprint:** [`backlog/BACKLOG_SIGNAL_INTELLIGENCE_ENGINE_v1.md`](backlog/BACKLOG_SIGNAL_INTELLIGENCE_ENGINE_v1.md), [`backlog/SPRINT_SIGNAL_INTELLIGENCE_ENGINE_v1.md`](backlog/SPRINT_SIGNAL_INTELLIGENCE_ENGINE_v1.md)

---

## SIGNAL SYSTEM CONSOLIDATION v1 ACTIVE

**TYPE:** SIGNAL ARCHITECTURE CONSOLIDATION — unify existing `/profile`, `/quiz`, `/insight`, memory, and signal wording (**SAFE MODE**; **no** new onboarding route; **no** SNS / vector / auth implementation).  
**Docs:** [`ops/product/SIGNAL_SYSTEM_CONSTITUTION.md`](ops/product/SIGNAL_SYSTEM_CONSTITUTION.md), [`ops/product/SIGNAL_PROFILE_SCHEMA.md`](ops/product/SIGNAL_PROFILE_SCHEMA.md), [`ops/product/SIGNAL_FLOW_ARCHITECTURE.md`](ops/product/SIGNAL_FLOW_ARCHITECTURE.md), [`ops/product/SIGNAL_INPUT_AUDIT.md`](ops/product/SIGNAL_INPUT_AUDIT.md), [`ops/product/SIGNAL_STATE_MAPPING.md`](ops/product/SIGNAL_STATE_MAPPING.md)  
**UAT:** [`ops/uat/SIGNAL_SYSTEM_CONSOLIDATION_UAT.md`](ops/uat/SIGNAL_SYSTEM_CONSOLIDATION_UAT.md)  
**Backlog / sprint:** [`backlog/BACKLOG_SIGNAL_SYSTEM_CONSOLIDATION_v1.md`](backlog/BACKLOG_SIGNAL_SYSTEM_CONSOLIDATION_v1.md), [`backlog/SPRINT_SIGNAL_SYSTEM_CONSOLIDATION_v1.md`](backlog/SPRINT_SIGNAL_SYSTEM_CONSOLIDATION_v1.md)

---

## PHASE1 UAT FLOW FIX v2 ACTIVE

**TYPE:** UX RECOVERY SPRINT — onboarding + journey clarity (not visual polish).  
See [`backlog/BACKLOG_PHASE1_UAT_FLOW_FIX_v2.md`](backlog/BACKLOG_PHASE1_UAT_FLOW_FIX_v2.md), UAT script [`ops/uat/PHASE1_UAT_SCRIPT.md`](ops/uat/PHASE1_UAT_SCRIPT.md), UX constitution [`ops/product/UAT_EXPERIENCE_CONSTITUTION.md`](ops/product/UAT_EXPERIENCE_CONSTITUTION.md).

