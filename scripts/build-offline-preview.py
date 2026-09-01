from pathlib import Path
import json, re, html, shutil, math, yaml

R = Path(__file__).resolve().parents[1]
O = R / 'preview'
if O.exists(): shutil.rmtree(O)
(O / 'assets/scenarios').mkdir(parents=True)
(O / 'assets/brand').mkdir(parents=True)
(O / 'assets/icons/palette').mkdir(parents=True)

metadata = json.loads((R / 'src/data/scenarios.json').read_text(encoding='utf-8'))
fr_tags = json.loads((R / 'src/i18n/fr-tags.json').read_text(encoding='utf-8'))
layout = json.loads((R / 'src/data/mosaic-layout.json').read_text(encoding='utf-8'))
system_catalog = json.loads((R / 'src/data/system-catalog.json').read_text(encoding='utf-8'))
scenario_system_routes = json.loads((R / 'src/data/scenario-system-routes.json').read_text(encoding='utf-8'))
scenario_capability_titles = json.loads((R / 'src/data/scenario-capability-titles.json').read_text(encoding='utf-8'))

for p in (R / 'public/scenarios/placeholders').glob('*.svg'):
    shutil.copy2(p, O / 'assets/scenarios' / p.name)
shutil.copy2(R / 'public/mosaic-cover.svg', O / 'assets/mosaic-cover.svg')
shutil.copy2(R / 'public/mosaic-cover-fr.svg', O / 'assets/mosaic-cover-fr.svg')
shutil.copy2(R / 'public/brand/koali-mark.svg', O / 'assets/brand/koali-mark.svg')
for p in (R / 'public/icons/palette').glob('*.svg'):
    shutil.copy2(p, O / 'assets/icons/palette' / p.name)
(O / 'assets/styles.css').write_text(
    (R / 'src/styles/global.css').read_text(encoding='utf-8') +
    (R / 'src/styles/mosaic.css').read_text(encoding='utf-8') +
    (R / 'src/styles/scenario.css').read_text(encoding='utf-8'), encoding='utf-8')
shutil.copy2(R / 'src/scripts/preview-layout.ts', O / 'assets/preview-layout.js')

BACKLIGHT_GROUPS = [
    {'key':'find','palette':['find','verify'],'icon':'search.svg','label':{'en':'Find','fr':'Trouver'},'architecture':['Kristal','Konnaxion']},
    {'key':'understand','palette':['understand'],'icon':'lightbulb.svg','label':{'en':'Understand','fr':'Comprendre'},'architecture':['Kristal','SemantiK']},
    {'key':'learn','palette':['learn','teach-share'],'icon':'book-open.svg','label':{'en':'Learn','fr':'Apprendre'},'architecture':['Konnaxion','UCKK']},
    {'key':'collaborate','palette':['collaborate','create'],'icon':'users.svg','label':{'en':'Collaborate','fr':'Collaborer'},'architecture':['Konnaxion']},
    {'key':'choose','palette':['deliberate','choose'],'icon':'git-branch.svg','label':{'en':'Choose','fr':'Choisir'},'architecture':['Konnaxion','Smart Vote','EkoH']},
    {'key':'act','palette':['organize','act'],'icon':'zap.svg','label':{'en':'Act','fr':'Agir'},'architecture':['Orgo']},
    {'key':'respond','palette':['respond','coordinate'],'icon':'message-circle-reply.svg','label':{'en':'Respond','fr':'Répondre'},'architecture':['Orgo','Konnaxion']},
    {'key':'remember','palette':['remember','disseminate'],'icon':'history.svg','label':{'en':'Remember','fr':'Se souvenir'},'architecture':['Kristal','UCKK']},
]

PALETTE_ICONS = {'find': 'search.svg', 'understand': 'lightbulb.svg', 'verify': 'badge-check.svg', 'learn': 'book-open.svg', 'teach-share': 'graduation-cap.svg', 'collaborate': 'users.svg', 'create': 'sparkles.svg', 'deliberate': 'messages-square.svg', 'choose': 'git-branch.svg', 'organize': 'list-checks.svg', 'act': 'zap.svg', 'respond': 'message-circle-reply.svg', 'coordinate': 'network.svg', 'remember': 'history.svg', 'disseminate': 'radio.svg'}


def lower_first(value):
    return value[:1].lower()+value[1:] if value else value


def strip_terminal_punctuation(value):
    return re.sub(r'[.!?;:]+$', '', (value or '').strip())


def example_lead(summary):
    marker=summary.find('Koali')
    return summary[:marker].strip() if marker>0 else ''


def build_koali_continuity_copy(x, locale):
    _, flow=public_details(x, locale)
    steps=[strip_terminal_punctuation(step) for step in flow.split('→') if strip_terminal_punctuation(step)]
    start=steps[0] if steps else ''
    end=steps[-1] if len(steps)>1 else ''
    gap=strip_terminal_punctuation(x.get('continuity_gap',''))

    if start and end:
        if locale=='fr':
            continuity=f"Dans Koali, le même contexte passe d’une capacité spécialisée à l’autre sans être recréé, du point de départ « {start} » jusqu’à « {end} »."
        else:
            continuity=f"In Koali, the same context moves across specialized capabilities without being recreated, from “{start}” through “{end}”."
    else:
        continuity=(
            'Dans Koali, le même contexte passe d’une capacité spécialisée à l’autre sans être recréé.'
            if locale=='fr' else
            'In Koali, the same context moves across specialized capabilities without being recreated.'
        )

    if not gap:
        return continuity
    if locale=='fr':
        return f"{continuity} Sans ce fil commun, {lower_first(gap)}."
    return f"{continuity} Without that shared thread, {lower_first(gap)}."


