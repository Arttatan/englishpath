const {
  getStripe,
  getProfileBilling,
  updateProfileBilling,
  getUserFromAuthHeader,
  sendJson,
} = require("../lib/server-helpers");

/**
 * Sync Premium status from Stripe (works without webhooks).
 * Optional body: { session_id } after Checkout to confirm that session first.
 */
module.exports = async function handler(req, res) {
  if (req.method !== "POST") return sendJson(res, 405, { error: "Method not allowed" });

  try {
    const user = await getUserFromAuthHeader(req);
    if (!user) return sendJson(res, 401, { error: "Please log in first." });

    const stripe = getStripe();
    let profile = await getProfileBilling(user.id);
    if (!profile) return sendJson(res, 404, { error: "Profile not found" });

    let body = {};
    try {
      const chunks = [];
      for await (const chunk of req) chunks.push(chunk);
      const raw = Buffer.concat(chunks).toString("utf8");
      if (raw) body = JSON.parse(raw);
    } catch (_) {
      body = {};
    }

    if (body.session_id) {
      const session = await stripe.checkout.sessions.retrieve(body.session_id);
      const sessionUser =
        session.client_reference_id || session.metadata?.supabase_user_id || null;
      if (sessionUser && sessionUser !== user.id) {
        return sendJson(res, 403, { error: "Checkout session does not belong to you." });
      }
      if (session.customer && !profile.stripe_customer_id) {
        const customerId =
          typeof session.customer === "string" ? session.customer : session.customer.id;
        await updateProfileBilling(user.id, { stripe_customer_id: customerId });
        profile = await getProfileBilling(user.id);
      }
    }

    let customerId = profile.stripe_customer_id;
    if (!customerId) {
      await updateProfileBilling(user.id, {
        is_premium: false,
        stripe_subscription_id: null,
      });
      return sendJson(res, 200, { is_premium: false });
    }

    const subs = await stripe.subscriptions.list({
      customer: customerId,
      status: "all",
      limit: 10,
    });

    const active = subs.data.find((s) => ["active", "trialing"].includes(s.status));
    const patch = {
      is_premium: !!active,
      stripe_subscription_id: active ? active.id : null,
    };
    if (!active) patch.premium_until = null;

    await updateProfileBilling(user.id, patch);
    return sendJson(res, 200, {
      is_premium: !!active,
      subscription_id: active ? active.id : null,
    });
  } catch (err) {
    console.error("sync-subscription", err);
    return sendJson(res, 500, { error: err.message || "Sync failed" });
  }
};
