/**
 * QA unit tests for ExerciseEngine (run: node tests/qa-exercise-engine.mjs)
 */
import { readFileSync } from "fs";
import { JSDOM } from "jsdom";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");

const dom = new JSDOM("<!DOCTYPE html><html><body></body></html>", { runScripts: "dangerously" });
const { window } = dom;
const document = window.document;
global.window = window;
global.document = document;
eval(readFileSync(join(root, "js/exercise-engine.js"), "utf8"));
const EE = window.ExerciseEngine;

let passed = 0;
let failed = 0;

function assert(cond, msg) {
  if (cond) {
    passed++;
  } else {
    failed++;
    console.error("FAIL:", msg);
  }
}

function makeStack(options, selectedIndex) {
  const parts = EE.parseInlineText(`Test [*a|b|c] here.`);
  const html = EE.renderLettered(parts, "t0");
  document.body.innerHTML = html;
  const stack = document.querySelector(".te-options-stack");
  if (selectedIndex != null) {
    const inp = stack.querySelector(`input[value="${selectedIndex}"]`);
    inp.checked = true;
    inp.dispatchEvent(new window.Event("change", { bubbles: true }));
  }
  return stack;
}

// --- Parser tests ---
const inline = EE.parseInlineText("I [*don't drink|not drink] tea.");
assert(inline.length === 3, "inline parts count");
assert(inline[1].type === "choice" && inline[1].correct === 0, "inline correct index");

const gap = EE.parseLetteredGap("After I ____. | *have breakfast | go shopping");
assert(gap.sentence.includes("____"), "lettered gap sentence");
assert(gap.correct === 0 && gap.options[0] === "have breakfast", "lettered gap correct");

const dd = EE.parseDropdownText("After I ___ in the morning. | get up");
assert(dd.answers[0] === "get up" && dd.blankCount === 1, "dropdown parse");

// --- Lettered check ---
let stack = makeStack([], 0);
assert(EE.checkLetteredStack(stack, 0) === true, "lettered correct answer");

stack = makeStack([], 1);
assert(EE.checkLetteredStack(stack, 0) === false, "lettered wrong answer");

stack = makeStack([], null);
assert(EE.checkLetteredStack(stack, 0) === false, "lettered no selection");

// --- Dropdown check ---
document.body.innerHTML = EE.renderDropdown("After I ___ today.", "d0", ["get up", "go to bed"]);
const body = document.querySelector(".te-question-body") || document.body;
const container = document.createElement("div");
container.innerHTML = EE.renderDropdown("After I ___ today.", "d0", ["get up", "go to bed"]);
document.body.innerHTML = container.innerHTML;
const wrap = document.body;
wrap.querySelector("select").value = "get up";
const used = new Set();
assert(EE.checkDropdown(wrap, ["get up"], true, used) === true, "dropdown correct");
assert(used.has("get up"), "use_once tracks word");

document.body.innerHTML = EE.renderDropdown("Sam ___ early.", "d1", ["get up", "starts work"]);
const wrap2 = document.body;
wrap2.querySelector("select").value = "get up";
const used2 = new Set();
used2.add("get up");
assert(EE.checkDropdown(wrap2, ["starts work"], true, used2) === false, "use_once rejects duplicate word");

// --- HTML escape ---
assert(EE.escapeHtml('<script>') === "&lt;script&gt;", "escape html");

console.log(`\nResults: ${passed} passed, ${failed} failed`);
process.exit(failed > 0 ? 1 : 0);
