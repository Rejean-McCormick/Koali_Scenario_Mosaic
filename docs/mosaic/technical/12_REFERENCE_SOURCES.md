# Verified Technical References — August 2026

Official Astro documentation used for this specification:

- Content Collections — https://docs.astro.build/en/guides/content-collections/
- Content API — https://docs.astro.build/en/reference/modules/astro-content/
- Routing / getStaticPaths — https://docs.astro.build/en/guides/routing/
- Client-side scripts — https://docs.astro.build/en/guides/client-side-scripts/
- Images — https://docs.astro.build/en/guides/images/

Verified points:

- build-time collections use a `loader` and can use a Zod schema;
- `glob()` can load local Markdown files;
- `getStaticPaths()` can generate static routes;
- Astro scripts can contain TypeScript and are bundled without a UI framework;
- the collection `image()` helper can validate/import local images;
- Astro image components can optimize local assets.

At implementation time, re-read the documentation for the installed stable version before copying code from this documentation verbatim.
