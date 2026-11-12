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

function activate(root, spec, sid = OWNER) {
  const dir = join(root, ".review-state", sid);
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, "active.json"), JSON.stringify({ spec, round: 1 }));
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

test("review state is per session", async (t) => {
  const temp = mkdtempSync(join(tmpdir(), "review-gate-sessions-"));
  t.after(() => rmSync(temp, { recursive: true, force: true }));
  const repo = join(temp, "repo");
  mkdirSync(repo);
  git(repo, "init");
  writeFileSync(join(repo, "spec.md"), "Original\n");
  writeFileSync(join(repo, "spec-b.md"), "Original B\n");
  git(repo, "add", ".");
  git(repo, "commit", "-m", "specs");
  writeFileSync(join(repo, "spec.md"), "Changed\n");
  writeFileSync(join(repo, "spec-b.md"), "Changed B\n");
  const pre = (session, tool_name, tool_input, event = "PreToolUse") =>
    run(repo, { session_id: session, tool_name, tool_input, hook_event_name: event });
  const reviewer = { subagent_type: "general-purpose", prompt: "review" };
  const edit = (f) => ({ file_path: join(repo, f) });
  const gate = (sid, file, content = "x") => {
    mkdirSync(join(repo, ".review-state", sid, "round-1"), { recursive: true });
    writeFileSync(join(repo, ".review-state", sid, "round-1", file), content);
  };
  const tree = () => spawnSync("find", [join(repo, ".review-state"), "-type", "f", "-exec", "md5sum", "{}", "+"], { encoding: "utf8" }).stdout;
  activate(repo, join(repo, "spec.md"), OWNER);

  await t.test("A is gated at Step 0/2, 7/8a, 8b commit and Stop", () => {
    const r = pre(OWNER, "Agent", reviewer);
    assert.equal(r.status, 2);
    assert.match(r.stderr, /Step 0\/2 not done/);
    assert.match(r.stderr, /\.review-state\/session-owner\/round-1\/0-checklist\.md/);
    assert.equal(pre(OWNER, "Edit", edit("spec.md")).status, 2);
    assert.equal(pre(OWNER, "Bash", { command: "git commit -am x" }).status, 2);
    gate(OWNER, "8a-impact-trace.md");
    assert.equal(pre(OWNER, undefined, {}, "Stop").status, 2);
  });
  await t.test("A may spawn web-fetch before the team OK", () => {
    assert.equal(pre(OWNER, "Agent", { subagent_type: "web-fetch", prompt: "x" }).status, 0);
  });
  await t.test("B is never gated by A's review", () => {
    for (const [tool, input, event] of [
      ["Agent", reviewer], ["Edit", edit("spec.md")], ["Bash", { command: "git commit -am x" }],
      ["Bash", { command: "echo hi > spec.md" }], [undefined, {}, "Stop"],
    ]) {
      const r = pre(OTHER, tool, input, event);
      assert.equal(r.status, 0, `${tool} ${r.stderr}`);
      assert.equal(r.stderr, "");
    }
  });
  await t.test("B's own review runs side by side with its own gates", () => {
    activate(repo, join(repo, "spec-b.md"), OTHER);
    const r = pre(OTHER, "Agent", reviewer);
    assert.equal(r.status, 2);
    assert.match(r.stderr, /session-other\/round-1\/0-checklist\.md/);
    // A's gate files do not satisfy B, and B's do not satisfy A.
    gate(OWNER, "0-checklist.md"); gate(OWNER, "2-team-ok.md");
    assert.equal(pre(OWNER, "Agent", reviewer).status, 0);
    assert.equal(pre(OTHER, "Agent", reviewer).status, 2);
    // Each session's gate is about its own spec.
    assert.equal(pre(OTHER, "Edit", edit("spec-b.md")).status, 2);
    assert.equal(pre(OTHER, "Edit", edit("spec.md")).status, 0);
    assert.equal(pre(OWNER, "Edit", edit("spec-b.md")).status, 0);
    assert.equal(pre(OWNER, "Edit", edit("spec.md")).status, 2);
  });
  await t.test("read-only commands on .review-state change nothing for anyone", () => {
    const before = tree();
    for (const command of ["ls .review-state", "cat .review-state/session-owner/active.json", `ls ${repo}/.review-state/session-other`]) {
      for (const event of ["PreToolUse", "PostToolUse"]) {
        assert.equal(pre("session-onlooker", "Bash", { command }, event).status, 0);
        assert.equal(pre(OTHER, "Bash", { command }, event).status, 0);
      }
    }
    assert.equal(tree(), before);
    assert.equal(pre(OWNER, "Agent", reviewer).status, 0);
    assert.equal(pre("session-onlooker", "Edit", edit("spec.md")).status, 0);
    assert.equal(pre(OTHER, "Agent", reviewer).status, 2);
  });
  await t.test("a broken state file gates only its own session", () => {
    writeFileSync(join(repo, ".review-state", OWNER, "active.json"), "{nope");
    assert.equal(pre(OWNER, "Agent", reviewer).status, 2);
    assert.equal(pre(OTHER, "Edit", edit("spec.md")).status, 0);
    assert.equal(pre(OWNER, "Bash", { command: "rm .review-state/session-owner/active.json" }).status, 0);
    activate(repo, join(repo, "spec.md"), OWNER);
  });
  await t.test("legacy top-level state (with or without an owner file) blocks nobody", () => {
    const legacy = join(temp, "legacy");
    mkdirSync(join(legacy, ".review-state"), { recursive: true });
    git(legacy, "init");
    writeFileSync(join(legacy, "spec.md"), "x\n");
    writeFileSync(join(legacy, ".review-state", "active.json"), JSON.stringify({ spec: join(legacy, "spec.md"), round: 1 }));
    for (const withOwner of [false, true]) {
      if (withOwner) writeFileSync(join(legacy, ".review-state", "owner"), OWNER);
      for (const s of [OWNER, OTHER]) {
        for (const [tool, input] of [["Agent", reviewer], ["Edit", { file_path: join(legacy, "spec.md") }]]) {
          assert.equal(run(legacy, { session_id: s, tool_name: tool, tool_input: input, hook_event_name: "PreToolUse" }).status, 0);
        }
        assert.equal(run(legacy, { session_id: s, hook_event_name: "Stop" }).status, 0);
      }
    }
  });
  await t.test("a payload without a session id, or with an unsafe one, gates nobody", () => {
    for (const s of [undefined, "", "../session-owner", "a/b"]) {
      const r = run(repo, { session_id: s, tool_name: "Agent", tool_input: reviewer, hook_event_name: "PreToolUse" });
      assert.equal(r.status, 0);
    }
  });
  await t.test("cleanup of A's folder leaves B's intact and ends A's gates", () => {
    rmSync(join(repo, ".review-state", OWNER), { recursive: true });
    assert.equal(pre(OWNER, "Agent", reviewer).status, 0);
    assert.equal(existsSync(join(repo, ".review-state", OTHER, "active.json")), true);
    assert.equal(pre(OTHER, "Agent", reviewer).status, 2);
  });
});
