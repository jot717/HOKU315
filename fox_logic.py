"""
狐狸測驗：20 維「社交地雷」語意維度與向量生成。

輸出 `list[float]`（長度 20），可直接餵給 `db_service.update_user_vector` / `get_matches`。
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence

VECTOR_DIM = 20

# (維度鍵, 中文標籤) — 順序即向量分量索引 0..19
SOCIAL_MINE_DIMENSIONS: tuple[tuple[str, str], ...] = (
    ("boundary_intrusion", "邊界被踩（過問私事、強行建議）"),
    ("emotional_tone_deaf", "情緒讀空氣失靈（該停話題卻續聊）"),
    ("punctuality_mine", "遲到／改期地雷"),
    ("dm_pace_sensitivity", "私訊回覆節奏焦慮"),
    ("joke_boundary", "玩笑尺度踩線（嘲諷、地獄梗）"),
    ("personal_space", "肢體／距離界線"),
    ("backhanded_praise", "否定式稱讚（明褒暗貶）"),
    ("humblebrag_trigger", "謙虛炫耀反彈"),
    ("interruption_intolerance", "插話／打斷耐受低"),
    ("reply_latency_anxiety", "已讀不回／慢回焦慮"),
    ("group_mention_stress", "群組被@／洗版壓力"),
    ("silence_discomfort", "沈默尷尬地雷"),
    ("overcare_cling", "過度關心／黏人警報"),
    ("ambiguous_signals", "訊號模糊（曖昧不清）"),
    ("excuse_skepticism", "藉口可信度敏感"),
    ("gift_reciprocity", "送禮／人情往來壓力"),
    ("food_plan_mine", "聚餐飲食選擇衝突"),
    ("values_debate_spike", "價值觀辯論一觸即發"),
    ("life_stage_comparison", "人生進度比較（婚育／職稱）"),
    ("work_talk_saturation", "工作話題過載"),
)

SOCIAL_MINE_KEYS: tuple[str, ...] = tuple(k for k, _ in SOCIAL_MINE_DIMENSIONS)

# 織光維度：向量前四維（與 UI 狐狸反饋文案一致）
WEAVE_LIGHT_DIMS = 4


def weave_light_mean(vector: Sequence[float]) -> float:
    """前四維（織光維度）算術平均，須 len(vector) >= 4。"""
    if len(vector) < WEAVE_LIGHT_DIMS:
        raise ValueError(f"向量長度至少 {WEAVE_LIGHT_DIMS}，目前為 {len(vector)}")
    return sum(float(vector[i]) for i in range(WEAVE_LIGHT_DIMS)) / float(WEAVE_LIGHT_DIMS)


# 狐狸譜系：四組各 5 維，覆蓋 20 維向量（與 UI 狐狸語一致）
FOX_ARCANA_GROUPS: tuple[tuple[str, str, tuple[int, ...]], ...] = (
    ("weave", "織光", tuple(range(0, 5))),
    ("vein", "靜脈", tuple(range(5, 10))),
    ("rime", "霜鎧", tuple(range(10, 15))),
    ("ember", "餘燼", tuple(range(15, 20))),
)

FOX_ARCANA_PROSE: dict[str, str] = {
    "weave": "檢測到織光譜系閃爍：你像隻把情緒波形讀得極細、對細節過招毫不手軟的沙漠耳廓狐。",
    "vein": "靜脈迴路噪聲偏高：你像隻緊盯群體節拍、對聊天室血壓極敏感的赤耳狐。",
    "rime": "檢測到強大的霜鎧防禦場：你是一隻極度注重邊界、把個人領域守成冰原的北極狐。",
    "ember": "餘燼餘溫仍灼：你像隻在價值與人生進度上不肯讓步、把話題燃到最後的沙狐。",
}


def group_mean(vector: Sequence[float], indices: tuple[int, ...]) -> float:
    if not indices:
        raise ValueError("indices 不可為空")
    return sum(float(vector[i]) for i in indices) / float(len(indices))


def _pick_dominant_arcana(vector: Sequence[float]) -> tuple[str, str, float]:
    """回傳 (譜系鍵, 中文譜系名, 該組均值)。"""
    if len(vector) < VECTOR_DIM:
        raise ValueError(f"需要長度 {VECTOR_DIM} 的向量")
    v = [float(vector[i]) for i in range(VECTOR_DIM)]
    best_key = "weave"
    best_label = "織光"
    best_mean = -1.0
    for key, label, idxs in FOX_ARCANA_GROUPS:
        m = group_mean(v, idxs)
        if m > best_mean + 1e-12:
            best_mean = m
            best_key = key
            best_label = label
    return best_key, best_label, best_mean


def dominant_fox_archetype_key(vector: Sequence[float]) -> str:
    """
    與 dominant_fox_message 相同之譜系判定，回傳鍵名：weave / vein / rime / ember。
    供 UI 頭像與主題切換。
    """
    return _pick_dominant_arcana(vector)[0]


def minefield_hints_from_vector(
    vector: Sequence[float],
    *,
    threshold: float = 0.62,
    max_hints: int = 5,
) -> list[str]:
    """
    由 20 維 profile／查詢向量挑出最敏感之社交地雷維度，供 LLM system 注入。
    回傳中文短句列表（由高到低），僅收錄 >= threshold 之維度，最多 max_hints 條。
    """
    if len(vector) < VECTOR_DIM:
        raise ValueError(f"需要長度 {VECTOR_DIM} 的向量")
    scored: list[tuple[int, float]] = [
        (i, float(vector[i])) for i in range(VECTOR_DIM)
    ]
    scored.sort(key=lambda t: -t[1])
    out: list[str] = []
    for i, val in scored:
        if val < threshold:
            break
        label = SOCIAL_MINE_DIMENSIONS[i][1]
        out.append(f"{label}（敏感度 {val:.2f}）")
        if len(out) >= max_hints:
            break
    if not out:
        for i, val in scored[:3]:
            label = SOCIAL_MINE_DIMENSIONS[i][1]
            out.append(f"{label}（敏感度 {val:.2f}）")
    return out


def dominant_fox_message(vector: Sequence[float]) -> str:
    """
    比較織光／靜脈／霜鎧／餘燼四組均值，取最高者並回傳對應「狐狸語」段落。
    平手時依 FOX_ARCANA_GROUPS 宣告順序優先。
    """
    best_key, best_label, best_mean = _pick_dominant_arcana(vector)
    prose = FOX_ARCANA_PROSE.get(best_key, "狐狸語待補。")
    return f"【{best_label}譜系主導 · 組內均值 {best_mean:.2f}】\n{prose}"


def _clamp_unit(x: float) -> float:
    v = float(x)
    if v < 0.0:
        return 0.0
    if v > 1.0:
        return 1.0
    return v


def generate_vector(values: Sequence[float] | Mapping[str, float]) -> list[float]:
    """
    將測驗輸入轉成 20 維 float 向量（每維預設語意為 0..1 強度，越接近 1 越「踩雷敏感」）。

    - 傳入 `Sequence[float]`：依 `SOCIAL_MINE_KEYS` 順序對應 20 題滑桿值。
    - 傳入 `Mapping[str, float]`：以維度鍵取值，順序仍依 `SOCIAL_MINE_KEYS` 輸出。
    """
    if isinstance(values, Mapping):
        missing = [k for k in SOCIAL_MINE_KEYS if k not in values]
        if missing:
            raise KeyError(f"缺少維度鍵（共 {len(missing)} 個），例如：{missing[:3]}")
        raw = [float(values[k]) for k in SOCIAL_MINE_KEYS]
    else:
        seq = list(values)
        if len(seq) != VECTOR_DIM:
            raise ValueError(f"需要 {VECTOR_DIM} 個數值，收到 {len(seq)} 個")
        raw = [float(v) for v in seq]

    return [_clamp_unit(v) for v in raw]
