-- PHASE2-B entity snapshots (JSON port cloud mirror)
-- Apply in Supabase SQL Editor; record in sql/DEPLOY_LOG.md

create table if not exists public.hoku_entity_snapshots (
  user_id uuid not null references auth.users (id) on delete cascade,
  entity_key text not null,
  schema_version int not null default 1,
  updated_at timestamptz not null default now(),
  payload jsonb not null default '{}'::jsonb,
  primary key (user_id, entity_key)
);

alter table public.hoku_entity_snapshots enable row level security;

create policy "hoku_entity_snapshots_select_own"
  on public.hoku_entity_snapshots for select
  using (auth.uid() = user_id);

create policy "hoku_entity_snapshots_upsert_own"
  on public.hoku_entity_snapshots for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
