# Sprint Log

## 2026-05-16

### DONE

* **PHASE1-G PROJECT GOVERNANCE & PRODUCT CLARITY v1**: `docs/active/product/PRODUCT_MASTER.md`, `REPO_GOVERNANCE_RULES.md`, `docs/active/governance/MASTER_BACKLOG.md`, `docs/active/uat/UAT_MASTER_GUIDE.md`; README indexes; `docs/deprecated/archive/` + `backlog/archive/`; home guest/account CTAs; login/nav clarity.

* **PHASE1-F MATCH CREDIBILITY SYSTEM v1**: social energy match archetypes, `match_rhythm_engine.py`, match wall + insight weakness link; docs + regression.

* **PHASE1-D UX INTELLIGENCE LAYER v1**: interaction pressure ontology, `ux_intelligence_engine.py`, insight/match copy upgrade; fox observer rebalance.

* **MATCH WALL COMPILE HOTFIX v1** + **REMOVE PREMATURE SNS LAYER v1**: Reflex foreach safety; Phase1 UI without API/token noise.

* **PHASE1 PRODUCT FLOW RECOVERY v1**: signal-first home/profile/quiz/target/insight/match copy; insight six-block layout + single fox note; primary nav reduced to core six links; `MatchWall` cards expose compatibility / pressure / rhythm / risk / rationale; archived drifted docs under `docs/deprecated/`; added `docs/active/product/PHASE1_PRODUCT_FLOW.md`, `PAGE_PURPOSE_SYSTEM.md`, `SIGNAL_FIRST_PRODUCT_POSITION.md`, `docs/active/uat/PHASE1_PRODUCT_FLOW_UAT.md`, and recovery backlog/sprint entries.

* **PHASE1-E ENVIRONMENT LOCKDOWN v1**: `.python-version` (3.11.9), `requirements-lock.txt`, Reflex **0.9.2.post1** + **reflex-components-radix 0.9.2** (fixes `reflex_components_radix.plugin`), `start_hoku.bat` / `run_all_checks.bat`, `ops/env/*` policies + `runtime_sanity_check.py` + `reflex_compile_gate.py`, regression `test_phase1e_environment_lockdown_v1.py`, backlog/sprint entries, `BACKLOG.md` section.

* **MATCH WALL COMPILE HOTFIX v1**: moved distance / threshold logic out of `rx.foreach` card UI into `enrich_match_row_for_ui`; badges use string buckets + `rx.cond`; audit of other `rx.foreach` usages (no numeric-risk patterns); UAT `docs/active/uat/MATCH_WALL_COMPILE_HOTFIX.md`, regression `test_match_wall_compile_hotfix_v1.py`, backlog/sprint, `BACKLOG.md` section.

### NEXT

* Manual UAT per `docs/active/uat/PHASE1_PRODUCT_FLOW_UAT.md` on deployed/staging build.
* Run `run_all_checks.bat` from **`.venv`** (3.11/3.12). Reflex compile may hit OneDrive file locks on `.web` — see `ops/env/STARTUP_GUIDE.md`.
* **Do not start PHASE1-D** until PHASE1-E is signed off on target machines.

---

## 2026-05-08

### DONE

* remove `.states` runtime tracking（`git rm -r --cached .states` + `.gitignore`）

### BLOCKER

### NEXT

* UAT /match loading
* console error cleanup
* verify unlock flow

---

## 2026-05-09

### DONE

* 修復 Reflex nested p hydration warning（`rx.callout`／`rx.text` 調整：`fox_quiz.py`、`match_wall.py`、`login`／`story`／`unlocks`）

* Console hydration warning 清除（需本機 `/match`、`/quiz` 自驗）

### BLOCKER

### NEXT

* 驗證 /match console clean

* 驗證 unlock modal 無 hydration error

---

## 2026-05-10

### DONE

* 建立 **`ops/debug/DEBUG_GUIDE.md`**

* 建立標準除錯證據流（Console／Network／Backend／SQL／優先級／禁止事項）

