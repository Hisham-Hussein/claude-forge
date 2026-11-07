# Product first: build the real design

For when the product is decided. Output: high-fidelity mockups of every screen of this release, with the user experience built in, close to what users will see.

## 1. Check the inputs

You need a chosen DESIGN.md, the story map and a UX plan.

With no UX plan, or one that does not cover this release, stop and send the user to `create-ux-plans`. It holds the layouts, states and wording this workflow builds from; guessing them here would make the mockups wrong in ways that look right.

## 2. Work out the release page list

Find what is being built in this release: the MVP on the first run, release 2 on the next, and so on. Read the release from the story map, PRD or UX plan. If that is unclear, interview the user. The aim is neither piecemeal pages nor 50 pages in one go.

On a later release, list only the new or changed pages, and reuse DESIGN.md and the existing screens.

Settle "Decisions first" in SKILL.md. Then write `RELEASE-LIST.md` beside the chosen DESIGN.md: each page, its ID in the UX plan, its states, the stories it serves, the languages and themes. Tell the user what you understood and ask them to approve the list. **This is the one stop.** After approval, run to the end.

## 3. Build

- Use the project's real front-end stack, so the front end reuses the screens with few changes. Follow the project's constitution if it has one.
- Layouts, states and wording come from the UX plan, exactly: follow `plan-match.md`. Where it and DESIGN.md seem to disagree, the plan says what is on the screen and DESIGN.md how it looks.
- Every state the plan lists gets built and reachable: loading, empty, error, no permission, and the rest. A page with only its happy path is not finished.
- Use sample data, behind a seam the real data can replace.
- Components come first: build each one once from DESIGN.md §5, then compose pages from them.
- If DESIGN.md is missing something a screen needs, extend it, run design-review on the change (called by this skill), and carry on.

## 4. Check and finish

Rules 3 to 5 in SKILL.md, then the end report. The scripts read HTML files. When the stack is not plain HTML, serve the app, take the same set of screenshots with Playwright, walk design-review's `auto N` checks by hand, and say so in the end report.
