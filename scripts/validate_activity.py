#!/usr/bin/env python3
"""Validate generated SVG assets, public identity policy and scheduled workflow invariants."""
import json,pathlib,re,sys,xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[1];errors=[];checked=0
for folder in ('github-metrics','profile-3d-contrib','profile-snake-contrib'):
    for p in (ROOT/folder).glob('*.svg'):
        s=p.read_text(encoding='utf-8');checked+=1
        try:ET.fromstring(s)
        except ET.ParseError:errors.append(str(p.relative_to(ROOT))+': invalid SVG')
        if re.search(r'<script\b|onload\s*=',s,re.I):errors.append(str(p.relative_to(ROOT))+': active script')
        if p.stem.endswith('-static') and (re.search(r'<(?:animate|animateTransform|animateMotion|set)\b',s) or 'animation:none!important' not in s):errors.append(str(p.relative_to(ROOT))+': static alternative still animates')
status=json.loads((ROOT/'assets/profile/activity-status.json').read_text(encoding='utf-8'))
for key,item in status['cards'].items():
    if item['status'] not in ('fresh','stale','unavailable'):errors.append(key+': invalid freshness')
    if item['status']=='fresh' and not item.get('updated_at'):errors.append(key+': fresh without timestamp')
    for asset in item.get('assets',[]):
        if not (ROOT/asset).is_file():errors.append(key+': missing referenced asset')
for name in ('matrics.yml','snack.yml','contrib.yml'):
    s=(ROOT/'.github/workflows'/name).read_text(encoding='utf-8')
    if 'schedule:' not in s or 'workflow_dispatch:' not in s:errors.append(name+': missing daily/manual trigger')
    if 'profile-generated-assets' not in s or 'cancel-in-progress: false' not in s:errors.append(name+': missing shared write serialization')
    if re.search(r'git\s+push.*--force|git\s+add\s+-A|crazy-max/ghaction-github-pages',s):errors.append(name+': unsafe branch mutation')
pages=(ROOT/'.github/workflows/pages.yml').read_text(encoding='utf-8')
for required in ('workflow_run:','conclusion == \'success\'','ref: main','group: profile-pages','cancel-in-progress: false','persist-credentials: false','pages: write','id-token: write'):
    if required not in pages:errors.append('pages.yml: missing deployment invariant')
if 'cp -R . ' in pages or 'path: .' in pages.split('path: .pages-stage')[0]:errors.append('pages.yml: unscoped deploy artifact')
for e in errors:print('ERROR:',e)
print(f'Checked {checked} SVGs, three scheduled generators and Pages workflow; errors={len(errors)}')
raise SystemExit(bool(errors))
