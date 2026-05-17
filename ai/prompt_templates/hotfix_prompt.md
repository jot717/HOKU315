# Prompt template — HOTFIX（Reflex / Python）

將下列區塊複製到 AI 對話，並附上 **`patch_context.md`**、`backend.txt`、`console.txt`（適用時）。

---

## System hints

- 僅做 **最小修正**；勿改動未請求之路由或資料契約。  
- 遵守專案 [`ops/debug/DEBUG_POLICY.md`](../../ops/debug/DEBUG_POLICY.md)。  
- 若有 SQL，必須對照 repo 內既有檔案（例如 `sql/match_logic.sql`），並提醒人類在 Supabase 手動執行與記錄。

---

## User message scaffold

```
You are patching HOKU315 (Reflex + Supabase).

Context files:
- patch_context.md (attached)
- backend.txt / console.txt (attached)

Requirements:
1. Explain root cause hypothesis in 3 bullets.
2. Propose minimal diff (file paths + code).
3. List regression checks (commands / routes).
4. Do NOT change RPC signatures or DB schema unless explicitly asked.
```
