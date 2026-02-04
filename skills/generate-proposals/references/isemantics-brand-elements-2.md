# iSemantics Brand Elements v2.0

## Theme Analysis from AI Automation Proposal PPTX

This document extracts the **exact** visual design language from the iSemantics AI Automation Proposal presentation (PPTX source) for replication in web formats.

---

## Color Palette (Exact Values from PPTX)

### Primary Colors

| Color | Hex (Exact) | Usage |
|-------|-------------|-------|
| **Off-White** | `#F2F2F3` | Primary headlines, main text |
| **Warm Gray** | `#E5E0DF` | Body text, descriptions, subheadings |
| **Pure Black** | `#000000` | Primary background (implied) |

### Card & UI Colors

| Color | Hex (Exact) | Usage |
|-------|-------------|-------|
| **Card Background Dark** | `#050505` | Card/panel fill (near black) |
| **Card Background Medium** | `#3D3D42` | Feature card backgrounds |
| **Border Gray** | `#56565B` | Card borders, divider lines |
| **Icon Background** | `#F2F2F3` | Icon container circles (white) |

### Border Properties

| Property | Value |
|----------|-------|
| Card border width (thick) | `30480 EMUs` (~2.4px) |
| Card border width (thin) | `7620 EMUs` (~0.6px) |
| Border color | `#56565B` |
| Border style | Solid |

---

## Accent Colors (from iSemantics Brand Guidelines)

Use these sparingly for highlights, links, and important elements.

### iSemantics Blue Palette

| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| **Primary Blue** | `#2DA7FF` | (45, 167, 255) | Links, primary highlights |
| **Light Blue** | `#92E6FD` | (146, 230, 253) | Secondary highlights, hover states |
| **Accent Blue** | `#3A5AFF` | (58, 90, 255) | CTAs, gradient start |

### iSemantics Gradient

```css
/* Primary gradient - for important highlights */
background: linear-gradient(135deg, #3A5AFF 0%, #92E6FD 100%);

/* Text gradient (for hero elements) */
background: linear-gradient(90deg, #3A5AFF, #92E6FD);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
```

**Usage Guidelines:**
- Use gradient sparingly for hero elements, CTAs, or key highlights
- Primary Blue (`#2DA7FF`) for links and interactive elements
- Light Blue (`#92E6FD`) for secondary accents and hover states

### Functional/Status Colors (Use Sparingly)

For data visualization and status indicators:

| Color | Hex | Usage |
|-------|-----|-------|
| **Success/Positive** | `#22C55E` | Green indicators, positive stats |
| **Warning** | `#EAB308` | Yellow/amber warnings |
| **Danger/Negative** | `#EF4444` | Red indicators, negative stats |

**Important:** These colors should only be used:
1. For data visualization where color conveys meaning
2. Sparingly - the main palette should dominate

### WhatsApp Brand Colors

For WhatsApp UI mockups and demonstrations only:

| Color | Hex | Usage |
|-------|-----|-------|
| **WhatsApp Green** | `#25D366` | WhatsApp UI elements, send buttons |
| **WhatsApp Dark** | `#128C7E` | WhatsApp header, status bar |

**Important:** These colors should only be used in WhatsApp interface mockups or when specifically referencing WhatsApp functionality. Do not use for general UI elements.

---

## Typography (Exact Values from PPTX)

### Font Families

| Font | Usage |
|------|-------|
| **Poppins Light** | Headlines, titles, subheadings |
| **Roboto Light** | Body text, descriptions |

### Typography Scale

| Element | Size (Points) | Font | Weight | Color |
|---------|---------------|------|--------|-------|
| **Hero Headlines** | 5400 (54pt) | Poppins Light | Light | `#F2F2F3` |
| **Slide Titles** | 4600 (46pt) | Poppins Light | Light | `#F2F2F3` |
| **Large Titles** | 4300 (43pt) | Poppins Light | Light | `#F2F2F3` |
| **Title Slide Main** | 4050 (40.5pt) | Poppins Light | Light | `#F2F2F3` |
| **Section Subheads** | 2750 (27.5pt) | Poppins Light | Light | `#F2F2F3` |
| **Card Titles** | 2700 (27pt) | Poppins Light | Light | `#E5E0DF` |
| **Card Subtitles** | 2300 (23pt) | Poppins Light | Light | `#E5E0DF` |
| **Card Titles Alt** | 2150 (21.5pt) | Poppins Light | Light | `#E5E0DF` |
| **Body Text Large** | 2150 (21.5pt) | Roboto Light | Light | `#E5E0DF` |
| **Body Text** | 1800 (18pt) | Roboto Light | Light | `#E5E0DF` |
| **Body Text Small** | 1700 (17pt) | Roboto Light | Light | `#E5E0DF` |
| **Labels/Captions** | 1300 (13pt) | Roboto Light | Light | `#E5E0DF` |

