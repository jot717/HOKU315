-- Task 7：北極狐配對牆 RPC（UAT-04 門檻版）
-- get_safe_matches(current_uid uuid)
--   - 消失門檻 Blocked: distance >= 1.2 -> 不回傳
--   - 模糊門檻 Blurred: distance >= 0.7 -> is_blurred = true
--   - 衝突分析: 取 |a_i - b_i| 最大之維度 index + label

create extension if not exists vector;

create or replace function public.get_safe_matches(current_uid uuid)
returns table (
  matched_user_id uuid,
  distance double precision,
  is_blurred boolean,
  conflict_dim_index int,
  conflict_dim_label text,
  image_object_path text,
  image_bucket text,
  blocked_count int
)
language sql
stable
as $$
  with labels as (
    select array[
      '邊界被踩（過問私事、強行建議）',
      '情緒讀空氣失靈（該停話題卻續聊）',
      '遲到／改期地雷',
      '私訊回覆節奏焦慮',
      '玩笑尺度踩線（嘲諷、地獄梗）',
      '肢體／距離界線',
      '否定式稱讚（明褒暗貶）',
      '謙虛炫耀反彈',
      '插話／打斷耐受低',
      '已讀不回／慢回焦慮',
      '群組被@／洗版壓力',
      '沈默尷尬地雷',
      '過度關心／黏人警報',
      '訊號模糊（曖昧不清）',
      '藉口可信度敏感',
      '送禮／人情往來壓力',
      '聚餐飲食選擇衝突',
      '價值觀辯論一觸即發',
      '人生進度比較（婚育／職稱）',
      '工作話題過載'
    ]::text[] as dim_labels
  ),
  me as (
    select id, mine_vector
    from public.profiles
    where id = current_uid
    limit 1
  ),
  candidates as (
    select
      p.id as matched_user_id,
      p.mine_vector as other_vec,
      m.mine_vector as me_vec,
      (p.mine_vector <-> m.mine_vector)::double precision as distance
    from public.profiles p
    cross join me m
    where p.id <> m.id
  ),
  with_conflict as (
    select
      c.matched_user_id,
      c.distance,
      d.dim_1based as conflict_dim_index,
      l.dim_labels[d.dim_1based] as conflict_dim_label,
      s.image_object_path,
      s.image_bucket
    from candidates c
    cross join labels l
    left join lateral (
      select st.image_object_path, st.image_bucket
      from public.stories st
      where st.user_id = c.matched_user_id
      order by st.created_at desc
      limit 1
    ) s on true
    cross join lateral (
      select
        gs as dim_1based,
        abs((c.other_vec[gs]::double precision - c.me_vec[gs]::double precision)) as delta
      from generate_series(1, 20) as gs
      order by delta desc, gs asc
      limit 1
    ) d
  ),
  stats as (
    select count(*)::int as blocked_count
    from with_conflict
    where distance >= 1.2
  )
  select
    w.matched_user_id,
    w.distance,
    (w.distance >= 0.7) as is_blurred,
    w.conflict_dim_index,
    w.conflict_dim_label,
    w.image_object_path,
    coalesce(w.image_bucket, 'stories') as image_bucket,
    s.blocked_count
  from with_conflict w
  cross join stats s
  where w.distance < 1.2
  order by w.distance asc, w.matched_user_id;
$$;
