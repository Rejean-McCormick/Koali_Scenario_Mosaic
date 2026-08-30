# Astro Architecture

## Why Astro

The project is primarily static content with lightweight interaction. Astro can load content collections, validate them with schemas, generate static routes, and add client-side TypeScript without requiring React/Vue/Svelte.

## Recommended structure

```text
src/
  content.config.ts
  content/
    scenarios/
      SCN-001/
        index.md
        preview.webp
      ...
  components/
    UsageMosaic.astro
    ScenarioPreview.astro
    ScenarioCell.astro
  data/
    mosaic-layout.json
  pages/
    uses/
      index.astro
      [id].astro
  scripts/
    mosaic.ts
  styles/
    mosaic.css
```

## Content Collection

Use a build-time collection with `glob()` and a Zod schema. This fits 120 relatively static files and provides validation plus TypeScript typing.

## Routes

`getStaticPaths()` generates all 120 scenario pages during the build.

## Scripts

An Astro `<script>` can contain TypeScript processed/bundled by Astro. No React island is required for the MVP.

## Version

Do not write the documentation against one exact minor release. At project start, pin a validated stable Astro version in `package.json`, then upgrade deliberately.
