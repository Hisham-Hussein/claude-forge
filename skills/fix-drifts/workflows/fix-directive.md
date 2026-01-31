# Workflow: Fix Directive

Update a directive to document behaviors that exist in the script but aren't documented.

<input>
- **directive_path**: Path to the directive to update
- **drift_items**: List of script drift items (undocumented behaviors)
  - Each item: behavior description, location (file:line), severity
</input>

<process>

## Step 1: Read Current Directive

Read the full directive file to understand its structure:
- What sections exist (Inputs, Outputs, Process, Edge Cases, etc.)
- What format/style it uses
- Where new content should be added

## Step 2: Read Script Evidence

For each drift item, read the relevant script code at the specified location to understand:
- What the undocumented behavior actually does
- Why it exists (check comments, git history if unclear)
- How it should be documented

## Step 3: Draft Documentation Updates

For each drift item, draft the documentation to add:

```markdown
### Drift Item: {behavior}
**Location**: {file:line}
**Severity**: {severity}

**Current script behavior:**
{description of what the code does}

**Proposed documentation:**
Add to {section_name}:
"{new documentation text}"
```

## Step 4: Present Changes for Approval

Show user the proposed changes:

```markdown
## Proposed Directive Updates

**File**: {directive_path}

### Change 1: {brief description}
**Section**: {section_name}
**Add**:
```
{new text to add}
```

### Change 2: {brief description}
...

**Total changes**: {n}
```

Ask: "Apply these documentation updates?"
- Yes, apply all
- Let me modify first (show changes, let user edit)
- Skip this item / Skip all

## Step 5: Apply Changes

Use the Edit tool to add each approved change to the directive.

**Placement rules:**
- Input parameters → Add to Inputs section
- Output fields → Add to Outputs section
- Side effects (API calls, file writes) → Add to Process section or new Side Effects section
- Error handling → Add to Edge Cases section
- Dependencies → Add to Tools/Scripts section

Preserve existing formatting and style.

## Step 6: Verify Changes

After applying:
1. Read the updated directive
2. Confirm changes were applied correctly
3. If using mapping file, update status

## Step 7: Re-run Drift Detection (Optional)

If user wants verification:
1. Re-invoke contract-driven-integration detect-drift
2. Confirm the script drift items are now resolved
3. Report remaining drift (if any)

</process>

<success_criteria>
This workflow is complete when:
- [ ] All approved documentation has been added to directive
- [ ] Directive maintains consistent formatting
- [ ] No duplicate documentation introduced
- [ ] Changes accurately describe script behavior
</success_criteria>
