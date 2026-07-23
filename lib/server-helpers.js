const { createClient } = require("@supabase/supabase-js");
const { Pool } = require("pg");
const Stripe = require("stripe");

let pool;

function requireEnv(name) {
  const v = process.env[name];
  if (!v) throw new Error(`Missing env: ${name}`);
  return v;
}

function getStripe() {
  return new Stripe(requireEnv("STRIPE_SECRET_KEY"));
}

function getPool() {
  if (!pool) {
    pool = new Pool({
      connectionString: requireEnv("DATABASE_URL"),
      ssl: { rejectUnauthorized: false },
      max: 2,
    });
  }
  return pool;
}

/** Profile billing reads/writes via Postgres (bypasses RLS + billing trigger). */
async function getProfileBilling(userId) {
  const { rows } = await getPool().query(
    `select id, email, is_premium, stripe_customer_id, stripe_subscription_id
     from public.profiles where id = $1`,
    [userId]
  );
  return rows[0] || null;
}

async function updateProfileBilling(userId, patch) {
  const fields = [];
  const values = [];
  let i = 1;
  for (const [key, val] of Object.entries(patch)) {
    if (val === undefined) continue;
    fields.push(`${key} = $${i++}`);
    values.push(val);
  }
  if (!fields.length) return;
  values.push(userId);
  await getPool().query(
    `update public.profiles set ${fields.join(", ")} where id = $${i}`,
    values
  );
}

async function updateProfileBillingByCustomer(customerId, patch) {
  const fields = [];
  const values = [];
  let i = 1;
  for (const [key, val] of Object.entries(patch)) {
    if (val === undefined) continue;
    fields.push(`${key} = $${i++}`);
    values.push(val);
  }
  if (!fields.length) return;
  values.push(customerId);
  await getPool().query(
    `update public.profiles set ${fields.join(", ")} where stripe_customer_id = $${i}`,
    values
  );
}

function getSiteUrl(req) {
  if (process.env.SITE_URL) return process.env.SITE_URL.replace(/\/$/, "");
  const proto = req.headers["x-forwarded-proto"] || "https";
  const host = req.headers["x-forwarded-host"] || req.headers.host;
  return `${proto}://${host}`;
}

async function getUserFromAuthHeader(req) {
  const auth = req.headers.authorization || "";
  const token = auth.startsWith("Bearer ") ? auth.slice(7) : "";
  if (!token) return null;

  const supabase = createClient(requireEnv("SUPABASE_URL"), requireEnv("SUPABASE_ANON_KEY"), {
    auth: { persistSession: false, autoRefreshToken: false },
    global: { headers: { Authorization: `Bearer ${token}` } },
  });

  const { data, error } = await supabase.auth.getUser();
  if (error || !data?.user) return null;
  return data.user;
}

function sendJson(res, status, body) {
  res.statusCode = status;
  res.setHeader("Content-Type", "application/json");
  res.end(JSON.stringify(body));
}

module.exports = {
  requireEnv,
  getStripe,
  getPool,
  getProfileBilling,
  updateProfileBilling,
  updateProfileBillingByCustomer,
  getSiteUrl,
  getUserFromAuthHeader,
  sendJson,
};
