# Preview Copy Deduplication — v3.8

## Problem

The scenario title and `preview_summary` were generated from the same opening situation sentence. In the public preview this produced copy such as:

```text
An elevator breaks down in a building

An elevator breaks down in a building. The person doing the work needs...
```

The repetition wastes scarce preview space and makes the interface feel mechanically generated.

## Decision

`title` states the concrete situation. `preview_summary` must **continue the thought** rather than restate it.

For example:

```text
TITLE
An elevator breaks down in a building

SUMMARY
The person doing the work needs more than a task title: they need context,
history, constraints, and expected evidence of completion.
```

## Corpus migration

All 120 canonical scenario files were normalized in v3.8. The duplicated title sentence was removed from `preview_summary`; the body of each scenario remains unchanged.

This means the same cleaner copy is used by:

- the Mosaic hover/focus preview;
- the full scenario page subtitle/deck;
- the zero-install offline preview;
- any future surface consuming `preview_summary`.

## Validation

`npm run validate:copy` checks every canonical scenario and fails if:

- `preview_summary` is empty;
- it starts with the scenario title;
- its first sentence normalizes to the scenario title.

The production validation chain includes this check automatically.
