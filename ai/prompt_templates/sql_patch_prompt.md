# Prompt template — SQL patch（Supabase）

用於需要 **`CREATE OR REPLACE FUNCTION`**、索引或診斷查詢**建議**時。實際執行一律由人類在 SQL Editor 完成並更新 **`sql/DEPLOY_LOG.md`**。

---

## User message scaffold

```
Repo SQL source of truth: sql/match_logic.sql (and DEPLOY_LOG.md).

Incident evidence:
- rpc.sql from debug_evidence folder (attached)
- patch_context.md (attached)

Task:
1. Diff mentally against deployed assumptions in DEPLOY_LOG.md.
2. Output a single SQL script proposal with comments.
3. Call out PostgREST cache / PGRST205 risks.
4. Explicitly state what NOT to run on production if ambiguous.
```
