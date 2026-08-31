# v4.3.4 — Two-tone Koali brand checker

The eight category territories no longer use an eight-hue rainbow palette. The Mosaic now uses two tones derived from the Koali brand color and alternates them spatially as a checker.

## Palette

- Tone A — canonical Koali: `#1e6864`
- Tone B — lighter Koali teal: `#4a9690`

## Territory assignment

```text
Top row:    CAT-01 A · CAT-02 B · CAT-03 A · CAT-04 B
Bottom row: CAT-05 B · CAT-06 A · CAT-07 B · CAT-08 A
```

This makes every horizontally or vertically neighboring territory visually alternate while keeping the entire map inside one brand family. Category identity is carried primarily by spatial position and the embedded magnetic label.

The same A/B mapping is reused in the scenario profile accent, public scenario information honeycomb, cover art, and SVG scenario fallbacks.

## Magnetic label contrast

Because the labels now sit on closely related teal fields, their resting treatment is intentionally brighter than in v4.3.2: the label color mixes 76% white with the local territory tone, resting opacity is 0.46, and the active territory rises to 0.82 with a small dark text shadow. The letters still repel and spring independently; the honeycomb remains fixed.
