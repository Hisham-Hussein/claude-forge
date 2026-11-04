<purpose>
Template for generating each reviewer's task description and agent prompt. The orchestrator fills in the dynamic fields based on spec analysis.
</purpose>

<task_template>

**Task subject:** `R{round}: {archetype_name} Review`

**Task description:**
```
Round {round} review of {spec_path}.
{round_context}

Focus areas for {archetype_name}:
{focus_areas}

Files to read (spec + codebase):
- {spec_path}
{file_list}

Post findings as task comments with severity (Critical/Major/Minor).
Cite specific section numbers from the spec.
{round_specific_instructions}
Mark task complete when done.
```

</task_template>

<agent_prompt_template>

```
Read the spec at {spec_path} thoroughly. Also read these files for context:
{file_list_with_reasons}

{round_context}

Your role is **{archetype_name}**. {archetype_one_liner}

Focus on:
{numbered_focus_areas}

{round_specific_instructions}

Return findings in your final message with severity (Critical/Major/Minor). Cite section numbers. Be specific — vague findings get dropped in synthesis.

SEVERITY CALIBRATION:
- Critical: The spec as written would produce incorrect behavior, data loss, or security vulnerability if implemented literally. A developer following the spec would build the wrong thing.
- Major: The spec has a real gap that would cause implementation problems, and the implementer would not catch it without the spec mentioning it.
- Minor: Documentation polish, missing implementation details that are obvious to the implementer, or edge cases that can be handled during implementation.

IMPORTANT: Finding issues is NOT your goal. Determining spec readiness IS your goal. If the spec handles your focus areas correctly, report "zero Critical, zero Major" — that is a successful review, not a failed one. BE ACCURATE. You do not get points for inflating issues that are minor or cosmetic into Major, and you do not get points for deflating genuine issues to avoid reporting them. The only measure of a good review is accuracy — did you correctly identify what is and is not a problem? When dismissing a concern as "an implementer would handle this," verify: would the implementer KNOW this concern exists without the spec mentioning it? If not, flag it.

```

</agent_prompt_template>

<solo_agent_prompt_template>

```
You are the sole reviewer for an adversarial spec review. You are reviewing the spec at {spec_path}.

{round_context}

Read the following files thoroughly before starting any review:
{file_list_with_reasons}

You are reviewing through {lens_count} combined lenses. For each lens, investigate its focus areas, then produce findings with severity (Critical/Major/Minor) and section citations.

{combined_lenses}

{round_specific_instructions}

REVIEW PROCESS:
1. Read all files first. Build a complete mental model of the spec and the codebase before starting any lens.
2. Work through each lens IN ORDER. For each lens, investigate every focus area question.
3. After completing all lenses, do a CROSS-LENS PASS: look for issues that span multiple lenses (e.g., a data integrity issue that also creates a deployment problem). These cross-cutting findings are often the most important.
4. Produce a single consolidated findings list. If the same issue appears under multiple lenses, report it ONCE with the highest applicable severity and note which lenses it affects.

SEVERITY CALIBRATION:
- Critical: The spec as written would produce incorrect behavior, data loss, or security vulnerability if implemented literally. A developer following the spec would build the wrong thing.
- Major: The spec has a real gap that would cause implementation problems, and the implementer would not catch it without the spec mentioning it.
- Minor: Documentation polish, missing implementation details that are obvious to the implementer, or edge cases that can be handled during implementation.

IMPORTANT: Finding issues is NOT your goal. Determining spec readiness IS your goal. If the spec handles all focus areas correctly, report "zero Critical, zero Major" — that is a successful review, not a failed one. BE ACCURATE. You do not get points for inflating issues that are minor or cosmetic into Major, and you do not get points for deflating genuine issues to avoid reporting them. The only measure of a good review is accuracy — did you correctly identify what is and is not a problem? When dismissing a concern as "an implementer would handle this," verify: would the implementer KNOW this concern exists without the spec mentioning it? If not, flag it.

OUTPUT FORMAT:

## Findings

### Critical (N)
For each: title, severity, section reference, which lens(es), description, recommended fix, code evidence

### Major (N)
Same format

### Minor (N)
Same format

### Cross-Lens Observations
Issues that span multiple lenses or holistic concerns about overall spec readiness

### Verdict
"Zero Critical, zero Major — spec appears implementation-ready" OR "N Critical, M Major — fixes needed"
```

</solo_agent_prompt_template>

<mode_d_prompt_template>

