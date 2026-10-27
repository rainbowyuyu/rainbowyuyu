#!/usr/bin/env python3
"""Render public GitHub cards and optional aggregate WakaTime stats; never expose private repositories."""
from __future__ import annotations
import argparse, base64, collections, concurrent.futures, datetime as dt, html, json, os, pathlib, re, subprocess, urllib.request, xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
OWNER = 'rainbowyuyu'
STATUS = ROOT / 'assets/profile/activity-status.json'
NOW = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
COLORS = ['#6ce9c4','#69b5ff','#a894ff','#f6c467','#f08bb7','#89d8e3']

def api(endpoint, query=None):
    args=['gh','api',endpoint]
    if query: args += ['-f','query='+query]
    result=subprocess.run(args,capture_output=True,timeout=45)
    if result.returncode: raise RuntimeError('GitHub request failed')
    data=json.loads(result.stdout)
    if isinstance(data,dict) and data.get('errors'): raise RuntimeError('GitHub query unavailable')
    return data

def txt(x,y,value,size=14,color='#9dafc4',weight='400'):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}">{html.escape(str(value))}</text>'

def card(title,subtitle,body,height=290):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{height}" viewBox="0 0 800 {height}" role="img" aria-label="{html.escape(title,quote=True)}"><title>{html.escape(title)}</title><desc>{html.escape(subtitle)}. Updated {NOW}. Public aggregate data.</desc><style>text{{font-family:Inter,Arial,'Microsoft YaHei',sans-serif}}</style><rect x=".5" y=".5" width="799" height="{height-1}" rx="18" fill="#0b111d" stroke="#223149"/>{txt(28,35,title,18,'#e9f1f8','600')}{txt(28,59,subtitle,12)}{body}<path d="M28 {height-36}H772" stroke="#223149"/>{txt(28,height-15,'rainbow鱼 · GitHub public data',10,'#6e859f')}{txt(556,height-15,NOW[:16].replace('T',' ')+' UTC',10,'#6e859f')}</svg>'''

def write_svg(name,content):
    ET.fromstring(content)
    path=ROOT/'github-metrics'/name
    path.write_text(content,encoding='utf-8',newline='\n')

def load_status():
    if STATUS.exists(): return json.loads(STATUS.read_text(encoding='utf-8'))
    return {'schema_version':1,'timezone':'Asia/Shanghai','cards':{}}

def mark(status,key,state,source,paths,reason=None):
    prior=status['cards'].get(key,{})
    item={'status':state,'source':source,'assets':paths,'checked_at':NOW,'updated_at':NOW if state=='fresh' else prior.get('updated_at')}
    if reason: item['note']=reason
    status['cards'][key]=item

def repos_public():
    out=[]
    for p in range(1,11):
        page=api(f'users/{OWNER}/repos?type=owner&per_page=100&page={p}')
        out += [r for r in page if r.get('private') is False and r.get('owner',{}).get('login','').lower()==OWNER]
        if len(page)<100: break
    return out

def base_card(status,repos):
    user=api('users/'+OWNER)
    values=[(user['public_repos'],'公开仓库 / Repositories'),(sum(r['stargazers_count'] for r in repos),'公开 Stars / Stars'),(user['followers'],'关注者 / Followers'),(sum(r['forks_count'] for r in repos),'公开 Forks / Forks')]
    body=''
    for i,(value,label) in enumerate(values):
        x=30+i*194
        body+=txt(x,144,f'{value:,}',43,COLORS[i],'650')+txt(x,177,label,12)
    write_svg('base.svg',card('PUBLIC SIGNAL / 公开动态','Public profile totals · no private repository names or counts',body,240))
    mark(status,'metrics','fresh','GitHub REST public profile and owned public repositories',['github-metrics/base.svg'])

def languages_card(status,repos):
    repos=[r for r in repos if not r['fork']]
    counts=collections.Counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        for data in pool.map(lambda r:api('repos/'+r['full_name']+'/languages'),repos): counts.update(data)
    total=sum(counts.values());rows=counts.most_common(5)
    body='';x=28
    if total:
        for i,(name,value) in enumerate(rows):
            y=92+i*29; pct=value/total*100
            body+=txt(28,y,name,13,'#d8e6f2')+f'<rect x="170" y="{y-12}" width="{max(.4,510*pct/100):.2f}" height="12" rx="5" fill="{COLORS[i]}"/>'+txt(718,y,f'{pct:.1f}%',12)
    else: body=txt(28,130,'No public source-language data available / 暂无语言数据',15)
    write_svg('languages.indepth.svg',card('LANGUAGE SPECTRUM / 语言分布','Source bytes across non-fork public repositories · not coding proficiency',body,290))
    mark(status,'languages','fresh','GitHub REST language bytes, public non-fork repositories',['github-metrics/languages.indepth.svg'])

