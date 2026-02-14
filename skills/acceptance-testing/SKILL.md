---
name: acceptance-testing
description: Use when verifying that a product actually works against live infrastructure. Complements automated tests (which verify code correctness) with interactive product testing (which verifies product correctness). Uses Convex MCP for backend data verification and Playwright MCP for UI interaction. Works standalone or as a checkpoint within charter-to-superpowers.
---

<objective>
Exploratory acceptance testing that verifies the **product works** — not just that tests pass.

Automated tests answer: "Does the code do what the code says it should do?"
Acceptance testing answers: "Does the product actually work when a real user uses it?"

These catch fundamentally different bugs. Automated tests can't detect: infrastructure failures (API credit depletion, deployment misconfigurations), cross-layer data integrity issues (UI shows data that doesn't match the database), or UX problems that only manifest with real latency (loading flashes, WebSocket sync delays).

**Five layers, progressive reporting, adapts to available MCP tools.**

**Invocation:** `/acceptance-test` with optional scope arguments, or invoked by charter-to-superpowers at States 4 and 5.
</objective>

<quick_start>
```
/acceptance-test                                          # Auto-detect scope from git branch
/acceptance-test --plan .charter/PHASE-1-PLAN.md          # Explicit phase plan, test all stories
/acceptance-test --stories US-001,US-004                  # Specific stories only
/acceptance-test --scope group --plan .charter/PHASE-1-PLAN.md --stories US-001,US-004
```

Layers execute in order. Each layer gates the next. Findings are reported progressively.
</quick_start>

<process>

**Announce at start:** "Using the acceptance-testing skill to verify the product works against live infrastructure."

<step_0 title="Detect Tools and Gather Context">

**Detect MCP tools:**

1. **Convex MCP:** Call `mcp__convex__status` with the project directory. If it returns deployment info, record the deployment selector. Mark Convex MCP as available.
2. **Playwright MCP:** Call `mcp__plugin_playwright_playwright__browser_snapshot`. If it responds (even with "no page open"), mark Playwright MCP as available.

Report which tools are available:
```
MCP Tools Detected:
- Convex MCP: [Available — deployment: {name}] or [Not available — skipping Layers 2, 4]
- Playwright MCP: [Available] or [Not available — skipping Layers 3, 4]
```

If NEITHER is available, warn: "No MCP tools detected. Only Layer 1 (automated suite gate) will run. For full acceptance testing, connect Convex MCP and/or Playwright MCP."

**Parse scope from arguments:**

| Argument | Meaning |
|----------|---------|
| `--plan <path>` | Path to the phase plan (e.g., `.charter/PHASE-1-PLAN.md`) |
| `--stories <csv>` | Comma-separated story IDs to test (e.g., `US-001,US-004`) |
| `--scope group` | Test stories in the current execution group only |
| `--scope phase` | Test all stories in the phase |

**If no arguments provided (standalone mode):**
1. Detect phase from git branch: `git branch --show-current` → extract `phase-{N}` pattern
2. Find phase plan: `.charter/PHASE-{N}-PLAN.md`
3. If phase plan found, ask user:
   > What scope should acceptance testing cover?
   > - **Current group** — test the most recently completed execution group
   > - **Full phase** — test all stories in the phase
4. If no phase plan found, ask user to describe what was built or provide story IDs

**Extract test scenarios:**
1. Read the phase plan for scoped stories — extract the Story Summary section
2. Read `.charter/USER-STORIES.md` for acceptance criteria of each scoped story
3. Build a test scenario list: one scenario per acceptance criterion, grouped by story
4. Read `package.json` to identify available test/build/typecheck commands

**Create TodoWrite checklist:**
```
- Layer 1: Automated Suite Gate
- Layer 2: Backend Data Verification
- Layer 3: UI Interactive Testing — {story-id}: {story-name} (one per story)
- Layer 4: End-to-End Product Flow
- Layer 5: Issue Documentation and Verdict
```

</step_0>

<layer_1 title="Automated Suite Gate">

**Always runs, even without MCP tools.**

Run every verification command the project provides, in order:

1. **Type checking:** `npm run typecheck` (if script exists in package.json)
2. **Unit/integration tests:** `npx vitest run` (or `npm test`)
3. **Build:** `npm run build`
4. **E2E tests:** `npm run test:e2e` (if script exists)

