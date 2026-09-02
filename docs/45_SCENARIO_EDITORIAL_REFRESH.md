# v4.3 — Scenario editorial refresh

## What changed

All 120 scenarios were rewritten around stronger narrative hooks and pressure tests while preserving the stable `SCN-001`…`SCN-120` identities, the eight categories, and the 24 pattern families.

The refresh is complete in **French and English**. Shared metadata was also realigned so public context tags, transferable domains, flow/search data, scale, and important operating conditions do not describe the superseded scenarios.

## Editorial direction

The new corpus favors situations that reveal why continuity matters:

- rare or contradictory signals;
- provenance and contested realities;
- tacit expertise that may disappear;
- distributed learning and coordination;
- collective decision-making and explicit mandates;
- crisis response with confidentiality and degraded connectivity;
- long-term institutional memory;
- knowledge that becomes media, learning, or new combinations.

“Punchier” does not mean sensational for its own sake. Each hook must exercise the canonical pattern and preserve authority, evidence, privacy, and safety boundaries.

## Title and continuity pass

The current pass sharpens the 120 English titles, then aligns all 120 French titles to the same intent rather than translating word for word. Each scenario now also carries a distinct `continuity_gap` tied to its concrete pressure point.

To keep the public reading rhythm varied:

- titles avoid repeated article-led openings and recurring sentence frames;
- continuity gaps name the specific information, decision, relationship, or memory at risk;
- every `preview_summary` contains exactly two public-facing sentences: the concrete problem first, then the change Koali makes possible;
- the public card displays that complete impact arc instead of extracting a Koali sentence that paraphrases the capability title;
- the second sentence is also the source for each internal `With Koali / Avec Koali` section, preventing the public and editorial versions from drifting;
- titles, H1 headings, image alt text, and generated EN/FR previews remain synchronized.

`scripts/validate-editorial-variety.py` enforces uniqueness, the two-sentence problem/impact structure, a 30–50 word display budget, EN/FR preview alignment, and a strict ceiling on meaningful word reuse between the capability title and the Koali response.

## Compatibility

Mosaic geometry, scenario IDs, pattern families, component scores, canon references, derivation states, and runtime-evidence states remain stable. Existing links by scenario ID continue to work.
