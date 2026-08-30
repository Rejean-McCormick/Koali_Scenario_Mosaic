# Content Schema

## Mosaic fields

The detailed corpus may retain many metadata fields. The Mosaic page only requires a stable subset.

### Required for preview

```yaml
id: SCN-001
title: "..."
preview_summary: "..."
preview_image: "./preview.webp"
preview_image_alt: "..."
palette: [understand, collaborate, act]
components:
  kristal: 5
  konnaxion: 3
  orgo: 4
  uckk: 0
badges: [maintenance]
```

### Required for detailed page

The Markdown body contains the full scenario.

### Optional

```yaml
related: [SCN-004, SCN-092]
hero: false
status: COMPOSED
runtime_evidence: UNVERIFIED
```

## Do not put layout coordinates inside scenarios

A scenario should not carry `x` and `y`. Layout lives in `mosaic-layout.json`.

## Validation

The schema should:

- enforce `SCN-###` IDs;
- constrain intensities to 0–5;
- constrain visible badges;
- require image alt text;
- enforce a reasonable preview length;
- reject scenarios with no title.

## Images

In production, keeping images alongside Markdown and using Astro's `image()` helper enables validation/import and optimization through the asset components.