def portal_fields(x, locale):
    systems=[]
    for key in scenario_system_routes.get(x['id'],[]):
        item=system_catalog[key]
        systems.append({'key':key,'label':item['label'],'description':item['description'][locale]})
    return {
        'title':scenario_capability_titles.get(x['id'],{}).get(locale,x['pattern_label']),
        'summary':build_koali_continuity_copy(x, locale),
        'example':x['title'],
        'exampleLead':example_lead(x['preview_summary']),
        'systems':systems,
    }

def systems_html(x, locale, compact=False):
    systems=portal_fields(x,locale)['systems']
    if compact:
        return ''.join(f'<strong title="{html.escape(system["description"])}">{html.escape(system["label"])}</strong>' for system in systems)
    return ''.join(
        f'<span class="system-route" data-system-key="{html.escape(system["key"])}" title="{html.escape(system["description"])}"><strong>{html.escape(system["label"])}</strong><small>{html.escape(system["description"])}</small></span>'
        for system in systems
    )

UI = {
'en': {
  'product':'Scenario Mosaic','scenarios':'scenarios','examples':'concrete examples','explore':'Explore 120 concrete ways Koali helps',
  'hover':'Select an example to see the specific Koali action, the system path behind it, and how the pattern transfers elsewhere.',
  'select_prompt':'Select an example to reveal the specific Koali action behind it.',
  'hover_tag':'Hover or focus a cell','read':'Read the scenario','profile':'Inside Koali','example':'Example','open_example':'Open the full example','system_path':'System path','system_hint':'Select an example to see the specific Koali systems involved.','usually_via':'Usually via','swipe':'Swipe left for next · right for previous',
  'explore_mosaic':'Explore the Mosaic','motion':'Typical motion','inspect':'Hover a cell to inspect it.',
  'what':'What happens here','scale':'Scale','context':'Context','conditions':'Special conditions','none':'None highlighted',
  'search':'Search a need, system, or example…','surprise':'Surprise me','reset':'Reset','legend':'Scenario families',
  'hint':'Each hexagon is an example. Select one to see the specific Koali action and its system path above.',
  'map_labels':{'CAT-01':['Find &','Understand'],'CAT-02':['Learn &','Share'],'CAT-03':['Collaborate &','Create'],'CAT-04':['Choose &','Govern'],'CAT-05':['Organize &','Act'],'CAT-06':['Respond &','Coordinate'],'CAT-07':['Remember &','Improve'],'CAT-08':['Disseminate &','Connect']},
  'back':'← Back to mosaic','all':'All scenarios',
  'detail_starts':'Starts from','detail_loss':'What breaks without continuity','detail_continuity':'System path','detail_flow':'How it moves','detail_transfer':'Also useful for','detail_back':'Back to the full Mosaic',
  'activities':{'understand':'Understand','learn':'Learn & share','create':'Create together','decide':'Decide','act':'Organize & act','respond':'Respond','remember':'Remember & share'},
  'involved':'involved','notCentral':'not central','lang':'Language',
},
'fr': {
  'product':'Mosaïque de scénarios','scenarios':'scénarios','examples':'exemples concrets','explore':'Explorez 120 façons concrètes dont Koali aide',
  'hover':'Sélectionnez un exemple pour voir l’action précise de Koali, le chemin système qui la porte et comment le pattern se transpose ailleurs.',
  'select_prompt':'Sélectionnez un exemple pour révéler l’action précise de Koali derrière la situation.',
  'hover_tag':'Survolez ou ciblez une cellule','read':'Lire le scénario','profile':'Dans Koali','example':'Exemple','open_example':'Ouvrir l’exemple complet','system_path':'Chemin système','system_hint':'Sélectionnez un exemple pour voir les systèmes Koali précisément concernés.','usually_via':'Généralement via','swipe':'Balayez à gauche : suivant · à droite : précédent',
  'explore_mosaic':'Explorer la mosaïque','motion':'Dynamique typique','inspect':'Survolez une cellule pour l’examiner.',
  'what':'Ce qui se passe ici','scale':'Échelle','context':'Contexte','conditions':'Conditions particulières','none':'Aucune mise en évidence',
  'search':'Rechercher un besoin, un système ou un exemple…','surprise':'Au hasard','reset':'Réinitialiser','legend':'Familles de scénarios',
  'hint':'Chaque hexagone est un exemple. Sélectionnez-en un pour voir l’action précise de Koali et son chemin système au-dessus.',
  'map_labels':{'CAT-01':['Trouver &','comprendre'],'CAT-02':['Apprendre &','transmettre'],'CAT-03':['Collaborer &','créer'],'CAT-04':['Choisir &','gouverner'],'CAT-05':['Organiser &','agir'],'CAT-06':['Répondre &','coordonner'],'CAT-07':['Se souvenir &','améliorer'],'CAT-08':['Diffuser &','connecter']},
  'back':'← Retour à la mosaïque','all':'Tous les scénarios',
  'detail_starts':'Part de','detail_loss':'Ce qui se perd sans continuité','detail_continuity':'Chemin système','detail_flow':'Comment ça circule','detail_transfer':'Aussi utile pour','detail_back':'Retour à la mosaïque complète',
  'activities':{'understand':'Comprendre','learn':'Apprendre & transmettre','create':'Créer ensemble','decide':'Décider','act':'Organiser & agir','respond':'Répondre','remember':'Se souvenir & partager'},
  'involved':'impliqué','notCentral':'non central','lang':'Langue',
}}

