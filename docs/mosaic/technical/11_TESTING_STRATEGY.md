# Testing Strategy

## Build-time

- valid content schema;
- 120 unique IDs;
- every scenario has a layout slot;
- no slot assigned twice;
- no missing image;
- no broken route;
- component scores stay within 0–5.

## Lightweight unit tests

For functions such as:

- scenario lookup;
- polygon point calculation if used;
- mobile selection;
- filtering/search if added.

## Browser / E2E

With Playwright or equivalent:

1. page loads;
2. hovering SCN-001 updates the panel;
3. keyboard focus produces the same result;
4. click navigates to `/uses/SCN-001/`;
5. mobile tap selects without leaving;
6. mobile CTA opens;
7. accessible list view works.

## Visual regression

Very useful for this page: capture desktop/tablet/mobile screenshots on every release to detect layout movement or styling regressions.
