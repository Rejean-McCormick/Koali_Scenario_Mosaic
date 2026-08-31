# Magnetic Territory Labels — Technical Specification

**Status:** implemented in Koali Scenario Mosaic v4.3 (specification retained as the implementation contract)  
**Target:** Koali Scenario Mosaic  
**Applies to:** main 120-scenario Mosaic only  
**Languages:** English and French  
**Rendering model:** Astro + SVG Mosaic + HTML overlay + GSAP/SplitText progressive enhancement

## 1. Purpose

The current Mosaic uses color to distinguish eight scenario territories. A conventional legend explains those colors, but it creates a separate visual layer that the visitor must mentally map back onto the honeycomb.

The proposed interaction removes that separation.

Each territory name becomes a large, low-opacity label that floats directly over its own 5 × 3 block of hexagons. The label is part of the map itself. When the pointer enters the Mosaic, nearby letters are repelled from the pointer as if affected by a magnetic field. When the pointer leaves, the letters return to their resting positions with a small spring/bounce.

The effect must feel alive without destabilizing the Mosaic.

> **Only the letters move. The hexagons never move.**

The fixed geography, one-active-cell rule, preview behavior, scenario routes, and bilingual structure remain unchanged. Territory color is now a two-tone Koali-brand checker rather than eight independent category hues.

## 2. Product intent

The effect should accomplish three things at once:

1. **Replace the detached color legend** with labels embedded directly in the eight color territories.
2. **Strengthen spatial understanding**: category meaning, color, and location become one object.
3. **Give the Mosaic a distinctive Koali interaction signature** without introducing a physics engine, Canvas, WebGL, or dynamic layout.

The interaction is decorative and explanatory. It must never become required to understand or operate the Mosaic.

## 3. Non-goals

This implementation must **not**:

- move, resize, rotate, or reflow scenario hexagons;
- dynamically reposition scenarios based on semantics;
- alter the fixed 20 × 6 Mosaic geography;
- create multiple active scenario highlights;
- require Three.js, Canvas, WebGL, Matter.js, or another physics engine;
- make category labels depend on JavaScript in order to exist;
- create pointer-driven effects on coarse-pointer/touch devices;
- animate when `prefers-reduced-motion: reduce` is active;
- expose internal Koali architecture names as category labels;
- replace the full category label used in the scenario preview/profile.

## 4. Selected technical approach

### 4.1 Stack

Use the existing stack plus one animation dependency:

- Astro 7
- TypeScript
- plain CSS
- existing SVG honeycomb
- **GSAP**
- **GSAP SplitText**
- custom proximity/repulsion calculation
- GSAP ticker or `requestAnimationFrame` for the spring loop

No framework hydration layer is required.

### 4.2 Why an HTML overlay instead of animating SVG `<text>` directly

The Mosaic itself remains SVG. The territory labels should be rendered as an absolutely positioned HTML layer over the SVG stage.

This is preferred because:

- SplitText can split normal HTML text into individual character elements cleanly;
- CSS typography and line wrapping are easier to control;
- EN and FR labels can use different line breaks without editing SVG markup;
- the character elements are straightforward to measure and animate;
- the overlay can use `pointer-events: none`, so it never interferes with hexagon interaction;
- if JavaScript fails, the unsplit label remains visible as normal text.

The overlay and the SVG must live inside the same positioned stage so they scale and scroll together.

## 5. Proposed component structure

Add:

```text
src/
├── components/
│   └── MosaicTerritoryLabels.astro
├── scripts/
│   └── territory-repulsion.ts
├── styles/
│   └── territory-labels.css
└── data/
    └── mosaic-layout.json
```

Existing files affected:

```text
src/components/ScenarioMosaic.astro
src/components/MosaicLegend.astro
src/scripts/mosaic.ts
src/styles/mosaic.css
src/i18n/...
src/data/mosaic-layout.json
```

### 5.1 `MosaicTerritoryLabels.astro`

Responsibilities:

- server-render the eight territory labels;
- render localized text from the active language;
- expose stable `data-territory-id` values (`CAT-01` … `CAT-08`);
- expose one text node per visual line;
- remain readable with JavaScript disabled;
- remain `aria-hidden="true"` because the labels are decorative duplicates of semantic category information available elsewhere.

Illustrative markup:

