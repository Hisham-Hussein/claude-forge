<overview>
Export Mermaid diagrams to images (SVG, PNG, PDF) using the Mermaid CLI or web services. Useful for documentation, presentations, and CI/CD pipelines.
</overview>

<mermaid_cli>
## Mermaid CLI (mmdc)

**Install:**
```bash
npm install -g @mermaid-js/mermaid-cli
```

**Basic usage:**
```bash
# SVG output (recommended for web)
mmdc -i diagram.mmd -o diagram.svg

# PNG output (for documents)
mmdc -i diagram.mmd -o diagram.png

# PDF output
mmdc -i diagram.mmd -o diagram.pdf
```

**With theme:**
```bash
# Built-in dark theme
mmdc -i diagram.mmd -o diagram.png -t dark

# Built-in themes: default, dark, neutral, forest
mmdc -i diagram.mmd -o diagram.svg -t neutral
```

**With config file:**
```bash
mmdc -i diagram.mmd -o diagram.svg -c config.json
```

**Batch processing:**
```bash
# All .mmd files in directory
for f in *.mmd; do mmdc -i "$f" -o "${f%.mmd}.svg"; done
```
</mermaid_cli>

<config_file>
## Config File Examples

**Dark theme config (config-dark.json):**
```json
{
  "theme": "dark",
  "themeVariables": {
    "primaryColor": "#004A77",
    "primaryTextColor": "#C2E7FF",
    "primaryBorderColor": "#8ECAE6",
    "lineColor": "#8ECAE6",
    "secondaryColor": "#4A4458",
    "tertiaryColor": "#005141",
    "background": "#1C1B1F",
    "mainBkg": "#1C1B1F"
  }
}
```

**Light theme config (config-light.json):**
```json
{
  "theme": "base",
  "themeVariables": {
    "primaryColor": "#BBDEFB",
    "primaryTextColor": "#0D47A1",
    "primaryBorderColor": "#1976D2",
    "lineColor": "#1976D2",
    "secondaryColor": "#E8DEF8",
    "tertiaryColor": "#9EF2DE",
    "background": "#FFFBFE",
    "mainBkg": "#FFFBFE"
  }
}
```

**High-resolution PNG:**
```json
{
  "theme": "dark",
  "width": 2400,
  "height": 1600,
  "backgroundColor": "#1C1B1F"
}
```
</config_file>

<cli_options>
## CLI Options Reference

| Option | Description | Example |
|--------|-------------|---------|
| `-i, --input` | Input file | `-i diagram.mmd` |
| `-o, --output` | Output file | `-o diagram.svg` |
| `-t, --theme` | Built-in theme | `-t dark` |
| `-c, --config` | Config file | `-c config.json` |
| `-w, --width` | Width in pixels | `-w 1200` |
| `-H, --height` | Height in pixels | `-H 800` |
| `-b, --backgroundColor` | Background color | `-b "#1C1B1F"` |
| `-p, --puppeteerConfig` | Puppeteer config | `-p puppeteer.json` |
</cli_options>

<web_services>
## Web Services

**Mermaid Live Editor:**
- URL: https://mermaid.live
- Features: Edit, preview, export (SVG, PNG)
- Use: Quick testing and one-off exports

**kroki.io:**
- URL: https://kroki.io
- Features: API-based rendering, multiple diagram formats
- Use: CI/CD integration, automated documentation

**mermaid.ink:**
- URL: https://mermaid.ink
- Features: URL-based rendering (encode diagram in URL)
- Use: Embedding in external systems

**Example kroki.io API call:**
```bash
curl -X POST https://kroki.io/mermaid/svg \
  -H "Content-Type: text/plain" \
  -d 'flowchart LR
    A --> B --> C' \
  -o diagram.svg
```
</web_services>

<ci_cd>
## CI/CD Integration

**GitHub Actions example:**
```yaml
- name: Generate diagrams
  run: |
    npm install -g @mermaid-js/mermaid-cli
    mmdc -i docs/architecture.mmd -o docs/architecture.svg -t dark

- name: Commit generated diagrams
  run: |
    git add docs/*.svg
    git commit -m "Update generated diagrams" || true
    git push
```

**Pre-commit hook:**
```bash
#!/bin/bash
# .git/hooks/pre-commit
for mmd in $(git diff --cached --name-only | grep '\.mmd$'); do
  svg="${mmd%.mmd}.svg"
  mmdc -i "$mmd" -o "$svg" -t dark
  git add "$svg"
done
```
</ci_cd>

<file_formats>
## Output Format Comparison

| Format | Best For | Notes |
|--------|----------|-------|
| SVG | Web, scalable docs | Vector, scales infinitely, searchable text |
| PNG | Documents, slides | Raster, fixed resolution, universal support |
| PDF | Print, formal docs | Vector, good for archiving |

**Recommendation:** Use SVG for web/docs, PNG for presentations/exports where SVG isn't supported.
</file_formats>

<troubleshooting>
## CLI Troubleshooting

**"puppeteer" errors:**
```bash
# Install Chromium for puppeteer
npx puppeteer browsers install chrome
```

**Permission errors:**
```bash
# Use npx instead of global install
npx -p @mermaid-js/mermaid-cli mmdc -i input.mmd -o output.svg
```

**Timeout on large diagrams:**
```bash
# Increase timeout
mmdc -i diagram.mmd -o diagram.svg -p '{"timeout": 60000}'
```
</troubleshooting>
