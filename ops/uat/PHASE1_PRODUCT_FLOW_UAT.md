# PHASE1 product flow — UAT script

**Goal:** Verify one coherent product story and the locked route order.

## Preconditions

- Local or deployed app running; optional login for `/match` if required by environment.

## Flow walkthrough

| Step | Route | Pass if user can answer (without confusion) |
|------|-------|-----------------------------------------------|
| 1 | `/` | “What is this?” — social signal analysis, not fox fantasy / therapy. |
| 2 | `/profile` | “Why am I filling this?” — baseline *my* signal model for later analysis. |
| 3 | `/quiz` | “Is this another profile?” — **no**; it deepens sensitivity dimensions. |
| 4 | `/target` | “Who is this for?” — the person or context I’m observing. |
| 5 | `/insight` | “What did I get?” — summary metrics, high-risk bullets, fit / avoid, one fox note, three next actions. |
| 6 | `/match` | “Why these cards?” — filtered by signal distance / risk; fields on card explain pressure, rhythm, risk, reason. |

## Navigation checks

- **Pass:** Nav shows only: 首頁、我的訊號、訊號問卷、觀察對象、分析結果、適合對象 (+ 登入/登出).  
- **Fail:** Primary nav still pushes 故事 / 解鎖 as part of the main journey without a deliberate legacy reason.

## Clarity checks (fail = stop ship)

1. No page feels like a **different product** (lore dump + signal form side by side with no bridge).  
2. **Insight** does not stack multiple fox/guardian essays; **one** short fox block only.  
3. **Home** does not repeat the same onboarding block twice with different wording.  
4. **Fox** reads as **hint**, not as the core engine.  

## Sign-off

- Tester: _______________  
- Date: _______________  
- Result: PASS / FAIL (notes): _______________
