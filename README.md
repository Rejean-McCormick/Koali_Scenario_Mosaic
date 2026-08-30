# Koali Scenario Mosaic — v3.6

Double-click `START.html` to open the zero-install Mosaic preview.

## Current UI fixes

- one highlighted hexagon at a time;
- exact regular 12 × 10 honeycomb grid;
- stable fixed-height scenario preview;
- complete two-line title box with no vertical clipping;
- public-language scenario profile;
- **automatic PNG scenario images with SVG fallback**.

## Scenario PNG convention

Put a scenario image in:

```text
public/scenarios/images/scenario_001.png
public/scenarios/images/scenario_002.png
...
public/scenarios/images/scenario_120.png
```

The numeric suffix maps directly to `SCN-001` … `SCN-120`.

No scenario Markdown edit is required. Astro resolves the PNG automatically when it exists; if it does not exist, the existing SVG placeholder remains in use.

For the zero-install `START.html` preview, regenerate after adding images:

```bash
npm run preview:offline
```

A normal production build does this automatically before validation:

```bash
npm run build
```

## Current image coverage

This v3.6 package includes **31 real PNG scenario images** from the supplied image bundle. The remaining 89 scenarios continue to use SVG placeholders until their corresponding PNG is added.

Validate the image mapping with:

```bash
npm run validate:images
```


## Product name

The public product name is **Koali Scenario Mosaic**. Use the singular **Scenario** in the compound name. Generic technical filenames such as `mosaic.ts`, `mosaic.css`, and `mosaic-layout.json` remain unchanged because they describe the interface mechanism rather than the product name.
