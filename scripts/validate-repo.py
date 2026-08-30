from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[1];js=(R/'src/scripts/mosaic.ts').read_text();css=(R/'src/styles/mosaic.css').read_text();l=json.loads((R/'src/data/mosaic-layout.json').read_text());e=[]
if len(list((R/'src/content/scenarios').glob('SCN-*.md')))!=120:e.append('scenario count')
if 'is-related' in js or 'is-related' in css:e.append('related highlight')
if '.mosaic-cell:hover' in css:e.append('css hover state')
if '.mosaic-cell:focus-visible' in css:e.append('independent focus highlight')
if 'selectOnly' not in js:e.append('single select')
dx=l['geometry']['dx'];dy=l['geometry']['dy'];pts=[l['slots'][l['assignments'][f'SCN-{i:03d}']] for i in range(1,121)]
for r in range(12):
 row=pts[r*10:(r+1)*10]
 if any(abs((b['x']-a['x'])-dx)>.01 for a,b in zip(row,row[1:])):e.append(f'row {r}')
if any(abs(pts[(r+1)*10]['y']-pts[r*10]['y']-dy)>.01 for r in range(11)):e.append('vertical')
print('120 scenarios; 12 × 10 regular honeycomb; single active cell; related highlighting removed')
if e:print(e);sys.exit(1)