For each command:
- Run it fresh (do not rely on cached results)
- Read the FULL output
- Report: command, exit code, pass/fail counts, any failures

**GATE decision:**

If ALL pass → proceed to Layer 2.

If ANY fail:
- Report the failures with full output
- Ask user:
  > Automated suite has failures:
  > - {list of failing commands with summary}
  >
  > Options:
  > - **Fix first** (Recommended) — stop here, fix failures, re-invoke `/acceptance-test`
  > - **Continue anyway** — proceed with interactive testing despite failures (findings will note this)

If user chooses "Fix first" → STOP. Report the failures and exit.
If user chooses "Continue anyway" → proceed, but prepend all subsequent findings with: "NOTE: Automated suite has failures. Interactive testing results may be unreliable."

</layer_1>

<layer_2 title="Backend Data Verification">

**Requires Convex MCP. Skip if unavailable:** Report "Skipping Layer 2 — Convex MCP not available." and proceed to Layer 3.

**Read `references/layer-methodology.md`** for detailed query patterns before executing this layer.

Use the deployment selector obtained in Step 0.

**a. Schema verification:**
- Call `mcp__convex__tables` to list all tables with their schema
- Compare against the phase plan's expected tables (from task I/O sections)
- Report any: missing tables, extra unexpected tables, missing fields, type mismatches

**b. Data shape verification:**
- For each table relevant to the scoped stories, call `mcp__convex__data` (limit 10-20 rows)
- Check each row against domain rules:
  - Nullable fields must be `null` when data is absent, NEVER fake defaults (per CLAUDE.md "no fake defaults" principle)
  - Required fields must be populated (not null, not empty string)
  - Value ranges must comply with domain constraints (e.g., follower floors per size bucket)
  - Enum fields must contain valid values from the domain model

**c. Index verification:**
- From the schema output, identify declared indexes
- For each index, run a query using that index to verify it returns results (if data exists)
- Report any indexes that exist in schema but fail to resolve, or expected indexes that are missing

**d. Data quality queries:**
- Use `mcp__convex__runOneoffQuery` to run aggregate compliance checks
- Essential queries (adapt to the domain):
  - Null audit: count of records with plausible-looking defaults in nullable fields
  - Range validation: count of records outside configured domain boundaries
  - Distribution check: breakdown by key categorical fields (size bucket, status, niche)
  - Referential integrity: cross-table reference validation

**Report findings progressively** — as each sub-step (a, b, c, d) completes, report results immediately.

</layer_2>

<layer_3 title="UI Interactive Testing">

**Requires Playwright MCP. Skip if unavailable:** Report "Skipping Layer 3 — Playwright MCP not available." and proceed to Layer 4.

**Determine app URL:**
1. Check `package.json` scripts for dev server port (typically 3000 or 3001)
2. Attempt `mcp__plugin_playwright_playwright__browser_navigate` to `http://localhost:3000`
3. If navigation fails, ask user for the correct URL
4. If app is not running, report: "App not running at {URL}. Start the dev server (`npm run dev`) and re-invoke."

**For each story in scope, test its acceptance criteria:**

Read `references/layer-methodology.md` for the AC-to-Playwright action mapping.

For each acceptance criterion:

1. **Navigate** to the relevant page (`browser_navigate`)
2. **Snapshot** the page state (`browser_snapshot`) — verify expected elements exist
3. **Interact** per the AC requirement:
   - Forms: `browser_fill_form` or `browser_type` + `browser_click` submit
   - Dropdowns: `browser_click` trigger + `browser_click` option
   - Navigation: `browser_click` link + verify URL change
   - Lists: verify items in snapshot match expected data
4. **Verify** the result via `browser_snapshot`:
   - Expected elements present? Expected text displayed?
   - Error messages shown when expected? Loading states visible?
5. **Record** the result:
   ```
   {story-id} AC-{N}: {AC description}
   Action: {what was done}
   Expected: {expected outcome}
   Actual: {actual outcome}
   Result: PASS / FAIL
   Evidence: {snapshot reference or screenshot}
   ```

