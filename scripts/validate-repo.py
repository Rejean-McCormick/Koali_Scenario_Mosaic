from pathlib import Path
import json, sys, re
R=Path(__file__).resolve().parents[1]
errors=[]
js=(R/'src/scripts/mosaic.ts').read_text(encoding='utf-8')
css=(R/'src/styles/mosaic.css').read_text(encoding='utf-8')
component=(R/'src/components/ScenarioMosaic.astro').read_text(encoding='utf-8')
layout=json.loads((R/'src/data/mosaic-layout.json').read_text(encoding='utf-8'))
package=json.loads((R/'package.json').read_text(encoding='utf-8'))
netlify=(R/'netlify.toml').read_text(encoding='utf-8') if (R/'netlify.toml').exists() else ''
meta=json.loads((R/'src/data/scenarios.json').read_text(encoding='utf-8'))
if len(meta)!=120: errors.append('shared scenario metadata count')
for locale in ('en','fr'):
    if len(list((R/f'src/content/scenarios/{locale}').glob('SCN-*.md')))!=120: errors.append(f'{locale} scenario count')
if 'is-related' in js or 'is-related' in css: errors.append('related highlight')
if '.mosaic-cell:hover' in css: errors.append('css hover state')
if '.mosaic-cell:focus-visible' in css: errors.append('independent focus highlight')
if 'selectOnly' not in js: errors.append('single select')
title_rule = re.search(r'\.preview-copy h1\{([^}]*)\}', css)
title_css = title_rule.group(1) if title_rule else ''
if 'line-height:1.08' not in title_css or 'height:6.7rem' not in title_css: errors.append('title line box')
if '-webkit-line-clamp:3' not in title_css: errors.append('title clamp')
if 'data-title-density' not in css or 'titleDensity' not in js: errors.append('adaptive title density')
if 'height:286px' not in css or 'height:clamp(180px,24vh,220px)' not in css: errors.append('one-viewport compact sizing')
if 'territory-legend' not in css or 'MosaicLegend' not in component: errors.append('color legend')
if package.get('scripts',{}).get('build')!='npm run validate && astro build': errors.append('Netlify-safe production build')
if 'preview:offline' in package.get('scripts',{}).get('build',''): errors.append('offline preview leaked into production build')
if 'NODE_VERSION = "24.20.0"' not in netlify or 'publish = "dist"' not in netlify: errors.append('Netlify configuration')
if 'align-items:end' not in css or '.profile-context span{line-height:1.12}' not in css: errors.append('profile context bottom alignment')
if layout['geometry']['rows']!=6 or layout['geometry']['columns']!=20: errors.append('panorama geometry')
if layout['geometry'].get('territories')!=8: errors.append('territory count')

# Responsive preview contract: no horizontal spill and no branded cover crop.
if 'grid-template-columns:minmax(180px,.72fr) minmax(0,1.28fr)' not in css: errors.append('tablet preview grid contract')
if '@media(max-width:720px)' not in css or 'grid-template-columns:1fr' not in css: errors.append('narrow preview stack contract')
if 'img[data-image-state="cover"]{object-fit:contain' not in css: errors.append('cover contain contract')
if 'img[data-image-state="scenario"]{object-fit:cover' not in css: errors.append('scenario image cover contract')
if "dataset.imageState = 'scenario'" not in js: errors.append('scenario image state switch')
cover=(R/'public/mosaic-cover.svg').read_text(encoding='utf-8')
if '<text ' in cover: errors.append('initial cover repeats product text')
if not (R/'src/pages/[lang]/uses/index.astro').exists(): errors.append('localized mosaic route')
if not (R/'src/pages/[lang]/uses/[id].astro').exists(): errors.append('localized scenario route')
if not (R/'preview/en/index.html').exists() or not (R/'preview/fr/index.html').exists(): errors.append('bilingual offline preview')

# Public scenario page contract: same preview shell, supplemental public hexes, no internal Markdown dump.
scenario_route=(R/'src/pages/[lang]/uses/[id].astro').read_text(encoding='utf-8')
preview_component=(R/'src/components/ScenarioPreview.astro').read_text(encoding='utf-8')
detail_component=(R/'src/components/ScenarioInfoMosaic.astro').read_text(encoding='utf-8')
scenario_css=(R/'src/styles/scenario.css').read_text(encoding='utf-8')
if 'ScenarioPreview' not in scenario_route or 'ScenarioInfoMosaic' not in scenario_route: errors.append('scenario selected-state composition')
if 'render(' in scenario_route or '<Content' in scenario_route or 'scenario-body' in scenario_route: errors.append('public scenario still renders internal markdown')
for token in ('detailStartsWith','detailWhatGetsLost','detailKoaliContinuity','detailFlow','detailTransferable'):
    if token not in detail_component: errors.append(f'missing public detail token {token}')
if 'scenario-info-mosaic' not in scenario_css or 'detail-hex--continuity' not in scenario_css: errors.append('public detail honeycomb styling')
if 'scenario = null' not in preview_component or "data-image-state={selected ? 'scenario' : 'cover'}" not in preview_component: errors.append('shared preview selected-state contract')

# Generated public detail pages must not expose editorial/internal governance markers.
internal_markers=('PAT-','SIG-','POS-','COMPOSED','UNVERIFIED','PARTIALLY-VALIDATED','DOCUMENTED','Kristal','KristALL','Konnaxion','Orgo','UCKK')
for locale in ('en','fr'):
    pages=sorted((R/f'preview/{locale}/uses').glob('SCN-*/index.html'))
    if len(pages)!=120: errors.append(f'{locale} offline public scenario page count')
    for page in pages:
        html=page.read_text(encoding='utf-8')
        for marker in internal_markers:
            if marker in html: errors.append(f'internal marker leaked into {locale}/{page.parent.name}: {marker}')
        if 'scenario-info-mosaic' not in html: errors.append(f'{locale}/{page.parent.name} missing public detail honeycomb')

print('120 shared scenarios; 240 localized documents; 20 × 6 panoramic honeycomb; bilingual EN/FR routes')
if errors:
    print(errors); sys.exit(1)
