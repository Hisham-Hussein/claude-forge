import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";

const hookPath = fileURLToPath(new URL("./review-gate.mjs", import.meta.url));
// Ignore inherited Git configuration and repository overrides in every child.
const env = Object.fromEntries(Object.entries(process.env).filter(([key]) => !key.startsWith("GIT_")));
Object.assign(env, {
  GIT_CONFIG_GLOBAL: "/dev/null",
  GIT_CONFIG_SYSTEM: "/dev/null",
  GIT_CONFIG_NOSYSTEM: "1",
  GIT_TERMINAL_PROMPT: "0",
});

function git(cwd, ...args) {
  const result = spawnSync("git", [
    "-c", "user.name=Review Gate Test",
    "-c", "user.email=review-gate@example.invalid",
    "-c", "core.hooksPath=/dev/null",
    "-c", "commit.gpgSign=false",
    ...args,
  ], { cwd, env, encoding: "utf8" });
  assert.ifError(result.error);
  assert.equal(result.status, 0, `git ${args.join(" ")}: ${result.stderr}`);
  return result.stdout;
}

const OWNER = "session-owner";
const OTHER = "session-other";

function activate(root, spec, owner = OWNER) {
  mkdirSync(join(root, ".review-state"), { recursive: true });
  writeFileSync(join(root, ".review-state", "active.json"), JSON.stringify({ spec, round: 1 }));
  if (owner) writeFileSync(join(root, ".review-state", "owner"), owner);
}

function run(cwd, payload) {
  const result = spawnSync(process.execPath, [hookPath], {
    cwd, env, encoding: "utf8", input: JSON.stringify({ cwd, session_id: OWNER, ...payload }),
  });
  assert.ifError(result.error);
  return result;
}

function check(cwd, command, status, message = /Step 8b not done/) {
  const result = run(cwd, { tool_name: "Bash", tool_input: { command }, hook_event_name: "PreToolUse" });
  assert.equal(result.status, status, `${command}\n${result.stderr}`);
  if (status === 2) assert.match(result.stderr, message);
  else assert.equal(result.stderr, "");
}

test("review gate checkout scope and commit matching", async (t) => {
  const temp = mkdtempSync(join(tmpdir(), "review-gate-"));
  t.after(() => rmSync(temp, { recursive: true, force: true }));
  const main = join(temp, "main");
  mkdirSync(main);
  git(main, "init");
  writeFileSync(join(main, "spec.md"), "Original spec\n");
  git(main, "add", "spec.md");
  git(main, "commit", "-m", "Create test spec");
  const worktree = join(main, ".worktrees", "feat", "x");
  git(main, "worktree", "add", "-b", "fixture-feature", worktree);
  writeFileSync(join(main, "spec.md"), "Changed spec\n");
  activate(main, "spec.md");
  assert.match(git(main, "status", "--porcelain", "--", "spec.md"), / M spec\.md/);

  await t.test("nested linked worktree ignores the main checkout review", () => {
    check(worktree, "git commit -m x", 0);
  });
  await t.test("symlinked nested worktree ignores the main checkout review", () => {
    const linkedWorktree = join(main, "linked-worktree");
    symlinkSync(worktree, linkedWorktree, "dir");
    check(linkedWorktree, "git commit -m x", 0);
  });
  await t.test("walk includes the main checkout root", () => {
    const subdir = join(main, "subdir");
    mkdirSync(subdir);
    check(subdir, "git commit -m x", 2);
  });
  await t.test("worktree subdirectories also ignore the main checkout review", () => {
    const subdir = join(worktree, "subdir");
    mkdirSync(subdir);
    check(subdir, "git commit -m x", 0);
  });

  for (const command of [
    'echo "run git commit later" >> notes.txt',
    "echo 'run git commit later' >> notes.txt",
    "echo '$(git commit -m x)' >> notes.txt",
    "echo '`git commit -m x`' >> notes.txt",
    'echo "say \\"git commit later\\"" >> notes.txt',
    "cat <<'EOF' >> notes.txt\nrun git commit later\nEOF",
  ]) {
    await t.test(`allows command data: ${JSON.stringify(command)}`, () => check(main, command, 0));
  }
  for (const command of [
    "git commit -m x",
    'git commit -m "x"',
    "git -C dir commit -m x",
    'git -C "dir with space" commit -m x',
    "cd x && git commit -m y",
    "git add a; git commit -m y",
    'bash -c "git commit -m x"',
    "sh -c 'git commit -m x'",
    'bash -lc "git commit -m x"',
    "sh -ec 'git commit -m x'",
    'echo "$(git commit -m x)"',
    'echo "`git commit -m x`"',
  ]) {
    await t.test(`blocks actual commit: ${command}`, () => check(main, command, 2));
  }
  await t.test("quoted spec paths still trigger the spec edit gate", () => {
    check(main, 'echo changed > "spec.md"', 2, /Step 7\/8a not done/);
  });
  await t.test("non-git cwd still discovers review state above it", () => {
    const nonGit = join(temp, "non-git");
    const subdir = join(nonGit, "child");
    mkdirSync(subdir, { recursive: true });
    // The spec remains in a repository so specDirty() can detect its edits.
    activate(nonGit, join(main, "spec.md"));
    check(subdir, "git commit -m x", 2);
  });
});

