/*
  Section page logic (section.html).
  Reads ?level=a1&section=grammar from the URL and loads published lessons from Supabase.
  Renders square illustrated cards (click → lesson).
*/

document.addEventListener("DOMContentLoaded", async () => {
  const data = window.SITE;
  if (!data) return;

  document.querySelectorAll("[data-brand]").forEach((el) => (el.textContent = data.brand));
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  const params = new URLSearchParams(window.location.search);
  const levelId = params.get("level");
  const sectionId = params.get("section");

  const level = data.levels.find((l) => l.id === levelId);
  const section = data.sections.find((s) => s.id === sectionId);

  const breadcrumbLevel = document.getElementById("breadcrumb-level");
  const breadcrumbSection = document.getElementById("breadcrumb-section");
  const titleEl = document.getElementById("section-title");
  const subtitleEl = document.getElementById("section-subtitle");
  const listEl = document.getElementById("lessons-list");
  const statusEl = document.getElementById("status");

  if (!level || !section) {
    if (titleEl) titleEl.textContent = "Section not found";
    if (statusEl) statusEl.textContent = "Go back and pick a level and section from the menu.";
    return;
  }

  document.title = `${section.title} — ${level.title} — ${data.brand}`;
  if (breadcrumbLevel) {
    breadcrumbLevel.textContent = level.title;
    breadcrumbLevel.href = `level.html?level=${level.id}`;
  }
  if (breadcrumbSection) breadcrumbSection.textContent = section.title;
  if (titleEl) titleEl.textContent = section.title;
  if (subtitleEl) subtitleEl.textContent = `${level.title} · ${level.subtitle}`;

  const burger = document.getElementById("burger");
  const mobileMenu = document.getElementById("mobile-menu");
  if (burger && mobileMenu) {
    burger.addEventListener("click", () => mobileMenu.classList.toggle("hidden"));
  }

  if (!window.sb || !window.SUPABASE_READY) {
    if (statusEl) statusEl.textContent = "Database not connected. Check js/config.js.";
    return;
  }

  if (statusEl) statusEl.textContent = "Loading lessons…";

  await maybePublishHaveGot(levelId, sectionId);

  const { data: lessons, error } = await window.sb
    .from("lessons")
    .select("id, title, sort_order, is_premium, cover_key")
    .eq("level", levelId)
    .eq("section", sectionId)
    .eq("is_published", true)
    .order("sort_order", { ascending: true });

  if (error) {
    if (statusEl) statusEl.textContent = "Could not load lessons: " + error.message;
    return;
  }

  const listed =
    window.EnglishPathCatalog && typeof window.EnglishPathCatalog.isListedOnSection === "function"
      ? (lessons || []).filter((l) => window.EnglishPathCatalog.isListedOnSection(l, levelId))
      : lessons || [];

  if (!listed.length) {
    if (listEl) listEl.innerHTML = "";
    if (statusEl) {
      statusEl.textContent = "No lessons here yet. New content is added regularly — check back soon.";
    }
    return;
  }

  if (statusEl) statusEl.textContent = `${listed.length} lesson${listed.length === 1 ? "" : "s"}`;

  const sectionWrap = listEl?.closest("section");
  if (sectionWrap) {
    sectionWrap.classList.remove("max-w-3xl");
    sectionWrap.classList.add("max-w-5xl");
  }

  if (listEl) {
    listEl.className = "lesson-card-grid";
    listEl.innerHTML = listed.map((lesson) => renderLessonCard(lesson, level)).join("");
  }
});

async function maybePublishHaveGot(levelId, sectionId) {
  if (levelId !== "a1" || sectionId !== "grammar" || !window.sb) return;
  try {
    const { data: sessionData } = await window.sb.auth.getSession();
    const token = sessionData?.session?.access_token;
    if (!token) return;
    const { data: profile } = await window.sb
      .from("profiles")
      .select("is_admin")
      .eq("id", sessionData.session.user.id)
      .maybeSingle();
    if (!profile?.is_admin) return;
    await fetch("/api/admin-seed-lesson", {
      method: "POST",
      headers: {
        Authorization: "Bearer " + token,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ lesson: "have-got" }),
    });
  } catch (_) {
    /* seed is best-effort; catalog still shows lesson 209 */
  }
}

function renderLessonCard(lesson, level) {
  const levelLabel = (level?.id || "a1").toUpperCase();
  const art = coverArt(lesson.cover_key, lesson.title);
  return `
    <a href="lesson.html?id=${lesson.id}" class="lesson-card" aria-label="${escapeHtml(lesson.title)}">
      <div class="lesson-card-art">
        <span class="lesson-card-badge" aria-hidden="true">${escapeHtml(levelLabel)}</span>
        <div class="lesson-card-art-inner">${art}</div>
      </div>
      <h3 class="lesson-card-title">${escapeHtml(lesson.title)}</h3>
    </a>`;
}

function coverArt(coverKey, title) {
  if (coverKey === "to-be") {
    return `
      <div class="cover-to-be cover-to-be--photo" style="width:100%;height:100%">
        <img
          src="images/grammar/a1/to-be-cover.png"
          alt="Present simple forms of to be: am, is, are"
          class="cover-to-be-img"
          width="1024"
          height="1024"
          loading="lazy"
          decoding="async"
        />
      </div>`;
  }

  const initial = String(title || "?").trim().charAt(0).toUpperCase() || "?";
  return `<div class="cover-fallback" style="width:100%;height:100%"><span class="cover-fallback-mark">${escapeHtml(initial)}</span></div>`;
}

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
