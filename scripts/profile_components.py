"""Rainbow Fieldnotes: shared, editable artwork for the profile component system."""
from pathlib import Path
from html import escape
import base64,json,re
from handpainted_icons import TOOL_ICONS, painted_icon, brush_divider

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/components'
FONT='Segoe UI,Microsoft YaHei,Arial,sans-serif'
COLOURS={
 'physcast':('#2f7090','#8fcde1','#edf4f5','#202f37'),
 'omniforge':('#87652c','#e6c68a','#f8f0df','#342e24'),
 'wiscomper':('#716099','#c5b1e9','#f0ecf6','#2c2938'),
 'ai-engineer':('#366f9b','#9ac9ee','#eaf1f7','#202f3c'),
 'ai-revolution':('#9b613c','#e7b48c','#f7eee4','#382d27'),
 'science-studio':('#337b6a','#9edbc5','#eaf3ec','#22352f'),
 'manim':('#4d7d57','#aed19e','#eff4e9','#29342a')}
SKILLS=[
 dict(id='research',zh='研究与计算',en='Research & computing',art='physcast',desc='从观测与模型，到可以检查的证据。',en_desc='From observations and models to inspectable evidence.',tools=['Python','PyTorch','MATLAB','OpenFAST / FAST.Farm','LaTeX'],more=['C','C++']),
 dict(id='engineering',zh='工程与构建',en='Engineering & building',art='omniforge',desc='让工具协作，让想法成为可运行的作品。',en_desc='Bringing tools together to make ideas run.',tools=['TypeScript','Three.js','Docker','Git','MySQL'],more=['Java','GitHub','Markdown']),
 dict(id='creation',zh='影像与表达',en='Motion & storytelling',art='science-studio',desc='用图像、动画和故事解释复杂问题。',en_desc='Explaining complex ideas through images and motion.',tools=['Manim','Blender','Photoshop','Premiere','After Effects'],more=['Audition'])]

def uri(path):
 p=ROOT/path
 mime={'.png':'image/png','.webp':'image/webp','.jpg':'image/jpeg','.svg':'image/svg+xml'}[p.suffix]
 return 'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode('ascii')

def art(name,x,y,w,h):
 return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="{uri("assets/components/illustrations/"+name+".png")}"/>'

def logo(slug,x,y,size):
 path=ROOT/'assets/projects'/f'{slug}.svg'
 if not path.exists():
  bitmap=ROOT/'assets/projects'/f'{slug}.png'
  return f'<image x="{x}" y="{y}" width="{size}" height="{size}" href="{uri(bitmap.relative_to(ROOT))}"/>' if bitmap.exists() else ''
 raw=path.read_text(encoding='utf-8')
 raw=re.sub(r'<\?xml[^>]*>','',raw)
 raw=re.sub(r'<svg\b[^>]*>',f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 80 80">',raw,count=1) if 'viewBox="0 0 80 80"' in raw else re.sub(r'<svg\b([^>]*)>',lambda m:'<svg '+re.sub(r'\b(?:width|height)="[^"]*"','',m.group(1))+f' x="{x}" y="{y}" width="{size}" height="{size}">',raw,count=1)
 return raw

def text(x,y,value,size=24,fill='#253b42',weight=400):
 return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}">{escape(value)}</text>'

def lines(value,limit):
 import textwrap
 return textwrap.wrap(value,limit,break_long_words=False) if re.search('[a-zA-Z]{4}',value) else [value[i:i+limit] for i in range(0,len(value),limit)]

def svg(w,h,label,body):
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label,quote=True)}"><g font-family="{FONT}">{body}</g></svg>'

