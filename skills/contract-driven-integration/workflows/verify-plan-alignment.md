# Verify Plan Alignment Workflow

Check if a project plan addresses all principles from a strategic directive. Produces an alignment report (not executable tests).

## Input

- **strategic_directive_path**: Path to strategic directive (e.g., `directives/strategic/architecture_principles.md`)
- **plan_path**: Path to project plan (e.g., `.planning/PLAN.md`)

## When to Use

Use this workflow when:
- Verifying a project plan against architecture principles
- Checking if a plan addresses all items in a methodology document
- Auditing plan completeness against strategic requirements

**Not for:** Verifying executable scripts (use detect-drift workflow instead).

## Process

### Step 1: Extract principles from strategic directive

Read the strategic directive and extract checkable assertions:

1. Look for numbered principles, sections, or bullet points
2. For each principle, identify:
   - **Name**: Short identifier (e.g., "Fail Fast", "Idempotency")
   - **Requirement**: What the principle demands
   - **Evidence needed**: What would satisfy this in a plan

Output: List of principles with expected evidence.

### Step 2: Scan plan for evidence

For each extracted principle:

1. Search plan for keywords related to the principle
2. Check for explicit sections addressing the principle
3. Look for implicit coverage in related sections

Mark each principle as:
- `✅ Aligned` - Plan explicitly addresses this principle with specific decisions
- `⚠️ Partial` - Plan mentions but doesn't specify project-specific application
- `❌ Missing` - Plan doesn't address this principle

### Step 3: Generate alignment report

```markdown
## Contract Verification: {strategic_directive} → {plan_name}

**Source:** {strategic_directive_path}
**Target:** {plan_path}
**Date:** {date}

---

### Alignment Summary

| Status | Count | Principles |
|--------|-------|------------|
| ✅ Aligned | {n} | {list} |
| ⚠️ Partial | {n} | {list} |
| ❌ Missing | {n} | {list} |

---

### Detailed Verification

#### ✅ ALIGNED ({n} principles)

| # | Principle | Evidence in Plan | Location |
|---|-----------|------------------|----------|
| {n} | **{name}** | {what plan says} | Line {n} |

#### ⚠️ PARTIAL ({n} principles)

| # | Principle | What's Present | What's Missing |
|---|-----------|----------------|----------------|
| {n} | **{name}** | {partial coverage} | {gap description} |

**Suggested additions for {principle}:**
```
{suggested text to add to plan}
```

#### ❌ MISSING ({n} principles)

| # | Principle | Impact | Recommended Addition |
|---|-----------|--------|---------------------|
| {n} | **{name}** | {why it matters} | {what to add} |

---

### Contract Status

```
{plan_name} Contract Verification
├── ✅ {n}/{total} principles fully addressed
├── ⚠️ {n}/{total} principles partially addressed
├── ❌ {n}/{total} principles not addressed
└── Overall: {percentage}% aligned
```
```

### Step 4: Suggest fixes for gaps

For each partial or missing principle, provide:
1. Specific text to add to the plan
2. Which section it should go in
3. Why this addition satisfies the principle

## Output

Return:
1. Alignment report (markdown format)
2. Suggested edits for incomplete principles
3. Overall alignment percentage

## Notes

- This produces documentation, not executable tests
- Run after major plan changes to ensure principle coverage
- Can be automated as a plan review checklist