```astro
<div class="territory-label-layer" aria-hidden="true" data-territory-label-layer>
  <div
    class="territory-label territory-label--cat-01"
    data-territory-id="CAT-01"
    style="--x: 12.5%; --y: 25%; --w: 22%;"
  >
    <span class="territory-label__line">Find &amp;</span>
    <span class="territory-label__line">Understand</span>
  </div>
</div>
```

The final positions must come from layout data rather than being hard-coded in the component.

## 6. Territory layout data

The Mosaic is editorially composed. Territory-label positions should therefore also be explicit and stable rather than inferred dynamically at runtime.

Extend `mosaic-layout.json` with an optional section such as:

```json
{
  "territoryLabels": {
    "CAT-01": {
      "x": 0.125,
      "y": 0.245,
      "width": 0.215,
      "anchor": "center"
    },
    "CAT-02": {
      "x": 0.375,
      "y": 0.245,
      "width": 0.215,
      "anchor": "center"
    }
  }
}
```

Coordinates are normalized to the Mosaic stage (`0..1`) so they remain valid when the SVG scales.

Do not compute territory-label anchors from current DOM positions every load. The geography is stable and the label anchors should be versioned with that geography.

If the Mosaic receives a major future recomposition (`mosaic-v2`, `mosaic-v3`, etc.), the label anchors are versioned with it.

## 7. Localized territory strings

The text used as a large map label is a visual label and may need to be shorter than the full public category name.

Provide a dedicated localized field rather than truncating at runtime.

Example:

```ts
territories: {
  'CAT-01': {
    full: 'Find & Understand',
    mapLines: ['Find &', 'Understand'],
  },
  'CAT-08': {
    full: 'Disseminate & Connect to the Public',
    mapLines: ['Disseminate &', 'Connect'],
  },
}
```

French example:

```ts
territories: {
  'CAT-01': {
    full: 'Trouver et comprendre',
    mapLines: ['Trouver &', 'comprendre'],
  },
  'CAT-08': {
    full: 'Diffuser et rejoindre le public',
    mapLines: ['Diffuser &', 'connecter'],
  },
}
```

The full label remains available in the scenario preview/profile. The shorter `mapLines` version exists only for the large territory watermark.

No automatic hyphenation or machine abbreviation should be used.

## 8. Visual design

### 8.1 Rest state

Each territory label:

- sits visually over its territory;
- uses the same hue family as the territory;
- uses a lighter value than the hexagon fill;
- has low opacity;
- does not block or obscure scenario cells;
- remains legible enough to explain the color map without a separate legend.

Suggested initial values:

```css
.territory-label {
  opacity: 0.18;
  font-size: clamp(1.25rem, 2.4vw, 3.2rem);
  font-weight: 760;
  letter-spacing: 0.055em;
  line-height: 0.92;
  text-transform: uppercase;
  pointer-events: none;
  user-select: none;
}
```

These are tuning values, not immutable constants.

### 8.2 Color

Do not use the raw cell fill color as the text color because it may disappear into the cells.

Prefer a lightened variant of the same hue.

Conceptually:

```css
color: color-mix(in srgb, var(--territory-color) 62%, white 38%);
```

Provide explicit fallback values for browsers where `color-mix()` behavior is undesirable.

### 8.3 Active territory emphasis

When a scenario in a territory is hovered or keyboard-focused:

- that territory label may increase opacity modestly;
- other labels remain calm;
- the active scenario cell remains the strongest local focus.

Suggested opacity range:

```text
resting territory label: 0.16–0.22
active territory label:  0.34–0.48
```

Avoid turning the labels into foreground headlines.

## 9. SplitText lifecycle

### 9.1 Progressive enhancement

The server renders readable whole strings.

Client-side initialization:

1. detect motion/pointer eligibility;
2. wait for fonts to be ready;
3. SplitText each territory line into characters;
4. cache each character's resting center;
5. start the proximity engine only when needed.

If any step fails, leave the original static labels in place.

### 9.2 Import pattern

Illustrative client import:

```ts
import { gsap } from 'gsap';
import { SplitText } from 'gsap/SplitText';

gsap.registerPlugin(SplitText);
```

Pin a tested GSAP version in `package.json` and commit the lockfile. Do not rely on a floating `latest` dependency in production.

### 9.3 Avoid repeated splitting

Split each label once per initialization cycle.

Rebuild only after a layout-affecting change such as:

