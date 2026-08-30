# Title line-box stability — v3.4

## Problem

Some two-line scenario titles were visually clipped through the second line even though the preview panel itself stayed at a fixed height. The cause was the title box: it reserved only `2.05em`, while the browser's actual line boxes required more vertical space.

## Fix

The title now has an explicit line height and a non-shrinking flex basis. It reserves slightly more than two true line boxes:

```css
.preview-copy h1 {
  line-height: 1.12;
  flex: 0 0 2.5em;      /* fallback */
  block-size: 2.25lh;    /* line-height-relative size */
  -webkit-line-clamp: 2;
}
```

The `lh` unit ties the reserved block size to the computed line height rather than assuming that one `em` equals one rendered line. The `flex` basis prevents the title region from being compressed by the surrounding summary, tags, or CTA.

## Invariant

- The overall preview height remains fixed.
- A title may use up to two complete visible lines.
- A longer title may be clamped/ellipsized after line two, but the second line itself must never be vertically clipped.
- Hovering another scenario must not move the Mosaic.
