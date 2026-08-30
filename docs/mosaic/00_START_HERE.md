# START HERE

## 1. What we are building

A primary public page presents the 120 Koali use cases as a **mosaic of interactive cells**. Visitors should not have to learn a taxonomy before they can explore. They can simply move the pointer across the mosaic, watch short summaries appear, and click when a scenario catches their interest.

The target experience is closer to an **interactive exhibition wall** or a **visual mosaic** than to an analytics dashboard.

## 2. Primary interaction

### Idle
The top of the page introduces Koali and invites exploration.

### Desktop hover / keyboard focus
A cell becomes active. The discovery panel shows:

- image;
- title;
- short summary;
- usage palette;
- seven public activity indicators;
- scale and context;
- special conditions when relevant;
- invitation to open the full scenario.

Target reading time: **10–30 seconds**.

### Click
Navigate to a static page dedicated to the scenario.

### Mobile
A tap selects a cell and displays its summary; an explicit button opens the full scenario page.

## 3. Locked decisions

- 120 initial scenarios;
- **fixed, versioned layout**;
- positions are not automatically recomputed;
- free-form overall composition;
- cells may be hexagonal as a subtle Koali motif, without forcing the whole mosaic into one large hexagon;
- spatial organization is primarily editorial and intuitive;
- proximity logic does not need to be explained to the general public;
- Markdown is the editorial source of truth;
- scenario pages are statically generated;
- SVG DOM elements for the mosaic;
- no Canvas/WebGL for the MVP;
- no database for the MVP;
- no CMS for the MVP;
- invisible/reserved slots may be kept for future scenarios.

## 4. Design principle

> **We do not generate the map. We compose it. The system makes that composition extensible.**

## 5. Conceptual basis

The 120-scenario corpus is based on the idea that Koali preserves the passages between knowledge, people, decisions, organization, action, and memory. The Mosaic is the public-facing surface that makes this breadth discoverable without requiring visitors to understand the architecture first.
