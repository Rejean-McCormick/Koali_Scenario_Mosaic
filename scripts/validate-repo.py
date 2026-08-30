from pathlib import Path
import json, sys

R = Path(__file__).resolve().parents[1]
js = (R / 'src/scripts/mosaic.ts').read_text()
css = (R / 'src/styles/mosaic.css').read_text()
component = (R / 'src/components/ScenarioMosaic.astro').read_text()
legend = (R / 'src/components/MosaicLegend.astro').read_text()
layout = json.loads((R / 'src/data/mosaic-layout.json').read_text())
package = json.loads((R / 'package.json').read_text())
netlify = (R / 'netlify.toml').read_text() if (R / 'netlify.toml').exists() else ''
errors = []

if len(list((R / 'src/content/scenarios').glob('SCN-*.md'))) != 120:
    errors.append('scenario count')
if 'is-related' in js or 'is-related' in css:
    errors.append('related highlight')
if '.mosaic-cell:hover' in css:
    errors.append('css hover state')
if '.mosaic-cell:focus-visible' in css:
    errors.append('independent focus highlight')
if 'selectOnly' not in js:
    errors.append('single select')

if 'line-height:1.12' not in css or 'block-size:2.25lh' not in css:
    errors.append('title line box')
if '-webkit-line-clamp:2' not in css:
    errors.append('title clamp')
if 'height:286px' not in css or 'height:clamp(180px,24vh,220px)' not in css:
    errors.append('one-viewport compact sizing')
if 'territory-legend' not in css or 'MosaicLegend' not in component:
    errors.append('color legend')
if package.get('scripts', {}).get('build') != 'npm run validate && astro build':
    errors.append('Netlify-safe production build')
if 'npm run preview:offline' in package.get('scripts', {}).get('build', ''):
    errors.append('offline preview leaked into production build')
if 'NODE_VERSION = "24.20.0"' not in netlify or 'publish = "dist"' not in netlify:
    errors.append('Netlify configuration')
if 'Scenario color legend' not in legend:
    errors.append('legend accessibility label')

geometry = layout['geometry']
if geometry['rows'] != 6 or geometry['columns'] != 20:
    errors.append('panorama geometry')
if geometry.get('territories') != 8:
    errors.append('territory count')

print('120 scenarios; 20 × 6 panoramic honeycomb; 8 category territories; compact preview; color legend; single active cell')
if errors:
    print(errors)
    sys.exit(1)
