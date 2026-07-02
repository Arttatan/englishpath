/*
  Home page logic:
  - inserts the brand name
  - builds the level and section cards from data.js
  - fills the "Levels" dropdown menu
  - handles the mobile menu
*/

document.addEventListener("DOMContentLoaded", () => {
  const data = window.SITE;
  if (!data) {
    console.error("Data file not found (js/data.js).");
    return;
  }

  // 1) Brand name in every element with the data-brand attribute
  document.querySelectorAll("[data-brand]").forEach((el) => {
    el.textContent = data.brand;
  });
  document.title = `${data.brand} — learn English step by step`;

  // 2) Level cards
  const levelsGrid = document.getElementById("levels-grid");
  if (levelsGrid) {
    levelsGrid.innerHTML = data.levels
      .map(
        (lvl) => `
        <a href="level.html?level=${lvl.id}"
           class="lift block rounded-xl bg-white shadow-sm ring-1 ring-gray-100 overflow-hidden">
          <div class="level-bar" style="background:${lvl.color}"></div>
          <div class="p-6">
            <div class="flex items-baseline gap-3">
              <span class="text-3xl font-extrabold" style="color:${lvl.color}">${lvl.title}</span>
              <span class="text-sm font-medium text-gray-500">${lvl.subtitle}</span>
            </div>
            <p class="mt-3 text-sm leading-relaxed text-gray-600">${lvl.description}</p>
            <span class="mt-4 inline-flex items-center gap-1 text-sm font-semibold text-indigo-600">
              Open level <span aria-hidden="true">→</span>
            </span>
          </div>
        </a>`
      )
      .join("");
  }

  // 3) Section cards
  const sectionsGrid = document.getElementById("sections-grid");
  if (sectionsGrid) {
    sectionsGrid.innerHTML = data.sections
      .map(
        (s) => `
        <div class="lift rounded-xl bg-white p-6 shadow-sm ring-1 ring-gray-100">
          <div class="text-3xl">${s.icon}</div>
          <h3 class="mt-3 text-lg font-semibold text-gray-900">${s.title}</h3>
          <p class="text-xs uppercase tracking-wide text-gray-400">${s.en}</p>
          <p class="mt-2 text-sm leading-relaxed text-gray-600">${s.description}</p>
        </div>`
      )
      .join("");
  }

  // 4) "Levels" dropdown in the header (desktop and mobile)
  const levelsLinks = data.levels
    .map(
      (lvl) => `
        <a href="level.html?level=${lvl.id}"
           class="flex items-center justify-between rounded-md px-3 py-2 text-sm text-gray-700 hover:bg-indigo-50">
          <span class="font-semibold">${lvl.title}</span>
          <span class="text-xs text-gray-400">${lvl.subtitle}</span>
        </a>`
    )
    .join("");
  const levelsMenu = document.getElementById("levels-menu");
  if (levelsMenu) levelsMenu.innerHTML = levelsLinks;
  const levelsMenuMobile = document.getElementById("levels-menu-mobile");
  if (levelsMenuMobile) levelsMenuMobile.innerHTML = levelsLinks;

  // 5) Subscription price in the banner
  document.querySelectorAll("[data-price]").forEach((el) => {
    el.textContent = data.price;
  });

  // 6) Mobile menu (open/close)
  const burger = document.getElementById("burger");
  const mobileMenu = document.getElementById("mobile-menu");
  if (burger && mobileMenu) {
    burger.addEventListener("click", () => {
      mobileMenu.classList.toggle("hidden");
    });
  }

  // 7) "Levels" dropdown toggle (desktop and mobile)
  const levelsToggle = document.getElementById("levels-toggle");
  const levelsDropdown = document.getElementById("levels-dropdown");
  if (levelsToggle && levelsDropdown) {
    levelsToggle.addEventListener("click", (e) => {
      e.stopPropagation();
      levelsDropdown.classList.toggle("hidden");
    });
    document.addEventListener("click", () => {
      levelsDropdown.classList.add("hidden");
    });
  }

  // 8) Current year in the footer
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();
});
