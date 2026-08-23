/*
  Exercise rendering & checking — matches test-english.com UI.
 *
 * Grammar / lettered: sentence + vertical A B C options (not in a row).
 * Vocabulary / dropdown: inline <select> gaps + shared word bank + use-once.
 */

window.ExerciseEngine = (function () {
  const LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H"];

  function parseInlineText(text) {
    const parts = [];
    const regex = /\[([^\]]+)\]/g;
    let last = 0;
    let match;
    while ((match = regex.exec(text)) !== null) {
      if (match.index > last) {
        parts.push({ type: "text", value: text.slice(last, match.index) });
      }
      const raw = match[1].split("|").map((s) => s.trim());
      let correct = 0;
      const options = raw.map((opt, i) => {
        if (opt.startsWith("*")) {
          correct = i;
          return opt.slice(1).trim();
        }
        return opt;
      });
      parts.push({ type: "choice", options, correct });
      last = regex.lastIndex;
    }
    if (last < text.length) parts.push({ type: "text", value: text.slice(last) });
    return parts;
  }

  /** lettered_gap: "After I ____, I get dressed. | *have breakfast | go shopping" */
  function parseLetteredGap(text) {
    const pipe = text.indexOf("|");
    const sentence = (pipe >= 0 ? text.slice(0, pipe) : text).trim();
    const opts =
      pipe >= 0
        ? text
            .slice(pipe + 1)
            .split("|")
            .map((s) => s.trim())
            .filter(Boolean)
        : [];
    let correct = 0;
    const options = opts.map((opt, i) => {
      if (opt.startsWith("*")) {
        correct = i;
        return opt.slice(1).trim();
      }
      return opt;
    });
    return { sentence, options, correct };
  }

  function parseDropdownText(text) {
    const pipe = text.indexOf("|");
    const sentence = (pipe >= 0 ? text.slice(0, pipe) : text).trim();
    const answers =
      pipe >= 0
        ? text
            .slice(pipe + 1)
            .split("|")
            .map((s) => s.trim())
            .filter(Boolean)
        : [];
    const blankCount = (sentence.match(/___/g) || []).length;
    return { sentence, answers, blankCount: Math.max(blankCount, 1) };
  }

  /** Sentence with blank + vertical lettered options (test-english grammar & vocab style 1) */
  function renderLettered(parts, qIndex) {
    const sentence = parts.map((p) => (p.type === "text" ? p.value : "______")).join("");
    const choice = parts.find((p) => p.type === "choice");
    if (!choice) return `<p class="te-q-sentence">${escapeHtml(sentence)}</p>`;

    let html = `<p class="te-q-sentence">${escapeHtml(sentence)}</p>`;
    html += `<div class="te-options-stack" data-stack-for="${qIndex}">`;
    choice.options.forEach((opt, oi) => {
      html += `
        <label class="te-option-row">
          <input type="radio" class="sr-only" name="q${qIndex}" value="${oi}" data-lettered-choice />
          <span class="te-option-letter">${LETTERS[oi]}.</span>
          <span class="te-option-text">${escapeHtml(opt)}</span>
        </label>`;
    });
    html += `</div>`;
    return html;
  }

  function renderLetteredGap(parsed, qIndex) {
    let html = `<p class="te-q-sentence">${escapeHtml(parsed.sentence)}</p>`;
    html += `<div class="te-options-stack" data-stack-for="${qIndex}">`;
    parsed.options.forEach((opt, oi) => {
      html += `
        <label class="te-option-row">
          <input type="radio" class="sr-only" name="q${qIndex}" value="${oi}" data-lettered-choice />
          <span class="te-option-letter">${LETTERS[oi]}.</span>
          <span class="te-option-text">${escapeHtml(opt)}</span>
        </label>`;
    });
    html += `</div>`;
    return html;
  }

  /** Inline dropdown gaps (test-english vocabulary style 2) */
  function renderDropdown(sentence, qIndex, wordBank) {
    const pieces = sentence.split("___");
    let html = `<p class="te-q-sentence te-q-sentence-inline">`;
    for (let i = 0; i < pieces.length; i++) {
      html += escapeHtml(pieces[i]);
      if (i < pieces.length - 1) {
        html += `<select class="te-dropdown" data-gap-index="${i}" data-q="${qIndex}" aria-label="Choose an option">
          <option value="">— select —</option>
          ${wordBank
            .map((w) => `<option value="${escapeAttr(w)}">${escapeHtml(w)}</option>`)
            .join("")}
        </select>`;
      }
    }
    html += `</p>`;
    return html;
  }

  function checkLetteredStack(stackEl, correctIndex) {
    const selected = stackEl.querySelector("input[data-lettered-choice]:checked");
    const ok = !!(selected && Number(selected.value) === correctIndex);

    stackEl.querySelectorAll(".te-option-row").forEach((row, oi) => {
      row.classList.remove("te-selected", "te-correct", "te-wrong", "te-reveal-correct");
      const inp = row.querySelector("input");
      if (inp?.checked) row.classList.add(ok ? "te-correct" : "te-wrong");
      if (!ok && oi === correctIndex) row.classList.add("te-reveal-correct");
    });
    return ok;
  }

  function checkDropdown(container, answers, useOnce, usedBank) {
    const selects = container.querySelectorAll("select.te-dropdown");
    let allCorrect = true;
    selects.forEach((sel, i) => {
      const expected = (answers[i] || "").trim().toLowerCase();
      const got = (sel.value || "").trim().toLowerCase();
      let ok = expected && got === expected;
      if (useOnce && sel.value) {
        if (usedBank.has(sel.value)) ok = false;
        else usedBank.add(sel.value);
      }
      if (!ok) allCorrect = false;
      sel.classList.toggle("te-select-correct", ok);
      sel.classList.toggle("te-select-wrong", !ok && sel.value);
      sel.disabled = true;
    });
    return allCorrect;
  }

  function wireDropdownUseOnce(rootEl) {
    const selects = rootEl.querySelectorAll("select.te-dropdown");
    function refresh() {
      const chosen = new Set();
      selects.forEach((s) => {
        if (s.value) chosen.add(s.value);
      });
      selects.forEach((s) => {
        if (s.disabled) return;
        s.querySelectorAll("option").forEach((opt) => {
          if (!opt.value) return;
          opt.hidden = chosen.has(opt.value) && s.value !== opt.value;
        });
      });
    }
    selects.forEach((sel) => sel.addEventListener("change", refresh));
  }

  /**
   * Inline dropdowns per gap (test-english grammar style).
   * Text uses same [opt|*correct|opt] markers as inline_choice.
   */
  function renderInlineDropdown(parts, qIndex) {
    let html = `<p class="te-q-sentence te-q-sentence-inline">`;
    let gap = 0;
    parts.forEach((p) => {
      if (p.type === "text") {
        html += escapeHtml(p.value);
        return;
      }
      const opts = p.options
        .map(
          (o, i) =>
            `<option value="${i}">${escapeHtml(o)}</option>`
        )
        .join("");
      html += `<select class="te-dropdown te-inline-dd" data-q="${qIndex}" data-gap="${gap}" data-correct="${p.correct}" aria-label="Choose an option">
        <option value="">—</option>
        ${opts}
      </select>`;
      gap += 1;
    });
    html += `</p>`;
    return html;
  }

  function decorateControl(el, ok, correctText) {
    if (!el) return;
    el.classList.remove("te-select-correct", "te-select-wrong", "te-no-answer");
    const empty =
      (el.tagName === "SELECT" && el.value === "") ||
      (el.tagName === "INPUT" && !String(el.value || "").trim());

    if (empty && !ok) {
      if (el.tagName === "INPUT") {
        el.value = "[no answer]";
        el.classList.add("te-no-answer");
      }
      el.classList.add("te-select-wrong");
    } else {
      el.classList.toggle("te-select-correct", ok);
      el.classList.toggle("te-select-wrong", !ok);
    }

    el.disabled = true;

    let mark = el.nextElementSibling;
    while (mark && (mark.classList.contains("te-type-reveal") || mark.classList.contains("te-answer-mark"))) {
      const next = mark.nextElementSibling;
      mark.remove();
      mark = next;
    }

    mark = document.createElement("span");
    mark.className = `te-answer-mark ${ok ? "te-mark-ok" : "te-mark-bad"}`;
    mark.setAttribute("aria-hidden", "true");
    mark.textContent = ok ? "✓" : "✕";
    el.insertAdjacentElement("afterend", mark);

    if (!ok && correctText) {
      const hint = document.createElement("span");
      hint.className = "te-type-reveal";
      hint.textContent = " → " + correctText;
      mark.insertAdjacentElement("afterend", hint);
    }
  }

  function clearDecorations(root) {
    root.querySelectorAll(".te-answer-mark, .te-type-reveal, .te-q-feedback").forEach((n) => n.remove());
    root.querySelectorAll(".te-select-correct, .te-select-wrong, .te-no-answer").forEach((el) => {
      el.classList.remove("te-select-correct", "te-select-wrong", "te-no-answer");
      if (el.tagName === "INPUT" && el.value === "[no answer]") el.value = "";
      if (!el.classList.contains("te-type-example") && !el.closest(".te-type-example")) {
        el.disabled = false;
      }
    });
  }

  function formatTipsHtml(tips) {
    if (!tips) return "";
    const list = Array.isArray(tips)
      ? tips
      : String(tips)
          .split(/\n+/)
          .map((s) => s.trim())
          .filter(Boolean);
    if (!list.length) return "";
    return `<ul>${list
      .map((t) => `<li>${String(t).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")}</li>`)
      .join("")}</ul>`;
  }

  function appendQuestionFeedback(container, correctLabel, tips) {
    if (!container) return;
    container.querySelectorAll(".te-q-feedback").forEach((n) => n.remove());
    if (!correctLabel && !tips) return;
    const box = document.createElement("div");
    box.className = "te-q-feedback";
    const label = correctLabel
      ? `<p class="te-q-feedback-correct">Correct answer${String(correctLabel).includes("/") || String(correctLabel).includes(" / ") ? "s" : ""}: ${escapeHtml(correctLabel)}</p>`
      : "";
    box.innerHTML = label + formatTipsHtml(tips);
    container.appendChild(box);
  }

  function checkInlineDropdown(container) {
    const selects = container.querySelectorAll("select.te-inline-dd");
    if (!selects.length) return { ok: false, correctLabel: "" };
    let allOk = true;
    const correctParts = [];
    selects.forEach((sel) => {
      const expected = Number(sel.getAttribute("data-correct"));
      const got = sel.value === "" ? NaN : Number(sel.value);
      const ok = got === expected;
      if (!ok) allOk = false;
      const opt = sel.querySelector(`option[value="${expected}"]`);
      const correctText = opt ? opt.textContent.trim() : "";
      if (correctText) correctParts.push(correctText);
      decorateControl(sel, ok, ok ? "" : correctText);
    });
    return { ok: allOk, correctLabel: correctParts.join(" / ") };
  }

  function lockInlineDropdown(container, locked) {
    container.querySelectorAll("select.te-inline-dd").forEach((sel) => {
      sel.disabled = locked;
    });
  }

  function normalizeAnswer(s) {
    return String(s || "")
      .trim()
      .replace(/[’‘`]/g, "'")
      .replace(/\s+/g, " ")
      .toLowerCase();
  }

  /**
   * type_gap: rewrite / fill blank by typing.
   * q: { source, before, after, answers: ["She's", ...], example?: bool }
   */
  function renderTypeGap(q, qIndex) {
    const source = escapeHtml(q.source || "");
    const before = escapeHtml(q.before || "");
    const after = escapeHtml(q.after || "");
    const isExample = !!q.example;
    const prefill = isExample && Array.isArray(q.answers) && q.answers[0] ? escapeAttr(q.answers[0]) : "";
    const disabled = isExample ? "disabled" : "";
    const exampleClass = isExample ? " te-type-example" : "";
    const label = isExample
      ? `<span class="te-example-label">EXAMPLE:</span> `
      : "";

    return `
      <div class="te-type-gap${exampleClass}" data-type-gap="${qIndex}">
        <p class="te-q-sentence te-type-source">${label}${source} <span class="te-type-arrow" aria-hidden="true">⇒</span></p>
        <p class="te-q-sentence te-type-target">
          ${before}<input type="text" class="te-type-input" data-type-input autocomplete="off" spellcheck="false"
            value="${prefill}" ${disabled} aria-label="Type the short form" />${after}
        </p>
      </div>`;
  }

  function checkTypeGap(container, answers) {
    const input = container.querySelector("input.te-type-input");
    if (!input) return { ok: false, correctLabel: "" };
    if (input.disabled && input.closest(".te-type-example")) {
      return { ok: true, correctLabel: (answers && answers[0]) || "" };
    }
    const raw = String(input.value || "").trim();
    const got = normalizeAnswer(raw === "[no answer]" ? "" : raw);
    const ok = got !== "" && (answers || []).some((a) => normalizeAnswer(a) === got);
    const correctLabel = (answers && answers[0]) || "";
    decorateControl(input, ok, ok ? "" : correctLabel);
    return { ok, correctLabel };
  }

  function lockTypeGap(container, locked) {
    container.querySelectorAll("input.te-type-input:not([disabled])").forEach((inp) => {
      if (locked) inp.disabled = true;
    });
  }

  /** multiple_choice: 4 vertical options A–D */
  function renderMultipleChoice(q, qIndex) {
    const options = Array.isArray(q.options) ? q.options : [];
    let html = `<p class="te-q-sentence">${escapeHtml(q.prompt || q.text || "")}</p>`;
    html += `<div class="te-options-stack" data-stack-for="${qIndex}" data-mcq="1">`;
    options.forEach((opt, oi) => {
      html += `
        <label class="te-option-row">
          <input type="radio" class="sr-only" name="q${qIndex}" value="${oi}" data-lettered-choice data-mcq-choice />
          <span class="te-option-letter">${LETTERS[oi]}.</span>
          <span class="te-option-text">${escapeHtml(opt)}</span>
        </label>`;
    });
    html += `</div>`;
    return html;
  }

  function checkMultipleChoice(stackEl, correctIndex) {
    return checkLetteredStack(stackEl, Number(correctIndex));
  }

  /** Pink highlight when student picks an option (before Check) */
  function initLetteredStacks(rootEl, onChange) {
    rootEl.querySelectorAll(".te-options-stack").forEach((stack) => {
      stack.querySelectorAll("input[data-lettered-choice]").forEach((inp) => {
        inp.addEventListener("change", () => {
          stack.querySelectorAll(".te-option-row").forEach((row) => row.classList.remove("te-selected"));
          const row = inp.closest(".te-option-row");
          if (row) row.classList.add("te-selected");
          if (typeof onChange === "function") onChange();
        });
      });
    });
  }

  function lockLettered(rootEl, locked) {
    rootEl.querySelectorAll("input[data-lettered-choice]").forEach((inp) => {
      inp.disabled = locked;
      const row = inp.closest(".te-option-row");
      if (row && inp.checked) row.classList.add("te-selected");
    });
  }

  function renderDualTypeGap(q, qIndex) {
    const source = escapeHtml(q.source || "");
    const isExample = !!q.example;
    const negPre = isExample && q.neg_answers?.[0] ? escapeAttr(q.neg_answers[0]) : "";
    const qPre = isExample && q.q_answers?.[0] ? escapeAttr(q.q_answers[0]) : "";
    const disabled = isExample ? "disabled" : "";
    const label = isExample ? `<span class="te-example-label">EXAMPLE:</span> ` : "";

    return `
      <div class="te-dual-gap${isExample ? " te-type-example" : ""}" data-dual-gap="${qIndex}">
        <p class="te-q-sentence te-type-source">${label}${source}</p>
        <p class="te-q-sentence te-type-target">
          <span class="te-type-arrow">⇒</span>
          <input type="text" class="te-type-input" data-dual="neg" autocomplete="off" spellcheck="false"
            value="${negPre}" ${disabled} aria-label="Negative form" />
          ${escapeHtml(q.neg_after || "")}
        </p>
        <p class="te-q-sentence te-type-target">
          <span class="te-type-arrow">⇒</span>
          <input type="text" class="te-type-input" data-dual="q" autocomplete="off" spellcheck="false"
            value="${qPre}" ${disabled} aria-label="Question form" />
          ${escapeHtml(q.q_after || "")}
        </p>
      </div>`;
  }

  function checkDualTypeGap(container, q) {
    const neg = container.querySelector('input[data-dual="neg"]');
    const ques = container.querySelector('input[data-dual="q"]');
    if (!neg || !ques) return { ok: false, correctLabel: "" };
    if (neg.disabled && ques.disabled && container.querySelector(".te-type-example")) {
      return {
        ok: true,
        correctLabel: `${(q.neg_answers || [])[0] || ""} / ${(q.q_answers || [])[0] || ""}`,
      };
    }

    const negRaw = String(neg.value || "").trim();
    const qRaw = String(ques.value || "").trim();
    const negGot = normalizeAnswer(negRaw === "[no answer]" ? "" : negRaw);
    const qGot = normalizeAnswer(qRaw === "[no answer]" ? "" : qRaw);
    const negOk = negGot !== "" && (q.neg_answers || []).some((a) => normalizeAnswer(a) === negGot);
    const qOk = qGot !== "" && (q.q_answers || []).some((a) => normalizeAnswer(a) === qGot);
    const negLabel = (q.neg_answers || [])[0] || "";
    const qLabel = (q.q_answers || [])[0] || "";
    decorateControl(neg, negOk, negOk ? "" : negLabel);
    decorateControl(ques, qOk, qOk ? "" : qLabel);
    return {
      ok: negOk && qOk,
      correctLabel: `${negLabel} / ${qLabel}`.replace(/^ \/ | \/ $/g, ""),
    };
  }

  /**
   * dialogue_gap: one block with numbered typed gaps.
   * q: { script: [{speaker, html}], gaps: [{answers:[...]}, ...] }
   * html uses {{1}} {{2}} placeholders (1-based).
   */
  function renderDialogueGap(q) {
    const script = Array.isArray(q.script) ? q.script : [];
    let html = `<div class="te-dialogue" data-dialogue="1">`;
    script.forEach((line) => {
      const parts = String(line.html || "").split(/(\{\{\d+\}\})/g);
      const lineHtml = parts
        .map((part) => {
          const m = part.match(/^\{\{(\d+)\}\}$/);
          if (!m) return escapeHtml(part);
          const n = Number(m[1]);
          return `<span class="te-dialogue-gap"><span class="te-dialogue-num">${n}</span><input type="text" class="te-type-input te-dialogue-input" data-gap="${n}" autocomplete="off" spellcheck="false" aria-label="Gap ${n}" /></span>`;
        })
        .join("");
      html += `<p class="te-dialogue-line"><strong class="te-dialogue-speaker">${escapeHtml(line.speaker || "")}:</strong> ${lineHtml}</p>`;
    });
    html += `</div>`;
    return html;
  }

  function checkDialogueGap(container, gaps) {
    let score = 0;
    const total = (gaps || []).length;
    const wrong = [];
    (gaps || []).forEach((g, i) => {
      const n = i + 1;
      const input = container.querySelector(`input.te-dialogue-input[data-gap="${n}"]`);
      if (!input) return;
      const raw = String(input.value || "").trim();
      const got = normalizeAnswer(raw === "[no answer]" ? "" : raw);
      const ok = got !== "" && (g.answers || []).some((a) => normalizeAnswer(a) === got);
      const correctLabel = (g.answers && g.answers[0]) || "";
      decorateControl(input, ok, ok ? "" : correctLabel);
      if (ok) score++;
      else wrong.push({ n, correctLabel });
    });
    return { score, total, wrong };
  }

  function escapeHtml(text) {
    return String(text)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function escapeAttr(text) {
    return escapeHtml(text).replace(/'/g, "&#39;");
  }

  return {
    parseInlineText,
    parseLetteredGap,
    parseDropdownText,
    renderLettered,
    renderLetteredGap,
    renderDropdown,
    renderInlineDropdown,
    renderTypeGap,
    renderDualTypeGap,
    renderDialogueGap,
    renderMultipleChoice,
    checkLetteredStack,
    checkMultipleChoice,
    checkDropdown,
    checkInlineDropdown,
    checkTypeGap,
    checkDualTypeGap,
    checkDialogueGap,
    decorateControl,
    clearDecorations,
    appendQuestionFeedback,
    lockInlineDropdown,
    lockTypeGap,
    wireDropdownUseOnce,
    initLetteredStacks,
    lockLettered,
    escapeHtml,
  };
})();
