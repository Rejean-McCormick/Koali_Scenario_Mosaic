# Contributing

1. Edit canonical scenarios in `src/content/scenarios/`.
2. Keep `derivation` and `runtime_evidence` truthful.
3. Never hand-edit `preview/`.
4. Run `npm run validate` before committing.
5. Run `npm run preview:offline` after visible content/UI changes.
6. Add scenario 121+ with `npm run slot:assign -- SCN-121`.
7. Do not automatically cluster/recompute the existing Mosaic layout.
