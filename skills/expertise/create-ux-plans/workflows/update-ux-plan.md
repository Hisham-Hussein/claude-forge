<status>
**This workflow is a future stub.** It is not yet implemented. When invoked, inform the user that UX plan updates are planned but not yet available, and suggest manually editing the existing UX-DESIGN-PLAN.md or regenerating with the `create-ux-plan` workflow.
</status>

<objective>
Incrementally update an existing UX-DESIGN-PLAN.md when user stories are added, modified, or removed — without regenerating the entire plan from scratch.
</objective>

<planned_scope>
- Diff new/changed stories against existing plan coverage
- Add component specs for new stories
- Update affected sections (IA, hierarchy, components, flows)
- Re-run traceability matrix and Nielsen validation on changed sections only
- Preserve unchanged sections intact
</planned_scope>
