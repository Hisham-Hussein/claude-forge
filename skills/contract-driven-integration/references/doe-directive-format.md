# DOE Directive Format

Standard structure for directives in the DOE (Directive-Orchestration-Execution) architecture.

## Directive Types

### 1. Workflow Directives
Location: `directives/workflows/`

Task-specific SOPs that define a complete workflow. Always have:
- Clear trigger
- Defined inputs/outputs
- Step-by-step process
- Mapped to specific scripts

Example: `onboard_client.md`, `add_webhook.md`

### 2. Strategic Directives
Location: `directives/strategic/`

Cross-cutting guidance that applies to multiple workflows. May have:
- Principles instead of steps
- References instead of scripts
- Guidelines instead of outputs

Example: `architecture_principles.md`, `testing_methodology.md`

### 3. Template Directives
Location: `directives/templates/`

Content templates used by workflows. Typically:
- No trigger or process
- Static content with placeholders
- Referenced by workflow directives

Example: `company_intro.md`

## Standard Sections (Workflow Directives)

### Header
```markdown
# {Directive Name}

{One-line description of what this directive does.}
```

### Trigger
```markdown
## Trigger

User says:
- `/{command} --arg value`
- "{natural language trigger}"

When triggered, run:
\`\`\`bash
PYTHONPATH=. python -m execution.{module} [args]
\`\`\`
```

### Inputs
```markdown
## Inputs

- **{param_name}**: {Description} (required|optional)
- **{param_name}**: {Description}, default: {value}
```

### Tools
```markdown
## Tools

- `execution/{path}.py` - {What it does}
- `execution/{path}.py` - {What it does}
```

### Process
```markdown
## Process

1. **{Step Name}** - {Description}
2. **{Step Name}** - {Description}
3. **{Step Name}** - {Description}
```

Or with sub-steps:
```markdown
## Process

1. **{Step Name}**
   - {Sub-step}
   - {Sub-step}

2. **{Step Name}**
   - {Sub-step}
```

### Outputs
```markdown
## Outputs

Success:
\`\`\`json
{
  "success": true,
  "field": "value"
}
\`\`\`

Failure:
\`\`\`json
{
  "success": false,
  "error": "description"
}
\`\`\`
```

### Edge Cases
```markdown
## Edge Cases

- **{Case name}**: {How it's handled}
- **{Case name}**: {How it's handled}
```

## Optional Sections

### Configuration
```markdown
## Configuration

Required in `.env`:
- `{VAR_NAME}` - {Description}

Required files:
- `{path}` - {Description}
```

### CLI Usage
```markdown
## CLI Usage

\`\`\`bash
# Basic usage
PYTHONPATH=. python -m execution.{module} --arg value

# With options
PYTHONPATH=. python -m execution.{module} --arg value --flag
\`\`\`
```

### Architecture Principles
```markdown
## Architecture Principles Applied

| Principle | Implementation |
|-----------|----------------|
| {Name} | {How applied} |
```

### Monitoring
```markdown
## Monitoring

{Logging format, metrics, alerts}
```

## Contract Extraction by Section

| Section | Contract Type | Assertion Pattern |
|---------|---------------|-------------------|
| Trigger | Invocation | "Script callable via {command}" |
| Inputs | Precondition | "Script accepts/requires {param}" |
| Tools | Dependency | "Script uses {tool}" |
| Process | Behavior | "Script performs {step}" |
| Outputs | Postcondition | "Output contains {field}" |
| Edge Cases | Error handling | "Script handles {case}" |

## Minimal Viable Directive

At minimum, a workflow directive must have:

```markdown
# {Name}

{Description}

## Trigger

{How to invoke}

## Inputs

{What it needs}

## Process

{What it does}

## Outputs

{What it returns}
```

## Quality Indicators

**Well-documented directive:**
- All standard sections present
- Inputs marked required/optional
- Output examples in JSON
- Edge cases are specific
- Tools section lists all scripts

**Poorly-documented directive:**
- Missing sections
- Vague descriptions ("handles errors")
- No output examples
- No edge cases
- Missing tool references

## Directive Validation

Check for:

1. **Structure**: Required sections present
2. **Completeness**: All inputs/outputs documented
3. **Clarity**: Specific, testable statements
4. **Accuracy**: References valid files
5. **Currency**: Matches actual script behavior
