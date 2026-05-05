-- JOT717 / HOKU315：個人故事（Story）、Storage bucket `stories` 與物件 RLS
-- 前置：public.profiles(id) 須與 auth.users 之 UUID 對齊。
-- 建議先執行 sql/profiles_rls.sql（允許 authenticated INSERT/UPDATE 自己的 profile），避免 stories FK／42501 聯調失敗。
-- 於 Supabase SQL Editor 以具權限帳號執行。

-- -----------------------------------------------------------------------------
-- Storage：bucket（私有；物件路徑必須為 `{auth.uid()}/{filename}`）
-- -----------------------------------------------------------------------------
INSERT INTO storage.buckets (id, name, public)
VALUES ('stories', 'stories', false)
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;

-- 物件僅能讀寫「自己 UUID 資料夾」——防止繞過前端拼路徑直接抓他人原圖
DROP POLICY IF EXISTS "storage_stories_select_own_folder" ON storage.objects;
DROP POLICY IF EXISTS "storage_stories_insert_own_folder" ON storage.objects;
DROP POLICY IF EXISTS "storage_stories_update_own_folder" ON storage.objects;
DROP POLICY IF EXISTS "storage_stories_delete_own_folder" ON storage.objects;

CREATE POLICY "storage_stories_select_own_folder"
  ON storage.objects FOR SELECT TO authenticated
  USING (
    bucket_id = 'stories'
    AND split_part(name, '/', 1) = auth.uid()::text
  );

CREATE POLICY "storage_stories_insert_own_folder"
  ON storage.objects FOR INSERT TO authenticated
  WITH CHECK (
    bucket_id = 'stories'
    AND split_part(name, '/', 1) = auth.uid()::text
  );

CREATE POLICY "storage_stories_update_own_folder"
  ON storage.objects FOR UPDATE TO authenticated
  USING (
    bucket_id = 'stories'
    AND split_part(name, '/', 1) = auth.uid()::text
  )
  WITH CHECK (
    bucket_id = 'stories'
    AND split_part(name, '/', 1) = auth.uid()::text
  );

CREATE POLICY "storage_stories_delete_own_folder"
  ON storage.objects FOR DELETE TO authenticated
  USING (
    bucket_id = 'stories'
    AND split_part(name, '/', 1) = auth.uid()::text
  );

-- -----------------------------------------------------------------------------
-- public.stories
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.stories (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES public.profiles (id) ON DELETE CASCADE,
  title text,
  body text,
  image_object_path text,
  image_bucket text NOT NULL DEFAULT 'stories',
  status text NOT NULL DEFAULT 'draft'
    CHECK (status IN ('draft', 'published', 'archived')),
  sort_order int NOT NULL DEFAULT 0,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS stories_user_id_idx ON public.stories (user_id);
CREATE INDEX IF NOT EXISTS stories_status_idx ON public.stories (status);

ALTER TABLE public.stories ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "stories_select_own" ON public.stories;
DROP POLICY IF EXISTS "stories_insert_own" ON public.stories;
DROP POLICY IF EXISTS "stories_update_own" ON public.stories;
DROP POLICY IF EXISTS "stories_delete_own" ON public.stories;

CREATE POLICY "stories_select_own"
  ON public.stories FOR SELECT TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "stories_insert_own"
  ON public.stories FOR INSERT TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "stories_update_own"
  ON public.stories FOR UPDATE TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "stories_delete_own"
  ON public.stories FOR DELETE TO authenticated
  USING (auth.uid() = user_id);

-- 若早期已建表且 image_bucket 預設為 story-images，可手動對齊：
-- ALTER TABLE public.stories ALTER COLUMN image_bucket SET DEFAULT 'stories';
