# Magnetic Territory Labels — v4.3 Implementation

**Status:** implemented  
**Scope:** `/en/uses/` and `/fr/uses/` main 120-scenario Mosaic only

## What changed

The detached visible category legend has been replaced by eight localized category names positioned directly over their fixed 5 × 3 color territories.

On a fine-pointer device, the territory typography is progressively enhanced with a local magnetic field:

- each rendered character becomes independently transformable;
- characters within a 96 px radius are repelled away from the pointer;
- maximum displacement is 15 px;
- displacement falls off smoothly with distance (`exponent = 1.85`);
- when the field leaves, characters return through a damped spring (`spring = 0.15`, `damping = 0.77`);
- the animation ticker sleeps after the text settles.

The hexagons never move.

## Production architecture

```text
ScenarioMosaic.astro
├── fixed SVG honeycomb
├── MosaicTerritoryLabels.astro
│   └── static localized HTML labels
├── mosaic.ts
│   └── scenario preview + active territory state
└── territory-repulsion.ts
    └── GSAP 3.13.0 + SplitText + custom spring field
```

`mosaic-layout.json` now owns eight normalized territory-label anchors. They are versioned with the fixed geography rather than inferred from DOM layout at runtime.

## Localization

`src/i18n/ui.ts` contains editorially controlled `territoryMapLabels` for EN and FR. These short map labels are separate from the full public category names.

Examples:

```text
EN  CAT-01  Find & / Understand
FR  CAT-01  Trouver & / comprendre

EN  CAT-08  Disseminate & / Connect
FR  CAT-08  Diffuser & / connecter
```

## Interaction contract

Scenario hover/focus remains authoritative:

```text
hover/focus scenario
    → exactly one scenario cell active
    → preview updates
    → matching territory label opacity rises

pointer proximity to label
    → letters move
    → cells do not move
```

The two client behaviors are loaded from separate module scripts so failure of the decorative magnetic enhancement does not intentionally couple its logic to scenario-selection behavior.

## Accessibility and fallback

- label overlay is `aria-hidden="true"` and `pointer-events: none`;
- the original category list remains present as an `.sr-only` semantic legend;
- coarse-pointer/touch devices receive static labels;
- `prefers-reduced-motion: reduce` receives static labels;
- keyboard focus raises the relevant territory label opacity but does not create a pointer field;
- JavaScript-independent text exists before enhancement.

## Performance

The production controller:

- waits for fonts before final geometry measurement;
- stores character centers in Mosaic-local coordinates;
- performs no layout reads in the animation loop;
- uses transform-only writes;
- uses `ResizeObserver` for geometry rebuilds;
- uses `IntersectionObserver` to stop work off-screen;
- removes the GSAP ticker when all characters have settled;
- clamps frame-factor integration to reduce refresh-rate/throttling differences.

## Offline preview

`START.html` must continue to work without an npm server and under `file://`. The generated offline preview therefore mirrors the same physics constants with a small dependency-free `requestAnimationFrame` controller rather than attempting to load the npm GSAP bundle.

This is an implementation detail of the preview artifact; production Astro uses the pinned GSAP/SplitText path.

## Validation

`npm run validate:territory-labels` verifies:

- exactly 8 normalized anchors;
- `CAT-01` through `CAT-08` coverage;
- EN and FR map labels;
- overlay/accessibility hooks;
- GSAP/SplitText integration;
- fine-pointer and reduced-motion gates;
- observer and sleep/wake lifecycle;
- exact GSAP version pin.

The broader repository validation also verifies eight labels in both generated offline Mosaic pages and confirms the detached legend is screen-reader-only.

## Design invariant

> **The map stays still. Meaning becomes alive.**