- viewport resize beyond a meaningful breakpoint;
- font load/reload;
- explicit language route change (normally a full page navigation in the current EN/FR architecture).

Use SplitText's revert/re-split lifecycle when rebuilding.

## 10. Interaction model

### 10.1 Pointer field

The pointer creates a circular influence field around itself.

For every character within the field:

1. measure the vector from pointer to character rest position;
2. calculate distance;
3. normalize the outward direction;
4. calculate a distance-based falloff;
5. set a temporary target displacement away from the pointer;
6. let the spring integrator move the character toward that target.

Characters outside the radius have a target offset of `(0,0)`.

### 10.2 Suggested tuning constants

Start with:

```ts
const CONFIG = {
  radius: 95,          // px at desktop scale
  maxOffset: 16,       // px maximum displacement
  forceExponent: 1.8,  // stronger close to pointer
  spring: 0.16,
  damping: 0.76,
  settleDistance: 0.08,
  settleVelocity: 0.08,
};
```

These are initial tuning values.

The intended visual range is approximately **8–18 px maximum movement**. More than this risks looking chaotic and may interfere with cell reading.

### 10.3 Falloff function

For distance `d` and influence radius `r`:

```ts
const proximity = Math.max(0, 1 - d / r);
const force = Math.pow(proximity, CONFIG.forceExponent);
```

Target displacement:

```ts
const targetX = directionX * CONFIG.maxOffset * force;
const targetY = directionY * CONFIG.maxOffset * force;
```

This makes the field strong near the cursor and fade smoothly at the boundary.

Do not use a hard on/off radius without falloff.

## 11. Spring / bounce model

Each character owns state:

```ts
type CharState = {
  el: HTMLElement;
  restX: number;
  restY: number;
  x: number;
  y: number;
  vx: number;
  vy: number;
  targetX: number;
  targetY: number;
};
```

At every animation tick:

```ts
vx += (targetX - x) * spring;
vy += (targetY - y) * spring;

vx *= damping;
vy *= damping;

x += vx;
y += vy;
```

Then apply only a transform:

```ts
gsap.set(el, {
  x,
  y,
  force3D: true,
});
```

This creates the desired overshoot/bounce when `targetX/targetY` return to zero.

### 11.1 Frame-rate independence

The production implementation should normalize spring integration using GSAP ticker delta time or a clamped frame factor so behavior remains consistent on 60 Hz, 90 Hz, 120 Hz, and temporarily throttled tabs.

Do not tune exclusively against a fixed 16.67 ms frame.

## 12. Event architecture

### 12.1 `pointermove`

`pointermove` should only update cached pointer coordinates and pointer-inside state.

Do **not**:

- query character DOM rectangles on every pointer event;
- create new GSAP tweens on every pointer event;
- write transforms directly in the pointer handler.

Example:

```ts
stage.addEventListener('pointermove', (event) => {
  pointer.x = event.clientX;
  pointer.y = event.clientY;
  pointer.active = true;
  wakeTicker();
}, { passive: true });
```

### 12.2 Pointer leave

On `pointerleave`:

```ts
pointer.active = false;
```

All character targets become zero. The ticker continues only until the spring settles, then sleeps.

### 12.3 Keyboard focus

Keyboard focus on a scenario cell should:

- keep the current single-cell highlight behavior;
- raise the corresponding territory label opacity;
- **not** trigger magnetic displacement because there is no pointer field.

This preserves accessibility and avoids arbitrary motion for keyboard users.

## 13. Coordinate system

Character centers must be measured in the same viewport coordinate system as the pointer.

Recommended approach:

```ts
const rect = char.getBoundingClientRect();
state.restX = rect.left + rect.width / 2;
state.restY = rect.top + rect.height / 2;
```

These reads occur during measurement/rebuild, not every frame.

When the page scrolls, the cached viewport coordinates become stale. Use one of these strategies:

**Preferred:** store rest positions relative to the Mosaic stage and convert pointer coordinates into stage-local coordinates.

```ts
const stageRect = stage.getBoundingClientRect();
const pointerLocalX = event.clientX - stageRect.left;
const pointerLocalY = event.clientY - stageRect.top;
```

Character rest centers are likewise stored relative to `stageRect`.

This avoids recalculating all characters on normal page scroll.

## 14. Responsive behavior

### 14.1 Desktop / fine pointer

Enable the full repulsion + spring effect when:

```css
(hover: hover) and (pointer: fine)
```

