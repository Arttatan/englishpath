-- Allow multiple_choice exercise type (4-option MCQ with pagination).

alter table public.exercise_sets drop constraint if exists exercise_sets_type_check;
alter table public.exercise_sets
  add constraint exercise_sets_type_check
  check (type in ('inline_choice', 'dropdown_gap', 'lettered_gap', 'multiple_choice'));

alter table public.lessons
  add column if not exists cover_key text;
