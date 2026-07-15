/**
 * On agent stop: if project files were edited, request a QA follow-up turn.
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
    if (!fs.existsSync(flagPath)) {
      process.stdout.write("{}\n");
      return;
    }
    const meta = fs.readFileSync(flagPath, "utf8").trim();
    fs.unlinkSync(flagPath);

    const followup = [
      "Expert QA follow-up (EnglishPath): project files were just edited.",
      "Read and follow .cursor/skills/englishpath-qa-tester/SKILL.md.",
      "Focus on the latest changes; catch bugs; fix safe ones;",
      "end with the mandatory QA Report (bugs found + fixed).",
      "Edited hint: " + meta,
    ].join(" ");

    process.stdout.write(
      JSON.stringify({ followup_message: followup }) + "\n"
    );
  } catch (_) {
    process.stdout.write("{}\n");
  }
});
