"""Generate synchronized GitHub profiles from the shared Fieldnotes catalog."""
from pathlib import Path
from html import escape
import json
from profile_components import SKILLS, button, generate, svg, text, lines
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/components'
SITE='https://rainbowyuyu.github.io/rainbowyuyu/'
RAW='https://raw.githubusercontent.com/rainbowyuyu/rainbowyuyu/main/'
PROJECTS=json.loads((ROOT/'assets/catalog/projects.json').read_text(encoding='utf-8'))

def source(path):
    # Relative GitHub /raw redirects discard version query parameters.
    return RAW+path if '?v=' in path else path

def picture(dark,light,alt,width=None,height=None):
    size=(f' width="{width}"' if width else '')+(f' height="{height}"' if height else '')
    return f'<picture><source media="(prefers-color-scheme: dark)" srcset="{source(dark)}"/><source media="(prefers-color-scheme: light)" srcset="{source(light)}"/><img src="{source(light)}"{size} alt="{escape(alt,quote=True)}"/></picture>'

def component(stem,alt,width=None,height=None):
    result=picture(f'assets/components/{stem}-dark.svg?v=fieldnotes-v7',f'assets/components/{stem}-light.svg?v=fieldnotes-v7',alt,width,height)
    if stem.startswith(('project-','skills-','drawer-')):
        narrow=''.join(f'<source media="(max-width: 600px) and (prefers-color-scheme: {theme})" srcset="{source(f"assets/components/{stem}-mobile-{theme}.svg?v=fieldnotes-v7")}"/>' for theme in ('dark','light'))
        result=result.replace('<picture>','<picture>'+narrow,1)
    return result

def action(stem,zh,en,url,lang,icon='arrow',width=220):
    label=en if lang=='en' else zh
    for theme in ('light','dark'):
        (OUT/f'button-{stem}-{lang}-{theme}.svg').write_text(button(label,theme,width=width,icon=icon),encoding='utf-8')
    return f'<a href="{escape(url,quote=True)}">'+component(f'button-{stem}-{lang}',label,height='42')+'</a>'

def drawer(stem,zh,en,lang):
    label=en if lang=='en' else zh
    hint='Click to expand / collapse' if lang=='en' else '点击展开 / 收起'
    for theme in ('light','dark'):
        bg,ink,muted=('#202c30','#edf1e9','#bac7c6') if theme=='dark' else ('#f1eee5','#263e43','#52666a')
        body=f'<rect x="1" y="1" width="1198" height="126" rx="26" fill="{bg}"/>'
        for i,color in enumerate(['#c78371','#d1ad72','#8eb79b','#83a8b8','#b4a0c4']):
            body+=f'<path d="M{30+i*6} 38v48" stroke="{color}" stroke-width="6" stroke-linecap="round"/>'
        body+=text(90,57,label,29,ink,600)+text(92,94,hint,19,muted)
        body+=f'<circle cx="1139" cy="64" r="30" fill="{ink}"/><path d="M1128 64h22m-11-11v22" stroke="{bg}" stroke-width="2.5" stroke-linecap="round"/>'
        (OUT/f'drawer-{stem}-{lang}-{theme}.svg').write_text(svg(1200,128,label+' — '+hint,body),encoding='utf-8')
        body=f'<rect width="640" height="188" rx="26" fill="{bg}"/>'
        for i,color in enumerate(['#c78371','#d1ad72','#8eb79b','#83a8b8','#b4a0c4']):body+=f'<path d="M{20+i*5} 40v100" stroke="{color}" stroke-width="5" stroke-linecap="round"/>'
        for i,line in enumerate(lines(label,28 if lang=='en' else 16)):body+=text(64,57+i*38,line,30,ink,600)
        body+=text(64,148,hint,24,muted)+f'<circle cx="584" cy="94" r="25" fill="{ink}"/><path d="M574 94h20m-10-10v20" stroke="{bg}" stroke-width="2"/>'
        (OUT/f'drawer-{stem}-{lang}-mobile-{theme}.svg').write_text(svg(640,188,label+' — '+hint,body),encoding='utf-8')
    return '<summary>'+component(f'drawer-{stem}-{lang}',label+' · '+hint,'100%')+'</summary>'

def metric(stem,alt,width):
    return picture(f'github-metrics/{stem}-dark.svg?v=studio-v6',f'github-metrics/{stem}-light.svg?v=studio-v6',alt,width)

def landscape():
    prefix='profile-3d-contrib/profile-rainbow-'
    reduced=''.join(f'<source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: {theme})" srcset="{source(prefix+theme+"-static.svg?v=studio-v6")}"/>' for theme in ('dark','light'))
    return picture(prefix+'dark.svg?v=studio-v6',prefix+'light.svg?v=studio-v6','Rainbow contribution landscape','100%').replace('<picture>','<picture>'+reduced,1)

def project(p,lang):
    en=lang=='en';site=SITE+('?lang=en' if en else '')
    title=p['en'] if en else p['name']
    hint='Click to explore / fold' if en else '点击展开项目介绍 / 收起'
    url=site+p['url'] if p['url'].startswith('#') else p['url']
    parts=['<details>','<summary>'+component('project-'+p['slug']+'-'+lang,title+' — '+hint,'100%')+'</summary>','',
        '<p>'+escape(p['en_desc'] if en else p['desc'])+'</p>',
        '<p><sub>'+escape(p['en_status'] if en else p['status'])+' · '+escape(' / '.join(p['tags']))+'</sub></p>',
        '<p>'+action(p['slug'],'查看项目','Explore project',url,lang,width=224)]
    if p['repo'] and not url.startswith('https://github.com/'):
        parts.append(action('source','查看源码','Source code','https://github.com/rainbowyuyu/'+p['repo'],lang,'code'))
    return '\n'.join(parts+['</p>','','</details>'])

