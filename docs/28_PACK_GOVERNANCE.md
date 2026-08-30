# Repository governance and source-of-truth hierarchy

1. **External Koali capability / possibility canon** — authority for capability and evidence status.
2. **`src/content/scenarios/SCN-*.md`** — authority for the 120 public scenario texts and preview metadata.
3. **`src/data/mosaic-layout.json`** — authority for current Mosaic placement. Coordinates are presentation decisions, not semantic truth.
4. **Astro components/pages** — executable presentation of canonical content.
5. **`preview/`** — generated convenience artifact; never edit it as source.
6. **`docs/`** — explanatory and editorial documentation.

Edit scenarios only in `src/content/scenarios/`. Move cells only through the versioned layout. Rebuild `preview/` after content or UI changes.

The public spatial interface is **Koali Use Mosaic**.
