# Code review notes — repository edition

## Resolved

- Product terminology is consistently **Koali Use Mosaic**.
- The 120 rich English scenario bodies are the Astro content collection itself.
- There is one scenario source, not a canonical/snapshot pair.
- Scenario content and Mosaic coordinates remain separate.
- The layout has 120 occupied and 30 reserved slots.
- Public routes are `/uses/`, `/uses/SCN-XXX/`, and `/uses/list/`.
- A dependency-free `preview/` is generated from the same source for double-click viewing.

## Production follow-ups

1. Replace placeholder SVGs with final scenario artwork when art direction is ready.
2. Run `npm install && npm run build` in the target deployment environment.
3. Add automated browser accessibility/regression tests for production.
4. Keep released layout versions immutable; create a new layout version for substantial recomposition.
5. Run `npm run preview:offline` after visible content or UI changes.
