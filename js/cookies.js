/*
  Soft cookie notice for AdSense readiness.
  Stores choice in localStorage: englishpath_cookie_consent = "accepted" | "essential"
*/

(function () {
  const KEY = "englishpath_cookie_consent";
  if (localStorage.getItem(KEY)) return;

  const bar = document.createElement("div");
  bar.id = "cookie-banner";
  bar.setAttribute("role", "dialog");
  bar.setAttribute("aria-live", "polite");
  bar.className =
    "fixed inset-x-0 bottom-0 z-[100] border-t border-gray-200 bg-white/95 p-4 shadow-[0_-8px_30px_rgba(0,0,0,0.08)] backdrop-blur";
  bar.innerHTML = `
    <div class="mx-auto flex max-w-6xl flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <p class="text-sm text-gray-600">
        We use essential cookies to keep you signed in, and may use analytics/advertising cookies later (e.g. Google AdSense).
        See our <a href="privacy.html" class="font-semibold text-brand hover:underline">Privacy Policy</a>.
      </p>
      <div class="flex shrink-0 gap-2">
        <button type="button" data-cookie="essential"
          class="rounded-lg border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">
          Essential only
        </button>
        <button type="button" data-cookie="accepted"
          class="rounded-lg bg-brand px-4 py-2 text-sm font-semibold text-white hover:bg-brand-dark">
          Accept
        </button>
      </div>
    </div>`;

  document.body.appendChild(bar);

  bar.querySelectorAll("[data-cookie]").forEach((btn) => {
    btn.addEventListener("click", () => {
      localStorage.setItem(KEY, btn.getAttribute("data-cookie"));
      bar.remove();
    });
  });
})();