def contribution_card(status):
    query='{user(login:"rainbowyuyu"){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date weekday contributionCount color}}}}}}'
    calendar=api('graphql',query)['data']['user']['contributionsCollection']['contributionCalendar']
    days=[d for w in calendar['weeks'] for d in w['contributionDays']]
    if len(days)<300: raise RuntimeError('Incomplete calendar')
    body=txt(28,100,f"{calendar['totalContributions']:,}",34,'#74dfbd','600')+txt(155,99,'contributions in the past year / 年度贡献',13)
    maxcount=max(d['contributionCount'] for d in days) or 1
    palette=['#172439','#1f5d57','#2e8b75','#48bd99','#77efd0']
    for i,week in enumerate(calendar['weeks']):
        for d in week['contributionDays']:
            value=d['contributionCount'];level=0 if value==0 else min(4,1+int(value/maxcount*3))
            body+=f'<rect x="{29+i*14}" y="{121+d["weekday"]*15}" width="11" height="11" rx="2" fill="{palette[level]}"><title>{d["date"]}: {value} contributions</title></rect>'
    write_svg('calendar.full.svg',card('CONTRIBUTION FIELD / 贡献日历','GitHub contribution calendar · rolling year',body,285))
    mark(status,'calendar','fresh','GitHub GraphQL contribution calendar',['github-metrics/calendar.full.svg'])
    ordered=sorted(days,key=lambda d:d['date']);longest=current=run=0
    for d in ordered:
        run=run+1 if d['contributionCount'] else 0;longest=max(longest,run)
    recent=ordered[:-1] if ordered and ordered[-1]['contributionCount']==0 else ordered
    for d in reversed(recent):
        if not d['contributionCount']:break
        current+=1
    body=txt(30,140,str(current),48,'#79dfbf','650')+txt(30,175,'current streak / 当前连续天数',13)+txt(400,140,str(longest),48,'#b09cff','650')+txt(400,175,'longest in returned year / 年度最长',13)
    write_svg('streak.svg',card('BUILDING CONTINUITY / 持续构建','Contribution days · current streak allows an unfinished today',body,245))
    mark(status,'streak','fresh','GitHub contribution calendar, rolling-year streak calculation',['github-metrics/streak.svg'])

def event_cards(status):
    events=[]
    for page in range(1,4):
        batch=api(f'users/{OWNER}/events/public?per_page=100&page={page}')
        events += [e for e in batch if e.get('public') is True]
        if len(batch)<100: break
    hours=[0]*24;daily=collections.Counter();today=dt.datetime.now(dt.timezone.utc).date()
    for event in events:
        when=dt.datetime.fromisoformat(event['created_at'].replace('Z','+00:00'))
        hours[(when.hour+8)%24]+=1;daily[when.date().isoformat()]+=1
    body='';maximum=max(hours) or 1
    for i,count in enumerate(hours):
        h=count/maximum*108;x=32+i*31
        body+=f'<rect x="{x}" y="{210-h:.2f}" width="22" height="{max(h,1):.2f}" rx="3" fill="{COLORS[0] if count else "#1b2b40"}"><title>{i:02}:00 UTC+8: {count} public events</title></rect>'
        if i%3==0:body+=txt(x,232,f'{i:02}',10)
    write_svg('habits.charts.svg',card('ACTIVITY RHYTHM / 活跃时段',f'Last {len(events)} public events, up to 90 days · UTC+8 · not coding hours',body,290))
    mark(status,'habits','fresh','GitHub public events, max 300 events / 90 days',['github-metrics/habits.charts.svg'])
    counts=[daily[(today-dt.timedelta(days=29-i)).isoformat()] for i in range(30)];maximum=max(counts) or 1;pts=' '.join(f'{30+i*25.5:.1f},{210-count/maximum*110:.1f}' for i,count in enumerate(counts))
    body=f'<path d="M30 210H770" stroke="#2b3b51"/><polyline points="{pts}" fill="none" stroke="#87a8ff" stroke-width="3" stroke-linejoin="round"/>'
    body+=txt(30,234,(today-dt.timedelta(days=29)).isoformat(),11)+txt(660,234,today.isoformat(),11)
    write_svg('activity.svg',card('PUBLIC ACTIVITY / 公开活动','30-day event window · bounded by GitHub public events API, not all commits',body,290))
    mark(status,'activity','fresh','GitHub public events, last 30 days within available API window',['github-metrics/activity.svg'])

