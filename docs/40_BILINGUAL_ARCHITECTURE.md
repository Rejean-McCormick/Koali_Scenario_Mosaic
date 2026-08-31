# Bilingual Architecture — v4.0

## Principle

**One scenario identity, one Mosaic position, one semantic profile — multiple editorial languages.**

English and French are not independent copies of the product. They are localized editorial views over the same 120 scenario identities.

## Source hierarchy

### Shared machine-facing scenario data

`src/data/scenarios.json`

This file is authoritative for language-independent fields such as:

- `id`;
- `primary_category`;
- `pattern_family`;
- usage-palette keys;
- component profiles;
- entry trigger;
- scales, settings, properties, and domain keys;
- signature/canon references;
- transfer domains;
- derivation and runtime-evidence status;
- preview-image identity;
- stable operational loop.

These fields are not copied into EN/FR Markdown files.

### Localized editorial content

```text
src/content/scenarios/en/SCN-001.md … SCN-120.md
src/content/scenarios/fr/SCN-001.md … SCN-120.md
```

Localized frontmatter contains only:

- stable `id`;
- `locale`;
- title;
- category label;
- pattern label and public pattern description;
- continuity-gap prose;
- preview summary;
- localized image alt text.

The Markdown body is editorial content in that language.

## Routes

```text
/en/uses/
/fr/uses/
/en/uses/SCN-###/
/fr/uses/SCN-###/
```

The root `/` uses `navigator.languages` to choose French when a French browser language is present; otherwise it opens English. The visible EN/FR switch remains the authoritative user choice.

The language switch preserves the current path. For example:

```text
/en/uses/SCN-061/  ⇄  /fr/uses/SCN-061/
```

## Shared geography

Both languages read the same `src/data/mosaic-layout.json`. Translation never changes an ID, slot, color family, image, or semantic relationship.

This makes the Mosaic itself a continuity device between languages: a person who learns where a scenario is located in English finds it in the same place in French.

## UI localization

`src/i18n/ui.ts` contains interface copy and activity labels.

`src/i18n/fr-tags.json` translates machine-facing public labels such as:

- scales;
- settings;
- properties;
- domains;
- transfer domains;
- usage-palette verbs.

The v4 validator confirms that every shared public tag used by the 120 scenarios has a French label.

## Translation policy

French source files are versioned content, not runtime translations. AI or machine translation may assist an editorial revision, but the result must be committed as normal source text and can be reviewed independently.

No visitor depends on an external translation service.

## Offline preview

`npm run preview:offline` now creates both language surfaces:

```text
preview/index.html
preview/en/index.html
preview/fr/index.html
preview/en/uses/SCN-###/index.html
preview/fr/uses/SCN-###/index.html
```

`START.html` remains the zero-install entry point.

## Adding a third language later

The architecture is intentionally extensible. A third language would require:

1. a new locale in `src/i18n/ui.ts`;
2. translated public tag labels;
3. 120 localized scenario Markdown documents;
4. adding the locale to static route generation and validators.

The shared metadata, Mosaic layout, image mapping, and scenario IDs would remain unchanged.
