KOALI_USAGE_MOSAIC — typography Windows-scale overlay

Goal
----
Increase small UI text so it visually aligns better with the Windows/Chrome
interface visible around the application, while preserving the existing layout.

Main adjustments
----------------
Backlight labels:
  ~8.5 px -> ~10.2 px
  icons: 14 px -> 16 px
  height: 38 px -> 44 px

Scenario profile:
  micro labels: ~9.3 px -> ~10.7 px
  activity/context values: ~9.9 px -> ~11.2-11.4 px
  pattern text: ~12.2 px -> ~13.4 px

Scenario hexagons:
  headings: ~10.6 px -> ~11.8 px
  body: ~13.4 px -> ~14.7 px
  strong values: ~15 px -> ~16.3 px

Header:
  secondary brand text and language switcher enlarged slightly.

The main scenario title is intentionally not enlarged substantially because it
was already at a strong desktop reading size.

Files
-----
- src/styles/global.css
- src/styles/mosaic.css
- src/styles/scenario.css
- preview/assets/styles.css

Apply this overlay over the current backlight/path-fix state.
