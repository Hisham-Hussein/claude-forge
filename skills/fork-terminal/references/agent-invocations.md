# Agent Invocation Patterns

Reference for invoking each supported AI coding assistant.

<claude_code>
## Claude Code

**Binary:** `claude`

### Interactive Mode (Default)
```bash
# Start in directory with initial prompt
cd /path/to/project && claude "Your task description here"

# With specific files to focus on
cd /path/to/project && claude "Focus on src/auth/ - implement OAuth2 flow"

# Resume existing session
claude --resume
```

### Headless Mode (Print Output)
```bash
# Run task and print result
claude --print "Analyze this codebase and list all API endpoints"

# With JSON output
claude --print --output-format json "List all TODO comments"
```

### With Context Handoff
```bash
# Pass handoff document via stdin
cat handoff.md | claude

# Or use --prompt-file
claude --prompt-file handoff.md
```

### Key Flags
| Flag | Purpose |
|------|---------|
| `--print` | Headless mode, output to stdout |
| `--resume` | Resume last session |
| `--output-format json` | Structured output |
| `--model` | Specify model (sonnet, opus, haiku) |
| `--allowedTools` | Restrict available tools |
</claude_code>

<gemini_cli>
## Gemini CLI

**Binary:** `gemini`

### Interactive Mode
```bash
# Start interactive session
cd /path/to/project && gemini

# With initial prompt
cd /path/to/project && gemini "Explore this codebase and explain the architecture"
```

### Headless Mode
```bash
# Single prompt, exit after response
gemini --prompt "Your task" --no-interactive

# With file context
gemini --prompt "Review this file" --files src/main.py
```

### With Context Handoff
```bash
# Pass context via prompt
gemini --prompt "$(cat handoff.md)"

# Or pipe
cat handoff.md | gemini --no-interactive
```

### Key Flags
| Flag | Purpose |
|------|---------|
| `--no-interactive` | Headless mode |
| `--files` | Include specific files |
| `--model` | Specify model |
| `--sandbox` | Run in sandboxed environment |
</gemini_cli>

<aider>
## Aider (with Claude/GPT backend)

**Binary:** `aider`

### Interactive Mode
```bash
# Start with specific files
cd /path/to/project && aider src/auth.py src/models.py

# With Claude backend
aider --model claude-3-5-sonnet-20241022 src/file.py

# Watch mode (auto-reload on file changes)
aider --watch src/
```

### Headless Mode
```bash
# Single message, auto-commit
aider --message "Add input validation to login function" src/auth.py

# No auto-commit
aider --message "Refactor this" --no-auto-commit src/file.py
```

### With Context Handoff
```bash
# Pass task via message
aider --message "$(cat handoff.md)" src/relevant_files.py

# With read-only context files
aider --read ARCHITECTURE.md --message "Follow this architecture" src/new_feature.py
```

### Key Flags
| Flag | Purpose |
|------|---------|
| `--message` | Single prompt, headless |
| `--model` | Specify LLM backend |
| `--no-auto-commit` | Don't auto-commit changes |
| `--read` | Add read-only context files |
| `--watch` | Watch mode |
| `--yes` | Auto-confirm prompts |
</aider>

<choosing_agent>
## When to Use Each Agent

| Scenario | Best Agent | Why |
|----------|------------|-----|
| Multi-file refactoring | Claude Code | Best at coordinating complex changes |
| Focused single-file edits | Aider | Fast, git-integrated |
| Codebase exploration | Gemini CLI | Strong at research and analysis |
| Documentation tasks | Claude Code | Thorough, well-structured output |
| Quick prototyping | Aider | Rapid iteration with watch mode |
| Architecture review | Gemini CLI | Broad perspective |
</choosing_agent>

<terminal_spawning>
## Spawning Terminals

### Linux/WSL (using GNOME Terminal)
```bash
gnome-terminal --working-directory=/path/to/project -- bash -c 'claude "task"; exec bash'
```

### Linux (using tmux)
```bash
tmux new-window -c /path/to/project 'claude "task"'
```

### macOS (using iTerm2)
```bash
osascript -e 'tell application "iTerm2" to create window with default profile command "cd /path && claude task"'
```

### macOS (using Terminal.app)
```bash
osascript -e 'tell application "Terminal" to do script "cd /path && claude task"'
```

### Windows Terminal (from WSL)
```bash
cmd.exe /c start wt.exe -d "\\wsl$\Ubuntu\path\to\project" -- wsl bash -c 'claude "task"'
```
</terminal_spawning>
