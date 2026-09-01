# Title completeness and line-box stability — superseded

The v4.3.1 implementation reserved a fixed three-line title box and selected a
font size from the title's character count. That rule is superseded by the
current preview layout contract.

## Current rule

- The title has natural height and uses at most two visible lines.
- It starts at the normal display size.
- `preview-layout.ts` progressively reduces only the title font size until the
  text fits on two lines.
- The reduction stops at a readable minimum.
- If an extreme title still does not fit, the browser clamps it to two lines.
- `text-wrap: balance` improves the distribution of words.

The fit is measured from rendered dimensions rather than character count. It
is recalculated after scenario changes, width changes, browser zoom, and font
loading. No fixed one-, two-, or three-line height is reserved.

## Stability invariant

The title, summary, and example remain naturally packed at the top. A flexible
row absorbs the remaining height. The CTA and action palette stay anchored at
the bottom of block 2, so title fitting does not move the functional baseline.

See `PREVIEW_LAYOUT_INTERACTION_CONTRACT.md` for the active contract.
