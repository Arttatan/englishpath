/**
 * Marks that project source was edited so the stop hook can trigger QA.
 * Skips edits under .cursor/ (except we never mark for .cursor paths).
 */
const fs = require("fs");
const path = require("path");

const root = process.cwd();
const flagPath = path.join(root, ".cursor", "qa-pending");

let input = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => (input += chunk));
process.stdin.on("end", () => {
  try {
    const data = JSON.parse(input || "{}");
    const file =
      data.file_path ||
      data.filePath ||
      data.path ||
      (data.tool_input && (data.tool_input.path || data.tool_input.file_path)) ||
      "";
    const normalized = String(file).replace(/\\/g, "/");
    if (
      !normalized ||
      normalized.includes("/.cursor/") ||
      normalized.endsWith(".cursor/qa-pending")
    ) {
      process.stdout.write("{}\n");
      return;
    }
    // Only mark for site source / content
    const relevant =
      /\.(html|js|css|json|md|sql)$/i.test(normalized) ||
      normalized.includes("/js/") ||
      normalized.includes("/css/") ||
      normalized.includes("/database/");
    if (!relevant) {
      process.stdout.write("{}\n");
      return;
    }
    fs.mkdirSync(path.dirname(flagPath), { recursive: true });
    fs.writeFileSync(
      flagPath,
      JSON.stringify({ path: normalized, at: new Date().toISOString() }) + "\n",
      "utf8"
    );
  } catch (_) {
    // fail open
  }
  process.stdout.write("{}\n");
});
