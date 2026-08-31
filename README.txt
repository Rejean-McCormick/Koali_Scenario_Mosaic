KOALI mobile UI fix

Changes for screens <= 720px:
- scenario text first
- scenario profile second
- preview image moved to the bottom
- profile layout forced to one column
- activity signature forced to one column
- context labels/values stacked vertically

Desktop/tablet layout above 720px is unchanged.

Apply either:
1. Replace src/styles/mosaic.css with the included file, or
2. Apply koali-mobile-smartphone.patch.

Then regenerate the offline preview if needed with the repository's preview build command.
