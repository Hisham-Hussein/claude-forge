# Excalidraw Technical Specifications

Reference for generating valid Excalidraw clipboard JSON. Read this when generating slide JSON.

## Table of Contents

- [JSON Structure](#json-structure)
- [Canvas Layout](#canvas-layout)
- [Element Specifications](#element-specifications)
- [Color Palette](#color-palette)
- [Visual Hierarchy Rules](#visual-hierarchy-rules)
- [Icon Usage](#icon-usage)

---

## JSON Structure

The top-level clipboard format. All child elements go first, frame goes last.

```json
{
  "type": "excalidraw/clipboard",
  "elements": [ /* all children FIRST, frame LAST */ ],
  "files": {}
}
```

## Canvas Layout

| Zone | Y Coordinates | Purpose |
|------|---------------|---------|
| Header | 30 - 100 | Title bar, slide identifier |
| Main Content | 110 - 650 | Primary diagram area |
| Footer | 660 - 760 | Callouts, legends, tips |

- **Frame Size:** 1200 x 800 pixels (adjust height if needed for complex slides)
- **Margins:** 50px minimum from frame edges
- **Element Spacing:** 30px minimum between elements

## Element Specifications

Every element must include `frameId` matching the slide's frame ID.

### Frame (Always Last in Array)

```json
{
  "type": "frame",
  "id": "frame_N",
  "x": 0,
  "y": 0,
  "width": 1200,
  "height": 800,
  "name": "Slide N - Title",
  "strokeColor": "#bbb"
}
```

### Rectangle

```json
{
  "type": "rectangle",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "roundness": { "type": 3 },
  "frameId": "frame_N"
}
```

### Ellipse

```json
{
  "type": "ellipse",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "frameId": "frame_N"
}
```

### Diamond

```json
{
  "type": "diamond",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "frameId": "frame_N"
}
```

### Arrow

```json
{
  "type": "arrow",
  "strokeWidth": 2,
  "roundness": { "type": 2 },
  "points": [[0, 0], [endX, endY]],
  "frameId": "frame_N"
}
```

### Line

```json
{
  "type": "line",
  "strokeWidth": 2,
  "points": [[0, 0], [endX, endY]],
  "frameId": "frame_N"
}
```

### Text

Text elements **must** include `width` and `height` for proper rendering.

```json
{
  "type": "text",
  "fontFamily": 5,
  "fontSize": 14,
  "strokeColor": "#1e1e1e",
  "width": 100,
  "height": 20,
  "frameId": "frame_N"
}
```

## Color Palette

| Purpose | Color Code | Name |
|---------|------------|------|
| Primary Accent | `#b2f2bb` | Mint Green |
| Strong Accent / CTA | `#2f9e44` | Dark Green |
| Warning / Danger | `#fa5252` | Red |
| Info / Links | `#228be6` | Blue |
| Neutral Background | `#e9ecef` | Light Grey |
| Caution / Notes | `#fff9db` | Light Yellow |
| Info Background | `#e7f5ff` | Light Blue |
| Success Background | `#ebfbee` | Pale Mint |
| Warning Background | `#ffe3e3` | Light Red |
| Text (default) | `#1e1e1e` | Dark Grey |
| Secondary Text | `#868e96` | Medium Grey |

## Visual Hierarchy Rules

1. **One focal point** per slide — largest, brightest, or center-positioned element
2. **Flow direction** — guide the eye left-to-right or top-to-bottom
3. **Color grouping** — related items share a color family
4. **Emphasis** — priority items get `strokeWidth: 3` and darker stroke color
5. **Contrast** — important elements use saturated colors; secondary elements use neutral colors

## Icon Usage

Use emoji inside shapes or as standalone visual markers:

| Icon | Meaning | Icon | Meaning |
|------|---------|------|---------|
| 🎯 | Target/Goal | ⚡ | Fast/Energy |
| 💡 | Insight/Idea | 🔥 | Hot/Trending |
| ⭐ | Priority/Star | ✅ | Done/Success |
| ⚠️ | Warning | ❌ | Error/Avoid |
| 💰 | Money/Revenue | 📈 | Growth |
| 👤 | Person/User | 👥 | Team/People |
| 🛠️ | Tools/Build | 🔍 | Search/Discovery |
| 📋 | Document/List | 🎁 | Free/Gift |
| 💎 | Value/Premium | 🏗️ | Construction |
