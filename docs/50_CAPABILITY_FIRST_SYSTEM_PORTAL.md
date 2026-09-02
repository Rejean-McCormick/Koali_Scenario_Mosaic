# Capability-first system portal — v4.4.12

## Purpose

The public Mosaic is a door into Koali, not a gallery of edge cases. The 120 scenario identities remain valuable as concrete examples, but they no longer carry the conceptual hierarchy. The public hierarchy is:

`need / action → specific Koali action → what Koali does → specific system path → concrete example`

The 24 recurring patterns organize those 120 specific actions as a secondary taxonomy; they are not reused as the public headline.

## 24 pattern families, 120 specific public actions

The existing 24 pattern families remain the reusable conceptual layer, but they are no longer reused as public titles. `src/data/scenario-capability-titles.json` gives every scenario a specific bilingual action title derived from what Koali actually does in that example. The original scenario title remains the concrete example, while `pattern_label` remains the recurring family for taxonomy and search. This prevents repeated headings such as “Investigate a signal / Enquêter sur un signal” while preserving the 24-pattern architecture.

The main explanatory paragraph no longer repeats a generic continuity formula or paraphrases the public action title. The title names the **specific action**; the complete `preview_summary` creates a two-sentence impact arc: first the concrete problem, then the change Koali makes possible and its practical payoff. `continuity_gap` separately explains what tends to break when the shared thread is lost. A generated continuity paragraph remains available only as a fallback for legacy scenarios without authored public impact copy.

## System paths

`src/data/system-catalog.json` defines the public system vocabulary and short bilingual descriptions. `src/data/scenario-system-routes.json` gives every `SCN-xxx` one to three curated discovery paths.

The routes are **entry points, not exclusive ownership claims**. A real Koali use can involve more components than the 1–3 names shown publicly. The purpose of the list is to answer the visitor's next question: “Which part of Koali does this?”

Examples of path granularity include:

- `Kristal`
- `SemantiK`
- `Konnaxion → KonnectED → Knowledge`
- `Konnaxion → KonnectED → CertifiKation`
- `Konnaxion → Ethikos → Korum`
- `Konnaxion → Ethikos → Konsultations`
- `Konnaxion → Kollective Intelligence → Smart Vote`
- `Konnaxion → Kollective Intelligence → EkoH`
- `Konnaxion → keenKonnect → Konstruct`
- `Konnaxion → keenKonnect → Stockage`
- `Konnaxion → Kreative → Kontact`
- `Konnaxion → Kreative → Konservation`
- `Orgo`
- `UCKK`

These names are based on the supplied Koali/Konnaxion architecture material. They are intentionally kept outside the main prose.

## Eight human-facing actions

The eight backlight tags remain short human verbs: Find, Understand, Learn, Collaborate, Choose, Act, Respond, Remember (and their French equivalents). They are not redefined as modules. Their tooltip/ARIA metadata can point toward the architecture usually involved, while the selected example provides the more precise system route.

## Public selected-example layout

The top preview now reads:

1. scenario ID + broad family;
2. **specific Koali action title**;
3. **the problem and practical change Koali makes possible**;
4. **Example:** original scenario title;
5. eight action tags;
6. **Inside Koali / Dans Koali:** the precise system path plus scale/context/conditions.

On the detailed route, the five public information cards are:

1. Starts from / Part de;
2. What breaks without continuity / Ce qui se perd sans continuité;
3. System path / Chemin système;
4. How it moves / Comment ça circule;
5. Also useful for / Aussi utile pour.

`continuity_gap` is public again because it explains **why continuity matters** without pretending that Koali itself performs every specialized action. The reusable `pattern` remains in taxonomy and search rather than being mislabeled as a “Koali mechanism.”

## Search

Search indexes the specific action title, recurring pattern family, Koali explanation, system route names and descriptions, original example title, palette, scale, setting, property, and domain. A visitor can therefore search `Smart Vote`, `SemantiK`, `Orgo`, a Konnaxion sub-system, a human need, or the concrete example.

## Responsive behavior

The v4.3.5 selected-state and swipe behavior are retained. On smartphone the reading order remains copy → system path/context → image. The longer mechanism paragraph is not clamped on narrow screens.

## Offline parity

`scripts/build-offline-preview.py` reads the same system catalog and scenario route map and generates the same hierarchy under `preview/`. The zero-install preview therefore remains conceptually aligned with the Astro site.

## Validation

`validate:repo` enforces:

- exactly 120 scenario route entries;
- exactly 120 bilingual specific action-title entries;
- specific public titles are unique per language and cannot equal the recurring `pattern_label`;
- 1–3 unique system paths per scenario;
- every route key exists in the system catalog;
- explicitly tagged Smart Vote, EkoH, and SemantiK metadata cannot silently lose their specialized route;
- the capability-first preview and system-list contracts remain present.
- scenario titles, continuity gaps, and impact summaries remain unique and synchronized in English and French;
- each impact summary presents the problem before the Koali response in exactly two concise sentences;
- the Koali response stays below the allowed meaningful-word overlap with its capability title.
