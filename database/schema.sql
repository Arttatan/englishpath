-- ============================================================
-- EnglishPath — database schema (Step 3)
-- How to run: Supabase dashboard → SQL Editor → New query →
--   paste everything below → click "Run".
-- Safe to run more than once (it uses "if not exists" / "drop ... if exists").
-- ============================================================


-- ------------------------------------------------------------
-- 1) TABLES
-- ------------------------------------------------------------

-- Extra info for each user, linked to Supabase's built-in auth.users table.
create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  email text,
  is_admin boolean not null default false,   -- the site owner = true
  is_premium boolean not null default false, -- set by Stripe later (Step 7)
  created_at timestamptz not null default now()
);

-- Lessons.
create table if not exists public.lessons (
  id bigint generated always as identity primary key,
  title text not null,
  level text not null,          -- a1, a2, b1, b1plus, b2
  section text not null,        -- grammar, vocabulary, listening, reading, use-of-english, writing
  explanation text,             -- rich HTML produced by the admin editor
  audio_url text,               -- optional link (YouTube / audio) for listening & reading
  is_published boolean not null default false,  -- draft vs published
  is_premium boolean not null default false,    -- soft freemium: false = free for everyone
  sort_order int not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- Exercises that belong to a lesson.
-- "options" and "correct_answer" are JSON so they can fit every exercise type:
--   multiple_choice: options = ["go","goes","going"], correct_answer = "goes"
--   fill_blank:      options = null,                  correct_answer = ["goes","go"]  (accepted answers)
--   matching:        options = {"left":[...],"right":[...]}, correct_answer = {"0":1,"1":0,...}
create table if not exists public.exercises (
  id bigint generated always as identity primary key,
  lesson_id bigint not null references public.lessons(id) on delete cascade,
  type text not null,           -- multiple_choice | fill_blank | matching
  question text not null,
  options jsonb,
  correct_answer jsonb,
  explanation text,             -- feedback shown after answering
  sort_order int not null default 0,
  created_at timestamptz not null default now()
);

-- One row per user per lesson (their best/last result).
create table if not exists public.user_progress (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  lesson_id bigint not null references public.lessons(id) on delete cascade,
  score int not null default 0,
  total int not null default 0,
  completed_at timestamptz not null default now(),
  unique (user_id, lesson_id)
);

-- Indexes to keep queries fast.
create index if not exists idx_lessons_level_section on public.lessons(level, section);
create index if not exists idx_exercises_lesson on public.exercises(lesson_id);
create index if not exists idx_progress_user on public.user_progress(user_id);


-- ------------------------------------------------------------
-- 2) FUNCTIONS & TRIGGERS
-- ------------------------------------------------------------

-- Automatically create a profile row whenever a new user signs up.
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.profiles (id, email)
  values (new.id, new.email)
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- Backfill profiles for any users who signed up before this trigger existed.
insert into public.profiles (id, email)
select id, email from auth.users
on conflict (id) do nothing;

-- Helper used by the security rules below: is the current user an admin?
create or replace function public.is_admin()
returns boolean
language sql
security definer set search_path = public
stable
as $$
  select coalesce((select is_admin from public.profiles where id = auth.uid()), false);
$$;


-- ------------------------------------------------------------
-- 3) ROW LEVEL SECURITY (who can read / write what)
-- ------------------------------------------------------------

alter table public.profiles enable row level security;
alter table public.lessons enable row level security;
alter table public.exercises enable row level security;
alter table public.user_progress enable row level security;

-- PROFILES: a user can see and edit only their own profile.
drop policy if exists profiles_select_own on public.profiles;
create policy profiles_select_own on public.profiles
  for select using (auth.uid() = id);

drop policy if exists profiles_update_own on public.profiles;
create policy profiles_update_own on public.profiles
  for update using (auth.uid() = id);

-- LESSONS: everyone can read published lessons; admins can read everything.
drop policy if exists lessons_select on public.lessons;
create policy lessons_select on public.lessons
  for select using (is_published = true or public.is_admin());

-- Only admins can create / edit / delete lessons.
drop policy if exists lessons_admin_write on public.lessons;
create policy lessons_admin_write on public.lessons
  for all using (public.is_admin()) with check (public.is_admin());

-- EXERCISES: readable if their lesson is published (or you are an admin).
drop policy if exists exercises_select on public.exercises;
create policy exercises_select on public.exercises
  for select using (
    public.is_admin()
    or exists (
      select 1 from public.lessons l
      where l.id = exercises.lesson_id and l.is_published = true
    )
  );

-- Only admins can create / edit / delete exercises.
drop policy if exists exercises_admin_write on public.exercises;
create policy exercises_admin_write on public.exercises
  for all using (public.is_admin()) with check (public.is_admin());

-- USER PROGRESS: each user can only see and change their own rows.
drop policy if exists progress_select_own on public.user_progress;
create policy progress_select_own on public.user_progress
  for select using (auth.uid() = user_id);

drop policy if exists progress_insert_own on public.user_progress;
create policy progress_insert_own on public.user_progress
  for insert with check (auth.uid() = user_id);

drop policy if exists progress_update_own on public.user_progress;
create policy progress_update_own on public.user_progress
  for update using (auth.uid() = user_id);


-- ------------------------------------------------------------
-- 4) API GRANTS (required for the website to read/write via Supabase)
-- ------------------------------------------------------------

grant usage on schema public to anon, authenticated;

grant select on public.lessons to anon, authenticated;
grant select on public.exercises to anon, authenticated;
grant select on public.profiles to anon, authenticated;

grant select, insert, update on public.user_progress to authenticated;

grant insert, update, delete on public.lessons to authenticated;
grant insert, update, delete on public.exercises to authenticated;
grant update on public.profiles to authenticated;

grant usage, select on all sequences in schema public to anon, authenticated;


-- ============================================================
-- Done. Next: run make-admin.sql to make YOUR account an admin,
-- and optionally seed-sample.sql to add one demo lesson.
-- ============================================================
