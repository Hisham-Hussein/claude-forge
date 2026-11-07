---
name: design-review
description: Reviews a design against its own DESIGN.md, the project's front-end constitution if it has one, and Material 3 principles. Use when asked to review, critique, audit or check UI for design quality or accessibility - screens, HTML mockups or a design concept's folder, screenshots or PDFs, front-end code, a change to a DESIGN.md, or a whole new DESIGN.md (is it complete, consistent, true to its inspiration) - in any language, left to right or right to left, light or dark; also when asked whether a screen meets Material Design 3, and when another skill such as design-concept calls for a review. It reviews designs; it does not produce them.
---

# Design review

Review a design against its own rules. Order on a conflict: the project's constitution > the concept's DESIGN.md > Material 3. Material gives principles, never the look. Where DESIGN.md and Material disagree, DESIGN.md is right and there is no finding. Where DESIGN.md is silent, Material decides.

## What to review against

- **The concept:** a folder and its DESIGN.md. Use the ones you are given. Otherwise use `<folder>/DESIGN.md`, then the project's own (`design/DESIGN.md`, `DESIGN.md`). DESIGN.md's header can name another file as its reference CSS and screens. With no DESIGN.md at all, say so and review against Material and WCAG only.
- **Mockup layout:** pages, CSS and JS in `src/`, renders in `renders/`, the captured inspiration in `inspiration-<source>/`.
- **The constitution** is optional. Use the file you are given, or the one DESIGN.md's header links, or `docs/frontend/CONSTITUTION.md`. If there is none, skip every constitution step and do not report its absence.
- **Who decides:** the user, or, when another skill called you, the end of that run ("Called by another skill").

`scripts/` below means this skill's folder. Run the scripts from the project (`node <skill>/scripts/check.cjs <folder> --design <DESIGN.md>`; `--design` is needed only when DESIGN.md is not in the folder). They need Playwright: they look in the project, `NODE_PATH` and the global npm folder.

## What each input can show

Every check in `references/` carries a tag after its ID. Walk only the tags your input gets:

