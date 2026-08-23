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
  if (
    window.EnglishPathCatalog &&
    typeof window.EnglishPathCatalog.isListedOnSection === "function" &&
    !window.EnglishPathCatalog.isListedOnSection(lessonData, lessonData.level)
  ) {
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
  await setupDownloads(lesson);

  if (!sets.length) {
    document.getElementById("questions-list").innerHTML =
      '<p class="text-sm text-gray-500">Exercises coming soon.</p>';
    document.getElementById("check-btn").classList.add("hidden");
    return;
  }

  document.getElementById("check-btn").addEventListener("click", () => checkCurrentSet(false));
  document.getElementById("next-btn").addEventListener("click", onNextClick);
  document.getElementById("try-again-btn").addEventListener("click", onTryAgain);

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

  async function fetchIsPremium() {
    if (!window.sb || !window.SUPABASE_READY) return false;
    const { data: sessionData } = await window.sb.auth.getSession();
    const user = sessionData?.session?.user;
    if (!user) return false;
    const { data: profile } = await window.sb
      .from("profiles")
      .select("is_premium")
      .eq("id", user.id)
      .maybeSingle();
    return !!profile?.is_premium;
  }

  function showPdfDownload(lesson) {
    const link = document.getElementById("pdf-link");
    const ph = document.getElementById("pdf-placeholder");
    const content = document.getElementById("downloads-content");
    content.classList.remove("hidden");
    if (lesson.pdf_url) {
      link.href = lesson.pdf_url;
      link.textContent = lesson.pdf_url.endsWith(".html")
        ? "Open printable worksheet"
        : "Download PDF";
      link.classList.remove("hidden");
      ph.classList.add("hidden");
    } else {
      link.classList.add("hidden");
      ph.classList.remove("hidden");
    }
  }

  async function setupDownloads(lesson) {
    const paywall = document.getElementById("downloads-paywall");
    const content = document.getElementById("downloads-content");
    const btnPlans = document.getElementById("btn-check-plans");
    const isA1 = lesson.level === "a1";

    if (!isA1) {
      paywall?.classList.add("hidden");
      content?.classList.remove("hidden");
      showPdfDownload(lesson);
      return;
    }

    const isPremium = await fetchIsPremium();

    if (isPremium) {
      paywall?.classList.add("hidden");
      content?.classList.remove("hidden");
      showPdfDownload(lesson);
      return;
    }

    paywall?.classList.remove("hidden");
    content?.classList.add("hidden");

    if (btnPlans && !btnPlans.dataset.wired) {
      btnPlans.dataset.wired = "1";
      btnPlans.addEventListener("click", async () => {
        btnPlans.disabled = true;
        const old = btnPlans.textContent;
        btnPlans.textContent = "Please wait…";
        try {
          if (window.EnglishPathBilling?.startCheckout) {
            const returnTo =
              window.location.pathname.replace(/^\//, "") +
              window.location.search +
              (window.location.hash || "");
            await window.EnglishPathBilling.startCheckout({ next: returnTo || "account.html" });
          } else {
            window.location.href = "index.html#pricing";
          }
        } catch (err) {
          alert(err.message || "Could not start checkout");
          btnPlans.disabled = false;
          btnPlans.textContent = old;
        }
      });
    }
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
            const done = completedSets.has(i);
            return `<button type="button" data-set="${i}" class="te-ex-num ${i === currentSet ? "te-ex-num-active" : ""} ${done ? "te-ex-num-done" : ""}">${i + 1}</button>`;
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
        if (idx === currentSet) return;
        persistCurrentDraft();
        showExerciseSet(idx, false);
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

  function persistCurrentDraft() {
    const set = sets[currentSet];
    if (!set || isMcqSet(set)) return;
    if (completedSets.has(currentSet)) return;
    captureSnapshot(set, null, null, null);
  }

  function questionTips(q) {
    if (Array.isArray(q.tips) && q.tips.length) return q.tips;
    if (!q.feedback) return [];
    return String(q.feedback)
      .split(/\n+/)
      .map((s) => s.trim())
      .filter(Boolean);
  }

  function showScoreSummary(score, total) {
    const pct = total ? Math.round((score / total) * 100) : 0;
    const box = document.getElementById("score-box");
    box.classList.remove("hidden");
    const tone = pct === 100 ? "te-score-good" : pct >= 50 ? "te-score-ok" : "te-score-low";
    box.className = `te-score-box ${tone}`;
    box.innerHTML = `
      <p class="te-score-title">🚀 Test completed!</p>
      <p>Correct answers: <strong>${score}/${total}</strong>.</p>
      <p>Your score is <strong>${pct}%</strong>.</p>
      <p class="te-score-hint">Check your answers below:</p>`;
    return pct / 100;
  }

  function setCheckUi(checked) {
    const checkBtn = document.getElementById("check-btn");
    const tryBtn = document.getElementById("try-again-btn");
    const nextBtn = document.getElementById("next-btn");
    checkBtn.classList.toggle("hidden", checked);
    checkBtn.disabled = false;
    tryBtn.classList.toggle("hidden", !checked);
    if (checked) {
      nextBtn.classList.remove("hidden");
      nextBtn.textContent =
        currentSet >= sets.length - 1 ? "Go to Explanation →" : "Continue to next exercise →";
    } else {
      nextBtn.classList.add("hidden");
    }
  }

  function onTryAgain() {
    const set = sets[currentSet];
    completedSets.delete(currentSet);
    const snap = setSnapshots.get(currentSet);
    if (snap) {
      snap.checked = false;
      snap.score = null;
      snap.pct = null;
    }
    document.getElementById("score-box").classList.add("hidden");
    const list = document.getElementById("questions-list");
    EE.clearDecorations(list);
    // restore draft answers without [no answer]
    if (snap) {
      restoreAnswersOnly(currentSet);
    }
    setCheckUi(false);
    renderExerciseNav();
  }

  function showExerciseSet(index, resetChecked = true) {
    currentSet = index;
    currentPage = 0;
    const set = sets[index];
    const checked = completedSets.has(index);

    if (useMcqPagination(set)) {
      const n = Array.isArray(set.questions) ? set.questions.length : 0;
      if (resetChecked || mcqAnswers.length !== n) {
        mcqAnswers = Array(n).fill(null);
        mcqChecked = false;
      }
      document.getElementById("exercise-title").textContent = set.title || "Exercises";
      document.getElementById("exercise-instructions").textContent =
        set.instructions || "Choose the best answer for each question.";
      if (!mcqChecked) document.getElementById("score-box").classList.add("hidden");
      setCheckUi(mcqChecked);
      renderMcqPage();
      return;
    }

    if (isMcqSet(set)) {
      document.getElementById("progress-wrap").classList.remove("hidden");
      const n = Array.isArray(set.questions) ? set.questions.length : 0;
      if (resetChecked || !completedSets.has(index)) {
        if (!setSnapshots.has(index)) {
          mcqAnswers = Array(n).fill(null);
          mcqChecked = false;
        }
      }
    } else {
      document.getElementById("progress-wrap").classList.add("hidden");
    }

    if (isMcqSet(set) && !useMcqPagination(set)) {
      document.getElementById("exercise-title").textContent = set.title || `Exercise ${index + 1}`;
      document.getElementById("exercise-instructions").textContent =
        set.instructions || "Choose the best answer for each question.";
      if (!checked) document.getElementById("score-box").classList.add("hidden");
      setCheckUi(checked);

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

      if (checked) {
        questions.forEach((q, qi) => {
          const body = document.querySelector(`.te-question-body[data-q-key="mcq-set${index}-${qi}"]`);
          const stack = body?.querySelector(".te-options-stack");
          if (stack) EE.checkMultipleChoice(stack, q.correct);
          if (body && mcqAnswers[qi] !== Number(q.correct)) {
            const label = Array.isArray(q.options) ? q.options[q.correct] : "";
            EE.appendQuestionFeedback(body, label, questionTips(q));
          }
        });
        EE.lockLettered(list, true);
        const snap = setSnapshots.get(index);
        if (snap && snap.total != null) showScoreSummary(snap.score, snap.total);
      }

      renderExerciseNav();
      return;
    }

    if (!checked) document.getElementById("score-box").classList.add("hidden");
    setCheckUi(checked);

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
        } else if (set.type === "dual_type_gap") {
          body = EE.renderDualTypeGap(q, qKey);
        } else if (set.type === "dialogue_gap") {
          body = EE.renderDialogueGap(q);
        } else if (set.type === "lettered_gap") {
          body = EE.renderLetteredGap(EE.parseLetteredGap(q.text || ""), qKey);
        } else if (set.type === "dropdown_gap") {
          const parsed = EE.parseDropdownText(q.text || "");
          const bank = Array.isArray(set.word_bank) ? set.word_bank : [];
          body = EE.renderDropdown(parsed.sentence, qKey, bank);
        }
        const hideNum = set.type === "dialogue_gap";
        const numLabel = hideNum ? "" : q.example ? "Ex" : String(displayNum++);
        return `
          <li class="te-question-item${q.example ? " te-example-item" : ""}${hideNum ? " te-dialogue-item" : ""}" data-qi="${qi}">
            ${hideNum ? "" : `<span class="te-q-num">${numLabel}</span>`}
            <div class="te-question-body" data-q-key="${qKey}" data-q-text="${escapeAttr(q.text || q.source || "")}">${body}</div>
          </li>`;
      })
      .join("");

    if (set.type === "dropdown_gap" && set.use_once) {
      EE.wireDropdownUseOnce(list);
    }
    EE.initLetteredStacks(list);
    renderExerciseNav();

    if (setSnapshots.has(index)) {
      restoreAnswersOnly(index);
      if (checked) {
        checkCurrentSet(true, true);
      }
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
        return { kind: "inline_dd", values: inlineDd.map((s) => (s.value === "" ? "" : s.value)) };
      }
      const dualNeg = body.querySelector('input[data-dual="neg"]');
      const dualQ = body.querySelector('input[data-dual="q"]');
      if (dualNeg && dualQ) {
        const clean = (v) => (v === "[no answer]" ? "" : v);
        return { kind: "dual_type", neg: clean(dualNeg.value), q: clean(dualQ.value) };
      }
      const dialogueInputs = [...body.querySelectorAll("input.te-dialogue-input")];
      if (dialogueInputs.length) {
        return {
          kind: "dialogue_gap",
          values: dialogueInputs.map((inp) => ({
            gap: inp.dataset.gap,
            value: inp.value === "[no answer]" ? "" : inp.value,
          })),
        };
      }
      const typeInp = body.querySelector("input.te-type-input");
      if (typeInp) {
        return {
          kind: "type_gap",
          value: typeInp.value === "[no answer]" ? "" : typeInp.value,
        };
      }
      const selects = [...body.querySelectorAll("select.te-dropdown")];
      return { kind: "dropdown", values: selects.map((s) => s.value) };
    });
    const prev = setSnapshots.get(currentSet) || {};
    setSnapshots.set(currentSet, {
      ...prev,
      score,
      total,
      pct,
      answers,
      checked: score != null && total != null,
    });
  }

  function restoreAnswersOnly(index) {
    const snap = setSnapshots.get(index);
    if (!snap || !Array.isArray(snap.answers)) return;

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
          if (ans.values[i] !== undefined) sel.value = ans.values[i];
        });
      } else if (ans.kind === "dual_type") {
        const neg = body.querySelector('input[data-dual="neg"]');
        const ques = body.querySelector('input[data-dual="q"]');
        if (neg) neg.value = ans.neg || "";
        if (ques) ques.value = ans.q || "";
      } else if (ans.kind === "dialogue_gap" && Array.isArray(ans.values)) {
        ans.values.forEach((v) => {
          const inp = body.querySelector(`input.te-dialogue-input[data-gap="${v.gap}"]`);
          if (inp) inp.value = v.value || "";
        });
      } else if (ans.kind === "type_gap" && ans.value != null) {
        const inp = body.querySelector("input.te-type-input");
        if (inp && !inp.closest(".te-type-example")) inp.value = ans.value;
      } else if (ans.kind === "dropdown") {
        body.querySelectorAll("select.te-dropdown").forEach((sel, i) => {
          if (ans.values[i]) sel.value = ans.values[i];
        });
      }
    });
  }

  function restoreSnapshot(index) {
    restoreAnswersOnly(index);
    checkCurrentSet(true, true);
  }

  function onNextClick() {
    const set = sets[currentSet];
    if (useMcqPagination(set) || currentSet >= sets.length - 1) {
      document.querySelector('[data-tab="explanation"]')?.click();
      window.scrollTo({ top: 0, behavior: "smooth" });
      return;
    }
    persistCurrentDraft();
    goNextExercise();
  }

  function checkCurrentSet(silent, fromSnapshot = false) {
    const set = sets[currentSet];

    if (isMcqSet(set)) {
      const questions = Array.isArray(set.questions) ? set.questions : [];
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
      showScoreSummary(score, total);
      setSnapshots.set(currentSet, { score, total, pct: total ? score / total : 0, answers: mcqAnswers.slice(), checked: true });
      setCheckUi(true);

      if (useMcqPagination(set)) {
        renderMcqPage();
      } else {
        questions.forEach((q, qi) => {
          const body = document.querySelector(
            `.te-question-body[data-q-key="mcq-set${currentSet}-${qi}"]`
          );
          const stack = body?.querySelector(".te-options-stack");
          if (stack) EE.checkMultipleChoice(stack, q.correct);
          if (body && mcqAnswers[qi] !== Number(q.correct)) {
            const label = Array.isArray(q.options) ? q.options[q.correct] : "";
            EE.appendQuestionFeedback(body, label, questionTips(q));
          }
        });
        EE.lockLettered(document.getElementById("questions-list"), true);
        renderExerciseNav();
      }
      if (!silent) saveProgress(lesson.id, score, total);
      return;
    }

    const questions = Array.isArray(set.questions) ? set.questions : [];
    let score = 0;
    let totalOverride = null;
    const usedBank = new Set();

    if (set.type === "dialogue_gap") {
      const q = questions[0] || {};
      const body = document.querySelector(`.te-question-body[data-q-key="${currentSet}-0"]`);
      if (body) {
        body.querySelectorAll(".te-q-feedback").forEach((n) => n.remove());
        const result = EE.checkDialogueGap(body, q.gaps || []);
        score = result.score;
        totalOverride = result.total;
        if (result.wrong && result.wrong.length) {
          const tips = result.wrong.map((w) => `Gap ${w.n}: **${w.correctLabel}**`);
          EE.appendQuestionFeedback(body, result.wrong.map((w) => w.correctLabel).join(", "), tips);
        }
      }
    } else {
      questions.forEach((q, qi) => {
        const body = document.querySelector(`.te-question-body[data-q-key="${currentSet}-${qi}"]`);
        if (!body) return;

        let ok = false;
        let correctLabel = q.correct_label || "";
        const stack = body.querySelector(".te-options-stack");
        body.querySelectorAll(".te-q-feedback").forEach((n) => n.remove());

        if (set.type === "inline_choice") {
          const parts = EE.parseInlineText(q.text || "");
          const choice = parts.find((p) => p.type === "choice");
          if (stack && choice) {
            ok = EE.checkLetteredStack(stack, choice.correct);
            correctLabel = choice.options[choice.correct] || correctLabel;
          }
        } else if (set.type === "inline_dropdown") {
          const result = EE.checkInlineDropdown(body);
          ok = !!result.ok;
          correctLabel = result.correctLabel || correctLabel;
        } else if (set.type === "type_gap") {
          const result = EE.checkTypeGap(body, q.answers || []);
          ok = !!result.ok;
          correctLabel = result.correctLabel || correctLabel;
          if (q.example) return;
        } else if (set.type === "dual_type_gap") {
          const result = EE.checkDualTypeGap(body, q);
          ok = !!result.ok;
          correctLabel = result.correctLabel || correctLabel;
          if (q.example) return;
        } else if (set.type === "lettered_gap") {
          const parsed = EE.parseLetteredGap(q.text || "");
          if (stack) {
            ok = EE.checkLetteredStack(stack, parsed.correct);
            correctLabel = parsed.options[parsed.correct] || correctLabel;
          }
        } else if (set.type === "dropdown_gap") {
          const parsed = EE.parseDropdownText(q.text || "");
          ok = EE.checkDropdown(body, parsed.answers, set.use_once, usedBank);
          correctLabel = (parsed.answers || []).join(" / ");
        }

        if (ok) score++;
        else EE.appendQuestionFeedback(body, correctLabel, questionTips(q));
        if (stack) EE.lockLettered(body, true);
      });
    }

    completedSets.add(currentSet);

    const total =
      totalOverride != null
        ? totalOverride
        : set.type === "type_gap" || set.type === "dual_type_gap"
          ? questions.filter((q) => !q.example).length
          : questions.length;
    const pct = showScoreSummary(score, total);
    setCheckUi(true);

    renderExerciseNav();
    if (!fromSnapshot) captureSnapshot(set, score, total, pct);
    else {
      const snap = setSnapshots.get(currentSet);
      if (snap) {
        snap.score = score;
        snap.total = total;
        snap.pct = pct;
        snap.checked = true;
      }
    }
    if (!silent) saveProgress(lesson.id, score, total);
  }

  function goNextExercise() {
    if (currentSet < sets.length - 1) {
      showExerciseSet(currentSet + 1, false);
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