### 14.2 Tablet / touch / coarse pointer

Do not run magnetic pointer physics.

Territory labels remain static map labels.

Scenario tap behavior remains unchanged.

### 14.3 Narrow viewport / horizontal Mosaic scroll

The label overlay must be inside the same scrollable Mosaic stage as the SVG so both move together horizontally.

Do not position the labels relative to the viewport or page body.

### 14.4 `prefers-reduced-motion`

When:

```css
@media (prefers-reduced-motion: reduce)
```

- do not SplitText for animation purposes unless needed for styling;
- do not start the magnetic ticker;
- render territory labels statically;
- preserve category emphasis through opacity only.

The reduced-motion experience must remain fully understandable.

## 15. Interaction with scenario hover

The magnetic effect is independent from scenario selection.

The existing one-cell rule remains authoritative:

```text
pointer near territory text
    → letters move

pointer over scenario hexagon
    → exactly one cell becomes active
    → preview updates
    → territory label becomes more visible

related scenarios
    → no automatic highlight
```

Never let magnetic label logic add classes to scenario cells other than territory-level presentation state on the stage.

Suggested stage state:

```html
<div
  class="mosaic-stage"
  data-mosaic-stage
  data-active-territory="CAT-03"
>
```

CSS can then raise the corresponding label opacity without coupling the two scripts tightly.

## 16. Removal/replacement of the current legend

The final territory-label implementation is intended to replace the visible detached color legend.

However, removal should happen only after the embedded labels pass usability review.

Recommended rollout:

### Phase A — static labels

- add the eight embedded territory labels;
- leave current legend visible temporarily;
- test alignment, EN/FR text, responsive behavior.

### Phase B — magnetic enhancement

- enable SplitText + repulsion on desktop;
- tune opacity, force, radius, bounce;
- validate reduced motion and touch fallback.

### Phase C — remove visual legend

- remove/hide the detached visual legend;
- keep semantic category information for assistive technology;
- validate that a first-time visitor can still infer category/color meaning.

Do not remove the current legend in the same commit as the first physics prototype unless visual testing is already complete.

## 17. Accessibility

The animated labels are a decorative representation of category names already available semantically.

Requirements:

- label overlay: `aria-hidden="true"`;
- `pointer-events: none`;
- no focusable character spans;
- scenario cells retain current labels/titles;
- category meaning remains available in the preview and/or visually hidden semantic legend;
- reduced motion is respected;
- no information is available only through animation;
- color is not the only differentiator because territory names remain visible.

If the visible legend is removed, retain a screen-reader-only category list if needed.

## 18. Performance budget

Expected animated character count is small: approximately 100–200 characters across eight labels.

Target behavior:

- 60 fps on a typical laptop;
- no layout reads during animation frames;
- transform-only writes;
- no shadow/filter animation per character;
- no per-pointer-event tween creation;
- ticker sleeps after all characters settle;
- engine pauses when Mosaic is not visible.

### 18.1 Recommended optimization controls

Use:

- `IntersectionObserver` to disable/sleep when Mosaic is off-screen;
- `ResizeObserver` to schedule a single geometry rebuild;
- `document.fonts.ready` before first character measurement;
- GSAP `quickSetter` or cached `gsap.set` target references if profiling shows benefit;
- `will-change: transform` only on split character elements while animation is enabled.

Avoid permanent `will-change` on hundreds of elements if not necessary.

## 19. Animation sleep/wake lifecycle

The animation engine should not run continuously.

Wake when:

- pointer enters/moves within the Mosaic;
- pointer leaves and characters need to spring home;
- active category opacity needs animated transition.

Sleep when:

- pointer is outside the Mosaic;
- every character is within settle thresholds;
- no character velocity exceeds settle threshold.

Example condition:

```ts
const settled = chars.every((char) =>
  Math.abs(char.x) < CONFIG.settleDistance &&
  Math.abs(char.y) < CONFIG.settleDistance &&
  Math.abs(char.vx) < CONFIG.settleVelocity &&
  Math.abs(char.vy) < CONFIG.settleVelocity
);
```

## 20. CSS layering contract

Recommended layer order:

```text
z-index 1  → background / stage decoration
z-index 2  → scenario hexagons
z-index 3  → territory text watermark
z-index 4  → active hexagon visual emphasis (via SVG ordering/filter)
```

The exact technique depends on the current SVG stacking behavior. The important visual rule is:

