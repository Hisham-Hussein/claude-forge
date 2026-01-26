# Map to Scripts Workflow

Identify which scripts implement a directive and create/update the mapping file.

## Input

- **directive_path**: Path to the directive file
- **extracted_contract**: (Optional) Output from extract-contract workflow

## Process

### Step 1: Check directive's Tools section

The directive often explicitly lists its scripts:

```markdown
## Tools
- `execution/scripts/foo.py` - Does X
- `execution/utils/bar.py` - Does Y
```

Extract all script paths mentioned in Tools section.

### Step 2: Search for imports and references

If the directive mentions a main script, read it and check:
- What other modules does it import from `execution/`?
- What utility functions does it use?

These are indirect dependencies that should also be mapped.

### Step 3: Search for naming patterns

Look for scripts that match the directive name:
- `execution/{directive_name}.py`
- `execution/workflows/{directive_name}/`
- `execution/utils/{related_function}.py`

Use glob patterns:
```
execution/**/*{directive_stem}*.py
```

### Step 4: Verify scripts exist

For each identified script:
1. Confirm the file exists
2. Check if it's importable (no syntax errors)
3. Note any missing scripts (directive references non-existent files)

### Step 5: Classify relationship

For each script, determine its role:

| Relationship | Description |
|--------------|-------------|
| **primary** | Main entry point for the directive |
| **dependency** | Used by primary script |
| **utility** | Shared utility used by this directive |

### Step 6: Update mapping file

Update or create `execution/directive_mappings.json`:

```json
{
  "version": "1.0",
  "mappings": {
    "directives/workflows/onboard_client.md": {
      "scripts": [
        {
          "path": "execution/workflows/onboard_client/workflow.py",
          "relationship": "primary"
        },
        {
          "path": "execution/workflows/onboard_client/send_email.py",
          "relationship": "dependency"
        }
      ],
      "last_verified": "2026-01-19",
      "contract_status": "pending"
    }
  }
}
```

### Step 7: Handle missing scripts

If directive references scripts that don't exist:

1. Log the missing scripts
2. Mark `contract_status` as `"missing_scripts"`
3. Add to gaps:

```json
{
  "gaps": [
    {
      "type": "missing_script",
      "path": "execution/foo.py",
      "referenced_in": "Tools section"
    }
  ]
}
```

## Output

Return:
1. List of mapped scripts with relationships
2. Any missing scripts
3. Path to updated mapping file

Format:

```markdown
# Script Mapping: {directive_name}

**Directive**: {directive_path}
**Mapped**: {date}

## Scripts Found

| Script | Relationship | Exists |
|--------|--------------|--------|
| {path} | primary | Yes |
| {path} | dependency | Yes |
| {path} | utility | No - MISSING |

## Mapping File

Updated: `execution/directive_mappings.json`

## Issues

{Any missing scripts or unresolved references}
```

## Example

Given `directives/workflows/onboard_client.md`:

```markdown
# Script Mapping: onboard_client

**Directive**: directives/workflows/onboard_client.md
**Mapped**: 2026-01-19

## Scripts Found

| Script | Relationship | Exists |
|--------|--------------|--------|
| execution/workflows/onboard_client/workflow.py | primary | Yes |
| execution/workflows/onboard_client/send_email.py | dependency | Yes |
| execution/utils/gmail.py | utility | Yes |
| execution/utils/idempotency.py | utility | Yes |

## Mapping File

Updated: `execution/directive_mappings.json`

## Issues

None - all referenced scripts exist.
```

## Notes

- The mapping file is versioned with the codebase
- Run this workflow when scripts are added/removed
- The mapping is input for `detect-drift.md` workflow
