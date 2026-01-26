<overview>
Platform choice affects what Mermaid features work. GitHub has significant limitations compared to VSCode. Always design for the target platform.
</overview>

<github_support>
## GitHub Mermaid Support

**Version:** ~10.8.0 (not always latest)

| Feature | Supported | Notes |
|---------|-----------|-------|
| Flowchart | Yes | Full support |
| Sequence | Yes | Full support |
| Sequence `box` syntax | **Yes** | `box rgb(r,g,b)` works (v10.6+) |
| Class | Yes | Full support |
| State | Yes | Use `stateDiagram-v2` |
| ER | Yes | Full support |
| Gantt | Yes | Full support |
| C4 | Yes | Full support (stable now) |
| Mindmap | Yes | Full support |
| Timeline | Yes | Full support |
| Click events | **No** | Security restriction |
| JavaScript callbacks | **No** | Security restriction |
| Custom fonts | **No** | System fonts only |
| Layout control | **No** | Auto-layout only |
| Quadrant charts | Partial | May not render |
| XY Charts | Partial | May have issues |

**Where Mermaid works on GitHub:**
- README files
- Issues and PRs
- Discussions
- Markdown files in repos

**Where it doesn't work:**
- GitHub Pages (needs additional setup)
- GitHub Wiki (limited)
- Code comments
</github_support>

<vscode_support>
## VSCode Mermaid Support

With the Markdown Preview Mermaid extension:

| Feature | Supported |
|---------|-----------|
| All diagram types | Yes |
| Click events | Yes (with `securityLevel: loose`) |
| Custom fonts | Yes |
| Theme control | Full |
| Export to image | Yes (with extensions) |
| Live preview | Yes |
| Max nodes | ~50+ (more than GitHub) |
</vscode_support>

<comparison>
## GitHub vs VSCode

| Feature | GitHub | VSCode |
|---------|--------|--------|
| Click events | No | Yes |
| Theme control | Auto only | Full control |
| Export to image | No | Yes |
| All diagram types | Most | All |
| Max recommended nodes | ~30 | ~50+ |
| Live preview | No | Yes |
| Custom styling | Limited | Full |
</comparison>

<safe_patterns>
## Cross-Platform Safe Patterns

To ensure diagrams work everywhere:

1. **Use hex colors only** - `#1976D2` not `blue`
2. **Avoid click events** - Remove all `click` statements
3. **Keep under 30 nodes** - GitHub performance limit
4. **Use standard ASCII in labels** - Avoid special Unicode
5. **Test in both environments** - What works in VSCode may fail on GitHub
6. **Use `stateDiagram-v2`** - Not the older `stateDiagram`
7. **Avoid experimental features** - quadrantChart, xychart-beta may fail
</safe_patterns>

<sequence_diagram_support>
## Sequence Diagram Styling on GitHub

Sequence diagrams have different styling capabilities than flowcharts:

| Feature | Flowchart | Sequence | GitHub Support |
|---------|-----------|----------|----------------|
| `classDef` | ✓ | ✗ | N/A |
| `box rgb()` grouping | N/A | ✓ | **Yes** (v10.6+) |
| `mirrorActors` | N/A | ✓ | Yes |
| `alt`/`else` blocks | N/A | ✓ | Yes |
| `loop` construct | N/A | ✓ | Yes |
| `Note` annotations | N/A | ✓ | Yes |

**Recommended init for sequence diagrams:**
```mermaid
%%{init: {"sequence": {"mirrorActors": false}} }%%
```

**Box syntax example (GitHub-compatible):**
```mermaid
box rgb(30, 64, 175) Human
    actor User as End User
end
box rgb(6, 95, 70) System
    participant API as API Server
end
```

**Note:** Use RGB values (0-255), not hex codes, in the `box` syntax.
</sequence_diagram_support>

<mermaid_vs_plantuml>
## Mermaid vs PlantUML

| Scenario | Use Mermaid | Use PlantUML |
|----------|-------------|--------------|
| Quick documentation | ✓ | |
| GitHub README | ✓ | |
| PR descriptions | ✓ | |
| Wiki pages | ✓ | |
| Complex C4 with full control | | ✓ |
| Formal architecture specs | | ✓ |
| Print-quality docs | | ✓ |
| Advanced UML customization | | ✓ |

| Aspect | Mermaid | PlantUML |
|--------|---------|----------|
| Technology | JavaScript (browser) | Java (server) |
| Setup | Zero (native) | Requires Java + GraphViz |
| GitHub | Native rendering | Needs pre-rendering |
| Syntax | Simple, Markdown-like | Verbose, powerful |
| Customization | CSS-based, limited | Full theming system |
| C4 Support | Good | Excellent with sprites |

**Recommendation:** Start with Mermaid. Fall back to PlantUML for complex architecture diagrams or when you need fine-grained control.
</mermaid_vs_plantuml>

<target_decision>
## Choosing Target Platform

**Default to GitHub** when:
- Diagram goes in README or docs
- Sharing via PR/issue
- Team collaboration
- Public documentation

**Use VSCode** when:
- Local development docs
- Need interactivity (click events)
- Exporting to images
- Complex diagrams (>30 nodes)
- Full theme control needed
</target_decision>
