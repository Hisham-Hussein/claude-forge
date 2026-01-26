<overview>
Accessible diagrams ensure all users can understand the information, including those with visual impairments or color blindness. Follow WCAG 2.1 guidelines.
</overview>

<contrast_requirements>
## WCAG 2.1 Contrast Requirements

| Element Type | Minimum Ratio |
|--------------|---------------|
| Normal text (<18pt) | 4.5:1 |
| Large text (≥18pt) | 3:1 |
| UI components & graphics | 3:1 |

The MD3 color palettes in `color-palettes.md` are pre-validated for WCAG compliance.
</contrast_requirements>

<color_blind_design>
## Color-Blind Friendly Design

**8% of men and 0.5% of women have color vision deficiency.**

<do_list>
**Do:**
- Use patterns/shapes in addition to color
- Add text labels to colored elements
- Use high brightness/saturation contrast
- Test with color blindness simulators
- Combine color with other visual cues (icons, patterns)
</do_list>

<dont_list>
**Don't:**
- Rely solely on color to convey information
- Combine red + green (most common deficiency)
- Use pink + turquoise + grey together
- Use purple + blue without other differentiators
- Assume "green = good, red = bad" is universally visible
</dont_list>
</color_blind_design>

<safe_combinations>
## Safe Color Combinations

These combinations work for most color vision types:

| Combination | Use Case |
|-------------|----------|
| Blue + Orange | Primary contrast |
| Blue + Red (different saturation) | Status differentiation |
| Purple + Yellow/Gold | Highlight + neutral |
| Dark blue + Light blue | Same hue, different value |

**Avoid:**
- Red + Green (protanopia, deuteranopia)
- Blue + Purple without value contrast (tritanopia)
- Any two colors that only differ in hue (no brightness difference)
</safe_combinations>

<techniques>
## Accessibility Techniques for Diagrams

<shapes>
**Use shapes to reinforce meaning:**
- Rectangles for processes
- Diamonds for decisions
- Circles for start/end
- Different shapes for different entity types
</shapes>

<labels>
**Always include text labels:**
- Node labels describe the element
- Edge labels describe the relationship
- Don't rely on color alone to convey type
</labels>

<patterns>
**Consider patterns for print/grayscale:**
- Solid fill vs hatched
- Different border styles (solid, dashed, dotted)
- Icons within nodes
</patterns>
</techniques>

<checklist>
## Accessibility Checklist

Before finalizing a diagram, verify:

- [ ] Text on colored backgrounds meets 4.5:1 contrast
- [ ] Graphical elements meet 3:1 contrast against background
- [ ] Information is not conveyed by color alone
- [ ] Text labels accompany all color-coded elements
- [ ] Diagram is readable in grayscale (test by desaturating)
- [ ] Critical paths don't rely on red/green distinction
- [ ] Font size is readable (not too small)
- [ ] Labels are clear and descriptive
</checklist>

<testing>
## Testing Accessibility

**Tools:**
- Browser extensions: "Colorblind" or "NoCoffee"
- macOS: System Preferences → Accessibility → Display → Color Filters
- Online: coblis.com (color blindness simulator)

**Quick test:** Convert diagram to grayscale. Can you still understand it?
</testing>
