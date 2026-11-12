---
name: reviewing-documents
description: Runs an independent reviewer loop on any written document that isn't running code (a design, plan, requirements or experience document, proposal, runbook, policy) and fixes it round by round until it is ready for whoever uses it next. Use whenever the user asks to review, check, stress-test or harden a document, says "review this doc", "Mode D", "Independent Reviewer Loop", or "is this ready", even if they don't say "adversarial". Not for reviewing code, a diff or a pull request (tests and code review do that), and not for a multi-reviewer team review (reviewing-specs-adversarially Modes A-C, reviewing-plans-adversarially Modes A-C). For Mode D on an implementation plan, use reviewing-plans-adversarially, which runs this skill with its plan profile.
allowed-tools: Read, Glob, Grep, Agent, TaskCreate, TaskUpdate, TaskList, TaskGet, AskUserQuestion, Edit, Write, Bash
---

# Reviewing Documents

One fresh independent reviewer per round reads the document. The orchestrator judges every finding against evidence, fixes what is worth fixing without asking, and starts the next round. The loop stops at the first round where nothing is judged Critical or Major; that round's worthwhile Minors are fixed and no further round runs.

The skill knows nothing about document types. What the document is, who it serves and what "ready" means are worked out from the document itself in the review brief (R1), and everything later reads from that brief.

**A profile.** Another skill may invoke this one with a profile for its kind of document: brief lines, extra R3 checks, a fix limit. A profile's lines go into the brief as given, its checks join R3, and its fix limit replaces the one below. Everything else runs as written here. If you are asked for this review on an implementation plan and no profile came with the request, stop and invoke `reviewing-plans-adversarially` with the user's words, naming Mode D.

**One document.** The review edits only the document it was given. Other documents it affects are reported, never edited, because editing whatever a search finds turns one review into an uncontrolled change across the repo.

**A review repairs a document; it does not extend it.** A fix may only correct, simplify or remove text, or fill a gap with one short statement. Anything that needs new procedure, new design or a change of goal is not written in: it goes under "Decisions for the owner" in the final report, and that finding doesn't count toward another round. Without this limit each fresh reviewer finds problems in the last round's new text, and the document grows instead of settling.

**Running the skill is the approval** for every round's fixes and every new round of this review. It does not carry over to another review.

Post this checklist first and re-post it ticked as you go:

```
Review Progress:
- [ ] R0: Set up the gate state
- [ ] R1: Read the document, write and post the review brief
- [ ] R2: Find related documents, ask the start question
- [ ] R3: Mechanical checks before round 1
- [ ] R4: Spawn a fresh reviewer for round N
- [ ] R5: Judge every finding against the evidence (spike where nothing settles it)
- [ ] R6: Fix with the impact trace and the three verification passes
- [ ] R7: Re-run the mechanical checks, commit, report the round
- [ ] R8: Stop rule: next round, or the final Minor pass
- [ ] R9: Impact appendix (if asked for), clean up, final report
```

## R0: Gate files

A hook blocks reviewers, document edits, commits and ending the turn until the matching file exists in your own session folder `S` = `.review-state/${CLAUDE_SESSION_ID}/` in the working directory (the id is filled in when this skill loads; if you see a literal `${CLAUDE_SESSION_ID}`, stop and tell the user). The hook looks only at `S`: another session's review never gates you, and you never touch another session's folder. Below, `<S>` means `S`. It checks that the file exists, not its quality, so do the step and then write its file. Its messages use step numbers from `reviewing-specs-adversarially`: Step 0/2 is R4's gate files, 7/8a is R5 and R6's trace, 8b is R6's verification.

