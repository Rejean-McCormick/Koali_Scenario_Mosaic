# Mosaic content integration

## One canonical scenario file

This repository has one editorial and executable source for each scenario: `src/content/scenarios/SCN-001.md` through `SCN-120.md`. Astro reads those files directly. There is no synchronized duplicate corpus.

## Two reading depths

**Preview mode** reads frontmatter (`title`, `preview_summary`, `preview_image`, `category_label`, `pattern_label`, `palette`, `components`, `badges`, `related`) and targets roughly 10–30 seconds of attention.

**Full scenario mode** renders the body of the same Markdown file at `/uses/{scenario-id}/`.

## Layout separation

Scenario prose does not own coordinates. Placement lives in [`../src/data/mosaic-layout.json`](../src/data/mosaic-layout.json), keeping content editable while the public composition remains stable.

## Generated preview

[`../preview/`](../preview/) is generated for zero-install double-click viewing. Never edit it as a source.

## Claim discipline

Visual polish never upgrades evidence. `derivation` and `runtime_evidence` remain authoritative.
