from pathlib import Path
import json, re, html, shutil, math, yaml
R=Path(__file__).resolve().parents[1]
O=R/'preview'
if O.exists(): shutil.rmtree(O)
(O/'assets/scenarios').mkdir(parents=True)
(O/'uses').mkdir(parents=True)
def parse(p):
    t=p.read_text(encoding='utf-8');_,fm,b=t.split('---',2);d=yaml.safe_load(fm);d['body']=b;return d
scenarios=[parse(p) for p in sorted((R/'src/content/scenarios').glob('SCN-*.md'))]
by={x['id']:x for x in scenarios}
layout=json.loads((R/'src/data/mosaic-layout.json').read_text())
for p in (R/'public/scenarios/placeholders').glob('*.svg'): shutil.copy2(p,O/'assets/scenarios'/p.name)
shutil.copy2(R/'public/mosaic-cover.svg',O/'assets/mosaic-cover.svg')
(O/'assets/styles.css').write_text((R/'src/styles/global.css').read_text()+(R/'src/styles/mosaic.css').read_text()+(R/'src/styles/scenario.css').read_text())
groups={'understand':['find','understand','verify'],'learn':['learn','teach-share'],'create':['collaborate','create'],'decide':['deliberate','choose'],'act':['organize','act'],'respond':['respond','coordinate'],'remember':['remember','disseminate']}
def hum(v): return re.sub(r'\b\w',lambda m:m.group().upper(),re.sub(r'[-_]+',' ',v))
def preview_image(x):
    number=x['id'].split('-')[1]
    png=R/'public/scenarios/images'/f'scenario_{number}.png'
    if png.exists():
        return f'../public/scenarios/images/{png.name}'
    return './assets/scenarios/'+Path(x['preview_image']).name
data={}
for x in scenarios:
    contexts=list(dict.fromkeys([*x.get('settings',[]),*x.get('domains',[])]))[:3]
    data[x['id']]={'id':x['id'],'title':x['title'],'category':x['category_label'],'categoryId':x['primary_category'],'pattern':x['pattern_label'],'summary':x['preview_summary'],'palette':x['palette'],'activities':{k:any(v in x['palette'] for v in vals) for k,vals in groups.items()},'scales':[hum(v) for v in x.get('scales',[])],'contexts':[hum(v) for v in contexts],'properties':[hum(v) for v in x.get('properties',[])],'image':preview_image(x),'imageAlt':x['preview_image_alt'],'href':f'./uses/{x["id"]}/index.html','search':' '.join([x['title'],x['category_label'],x['pattern_label'],*x['palette'],*x.get('domains',[]),*x.get('settings',[])]).lower()}
cells=[]
for sid,slotid in layout['assignments'].items():
    p=layout['slots'][slotid];z=p['size']
    pts=' '.join(f'{p["x"]+z*math.cos(math.pi/3*i-math.pi/6):.2f},{p["y"]+z*math.sin(math.pi/3*i-math.pi/6):.2f}' for i in range(6))
    cells.append(f'<a class="mosaic-cell {by[sid]["primary_category"].lower()}" href="./uses/{sid}/index.html" data-scenario-id="{sid}"><polygon points="{pts}"/></a>')
category_labels = []
seen_categories = set()
for x in scenarios:
    cid = x['primary_category']
    if cid not in seen_categories:
        seen_categories.add(cid)
        category_labels.append((cid, x['category_label']))
