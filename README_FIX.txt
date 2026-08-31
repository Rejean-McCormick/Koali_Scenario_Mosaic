KOALI_USAGE_MOSAIC — fixed backlight palette overlay

Behavior
--------
The palette/action indicators no longer disappear, change width, or get rebuilt
when hovering/focusing another scenario.

Eight fixed indicators are always visible:
- Find / Trouver
- Understand / Comprendre
- Learn / Apprendre
- Collaborate / Collaborer
- Choose / Choisir
- Act / Agir
- Respond / Répondre
- Remember / Se souvenir

Inactive:
- muted grey
- low icon opacity
- no glow

Active:
- brighter foreground
- teal backlight
- subtle inner + outer glow

All 15 original palette keys are covered by these 8 stable groups.

This overlay also preserves:
- local SVG icons
- two-line icon-over-label layout
- square scenario image preview
- generated EN/FR offline preview