test("review gate is scoped to the owning session", async (t) => {
  const temp = mkdtempSync(join(tmpdir(), "review-gate-owner-"));
  t.after(() => rmSync(temp, { recursive: true, force: true }));
  const repo = join(temp, "repo");
  mkdirSync(repo);
  git(repo, "init");
  writeFileSync(join(repo, "spec.md"), "Original\n");
  git(repo, "add", "spec.md");
  git(repo, "commit", "-m", "spec");
  writeFileSync(join(repo, "spec.md"), "Changed\n");
  activate(repo, join(repo, "spec.md"));
  const owned = () => readFileSync(join(repo, ".review-state", "owner"), "utf8");
  const pre = (session, tool_name, tool_input, event = "PreToolUse") =>
    run(repo, { session_id: session, tool_name, tool_input, hook_event_name: event });
  const reviewer = { subagent_type: "general-purpose", prompt: "review" };
  const edit = { file_path: join(repo, "spec.md") };

  await t.test("owner is blocked at Step 0/2 for a reviewer agent", () => {
    const r = pre(OWNER, "Agent", reviewer);
    assert.equal(r.status, 2);
    assert.match(r.stderr, /Step 0\/2 not done/);
  });
  await t.test("owner is blocked editing the spec, committing and stopping", () => {
    assert.equal(pre(OWNER, "Edit", edit).status, 2);
    assert.equal(pre(OWNER, "Bash", { command: "git commit -am x" }).status, 2);
  });
  await t.test("owner may spawn web-fetch before the team OK", () => {
    assert.equal(pre(OWNER, "Agent", { subagent_type: "web-fetch", prompt: "x" }).status, 0);
  });
  await t.test("another session is not blocked for agent, edit, commit or stop", () => {
    for (const [tool, input, event] of [
      ["Agent", reviewer], ["Edit", edit], ["Bash", { command: "git commit -am x" }],
      ["Bash", { command: "echo hi > spec.md" }], [undefined, {}, "Stop"],
    ]) {
      const r = pre(OTHER, tool, input, event);
      assert.equal(r.status, 0, `${tool} ${r.stderr}`);
      assert.equal(r.stderr, "");
    }
  });
  await t.test("another session is not blocked by a broken state file", () => {
    writeFileSync(join(repo, ".review-state", "active.json"), "{nope");
    assert.equal(pre(OTHER, "Agent", reviewer).status, 0);
    assert.equal(pre(OWNER, "Agent", reviewer).status, 2);
    activate(repo, join(repo, "spec.md"));
  });
  await t.test("legacy state without an owner blocks nobody", () => {
    rmSync(join(repo, ".review-state", "owner"));
    for (const s of [OWNER, OTHER]) {
      assert.equal(pre(s, "Agent", reviewer).status, 0);
      assert.equal(pre(s, "Edit", edit).status, 0);
    }
  });
  await t.test("PostToolUse on a Write under .review-state claims ownership", () => {
    const r = pre(OTHER, "Write", { file_path: join(repo, ".review-state", "round-1", "0-checklist.md") }, "PostToolUse");
    assert.equal(r.status, 0);
    assert.equal(owned(), OTHER);
    assert.equal(pre(OTHER, "Agent", reviewer).status, 2);
    assert.equal(pre(OWNER, "Agent", reviewer).status, 0);
  });
  await t.test("PostToolUse on a Bash command mentioning .review-state hands ownership over", () => {
    pre(OWNER, "Bash", { command: "ls .review-state/round-1" }, "PostToolUse");
    assert.equal(owned(), OWNER);
  });
  await t.test("PostToolUse on unrelated calls changes nothing", () => {
    pre(OTHER, "Bash", { command: "ls" }, "PostToolUse");
    pre(OTHER, "Write", { file_path: join(repo, "x.md") }, "PostToolUse");
    assert.equal(owned(), OWNER);
  });
  await t.test("deleting the review folder leaves no owner file behind", () => {
    rmSync(join(repo, ".review-state"), { recursive: true });
    pre(OWNER, "Bash", { command: "rm -rf .review-state" }, "PostToolUse");
    assert.equal(existsSync(join(repo, ".review-state")), false);
  });
});
