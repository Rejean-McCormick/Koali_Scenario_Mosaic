KOALI_USAGE_MOSAIC — SCN image filename fix v2

Included:
- src/lib/scenario-image.ts
- scripts/validate-images.py
- scripts/build-offline-preview.py
- package.json

Key fix:
The Netlify build now runs:
  npm run preview:offline && npm run validate && astro build

This regenerates preview/en and preview/fr before validate:images checks them,
so stale scenario_###.png references are replaced by SCN-###.png references.
