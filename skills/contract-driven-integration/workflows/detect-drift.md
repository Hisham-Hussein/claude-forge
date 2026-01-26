# Detect Drift Workflow

Check if directives and scripts are aligned. Find misalignments in both directions.

## Input

- **directive_path**: Path to the directive
- **extracted_contract**: Output from extract-contract workflow
- **script_mapping**: Output from map-to-scripts workflow

## Two Types of Drift

### Directive Drift
The directive promises something the script doesn't do.

**Detection**: Check if contract assertions are satisfied by actual script behavior.

### Script Drift
The script does something the directive doesn't document.

**Detection**: Analyze script behavior and compare against directive documentation.

## Process

### Step 1: Check directive drift (directive promises → script delivers?)

For each assertion in the extracted contract:

1. **Input assertions**: Does script accept the declared inputs?
   - Read script function signatures
   - Check for parameter validation
   - Verify optional parameters have defaults

2. **Output assertions**: Does script return declared outputs?
   - Check return statements
   - Verify output structure matches directive

3. **Process assertions**: Does script follow declared steps?
   - Trace the execution flow
   - Verify step ordering

4. **Edge case assertions**: Does script handle declared cases?
   - Check for error handling code
   - Verify edge case conditions are tested

Mark each assertion as:
- `aligned` - Script satisfies the assertion
- `drift` - Script does NOT satisfy the assertion
- `unclear` - Cannot determine from code analysis

### Step 2: Check script drift (script does → directive documents?)

Analyze each mapped script for undocumented behaviors:

1. **Undocumented inputs**: Does script accept parameters not in directive?
   - Check function signatures
   - Look for environment variables
   - Find config file reads

2. **Undocumented outputs**: Does script produce outputs not in directive?
   - Check return statements
   - Look for file writes
   - Find database operations

3. **Undocumented side effects**: Does script do things not mentioned?
   - External API calls
   - File system operations
   - Network operations
   - Logging beyond standard

4. **Undocumented dependencies**: Does script use modules not listed?
   - Check imports
   - Find runtime dependencies

Mark each finding as:
- `documented` - Directive mentions this
- `drift` - Script does this but directive doesn't mention it
- `acceptable` - Standard behavior that doesn't need documentation (e.g., basic logging)

### Step 3: Classify drift severity

| Severity | Criteria | Example |
|----------|----------|---------|
| **Critical** | Contract violation that affects correctness | Script doesn't handle declared edge case |
| **Major** | Missing documentation for significant behavior | Script writes to database but directive doesn't mention |
| **Minor** | Cosmetic or low-impact differences | Output includes extra debug field |
| **Info** | Acceptable deviations | Standard library usage |

### Step 4: Generate drift report

```markdown
# Drift Report: {directive_name}

**Directive**: {directive_path}
**Analyzed**: {date}
**Status**: {aligned | drift_detected}

## Summary

| Type | Count |
|------|-------|
| Directive Drift | {n} |
| Script Drift | {n} |
| Total Misalignments | {n} |

## Directive Drift (Directive promises, script doesn't deliver)

### Critical
| Assertion | Status | Evidence |
|-----------|--------|----------|
| {assertion} | drift | {what's missing} |

### Major
| Assertion | Status | Evidence |
|-----------|--------|----------|

### Minor
| Assertion | Status | Evidence |
|-----------|--------|----------|

## Script Drift (Script does, directive doesn't document)

### Critical
| Behavior | Location | Recommendation |
|----------|----------|----------------|
| {behavior} | {file:line} | Document in directive |

### Major
| Behavior | Location | Recommendation |
|----------|----------|----------------|

### Minor
| Behavior | Location | Recommendation |
|----------|----------|----------------|

## Alignment Verified

These assertions are correctly aligned:
- {assertion_1}
- {assertion_2}
...

## Recommendations

1. {Fix directive drift: Update script OR update directive}
2. {Fix script drift: Document behavior OR remove behavior}
```

### Step 5: Update mapping status

Update `execution/directive_mappings.json`:

```json
{
  "directives/workflows/foo.md": {
    "scripts": [...],
    "last_verified": "2026-01-19",
    "contract_status": "drift_detected",
    "drift_summary": {
      "directive_drift": 2,
      "script_drift": 1,
      "severity": "major"
    }
  }
}
```

### Step 6: Create backlog items

For each drift item, suggest a backlog entry:

```markdown
## Backlog: Fix {directive_name} contract drift

**Source**: Contract drift detection
**Severity**: {severity}

### Issue
{Description of drift}

### Evidence
{Where the drift was found}

### Resolution Options
1. Update directive to match script behavior
2. Update script to match directive specification
3. Document as intentional deviation

### Recommended
{Which option and why}
```

## Output

Return:
1. Drift report
2. Updated mapping file status
3. Backlog items for drift fixes

## Quick Checks

Use these quick checks for rapid drift detection:

| Check | Command | What it finds |
|-------|---------|---------------|
| Script exists | `ls {script_path}` | Missing scripts |
| Function signature | Grep for `def ` | Undocumented parameters |
| Return statements | Grep for `return ` | Undocumented outputs |
| External calls | Grep for `requests.`, `gmail.`, etc. | Undocumented integrations |
| File operations | Grep for `open(`, `Path(` | Undocumented file I/O |
| Env vars | Grep for `os.environ`, `os.getenv` | Undocumented configuration |

## Notes

- Run this workflow periodically to catch drift early
- After fixing drift, re-run to verify alignment
- Some drift is acceptable if documented as intentional
- Critical drift should block deployments
