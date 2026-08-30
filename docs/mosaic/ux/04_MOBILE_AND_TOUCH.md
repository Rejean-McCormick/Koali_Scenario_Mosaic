# Mobile and Touch

## Problem

Hover does not exist on mobile.

## Recommended interaction

### First tap
Select the cell and update a sticky panel or a card that appears below/above the mosaic.

### CTA inside the panel
**Read scenario** opens the dedicated page.

Do not rely on a second tap on the cell as the only way to open it: an explicit button is clearer.

## Mobile mosaic

Options:

1. full SVG with slight horizontal panning;
2. responsive SVG reduced enough while keeping cells tappable;
3. lightweight zoom controlled by buttons.

MVP preference: keep the full map visible, then provide an **Enlarge** control if cells become too small.

## Touch targets

Aim for at least roughly 44×44 CSS pixels whenever possible, even if the visible hexagon is smaller.

## Panel

On mobile: image + title + summary + CTA; detailed indicators can move below the summary.
