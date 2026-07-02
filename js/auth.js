/*
  Shared auth logic for the header.
  - Checks if a user is logged in (Supabase session).
  - Shows "Log in / Sign up" for guests, or the user's email + "Log out" for members.
  - Handles the Log out button.

  Each page that uses this must have:
    <div id="auth-desktop"></div>   (in the desktop nav)
    <div id="auth-mobile"></div>    (in the mobile menu)
*/

(function () {
  // Buttons shown to visitors who are NOT logged in
  function guestDesktop() {
    return `
      <a href="login.html" class="rounded-md px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100">Log in</a>
      <a href="register.html" class="rounded-md bg-brand px-4 py-2 text-sm font-semibold text-white hover:bg-brand-dark">Sign up</a>`;
  }
  function guestMobile() {
    return `
      <div class="mt-2 flex gap-2">
        <a href="login.html" class="flex-1 rounded-md border border-gray-200 px-3 py-2 text-center text-sm font-medium">Log in</a>
        <a href="register.html" class="flex-1 rounded-md bg-brand px-3 py-2 text-center text-sm font-semibold text-white">Sign up</a>
      </div>`;
  }

  // Buttons shown to logged-in members
  function memberDesktop(email, isAdmin) {
    const adminLink = isAdmin
      ? `<a href="admin.html" class="rounded-md px-3 py-2 text-sm font-medium text-amber-700 hover:bg-amber-50">Admin</a>`
      : "";
    return `
      ${adminLink}
      <span class="hidden px-2 text-sm text-gray-500 lg:inline">${email}</span>
      <a href="account.html" class="rounded-md px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100">My account</a>
      <button data-logout class="rounded-md bg-gray-900 px-4 py-2 text-sm font-semibold text-white hover:bg-black">Log out</button>`;
  }
  function memberMobile(email, isAdmin) {
    const adminLink = isAdmin
      ? `<a href="admin.html" class="block rounded-md px-3 py-2 text-sm font-medium text-amber-700 hover:bg-amber-50">Admin</a>`
      : "";
    return `
      ${adminLink}
      <p class="px-1 pb-1 text-xs text-gray-400">${email}</p>
      <a href="account.html" class="block rounded-md px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100">My account</a>
      <button data-logout class="mt-2 w-full rounded-md bg-gray-900 px-3 py-2 text-sm font-semibold text-white">Log out</button>`;
  }

  async function render(session) {
    const desktop = document.getElementById("auth-desktop");
    const mobile = document.getElementById("auth-mobile");
    const loggedIn = session && session.user;
    const email = loggedIn ? session.user.email : "";
    let isAdmin = false;

    if (loggedIn && window.sb && window.SUPABASE_READY) {
      const { data: profile } = await window.sb
        .from("profiles")
        .select("is_admin")
        .eq("id", session.user.id)
        .single();
      isAdmin = !!profile?.is_admin;
    }

    if (desktop) desktop.innerHTML = loggedIn ? memberDesktop(email, isAdmin) : guestDesktop();
    if (mobile) mobile.innerHTML = loggedIn ? memberMobile(email, isAdmin) : guestMobile();

    // Attach Log out handlers
    document.querySelectorAll("[data-logout]").forEach((btn) => {
      btn.addEventListener("click", async () => {
        await window.sb.auth.signOut();
        window.location.href = "index.html";
      });
    });
  }

  document.addEventListener("DOMContentLoaded", async () => {
    // If keys are not set yet, just show guest buttons so the site still works.
    if (!window.sb || !window.SUPABASE_READY) {
      render(null);
      return;
    }
    const { data } = await window.sb.auth.getSession();
    await render(data.session);

    // Keep the header in sync if the user logs in/out in another tab.
    window.sb.auth.onAuthStateChange((_event, session) => {
      render(session);
    });
  });
})();
