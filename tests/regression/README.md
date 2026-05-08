# Regression tests

本目錄為 **REGRESSION SYSTEM v1**：與事故回放／AI patch／deploy 閘門對齊。

## 政策（v1）

- 所有 **deploy／hotfix** 合併前必須通過 **`pytest tests/regression/`**（見根目錄 [`BACKLOG.md`](../BACKLOG.md) — **REGRESSION GATE**）。
- CI：GitHub Actions **`.github/workflows/regression.yml`**（push／PR）。

## `test_core_flows.py`

| 測試 | 說明 |
|------|------|
| `test_reflex_compile_gate` | `python -m reflex compile` 必須成功 |
| `test_run_all_tests_gate` | `python -m tests.run_all_tests` 必須 exit 0 |
| `test_match` / `test_unlock` / `test_chat` | **選用**：需本機 **`reflex run`** 並設 **`REGRESSION_HTTP=1`**；對 **`/match`**、**`/unlocks`**、**`/chat`** 做 GET smoke（Reflex 為頁面路由，非 REST POST） |

本機跑頁面 smoke（範例，single-port 8000）：

```powershell
$env:REGRESSION_HTTP = "1"
$env:REGRESSION_BASE_URL = "http://127.0.0.1:8000"
pytest tests/regression/ -v
```

## 與事故資料的對齊

請將事故 **`root_cause.md`** 內「驗證」段落與此目錄案例交叉引用。

## 相關文件

- [`docs/REPLAY_GUIDE.md`](../docs/REPLAY_GUIDE.md)  
- [`docs/AI_PATCH_FLOW.md`](../docs/AI_PATCH_FLOW.md)  