### Key Typography Observations
- **ALL text uses Light weight** (300)
- Headlines: Poppins Light
- Body: Roboto Light
- Consistent warm off-white color scheme (`#F2F2F3` for headlines, `#E5E0DF` for body)
- No bold text used in main content (bold + italic + underline only for hyperlinks)

---

## Layout Patterns

### Slide Layouts Identified

1. **Split Layout (50/50)**
   - Left: Full-bleed image (5486400 EMUs wide)
   - Right: Content on black background
   - Images positioned at x=0 or x=9144000 (right side)
   - Used for: Title slides, "Why Now?" style slides

2. **2x2 Card Grid**
   - Four equal cards in grid pattern
   - Card dimensions: ~6244709 x 2510433 EMUs
   - Gap between cards: ~200k EMUs
   - Cards have rounded corners (roundRect with adj ~3674)

3. **Stacked Cards (Vertical)**
   - Two rows of cards
   - Full-width or half-width cards
   - Consistent vertical spacing

4. **Circular Process Diagram**
   - Center circle with four surrounding elements
   - Labels positioned radially

### Card Border Radius

| Style | Value |
|-------|-------|
| Standard cards | `adj="3674"` (moderate rounding ~8-12px) |
| Accent bars | `adj="6762"` (more rounded) |
| Icon circles | `adj="13878962"` (fully circular) |
| Pill shapes | `adj="80831"` (capsule/pill) |

---

## Card Styles (Exact from PPTX)

### Standard Feature Card
```css
background: #3D3D42;
border: 0.6px solid #56565B;
border-radius: 8-12px;
/* Icon in circular white container above */
```

### Dark Accent Card (for "Current Reality" style)
```css
background: #050505;
border: 2.4px solid #56565B;
border-radius: 12px;
/* White accent bar on left edge */
```

### Accent Bar (Left Edge)
```css
width: ~10px (121920 EMUs);
background: #F2F2F3;
border-radius: pill/capsule;
height: matches parent card;
position: left edge, overlapping;
```

---

## Visual Elements

### Icon Containers
```css
/* Circular white container for icons */
background: #F2F2F3;
border-radius: 50%;
width: ~50px (658773 EMUs);
height: ~50px (658773 EMUs);
/* Icon centered inside, ~24px */
```

### Icon Specifications
- Size: 296466 EMUs (~24px)
- Format: SVG with PNG fallback
- Color: Dark (on white background) or White (standalone)

### Images
- Full-bleed images: 5486400 x 8229600 EMUs (9:16 portrait ratio)
- Positioned at x=0 or x=9144000 for split layouts
- No border/effects

---

## Component Patterns

### Card with Icon (2x2 Grid Style)
```
┌─────────────────────────────────────┐
│ ┌────┐                              │
│ │icon│  (white circle, dark icon)   │
│ └────┘                              │
│                                     │
│ Card Title                          │
│ (Poppins Light 21.5pt #E5E0DF)      │
│                                     │
│ Description text goes here with    │
│ multiple lines if needed            │
│ (Roboto Light 17pt #E5E0DF)         │
└─────────────────────────────────────┘
Background: #3D3D42
Border: 0.6px solid #56565B
```

### Accent Card (Left Bar Style)
```
┌──────────────────────────────────────┐
│▌                                     │
│▌ Section Title                       │
│▌ (Poppins Light 23pt #E5E0DF)        │
│▌                                     │
│▌ Body text description that spans   │
│▌ multiple lines as needed            │
│▌ (Roboto Light 18pt #E5E0DF)         │
│▌                                     │
└──────────────────────────────────────┘
▌= White accent bar (#F2F2F3)
Background: #050505
Border: 2.4px solid #56565B
```

---

## Logo Placement

### iSemantics Logo
- **Position:** Bottom-right corner
- **Size:** ~795576 x 523875 EMUs (~66px x 44px)
- **Offset:** ~13641705 x ~7498437 EMUs from origin

---

## Tailwind CSS Implementation

### Updated Tailwind Config

