# Panoramic Spread and Color Legend — v3.7

## Problem addressed

The previous 12 × 10 honeycomb was mathematically regular, but it was too tall for the interaction model. On a laptop, users could need to scroll down before reaching the lower cells. Once they did, the scenario preview at the top was no longer visible, weakening the core hover → preview relationship.

The category colors also had no immediate public legend, so a visitor could see different hues without knowing what they meant.

## Design decision

The Mosaic is now treated as a **panoramic spread**, not a vertical wall.

### Active geometry

- 120 scenarios;
- 20 columns × 6 rows;
- pointy-top regular hexagons;
- exact horizontal spacing `sqrt(3) × radius`;
- exact vertical spacing `1.5 × radius`;
- alternate rows offset by exactly half the horizontal spacing.

The SVG is given a bounded desktop height (`180–220px`) so its visual size is controlled by the viewport rather than expanding to the full available width.

## Eight category territories

The corpus already contains exactly 15 scenarios in each of the eight public categories. v3.7 uses that symmetry directly.

The 20 × 6 active grid is divided into eight contiguous **5 × 3 territories**:

```text
TOP HALF
┌─────────┬─────────┬─────────┬─────────┐
│ CAT-01  │ CAT-02  │ CAT-03  │ CAT-04  │
│  5 × 3  │  5 × 3  │  5 × 3  │  5 × 3  │
└─────────┴─────────┴─────────┴─────────┘

BOTTOM HALF
┌─────────┬─────────┬─────────┬─────────┐
│ CAT-05  │ CAT-06  │ CAT-07  │ CAT-08  │
│  5 × 3  │  5 × 3  │  5 × 3  │  5 × 3  │
└─────────┴─────────┴─────────┴─────────┘
```

The cells never leave the common honeycomb lattice. “Territory” describes editorial grouping, not a separate or dynamically generated layout.

## Color legend

A compact legend appears immediately above the panorama. It uses the same four-by-two ordering as the category territories and the same colors as the cells.

The legend is intentionally informational rather than interactive in v3.7. Hover remains reserved for individual scenarios, which preserves the rule that only one hexagon can be highlighted at a time.

## One-viewport target

On a normal desktop/laptop viewport, the intended composition is:

```text
Scenario preview
Controls
4 × 2 category legend
20 × 6 Mosaic panorama
```

The preview remains fixed-height and the Mosaic uses a viewport-bounded height. The design goal is that users can hover the lower spread while still seeing the preview update above.

At smaller widths, the panorama can scroll horizontally rather than becoming tall again.

## Stability rules

The following are validated automatically:

- exactly 120 active assignments;
- exactly 150 total slots, with 30 reserved;
- 20 × 6 active geometry;
- exact honeycomb spacing and alternating offset;
- eight contiguous 5 × 3 territories;
- panoramic viewBox ratio greater than 3.4:1;
- single active-cell highlight;
- no related-cell highlighting;
- color legend present;
- compact desktop preview and bounded Mosaic height.

## Production build

v3.7 also keeps the Netlify production build independent from the offline-preview generator:

```text
npm run build = npm run validate && astro build
```

`npm run preview:offline` remains available explicitly for preparing the double-click package preview.
