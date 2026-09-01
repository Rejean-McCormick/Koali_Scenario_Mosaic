# Responsive Preview and Cover

## Media states

The initial cover and selected scenario imagery keep separate fitting rules:

- initial cover: `object-fit: contain`;
- selected scenario image: `object-fit: cover`.

The image shell always remains square. It is never stretched vertically to
match the copy or profile blocks.

## Container-driven geometry

Responsive geometry follows the width of `.mosaic-experience`, not the browser
viewport. The element is named `scenario-layout` and supplies the container
queries used by the preview.

### Wide — 1120 px and above

The preview uses three columns:

```text
250–292 px image | flexible copy, minimum 480 px | 300–340 px profile
```

The copy is intentionally dominant. The profile is capped because its system
and context content does not benefit from unlimited proportional growth.

### Intermediate — 721–1119 px

The image and copy share the first row. The profile spans the complete second
row:

```text
┌──────────────┬─────────────────────────┐
│ cover/image  │ title + summary + CTA   │
├──────────────┴─────────────────────────┤
│ scenario profile                       │
└────────────────────────────────────────┘
```

This earlier transition prevents the copy column from collapsing just above
the former 900 px viewport breakpoint.

### Narrow — 720 px and below

The reading order is:

```text
copy
scenario profile
cover/image
```

The action palette uses a fixed 4 × 2 grid. Only the panoramic Mosaic may
scroll horizontally; the preview remains container-bound.

## Validation contract

`validate:repo` checks the named container, the three geometry ranges, the
wide column bounds, the square media behavior, and the two distinct image
fitting states.
