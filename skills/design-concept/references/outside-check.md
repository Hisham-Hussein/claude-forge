# The outside check

You built it, so you are the wrong judge of it. Spawn a separate agent that has not seen this run. Give it only:

- the concept's DESIGN.md
- `AGREED-LIST.md` (`RELEASE-LIST.md` in Product first)
- the screenshots from `scripts/shots.cjs` (`renders/check/`), a set the agent can really open: each screen in every language and theme at 1440px, each screen at phone width in the main language, each state, dialog and menu once, with long pages cut into slices.

Never give it the inspiration site, a competitor, or your notes. The pages and functions differ from both on purpose, so a comparison would only reward copying.

Use the prompt below as it stands, filling the three paths.

```
You are checking a finished design. You did not build it. Report only what the files show.

DESIGN.md: <path>
Agreed list: <path>
Screenshots: <folder>

Part 1, Look. Open every screenshot. First hold each main screen against DESIGN.md's Signatures and §1 Principles: does the screen actually show them, or could it be any admin template? A broken signature or principle fails the check, even when every token is right. Then, does it match the rest of DESIGN.md: colours, type, corners, spacing, depth, component rules, right-to-left rules? Would a person take this for a finished product? Placeholder images, cells wrapping to three lines and names cut in the middle count against it. The "Demo state" selector and notes about sample data are there on purpose: ignore them. Cite the section and the screenshot for each mismatch.

Part 2, Completeness. For each item on the agreed list: is the page there, in each language and theme listed, with every function and state a screenshot can show, and finished? List the rest under NOT COVERED. Placeholder text, an empty region, or a state that cannot be seen counts as missing, apart from the selector and notes named above.

Answer in this form:
VERDICT: PASS or FAIL
FAILS: one line each (screen, what is wrong, rule or list item)
COVERED: what you could judge
NOT COVERED: what screenshots cannot show

FAIL if any list item is missing or unfinished, or any screen breaks a DESIGN.md rule a person would notice. Small flaws go under FAILS marked "minor" and do not fail the check.
```

## After the verdict

- **PASS:** go to the end report. Include COVERED and NOT COVERED.
- **FAIL:** fix the screens, re-run the mechanical checks and renders, and spawn a fresh agent with the same three inputs. A fresh one, so it does not remember being told what was fixed.
- **Disagreeing with a FAIL:** fix DESIGN.md only if it is really wrong, and run design-review on that change. Never drop an item from the list to get a pass.
- **Third FAIL:** stop. Report what still fails, with the agent's lines as they stand.

Save each round's answer in `<concept>/OUTSIDE-CHECK.md`.
