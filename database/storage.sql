-- Supabase Storage bucket for lesson audio / images (admin upload, public read).

insert into storage.buckets (id, name, public)
values ('lesson-media', 'lesson-media', true)
on conflict (id) do update set public = true;

drop policy if exists "Public read lesson media" on storage.objects;
create policy "Public read lesson media"
  on storage.objects for select
  using (bucket_id = 'lesson-media');

drop policy if exists "Admins upload lesson media" on storage.objects;
create policy "Admins upload lesson media"
  on storage.objects for insert
  with check (bucket_id = 'lesson-media' and public.is_admin());

drop policy if exists "Admins update lesson media" on storage.objects;
create policy "Admins update lesson media"
  on storage.objects for update
  using (bucket_id = 'lesson-media' and public.is_admin());

drop policy if exists "Admins delete lesson media" on storage.objects;
create policy "Admins delete lesson media"
  on storage.objects for delete
  using (bucket_id = 'lesson-media' and public.is_admin());
