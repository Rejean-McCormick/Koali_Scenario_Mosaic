# Accessibility

## Objective

The Mosaic must remain exploratory without becoming inaccessible to keyboard users, screen-reader users, or people who prefer reduced motion.

## SVG

Every interactive cell should be a real link (`<a>`) inside the SVG or a correctly labeled focusable element.

Use:

- descriptive `aria-label`;
- `<title>` for the scenario when appropriate;
- logical DOM order;
- visible focus.

## Keyboard

- Tab moves through cells;
- focus triggers the preview;
- Enter opens the scenario;
- Escape may restore the default panel.

## Motion

Respect `prefers-reduced-motion: reduce`: remove unnecessary scaling or transitions.

## Color

Never encode a badge/status using color alone. Text and labels remain available.

## Screen readers

The mosaic should have an accessible title and short description: **Interactive Mosaic of 120 Koali scenarios. Use Tab to browse the scenarios.**

## Alternative

Add a **View scenarios as a list** link leading to a linear HTML view. This also helps SEO and fast navigation.
