#!/usr/bin/env python3
"""
trace-phase-stories.py — Extract user stories for a given phase

Traces from ROADMAP.md (SM-XXX IDs per phase) to USER-STORIES.md
(US-XXX stories with **Parent:** SM-XXX), outputting filtered markdown.

Usage:
    trace-phase-stories.py <phase-number> <roadmap-path> <user-stories-path>

Example:
    trace-phase-stories.py 1 .charter/ROADMAP.md .charter/USER-STORIES.md

Output:
    Filtered markdown containing only the US-XXX stories that belong
    to the specified phase's SM-XXX IDs, preserving original formatting.
"""

import re
import sys
from dataclasses import dataclass, field


@dataclass
class MatchResult:
    """Result of matching SM-XXX IDs against USER-STORIES.md blocks."""
    stories: list[str] = field(default_factory=list)       # matched blocks as markdown
    found_sm_ids: set[str] = field(default_factory=set)     # SM-XXX IDs that had matches
    us_ids: list[str] = field(default_factory=list)         # US-XXX IDs found (for manifest lookup)
    us_count: int = 0                                        # total stories found


def extract_sm_ids(phase_num: int, roadmap_text: str) -> list[str]:
    """Parse SM-XXX IDs from a phase section in ROADMAP.md.

    Finds the section starting with '#### PHASE-{phase_num}:' and collects
    all SM-XXX IDs until the next heading (##, ###, or ####).

    Returns a sorted, deduplicated list of SM-XXX IDs.
    """
    sm_ids: list[str] = []
    in_phase = False

    for line in roadmap_text.splitlines():
        # Detect start of target phase
        if re.match(rf"^####\s+PHASE-{phase_num}:", line):
            in_phase = True
            continue

        # Detect end of phase section (any heading level 2-4)
        if in_phase and re.match(r"^#{2,4}\s", line):
            break

        # Extract SM-XXX from table rows while inside the phase
        # Supports both simple (SM-001) and hierarchical (SM-1.2-01) formats
        if in_phase:
            for match in re.finditer(r"SM-\d+(?:\.\d+-\d+)?", line):
                sm_ids.append(match.group())

    # Deduplicate and sort
    return sorted(set(sm_ids))


def extract_matching_stories(
    sm_ids: list[str], user_stories_text: str
) -> MatchResult:
    """Single-pass extraction of matching story blocks from USER-STORIES.md.

    Algorithm:
      - When we see '#### US-XXX:', start buffering lines
      - When we see '---' or a higher-level header (##/###), flush the buffer
        if it contained a matching Parent field
      - Single pass, O(n)

    One SM-XXX can map to multiple US-XXX stories (one-to-many).
    """
    result = MatchResult()

    # Build a regex pattern that matches any of our SM-XXX IDs exactly
    # Using word boundary (\b) would not work well since SM-001 vs SM-00 needs
    # exact matching. We match the full SM-NNN token in the Parent field.
    sm_set = set(sm_ids)

    in_story = False
    buffer_lines: list[str] = []
    matched = False
    current_us_id: str | None = None

    def flush():
        nonlocal in_story, buffer_lines, matched, current_us_id
        if in_story and matched:
            result.stories.append("\n".join(buffer_lines))
            result.us_count += 1
            if current_us_id:
                result.us_ids.append(current_us_id)
        in_story = False
        buffer_lines = []
        matched = False
        current_us_id = None

    for line in user_stories_text.splitlines():
        # Story header: #### US-XXX: Title
        us_header_match = re.match(r"^#### (US-\d+)", line)
        if us_header_match:
            flush()
            in_story = True
            buffer_lines = [line]
            matched = False
            current_us_id = us_header_match.group(1)
            continue

        # End of story block: --- or higher-level header (## or ###)
        if re.match(r"^---$", line) or re.match(r"^#{2,3}\s", line):
            flush()
            continue

        # Inside a story block
        if in_story:
            buffer_lines.append(line)

            # Check for Parent match: **Parent:** SM-XXX
            # Supports both simple (SM-001) and hierarchical (SM-1.2-01) formats
            parent_match = re.search(r"\*\*Parent:\*\*\s+(SM-\d+(?:\.\d+-\d+)?)", line)
            if parent_match:
                parent_id = parent_match.group(1)
                if parent_id in sm_set:
                    matched = True
                    result.found_sm_ids.add(parent_id)

    # Flush final story if matched
    flush()

    return result


def format_output(
    phase_num: int, sm_ids: list[str], result: MatchResult
) -> str:
    """Format the final markdown output with header, stories, and trace summary."""
    lines: list[str] = []

    # Header
    lines.append(f"# Phase {phase_num} — Traced User Stories")
    lines.append("")
    lines.append(f"**SM-XXX IDs in this phase:** {' '.join(sm_ids)}")
    lines.append(f"**US-XXX IDs in this phase:** {' '.join(result.us_ids)}")
    lines.append(
        f"**US stories found:** {result.us_count} "
        f"(covering {len(result.found_sm_ids)} of {len(sm_ids)} SM-XXX IDs)"
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Story blocks separated by ---
    for story in result.stories:
        lines.append(story)
        lines.append("---")

    lines.append("")

    # Trace summary
    lines.append("## Trace Summary")
    lines.append("")
    lines.append(f"- **Phase:** {phase_num}")
    lines.append(f"- **SM-XXX IDs:** {len(sm_ids)}")
    lines.append(f"- **US-XXX stories found:** {result.us_count}")

    # Missing SM-XXX IDs
    missing = [sm for sm in sm_ids if sm not in result.found_sm_ids]
    if missing:
        lines.append(f"- **Missing (no US-XXX for SM-XXX):** {' '.join(missing)}")
        lines.append("")
        lines.append(
            "> **Warning:** The above SM-XXX IDs have no matching "
            "US-XXX story in USER-STORIES.md."
        )
        lines.append(
            "> Fall back to STORY-MAP.md for these stories' descriptions."
        )

    return "\n".join(lines)


def main() -> None:
    """CLI entry point with argument validation."""
    if len(sys.argv) < 4:
        print(
            "Usage: trace-phase-stories.py <phase-number> "
            "<roadmap-path> <user-stories-path>",
            file=sys.stderr,
        )
        print("", file=sys.stderr)
        print(
            "Example: trace-phase-stories.py 1 "
            ".charter/ROADMAP.md .charter/USER-STORIES.md",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        phase_num = int(sys.argv[1])
    except ValueError:
        print(
            f"Error: Phase number must be an integer, got: {sys.argv[1]}",
            file=sys.stderr,
        )
        sys.exit(1)

    roadmap_path = sys.argv[2]
    user_stories_path = sys.argv[3]

    # Validate files exist
    try:
        with open(roadmap_path, "r") as f:
            roadmap_text = f.read()
    except FileNotFoundError:
        print(f"Error: Roadmap file not found: {roadmap_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(user_stories_path, "r") as f:
            user_stories_text = f.read()
    except FileNotFoundError:
        print(
            f"Error: User stories file not found: {user_stories_path}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Step 1: Extract SM-XXX IDs from the target phase
    sm_ids = extract_sm_ids(phase_num, roadmap_text)

    if not sm_ids:
        print(
            f"Error: No SM-XXX IDs found for PHASE-{phase_num} in {roadmap_path}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Step 2: Extract matching story blocks
    result = extract_matching_stories(sm_ids, user_stories_text)

    # Step 3: Output
    output = format_output(phase_num, sm_ids, result)
    print(output)


if __name__ == "__main__":
    main()
