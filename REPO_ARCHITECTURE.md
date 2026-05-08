# AI-Native Repo Architecture v1

本檔描述 **邏輯分層** 與 **實體路徑對照**。目標：AI-native 協作時能快速定位「產品／AI 工程／維運」邊界，且在 **不改 Reflex 模組名、不破壞 pytest／CI** 的前提下完成 **SAFE LAYERING**。

---

## PRODUCT LAYER

**責任**：使用者流程、業務與 UI／後端契約（Reflex pages、`db_service` 等）。

**邏輯目錄**：`product/match`、`product/unlock`、`product/chat`（各附 README，指向現有 `fox_quiz/`、`db_service.py`）。

**原則**：未將 `fox_quiz` 整包搬入 `product/`，以免改動 `rxconfig.py` 之 `app_name` 與匯入路徑（非無破壞搬移）。

---

## AI ENGINEERING LAYER

**責任**：事故、回放、診斷、taxonomy、建議、安全 self-heal 占位。

**實體**：

| 區域 | 路徑 |
|------|------|
| Incident（對照） | `ai/incident/README.md` → `debug_evidence/`、`scripts/create_incident.py` 等 |
| Replay（mock） | `ai/replay/replay_incident.py`（亦可 `python replay/replay_incident.py` shim） |
| Diagnosis | `ai/diagnosis/root_cause_engine.py` |
| Taxonomy | `ai/taxonomy/error_taxonomy.yaml` |
| Suggestion | `ai/suggestion/suggest_engine.py` |
| Self-heal | `ai/self_heal/` |

---

## OPS LAYER

**責任**：CI／回歸／工具／文件（跨層協調說明）。

**實體**：`scripts/`、`tests/`、`docs/`、`.github/workflows/` 維持在 **repo 根目錄**；`ops/` 內 README 為對照索引（見 [`ops/README.md`](ops/README.md)）。

---

## RULES（設計約束）

1. **Product 程式碼**不應依賴 AI 層內部模組（例如不要在 `fox_quiz` 內 `import ai.self_heal`）；事故流程維持在工具／文件層。
2. **AI 層**不應依賴具體 UI 元件實作；可讀 taxonomy、debug_evidence、共用 `db_service` 契約說明（文件／型別），避免循環耦合。
3. **Ops** 為編排與閘門：`pytest tests/regression/`、`python scripts/run_regression.py`（見 [`BACKLOG.md`](BACKLOG.md)）。
4. **所有 patch** 合併前須通過 **REGRESSION GATE**（與 [`tests/regression/README.md`](tests/regression/README.md) 一致）。

---

## REPO LAYERING v1（摘要）

- 已建立 **product／ai／ops** 目錄與對照 README。
- **Replay** 實作已歸位 **`ai/replay/`**；根目錄 **`replay/`** 保留輕量 shim 與說明。
- **未**搬移 `scripts`／`tests`／`docs` 至 `ops/` 子樹（避免破壞模組路徑與 CI）。
