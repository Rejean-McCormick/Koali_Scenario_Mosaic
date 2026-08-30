# Preview Panel

## Role

The panel turns an abstract cell into an understandable story in roughly 10–30 seconds of attention.

## Non-negotiable layout rule

**Hovering or focusing a different scenario must never move the Mosaic vertically.**

The preview reserves an explicit height at each responsive breakpoint. Variable-length fields are constrained inside fixed regions:

- title: maximum 2 displayed lines;
- summary: maximum 3 displayed lines;
- palette: one reserved row;
- typical-motion label: maximum 2 displayed lines;
- public profile: fixed indicator and context regions.

The complete content remains available on the full scenario page.

## Desktop composition

```text
┌───────────────┬──────────────────────────────┬────────────────────────────┐
│ IMAGE         │ SCN-### · CATEGORY           │ SCENARIO PROFILE           │
│               │ Title                        │ ● Find & Understand        │
│               │ 3-line summary               │ Typical motion             │
│               │ palette tags                 │ Investigate a signal       │
│               │ Read scenario →              │                            │
│               │                              │ ● Understand   ○ Learn     │
│               │                              │ ● Create       ○ Decide    │
│               │                              │ ● Act          ○ Respond   │
│               │                              │ ● Remember                  │
│               │                              │ Scale · Context · Conditions│
└───────────────┴──────────────────────────────┴────────────────────────────┘
```

## Public scenario indicators

### Category

A category-colored swatch plus the **category name**. Stable `CAT-##` IDs remain internal metadata and are not required in the public hover.

### Typical motion

The public pattern name explains what kind of continuity is happening, without displaying `PAT-##` codes.

### What happens here

Seven visual lights are derived directly from the canonical usage palette:

- Understand
- Learn & share
- Create together
- Decide
- Organize & act
- Respond
- Remember & share

They are binary indicators, not numerical scores. See [`../../31_PUBLIC_SCENARIO_PROFILE.md`](../../31_PUBLIC_SCENARIO_PROFILE.md) for the exact mapping.

### Scale

Shows who the scenario spans: individual, team, organization, community, public institution, etc.

### Context

Combines the scenario's existing setting/domain metadata into a compact human-readable phrase.

### Special conditions

Shows explicit cross-cutting constraints only when present: offline, multilingual, sensitive data, public-facing, high consequence, and similar properties. If none is assigned, the UI says **None highlighted**.

## What is intentionally absent

Kristal, Konnaxion, Orgo, and UCKK are **not public hover indicators**. They are architectural implementation concepts. They may be explained on the full scenario page after the visitor already understands the situation.

Derivation status and runtime-evidence status are also excluded from the public preview. They remain part of editorial/claim governance, not the 10–30 second discovery interaction.

## Copy

### Title

The canonical title is used, but the preview displays at most two lines.

### Summary

A concise hover summary communicates:

1. the situation;
2. what Koali connects;
3. the continuity/result created.

The preview displays at most three lines to protect layout stability.

## Palette tags

Up to five usage-palette verbs remain visible below the summary. They provide direct action vocabulary and complement the public profile.

## Image

The image area has a fixed reserved size. Switching images cannot change panel geometry. Images use `object-fit: cover`; only the pixels change.

## Responsive behavior

The same stability rule applies at every breakpoint:

- desktop: three-column fixed-height preview;
- tablet: image/copy above a fixed-height profile strip;
- mobile: fixed rows for image, copy, and profile panel.

The exact pixel heights are implementation details defined in `src/styles/mosaic.css`; the invariant is that scenario-to-scenario changes never reflow the Mosaic.