```javascript
theme: {
  extend: {
    colors: {
      // Core theme colors (from AI Automation Proposal PPTX)
      'bg-primary': '#000000',
      'bg-card-dark': '#050505',
      'bg-card': '#3D3D42',
      'border-card': '#56565B',
      'text-headline': '#F2F2F3',
      'text-body': '#E5E0DF',
      'icon-bg': '#F2F2F3',

      // Accent colors (from iSemantics Brand Guidelines) - USE SPARINGLY
      'accent-blue': '#3A5AFF',     // Gradient start, CTAs
      'primary-blue': '#2DA7FF',    // Links, highlights
      'light-blue': '#92E6FD',      // Gradient end, hover states

      // Functional colors (for data viz/status only)
      'status-success': '#22C55E',
      'status-warning': '#EAB308',
      'status-danger': '#EF4444',

      // WhatsApp (for WhatsApp UI context ONLY)
      'whatsapp-green': '#25D366',
      'whatsapp-dark': '#128C7E',
    },
    fontFamily: {
      'headline': ['Poppins', 'sans-serif'],
      'body': ['Roboto', 'sans-serif'],
    },
    fontWeight: {
      'light': 300,
    },
    fontSize: {
      'hero': ['54px', { lineHeight: '1.2' }],
      'title-lg': ['46px', { lineHeight: '1.2' }],
      'title': ['43px', { lineHeight: '1.2' }],
      'title-sm': ['40px', { lineHeight: '1.25' }],
      'subhead': ['27px', { lineHeight: '1.3' }],
      'card-title': ['23px', { lineHeight: '1.3' }],
      'card-title-sm': ['21px', { lineHeight: '1.3' }],
      'body-lg': ['21px', { lineHeight: '1.6' }],
      'body': ['18px', { lineHeight: '1.65' }],
      'body-sm': ['17px', { lineHeight: '1.65' }],
      'caption': ['13px', { lineHeight: '1.5' }],
    },
    borderWidth: {
      'card': '0.6px',
      'card-thick': '2.4px',
    },
  }
}
```

### Key CSS Classes

```css
/* Backgrounds */
.bg-black               /* Primary slide background */
.bg-card-dark           /* #050505 - dark accent cards */
.bg-card                /* #3D3D42 - feature cards */

/* Text */
.text-headline          /* #F2F2F3 - Headlines */
.text-body              /* #E5E0DF - Body text */
.font-headline          /* Poppins */
.font-body              /* Roboto */
.font-light             /* Weight 300 - USE EVERYWHERE */

/* Borders */
.border-card            /* #56565B */
.border-card            /* 0.6px width */
.border-card-thick      /* 2.4px width */
.rounded-lg             /* Card corners ~12px */

/* Icon containers */
.bg-icon-bg             /* #F2F2F3 white circle */
.rounded-full           /* Circular */
.w-12 .h-12             /* 48px icon container */

/* Accent colors (use sparingly) */
.text-primary-blue      /* #2DA7FF - Links */
.text-light-blue        /* #92E6FD - Hover states */
.text-accent-blue       /* #3A5AFF - CTAs */

/* Functional colors (data viz/status only) */
.text-status-success    /* #22C55E - Positive */
.text-status-warning    /* #EAB308 - Warning */
.text-status-danger     /* #EF4444 - Negative */
```

### Gradient Utilities (Custom CSS)

```css
/* iSemantics gradient for backgrounds */
.bg-gradient-isemantics {
  background: linear-gradient(135deg, #3A5AFF 0%, #92E6FD 100%);
}

/* iSemantics gradient for text */
.text-gradient-isemantics {
  background: linear-gradient(90deg, #3A5AFF, #92E6FD);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Link styling */
a.link {
  color: #2DA7FF;
  text-decoration: none;
  transition: color 0.2s ease;
}
a.link:hover {
  color: #92E6FD;
}
```

---

## Google Fonts Import

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300&family=Roboto:wght@300&display=swap" rel="stylesheet">
```

---

## Key Differences from Current Noura Deck

| Element | Current Noura Deck | New iSemantics Style (Exact) |
|---------|-------------------|------------------------------|
| Background | `#000032` (Dark Navy) | `#000000` (Pure Black) |
| Card BG | Blue-tinted | `#3D3D42` or `#050505` |
| Headlines | Bold weight | **Light weight (300)** |
| Headline font | Plus Jakarta Sans | **Poppins Light** |
| Body font | Plus Jakarta Sans | **Roboto Light** |
| Text color | White `#FFFFFF` | Off-white `#F2F2F3` / `#E5E0DF` |
| Card borders | Gradient/glow | Solid `#56565B` |
| Card radius | Large rounded | Moderate ~12px |
| Layout | Centered, contained | Split layouts, offset text |

