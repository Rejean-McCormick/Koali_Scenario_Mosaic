# PNG Scenario Image Loading — introduced in v3.5

## Goal

Scenario artwork should be replaceable progressively without editing the 120 Markdown records or breaking scenarios that do not yet have final art.

## Naming contract

A PNG is associated with a scenario by filename:

```text
SCN-001 → public/scenarios/images/scenario_001.png
SCN-042 → public/scenarios/images/scenario_042.png
SCN-120 → public/scenarios/images/scenario_120.png
```

Only the numeric stable scenario ID controls the association.

## Astro behavior

`src/lib/scenario-image.ts` checks the public image directory at build/dev time.

If `scenario_###.png` exists, the Mosaic preview receives:

```text
/scenarios/images/scenario_###.png
```

Otherwise it receives the scenario's existing `preview_image` SVG path.

This means final art can arrive gradually and the content schema does not have to change.

## Zero-install preview behavior

`scripts/build-offline-preview.py` applies the same lookup when generating `preview/index.html`.

PNG files are **not duplicated** into `preview/`; generated HTML references the single copy in `public/scenarios/images/` using a relative path. SVG placeholders remain copied into the lightweight preview assets for fallback scenarios.

After adding new PNGs, run:

```bash
npm run preview:offline
```

`npm run build` runs that preview regeneration automatically.

## Current packaged coverage

The supplied bundle contains 31 PNGs:

- SCN-001 through SCN-021;
- SCN-023;
- SCN-080 through SCN-084;
- SCN-100 through SCN-103.

All other scenarios continue to use their SVG placeholder.

## Validation

`npm run validate:images` checks:

- `scenario_###.png` naming;
- IDs restricted to 001–120;
- PNG binary signature and IHDR dimensions;
- Astro resolver wiring;
- offline-preview mapping;
- existence of every resolved PNG/SVG asset.

The expected result is a mixed image set until all 120 final images exist.
