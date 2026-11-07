---
name: design-concept
description: Turns a design inspiration into a working design in code, in one run - a DESIGN.md plus finished HTML or front-end screens - by studying the inspiration in depth, passing DESIGN.md through design-review, building every screen, and proving the result with an outside check. Two workflows - Look first (try a style from an inspiration site on a few screens, even with an unfinished idea) and Product first (build every screen of a release from a chosen DESIGN.md and a UX plan). Use when the user wants to try a style or a website's look on their product, compare design directions with real prototypes, turn an inspiration site or Webflow template into a design, create high-fidelity mockups, or build the mockups of a release, even if they don't say "design concept".
---

# Design concept

Turn a design inspiration into a working design in code, in one go. Each inspiration should be cheap to try, so a direction is picked from real prototypes, not mood boards.

This skill exists to end two failures:

- **Lazy work:** doing the least that would work and calling it done, without studying the inspiration or capturing it in DESIGN.md.
- **Piecemeal pages:** one or two pages at a time, so the user has to keep asking for the rest.

So the run finishes everything on its list before it shows anything, and it cannot say "done" on its own word.

## Pick the workflow

| | Look first | Product first |
|---|---|---|
| **For** | Trying a style; the idea may be unfinished | Building the real design; the product is decided |
| **Needs** | An inspiration site and an idea | A chosen DESIGN.md, a story map and a UX plan |
| **Makes** | DESIGN.md and a clickable prototype of a few screens | High-fidelity mockups of every screen of a release |
| **Read next** | `references/look-first.md` | `references/product-first.md` |

An inspiration site with no chosen DESIGN.md means Look first. "Build the mockups", "the MVP screens" or a named release means Product first. If you cannot tell, ask once.

## Two sources, two jobs

- **Look and feel** comes from the inspiration site and nothing else: colours, type, shapes, spacing, depth, motion.
- **Functionality** comes from the idea (a story map, PRD, business case or brief) plus competitor research. Use the research in the UX plan or a standalone file, whichever exists. Do no competitor research here: `create-ux-plans` runs it when a project has none. Competitors show what is possible, not what must be matched.

A competitor's colour or an inspiration site's feature does not cross over.

## Rules for both workflows

1. **DESIGN.md comes first.** Study the inspiration (`references/capture-inspiration.md`), write DESIGN.md in the concept's folder to the structure in design-review's `references/design-md-structure.md`, and pass it through `claude-forge:design-review` before building any screen. Run it with the Skill tool, not by hand: a builder checking its own file is what this rule exists to prevent. This is enforced: write `AGREED-LIST.md` first, and a hook then refuses every screen and build command in that folder until design-review has signed `DESIGN-REVIEW.md` for the current DESIGN.md. Editing DESIGN.md outside its settings block voids the signature. Tell design-review it was called by this skill, so it never stops the run: it settles what it can and returns any real choice, which waits for the end. Product first starts from a chosen DESIGN.md, so it skips the study and this review unless DESIGN.md changes.
2. **Build the whole list in one go.** Every screen on the agreed list, in every language and theme the project needs, before showing anything. Build in the concept's folder (`references/prototype.md`).
3. **Run the mechanical checks after building:** `check.cjs` and `render.cjs` from design-review, then `scripts/links.cjs` from this skill. Fix every FAIL. They prove the rules hold, not that the design is good.
4. **Hold the look against the inspiration yourself:** before the outside check, put your main screens beside the inspiration's pictures and go through DESIGN.md's signature list (`references/capture-inspiration.md`). A screen that passes every check and reads as a generic admin kit has failed: it is the most likely way this skill goes wrong. Fix it before going on.
5. **Pass the outside check before saying "done"** (`references/outside-check.md`): a separate agent given only DESIGN.md, the agreed list and the screenshots. If it fails, fix the screens and run it again. After three failed rounds, stop and report what still fails. Never soften a failure: the end report states it.
6. **Mockups live in code, not Figma.**

`scripts/` means this skill's folder. Scripts need Playwright: they look in the project, `NODE_PATH` and the global npm folder.

## The end report

Show the user, once, at the end:

- Where the concept is, and how to open it (the first page or the running app).
- The screens, as pictures.
- The outside check's result, including what it did not cover.
- Any real choices from design-review, with their pictures from `<folder>/review-choices/`.

## Common mistakes

- Starting screens before design-review has passed DESIGN.md.
- Stopping after the first screen to ask how it looks. The list is agreed; finish it.
- Copying the inspiration's pages. Its look carries over; its pages and functions do not.
- Letting a competitor's look in, or an inspiration's feature.
- Inventing product structure a UX plan already decides, or reusing an old prototype's screens as the product's structure.
- Writing "matches the inspiration" with no measured value behind it.
- Drawing placeholder shapes where the look needs photos. See `references/prototype.md`.
- Letting the required content crush the look: fitting every column by shrinking everything until the screen reads as an admin panel.
- Leaving scaffolding on the page: notes about the test, sample-data labels, a demo footer.
- Taking the outside agent's pass as covering what it could not see: behaviour, keyboard, real data.
