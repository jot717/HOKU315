# SIGNAL INTELLIGENCE ENGINE — UAT (v1)

**TYPE:** Rule-based inference + guardian integration (no LLM / embeddings / SNS).  
**Refs:** [`docs/active/product/SIGNAL_INTELLIGENCE_CONSTITUTION.md`](../product/SIGNAL_INTELLIGENCE_CONSTITUTION.md), [`docs/active/product/SIGNAL_INFERENCE_MODEL.md`](../product/SIGNAL_INFERENCE_MODEL.md)

---

## What users should understand (pass)

* The product **detects danger-style interaction patterns** from **their own signal inputs** (訊號檔案、地雷問卷、觀察節奏)，不是通靈。
* Explanations are **規則式推論**，可讀、可反駁、可再用新輸入覆寫。
* **Highest risk first**：顏色與標題反映合併後的 HIGH / MEDIUM / LOW，不平均分配版面給所有分析。

---

## What users should NOT believe (fail)

* 這是 **心理治療**、**診斷**、或 **AI 算命**。
* 單一答案就決定「你是誰」。

---

## Guardian explanations (pass)

* 短句、具體行為後果（例如慢回、通知、比較場景），**不出長篇報告**。
* 危險型態區塊明確寫「**不是心理診斷**」。

---

## Risks feel connected to input (pass)

* 壓力數字、地雷維度、或先前觀察記憶變化後，**警告語與建議跟著變**，而非固定文案。

---

## Usefulness vs random (pass)

* 在極端輸入（高壓 + 高回覆焦慮）下應出現 **注意力消耗 / 幽靈式壓力** 類訊息；全中立輸入應偏 **LOW** 語氣。

---

## Pass / fail checklist

| ID | Check | Pass |
|----|--------|------|
| I1 | 觀察室出現「北極狐看到的危險型態」區塊 | 肉眼 |
| I2 | 區塊含「不是心理診斷」免責 | 肉眼 |
| I3 | `infer_signal_risks` 回傳鍵齐全 | 單元測試 |
| I4 | 無 `/onboarding` 新路徑 | grep |
| I5 | 文檔三份 + ontology 存在 | 單元測試 |
