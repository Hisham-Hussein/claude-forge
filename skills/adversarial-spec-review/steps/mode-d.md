<mode_d>
**Mode D: Independent Reviewer Loop** lives in the `reviewing-documents` skill, which runs it on any document.

Stop this workflow, delete any `.review-state/` this review created, and invoke `reviewing-documents` with the spec's path and the user's words. It owns the whole review from there, including its own gates and finish.
</mode_d>
