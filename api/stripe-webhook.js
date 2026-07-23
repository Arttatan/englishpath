const {
  getStripe,
  updateProfileBilling,
  updateProfileBillingByCustomer,
  requireEnv,
  sendJson,
} = require("../lib/server-helpers");

async function readRawBody(req) {
  const chunks = [];
  for await (const chunk of req) {
    chunks.push(typeof chunk === "string" ? Buffer.from(chunk) : chunk);
  }
  return Buffer.concat(chunks);
}

async function setPremiumByUserId(userId, premium, subscriptionId) {
  if (!userId) return;
  const patch = {
    is_premium: !!premium,
    stripe_subscription_id: subscriptionId || null,
  };
  if (!premium) patch.premium_until = null;
  await updateProfileBilling(userId, patch);
}

async function setPremiumByCustomerId(customerId, premium, subscriptionId) {
  if (!customerId) return;
  const patch = {
    is_premium: !!premium,
    stripe_subscription_id: subscriptionId || null,
  };
  if (!premium) patch.premium_until = null;
  await updateProfileBillingByCustomer(customerId, patch);
}

module.exports = async function handler(req, res) {
  if (req.method !== "POST") return sendJson(res, 405, { error: "Method not allowed" });

  // Sandbox keys cannot create webhook endpoints until claimed.
  // Sync via /api/sync-subscription works without this.
  if (!process.env.STRIPE_WEBHOOK_SECRET) {
    return sendJson(res, 503, { error: "Webhook not configured yet" });
  }

  const stripe = getStripe();
  const webhookSecret = requireEnv("STRIPE_WEBHOOK_SECRET");

  let event;
  try {
    const rawBody = await readRawBody(req);
    const signature = req.headers["stripe-signature"];
    event = stripe.webhooks.constructEvent(rawBody, signature, webhookSecret);
  } catch (err) {
    console.error("webhook signature", err.message);
    return sendJson(res, 400, { error: `Webhook Error: ${err.message}` });
  }

  try {
    switch (event.type) {
      case "checkout.session.completed": {
        const session = event.data.object;
        if (session.mode !== "subscription") break;
        const userId = session.client_reference_id || session.metadata?.supabase_user_id;
        const subId =
          typeof session.subscription === "string"
            ? session.subscription
            : session.subscription?.id;
        const customerId =
          typeof session.customer === "string" ? session.customer : session.customer?.id;
        if (userId) {
          await updateProfileBilling(userId, {
            is_premium: true,
            stripe_customer_id: customerId || undefined,
            stripe_subscription_id: subId || null,
          });
        } else if (customerId) {
          await setPremiumByCustomerId(customerId, true, subId);
        }
        break;
      }
      case "customer.subscription.updated":
      case "customer.subscription.created": {
        const sub = event.data.object;
        const active = ["active", "trialing"].includes(sub.status);
        const userId = sub.metadata?.supabase_user_id;
        const customerId = typeof sub.customer === "string" ? sub.customer : sub.customer?.id;
        if (userId) await setPremiumByUserId(userId, active, sub.id);
        else await setPremiumByCustomerId(customerId, active, sub.id);
        break;
      }
      case "customer.subscription.deleted": {
        const sub = event.data.object;
        const userId = sub.metadata?.supabase_user_id;
        const customerId = typeof sub.customer === "string" ? sub.customer : sub.customer?.id;
        if (userId) await setPremiumByUserId(userId, false, null);
        else await setPremiumByCustomerId(customerId, false, null);
        break;
      }
      default:
        break;
    }
  } catch (err) {
    console.error("webhook handler", err);
    return sendJson(res, 500, { error: "Webhook handler failed" });
  }

  return sendJson(res, 200, { received: true });
};

module.exports.config = {
  api: {
    bodyParser: false,
  },
};
