# v4.3.2 — Refreshed scenarios + magnetic interface integration

## Purpose

Integrate the complete scenario rewrite supplied in **v4.3.1** into the magnetic Koali Scenario Mosaic without regressing the interaction model introduced in v4.3.

## Source-of-truth rule

For scenario content, v4.3.1 is authoritative. The following files are copied exactly from that corpus:

- `src/content/scenarios/en/SCN-001.md` … `SCN-120.md`;
- `src/content/scenarios/fr/SCN-001.md` … `SCN-120.md`;
- `src/data/scenarios.json`;
- `src/i18n/fr-tags.json`.

This means titles, preview summaries, domains, transfer domains, loops, scales, settings, properties, and other shared scenario metadata now describe the refreshed situations rather than the superseded stories.

## Magnetic interface retained

The integration intentionally keeps the v4.3 magnetic presentation layer:

- `MosaicTerritoryLabels.astro`;
- `territory-repulsion.ts`;
- GSAP 3.13.0 + SplitText;
- 8 normalized `territoryLabels` anchors in `mosaic-layout.json`;
- screen-reader-only semantic category legend;
- one active hexagon at a time;
- static fallback for coarse pointer and reduced motion;
- dependency-free magnetic behavior in the offline preview.

The 20 × 6 assignments are unchanged, so every refreshed `SCN-*` identity remains in its established map cell and category territory.

## Long-title adaptation

The new editorial hooks are intentionally more specific and often longer. The preview therefore uses three density states:

- `short`: up to 72 characters;
- `medium`: 73–96 characters;
- `long`: over 96 characters.

The title area is a fixed three-line box. `mosaic.ts` updates `data-title-density` whenever hover/focus selects a different scenario, preventing long refreshed titles from being clipped while preserving preview height stability.

The same rule is implemented in the zero-install offline preview.

## Public scenario pages

Scenario routes continue to use the selected-Mosaic-state model. The public page does not render the internal Markdown body. It reuses the shared preview and displays only the five public supplemental information cells.

Internal tokens such as `PAT-*`, `SIG-*`, `POS-*`, component scores, derivation states, and runtime-evidence states remain in repository source for governance but are not emitted into the public scenario-page body.

## Compatibility

Preserved:

- `SCN-001` … `SCN-120` URLs;
- EN/FR identity parity;
- 8 categories;
- 24 pattern families;
- Mosaic geometry;
- Netlify production build contract;
- scenario PNG naming convention and SVG fallback.

## Image note

The supplied v4.3.1 archive contains the same 31 PNG assets as the previous magnetic repository. They are therefore preserved as supplied; 89 scenarios continue to use SVG fallback. Any future image editorial refresh can replace `scenario_###.png` without changing scenario content or Mosaic code.

## Validation

`npm run validate` checks both contracts simultaneously:

1. refreshed bilingual scenario content / metadata;
2. magnetic territory-label implementation and geometry.

The offline preview is regenerated from the refreshed source before validation.
