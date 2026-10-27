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
const projects=qa('.project-details'),expandButton=q('#expand-projects');
let savedOpen;try{savedOpen=JSON.parse(read('rainbow-projects'))}catch{}
if(Array.isArray(savedOpen))projects.forEach(p=>p.open=savedOpen.includes(p.closest('.project-row').id));
function updateProjectButtons(){
 projects.forEach(p=>{const label=p.querySelector('.expand-label');if(label)label.textContent=p.open?tr('收起','Collapse'):tr('展开','Explore')});
 const all=projects.every(p=>p.open);
 expandButton.textContent=(all?tr('收起全部介绍','Collapse all details'):tr('展开全部介绍','Expand all details'))+(all?' −':' ＋');
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
 qa('[data-zh][data-en]').forEach(el=>{el.replaceChildren(...el.dataset[lang].split('<br>').flatMap((text,i)=>i?[document.createElement('br'),document.createTextNode(text)]:[document.createTextNode(text)]))});
 qa('[data-label-zh]').forEach(el=>el.setAttribute('aria-label',el.dataset[lang==='en'?'labelEn':'labelZh']));
 qa('[data-alt-zh]').forEach(el=>el.alt=el.dataset[lang==='en'?'altEn':'altZh']);
 qa('[data-placeholder-zh]').forEach(el=>el.placeholder=el.dataset[lang==='en'?'placeholderEn':'placeholderZh']);
 document.title=tr('rainbow鱼 · 浙江大学博士 | Research. Build. Create.','rainbow鱼 · PhD researcher at Zhejiang University');
 q('meta[name=description]').content=tr('rainbow鱼，浙江大学博士。探索物理 AI、工程智能体与科学可视化。精选项目：PhysCast、OmniForge、Wiscomper。','rainbow鱼, PhD researcher at Zhejiang University. Exploring physical AI, engineering agents and scientific visualization. Selected projects: PhysCast, OmniForge, Wiscomper.');
 q('meta[property="og:title"]').content=document.title;
 q('meta[property="og:description"]').content=q('meta[name=description]').content;
 languageButton.textContent=lang==='en'?'中':'EN';languageButton.lang=lang==='en'?'zh-CN':'en';
 languageButton.setAttribute('aria-label',lang==='en'?'切换到中文':'Switch to English');
 themeButton.setAttribute('aria-label',theme==='dark'?tr('切换浅色主题','Switch to light theme'):tr('切换深色主题','Switch to dark theme'));
 updateProjectButtons();updateMotionLabels();if(statusLoaded)updateStatus();
 if(writeURL){const url=new URL(location.href);url.searchParams.set('lang',lang);history.replaceState(null,'',url)}
}
function setTheme(next){theme=next;root.dataset.theme=theme;save('rainbow-theme',theme);themeButton.textContent=theme==='dark'?'☼':'☾';q('meta[name=theme-color]').content=theme==='dark'?'#090e13':'#f2f3ed';themeButton.setAttribute('aria-label',theme==='dark'?tr('切换浅色主题','Switch to light theme'):tr('切换深色主题','Switch to dark theme'));updateContributionImages();window.dispatchEvent(new Event('rainbow-theme'))}
projects.forEach(p=>p.addEventListener('toggle',()=>{updateProjectButtons();save('rainbow-projects',JSON.stringify(projects.filter(x=>x.open).map(x=>x.closest('.project-row').id)))}));
expandButton.hidden=false;expandButton.addEventListener('click',()=>{const open=!projects.every(p=>p.open);projects.forEach(p=>{p.open=open});updateProjectButtons()});
languageButton.hidden=false;languageButton.addEventListener('click',()=>setLanguage(lang==='en'?'zh':'en',true));
themeButton.hidden=false;themeButton.addEventListener('click',()=>setTheme(theme==='dark'?'light':'dark'));
function openHash(){let id;try{id=decodeURIComponent(location.hash.slice(1))}catch{return}const target=document.getElementById(id);if(target&&target.classList.contains('project-row')){target.querySelector('.project-details').open=true;updateProjectButtons()}}
window.addEventListener('hashchange',openHash);qa('a[href^="#"]').forEach(a=>a.addEventListener('click',()=>{const el=document.getElementById(a.hash.slice(1));if(el&&el.classList.contains('project-row'))el.querySelector('.project-details').open=true}));
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
commands.forEach(a=>a.addEventListener('click',event=>{event.preventDefault();dialog.close();const target=document.getElementById(a.hash.slice(1));if(target){if(target.classList.contains('project-row'))target.querySelector('.project-details').open=true;history.pushState(null,'',a.hash);target.scrollIntoView({behavior:paused?'instant':'smooth',block:'start'});const focus=target.querySelector('h2,h3')||target;if(focus.tagName!=='SUMMARY')focus.tabIndex=-1;focus.focus({preventScroll:true})}}));
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
let progressFrame=0;function updateProgress(){progressFrame=0;const length=document.documentElement.scrollHeight-innerHeight;q('.scroll-progress').style.transform='scaleX('+(length>0?scrollY/length:0)+')'}addEventListener('scroll',()=>{if(!progressFrame)progressFrame=requestAnimationFrame(updateProgress)},{passive:true});updateProgress();

