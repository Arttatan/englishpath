-- B1 Grammar lesson: Present Perfect vs Past Simple
-- 12 inline-choice questions (3 options each, grammar style like test-english.com)

with new_lesson as (
  insert into public.lessons
    (title, level, section, explanation, is_published, is_premium, sort_order)
  values
    (
      'Present Perfect vs Past Simple',
      'b1',
      'grammar',
      '<h2>Present Perfect vs Past Simple</h2>
<p>We use the <strong>Past Simple</strong> for finished actions at a specific time in the past (<em>yesterday, last week, in 2010</em>).</p>
<p>We use the <strong>Present Perfect</strong> for:</p>
<ul>
<li>experiences without a specific time (<em>I have visited Paris</em>)</li>
<li>actions that started in the past and continue now (<em>She has lived here since 2015</em>)</li>
<li>recent news with <em>just, already, yet</em></li>
</ul>
<h3>Quick contrast</h3>
<ul>
<li><strong>Past Simple:</strong> I <em>saw</em> him yesterday.</li>
<li><strong>Present Perfect:</strong> I <em>have seen</em> him this week.</li>
<li><strong>Past Simple:</strong> She <em>went</em> to Italy last summer.</li>
<li><strong>Present Perfect:</strong> She <em>has been</em> to Italy three times.</li>
</ul>',
      true,
      false,
      1
    )
  returning id
)
insert into public.exercise_sets
  (lesson_id, title, instructions, type, word_bank, use_once, questions, sort_order)
select
  id,
  'Exercise 1',
  'Choose the correct form to complete each sentence.',
  'inline_choice',
  null,
  false,
  '[
    {"text": "I [*have seen|saw|see] this film before — I remember the ending.", "feedback": "Use the present perfect for life experience without a specific past time."},
    {"text": "She [*went|has gone|goes] to Berlin last summer on holiday.", "feedback": "Past simple is used with a finished time (last summer)."},
    {"text": "They [*have lived|lived|live] in Manchester since 2018.", "feedback": "Present perfect + since shows an action that started in the past and continues now."},
    {"text": "We [*did not see|have not seen|do not see] him at the party yesterday.", "feedback": "Yesterday is a finished past time → past simple."},
    {"text": "How long [*have you known|did you know|you know] your neighbour?", "feedback": "How long …? often takes present perfect when the situation continues."},
    {"text": "I [*have just finished|just finished|finished just] my report. Can you read it?", "feedback": "Just + present perfect describes a very recent action."},
    {"text": "He [*has never been|never was|did not never be] to South America.", "feedback": "Never + present perfect for experiences up to now."},
    {"text": "When [*did you buy|have you bought|you bought] this laptop?", "feedback": "When …? asks for a specific past moment → past simple."},
    {"text": "She [*has worked|worked|works] at the hospital for twelve years.", "feedback": "For + period of time that continues → present perfect."},
    {"text": "I [*met|have met|meet] my partner at a concert in 2015.", "feedback": "A specific year in the past → past simple."},
    {"text": "There [*has been|was|is] a lot of traffic on the roads this morning.", "feedback": "Recent news / today with present time reference → present perfect is common."},
    {"text": "We [*have not decided|did not decide|do not decide] where to go yet.", "feedback": "Yet with present perfect in negative sentences."}
  ]'::jsonb,
  1
from new_lesson;
