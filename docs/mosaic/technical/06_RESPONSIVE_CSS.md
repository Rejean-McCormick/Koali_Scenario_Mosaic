# Responsive CSS

## Large desktop

Preview panel in 3 columns, wide mosaic below.

## Laptop

Preview panel in 2 columns; indicators may move below the text.

## Tablet

Compact vertical panel; mosaic uses full width.

## Mobile

Sticky selected-scenario panel or lightweight drawer; reduced mosaic with generous hit areas.

## CSS tokens

Define:

```css
:root {
  --mosaic-bg: ...;
  --mosaic-cell-gap: ...;
  --mosaic-cell-scale-hover: 1.12;
  --preview-radius: ...;
  --motion-fast: 120ms;
}
```

## Layout shift

The panel should have a stable `min-height` per breakpoint so content changes do not move the mosaic up and down.
