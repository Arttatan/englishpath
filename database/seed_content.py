"""
Load lesson JSON files from database/content/ into Supabase Postgres.

Usage (PowerShell):
    $env:SUPA_DB_URL = "postgresql://..."
    python database/seed_content.py
    python database/seed_content.py database/content/grammar/a1

Skips lessons that already exist (matched by title + level + section).
Re-running is safe.
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


def seed_lesson(cur, data: dict) -> str:
    cur.execute(
        """
        SELECT id FROM public.lessons
        WHERE title = %s AND level = %s AND section = %s
        LIMIT 1
        """,
        (data["title"], data["level"], data["section"]),
    )
    row = cur.fetchone()
    if row:
        return f"skip  {data['level']}/{data['section']}: {data['title']}"

    cur.execute(
        """
        INSERT INTO public.lessons
          (title, level, section, explanation, audio_url, pdf_url,
           is_published, is_premium, sort_order, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, true, false, %s, now())
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
        ),
    )
    lesson_id = cur.fetchone()[0]

    for i, es in enumerate(data["exercise_sets"], start=1):
        questions = [{"text": q["text"], "feedback": q.get("feedback", "")} for q in es["questions"]]
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

    return f"added {data['level']}/{data['section']}: {data['title']} (id {lesson_id})"


def main():
    db_url = os.environ.get("SUPA_DB_URL")
    if not db_url:
        print("ERROR: set SUPA_DB_URL environment variable.")
        sys.exit(1)

    targets = [Path(p) for p in sys.argv[1:]] if len(sys.argv) > 1 else [CONTENT_DIR]
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
                    msg = seed_lesson(cur, data)
                    print(msg)
                    if msg.startswith("added"):
                        added += 1
                    else:
                        skipped += 1
                except Exception as e:
                    errors += 1
                    print(f"ERROR {path}: {e}")
    finally:
        conn.close()

    print(f"\nDone: {added} added, {skipped} skipped, {errors} errors.")


if __name__ == "__main__":
    main()
