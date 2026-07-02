/*
  Admin panel — test-english.com style lesson builder.
  Exercise sets: Grammar (inline_choice) | Vocabulary (dropdown_gap).
*/

(function () {
  let quill = null;
  let editingId = null;
  /** @type {Array<object>} */
  let exerciseSets = [];

  const gate = document.getElementById("gate");
  const app = document.getElementById("app");
  const lessonForm = document.getElementById("lesson-form");
  const setsContainer = document.getElementById("sets-container");
  const editorPanel = document.getElementById("editor-panel");
  const editorEmpty = document.getElementById("editor-empty");

  document.addEventListener("DOMContentLoaded", init);

  async function init() {
    document.querySelectorAll("[data-brand]").forEach((el) => (el.textContent = window.SITE?.brand || "EnglishPath"));

    if (!window.sb || !window.SUPABASE_READY) {
      document.getElementById("gate-message").textContent = "Configure js/config.js first.";
      return;
    }

    const { data: sessionData } = await window.sb.auth.getSession();
    if (!sessionData?.session) {
      document.getElementById("gate-message").textContent = "Please log in.";
      document.getElementById("gate-login").classList.remove("hidden");
      return;
    }

    const { data: profile } = await window.sb
      .from("profiles")
      .select("is_admin")
      .eq("id", sessionData.session.user.id)
      .single();

    if (!profile?.is_admin) {
      document.getElementById("gate-message").textContent = "Admin access only.";
      return;
    }

    gate.classList.add("hidden");
    app.classList.remove("hidden");

    quill = new Quill("#editor", {
      theme: "snow",
      placeholder: "Grammar chart, vocabulary list, usage notes…",
      modules: {
        toolbar: [[{ header: [2, 3, false] }], ["bold", "italic"], [{ list: "ordered" }, { list: "bullet" }], ["clean"]],
      },
    });

    fillDropdowns();
    document.getElementById("btn-new").addEventListener("click", openNew);
    document.getElementById("add-grammar").addEventListener("click", () => addSet("inline_choice"));
    document.getElementById("add-vocab").addEventListener("click", () => addSet("dropdown_gap"));
    document.getElementById("add-vocab-lettered").addEventListener("click", () => addSet("lettered_gap"));
    lessonForm.addEventListener("submit", onSave);
    document.getElementById("btn-preview").addEventListener("click", () => editingId && window.open(`lesson.html?id=${editingId}`, "_blank"));
    document.getElementById("btn-delete").addEventListener("click", onDelete);

    await refreshList();
  }

  function fillDropdowns() {
    const site = window.SITE;
    document.getElementById("level").innerHTML = site.levels.map((l) => `<option value="${l.id}">${l.title} — ${l.subtitle}</option>`).join("");
    document.getElementById("section").innerHTML = site.sections.map((s) => `<option value="${s.id}">${s.title}</option>`).join("");
  }

  async function refreshList() {
    const { data, error } = await window.sb.from("lessons").select("id, title, level, section, is_published").order("updated_at", { ascending: false });
    const el = document.getElementById("lesson-list");
    document.getElementById("list-status").textContent = error ? error.message : `${data?.length || 0} lessons`;
    if (!data?.length) {
      el.innerHTML = "<p class='text-sm text-gray-400'>No lessons yet.</p>";
      return;
    }
    el.innerHTML = data
      .map(
        (l) => `
      <button type="button" data-id="${l.id}" class="w-full rounded-xl border bg-white px-4 py-3 text-left text-sm hover:border-brand ${editingId === l.id ? "ring-2 ring-brand" : ""}">
        <span class="font-semibold">${esc(l.title)}</span>
        <span class="mt-1 block text-xs text-gray-400">${l.level.toUpperCase()} · ${l.section} ${l.is_published ? "· LIVE" : "· draft"}</span>
      </button>`
      )
      .join("");
    el.querySelectorAll("[data-id]").forEach((btn) => btn.addEventListener("click", () => loadLesson(Number(btn.dataset.id))));
  }

  function openNew() {
    editingId = null;
    exerciseSets = [];
    lessonForm.reset();
    quill.setContents([]);
    document.getElementById("editor-heading").textContent = "New lesson";
    document.getElementById("btn-preview").classList.add("hidden");
    document.getElementById("btn-delete").classList.add("hidden");
    editorEmpty.classList.add("hidden");
    editorPanel.classList.remove("hidden");
    renderSets();
    hideMsg();
  }

  async function loadLesson(id) {
    const { data: lesson } = await window.sb.from("lessons").select("*").eq("id", id).single();
    if (!lesson) return;

    const { data: sets } = await window.sb.from("exercise_sets").select("*").eq("lesson_id", id).order("sort_order");

    editingId = id;
    document.getElementById("title").value = lesson.title;
    document.getElementById("level").value = lesson.level;
    document.getElementById("section").value = lesson.section;
    document.getElementById("audio-url").value = lesson.audio_url || "";
    document.getElementById("pdf-url").value = lesson.pdf_url || "";
    document.getElementById("is-published").checked = lesson.is_published;
    document.getElementById("is-premium").checked = lesson.is_premium;
    quill.root.innerHTML = lesson.explanation || "";

    exerciseSets = (sets || []).map((s) => ({
      title: s.title,
      instructions: s.instructions || "",
      type: s.type,
      word_bank: (s.word_bank || []).join("\n"),
      use_once: s.use_once,
      questions_text: (s.questions || []).map((q) => q.text).join("\n"),
    }));

    document.getElementById("editor-heading").textContent = "Edit lesson";
    document.getElementById("btn-preview").classList.remove("hidden");
    document.getElementById("btn-delete").classList.remove("hidden");
    editorEmpty.classList.add("hidden");
    editorPanel.classList.remove("hidden");
    renderSets();
    await refreshList();
  }

  function addSet(type) {
    const n = exerciseSets.length + 1;
    const isDropdown = type === "dropdown_gap";
    const isLettered = type === "lettered_gap";
    const defaults = {
      title: `Exercise ${n}`,
      instructions: isDropdown
        ? "Choose the correct option to complete these sentences. Use each option ONLY ONCE."
        : isLettered
          ? "Choose the correct option for each gap."
          : "Choose the correct option to complete the sentences.",
      type,
      word_bank: isDropdown
        ? "get up\nhave breakfast\ngo to bed\ngo shopping\nwatch TV"
        : "",
      use_once: isDropdown,
      questions_text: isDropdown
        ? "After I ___ in the morning, I make my bed. | get up\nWe ___ on the sofa after dinner. | watch TV"
        : isLettered
          ? "After I ____, I get dressed and go to school. | *have breakfast | go shopping | watch TV\nBefore I go to bed, I ____. | *brush my teeth | go to the gym | have lunch"
          : "I [*don't drink|not drink|drink not] tea.\nShe [*goes|go|going] to school every day.",
    };
    exerciseSets.push(defaults);
    renderSets();
  }

  function renderSets() {
    setsContainer.innerHTML = exerciseSets
      .map((set, i) => {
        const isDropdown = set.type === "dropdown_gap";
        const isLettered = set.type === "lettered_gap";
        const label = isDropdown ? "Vocabulary (dropdown)" : isLettered ? "Vocabulary (lettered)" : "Grammar";
        return `
        <div class="rounded-xl border border-gray-200 bg-gray-50 p-4" data-set-index="${i}">
          <div class="flex items-center justify-between">
            <span class="text-sm font-bold text-brand">${label} — Exercise ${i + 1}</span>
            <button type="button" data-remove-set="${i}" class="text-xs text-red-600 hover:underline">Remove</button>
          </div>
          <div class="mt-3 space-y-3">
            <input data-field="title" data-i="${i}" value="${escAttr(set.title)}" placeholder="Exercise title"
                   class="w-full rounded-lg border px-3 py-2 text-sm" />
            <textarea data-field="instructions" data-i="${i}" rows="2" placeholder="Instructions for students"
                      class="w-full rounded-lg border px-3 py-2 text-sm">${esc(set.instructions)}</textarea>
            ${
              isDropdown
                ? `<textarea data-field="word_bank" data-i="${i}" rows="5" placeholder="Word bank — one phrase per line"
                      class="w-full rounded-lg border px-3 py-2 text-sm font-mono text-xs">${esc(set.word_bank)}</textarea>
                   <label class="flex items-center gap-2 text-sm"><input type="checkbox" data-field="use_once" data-i="${i}" ${set.use_once ? "checked" : ""} /> Use each option ONLY ONCE</label>`
                : isLettered
                  ? `<p class="text-xs text-gray-500">Format: <code class="rounded bg-gray-100 px-1">Sentence with ____. | *correct | wrong | wrong</code></p>`
                  : `<p class="text-xs text-gray-500">Format: <code class="rounded bg-gray-100 px-1">I [*don't drink|not drink|drink not] tea.</code></p>`
            }
            <div>
              <label class="text-xs font-medium text-gray-600">Questions (one per line)</label>
              <textarea data-field="questions_text" data-i="${i}" rows="6"
                        class="mt-1 w-full rounded-lg border px-3 py-2 font-mono text-xs leading-relaxed">${esc(set.questions_text)}</textarea>
            </div>
          </div>
        </div>`;
      })
      .join("");

    setsContainer.querySelectorAll("[data-remove-set]").forEach((btn) => {
      btn.addEventListener("click", () => {
        exerciseSets.splice(Number(btn.dataset.removeSet), 1);
        renderSets();
      });
    });

    setsContainer.querySelectorAll("[data-field]").forEach((el) => {
      el.addEventListener("input", syncSetsFromDom);
      el.addEventListener("change", syncSetsFromDom);
    });
  }

  function syncSetsFromDom() {
    setsContainer.querySelectorAll("[data-set-index]").forEach((card) => {
      const i = Number(card.dataset.setIndex);
      card.querySelectorAll("[data-field]").forEach((el) => {
        const field = el.dataset.field;
        if (field === "use_once") exerciseSets[i][field] = el.checked;
        else exerciseSets[i][field] = el.value;
      });
    });
  }

  function buildSetsPayload() {
    syncSetsFromDom();
    return exerciseSets.map((set, i) => {
      const lines = set.questions_text.split("\n").map((l) => l.trim()).filter(Boolean);
      const questions = lines.map((text) => ({ text, feedback: "" }));
      const word_bank = set.type === "dropdown_gap"
        ? set.word_bank.split("\n").map((s) => s.trim()).filter(Boolean)
        : null;
      return {
        title: set.title || `Exercise ${i + 1}`,
        instructions: set.instructions,
        type: set.type,
        word_bank,
        use_once: !!set.use_once,
        questions,
        sort_order: i + 1,
      };
    });
  }

  async function onSave(e) {
    e.preventDefault();
    syncSetsFromDom();
    const publish = e.submitter?.dataset.mode === "publish";

    if (publish && !exerciseSets.length) {
      showMsg("Add at least one exercise before publishing.", "error");
      return;
    }

    const payload = {
      title: document.getElementById("title").value.trim(),
      level: document.getElementById("level").value,
      section: document.getElementById("section").value,
      explanation: quill.root.innerHTML,
      audio_url: document.getElementById("audio-url").value.trim() || null,
      pdf_url: document.getElementById("pdf-url").value.trim() || null,
      is_published: publish || document.getElementById("is-published").checked,
      is_premium: document.getElementById("is-premium").checked,
      updated_at: new Date().toISOString(),
    };

    let lessonId = editingId;
    if (lessonId) {
      const { error } = await window.sb.from("lessons").update(payload).eq("id", lessonId);
      if (error) return showMsg(error.message, "error");
      await window.sb.from("exercise_sets").delete().eq("lesson_id", lessonId);
    } else {
      const { data, error } = await window.sb.from("lessons").insert({ ...payload, sort_order: 0 }).select("id").single();
      if (error) return showMsg(error.message, "error");
      lessonId = data.id;
      editingId = lessonId;
    }

    const rows = buildSetsPayload().map((r) => ({ ...r, lesson_id: lessonId }));
    if (rows.length) {
      const { error } = await window.sb.from("exercise_sets").insert(rows);
      if (error) return showMsg("Lesson saved but exercises failed: " + error.message, "error");
    }

    showMsg(publish ? "Published!" : "Draft saved.", "success");
    document.getElementById("btn-preview").classList.remove("hidden");
    document.getElementById("btn-delete").classList.remove("hidden");
    await refreshList();
  }

  async function onDelete() {
    if (!editingId || !confirm("Delete this lesson and all exercises?")) return;
    await window.sb.from("lessons").delete().eq("id", editingId);
    editingId = null;
    editorPanel.classList.add("hidden");
    editorEmpty.classList.remove("hidden");
    await refreshList();
  }

  function showMsg(text, type) {
    const el = document.getElementById("save-message");
    el.textContent = text;
    el.className = "rounded-lg px-4 py-3 text-sm " + (type === "error" ? "bg-red-50 text-red-700" : "bg-green-50 text-green-700");
    el.classList.remove("hidden");
  }
  function hideMsg() {
    document.getElementById("save-message").classList.add("hidden");
  }

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function escAttr(s) {
    return esc(s).replace(/"/g, "&quot;");
  }
})();
