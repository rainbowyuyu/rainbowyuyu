"""Generate synchronized GitHub profiles from the shared Fieldnotes catalog."""
from pathlib import Path
from html import escape
import json
from profile_components import SKILLS, button, generate, svg, text, lines, skill_card
from handpainted_icons import painted_icon, brush_divider
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
    result=picture(f'assets/components/{stem}-dark.svg?v=icons-v8',f'assets/components/{stem}-light.svg?v=icons-v8',alt,width,height)
    if stem.startswith(('project-','skills-','drawer-')):
        narrow=''.join(f'<source media="(max-width: 600px) and (prefers-color-scheme: {theme})" srcset="{source(f"assets/components/{stem}-mobile-{theme}.svg?v=icons-v8")}"/>' for theme in ('dark','light'))
        result=result.replace('<picture>','<picture>'+narrow,1)
    return result

def action(stem,zh,en,url,lang,icon='arrow',width=220):
    label=en if lang=='en' else zh
    for theme in ('light','dark'):
        (OUT/f'button-{stem}-{lang}-{theme}.svg').write_text(button(label,theme,width=width,icon=icon),encoding='utf-8')
    return f'<a href="{escape(url,quote=True)}">'+component(f'button-{stem}-{lang}',label,height='100')+'</a>'

def drawer(stem,zh,en,lang):
    label=en if lang=='en' else zh
    hint='Click to expand / collapse' if lang=='en' else '点击展开 / 收起'
    for theme in ('light','dark'):
        bg,ink,muted=('#202c30','#edf1e9','#bac7c6') if theme=='dark' else ('#f1eee5','#263e43','#52666a')
        motif={'projects':'compass','tools':'toolbox','activity':'calendar','archive':'archive'}[stem]
        for mobile in (False,True):
            w,h=(640,194) if mobile else (1200,138)
            body=f'<rect width="{w}" height="{h}" rx="26" fill="{bg}"/>'
            body+=painted_icon(motif,14,32 if mobile else 22,78)
            label_lines=lines(label,25 if mobile and lang=='en' else 14 if mobile else 80)
            for i,line in enumerate(label_lines):body+=text(108,61+i*37,line,30 if mobile else 29,ink,600)
            body+=text(108,150 if mobile else 101,hint,23 if mobile else 20,muted)
            body+=painted_icon('expand',w-80,h/2-31,62)
            body+=brush_divider(30,h-28,w-60,18)
            suffix='-mobile' if mobile else ''
            (OUT/f'drawer-{stem}-{lang}{suffix}-{theme}.svg').write_text(svg(w,h,label+' — '+hint,body),encoding='utf-8')
    return '<summary>'+component(f'drawer-{stem}-{lang}',label+' · '+hint,'100%')+'</summary>'

def metric(stem,alt,width):
    return picture(f'github-metrics/{stem}-dark.svg?v=icons-v8',f'github-metrics/{stem}-light.svg?v=icons-v8',alt,width)

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

def section_heading(label):
    return '<p><img src="'+RAW+'assets/components/icons/divider-fish.png?v=icons-v8" width="100%" alt=""/></p><h3>'+escape(label)+'</h3>'

