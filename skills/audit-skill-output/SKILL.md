---
name: audit-skill-output
description: Use when a skill's output seems incomplete, inaccurate, or missing details from the input. Also use when reviewing skill quality after any skill invocation.
allowed-tools: Read, Glob, Grep, Task, Write, TodoWrite, AskUserQuestion
---

<objective>
Perform a comprehensive gap analysis and root cause analysis on any skill's output by comparing what the skill produced (output file) against what it was given (input file) and what it was supposed to do (skill source files). Identify every gap — MISSING, PARTIAL, DISTORTED, or ADEQUATE — then trace each gap back to specific deficiencies in the skill's instructions, template, methodology, or command. Propose structural, generalizable fixes to the skill itself (not case-specific patches).

The output is a machine-parseable report s I guess you haven't been able to invoke the skill because of the aved to `./reviews/` that serves two audiences:

1. **Project team** — knows exactly what to add/fix in the current output file
2. **Skill maintainer** — knows exactly what to improve in the skill so future invocations don't have the same gaps

This skill spawns a sub-agent to perform the analysis. The main conversation handles input parsing, skill discovery, and presenting results.
</objective>

<inputs>

This skill requires 4 inputs (3 required, 1 optional):

| # | Input | Required | Description |
|---|-------|----------|-------------|
| 1 | **Input file** | Yes | The source document that was fed into the skill (e.g., `CLIENT-BRIEF.md`, `REQUIREMENTS.md`) |
| 2 | **Output file** | Yes | The document the skill produced from that input (e.g., `BUSINESS-CASE.md`, `ARCHITECTURE-DOC.md`) |
| 3 | **Skill identifier** | Yes | The skill to audit, in `plugin:skill-name` format (e.g., `claude-forge:create-business-case`). If the user provides just a skill name without a plugin prefix, search all marketplace directories under `~/.claude/plugins/marketplaces/*/skills/` and ask the user to disambiguate if multiple matches are found. |
| 4 | **Reference methodology** | No | An external standard or guide the skill should have followed (e.g., clean architecture principles, BRD best practices, IEEE 830 standard) |

</inputs>

<quick_start>

1. Collect all 4 inputs from the user (prompt for any missing required inputs)
2. Resolve the skill identifier to a marketplace directory path
3. Read and verify the skill source files exist (SKILL.md, templates/, references/, command)
4. Spawn a sub-agent with all file paths to perform the analysis
5. Verify report structure (metadata header, coverage score, table rows)
6. Present the report path and a brief summary to the user
</quick_start>

<essential_principles>

**Generalizability Above All**
Every proposed fix must improve the skill for ALL future invocations, not just the specific case being analyzed. This is the single most important constraint.

BAD: "The template should include a section for extracting budget details from influencer marketing briefs"
GOOD: "The template lacks a section for extracting quantifiable constraints (financial, timeline, resource) from source documents — add a 'Constraints Extraction' placeholder that prompts the agent to identify all measurable boundaries in the input"

The fix must apply to any future project, not just the current one.

**Trace Gaps to Skill Source, Not to Agent Behavior**
When a gap exists, the root cause is almost always in the skill's source files (instructions, template, methodology), not in a one-off agent failure. Ask: "What should the skill have told the agent to do?" not "Why did the agent miss this?"

**Classify, Don't Judge**
Use the four classifications consistently:

- **MISSING** — Requirement or detail entirely absent from the output
- **PARTIAL** — Present but incomplete, vague, or lacking specificity compared to the input
- **DISTORTED** — Present but misrepresented, reinterpreted, or changed in meaning
- **ADEQUATE** — Fully and accurately captured

**Exhaustive Coverage**
Every meaningful item in the input file must be evaluated. Do not skip items that seem "obviously covered." The most dangerous gaps are subtle — partial coverage that looks adequate until closely inspected.

**Machine-Parseable Fixes**
All upstream fix proposals must follow the Fix Format Contract (see output section) so the companion `/apply-skill-fixes` command can parse and apply them programmatically.

</essential_principles>

<process>

**Before starting, read:** `references/methodology.md` for the detailed gap analysis and root cause analysis methodology.

**Step 1: Collect Inputs**

Ask the user for any inputs not already provided. You need:

