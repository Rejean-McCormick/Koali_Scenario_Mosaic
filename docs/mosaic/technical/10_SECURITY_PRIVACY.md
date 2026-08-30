# Security and Privacy

## Static MVP

No forms, accounts, database, or backend are required. This significantly reduces the attack surface.

## Content

Treat Markdown as trusted repository-maintained content. If a CMS is added later, reassess sanitization and permissions.

## Remote images

Prefer local assets. If remote images are used, explicitly restrict allowed domains in Astro configuration.

## Analytics

If analytics are used: minimize collection, avoid fingerprinting, define a clear policy.

## No client secrets

No API key or secret may be embedded in the public bundle.
