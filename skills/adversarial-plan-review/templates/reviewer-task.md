<purpose>
Template for generating each reviewer's task description and agent prompt. The orchestrator fills in the dynamic fields based on plan analysis.
</purpose>

<task_template>

**Task subject:** `R{round}: {archetype_name} Review`

**Task description:**
```
Round {round} review of {plan_path} (implementing {spec_path}).
{round_context}

Focus areas for {archetype_name}:
{focus_areas}

Files to read (plan + spec + codebase):
- {plan_path}
- {spec_path}
{file_list}

Post findings as task comments with severity (Critical/Major/Minor).
Cite specific task numbers and step numbers from the plan.
{round_specific_instructions}
Mark task complete when done.
```

</task_template>

<agent_prompt_template>

```
You are a teammate on an agent team (Claude Code Agent Teams). Claim task #{task_id} from the shared task list and execute it.

Read the implementation plan at {plan_path} thoroughly. Also read the source spec at {spec_path} — the plan implements this spec. Also read these files for context:
{file_list_with_reasons}

{round_context}

Your role is **{archetype_name}**. {archetype_one_liner}

Focus on:
{numbered_focus_areas}

{round_specific_instructions}

Post findings as task comments with severity (Critical/Major/Minor). Cite task numbers and step numbers from the plan (e.g., "Task 5, Step 3"). Be specific — vague findings get dropped in synthesis.

IMPORTANT: Finding issues is NOT your goal. Determining plan readiness IS your goal. If the plan handles your focus areas correctly, report "zero Critical, zero Major" — that is a successful review, not a failed one. BE ACCURATE. You do not get points for inflating issues that are minor or cosmetic into Major, and you do not get points for deflating genuine issues to avoid reporting them. The only measure of a good review is accuracy — did you correctly identify what is and is not a problem? When dismissing a concern as "an implementer would handle this," verify: would the implementer KNOW this concern exists without the plan mentioning it? If not, flag it.

Mark task complete when done.
```

</agent_prompt_template>

<dynamic_fields>

The orchestrator fills these fields:

| Field | Source |
|-------|--------|
| `{round}` | Current round number (1, 2, 3...) |
| `{plan_path}` | Path to the plan file |
| `{spec_path}` | Path to the source spec the plan implements |
| `{round_context}` | Round 1: empty. Round 2+: "Prior rounds fixed: [list of fixes]. Find remaining issues or problems the fixes introduced." |
| `{archetype_name}` | From reviewer-archetypes.md |
| `{archetype_one_liner}` | Brief description from archetype |
| `{focus_areas}` | Generated from plan analysis — the specific tasks and concerns this reviewer should examine |
| `{file_list}` | Relevant source files detected from plan references and codebase analysis |
| `{file_list_with_reasons}` | Same files but with "(for X context)" annotations |
| `{numbered_focus_areas}` | Numbered list of specific questions/checks for this reviewer |
| `{round_specific_instructions}` | Round 1: "Be thorough." Round 2+: "Don't re-report fixed issues. Focus on what's STILL broken or what the fixes INTRODUCED." |
| `{task_id}` | Task ID from TaskCreate |

</dynamic_fields>

<focus_area_generation>

The orchestrator generates focus areas by:

1. Reading the plan's task list and structure
2. Mapping tasks to the reviewer's expertise
3. Formulating specific questions the reviewer should answer

Example for Dependency Analyst on a campaign shortlists plan:
```
1. Tasks 3 and 4 both claim to be independent and create files in src/. Task 3 creates campaignMatchingEngine.ts and Task 4 creates campaignManager.ts that imports from the matching engine. Can these actually run in parallel?
2. Task 7 adds a route to server.ts that calls populateCampaign(). Verify that all modules populateCampaign() depends on are created in earlier tasks.
3. Task 2 creates types in src/types.ts. Tasks 3-6 all import these types. If Task 2's type definitions change during implementation, what's the blast radius on later tasks?
```

Example for Spec Fidelity Reviewer:
```
1. The spec (Section 2) requires 6 campaign statuses: Queued, Populating, Review, Ready, Shared, Closed. Walk through the plan's tasks — is every status transition implemented? Is there a task that creates the status field with all 6 options?
2. The spec (Section 1) lists 9 always-shown fields and 26 optional fields. Which plan task implements the field mapping? Does it cover all 35 fields?
3. The spec (Section 2) requires server-side Hard Max enforcement. Which task implements this? Does the test cover the case where campaign.maxInfluencers exceeds settings.hardMax?
```

Focus areas should be QUESTIONS, not instructions. Questions force investigation; instructions invite rubber-stamping.

</focus_area_generation>
