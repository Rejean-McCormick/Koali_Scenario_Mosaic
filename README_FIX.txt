KOALI_USAGE_MOSAIC — mobile unclipped backlights

Fixes the mobile clipping visible in the screenshot.

Problem
-------
The mobile preview used fixed grid row heights. After adding two-line backlight
buttons and larger typography, the backlight row overflowed into the next row,
so icons/text (for example the lightbulb) were visibly cut.

Fix
---
On screens <= 720px:
- scenario preview height becomes content-driven
- title and summary are no longer height-clamped by the container
- backlights use 4 columns x 2 rows, 48px each
- icons and labels are fully visible
- profile height becomes automatic
- touch-only "Open full dossier" link remains visible below the backlights

Desktop is unchanged.

Files
-----
- src/styles/mosaic.css
- preview/assets/styles.css
