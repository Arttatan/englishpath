-- Fix: grant table access to Supabase API roles (anon + authenticated).
-- Tables created via direct SQL do not get these grants automatically.

grant usage on schema public to anon, authenticated;

grant select on public.lessons to anon, authenticated;
grant select on public.exercises to anon, authenticated;
grant select on public.profiles to anon, authenticated;

grant select, insert, update on public.user_progress to authenticated;

grant insert, update, delete on public.lessons to authenticated;
grant insert, update, delete on public.exercises to authenticated;
grant update on public.profiles to authenticated;

grant usage, select on all sequences in schema public to anon, authenticated;
