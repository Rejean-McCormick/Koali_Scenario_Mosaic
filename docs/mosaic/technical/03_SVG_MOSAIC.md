# SVG Mosaic

## Why SVG

With 120 cells, SVG keeps each element in the DOM: links, focus, hover, ARIA attributes, and CSS remain straightforward. Canvas/WebGL would add hit-testing, accessibility work, and complexity without a necessary benefit.

## Structure

```html
<svg viewBox="0 0 1440 900" role="group" aria-labelledby="mosaic-title mosaic-desc">
  <title id="mosaic-title">Koali Use Mosaic</title>
  <desc id="mosaic-desc">120 interactive scenarios...</desc>

  <a href="/uses/SCN-001/" data-scenario-id="SCN-001" aria-label="...">
    <polygon points="..." />
  </a>
</svg>
```

## Hexagonal cell

For center `(cx, cy)` and radius `r`, the six vertices can be precomputed at build time. There is no reason to recalculate them on every hover.

## Hit area

If the visible cell is small, add a slightly larger transparent shape inside the link to improve pointer/touch targeting without altering the visible design.

## DOM order

DOM order can follow ID or editorial order. Visual position must not determine keyboard accessibility order.

## Performance

120 links + polygons are very light. Avoid expensive SVG filters, complex shadows on every cell, or continuous animation.
