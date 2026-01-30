<overview>
**Gap Analysis & Root Cause Analysis Methodology**

This methodology defines how to systematically audit any skill's output against its input and trace gaps to their root causes in the skill's source files. It is domain-agnostic — it works regardless of what the skill does.
</overview>

<table_of_contents>
- Phase 1: Preparation (file inventory, understand skill intent)
- Phase 2: Gap Analysis (decompose input, classify each item, rate impact, coverage summary)
- Phase 3: Root Cause Analysis (categorize causes, trace to source files, formulate fixes, identify systemic issues)
- Phase 4: Report Assembly (structure, fix format contract, metadata header, verification)
- Common Patterns (flattened priorities, open items converted to facts, conditional directives simplified, operational context dropped, actor details collapsed, integration landscape lost)
</table_of_contents>

<phase_1 name="Preparation">

<step_1_1 name="File Inventory">
Before any analysis, read ALL files completely. Do not start analyzing until every file is loaded:

1. **Input file** — The source document fed into the skill
2. **Output file** — The document the skill produced
3. **SKILL.md** — The skill's instructions (what it tells the agent to do)
4. **Template files** — The structural scaffolding the skill uses for output
5. **Reference files** — Methodology, frameworks, or domain knowledge the skill references
6. **Command file** — The slash command that invokes the skill
7. **Reference methodology** (optional) — External standard the output should comply with
</step_1_1>

<step_1_2 name="Understand the Skill's Intent">
Before evaluating gaps, understand what the skill is designed to do:
- What is the skill's stated objective? (from SKILL.md `<objective>`)
- What extraction/analysis steps does it define? (from `<process>`)
- What template structure does it prescribe? (from templates/)
- What principles or constraints does it impose? (from `<essential_principles>`)
- What does it explicitly warn against? (from `<anti_patterns>`)

This establishes the baseline for what the skill *should* produce, which is essential for distinguishing "the skill didn't tell the agent to do this" (instruction gap) from "the skill told the agent but the agent failed" (execution failure — outside scope of this audit).
</step_1_2>

</phase_1>

<phase_2 name="Gap Analysis (Input vs. Output)">

<step_2_1 name="Decompose the Input File">
Break the input file into discrete, evaluable items. An "item" is any:
- Explicit requirement or specification
- Named entity, value, or data point (e.g., a list of categories, a threshold value)
- Process or workflow step
- Constraint, assumption, or decision
- Relationship or dependency between items
- Open question, pending item, or TBD
- Priority ordering or ranking
- Integration directive or tool reference

Be exhaustive. Go section by section, paragraph by paragraph. Items that seem trivially obvious are often the ones that get silently dropped.
</step_2_1>

<step_2_2 name="Evaluate Each Item Against the Output">
For each item from the input, classify its presence in the output:

| Classification | Definition | Criteria |
|---------------|-----------|----------|
| **ADEQUATE** | Fully and accurately captured | The output contains the item with equivalent meaning, specificity, and completeness. Minor rewording is acceptable if meaning is preserved. |
| **PARTIAL** | Present but incomplete | The output references the item but misses details, reduces specificity, drops qualifiers, or captures only part of a multi-part requirement. |
| **MISSING** | Entirely absent | The output has no trace of this item — not even an indirect reference or implication. |
| **DISTORTED** | Present but misrepresented | The output contains the item but changes its meaning, inverts its intent, adds unsupported claims, or converts it into a different category (e.g., an open question becomes a stated fact). |
</step_2_2>

<step_2_3 name="Rate Impact">
For each non-ADEQUATE item, rate the impact of the gap:

| Impact | Definition |
|--------|-----------|
| **HIGH** | Gap would cause incorrect implementation, wrong priorities, or missed critical requirements. The project would build the wrong thing. |
| **MEDIUM** | Gap would cause incomplete implementation or missed context. The project would build an adequate but suboptimal thing. |
| **LOW** | Gap is cosmetic, minor, or relates to a non-critical item. The project would still succeed but with minor rough edges. |
</step_2_3>

<step_2_4 name="Produce the Coverage Summary">
Calculate:
- Total items evaluated (after deduplication)
- Count and percentage for each classification
- Overall coverage score using the **Weighted Coverage Formula**

**Weighted Coverage Score Formula:**

PARTIAL items receive partial credit based on their impact level — higher-impact gaps get less credit because more critical information was lost:

| Classification | Impact | Weight |
|---------------|--------|--------|
| ADEQUATE | -- | 1.00 |
| PARTIAL | LOW | 0.75 |
| PARTIAL | MED | 0.50 |
| PARTIAL | HIGH | 0.25 |
| MISSING | any | 0.00 |
| DISTORTED | any | 0.00 |

