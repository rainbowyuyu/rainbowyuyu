/* Dependency-free progressive enhancement. All project content remains readable without JavaScript. */
(() => {
'use strict';
const root=document.documentElement;
const q=s=>document.querySelector(s), qa=s=>[...document.querySelectorAll(s)];
const read=k=>{try{return localStorage.getItem(k)}catch{return null}};
const save=(k,v)=>{try{localStorage.setItem(k,v)}catch{}};
const params=new URLSearchParams(location.search);
let lang=params.get('lang')==='en'?'en':params.get('lang')==='zh'?'zh':read('rainbow-language')==='en'?'en':'zh';
let theme=read('rainbow-theme')==='light'?'light':'dark';
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
let paused=reduced.matches||read('rainbow-motion')==='paused';
let statusData=null;let statusLoaded=false;
const tr=(z,e)=>lang==='en'?e:z;
const languageButton=q('#language-toggle'),themeButton=q('#theme-toggle'),motionButton=q('#motion-toggle');
const projects=qa('.project-row'),expandButton=q('#expand-projects');
let savedOpen;try{savedOpen=JSON.parse(read('rainbow-projects'))}catch{}
if(Array.isArray(savedOpen))projects.forEach(p=>p.open=savedOpen.includes(p.id));
function updateProjectButtons(){
 projects.forEach(p=>{const label=p.querySelector('.expand-label');if(label)label.textContent=p.open?tr('收起','Collapse'):tr('展开','Explore')});
 const all=projects.every(p=>p.open);
 expandButton.textContent=(all?tr('收起全部','Collapse all'):tr('展开全部','Expand all'))+(all?' −':' ＋');
 expandButton.setAttribute('aria-expanded',String(all));
}
function updateStatus(){
 const el=q('#activity-status');
 if(!statusData){el.textContent=tr('更新时间暂不可用 · 以下为已保存快照','Update status unavailable · Saved snapshots below');return}
 const when=statusData.updated_at?new Date(statusData.updated_at):null;
 const formatted=when&&!Number.isNaN(when.valueOf())?new Intl.DateTimeFormat(lang==='en'?'en-GB':'zh-CN',{dateStyle:'medium',timeZone:'Asia/Shanghai'}).format(when):tr('未知','unknown');
 const cards=statusData.cards||{};
 const stats=Object.values(cards).map(c=>c.status);
 const stale=stats.some(s=>s==='stale'||s==='unavailable');
 el.textContent=tr('最近整理：','Last checked: ')+formatted+tr(' · 中国标准时间',' · China Standard Time')+(stale?tr(' · 部分来源待更新',' · Some sources need updating'):'');
 qa('.metric-card img').forEach(img=>{
  const src=img.getAttribute('src')||'';
  if(img.closest('.archive-cards'))return;let key=Object.keys(cards).find(k=>Array.isArray(cards[k].assets)&&cards[k].assets.includes(src));if(!key&&src.includes('snake'))key='snake';if(!key&&src.includes('profile-3d'))key='contributions3d';
  if(!key||!cards[key])return;
  const card=img.closest('.metric-card');let state=card.querySelector('.card-data-status');
  if(!state){state=document.createElement('p');state.className='card-data-status';card.append(state)}
  const s=cards[key].status;
  state.textContent=s==='fresh'?tr('已更新','Updated'):s==='stale'?tr('历史快照 · 等待更新','Saved snapshot · Awaiting update'):tr('来源暂不可用','Source currently unavailable');
  state.dataset.status=s;
 });
}
function updateMotionLabels(){
 root.dataset.motion=paused?'paused':'running';
 motionButton.setAttribute('aria-pressed',String(paused));
 motionButton.querySelector('.motion-icon').textContent=paused?'▶':'Ⅱ';
 motionButton.querySelector('.motion-label').textContent=paused?tr('开启动效','Enable motion'):tr('暂停动效','Pause motion');
 motionButton.setAttribute('aria-label',paused?tr('开启首页与贡献动画','Enable hero and contribution animation'):tr('暂停首页与贡献动画','Pause hero and contribution animation'));
}
function setLanguage(next,writeURL=false){
 lang=next;root.lang=lang==='en'?'en':'zh-CN';save('rainbow-language',lang);
 qa('[data-zh][data-en]').forEach(el=>{el.textContent=el.dataset[lang]});
 qa('[data-label-zh]').forEach(el=>el.setAttribute('aria-label',el.dataset[lang==='en'?'labelEn':'labelZh']));
 qa('[data-alt-zh]').forEach(el=>el.alt=el.dataset[lang==='en'?'altEn':'altZh']);
 qa('[data-placeholder-zh]').forEach(el=>el.placeholder=el.dataset[lang==='en'?'placeholderEn':'placeholderZh']);
 document.title=tr('rainbow鱼 · 浙江大学博士 | Research, Build, Explain','rainbow鱼 · PhD researcher at Zhejiang University');
 q('meta[name=description]').content=tr('rainbow鱼，浙江大学博士。探索物理 AI、工程智能体与科学可视化。精选项目：PhysCast、OmniForge、Wiscomper。','rainbow鱼, PhD researcher at Zhejiang University. Exploring physical AI, engineering agents and scientific visualization. Selected projects: PhysCast, OmniForge, Wiscomper.');
 q('meta[property="og:title"]').content=document.title;
 q('meta[property="og:description"]').content=q('meta[name=description]').content;
 languageButton.textContent=lang==='en'?'中文 ⇄':'EN ⇄';languageButton.lang=lang==='en'?'zh-CN':'en';
 languageButton.setAttribute('aria-label',lang==='en'?'切换到中文':'Switch to English');
 themeButton.setAttribute('aria-label',theme==='dark'?tr('切换浅色主题','Switch to light theme'):tr('切换深色主题','Switch to dark theme'));
 updateProjectButtons();updateMotionLabels();if(statusLoaded)updateStatus();
 if(writeURL){const url=new URL(location.href);url.searchParams.set('lang',lang);history.replaceState(null,'',url)}
}
function setTheme(next){theme=next;root.dataset.theme=theme;save('rainbow-theme',theme);themeButton.textContent=theme==='dark'?'☼':'☾';q('meta[name=theme-color]').content=theme==='dark'?'#0a0d14':'#f6f7fa';themeButton.setAttribute('aria-label',theme==='dark'?tr('切换浅色主题','Switch to light theme'):tr('切换深色主题','Switch to dark theme'));updateContributionImages();window.dispatchEvent(new Event('rainbow-theme'))}
projects.forEach(p=>p.addEventListener('toggle',()=>{updateProjectButtons();save('rainbow-projects',JSON.stringify(projects.filter(x=>x.open).map(x=>x.id)))}));
expandButton.hidden=false;expandButton.addEventListener('click',()=>{const open=!projects.every(p=>p.open);projects.forEach(p=>{p.open=open});updateProjectButtons()});
languageButton.hidden=false;languageButton.addEventListener('click',()=>setLanguage(lang==='en'?'zh':'en',true));
themeButton.hidden=false;themeButton.addEventListener('click',()=>setTheme(theme==='dark'?'light':'dark'));
function openHash(){let id;try{id=decodeURIComponent(location.hash.slice(1))}catch{return}const target=document.getElementById(id);if(target&&target.classList.contains('project-row')){target.open=true;updateProjectButtons()}}
window.addEventListener('hashchange',openHash);qa('a[href^="#"]').forEach(a=>a.addEventListener('click',()=>{const el=document.getElementById(a.hash.slice(1));if(el&&el.classList.contains('project-row'))el.open=true}));
q('#copyright-year').textContent=String(new Date().getFullYear());
qa('.metric-card img').forEach(img=>{const fail=()=>{img.closest('.metric-card').classList.add('is-unavailable');const fallback=img.parentElement.querySelector('.image-unavailable');if(fallback)fallback.hidden=false};img.addEventListener('error',fail);img.addEventListener('load',()=>{img.closest('.metric-card').classList.remove('is-unavailable');const fallback=img.parentElement.querySelector('.image-unavailable');if(fallback)fallback.hidden=true});if(img.complete&&!img.naturalWidth)fail()});
fetch('assets/profile/activity-status.json',{cache:'no-cache'}).then(r=>{if(!r.ok)throw Error('status');return r.json()}).then(data=>{statusData=data;statusLoaded=true;updateStatus()}).catch(()=>{statusLoaded=true;updateStatus()});
const dialog=q('#command-dialog'),search=q('#command-search'),commands=qa('#command-list a');
let commandIndex=0;
function visibleCommands(){return commands.filter(a=>!a.hidden)}
function markCommand(){const visible=visibleCommands();commandIndex=Math.max(0,Math.min(commandIndex,visible.length-1));commands.forEach(a=>a.classList.remove('selected'));if(visible[commandIndex])visible[commandIndex].classList.add('selected')}
function filterCommands(){const value=search.value.trim().toLocaleLowerCase();commands.forEach(a=>a.hidden=!a.dataset.search.toLocaleLowerCase().includes(value));q('#command-empty').hidden=visibleCommands().length>0;commandIndex=0;markCommand()}
function openCommands(){if(typeof dialog.showModal!=='function')return;search.value='';filterCommands();dialog.showModal();search.focus()}
qa('.search-trigger').forEach(b=>{b.hidden=false;b.addEventListener('click',openCommands)});
q('#command-close').addEventListener('click',()=>dialog.close());
search.addEventListener('input',filterCommands);
dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close()}});
commands.forEach(a=>a.addEventListener('click',event=>{event.preventDefault();dialog.close();const target=document.getElementById(a.hash.slice(1));if(target){if(target.classList.contains('project-row'))target.open=true;history.pushState(null,'',a.hash);target.scrollIntoView({behavior:paused?'instant':'smooth',block:'start'});const focus=target.querySelector('summary,h2')||target;if(focus.tagName!=='SUMMARY')focus.tabIndex=-1;focus.focus({preventScroll:true})}}));
dialog.addEventListener('keydown',e=>{if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();const list=visibleCommands();if(!list.length)return;commandIndex=(commandIndex+(e.key==='ArrowDown'?1:-1)+list.length)%list.length;markCommand();list[commandIndex].scrollIntoView({block:'nearest'})}if(e.key==='Enter'&&e.target===search){const target=visibleCommands()[commandIndex];if(target){e.preventDefault();target.click()}}});
document.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();dialog.open?dialog.close():openCommands()}});
if('IntersectionObserver'in window){const links=qa('.site-nav a');const observer=new IntersectionObserver(entries=>{for(const e of entries){if(!e.isIntersecting)continue;links.forEach(a=>{if(a.hash==='#'+e.target.id)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current')})}},{rootMargin:'-15% 0px -55% 0px'});links.forEach(a=>{const el=document.getElementById(a.hash.slice(1));if(el)observer.observe(el)})}
const contributions=qa('.animated-contribution');
contributions.forEach(img=>img.dataset.onScreen='true');
function updateContributionImages(){contributions.forEach(img=>{const playing=!paused&&!document.hidden&&img.dataset.onScreen!=='false';const src=playing?(theme==='light'?img.dataset.lightSrc:img.dataset.animatedSrc):(theme==='light'?img.dataset.lightStaticSrc:img.dataset.staticSrc);if(src&&img.getAttribute('src')!==src)img.src=src})}
if('IntersectionObserver'in window){const observer=new IntersectionObserver(entries=>{entries.forEach(e=>e.target.dataset.onScreen=String(e.isIntersecting));updateContributionImages()},{rootMargin:'150px'});contributions.forEach(img=>observer.observe(img))}
function changeMotion(value,persist=true){paused=value;if(persist)save('rainbow-motion',paused?'paused':'running');updateMotionLabels();updateContributionImages();window.dispatchEvent(new Event('rainbow-motion'))}
motionButton.hidden=false;motionButton.addEventListener('click',()=>changeMotion(!paused));
reduced.addEventListener('change',e=>changeMotion(e.matches||read('rainbow-motion')==='paused',false));
document.addEventListener('visibilitychange',()=>{updateContributionImages();window.dispatchEvent(new Event('rainbow-motion'))});
setTheme(theme);setLanguage(lang);openHash();
const canvas=q('#curiosity-field');const ctx=canvas.getContext('2d');if(!ctx)return;
canvas.parentElement.classList.add('canvas-ready');
let width=1,height=1,scale=1,frame=0,last=0,time=0,onScreen=true;
const TAU=Math.PI*2;
function project(x,y,z){const tilt=.42;const ry=y*Math.cos(tilt)-z*Math.sin(tilt),rz=y*Math.sin(tilt)+z*Math.cos(tilt);const p=3.7/(3.7+rz);return[width*.5+x*scale*p,height*.5+ry*scale*p,rz]}
function point(a,ring,t){const lat=(ring/19-.5)*Math.PI*.92;const r=Math.cos(lat)*(1+.07*Math.sin(a*3+t*.35+ring*.13));const x=r*Math.cos(a),y=Math.sin(lat),z=r*Math.sin(a);const rot=t*.13;return project(x*Math.cos(rot)+z*Math.sin(rot),y,-x*Math.sin(rot)+z*Math.cos(rot))}
function draw(){ctx.clearRect(0,0,width,height);const light=theme==='light';const gradient=ctx.createRadialGradient(width*.5,height*.5,0,width*.5,height*.5,scale*1.5);gradient.addColorStop(0,light?'rgba(87,128,190,.08)':'rgba(96,144,217,.12)');gradient.addColorStop(1,'rgba(60,100,170,0)');ctx.fillStyle=gradient;ctx.fillRect(0,0,width,height);for(let ring=0;ring<20;ring++){const hue=207+ring*3.2;ctx.beginPath();for(let j=0;j<=110;j++){const p=point(j/110*TAU,ring,time);if(!j)ctx.moveTo(p[0],p[1]);else ctx.lineTo(p[0],p[1])}ctx.strokeStyle='hsla('+hue+', '+(light?45:55)+'%, '+(light?42:73)+'%, '+(light?.33:.27)+')';ctx.lineWidth=.7;ctx.stroke();for(let j=0;j<10;j++){const p=point(j/10*TAU+time*.08,ring,time);const alpha=Math.max(.12,.6-(p[2]+1)*.2);ctx.fillStyle='hsla('+hue+',55%,'+(light?40:77)+'%,'+alpha+')';ctx.beginPath();ctx.arc(p[0],p[1],p[2]<0?1.5:1,0,TAU);ctx.fill()}}for(let i=0;i<3;i++){ctx.beginPath();for(let j=0;j<=150;j++){const a=j/150*TAU;const tilt=i*.7-.7;const r=1.25+i*.04;const x=Math.cos(a)*r,y=Math.sin(a)*Math.sin(tilt)*r,z=Math.sin(a)*Math.cos(tilt)*r;const p=project(x,y,z);if(j===0)ctx.moveTo(p[0],p[1]);else ctx.lineTo(p[0],p[1])}ctx.strokeStyle=light?'rgba(128,95,52,.32)':'rgba(210,182,141,.27)';ctx.lineWidth=.8;ctx.stroke()}}
function resize(){const box=canvas.getBoundingClientRect();width=Math.max(1,box.width);height=Math.max(1,box.height);const dpr=Math.min(devicePixelRatio||1,2);canvas.width=Math.round(width*dpr);canvas.height=Math.round(height*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);scale=Math.min(width,height)*.33;draw()}
function tick(now){frame=0;if(paused||document.hidden||!onScreen)return;if(now-last>=32){time+=Math.min((now-last)/1000,.05);last=now;draw()}frame=requestAnimationFrame(tick)}
function refresh(){if(frame){cancelAnimationFrame(frame);frame=0}draw();if(!paused&&!document.hidden&&onScreen){last=performance.now();frame=requestAnimationFrame(tick)}}
window.addEventListener('rainbow-motion',refresh);window.addEventListener('rainbow-theme',draw);
if('IntersectionObserver'in window)new IntersectionObserver(entries=>{onScreen=entries[0].isIntersecting;refresh()},{rootMargin:'100px'}).observe(canvas);
if('ResizeObserver'in window)new ResizeObserver(resize).observe(canvas.parentElement);else window.addEventListener('resize',resize);resize();refresh();
})();
