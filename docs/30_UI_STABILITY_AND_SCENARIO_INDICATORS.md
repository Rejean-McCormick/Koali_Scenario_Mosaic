# UI Stability and Scenario Indicators — v3.1

> **Superseded in v3.2 for the public UI.** The fixed-height solution remains valid, but the component gauges described below were replaced by the public-language profile defined in [`31_PUBLIC_SCENARIO_PROFILE.md`](31_PUBLIC_SCENARIO_PROFILE.md). This file is retained as change history.

This revision addresses two interaction defects in the Mosaic preview.

## 1. Preview height is now stable

The scenario preview reserves an explicit block height at every responsive breakpoint:

- desktop: `330px`;
- tablet: `392px`;
- mobile: `622px`.

Variable fields are constrained inside those reserved regions. Titles display at most two lines and hover summaries at most three. Palette, pattern and trait regions are also bounded.

**Invariant:** changing the hovered/focused scenario must never move the Mosaic vertically.

## 2. Scenario character indicators

Every hover/focus now updates a dedicated **Scenario character** instrument panel with:

- category hue and stable `CAT-##` ID;
- stable `PAT-##` ID and pattern label;
- segmented 0–5 gauges for Kristal, Konnaxion, Orgo and UCKK;
- up to four context/property indicators;
- usage-palette tags in the summary column.

The component gauges use the category hue, so both color family and component mix change with the selected scenario.

## 3. Offline preview metadata parser

The zero-install preview builder was also corrected so YAML-style block arrays and inline empty arrays are preserved as arrays. This applies to fields such as:

- `palette`;
- `properties`;
- `settings`;
- `scales`;
- `related`.

The offline preview therefore consumes the same semantic shape expected by the Astro implementation.

## 4. Automated contract validation

`npm run validate` now includes `validate:ui`, which verifies:

- fixed preview heights exist at all three responsive breakpoints;
- title/summary clamping exists;
- all Scenario character DOM hooks are present in Astro and offline builds;
- all 120 hover payloads are present;
- all 8 categories and all 24 patterns are represented;
- component profiles vary across scenarios;
- array metadata remains array-valued in the offline preview.