Score = (Sum of all item weights / Total items) × 100

**Rationale:** A PARTIAL/LOW item (minor nuance lost) is mostly captured and deserves more credit than a PARTIAL/HIGH item (critical conditional directive simplified to a flat statement). MISSING and DISTORTED items receive zero credit regardless of impact.

**Example:** 46 ADEQUATE + 1 PARTIAL/HIGH + 4 PARTIAL/MED + 2 PARTIAL/LOW + 5 MISSING out of 58 total:
= (46×1.0 + 1×0.25 + 4×0.50 + 2×0.75 + 5×0.0) / 58 × 100
= (46 + 0.25 + 2.0 + 1.5 + 0) / 58 × 100
= 49.75 / 58 × 100
= 86%
</step_2_4>

<step_2_5 name="Methodology Compliance (if reference provided)">
If a reference methodology or external standard was provided as Input #4:
1. Identify the standard's key requirements or checkpoints
2. Evaluate whether the output adheres to each
3. Note deviations as additional gaps with classification and impact
4. These gaps also get root cause analysis in Phase 3
</step_2_5>

</phase_2>

<phase_3 name="Root Cause Analysis">

<step_3_1 name="Root Cause Categories">
For each gap identified in Phase 2, determine which skill source file is responsible. Use these categories:

| Category | Definition | What to Look For |
|----------|-----------|-----------------|
| **Template gap** | The output template has no section, placeholder, or structural element for this type of information | Missing sections, missing table columns, missing prompts/placeholders in the template |
| **Instruction gap** | SKILL.md does not tell the agent to extract, analyze, or produce this type of information | Missing extraction steps, missing mapping rules, missing guidance in the process section |
| **Methodology gap** | The skill's reference methodology does not cover this aspect | Missing concepts, missing frameworks, missing best practices in the methodology reference |
| **Command gap** | The slash command does not pass sufficient context or parameters | Missing arguments, missing guidance text, missing tool permissions |
| **Structural limitation** | The skill's overall architecture is fundamentally unable to capture this type of requirement | The skill's approach (e.g., single-pass analysis, no iteration, no external lookup) cannot handle this class of input |
</step_3_1>

<step_3_2 name="Tracing Process">
For each gap, work through this decision tree:

1. **Is there a place for this in the template?**
   - NO → Template gap (the agent had nowhere to put this information)
   - YES → Continue to #2

