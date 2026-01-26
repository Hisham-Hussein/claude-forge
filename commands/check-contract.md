---
name: check-contract
description: Verify alignment between directives and execution scripts using contract-driven integration
argument-hint: [directive-path] [workflow]
---

<objective>
Verify the contract between a directive (specification) and its implementing scripts.

This skill formalizes the implicit contract between directives and execution scripts, generating tests that verify alignment and detecting drift in both directions.
</objective>

<context>
Available workflows:
1. **extract** - Parse directive to identify contract assertions
2. **map** - Identify which scripts implement a directive
3. **generate** - Create contract tests for a directive
4. **detect** - Check if directives and scripts are aligned (find misalignments)
5. **full** - Run all workflows in sequence (complete audit)
6. **plan** - Check if a project plan addresses all principles from a strategic directive (use `verify-plan-alignment` workflow)

**Contract types:**
- **Directive → Script**: For executable SOPs (use workflows 1-5)
- **Strategic → Plan**: For strategic principles vs. project plans (use workflow 6)
</context>

<process>
1. If no directive path provided, list directives in `directives/workflows/` and ask user to select one
2. If no workflow specified, show the skill intake menu with workflow options
3. **MANDATORY:** Use the Skill tool to invoke `contract-driven-integration` skill
   - DO NOT perform analysis yourself - the skill has standardized workflows and output formats
   - After skill loads, read the appropriate workflow file and follow it EXACTLY
4. Follow the selected workflow exactly as documented in the skill's workflows/ directory
5. Update `execution/directive_mappings.json` with results
6. Add any drift findings to `plans/BACKLOG.md`

**CRITICAL:** This command is a wrapper that delegates to the contract-driven-integration skill. You must invoke that skill to get the correct workflows, templates, and verification procedures. Doing the analysis directly produces inconsistent output.
</process>

<success_criteria>
- Directive parsed into testable assertions (if extract workflow)
- Script(s) identified for directive (if map workflow)
- Contract tests generated and passing (if generate workflow)
- No unaddressed drift detected, or drift documented in backlog (if detect workflow)
- Mapping file updated with verification status
</success_criteria>

<output>
Depending on workflow:
- `tests/contract/test_{directive}_contract.py` - Contract test file
- `execution/directive_mappings.json` - Updated mapping
- `.tmp/drift_report_*.md` - Drift analysis (detect workflow)
- `plans/BACKLOG.md` - Drift findings added
</output>
