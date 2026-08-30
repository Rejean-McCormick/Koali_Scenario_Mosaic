from pathlib import Path
import ast, html, json, math, re, shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'preview'
if OUT.exists():
    shutil.rmtree(OUT)
(OUT / 'assets' / 'scenarios').mkdir(parents=True)
(OUT / 'uses').mkdir(parents=True)

layout = json.loads((ROOT / 'src/data/mosaic-layout.json').read_text(encoding='utf-8'))

def scalar(value: str):
    value = value.strip()
    if not value:
        return ''
    if value[0:1] in {'"', "'", '[', '{'}:
        try:
            return ast.literal_eval(value)
        except Exception:
            return value.strip('"\'')
    if value in {'true', 'True'}:
        return True
    if value in {'false', 'False'}:
        return False
    if value.isdigit():
        return int(value)
    return value

def parse_frontmatter(text: str):
    lines = text.splitlines()
    if not lines or lines[0].strip() != '---':
        raise ValueError('Missing YAML frontmatter')
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == '---'), None)
    if end is None:
        raise ValueError('Unclosed YAML frontmatter')
    fm = lines[1:end]
    body = '\n'.join(lines[end+1:]).strip()
    data = {}
    i = 0
    while i < len(fm):
        line = fm[i]
        if not line.strip() or line.startswith(' '):
            i += 1; continue
        if ':' not in line:
            i += 1; continue
        key, rest = line.split(':', 1)
        key, rest = key.strip(), rest.strip()
        if rest:
            data[key] = scalar(rest)
            i += 1; continue
        # block mapping or list
        j = i + 1
        block = []
        while j < len(fm) and (fm[j].startswith(' ') or fm[j].lstrip().startswith('- ') or not fm[j].strip()):
            if fm[j].strip():
                block.append(fm[j])
            j += 1
        if block and all(x.lstrip().startswith('- ') for x in block):
            data[key] = [scalar(x.lstrip()[2:]) for x in block]
        else:
            obj = {}
            for x in block:
                s = x.strip()
                if ':' in s:
                    k, v = s.split(':', 1)
                    vv = scalar(v)
                    if isinstance(vv, str) and vv.isdigit(): vv = int(vv)
                    obj[k.strip()] = vv
            data[key] = obj
        i = j
    return data, body