* 建立 HOTFIX workflow（證據 → 分層 → 修正 → UAT → BACKLOG／SPRINT_LOG／TEST_CHECKLIST）

### BLOCKER

### NEXT

* MATCH FLOW UAT

* RPC response verification

* console clean verification

---

## 2026-05-11

### DONE

* 建立 **`debug_evidence/`** 與 **`debug_evidence/README.md`**（事故目錄、`console.txt`／`network.json`／`backend.txt`／`rpc.sql`／`root_cause.md` 規格）

* 建立 **`ops/debug/DEBUG_POLICY.md`**（P0 HOTFIX 禁止／允許事項）

* 建立 root cause evidence workflow（串接 **`ops/debug/DEBUG_GUIDE.md`** §6–§7）

### BLOCKER

### NEXT

* MATCH FLOW evidence collection

* RPC evidence collection

* runtime incident archive

---

## 2026-05-12

### DONE

* 建立 **Incident Template Generator**（`scripts/create_incident.py`）

### NEXT

* 第一個真實事故演練

* MATCH FLOW incident archive

---

## 2026-05-13

### DONE

* 建立 **AI INCIDENT SYSTEM v1 skeleton**（`ai/`、`replay/`、`docs/`、`tests/regression/`、`scripts/collect_runtime.py`、`scripts/generate_patch_context.py`）

* 建立 **AI-NATIVE REPO LAYERING v1**（[`docs/active/governance/REPO_ARCHITECTURE.md`](docs/active/governance/REPO_ARCHITECTURE.md)、`product/`、`ops/`、`ai/replay/`、`ai/incident/README.md`；`scripts`/`tests`/`docs` 仍於 repo 根目錄以相容 pytest／CI）

* **INTERFACE STABILIZATION v1**：[`docs/active/governance/ARCHITECTURE_CONTRACT.md`](docs/active/governance/ARCHITECTURE_CONTRACT.md)、`product/INTERFACE.md`、`ai/INTERFACE.md`、`ops/INTERFACE.md`

* **PROCESS ENFORCEMENT v1**：[`ops/process/RULES.md`](ops/process/RULES.md)、`ops/hooks/check_process.py`

### NEXT

* replay runtime incident

* regression baseline

* root cause classification

---

## SPRINT 2026-W02 — MATCH FLOW v1

**STATUS**: ACTIVE

**GOAL**:

- implement minimal match system

詳見 [`backlog/SPRINT_MATCH_FLOW_v1.md`](backlog/SPRINT_MATCH_FLOW_v1.md)。

---

## PROCESS ENFORCEMENT ACTIVE

All development must follow:

`BACKLOG → SPRINT → IMPLEMENT → TEST → LOG`

Rules: [`ops/process/RULES.md`](ops/process/RULES.md).

---

## SPRINT 2026-W03 — UNLOCK FLOW v1

STATUS: ACTIVE

GOAL:

- implement unlock insight system

- remove chat-first direction

---

## FLOW CONSISTENCY SYSTEM v1

STATUS: ACTIVE

GOAL:

- standardize product flow architecture

- prevent flow drift

---

## SPRINT 2026-W04 — INSIGHT ENGINE v1

STATUS: ACTIVE

---

## SPRINT 2026-W05 — FLOW INTEGRATION v1

STATUS: ACTIVE

---

## SPRINT 2026-W07 — APP UI INTEGRATION v1

STATUS: ACTIVE

---

## SPRINT 2026-W08 — INSIGHT EXPERIENCE v1

STATUS: ACTIVE

---

## SPRINT 2026-W04 — USER PROFILE SYSTEM v1

STATUS: ACTIVE

---

## SPRINT 2026-W05 — PHASE 1 FINALIZATION

STATUS: ACTIVE

---

# SPRINT 2026-W06 — APP SHELL REPLACEMENT v1

STATUS: ACTIVE

GOAL:
Replace engineering/demo UI shell with real AI-native consumer UX.

---

## PRODUCT REALIGNMENT ACTIVE

