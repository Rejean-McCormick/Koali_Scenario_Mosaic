# Koali Use Mosaic

## Purpose

**Koali Use Mosaic** is the public-facing spatial interface for exploring the 120 usage scenarios in this pack.

It is intentionally designed as an intuitive visual field rather than as a diagram that requires the visitor to decode a formal spatial theory. The underlying editorial structure remains real—eight usage families, 24 recurring patterns, properties, domains, component architecture, and evidence states—but the public experience is allowed to feel simply like a rich mosaic of possibilities.

The public question is not “Can I understand the taxonomy?” It is:

> **What happens if I move my pointer across this field and discover what Koali can help people do?**

## Core experience

The Mosaic page has two primary regions:

1. a persistent **scenario preview area** at the top;
2. a dense visual field of **120 scenario cells** below it.

On desktop, hovering or focusing a cell updates the preview without navigating away. The visitor can spend roughly 10–30 seconds understanding a scenario. Clicking opens the full scenario as a simple static page.

On touch devices, the first tap selects/previews the cell; the detailed page remains an explicit action.

## What appears in the preview

The preview is intentionally compact:

- scenario image;
- title;
- short editorial summary;
- category and typical motion in plain language;
- usage palette;
- seven public activity indicators;
- scale and context;
- special-condition indicators when relevant;
- a link to read the full scenario.

The full page uses the richer editorial text in [`../src/content/scenarios/`](../src/content/scenarios/).

## Spatial principle

The 120-cell composition is **curated and fixed**, not recomputed from semantic weights at runtime.

This is deliberate. The Mosaic is a public design surface, not a scientific scatterplot. Visual quality, spatial memory, stability, and art direction are more important than forcing every coordinate to explain itself.

The current layout contains:

- 120 occupied slots;
- 30 reserved peripheral slots;
- 150 total predefined positions.

New scenarios can therefore be added later without shifting the existing 120. A new full layout version is created only when editorial/art-direction needs justify recomposition.

See [`src/data/mosaic-layout.json`](../src/data/mosaic-layout.json).

## Terminology rule

**Mosaic** is the canonical name for this subsystem.

Do not reintroduce the previous term in UI copy, filenames, route names, code identifiers, or documentation.

## Route model

Recommended public routing:

- `/uses/` — Koali Use Mosaic;
- `/uses/SCN-001/` … `/uses/SCN-120/` — full static scenario pages;
- `/uses/list/` — accessible/searchable text alternative.

## Source of truth

The canonical scenario files are under [`../src/content/scenarios/`](../src/content/scenarios/). Mosaic placement is separate in [`../src/data/mosaic-layout.json`](../src/data/mosaic-layout.json). Astro reads the canonical files directly; there is no duplicate implementation snapshot.

The dependency-free local preview in [`../preview/`](../preview/) is generated output.

## Detailed subsystem documentation

The complete UX, accessibility, technical, operations, and architecture documentation is under [`docs/mosaic/`](mosaic/README.md).
