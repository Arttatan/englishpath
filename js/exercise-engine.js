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

  /** Pink highlight when student picks an option (before Check) */
  function initLetteredStacks(rootEl) {
    rootEl.querySelectorAll(".te-options-stack").forEach((stack) => {
      stack.querySelectorAll("input[data-lettered-choice]").forEach((inp) => {
        inp.addEventListener("change", () => {
          stack.querySelectorAll(".te-option-row").forEach((row) => row.classList.remove("te-selected"));
          const row = inp.closest(".te-option-row");
          if (row) row.classList.add("te-selected");
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
    checkLetteredStack,
    checkDropdown,
    wireDropdownUseOnce,
    initLetteredStacks,
    lockLettered,
    escapeHtml,
  };
})();
