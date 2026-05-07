# Sprint Log

## YYYY-MM-DD

### DONE

### BLOCKER

### NEXT

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

* 建立 **`DEBUG_GUIDE.md`**

* 建立標準除錯證據流（Console／Network／Backend／SQL／優先級／禁止事項）

* 建立 HOTFIX workflow（證據 → 分層 → 修正 → UAT → BACKLOG／SPRINT_LOG／TEST_CHECKLIST）

### BLOCKER

### NEXT

* MATCH FLOW UAT

* RPC response verification

* console clean verification
