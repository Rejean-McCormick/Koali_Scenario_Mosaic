# Title completeness and line-box stability — v4.3.1

## Problem

The previous preview contract forced every scenario title into exactly two visible lines. This kept the Mosaic stable, but the narrative refresh introduced deliberately punchier titles that can exceed two lines. The browser then added an ellipsis, hiding meaningful text (for example the end of SCN-014).

## Fix

The preview now reserves a stable three-line title region and adapts font size by title length. Short titles remain prominent; medium and long titles step down slightly so the complete hook is much more likely to remain visible without moving the Mosaic.

```css
.preview-copy h1 {
  line-height: 1.08;
  height: 6.7rem;
  -webkit-line-clamp: 3;
}

.preview-copy h1[data-title-density="medium"] { /* slightly smaller */ }
.preview-copy h1[data-title-density="long"] { /* smaller again */ }
```

The Mosaic interaction updates `data-title-density` whenever a new scenario is selected. Static scenario pages receive the same density classification at render time.

## Invariant

- The overall preview remains layout-stable.
- A title may use up to three complete visible lines.
- Long narrative hooks are resized before they are clamped.
- The second or third line must never be vertically clipped.
- Hovering another scenario must not move the Mosaic.
- Tablet and narrow layouts reserve additional copy height so the title, summary, tags, and CTA do not collide.
