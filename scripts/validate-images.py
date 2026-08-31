from pathlib import Path
import json, re, struct, sys

R=Path(__file__).resolve().parents[1]
PNG_DIR=R/'public/scenarios/images'
errors=[]
pngs=sorted(PNG_DIR.glob('*.png')) if PNG_DIR.exists() else []
seen=set()
for p in pngs:
    m=re.fullmatch(r'SCN-(\d{3})\.png',p.name)
    if not m: errors.append(f'Invalid PNG name: {p.name}'); continue
    n=int(m.group(1))
    if not 1<=n<=120: errors.append(f'PNG outside SCN-001..120: {p.name}')
    if n in seen: errors.append(f'Duplicate scenario PNG number: {n:03d}')
    seen.add(n)
    b=p.read_bytes()
    if not b.startswith(b'\x89PNG\r\n\x1a\n'): errors.append(f'Invalid PNG signature: {p.name}'); continue
    if len(b)<24 or b[12:16]!=b'IHDR': errors.append(f'Missing PNG IHDR: {p.name}'); continue
    w,h=struct.unpack('>II',b[16:24])
    if w<64 or h<64: errors.append(f'PNG too small: {p.name} ({w}x{h})')

for locale in ('en','fr'):
    preview=R/'preview'/locale/'index.html'
    if not preview.exists(): errors.append(f'preview/{locale}/index.html missing; run npm run preview:offline'); continue
    text=preview.read_text(encoding='utf-8')
    m=re.search(r'<script type="application/json" data-mosaic-data>(.*?)</script>',text,re.S)
    if not m: errors.append(f'Offline {locale} preview scenario JSON missing'); continue
    data=json.loads(m.group(1))
    if len(data)!=120: errors.append(f'Offline {locale} preview has {len(data)} scenarios')
    for i in range(1,121):
        sid=f'SCN-{i:03d}'; item=data.get(sid)
        if not item: errors.append(f'Offline {locale} preview missing {sid}'); continue
        png_name=f'{sid}.png'; exists=(PNG_DIR/png_name).exists(); image=item.get('image','')
        expected=f'../../public/scenarios/images/{png_name}' if exists else f'../assets/scenarios/{sid}.svg'
        if image!=expected: errors.append(f'{locale}/{sid}: image is {image!r}, expected {expected!r}')
        resolved=(preview.parent/image).resolve()
        if not resolved.exists(): errors.append(f'{locale}/{sid}: resolved preview image missing: {resolved}')

helper=R/'src/lib/scenario-image.ts'; component=R/'src/components/ScenarioMosaic.astro'
if not helper.exists() or 'existsSync' not in helper.read_text(encoding='utf-8'): errors.append('Astro PNG resolver helper missing')
if not component.exists() or 'resolveScenarioPreviewImage' not in component.read_text(encoding='utf-8'): errors.append('Astro Mosaic does not use PNG resolver')
print(f'Scenario PNGs available: {len(pngs)} / 120; SVG fallback: {120-len(pngs)}')
if errors:
    print('\nIMAGE VALIDATION FAILED')
    for e in errors: print(' -',e)
    sys.exit(1)
print('Bilingual scenario image validation passed.')
