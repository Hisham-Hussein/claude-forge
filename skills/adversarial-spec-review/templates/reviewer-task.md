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
You are a teammate on an agent team (Claude Code Agent Teams). Claim task #{task_id} from the shared task list and execute it.

Read the spec at {spec_path} thoroughly. Also read these files for context:
{file_list_with_reasons}

{round_context}

Your role is **{archetype_name}**. {archetype_one_liner}

Focus on:
{numbered_focus_areas}

{round_specific_instructions}

Post findings as task comments with severity (Critical/Major/Minor). Cite section numbers. Be specific — vague findings get dropped in synthesis.

IMPORTANT: Finding issues is NOT your goal. Determining spec readiness IS your goal. If the spec handles your focus areas correctly, report "zero Critical, zero Major" — that is a successful review, not a failed one. BE ACCURATE. You do not get points for inflating issues that are minor or cosmetic into Major, and you do not get points for deflating genuine issues to avoid reporting them. The only measure of a good review is accuracy — did you correctly identify what is and is not a problem? When dismissing a concern as "an implementer would handle this," verify: would the implementer KNOW this concern exists without the spec mentioning it? If not, flag it.

Mark task complete when done.
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
- Major: The spec has a real gap that would cause implementation problems, but a competent developer might catch and fix it during implementation. Still should be fixed in the spec.
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

<dynamic_fields>

The orchestrator fills these fields:

| Field | Source |
|-------|--------|
| `{round}` | Current round number (1, 2, 3...) |
| `{spec_path}` | Path to the spec file |
| `{round_context}` | Round 1: empty. Round 2+: "Prior rounds fixed: [list of fixes]. Find remaining issues or problems the fixes introduced." |
| `{archetype_name}` | From reviewer-archetypes.md |
| `{archetype_one_liner}` | Brief description from archetype |
| `{focus_areas}` | Generated from spec analysis — the specific sections and concerns this reviewer should examine |
| `{file_list}` | Relevant source files detected from spec references and codebase analysis |
| `{file_list_with_reasons}` | Same files but with "(for X context)" annotations |
| `{numbered_focus_areas}` | Numbered list of specific questions/checks for this reviewer |
| `{round_specific_instructions}` | Round 1: "Be thorough." Round 2+: "Don't re-report fixed issues. Focus on what's STILL broken or what the fixes INTRODUCED." |
| `{task_id}` | Task ID from TaskCreate |
| `{combined_lenses}` | Mode C only: All selected archetypes formatted as numbered lens sections, each with name, one-liner, and focus areas |
| `{lens_count}` | Mode C only: Count of selected archetypes |

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
