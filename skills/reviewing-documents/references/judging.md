# Judging findings

Accuracy is the only measure of a review. Finding issues is not the goal; readiness is. Zero findings is a valid result, and inflating a Minor is as wrong as hiding a Major.

## Rules

A **Critical or Major candidate** is any finding the reviewer rated so, or that you would.

1. **Verify every finding.** One reviewer means no second opinion, so check each against the actual sources. If the evidence can't settle it and a spike can't either, keep it one severity lower, marked unverified in the round report; a Minor that can't be verified is dropped.
2. **Discard what the brief leaves out.** A detail the next reader settles in their own work is not a flaw. Check before dismissing: would that reader know the concern exists without the document mentioning it? If not, it stays.
3. **Weigh every Critical or Major candidate, in writing.**
   - FOR: the strongest argument it is real, will be hit, and the next reader wouldn't catch it unaided.
   - AGAINST: the strongest argument it isn't, or that their normal checks would catch it.
   - Verdict: which wins, and a confidence score. Try to defeat the finding. If AGAINST is stronger or even comparable, it is not Major.
4. **Ask whether last round's fixes broke something.** Each round of fixes can create regressions.
5. **Judge the goal as a whole.** If the next reader uses this document literally, is its stated goal achieved? If not, that is a Critical candidate even when no single finding says so: weigh it under Rule 3. A goal the document can't reach at all goes to the owner.

A Major found in a late round is still Major: each round is a fresh review.

## Automatic limits, whatever the reviewer's framing

- The content is right but surrounding prose is imprecise: Minor at most.
- The document says the right thing, but not prominently: Minor at most.
- A gap the next reader's normal checks would catch: Minor at most.
- A concern beyond 10x realistic use: drop.
- Existing practice already handles it without the document's help: drop.

## Severity and confidence

"How confident am I that this is real, will be hit, and the reader wouldn't catch it unaided?" If the brief quotes a project severity standard, that standard decides the severity.

| Score | Meaning | Result |
|---|---|---|
| Below 60 | False positive, theoretical, or a nitpick | Drop |
| 60-79 | Verified real, but the next reader would likely catch it; also defence in depth, or a principle breach that breaks nothing | Minor |
| 80-100 | Verified real, will be hit, the reader wouldn't catch it unaided; or a stated principle broken in a way that breaks something | Major |

**Critical** is classed by nature, not score: following the document literally breaks the outcome, loses data or opens a security hole, and the AGAINST argument has no weight. A Critical candidate scoring below 80 needs another look.

"The fix is easy" never raises severity.
