# Performance Budget

## Objective

The mosaic should appear quickly and hover should feel instantaneous.

## Pragmatic targets

- lightweight initial HTML/SVG;
- client JavaScript ideally below 40–60 KB compressed for this feature;
- do not bulk-load scenario images;
- no heavy visualization library at runtime;
- no continuous animation.

## 120 cells

120 SVG elements are not a meaningful performance problem. Images, fonts, CSS effects, and third-party scripts will dominate performance.

## Fonts

Limit font families/weights. Preload only what is genuinely used above the fold.

## Analytics

Avoid a heavy analytics package that cancels out the benefits of static-first.
