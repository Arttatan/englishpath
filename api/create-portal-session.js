const {
  getStripe,
  getProfileBilling,
  getSiteUrl,
  getUserFromAuthHeader,
  sendJson,
} = require("../lib/server-helpers");

module.exports = async function handler(req, res) {
  if (req.method !== "POST") return sendJson(res, 405, { error: "Method not allowed" });

  try {
    const user = await getUserFromAuthHeader(req);
    if (!user) return sendJson(res, 401, { error: "Please log in first." });

    const stripe = getStripe();
    const siteUrl = getSiteUrl(req);
    const profile = await getProfileBilling(user.id);

    if (!profile?.stripe_customer_id) {
      return sendJson(res, 400, { error: "No billing account yet. Subscribe to Premium first." });
    }

    const portal = await stripe.billingPortal.sessions.create({
      customer: profile.stripe_customer_id,
      return_url: `${siteUrl}/account.html`,
      locale: "en",
    });

    return sendJson(res, 200, { url: portal.url });
  } catch (err) {
    console.error("create-portal-session", err);
    return sendJson(res, 500, { error: err.message || "Portal failed" });
  }
};