FOX GUARDIAN SYSTEM direction locked.

---

## ROADMAP REALIGNMENT COMPLETE

Development direction migrated to FOX GUARDIAN SYSTEM.

---

## FOX PRESENCE v1

STATUS: ACTIVE

GOAL:
Make the Arctic Fox feel emotionally present inside the product.

---

## FOX IMMERSION SYSTEM v1

STATUS: ACTIVE

GOAL:
Move the product from debug-style insight UI into the Arctic Fox guardian world (presence, scan, white dream space).

---

## FOX MEMORY SYSTEM v1

STATUS: ACTIVE

GOAL:
Let the fox remember recent observation tone (local JSON, rule-based, no embeddings).

---

## FOX SIGNAL GUARD v1

STATUS: ACTIVE

GOAL:
Let the Arctic Fox actively block risky signals with calm guardian warnings.

---

## PHASE1 UX RESTRUCTURE v1

STATUS: ACTIVE

TYPE: PRODUCT DIRECTION LOCK (SAFE MODE — UX hierarchy + copy only)

GOAL: 「北極狐守護世界」：結論與危險優先、守護語氣、首頁／訊號檔案／觀察室層級一致；保留既有路由與 state 契約。

REFERENCES: [`backlog/BACKLOG_PHASE1_UX_RESTRUCTURE_v1.md`](backlog/BACKLOG_PHASE1_UX_RESTRUCTURE_v1.md), [`docs/deprecated/GUARDIAN_UX_CONSTITUTION.md`](docs/deprecated/GUARDIAN_UX_CONSTITUTION.md), [`docs/active/uat/PHASE1_PRODUCT_FLOW_UAT.md`](docs/active/uat/PHASE1_PRODUCT_FLOW_UAT.md)

---

## PRODUCT CORE REALIGNMENT v1

STATUS: ACTIVE

TYPE: PRODUCT REALIGNMENT SPRINT (documentation + roadmap lock only)

GOAL: Lock **AI Native SNS Guardian Network** as true core (social filtering, hater / dangerous interaction intelligence, SNS signals); fox = persona + guardian UX, not the engine alone.

REFERENCES: [`docs/active/product/CORE_PRODUCT_REALIGNMENT.md`](docs/active/product/CORE_PRODUCT_REALIGNMENT.md), [`docs/active/product/SOCIAL_SIGNAL_ARCHITECTURE.md`](docs/active/product/SOCIAL_SIGNAL_ARCHITECTURE.md), [`docs/active/product/HATER_SIGNAL_MODEL.md`](docs/active/product/HATER_SIGNAL_MODEL.md), [`docs/active/uat/PRODUCT_DIRECTION_RESET_NOTES.md`](docs/active/uat/PRODUCT_DIRECTION_RESET_NOTES.md), [`backlog/BACKLOG_PRODUCT_CORE_REALIGNMENT_v1.md`](backlog/BACKLOG_PRODUCT_CORE_REALIGNMENT_v1.md)

---

## STATE SANITIZATION HOTFIX v1

STATUS: ACTIVE

TYPE: RUNTIME STABILITY HOTFIX (Reflex state serialization + defensive loads)

GOAL: Remove hydration/socket instability from unsafe state shapes and dead computed vars; no feature changes.

REFERENCES: [`docs/active/uat/STATE_SANITIZATION_RUNTIME_UAT.md`](docs/active/uat/STATE_SANITIZATION_RUNTIME_UAT.md), [`backlog/BACKLOG_STATE_SANITIZATION_HOTFIX_v1.md`](backlog/BACKLOG_STATE_SANITIZATION_HOTFIX_v1.md), [`backlog/SPRINT_STATE_SANITIZATION_HOTFIX_v1.md`](backlog/SPRINT_STATE_SANITIZATION_HOTFIX_v1.md)

---

## TARGET SIGNAL PROFILE v1

STATUS: ACTIVE

TYPE: CORE PRODUCT LOOP FIX (target JSON + primary loop HOME→PROFILE→TARGET→INSIGHT)