def inline_md(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    return s

def render_markdown(md: str) -> str:
    lines = md.splitlines()
    out, para, list_items = [], [], []
    in_code = False; code = []
    def flush_para():
        nonlocal para
        if para:
            out.append('<p>' + inline_md(' '.join(x.strip() for x in para)) + '</p>'); para=[]
    def flush_list():
        nonlocal list_items
        if list_items:
            out.append('<ul>' + ''.join('<li>'+inline_md(x)+'</li>' for x in list_items) + '</ul>'); list_items=[]
    for line in lines:
        if line.strip().startswith('```'):
            flush_para(); flush_list()
            if in_code:
                out.append('<pre><code>'+html.escape('\n'.join(code))+'</code></pre>'); code=[]; in_code=False
            else:
                in_code=True
            continue
        if in_code:
            code.append(line); continue
        if not line.strip():
            flush_para(); flush_list(); continue
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            flush_para(); flush_list(); level=len(m.group(1)); out.append(f'<h{level}>'+inline_md(m.group(2))+f'</h{level}>'); continue
        if line.startswith('> '):
            flush_para(); flush_list(); out.append('<blockquote>'+inline_md(line[2:])+'</blockquote>'); continue
        if re.match(r'^[-*]\s+', line):
            flush_para(); list_items.append(re.sub(r'^[-*]\s+','',line)); continue
        para.append(line)
    flush_para(); flush_list()
    if in_code: out.append('<pre><code>'+html.escape('\n'.join(code))+'</code></pre>')
    return '\n'.join(out)

scenarios = []
for p in sorted((ROOT / 'src/content/scenarios').glob('SCN-*.md')):
    data, body = parse_frontmatter(p.read_text(encoding='utf-8'))
    data['body_html'] = render_markdown(body)
    scenarios.append(data)
byid = {s['id']: s for s in scenarios}

for p in (ROOT / 'public/scenarios/placeholders').glob('*.svg'):
    shutil.copy2(p, OUT / 'assets/scenarios' / p.name)
shutil.copy2(ROOT / 'public/mosaic-cover.svg', OUT / 'assets/mosaic-cover.svg')
css = '\n'.join((ROOT / 'src/styles' / f).read_text(encoding='utf-8') for f in ['global.css','mosaic.css','scenario.css'])
(OUT / 'assets/styles.css').write_text(css, encoding='utf-8')

catcss = {f'CAT-0{i}': f'cat-0{i}' for i in range(1,9)}
svg_cells = []
for sid, slotid in layout['assignments'].items():
    s, sl = byid[sid], layout['slots'][slotid]
    x, y, size = sl['x'], sl['y'], sl['size']
    pts = ' '.join(f'{x+size*math.cos(math.pi/3*i-math.pi/6):.2f},{y+size*math.sin(math.pi/3*i-math.pi/6):.2f}' for i in range(6))
    title = html.escape(f'{sid}: {s["title"]}')
    svg_cells.append(f'<a class="mosaic-cell {catcss[s["primary_category"]]}" href="./uses/{sid}/index.html" data-scenario-id="{sid}" aria-label="{title}"><polygon points="{pts}"/><title>{title}</title></a>')

PUBLIC_ACTIVITY_GROUPS = {
    'understand': ['find', 'understand', 'verify'],
    'learn': ['learn', 'teach-share'],
    'create': ['collaborate', 'create'],
    'decide': ['deliberate', 'choose'],
    'act': ['organize', 'act'],
    'respond': ['respond', 'coordinate'],
    'remember': ['remember', 'disseminate'],
}

def humanize(value):
    label = re.sub(r'[-_]+', ' ', str(value)).strip()
    return ' '.join(word[:1].upper() + word[1:] for word in label.split())

def public_activities(palette):
    active = set(palette or [])
    return {key: any(tag in active for tag in tags) for key, tags in PUBLIC_ACTIVITY_GROUPS.items()}

preview_data = {}
for s in scenarios:
    preview_data[s['id']] = {
        'id': s['id'],
        'title': s['title'],
        'category': s['category_label'],
        'categoryId': s['primary_category'],
        'pattern': s['pattern_label'],
        'summary': s['preview_summary'],
        'palette': s.get('palette', []),
        'activities': public_activities(s.get('palette', [])),
        'scales': [humanize(v) for v in s.get('scales', [])],
        'settings': [humanize(v) for v in s.get('settings', [])],
        'contexts': list(dict.fromkeys([humanize(v) for v in [*s.get('settings', []), *s.get('domains', [])]]))[:3],
        'properties': [humanize(v) for v in s.get('properties', [])],
        'domains': [humanize(v) for v in s.get('domains', [])],
        'related': s.get('related', []),
        'image': './assets/scenarios/' + Path(s['preview_image']).name,
        'imageAlt': s['preview_image_alt'],
        'href': f'./uses/{s["id"]}/index.html',
        'search': ' '.join([
            s['title'], s['category_label'], s['pattern_label'],
            *s.get('palette', []), *s.get('properties', []), *s.get('badges', []),
            *s.get('settings', []), *s.get('scales', []), *s.get('domains', []),
        ]).lower(),
    }
json_data = json.dumps(preview_data, ensure_ascii=False).replace('</','<\\/')

app_js = r'''const root=document.querySelector('[data-mosaic-root]');
if(root){
  const data=JSON.parse(root.querySelector('[data-mosaic-data]').textContent||'{}');
  const cells=[...root.querySelectorAll('[data-scenario-id]')];
  const search=root.querySelector('[data-mosaic-search]');
  const count=root.querySelector('[data-mosaic-result-count]');
  const touch=matchMedia('(hover:none),(pointer:coarse)').matches;
  const activityLabels={understand:'Understand',learn:'Learn & share',create:'Create together',decide:'Decide',act:'Organize & act',respond:'Respond',remember:'Remember & share'};
  const esc=v=>{const d=document.createElement('div');d.textContent=v;return d.innerHTML};
  const setText=(sel,value)=>{const el=root.querySelector(sel);if(el){el.textContent=value;el.title=value}};
  const compact=(values,empty='—',limit=3)=>{if(!values||!values.length)return empty;const v=values.slice(0,limit);return values.length>limit?`${v.join(' · ')} +${values.length-limit}`:v.join(' · ')};
  function activities(profile){Object.entries(activityLabels).forEach(([key,label])=>{const el=root.querySelector(`[data-activity="${key}"]`);if(!el)return;const active=!!profile[key];el.classList.toggle('is-active',active);el.setAttribute('aria-label',`${label}: ${active?'involved':'not central'}`)})}
  function show(id){
    const s=data[id];if(!s)return;
    setText('[data-preview-id]',s.id);setText('[data-preview-category]',s.category);setText('[data-preview-title]',s.title);setText('[data-preview-summary]',s.summary);setText('[data-preview-category-label]',s.category);setText('[data-preview-pattern]',s.pattern);setText('[data-preview-scales]',compact(s.scales));setText('[data-preview-context]',compact(s.contexts));setText('[data-preview-properties]',compact(s.properties,'None highlighted',2));
    const profile=root.querySelector('[data-preview-profile]');if(profile)profile.dataset.category=s.categoryId;
    const img=root.querySelector('[data-preview-image]');if(img){if(img.getAttribute('src')!==s.image)img.src=s.image;img.alt=s.imageAlt}
    const link=root.querySelector('[data-preview-link]');if(link){link.href=s.href;link.hidden=false}
    root.querySelector('[data-preview-palette]').innerHTML=s.palette.slice(0,5).map(x=>`<span class="tag">${esc(x.replace(/[-_]+/g,' '))}</span>`).join('');
    activities(s.activities||{});
    const rel=new Set(s.related);cells.forEach(c=>{const cid=c.dataset.scenarioId;c.classList.toggle('is-active',cid===id);c.classList.toggle('is-related',rel.has(cid))})
  }
  function filter(q){q=q.trim().toLowerCase();let n=0;cells.forEach(c=>{const hit=!q||data[c.dataset.scenarioId].search.includes(q);c.classList.toggle('is-filtered-out',!hit);c.tabIndex=hit?0:-1;if(hit)n++});count.textContent=`${n} scenario${n===1?'':'s'}`}
  cells.forEach(c=>{const id=c.dataset.scenarioId;c.addEventListener('pointerenter',e=>{if(e.pointerType!=='touch')show(id)});c.addEventListener('focus',()=>show(id));c.addEventListener('click',e=>{if(touch){e.preventDefault();show(id);root.querySelector('[data-preview]').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'})}})});
  search.addEventListener('input',()=>filter(search.value));
  root.querySelector('[data-mosaic-surprise]').addEventListener('click',()=>{const v=cells.filter(c=>!c.classList.contains('is-filtered-out'));if(v.length){const c=v[Math.floor(Math.random()*v.length)];show(c.dataset.scenarioId);c.focus()}});
  root.querySelector('[data-mosaic-reset]').addEventListener('click',()=>{search.value='';filter('');cells.forEach(c=>c.classList.remove('is-active','is-related'))});
}'''
(OUT / 'assets/app.js').write_text(app_js, encoding='utf-8')

header_root = '<header class="site-header"><a class="brand" href="./index.html">⬡ <span>KOALI <strong>USE MOSAIC</strong></span></a><nav><a href="./index.html">Mosaic</a><a href="./uses/index.html">All scenarios</a></nav></header>'
index = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <title>Koali Use Mosaic</title>
  <link rel="stylesheet" href="./assets/styles.css">
</head>
<body>
{header_root}
<main>
  <div class="mosaic-experience" data-mosaic-root>
    <section class="scenario-preview" data-preview>
      <div class="preview-image-shell">
        <img data-preview-image src="./assets/mosaic-cover.svg" alt="Koali Use Mosaic" width="960" height="540">
      </div>
      <div class="preview-copy">
        <p class="preview-eyebrow"><span data-preview-id>KOALI USE MOSAIC</span> · <span data-preview-category>{len(scenarios)} scenarios</span></p>
        <h1 data-preview-title>Explore {len(scenarios)} ways to use Koali</h1>
        <p class="preview-summary" data-preview-summary>Move across the mosaic and pause on any cell. Each one opens a concrete situation where Koali connects knowledge, people, decisions, work and memory.</p>
        <div class="preview-tags" data-preview-palette><span class="tag">Hover or focus a cell</span></div>
        <a class="preview-cta" data-preview-link hidden>Read the scenario →</a>
      </div>
      <aside class="preview-profile" data-preview-profile aria-label="Scenario profile">
        <div class="profile-heading"><span class="profile-title">Scenario profile</span><span class="profile-category"><span class="category-swatch" data-preview-category-swatch aria-hidden="true"></span><strong data-preview-category-label>Explore the Mosaic</strong></span></div>
        <div class="profile-pattern"><span>Typical motion</span><small data-preview-pattern>Hover over a cell to see what kind of situation it represents.</small></div>
        <div class="profile-actions"><span class="profile-section-label">What happens here</span><div class="activity-signature" data-preview-activities aria-label="Scenario activities">
          <span class="activity-indicator" data-activity="understand"><i aria-hidden="true"></i>Understand</span><span class="activity-indicator" data-activity="learn"><i aria-hidden="true"></i>Learn &amp; share</span><span class="activity-indicator" data-activity="create"><i aria-hidden="true"></i>Create together</span><span class="activity-indicator" data-activity="decide"><i aria-hidden="true"></i>Decide</span><span class="activity-indicator" data-activity="act"><i aria-hidden="true"></i>Organize &amp; act</span><span class="activity-indicator" data-activity="respond"><i aria-hidden="true"></i>Respond</span><span class="activity-indicator" data-activity="remember"><i aria-hidden="true"></i>Remember &amp; share</span>
        </div></div>
        <div class="profile-context" aria-label="Scenario context"><div class="profile-context-row"><span>Scale</span><strong data-preview-scales>—</strong></div><div class="profile-context-row"><span>Context</span><strong data-preview-context>—</strong></div><div class="profile-context-row profile-context-conditions"><span>Special conditions</span><strong data-preview-properties>None highlighted</strong></div></div>
      </aside>
    </section>
    <div class="mosaic-controls"><label class="search-box"><span class="sr-only">Search</span><input data-mosaic-search type="search" placeholder="Search the mosaic…"></label><button class="ghost-button" data-mosaic-surprise>Surprise me</button><button class="ghost-button" data-mosaic-reset>Reset</button><output data-mosaic-result-count>{len(scenarios)} scenarios</output></div>
    <div class="mosaic-stage"><svg class="mosaic" viewBox="{' '.join(map(str,layout['viewBox']))}" role="group"><title>Koali Use Mosaic</title>{''.join(svg_cells)}</svg></div>
    <script type="application/json" data-mosaic-data>{json_data}</script>
  </div>
</main>
<script src="./assets/app.js"></script>
</body>
</html>'''
(OUT / 'index.html').write_text(index, encoding='utf-8')

header_uses = '<header class="site-header"><a class="brand" href="../index.html">⬡ <span>KOALI <strong>USE MOSAIC</strong></span></a><nav><a href="../index.html">Mosaic</a><a href="./index.html">All scenarios</a></nav></header>'
items = ''.join(f'<a href="./{s["id"]}/index.html"><span>{s["id"]}</span><strong>{html.escape(s["title"])}</strong><small>{html.escape(s["category_label"])}</small></a>' for s in scenarios)
(OUT / 'uses/index.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>All scenarios</title><link rel="stylesheet" href="../assets/styles.css"></head><body>{header_uses}<main><section class="list-page"><a class="back-link" href="../index.html">← Back to mosaic</a><h1>All {len(scenarios)} scenarios</h1><div class="scenario-index">{items}</div></section></main></body></html>', encoding='utf-8')

for i, s in enumerate(scenarios):
    d = OUT / 'uses' / s['id']; d.mkdir()
    prev = scenarios[i-1] if i else None; nxt = scenarios[i+1] if i < len(scenarios)-1 else None
    tags = ''.join(f'<span>{html.escape(str(x).replace("-", " "))}</span>' for x in s.get('palette',[]))
    active = public_activities(s.get('palette', []))
    activity_labels = {
        'understand': 'Understand',
        'learn': 'Learn & share',
        'create': 'Create together',
        'decide': 'Decide',
        'act': 'Organize & act',
        'respond': 'Respond',
        'remember': 'Remember & share',
    }
    activities_html = ''.join(
        f'<span class="scenario-activity{" is-active" if active[key] else ""}"><i aria-hidden="true"></i>{html.escape(label)}</span>'
        for key, label in activity_labels.items()
    )
    scales = ' · '.join(humanize(v) for v in s.get('scales', [])) or '—'
    context_values = list(dict.fromkeys(humanize(v) for v in [*s.get('settings', []), *s.get('domains', [])]))
    context = ' · '.join(context_values[:4]) or '—'
    properties = ' · '.join(humanize(v) for v in s.get('properties', [])) or 'None highlighted'
    left = f'<a href="../{prev["id"]}/index.html"><span>Previous</span><strong>{html.escape(prev["title"])}</strong></a>' if prev else '<span></span>'
    right = f'<a href="../{nxt["id"]}/index.html"><span>Next</span><strong>{html.escape(nxt["title"])}</strong></a>' if nxt else '<span></span>'
    header = '<header class="site-header"><a class="brand" href="../../index.html">⬡ <span>KOALI <strong>USE MOSAIC</strong></span></a><nav><a href="../../index.html">Mosaic</a><a href="../index.html">All scenarios</a></nav></header>'
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>{html.escape(s['id']+' — '+s['title'])}</title><link rel="stylesheet" href="../../assets/styles.css"></head><body>{header}<main><article class="scenario-shell"><a class="back-link" href="../../index.html">← Back to mosaic</a><header class="scenario-hero"><div><p class="scenario-kicker">{s['id']} · {html.escape(s['category_label'])}</p><h1>{html.escape(s['title'])}</h1><p class="scenario-dek">{html.escape(s['preview_summary'])}</p><div class="scenario-tags">{tags}</div></div><img src="../../assets/scenarios/{Path(s['preview_image']).name}" alt="{html.escape(s['preview_image_alt'])}"></header><section class="scenario-facts" aria-label="Scenario profile"><div><strong>Typical motion</strong><span>{html.escape(s['pattern_label'])}</span></div><div><strong>Scale</strong><span>{html.escape(scales)}</span></div><div><strong>Context</strong><span>{html.escape(context)}</span></div><div><strong>Special conditions</strong><span>{html.escape(properties)}</span></div></section><section class="scenario-activities" aria-label="What happens in this scenario"><strong>What happens here</strong><div>{activities_html}</div></section><div class="scenario-body">{s['body_html']}</div><nav class="scenario-nav">{left}{right}</nav></article></main></body></html>'''
    (d / 'index.html').write_text(page, encoding='utf-8')

print(f'Built file://-safe preview with {len(scenarios)} scenarios at {OUT}')
