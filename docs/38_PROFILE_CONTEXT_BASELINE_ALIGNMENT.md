# Profile Context Baseline Alignment — v3.9

## Problem

The public scenario-profile metadata uses a narrow label column. A label such as **SPECIAL CONDITIONS** can wrap to two lines. Previously, its value was aligned with the top of the grid row, visually pairing `Role Routing` with `SPECIAL` while `CONDITIONS` appeared underneath.

## Rule

Each metadata row now aligns its label and value to the **bottom edge of the row**.

```text
SCALE       Organization
CONTEXT     Enterprise · Maintenance · Elevator
SPECIAL
CONDITIONS  Role Routing
```

This keeps the value visually attached to the final line of a wrapped label. One-line rows remain unchanged.

## Implementation

`src/styles/mosaic.css` uses bottom alignment on `.profile-context > div`, and the label/value share the same compact line-height. The offline preview is regenerated from the same CSS.

## Invariant

`validate:repo` now checks for the bottom-alignment rule so a future CSS refactor cannot silently restore top-aligned values.
