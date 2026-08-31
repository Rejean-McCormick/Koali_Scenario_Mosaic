from pathlib import Path
import json, re, html, shutil, math, yaml

R = Path(__file__).resolve().parents[1]
O = R / 'preview'
if O.exists(): shutil.rmtree(O)
(O / 'assets/scenarios').mkdir(parents=True)
(O / 'assets/brand').mkdir(parents=True)

metadata = json.loads((R / 'src/data/scenarios.json').read_text(encoding='utf-8'))
fr_tags = json.loads((R / 'src/i18n/fr-tags.json').read_text(encoding='utf-8'))
layout = json.loads((R / 'src/data/mosaic-layout.json').read_text(encoding='utf-8'))

for p in (R / 'public/scenarios/placeholders').glob('*.svg'):
    shutil.copy2(p, O / 'assets/scenarios' / p.name)
shutil.copy2(R / 'public/mosaic-cover.svg', O / 'assets/mosaic-cover.svg')
shutil.copy2(R / 'public/mosaic-cover-fr.svg', O / 'assets/mosaic-cover-fr.svg')
shutil.copy2(R / 'public/brand/koali-mark.svg', O / 'assets/brand/koali-mark.svg')
(O / 'assets/styles.css').write_text(
    (R / 'src/styles/global.css').read_text(encoding='utf-8') +
    (R / 'src/styles/mosaic.css').read_text(encoding='utf-8') +
    (R / 'src/styles/scenario.css').read_text(encoding='utf-8'), encoding='utf-8')

groups = {
    'understand':['find','understand','verify'],
    'learn':['learn','teach-share'],
    'create':['collaborate','create'],
    'decide':['deliberate','choose'],
    'act':['organize','act'],
    'respond':['respond','coordinate'],
    'remember':['remember','disseminate'],
}

UI = {
'en': {
  'product':'Scenario Mosaic','scenarios':'scenarios','explore':'Explore 120 ways to use Koali',
  'hover':'Hover a cell to discover a concrete situation and its public scenario profile.',
  'hover_tag':'Hover or focus a cell','read':'Read the scenario','profile':'Scenario profile',
  'explore_mosaic':'Explore the Mosaic','motion':'Typical motion','inspect':'Hover a cell to inspect it.',
  'what':'What happens here','scale':'Scale','context':'Context','conditions':'Special conditions','none':'None highlighted',
  'search':'Search the mosaic…','surprise':'Surprise me','reset':'Reset','legend':'Scenario color legend',
  'hint':'Each color is a scenario family. Hover or focus one hexagon to inspect it above.',
  'back':'← Back to mosaic','all':'All scenarios',
  'activities':{'understand':'Understand','learn':'Learn & share','create':'Create together','decide':'Decide','act':'Organize & act','respond':'Respond','remember':'Remember & share'},
  'involved':'involved','notCentral':'not central','lang':'Language',
},
'fr': {
  'product':'Mosaïque de scénarios','scenarios':'scénarios','explore':'Explorez 120 façons d’utiliser Koali',
  'hover':'Survolez une cellule pour découvrir une situation concrète et son profil public.',
  'hover_tag':'Survolez ou ciblez une cellule','read':'Lire le scénario','profile':'Profil du scénario',
  'explore_mosaic':'Explorer la mosaïque','motion':'Dynamique typique','inspect':'Survolez une cellule pour l’examiner.',
  'what':'Ce qui se passe ici','scale':'Échelle','context':'Contexte','conditions':'Conditions particulières','none':'Aucune mise en évidence',
  'search':'Rechercher dans la mosaïque…','surprise':'Au hasard','reset':'Réinitialiser','legend':'Légende des couleurs des scénarios',
  'hint':'Chaque couleur représente une famille de scénarios. Survolez ou ciblez un hexagone pour l’examiner ci-dessus.',
  'back':'← Retour à la mosaïque','all':'Tous les scénarios',
  'activities':{'understand':'Comprendre','learn':'Apprendre & transmettre','create':'Créer ensemble','decide':'Décider','act':'Organiser & agir','respond':'Répondre','remember':'Se souvenir & partager'},
  'involved':'impliqué','notCentral':'non central','lang':'Langue',
}}

def parse_localized(locale):
    out=[]
    for p in sorted((R / 'src/content/scenarios' / locale).glob('SCN-*.md')):
        text=p.read_text(encoding='utf-8'); _,fm,body=text.split('---',2)
        local=yaml.safe_load(fm)
        common=metadata[local['id']]
        out.append({**common, **local, 'body':body.strip()})
    return out

def humanize(locale, value):
    if locale == 'fr': return fr_tags.get(value, value.replace('-',' ').capitalize())
    return re.sub(r'\b\w', lambda m:m.group().upper(), re.sub(r'[-_]+',' ',value))

