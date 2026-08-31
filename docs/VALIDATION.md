# Validation — v4.3.2

## v4.3.4 brand checker

`npm run validate` passes with the two-tone Koali checker (`#1e6864` / `#4a9690`) mapped A/B/A/B on the top row and B/A/B/A on the bottom row. The offline bilingual preview was regenerated. See `VALIDATION_V4_3_4.txt`.


## Result

The refreshed v4.3.1 scenario corpus and the v4.3 magnetic interface pass the repository validation contract together.

Validated:

- 120 shared scenario identities;
- 120 English + 120 French editorial documents;
- all 240 localized scenario files exactly match the supplied v4.3.1 corpus;
- `src/data/scenarios.json` exactly matches the supplied v4.3.1 corpus;
- `src/i18n/fr-tags.json` exactly matches the supplied v4.3.1 corpus;
- 20 × 6 regular honeycomb geometry;
- 8 contiguous 5 × 3 territories;
- 8 versioned magnetic territory anchors;
- EN/FR magnetic territory labels;
- GSAP/SplitText magnetic progressive-enhancement contract;
- fine-pointer and reduced-motion gates;
- adaptive short/medium/long title density for refreshed titles;
- 31 PNG scenario images and 89 SVG fallbacks;
- bilingual public scenario routes and selected-state pages;
- internal governance markers excluded from generated public scenario bodies;
- 2,422 generated offline local `href`/`src` references checked;
- 0 broken local references;
- canonical Koali branding and `#1e6864`.

See `VALIDATION_V4_3_2.txt` for command output.

## Build caveat

A fresh `npm install` attempt timed out in the generation environment before `node_modules` was created, so a full fresh Astro build is not claimed here. The production build command remains `npm run validate && astro build`, and Netlify remains configured for Node 24.20.0.
