#!/usr/bin/env node
// Gate for the adversarial-spec-review and reviewing-documents skills. Active only while
// .review-state/<session_id>/active.json exists (walked up from the session cwd).
// Exit 2 blocks the tool call / the stop; stderr is shown to Claude.
import { existsSync, readFileSync, realpathSync } from "node:fs";
import { dirname, join, resolve, basename } from "node:path";
import { execFileSync } from "node:child_process";

let input;
try {
  input = JSON.parse(readFileSync(0, "utf8") || "{}");
} catch {
  process.exit(0); // not a hook payload; nothing to gate
}
const cwd = input.cwd || process.cwd();

// Review state is per session: .review-state/<session_id>/{active.json,brief.md,round-N/...}.
// The hook only ever looks at the folder named by its own session_id, so one session's review is
// invisible to every other session, and reviews can run side by side. A legacy top-level
// .review-state/active.json (no session folder) gates nobody. Hooks never write state.
const sid = typeof input.session_id === "string" && /^[A-Za-z0-9_-]+$/.test(input.session_id) ? input.session_id : "";
if (!sid || input.hook_event_name === "PostToolUse") process.exit(0);

function real(p) {
  try { return realpathSync(p); } catch { return p; }
}

function findRoot(dir) {
  let checkoutRoot;
  try {
    checkoutRoot = execFileSync("git", ["rev-parse", "--show-toplevel"], {
      cwd: dir, encoding: "utf8", stdio: "pipe",
    }).trim();
  } catch {
    // Outside Git, retain the walk to the filesystem root.
  }
  for (let d = resolve(dir); ; d = dirname(d)) {
    if (existsSync(join(d, ".review-state", sid, "active.json"))) return d;
    if (real(d) === checkoutRoot || dirname(d) === d) return null;
  }
}

const root = findRoot(cwd);
if (!root) process.exit(0);
const SD = join(root, ".review-state", sid);
const SDN = `.review-state/${sid}`;

// A broken state file blocks everything except the calls that repair or remove it.
function badState(msg) {
  const t = input.tool_input || {};
  const target = `${t.file_path || ""} ${t.command || ""}`;
  if (input.hook_event_name === "Stop" || target.includes(".review-state")) process.exit(0);
  block(`${msg} Fix it, or delete ${SDN}/active.json to end the review.`);
}

let state;
try {
  state = JSON.parse(readFileSync(join(SD, "active.json"), "utf8"));
} catch {
  badState(`${SDN}/active.json is not valid JSON.`);
}
if (typeof state?.spec !== "string" || !Number.isInteger(state?.round)) {
  badState(`${SDN}/active.json must be {"spec": "<path>", "round": <integer>}.`);
}

const roundDir = join(SD, `round-${state.round}`);
const specPath = real(resolve(root, state.spec));
if (!existsSync(specPath)) badState(`${SDN}/active.json names a spec that doesn't exist: ${specPath}. Use the spec's absolute path.`);
const has = (f) => existsSync(join(roundDir, f));
const ABORT = ` (To abandon the review, or if this state is stale, delete ${SDN}/active.json.)`;
// Agents allowed before the team OK: read-only helpers, never reviewers.
const HELPER_AGENTS = new Set(["Explore", "Plan", "claude-code-guide", "web-fetch"]);

function block(msg) {
  process.stderr.write(`[review-gate] ${msg}\n`);
  process.exit(2);
}

function need(files, step) {
  const missing = files.filter((f) => !has(f));
  if (missing.length) {
    block(`Step ${step} not done for round ${state.round}: missing ${missing.map((f) => `${SDN}/round-${state.round}/${f}`).join(", ")}. Read the step file, do the step, then write the gate file.${ABORT}`);
  }
}

function verificationValid() {
  if (!has("8b-verification.md")) return false;
  const text = readFileSync(join(roundDir, "8b-verification.md"), "utf8");
  return ["## Pass 1", "## Pass 2", "## Pass 3"].every((h) => text.includes(h));
}

