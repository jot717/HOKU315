# Regression tests

本目錄預留 **與事故回放／AI patch 綁定** 的回歸測試。

## 政策（v1）

- 所有 **AI 建議並合併** 的 patch，在進入主線前必須：  
  - 執行 **`python -m tests.run_all_tests`**  
  - 並於此目錄逐步累積與 HOTFIX 對齊之最小案例（未來實作）。

## 目前狀態

Skeleton only —— 尚無強制檔案。請將事故 `root_cause.md` 內「驗證」段落與本目錄未來測試案例交叉引用。

## 相關文件

- [`docs/REPLAY_GUIDE.md`](../docs/REPLAY_GUIDE.md)  
- [`docs/AI_PATCH_FLOW.md`](../docs/AI_PATCH_FLOW.md)  
