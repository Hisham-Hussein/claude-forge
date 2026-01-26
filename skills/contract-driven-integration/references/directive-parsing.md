# Directive Parsing

How to parse DOE-style directives to extract contract assertions.

## Parsing Strategy

DOE directives are Markdown files with structured sections. Parse them as text, looking for patterns.

## Section Detection

### Header patterns
```
## Trigger
## When to Use
## Inputs
## Parameters
## Tools
## Dependencies
## Process
## Steps
## Outputs
## Results
## Edge Cases
## Error Handling
```

### Detection regex
```python
import re

SECTION_PATTERN = r'^##\s+(.+)$'
sections = re.findall(SECTION_PATTERN, content, re.MULTILINE)
```

## Extracting Content by Section

```python
def extract_section(content: str, header: str) -> str:
    """Extract content between this header and next ## header"""
    pattern = rf'^##\s+{re.escape(header)}\s*\n(.*?)(?=^##\s|\Z)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""
```

## Parsing Specific Sections

### Trigger Section

Look for:
- Command patterns: `/command`, `--flag`, `arg`
- Bash commands: `` `python ...` ``
- Natural language triggers: "User says..."

```python
# Extract CLI command
cli_pattern = r'```bash\n(.+?)\n```'
cli_match = re.search(cli_pattern, trigger_section, re.DOTALL)

# Extract slash commands
slash_pattern = r'`(/[\w-]+[^`]*)`'
slash_commands = re.findall(slash_pattern, trigger_section)
```

### Inputs Section

Look for:
- Bold parameters: `**param_name**`
- Required vs optional markers
- Type information

```python
# Extract bold parameters
param_pattern = r'\*\*([^*]+)\*\*[:\s]+(.+?)(?=\n|$)'
params = re.findall(param_pattern, inputs_section)

# Check for required/optional
for name, description in params:
    is_required = 'required' in description.lower()
    is_optional = 'optional' in description.lower()
```

### Tools Section

Look for:
- File paths: `execution/...`
- Code references: `` `module.function` ``

```python
# Extract file paths
path_pattern = r'`(execution/[^`]+)`'
tool_paths = re.findall(path_pattern, tools_section)

# Extract with descriptions
tool_line_pattern = r'-\s+`([^`]+)`\s*[-–]\s*(.+)'
tools = re.findall(tool_line_pattern, tools_section)
```

### Process Section

Look for:
- Numbered steps: `1.`, `2.`, etc.
- Bold step names: `**Step Name**`
- Order dependencies

```python
# Extract numbered steps
step_pattern = r'^\d+\.\s+\*\*([^*]+)\*\*\s*[-–]?\s*(.+?)$'
steps = re.findall(step_pattern, process_section, re.MULTILINE)

# Extract step order
step_names = [name for name, desc in steps]
```

### Outputs Section

Look for:
- JSON/code blocks with output examples
- Field names in output structure

```python
# Extract JSON examples
json_pattern = r'```json\n(.+?)\n```'
json_blocks = re.findall(json_pattern, outputs_section, re.DOTALL)

# Parse to find field names
import json
for block in json_blocks:
    try:
        obj = json.loads(block)
        fields = list(obj.keys())
    except:
        pass
```

### Edge Cases Section

Look for:
- Bold case names: `**Invalid email**`
- Colon-separated: `Case: behavior`
- List items describing scenarios

```python
# Extract edge cases
edge_pattern = r'-\s+\*\*([^*]+)\*\*[:\s]+(.+?)(?=\n|$)'
edge_cases = re.findall(edge_pattern, edge_section)

# Or simpler list items
list_pattern = r'^\s*-\s+(.+)$'
edge_items = re.findall(list_pattern, edge_section, re.MULTILINE)
```

## Handling Variations

Not all directives follow the exact same format. Handle variations:

| Expected | Variation | Handling |
|----------|-----------|----------|
| `## Inputs` | `## Parameters` | Check both headers |
| `## Process` | `## Steps` | Check both headers |
| `## Outputs` | `## Returns` | Check both headers |
| Numbered steps | Bullet points | Parse both formats |
| JSON output | Prose description | Extract what's available |

## Document Gaps

When parsing finds missing or vague content:

```python
gaps = []

if not inputs_section:
    gaps.append({"type": "missing_section", "section": "Inputs"})

if inputs_section and "required" not in inputs_section.lower():
    gaps.append({"type": "unclear", "section": "Inputs",
                 "issue": "No required/optional markers"})
```

## Full Parsing Example

```python
def parse_directive(path: str) -> dict:
    content = Path(path).read_text()

    return {
        "path": path,
        "title": extract_title(content),
        "trigger": {
            "raw": extract_section(content, "Trigger"),
            "cli_command": extract_cli(content),
            "slash_commands": extract_slash_commands(content),
        },
        "inputs": {
            "raw": extract_section(content, "Inputs"),
            "parameters": extract_parameters(content),
        },
        "tools": {
            "raw": extract_section(content, "Tools"),
            "paths": extract_tool_paths(content),
        },
        "process": {
            "raw": extract_section(content, "Process"),
            "steps": extract_steps(content),
        },
        "outputs": {
            "raw": extract_section(content, "Outputs"),
            "fields": extract_output_fields(content),
        },
        "edge_cases": {
            "raw": extract_section(content, "Edge Cases"),
            "cases": extract_edge_cases(content),
        },
        "gaps": identify_gaps(content),
    }
```

## Notes

- Parse flexibly, document gaps
- Don't fail on unusual formats
- Strategic directives differ from workflow directives
- Extract what exists, note what's missing
