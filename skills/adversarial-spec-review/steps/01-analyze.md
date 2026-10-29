<step_1>
**Step 1: Read and Analyze the Spec**

Read the spec file completely. Then analyze it for domain dimensions:

1. **Extract section structure** — list all ## headings and their topics
2. **Identify referenced files** — find all file paths, module names, function names, interface names mentioned in the spec. These are the files reviewers must read.
3. **Scan for domain signals** — for each archetype in reviewer-archetypes.md, count how many selection signals appear in the spec
4. **Note the spec's scope** — is it a narrow change (1-2 sections of concern) or a broad design (5+ interacting systems)? Name the 3 riskiest areas.

Output: a mental map of the spec's domain dimensions and which archetypes match.
</step_1>

