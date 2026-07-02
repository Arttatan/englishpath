-- Allow lettered_gap exercise type (vocabulary with vertical A/B/C options).

alter table public.exercise_sets drop constraint if exists exercise_sets_type_check;
alter table public.exercise_sets
  add constraint exercise_sets_type_check
  check (type in ('inline_choice', 'dropdown_gap', 'lettered_gap'));
