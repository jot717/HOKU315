# Prompt template — Runtime bug（async / state）

用於 **`ImmutableStateError`**、`asyncio` traceback、Reflex 事件處理器異常。

---

## User message scaffold

```
Symptoms: (paste backend.txt traceback)

Constraints:
- Prefer async with self patterns per Reflex docs and project HOTFIX history.
- No drive-by refactors across unrelated pages.

Deliver:
1. Stack trace interpretation
2. Minimal code change proposal (single handler if possible)
3. How to verify on reflex run + which route to hit
```
