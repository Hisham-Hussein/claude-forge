---
name: article-extractor
description: Extract clean article content from URLs (blog posts, articles, tutorials) and save as readable text. Use when user wants to download, extract, or save an article/blog post from a URL without ads, navigation, or clutter.
allowed-tools: Bash,Write
---

<objective>
Extract main content from web articles, removing navigation, ads, and clutter, saving clean readable text.
</objective>

<triggers>
Use this skill when the user:
- Provides an article/blog URL and wants the text content
- Asks to "download this article"
- Wants to "extract the content from [URL]"
- Asks to "save this blog post as text"
- Needs clean article text without distractions
</triggers>

<quick_start>
1. Check for tools: `command -v reader` or `command -v trafilatura`
2. Extract: `reader "URL" > article.txt` or `trafilatura --URL "URL" --output-format txt > article.txt`
3. Get title for filename
4. Show preview and confirm location
</quick_start>

<success_criteria>
- Extraction tool is available (reader, trafilatura, or fallback)
- Article content extracted without ads/navigation/clutter
- Saved to file with article title as filename
- User shown file location and preview (first 10 lines)
</success_criteria>

<process>
<tool_priority>
1. reader (Mozilla Readability) - best all-around
2. trafilatura (Python) - good for blogs/news
3. curl + basic parsing - fallback if no tools
</tool_priority>

<extraction>
Using reader (preferred):
```bash
reader "URL" > article.txt
```

Using trafilatura:
```bash
trafilatura --URL "URL" --output-format txt > article.txt
# Options: --no-comments, --no-tables, --precision, --recall
```

Get title:
```bash
# From reader (markdown with title at top)
TITLE=$(reader "URL" | head -n 1 | sed 's/^# //')

# From trafilatura
TITLE=$(trafilatura --URL "URL" --json | python3 -c "import json, sys; print(json.load(sys.stdin)['title'])")

# From curl (fallback)
TITLE=$(curl -s "URL" | grep -oP '<title>\K[^<]+' | sed 's/ - .*//' | sed 's/ | .*//')
```

Clean filename:
```bash
FILENAME=$(echo "$TITLE" | tr '/' '-' | tr ':' '-' | tr '?' '' | tr '"' '' | tr '<>' '' | tr '|' '-' | cut -c 1-80 | sed 's/ *$//')
FILENAME="${FILENAME}.txt"
```
</extraction>
</process>

<installation>
<check>
```bash
command -v reader
command -v trafilatura
```
</check>

<install_reader>
```bash
npm install -g @mozilla/readability-cli
# or
npm install -g reader-cli
```
</install_reader>

<install_trafilatura>
```bash
pip3 install trafilatura
```
</install_trafilatura>
</installation>

<reference>
<complete_workflow>
```bash
ARTICLE_URL="https://example.com/article"

# Check for tools
if command -v reader &> /dev/null; then
    TOOL="reader"
    echo "Using reader (Mozilla Readability)"
elif command -v trafilatura &> /dev/null; then
    TOOL="trafilatura"
    echo "Using trafilatura"
else
    TOOL="fallback"
    echo "Using fallback method (may be less accurate)"
fi

# Extract article
case $TOOL in
    reader)
        reader "$ARTICLE_URL" > temp_article.txt
        TITLE=$(head -n 1 temp_article.txt | sed 's/^# //')
        ;;
    trafilatura)
        METADATA=$(trafilatura --URL "$ARTICLE_URL" --json)
        TITLE=$(echo "$METADATA" | python3 -c "import json, sys; print(json.load(sys.stdin).get('title', 'Article'))")
        trafilatura --URL "$ARTICLE_URL" --output-format txt --no-comments > temp_article.txt
        ;;
    fallback)
        TITLE=$(curl -s "$ARTICLE_URL" | grep -oP '<title>\K[^<]+' | head -n 1)
        TITLE=${TITLE%% - *}
        TITLE=${TITLE%% | *}
        curl -s "$ARTICLE_URL" | python3 -c "
from html.parser import HTMLParser
import sys

class ArticleExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_content = False
        self.content = []
        self.skip_tags = {'script', 'style', 'nav', 'header', 'footer', 'aside', 'form'}

    def handle_starttag(self, tag, attrs):
        if tag not in self.skip_tags:
            if tag in {'p', 'article', 'main'}:
                self.in_content = True
        if tag in {'h1', 'h2', 'h3'}:
            self.content.append('\n')

    def handle_data(self, data):
        if self.in_content and data.strip():
            self.content.append(data.strip())

    def get_content(self):
        return '\n\n'.join(self.content)

parser = ArticleExtractor()
parser.feed(sys.stdin.read())
print(parser.get_content())
" > temp_article.txt
        ;;
esac

# Clean filename
FILENAME=$(echo "$TITLE" | tr '/' '-' | tr ':' '-' | tr '?' '' | tr '"' '' | tr '<>' '' | tr '|' '-' | cut -c 1-80 | sed 's/ *$//' | sed 's/^ *//')
FILENAME="${FILENAME}.txt"

# Move to final filename
mv temp_article.txt "$FILENAME"

# Show result
echo "Extracted: $TITLE"
echo "Saved to: $FILENAME"
echo ""
echo "Preview (first 10 lines):"
head -n 10 "$FILENAME"
```
</complete_workflow>
</reference>

<troubleshooting>
<tool_not_installed>
Try alternate tool: reader → trafilatura → fallback
Offer to install: "Install reader with: npm install -g reader-cli"
</tool_not_installed>

<paywall_or_login>
Extraction tools may fail on protected content.
Inform user: "This article requires authentication. Cannot extract."
</paywall_or_login>

<no_content>
Site may use heavy JavaScript rendering.
Try fallback method or inform user extraction failed.
</no_content>

<special_characters>
Clean filename by removing: / : ? " < > |
Replace with - or remove entirely.
Keep length under 80-100 characters.
</special_characters>
</troubleshooting>

<output_format>
Saved file contains:
- Article title (if available)
- Author (if extracted)
- Main article text
- Section headings
- No navigation, ads, newsletter forms, sidebars, comments, social buttons, cookie notices
</output_format>

<tool_recommendations>
reader: Best for most articles, based on Firefox Reader View, excellent clutter removal
trafilatura: Best for academic articles, news sites, blogs with complex layouts, non-English content
fallback: Works without dependencies but may include noise, less accurate paragraph detection
</tool_recommendations>

<best_practices>
- Always show preview after extraction (first 10 lines)
- Verify extraction succeeded before saving
- Clean filename for filesystem compatibility
- Try fallback method if primary fails
- Inform user which tool was used
- Keep filename length reasonable (under 100 chars)
- Ask user about related actions: "Would you like me to create a Ship-Learn-Next plan from this?"
</best_practices>
