# Workflow: Detect and Propose Fixes

Run drift detection on a directive, analyze results, and propose corrections with recommendations.

<input>
- **directive_path**: Path to the directive to check (e.g., `directives/workflows/onboard_client.md`)
</input>

<process>

## Step 1: Run Drift Detection

Invoke the contract-driven-integration skill with the "detect drift" option:

```
Use the Skill tool:
skill: contract-driven-integration
args: "4 {directive_path}"
```

Wait for the drift report to be generated.

## Step 2: Parse Drift Report

Extract from the drift report:

1. **Directive drift items** - Promises in directive that script doesn't fulfill
   - Section: "Directive Drift (Directive promises, script doesn't deliver)"
   - Each row: assertion, status, evidence

2. **Script drift items** - Behaviors in script that directive doesn't document
   - Section: "Script Drift (Script does, directive doesn't document)"
   - Each row: behavior, location, recommendation

3. **Severity levels** - Critical > Major > Minor

If the report shows "Status: aligned", inform user no drift detected and exit.

## Step 3: Analyze Each Drift Item

For each drift item, determine the recommended fix direction:

| Drift Type | Default Recommendation | Reasoning |
|------------|----------------------|-----------|
| Script Drift (undocumented behavior) | Fix directive | Script works correctly, just needs documentation |
| Directive Drift (missing implementation) | Fix script | Directive is the spec, script should implement it |

**Override recommendations when:**
- Script behavior is a bug → Fix script, not directive
- Directive is outdated/wrong → Fix directive, not script
- Behavior is intentionally undocumented → Mark as acceptable, no fix needed

## Step 4: Present Proposals

Format the proposals for user review:

```markdown
## Drift Correction Proposals for {directive_name}

### Script Drift (recommend: fix directive)

| # | Behavior | Location | Proposal |
|---|----------|----------|----------|
| 1 | {behavior} | {file:line} | Add to directive under {section} |
| 2 | {behavior} | {file:line} | Add to directive under {section} |

### Directive Drift (recommend: fix script)

| # | Promise | Evidence | Proposal |
|---|---------|----------|----------|
| 1 | {assertion} | {what's missing} | Implement in {script} |

### Summary

- Script drift items: {n} (recommend fixing directive)
- Directive drift items: {n} (recommend fixing script)
- Total corrections needed: {n}
```

## Step 5: Get User Decision

Ask user using AskUserQuestion:

**Question**: "How would you like to proceed with these {n} drift corrections?"

**Options**:
1. **Fix all as recommended** - Apply script drift → directive, directive drift → script
2. **Fix directive only** - Document undocumented behaviors, defer script changes
3. **Fix script only** - Implement missing features, defer documentation
4. **Review each item** - Decide direction for each item individually
5. **Defer all** - Add to backlog, don't fix now

## Step 6: Route to Fix Workflows

Based on user choice:

| Choice | Action |
|--------|--------|
| Fix all as recommended | Run fix-directive.md for script drifts, then fix-script.md for directive drifts |
| Fix directive only | Run fix-directive.md with all script drift items |
| Fix script only | Run fix-script.md with all directive drift items |
| Review each item | Loop through items, ask direction for each, then apply |
| Defer all | Add items to QUEUE.md backlog, update mapping status to "drift_deferred" |

</process>

<success_criteria>
This workflow is complete when:
- [ ] Drift detection has run
- [ ] All drift items have been categorized
- [ ] User has decided on fix direction
- [ ] Appropriate fix workflow(s) have been triggered OR items deferred to backlog
</success_criteria>
