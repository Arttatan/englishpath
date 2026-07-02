-- ============================================================
-- Make YOUR account an admin.
-- Replace the email below with the email you registered with,
-- then run this in Supabase → SQL Editor.
-- ============================================================

update public.profiles
set is_admin = true
where email = 'YOUR_EMAIL_HERE';

-- Check the result (should show your row with is_admin = true):
select id, email, is_admin, is_premium from public.profiles;
