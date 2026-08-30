# v3.3 — Regular honeycomb + single hover

> **Geometry superseded in v3.7.** The single-highlight rule remains active, but the 12 × 10 geometry described here was replaced by the 20 × 6 panoramic spread in [`36_PANORAMIC_SPREAD_AND_COLOR_LEGEND.md`](36_PANORAMIC_SPREAD_AND_COLOR_LEGEND.md).


Only one cell receives `is-active`. Related-scenario highlighting is removed. The 120 current cells are generated on a pointy-top hex lattice: horizontal spacing `sqrt(3)×s`, vertical spacing `1.5×s`, odd-row offset `sqrt(3)×s/2`. There are no row-specific drifts.