**Edge case testing per story (after AC verification):**
- Empty required fields → expect validation error
- Boundary values from domain rules (use specific numbers, not just "large")
- Arabic text from domain value objects (niche names, hashtag content)
- Special characters in text fields (commas, #, @, URLs)

**Report each story's results as completed** — don't wait until all stories are tested.

</layer_3>

<layer_4 title="End-to-End Product Flow">

**Requires BOTH Convex MCP and Playwright MCP. Skip if either unavailable:** Report "Skipping Layer 4 — requires both Convex MCP and Playwright MCP." and proceed to Layer 5.

**Read `references/layer-methodology.md`** for workflow derivation and cross-layer verification patterns.

**Identify the primary user workflow:**
1. Read the phase plan's Story Summary or acceptance test scenarios
2. Chain the scoped stories into a chronological user journey
3. Present the workflow steps to the user for confirmation before executing

**Execute the workflow start-to-finish:**

For each step in the workflow:

1. **Perform the action** via Playwright MCP (navigate, fill form, click button)
2. **Wait briefly** (2-5 seconds) for backend sync — use `browser_wait_for` with time parameter
3. **Verify backend state** via Convex MCP:
   - Query the relevant table (`mcp__convex__data` or `mcp__convex__runOneoffQuery`)
   - Check that the expected record exists with correct values
   - Check status transitions happened (e.g., "Configured" → "Running" → "Completed")
4. **Verify UI reflects backend** via Playwright MCP:
   - Take a fresh `browser_snapshot`
   - Compare displayed data against what Convex MCP returned
   - Flag any discrepancies (UI shows stale data, wrong counts, missing records)

**For workflows involving external APIs (Apify, OpenAI, etc.):**
- Do NOT trigger API calls unless the user explicitly approves (cost awareness per CLAUDE.md)
- If the workflow requires an external API call to complete:
  - Ask user: "This workflow triggers {API name}. Proceed? (This will incur API costs.)"
  - If user approves: execute and verify
  - If user declines: verify up to the API call point, then note: "Workflow verified up to external API call. Full end-to-end not tested — user declined due to cost."

**Report the workflow trace:**
```
E2E Workflow: {workflow description}

Step 1: {action} → UI: {snapshot result} | Backend: {query result} | Match: YES/NO
Step 2: {action} → UI: {snapshot result} | Backend: {query result} | Match: YES/NO
...
Overall: {all steps passed / N steps failed}
```

</layer_4>

<layer_5 title="Issue Documentation and Verdict">

**Always runs — compiles findings from all completed layers.**

**Compile all findings** from Layers 1-4 into a single list. For each finding:

```
[SEVERITY] {story-id} / AC-{N}: {description}
  Evidence: {command output / query result / snapshot reference}
  Layer: {which layer discovered this}
```

**Severity classification** (see `references/layer-methodology.md` for detailed examples):
- **CRITICAL:** Blocks the user from completing a core workflow. Data loss, crashes, broken submissions, corrupted persistence.
- **IMPORTANT:** Degrades experience but a workaround exists. Missing validation, wrong error messages, loading flash, stale data without refresh.
- **MINOR:** Cosmetic or polish. Alignment, spacing, placeholder text, console warnings.

**Summary table:**

```
## Acceptance Testing Summary

| Metric | Value |
|--------|-------|
| Stories tested | {list of story IDs} |
| Layers completed | {1, 2, 3, 4 — or subset with skip reasons} |
| Acceptance criteria verified | {N of M} |
| Issues found | {total} |
| Critical | {count} |
| Important | {count} |
| Minor | {count} |
```

**Verdict:**

| Condition | Verdict |
|-----------|---------|
| 0 critical AND 0 important | **ACCEPT** — Product works as specified. |
| 0 critical AND 1+ important | **ACCEPT WITH ISSUES** — Core workflows work but experience is degraded. List the important issues. |
| 1+ critical | **REJECT** — Core workflows are broken. List the critical issues. Must fix before proceeding. |

**Present the verdict clearly:**
```
VERDICT: {ACCEPT / ACCEPT WITH ISSUES / REJECT}

{If ACCEPT WITH ISSUES or REJECT, list the blocking/degrading issues with their evidence}
```

</layer_5>

</process>

<detection_logic>

**MCP tool detection:**
```
Convex MCP: Call mcp__convex__status with projectDir.
  - Response with deployment info → Available. Record deploymentSelector.
  - Error or no response → Not available.

Playwright MCP: Call mcp__plugin_playwright_playwright__browser_snapshot.
  - Any response (even "no page open") → Available.
  - Error or no response → Not available.
```

**Scope detection (standalone mode):**
```bash
# 1. Get current branch
BRANCH=$(git branch --show-current)

# 2. Extract phase number
PHASE=$(echo "$BRANCH" | grep -oP 'phase-\K\d+')

# 3. Find phase plan
PLAN=".charter/PHASE-${PHASE}-PLAN.md"

# 4. Parse execution groups (same regex as charter-to-superpowers)
# Regex: ### (?:Execution Group|Parallel Group) (\d+)

# 5. Find most recently completed group via git log story ID detection
# (same logic as charter-to-superpowers detection_logic)
```

**App URL detection:**
```bash
# Check package.json for dev server port
grep -o '"dev":\s*"[^"]*"' package.json
# Common: "next dev -p 3000" or "next dev" (default 3000)
# Attempt connection: curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
```

</detection_logic>

<edge_cases>
1. **No MCP tools available:** Run Layer 1 only (automated suite gate). Report: "No MCP tools detected. Only automated verification completed. Connect Convex MCP and/or Playwright MCP for full acceptance testing."
2. **Convex MCP available but tables empty:** Report "Tables exist but contain no data — has the feature been exercised?" Suggest running Layer 3 first (to populate data via UI), then re-run Layer 2.
3. **Playwright available but app not running:** Detect via failed navigation. Report: "App not running at {URL}. Start the dev server and re-invoke." Do not proceed with Layers 3 or 4.
4. **No phase plan provided or found:** Ask user to describe what was built, or provide specific story IDs. Derive test scenarios from conversation context rather than phase plan.
5. **Stories involve external paid APIs (Apify, OpenAI):** Verify that integration code exists (functions deployed, UI triggers wired) but do NOT call paid APIs unless user explicitly approves. Note: "External API integration verified structurally. Live API call not tested — requires explicit approval due to cost."
6. **Auth-gated pages:** If navigation results in a login redirect, report it and ask user: "Page requires authentication. Options: (a) Provide test credentials, (b) Skip auth-gated pages, (c) Bypass auth for testing (if dev mode supports it)."
7. **Re-invocation after fixing issues:** The skill runs fresh each time. No state is carried between invocations. All layers re-execute from scratch.
8. **Arabic text testing:** Use real domain values from the codebase (e.g., niche names from `valueObjects.ts` or test fixtures). Do not fabricate Arabic strings — use what the domain model actually defines.
</edge_cases>

<anti_patterns>
- **Never modify code or fix issues.** This skill ONLY tests and reports. Fixing is a separate activity — the user or a follow-up development session handles fixes. If you find a bug, report it with evidence and move on.
- **Never call paid external APIs (Apify, OpenAI) without explicit user approval.** Verify the integration code exists, but do not trigger API calls that incur cost. Ask first.
- **Never skip Layer 1.** The automated suite gate catches regressions that interactive testing alone might miss. Even if all MCP tools are available, Layer 1 runs first.
- **Never batch findings to the end.** Report findings progressively — as each layer or sub-step completes. The user should see issues as they are discovered, not in a single dump at the end.
- **Never claim PASS without evidence.** Every passing test needs a snapshot, query result, or command output as proof. Follows the verification-before-completion discipline: no claims without evidence.
- **Never test against the production deployment by default.** Use the development deployment unless the user explicitly requests production testing.
</anti_patterns>

<success_criteria>
- Correct MCP tool detection with graceful degradation (skip layers, don't crash)
- All stories in scope have their acceptance criteria tested (or explicitly skipped with documented reason)
- Every finding (PASS or FAIL) includes evidence — not just assertions
- Progressive reporting throughout (findings appear as discovered, not batched)
- Clear verdict (ACCEPT / ACCEPT WITH ISSUES / REJECT) with severity-based categorization
- Works both standalone (`/acceptance-test`) and when invoked from charter-to-superpowers
- Skipped layers are clearly reported with reason
- External API boundaries are respected (no unauthorized paid API calls)
</success_criteria>
