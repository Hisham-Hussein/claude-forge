# Workflow: Fix Script

Update a script to implement behaviors promised in the directive but not yet implemented.

<input>
- **directive_path**: Path to the directive (source of truth)
- **script_path**: Path to the script to update
- **drift_items**: List of directive drift items (missing implementations)
  - Each item: assertion (what directive promises), evidence (what's missing)
</input>

<process>

## Step 1: Read Directive Specification

Read the full directive to understand:
- What the directive promises (the "contract")
- Expected inputs and outputs
- Process steps that should be implemented
- Edge cases that should be handled

## Step 2: Read Current Script

Read the script to understand:
- Current implementation structure
- Where new code should be added
- Existing patterns to follow
- Dependencies already imported

## Step 3: Analyze Each Missing Implementation

For each directive drift item:

```markdown
### Missing: {assertion}
**Evidence**: {what's missing from script}

**Directive says:**
{relevant section from directive}

**Script currently:**
{what script does or doesn't do}

**Implementation needed:**
{description of code to add}
```

## Step 4: Draft Implementation

For each missing implementation, draft the code:

```python
# Drift fix: {assertion}
# Implements: {directive section reference}

{implementation code}
```

**Implementation guidelines:**
- Follow existing code style in the script
- Use existing helper functions where possible
- Add appropriate error handling
- Include comments referencing the directive

## Step 5: Present Changes for Approval

Show user the proposed code changes:

```markdown
## Proposed Script Updates

**File**: {script_path}

### Change 1: {what it implements}
**Directive reference**: {section}
**Location**: After line {n} / In function {name}

```python
{code to add}
```

### Change 2: {what it implements}
...

**Total changes**: {n}
```

Ask: "Apply these implementation changes?"
- Yes, apply all
- Let me modify first
- Skip this item / Skip all

**Warning for complex changes:**
If implementation requires significant refactoring (>20 lines, new functions, architectural changes):
- Flag as "complex change"
- Recommend implementing manually with TDD
- Offer to create a TODO item instead

## Step 6: Apply Changes

Use the Edit tool to add each approved change to the script.

**Placement rules:**
- New imports → Top of file with existing imports
- New helper functions → Near related functions
- New code in existing functions → Logical location within function
- New error handling → Wrap existing code or add checks

## Step 7: Run Tests (If Available)

After applying changes:
1. Check if tests exist: `tests/test_{script_name}.py` or `tests/contract/test_{directive_name}_contract.py`
2. If tests exist, run them: `pytest {test_path} -v`
3. Report pass/fail status
4. If tests fail, offer to rollback or fix

## Step 8: Re-run Drift Detection

1. Re-invoke contract-driven-integration detect-drift on the directive
2. Confirm the directive drift items are now resolved
3. Report remaining drift (if any)

</process>

<caution>
**Script changes carry more risk than directive changes.**

Before modifying scripts:
- Ensure you understand the full context
- Check for existing tests
- Consider side effects on other parts of the system
- Prefer small, focused changes over large refactors

If uncertain, recommend:
1. Writing a test first (characterization test)
2. Making the change
3. Verifying the test passes
</caution>

<success_criteria>
This workflow is complete when:
- [ ] All approved implementations have been added to script
- [ ] Script follows existing code patterns
- [ ] Tests pass (if available)
- [ ] Drift detection confirms alignment
</success_criteria>
