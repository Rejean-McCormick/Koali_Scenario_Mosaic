# Build and validation status — repository edition

## Repository/data validation

Validated state:

- 120 canonical scenario files under `src/content/scenarios/`;
- scenario IDs unique;
- 150 fixed Mosaic slots;
- 120 scenario assignments;
- no duplicate slot assignments;
- 30 reserved slots;
- 120 generated offline preview scenario pages;
- repository-relative documentation links checked.

## Editorial integration

Astro reads the rich English scenario bodies directly from `src/content/scenarios/`. There is no synchronized implementation snapshot.

## Astro build

The repository is structured for:

```bash
npm install
npm run build
```

The zero-install preview does not require npm and is opened with `START.html`.
