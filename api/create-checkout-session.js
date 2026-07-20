const {
  getStripe,
  getServiceSupabase,
  getSiteUrl,
  getUserFromAuthHeader,
  requireEnv,
  sendJson,
} = require("../lib/server-helpers");

module.exports = async function handler(req, res) {
  if (req.method !== "POST") return sendJson(res, 405, { error: "Method not allowed" });

  try {
    const user = await getUserFromAuthHeader(req);
    if (!user) return sendJson(res, 401, { error: "Please log in first." });

    const stripe = getStripe();
    const supabase = getServiceSupabase();
    const siteUrl = getSiteUrl(req);
    const priceId = requireEnv("STRIPE_PRICE_ID");

    const { data: profile } = await supabase
      .from("profiles")
      .select("stripe_customer_id, email, is_premium")
      .eq("id", user.id)
      .maybeSingle();

    if (profile?.is_premium) {
      return sendJson(res, 400, { error: "You already have Premium." });
    }

    let customerId = profile?.stripe_customer_id || null;
    if (!customerId) {
      const customer = await stripe.customers.create({
        email: user.email || profile?.email || undefined,
        metadata: { supabase_user_id: user.id },
      });
      customerId = customer.id;
      await supabase
        .from("profiles")
        .update({ stripe_customer_id: customerId })
        .eq("id", user.id);
    }

    const session = await stripe.checkout.sessions.create({
      mode: "subscription",
      customer: customerId,
      client_reference_id: user.id,
      line_items: [{ price: priceId, quantity: 1 }],
      success_url: `${siteUrl}/account.html?checkout=success`,
      cancel_url: `${siteUrl}/account.html?checkout=cancel`,
      allow_promotion_codes: true,
      subscription_data: {
        metadata: { supabase_user_id: user.id },
      },
      metadata: { supabase_user_id: user.id },
    });

    return sendJson(res, 200, { url: session.url });
  } catch (err) {
    console.error("create-checkout-session", err);
    return sendJson(res, 500, { error: err.message || "Checkout failed" });
  }
};