> The territory label is visible across the field, but the active scenario cell remains the strongest foreground object.

Because the label overlay cannot intercept input, it may visually overlap cells safely.

## 21. Suggested CSS state model

```css
.territory-label {
  --territory-color: var(--territory-tone-a);
  opacity: .18;
  color: color-mix(in srgb, var(--territory-color) 58%, white 42%);
  transition: opacity 160ms ease;
}

.mosaic-stage[data-active-territory="CAT-01"]
  .territory-label[data-territory-id="CAT-01"] {
  opacity: .42;
}

.territory-label__char {
  display: inline-block;
  transform: translate3d(0,0,0);
  transform-origin: center;
}

@media (prefers-reduced-motion: reduce) {
  .territory-label__char {
    transform: none !important;
  }
}
```

## 22. Script skeleton

Illustrative architecture only:

```ts
import { gsap } from 'gsap';
import { SplitText } from 'gsap/SplitText';

gsap.registerPlugin(SplitText);

const stage = document.querySelector<HTMLElement>('[data-mosaic-stage]');
if (!stage) throw new Error('Missing Mosaic stage');

const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

if (finePointer && !reducedMotion) {
  initTerritoryRepulsion(stage);
}
```

Inside `initTerritoryRepulsion()`:

```text
1. split label lines into characters
2. measure rest positions in stage-local coordinates
3. register pointermove / pointerleave
4. register ResizeObserver
5. register IntersectionObserver
6. run spring integration through GSAP ticker
7. sleep ticker when all characters settle
8. revert SplitText on teardown
```

## 23. Teardown contract

The controller should expose a cleanup function even though Astro pages are currently static navigations.

Cleanup must:

- remove pointer listeners;
- disconnect `ResizeObserver`;
- disconnect `IntersectionObserver`;
- remove GSAP ticker callback;
- revert SplitText instances;
- clear transient transforms/classes.

This keeps the module safe if future navigation becomes client-side.

## 24. Bilingual behavior

EN and FR must share:

- territory IDs;
- anchor geometry;
- colors;
- physics constants;
- scenario membership.

They may differ in:

- number of characters;
- line breaks;
- label width;
- typographic scale within a bounded range.

Do not force French strings into English line breaks.

Each locale should define its own `mapLines` so composition remains editorially controlled.

The physics always operates on rendered characters after localization.

## 25. Scenario detail pages

The magnetic territory-label effect is **not required** on the selected scenario detail state introduced in v4.2.

Reason:

- that page replaces the 120-cell panorama with five information hexagons;
- the eight-category territory map is no longer being shown;
- magnetic category labels would add noise to a page whose goal is focused scenario reading.

Therefore:

```text
/en/uses/ and /fr/uses/
    → magnetic territory labels eligible

/en/uses/SCN-###/ and /fr/uses/SCN-###/
    → no magnetic territory labels by default
```

A future separate effect for the five information hexagons should be designed independently.

## 26. Failure and fallback behavior

### JavaScript disabled

- labels remain static and readable;
- Mosaic remains fully functional as static links where applicable.

### GSAP fails to load

- do not hide labels;
- do not throw a page-breaking error;
- leave unsplit text intact.

### SplitText fails

- same static fallback;
- scenario hover and preview script must remain independent.

### Runtime exception in magnetic controller

- controller should fail closed locally;
- remove transient transforms if possible;
- do not affect Mosaic cell interaction.

## 27. Testing matrix

### Functional

- [ ] exactly eight territory labels render in EN;
- [ ] exactly eight territory labels render in FR;
- [ ] labels align with the correct 5 × 3 territory blocks;
- [ ] labels never intercept pointer/click events;
- [ ] one and only one scenario cell is active on hover/focus;
- [ ] pointer proximity moves only letters;
- [ ] hexagon positions remain bit-for-bit unchanged;
- [ ] pointer leave returns all letters to rest;
- [ ] return includes a small overshoot/bounce;
- [ ] active category label becomes more visible;
- [ ] related scenarios remain unhighlighted.

### Accessibility

- [ ] `prefers-reduced-motion` produces static labels;
- [ ] touch/coarse pointer produces static labels;
- [ ] keyboard scenario focus still updates preview;
- [ ] keyboard navigation does not trigger arbitrary character motion;
- [ ] animated characters are hidden from assistive technology;
- [ ] category meaning remains available semantically.

