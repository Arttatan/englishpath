-- A1 Vocabulary: Daily routines — 3 exercises like test-english.com
-- Run after alter-lettered-gap.sql (safe to run more than once)

do $$
declare
  lid bigint;
begin
  select id into lid from public.lessons
  where title = 'Daily routines' and level = 'a1' and section = 'vocabulary'
  limit 1;

  if lid is null then
    insert into public.lessons
      (title, level, section, explanation, is_published, is_premium, sort_order)
    values
      (
        'Daily routines',
        'a1',
        'vocabulary',
        '<h2>Daily routines — vocabulary</h2><p>Learn common phrases to talk about your day.</p><ul><li><strong>get up</strong> — leave your bed in the morning</li><li><strong>have breakfast</strong> — eat in the morning</li><li><strong>go to bed</strong> — go to sleep at night</li><li><strong>brush my teeth</strong> — clean your teeth</li></ul>',
        true,
        false,
        2
      )
    returning id into lid;
  end if;

  if exists (select 1 from public.exercise_sets where lesson_id = lid) then
    raise notice 'Daily routines exercises already exist for lesson %', lid;
    return;
  end if;

  insert into public.exercise_sets
    (lesson_id, title, instructions, type, word_bank, use_once, questions, sort_order)
  values
    (
      lid,
      'Exercise 1',
      'Choose the correct option for each gap.',
      'lettered_gap',
      null,
      false,
      '[
        {"text": "After I ____, I get dressed and go to school. | *have breakfast | go shopping | watch TV", "feedback": ""},
        {"text": "Before I go to bed, I ____. | *brush my teeth | go to the gym | have lunch", "feedback": ""},
        {"text": "I usually ____ at 7:00 in the morning. | *get up | go to bed | go shopping", "feedback": ""}
      ]'::jsonb,
      1
    ),
    (
      lid,
      'Exercise 2',
      'Choose the correct option to complete these sentences. Use each option ONLY ONCE.',
      'dropdown_gap',
      '["go shopping","watch TV","check my emails","go to the gym","have lunch","go to bed","get up","have breakfast","starts work","have a shower"]'::jsonb,
      true,
      '[
        {"text": "After I ___ in the morning, I make my bed. | get up", "feedback": ""},
        {"text": "Sam ___ at 9:00 every morning. | starts work", "feedback": ""},
        {"text": "The children put on their pyjamas before they ___. | go to bed", "feedback": ""},
        {"text": "We ___ together at 1:00 p.m. | have lunch", "feedback": ""},
        {"text": "I like to ___ after work. | go to the gym", "feedback": ""}
      ]'::jsonb,
      2
    ),
    (
      lid,
      'Exercise 3',
      'Choose the correct option for each gap.',
      'lettered_gap',
      null,
      false,
      '[
        {"text": "I ____ every evening after dinner. | *watch TV | get up | have breakfast", "feedback": ""},
        {"text": "She ____ before breakfast. | *has a shower | goes shopping | goes to bed", "feedback": ""},
        {"text": "He ____ on Saturday mornings. | *goes shopping | brushes his teeth | starts work", "feedback": ""}
      ]'::jsonb,
      3
    );
end $$;
