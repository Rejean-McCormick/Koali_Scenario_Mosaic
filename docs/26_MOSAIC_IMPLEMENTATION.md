# Mosaic implementation

The Astro application lives at the **repository root**.

Key paths:

- [`../package.json`](../package.json) — scripts/dependencies;
- [`../src/content/scenarios/`](../src/content/scenarios/) — 120 canonical scenarios;
- [`../src/components/`](../src/components/) — Mosaic UI;
- [`../src/pages/uses/`](../src/pages/uses/) — Mosaic/list/scenario routes;
- [`../src/data/mosaic-layout.json`](../src/data/mosaic-layout.json) — fixed 150-slot composition;
- [`../public/`](../public/) — runtime assets;
- [`../preview/`](../preview/) — dependency-free generated preview;
- [`../scripts/`](../scripts/) — validation, preview generation and slot tooling.

## Develop

```bash
npm install
npm run dev:open
```

## Build

```bash
npm run validate
npm run build
```

## Add scenario 121+

1. Add `src/content/scenarios/SCN-121.md`.
2. Add required preview metadata.
3. Run `npm run slot:assign -- SCN-121`.
4. Run `npm run validate`.
5. Run `npm run preview:offline`.

Existing cells do not move.