ENTRY_TRIGGER_LABELS = {
'en': {
  'question-or-signal':'A question, signal, or anomaly',
  'knowledge-to-transfer':'Knowledge that needs to be transmitted',
  'idea-or-goal':'An idea or goal to develop together',
  'decision-to-make':'A choice that needs to be made',
  'mandate-or-plan':'A mandate or plan that must become action',
  'incident-or-change':'An incident or changing situation',
  'result-or-lessons-learned':'A result or lesson worth preserving',
  'knowledge-to-publish':'Knowledge that needs to reach a public',
},
'fr': {
  'question-or-signal':'Une question, un signal ou une anomalie',
  'knowledge-to-transfer':'Un savoir qui doit être transmis',
  'idea-or-goal':'Une idée ou un objectif à développer ensemble',
  'decision-to-make':'Un choix qui doit être fait',
  'mandate-or-plan':'Un mandat ou un plan qui doit devenir action',
  'incident-or-change':'Un incident ou une situation qui évolue',
  'result-or-lessons-learned':'Un résultat ou une leçon à préserver',
  'knowledge-to-publish':'Un savoir qui doit rejoindre un public',
}}

def clean_md(value):
    value=re.sub(r'`([^`]+)`',r'\1',value)
    value=re.sub(r'\*\*([^*]+)\*\*',r'\1',value)
    value=re.sub(r'\*([^*]+)\*',r'\1',value)
    return re.sub(r'\s+',' ',value).strip()

def extract_section(body, heading):
    m=re.search(r'^## '+re.escape(heading)+r'\s*$([\s\S]*?)(?=^## |\Z)',body,re.M)
    return clean_md(m.group(1)) if m else ''

def public_details(x, locale):
    continuity_heading='Ce qui rend ce scénario caractéristique de Koali' if locale=='fr' else 'What makes this characteristically Koali'
    loop_heading='Boucle' if locale=='fr' else 'Loop'
    continuity=extract_section(x['body'],continuity_heading)
    flow=extract_section(x['body'],loop_heading)
    if not continuity:
        continuity='Koali préserve le contexte utile tout au long du parcours, afin que compréhension, action et apprentissage restent reliés.' if locale=='fr' else 'Koali preserves the useful context across the whole journey so understanding, action, and learning remain connected.'
    return continuity, flow or x['pattern']

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

def palette_tag(locale, value, icon_prefix):
    label=html.escape(palette_label(locale,value))
    filename=PALETTE_ICONS.get(value)
    icon=f'<img class="tag-icon" src="{icon_prefix}/{filename}" alt="" aria-hidden="true">' if filename else ''
    return f'<span class="tag" data-palette-key="{html.escape(value)}">{icon}{label}</span>'


def backlight_strip(locale, palette_values, icon_prefix):
    active=set(palette_values)
    tags=[]
    for group in BACKLIGHT_GROUPS:
        is_active=any(key in active for key in group['palette'])
        state=' is-active' if is_active else ''
        label=html.escape(group['label'][locale])
        architecture=html.escape(' · '.join(group['architecture']))
        icon=f'<img class="tag-icon" src="{icon_prefix}/{group["icon"]}" alt="" aria-hidden="true">'
        tags.append(f'<span class="tag tag-backlight{state}" data-backlight-key="{group["key"]}" data-architecture="{architecture}" title="{label} — {architecture}">{icon}<span class="tag-label">{label}</span></span>')
    return ''.join(tags)

RESPONSIVE_IMAGE_WIDTHS=(418,627,836,1254)
RESPONSIVE_IMAGE_DEFAULT=627
RESPONSIVE_IMAGE_SIZES='(min-width: 901px) 292px, (min-width: 721px) 220px, (min-width: 363px) 210px, 58vw'

def responsive_variant_name(sid, width):
    return f'{sid}.png' if width==RESPONSIVE_IMAGE_DEFAULT else f'{sid}-{width}.png'

def responsive_image(x, png_prefix, fallback):
    sid=x['id']
    default=R/'public/scenarios/images'/f'{sid}.png'
    if not default.exists():
        return {'src':fallback,'srcset':'','sizes':''}
    candidates=[]
    for width in RESPONSIVE_IMAGE_WIDTHS:
        name=responsive_variant_name(sid,width)
        if (R/'public/scenarios/images'/name).exists():
            candidates.append(f'{png_prefix}/{name} {width}w')
    return {
        'src':f'{png_prefix}/{sid}.png',
        'srcset':', '.join(candidates) if len(candidates)>1 else '',
        'sizes':RESPONSIVE_IMAGE_SIZES if len(candidates)>1 else '',
    }

