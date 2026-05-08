# Ops layer

**Logical ownership**：自動化腳本、測試發現、文件與 CI——與 **product／AI** 分類對照。

## 為何 `scripts/`、`tests/`、`docs/` 仍在 repo 根目錄？

搬移會破壞 **無邏輯變更** 約束：

- `python -m tests.run_all_tests`、`pytest tests/regression/`（GitHub Actions）
- Reflex／套件慣例與既有連結

因此 **物理路徑維持根目錄**；此樹以 README **對照**「ops 責任」。

| 路徑 | 說明 |
|------|------|
| [`scripts/`](../scripts/) | 工具腳本 |
| [`tests/`](../tests/) | 單元／回歸／`run_all_tests` |
| [`docs/`](../docs/) | 架構與流程文件 |
| [`.github/workflows/`](../.github/workflows/) | CI |
| [`process/`](process/) | 流程規則與模板（[`RULES.md`](process/RULES.md)） |
| [`hooks/`](hooks/) | 輕量檢查腳本 |

詳見 [`REPO_ARCHITECTURE.md`](../REPO_ARCHITECTURE.md)。
