from pathlib import Path
import json, re, struct, sys

R = Path(__file__).resolve().parents[1]
PNG_DIR = R / 'public' / 'scenarios' / 'images'
PREVIEW = R / 'preview' / 'index.html'
errors = []

pngs = sorted(PNG_DIR.glob('*.png')) if PNG_DIR.exists() else []
seen = set()
for p in pngs:
    m = re.fullmatch(r'scenario_(\d{3})\.png', p.name)
    if not m:
        errors.append(f'Invalid PNG name: {p.name}')
        continue
    number = int(m.group(1))
    if not 1 <= number <= 120:
        errors.append(f'PNG outside SCN-001..120: {p.name}')
    if number in seen:
        errors.append(f'Duplicate scenario PNG number: {number:03d}')
    seen.add(number)
    b = p.read_bytes()
    if not b.startswith(b'\x89PNG\r\n\x1a\n'):
        errors.append(f'Invalid PNG signature: {p.name}')
        continue
    if len(b) < 24 or b[12:16] != b'IHDR':
        errors.append(f'Missing PNG IHDR: {p.name}')
        continue
    width, height = struct.unpack('>II', b[16:24])
    if width < 64 or height < 64:
        errors.append(f'PNG too small: {p.name} ({width}x{height})')

if not PREVIEW.exists():
    errors.append('preview/index.html missing; run npm run preview:offline')
else:
    html = PREVIEW.read_text(encoding='utf-8')
    m = re.search(r'<script type="application/json" data-mosaic-data>(.*?)</script>', html, re.S)
    if not m:
        errors.append('Offline preview scenario JSON missing')
    else:
        data = json.loads(m.group(1))
        for i in range(1, 121):
            sid = f'SCN-{i:03d}'
            item = data.get(sid)
            if not item:
                errors.append(f'Offline preview missing {sid}')
                continue
            png_name = f'scenario_{i:03d}.png'
            png_exists = (PNG_DIR / png_name).exists()
            image = item.get('image', '')
            expected = f'../public/scenarios/images/{png_name}' if png_exists else f'./assets/scenarios/{sid}.svg'
            if image != expected:
                errors.append(f'{sid}: preview image is {image!r}, expected {expected!r}')
            resolved = (PREVIEW.parent / image).resolve()
            if not resolved.exists():
                errors.append(f'{sid}: resolved preview image missing: {resolved}')

helper = R / 'src' / 'lib' / 'scenario-image.ts'
usage = R / 'src' / 'components' / 'ScenarioMosaic.astro'
if not helper.exists() or 'existsSync' not in helper.read_text(encoding='utf-8'):
    errors.append('Astro PNG resolver helper missing')
if not usage.exists() or 'resolveScenarioPreviewImage' not in usage.read_text(encoding='utf-8'):
    errors.append('Astro Mosaic does not use PNG resolver')

print(f'Scenario PNGs available: {len(pngs)} / 120')
if pngs:
    print('PNG IDs:', ', '.join(p.stem.replace('scenario_', 'SCN-') for p in pngs))
print(f'SVG fallback scenarios: {120 - len(pngs)}')

if errors:
    print('\nIMAGE VALIDATION FAILED')
    for e in errors:
        print(' -', e)
    sys.exit(1)
print('Scenario image validation passed.')
