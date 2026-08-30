# Build and Deployment

## Local

```bash
npm install
npm run dev
npm run build
npm run preview
```

## Build

The build should fail when:

- schema is invalid;
- a slot is missing;
- an ID is duplicated;
- a required image is missing;
- a route cannot be generated.

## Hosting

Any static host works: CDN, object storage, static hosting platform, or a conventional web server.

## Cache

- HTML: normal revalidation according to the deployment strategy;
- Astro hashed assets: long cache;
- optimized images: long cache.

## CI

Minimal pipeline:

1. install;
2. lint/typecheck;
3. validate content/layout;
4. build;
5. E2E smoke tests;
6. deploy.
