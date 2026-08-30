# TypeScript Interactions

## Responsibility

The client script should only:

- listen for pointer/focus events;
- find scenario data;
- update the panel;
- manage CSS states;
- handle touch behavior;
- optionally preload an image.

## No global store required

A simple `scenarioById` object serialized into the page is sufficient.

## Events

Desktop:

- `pointerenter` → preview;
- `focus` → preview;
- `click` → native link navigation.

Mobile:

- detect fine/coarse pointer;
- tap → prevent immediate navigation if the scenario is not already selected;
- CTA → navigate.

## Debounce

A 40–80 ms delay can prevent frantic updates when the pointer crosses cells quickly. Do not exceed roughly 120 ms or the page starts to feel sluggish.

## Preloading

When the preview changes, load the current image; optionally preload images for the 3–6 nearby or `related` scenarios.

## Graceful degradation

Without JavaScript:

- cells remain links;
- clicking opens scenario pages;
- only the dynamic preview is lost.

This is an important objective.
