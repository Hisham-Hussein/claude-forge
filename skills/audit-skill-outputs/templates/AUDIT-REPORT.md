# Skill Output Audit: {skill_name}

## Metadata

| Field | Value |
|-------|-------|
| **Skill identifier** | {plugin}:{skill_name} |
| **Plugin** | {plugin} |
| **Skill name** | {skill_name} |
| **Skill root** | `~/.claude/plugins/marketplaces/{plugin}/skills/{skill_name}` |
| **Input file** | `{input_file_path}` |
| **Output file** | `{output_file_path}` |
| **Audit date** | {YYYY-MM-DD} |

> **Documents under review:**
> - Input: `{input_file_path}` (source document fed into the skill)
> - Output: `{output_file_path}` (document the skill produced)
> **Skill:** `{plugin}:{skill_name}` at `~/.claude/plugins/marketplaces/{plugin}/skills/{skill_name}`
> **Methodology:** Exhaustive gap analysis, root cause tracing, generalizable fix proposals

---

## Executive Summary

**Coverage Score: {X}% (weighted) | {adequate_count} of {total_count} items fully adequate**

{2-3 paragraph overview covering:
- Coverage percentage and gap counts by type (MISSING, PARTIAL, DISTORTED, ADEQUATE)
- Top systemic skill issues (the 2-3 root causes that explain the most gaps)
- The proportion of gaps that would be resolved by fixing the top systemic issues}

---

## Part 1: Gap Analysis

### Coverage Summary Table

| # | Input Requirement / Detail | Classification | Impact | Output Section |
|---|---------------------------|---------------|--------|----------------|
| 1 | {requirement from input file} | ADEQUATE / MISSING / PARTIAL / DISTORTED | -- / HIGH / MED / LOW | {output section or N/A} |
| ... | ... | ... | ... | ... |

{Every meaningful item from the input file must appear in this table. ADEQUATE items are listed for completeness.}

### Coverage Score

- **Total items evaluated:** {N}
- **Adequate:** {N}
- **Partial:** {N} — HIGH: {N}, MED: {N}, LOW: {N}
- **Missing:** {N}
- **Distorted:** {N}

**Weighted Score Calculation:**

| Classification | Count | Weight | Contribution |
|---------------|-------|--------|-------------|
| Adequate | {N} | 1.00 | {N.00} |
| Partial (HIGH) | {N} | 0.25 | {N.NN} |
| Partial (MED) | {N} | 0.50 | {N.NN} |
| Partial (LOW) | {N} | 0.75 | {N.NN} |
| Missing | {N} | 0.00 | 0 |
| Distorted | {N} | 0.00 | 0 |
| **Total** | **{N}** | | **{sum} / {total} = {X}%** |

{If duplicates exist, note them and provide a deduplicated count.}

### Detailed Gap Analysis

{For each non-ADEQUATE item, provide a detailed analysis block:}

#### Gap #{N} -- {Short description}

- **Input reference:** {exact text or requirement from the input file, with location}
- **Classification:** MISSING / PARTIAL / DISTORTED
- **Impact:** HIGH / MEDIUM / LOW -- {brief explanation of why}
- **What the output says:** {what the output file contains for this item, or "N/A" if absent}
- **Recommended fix for current output:** {exact content or section to add/modify in the output file}

---

## Part 2: Root Cause Analysis

### Root Cause Summary Table

| Gap # | Root Cause Category | Specific Source File | Fix Complexity |
|-------|--------------------|--------------------|----------------|
| {N} | Template gap / Instruction gap / Methodology gap / Command gap / Structural limitation | {file} ({location}) | Low / Medium / High |

### Top Systemic Issues

{Identify the 2-4 root causes that, if fixed, would eliminate the most gaps. Order by impact (most gaps resolved first).}

#### Issue {N}: {Name}

- **Gaps caused:** #{X}, #{Y}, #{Z}
- **Root cause:** {Detailed explanation of why the skill fails here. Reference specific lines, sections, or absence of content in the skill source files.}
- **Proposed fix:** {Specific changes with file paths and exact content. Use the same format as the upstream fix blocks below for consistency.}

### All Root Causes by File

{Group every root cause by which skill source file it belongs to.}

#### SKILL.md Issues

| # | Issue | Location | Gaps Affected | Proposed Fix |
|---|-------|----------|---------------|-------------|
| S{N} | {issue description} | {section/step} | #{X}, #{Y} | {brief fix} |

#### Template Issues

| # | Issue | Location | Gaps Affected | Proposed Fix |
|---|-------|----------|---------------|-------------|
| T{N} | {issue description} | {section} | #{X}, #{Y} | {brief fix} |

#### Methodology Issues

| # | Issue | Location | Gaps Affected | Proposed Fix |
|---|-------|----------|---------------|-------------|
| M{N} | {issue description} | {section} | #{X}, #{Y} | {brief fix} |

#### Command Issues

| # | Issue | Location | Gaps Affected | Proposed Fix |
|---|-------|----------|---------------|-------------|
| C{N} | {issue description} | {location} | #{X}, #{Y} | {brief fix} |

{If a category has no issues, state "No issues identified." Do not omit the section.}

---

## Recommendations

### Immediate (Fix the current output file)

{Priority-ordered list of fixes to apply to the current output file, from highest to lowest impact:}

| Priority | Fix | Impact |
|----------|-----|--------|
| 1 | {fix description with gap references} | HIGH / MED / LOW |
| ... | ... | ... |

### Upstream (Fix the skill itself)

{Priority-ordered list of generalizable skill improvements. Top systemic issues first, then individual fixes.}

{IMPORTANT: Each upstream fix MUST follow the Fix Format Contract below. The `/apply-skill-fixes` command parses these blocks programmatically.}

#### Fix U-1: {Title}

- **Priority:** Critical | High | Medium | Low
- **Target file:** `{relative path from skill root, e.g., SKILL.md, templates/BUSINESS-CASE.md}`
- **Action:** ADD | REPLACE | RESTRUCTURE
- **Location:** {Section name, or "after line X", or "new section after Y"}
- **Current content:** (for REPLACE only)
```
{exact text being replaced}
```
- **Proposed content:**
```
{exact text to insert or replace with}
```
- **Rationale:** {Why this is a generalizable improvement, not a case-specific patch}

#### Fix U-2: {Title}

- **Priority:** Critical | High | Medium | Low
- **Target file:** `{relative path from skill root}`
- **Action:** ADD | REPLACE | RESTRUCTURE
- **Location:** {location}
- **Proposed content:**
```
{exact text}
```
- **Rationale:** {generalizability explanation}

{Continue for all upstream fixes: U-3, U-4, etc.}

---

## Appendix: Verification Checklist

- [ ] Every section of the input file has been compared against the output file
- [ ] Every gap has a root cause traced to a specific skill source file
- [ ] Weighted coverage score math is correct (sum of weighted contributions / {total_count} = {X}%)
- [ ] All recommended upstream fixes are generalizable (would help any future project)
- [ ] All upstream fixes follow the Fix Format Contract (U-{N} numbering, target file, action, location, content)
- [ ] Top systemic issues genuinely address the highest number of gaps
- [ ] Report metadata header is filled with correct values

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | {YYYY-MM-DD} | Skill Output Audit | Initial audit of {skill_name} output |
