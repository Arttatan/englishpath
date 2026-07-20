/*
  Stripe Checkout + Customer Portal helpers (browser).
*/

window.EnglishPathBilling = {
  async startCheckout() {
    if (!window.sb || !window.SUPABASE_READY) {
      window.location.href = "login.html";
      return;
    }
    const { data } = await window.sb.auth.getSession();
    if (!data?.session) {
      window.location.href = "login.html?next=account.html";
      return;
    }

    const res = await fetch("/api/create-checkout-session", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + data.session.access_token,
      },
    });
    const json = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(json.error || "Could not start checkout");
    if (!json.url) throw new Error("No checkout URL returned");
    window.location.href = json.url;
  },

  async openPortal() {
    if (!window.sb || !window.SUPABASE_READY) {
      window.location.href = "login.html";
      return;
    }
    const { data } = await window.sb.auth.getSession();
    if (!data?.session) {
      window.location.href = "login.html";
      return;
    }

    const res = await fetch("/api/create-portal-session", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + data.session.access_token,
      },
    });
    const json = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(json.error || "Could not open billing portal");
    if (!json.url) throw new Error("No portal URL returned");
    window.location.href = json.url;
  },
};
