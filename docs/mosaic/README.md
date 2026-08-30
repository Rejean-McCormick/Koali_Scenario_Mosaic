# Koali Use Mosaic — Complete Documentation v1 (English)

Product, UX, visual, and technical specification for the public page used to explore the **120 Koali usage scenarios** as an interactive spatial mosaic.

## Master decision

> **Extensible content, composed and stable geography.**

The page is not a scientific visualization that recalculates positions. It is an **editorially composed spatial display**: scenarios occupy fixed slots, visitors explore them intuitively, hover reveals a 10–30 second summary, and click opens a detailed static page.

## Recommended stack

- **Astro** — static site generation;
- **Markdown** — scenario source content;
- **native TypeScript** — lightweight interactions;
- **CSS** — visual design;
- **inline SVG** — interactive mosaic;
- **no backend required** for the MVP;
- **no React/Vue/Svelte framework required** for the MVP.

## Read in this order

1. `00_START_HERE.md`
2. `architecture/01_PRODUCT_DEFINITION.md`
3. `architecture/02_SYSTEM_ARCHITECTURE.md`
4. `ux/01_MOSAIC_PAGE_UX.md`
5. `ux/02_VISUAL_LAYOUT_SYSTEM.md`
6. `technical/01_ASTRO_ARCHITECTURE.md`
7. `technical/02_CONTENT_SCHEMA.md`
8. `technical/03_SVG_MOSAIC.md`
9. `operations/01_ADDING_A_SCENARIO.md`
10. `operations/04_ACCEPTANCE_CRITERIA.md`

The `examples/` directory contains a deliberately minimal **reference skeleton** showing how the documentation can map to code.
