# Spatial Layout Data Model

## Principle

Position is **editorially assigned**, not calculated at runtime.

Each scenario is assigned to a slot. Slots have fixed coordinates in a virtual SVG space.

## Recommended format

```json
{
  "version": "mosaic-v1",
  "viewBox": [0, 0, 1440, 900],
  "slots": {
    "slot-001": { "x": 220, "y": 140, "size": 22 },
    "slot-002": { "x": 264, "y": 165, "size": 22 }
  },
  "assignments": {
    "SCN-001": "slot-037",
    "SCN-002": "slot-061"
  }
}
```

## Why slots instead of x/y inside Markdown

- layout remains independent from content;
- free positions can be reserved;
- scenarios can be reassigned without touching 120 files;
- the design can be versioned;
- a visual editor can be built later.

## Free slots

Plan for approximately 140–160 slots for 120 scenarios. Unassigned slots are not rendered.

## Stability

Once `mosaic-v1` is published:

- do not move a cell for a simple copy change;
- prefer assigning a new scenario to a free slot;
- perform a major relayout only as an explicit new editorial version.
