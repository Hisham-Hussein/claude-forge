# Extract Contract Workflow

Parse a directive to identify its contract assertions.

## Input

- **directive_path**: Path to the directive file (e.g., `directives/workflows/onboard_client.md`)

## Process

### Step 1: Read the directive

Read the full directive file. Do not skim.

### Step 2: Identify sections

Look for these standard sections (may not all be present):

| Section | Common Headers |
|---------|----------------|
| Trigger | `## Trigger`, `## When to use`, `## Invocation` |
| Inputs | `## Inputs`, `## Parameters`, `## Arguments` |
| Tools | `## Tools`, `## Dependencies`, `## Scripts Used` |
| Process | `## Process`, `## Steps`, `## Workflow` |
| Outputs | `## Outputs`, `## Returns`, `## Results` |
| Edge Cases | `## Edge Cases`, `## Error Handling`, `## Failure Modes` |

Note which sections are present and which are missing.

### Step 3: Extract assertions per section

For each section found, extract testable assertions:

**From Trigger:**
- What conditions activate this directive?
- What CLI/commands/phrases trigger it?
- Assertion: "Script is callable via {trigger}"

**From Inputs:**
- What parameters are required vs optional?
- What types/formats are expected?
- Assertion: "Script accepts {input} of type {type}"
- Assertion: "Script requires {required_input}"
- Assertion: "Script handles missing {optional_input}"

**From Tools:**
- What scripts/files does this directive use?
- Assertion: "Script uses {tool}"
- Assertion: "Script depends on {file}"

**From Process:**
- What steps must occur?
- What order must they follow?
- Assertion: "Script performs {step} before {next_step}"
- Assertion: "Script includes step: {step_description}"

**From Outputs:**
- What format is the output?
- What fields must be present?
- Assertion: "Script returns {output_format}"
- Assertion: "Output contains field: {field}"

**From Edge Cases:**
- What errors are handled?
- What happens in degraded modes?
- Assertion: "Script handles {edge_case}"
- Assertion: "Script returns {error} when {condition}"

### Step 4: Note gaps

Document what's missing from the directive:
- Missing sections that should exist
- Vague descriptions that can't be tested
- Implicit behaviors not documented

These gaps are **directive drift candidates** - behaviors that may exist in code but aren't documented.

### Step 5: Format output

Structure the extracted contract as:

```markdown
# Contract: {directive_name}

**Source**: {directive_path}
**Extracted**: {date}

## Assertions

### Trigger Assertions
- [ ] {assertion_1}
- [ ] {assertion_2}

### Input Assertions
- [ ] {assertion_1}
- [ ] {assertion_2}

### Tool Assertions
- [ ] {assertion_1}

### Process Assertions
- [ ] {assertion_1}
- [ ] {assertion_2}

### Output Assertions
- [ ] {assertion_1}
- [ ] {assertion_2}

### Edge Case Assertions
- [ ] {assertion_1}
- [ ] {assertion_2}

## Gaps Identified

| Gap | Type | Recommendation |
|-----|------|----------------|
| {description} | Missing section / Vague / Implicit | {action} |
```

## Output

Return the formatted contract document. This becomes input for:
- `workflows/map-to-scripts.md` - Find implementing scripts
- `workflows/generate-tests.md` - Create test file

## Example

Given `directives/workflows/onboard_client.md`:

```markdown
# Contract: onboard_client

**Source**: directives/workflows/onboard_client.md
**Extracted**: 2026-01-19

## Assertions

### Trigger Assertions
- [ ] Script callable via `PYTHONPATH=. python -m execution.workflows.onboard_client`
- [ ] Script accepts --email argument
- [ ] Script accepts --name argument (optional)
- [ ] Script accepts --dry-run flag

### Input Assertions
- [ ] Script requires email parameter
- [ ] Script validates email format
- [ ] Script handles missing name gracefully

### Tool Assertions
- [ ] Script uses execution/workflows/onboard_client/workflow.py
- [ ] Script uses execution/workflows/onboard_client/send_email.py
- [ ] Script reads directives/templates/company_intro.md

### Process Assertions
- [ ] Script validates inputs before side effects
- [ ] Script checks idempotency before processing
- [ ] Script loads template before generating content
- [ ] Script generates content before sending
- [ ] Script records completion after sending

### Output Assertions
- [ ] Success output contains: success, email, correlation_id, message_id
- [ ] Degraded output contains: queue_id, degraded flag
- [ ] Failure output contains: error, failed_step
- [ ] Duplicate output contains: duplicate flag

### Edge Case Assertions
- [ ] Script rejects invalid email format with clear error
- [ ] Script prevents duplicate onboarding via idempotency
- [ ] Script handles Gmail auth expiration
- [ ] Script handles rate limits with retry
- [ ] Script handles missing template with clear error
- [ ] Script times out after 30s per attempt

## Gaps Identified

| Gap | Type | Recommendation |
|-----|------|----------------|
| None identified | - | Directive is well-documented |
```