def palette_label(locale,value):
    if locale=='fr': return fr_tags.get(value,value)
    return value.replace('-',' ')

def preview_image(x, locale):
    number=x['id'].split('-')[1]
    png=R/'public/scenarios/images'/f'scenario_{number}.png'
    # index.html is preview/<locale>/index.html
    if png.exists(): return f'../../public/scenarios/images/{png.name}'
    return '../assets/scenarios/'+Path(x['preview_image']).name

def inline_md(text):
    text=html.escape(text)
    text=re.sub(r'`([^`]+)`',r'<code>\1</code>',text)
    text=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',text)
    return text

def markdown_to_html(md):
    lines=md.splitlines(); out=[]; para=[]; ul=False
    def flush_para():
        nonlocal para
        if para:
            out.append('<p>'+inline_md(' '.join(x.strip() for x in para))+'</p>'); para=[]
    def close_ul():
        nonlocal ul
        if ul: out.append('</ul>'); ul=False
    for line in lines:
        if not line.strip(): flush_para(); close_ul(); continue
        if line.startswith('# '): flush_para(); close_ul(); out.append('<h1>'+inline_md(line[2:].strip())+'</h1>'); continue
        if line.startswith('## '): flush_para(); close_ul(); out.append('<h2>'+inline_md(line[3:].strip())+'</h2>'); continue
        if line.startswith('> '): flush_para(); close_ul(); out.append('<blockquote>'+inline_md(line[2:].strip())+'</blockquote>'); continue
        if line.startswith('- '):
            flush_para()
            if not ul: out.append('<ul>'); ul=True
            out.append('<li>'+inline_md(line[2:].strip())+'</li>'); continue
        para.append(line)
    flush_para(); close_ul(); return '\n'.join(out)

# Shared JS reads localized labels from data-mosaic-i18n.
app_js = r'''const root=document.querySelector('[data-mosaic-root]');if(root){const data=JSON.parse(root.querySelector('[data-mosaic-data]').textContent||'{}');const tr=JSON.parse(root.querySelector('[data-mosaic-i18n]').textContent||'{}');const cells=[...root.querySelectorAll('[data-scenario-id]')];const search=root.querySelector('[data-mosaic-search]');const count=root.querySelector('[data-mosaic-result-count]');const setText=(q,v)=>{const e=root.querySelector(q);if(e){e.textContent=v;e.title=v}};const compact=(a,empty='—',limit=3)=>!a||!a.length?empty:(a.length>limit?`${a.slice(0,limit).join(' · ')} +${a.length-limit}`:a.join(' · '));function selectOnly(id){cells.forEach(c=>c.classList.toggle('is-active',c.dataset.scenarioId===id))}function show(id){const s=data[id];if(!s)return;selectOnly(id);setText('[data-preview-id]',s.id);setText('[data-preview-category]',s.category);setText('[data-preview-title]',s.title);setText('[data-preview-summary]',s.summary);setText('[data-preview-category-label]',s.category);setText('[data-preview-pattern]',s.pattern);setText('[data-preview-scales]',compact(s.scales));setText('[data-preview-context]',compact(s.contexts));setText('[data-preview-properties]',compact(s.properties,tr.noneHighlighted,2));const p=root.querySelector('[data-preview-profile]');if(p)p.dataset.category=s.categoryId;const img=root.querySelector('[data-preview-image]');if(img){img.src=s.image;img.alt=s.imageAlt}const link=root.querySelector('[data-preview-link]');if(link){link.href=s.href;link.hidden=false}const pal=root.querySelector('[data-preview-palette]');if(pal)pal.innerHTML=s.palette.slice(0,5).map(x=>`<span class="tag">${x}</span>`).join('');root.querySelectorAll('[data-activity]').forEach(el=>{const k=el.dataset.activity;const on=!!s.activities[k];el.classList.toggle('is-active',on);el.setAttribute('aria-label',`${el.textContent.trim()}: ${on?tr.involved:tr.notCentral}`)})}cells.forEach(c=>{const id=c.dataset.scenarioId;c.addEventListener('pointerenter',()=>show(id));c.addEventListener('focus',()=>show(id))});search.addEventListener('input',()=>{const q=search.value.trim().toLowerCase();let n=0;cells.forEach(c=>{const hit=!q||data[c.dataset.scenarioId].search.includes(q);c.classList.toggle('is-filtered-out',!hit);if(hit)n++});count.textContent=`${n} ${n===1?tr.scenarioSingular:tr.scenarios}`});root.querySelector('[data-mosaic-surprise]').addEventListener('click',()=>{const v=cells.filter(c=>!c.classList.contains('is-filtered-out'));if(v.length){const c=v[Math.floor(Math.random()*v.length)];show(c.dataset.scenarioId);c.focus()}});root.querySelector('[data-mosaic-reset]').addEventListener('click',()=>{search.value='';cells.forEach(c=>c.classList.remove('is-filtered-out','is-active'));count.textContent=`${cells.length} ${tr.scenarios}`})}'''
(O/'assets/app.js').write_text(app_js,encoding='utf-8')