def project_card(p,lang,theme,mobile=False):
 dark=theme=='dark'; a,b,bg,db=COLOURS[p['slug']]; accent=b if dark else a; ink='#edf2ed' if dark else '#243a42'; muted='#b9c6c7' if dark else '#52666c'
 title=p['en'] if lang=='en' else p['name']; title={'rainbow鱼 · Science Studio':'Science Studio','rainbow鱼 · 科普工作台':'rainbow鱼 · 科普工作台'}.get(title,title)
 subtitle=p['title'] if lang=='en' else p['zh']
 if mobile:
  body=f'<rect x="1" y="1" width="638" height="688" rx="30" fill="{db if dark else bg}"/>'+art(p['slug'],65,22,510,298)
  body+=logo(p['slug'],36,324,38)+text(89,351,p['tag'].title(),20,muted,500)
  for i,line in enumerate(lines(title,26 if lang=='en' else 19)):body+=text(36,407+i*44,line,40,ink,650)
  y=463 if len(lines(title,26 if lang=='en' else 19))==1 else 495
  for i,line in enumerate(lines(subtitle,35 if lang=='en' else 19)):body+=text(36,y+i*36,line,28,muted)
  body+=f'<rect x="36" y="600" width="264" height="54" rx="27" fill="{accent}"/>'+text(58,636,'Explore / fold' if lang=='en' else '展开项目介绍',26,db if dark else '#ffffff',600)
  body+=painted_icon("expand",263,611,34)
  body+=text(328,635,('Private source' if not p['repo'] else 'Open source') if lang=='en' else ('源码私有' if not p['repo'] else '开源项目'),24,muted)
  return svg(640,690,title+' — '+subtitle,body)
 body=f'<rect x="1" y="1" width="1198" height="478" rx="30" fill="{db if dark else bg}"/>'
 body+=brush_divider(35,35,170,23)
 body+=f'<rect x="46" y="80" width="56" height="56" rx="15" fill="{("#39434a" if dark else "#ffffff")}"/>'+logo(p['slug'],52,86,44)
 body+=text(120,118,p['tag'].replace(' × ',' / ').title(),20,muted,500)
 for i,line in enumerate(lines(title,30 if lang=='en' else 22)):
  body+=text(46,206+i*48,line,44 if len(title)>20 else 52,ink,650)
 y=268 if len(lines(title,30 if lang=='en' else 22))==1 else 298
 for i,line in enumerate(lines(subtitle,43 if lang=='en' else 23)):body+=text(48,y+i*33,line,25,muted)
 label='Explore / fold' if lang=='en' else '展开项目介绍'
 body+=f'<rect x="46" y="382" width="212" height="54" rx="27" fill="{accent}"/>'+text(68,416,label,20,db if dark else '#ffffff',600)
 body+=painted_icon("expand",220,396,29)
 body+=text(284,415,('Private source' if not p['repo'] else 'Open source') if lang=='en' else ('源码私有' if not p['repo'] else '开源项目'),18,muted)
 body+=art(p['slug'],665,32,510,408)
 return svg(1200,480,title+' — '+subtitle,body)

def skill_card(s,lang,theme,mobile=False):
 dark=theme=='dark';ink='#edf2ed' if dark else '#243a42';muted='#b9c6c7' if dark else '#52666c';bg='#202b30' if dark else '#f4f0e5'
 w,h=(640,688) if mobile else (1120,352);cols=3 if mobile else len(s['tools']);step=(w-56)/cols
 body=f'<rect width="{w}" height="{h}" rx="28" fill="{bg}"/>'
 body+=text(32,55,s['en'] if lang=='en' else s['zh'],34 if mobile else 32,ink,650)
 for i,line in enumerate(lines(s['en_desc'] if lang=='en' else s['desc'],42 if mobile and lang=='en' else 23 if mobile else 90)):
  body+=text(32,96+i*30,line,25 if mobile else 22,muted)
 body+=brush_divider(30,134 if mobile else 109,w-60,24)
 for i,tool in enumerate(s['tools']):
  x=28+(i%cols)*step;y=(170 if mobile else 145)+(i//cols)*235;size=144 if mobile else 124;cx=x+step/2
  body+=painted_icon(TOOL_ICONS[tool],cx-size/2,y,size)
  names=tool.split(' / ') if ' / ' in tool else tool.split(' ') if mobile and tool=='After Effects' else [tool]
  for j,name in enumerate(names):
   body+=text(cx,y+size+32+j*31,name,28 if mobile else 23,ink,550).replace('<text ','<text text-anchor="middle" ',1)
 return svg(w,h,(s['en'] if lang=='en' else s['zh'])+' · '+', '.join(s['tools']),body)

def button(label,theme,accent='#287b70',width=198,icon='arrow'):
 dark=theme=='dark';bg='#24332f' if dark else '#edf0e7';ink='#dcebe2' if dark else '#285e52'
 name={'arrow':'compass','code':'github','book':'notebook','play':'film','leaf':'fish','tools':'toolbox','archive':'archive','status':'activity'}.get(icon,icon)
 body=f'<rect x="4" y="3" width="{width-8}" height="130" rx="23" fill="{bg}"/>'+painted_icon(name,width/2-36,10,72)
 body+=text(width/2,110,label,20,ink,600).replace('<text ','<text text-anchor="middle" ',1)
 return svg(width,140,label,body)

def generate():
 OUT.mkdir(exist_ok=True)
 projects=json.loads((ROOT/'assets/catalog/projects.json').read_text(encoding='utf-8'))
 for theme in ('light','dark'):
  for lang in ('zh','en'):
   for mobile in (False,True):
    suffix='-mobile' if mobile else ''
    for p in projects:(OUT/f'project-{p["slug"]}-{lang}{suffix}-{theme}.svg').write_text(project_card(p,lang,theme,mobile),encoding='utf-8')
    for s in SKILLS:(OUT/f'skills-{s["id"]}-{lang}{suffix}-{theme}.svg').write_text(skill_card(s,lang,theme,mobile),encoding='utf-8')
 print('Generated 56 project folios and 24 tool shelves.')

if __name__=='__main__':generate()
