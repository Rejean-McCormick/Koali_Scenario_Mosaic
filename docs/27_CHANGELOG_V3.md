# Changelog — v3 English

## Major change: Koali Use Mosaic integrated

v3 consolidates the usage-presentation corpus and the public spatial discovery interface into one maintained repository.

### Terminology

- The previous spatial-interface term has been removed from the active corpus.
- **Koali Use Mosaic** is now the canonical subsystem name.

### Canonical scenario corpus

- The 120 rich English scenario cards from v2 remain the editorial source of truth.
- Each scenario now also includes preview metadata needed by the Mosaic: short summary, image reference, accessibility alt text, badges, related scenarios, category label, and pattern label.
- Claim/evidence fields remain unchanged.

### Mosaic system

Added:

- complete Mosaic product/UX/technical documentation;
- fixed `mosaic-layout-v1` data;
- 120 scenario-to-slot assignments;
- 30 reserved peripheral slots;
- layout preview asset;
- source-of-truth and synchronization rules.

### Reference implementation

The Astro reference implementation is now promoted to the **repository root**, following standard GitHub project structure.

The implementation uses the rich canonical scenario bodies instead of the earlier short placeholder body copy.

### Maintenance tooling

The previous synchronization layer has been removed: `src/content/scenarios/` is now the single canonical and executable scenario source. A generated `preview/` provides zero-install viewing without becoming a second source of truth.

### Site architecture

The primary public discovery route is `/uses/` and individual scenarios are static pages under `/uses/SCN-XXX/`.

### No change to capability/evidence discipline

The Mosaic is a presentation and navigation layer. It does not convert `COMPOSED` or `DERIVED` scenarios into validated runtime claims.