for locale in ('en','fr'):
    s=UI[locale]; other='fr' if locale=='en' else 'en'
    scenarios=parse_localized(locale); by={x['id']:x for x in scenarios}
    base=O/locale; (base/'uses').mkdir(parents=True,exist_ok=True)
    data={}
    for x in scenarios:
        contexts=list(dict.fromkeys([*x.get('settings',[]),*x.get('domains',[])]))[:3]
        data[x['id']]={
          'id':x['id'],'title':x['title'],'category':x['category_label'],'categoryId':x['primary_category'],'pattern':x['pattern_label'],'summary':x['preview_summary'],
          'palette':[palette_label(locale,v) for v in x['palette']],
          'activities':{k:any(v in x['palette'] for v in vals) for k,vals in groups.items()},
          'scales':[humanize(locale,v) for v in x.get('scales',[])],
          'contexts':[humanize(locale,v) for v in contexts],
          'properties':[humanize(locale,v) for v in x.get('properties',[])],
          'image':preview_image(x,locale),'imageAlt':x['preview_image_alt'],'href':f'./uses/{x["id"]}/index.html',
          'search':' '.join([x['title'],x['category_label'],x['pattern_label'],*x['palette'],*x.get('domains',[]),*x.get('settings',[]),*[humanize(locale,v) for v in x.get('domains',[])]]).lower()}
    cells=[]
    for sid,slotid in layout['assignments'].items():
        p=layout['slots'][slotid];z=p['size']
        pts=' '.join(f'{p["x"]+z*math.cos(math.pi/3*i-math.pi/6):.2f},{p["y"]+z*math.sin(math.pi/3*i-math.pi/6):.2f}' for i in range(6))
        cells.append(f'<a class="mosaic-cell {by[sid]["primary_category"].lower()}" href="./uses/{sid}/index.html" data-scenario-id="{sid}" tabindex="0" aria-label="{html.escape(sid+": "+by[sid]["title"])}"><polygon points="{pts}"/></a>')
    category_labels=[]; seen=set()
    for x in scenarios:
        cid=x['primary_category']
        if cid not in seen: seen.add(cid);category_labels.append((cid,x['category_label']))
    category_labels.sort()
    legend=''.join(f'<span class="legend-item {cid.lower()}"><i aria-hidden="true"></i><span>{html.escape(label)}</span></span>' for cid,label in category_labels)
    acts=''.join(f'<span data-activity="{key}"><i></i>{html.escape(label)}</span>' for key,label in s['activities'].items())
    profile=f'''<aside class="preview-profile" data-preview-profile><div class="profile-heading"><span class="profile-title">{html.escape(s['profile'])}</span><span class="profile-category"><span class="category-swatch"></span><strong data-preview-category-label>{html.escape(s['explore_mosaic'])}</strong></span></div><div class="profile-pattern"><span>{html.escape(s['motion'])}</span><small data-preview-pattern>{html.escape(s['inspect'])}</small></div><div class="profile-actions"><span class="profile-section-label">{html.escape(s['what'])}</span><div class="activity-signature">{acts}</div></div><div class="profile-context"><div><span>{html.escape(s['scale'])}</span><strong data-preview-scales>—</strong></div><div><span>{html.escape(s['context'])}</span><strong data-preview-context>—</strong></div><div><span>{html.escape(s['conditions'])}</span><strong data-preview-properties>{html.escape(s['none'])}</strong></div></div></aside>'''
    cover = '../assets/mosaic-cover-fr.svg' if locale == 'fr' else '../assets/mosaic-cover.svg'
    switch=f'<nav class="language-switcher" aria-label="{html.escape(s["lang"])}"><a class="{"active" if locale=="en" else ""}" href="../en/index.html">EN</a><span>/</span><a class="{"active" if locale=="fr" else ""}" href="../fr/index.html">FR</a></nav>'
    index=f'''<!doctype html><html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><meta name="theme-color" content="#1e6864"><link rel="icon" href="../assets/brand/koali-mark.svg"><link rel="stylesheet" href="../assets/styles.css"><title>{'Mosaïque de scénarios Koali' if locale=='fr' else 'Koali Scenario Mosaic'}</title></head><body><header class="site-header"><a class="brand" href="./index.html"><img class="brand-mark" src="../assets/brand/koali-mark.svg" alt=""><span class="brand-copy"><span class="brand-product"><strong>Koali</strong><span>{html.escape(s['product'])}</span></span><small>the Sociotechnical Operating System</small></span></a>{switch}</header><main><div class="mosaic-experience" data-mosaic-root><section class="scenario-preview"><div class="preview-image-shell"><img data-preview-image src="{cover}"></div><div class="preview-copy"><p class="preview-eyebrow"><span data-preview-id>{'Mosaïque de scénarios Koali' if locale=='fr' else 'Koali Scenario Mosaic'}</span> · <span data-preview-category>120 {s['scenarios']}</span></p><h1 data-preview-title>{html.escape(s['explore'])}</h1><p class="preview-summary" data-preview-summary>{html.escape(s['hover'])}</p><div class="preview-tags" data-preview-palette><span class="tag">{html.escape(s['hover_tag'])}</span></div><a class="preview-cta" data-preview-link hidden>{html.escape(s['read'])} →</a></div>{profile}</section><div class="mosaic-controls"><label class="search-box"><input data-mosaic-search placeholder="{html.escape(s['search'])}"></label><button class="ghost-button" data-mosaic-surprise>{html.escape(s['surprise'])}</button><button class="ghost-button" data-mosaic-reset>{html.escape(s['reset'])}</button><output data-mosaic-result-count>120 {s['scenarios']}</output></div><div class="territory-legend" aria-label="{html.escape(s['legend'])}">{legend}</div><div class="mosaic-stage"><svg class="mosaic" viewBox="{' '.join(map(str,layout['viewBox']))}">{''.join(cells)}</svg><p class="mosaic-hint">{html.escape(s['hint'])}</p></div><script type="application/json" data-mosaic-data>{json.dumps(data,ensure_ascii=False).replace('</','<\\/')}</script><script type="application/json" data-mosaic-i18n>{json.dumps({'noneHighlighted':s['none'],'scenarios':s['scenarios'],'scenarioSingular':'scénario' if locale=='fr' else 'scenario','involved':s['involved'],'notCentral':s['notCentral']},ensure_ascii=False)}</script></div></main><script src="../assets/app.js"></script></body></html>'''
    (base/'index.html').write_text(index,encoding='utf-8')

    list_items=''.join(f'<p><a href="./{x["id"]}/index.html">{x["id"]} — {html.escape(x["title"])}</a></p>' for x in scenarios)
    (base/'uses/index.html').write_text(f'<!doctype html><html lang="{locale}"><head><meta charset="utf-8"><link rel="stylesheet" href="../../assets/styles.css"><title>{html.escape(s["all"])}</title></head><body><main><section class="scenario-shell"><a class="back-link" href="../index.html">{html.escape(s["back"])}</a><h1>{html.escape(s["all"])}</h1>{list_items}</section></main></body></html>',encoding='utf-8')

    for x in scenarios:
        d=base/'uses'/x['id']; d.mkdir(parents=True,exist_ok=True)
        alt=f'../../../{other}/uses/{x["id"]}/index.html'
        switch_detail=f'<nav class="language-switcher"><a class="{"active" if locale=="en" else ""}" href="{"index.html" if locale=="en" else alt}">EN</a><span>/</span><a class="{"active" if locale=="fr" else ""}" href="{"index.html" if locale=="fr" else alt}">FR</a></nav>'
        page=f'''<!doctype html><html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><link rel="stylesheet" href="../../../assets/styles.css"><title>{html.escape(x['title'])}</title></head><body><header class="site-header"><a class="brand" href="../../index.html"><img class="brand-mark" src="../../../assets/brand/koali-mark.svg" alt=""><span class="brand-copy"><span class="brand-product"><strong>Koali</strong><span>{html.escape(s['product'])}</span></span><small>the Sociotechnical Operating System</small></span></a>{switch_detail}</header><main><article class="scenario-shell"><a class="back-link" href="../../index.html">{html.escape(s['back'])}</a><h1>{html.escape(x['title'])}</h1><p class="scenario-dek">{html.escape(x['preview_summary'])}</p><div class="scenario-body">{markdown_to_html(x['body'])}</div></article></main></body></html>'''
        (d/'index.html').write_text(page,encoding='utf-8')

# Root offline language redirect. This remains file:// safe.
(O/'index.html').write_text('''<!doctype html><html><head><meta charset="utf-8"><title>Koali Scenario Mosaic</title><script>const l=(navigator.languages||[navigator.language||'en']).some(x=>String(x).toLowerCase().startsWith('fr'))?'fr':'en';location.replace('./'+l+'/index.html');</script></head><body><p><a href="./en/index.html">English</a> · <a href="./fr/index.html">Français</a></p></body></html>''',encoding='utf-8')
print('offline bilingual preview built: 120 EN + 120 FR scenarios')
