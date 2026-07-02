-- Make all currently existing accounts admins (these are the owner's test
-- accounts created so far). New sign-ups will NOT be admins by default.
update public.profiles set is_admin = true;

-- Show the result so we can confirm.
select id, email, is_admin, is_premium from public.profiles;
