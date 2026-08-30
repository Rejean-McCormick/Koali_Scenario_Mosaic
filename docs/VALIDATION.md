# Repository validation

Validated for the GitHub-ready repository edition.

## Content and layout

- 120 canonical scenario Markdown files in `src/content/scenarios/`;
- unique `SCN-001` … `SCN-120` IDs;
- 150 fixed Mosaic slots;
- 120 occupied assignments;
- 30 reserved peripheral slots;
- no duplicate slot assignments.

## Zero-install preview

- `START.html` targets `preview/index.html`;
- preview index contains 120 scenario cells;
- 120 full scenario preview pages are generated;
- SCN-001 preview page includes the developed editorial sections, not only the hover summary;
- all generated HTML `href`/`src` local references were checked for file existence.

## Documentation

- 2,383 relative Markdown links checked;
- 0 broken relative Markdown links.

## npm validation

`npm run validate` passes without requiring Astro dependencies to be installed because the validation scripts use Node/Python standard tooling only.

## Production build note

The repository is configured for `npm install && npm run build`. In this execution environment, npm dependency download previously timed out, so the full Astro dependency build was not used as the proof for the zero-install launcher. The bundled `preview/` is generated directly from the same canonical 120 Markdown files and fixed Mosaic layout.
