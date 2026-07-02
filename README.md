# EnglishPath — an English learning website

An educational platform with lessons by level (A1, A2, B1, B1+, B2), exercises with
instant checking, a paid subscription ($5/month via Stripe), and an admin panel for
creating lessons without programming.

**Stack (as simple as possible):** HTML + Tailwind CSS (via CDN) + plain JavaScript.
Backend — Supabase. Payments — Stripe. Hosting — Vercel/Netlify.

> The whole site is in English: it targets an international (non-Russian) audience.

## Monetization model (decided): soft freemium

- Almost all lessons are **free** and supported by ads (Google AdSense).
- **Premium ($5/month)** is an optional upsell, not a content wall. Premium gives:
  - an ad-free experience,
  - downloadable PDF worksheets,
  - exam practice materials,
  - progress tracking.
- The home page leads with **learning**, not with the price. Premium is offered
  discreetly (like test-english.com), so we don't scare away new visitors and we keep
  the large free traffic that AdSense and SEO depend on.

---

## How to open the site (preview)

The easiest way: **double-click `index.html`** — it opens in your browser.

Everything works with no installation because we use CDNs (Tailwind, fonts)
and regular `<script>` files.

> Later, when we add Supabase and Stripe, you'll need to run a local server.
> That is not needed at this stage.

---

## Project structure

```
Test english site/
├── index.html        ← Home page (done in Step 1)
├── level.html        ← Level page with sections (done in Step 1)
├── css/
│   └── styles.css    ← Extra styles
├── js/
│   ├── data.js       ← Levels and sections (edit content here)
│   ├── main.js       ← Home page logic
│   └── level.js      ← Level page logic
└── README.md         ← This file
```

---

## Project roadmap

- [x] **Step 1.** Base structure: home page + navigation by levels and sections, responsive design.
- [x] **Step 2.** Sign up and log in (Supabase) + email confirmation + password reset + logout.
- [x] **Step 3.** Lessons and exercises database + security (RLS).
- [x] **Step 4.** Displaying lessons and exercises with instant checking (`section.html`, `lesson.html`).
- [x] **Step 5.** Admin panel (`admin.html`) — lesson builder with rich text editor, exercises, publish/draft, preview, delete.
- [ ] Step 6. Free vs premium lessons.
- [ ] Step 7. Subscription via Stripe.
- [ ] Step 8. User progress and account page.
- [ ] Step 9. Legal pages, cookie banner, AdSense, SEO.
- [ ] Step 10. Deploy to Vercel/Netlify.

---

## What to check in Step 1

1. Open `index.html` in your browser.
2. You should see: a header with a menu, a hero banner with a sign-up call to action,
   cards for 5 levels, 6 sections, and a subscription pricing block.
3. Click "Levels" in the header — a dropdown opens. Pick any level — the `level.html`
   page opens with that level's sections.
4. Make the browser window narrow (or open it on a phone) — a burger button appears
   instead of the menu.

> The "Log in", "Sign up" and section links currently point to pages we'll build in
> later steps — that's expected.

---

## Step 2 setup — Supabase (auth)

1. Open `js/config.js` and paste your two values from
   Supabase → Project Settings → API:
   - `SUPABASE_URL` = Project URL
   - `SUPABASE_ANON_KEY` = anon public key
2. New auth pages: `register.html`, `login.html`, `forgot-password.html`,
   `update-password.html`. The header now shows the logged-in user + a Log out button.
3. In Supabase → Authentication → URL Configuration, add your site address to
   "Redirect URLs" (for local testing with a server, e.g. `http://localhost:5500/*`;
   for production, your deployed domain). Set "Site URL" to the same address.
4. Quick local test without a server: in Supabase → Authentication → Providers → Email,
   you can temporarily turn OFF "Confirm email" so sign-up logs you in right away.
   Turn it back ON before going live.

## What to check in Step 4

1. Open `index.html` → click **A1** → **Grammar** → you should see the demo lesson
   *Present Simple: he / she / it*.
2. Click **Start** → read the explanation → answer the two questions → **Check my answers**.
3. Correct answers turn green, wrong ones red, with explanations. Score shows at the bottom.
4. If you are logged in, your result is saved to the database automatically.

## What to check in Step 5 (Admin panel)

1. Log in with your admin account (`art.tatan@gmail.com`).
2. On any page you should see an **Admin** link in the header (amber colour).
3. Open **`admin.html`** — you should see the lesson list on the left.
4. Click the existing demo lesson to edit it, or **+ New lesson** to create one.
5. Use the toolbar to format the explanation, add exercises, then **Save & publish**.
6. Click **Preview** to open the lesson on the public site in a new tab.

Only accounts with `is_admin = true` in the `profiles` table can access the admin panel.

## How to change the site name

Open `js/data.js` and change this line:

```js
brand: "EnglishPath",
```

The name updates on all pages automatically.