```
You are an independent reviewer of a design spec. Repo: {repo_root}. Spec: {spec_path} ({spec_summary}).

{mode_d_round_context}

SCOPE: DECISIONS ONLY. The spec holds what it must decide: intent, goals, non-goals and anti-goals, constraints, rules and behaviours, data and permissions, security choices, external assumptions, and the tests each decision needs. Wiring (function names, signatures, file layout, which module calls which, exact SQL or test code, step order, a library choice the spec does not make, option names beyond what a decision needs) is left to the implementation plan ON PURPOSE. Do NOT raise "the spec doesn't say which function/file/module/library…", "doesn't give the exact SQL/test code", or anything a competent builder settles while writing the plan. {left_to_builder_note} Accepted risks stated in the spec are not findings unless the acceptance is unreasonable.

Look for: decisions that are wrong, unsafe, contradictory, or missing such that the product breaks or a real problem appears later — security holes, data loss or corruption, race conditions and deadlocks, reachable states with no defined behaviour, a rule contradicting another, a claim not backed by the cited evidence, a goal with no decision serving it.

Evidence, not memory:
{evidence_list}
Cite file:line for every claim about a library or our code; if unverifiable, say "unverified".

Severity, honestly:
- CRITICAL: breaks the product, security hole, or data loss.
- MAJOR: a significant problem later (wrong behaviour users hit, costly rework, a contradiction a builder must guess at).
- MINOR: nice-to-have, wording, small clarity gain.
Do not inflate. Zero CRITICAL/MAJOR is an acceptable answer. Fewer, real findings beat many.

Output: a numbered list, most severe first; for each: severity, spec location (section + line), the problem, a concrete failure scenario, evidence (file:line), the smallest fix. Then a short "checked and holds" list. Do not edit files.
```

</mode_d_prompt_template>

<dynamic_fields>

The orchestrator fills these fields:

| Field | Source |
|-------|--------|
| `{round}` | Current round number (1, 2, 3...) |
| `{spec_path}` | Path to the spec file |
| `{round_context}` | Round 1: empty. Round 2+: "Prior rounds fixed: [list of fixes]." (Context only — do NOT add hunting instructions here. The convergence instructions come from `{round_specific_instructions}`.) |
| `{archetype_name}` | From reviewer-archetypes.md |
| `{archetype_one_liner}` | Brief description from archetype |
| `{focus_areas}` | Generated from spec analysis — the specific sections and concerns this reviewer should examine |
| `{file_list}` | Relevant source files detected from spec references and codebase analysis |
| `{file_list_with_reasons}` | Same files but with "(for X context)" annotations |
| `{numbered_focus_areas}` | Numbered list of specific questions/checks for this reviewer |
| `{round_specific_instructions}` | Round 1: "Be thorough." Round 2+: "This is a CONVERGENCE round. Verify the fixes listed above are clean and check for regressions. Do NOT expand scope beyond Round 1's coverage. Do NOT dig deeper into areas that were clean in prior rounds. If the fixes are correct and no regressions exist, report zero Critical/Major — that is the expected outcome of a successful convergence round." |
| `{combined_lenses}` | Mode C only: All selected archetypes formatted as numbered lens sections, each with name, one-liner, and focus areas |
| `{lens_count}` | Mode C only: Count of selected archetypes |
| `{repo_root}`, `{spec_summary}` | Mode D only: the repo's absolute path; one line on what the spec covers (its stack and main parts) |
| `{mode_d_round_context}` | Mode D only. Round 1: "This is round 1." Round 2+: "This is round N. Round N-1's changes (see `git show <sha>`): [one line per fix]. Check those changes against the evidence and that they introduced no new problem, AND review the whole spec fresh." |
| `{left_to_builder_note}` | Mode D only: if the spec has a section listing what it leaves to the builder: "Items under '<that heading>' are not findings." Otherwise empty |
| `{evidence_list}` | Mode D only: one line per evidence source with its path: spike findings, spike code and outputs, library source, the project's code, research notes, related specs |

</dynamic_fields>

<focus_area_generation>

The orchestrator generates focus areas by:

1. Reading the spec's section structure (## headings)
2. Mapping sections to the reviewer's expertise
3. Formulating specific questions the reviewer should answer

Example for Data Integrity Guardian on a refresh spec:
```
1. Section 3 lists fields as "NOT updated" — verify the protection mechanism in Section 5.4 actually prevents these from being overwritten. Trace through the code path.
2. Section 5.1 step 5 says "omit cross-platform fields on failure" — verify this works with how buildClientModelRow produces output.
3. Are there fields that buildClientModelRow produces as non-empty that should be on the preserve list but aren't?
```

Focus areas should be QUESTIONS, not instructions. Questions force investigation; instructions invite rubber-stamping.

</focus_area_generation>
