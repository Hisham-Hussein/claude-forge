import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdirSync, mkdtempSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
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

function activate(root, spec) {
  mkdirSync(join(root, ".review-state"), { recursive: true });
  writeFileSync(join(root, ".review-state", "active.json"), JSON.stringify({ spec, round: 1 }));
}

function check(cwd, command, status, message = /Step 8b not done/) {
  const result = spawnSync(process.execPath, [hookPath], {
    cwd, env, encoding: "utf8",
    input: JSON.stringify({
      tool_name: "Bash", tool_input: { command }, cwd, hook_event_name: "PreToolUse",
    }),
  });
  assert.ifError(result.error);
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
