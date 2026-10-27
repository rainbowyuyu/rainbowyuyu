#!/usr/bin/env python3
"""Render public GitHub cards and optional aggregate WakaTime stats; never expose private repositories."""
from __future__ import annotations
import argparse, base64, collections, concurrent.futures, datetime as dt, json, os, pathlib, re, subprocess, urllib.request, xml.etree.ElementTree as ET
from generate_activity_themes import generate_metric_themes
from activity_card_renderer import render_card, snapshot

ROOT = pathlib.Path(__file__).resolve().parents[1]
OWNER = 'rainbowyuyu'
STATUS = ROOT / 'assets/profile/activity-status.json'
NOW = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')

def api(endpoint, query=None):
    args=['gh','api',endpoint]
    if query: args += ['-f','query='+query]
    result=subprocess.run(args,capture_output=True,timeout=45)
    if result.returncode: raise RuntimeError('GitHub request failed')
    data=json.loads(result.stdout)
    if isinstance(data,dict) and data.get('errors'): raise RuntimeError('GitHub query unavailable')
    return data

def write_svg(name,content):
    ET.fromstring(content)
    path=ROOT/'github-metrics'/name
    path.write_text(content,encoding='utf-8',newline='\n')

def write_card(name,kind,data,description):
    write_svg(name,render_card(snapshot(kind,NOW,data,description),'dark'))

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
    data={'repositories':user['public_repos'],'stars':sum(r['stargazers_count'] for r in repos),
          'followers':user['followers'],'forks':sum(r['forks_count'] for r in repos)}
    write_card('base.svg','base',data,'Public profile totals · no private repository names or counts')
    mark(status,'metrics','fresh','GitHub REST public profile and owned public repositories',['github-metrics/base.svg'])

def languages_card(status,repos):
    repos=[r for r in repos if not r['fork']]
    counts=collections.Counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        for data in pool.map(lambda r:api('repos/'+r['full_name']+'/languages'),repos): counts.update(data)
    total=sum(counts.values())
    rows=[{'name':name,'bytes':value,'percentage':value/total*100}
          for name,value in counts.most_common(5)] if total else []
    write_card('languages.indepth.svg','languages',{'rows':rows,'total_bytes':total,
               'scope':'public non-fork source bytes; top five only'},
               'Source bytes across non-fork public repositories · not coding proficiency')
    mark(status,'languages','fresh','GitHub REST language bytes, public non-fork repositories',['github-metrics/languages.indepth.svg'])

def contribution_card(status):
    query='{user(login:"rainbowyuyu"){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date weekday contributionCount color}}}}}}'
    calendar=api('graphql',query)['data']['user']['contributionsCollection']['contributionCalendar']
    days=[d for w in calendar['weeks'] for d in w['contributionDays']]
    if len(days)<300: raise RuntimeError('Incomplete calendar')
    aggregate_days=[{'date':d['date'],'count':d['contributionCount']} for d in days]
    write_card('calendar.full.svg','calendar',{'total':calendar['totalContributions'],'days':aggregate_days},
               'GitHub contribution calendar · rolling year')
    mark(status,'calendar','fresh','GitHub GraphQL contribution calendar',['github-metrics/calendar.full.svg'])
    ordered=sorted(days,key=lambda d:d['date']);longest=current=run=0
    for d in ordered:
        run=run+1 if d['contributionCount'] else 0;longest=max(longest,run)
    recent=ordered[:-1] if ordered and ordered[-1]['contributionCount']==0 else ordered
    for d in reversed(recent):
        if not d['contributionCount']:break
        current+=1
    write_card('streak.svg','streak',{'current':current,'longest':longest,'recent_days':aggregate_days[-14:]},
               'Contribution days · current streak allows an unfinished today')
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
    write_card('habits.charts.svg','habits',{'hours':hours,'sample_size':len(events),'timezone':'UTC+8'},
               f'Last {len(events)} public events, up to 90 days · UTC+8 · not coding hours')
    mark(status,'habits','fresh','GitHub public events, max 300 events / 90 days',['github-metrics/habits.charts.svg'])
    counts=[daily[(today-dt.timedelta(days=29-i)).isoformat()] for i in range(30)]
    write_card('activity.svg','activity',{'counts':counts,'start':(today-dt.timedelta(days=29)).isoformat(),
               'end':today.isoformat()},'30-day event window · bounded by GitHub public events API, not all commits')
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
    write_card('wakatime.svg','wakatime',{'hours':seconds/3600,'daily_average_hours':average/3600,
               'total_seconds':seconds,'daily_average_seconds':average},
               'WakaTime measured activity · optional provider. Recorded activity only · no private project names')
    mark(status,'wakatime','fresh','WakaTime last_7_days aggregate statistics',['github-metrics/wakatime.svg'])

def static_variants():
    pairs=[('profile-snake-contrib/github-contribution-grid-snake-dark.svg','profile-snake-contrib/github-contribution-grid-snake-static.svg'),('profile-snake-contrib/github-contribution-grid-snake.svg','profile-snake-contrib/github-contribution-grid-snake-static-light.svg'),('profile-3d-contrib/profile-night-view.svg','profile-3d-contrib/profile-night-static.svg'),('profile-3d-contrib/profile-green.svg','profile-3d-contrib/profile-day-static.svg')]
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
    if args.kind=='metrics':
        generate_metric_themes(ROOT)
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