- If `<S>/active.json` already exists, tell the user which document and round it names and ask before replacing it.
- A top-level `.review-state/active.json` (no session folder) is legacy state from an older plugin version and gates nobody. If the user says this review continues it, move it with `mkdir -p <S> && mv .review-state/active.json .review-state/brief.md .review-state/round-* <S>/` (skip names that don't exist) and `rm -f .review-state/owner`; otherwise leave it alone.
- Delete any old `<S>/round-*` folders, because old gate files would satisfy this review's gates.
- Create `<S>/active.json` with the Write tool: `{"spec": "<absolute document path>", "round": 1}`. The key is `spec` for every document; the hook reads that name.
- Append `.review-state/` to the file `git rev-parse --git-path info/exclude` prints.

## R1: Review brief

Read the whole document, then write `<S>/brief.md` and post it to the user. Do not wait for an answer; the user corrects it if it is off, and a correction applies from that point on.

```
Document: <path>, and what it is in one line
Next readers: who uses it next, and what they do with it
Ready means: what those readers must be able to do from this document alone
In scope: what this document is responsible for deciding or saying
Left out on purpose: what it leaves to someone else, each item quoted from this document or the next stage's own text
Severity standard: the project's own definition, quoted, if it states one; otherwise references/judging.md
Evidence: the files, code, data, research and sources its claims can be checked against
Riskiest areas: the 3 places a mistake would cost most
Review focus: the questions a profile gave the reviewer to answer; "none" without a profile
History: what in this repo is a record of the past, and is never changed (archives, spikes, logs, finished work), judged from this repo's layout
```

Take every answer from the document, what cites it, the user's words and any profile. The brief drives everything after it, so a vague "Ready means" gives a vague review: write it as something the next reader does. An item with no text to quote stays in scope, because "Left out on purpose" tells the reviewer not to look there.

## R2: Related documents and the start question

List the documents related to this one:
- documents this one cites, and documents that cite it (search for its file name);
- documents using the IDs or defined names this document owns.

Search written documents only, skip what the brief marks as history, and stop at this one hop.

Then ask the one question of the run with AskUserQuestion, showing the list: "Do you want an impact report on these documents at the end? It is added as an appendix to this document; they are not edited." If the document has uncommitted changes, ask in the same call whether to commit them first, because R7 commits it each round. If the list is empty and the document has no impact appendix, record `Impact report: no` and skip that part of the question. If another agent is running this skill, there is no one to ask: use its instructions, or `Impact report: no`.

Record the answer as `Impact report: yes|no` and the list under `Related:` in `brief.md`. Ask nothing else for the rest of the run, unless a blocker leaves no way to continue.

The reviewer engine is Claude unless the user named Codex.

## R3: Mechanical checks before round 1

Check what a script can check, so the reviewer's rounds go to judgment:
- If the project requires a checklist or appendix in this kind of document, it is filled and has no gaps.
- Write a check script in the scratchpad, or reuse the project's if it keeps one. It checks: cross-references point at sections that exist; numbered lists run in order; cited files and `file:line` exist; every defined name, ID, setting and code is declared once and used consistently; IDs trace to their source; every list that must be complete matches its source. It reads the document path from `<S>/active.json` and never writes the document: the gate treats a `python` or `node` command that names the document as an edit.
- If the checks need edits, do them as round 0: set `round` to 0 in `active.json`, write `round-0/7-approved.md` (the user's request to run this review, and the check findings), do R6 and R7 for them, then set `round` to 1.

## R4: Spawn a fresh reviewer for round N

- Gate files: `round-N/0-checklist.md` (the checklist as posted) and `round-N/2-team-ok.md` (quote the request that started this review; the same quote stands for every round).
- Prompt: `templates/reviewer-prompt.md`, every field filled from the brief. Round 2+ also reviews the whole document fresh.
- A new reviewer every round, never a previous round's reviewer: a fresh reader is the point of the loop.
- **Claude:** one Agent call, `model: opus`, `effort: high` (Opus 5.5 at high effort, the default for every Mode D reviewer, spec and plan reviews included). Use another model or effort if the user names one.
- **Codex:** one read-only job, from the directory that holds `.review-state/`. Write the prompt to `<S>/round-N/codex/solo-prompt.md`, then run in the background:
  ```
  CX=$(ls -d ~/.claude/plugins/cache/openai-codex/codex/*/ | sort -V | tail -1) && \
  node "$CX"scripts/codex-companion.mjs task --model gpt-6.1-sol --effort high \
    --prompt-file <S>/round-N/codex/solo-prompt.md \
    > <S>/round-N/codex/solo-review.md 2> <S>/round-N/codex/solo.log
  ```
  Check before the first job, in one Bash call, since variables don't survive between calls: `CX=$(ls -d ~/.claude/plugins/cache/openai-codex/codex/*/ | sort -V | tail -1) && node "$CX"scripts/codex-companion.mjs setup --json` must report `"ready": true`. If a job fails twice or setup isn't ready, tell the user and offer Claude. Use another model or effort if the user names one.

## R5: Judge every finding against the evidence

Read `references/judging.md` now. Before any verdict:
- Open the cited document lines and the cited evidence for each finding, and confirm or refute it there. Never accept a finding, its severity or its suggested fix at face value.
- When a finding's truth depends on outside behaviour no evidence settles, spike it now, as the spike rule in R6 describes. A finding about the project's own files is settled by reading them. If nothing can settle it, apply Rule 1 of `references/judging.md`.
- Re-rank on evidence: upgrade, downgrade, or drop with a one-line reason. What the brief lists under "Left out on purpose", and risks the document accepts, are not findings unless the acceptance is unreasonable.
- Write the FOR/AGAINST weighing down for every Critical or Major candidate.
- Spot-check the areas the last round's fixes touched (round 1: the brief's riskiest areas). A Critical or Major you find there is a finding of this round.
- Decide each finding worth acting on, whatever its severity: **fix** it within the limit at the top of this skill (or the profile's), or send it to the **owner** if it needs new procedure, new design, a change of goal, or a choice only the owner can make. The reviewer's suggested fix is an input, not the decision.
- Write `round-N/7-approved.md`: the request's quote, then per finding: fix, owner or drop, judged severity, one-line reason.

## R6: Fix

**Spike before fix.** When a finding or fix depends on how an outside system behaves and no evidence (a spike result, a cited source line, the vendor's docs) proves it, prove it with a spike first and cite the result in the document. Never write outside behaviour into a document from memory. If the project keeps a place for spike findings, record it there in its own commit: that is new evidence, not an edit to another document. If it keeps none, leave the spike in the scratchpad and put the result in the round report; don't create a place. Run spikes before the round's first edit: the gate blocks every `git commit` while the document has unverified edits.

**Impact trace, for every fix.** Write `round-N/8a-impact-trace.md` before the first edit:
1. Search the document for every reference to what the fix changes (names, IDs, numbers, rules) and list them.
2. If `Impact report: yes`, search the related documents for the same items. Under `## Other documents`, record each hit: document, line or section, what must change there. Do not open those documents for editing.
3. Read the target section, then fix it. First correct, simplify or remove the text that caused the problem; add new text only if that can't fix it, and keep it short.
4. Revisit each reference from step 1 and update what is now stale.

**Three verification passes**, as an adversary of your own edits, written to `round-N/8b-verification.md` with the headings `## Pass 1`, `## Pass 2`, `## Pass 3` and what each found:
- **Pass 1, fix to finding:** does each edit resolve the concern raised, or something next to it?
- **Pass 2, consistency:** search for old names (zero matches); confirm anything removed is absorbed elsewhere; compare every list that must be complete against its source; check totals and counts.
- **Pass 3, re-read:** read each changed section from the file, not from memory; check it renders and matches the surrounding style.

If a pass finds an issue, fix it and re-run that pass.

## R7: Re-run the checks, commit, report

- A round with nothing worth fixing skips R6 and the commit; report it and go to R8.
- Re-run the R3 script. Fix what it finds the same way (R6).
- Commit the round as one commit: `docs: fix N Critical + M Major + K Minor findings from adversarial review round R`, with a body listing each fix. If the document isn't in a git repository, skip commits and say so in the round report.
- Report the round in a few lines: judged counts, what was fixed, what went to the owner, what was dropped and why, and the document's word count before and after the round (`wc -w`). Do not wait for an answer.

## R8: Stop rule

Decided by the round's R5 verdicts.
- **A finding sent to fix was judged Critical or Major:** set `round` to N+1 in `active.json` and go to R4. There is no round limit; the loop ends by this rule or when the user says stop.
- **Otherwise** (reviewer's findings and your spot-check; findings sent to the owner don't count): this round's R6 and R7 fixed its worthwhile Minors, and that was the final pass. Run no further round.

## R9: Impact appendix, clean up, final report

**If `Impact report: yes`:** gather the `## Other documents` entries of every round, then re-check each against the final document, since a later fix can undo an earlier hit. Keep one `## Impact on other documents` appendix as the document's last section, in this shape:

```
## Impact on other documents

From the review of <date>. These documents were not edited.

| Document | Likely place | What needs to change |
|---|---|---|
```

If the document already has this appendix, update it in place: re-check every existing row, remove the rows now resolved, add the new ones. If no rows remain, remove the appendix. The appendix is a to-do list that should shrink to nothing, so it never gets a second copy.

Then, in this order, with no reviewer and no further round:
1. If the final round wrote no gate files, write its `7-approved.md` and `8a-impact-trace.md` for the appendix; the gate covers this edit too.
2. Write the appendix.
3. Check each row yourself by opening the lines it points to: the place exists, the conflict is still real against the final document, and "what needs to change" is right. Correct or remove a wrong row on the spot. Record this in `8b-verification.md`.
4. Commit it on its own: `docs: impact appendix from document review`.

If `Impact report: no`, leave any existing appendix as it is.

Delete your session folder `<S>` (`active.json`, the brief and every round folder; never `.review-state/` itself or another session's folder), so the gates stop and nothing satisfies a later review's gates. Then end with:

```
Document is ready for <next readers>. N rounds. Critical/Major by round: R1 a, R2 b, ...
Final Minors fixed: K. Dropped: [finding: reason]. Last commit: <sha>.
Words: <start> to <end>.
Impact report: appendix lists M documents | none affected | not requested.

Decisions for the owner:
- <the decision, why it is yours, severity, and what happens if it stays open>
```

If a Critical went to the owner, say so in the first line: the document is ready apart from that decision.

If the user stops the review early, delete `<S>` and report the open Critical and Major findings instead of the verdict.
