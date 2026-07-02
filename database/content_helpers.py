"""Shared helpers for building lesson JSON files."""

from __future__ import annotations


def ic(correct: str, w1: str, w2: str, before: str = "", after: str = "", feedback: str = "") -> dict:
    return {
        "text": f"{before}[*{correct}|{w1}|{w2}]{after}",
        "feedback": feedback or f"Correct: {correct}.",
    }


def lg(sentence: str, *options: str, feedback: str = "") -> dict:
    return {"text": f"{sentence} | {' | '.join(options)}", "feedback": feedback}


def dd(sentence: str, answer: str, feedback: str = "") -> dict:
    return {"text": f"{sentence} | {answer}", "feedback": feedback}


def split_three(qs: list[dict], types: tuple[str, ...] = ("inline_choice", "lettered_gap", "inline_choice")) -> list[dict]:
    instructions = [
        "Choose the correct option to complete the sentences.",
        "Choose the correct option for each gap.",
        "Choose the correct option to complete the sentences.",
    ]
    n = max(len(qs), 3)
    size = max(1, len(qs) // 3)
    parts = [qs[i * size : (i + 1) * size] for i in range(2)]
    parts.append(qs[2 * size :])
    parts = [p for p in parts if p]
    while len(parts) < 3 and qs:
        parts.append(qs[-2:])
    out = []
    for i in range(min(3, len(parts))):
        out.append(
            {
                "title": f"Exercise {i + 1}",
                "instructions": instructions[i],
                "type": types[i] if i < len(types) else "inline_choice",
                "questions": parts[i],
            }
        )
    return out


def lesson(title: str, level: str, section: str, sort_order: int, explanation: str, exercise_sets: list[dict], **extra) -> dict:
    return {"title": title, "level": level, "section": section, "sort_order": sort_order, "explanation": explanation, "exercise_sets": exercise_sets, **extra}


def grammar_lesson(title, level, sort, explanation, inline_qs, gap_qs, inline2_qs):
    return lesson(
        title,
        level,
        "grammar",
        sort,
        explanation,
        [
            {"title": "Exercise 1", "instructions": "Choose the correct option to complete the sentences.", "type": "inline_choice", "questions": inline_qs},
            {"title": "Exercise 2", "instructions": "Choose the correct option for each gap.", "type": "lettered_gap", "questions": gap_qs},
            {"title": "Exercise 3", "instructions": "Choose the correct option to complete the sentences.", "type": "inline_choice", "questions": inline2_qs},
        ],
    )


def vocab_lesson(title, level, sort, explanation, pairs):
    lettered1 = [lg(s, f"*{c}", d[0], d[1]) for s, c, d in pairs[:4]]
    bank = []
    for _, c, ds in pairs:
        bank.extend([c, ds[0], ds[1]])
    bank = list(dict.fromkeys(bank))[:12]
    dropdown = [dd(s.replace("____", "___"), c) for s, c, _ in pairs[:5]]
    lettered2 = [lg(s, f"*{c}", d[0], d[1]) for s, c, d in pairs[4:8]]
    return lesson(
        title,
        level,
        "vocabulary",
        sort,
        explanation,
        [
            {"title": "Exercise 1", "instructions": "Choose the correct option for each gap.", "type": "lettered_gap", "questions": lettered1},
            {"title": "Exercise 2", "instructions": "Choose the correct option. Use each option ONLY ONCE.", "type": "dropdown_gap", "use_once": True, "word_bank": bank, "questions": dropdown},
            {"title": "Exercise 3", "instructions": "Choose the correct option for each gap.", "type": "lettered_gap", "questions": lettered2 or lettered1[:3]},
        ],
    )


def skill_lesson(title, level, section, sort, explanation, qs, audio_url=None):
    sets = split_three(qs)
    extra = {"audio_url": audio_url} if audio_url else {}
    return lesson(title, level, section, sort, explanation, sets, **extra)
