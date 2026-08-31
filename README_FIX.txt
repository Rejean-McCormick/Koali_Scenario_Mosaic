KOALI_USAGE_MOSAIC — touch-only full dossier link

Behavior
--------
On smartphones/tablets (touch/coarse pointer):
- tapping a mosaic cell still opens the temporary preview
- once a scenario is selected, a button appears:
    FR: Ouvrir le dossier complet
    EN: Open full scenario
- that button opens the normal full scenario route

On desktop/fine pointer:
- the button is completely hidden
- hover behavior remains unchanged

Files
-----
- src/components/ScenarioPreview.astro
- src/styles/mosaic.css
- scripts/build-offline-preview.py
- preview/assets/styles.css
- preview/en/index.html
- preview/fr/index.html

Apply after the current backlight/path-fix/typography overlays.