category_labels.sort(key=lambda item: item[0])
legend = ''.join(
    f'<span class="legend-item {cid.lower()}"><i aria-hidden="true"></i><span>{html.escape(label)}</span></span>'
    for cid, label in category_labels
)
profile='''<aside class="preview-profile" data-preview-profile><div class="profile-heading"><span class="profile-title">Scenario profile</span><span class="profile-category"><span class="category-swatch"></span><strong data-preview-category-label>Explore the Mosaic</strong></span></div><div class="profile-pattern"><span>Typical motion</span><small data-preview-pattern>Hover a cell to inspect it.</small></div><div class="profile-actions"><span class="profile-section-label">What happens here</span><div class="activity-signature"><span data-activity="understand"><i></i>Understand</span><span data-activity="learn"><i></i>Learn & share</span><span data-activity="create"><i></i>Create together</span><span data-activity="decide"><i></i>Decide</span><span data-activity="act"><i></i>Organize & act</span><span data-activity="respond"><i></i>Respond</span><span data-activity="remember"><i></i>Remember & share</span></div></div><div class="profile-context"><div><span>Scale</span><strong data-preview-scales>—</strong></div><div><span>Context</span><strong data-preview-context>—</strong></div><div><span>Special conditions</span><strong data-preview-properties>None highlighted</strong></div></div></aside>'''
index=f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><link rel="stylesheet" href="./assets/styles.css"><title>Koali Scenario Mosaic</title></head><body><header class="site-header"><a class="brand" href="./index.html">⬡ KOALI <strong>SCENARIO MOSAIC</strong></a></header><main><div class="mosaic-experience" data-mosaic-root><section class="scenario-preview"><div class="preview-image-shell"><img data-preview-image src="./assets/mosaic-cover.svg"></div><div class="preview-copy"><p class="preview-eyebrow"><span data-preview-id>KOALI SCENARIO MOSAIC</span> · <span data-preview-category>120 scenarios</span></p><h1 data-preview-title>Explore 120 ways to use Koali</h1><p class="preview-summary" data-preview-summary>Hover a cell to discover a concrete situation and its public scenario profile.</p><div class="preview-tags" data-preview-palette><span class="tag">Hover or focus a cell</span></div><a class="preview-cta" data-preview-link hidden>Read the scenario →</a></div>{profile}</section><div class="mosaic-controls"><label class="search-box"><input data-mosaic-search placeholder="Search the mosaic…"></label><button class="ghost-button" data-mosaic-surprise>Surprise me</button><button class="ghost-button" data-mosaic-reset>Reset</button><output data-mosaic-result-count>120 scenarios</output></div><div class="territory-legend" aria-label="Scenario color legend">{legend}</div><div class="mosaic-stage"><svg class="mosaic" viewBox="{' '.join(map(str,layout['viewBox']))}">{''.join(cells)}</svg><p class="mosaic-hint">Each color is a scenario family. Hover or focus one hexagon to inspect it above.</p></div><script type="application/json" data-mosaic-data>{json.dumps(data).replace('</','<\\/')}</script></div></main><script src="./assets/app.js"></script></body></html>'''
(O/'index.html').write_text(index)
js='''const root=document.querySelector('[data-mosaic-root]');if(root){const data=JSON.parse(root.querySelector('[data-mosaic-data]').textContent||'{}');const cells=[...root.querySelectorAll('[data-scenario-id]')];const search=root.querySelector('[data-mosaic-search]');const count=root.querySelector('[data-mosaic-result-count]');const labels={understand:'Understand',learn:'Learn & share',create:'Create together',decide:'Decide',act:'Organize & act',respond:'Respond',remember:'Remember & share'};const setText=(q,v)=>{const e=root.querySelector(q);if(e){e.textContent=v;e.title=v}};const compact=(a,empty='—',limit=3)=>!a||!a.length?empty:(a.length>limit?`${a.slice(0,limit).join(' · ')} +${a.length-limit}`:a.join(' · '));function selectOnly(id){cells.forEach(c=>c.classList.toggle('is-active',c.dataset.scenarioId===id))}function show(id){const s=data[id];if(!s)return;selectOnly(id);setText('[data-preview-id]',s.id);setText('[data-preview-category]',s.category);setText('[data-preview-title]',s.title);setText('[data-preview-summary]',s.summary);setText('[data-preview-category-label]',s.category);setText('[data-preview-pattern]',s.pattern);setText('[data-preview-scales]',compact(s.scales));setText('[data-preview-context]',compact(s.contexts));setText('[data-preview-properties]',compact(s.properties,'None highlighted',2));const p=root.querySelector('[data-preview-profile]');if(p)p.dataset.category=s.categoryId;const img=root.querySelector('[data-preview-image]');if(img){img.src=s.image;img.alt=s.imageAlt}const link=root.querySelector('[data-preview-link]');if(link){link.href=s.href;link.hidden=false}const pal=root.querySelector('[data-preview-palette]');if(pal)pal.innerHTML=s.palette.slice(0,5).map(x=>`<span class="tag">${x.replace(/[-_]+/g,' ')}</span>`).join('');Object.entries(labels).forEach(([k,label])=>{const el=root.querySelector(`[data-activity="${k}"]`);if(el){const on=!!s.activities[k];el.classList.toggle('is-active',on);el.setAttribute('aria-label',`${label}: ${on?'involved':'not central'}`)}})}cells.forEach(c=>{const id=c.dataset.scenarioId;c.addEventListener('pointerenter',()=>show(id));c.addEventListener('focus',()=>show(id))});search.addEventListener('input',()=>{const q=search.value.trim().toLowerCase();let n=0;cells.forEach(c=>{const hit=!q||data[c.dataset.scenarioId].search.includes(q);c.classList.toggle('is-filtered-out',!hit);if(hit)n++});count.textContent=`${n} scenario${n===1?'':'s'}`});root.querySelector('[data-mosaic-surprise]').addEventListener('click',()=>{const v=cells.filter(c=>!c.classList.contains('is-filtered-out'));if(v.length){const c=v[Math.floor(Math.random()*v.length)];show(c.dataset.scenarioId);c.focus()}});root.querySelector('[data-mosaic-reset]').addEventListener('click',()=>{search.value='';cells.forEach(c=>c.classList.remove('is-filtered-out','is-active'));count.textContent=`${cells.length} scenarios`})}'''
(O/'assets/app.js').write_text(js)
for x in scenarios:
    d=O/'uses'/x['id'];d.mkdir()
    (d/'index.html').write_text(f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="../../assets/styles.css"><title>{html.escape(x["title"])}</title></head><body><main><article class="scenario-shell"><a class="back-link" href="../../index.html">← Back to mosaic</a><h1>{html.escape(x["title"])}</h1><p class="scenario-dek">{html.escape(x["preview_summary"])}</p><div class="scenario-body"><pre style="white-space:pre-wrap">{html.escape(x["body"])}</pre></div></article></main></body></html>')
print('offline preview built:',len(scenarios),'scenarios')
