const root=document.querySelector('[data-mosaic-root]');
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
}