function needVerification(what) {
  if (!verificationValid()) {
    block(`Step 8b not done for round ${state.round}: ${what} needs ${SDN}/round-${state.round}/8b-verification.md with "## Pass 1", "## Pass 2" and "## Pass 3". Read steps/08b-verify.md and run all three passes.${ABORT}`);
  }
}

function specDirty() {
  try {
    const out = execFileSync("git", ["status", "--porcelain", "--", specPath], { cwd: dirname(specPath), encoding: "utf8" });
    return out.trim().length > 0;
  } catch {
    return false;
  }
}

const event = input.hook_event_name;
const tool = input.tool_name;
const ti = input.tool_input || {};

if (event === "Stop") {
  // To ask the user something before 8b is done, use AskUserQuestion instead of ending the turn.
  if (has("8a-impact-trace.md")) needVerification("ending the turn after spec edits (to ask the user mid-step, use AskUserQuestion)");
  process.exit(0);
}

if (event !== "PreToolUse") process.exit(0);

if (tool === "Agent" || tool === "Task") {
  if (!HELPER_AGENTS.has(ti.subagent_type)) need(["0-checklist.md", "2-team-ok.md"], "0/2");
} else if (tool === "Edit" || tool === "Write" || tool === "MultiEdit") {
  if (ti.file_path && real(resolve(cwd, ti.file_path)) === specPath) {
    need(["7-approved.md", "8a-impact-trace.md"], "7/8a");
  }
} else if (tool === "Bash") {
  // A Codex job is a reviewer seat (Codex engine), gated like an Agent spawn; setup/status/result/cancel are not.
  if (/codex-companion\.mjs["']?\s+(task|review|adversarial-review)\b/.test(String(ti.command || ""))) need(["0-checklist.md", "2-team-ok.md"], "0/2");
  // Heredoc bodies are data (e.g. a gate file that mentions the spec), not commands.
  const cmd = String(ti.command || "").replace(/<<-?\s*["']?(\w+)["']?[^\n]*\n[\s\S]*?\n\s*\1\s*(?=\n|$)/g, (m) => m.split("\n")[0]);
  // Paths in the command that resolve to the spec (basename alone is not enough),
  // except after a cd/pushd in the same command, where a bare basename fails closed.
  const names = cmd.split(/[\s"'=<>|;&()]+/).filter((t) => t && basename(t) === basename(specPath));
  const changesDir = /(^|[;&|(]\s*)(cd|pushd)\s/.test(cmd);
  const isSpec = (t) => real(resolve(cwd, t)) === specPath || (changesDir && !t.includes("/"));
  const namesSpec = names.some(isSpec);
  // A redirect whose target is the spec, or a writing tool in a command that names it (fails closed).
  const redirectsIntoSpec = [...cmd.matchAll(/>{1,2}\s*["']?([^\s"';&|<>]+)/g)].some((m) => isSpec(m[1]));
  const writer = /(\b(sed|perl)\b.*\s(-[a-zA-Z]*i|--in-place)|\bcp\b|\bmv\b|\bpython3?\b|\bnode\b|\btee\b|\btruncate\b|\bdd\b)/.test(cmd);
  if (redirectsIntoSpec || (namesSpec && writer)) need(["7-approved.md", "8a-impact-trace.md"], "7/8a");
  // Strip quoted data, but preserve shell -c arguments and double-quoted substitutions.
  // Keep a token for options like -C "dir with space".
  const commitCmd = cmd.replace(/"(?:\\.|[^"\\])*"|'[^']*'/g, (quoted, offset) => {
    if (/(?:^|\s)-[a-zA-Z]*c\s+$/.test(cmd.slice(0, offset)) ||
        (quoted.startsWith('"') && /\$\(|`/.test(quoted))) {
      // Expose command boundaries to the commit matcher, including backticks.
      return quoted.slice(1, -1).replace(/`/g, " ");
    }
    return "Q";
  });
  if (/(?:^|[;&|(]\s*|\s)git(?:\s+(?:-[Cc]\s+\S+|--[\w-]+(?:=\S+)?))*\s+commit(?![-\w])/.test(commitCmd) && specDirty()) {
    needVerification("committing the spec");
  }
}

process.exit(0);
