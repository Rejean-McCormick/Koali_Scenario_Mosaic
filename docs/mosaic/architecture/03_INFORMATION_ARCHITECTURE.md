# Information Architecture

## Routes

### `/uses/`
Main Mosaic.

### `/uses/{scenario-id}/`
Detailed static scenario page.

Example: `/uses/SCN-079/`.

### Optional future routes

- `/uses/theme/offline/`
- `/uses/theme/multilingual/`
- `/uses/component/kristal/`
- `/uses/search/`

They are not required for the MVP.

## Mosaic page

Recommended order:

1. minimal header;
2. discovery panel;
3. mosaic;
4. small help / legend area;
5. link to a Koali explanation;
6. footer.

On desktop, the discovery panel and mosaic should be visible together whenever practical.

## Scenario page

1. back to Mosaic;
2. image;
3. title;
4. summary;
5. full scenario;
6. loop/workflow;
7. palette and components;
8. a few related scenarios;
9. source/status if desired;
10. previous / next or back to Mosaic.

## URLs

The ID (`SCN-001`) is the stable key. A human-readable slug may be added, but the ID must never change after publication.
