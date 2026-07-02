/*
  Level page logic (level.html).
  Reads ?level=a1 from the URL, finds the level in data.js
  and shows its sections. Lessons will appear in later steps.
*/

document.addEventListener("DOMContentLoaded", () => {
  const data = window.SITE;
  if (!data) return;

  // Brand name
  document.querySelectorAll("[data-brand]").forEach((el) => (el.textContent = data.brand));

  // Year in the footer
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Which level is open?
  const params = new URLSearchParams(window.location.search);
  const levelId = params.get("level");
  const level = data.levels.find((l) => l.id === levelId);

  const titleEl = document.getElementById("level-title");
  const subtitleEl = document.getElementById("level-subtitle");
  const descEl = document.getElementById("level-desc");
  const barEl = document.getElementById("level-bar");
  const grid = document.getElementById("level-sections");

  // If the level was not found, show a message
  if (!level) {
    if (titleEl) titleEl.textContent = "Level not found";
    if (descEl) descEl.textContent = "Go back to the home page and pick a level from the list.";
    return;
  }

  document.title = `${level.title} (${level.subtitle}) — ${data.brand}`;
  if (titleEl) titleEl.textContent = level.title;
  if (subtitleEl) subtitleEl.textContent = level.subtitle;
  if (descEl) descEl.textContent = level.description;
  if (barEl) barEl.style.background = level.color;

  // Level sections
  if (grid) {
    grid.innerHTML = data.sections
      .map(
        (s) => `
        <a href="section.html?level=${level.id}&section=${s.id}"
           class="lift block rounded-xl bg-white p-6 shadow-sm ring-1 ring-gray-100">
          <div class="text-3xl">${s.icon}</div>
          <h3 class="mt-3 text-lg font-semibold text-gray-900">${s.title}</h3>
          <p class="text-xs uppercase tracking-wide text-gray-400">${s.en}</p>
          <p class="mt-2 text-sm leading-relaxed text-gray-600">${s.description}</p>
          <span class="mt-4 inline-flex items-center gap-1 text-sm font-semibold text-indigo-600">
            Open <span aria-hidden="true">→</span>
          </span>
        </a>`
      )
      .join("");
  }

  // Mobile menu
  const burger = document.getElementById("burger");
  const mobileMenu = document.getElementById("mobile-menu");
  if (burger && mobileMenu) {
    burger.addEventListener("click", () => mobileMenu.classList.toggle("hidden"));
  }
});
