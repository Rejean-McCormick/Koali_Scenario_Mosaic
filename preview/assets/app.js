(() => {
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
  const paletteIcons={"find":"search.svg","understand":"lightbulb.svg","verify":"badge-check.svg","learn":"book-open.svg","teach-share":"graduation-cap.svg","collaborate":"users.svg","create":"sparkles.svg","deliberate":"messages-square.svg","choose":"git-branch.svg","organize":"list-checks.svg","act":"zap.svg","respond":"message-circle-reply.svg","coordinate":"network.svg","remember":"history.svg","disseminate":"radio.svg"};
  const titleDensity = value => value.length > 80 ? 'long' : value.length > 54 ? 'medium' : 'short';
  const renderSystems = systems => { const list=root.querySelector('[data-preview-system-list]'); if(!list)return; list.replaceChildren(); (systems||[]).forEach(system=>{const item=document.createElement('span');item.className='system-route';item.dataset.systemKey=system.key;item.title=system.description;const name=document.createElement('strong');name.textContent=system.label;const detail=document.createElement('small');detail.textContent=system.description;item.append(name,detail);list.append(item);}); };
  const selectOnly = id => cells.forEach(c => c.classList.toggle('is-active',c.dataset.scenarioId===id));
  function show(id){
    const s=data[id]; if(!s) return;
    selectOnly(id);
    if(preview) preview.dataset.previewSelected='true';
    if(canvas) canvas.dataset.activeTerritory=s.categoryId;
    setText('[data-preview-id]',s.id);setText('[data-preview-category]',s.category);setText('[data-preview-title]',s.title);setText('[data-preview-summary]',s.summary);setText('[data-preview-example]',s.example);const ew=root.querySelector('[data-preview-example-wrap]');if(ew)ew.hidden=false;renderSystems(s.systems||[]);setText('[data-preview-scales]',compact(s.scales));setText('[data-preview-context]',compact(s.contexts));setText('[data-preview-properties]',compact(s.properties,tr.noneHighlighted,2));
    const title=root.querySelector('[data-preview-title]');if(title)title.dataset.titleDensity=titleDensity(s.title);
    const p=root.querySelector('[data-preview-profile]');if(p)p.dataset.category=s.categoryId;
    const prompt=root.querySelector('[data-preview-prompt]');if(prompt)prompt.hidden=true;
    const img=root.querySelector('[data-preview-image]');if(img){img.src=s.image;img.alt=s.imageAlt;img.dataset.imageState='scenario';img.hidden=false;}
    const link=root.querySelector('[data-preview-link]');if(link){link.href=s.href;link.hidden=false;}
    const activePalette=new Set(s.paletteKeys||[]);
    const backlightGroups=[{"key":"find","palette":["find","verify"],"architecture":"Kristal · Konnaxion"},{"key":"understand","palette":["understand"],"architecture":"Kristal · SemantiK"},{"key":"learn","palette":["learn","teach-share"],"architecture":"Konnaxion · UCKK"},{"key":"collaborate","palette":["collaborate","create"],"architecture":"Konnaxion"},{"key":"choose","palette":["deliberate","choose"],"architecture":"Konnaxion · Smart Vote · EkoH"},{"key":"act","palette":["organize","act"],"architecture":"Orgo"},{"key":"respond","palette":["respond","coordinate"],"architecture":"Orgo · Konnaxion"},{"key":"remember","palette":["remember","disseminate"],"architecture":"Kristal · UCKK"}];
    root.querySelectorAll('[data-backlight-key]').forEach(el=>{const g=backlightGroups.find(x=>x.key===el.dataset.backlightKey);const on=!!g&&g.palette.some(k=>activePalette.has(k));el.classList.toggle('is-active',on);const label=el.querySelector('.tag-label')?.textContent||'';el.setAttribute('aria-label',`${label}: ${on?tr.involved:tr.notCentral}. Architecture: ${g?.architecture||''}`);});
  }
  const touchPreviewMode=matchMedia('(hover: none), (pointer: coarse)').matches;
  const reducedMotion=matchMedia('(prefers-reduced-motion: reduce)');
  const preview=root.querySelector('.scenario-preview');
  const availableScenarioCells=()=>cells.filter(c=>!c.classList.contains('is-filtered-out')).sort((a,b)=>(a.dataset.scenarioId||'').localeCompare(b.dataset.scenarioId||'',undefined,{numeric:true}));
  const stepScenario=direction=>{const available=availableScenarioCells();if(!available.length)return;const activeId=cells.find(c=>c.classList.contains('is-active'))?.dataset.scenarioId;let index=available.findIndex(c=>c.dataset.scenarioId===activeId);if(index<0)index=direction>0?-1:0;const next=available[(index+direction+available.length)%available.length];if(next)show(next.dataset.scenarioId);};
  if(touchPreviewMode&&preview){let start=null;preview.addEventListener('touchstart',e=>{if(e.touches.length!==1){start=null;return;}const t=e.touches[0];start={x:t.clientX,y:t.clientY,time:performance.now()};},{passive:true});preview.addEventListener('touchend',e=>{if(!start||e.changedTouches.length!==1){start=null;return;}const t=e.changedTouches[0],dx=t.clientX-start.x,dy=t.clientY-start.y,duration=performance.now()-start.time;start=null;if(duration>900||Math.abs(dx)<48||Math.abs(dx)<=Math.abs(dy)*1.2)return;stepScenario(dx<0?1:-1);},{passive:true});preview.addEventListener('touchcancel',()=>{start=null;},{passive:true});}
  cells.forEach(c=>{const id=c.dataset.scenarioId;c.addEventListener('pointerenter',()=>show(id));c.addEventListener('focus',()=>show(id));c.addEventListener('click',e=>{if(!touchPreviewMode)return;e.preventDefault();show(id);preview?.scrollIntoView({behavior:reducedMotion.matches?'auto':'smooth',block:'start'});});});
  search?.addEventListener('input',()=>{const q=search.value.trim().toLowerCase();let n=0;cells.forEach(c=>{const hit=!q||data[c.dataset.scenarioId].search.includes(q);c.classList.toggle('is-filtered-out',!hit);if(hit)n++;});if(count)count.textContent=`${n} ${n===1?tr.scenarioSingular:tr.scenarios}`;});
  root.querySelector('[data-mosaic-surprise]')?.addEventListener('click',()=>{const v=cells.filter(c=>!c.classList.contains('is-filtered-out'));if(v.length){const c=v[Math.floor(Math.random()*v.length)];show(c.dataset.scenarioId);c.focus();}});
  root.querySelector('[data-mosaic-reset]')?.addEventListener('click',()=>{if(search)search.value='';cells.forEach(c=>c.classList.remove('is-filtered-out','is-active'));if(canvas)delete canvas.dataset.activeTerritory;if(count)count.textContent=`${cells.length} ${tr.scenarios}`;});

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
})();