-- ============================================================
-- OPTIONAL: add one demo lesson so you can test the site before
-- the admin panel is ready. Run this ONCE in Supabase → SQL Editor.
-- You can delete this lesson later from the admin panel (Step 5).
-- ============================================================

with new_lesson as (
  insert into public.lessons
    (title, level, section, explanation, is_published, is_premium, sort_order)
  values
    (
      'Present Simple: he / she / it',
      'a1',
      'grammar',
      '<p>With <strong>he</strong>, <strong>she</strong> and <strong>it</strong> we add <strong>-s</strong> (or <strong>-es</strong>) to the verb in the Present Simple.</p><ul><li>She <strong>works</strong> in a bank.</li><li>He <strong>goes</strong> to school every day.</li></ul>',
      true,   -- published
      false,  -- free for everyone
      1
    )
  returning id
)
insert into public.exercises
  (lesson_id, type, question, options, correct_answer, explanation, sort_order)
select id, 'multiple_choice', 'She ____ to school every day.',
       '["go","goes","going"]'::jsonb, '"goes"'::jsonb,
       'With he / she / it we add -es, so the answer is "goes".', 1
from new_lesson
union all
select id, 'multiple_choice', 'He ____ in a bank.',
       '["work","works","working"]'::jsonb, '"works"'::jsonb,
       'With he / she / it we add -s, so the answer is "works".', 2
from new_lesson;
