/*
  Lesson page — test-english.com flow:
  One exercise block at a time → Check → score → Next exercise.
*/

document.addEventListener("DOMContentLoaded", async () => {
  const EE = window.ExerciseEngine;
  const site = window.SITE;

  if (site) document.querySelectorAll("[data-brand]").forEach((el) => (el.textContent = site.brand));
  document.getElementById("year").textContent = new Date().getFullYear();

  const lessonId = new URLSearchParams(location.search).get("id");
  const statusEl = document.getElementById("status");

  let lesson = null;
  let sets = [];
  let currentSet = 0;
  /** @type {Set<number>} */
  const completedSets = new Set();
  /** @type {Map<number, { score: number, total: number, pct: number, answers: Array<object> }>} */
  const setSnapshots = new Map();

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
    const html =
      `<span class="font-semibold text-gray-700">Exercises:</span>` +
      sets
        .map((_, i) => {
          const locked = i > maxUnlockedSet();
          const done = completedSets.has(i);
          return `<button type="button" data-set="${i}" class="te-ex-num ${i === currentSet ? "te-ex-num-active" : ""} ${done ? "te-ex-num-done" : ""} ${locked ? "te-ex-num-locked" : ""}" ${locked ? "disabled" : ""}>${i + 1}</button>`;
        })
        .join("");
    document.getElementById("exercise-nav").innerHTML = html;
    document.getElementById("exercise-nav-bottom").innerHTML = html;

    document.querySelectorAll("[data-set]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const idx = Number(btn.dataset.set);
        if (idx <= maxUnlockedSet()) showExerciseSet(idx, false);
      });
    });
  }

  function showExerciseSet(index, resetChecked = true) {
    if (index > maxUnlockedSet()) return;

    currentSet = index;
    renderExerciseNav();

    document.getElementById("score-box").classList.add("hidden");
    document.getElementById("next-btn").classList.add("hidden");
    document.getElementById("next-btn").textContent = "Continue to next exercise →";
    document.getElementById("check-btn").classList.remove("hidden");
    document.getElementById("check-btn").disabled = false;

    const set = sets[index];
    document.getElementById("exercise-title").textContent = set.title || `Exercise ${index + 1}`;
    document.getElementById("exercise-instructions").textContent =
      set.instructions || "Complete the exercise below.";

    const questions = Array.isArray(set.questions) ? set.questions : [];
    const list = document.getElementById("questions-list");

    list.innerHTML = questions
      .map((q, qi) => {
        const qKey = `${index}-${qi}`;
        let body = "";
        if (set.type === "inline_choice") {
          body = EE.renderLettered(EE.parseInlineText(q.text || ""), qKey);
        } else if (set.type === "lettered_gap") {
          body = EE.renderLetteredGap(EE.parseLetteredGap(q.text || ""), qKey);
        } else if (set.type === "dropdown_gap") {
          const parsed = EE.parseDropdownText(q.text || "");
          const bank = Array.isArray(set.word_bank) ? set.word_bank : [];
          body = EE.renderDropdown(parsed.sentence, qKey, bank);
        }
        return `
          <li class="te-question-item" data-qi="${qi}">
            <span class="te-q-num">${qi + 1}</span>
            <div class="te-question-body" data-q-key="${qKey}" data-q-text="${escapeAttr(q.text || "")}">${body}</div>
          </li>`;
      })
      .join("");

    if (set.type === "dropdown_gap" && set.use_once) {
      EE.wireDropdownUseOnce(list);
    }
    EE.initLetteredStacks(list);

    if (!resetChecked && completedSets.has(index) && setSnapshots.has(index)) {
      restoreSnapshot(index);
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
      } else if (ans.kind === "dropdown") {
        body.querySelectorAll("select.te-dropdown").forEach((sel, i) => {
          if (ans.values[i]) sel.value = ans.values[i];
        });
      }
    });

    checkCurrentSet(true, true);
  }

  function onNextClick() {
    if (currentSet < sets.length - 1) {
      goNextExercise();
    } else {
      document.querySelector('[data-tab="explanation"]')?.click();
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }

  function checkCurrentSet(silent, fromSnapshot = false) {
    const set = sets[currentSet];
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
    if (currentSet < sets.length - 1) {
      nextBtn.classList.remove("hidden");
      nextBtn.textContent =
        pct >= 0.5 ? "Continue to next exercise →" : "Continue anyway →";
    } else {
      nextBtn.classList.remove("hidden");
      nextBtn.textContent = "Lesson complete ✓";
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
