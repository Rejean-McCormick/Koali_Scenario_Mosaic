KOALI_USAGE_MOSAIC — SCN image filename fix v4

This overlay follows the repository's validation contract.

Included:
- package.json
- src/lib/scenario-image.ts
- scripts/validate-images.py
- scripts/build-offline-preview.py
- regenerated preview/ directory (247 files)

Production build restored to:
  npm run validate && astro build

The offline preview is pre-generated/committed instead of generated inside
the Netlify production build.

Image resolution:
- SCN-001 through SCN-060 -> public/scenarios/images/SCN-###.png
- SCN-061 through SCN-120 -> SVG fallback
