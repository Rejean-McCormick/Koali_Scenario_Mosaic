# Koali Scenario Mosaic — v4.3.4 Two-tone Brand Checker + Magnetic Territories

**Koali, the Sociotechnical Operating System**

Koali Scenario Mosaic is a public-facing panorama of **120 stable scenario identities**, now available in **English and French** without duplicating the Mosaic geometry or machine-facing scenario metadata.


## v4.3.4 — two-tone Koali brand checker

The eight category hues have been replaced by a **two-tone checker derived from Koali green**. The top territories alternate A/B/A/B and the lower row alternates B/A/B/A, so neighboring territories remain distinct without the former rainbow palette. Magnetic territory labels are also brighter at rest and on hover for stronger contrast. See [`docs/47_TWO_TONE_BRAND_CHECKER.md`](docs/47_TWO_TONE_BRAND_CHECKER.md).

## v4.3.2 — refreshed scenarios integrated into the magnetic interface

The **v4.3.1 scenario corpus is the new editorial source of truth** in this repository. All 120 English and all 120 French scenario documents, plus their shared public metadata and French tag vocabulary, are carried over exactly from the supplied v4.3.1 refresh.

The magnetic Mosaic remains the interaction shell:

- the same 20 × 6 geometry and 8 category territories;
- the same embedded magnetic territory labels;
- the same public selected-scenario layout;
- the same EN/FR route continuity;
- refreshed titles, summaries, contexts, domains, flows, and transferable domains everywhere the interface reads scenario data.

Because the refreshed corpus contains longer, more narrative titles, the preview now uses an **adaptive three-line title box** with short / medium / long density states. Hovering a new scenario updates this density without changing the Mosaic geometry.

See [`docs/45_SCENARIO_EDITORIAL_REFRESH.md`](docs/45_SCENARIO_EDITORIAL_REFRESH.md) and [`docs/46_REFRESHED_SCENARIOS_MAGNETIC_INTEGRATION.md`](docs/46_REFRESHED_SCENARIOS_MAGNETIC_INTEGRATION.md).

## Open immediately

Double-click `START.html`.

The zero-install preview detects the browser language:

- French browser → French Mosaic;
- otherwise → English Mosaic.

The **EN / FR** switch is always visible and keeps the current scenario when changing language.

## Public routes

```text
/                  → browser-language choice
/en/uses/          → English Mosaic
/fr/uses/          → Mosaïque française
/en/uses/SCN-061/  → English scenario
/fr/uses/SCN-061/  → French scenario
```

Legacy `/uses/` links continue to redirect to English for compatibility.

## One scenario identity, two editorial languages

The v4 architecture separates stable scenario structure from translated editorial text:

```text
src/data/scenarios.json
    120 shared scenario identities
    IDs, categories, patterns, palette keys, scales,
    settings, properties, domains, component data,
    evidence status, image identity, layout continuity

src/content/scenarios/en/
    120 English editorial scenario documents

src/content/scenarios/fr/
    120 French editorial scenario documents

src/data/mosaic-layout.json
    one shared 20 × 6 geography for both languages
```

`SCN-061` therefore occupies the **same hexagon, color family, image, pattern family, and semantic profile** in both languages. Only the human-readable editorial layer changes.

## French coverage

The French edition includes:

- all **120 titles**;
- all **120 preview summaries**;
- all **24 recurring pattern names and descriptions**;
- all **8 public category names**;
- localized scale, context, domain, property, and palette labels;
- complete French editorial scenario sources;
- French search, legend, controls, profile labels, accessibility text, and cover;
- French offline pages under `preview/fr/`.

Translations are versioned source content. There is **no runtime machine translation**.

## Interaction design retained

- 20 × 6 panoramic honeycomb;
- 8 contiguous category territories;
- eight territory names embedded directly over their color regions;
- one highlighted hexagon at a time;
- stable fixed-height preview;
- adaptive three-line title box for the refreshed, longer scenario hooks;
- public-language scenario profile;
- automatic PNG scenario image loading with SVG fallback;
- two-tone Koali brand checker (`#1e6864` / `#4a9690`) and supplied SVG logo.


## Responsive preview behavior

The v4.1 preview explicitly separates the **initial cover** from **scenario images**:

- the initial cover is a text-free abstract territory graphic and uses `object-fit: contain`;
- scenario PNG/SVG images switch to `object-fit: cover` after hover/focus;
- at tablet widths the preview uses a bounded two-column top row and a full-width profile strip;
- below 720 px the preview becomes a single-column stack;
- the legend no longer forces a 760 px page width;
- only the Mosaic itself becomes horizontally scrollable on narrow screens.

This prevents the preview panel from spilling outside the viewport and prevents the cover branding from being cropped.


## Scenario pages: selected Mosaic state

A public scenario page is no longer a separate article layout. It reuses the **same Koali header and the same scenario-preview panel** as the main Mosaic. The only major visual change is the lower honeycomb.

On the main page, that honeycomb contains the 120 scenarios. On a selected scenario page, it becomes five public information hexagons:

