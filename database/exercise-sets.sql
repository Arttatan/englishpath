-- Exercise sets: matches test-english.com structure (Exercise 1, 2, 3… per lesson).
-- Each set has its own instructions and a list of questions stored as JSON.

create table if not exists public.exercise_sets (
  id bigint generated always as identity primary key,
  lesson_id bigint not null references public.lessons(id) on delete cascade,
  title text not null default 'Exercise 1',
  instructions text,
  type text not null check (type in ('inline_choice', 'dropdown_gap', 'lettered_gap')),
  word_bank jsonb,
  use_once boolean not null default false,
  questions jsonb not null default '[]'::jsonb,
  sort_order int not null default 0,
  created_at timestamptz not null default now()
);

create index if not exists idx_exercise_sets_lesson on public.exercise_sets(lesson_id);

alter table public.lessons
  add column if not exists pdf_url text;

alter table public.exercise_sets enable row level security;

drop policy if exists exercise_sets_select on public.exercise_sets;
create policy exercise_sets_select on public.exercise_sets
  for select using (
    public.is_admin()
    or exists (
      select 1 from public.lessons l
      where l.id = exercise_sets.lesson_id and l.is_published = true
    )
  );

drop policy if exists exercise_sets_admin_write on public.exercise_sets;
create policy exercise_sets_admin_write on public.exercise_sets
  for all using (public.is_admin()) with check (public.is_admin());

grant select on public.exercise_sets to anon, authenticated;
grant insert, update, delete on public.exercise_sets to authenticated;

-- Migrate existing demo lesson (old exercises table) into one inline_choice set.
insert into public.exercise_sets (lesson_id, title, instructions, type, questions, sort_order)
select
  e.lesson_id,
  'Exercise 1',
  'Choose the correct option to complete the sentence.',
  'inline_choice',
  jsonb_agg(
    jsonb_build_object(
      'text', e.question || ' [' ||
        coalesce(
          (select string_agg(
            case when opt = (e.correct_answer #>> '{}')
              then '*' || opt else opt end, '|' order by ord)
           from jsonb_array_elements_text(e.options) with ordinality as t(opt, ord)),
          ''
        ) || ']',
      'feedback', coalesce(e.explanation, '')
    )
    order by e.sort_order
  ),
  1
from public.exercises e
where not exists (
  select 1 from public.exercise_sets es where es.lesson_id = e.lesson_id
)
group by e.lesson_id;