def preview_image(x, locale):
    # index.html is preview/<locale>/index.html
    fallback='../assets/scenarios/'+Path(x['preview_image']).name
    return responsive_image(x,'../../public/scenarios/images',fallback)

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

# Shared offline JS mirrors the production interaction without requiring npm modules under file://.
# Production Astro uses GSAP + SplitText; this preview keeps the same spring model with requestAnimationFrame.
app_js = r'''(() => {
  const root = document.querySelector('[data-mosaic-root]');
  if (!root) return;
  const data = JSON.parse(root.querySelector('[data-mosaic-data]')?.textContent || '{}');
  const tr = JSON.parse(root.querySelector('[data-mosaic-i18n]')?.textContent || '{}');
  const cells = [...root.querySelectorAll('[data-scenario-id]')];
  const search = root.querySelector('[data-mosaic-search]');
  const count = root.querySelector('[data-mosaic-result-count]');
  const canvas = root.querySelector('[data-mosaic-canvas]');
  const setText = (q,v) => { const e=root.querySelector(q); if(e){e.textContent=v;e.title=v;} };
  const compact = (a,empty='—',limit=3) => !a||!a.length ? empty : (a.length>limit ? `${a.slice(0,limit).join(' · ')} +${a.length-limit}` : a.join(' · '));
  const renderSystems = systems => { const list=root.querySelector('[data-preview-system-list]'); if(!list)return; list.replaceChildren(); (systems||[]).forEach(system=>{const item=document.createElement('span');item.className='system-route';item.dataset.systemKey=system.key;item.title=system.description;const name=document.createElement('strong');name.textContent=system.label;const detail=document.createElement('small');detail.textContent=system.description;item.append(name,detail);list.append(item);}); };
  const selectOnly = id => cells.forEach(c => c.classList.toggle('is-active',c.dataset.scenarioId===id));
  function show(id){
    const s=data[id]; if(!s) return;
    selectOnly(id);
    if(preview) preview.dataset.previewSelected='true';
    if(canvas) canvas.dataset.activeTerritory=s.categoryId;
    setText('[data-preview-id]',s.id);setText('[data-preview-category]',s.category);setText('[data-preview-title]',s.title);setText('[data-preview-summary]',s.summary);setText('[data-preview-example]',s.example);const ew=root.querySelector('[data-preview-example-wrap]');if(ew)ew.hidden=false;renderSystems(s.systems||[]);setText('[data-preview-scales]',compact(s.scales));setText('[data-preview-context]',compact(s.contexts));setText('[data-preview-properties]',compact(s.properties,tr.noneHighlighted,2));
    const p=root.querySelector('[data-preview-profile]');if(p)p.dataset.category=s.categoryId;
    const prompt=root.querySelector('[data-preview-prompt]');if(prompt)prompt.hidden=true;
    const img=root.querySelector('[data-preview-image]');if(img){if(s.imageSrcSet){img.sizes=s.imageSizes||'100vw';img.srcset=s.imageSrcSet;}else{img.removeAttribute('srcset');img.removeAttribute('sizes');}img.src=s.image;img.alt=s.imageAlt;img.dataset.imageState='scenario';img.hidden=false;}
    const link=root.querySelector('[data-preview-link]');if(link){link.href=s.href;link.hidden=false;}
    const activePalette=new Set(s.paletteKeys||[]);
    const backlightGroups=[{"key":"find","palette":["find","verify"],"architecture":"Kristal · Konnaxion"},{"key":"understand","palette":["understand"],"architecture":"Kristal · SemantiK"},{"key":"learn","palette":["learn","teach-share"],"architecture":"Konnaxion · UCKK"},{"key":"collaborate","palette":["collaborate","create"],"architecture":"Konnaxion"},{"key":"choose","palette":["deliberate","choose"],"architecture":"Konnaxion · Smart Vote · EkoH"},{"key":"act","palette":["organize","act"],"architecture":"Orgo"},{"key":"respond","palette":["respond","coordinate"],"architecture":"Orgo · Konnaxion"},{"key":"remember","palette":["remember","disseminate"],"architecture":"Kristal · UCKK"}];
    root.querySelectorAll('[data-backlight-key]').forEach(el=>{const g=backlightGroups.find(x=>x.key===el.dataset.backlightKey);const on=!!g&&g.palette.some(k=>activePalette.has(k));el.classList.toggle('is-active',on);const label=el.querySelector('.tag-label')?.textContent||'';el.setAttribute('aria-label',`${label}: ${on?tr.involved:tr.notCentral}. Architecture: ${g?.architecture||''}`);});
    preview?.dispatchEvent(new CustomEvent('preview:contentchange'));
  }
  const touchPreviewMode=matchMedia('(hover: none), (pointer: coarse)').matches;
  const reducedMotion=matchMedia('(prefers-reduced-motion: reduce)');
  const preview=root.querySelector('.scenario-preview');
  /* Hover remains intent-delayed. Shared title and palette sizing comes from
     preview-layout.js on both the Mosaic and the static detail pages. */
  const hoverPreviewDelayMs=140;
  let hoverPreviewTimer,pendingHoverId=null;
  const cancelScheduledPreview=id=>{if(id&&pendingHoverId!==id)return;if(hoverPreviewTimer!==undefined)clearTimeout(hoverPreviewTimer);hoverPreviewTimer=undefined;pendingHoverId=null;};
  const schedulePreview=id=>{cancelScheduledPreview();pendingHoverId=id;hoverPreviewTimer=setTimeout(()=>{hoverPreviewTimer=undefined;pendingHoverId=null;show(id);},hoverPreviewDelayMs);};
  const availableScenarioCells=()=>cells.filter(c=>!c.classList.contains('is-filtered-out')).sort((a,b)=>(a.dataset.scenarioId||'').localeCompare(b.dataset.scenarioId||'',undefined,{numeric:true}));
  const stepScenario=direction=>{const available=availableScenarioCells();if(!available.length)return;const activeId=cells.find(c=>c.classList.contains('is-active'))?.dataset.scenarioId;let index=available.findIndex(c=>c.dataset.scenarioId===activeId);if(index<0)index=direction>0?-1:0;const next=available[(index+direction+available.length)%available.length];if(next)show(next.dataset.scenarioId);};
  if(touchPreviewMode&&preview){let start=null;preview.addEventListener('touchstart',e=>{if(e.touches.length!==1){start=null;return;}const t=e.touches[0];start={x:t.clientX,y:t.clientY,time:performance.now()};},{passive:true});preview.addEventListener('touchend',e=>{if(!start||e.changedTouches.length!==1){start=null;return;}const t=e.changedTouches[0],dx=t.clientX-start.x,dy=t.clientY-start.y,duration=performance.now()-start.time;start=null;if(duration>900||Math.abs(dx)<48||Math.abs(dx)<=Math.abs(dy)*1.2)return;stepScenario(dx<0?1:-1);},{passive:true});preview.addEventListener('touchcancel',()=>{start=null;},{passive:true});}
  cells.forEach(c=>{const id=c.dataset.scenarioId;c.addEventListener('pointerenter',e=>{if(touchPreviewMode||e.pointerType==='touch')return;schedulePreview(id);});c.addEventListener('pointerleave',()=>cancelScheduledPreview(id));c.addEventListener('focus',()=>{cancelScheduledPreview();show(id);});c.addEventListener('click',e=>{if(!touchPreviewMode)return;e.preventDefault();cancelScheduledPreview();show(id);preview?.scrollIntoView({behavior:reducedMotion.matches?'auto':'smooth',block:'start'});});});
  search?.addEventListener('input',()=>{const q=search.value.trim().toLowerCase();let n=0;cells.forEach(c=>{const hit=!q||data[c.dataset.scenarioId].search.includes(q);c.classList.toggle('is-filtered-out',!hit);if(hit)n++;});if(count)count.textContent=`${n} ${n===1?tr.scenarioSingular:tr.scenarios}`;});
  root.querySelector('[data-mosaic-surprise]')?.addEventListener('click',()=>{cancelScheduledPreview();const v=cells.filter(c=>!c.classList.contains('is-filtered-out'));if(v.length){const c=v[Math.floor(Math.random()*v.length)];show(c.dataset.scenarioId);c.focus();}});
  root.querySelector('[data-mosaic-reset]')?.addEventListener('click',()=>{cancelScheduledPreview();if(search)search.value='';cells.forEach(c=>c.classList.remove('is-filtered-out','is-active'));if(canvas)delete canvas.dataset.activeTerritory;if(count)count.textContent=`${cells.length} ${tr.scenarios}`;});

  if (!canvas || !matchMedia('(hover: hover) and (pointer: fine)').matches || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const lines=[...canvas.querySelectorAll('[data-territory-line]')];
  const states=[];
  for(const line of lines){
    const text=line.textContent||'';line.textContent='';
    for(const ch of [...text]){const span=document.createElement('span');span.className='territory-label__char';span.textContent=ch===' '?'\u00a0':ch;line.append(span);states.push({el:span,restX:0,restY:0,x:0,y:0,vx:0,vy:0,targetX:0,targetY:0});}
  }
  const cfg={radius:104,maxOffset:11,forceExponent:1.95,spring:.085,damping:.56,pointerSmoothing:.34,maxVelocity:1.35,settleDistance:.06,settleVelocity:.05};
  const pointer={x:0,y:0,rawX:0,rawY:0,active:false,initialized:false};let raf=0,last=performance.now(),visible=true;
  const measure=()=>{const cr=canvas.getBoundingClientRect();for(const s of states){const r=s.el.getBoundingClientRect();s.restX=r.left+r.width/2-cr.left-s.x;s.restY=r.top+r.height/2-cr.top-s.y;}};
  const settled=()=>states.every(s=>Math.abs(s.x)<cfg.settleDistance&&Math.abs(s.y)<cfg.settleDistance&&Math.abs(s.vx)<cfg.settleVelocity&&Math.abs(s.vy)<cfg.settleVelocity);
  const wake=()=>{if(!raf&&visible){last=performance.now();raf=requestAnimationFrame(tick);}};
  function tick(now){raf=0;if(!visible)return;const factor=Math.min(2,Math.max(.5,(now-last)/16.667));last=now;const damp=Math.pow(cfg.damping,factor);if(pointer.active){if(!pointer.initialized){pointer.x=pointer.rawX;pointer.y=pointer.rawY;pointer.initialized=true;}else{const follow=1-Math.pow(1-cfg.pointerSmoothing,factor);pointer.x+=(pointer.rawX-pointer.x)*follow;pointer.y+=(pointer.rawY-pointer.y)*follow;}}for(const s of states){if(pointer.active){const dx=s.restX-pointer.x,dy=s.restY-pointer.y,d=Math.hypot(dx,dy);if(d>.001&&d<cfg.radius){const prox=Math.max(0,1-d/cfg.radius),force=Math.pow(prox,cfg.forceExponent),a=cfg.maxOffset*force;s.targetX=dx/d*a;s.targetY=dy/d*a;}else{s.targetX=s.targetY=0;}}else{s.targetX=s.targetY=0;}s.vx+=(s.targetX-s.x)*cfg.spring*factor;s.vy+=(s.targetY-s.y)*cfg.spring*factor;s.vx*=damp;s.vy*=damp;s.vx=Math.max(-cfg.maxVelocity,Math.min(cfg.maxVelocity,s.vx));s.vy=Math.max(-cfg.maxVelocity,Math.min(cfg.maxVelocity,s.vy));s.x+=s.vx*factor;s.y+=s.vy*factor;s.el.style.transform=`translate3d(${s.x}px,${s.y}px,0)`;}if(pointer.active||!settled())raf=requestAnimationFrame(tick);}
  canvas.addEventListener('pointermove',e=>{const r=canvas.getBoundingClientRect();pointer.rawX=e.clientX-r.left;pointer.rawY=e.clientY-r.top;if(!pointer.active){pointer.x=pointer.rawX;pointer.y=pointer.rawY;pointer.initialized=true;}pointer.active=true;wake();},{passive:true});
  canvas.addEventListener('pointerleave',()=>{pointer.active=false;wake();},{passive:true});
  new ResizeObserver(()=>requestAnimationFrame(measure)).observe(canvas);
  new IntersectionObserver(es=>{visible=!!es[0]?.isIntersecting;if(visible)requestAnimationFrame(measure);else{pointer.active=false;}},{threshold:.01}).observe(canvas);
  (document.fonts?.ready||Promise.resolve()).then(()=>requestAnimationFrame(measure));
})();'''
(O/'assets/app.js').write_text(app_js,encoding='utf-8')

