# The outside check

You built it, so you are the wrong judge of it. Spawn a separate agent that has not seen this run. Give it only:

- the concept's DESIGN.md
- `AGREED-LIST.md` (`RELEASE-LIST.md` in Product first)
- the UX plan's sections for these screens, when a plan covers them
- the pictures from `scripts/walk.cjs` (`renders/walk/`): every kind of control, opened
- the screenshots from `scripts/shots.cjs` (`renders/check/`), a set the agent can really open: each screen in every language and theme at 1440px, each screen at phone width in the main language, each state, dialog and menu once, with long pages cut into slices.

Never give it the inspiration site, a competitor, or your notes. The pages and functions differ from both on purpose, so a comparison would only reward copying.

Use the prompt below as it stands, filling the paths. With no UX plan, leave out the UX plan line, Part 3 and the UX plan clause in the last sentence. `PLAN-MATCH.md` is your own table, so do not give it: the agent reads the plan itself.

```
You are checking a finished design. You did not build it. Report only what the files show.

DESIGN.md: <path>
Agreed list: <path>
Screenshots: <folder>
Controls in use: <concept>/renders/walk
UX plan: <path and section names>

Part 1, Look. Open every screenshot. First hold each main screen against DESIGN.md's Signatures and §1 Principles: does the screen actually show them, or could it be any admin template? A broken signature or principle fails the check, even when every token is right. Then, does it match the rest of DESIGN.md: colours, type, corners, spacing, depth, component rules, right-to-left rules? Would a person take this for a finished product? Placeholder images, cells wrapping to three lines and names cut in the middle count against it. The "Demo state" selector and notes about sample data are there on purpose: ignore them. Cite the section and the screenshot for each mismatch.

Then open every picture in "Controls in use": each shows a menu, dialog or panel opened from a page. Each must match the screens around it. A plain browser-default look, text overlapping or cut, a control spilling out of its box, or a scrollbar showing where none is needed fails the check.

Part 2, Completeness. For each item on the agreed list: is the page there, in each language and theme listed, with every function and state a screenshot can show, and finished? List the rest under NOT COVERED. Placeholder text, an empty region, or a state that cannot be seen counts as missing, apart from the selector and notes named above.

Part 3, Plan match. Go through the UX plan's sections for these screens line by line, reading its notation first. For each control, field, column, section and state it names, find it in the screenshots: is it there, in the plan's order, as the same kind of control? A select shown as pills, a missing column or tag, or sections in another order is a mismatch, whatever the look. Also fail any list of options laid out in full when that kind of list, such as countries or cities, can grow far past what fits on screen. A mismatch named under "Departures from the UX plan" in the agreed list is not a fail, but quote it so the reader sees it. It is a fail if the plan could have been built as written, or the reason given is only the look, crowding or the sample's size. Cite the plan's line and the screenshot.

Answer in this form:
VERDICT: PASS or FAIL
FAILS: one line each (screen, what is wrong, rule or list item)
COVERED: what you could judge
NOT COVERED: what screenshots cannot show

FAIL if any list item is missing or unfinished, any screen breaks a DESIGN.md rule a person would notice, or the screens differ from the UX plan in a way the list does not name. Small flaws go under FAILS marked "minor" and do not fail the check.
```

## After the verdict

- **PASS:** go to the end report. Include COVERED and NOT COVERED.
- **FAIL:** fix the screens, re-run the mechanical checks and renders, and spawn a fresh agent with the same inputs. A fresh one, so it does not remember being told what was fixed.
- **Disagreeing with a FAIL:** fix DESIGN.md only if it is really wrong, and run design-review on that change. Never drop an item from the list to get a pass.
- **Third FAIL:** stop. Report what still fails, with the agent's lines as they stand.

Save each round's answer in `<concept>/OUTSIDE-CHECK.md`.