1. Path to the input file (source document)
2. Path to the output file (skill's product)
3. Skill identifier in `plugin:skill-name` format
4. (Optional) Path to a reference methodology or external standard

If the user provides a skill name without a plugin prefix (e.g., just `create-business-case`), search for it:

```
~/.claude/plugins/marketplaces/*/skills/<skill-name>/SKILL.md
```

If found in exactly one plugin, use that. If found in multiple, present the options and ask the user to pick.

**Step 2: Resolve Skill Source Files**

From the skill identifier `<plugin>:<skill-name>`, construct the paths:

- Skill root: `~/.claude/plugins/marketplaces/<plugin>/skills/<skill-name>/`
- SKILL.md: `<skill-root>/SKILL.md`
- Templates: `<skill-root>/templates/` (glob for all .md files)
- References: `<skill-root>/references/` (glob for all .md files)
- Command: `~/.claude/plugins/marketplaces/<plugin>/commands/<skill-name>.md`

Read and verify each exists. The SKILL.md is required; others are optional but their absence may itself be a finding.

**Step 3: Spawn Sub-Agent**

Use the Task tool to spawn a sub-agent (subagent_type: "general-purpose") with the following prompt structure. The sub-agent does all the analytical work to keep the main conversation lean.

The sub-agent prompt must include:

1. The full methodology (from `references/methodology.md`)
2. All file paths to read (input, output, skill source files, optional reference)
3. The report template structure (from `templates/AUDIT-REPORT.md`)
4. The output path for the report
5. The skill metadata (identifier, plugin, skill name, skill root path)
6. Clear instructions to follow the methodology exactly

**Sub-agent prompt template:**

```
You are performing a comprehensive audit of a skill's output. Your job is to compare what the skill produced against what it was given, trace every gap back to the skill's source files, and propose generalizable fixes.

## Files to Read (read ALL before starting analysis)

**Project Documents:**
1. Input file: {input_file_path}
2. Output file: {output_file_path}

**Skill Source Files (read from marketplace source, NOT cache):**
3. SKILL.md: {skill_root}/SKILL.md
4. Templates: {list of template files}
5. References: {list of reference files}
6. Command: {command_file_path}

{if reference_methodology}
**Reference Methodology:**
7. {reference_methodology_path}
{endif}

## Methodology

{paste full contents of references/methodology.md here}

## Report Template

{paste full contents of templates/AUDIT-REPORT.md here}

## Skill Metadata (for report header)

- skill_identifier: {plugin}:{skill_name}
- plugin: {plugin}
- skill_name: {skill_name}
- skill_root: ~/.claude/plugins/marketplaces/{plugin}/skills/{skill_name}
- input_file: {input_file_path}
- output_file: {output_file_path}
- date: {today's date}

## Output

Save the complete report to: {output_path}

## Critical Constraints

1. GENERALIZABILITY: Every proposed upstream fix must improve the skill for ALL future invocations, not just this case. Fixes must address categories of gaps, not specific instances.
2. EXHAUSTIVENESS: Every meaningful item in the input file must be evaluated. No skipping.
3. TRACEABILITY: Every gap must have a root cause traced to a specific skill source file.
4. FIX FORMAT: All upstream fixes must follow the Fix Format Contract in the report template exactly. The apply command depends on this format.
5. Read ALL files completely before beginning any analysis.
6. SELF-VALIDATION: Before saving the final report, verify every item in the Verification Checklist (Phase 4.4 of the methodology). If any check fails, fix it before saving. Do not save a report that fails verification.
```

**Step 4: Verify Report Structure**

When the sub-agent completes, read the first 30 lines of the generated report and verify:

1. File exists and is non-empty
2. Contains a `## Metadata` table with all 7 fields populated (Skill identifier, Plugin, Skill name, Skill root, Input file, Output file, Audit date) — no `{placeholder}` values remaining
3. Coverage Score line contains an actual percentage (not `{X}%`)
4. At least one row exists in the Coverage Summary Table

If any check fails, note the specific failure and inform the user the report may be incomplete.

**Step 5: Present Results**

After verification passes:

1. Read the generated report to extract the executive summary
2. Present to the user:
   - Report path
   - Coverage score
   - Gap count by type (MISSING, PARTIAL, DISTORTED)
   - Top systemic issues (brief)
   - Remind user they can run `/apply-skill-fixes` on the report to apply upstream fixes

</process>

<output_conventions>

**Report path:** `./reviews/audit-{skill-name}-{YYYY-MM-DD}.md`

If a report already exists at that path, append a numeric suffix: `audit-{skill-name}-{YYYY-MM-DD}-2.md`

The user can override the path by specifying one explicitly.

**Report structure:** Defined in `templates/AUDIT-REPORT.md`

</output_conventions>

<anti_patterns>

- Proposing case-specific fixes instead of generalizable skill improvements
- Skipping "ADEQUATE" items — they must be listed for completeness and coverage math
- Tracing root causes to "the agent just missed it" instead of skill source deficiencies
- Writing vague fixes like "improve coverage" instead of exact text + file + location
- Fabricating gap impact ratings — if the impact is unclear, say so
- Reading from `~/.claude/plugins/cache/` instead of `~/.claude/plugins/marketplaces/` for skill sources
- Running the analysis inline instead of spawning a sub-agent (context will be consumed)
- Producing fixes that reference project-specific details (company names, domain terms) in skill improvements

</anti_patterns>

<success_criteria>
Skill is complete when:

- A report exists at the output path
- The report contains machine-parseable AUDIT-METADATA header
- Every meaningful item from the input file is classified (ADEQUATE/MISSING/PARTIAL/DISTORTED)
- Coverage percentage is calculated correctly
- Every non-adequate gap has a root cause traced to a specific skill source file
- Top systemic issues are identified and address the highest number of gaps
- All upstream fix proposals follow the Fix Format Contract (U-{N} numbering, target file, action, location, content)
- All proposed fixes are generalizable (would help any future project, not just this one)
- The user has been presented with the report path and summary
</success_criteria>