| Input | Walk checks tagged | Also |
|---|---|---|
| PDF, screenshot, image | `see` | Render a PDF with `pdftoppm -r 144 -png`. Measure contrast from sampled pixels and say so in the evidence. |
| Mockup HTML (a concept's folder) | `see`, `source` | Run check.cjs and render.cjs; look at the renders. |
| Product code (TSX, a running screen) | `see`, `source`, `product` | check.cjs does not run here: walk the `auto N` checks by hand. |
| A change to DESIGN.md | none | Follow "Reviewing a DESIGN.md change". |
| A whole new DESIGN.md | none | Follow "Reviewing a whole DESIGN.md". |

Skip the checks, and the parts of a check (an `aria-` attribute in a `see` check), that your input cannot answer, without listing them. End the report with one line naming what it could not show ("Not judged from a PDF: keyboard, focus, names, markup, motion").

Numbers on mockups and images are invented. Judge only how values are shown (the missing-value mark, number and date formats, units in column heads); never sums, totals or whether a value is real. Those are findings in product code only.

## Reviewing a screen

1. **Read** the constitution, if any, and DESIGN.md in full, every time (they change). Note §10 (open items) and §11 (departures).
2. **Mockups only:** run `scripts/check.cjs` on the folder. Each FAIL line is a finding (rule: DESIGN.md §9.N). A check tagged `auto N` is covered when check N passes: do not re-check it by hand, except the part the tag says the check misses. If check 0 fails because the settings are missing, the page checks cannot run: that is a Major finding, and you walk the `auto N` checks by hand.
3. **Look** at what you have: the source with line numbers, and the picture in each language and theme you were given. For mockups, `scripts/render.cjs` writes `renders/<page>.png` and `<page>-dark.png`.
4. **Walk the checks** with your input's tags in the files for the areas the target touches (table below); a full page touches all four files, so walk them all, not only the ones where a defect shows. List them with ``grep -n '`see`' references/<file>.md``, adding `source` and `product` when your input gets them. A check about something the concept does not have (right-to-left pages, charts) does not apply.
5. **Report** every finding in the format below.
6. **Split the findings.** A finding whose fix DESIGN.md, the constitution or WCAG already settles is technical: fix it, re-run step 2, and list it as fixed. An Advisory (M3) finding is settled by Material: apply its answer, add the rule to DESIGN.md with the Material URL, and list it. Only a choice neither DESIGN.md nor Material settles, or one where Material's answer is Material's look ("Never report"), is a real choice, and it goes to the user as pictures: render each option from the page (Playwright, the same width and theme), label it, and send it. Never describe a design choice in text alone.

| Target touches | Read |
|---|---|
| contrast, keyboard, focus, names, landmarks, layout, widths, 200% text, right-to-left layout | `references/foundations-accessibility-layout.md` |
| colour tokens, type, corners, shadows, motion, icons, spacing, charts | `references/styles-motion-type.md` |
| any component in DESIGN.md §5 | `references/components.md` (only the components used) |
| any words: labels, buttons, messages, numbers, dates, alt text | `references/content-writing.md` |

## Reviewing a DESIGN.md change

1. **Read** the change (`git diff`, or the proposed text), then DESIGN.md and the constitution, if any, in full.
2. **Consistency:** does a changed rule contradict another section (§9's checklist and settings included) or the constitution? A contradiction is Major; Blocker if the new rule breaks WCAG AA or the constitution.
3. **Material 3:** find the checks that cite the changed section (`grep -n '§5 Toast' references/*.md`) and open their Material pages. Where the change moves away from a Material principle that §11 does not list, report Advisory with the Material URL: keep it and add it to §11 with the reason, or drop it. A departure §11 already lists is not raised.
4. **Run** `scripts/check.cjs --structure`. If the change touches colours, type sizes, spacing or corners, run the full check too (check 8 compares DESIGN.md with the CSS).
5. **Report and stop.** A new or changed rule is the user's choice; correcting a contradiction or a stale line is technical (step 6 above).

## Reviewing a whole DESIGN.md

For a new concept's DESIGN.md, before any screen is built from it. Read `references/design-md-structure.md` first.

1. **Complete:** run `scripts/check.cjs --structure`; each FAIL is Major. Then read each section against the structure's "Must hold" column: a gap a builder would have to guess at is Major, a thin one Minor.
2. **Consistent:** no section contradicts another, and the settings block agrees with §3 and §4. A contradiction is Major. Compute the contrast of every text and fill pair in §2, in each theme: a pair below WCAG AA is a Blocker.
3. **True to the inspiration:** read everything in `inspiration-<source>/`: README, measured styles, findings, screenshots. It judges the look only (colours, type, shapes, spacing, depth, motion); pages and functions differ on purpose and are never compared. Report a value that differs from what was measured with no reason given, and anything distinctive in the capture that DESIGN.md left out; Major if a person would notice, Minor if not. A departure with a reason, such as a darker grey to pass contrast, is not a finding. With no inspiration folder, say "Not judged: true to the inspiration".
4. **Material 3:** where DESIGN.md departs from a Material principle, §11 lists it with the reason; if not, report Advisory with the URL.
5. **Settle:** apply "Split the findings". Whatever the inspiration or the other sections already answer is technical: write it in. What is left is a real choice, and so is any conflict between two of them, such as an inspiration's look that breaks a rule in §4: rewriting a rule to resolve it is a decision, not a fix. Change only DESIGN.md here; screens are judged in their own review.

## Called by another skill

When a skill such as `design-concept` runs you in the middle of its own work, the run must not stop. Do everything above, except:

- Ask nothing. Fix all technical findings and apply Material's answers, as in step 6.
- For each real choice, keep the design as it stands, render the options, save the pictures in `<folder>/review-choices/`, and list them. With no screens yet, render each option on a small sample of the component. A judgement call you would mention is a real choice: list it there, never as a side note.
- Return the findings table, what you fixed, and that list. The calling skill shows the list with its result.

## Finding format

| # | Severity | Finding | Rule | Evidence | Proposed fix |
|---|---|---|---|---|---|
| 1 | Major | One plain sentence | DESIGN.md §5 Toast; CO-56 | `list.html:88`; measured 3.1:1 | What to change |

- **Rule** is a DESIGN.md or constitution section, or a full `https://m3.material.io/...` URL, plus the question ID. A finding with no rule is not a finding.
- **Evidence** is a file:line, a render or page name, or a measured value. No evidence, no finding.
- **Severity:**
  - **Blocker:** breaks the constitution, WCAG AA (contrast, keyboard, names), or, in product code, honest data (a wrong, made-up or defaulted value).
  - **Major:** breaks a DESIGN.md rule people will notice.
  - **Minor:** breaks a DESIGN.md rule in a small way.
  - **Advisory:** a question marked **M3**: DESIGN.md has no rule, so Material's principle decides (step 6).

## Never report

- **DESIGN.md §11 departures** and **§10 open items:** whatever the concept lists there is decided or known.
- **Material's look:** tonal palettes, Roboto, Material Symbols, FABs, bottom navigation or rail, tonal surfaces and elevation, ripples, 48dp targets on desktop, 56dp fields, the 3dp focus ring, a 32% scrim.
- **The constitution's code rules** (classes, no inline `style`) apply to product code, not to mockup HTML.

You may list these in one line under "Not raised (decided)".

## Common mistakes

- "Material says" with no URL. Copy the URL from the reference file's key table.
- Bringing a value from another concept. The checks name sections on purpose: read the value from this DESIGN.md.
- Comparing screens or functions with the inspiration. It judges DESIGN.md's look, and only that.
- Sending the user a choice Material already answers (pill spacing, where bulk actions go). Apply Material and record it in DESIGN.md.
- Asking a picture about keyboard, focus, names or markup, or a mockup about behaviour. Walk only your input's tags.
- Checking numbers on a mockup or image. In product code, recompute a total from every source and check what it claims to cover before calling it wrong.
- Measuring contrast or target sizes by hand when check.cjs passed them.
- Judging a whole page from one example. Count with grep: every name in `<bdi>`, every icon button with an `aria-label`.
- Asking the user about a technical fix, or asking them to pick between designs described only in words.
