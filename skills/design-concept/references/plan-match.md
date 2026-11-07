# Plan match

For every screen a UX plan covers. Skip this file when no UX plan covers the screen.

The plan decides what each control is and what is on the screen. The look decides how it appears. A look can restyle a select, but it cannot turn a select into a row of pills, drop a column, or reorder sections. These are the deviations that pass every look check, so they need their own step.

## Before building

Write `<concept>/PLAN-MATCH.md` (beside `RELEASE-LIST.md` in Product first): one table per screen, one row for each control, field, column, section and state the plan names, in the plan's order.

| Plan says (quoted) | Built as | Where |
|---|---|---|
| Country (select, several) | select of several with search | creators, filters rail |

Read the plan's own notation first; it usually defines what brackets and fields mean. Fill "Built as" before writing the screen's code, then correct it to what was really built.

## While building

- **Match the control.** Keep the plan's control type, its order and its options. What the plan does not name is your choice and needs no row, but the rule on real size below still applies.
- **Build for the product's real size, not the sample's.** Sample data is small and the product's is not. Any option list that can grow, such as countries, cities or categories, needs a control that still works with hundreds of options: a searchable select, never one pill or checkbox per option laid out in full. Take the options from the data or a full list, never a list cut to fit the sample.
- **A look rule never overrides the plan.** If DESIGN.md or the inspiration seems to need a change to a control, keep the plan's control and style it. A screen too crowded to hold what the plan lists is a problem to solve in layout first.

## Departures

A row that differs from the plan is a departure. Make one only when the plan cannot be built as written. List each in `AGREED-LIST.md` (`RELEASE-LIST.md` in Product first) under "Departures from the UX plan", with what the plan says, what was built and why, and name it in the end report as a real choice. Anything else that differs is a defect: fix it.

Before the outside check, go through the table once more against the built pages, so no row is left as it was planned rather than as it was built.
