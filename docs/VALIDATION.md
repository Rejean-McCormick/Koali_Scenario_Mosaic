# Validation report — v4.0 bilingual

## Corpus

- shared scenario identities: **120**;
- English editorial scenario documents: **120**;
- French editorial scenario documents: **120**;
- EN/FR scenario ID parity: **120 / 120**;
- category balance: **15 scenarios × 8 families**;
- recurring pattern labels: **24 EN + 24 FR**.

## Bilingual contract

- one shared `src/data/scenarios.json` metadata layer;
- localized Markdown does not duplicate machine-facing scenario metadata;
- complete French labels for every public scale, setting, property, domain, transfer-domain, and palette key used by the corpus;
- `/en/uses/` and `/fr/uses/` route architecture present;
- language switch preserves the current scenario path;
- root browser-language chooser present;
- zero-install preview generated in both languages.

## Interaction contract

- 120 assignments;
- 150 layout slots, including 30 reserved slots;
- regular **20 × 6** panoramic honeycomb;
- eight contiguous **5 × 3** category territories;
- one active/highlighted hexagon at a time;
- no related-cell highlight;
- fixed preview geometry;
- two-line title box without clipping;
- color legend present;
- bottom-aligned profile metadata.

## Images

- PNG scenario images available: **31 / 120**;
- SVG fallback scenarios: **89**;
- both EN and FR previews resolve the same image identity;
- image-path validation passes.

## Offline preview

Generated HTML files: **245**:

- 1 language chooser;
- 2 Mosaic pages;
- 2 localized scenario lists;
- 240 localized detailed scenario pages.

A structural local-reference audit checked **1,942** `href`/`src` references with **0 broken local references**.

## Production build environment

Production configuration:

- Astro `7.2.9`;
- Node target `24.20.0` via `.nvmrc` and `netlify.toml`;
- Netlify build command: `npm run build`;
- publish directory: `dist`;
- production build does **not** invoke `preview:offline` or require PyYAML.

## Current environment note

All repository, geometry, image, copy, i18n, and naming validators pass locally. A fresh `npm install` could not be completed in the artifact container because dependency download timed out, so a fresh Astro dependency build was not claimed from this environment. Netlify/GitHub environments are configured to install dependencies and run the same production build.

## Result

**PASS — source/preview validation.**
