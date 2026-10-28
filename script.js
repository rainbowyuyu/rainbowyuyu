/* Dependency-free progressive enhancement. All project content remains readable without JavaScript. */
(() => {
'use strict';
const root=document.documentElement;
const q=s=>document.querySelector(s), qa=s=>[...document.querySelectorAll(s)];
const read=k=>{try{return localStorage.getItem(k)}catch{return null}};
const save=(k,v)=>{try{localStorage.setItem(k,v)}catch{}};
const params=new URLSearchParams(location.search);
let lang=params.get('lang')==='en'?'en':params.get('lang')==='zh'?'zh':read('rainbow-language')==='en'?'en':'zh';
const systemTheme=matchMedia('(prefers-color-scheme: dark)');
const THEME_KEY='rainbow-theme-v2';
const validThemeChoice=value=>['system','light','dark'].includes(value)?value:'system';
let themeChoice=validThemeChoice(read(THEME_KEY));
const resolveTheme=()=>themeChoice==='system'?(systemTheme.matches?'dark':'light'):themeChoice;
let theme=resolveTheme();
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
let paused=reduced.matches||read('rainbow-motion')==='paused';
let statusData=null;let statusLoaded=false;
const tr=(z,e)=>lang==='en'?e:z;
const languageButton=q('#language-toggle'),themeButton=q('#theme-toggle'),motionButton=q('#motion-toggle');
const themeControl=q('.theme-control'),themeMenu=q('#theme-menu'),themeOptions=qa('[data-theme-choice]');
const projects=qa('.project-details'),expandButton=q('#expand-projects');
let savedOpen;try{savedOpen=JSON.parse(read('rainbow-projects'))}catch{}
if(Array.isArray(savedOpen))projects.forEach(p=>p.open=savedOpen.includes(p.closest('.project-row').id));
function updateProjectButtons(){
 qa('details').forEach(p=>{const label=p.querySelector('.disclosure-label');if(label)label.textContent=p.open?tr('收起','Collapse'):tr('展开','Expand')});
 projects.forEach(p=>{const label=p.querySelector('.expand-label');if(label)label.textContent=p.open?tr('收起','Collapse'):tr('展开','Explore')});
 const all=projects.every(p=>p.open);
 expandButton.textContent=all?tr('收起全部介绍','Collapse all details'):tr('展开全部介绍','Expand all details');
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
  const src=img.dataset.activitySource||img.getAttribute('src')||'';
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
 motionButton.querySelector('.motion-icon').textContent='';
 motionButton.querySelector('.motion-label').textContent=paused?tr('开启动效','Enable motion'):tr('暂停动效','Pause motion');
 motionButton.setAttribute('aria-label',paused?tr('开启首页与贡献动画','Enable hero and contribution animation'):tr('暂停首页与贡献动画','Pause hero and contribution animation'));
}
function setLanguage(next,writeURL=false){
 lang=next;root.lang=lang==='en'?'en':'zh-CN';save('rainbow-language',lang);
 qa('[data-zh][data-en]').forEach(el=>{el.replaceChildren(...el.dataset[lang].split('<br>').flatMap((text,i)=>i?[document.createElement('br'),document.createTextNode(text)]:[document.createTextNode(text)]))});
 qa('[data-label-zh]').forEach(el=>el.setAttribute('aria-label',el.dataset[lang==='en'?'labelEn':'labelZh']));
 qa('[data-alt-zh]').forEach(el=>el.alt=el.dataset[lang==='en'?'altEn':'altZh']);
 qa('[data-placeholder-zh]').forEach(el=>el.placeholder=el.dataset[lang==='en'?'placeholderEn':'placeholderZh']);
 document.title=tr('rainbow鱼 · 浙江大学博士在读 | Research. Build. Create.','rainbow鱼 · PhD student at Zhejiang University');
 q('meta[name=description]').content=tr('rainbow鱼，浙江大学博士在读。探索物理 AI、工程智能体与科学可视化。精选项目：PhysCast、OmniForge、Wiscomper。','rainbow鱼, PhD student at Zhejiang University. Exploring physical AI, engineering agents and scientific visualization. Selected projects: PhysCast, OmniForge, Wiscomper.');
 q('meta[property="og:title"]').content=document.title;
 q('meta[property="og:description"]').content=q('meta[name=description]').content;
 languageButton.textContent=lang==='en'?'中':'EN';languageButton.lang=lang==='en'?'zh-CN':'en';
 languageButton.setAttribute('aria-label',lang==='en'?'切换到中文':'Switch to English');
 updateThemeControl();
 updateProjectButtons();updateMotionLabels();if(statusLoaded)updateStatus();
 if(writeURL){const url=new URL(location.href);url.searchParams.set('lang',lang);history.replaceState(null,'',url)}
}
function updateThemedArtwork(){
 qa('picture source[data-theme-source]').forEach(source=>{source.media=theme==='dark'?'all':'not all'});
 qa('img[data-dark-src][data-light-src]').forEach(img=>{if(!img.closest('picture')){const src=theme==='dark'?img.dataset.darkSrc:img.dataset.lightSrc;if(img.getAttribute('src')!==src)img.src=src}});
 qa('a[data-dark-href][data-light-href]').forEach(a=>{a.href=theme==='dark'?a.dataset.darkHref:a.dataset.lightHref});
}
function updateThemeControl(){
 const choiceLabel=themeChoice==='system'?tr('跟随系统','System'):themeChoice==='dark'?tr('深色','Dark'):tr('浅色','Light');
 const resolvedLabel=theme==='dark'?tr('当前深色','Currently dark'):tr('当前浅色','Currently light');
 const label=tr('外观：','Appearance: ')+choiceLabel+(themeChoice==='system'?' · '+resolvedLabel:'');
 themeButton.setAttribute('aria-label',label);themeButton.title=label;
 q('#theme-resolved').textContent=resolvedLabel;
 themeOptions.forEach(option=>option.setAttribute('aria-checked',String(option.dataset.themeChoice===themeChoice)));
}
function setTheme(next){
 theme=next;root.dataset.theme=theme;root.dataset.themePreference=themeChoice;
 q('meta[name=theme-color]').content=theme==='dark'?'#182126':'#faf8f2';
 updateThemeControl();
 updateThemedArtwork();updateContributionImages();window.dispatchEvent(new Event('rainbow-theme'));
}
function setThemePreference(next,persist=true){
 themeChoice=validThemeChoice(next);if(persist)save(THEME_KEY,themeChoice);setTheme(resolveTheme());
}
function closeThemeMenu(restoreFocus=false){
 themeMenu.hidden=true;themeButton.setAttribute('aria-expanded','false');
 if(restoreFocus)themeButton.focus();
}
function openThemeMenu(index=themeOptions.findIndex(option=>option.dataset.themeChoice===themeChoice)){
 themeMenu.hidden=false;themeButton.setAttribute('aria-expanded','true');
 (themeOptions[index]||themeOptions[0]).focus();
}
systemTheme.addEventListener('change',()=>{if(themeChoice==='system')setTheme(resolveTheme())});
window.addEventListener('storage',event=>{if(event.key===THEME_KEY||event.key===null)setThemePreference(read(THEME_KEY),false)});
projects.forEach(p=>p.addEventListener('toggle',()=>{updateProjectButtons();save('rainbow-projects',JSON.stringify(projects.filter(x=>x.open).map(x=>x.closest('.project-row').id)))}));
qa('.activity-more').forEach(p=>p.addEventListener('toggle',updateProjectButtons));
expandButton.hidden=false;expandButton.addEventListener('click',()=>{const open=!projects.every(p=>p.open);projects.forEach(p=>{p.open=open});updateProjectButtons()});
languageButton.hidden=false;languageButton.addEventListener('click',()=>setLanguage(lang==='en'?'zh':'en',true));
themeButton.hidden=false;themeButton.addEventListener('click',()=>themeMenu.hidden?openThemeMenu():closeThemeMenu());
themeButton.addEventListener('keydown',event=>{if(event.key==='ArrowDown'||event.key==='ArrowUp'){event.preventDefault();openThemeMenu(event.key==='ArrowDown'?0:themeOptions.length-1)}});
themeOptions.forEach(option=>option.addEventListener('click',()=>{setThemePreference(option.dataset.themeChoice);closeThemeMenu(true)}));
themeMenu.addEventListener('keydown',event=>{
 if(event.key==='Tab'){closeThemeMenu();themeButton.focus();return}
 const index=themeOptions.indexOf(document.activeElement);let next;
 if(event.key==='ArrowDown')next=(index+1)%themeOptions.length;
 if(event.key==='ArrowUp')next=(index-1+themeOptions.length)%themeOptions.length;
 if(event.key==='Home')next=0;if(event.key==='End')next=themeOptions.length-1;
 if(next!==undefined){event.preventDefault();themeOptions[next].focus()}
});
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&!themeMenu.hidden){event.preventDefault();closeThemeMenu(true)}});
document.addEventListener('pointerdown',event=>{if(!themeMenu.hidden&&!themeControl.contains(event.target))closeThemeMenu()});
themeControl.addEventListener('focusout',event=>{if(!themeControl.contains(event.relatedTarget))closeThemeMenu()});
function openHash(){let id;try{id=decodeURIComponent(location.hash.slice(1))}catch{return}const target=document.getElementById(id);if(target&&target.classList.contains('project-row')){target.querySelector('.project-details').open=true;updateProjectButtons()}}
window.addEventListener('hashchange',openHash);qa('a[href^="#"]').forEach(a=>a.addEventListener('click',()=>{const el=document.getElementById(a.hash.slice(1));if(el&&el.classList.contains('project-row'))el.querySelector('.project-details').open=true}));
q('#copyright-year').textContent=String(new Date().getFullYear());
qa('.metric-card img').forEach(img=>{const card=img.closest('.metric-card');const fail=()=>{card.classList.add('is-unavailable');const fallback=card.querySelector('.image-unavailable');if(fallback)fallback.hidden=false};img.addEventListener('error',fail);img.addEventListener('load',()=>{card.classList.remove('is-unavailable');const fallback=card.querySelector('.image-unavailable');if(fallback)fallback.hidden=true});if(img.complete&&!img.naturalWidth)fail()});
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
commands.forEach(a=>a.addEventListener('click',event=>{event.preventDefault();dialog.close();const target=document.getElementById(a.hash.slice(1));if(target){if(target.classList.contains('project-row'))target.querySelector('.project-details').open=true;history.pushState(null,'',a.hash);target.scrollIntoView({behavior:paused?'instant':'smooth',block:'start'});const focus=target.querySelector('h2,h3')||target;if(focus.tagName!=='SUMMARY')focus.tabIndex=-1;focus.focus({preventScroll:true})}}));
dialog.addEventListener('keydown',e=>{if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();const list=visibleCommands();if(!list.length)return;commandIndex=(commandIndex+(e.key==='ArrowDown'?1:-1)+list.length)%list.length;markCommand();list[commandIndex].scrollIntoView({block:'nearest'})}if(e.key==='Enter'&&e.target===search){const target=visibleCommands()[commandIndex];if(target){e.preventDefault();target.click()}}});
document.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();dialog.open?dialog.close():openCommands()}});
if('IntersectionObserver'in window){const links=qa('.site-nav a');const observer=new IntersectionObserver(entries=>{for(const e of entries){if(!e.isIntersecting)continue;links.forEach(a=>{if(a.hash==='#'+e.target.id)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current')})}},{rootMargin:'-15% 0px -55% 0px'});links.forEach(a=>{const el=document.getElementById(a.hash.slice(1));if(el)observer.observe(el)})}
const contributions=qa('.animated-contribution');
contributions.forEach(img=>img.dataset.onScreen='true');
function updateContributionImages(){contributions.forEach(img=>{const playing=!paused&&!document.hidden&&img.dataset.onScreen!=='false';const src=playing?(theme==='light'?img.dataset.lightSrc:img.dataset.animatedSrc):(theme==='light'?img.dataset.lightStaticSrc:img.dataset.staticSrc);const source=img.closest('picture')?.querySelector('[data-motion-source]');if(source){source.media='all';if(source.getAttribute('srcset')!==src)source.srcset=src}if(src&&img.getAttribute('src')!==src)img.src=src})}
if('IntersectionObserver'in window){const observer=new IntersectionObserver(entries=>{entries.forEach(e=>e.target.dataset.onScreen=String(e.isIntersecting));updateContributionImages()},{rootMargin:'150px'});contributions.forEach(img=>observer.observe(img))}
function changeMotion(value,persist=true){paused=value;if(persist)save('rainbow-motion',paused?'paused':'running');updateMotionLabels();updateContributionImages();window.dispatchEvent(new Event('rainbow-motion'))}
motionButton.hidden=false;motionButton.addEventListener('click',()=>changeMotion(!paused));
reduced.addEventListener('change',e=>changeMotion(e.matches||read('rainbow-motion')==='paused',false));
document.addEventListener('visibilitychange',()=>{updateContributionImages();window.dispatchEvent(new Event('rainbow-motion'))});
setThemePreference(themeChoice,false);setLanguage(lang);openHash();
// A quiet, one-time arrival for the illustrations; content is visible without JS.
const arrivals=new Set();
if('IntersectionObserver' in window){
 const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{
  if(!entry.isIntersecting)return;observer.unobserve(entry.target);
  if(paused||reduced.matches||!entry.target.animate)return;
  const shelf=entry.target.closest('.tool-shelf');
  const animation=entry.target.animate(shelf?[{opacity:.6,transform:'translateX(-14px)'},{opacity:1,transform:'none'}]:[{opacity:.6,transform:'translateY(18px) rotate(-1.5deg)'},{opacity:1,transform:'none'}],{duration:shelf?650:850,easing:'cubic-bezier(.16,1,.3,1)'});
  arrivals.add(animation);animation.onfinish=()=>arrivals.delete(animation);
 }),{threshold:.2});
 qa('.folio-art img,.tool-shelf>img,.about-art img').forEach(img=>observer.observe(img));
}
window.addEventListener('rainbow-motion',()=>{if(paused||reduced.matches){arrivals.forEach(animation=>animation.cancel());arrivals.clear()}});
let progressFrame=0;function updateProgress(){progressFrame=0;const length=document.documentElement.scrollHeight-innerHeight;q('.scroll-progress').style.transform='scaleX('+(length>0?scrollY/length:0)+')'}addEventListener('scroll',()=>{if(!progressFrame)progressFrame=requestAnimationFrame(updateProgress)},{passive:true});updateProgress();

})();
