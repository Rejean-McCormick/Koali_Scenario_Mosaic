KOALI_USAGE_MOSAIC — mobile tap = temporary preview

Behavior
--------
On touch/coarse-pointer devices:
- tapping a mosaic hexagon DOES NOT navigate to the full scenario page
- the scenario is loaded into the existing temporary preview panel
- the page scrolls smoothly to the preview
- the explicit preview CTA can still be used to open the full page

On desktop/fine-pointer devices:
- existing hover/focus/navigation behavior is unchanged

Files
-----
- src/scripts/mosaic.ts
- preview/assets/app.js

Apply this overlay after the current backlight/path-fix overlays.
