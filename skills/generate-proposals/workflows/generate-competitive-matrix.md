<objective>
Generate a glassmorphic 2x2 competitive matrix SVG that visually positions your company as the best value against competitors. The design tokens (colors, fonts, effects) are fixed to iSemantics brand guidelines. You provide the variables (axes, competitors, positioning).
</objective>

<design_principles>
**Fixed Design Elements:**
- Dark gradient background (#0a0a0f to #0d0d1a)
- Glassmorphic cards with blur and transparency
- iSemantics accent colors (#3A5AFF, #92E6FD, #00ff87)
- Poppins (headings) + Roboto (body) fonts, weight 300
- Green glow for winner position (top-right quadrant)
- Red tint for worst position (bottom-left quadrant)
- Gold badge for winner

**Matrix Layout:**
- Axes cross at center (true 2x2 quadrant)
- Top-right = BEST (your company)
- Bottom-left = WORST (expensive + slow/bad competitors)
- Arrows point toward "good" direction on each axis
</design_principles>

<intake>
I'll generate a competitive matrix SVG for your proposal. I need to understand:

1. **The two comparison axes** — What dimensions are you comparing?
   - Common combinations:
     - Price vs Timeline (expensive→affordable, slow→fast)
     - Price vs Expertise (generic→specialized)
     - Price vs Quality (low→high)
     - Cost vs Language/Region expertise
     - Investment vs Domain knowledge

2. **Your positioning** — Company name, price point, 2 key differentiators

3. **Competitors** — 2-3 alternatives with their position, price, and main limitation

Let me ask for the specifics.
</intake>

<questions>
Use AskUserQuestion to gather:

**Question 1: Axis Configuration**
```
What are the two comparison dimensions for your matrix?

Options:
1. Price vs Timeline (typical: expensive/slow vs affordable/fast)
2. Price vs Domain Expertise (generic vs specialized)
3. Price vs Quality/Capability (limited vs full-featured)
4. Custom (I'll specify both axes)
```

**Question 2: Your Company Details**
If not already known from the proposal context, ask:
- Company name
- Price point (e.g., "$25K · 6 months")
- Two key differentiators (e.g., "Domain expertise", "Evidence-first architecture")
- Badge text (default: "BEST VALUE")

**Question 3: Competitors**
Ask for 2-3 competitors. For each:
- Name (e.g., "Consultancies", "Generic AI", "In-House")
- Price range (e.g., "$100K-$500K+")
- Main limitation (e.g., "Slow delivery")
- Which quadrant? (bottom-left = expensive+slow, center-left = medium, etc.)
</questions>

<axis_presets>
**Preset 1: Price vs Timeline** (most common)
```
X-axis: TOTAL INVESTMENT
  Left: EXPENSIVE ($200K - $500K+)
  Right: AFFORDABLE ($25K - $50K)

Y-axis: DELIVERY TIMELINE
  Top: FAST (3-6 months)
  Bottom: SLOW (12-18+ months)

Quadrants:
  Top-left: EXPENSIVE + FAST
  Top-right: AFFORDABLE + FAST (winner)
  Bottom-left: EXPENSIVE + SLOW (worst)
  Bottom-right: AFFORDABLE + SLOW
```

**Preset 2: Price vs Domain Expertise**
```
X-axis: TOTAL INVESTMENT
  Left: EXPENSIVE ($200K - $500K+)
  Right: AFFORDABLE ($25K - $50K)

Y-axis: DOMAIN EXPERTISE
  Top: SPECIALIZED (deep domain knowledge)
  Bottom: GENERIC (no domain expertise)

Quadrants:
  Top-left: EXPENSIVE + SPECIALIZED
  Top-right: AFFORDABLE + SPECIALIZED (winner)
  Bottom-left: EXPENSIVE + GENERIC (worst)
  Bottom-right: AFFORDABLE + GENERIC
```

**Preset 3: Price vs Language/Regional Fit**
```
X-axis: TOTAL INVESTMENT
  Left: EXPENSIVE ($200K - $500K+)
  Right: AFFORDABLE ($25K - $50K)

Y-axis: REGIONAL FIT
  Top: NATIVE (Arabic-first, local expertise)
  Bottom: OFFSHORE (language/cultural gaps)

Quadrants:
  Top-left: EXPENSIVE + NATIVE
  Top-right: AFFORDABLE + NATIVE (winner)
  Bottom-left: EXPENSIVE + OFFSHORE (worst)
  Bottom-right: AFFORDABLE + OFFSHORE
```

**Custom Axes:**
If user selects custom, ask for:
- X-axis label and left/right values
- Y-axis label and top/bottom values
- Quadrant labels for all four corners
</axis_presets>

<competitor_positioning>
**Position Guide (16:9 coordinates - 1920x1080 - LARGE CARDS):**

| Position | X Range | Y Range | Card Size | Description |
|----------|---------|---------|-----------|-------------|
| Bottom-left (worst) | 350-420 | 650-910 | 340x190 or 310x160 | Expensive + bad on Y-axis |
| Top-left (medium) | 450-520 | 350-420 | 340x190 | Medium price, medium Y |
| Top-left | 350-450 | 250-350 | 340x190 | Expensive + good on Y-axis |
| Bottom-right | 1200-1500 | 700-900 | 340x190 | Affordable + bad on Y-axis |

**Winner position is fixed at (1450, 320)** — top-right quadrant.
**Winner card size:** 420x300
**Axis crossing point:** (960, 540)

**Text sizes (for visibility):**
- Card names: 24-26px
- Card prices: 17-18px
- Card limitations: 15px (opacity 0.7)
- Axis labels: 20px
- Winner name: 38px

**Color coding:**
- Orange (#FFA500): Medium-bad competitors
- Red (#ff6b6b): Worst competitors
- Gray (#9696b4): Neutral/medium competitors
</competitor_positioning>

<generation_process>
1. **Collect variables** using AskUserQuestion or extract from proposal context
2. **Map coordinates** — Position each competitor in appropriate quadrant
3. **Generate SVG** — Use the template from `templates/competitive-matrix.svg.template`
4. **Replace all {{VARIABLE}}** placeholders with actual values
5. **Write to file** — Save as `competitive-matrix.svg` in the proposal's assets folder
6. **Validate** — Offer to show the SVG or make adjustments
</generation_process>

<variable_mapping>
After collecting inputs, map to template variables:

```javascript
// Title
{{TITLE}} = "Why " + companyName + " Wins"

// Winner details
{{WINNER_NAME}} = companyName
{{WINNER_LOGO_ABBREV}} = first two letters or initials
{{WINNER_PRICE}} = winnerPrice
{{WINNER_FEATURE_1}} = feature1
{{WINNER_FEATURE_2}} = feature2
{{BADGE_LINE_1}} = "BEST"
{{BADGE_LINE_2}} = "VALUE"

// Axes (from preset or custom)
{{X_AXIS_LABEL}} = xAxisLabel
{{X_LEFT_LABEL}} = xLeftLabel
{{X_LEFT_DETAIL}} = xLeftDetail
{{X_RIGHT_LABEL}} = xRightLabel
{{X_RIGHT_DETAIL}} = xRightDetail
{{Y_AXIS_LABEL}} = yAxisLabel
{{Y_TOP_LABEL}} = yTopLabel
{{Y_TOP_DETAIL}} = yTopDetail
{{Y_BOTTOM_LABEL}} = yBottomLabel
{{Y_BOTTOM_DETAIL}} = yBottomDetail

// Quadrants
{{QUADRANT_TOP_LEFT}} = xLeftLabel + " + " + yTopLabel
{{QUADRANT_TOP_RIGHT}} = xRightLabel + " + " + yTopLabel
{{QUADRANT_BOTTOM_LEFT}} = xLeftLabel + " + " + yBottomLabel
{{QUADRANT_BOTTOM_RIGHT}} = xRightLabel + " + " + yBottomLabel

// Competitors (for each)
{{COMPETITOR_N_NAME}} = name
{{COMPETITOR_N_PRICE}} = price
{{COMPETITOR_N_LIMITATION}} = limitation
{{COMPETITOR_N_X}} = xCoordinate (based on quadrant)
{{COMPETITOR_N_Y}} = yCoordinate (based on quadrant)
{{COMPETITOR_N_COLOR}} = borderColor (rgba format)
{{COMPETITOR_N_TEXT_COLOR}} = textColor (hex format)

// Callouts
{{SAVINGS_TEXT}} = savingsText (e.g., "Up to 95%")
{{SOURCE_TEXT}} = sourceText (e.g., "Sources: Astrum, Coherent Solutions (2025)")
```
</variable_mapping>

<output_location>
Save the generated SVG to:
- If proposal has an assets folder: `[proposal_folder]/artifacts/assets/competitive-matrix.svg`
- Otherwise create: `[proposal_folder]/assets/competitive-matrix.svg`

After generation, inform the user of the file path.
</output_location>

<example_generation>
**Input:**
- Preset: Price vs Timeline
- Winner: iSemantics, $25K · 6 months
- Features: "Domain-aware (Shariah)", "Evidence-first architecture"
- Competitors:
  1. Consultancies ($100K-$500K+, slow delivery) — bottom-left
  2. In-House ($100K+ · 12-18 mo, recruiting burden) — bottom-left lower
  3. Generic AI ($50K-$200K, no domain expertise) — center-left

**Output:** Generates 1920x1080 (16:9) SVG with LARGE CARDS:
- Generic AI at (480, 380) with gray border (340x190 card)
- Consultancies at (380, 680) with orange border (340x190 card)
- In-House at (350, 910) with red border (310x160 card)
- iSemantics at (1450, 320) with green glow and gold badge (420x300 card)
</example_generation>

<success_criteria>
Matrix generation is complete when:
- [ ] Both axes clearly labeled with good/bad directions
- [ ] Winner positioned in top-right with spotlight and badge
- [ ] 2-3 competitors positioned in appropriate quadrants
- [ ] Quadrant colors indicate best (green) and worst (red) zones
- [ ] All text is readable and properly positioned
- [ ] SVG file saved to appropriate location
- [ ] User has seen or approved the result
</success_criteria>
