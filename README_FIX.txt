KOALI_USAGE_MOSAIC — SCN image filename fix v3

Fixes included:
- SCN-###.png naming in Astro resolver
- SCN-###.png naming in image validation
- SCN-###.png naming in offline preview generation
- offline preview regenerated before validation
- PyYAML installed during Netlify build before preview generation

Build command executed by npm:
  python -m pip install PyYAML && npm run preview:offline && npm run validate && astro build
