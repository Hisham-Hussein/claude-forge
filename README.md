# Claude Forge

Custom skills, agents, and commands for enhanced Claude Code workflows.

## Installation

```bash
claude plugin install claude-forge
```

Or test locally:
```bash
claude --plugin-dir ~/.claude/plugins/marketplaces/claude-forge
```

## Contents

### Skills (17)

| Skill | Description |
|-------|-------------|
| `brainstorm-userstories-ac` | Systematic methodology for brainstorming comprehensive acceptance criteria |
| `article-extractor` | Extract clean content from web articles |
| `build-llm-app` | Guide for building LLM applications |
| `characterization-first` | Characterize code before refactoring |
| `contract-driven-integration` | Verify alignment between directives and execution scripts |
| `create-business-case` | Create business cases with BRD |
| `create-hooks` | Expert guidance for creating Claude Code hooks |
| `create-requirements` | Transform business cases into formal requirements |
| `deepeval` | Work with DeepEval testing framework |
| `execute-phase` | Execute phases from project plans |
| `expertise` | Domain expertise guidance |
| `fix-drift` | Fix contract drifts between directives and scripts |
| `fork-terminal` | Distribute tasks across multiple terminal sessions |
| `ship-learn-next` | Process learning content and ship insights |
| `skills-discovery` | Discover and install agent skills |
| `tapestry` | Unified content extraction and action planning |
| `youtube-transcript` | Download and process YouTube transcripts |

### Agents (1)

| Agent | Description |
|-------|-------------|
| `ac-brainstormer` | Reviews and enhances acceptance criteria in USER-STORIES.md |

### Commands (9)

| Command | Description |
|---------|-------------|
| `/claude-forge:build-diagrams` | Create technical diagrams |
| `/claude-forge:build-llm-app` | Guide for building LLM apps |
| `/claude-forge:characterization-first` | Characterize before refactoring |
| `/claude-forge:check-contract` | Verify directive-script alignment |
| `/claude-forge:create-business-case` | Create business cases |
| `/claude-forge:execute-phase` | Execute project phases |
| `/claude-forge:fix-drift` | Fix directive-script drift |
| `/claude-forge:fork-terminal` | Distribute terminal tasks |
| `/claude-forge:update-roadmap` | Update project roadmap |

## Usage

Skills are automatically invoked by Claude based on context. Commands can be invoked with `/claude-forge:command-name`.

## License

MIT
