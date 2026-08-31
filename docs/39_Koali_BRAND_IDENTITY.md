# Koali brand identity — v3.10

## Canonical name

**Koali**

The public and editorial brand name is always written with this casing. Do not use an all-capital rendering of the brand name in user-facing text.

Lowercase `koali` remains valid only where a technical ecosystem convention requires it, for example the npm package name `koali-scenario-mosaic`.

## Canonical positioning line

> **Koali, the Sociotechnical Operating System**

This is the preferred English category/positioning phrase.

## Scenario interface name

> **Koali Scenario Mosaic**

“Scenario” remains singular because it functions attributively in the compound name.

## Primary brand color

**`#1e6864`**

The color is used for the Koali mark, the Koali word in the header, theme metadata, focus accents, and cover branding.

The eight Mosaic category colors remain intentionally distinct. They encode scenario families and should not be replaced by the Koali brand color.

## Logo asset

Canonical web asset:

```text
public/brand/koali-mark.svg
```

The supplied SVG geometry is preserved. Its accessibility metadata was normalized to identify it as the **Koali mark**.

The mark is integrated into:

- the Astro site header;
- the zero-install/offline preview header;
- the branded Mosaic cover composition.

## Header hierarchy

The header presents three levels without turning the brand into an all-caps wordmark:

```text
[Koali mark]  Koali  Scenario Mosaic
              the Sociotechnical Operating System
```

The product/interface name remains visible, while the positioning line establishes what Koali is.

## Validation

`npm run validate:name` checks the canonical product name, Koali capitalization, positioning line, brand color, and logo asset. Public/editorial text must not regress to an all-caps Koali wordmark.