/* Aurora shader adapted for this website from React Bits by David Haz.
 * Source: DavidHDev/react-bits at e12c22192ac7b4b452c5e2feb9b586d74765d696,
 * src/content/Backgrounds/Aurora/Aurora.jsx. MIT + Commons Clause.
 * Terms: assets/licenses/react-bits-LICENSE.txt. Native WebGL; no dependencies.
 */
const canvas=q('#aurora-canvas'),stage=q('.aurora-stage');
const gl=canvas.getContext('webgl2',{alpha:true,premultipliedAlpha:true,antialias:false,depth:false,stencil:false});
if(!gl)return;
const vertexSource=['#version 300 es','in vec2 aPosition;','void main(){gl_Position=vec4(aPosition,0.0,1.0);}'].join('\n');
const fragmentSource=[
 '#version 300 es',
 'precision highp float;',
 'uniform vec2 uResolution; uniform float uTime; uniform float uPointer; out vec4 outColor;',
 'vec3 permute(vec3 x){return mod(((x*34.0)+1.0)*x,289.0);}',
 'float snoise(vec2 v){',
 'const vec4 C=vec4(.211324865405187,.366025403784439,-.577350269189626,.024390243902439);',
 'vec2 i=floor(v+dot(v,C.yy));vec2 x0=v-i+dot(i,C.xx);',
 'vec2 i1=x0.x>x0.y?vec2(1.,0.):vec2(0.,1.);',
 'vec4 x12=x0.xyxy+C.xxzz;x12.xy-=i1;i=mod(i,289.);',
 'vec3 p=permute(permute(i.y+vec3(0.,i1.y,1.))+i.x+vec3(0.,i1.x,1.));',
 'vec3 m=max(.5-vec3(dot(x0,x0),dot(x12.xy,x12.xy),dot(x12.zw,x12.zw)),0.);m=m*m;m=m*m;',
 'vec3 x=2.*fract(p*C.www)-1.;vec3 h=abs(x)-.5;vec3 ox=floor(x+.5);vec3 a0=x-ox;',
 'm*=1.79284291400159-.85373472095314*(a0*a0+h*h);',
 'vec3 g;g.x=a0.x*x0.x+h.x*x0.y;g.yz=a0.yz*x12.xz+h.yz*x12.yw;return 130.*dot(m,g);}',
 'float smoother(float a,float b,float x){float t=clamp((x-a)/(b-a),0.,1.);return t*t*t*(t*(t*6.-15.)+10.);}',
 'void main(){',
 'vec2 uv=gl_FragCoord.xy/uResolution;float X=(gl_FragCoord.x-uResolution.x*.5)/uResolution.y;',
 'float y=1.-uv.y;float t=uTime;vec3 glow=vec3(0.);float cover=0.;',
 'for(int k=0;k<3;k++){',
 'float layer=float(k);float seed=layer*13.7;float pace=t*(1.-layer*.18);',
 'float warp=snoise(vec2(X*.45+pace*.02+seed,pace*.05+seed));',
 'float wave=snoise(vec2(X*.75+warp*.35-pace*.03+seed,pace*.07-seed))*.72+snoise(vec2(X*1.6+warp*.5+pace*.04-seed,pace*.1+seed*.5))*.28;',
 'float hem=.23+layer*.075+wave*.18+exp(-pow((X-uPointer)/.5,2.))*.025;',
 'float rise=hem-y;float body=pow(smoother(-.16,.38,rise),1.9);',
 'float alpha=body*(.86+.14*snoise(vec2(X*.9-pace*.025+seed,y*.3+pace*.04)))*(k==0?1.:.32/layer);',
 'vec3 tint=mix(vec3(.37,.78,.66),vec3(.55,.49,.85),smoother(.15,.95,uv.x+wave*.1));',
 'glow=1.-(1.-glow)*(1.-tint*alpha);cover=1.-(1.-cover)*(1.-alpha);}',
 'float noise=fract(sin(dot(gl_FragCoord.xy,vec2(12.9898,78.233)))*43758.5453)-.5;',
 'outColor=vec4(glow*.72+noise/255.,clamp(cover*.82,0.,1.));}'
].join('\n');
function compile(type,source){
 const shader=gl.createShader(type);gl.shaderSource(shader,source);gl.compileShader(shader);
 if(gl.getShaderParameter(shader,gl.COMPILE_STATUS))return shader;
 gl.deleteShader(shader);return null;
}
const vertex=compile(gl.VERTEX_SHADER,vertexSource),fragment=compile(gl.FRAGMENT_SHADER,fragmentSource);
if(!vertex||!fragment)return;
const program=gl.createProgram();gl.attachShader(program,vertex);gl.attachShader(program,fragment);
gl.bindAttribLocation(program,0,'aPosition');gl.linkProgram(program);gl.deleteShader(vertex);gl.deleteShader(fragment);
if(!gl.getProgramParameter(program,gl.LINK_STATUS))return;
const buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);
gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);
gl.enableVertexAttribArray(0);gl.vertexAttribPointer(0,2,gl.FLOAT,false,0,0);
const uniforms=Object.fromEntries(['uResolution','uTime','uPointer'].map(name=>[name,gl.getUniformLocation(program,name)]));
let frame=0,clock=7,last=0,visible=true,pointer=0,targetPointer=0,lost=false;
function renderAurora(){
 if(lost)return;
 gl.viewport(0,0,canvas.width,canvas.height);gl.useProgram(program);
 gl.uniform2f(uniforms.uResolution,canvas.width,canvas.height);gl.uniform1f(uniforms.uTime,clock);gl.uniform1f(uniforms.uPointer,pointer);
 gl.drawArrays(gl.TRIANGLES,0,3);
}
function tickAurora(now){
 frame=0;if(paused||document.hidden||!visible||lost)return;
 if(now-last>=32){const elapsed=Math.min((now-last)/1000,.05);last=now;clock+=elapsed*.65;pointer+=(targetPointer-pointer)*.035;renderAurora();}
 frame=requestAnimationFrame(tickAurora);
}
function wakeAurora(){
 if(frame)cancelAnimationFrame(frame);frame=0;renderAurora();
 if(!paused&&visible&&!document.hidden&&!lost){last=performance.now();frame=requestAnimationFrame(tickAurora);}
}
function resizeAurora(){
 const rect=stage.getBoundingClientRect();const ratio=Math.min(devicePixelRatio||1,innerWidth<700?1:1.5);
 canvas.width=Math.max(1,Math.round(rect.width*ratio));canvas.height=Math.max(1,Math.round(rect.height*ratio));wakeAurora();
}
q('.hero').addEventListener('pointermove',event=>{const rect=stage.getBoundingClientRect();targetPointer=(event.clientX-rect.left-rect.width/2)/rect.height;},{passive:true});
window.addEventListener('rainbow-motion',wakeAurora);window.addEventListener('rainbow-theme',renderAurora);
canvas.addEventListener('webglcontextlost',event=>{event.preventDefault();lost=true;cancelAnimationFrame(frame);stage.classList.remove('aurora-ready');});
if('ResizeObserver'in window)new ResizeObserver(resizeAurora).observe(stage);else addEventListener('resize',resizeAurora);
if('IntersectionObserver'in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;wakeAurora();},{rootMargin:'100px'}).observe(stage);
stage.classList.add('aurora-ready');resizeAurora();
})();
