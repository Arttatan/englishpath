const { getPool, getUserFromAuthHeader, sendJson } = require("../lib/server-helpers");

const LESSONS = {
  "have-got": () => require("../database/content/grammar/a1/have-got.json"),
};

function loadLesson(key) {
  const loader = LESSONS[key];
  return loader ? loader() : null;
}

function normalizeQuestions(es) {
  const esType = es.type;
  if (esType === "dual_type_gap" || esType === "dialogue_gap") return es.questions;
  return (es.questions || []).map((q) => {
    if (q.options && q.correct !== undefined) {
      return {
        prompt: q.prompt || q.text || "",
        options: q.options,
        correct: q.correct,
        feedback: q.feedback || "",
      };
    }
    if (q.answers && (q.source || q.example)) {
      const item = {
        source: q.source || "",
        before: q.before || "",
        after: q.after || "",
        answers: q.answers,
        feedback: q.feedback || "",
      };
      if (q.example) item.example = true;
      return item;
    }
    return { text: q.text || "", feedback: q.feedback || "" };
  });
}

async function insertSets(client, lessonId, data) {
  await client.query("DELETE FROM public.exercise_sets WHERE lesson_id = $1", [lessonId]);
  for (let i = 0; i < (data.exercise_sets || []).length; i++) {
    const es = data.exercise_sets[i];
    const questions = normalizeQuestions(es);
    const wordBank = es.word_bank ? JSON.stringify(es.word_bank) : null;
    await client.query(
      `INSERT INTO public.exercise_sets
        (lesson_id, title, instructions, type, word_bank, use_once, questions, sort_order)
       VALUES ($1, $2, $3, $4, $5::jsonb, $6, $7::jsonb, $8)`,
      [
        lessonId,
        es.title || `Exercise ${i + 1}`,
        es.instructions || "Complete the exercise below.",
        es.type,
        wordBank,
        !!es.use_once,
        JSON.stringify(questions),
        es.sort_order || i + 1,
      ]
    );
  }
}

async function isAdmin(userId) {
  const { rows } = await getPool().query("select is_admin from public.profiles where id = $1", [userId]);
  return !!rows[0]?.is_admin;
}

module.exports = async function handler(req, res) {
  if (req.method !== "POST") return sendJson(res, 405, { error: "Method not allowed" });

  try {
    const user = await getUserFromAuthHeader(req);
    if (!user) return sendJson(res, 401, { error: "Please log in first." });
    if (!(await isAdmin(user.id))) return sendJson(res, 403, { error: "Admin access only." });

    let body = {};
    try {
      const chunks = [];
      for await (const chunk of req) chunks.push(chunk);
      const raw = Buffer.concat(chunks).toString("utf8");
      if (raw) body = JSON.parse(raw);
    } catch (_) {
      body = {};
    }

    const key = body.lesson || "have-got";
    const data = loadLesson(key);
    if (!data) return sendJson(res, 400, { error: "Unknown lesson key." });

    const pool = getPool();
    const existing = await pool.query(
      `SELECT id FROM public.lessons
       WHERE title = $1 AND level = $2 AND section = $3
       LIMIT 1`,
      [data.title, data.level, data.section]
    );

    if (existing.rows[0] && !body.upsert) {
      return sendJson(res, 200, { status: "skip", id: existing.rows[0].id });
    }

    const client = await pool.connect();
    try {
      await client.query("BEGIN");
      let lessonId;
      if (existing.rows[0]) {
        lessonId = existing.rows[0].id;
        await client.query(
          `UPDATE public.lessons SET
             explanation = $1, audio_url = $2, pdf_url = $3,
             sort_order = $4, cover_key = $5, is_published = true, is_premium = false,
             updated_at = now()
           WHERE id = $6`,
          [
            data.explanation,
            data.audio_url || null,
            data.pdf_url || null,
            data.sort_order || 0,
            data.cover_key || null,
            lessonId,
          ]
        );
      } else {
        const inserted = await client.query(
          `INSERT INTO public.lessons
             (title, level, section, explanation, audio_url, pdf_url,
              is_published, is_premium, sort_order, cover_key, updated_at)
           VALUES ($1, $2, $3, $4, $5, $6, true, false, $7, $8, now())
           RETURNING id`,
          [
            data.title,
            data.level,
            data.section,
            data.explanation,
            data.audio_url || null,
            data.pdf_url || null,
            data.sort_order || 0,
            data.cover_key || null,
          ]
        );
        lessonId = inserted.rows[0].id;
      }
      await insertSets(client, lessonId, data);
      await client.query("COMMIT");
      return sendJson(res, 200, {
        status: existing.rows[0] ? "upsert" : "added",
        id: lessonId,
      });
    } catch (err) {
      await client.query("ROLLBACK");
      throw err;
    } finally {
      client.release();
    }
  } catch (err) {
    console.error("admin-seed-lesson", err);
    return sendJson(res, 500, { error: err.message || "Seed failed" });
  }
};
