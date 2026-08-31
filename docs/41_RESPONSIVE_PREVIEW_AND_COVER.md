# Responsive Preview and Cover — v4.1

## Problem observed

At a narrow/tablet viewport, the preview could visually spill beyond the right edge of the browser. The initial Mosaic cover was also treated like a scenario photograph with `object-fit: cover`, which cropped its embedded branding severely.

The color legend also carried a `min-width: 760px` directly on the legend element. On narrower viewports this could create page-level horizontal overflow instead of containing overflow inside the Mosaic region.

## Design decision

The initial cover and scenario imagery are different media states and should not share the same fitting rule.

### Initial state

The cover is now a **text-free abstract graphic** representing the eight scenario territories. It does not repeat the product name already present in the site header and preview copy.

The initial image uses:

```css
object-fit: contain;
```

### Scenario-selected state

When hover/focus selects a scenario, JavaScript changes the image state to `scenario`. Scenario PNG/SVG imagery then uses:

```css
object-fit: cover;
```

This preserves the photographic/full-bleed behavior of real scenario art without forcing that crop behavior onto the cover.

## Responsive geometry

### Desktop

The existing three-column, fixed-height preview remains.

### Tablet — up to 900 px

The preview becomes:

```text
┌──────────────┬─────────────────────────┐
│ cover/image  │ title + summary + CTA   │
├──────────────┴─────────────────────────┤
│ scenario profile strip                 │
└────────────────────────────────────────┘
```

Both columns use `minmax(0, …)` and all major children have explicit `min-width: 0`, preventing intrinsic content from widening the grid.

### Narrow — below 720 px

The preview becomes a single-column stack:

```text
cover/image
copy
scenario profile
```

No preview content is expected to require horizontal page scrolling.

## Legend and Mosaic overflow

At tablet width the legend reflows to two columns and has no artificial minimum width.

Below 720 px, the panoramic Mosaic may scroll horizontally inside `.mosaic-stage`, while the rest of the page remains viewport-bound. This is intentional: the panorama is the only surface that may need horizontal exploration on a narrow screen.

## Validation contract

`validate:repo` checks that:

- the tablet grid uses bounded `minmax(0, …)` columns;
- a single-column narrow breakpoint exists;
- the cover uses `object-fit: contain`;
- selected scenario imagery uses `object-fit: cover`;
- JavaScript switches the image media state on scenario selection;
- the initial cover SVG contains no visible `<text>` branding.