2. **Does SKILL.md instruct the agent to extract/produce this?**
   - NO → Instruction gap (the agent wasn't told to look for this)
   - YES → Continue to #3

3. **Does the methodology reference cover this concept?**
   - NO → Methodology gap (the skill lacks domain knowledge for this)
   - YES → Continue to #4

4. **Does the command pass sufficient context?**
   - NO → Command gap (the invocation doesn't provide enough information)
   - YES → Continue to #5

5. **Is this within the skill's architectural capability?**
   - NO → Structural limitation (the skill needs redesign, not just new instructions)
   - YES → Execution failure (the skill is adequate, the agent just missed it — note this but do not propose a skill fix)

Most gaps will be Template + Instruction gaps. These are the easiest to fix and highest leverage.
</step_3_2>

<step_3_3 name="Formulate Generalizable Fixes">
For each root cause, propose a fix that:

1. **Addresses the category, not the instance** — "Add a section for extracting quantifiable constraints" not "Add a section for extracting budget details from marketing briefs"
2. **Uses domain-neutral language** — Replace project-specific terms with generic equivalents (e.g., "source document" not "client brief", "enumerated categories" not "niche categories")
3. **Specifies exact location** — Which file, which section, where in the file
4. **Provides exact content** — The actual text to add or replace, not a description of what it should say
5. **Explains the rationale** — Why this fix is generalizable and what class of gaps it prevents

**Generalizability test:** Would this fix help if the skill were run on a completely different project in a different industry? If no, the fix is too specific.
</step_3_3>

<step_3_4 name="Identify Systemic Issues">
Group root causes by frequency and identify the top systemic issues — the fixes that would eliminate the most gaps at once.

For each systemic issue:
1. List all gaps it causes
2. Explain the common thread (why these gaps share a root cause)
3. Propose a unified fix that addresses all of them
4. Calculate the proportion of total gaps this fix would resolve

Order systemic issues by the number of gaps they would resolve (highest first).
</step_3_4>

</phase_3>

<phase_4 name="Report Assembly">

<step_4_1 name="Structure">
Follow the report template structure exactly (`templates/AUDIT-REPORT.md`). Do not omit sections, even if they are empty — state "No issues identified" instead.
</step_4_1>

<step_4_2 name="Fix Format Contract">
All upstream fix proposals MUST follow this exact format for machine parseability:

```markdown
#### Fix U-{N}: {Title}

- **Priority:** Critical | High | Medium | Low
- **Target file:** `{relative path from skill root}`
- **Action:** ADD | REPLACE | RESTRUCTURE
- **Location:** {Section name, or "after line X", or "new section after Y"}
- **Current content:** (for REPLACE only)
\`\`\`
{exact text being replaced}
\`\`\`
- **Proposed content:**
\`\`\`
{exact text to insert or replace with}
\`\`\`
- **Rationale:** {Why this is a generalizable improvement}
```

Priority assignment:
- **Critical** — Fix prevents DISTORTED output (actively misleading content, fabricated data)
- **High** — Fix prevents MISSING items with HIGH impact, or resolves a systemic issue affecting 3+ gaps
- **Medium** — Fix prevents PARTIAL or MISSING items with MEDIUM impact
- **Low** — Fix prevents PARTIAL items with LOW impact, or addresses cosmetic/minor gaps

Order fixes by priority (Critical first, Low last). Within the same priority level, order by number of gaps resolved.

Actions:
- **ADD** — Insert new content at the specified location (no existing content to replace)
- **REPLACE** — Replace existing content with new content (requires "Current content" field)
- **RESTRUCTURE** — Significant reorganization that can't be expressed as simple add/replace (describe the change in "Proposed content" as a full section rewrite)

The `U-{N}` numbering must be sequential (U-1, U-2, U-3...) and stable — do not renumber after the report is generated.
</step_4_2>

<step_4_3 name="Metadata Header">
The report must begin with a `## Metadata` section containing a Markdown table with these exact 7 fields: Skill identifier, Plugin, Skill name, Skill root, Input file, Output file, Audit date. The apply command parses this table by matching the bold field names in the first column. Do not change the field names or table structure.
</step_4_3>

<step_4_4 name="Verification">
Before completing the report, verify:
1. Every section of the input file has been compared against the output
2. Every gap has a root cause traced to a specific skill source file
3. Coverage percentage math is correct
4. All upstream fixes are generalizable (would help any future project)
5. All upstream fixes follow the Fix Format Contract exactly
6. Top systemic issues genuinely address the highest number of gaps
7. The metadata header is correctly filled
</step_4_4>

</phase_4>

<common_patterns>
These patterns frequently appear in skill audits. Watch for them:

<pattern name="Flattened Priority Orderings">
**Symptom:** Input specifies a ranked list (e.g., "Channel A first, Channel B second"), output presents as an unordered list.
**Root cause:** Usually an instruction gap — SKILL.md doesn't tell the agent to preserve explicit orderings.
**Fix category:** Add "preserve explicit priority orderings" instruction.
</pattern>

<pattern name="Open Items Converted to Facts">
**Symptom:** Input marks something as unknown/pending/TBD, output presents it as a stated fact (sometimes with a fabricated value).
**Root cause:** Template gap (no "Open Items" section) + instruction gap (no guidance to detect and preserve unknowns).
**Fix category:** Add open items section to template + add detection guidance to instructions.
</pattern>

<pattern name="Conditional Directives Simplified">
**Symptom:** Input says "use X unless Y" or "prefer A but consider B if...", output drops the conditional and states a flat decision.
**Root cause:** Instruction gap — SKILL.md doesn't tell the agent to preserve conditional/directive language.
**Fix category:** Add "preserve conditional directives" instruction.
</pattern>

<pattern name="Operational Context Dropped">
**Symptom:** Input describes usage patterns, frequency, volume, or operational characteristics, output doesn't capture them.
**Root cause:** Template gap (no operational context section) + instruction gap (no extraction guidance for operational details).
**Fix category:** Add operational context prompts to template + extraction guidance to instructions.
</pattern>

<pattern name="Actor/Role Details Collapsed">
**Symptom:** Input describes specific capabilities of actors (users, systems, agents), output summarizes them generically.
**Root cause:** Template gap (no actor capabilities section) + instruction gap (no guidance to decompose actor descriptions).
**Fix category:** Add actor capability mapping guidance.
</pattern>

<pattern name="Integration Landscape Lost">
**Symptom:** Input describes existing tools with their roles and integration/non-integration decisions, output only captures tools mentioned as dependencies.
**Root cause:** Instruction gap — SKILL.md extracts dependencies but not the full tool landscape or non-integration decisions.
**Fix category:** Add tool landscape extraction guidance + template section.
</pattern>

</common_patterns>
