"""Illustrated identity and disclosure artwork for the GitHub profile."""
from html import escape
from studio_art import illustration, image_uri, star, MOTION

FONT = 'Segoe UI,Microsoft YaHei,Arial,sans-serif'


def banner(theme):
    dark = theme == 'dark'
    ink = '#eef2ee' if dark else '#203744'
    muted = '#b9c9cd' if dark else '#536773'
    accent = '#a3d9ca' if dark else '#257d73'
    stars = ''.join(star(x,y,c,s,d) for x,y,c,s,d in [
        (740,168,'#d6ac6f',8,0),(1256,75,'#dfb3a7',8,-1),
        (1350,349,'#9ccfbe',6,-2),(832,370,'#c7b3d6',5,-.5)])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="720" viewBox="0 0 1440 720" role="img" aria-labelledby="title desc">
<title id="title">rainbow鱼 · 浙江大学博士在读</title><desc id="desc">PhD student at Zhejiang University. An illustrated journey through physical AI, engineering and science storytelling.</desc>
<defs><clipPath id="paper"><rect width="1440" height="720" rx="28"/></clipPath></defs><style>{MOTION}</style>
<g clip-path="url(#paper)"><image width="1440" height="720" href="{image_uri('hero-'+theme+'.jpg')}"/>
{stars}
{illustration('logo-'+theme+'.png',57,58,47,56)}
<g font-family="{FONT}">
<text x="124" y="94" fill="{muted}" font-size="24" font-weight="600">Research. Build. Create.</text>
<text x="56" y="274" fill="{ink}" font-size="112" letter-spacing="-5" font-weight="700">rainbow鱼</text>
<path d="M63 302q190 -8 385 0l-8 9q-210 -6 -372 0Z" fill="{accent}" opacity=".5"/>
<text x="62" y="377" fill="{ink}" font-size="36" font-weight="600">浙江大学博士在读</text>
<text x="64" y="421" fill="{muted}" font-size="23">PhD student at Zhejiang University</text>
<text x="62" y="503" fill="{ink}" font-size="28" font-weight="500">让 AI 理解物理，让知识看得见。</text>
<text x="64" y="546" fill="{muted}" font-size="20">Physical AI · Engineering agents · Visual stories</text>
<text x="64" y="642" fill="{accent}" font-size="20">保持好奇，持续创造。</text>
</g></g></svg>'''


def disclosure_banner(name, lang, theme):
    dark = theme == 'dark'
    ink = '#eef2ee' if dark else '#203744'
    bg = '#202a30' if dark else '#f8f4ea'
    muted = '#bdc9ca' if dark else '#526b70'
    accent = '#abdccb' if dark else '#287b71'
    button = '#31443f' if dark else '#e1eee5'
    if lang == 'en':
        title = 'Four more projects' if name == 'projects' else 'Activity & archive'
        hint, action = 'Click to unfold this collection', 'Open / Close'
    else:
        title = '还有 4 个作品，等你发现' if name == 'projects' else '翻开每日活动与历史卡片'
        hint, action = '点击这里，展开这份作品集' if name == 'projects' else '点击这里，查看完整记录', '展开 / 收起'
    icon = 'robot' if name == 'projects' else 'brushes'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="104" viewBox="0 0 720 104" role="img" aria-label="{escape(title)}">
<style>{MOTION}</style><rect x=".5" y=".5" width="719" height="103" rx="22" fill="{bg}"/>
{illustration(icon+'.png',14,11,80,78,True)}
<g font-family="{FONT}"><text x="112" y="43" font-size="23" font-weight="600" fill="{ink}">{escape(title)}</text>
<text x="113" y="73" font-size="15" fill="{muted}">{hint}</text>
<rect x="553" y="30" width="145" height="43" rx="22" fill="{button}"/>
<text x="571" y="57" font-size="15" fill="{accent}" font-weight="600">{action}</text>
<path d="m675 43 4-4 4 4m-8 12 4 4 4-4" fill="none" stroke="{accent}" stroke-width="1.7" stroke-linecap="round"/>
</g></svg>'''
