/*
  Account page: profile, progress, Stripe Premium actions.
*/

document.addEventListener("DOMContentLoaded", async () => {
  const brand = window.SITE?.brand || "EnglishPath";
  document.querySelectorAll("[data-brand]").forEach((el) => (el.textContent = brand));

  const burger = document.getElementById("burger");
  const mobileMenu = document.getElementById("mobile-menu");
  if (burger && mobileMenu) {
    burger.addEventListener("click", () => mobileMenu.classList.toggle("hidden"));
  }

  const billingMsg = document.getElementById("billing-message");
  function showBillingMessage(text, type) {
    if (!billingMsg) return;
    billingMsg.textContent = text;
    billingMsg.className =
      "mt-6 rounded-lg px-4 py-3 text-sm " +
      (type === "error" ? "bg-red-50 text-red-700" : "bg-green-50 text-green-700");
    billingMsg.classList.remove("hidden");
  }

  const params = new URLSearchParams(window.location.search);
  if (params.get("checkout") === "cancel") {
    showBillingMessage("Checkout cancelled. You can upgrade anytime.", "error");
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

  // After Checkout (or on every visit) sync Premium from Stripe
  if (window.EnglishPathBilling?.syncSubscription) {
    try {
      const sessionId = params.get("session_id");
      await window.EnglishPathBilling.syncSubscription(
        params.get("checkout") === "success" ? sessionId : null
      );
      if (params.get("checkout") === "success") {
        showBillingMessage("Payment received. Your Premium status is up to date.", "success");
      }
    } catch (err) {
      if (params.get("checkout") === "success") {
        showBillingMessage(
          "Payment received, but status sync failed: " + (err.message || "try refresh"),
          "error"
        );
      }
    }
  }

  const { data: profile } = await window.sb
    .from("profiles")
    .select("is_premium")
    .eq("id", user.id)
    .maybeSingle();

  const isPremium = !!profile?.is_premium;
  const planEl = document.getElementById("stat-plan");
  const planNote = document.getElementById("stat-plan-note");
  const btnUpgrade = document.getElementById("btn-upgrade");
  const btnManage = document.getElementById("btn-manage");

  if (planEl) planEl.textContent = isPremium ? "Premium" : "Free";
  if (planNote) {
    planNote.textContent = isPremium ? "Thank you for supporting EnglishPath" : "$5/mo optional Premium";
  }
  if (btnUpgrade) btnUpgrade.classList.toggle("hidden", isPremium);
  if (btnManage) btnManage.classList.toggle("hidden", !isPremium);

  if (btnUpgrade) {
    btnUpgrade.addEventListener("click", async () => {
      btnUpgrade.disabled = true;
      btnUpgrade.textContent = "Redirecting…";
      try {
        await window.EnglishPathBilling.startCheckout();
      } catch (err) {
        showBillingMessage(err.message || "Checkout failed", "error");
        btnUpgrade.disabled = false;
        btnUpgrade.textContent = "Upgrade — $5/mo";
      }
    });
  }

  if (btnManage) {
    btnManage.addEventListener("click", async () => {
      btnManage.disabled = true;
      btnManage.textContent = "Opening…";
      try {
        await window.EnglishPathBilling.openPortal();
      } catch (err) {
        showBillingMessage(err.message || "Could not open billing portal", "error");
        btnManage.disabled = false;
        btnManage.textContent = "Manage subscription";
      }
    });
  }

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
    statusEl.textContent =
      "No completed exercises yet. Open a lesson, check your answers, and your score will appear here.";
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