def main():
    generate()
    for lang in ('zh','en'):
        en=lang=='en';site=SITE+('?lang=en' if en else '');tr=lambda z,e:e if en else z
        blocks=['<!-- Generated by scripts/generate_readme.py from assets/catalog/projects.json. -->',
            '<p align="right">'+('<a href="README.md">简体中文</a> / <strong>English</strong>' if en else '<strong>简体中文</strong> / <a href="README.en.md">English</a>')+'</p>',
            '<a href="'+site+'">'+picture('assets/readme/profile-banner.svg?v=phd-student-v1','assets/readme/profile-banner-light.svg?v=phd-student-v1','rainbow鱼 · 浙江大学博士在读 / PhD student at Zhejiang University','100%')+'</a>',
            '<p align="center">'+action('portfolio','个人主页','Portfolio',site,lang,'leaf',196)+' '+action('work','精选项目','Projects','#projects',lang,'book',196)+' '+action('toolkit','我的工具','Toolkit','#toolbox',lang,'tools',196)+' '+action('films','科学影像','Science films','https://space.bilibili.com/343585138',lang,'play')+'</p>',
            '<a id="projects"></a>',section_heading(tr('在好奇心里，动手。','Ideas, made tangible.')),
            tr('物理研究、工程工具与科学影像。点击卡片，翻开每个项目。','Physics research, engineering tools and visual stories. Open a card to explore the work.')]
        blocks.extend(project(p,lang) for p in PROJECTS[:3])
        blocks+=['<details>',drawer('projects','还有 4 个项目','Four more projects',lang),'']
        blocks.extend(project(p,lang) for p in PROJECTS[3:])
        blocks+=['</details>','<sub>'+tr('研究与开发持续进行，功能与验证范围以各项目文档为准。','Research and development remain ongoing; see each project’s documentation for functionality and validation scope.')+'</sub>',
            '<a id="toolbox"></a>',section_heading(tr('把想法做出来的工具。','Tools for making ideas real.'))]
        for skill in SKILLS:
            blocks.append('<p>'+component('skills-'+skill['id']+'-'+lang,(skill['en'] if en else skill['zh'])+' · '+', '.join(skill['tools']),'100%')+'</p>')
        more=dict(id='extra',zh='更多工具',en='More tools',desc='工具因问题而选，作品随好奇心展开。',en_desc='Different tools for different questions.',tools=['C','C++','Java','GitHub','Markdown','Audition'])
        for theme in ('light','dark'):
            for mobile in (False,True):
                suffix='-mobile' if mobile else ''
                (OUT/f'skills-extra-{lang}{suffix}-{theme}.svg').write_text(skill_card(more,lang,theme,mobile),encoding='utf-8')
        blocks+=['<details>',drawer('tools','更多工具与熟悉的伙伴','More tools & familiar companions',lang),'<p>'+component('skills-extra-'+lang,', '.join(more['tools']),'100%')+'</p>','</details>',
            '<a id="activity"></a>',section_heading(tr('日复一日，留下痕迹。','Small steps, day by day.')),
            '<p>'+metric('base','GitHub public activity','400')+' '+metric('languages.indepth','Public source languages','400')+'</p>',
            '<p>'+metric('habits.charts','Activity rhythm','400')+' '+metric('wakatime','WakaTime recorded activity','400')+'</p>',
            '<p align="center">'+metric('streak','Contribution streak','90%')+'</p>',landscape(),
            '<details>',drawer('activity','贡献动画与更多记录','Contribution motion & more records',lang),
            '<picture><source media="(prefers-color-scheme: dark)" srcset="profile-snake-contrib/github-contribution-grid-snake-dark.svg"/><img src="profile-snake-contrib/github-contribution-grid-snake.svg" width="100%" alt="Animated contribution snake"/></picture>',
            '<p>'+metric('calendar.full','Contribution calendar','100%')+'</p>','<p>'+metric('activity','Recent public activity','100%')+'</p>','</details>',
            '<sub>'+tr('每日任务更新卡片。WakaTime 为最近 7 天真实记录；来源不可用时保留上次快照，请以卡片时间和更新状态判断时效。','Daily jobs refresh stored cards. WakaTime shows measured activity over seven days. Unavailable sources retain their last snapshot; check timestamps and update status for freshness.')+'</sub>',
            '<details>',drawer('archive','历史卡片与更新记录','Card archive & update records',lang),
            '<p>'+action('archive','历史卡片','Card archive','github-metrics/',lang,'archive')+' '+action('status','更新状态','Update status','assets/profile/activity-status.json',lang,'status')+' '+action('actions','自动更新','Automation','https://github.com/rainbowyuyu/rainbowyuyu/actions',lang,'code')+'</p>',
            '<p><sub>'+tr('目录中的旧版卡片为历史快照，不代表当前统计。','Older cards in the directory are archived snapshots, not current statistics.')+'</sub></p>','</details>',
            '<p align="center"><sub>'+tr('保持好奇，持续创造。','Stay curious. Keep creating.')+' · <a href="assets/readme/ATTRIBUTION.md">'+tr('素材与致谢','Artwork & credits')+'</a></sub></p>']
        (ROOT/('README.en.md' if en else 'README.md')).write_text('\n\n'.join(blocks).rstrip()+'\n',encoding='utf-8',newline='\n')
    print('Generated bilingual profiles, themed actions and disclosure drawers.')

if __name__=='__main__':main()
