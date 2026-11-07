# Content writing

Yes/no checks. "Yes" passes. Walk the groups the target touches. Every value comes from the concept's DESIGN.md, which the skill reads first; a check names the section, never the value.

The tag after each ID says what the target must include to answer the check: `see` (a picture is enough), `source` (needs the HTML, CSS or TSX), `product` (needs product code). SKILL.md says which tags each input gets.

Each line ends with its source: a DESIGN.md section, a Material page (key below), and `auto N` when `scripts/check.cjs` check N already tests it on the mockups.

**M3** before a question means Material decides when DESIGN.md has no rule on it (severity: Advisory; SKILL.md says how to apply it). If DESIGN.md has a rule, DESIGN.md is right.

| Key | Material page |
|---|---|
| ux | https://m3.material.io/foundations/content-design/style-guide/ux-writing-best-practices |
| words | https://m3.material.io/foundations/content-design/style-guide/word-choice |
| grammar | https://m3.material.io/foundations/content-design/style-guide/grammar-and-punctuation |
| global | https://m3.material.io/foundations/content-design/global-writing/overview |
| global-words | https://m3.material.io/foundations/content-design/global-writing/word-choice |
| notifications | https://m3.material.io/foundations/content-design/notifications |
| alt | https://m3.material.io/foundations/content-design/alt-text |
| writing | https://m3.material.io/foundations/writing/best-practices |
| app-bars | https://m3.material.io/components/app-bars/guidelines |
| truncation | https://m3.material.io/foundations/writing/text-truncation |
| dialogs | https://m3.material.io/components/dialogs/guidelines |

## Voice and wording

- **CW-1** `see` Is every title, label, heading, menu item and button in §8's case in the source text, with capitals only from CSS where §3 and §11 allow them, and no sentence or message in all caps? *DESIGN.md §8 Voice; grammar*
- **CW-2** `see` Does the copy speak to "you", never "we", "I" or the product's name as the speaker, and never mix "my" with "your" on one screen? *DESIGN.md §8 Voice; ux*
- **CW-3** `see` Are abbreviations few, with no "e.g." or "etc."? *DESIGN.md §8 Voice; words, global*
- **CW-4** `see` Is there no technical jargon or internal name (server, database, API, error codes) in what the person reads? *DESIGN.md §8 Messages; global-words*
- **CW-5** `see` Does each word keep one meaning across the screen ("filter", "save", "list")? *DESIGN.md §8 Voice; global-words*
- **CW-6** `see` M3 Does no sentence start with a bare "This" or "That", and no short string lean on "it"? *global-words*
- **CW-7** `see` Is there no idiom or slang in fixed copy? *global*
- **CW-8** `product` M3 In product code, does every string with a placeholder, a local reference or a word with two meanings carry a note for translators? *global*
- **CW-9** `product` Are statuses, categories, countries and formats named as the data source names them? *DESIGN.md §8; constitution*

## Punctuation and numbers

- **CW-10** `see` M3 Do one-sentence labels, tooltips, toasts and notices follow one period rule, the same in both languages? *grammar*
- **CW-11** `see` M3 Are ranges written with an en dash and no spaces ("5,000–7,000"), or with "to" in range fields? *grammar*
- **CW-12** `see` M3 Is there no em dash inside a sentence (§8's missing-value mark excepted)? *grammar*
- **CW-13** `see` Does no button or menu item end in an ellipsis, while in-progress states ("Saving…") do? *DESIGN.md §5 Save state; grammar*
- **CW-14** `see` Is there no exclamation mark anywhere? *DESIGN.md §8 Voice; grammar*
- **CW-15** `see` M3 Are ampersands used only in headings, column heads, navigation and buttons? *grammar*
- **CW-16** `see` Are numbers in §8's format, prices with thousands separators and the currency named once nearby? *DESIGN.md §8 Numbers; grammar*
- **CW-17** `see` Are dates in §8's format, recent updates relative ("3 days ago") if §8 says so? *DESIGN.md §8 Dates*
- **CW-18** `see` Does every missing value show §8's missing-value mark, never "Not available", "N/A", 0 or a guessed default? *DESIGN.md §1.7, §8; constitution*

## Messages

- **CW-19** `see` Does every error say what failed in the person's terms and the one next step, with no apology ("Sorry", "Please", "Thank you")? *DESIGN.md §8 Messages; ux*
- **CW-20** `see` Does every dialog title make a specific statement or question (no "Are you sure?", no "Warning!"), and every destructive confirmation say the result and whether it can be undone? *DESIGN.md §8 Messages; dialogs, ux*
- **CW-21** `see` Do empty states say why there is nothing and offer ways out with counts? *DESIGN.md §5 Empty state, §8; ux*
- **CW-22** `see` Is every toast one short line with at most one verb action ("Undo")? *DESIGN.md §5 Toast; ux*

## Images and charts

- **CW-23** `source` Do photos next to the person's name, and decorative images, have `alt=""`? *alt*
- **CW-24** `source` Does every informative image (post thumbnail, a logo that is a link) have alt text of 125 characters or fewer, without "Image of"? *alt*
- **CW-25** `source` Does every chart have a one-sentence name giving its data and what it shows ("Total followers by month: 1.5M … 2.3M"), with the table view holding the numbers? *DESIGN.md §5 names table "Chart", §6 "Accessible"; alt*

## Length and truncation

- **CW-26** `see` Do layouts leave room for text 1.5 times longer than English, and for any script that runs longer at its size? *DESIGN.md §8 Truncation; global*
- **CW-27** `product` Can the full text of every truncated name, handle, note or campaign name be reached by hover, focus or tap, or on the next screen? *DESIGN.md §8 Truncation; truncation*
- **CW-28** `see` Does right-to-left text cut at word ends or by width, never inside an isolated handle? *DESIGN.md §7; truncation*

- **CW-29** `see` Are page titles, navigation labels and dialog titles never truncated? *DESIGN.md §8 Truncation; truncation, app-bars*

## Notifications and emails (only when the target includes them)

- **CW-30** `see` Does each notification lead with what matters most, title under 29 characters and body under 40 (one line) or 80 (two)? *notifications*
- **CW-31** `see` Does it name the weekday and date instead of "today" or "tomorrow" (on screen, relative dates stay)? *DESIGN.md §8 Dates; notifications*
- **CW-32** `see` Does the title avoid dynamic text, or fall back to a version that fits, and is there an opt-out in context? *notifications*
