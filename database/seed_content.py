"""
Load lesson JSON files from database/content/ into Supabase Postgres.

Usage (PowerShell):
    $env:SUPA_DB_URL = "postgresql://..."
    python database/seed_content.py
    python database/seed_content.py database/content/grammar/a1/present-simple-to-be.json --upsert

By default, skips lessons that already exist (title + level + section).
With --upsert, replaces explanation/sets/cover for matching lessons.
"""

import json
import os
import sys
from pathlib import Path

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    print("Install: python -m pip install psycopg2-binary")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent
CONTENT_DIR = ROOT / "content"


def collect_json_files(target: Path | None) -> list[Path]:
    base = target if target else CONTENT_DIR
    if base.is_file() and base.suffix == ".json":
        return [base]
    return sorted(base.rglob("*.json"))


def load_lesson(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = {"title", "level", "section", "explanation", "exercise_sets"}
    missing = required - data.keys()
    if missing:
        raise ValueError(f"{path}: missing fields {missing}")
    if not data["exercise_sets"]:
        raise ValueError(f"{path}: exercise_sets is empty")
    return data


def normalize_questions(es: dict) -> list:
    """Support classic {text,feedback} and MCQ {prompt,options,correct,feedback}."""
    out = []
    for q in es["questions"]:
        if "options" in q and "correct" in q:
            out.append(
                {
                    "prompt": q.get("prompt") or q.get("text") or "",
                    "options": q["options"],
                    "correct": q["correct"],
                    "feedback": q.get("feedback", ""),
                }
            )
        else:
            out.append({"text": q.get("text", ""), "feedback": q.get("feedback", "")})
    return out


def insert_sets(cur, lesson_id: int, data: dict) -> None:
    cur.execute("DELETE FROM public.exercise_sets WHERE lesson_id = %s", (lesson_id,))
    for i, es in enumerate(data["exercise_sets"], start=1):
        questions = normalize_questions(es)
        word_bank = es.get("word_bank")
        cur.execute(
            """
            INSERT INTO public.exercise_sets
              (lesson_id, title, instructions, type, word_bank, use_once, questions, sort_order)
            VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb, %s)
            """,
            (
                lesson_id,
                es.get("title", f"Exercise {i}"),
                es.get("instructions", "Complete the exercise below."),
                es["type"],
                json.dumps(word_bank) if word_bank else None,
                es.get("use_once", False),
                json.dumps(questions),
                es.get("sort_order", i),
            ),
        )


def seed_lesson(cur, data: dict, upsert: bool = False) -> str:
    cur.execute(
        """
        SELECT id FROM public.lessons
        WHERE title = %s AND level = %s AND section = %s
        LIMIT 1
        """,
        (data["title"], data["level"], data["section"]),
    )
    row = cur.fetchone()

    if row and not upsert:
        return f"skip  {data['level']}/{data['section']}: {data['title']}"

    if row and upsert:
        lesson_id = row[0]
        cur.execute(
            """
            UPDATE public.lessons SET
              explanation = %s,
              audio_url = %s,
              pdf_url = %s,
              sort_order = %s,
              cover_key = %s,
              is_published = true,
              updated_at = now()
            WHERE id = %s
            """,
            (
                data["explanation"],
                data.get("audio_url"),
                data.get("pdf_url"),
                data.get("sort_order", 0),
                data.get("cover_key"),
                lesson_id,
            ),
        )
        insert_sets(cur, lesson_id, data)
        return f"upsert {data['level']}/{data['section']}: {data['title']} (id {lesson_id})"

    cur.execute(
        """
        INSERT INTO public.lessons
          (title, level, section, explanation, audio_url, pdf_url,
           is_published, is_premium, sort_order, cover_key, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, true, false, %s, %s, now())
        RETURNING id
        """,
        (
            data["title"],
            data["level"],
            data["section"],
            data["explanation"],
            data.get("audio_url"),
            data.get("pdf_url"),
            data.get("sort_order", 0),
            data.get("cover_key"),
        ),
    )
    lesson_id = cur.fetchone()[0]
    insert_sets(cur, lesson_id, data)
    return f"added {data['level']}/{data['section']}: {data['title']} (id {lesson_id})"


def main():
    db_url = os.environ.get("SUPA_DB_URL")
    if not db_url:
        print("ERROR: set SUPA_DB_URL environment variable.")
        sys.exit(1)

    args = [a for a in sys.argv[1:] if a != "--upsert"]
    upsert = "--upsert" in sys.argv[1:]

    targets = [Path(p) for p in args] if args else [CONTENT_DIR]
    files = []
    for t in targets:
        files.extend(collect_json_files(t))

    if not files:
        print(f"No JSON files found under {CONTENT_DIR}")
        sys.exit(1)

    conn = psycopg2.connect(db_url, sslmode="require", connect_timeout=15)
    conn.autocommit = True
    added = skipped = errors = 0

    try:
        with conn.cursor() as cur:
            for path in files:
                if path.name == "index.json":
                    continue
                try:
                    data = load_lesson(path)
                    msg = seed_lesson(cur, data, upsert=upsert)
                    print(msg)
                    if msg.startswith("added") or msg.startswith("upsert"):
                        added += 1
                    else:
                        skipped += 1
                except Exception as e:
                    errors += 1
                    print(f"ERROR {path}: {e}")
    finally:
        conn.close()

    print(f"\nDone: {added} added/upserted, {skipped} skipped, {errors} errors.")


if __name__ == "__main__":
    main()
