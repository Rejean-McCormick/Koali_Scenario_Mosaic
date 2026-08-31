# Public Scenario Selected State — v4.2

## Decision

A scenario page should not look like a separate documentation product.

The public interaction model is now:

> **The Mosaic remains the interface. A scenario page is simply the Mosaic with one scenario selected and the lower honeycomb repurposed for supplemental public information.**

This preserves visual continuity and removes the heavy redundancy of the former Markdown article view.

## What stays identical

The scenario page uses the same:

- Koali brand header;
- EN / FR language switcher;
- scenario preview proportions;
- scenario image behavior;
- title and preview summary;
- public scenario profile;
- category color;
- activity indicators;
- scale, context, and special-condition rows.

The selected page therefore does not repeat the title, summary, category, pattern, or public profile in a second article header.

## What changes

The 120-cell panoramic honeycomb is replaced by five supplemental information hexagons:

1. **Starts with / Point de départ** — the type of input or trigger that begins the scenario;
2. **What can get lost / Ce qui peut se perdre** — the continuity gap already localized in scenario frontmatter;
3. **Koali keeps connected / Koali maintient le lien** — the public explanation of what continuity Koali preserves;
4. **Flow / Déroulé** — the scenario progression;
5. **Transferable to / Transposable à** — other contexts where the same pattern can apply.

These five elements complement the preview instead of restating it.

## Public / internal separation

The localized Markdown scenario files remain rich editorial and governance sources. They may contain:

- internal component roles and scores;
- `PAT-*` identifiers;
- `SIG-*` signature references;
- `POS-*` canonical possibility references;
- derivation states such as `COMPOSED`;
- runtime-evidence states such as `UNVERIFIED`;
- explanatory notes intended for editors, reviewers, or architecture work.

These are **not rendered on the general-public scenario route**.

The information is not deleted. It remains versioned in the repository and can support future internal/editorial tooling. The change is strictly one of public presentation boundaries.

## Why

The former page repeated the same situation at multiple levels:

- preview title;
- article title;
- Situation heading;
- repeated summary;
- pattern metadata;
- usage palette;
- component roles;
- canonical anchoring;
- status notes.

That made the scenario feel like documentation rather than exploration.

The v4.2 selected-state model keeps the page focused on one question:

> **What is happening here, and what continuity does Koali add?**

## Source-of-truth rule

- shared structural metadata stays in `src/data/scenarios.json`;
- localized editorial material stays in `src/content/scenarios/en/` and `src/content/scenarios/fr/`;
- public routes selectively expose only public-language fields;
- internal material remains available in source but is not injected into public HTML.
