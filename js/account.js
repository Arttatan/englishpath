/*
  Account page: show profile email + lesson progress from user_progress.
*/

document.addEventListener("DOMContentLoaded", async () => {
  const brand = window.SITE?.brand || "EnglishPath";
  document.querySelectorAll("[data-brand]").forEach((el) => (el.textContent = brand));

  const burger = document.getElementById("burger");
  const mobileMenu = document.getElementById("mobile-menu");
  if (burger && mobileMenu) {
    burger.addEventListener("click", () => mobileMenu.classList.toggle("hidden"));
  }

  if (!window.sb || !window.SUPABASE_READY) {
    window.location.href = "login.html";
    return;
  }

  const { data: sessionData } = await window.sb.auth.getSession();
  const user = sessionData?.session?.user;
  if (!user) {
    window.location.href = "login.html";
    return;
  }

  document.getElementById("account-email").textContent = user.email || "";

  const { data: profile } = await window.sb
    .from("profiles")
    .select("is_premium")
    .eq("id", user.id)
    .maybeSingle();

  const planEl = document.getElementById("stat-plan");
  if (planEl) planEl.textContent = profile?.is_premium ? "Premium" : "Free";

  const statusEl = document.getElementById("progress-status");
  const listEl = document.getElementById("progress-list");

  const { data: rows, error } = await window.sb
    .from("user_progress")
    .select("score, total, completed_at, lesson_id, lessons(id, title, level, section)")
    .eq("user_id", user.id)
    .order("completed_at", { ascending: false })
    .limit(50);

  if (error) {
    statusEl.textContent = "Could not load progress: " + error.message;
    return;
  }

  if (!rows || rows.length === 0) {
    document.getElementById("stat-lessons").textContent = "0";
    document.getElementById("stat-avg").textContent = "—";
    statusEl.textContent = "No completed exercises yet. Open a lesson, check your answers, and your score will appear here.";
    listEl.innerHTML = "";
    return;
  }

  const lessonsDone = rows.length;
  let pctSum = 0;
  rows.forEach((r) => {
    pctSum += r.total > 0 ? r.score / r.total : 0;
  });
  const avgPct = Math.round((pctSum / lessonsDone) * 100);

  document.getElementById("stat-lessons").textContent = String(lessonsDone);
  document.getElementById("stat-avg").textContent = avgPct + "%";
  statusEl.textContent = `${lessonsDone} lesson${lessonsDone === 1 ? "" : "s"} with saved results.`;

  const levelTitle = (id) => window.SITE?.levels?.find((l) => l.id === id)?.title || id || "";
  const sectionTitle = (id) => window.SITE?.sections?.find((s) => s.id === id)?.title || id || "";

  listEl.innerHTML = rows
    .map((r) => {
      const lesson = r.lessons;
      const title = lesson?.title || "Lesson";
      const meta = [levelTitle(lesson?.level), sectionTitle(lesson?.section)].filter(Boolean).join(" · ");
      const pct = r.total > 0 ? Math.round((r.score / r.total) * 100) : 0;
      const when = r.completed_at ? new Date(r.completed_at).toLocaleDateString() : "";
      const href = lesson?.id ? `lesson.html?id=${lesson.id}` : "index.html";
      return `
        <a href="${href}" class="flex items-center justify-between gap-4 rounded-xl bg-white px-5 py-4 shadow-sm ring-1 ring-gray-100 hover:ring-brand/30">
          <div class="min-w-0">
            <p class="truncate font-semibold text-gray-900">${escapeHtml(title)}</p>
            <p class="mt-0.5 text-xs text-gray-500">${escapeHtml(meta)}${when ? " · " + when : ""}</p>
          </div>
          <div class="shrink-0 text-right">
            <p class="text-sm font-bold text-brand">${r.score}/${r.total}</p>
            <p class="text-xs text-gray-400">${pct}%</p>
          </div>
        </a>`;
    })
    .join("");
});

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
