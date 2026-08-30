# System Architecture

## Overview

```text
120 Markdown files
        │
        ▼
Astro Content Collection
(schema validation)
        │
        ├──────────────► static pages /uses/{id}/
        │
        ▼
/uses/ page
        │
        ├── HTML discovery panel
        ├── inline SVG mosaic
        └── lightweight TypeScript

mosaic-layout.json
        │
        └──────────────► scenario → slot / coordinates assignment
```

## Three data sources

### 1. Content
Markdown files describe each scenario.

### 2. Layout
An independent file describes where every scenario appears.

### 3. Design tokens
CSS defines typography, spacing, sizing, states, colors, and transitions.

This separation is fundamental: changing copy must not change geography; changing geography must not change the scenario content.

## Static-first

The entire site is built in advance. The browser receives HTML, SVG, and a small JavaScript bundle.

Benefits:

- speed;
- simple hosting;
- resilience;
- SEO;
- shareable URLs;
- low cost;
- small attack surface;
- easy archiving.

## Minimal dependencies

The MVP can run with Astro and its native dependencies. D3 is not required because the layout is fixed. It may be used offline as a design aid during the initial composition, but any resulting coordinates must be exported and frozen.
