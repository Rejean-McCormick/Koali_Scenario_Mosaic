# GitHub repository layout

## Goal

The repository should feel normal to both a non-technical recipient and a developer. Opening the root shows the executable project first, while the full body of documentation lives under `docs/`.

## Root contract

- `START.html` — zero-install entry point;
- `START.bat`, `START.command`, `START.sh` — convenience launchers;
- `START_DEV.*` — development launchers;
- `package.json`, `astro.config.mjs`, `tsconfig.json` — standard Astro project files;
- `src/` — canonical application/content source;
- `public/` — public assets;
- `scripts/` — maintenance/validation tooling;
- `preview/` — generated file-safe preview;
- `docs/` — complete product/editorial/UX/technical documentation;
- `.github/workflows/ci.yml` — CI validation/build workflow.

## Editing rule

`src/content/scenarios/` is the only place to edit scenario text. `preview/` is generated. The Mosaic layout is maintained separately in `src/data/mosaic-layout.json`.
