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

  if (!lessons || lessons.length === 0) {
    if (listEl) listEl.innerHTML = "";
    if (statusEl) {
      statusEl.textContent = "No lessons here yet. New content is added regularly — check back soon.";
    }
    return;
  }

  if (statusEl) statusEl.textContent = `${lessons.length} lesson${lessons.length === 1 ? "" : "s"}`;

  const sectionWrap = listEl?.closest("section");
  if (sectionWrap) {
    sectionWrap.classList.remove("max-w-3xl");
    sectionWrap.classList.add("max-w-5xl");
  }

  if (listEl) {
    listEl.className = "lesson-card-grid";
    listEl.innerHTML = lessons.map((lesson) => renderLessonCard(lesson, level)).join("");
  }
});

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
      <div class="cover-to-be" style="width:100%;height:100%">
        <svg viewBox="0 0 320 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="To be illustration">
          <defs>
            <linearGradient id="sky" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#0f2744"/>
              <stop offset="100%" stop-color="#2a5a84"/>
            </linearGradient>
          </defs>
          <rect width="320" height="320" fill="url(#sky)"/>
          <circle cx="250" cy="70" r="28" fill="#fbbf24" opacity="0.85">
            <animate attributeName="opacity" values="0.7;1;0.7" dur="4s" repeatCount="indefinite"/>
          </circle>
          <!-- dashed thought bubble -->
          <circle cx="105" cy="110" r="58" fill="none" stroke="#e2e8f0" stroke-width="3" stroke-dasharray="6 7" opacity="0.9"/>
          <text x="105" y="100" text-anchor="middle" fill="#f8fafc" font-family="Georgia, serif" font-size="15" font-style="italic">To be or</text>
          <text x="105" y="122" text-anchor="middle" fill="#f8fafc" font-family="Georgia, serif" font-size="15" font-style="italic">not to be!</text>
          <!-- person -->
          <ellipse cx="210" cy="250" rx="48" ry="14" fill="#0b1c2e" opacity="0.35"/>
          <circle cx="210" cy="145" r="28" fill="#fcd9b0"/>
          <path d="M182 175 Q210 165 238 175 L248 250 L172 250 Z" fill="#d63384"/>
          <rect x="198" y="168" width="24" height="18" rx="4" fill="#b82a6f"/>
          <!-- skull prop -->
          <g transform="translate(248 175)">
            <ellipse cx="0" cy="0" rx="16" ry="14" fill="#e8e0d5"/>
            <circle cx="-5" cy="-2" r="3" fill="#334155"/>
            <circle cx="5" cy="-2" r="3" fill="#334155"/>
            <path d="M-4 8 Q0 12 4 8" fill="none" stroke="#64748b" stroke-width="1.5"/>
          </g>
          <text x="160" y="300" text-anchor="middle" fill="#94a3b8" font-family="system-ui,sans-serif" font-size="11" font-weight="600">am · is · are</text>
        </svg>
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
