/*
  ============================================================
  SUPABASE CONFIG — PASTE YOUR TWO VALUES HERE
  ============================================================
  Where to get them:
    Supabase dashboard → Project Settings (gear icon) → API
      1) Project URL          (looks like https://abcdefgh.supabase.co)
      2) anon public API key   (long string that starts with eyJ...)

  These two values are PUBLIC and safe to use in the browser.
  Do NOT paste the "service_role" key or the database password here.
*/

const SUPABASE_URL = "https://ktijitzwdpmzshspuepp.supabase.co";        // <-- paste Project URL
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt0aWppdHp3ZHBtenNoc3B1ZXBwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI3NjczNTMsImV4cCI6MjA5ODM0MzM1M30.h2KTV4_5mYAn7E4-VQc19vsnqcsIfUMaw4S_LXiqYkw"; // <-- paste anon public key

/* ---------- Do not edit below this line ---------- */

// Create the Supabase client (the library is loaded from the CDN in each page).
// We expose it globally as window.sb so every page can use it.
window.sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Small helper: shows a friendly warning if the keys were not pasted yet.
window.SUPABASE_READY =
  SUPABASE_URL.startsWith("http") && SUPABASE_ANON_KEY.length > 20;

if (!window.SUPABASE_READY) {
  console.warn(
    "Supabase keys are not set yet. Open js/config.js and paste your Project URL and anon public key."
  );
}