GOAL: Remove abstract guardian UX by always having a **target signal** slot; merge insight layout to five blocks; memory tags for recurring target pressure.

REFERENCES: [`docs/active/product/TARGET_SIGNAL_CONSTITUTION.md`](docs/active/product/TARGET_SIGNAL_CONSTITUTION.md), [`backlog/BACKLOG_TARGET_SIGNAL_PROFILE_v1.md`](backlog/BACKLOG_TARGET_SIGNAL_PROFILE_v1.md), [`backlog/SPRINT_TARGET_SIGNAL_PROFILE_v1.md`](backlog/SPRINT_TARGET_SIGNAL_PROFILE_v1.md)

---

## RELATIONSHIP SIGNAL SIMULATION v1

STATUS: ACTIVE

TYPE: RELATIONSHIP INTELLIGENCE FOUNDATION (synthetic archetypes + interaction overlap)

GOAL: Explain **interaction danger patterns** (not solo vulnerability scoring); minimal UI strip + memory tags.

REFERENCES: [`docs/active/product/RELATIONSHIP_INTELLIGENCE_CONSTITUTION.md`](docs/active/product/RELATIONSHIP_INTELLIGENCE_CONSTITUTION.md), [`backlog/BACKLOG_RELATIONSHIP_SIGNAL_SIMULATION_v1.md`](backlog/BACKLOG_RELATIONSHIP_SIGNAL_SIMULATION_v1.md), [`backlog/SPRINT_RELATIONSHIP_SIGNAL_SIMULATION_v1.md`](backlog/SPRINT_RELATIONSHIP_SIGNAL_SIMULATION_v1.md)

---

## SIGNAL INTELLIGENCE ENGINE v1

STATUS: ACTIVE

TYPE: RULE-BASED SIGNAL INTELLIGENCE (`infer_signal_risks`; no LLM / embeddings / SNS)

GOAL: Interpret danger patterns from existing inputs; merge HIGH/MEDIUM/LOW with legacy signal guard; short guardian copy + optional fox-memory tags.

REFERENCES: [`docs/active/product/SIGNAL_INTELLIGENCE_CONSTITUTION.md`](docs/active/product/SIGNAL_INTELLIGENCE_CONSTITUTION.md), [`backlog/BACKLOG_SIGNAL_INTELLIGENCE_ENGINE_v1.md`](backlog/BACKLOG_SIGNAL_INTELLIGENCE_ENGINE_v1.md), [`backlog/SPRINT_SIGNAL_INTELLIGENCE_ENGINE_v1.md`](backlog/SPRINT_SIGNAL_INTELLIGENCE_ENGINE_v1.md)

---

## SIGNAL SYSTEM CONSOLIDATION v1

STATUS: ACTIVE

TYPE: SIGNAL ARCHITECTURE CONSOLIDATION (docs + terminology + light home/profile/quiz copy)

GOAL: One coherent signal path: **Signal Profile Setup** (`/profile`) → optional **signal questions** (`/quiz`) → **Guardian Observation** (`/insight`) → memory; no duplicate onboarding.

REFERENCES: [`docs/active/product/SIGNAL_SYSTEM_CONSTITUTION.md`](docs/active/product/SIGNAL_SYSTEM_CONSTITUTION.md), [`backlog/BACKLOG_SIGNAL_SYSTEM_CONSOLIDATION_v1.md`](backlog/BACKLOG_SIGNAL_SYSTEM_CONSOLIDATION_v1.md), [`backlog/SPRINT_SIGNAL_SYSTEM_CONSOLIDATION_v1.md`](backlog/SPRINT_SIGNAL_SYSTEM_CONSOLIDATION_v1.md)

---

## PHASE1 UAT FLOW FIX v2

STATUS: ACTIVE

TYPE: UX RECOVERY SPRINT

GOAL:
Fix user confusion and restore correct FOX GUARDIAN SYSTEM onboarding (profile → insight → explain → next step).

