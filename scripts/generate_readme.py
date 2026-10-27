"""Rebuild the two GitHub profile documents and their original navigation artwork."""
from pathlib import Path
from html import escape
import json, re

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/readme'

def button(name,label,color,icon='arrow',width=166):
    glyph={'arrow':'M13 27 27 13M14 13h13v13','grid':'M13 13h6v6h-6zM23 13h6v6h-6zM13 23h6v6h-6zM23 23h6v6h-6z','pulse':'M11 23h6l4-10 5 17 4-7h5','play':'M17 12 31 21 17 30Z','code':'m17 14-7 7 7 7m12-14 7 7-7 7M25 10l-5 22','globe':'M10 21h22M21 10a11 11 0 1 0 0 22 11 11 0 1 0 0-22M21 10c-8 8-8 14 0 22 8-8 8-14 0-22'}[icon]
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="44" viewBox="0 0 {width} 44" role="img" aria-label="{escape(label)}"><rect x=".5" y=".5" width="{width-1}" height="43" rx="10" fill="#111A2D" stroke="#34465F"/><path d="{glyph}" transform="translate(3 1)" stroke="{color}" fill="none" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/><text x="49" y="27.5" font-family="Segoe UI,Microsoft YaHei,Arial,sans-serif" font-weight="600" font-size="13" fill="{color}">{escape(label)}</text><path d="M{width-20} 17l5 5-5 5" stroke="{color}" fill="none" stroke-width="1.5"/></svg>'''
    (OUT/(name+'.svg')).write_text(svg,encoding='utf-8')

buttons=[('portfolio','个人主页','PORTFOLIO','#7EE5DD','globe',166),('projects','精选项目','PROJECTS','#B5AFFE','grid',166),('activity','每日动态','ACTIVITY','#F1CF9C','pulse',166),('bilibili','科学影像','BILIBILI','#EEA8CA','play',166)]
for stem,zh,en,color,icon,w in buttons:
    button(stem+'-zh',zh,color,icon,w);button(stem+'-en',en,color,icon,w)
for stem,zh,en,color in [('physcast','项目介绍','EXPLORE','#8EBAD1'),('omniforge','项目介绍','EXPLORE','#DDBE87'),('wiscomper','在线体验','LIVE DEMO','#B7A8FF'),('ai-engineer','查看源码','SOURCE','#6DC8FF'),('ai-revolution','查看系列','EXPLORE','#E4C7A0'),('science-studio','观看影像','WATCH','#83E3D6'),('manim','查看源码','SOURCE','#8ED0C2')]:
    button(stem+'-zh',zh,color,'arrow',150);button(stem+'-en',en,color,'arrow',150)
button('github-zh','GitHub 源码','#C5D1E5','code',150);button('github-en','SOURCE CODE','#C5D1E5','code',170)

projects=[
dict(slug='physcast',name='PhysCast',en='PhysCast',tag='PHYSICAL AI',zh='物理约束的生成式风场预测',title='Generative wind forecasting, grounded in physics',desc='连接 OpenFAST / FAST.Farm、条件扩散预测与独立验证，探索稀疏观测和控制干预下的风场变化。',en_desc='Connecting OpenFAST / FAST.Farm, conditional diffusion and independent validation to study wind fields under sparse observations and control interventions.',status='研究中 · 源码私有',en_status='RESEARCH IN PROGRESS · PRIVATE SOURCE',url='#physcast',repo=None),
dict(slug='omniforge',name='OmniForge · 万象工坊',en='OmniForge',tag='AGENTIC ENGINEERING',zh='让工程意图，走向可检查的设计过程',title='From engineering intent to an inspectable workflow',desc='把任务规划、工具协作、建模、有限元与拓扑优化组织在同一工作台，保留执行过程和设计依据。',en_desc='A workspace for planning, tool orchestration, modeling, finite elements and topology optimization—with inspectable execution and design evidence.',status='持续开发 · 源码私有',en_status='IN DEVELOPMENT · PRIVATE SOURCE',url='#omniforge',repo=None),
dict(slug='wiscomper',name='Wiscomper · 智算视界',en='Wiscomper',tag='VISUAL MATHEMATICS',zh='从一道公式，到一段看得懂的数学动画',title='From a formula to mathematics you can see',desc='连接公式识别、LaTeX、解题步骤与 Manim 动画，在交互工作台里编辑、理解和探索数学。',en_desc='Connecting formula recognition, LaTeX, worked solutions and Manim animation in an interactive mathematics workspace.',status='开源 · 在线体验',en_status='OPEN SOURCE · LIVE DEMO',url='https://www.wiscomper.com/',repo='Wisdom_Computing_Perspective'),
dict(slug='ai-engineer',name='The AI Engineer',en='The AI Engineer',tag='COMPUTATIONAL DESIGN',zh='设计之后，继续计算与验证',title='Design. Compute. Inspect. Iterate.',desc='将大模型与确定性的工程后端连接起来，串联几何、网格、拓扑优化、尺寸优化与设计报告。',en_desc='Connecting language models with deterministic engineering backends, from geometry and meshing to topology, sizing and design reports.',status='研究代码 · 开源',en_status='RESEARCH CODE · OPEN SOURCE',url='https://github.com/rainbowyuyu/ai_engineer',repo='ai_engineer'),
dict(slug='ai-revolution',name='AI 进化史',en='The Evolution of AI',tag='IDEAS IN MOTION',zh='把 AI 的演进，讲成可以看见的故事',title='A visual journey through the evolution of AI',desc='用可视化、动画与实验梳理视觉、生成模型、语言、多模态与空间重建；智能体与世界模型章节规划中。',en_desc='Exploring vision, generative models, language, multimodality and spatial reconstruction through animation and experiments. The agents and world-models chapter is planned.',status='系列创作 · 开源',en_status='ONGOING SERIES · OPEN SOURCE',url='#ai-revolution',repo='AI_revolution'),
dict(slug='science-studio',name='rainbow鱼 · 科普工作台',en='rainbow鱼 · Science Studio',tag='SCIENCE × STORYTELLING',zh='把科学问题，变成值得追问的画面',title='Turning science questions into stories worth exploring',desc='将故事、机制可视化、连续运镜、字幕与 AI 视频编辑组织成创作流程，让研究与工程知识更容易理解。',en_desc='A production workflow for stories, mechanism visualization, camera motion, captions and AI video editing, making research and engineering easier to understand.',status='持续创作 · 开源',en_status='ONGOING CREATION · OPEN SOURCE',url='https://space.bilibili.com/343585138',repo='Popula_science_video'),
dict(slug='manim',name='Manim Extend Rainbow',en='Manim Extend Rainbow',tag='VISUAL LEARNING TOOLS',zh='让算法和结构，有直观的表达',title='Giving algorithms and structures a visual language',desc='为数据结构、操作系统与计算机组成教学制作可复用的 Manim 扩展组件。',en_desc='Reusable Manim components for teaching data structures, operating systems and computer organization.',status='动画组件 · 开源',en_status='ANIMATION COMPONENTS · OPEN SOURCE',url='https://github.com/rainbowyuyu/manim_extend_rainbow',repo='manim_extend_rainbow')]

SITE='https://rainbowyuyu.github.io/rainbowyuyu/'
for lang in ('zh','en'):
    en=lang=='en';site=SITE+('?lang=en' if en else '')
    lines=['<!-- Generated by scripts/generate_readme.py. Edit the source copy and run Python to synchronize both languages. -->',
      '<p align="right">'+('<a href="README.md">简体中文</a> &nbsp; / &nbsp; <strong>English</strong>' if en else '<strong>简体中文</strong> &nbsp; / &nbsp; <a href="README.en.md">English</a>')+'</p>',
      f'<p align="center"><a href="{site}"><img src="assets/readme/profile-banner.svg" width="100%" alt="rainbow鱼 · 浙江大学博士 / PhD researcher at Zhejiang University"/></a></p>',
      '<p align="center"><strong>'+('AI for the physical world. Knowledge you can see.' if en else '让 AI 理解物理，让知识看得见。')+'</strong></p>',
      '<p align="center">'+('I am <strong>rainbow鱼</strong>, a <strong>PhD researcher at Zhejiang University</strong>.<br/>I build at the intersection of physical AI, engineering agents and scientific storytelling.' if en else '我是 <strong>rainbow鱼</strong>，<strong>浙江大学博士</strong>。<br/>在物理 AI、工程智能体与科学叙事之间，持续研究，也持续创造。')+'</p>',
      '<p align="center">']
    for stem,_,_,_,_,_ in buttons:
        url={'portfolio':site,'projects':'#projects','activity':'#activity','bilibili':'https://space.bilibili.com/343585138'}[stem]
        lines.append(f'<a href="{url}"><img src="assets/readme/{stem}-{lang}.svg" height="42" alt="{stem}"/></a> ')
    lines+=['</p>','', '<p align="center"><a href="assets/readme/ATTRIBUTION.md"><img src="assets/readme/typing.svg" width="720" alt="Research in physics. Build with agents. Explain through motion."/></a></p>',
      '<p align="center"><img src="assets/images/hr.gif" width="100%" height="2" alt=""/></p>',
      '<a id="toolbox"></a>', '## '+('A small toolbox, many possibilities' if en else '研究与创作工具箱'),
      '<p align="center">']
    for icon,title in [('python','Python'),('cpp','C++'),('mysql','MySQL'),('java','Java'),('docker','Docker'),('github','GitHub')]:
        lines.append(f'<img src="assets/widgets/{icon}.svg" width="54" height="54" alt="{title}" title="{title}"/> &nbsp;')
    lines+=['</p>', '<p align="center"><img src="assets/widgets/skills.svg" width="640" alt="PyTorch, C, Markdown, LaTeX, MATLAB, Photoshop, Premiere, After Effects, Audition, Git"/></p>',
      '<p align="center"><sub>'+('Research · Simulation · Visual computing · Animation · Open source' if en else '科研计算 · 物理仿真 · 交互可视化 · 动态影像 · 开源工具')+'</sub></p>', '', '<a id="projects"></a>', '## '+('Selected work' if en else '精选项目'),
      ('Research platforms, engineering tools and visual stories. Each project keeps its own visual identity.' if en else '从研究平台到工程工具，再到科学影像。每个项目，保留自己的问题、色彩和表达。'), '']
    for i,p in enumerate(projects):
        url=(site+p['url']) if p['url'].startswith('#') else p['url']
        lines += [f'### {i+1:02} / '+(p['en'] if en else p['name']),
          f'<p><a href="{site}#{p["slug"]}"><img src="assets/showcase/{p["slug"]}.webp" width="100%" alt="{escape(p["en"])} — {escape(p["title"] if en else p["zh"])}"/></a></p>',
          '**'+(p['title'] if en else p['zh'])+'**',
          p['en_desc'] if en else p['desc'],
          '<p><sub>'+(p['en_status'] if en else p['status'])+'</sub></p>',
          f'<p><a href="{url}"><img src="assets/readme/{p["slug"]}-{lang}.svg" height="38" alt="'+('Explore project' if en else '项目入口')+'"/></a>']
        if p['repo'] and not url.startswith('https://github.com/'):
            lines.append(f'<a href="https://github.com/rainbowyuyu/{p["repo"]}"><img src="assets/readme/github-{lang}.svg" height="38" alt="GitHub source"/></a>')
        lines+=['</p>','']
    lines += ['<sub>'+('Project descriptions updated 2026-10-27. Research and development remain ongoing; functionality and validation scope follow each project’s documentation.' if en else '项目介绍更新于 2026-10-27。研究与开发持续进行，功能与验证范围以各项目文档为准。')+'</sub>',
      '', '<p align="center"><img src="assets/images/hr.gif" width="100%" height="2" alt=""/></p>', '<a id="activity"></a>',
      '## '+('Built, day by day' if en else '日复一日，把想法做成作品'),
      '<p align="center"><img src="assets/images/left.png" width="10%" alt="Original profile mascot"/> &nbsp; <img src="github-metrics/streak.svg" width="74%" alt="Contribution streak"/> &nbsp; <img src="assets/images/right.png" width="10%" alt="Original profile mascot"/></p>',
      '<picture><source media="(prefers-color-scheme: dark)" srcset="profile-snake-contrib/github-contribution-grid-snake-dark.svg"/><img src="profile-snake-contrib/github-contribution-grid-snake.svg" width="100%" alt="Animated GitHub contribution snake"/></picture>',
      '<p><img src="github-metrics/base.svg" width="49%" alt="GitHub public activity"/> <img src="github-metrics/languages.indepth.svg" width="49%" alt="Public source language breakdown"/></p>',
      '<p><img src="github-metrics/habits.charts.svg" width="49%" alt="Activity rhythm"/> <img src="github-metrics/wakatime.svg" width="49%" alt="WakaTime recorded coding activity"/></p>',
      '<picture><source media="(prefers-color-scheme: dark)" srcset="profile-3d-contrib/profile-night-rainbow.svg"/><img src="profile-3d-contrib/profile-green-animate.svg" width="100%" alt="Animated three-dimensional contribution landscape"/></picture>',
      '', '<details>', '<summary><strong>'+('More daily activity & archived cards' if en else '展开更多每日活动与历史卡片')+'</strong></summary>', '',
      '<p><img src="github-metrics/calendar.full.svg" width="100%" alt="Contribution calendar"/></p>', '<p><img src="github-metrics/activity.svg" width="100%" alt="Recent public activity"/></p>',
      ('The following isometric calendar is an archived snapshot.' if en else '以下等距日历保留为历史快照。'), '<p><img src="github-metrics/isocalendar.fullyear.svg" width="100%" alt="Archived isometric calendar"/></p>', '', '</details>', '',
      '<sub>'+('The scheduled jobs refresh the stored cards daily. WakaTime reflects measured activity over the last seven days. Use each card’s timestamp and the update status to assess freshness; unavailable providers keep the last successful snapshot.' if en else '每日任务自动更新本地卡片；WakaTime 展示最近 7 天真实记录。请以卡片时间与更新状态判断时效，数据源不可用时保留上次成功快照。')+'</sub>', '',
      '[ '+('Update status' if en else '更新状态')+' ](assets/profile/activity-status.json) &nbsp; · &nbsp; [ GitHub Actions ](https://github.com/rainbowyuyu/rainbowyuyu/actions) &nbsp; · &nbsp; [ '+('All repositories' if en else '全部仓库')+' ](https://github.com/rainbowyuyu?tab=repositories)', '',
      '<p align="center"><img src="assets/readme/footer.svg" width="100%" alt="Stay curious. Keep creating."/></p>',
      '<p align="center"><a href="'+site+'">Portfolio</a> &nbsp; · &nbsp; <a href="https://space.bilibili.com/343585138">Bilibili</a> &nbsp; · &nbsp; <a href="https://www.wiscomper.com/">Wiscomper</a> &nbsp; · &nbsp; <a href="assets/readme/ATTRIBUTION.md">Widget credits</a></p>', '']
    (ROOT/('README.en.md' if en else 'README.md')).write_text(re.sub(r'<p(?: [^>]+)?>.*?</p>',lambda m:m.group(0).replace('\n\n','\n'),'\n\n'.join(x.rstrip() for x in lines),flags=re.S).rstrip()+'\n',encoding='utf-8',newline='\n')
print('Generated two README documents and navigation artwork.')