- **Starts with / Point de départ**;
- **What can get lost / Ce qui peut se perdre**;
- **Koali keeps connected / Koali maintient le lien**;
- **Flow / Déroulé**;
- **Transferable to / Transposable à**.

The public route intentionally does **not render the full editorial Markdown**. Internal architecture and claim-governance material such as component scores, `PAT-*`, `SIG-*`, `POS-*`, derivation states, and runtime-evidence states remain in the repository source for editorial/governance use, but are not part of the general-public reading experience.

This makes a scenario feel like a **selected state of the Mosaic**, not a jump into a different documentation system.

## Magnetic territory labels — retained in v4.3.2

The detached visual color legend has been replaced by **eight localized territory names embedded directly over the honeycomb**. On desktop/fine-pointer devices, individual letters are repelled by pointer proximity and return with a short spring/bounce.

The governing invariant remains:

> **The map stays still. Meaning becomes alive.**

Implementation details:

- production: pinned **GSAP 3.13.0 + SplitText** with a custom proximity/spring controller;
- exactly eight versioned normalized anchors in `mosaic-layout.json`;
- letters only move by `transform`; hexagon geometry never changes;
- active scenario hover/focus raises only the matching territory-label opacity;
- touch/coarse-pointer and `prefers-reduced-motion` receive complete static labels;
- the former category legend remains as a screen-reader-only semantic list;
- offline `START.html` preview mirrors the effect with a dependency-free `requestAnimationFrame` implementation so it also works under `file://`.

See [`docs/43_MAGNETIC_TERRITORY_LABELS_TECHNICAL_SPEC.md`](docs/43_MAGNETIC_TERRITORY_LABELS_TECHNICAL_SPEC.md) and [`docs/44_MAGNETIC_TERRITORY_LABELS_IMPLEMENTATION.md`](docs/44_MAGNETIC_TERRITORY_LABELS_IMPLEMENTATION.md).

## Develop locally

Use Node **24.20.0** when possible. Astro requires Node `>=22.12.0`.

```bash
npm install
npm run build
npx astro preview
```

Then open the local URL printed by Astro, normally `http://localhost:4321`.

The production build intentionally does **not** run the Python offline-preview generator.

## Regenerate the zero-install bilingual preview

The offline generator uses Python and PyYAML:

```bash
python -m pip install PyYAML
npm run preview:offline
```

It produces:

```text
preview/index.html          language chooser
preview/en/index.html       English Mosaic
preview/fr/index.html       French Mosaic
preview/en/uses/...         120 English detail pages
preview/fr/uses/...         120 French detail pages
```

## Validation

```bash
npm run validate
```

The validation contract checks:

- 120 shared scenario identities;
- 120 EN + 120 FR editorial documents;
- matching EN/FR scenario IDs;
- no duplicated shared metadata inside localized files;
- no title repetition in preview summaries;
- complete French public metadata vocabulary;
- bilingual routes and language switch;
- both offline previews;
- 20 × 6 Mosaic geometry and category territories;
- PNG/SVG image resolution;
- canonical Koali branding;
- eight territory anchors and localized map labels;
- GSAP/SplitText magnetic-label lifecycle, reduced-motion, fine-pointer, and observer contracts.

## Netlify

The included `netlify.toml` uses:

```text
Build command: npm run build
Publish directory: dist
Node: 24.20.0
```

A push to the connected GitHub repository can redeploy directly on Netlify.

## Scenario images

PNG convention remains unchanged:

```text
public/scenarios/images/scenario_001.png
...
public/scenarios/images/scenario_120.png
```

Both languages share the same scenario image. Missing PNGs automatically use the scenario SVG placeholder.

## Canonical naming

- brand: **Koali**;
- positioning: **Koali, the Sociotechnical Operating System**;
- English interface: **Koali Scenario Mosaic**;
- French interface: **Mosaïque de scénarios Koali**;
- npm package: `koali-scenario-mosaic`.

See [`docs/40_BILINGUAL_ARCHITECTURE.md`](docs/40_BILINGUAL_ARCHITECTURE.md) for the v4 language architecture, [`docs/41_RESPONSIVE_PREVIEW_AND_COVER.md`](docs/41_RESPONSIVE_PREVIEW_AND_COVER.md) for the responsive-preview contract, [`docs/42_PUBLIC_SCENARIO_SELECTED_STATE.md`](docs/42_PUBLIC_SCENARIO_SELECTED_STATE.md) for the public scenario-page model, and [`docs/44_MAGNETIC_TERRITORY_LABELS_IMPLEMENTATION.md`](docs/44_MAGNETIC_TERRITORY_LABELS_IMPLEMENTATION.md) for v4.3.2.

## v4.3.5 — softer magnetic motion

Territory labels keep their pointer-repulsion behavior, but the spring is now strongly damped to avoid repeated bounce / visual flicker. The field is broader, displacement is shorter, pointer input is smoothed, and character velocity is capped. See `docs/48_SOFT_MAGNETIC_MOTION.md`.
