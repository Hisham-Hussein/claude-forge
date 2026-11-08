# Look first: try a style

For when the look and feel matters most and the product idea may still be unfinished. Output: a DESIGN.md and a clickable prototype of a few representative screens. It captures the look, not the full page list.

## 1. Find the idea

Look in the project and use the most developed description: a story map, then a PRD or business case, then a product brief. Screens, a UX plan and competitor research help if they exist; none is required.

If you find no description, offer to help refine the idea, for example through `superpowers:brainstorming`; the refined idea is the product brief. If the user declines, the idea as they gave it is enough.

Then settle "Decisions first" in SKILL.md. These two are the only stops in this workflow, and both come before any work; with the answers in the project, there are none.

## 2. Agree the list

Use the screens the run was given. With none, pick three from the idea that test the style hardest, such as a dense list, a detail page with charts, and a working page, and name them at the start. Do not wait for an answer.

Use the languages and themes from "Decisions first".

**Comparing sites:** every run gets the same screens and the same sample data, so only the style differs. Use the sample data file you are given. With none, write `sample-data.json` beside the concept folders and reuse it in later runs. Sample data looks real: full names, odd lengths, missing values.

Write the list to `<concept>/AGREED-LIST.md`: each screen, what must be on it, its source, and the languages and themes.

## 3. Choose the libraries

If the project has a component stack, or the user names libraries, build the prototype on them in an `app/` folder and follow the four rules below. With neither, the prototype is plain HTML as in `prototype.md`, and this step does not apply: say so in the end report.

A toast, chart or command menu built from nothing misses the details that make a product feel finished. Libraries bring those details and someone else's taste, but only if they are left to do their work.

1. **Name the libraries before building.** The project's own rules and installed packages come first (its front-end rules, `package.json`, `components.json`). For each job they leave open, such as toasts, charts, changing numbers or searchable lists, run `pick-ui-library` with the Skill tool and one specific task ("which library for toasts?"), because with no question it only greets you. If that skill is not installed, stop and say so instead of guessing. Mark anything neither source covers as your own pick. Write each job and its library in `AGREED-LIST.md` and in DESIGN.md §5.
2. **Change only colours, fonts and radius on the foundation components.** Those three carry the look. Install through the library's CLI or registry, and keep its sizes, spacing and component code as they come, so controls stay consistent with each other.
3. **Leave on what each library does by default:** chart animation and tooltips, toast stacking, overlay behaviour, label spacing. A static chart or a suppressed toast throws away the reason for using the library. If a default truly has to change, write the reason in DESIGN.md and name it in the end report.
4. **Test that the behaviour works, in use.** Hover and tap every chart, trigger the toasts, drive the menus by keyboard, and turn on reduced motion. Repeat under each language's browser locale, not only the page's language, since a library can read the browser's settings. A screenshot cannot show a chart that never moves.

`check.cjs`, `links.cjs`, `shots.cjs` and `walk.cjs` read HTML pages, so they do not cover an app. Walk the same checks in a real browser with Playwright, and say in the end report which ones you did by hand.

## 4. Study, write, review

Follow rule 1 in SKILL.md. Use a new folder for the concept; never overwrite an earlier one.

## 5. Build

Follow `prototype.md`, or the project's stack if step 3 applies. If a UX plan covers a screen, its layout, states and wording apply, and only the look is yours: follow `plan-match.md`. If not, draw the screen from the idea and the competitor research.

## 6. Check and finish

Rules 3 to 5 in SKILL.md, then the end report.
