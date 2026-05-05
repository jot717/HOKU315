-- JOT717 / HOKU315：向量記憶表（RAG Lite）+ pgvector 檢索 RPC
-- 請在 Supabase SQL Editor 以 service role 或有權限帳號執行。

create extension if not exists vector;

create table if not exists public.user_memories (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.profiles (id) on delete cascade,
  summary text not null,
  embedding vector(20) not null,
  created_at timestamptz not null default now()
);

create index if not exists user_memories_user_id_idx on public.user_memories (user_id);
-- 資料量較大後再建立 ANN 索引（ivfflat / hnsw），避免空表建索引失敗

-- 依使用者與查詢向量取最相近的記憶列（PostgREST RPC）
create or replace function public.match_user_memories(
  p_user_id uuid,
  p_query_embedding vector(20),
  match_count int default 5
)
returns setof public.user_memories
language sql
stable
as $$
  select *
  from public.user_memories
  where user_id = p_user_id
  order by embedding <-> p_query_embedding
  limit greatest(1, least(coalesce(match_count, 5), 50));
$$;

-- RLS（依專案需求調整；若僅 service_role 存取可先略過）
-- alter table public.user_memories enable row level security;