---

## iSemantics Special Design Cards

### Glassmorphism Hero Card (Featured/Primary Card)

Used for highlighting the primary deliverable or hero element. Distinguished from standard cards with a blue-tinted glassmorphism effect.

#### Card Container

```css
/* Glassmorphism Hero Card */
.hero-card {
  background: linear-gradient(135deg,
    rgba(45, 167, 255, 0.12) 0%,      /* Primary Blue at 12% */
    rgba(58, 90, 255, 0.08) 50%,       /* Accent Blue at 8% */
    rgba(255, 255, 255, 0.04) 100%     /* White at 4% */
  );
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(45, 167, 255, 0.25);  /* Primary Blue at 25% */
  border-radius: 24px;  /* rounded-3xl */
  padding: 24px;
  position: relative;
  overflow: hidden;
  transition: all 0.5s ease;
}

.hero-card:hover {
  transform: scale(1.03);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}
```

#### Animated Glow Effects (Background Orbs)

```css
/* Top-right glow orb */
.hero-card::before {
  content: '';
  position: absolute;
  top: -40px;
  right: -40px;
  width: 128px;
  height: 128px;
  background: rgba(45, 167, 255, 0.2);  /* Primary Blue at 20% */
  border-radius: 50%;
  filter: blur(32px);
  transition: background 0.5s ease;
}

.hero-card:hover::before {
  background: rgba(45, 167, 255, 0.3);  /* Intensify on hover */
}

/* Bottom-left glow orb */
.hero-card::after {
  content: '';
  position: absolute;
  bottom: -32px;
  left: -32px;
  width: 96px;
  height: 96px;
  background: rgba(146, 230, 253, 0.15);  /* Light Blue at 15% */
  border-radius: 50%;
  filter: blur(32px);
  transition: background 0.5s ease;
}

.hero-card:hover::after {
  background: rgba(146, 230, 253, 0.25);  /* Intensify on hover */
}
```

#### Signature Accent Line (Bottom Edge)

```css
/* Subtle gradient line at card bottom */
.hero-card-accent-line {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(45, 167, 255, 0.5) 50%,  /* Primary Blue at 50% */
    transparent 100%
  );
}
```

#### Hero Card Title (Gradient Text)

```css
/* Gradient text for hero card titles */
.hero-card-title {
  font-family: 'Poppins', sans-serif;
  font-weight: 300;
  font-size: 18px;  /* text-lg */
  background: linear-gradient(90deg, #F2F2F3 0%, #92E6FD 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

---

### Standard Glassmorphism Card (Secondary Cards)

Used for non-featured items in the same grid.

```css
/* Standard glassmorphism card */
.glass-card {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.08) 0%,
    rgba(255, 255, 255, 0.02) 100%
  );
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 24px;
  transition: all 0.3s ease;
}

.glass-card:hover {
  transform: scale(1.02);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}
```

#### Standard Icon Container

```css
/* Icon container for standard cards */
.glass-icon-container {
  width: 48px;
  height: 48px;
  border-radius: 16px;  /* rounded-2xl */
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.15) 0%,
    rgba(255, 255, 255, 0.05) 100%
  );
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.15);
}

/* Icon styling */
.glass-icon-container svg {
  width: 24px;
  height: 24px;
  color: #F2F2F3;
  stroke-width: 1.5;
}
```

---

### Design Token Reference

| Token | Value | Usage |
|-------|-------|-------|
| `hero-card-bg-start` | `rgba(45, 167, 255, 0.12)` | Hero card gradient start |
| `hero-card-bg-mid` | `rgba(58, 90, 255, 0.08)` | Hero card gradient middle |
| `hero-card-bg-end` | `rgba(255, 255, 255, 0.04)` | Hero card gradient end |
| `hero-card-border` | `rgba(45, 167, 255, 0.25)` | Hero card border |
| `hero-glow-primary` | `rgba(45, 167, 255, 0.2)` | Top-right glow orb |
| `hero-glow-secondary` | `rgba(146, 230, 253, 0.15)` | Bottom-left glow orb |
| `glass-card-bg-start` | `rgba(255, 255, 255, 0.08)` | Standard card gradient start |
| `glass-card-bg-end` | `rgba(255, 255, 255, 0.02)` | Standard card gradient end |
| `glass-card-border` | `rgba(255, 255, 255, 0.1)` | Standard card border |

---

*Document Version: 2.1*
*Source: AI-Automation-Proposal-for-Influencer-Funnel-and-Outreach.pptx (PPTX extracted)*
*Updated: December 2025*