for locale in ('en','fr'):
    s=UI[locale]; other='fr' if locale=='en' else 'en'
    scenarios=parse_localized(locale); by={x['id']:x for x in scenarios}
    base=O/locale; (base/'uses').mkdir(parents=True,exist_ok=True)
    data={}
    for x in scenarios:
        contexts=list(dict.fromkeys([*x.get('settings',[]),*x.get('domains',[])]))[:3]
        portal=portal_fields(x,locale)
        system_search=[value for system in portal['systems'] for value in (system['label'],system['description'])]
        data[x['id']]={
          'id':x['id'],'title':portal['title'],'example':portal['example'],'exampleLead':portal['exampleLead'],'category':x['category_label'],'categoryId':x['primary_category'],'pattern':x['pattern_label'],'summary':portal['summary'],'systems':portal['systems'],
          'paletteKeys':list(x['palette']),
          'palette':[palette_label(locale,v) for v in x['palette']],
          'scales':[humanize(locale,v) for v in x.get('scales',[])],
          'contexts':[humanize(locale,v) for v in contexts],
          'properties':[humanize(locale,v) for v in x.get('properties',[])],
          'image':preview_image(x,locale)['src'],'imageSrcSet':preview_image(x,locale)['srcset'],'imageSizes':preview_image(x,locale)['sizes'],'imageAlt':x['preview_image_alt'],'href':f'./uses/{x["id"]}/index.html',
          'search':' '.join([x['title'],x['category_label'],x['pattern_label'],portal['summary'],*x['palette'],*x.get('domains',[]),*x.get('settings',[]),*system_search,*[humanize(locale,v) for v in x.get('domains',[])]]).lower()}
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
    territory_labels=[]
    for cid in sorted(layout.get('territoryLabels',{})):
        a=layout['territoryLabels'][cid]
        lines=''.join(f'<span class="territory-label__line" data-territory-line>{html.escape(line)}</span>' for line in s['map_labels'][cid])
        territory_labels.append(f'<div class="territory-label {cid.lower()}" data-territory-id="{cid}" style="--territory-x:{a["x"]*100}%;--territory-y:{a["y"]*100}%;--territory-w:{a["width"]*100}%">{lines}</div>')
    territory_layer='<div class="territory-label-layer" aria-hidden="true" data-territory-label-layer>'+''.join(territory_labels)+'</div>'
    profile=f'''<aside class="preview-profile" data-preview-profile><div class="profile-heading"><span class="profile-title">{html.escape(s['profile'])}</span></div><div class="profile-systems" data-preview-systems><span class="profile-section-label">{html.escape(s['system_path'])}</span><div class="system-route-list" data-preview-system-list><span class="system-route-empty">{html.escape(s['system_hint'])}</span></div></div><div class="profile-context"><div><span>{html.escape(s['scale'])}</span><strong data-preview-scales>—</strong></div><div><span>{html.escape(s['context'])}</span><strong data-preview-context>—</strong></div><div><span>{html.escape(s['conditions'])}</span><strong data-preview-properties>{html.escape(s['none'])}</strong></div></div></aside>'''
    switch=f'<nav class="language-switcher" aria-label="{html.escape(s["lang"])}"><a class="{"active" if locale=="en" else ""}" href="../en/index.html">EN</a><span>/</span><a class="{"active" if locale=="fr" else ""}" href="../fr/index.html">FR</a></nav>'
    index=f'''<!doctype html><html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><meta name="theme-color" content="#1e6864"><link rel="icon" href="../assets/brand/koali-mark.svg"><link rel="stylesheet" href="../assets/styles.css"><title>{'Mosaïque de scénarios Koali' if locale=='fr' else 'Koali Scenario Mosaic'}</title></head><body><header class="site-header"><a class="brand" href="./index.html"><img class="brand-mark" src="../assets/brand/koali-mark.svg" alt=""><span class="brand-copy"><span class="brand-product"><strong>Koali</strong><span>{html.escape(s['product'])}</span></span><small>the Sociotechnical Operating System</small></span></a>{switch}</header><main><div class="mosaic-experience" data-mosaic-root><section class="scenario-preview" data-preview-swipe="true" data-preview-selected="false"><div class="preview-image-shell" data-preview-media><p class="preview-image-prompt" data-preview-prompt>{html.escape(s['select_prompt'])}</p><img data-preview-image data-image-state="empty" alt="" hidden></div><div class="preview-copy"><p class="preview-eyebrow"><span data-preview-id>{'Mosaïque de scénarios Koali' if locale=='fr' else 'Koali Scenario Mosaic'}</span> · <span data-preview-category>120 {html.escape(s['examples'])}</span></p><h1 data-preview-title>{html.escape(s['explore'])}</h1><p class="preview-summary" data-preview-summary>{html.escape(s['hover'])}</p><p class="preview-example" data-preview-example-wrap hidden><span>{html.escape(s['example'])}</span><strong data-preview-example></strong></p><div class="preview-tags preview-backlights" data-preview-palette>{backlight_strip(locale, [], "../assets/icons/palette")}</div><a class="preview-cta touch-full-link" data-preview-link hidden>{html.escape(s['open_example'])} <span aria-hidden="true">→</span></a><p class="mobile-swipe-hint">{html.escape(s['swipe'])}</p></div>{profile}</section><div class="mosaic-controls"><label class="search-box"><input data-mosaic-search placeholder="{html.escape(s['search'])}"></label><button class="ghost-button" data-mosaic-surprise>{html.escape(s['surprise'])}</button><button class="ghost-button" data-mosaic-reset>{html.escape(s['reset'])}</button><output data-mosaic-result-count>120 {s['scenarios']}</output></div><div class="territory-legend sr-only" aria-label="{html.escape(s['legend'])}">{legend}</div><div class="mosaic-stage" data-mosaic-stage><div class="mosaic-scroll"><div class="mosaic-canvas" data-mosaic-canvas><svg class="mosaic" viewBox="{' '.join(map(str,layout['viewBox']))}">{''.join(cells)}</svg>{territory_layer}</div></div><p class="mosaic-hint">{html.escape(s['hint'])}</p></div><script type="application/json" data-mosaic-data>{json.dumps(data,ensure_ascii=False).replace('</','<\\/')}</script><script type="application/json" data-mosaic-i18n>{json.dumps({'noneHighlighted':s['none'],'scenarios':s['scenarios'],'scenarioSingular':'scénario' if locale=='fr' else 'scenario','involved':s['involved'],'notCentral':s['notCentral']},ensure_ascii=False)}</script></div></main><script src="../assets/preview-layout.js"></script><script src="../assets/app.js"></script></body></html>'''
    (base/'index.html').write_text(index,encoding='utf-8')

    list_items=''.join(f'<p><a href="./{x["id"]}/index.html">{x["id"]} — {html.escape(x["title"])}</a></p>' for x in scenarios)
    (base/'uses/index.html').write_text(f'<!doctype html><html lang="{locale}"><head><meta charset="utf-8"><link rel="stylesheet" href="../../assets/styles.css"><title>{html.escape(s["all"])}</title></head><body><main><section class="scenario-shell"><a class="back-link" href="../index.html">{html.escape(s["back"])}</a><h1>{html.escape(s["all"])}</h1>{list_items}</section></main></body></html>',encoding='utf-8')

    for x in scenarios:
        d=base/'uses'/x['id']; d.mkdir(parents=True,exist_ok=True)
        alt=f'../../../{other}/uses/{x["id"]}/index.html'
        switch_detail=f'<nav class="language-switcher"><a class="{"active" if locale=="en" else ""}" href="{"index.html" if locale=="en" else alt}">EN</a><span>/</span><a class="{"active" if locale=="fr" else ""}" href="{"index.html" if locale=="fr" else alt}">FR</a></nav>'

        contexts=list(dict.fromkeys([*x.get('settings',[]),*x.get('domains',[])]))[:3]
        scales=[humanize(locale,v) for v in x.get('scales',[])]
        context_labels=[humanize(locale,v) for v in contexts]
        props=[humanize(locale,v) for v in x.get('properties',[])]
        portal=portal_fields(x,locale)
        scenario_profile=f'''<aside class="preview-profile" data-preview-profile data-category="{x['primary_category']}"><div class="profile-heading"><span class="profile-title">{html.escape(s['profile'])}</span></div><div class="profile-systems" data-preview-systems><span class="profile-section-label">{html.escape(s['system_path'])}</span><div class="system-route-list" data-preview-system-list>{systems_html(x,locale)}</div></div><div class="profile-context"><div><span>{html.escape(s['scale'])}</span><strong data-preview-scales>{html.escape(' · '.join(scales))}</strong></div><div><span>{html.escape(s['context'])}</span><strong data-preview-context>{html.escape(' · '.join(context_labels))}</strong></div><div><span>{html.escape(s['conditions'])}</span><strong data-preview-properties>{html.escape(' · '.join(props) if props else s['none'])}</strong></div></div></aside>'''
        pal=backlight_strip(locale,x['palette'],'../../../assets/icons/palette')
        fallback=f'../../../assets/scenarios/{Path(x["preview_image"]).name}'
        image_data=responsive_image(x,'../../../../public/scenarios/images',fallback)
        img=image_data['src']
        srcset_attr=f' srcset="{html.escape(image_data["srcset"],quote=True)}" sizes="{html.escape(image_data["sizes"],quote=True)}"' if image_data['srcset'] else ''

        _,flow=public_details(x,locale)
        trigger=ENTRY_TRIGGER_LABELS[locale].get(x['entry_trigger'], humanize(locale,x['entry_trigger']))
        transfer=' · '.join(humanize(locale,v) for v in x.get('transfer_domains',[]))
        info=f'''<section class="scenario-info-mosaic" data-category="{x['primary_category']}"><article class="detail-hex detail-hex--trigger"><div class="detail-hex-inner"><span>{html.escape(s['detail_starts'])}</span><strong>{html.escape(trigger)}</strong></div></article><article class="detail-hex detail-hex--mechanism"><div class="detail-hex-inner"><span>{html.escape(s['detail_loss'])}</span><p>{html.escape(x['continuity_gap'])}</p></div></article><article class="detail-hex detail-hex--systems"><div class="detail-hex-inner"><span>{html.escape(s['detail_continuity'])}</span><div class="detail-system-list">{systems_html(x,locale,compact=True)}</div></div></article><article class="detail-hex detail-hex--flow"><div class="detail-hex-inner"><span>{html.escape(s['detail_flow'])}</span><p class="detail-flow">{html.escape(flow)}</p></div></article><article class="detail-hex detail-hex--transfer"><div class="detail-hex-inner"><span>{html.escape(s['detail_transfer'])}</span><strong>{html.escape(transfer)}</strong></div></article></section>'''
        preview=f'''<section class="scenario-preview"><div class="preview-image-shell"><img data-preview-image data-image-state="scenario" src="{img}"{srcset_attr} alt="{html.escape(x['preview_image_alt'])}"></div><div class="preview-copy"><p class="preview-eyebrow"><span data-preview-id>{x['id']}</span> · <span data-preview-category>{html.escape(x['category_label'])}</span></p><h1 data-preview-title>{html.escape(portal['title'])}</h1><p class="preview-summary" data-preview-summary>{html.escape(portal['summary'])}</p><p class="preview-example" data-preview-example-wrap><span>{html.escape(s['example'])}</span><strong data-preview-example>{html.escape(portal['example'])}</strong></p><div class="preview-tags preview-backlights" data-preview-palette>{pal}</div><a class="preview-cta" href="../../index.html">← {html.escape(s['detail_back'])}</a></div>{scenario_profile}</section>'''
        page=f'''<!doctype html><html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><meta name="theme-color" content="#1e6864"><link rel="icon" href="../../../assets/brand/koali-mark.svg"><link rel="stylesheet" href="../../../assets/styles.css"><title>{html.escape(portal['title'])} — {html.escape(x['title'])}</title></head><body><header class="site-header"><a class="brand" href="../../index.html"><img class="brand-mark" src="../../../assets/brand/koali-mark.svg" alt=""><span class="brand-copy"><span class="brand-product"><strong>Koali</strong><span>{html.escape(s['product'])}</span></span><small>the Sociotechnical Operating System</small></span></a>{switch_detail}</header><main><div class="mosaic-experience scenario-detail-experience">{preview}{info}</div></main><script src="../../../assets/preview-layout.js"></script></body></html>'''
        (d/'index.html').write_text(page,encoding='utf-8')

# Root offline language redirect. This remains file:// safe.
(O/'index.html').write_text('''<!doctype html><html><head><meta charset="utf-8"><title>Koali Scenario Mosaic</title><script>const l=(navigator.languages||[navigator.language||'en']).some(x=>String(x).toLowerCase().startsWith('fr'))?'fr':'en';location.replace('./'+l+'/index.html');</script></head><body><p><a href="./en/index.html">English</a> · <a href="./fr/index.html">Français</a></p></body></html>''',encoding='utf-8')
print('offline bilingual preview built: 120 EN + 120 FR scenarios')