/*
  Lesson page — test-english.com flow:
  Classic sets: one exercise block at a time → Check → score → Next.
  multiple_choice: one set of N questions, 10 per page, progress bar, Check scores all.
*/

document.addEventListener("DOMContentLoaded", async () => {
  const EE = window.ExerciseEngine;
  const site = window.SITE;
  const PAGE_SIZE = 10;

  if (site) document.querySelectorAll("[data-brand]").forEach((el) => (el.textContent = site.brand));
  document.getElementById("year").textContent = new Date().getFullYear();

  const lessonId = new URLSearchParams(location.search).get("id");
  const statusEl = document.getElementById("status");

  let lesson = null;
  let sets = [];
  let currentSet = 0;
  let currentPage = 0;
  /** @type {Set<number>} */
  const completedSets = new Set();
  /** @type {Map<number, { score: number, total: number, pct: number, answers: Array<object> }>} */
  const setSnapshots = new Map();
  /** Selected MCQ answers by global question index: number | null */
  let mcqAnswers = [];
  let mcqChecked = false;

  const burger = document.getElementById("burger");
  const mobileMenu = document.getElementById("mobile-menu");
  if (burger && mobileMenu) burger.addEventListener("click", () => mobileMenu.classList.toggle("hidden"));

  if (!lessonId || !window.sb || !window.SUPABASE_READY) {
    statusEl.textContent = lessonId ? "Database not connected." : "Lesson not found.";
    return;
  }

  const { data: lessonData, error: le } = await window.sb
    .from("lessons")
    .select("*")
    .eq("id", lessonId)
    .eq("is_published", true)
    .single();

  if (le || !lessonData) {
    document.getElementById("lesson-title").textContent = "Lesson not found";
    statusEl.textContent = "This lesson is not available.";
    return;
  }
  lesson = lessonData;

  const { data: setData } = await window.sb
    .from("exercise_sets")
    .select("*")
    .eq("lesson_id", lessonId)
    .order("sort_order");

  sets = setData || [];
  statusEl.textContent = "";

  setupHeader(lesson, site);
  setupTabs();
  setupExplanation(lesson);
  setupDownloads(lesson);

  if (!sets.length) {
    document.getElementById("questions-list").innerHTML =
      '<p class="text-sm text-gray-500">Exercises coming soon.</p>';
    document.getElementById("check-btn").classList.add("hidden");
    return;
  }

  document.getElementById("check-btn").addEventListener("click", () => checkCurrentSet(false));
  document.getElementById("next-btn").addEventListener("click", onNextClick);

  showExerciseSet(0);

  function isMcqSet(set) {
    return set && set.type === "multiple_choice";
  }

  /** Paginate only when this lesson is a single big MCQ set. */
  function useMcqPagination(set) {
    return isMcqSet(set) && sets.length === 1 && pageCount(set) > 1;
  }

  function pageCount(set) {
    const n = Array.isArray(set.questions) ? set.questions.length : 0;
    return Math.max(1, Math.ceil(n / PAGE_SIZE));
  }

  function setupHeader(lesson, site) {
    const levelInfo = site?.levels.find((l) => l.id === lesson.level);
    const sectionInfo = site?.sections.find((s) => s.id === lesson.section);
    document.title = `${lesson.title} — ${site?.brand || "EnglishPath"}`;
    document.getElementById("lesson-title").textContent = lesson.title;
    document.getElementById("lesson-banner").textContent = [
      levelInfo?.title || lesson.level.toUpperCase(),
      "English",
      sectionInfo?.title || lesson.section,
    ].join(" ");
    const bl = document.getElementById("breadcrumb-level");
    const bs = document.getElementById("breadcrumb-section");
    if (bl && levelInfo) {
      bl.textContent = levelInfo.title;
      bl.href = `level.html?level=${lesson.level}`;
    }
    if (bs && sectionInfo) {
      bs.textContent = sectionInfo.title;
      bs.href = `section.html?level=${lesson.level}&section=${lesson.section}`;
    }
  }

  function setupTabs() {
    document.querySelectorAll(".te-tab").forEach((btn) => {
      btn.addEventListener("click", () => {
        const tab = btn.getAttribute("data-tab");
        document.querySelectorAll(".te-tab").forEach((b) => b.classList.remove("te-tab-active"));
        btn.classList.add("te-tab-active");
        ["exercises", "explanation", "downloads"].forEach((t) => {
          document.getElementById(`panel-${t}`).classList.toggle("hidden", t !== tab);
        });
      });
    });
  }

  function setupExplanation(lesson) {
    document.getElementById("lesson-explanation").innerHTML =
      lesson.explanation || "<p>No explanation yet.</p>";
    const mediaEl = document.getElementById("lesson-media");
    if (lesson.audio_url) {
      mediaEl.innerHTML = renderMedia(lesson.audio_url);
      mediaEl.classList.remove("hidden");
    }
  }

  function setupDownloads(lesson) {
    const link = document.getElementById("pdf-link");
    const ph = document.getElementById("pdf-placeholder");
    if (lesson.pdf_url) {
      link.href = lesson.pdf_url;
      link.textContent = lesson.pdf_url.endsWith(".html") ? "Open printable worksheet" : "Download PDF";
      link.classList.remove("hidden");
      ph.classList.add("hidden");
    }
  }

  function maxUnlockedSet() {
    let max = 0;
    for (let i = 0; i < sets.length; i++) {
      if (i === 0 || completedSets.has(i - 1)) max = i;
      else break;
    }
    return max;
  }

  function renderExerciseNav() {
    const set = sets[currentSet];
    let html = "";

    if (useMcqPagination(set)) {
      const pages = pageCount(set);
      html =
        `<span class="font-semibold text-gray-700">Exercises:</span>` +
        Array.from({ length: pages }, (_, i) => {
          return `<button type="button" data-page="${i}" class="te-ex-num ${i === currentPage ? "te-ex-num-active" : ""} ${mcqChecked ? "te-ex-num-done" : ""}">${i + 1}</button>`;
        }).join("");
    } else {
      html =
        `<span class="font-semibold text-gray-700">Exercises:</span>` +
        sets
          .map((_, i) => {
            const locked = i > maxUnlockedSet();
            const done = completedSets.has(i);
            return `<button type="button" data-set="${i}" class="te-ex-num ${i === currentSet ? "te-ex-num-active" : ""} ${done ? "te-ex-num-done" : ""} ${locked ? "te-ex-num-locked" : ""}" ${locked ? "disabled" : ""}>${i + 1}</button>`;
          })
          .join("");
    }

    document.getElementById("exercise-nav").innerHTML = html;
    document.getElementById("exercise-nav-bottom").innerHTML = html;

    document.querySelectorAll("[data-page]").forEach((btn) => {
      btn.addEventListener("click", () => {
        saveMcqPageAnswers();
        currentPage = Number(btn.dataset.page);
        renderMcqPage();
      });
    });

    document.querySelectorAll("[data-set]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const idx = Number(btn.dataset.set);
        if (idx <= maxUnlockedSet()) showExerciseSet(idx, false);
      });
    });
  }

  function updateProgress() {
    const wrap = document.getElementById("progress-wrap");
    const set = sets[currentSet];
    if (!useMcqPagination(set)) {
      wrap.classList.add("hidden");
      return;
    }
    wrap.classList.remove("hidden");
    const total = Array.isArray(set.questions) ? set.questions.length : 0;
    const answered = mcqAnswers.filter((v) => v != null).length;
    const pct = total ? Math.round((answered / total) * 100) : 0;
    document.getElementById("progress-label").textContent = `${answered} of ${total} answered`;
    document.getElementById("progress-pct").textContent = `${pct}%`;
    document.getElementById("progress-bar").style.width = `${pct}%`;
  }

  function showExerciseSet(index, resetChecked = true) {
    if (!isMcqSet(sets[index]) && index > maxUnlockedSet()) return;

    currentSet = index;
    currentPage = 0;
    const set = sets[index];

    if (useMcqPagination(set)) {
      const n = Array.isArray(set.questions) ? set.questions.length : 0;
      if (resetChecked || mcqAnswers.length !== n) {
        mcqAnswers = Array(n).fill(null);
        mcqChecked = false;
      }
      document.getElementById("exercise-title").textContent = set.title || "Exercises";
      document.getElementById("exercise-instructions").textContent =
        set.instructions || "Choose the best answer for each question.";
      document.getElementById("score-box").classList.add("hidden");
      document.getElementById("next-btn").classList.add("hidden");
      document.getElementById("check-btn").classList.remove("hidden");
      document.getElementById("check-btn").disabled = mcqChecked;
      renderMcqPage();
      return;
    }

    // Classic / multi-set (including MCQ with exactly 10 items, or inline_dropdown)
    if (isMcqSet(set)) {
      document.getElementById("progress-wrap").classList.remove("hidden");
      const n = Array.isArray(set.questions) ? set.questions.length : 0;
      if (resetChecked || !completedSets.has(index)) {
        mcqAnswers = Array(n).fill(null);
        mcqChecked = false;
      }
    } else {
      document.getElementById("progress-wrap").classList.add("hidden");
    }

    if (isMcqSet(set) && !useMcqPagination(set)) {
      // Render all MCQ questions for this set on one page
      document.getElementById("exercise-title").textContent = set.title || `Exercise ${index + 1}`;
      document.getElementById("exercise-instructions").textContent =
        set.instructions || "Choose the best answer for each question.";
      document.getElementById("score-box").classList.add("hidden");
      document.getElementById("next-btn").classList.add("hidden");
      document.getElementById("check-btn").classList.remove("hidden");
      document.getElementById("check-btn").disabled = completedSets.has(index);

      const questions = Array.isArray(set.questions) ? set.questions : [];
      const list = document.getElementById("questions-list");
      list.innerHTML = questions
        .map((q, qi) => {
          const qKey = `mcq-set${index}-${qi}`;
          const body = EE.renderMultipleChoice(q, qKey);
          return `
          <li class="te-question-item" data-qi="${qi}">
            <span class="te-q-num">${qi + 1}</span>
            <div class="te-question-body" data-q-key="${qKey}">${body}</div>
          </li>`;
        })
        .join("");

      questions.forEach((q, qi) => {
        if (mcqAnswers[qi] == null) return;
        const inp = list.querySelector(
          `.te-question-body[data-q-key="mcq-set${index}-${qi}"] input[data-lettered-choice][value="${mcqAnswers[qi]}"]`
        );
        if (inp) {
          inp.checked = true;
          inp.closest(".te-option-row")?.classList.add("te-selected");
        }
      });

      EE.initLetteredStacks(list, () => {
        questions.forEach((_, qi) => {
          const body = document.querySelector(`.te-question-body[data-q-key="mcq-set${index}-${qi}"]`);
          const selected = body?.querySelector("input[data-lettered-choice]:checked");
          mcqAnswers[qi] = selected ? Number(selected.value) : mcqAnswers[qi];
        });
        const answered = mcqAnswers.filter((v) => v != null).length;
        const total = questions.length;
        const pct = total ? Math.round((answered / total) * 100) : 0;
        document.getElementById("progress-wrap").classList.remove("hidden");
        document.getElementById("progress-label").textContent = `${answered} of ${total} answered`;
        document.getElementById("progress-pct").textContent = `${pct}%`;
        document.getElementById("progress-bar").style.width = `${pct}%`;
      });

      if (completedSets.has(index)) {
        questions.forEach((q, qi) => {
          const body = document.querySelector(`.te-question-body[data-q-key="mcq-set${index}-${qi}"]`);
          const stack = body?.querySelector(".te-options-stack");
          if (stack) EE.checkMultipleChoice(stack, q.correct);
        });
        EE.lockLettered(list, true);
      }

      renderExerciseNav();
      return;
    }

    document.getElementById("progress-wrap").classList.add("hidden");
    document.getElementById("score-box").classList.add("hidden");
    document.getElementById("next-btn").classList.add("hidden");
    document.getElementById("next-btn").textContent = "Continue to next exercise →";
    document.getElementById("check-btn").classList.remove("hidden");
    document.getElementById("check-btn").disabled = completedSets.has(index);

    document.getElementById("exercise-title").textContent = set.title || `Exercise ${index + 1}`;
    document.getElementById("exercise-instructions").textContent =
      set.instructions || "Complete the exercise below.";

    const questions = Array.isArray(set.questions) ? set.questions : [];
    const list = document.getElementById("questions-list");
    let displayNum = 1;

    list.innerHTML = questions
      .map((q, qi) => {
        const qKey = `${index}-${qi}`;
        let body = "";
        if (set.type === "inline_choice") {
          body = EE.renderLettered(EE.parseInlineText(q.text || ""), qKey);
        } else if (set.type === "inline_dropdown") {
          body = EE.renderInlineDropdown(EE.parseInlineText(q.text || ""), qKey);
        } else if (set.type === "type_gap") {
          body = EE.renderTypeGap(q, qKey);
        } else if (set.type === "lettered_gap") {
          body = EE.renderLetteredGap(EE.parseLetteredGap(q.text || ""), qKey);
        } else if (set.type === "dropdown_gap") {
          const parsed = EE.parseDropdownText(q.text || "");
          const bank = Array.isArray(set.word_bank) ? set.word_bank : [];
          body = EE.renderDropdown(parsed.sentence, qKey, bank);
        }
        const numLabel = q.example ? "Ex" : String(displayNum++);
        return `
          <li class="te-question-item${q.example ? " te-example-item" : ""}" data-qi="${qi}">
            <span class="te-q-num">${numLabel}</span>
            <div class="te-question-body" data-q-key="${qKey}" data-q-text="${escapeAttr(q.text || q.source || "")}">${body}</div>
          </li>`;
      })
      .join("");

    if (set.type === "dropdown_gap" && set.use_once) {
      EE.wireDropdownUseOnce(list);
    }
    EE.initLetteredStacks(list);
    renderExerciseNav();

    if (!resetChecked && completedSets.has(index) && setSnapshots.has(index)) {
      restoreSnapshot(index);
    }
  }

  function saveMcqPageAnswers() {
    const set = sets[currentSet];
    if (!isMcqSet(set)) return;
    const questions = Array.isArray(set.questions) ? set.questions : [];
    const start = currentPage * PAGE_SIZE;
    const end = Math.min(start + PAGE_SIZE, questions.length);
    for (let qi = start; qi < end; qi++) {
      const body = document.querySelector(`.te-question-body[data-q-key="mcq-${qi}"]`);
      if (!body) continue;
      const selected = body.querySelector("input[data-lettered-choice]:checked");
      mcqAnswers[qi] = selected ? Number(selected.value) : mcqAnswers[qi];
    }
  }

  function renderMcqPage() {
    const set = sets[currentSet];
    const questions = Array.isArray(set.questions) ? set.questions : [];
    const start = currentPage * PAGE_SIZE;
    const end = Math.min(start + PAGE_SIZE, questions.length);
    const list = document.getElementById("questions-list");
    const pageLabel = currentPage + 1;

    document.getElementById("exercise-title").textContent =
      set.title || `Exercise ${pageLabel}`;

    list.innerHTML = questions
      .slice(start, end)
      .map((q, offset) => {
        const qi = start + offset;
        const qKey = `mcq-${qi}`;
        const body = EE.renderMultipleChoice(q, qKey);
        return `
          <li class="te-question-item" data-qi="${qi}">
            <span class="te-q-num">${qi + 1}</span>
            <div class="te-question-body" data-q-key="${qKey}">${body}</div>
          </li>`;
      })
      .join("");

    // Restore selections for this page
    for (let qi = start; qi < end; qi++) {
      if (mcqAnswers[qi] == null) continue;
      const inp = list.querySelector(
        `.te-question-body[data-q-key="mcq-${qi}"] input[data-lettered-choice][value="${mcqAnswers[qi]}"]`
      );
      if (inp) {
        inp.checked = true;
        const row = inp.closest(".te-option-row");
        if (row) row.classList.add("te-selected");
      }
    }

    EE.initLetteredStacks(list, () => {
      saveMcqPageAnswers();
      updateProgress();
    });

    if (mcqChecked) {
      applyMcqResults(start, end, true);
      EE.lockLettered(list, true);
    }

    renderExerciseNav();
    updateProgress();
  }

  function applyMcqResults(start, end, silent) {
    const set = sets[currentSet];
    const questions = Array.isArray(set.questions) ? set.questions : [];
    for (let qi = start; qi < end; qi++) {
      const q = questions[qi];
      const body = document.querySelector(`.te-question-body[data-q-key="mcq-${qi}"]`);
      if (!body || !q) continue;
      const stack = body.querySelector(".te-options-stack");
      if (stack) EE.checkMultipleChoice(stack, q.correct);
    }
  }

  function captureSnapshot(set, score, total, pct) {
    const questions = Array.isArray(set.questions) ? set.questions : [];
    const answers = questions.map((q, qi) => {
      const body = document.querySelector(`.te-question-body[data-q-key="${currentSet}-${qi}"]`);
      if (!body) return null;
      const stack = body.querySelector(".te-options-stack");
      if (stack) {
        const selected = stack.querySelector("input[data-lettered-choice]:checked");
        return { kind: "lettered", value: selected ? Number(selected.value) : null };
      }
      const inlineDd = [...body.querySelectorAll("select.te-inline-dd")];
      if (inlineDd.length) {
        return { kind: "inline_dd", values: inlineDd.map((s) => s.value) };
      }
      const typeInp = body.querySelector("input.te-type-input");
      if (typeInp) {
        return { kind: "type_gap", value: typeInp.value };
      }
      const selects = [...body.querySelectorAll("select.te-dropdown")];
      return { kind: "dropdown", values: selects.map((s) => s.value) };
    });
    setSnapshots.set(currentSet, { score, total, pct, answers });
  }

  function restoreSnapshot(index) {
    const snap = setSnapshots.get(index);
    if (!snap) return;

    snap.answers.forEach((ans, qi) => {
      const body = document.querySelector(`.te-question-body[data-q-key="${index}-${qi}"]`);
      if (!body || !ans) return;

      if (ans.kind === "lettered" && ans.value != null) {
        const inp = body.querySelector(`input[data-lettered-choice][value="${ans.value}"]`);
        if (inp) {
          inp.checked = true;
          inp.dispatchEvent(new Event("change", { bubbles: true }));
        }
      } else if (ans.kind === "inline_dd") {
        body.querySelectorAll("select.te-inline-dd").forEach((sel, i) => {
          if (ans.values[i] !== undefined && ans.values[i] !== "") sel.value = ans.values[i];
        });
      } else if (ans.kind === "type_gap" && ans.value != null) {
        const inp = body.querySelector("input.te-type-input");
        if (inp && !inp.disabled) inp.value = ans.value;
      } else if (ans.kind === "dropdown") {
        body.querySelectorAll("select.te-dropdown").forEach((sel, i) => {
          if (ans.values[i]) sel.value = ans.values[i];
        });
      }
    });

    checkCurrentSet(true, true);
  }

  function onNextClick() {
    const set = sets[currentSet];
    if (useMcqPagination(set) || currentSet >= sets.length - 1) {
      document.querySelector('[data-tab="explanation"]')?.click();
      window.scrollTo({ top: 0, behavior: "smooth" });
      return;
    }
    goNextExercise();
  }

  function checkCurrentSet(silent, fromSnapshot = false) {
    const set = sets[currentSet];

    if (isMcqSet(set)) {
      const questions = Array.isArray(set.questions) ? set.questions : [];
      // Collect answers from DOM (paginated or single-page set)
      if (useMcqPagination(set)) {
        saveMcqPageAnswers();
      } else {
        questions.forEach((_, qi) => {
          const body = document.querySelector(
            `.te-question-body[data-q-key="mcq-set${currentSet}-${qi}"]`
          );
          const selected = body?.querySelector("input[data-lettered-choice]:checked");
          mcqAnswers[qi] = selected ? Number(selected.value) : mcqAnswers[qi];
        });
      }

      let score = 0;
      questions.forEach((q, qi) => {
        if (mcqAnswers[qi] === Number(q.correct)) score++;
      });
      mcqChecked = true;
      completedSets.add(currentSet);

      const total = questions.length;
      const pct = total ? score / total : 0;
      const box = document.getElementById("score-box");
      box.classList.remove("hidden");
      if (pct === 1) {
        box.className = "te-score-box te-score-good";
        box.innerHTML = `<strong>Perfect!</strong> You got ${score} out of ${total} correct.`;
      } else if (pct >= 0.5) {
        box.className = "te-score-box te-score-ok";
        box.innerHTML = `<strong>Good job!</strong> You got ${score} out of ${total} correct.`;
      } else {
        box.className = "te-score-box te-score-low";
        box.innerHTML = `<strong>Keep practising.</strong> You got ${score} out of ${total}. Read the Explanation tab and try again.`;
      }

      document.getElementById("check-btn").disabled = true;
      const nextBtn = document.getElementById("next-btn");
      nextBtn.classList.remove("hidden");
      if (useMcqPagination(set) || currentSet >= sets.length - 1) {
        nextBtn.textContent = "Go to Explanation →";
      } else {
        nextBtn.textContent =
          pct >= 0.5 ? "Continue to next exercise →" : "Continue anyway →";
      }

      if (useMcqPagination(set)) {
        renderMcqPage();
      } else {
        questions.forEach((q, qi) => {
          const body = document.querySelector(
            `.te-question-body[data-q-key="mcq-set${currentSet}-${qi}"]`
          );
          const stack = body?.querySelector(".te-options-stack");
          if (stack) EE.checkMultipleChoice(stack, q.correct);
        });
        EE.lockLettered(document.getElementById("questions-list"), true);
        renderExerciseNav();
      }
      if (!silent) saveProgress(lesson.id, score, total);
      return;
    }

    const questions = Array.isArray(set.questions) ? set.questions : [];
    let score = 0;
    const usedBank = new Set();

    questions.forEach((q, qi) => {
      const body = document.querySelector(`.te-question-body[data-q-key="${currentSet}-${qi}"]`);
      if (!body) return;

      let ok = false;
      const stack = body.querySelector(".te-options-stack");

      if (set.type === "inline_choice") {
        const parts = EE.parseInlineText(q.text || "");
        const choice = parts.find((p) => p.type === "choice");
        if (stack && choice) ok = EE.checkLetteredStack(stack, choice.correct);
      } else if (set.type === "inline_dropdown") {
        ok = EE.checkInlineDropdown(body);
      } else if (set.type === "type_gap") {
        ok = EE.checkTypeGap(body, q.answers || []);
        if (q.example) return;
      } else if (set.type === "lettered_gap") {
        const parsed = EE.parseLetteredGap(q.text || "");
        if (stack) ok = EE.checkLetteredStack(stack, parsed.correct);
      } else if (set.type === "dropdown_gap") {
        const parsed = EE.parseDropdownText(q.text || "");
        ok = EE.checkDropdown(body, parsed.answers, set.use_once, usedBank);
      }

      if (ok) score++;
      if (stack) EE.lockLettered(body, true);
    });

    completedSets.add(currentSet);

    const total =
      set.type === "type_gap"
        ? questions.filter((q) => !q.example).length
        : questions.length;
    const pct = total ? score / total : 0;
    const box = document.getElementById("score-box");
    box.classList.remove("hidden");

    if (pct === 1) {
      box.className = "te-score-box te-score-good";
      box.innerHTML = `<strong>Perfect!</strong> You got ${score} out of ${total} correct.`;
    } else if (pct >= 0.5) {
      box.className = "te-score-box te-score-ok";
      box.innerHTML = `<strong>Good job!</strong> You got ${score} out of ${total} correct.`;
    } else {
      box.className = "te-score-box te-score-low";
      box.innerHTML = `<strong>Keep practising.</strong> You got ${score} out of ${total}. Read the Explanation tab and try again.`;
    }

    document.getElementById("check-btn").disabled = true;

    const nextBtn = document.getElementById("next-btn");
    if (currentSet < sets.length - 1) {
      nextBtn.classList.remove("hidden");
      nextBtn.textContent =
        pct >= 0.5 ? "Continue to next exercise →" : "Continue anyway →";
    } else {
      nextBtn.classList.remove("hidden");
      nextBtn.textContent = "Go to Explanation →";
    }

    renderExerciseNav();
    if (!fromSnapshot) captureSnapshot(set, score, total, pct);
    if (!silent) saveProgress(lesson.id, score, total);
  }

  function goNextExercise() {
    if (currentSet < sets.length - 1) {
      showExerciseSet(currentSet + 1);
      document.getElementById("exercise-card").scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  async function saveProgress(lessonId, score, total) {
    const { data } = await window.sb.auth.getSession();
    if (!data?.session?.user) return;
    await window.sb.from("user_progress").upsert(
      {
        user_id: data.session.user.id,
        lesson_id: lessonId,
        score,
        total,
        completed_at: new Date().toISOString(),
      },
      { onConflict: "user_id,lesson_id" }
    );
  }

  function escapeAttr(s) {
    return String(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;");
  }

  function renderMedia(url) {
    try {
      const u = new URL(url);
      if (u.hostname.includes("youtu.be") || u.hostname.includes("youtube.com")) {
        const id = u.hostname.includes("youtu.be")
          ? u.pathname.slice(1)
          : u.searchParams.get("v");
        return `<div class="aspect-video overflow-hidden rounded-xl ring-1 ring-gray-200"><iframe class="h-full w-full" src="https://www.youtube.com/embed/${id}" allowfullscreen loading="lazy"></iframe></div>`;
      }
    } catch (_) {}
    return `<a href="${url}" target="_blank" rel="noopener" class="text-brand hover:underline">Open media</a>`;
  }
});
