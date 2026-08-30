from pathlib import Path
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]
def err(s): errors.append(s)
scenarios=sorted((ROOT/'src/content/scenarios').glob('SCN-*.md'))
if len(scenarios)!=120: err(f'Expected 120 scenarios, found {len(scenarios)}')
ids=[]
for p in scenarios:
    m=re.fullmatch(r'(SCN-\d{3})\.md',p.name)
    if not m: err(f'Bad scenario filename: {p.name}'); continue
    ids.append(m.group(1)); t=p.read_text(encoding='utf-8')
    for field in ['preview_summary:','preview_image:','category_label:','pattern_label:','runtime_evidence:']:
        if field not in t: err(f'{p.name}: missing {field[:-1]}')
layout=json.loads((ROOT/'src/data/mosaic-layout.json').read_text())
if len(layout.get('slots',{}))!=150: err('Expected 150 Mosaic slots')
if len(layout.get('assignments',{}))!=120: err('Expected 120 assigned Mosaic slots')
if len(layout.get('reservedSlots',[]))!=30: err('Expected 30 reserved Mosaic slots')
for sid in ids:
    if sid not in layout.get('assignments',{}): err(f'Missing layout assignment: {sid}')
if not (ROOT/'preview/index.html').exists(): err('Missing preview/index.html')
for sid in ids:
    if not (ROOT/'preview/uses'/sid/'index.html').exists(): err(f'Missing preview page {sid}')
# relative Markdown link validation
link_re=re.compile(r'!?\[[^\]]*\]\(([^)]+)\)')
checked=0
for p in [*ROOT.glob('*.md'),*(ROOT/'docs').rglob('*.md')]:
    for raw in link_re.findall(p.read_text(encoding='utf-8')):
        target=raw.strip().split()[0]
        if target.startswith(('#','http://','https://','mailto:','tel:')): continue
        target=target.split('#',1)[0]
        if not target: continue
        checked+=1
        if not (p.parent/target).resolve().exists(): err(f'Broken link: {p.relative_to(ROOT)} -> {target}')
print(f'Scenarios: {len(scenarios)}')
print(f'Mosaic slots: {len(layout.get("slots",{}))} / assigned {len(layout.get("assignments",{}))} / reserved {len(layout.get("reservedSlots",[]))}')
print(f'Preview scenario pages: {sum(1 for _ in (ROOT/"preview/uses").glob("SCN-*/index.html"))}')
print(f'Markdown relative links checked: {checked}')
if errors:
    print('\nVALIDATION FAILED')
    for x in errors[:250]: print(' -',x)
    if len(errors)>250: print(f' ... {len(errors)-250} more')
    sys.exit(1)
print('Repository validation passed.')