def wakatime_card(status):
    key=os.environ.get('WAKATIME_API_KEY')
    if not key:
        mark(status,'wakatime','stale','WakaTime optional aggregate API',['github-metrics/wakatime.svg'],'No WakaTime credential in this run. Previous snapshot retained; freshness unknown.')
        return
    auth=base64.b64encode(key.encode()).decode()
    req=urllib.request.Request('https://wakatime.com/api/v1/users/current/stats/last_7_days',headers={'Authorization':'Basic '+auth,'User-Agent':'rainbow-profile-metrics/1'})
    with urllib.request.urlopen(req,timeout=30) as response:data=json.load(response)['data']
    if data.get('is_up_to_date') is not True:raise RuntimeError('WakaTime aggregate not current')
    seconds=data.get('total_seconds');average=data.get('daily_average')
    if not isinstance(seconds,(int,float)) or not isinstance(average,(int,float)):raise RuntimeError('Missing WakaTime totals')
    body=txt(30,131,f'{seconds/3600:.1f} h',36,'#b7a2ff','600')+txt(30,161,'last 7 days / 最近七天',13)+txt(390,131,f'{average/3600:.1f} h',36,'#74dfbd','600')+txt(390,161,'daily average / 日均记录',13)
    body+=txt(30,208,'Recorded activity only · no private project names / 仅记录活动，不展示私有项目名称',11)
    write_svg('wakatime.svg',card('CODING TIME / 编码时间','WakaTime measured activity · optional provider',body,275))
    mark(status,'wakatime','fresh','WakaTime last_7_days aggregate statistics',['github-metrics/wakatime.svg'])

def static_variants():
    pairs=[('profile-snake-contrib/github-contribution-grid-snake-dark.svg','profile-snake-contrib/github-contribution-grid-snake-static.svg'),('profile-3d-contrib/profile-night-view.svg','profile-3d-contrib/profile-night-static.svg')]
    for source,destination in pairs:
        path=ROOT/source
        if not path.exists():continue
        s=path.read_text(encoding='utf-8')
        # Preserve initial geometry and data; disable CSS animation and remove SMIL motion.
        s=re.sub(r'<(?:animate|animateTransform|animateMotion|set)\b[^>]*(?:/>|>.*?</(?:animate|animateTransform|animateMotion|set)>)','',s,flags=re.S)
        s=s.replace('</svg>','<style>*{animation:none!important;transition:none!important}</style></svg>')
        ET.fromstring(s);(ROOT/destination).write_text(s,encoding='utf-8',newline='\n')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--kind',choices=['metrics','snake','contributions3d'],default='metrics');parser.add_argument('--result',choices=['success','failure'],default='success');args=parser.parse_args()
    status=load_status();status.setdefault('cards',{})
    failures=[]
    if args.kind=='metrics':
        try:repos=repos_public()
        except Exception:repos=None
        jobs=[('metrics',lambda:base_card(status,repos) if repos is not None else (_ for _ in ()).throw(RuntimeError())),('languages',lambda:languages_card(status,repos) if repos is not None else (_ for _ in ()).throw(RuntimeError())),('calendar',lambda:contribution_card(status)),('events',lambda:event_cards(status)),('wakatime',lambda:wakatime_card(status))]
        mappings={'metrics':['github-metrics/base.svg'],'languages':['github-metrics/languages.indepth.svg'],'calendar':['github-metrics/calendar.full.svg'],'streak':['github-metrics/streak.svg'],'habits':['github-metrics/habits.charts.svg'],'activity':['github-metrics/activity.svg'],'wakatime':['github-metrics/wakatime.svg']}
        for name,job in jobs:
            try:job()
            except Exception:
                failures.append(name)
                for item in (['habits','activity'] if name=='events' else ['calendar','streak'] if name=='calendar' else [name]):mark(status,item,'stale','WakaTime aggregate API' if item=='wakatime' else 'GitHub public API',mappings[item],'Refresh unavailable; last stored snapshot retained. No fallback values invented.')
    else:
        paths=['profile-snake-contrib/github-contribution-grid-snake.svg','profile-snake-contrib/github-contribution-grid-snake-dark.svg'] if args.kind=='snake' else [p.relative_to(ROOT).as_posix() for p in sorted((ROOT/'profile-3d-contrib').glob('*.svg'))]
        success=args.result=='success' and bool(paths) and all((ROOT/p).is_file() for p in paths)
        mark(status,args.kind,'fresh' if success else 'stale','Platane/snk' if args.kind=='snake' else 'yoshi389111/github-profile-3d-contrib',paths,None if success else 'Generation failed; last stored artwork retained.')
    static_variants()
    status['updated_at']=NOW;status['timezone']='Asia/Shanghai';status['schema_version']=1
    originals={'snake':('Platane/snk',['profile-snake-contrib/github-contribution-grid-snake.svg','profile-snake-contrib/github-contribution-grid-snake-dark.svg']),'contributions3d':('yoshi389111/github-profile-3d-contrib',['profile-3d-contrib/profile-night-view.svg'])}
    for key,(source,paths) in originals.items():
        item=status['cards'].setdefault(key,{'status':'stale','updated_at':None,'note':'Existing artwork retained; awaiting a verified scheduled refresh.'})
        item.setdefault('source',source);item.setdefault('assets',paths);item.setdefault('checked_at',NOW)
    STATUS.parent.mkdir(parents=True,exist_ok=True);STATUS.write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'operation':args.kind,'failed_sources':failures,'status_file':STATUS.relative_to(ROOT).as_posix()}))
    return 0

if __name__=='__main__':raise SystemExit(main())
