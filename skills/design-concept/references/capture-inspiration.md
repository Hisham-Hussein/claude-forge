# Studying the inspiration

The look is only as good as this study. Experiment after experiment, a thin study gave a thin design: take the time here, because every later step inherits it. v1 takes websites, Webflow templates above all.

## Capture

Keep everything in `<concept>/inspiration-<source>/`. If that folder already holds a capture, read it, and add what is missing.

```bash
node <skill>/scripts/capture.cjs <concept>/inspiration-<source> <url> [<url> ...]
```

Give it every kind of page the site has: home (each version, if the template has several), a list or grid page, a detail page, an about or pricing page, a form. Find them from the navigation; a template's own style guide page, if it has one, is the best page there is. For each page and width the script saves the first screen, the full page, measured styles, and frames of the page scrolling slowly and of its first seconds.

If a site will not open, say so and stop: a concept from memory of a site is the failure this skill exists to prevent.

## Look

Open the pictures and read `*-styles.json`. Do not rely on the numbers alone: what makes a site good is usually how the parts work together.

Write `inspiration-<source>/README.md`:

- **Source:** the full link to the site, as the first line, and the link of each page captured.
- **Measured:** a table of colours (with where each is used), fonts with sizes, weights, line heights and tracking, corners, borders, shadows, spacing, section gaps, button and pill padding. Every value from the capture.
- **Motion:** what moves, when (load, scroll, hover), how far, how long, what easing. Say which frames show it. Animation is often why someone chose a site.
- **What makes it work:** five or so observations, each pointing at a picture.
- **Where it stops:** what the site never shows that a product needs: tables, forms, errors, dense data, a second theme, right to left. These are the design's own work, and the place concepts go wrong.

## From study to DESIGN.md

Read the project's standing design decisions first (its design README, brand notes, what the user chose before): a font or a language rule the user already settled binds every concept. A general "avoid" list does not remove something the inspiration itself uses: if the site has a gradient or a glow, it stays, because the look comes from the site.

Each rule in DESIGN.md either carries a measured value or says why it departs from one. Good reasons: WCAG contrast, density a work tool needs. "Simpler" is not one.

If a font the look depends on is paid, look for its licence and price, build with the closest open-licence match, name it in §3, and list the swap as a real choice with pictures of both in `review-choices/`, so the user decides whether to buy it. Never swap a signature font silently.

For what the site does not show, extend its logic, do not fall back to a default kit: a site of hairlines and flat fills gets tables of hairlines and flat fills. A missing second theme is built from the site's palette; if the user named which theme the site should inspire, follow that.

## Signatures

Name the three to six moves that make this site itself, and put them in DESIGN.md's header as a numbered **Signatures** list: for example, real photos carrying all the colour, huge light display titles, mono labels, calm rows with air between them. Each says how it shows up on a product screen, including a dense one. Every main screen must show them; they are what the rest of the run protects.

Before moving on, look at DESIGN.md beside the pictures and ask: would someone who knows the site recognise it from this file alone? If not, the study is not finished.
