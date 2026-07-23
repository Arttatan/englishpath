-- EnglishPath — Stripe Premium fields + protect is_premium from client updates
-- Run in Supabase → SQL Editor (safe to re-run)

alter table public.profiles
  add column if not exists stripe_customer_id text,
  add column if not exists stripe_subscription_id text,
  add column if not exists premium_until timestamptz;

create unique index if not exists idx_profiles_stripe_customer
  on public.profiles (stripe_customer_id)
  where stripe_customer_id is not null;

-- Clients may update their own profile row, but cannot change billing fields.
-- service_role JWT and direct Postgres (server) may update them.
create or replace function public.protect_billing_fields()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
  jwt_role text;
begin
  jwt_role := coalesce(auth.jwt() ->> 'role', '');
  if jwt_role = 'service_role' then
    return new;
  end if;

  if current_user = 'postgres'
     or current_user = 'supabase_admin'
     or current_user like 'postgres.%' then
    return new;
  end if;

  new.is_premium := old.is_premium;
  new.stripe_customer_id := old.stripe_customer_id;
  new.stripe_subscription_id := old.stripe_subscription_id;
  new.premium_until := old.premium_until;
  new.is_admin := old.is_admin;
  return new;
end;
$$;

drop trigger if exists trg_protect_billing_fields on public.profiles;
create trigger trg_protect_billing_fields
  before update on public.profiles
  for each row
  execute function public.protect_billing_fields();
