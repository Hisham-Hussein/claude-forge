# Workflow: Select Target

<required_reading>
**Read now:** `references/seam-identification.md`
</required_reading>

<scripts_to_use>
**Primary script:** `scripts/analyze_target.py`

Run this FIRST to get automated analysis, then verify/augment results:

```bash
python scripts/analyze_target.py <target_file> --output .tmp/analysis.json
```

The script identifies:

- Functions and their signatures (inputs)
- Return types (outputs)
- Side effects (file I/O, API calls, logging)
- Seams (mockable dependencies)
- Potential edge cases

Use script output as the foundation, then manually verify completeness.
</scripts_to_use>

<context>
Before capturing behavior, you must identify:
1. What code to characterize
2. Where the testable boundaries (seams) are
3. What inputs and outputs exist
</context>

<process>

**Step 1: Identify the target**

Ask the user (if not already specified):
- What file/function/class do you want to refactor?
- Why are you refactoring? (Understand scope)

Read the target code completely. Do not skim.

**Step 1b: Run automated analysis**

```bash
# Create temp directory if needed
mkdir -p .tmp

# Run analysis script (text report to stdout)
python ~/.claude/skills/characterization-first/scripts/analyze_target.py <target_file>

# Or save as JSON for scaffold script
python ~/.claude/skills/characterization-first/scripts/analyze_target.py <target_file> --json > .tmp/analysis.json
```

Review the script output. It provides:
- Extracted functions with parameters and return types
- Identified seams (external calls that can be mocked)
- Detected side effects
- Suggested edge cases

Use this as your foundation, then manually verify completeness below.

**Step 2: Map the inputs**

Document ALL inputs:
- Function parameters (explicit)
- Environment variables (implicit)
- File system reads (implicit)
- Global state accessed (implicit)
- External API calls (implicit)

```markdown
## Inputs for [target]

| Input | Type | Source | Example Value |
|-------|------|--------|---------------|
| param1 | str | explicit | "hello" |
| CONFIG_PATH | str | env var | "/etc/config.json" |
| ... | ... | ... | ... |
```

**Step 3: Map the outputs**

Document ALL outputs:
- Return values (explicit)
- Side effects: file writes, database changes
- External API calls made
- Exceptions raised
- Logging output

```markdown
## Outputs for [target]

| Output | Type | Destination | Description |
|--------|------|-------------|-------------|
| return | dict | caller | Processed result |
| log | str | stdout | Progress messages |
| ... | ... | ... | ... |
```

**Step 4: Identify seams**

A seam is a place where behavior can be altered without editing the code itself.

Look for:
- Function calls that can be mocked
- Class dependencies that can be injected
- Configuration that controls behavior
- File/network I/O that can be intercepted

Mark each seam:
```markdown
## Seams in [target]

| Location | Type | What it enables |
|----------|------|-----------------|
| line 45: api_client.get() | Object seam | Mock API responses |
| line 67: open(path) | Link seam | Mock file contents |
| ... | ... | ... |
```

**Step 5: Document edge cases**

List known edge cases from code inspection:
- Empty inputs
- Null/None values
- Boundary conditions (0, 1, max)
- Error conditions (file not found, API timeout)
- Unicode, special characters

**Step 6: Checkpoint**

Before proceeding to capture-behavior.md, verify:
- [ ] Target code is fully read and understood
- [ ] All inputs documented (explicit AND implicit)
- [ ] All outputs documented (return values AND side effects)
- [ ] Seams identified for test isolation
- [ ] Edge cases listed

Present this summary to the user and confirm before proceeding.

</process>

<blocking_rule>
**DO NOT proceed to capture-behavior until:**
1. User confirms the input/output/seam analysis
2. All checkpoints are marked complete

If user says "skip analysis" or "just start testing", respond:
"Characterization requires understanding what we're testing. Without this analysis, we'll miss edge cases. Let me complete the seam identification first."
</blocking_rule>

<success_criteria>
This workflow is complete when:
- [ ] Target file/function fully read
- [ ] Inputs table completed (explicit + implicit)
- [ ] Outputs table completed (returns + side effects)
- [ ] Seams identified and documented
- [ ] Edge cases listed
- [ ] User confirms analysis before proceeding
</success_criteria>