### Responsive

- [ ] 1440 × 900 desktop;
- [ ] 1280 × 800 laptop;
- [ ] 1024 × 768 tablet landscape;
- [ ] ~832 px width (known previous problem width);
- [ ] 390 px mobile;
- [ ] horizontal Mosaic scroll keeps labels aligned with cells.

### Browser

- [ ] Chrome / Chromium;
- [ ] Edge;
- [ ] Firefox;
- [ ] Safari desktop;
- [ ] Safari iOS static fallback;
- [ ] Chrome Android static fallback.

## 28. Visual acceptance criteria

The effect is accepted only if all are true:

1. A first-time visitor can associate each color territory with its name **without consulting a separate visible legend**.
2. The Mosaic remains visually ordered and stable.
3. No letter moves more than approximately 18 px under normal tuning.
4. The active scenario hexagon remains easier to identify than the moving text.
5. The spring return feels responsive, not rubbery or comedic.
6. The bounce settles quickly after the pointer leaves.
7. The effect does not cause scroll, reflow, or layout shift.
8. EN and FR both look intentionally composed.
9. With reduced motion, the Mosaic still looks complete rather than degraded.
10. The effect can be removed without changing scenario data or Mosaic geometry.

## 29. Recommended tuning sequence

Tune in this order:

### Step 1 — static typography

Get label position, size, line breaks, color, and opacity right with **no animation**.

### Step 2 — proximity radius

Tune only influence radius and max displacement.

### Step 3 — spring return

Tune spring and damping after the repulsion field already feels correct.

### Step 4 — active territory emphasis

Add opacity response to scenario hover/focus.

### Step 5 — performance

Profile animation and add sleep/wake logic.

### Step 6 — remove detached legend

Only after usability review confirms the embedded labels explain the territories sufficiently.

Do not tune all variables at once.

## 30. Initial recommended values

Use these only as a starting preset:

```ts
export const TERRITORY_REPULSION_DEFAULTS = {
  radiusDesktop: 96,
  maxOffset: 15,
  forceExponent: 1.85,
  spring: 0.15,
  damping: 0.77,
  restOpacity: 0.19,
  activeOpacity: 0.42,
  settleDistance: 0.08,
  settleVelocity: 0.08,
};
```

Expected perceptual behavior:

```text
pointer far away   → static watermark
pointer approaches → nearby letters drift outward
pointer close      → local 8–15 px repulsion
pointer moves      → field follows smoothly
pointer exits      → letters spring past rest slightly
                    → one small bounce
                    → settle at exact original position
```

## 31. Dependency policy

When implementation begins:

1. add GSAP through npm;
2. pin a tested version;
3. commit `package-lock.json`;
4. verify `npm run build` on the supported Node version;
5. verify the Netlify production build;
6. ensure no Python dependency is introduced into the production build path.

The magnetic labels are a client-side enhancement and must not affect Astro static generation.

## 32. Validation hooks to add during implementation

Add a dedicated validation script, e.g.:

```text
scripts/validate-territory-labels.mjs
```

It should verify statically that:

- exactly 8 territory label anchors exist;
- every `CAT-01..CAT-08` has one anchor;
- EN and FR both provide map-label text;
- every territory label anchor falls inside the Mosaic viewBox/normalized range;
- no label is attached to a scenario ID;
- the two Koali-derived checker tones remain mapped consistently to territory positions;
- the old visible legend is not removed until the feature flag/implementation status says magnetic labels are production-ready.

Once production-ready, extend the UI contract validation to assert:

- label overlay exists;
- `pointer-events: none` is present;
- reduced-motion fallback exists;
- magnetic script does not modify scenario geometry;
- the one-active-cell contract remains intact.

## 33. Suggested feature flag during development

During implementation, gate the effect behind a local configuration flag:

```ts
export const ENABLE_MAGNETIC_TERRITORY_LABELS = true;
```

or a `data-` attribute on the Mosaic root.

This allows rapid A/B comparison between:

- current legend;
- static embedded labels;
- animated embedded labels.

Remove the temporary flag once the design is accepted.

## 34. Design invariant

The governing rule for this feature is:

> **The map stays still. Meaning becomes alive.**

The Mosaic geography must remain calm and dependable. The kinetic behavior belongs only to the typographic layer that explains the territories.

That distinction is what lets the effect feel expressive without making the interface chaotic.
