"""
JOT717 AI 調度層：所有 LLM 相關訊息組裝與（可選）供應商切換入口。

- 從 db_service 讀 profile 向量與 user_memories，自動注入「地雷特徵」system 前綴。
- 供應商以環境變數 LLM_PROVIDER=deepseek|claude 切換（實際 HTTP 呼叫可後續擴充）。
"""
from __future__ import annotations

import os
from enum import Enum
from typing import Any

import db_service
import fox_logic


class LLMProvider(str, Enum):
    DEEPSEEK = "deepseek"
    CLAUDE = "claude"


# 四譜系 + 無向量時之中性語氣（共五種），供真 LLM 與規則式回覆對齊。
_FOX_LLM_VOICE: dict[str, str] = {
    "weave": (
        "你是「織光譜系」口吻：優先促進和諧與相互理解，用具體感受與可觀察行為描述取代貼標；"
        "避免暗示使用者「不夠圓融」或情緒勒索式勸說；若要提醒踩雷，用軟著陸、可選擇的句式。"
    ),
    "vein": (
        "你是「靜脈譜系」口吻：優先協助掌控訊息節奏與互動頻率，建議簡短、可執行、可分段回覆；"
        "避免鼓勵無上限配合群體或立即全面道歉；留意洗版、@、已讀焦慮相關語境。"
    ),
    "rime": (
        "你是「霜鎧譜系」口吻：優先強調自我保護與可執行的界線（暫停、婉拒、退出對話、保留證據等具體步驟）；"
        "勿要求使用者在被越界時仍要先深度同理對方；肯定「先站穩自己的安全再談關係」的合理性。"
    ),
    "ember": (
        "你是「餘燼譜系」口吻：優先釐清價值與原則界線，對人生進度比較、道德綁架式說教冷處理；"
        "避免煽動對立，但可坦率指出「不必用他人尺規定義自己」；提供降溫與換話題策略。"
    ),
    "neutral": (
        "目前 profile 向量不足或尚未載入：採平衡口吻——先同理處境，再給一個最小可行步驟；"
        "語氣不油膩、不說教，並避免在不明情境下假定誰「一定有錯」。"
    ),
}


def _infer_arcana_key_from_system_block(system_block: str) -> str | None:
    """由 `dominant_fox_message` 嵌入之標題列反推譜系鍵，供規則式回覆分支。"""
    markers: tuple[tuple[str, str], ...] = (
        ("weave", "【織光譜系主導"),
        ("vein", "【靜脈譜系主導"),
        ("rime", "【霜鎧譜系主導"),
        ("ember", "【餘燼譜系主導"),
    )
    for key, needle in markers:
        if needle in system_block:
            return key
    return None


