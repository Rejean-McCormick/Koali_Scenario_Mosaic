# Scenario card model v2 — English edition

## Why this schema

The scenario model separates human intent, scale, environment, technical properties, domain, and evidence status. It also adds two layers of traceability:

- `pattern_family` — reusable editorial abstraction;
- `canon_refs` / `signature_patterns` — links to the Koali capability canon.

## Frontmatter

```yaml
id: SCN-001
title:
primary_category: CAT-01
pattern_family: PAT-01
palette: []
components:
  kristal: 0..5
  konnaxion: 0..5
  orgo: 0..5
  uckk: 0..5
secondary_components: []
entry_trigger:
scales: []
settings: []
properties: []
domains: []
signature_patterns: []
canon_refs: []
transfer_domains: []
derivation: EXPLICIT | COMPOSED | DERIVED | FUTURE-DESIGN
runtime_evidence: DOCUMENTED | VALIDATED | PARTIALLY-VALIDATED | UNVERIFIED
pattern:
continuity_gap:
```

## Facets

**scales** — individual, team, organization, inter-organizational, community, public-institution.

**settings** — enterprise, research, education, culture, field, crisis, public-service, community.

**properties** — offline, multilingual, local-first, sensitive-data, ai-optional, public-facing, high-consequence, intermittent-connectivity, role-routing.

**domains** — professions and sectors; useful as secondary indexes, never as the primary information architecture.

## Quality rule

A scenario belongs in the Mosaic when a reader can recognize the problem without knowing Koali; the use crosses at least two meaningful steps; Koali’s role is continuity rather than a generic isolated feature; the pattern transfers to other domains; authority boundaries remain intact; and the wording matches the evidence level.


## Mosaic preview metadata (v3)

The canonical scenario file also carries the compact metadata required by Koali Use Mosaic:

```yaml
category_label: Find & understand
pattern_label: Investigate a signal
preview_summary: >-
  A 10–30 second public summary used during hover, focus, or touch selection.
preview_image: /scenarios/placeholders/SCN-001.svg
preview_image_alt: Abstract illustration for SCN-001...
badges: []
related:
  - SCN-002
  - SCN-016
```

These fields are editorial presentation metadata. **Spatial coordinates are deliberately not stored in the scenario file.** Scenario-to-slot assignment remains in the versioned Mosaic layout data under [`../src/data/`](../src/data/).
