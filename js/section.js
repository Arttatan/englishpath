/*
  Section page logic (section.html).
  Reads ?level=a1&section=grammar from the URL and loads published lessons from Supabase.
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

  // Mobile menu
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
    .select("id, title, sort_order, is_premium")
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

  if (listEl) {
    listEl.innerHTML = lessons
      .map(
        (lesson, i) => `
        <a href="lesson.html?id=${lesson.id}"
           class="lift flex items-center justify-between rounded-xl bg-white px-6 py-5 shadow-sm ring-1 ring-gray-100">
          <div class="flex items-center gap-4">
            <span class="grid h-10 w-10 shrink-0 place-items-center rounded-lg bg-indigo-50 text-sm font-bold text-brand">${i + 1}</span>
            <div>
              <h3 class="font-semibold text-gray-900">${escapeHtml(lesson.title)}</h3>
              ${lesson.is_premium ? '<span class="mt-1 inline-block text-xs font-medium text-amber-600">Premium bonus</span>' : '<span class="mt-1 inline-block text-xs text-gray-400">Free</span>'}
            </div>
          </div>
          <span class="text-sm font-semibold text-brand">Start →</span>
        </a>`
      )
      .join("");
  }
});

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
