# Koali Scenario Mosaic — v3.7

Koali Scenario Mosaic is a public-facing panorama of 120 Koali use scenarios.

## Open locally without installing anything

Double-click `START.html` to open the bundled zero-install preview.

## Current interaction design

- **20 × 6 panoramic honeycomb** so the scenario spread stays visible beneath the preview;
- 120 active scenarios arranged into **8 contiguous category territories**;
- each territory is a regular **5 × 3** block in the shared honeycomb grid;
- compact **color legend** mirrors the 4 × 2 territory organization;
- one highlighted hexagon at a time;
- stable fixed-height scenario preview;
- complete two-line title box with no vertical clipping;
- public-language scenario profile;
- automatic PNG scenario images with SVG fallback.

The desktop layout is intentionally designed so that a normal laptop viewport can show the preview, controls, legend, and Mosaic together rather than forcing the user to scroll away from the preview before hovering cells.

## Develop locally

Use Node 24.20.0 when possible. The repository also accepts Node >=22.12.0.

```bash
npm install
npm run build
npx astro preview
```

Then open the local URL printed by Astro, normally `http://localhost:4321`.

The production build **does not run the Python offline-preview generator**. This keeps Netlify builds independent of PyYAML.

To regenerate the double-click `START.html` preview after visible UI/content/image changes:

```bash
npm run preview:offline
```

## Netlify

The repo includes `netlify.toml`:

```text
Build command: npm run build
Publish directory: dist
Node: 24.20.0
```

A push to the connected GitHub repository can therefore redeploy directly on Netlify.

## Scenario PNG convention

Put scenario images in:

```text
public/scenarios/images/scenario_001.png
public/scenarios/images/scenario_002.png
...
public/scenarios/images/scenario_120.png
```

The numeric suffix maps directly to `SCN-001` … `SCN-120`. No scenario Markdown edit is required. If a PNG is missing, the SVG placeholder is used automatically.

This package currently includes **31 PNG scenario images**; 89 scenarios use SVG fallback.

Validate image mapping with:

```bash
npm run validate:images
```

## Product name

The public product name is **Koali Scenario Mosaic**. Generic technical filenames such as `mosaic.ts`, `mosaic.css`, and `mosaic-layout.json` remain unchanged because they describe the interface mechanism rather than the product name.
