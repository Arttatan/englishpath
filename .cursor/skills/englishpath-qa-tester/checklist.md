# EnglishPath QA — page matrix

## Production

- Home: `https://englishpath-mauve.vercel.app/`
- Levels: `/level.html?level=a1` … `c1`
- Section: `/section.html?level=a1&section=grammar`
- Lesson: `/lesson.html?id=<id>`
- Auth: `/login.html`, `/register.html`, `/forgot-password.html`, `/update-password.html`, `/auth-confirm.html`
- Account: `/account.html`
- Legal: `/privacy.html`, `/terms.html`, `/contact.html`
- Admin: `/admin.html`

## Scripts that must load on public pages

- `js/config.js` + Supabase CDN where auth/data needed
- `js/data.js` where brand/levels used
- `js/cookies.js` on public-facing pages (not required on admin)

## Known fragile areas

- Supabase free email rate limits — do not load-test recover/signup
- PowerShell: `$HOME` is reserved; don’t use that variable name in QA scripts
- Lesson progress needs a logged-in user
- `auth-confirm.html` + email templates with `token_hash` for reliable recovery
