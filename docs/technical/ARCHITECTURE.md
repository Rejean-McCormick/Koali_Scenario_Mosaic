# Implementation architecture

```text
120 Markdown files
      ↓ build-time validation
Astro content collection
      ├── /uses/ interactive page
      └── /uses/{SCN-ID}/ 120 static pages

mosaic-layout.json
      ↓
fixed SVG coordinates
      ↓
inline DOM cells
      ↓ pointer / focus / tap
preview panel
```

The defining rule is **dynamic/extensible content, stable human-composed geography**. Layout coordinates are data, not computed semantics.