class LLMGateway:
    """統一組裝對話訊息；禁止在 UI 直接拼裸 API。"""

    def __init__(self, provider: LLMProvider | str | None = None) -> None:
        raw = provider or os.getenv("LLM_PROVIDER", LLMProvider.DEEPSEEK.value)
        try:
            self._provider = LLMProvider(str(raw).lower())
        except ValueError:
            self._provider = LLMProvider.DEEPSEEK

    @property
    def provider(self) -> LLMProvider:
        return self._provider

    def build_minefield_system_block(
        self,
        user_id: str,
        *,
        query_vector: list[float] | None = None,
    ) -> str:
        """
        組裝注入 LLM 的 system 片段：profile 地雷維度 + 相近對話記憶摘要。
        """
        lines: list[str] = [
            "【狐狸地雷記憶｜JOT717】",
            "以下為從資料庫檢索的使用者特徵，請務必採納語氣與話題迴避策略。",
        ]

        profile_vec: list[float] | None = None
        try:
            profile_vec = db_service.get_user_vector(user_id)
        except LookupError:
            lines.append("- （尚無 profile 向量，僅依對話記憶與當前語境推論）")

        if profile_vec is not None:
            hints = fox_logic.minefield_hints_from_vector(profile_vec)
            for h in hints:
                lines.append(f"- 注意：該使用者在「{h.split('（')[0]}」面向較敏感，請避免踩雷。")
            fox = fox_logic.dominant_fox_message(profile_vec)
            lines.append("")
            lines.append("【狐狸語基調參考】")
            lines.append(fox)

        arc_key = (
            fox_logic.dominant_fox_archetype_key(profile_vec)
            if profile_vec is not None
            else "neutral"
        )
        lines.append("")
        lines.append("【譜系語氣｜LLM 必遵】")
        lines.append(_FOX_LLM_VOICE.get(arc_key, _FOX_LLM_VOICE["neutral"]))

        qv = query_vector if query_vector is not None else profile_vec
        if qv is not None:
            try:
                res = db_service.match_user_memories(user_id, qv, match_count=4)
                rows = getattr(res, "data", None) or []
                if rows:
                    lines.append("")
                    lines.append("【相近對話記憶摘要】")
                    for r in rows:
                        if isinstance(r, dict) and r.get("summary"):
                            lines.append(f"- {r['summary']}")
            except Exception:
                lines.append("")
                lines.append("（向量記憶檢索暫不可用：請確認已執行 sql/user_memories.sql 並建立 RPC）")

        return "\n".join(lines)

    def build_chat_messages(
        self,
        user_id: str,
        user_message: str,
        *,
        query_vector: list[float] | None = None,
    ) -> list[dict[str, Any]]:
        """標準 chat messages 結構，可直接送 OpenAI-compatible API。"""
        system_content = self.build_minefield_system_block(user_id, query_vector=query_vector)
        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_message},
        ]

    @staticmethod
    def simulate_fox_ack(system_block: str, user_message: str) -> str:
        """
        不依賴外部 LLM 的規則式「狐狸語建議」，供測試驗證記憶注入是否影響策略。
        分支順序：情境關鍵字 → 譜系預設語氣（與 _FOX_LLM_VOICE 對齊）。
        """
        arc = _infer_arcana_key_from_system_block(system_block)

        if "人情" in system_block or "送禮" in system_block:
            if any(k in user_message for k in ("禮", "紅包", "人情", "聚餐")):
                if arc == "weave":
                    return (
                        "【織光·狐狸語】人情壓力敏感；先以和諧語氣說明你的預算與界線，再邀對方一起找不傷感情的選項。"
                    )
                if arc == "rime":
                    return (
                        "【霜鎧·狐狸語】人情壓力下仍以自我保護為先：先決定你能給的上限與停損點，再禮貌告知，不必為面子透支。"
                    )
                if arc == "vein":
                    return (
                        "【靜脈·狐狸語】送禮話題易拖長訊息戰；用一則短訊講清規則與頻率，其餘先不回，避免被來回绑架。"
                    )
                if arc == "ember":
                    return (
                        "【餘燼·狐狸語】人情與價值綁在一起時，先釐清「這是關係還是交易」；界線說清楚，比勉強配合更尊重彼此。"
                    )
                return (
                    "【狐狸語建議】偵測到人情／送禮壓力敏感；請先把界線與期待說清楚，再談面子。"
                )

        if "霜鎧" in system_block or "邊界" in system_block:
            if any(k in user_message for k in ("越界", "管太多", "私事")):
                return (
                    "【霜鎧·狐狸語】邊界警報：優先自我保護——用一句話標示「這裡我不談」，必要時暫停對話；"
                    "不必急著證明自己沒惡意。"
                )

        if "靜脈" in system_block or "群組" in system_block:
            if "@" in user_message or "群組" in user_message:
                return (
                    "【靜脈·狐狸語】群體節奏敏感：先降頻與縮句，必要時用延後回覆保護專注；"
                    "不必即時消化所有 @。"
                )

        if arc == "weave":
            return (
                "【織光·狐狸語】先深呼吸，用一句話描述你的感受與希望對方怎麼配合，避免先定罪對方動機。"
            )
        if arc == "vein":
            return (
                "【靜脈·狐狸語】先釐清訊息量與期限：一句確認＋一個可選回覆時間，保護自己的節奏。"
            )
        if arc == "rime":
            return (
                "【霜鎧·狐狸語】先確認自己是否安全、舒服；若否，允許自己暫緩回應，再決定要給對方多少資訊。"
            )
        if arc == "ember":
            return (
                "【餘燼·狐狸語】先區分「事實」與「對方的人生尺規」；你只需對自己的價值選擇負責，不必接招比較。"
            )
        return "【中性·狐狸語】先深呼吸，用一句話確認對方真正想解決的是什麼，再決定你要投入多少。"