def main():
    generate()
    for lang in ('zh','en'):
        en=lang=='en';site=SITE+('?lang=en' if en else '');tr=lambda z,e:e if en else z
        blocks=['<!-- Generated by scripts/generate_readme.py from assets/catalog/projects.json. -->',
            '<p align="right">'+('<a href="README.md">简体中文</a> / <strong>English</strong>' if en else '<strong>简体中文</strong> / <a href="README.en.md">English</a>')+'</p>',
            '<a href="'+site+'">'+picture('assets/readme/profile-banner.svg?v=studio-v6','assets/readme/profile-banner-light.svg?v=studio-v6','rainbow鱼 · 浙江大学博士 / PhD researcher at Zhejiang University','100%')+'</a>',
            '<p align="center">'+action('portfolio','个人主页','Portfolio',site,lang,'leaf',196)+' '+action('work','精选项目','Projects','#projects',lang,'book',196)+' '+action('toolkit','我的工具','Toolkit','#toolbox',lang,'code',196)+' '+action('films','科学影像','Science films','https://space.bilibili.com/343585138',lang,'play')+'</p>',
            '<a id="projects"></a>','## '+tr('在好奇心里，动手。','Ideas, made tangible.'),
            tr('物理研究、工程工具与科学影像。点击卡片，翻开每个项目。','Physics research, engineering tools and visual stories. Open a card to explore the work.')]
        blocks.extend(project(p,lang) for p in PROJECTS[:3])
        blocks+=['<details>',drawer('projects','还有 4 个项目','Four more projects',lang),'']
        blocks.extend(project(p,lang) for p in PROJECTS[3:])
        blocks+=['</details>','<sub>'+tr('研究与开发持续进行，功能与验证范围以各项目文档为准。','Research and development remain ongoing; see each project’s documentation for functionality and validation scope.')+'</sub>',
            '<a id="toolbox"></a>','## '+tr('把想法做出来的工具。','Tools for making ideas real.')]
        for skill in SKILLS:
            blocks.append('<p>'+component('skills-'+skill['id']+'-'+lang,(skill['en'] if en else skill['zh'])+' · '+', '.join(skill['tools']),'100%')+'</p>')
        icons=' '.join(f'<img src="assets/widgets/{stem}.svg" width="48" height="48" alt="{label}"/>' for stem,label in [('python','Python'),('cpp','C++'),('mysql','MySQL'),('java','Java'),('docker','Docker'),('github','GitHub')])
        blocks+=['<details>',drawer('tools','工具架上的小图标','Icons from the toolbox',lang),'<p>'+icons+'</p>','<p><img src="assets/widgets/skills.svg" width="680" alt="PyTorch, C, Markdown, LaTeX, MATLAB, Photoshop, Premiere, After Effects, Audition, Git"/></p>','</details>',
            '<a id="activity"></a>','## '+tr('日复一日，留下痕迹。','Small steps, day by day.'),
            '<p>'+metric('base','GitHub public activity','400')+' '+metric('languages.indepth','Public source languages','400')+'</p>',
            '<p>'+metric('habits.charts','Activity rhythm','400')+' '+metric('wakatime','WakaTime recorded activity','400')+'</p>',
            '<p align="center">'+metric('streak','Contribution streak','90%')+'</p>',landscape(),
            '<details>',drawer('activity','贡献动画与更多记录','Contribution motion & more records',lang),
            '<picture><source media="(prefers-color-scheme: dark)" srcset="profile-snake-contrib/github-contribution-grid-snake-dark.svg"/><img src="profile-snake-contrib/github-contribution-grid-snake.svg" width="100%" alt="Animated contribution snake"/></picture>',
            '<p>'+metric('calendar.full','Contribution calendar','100%')+'</p>','<p>'+metric('activity','Recent public activity','100%')+'</p>','</details>',
            '<sub>'+tr('每日任务更新卡片。WakaTime 为最近 7 天真实记录；来源不可用时保留上次快照，请以卡片时间和更新状态判断时效。','Daily jobs refresh stored cards. WakaTime shows measured activity over seven days. Unavailable sources retain their last snapshot; check timestamps and update status for freshness.')+'</sub>',
            '<details>',drawer('archive','历史卡片与更新记录','Card archive & update records',lang),
            '<p>'+action('archive','历史卡片','Card archive','github-metrics/',lang,'book')+' '+action('status','更新状态','Update status','assets/profile/activity-status.json',lang,'leaf')+' '+action('actions','自动更新','Automation','https://github.com/rainbowyuyu/rainbowyuyu/actions',lang,'code')+'</p>',
            '<p><sub>'+tr('目录中的旧版卡片为历史快照，不代表当前统计。','Older cards in the directory are archived snapshots, not current statistics.')+'</sub></p>','</details>',
            '<p align="center"><sub>'+tr('保持好奇，持续创造。','Stay curious. Keep creating.')+' · <a href="assets/readme/ATTRIBUTION.md">'+tr('素材与致谢','Artwork & credits')+'</a></sub></p>']
        (ROOT/('README.en.md' if en else 'README.md')).write_text('\n\n'.join(blocks).rstrip()+'\n',encoding='utf-8',newline='\n')
    print('Generated bilingual profiles, themed actions and disclosure drawers.')

if __name__=='__main__':main()
