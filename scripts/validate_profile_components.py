"""Check the shared public profile component contract without fetching new data."""
from pathlib import Path
import hashlib,json,re,subprocess,sys,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot():
    paths=list((ROOT/'assets/components').rglob('*'))+[ROOT/'README.md',ROOT/'README.en.md']
    return {p.relative_to(ROOT).as_posix():digest(p) for p in paths if p.is_file()}

projects=json.loads((ROOT/'assets/catalog/projects.json').read_text(encoding='utf-8'))
assert len(projects)==7 and len({p['slug'] for p in projects})==7
assert all(p['tags'] and p['desc'] and p['en_desc'] for p in projects)
assert all(p['repo'] is None for p in projects if p['slug'] in ('physcast','omniforge'))
files=list((ROOT/'assets/components').glob('*.svg'))
for p in files:
    root=ET.parse(p).getroot()
    assert root.attrib.get('viewBox') and root.attrib.get('aria-label'),p
    assert not any(e.tag.rsplit('}',1)[-1] in ('script','foreignObject') for e in root.iter()),p
for lang in ('zh','en'):
    for theme in ('light','dark'):
        for mobile in ('','-mobile'):
            for project in projects:
                assert (ROOT/f'assets/components/project-{project["slug"]}-{lang}{mobile}-{theme}.svg').exists()
            for skill in ('research','engineering','creation'):
                assert (ROOT/f'assets/components/skills-{skill}-{lang}{mobile}-{theme}.svg').exists()
for name in ('README.md','README.en.md'):
    data=(ROOT/name).read_text(encoding='utf-8')
    assert data.count('<details>')==11 and data.count('</details>')==11,name
    assert '<details open' not in data,name
    assert data.index('project-wiscomper')<data.index('drawer-projects')<data.index('project-ai-engineer'),name
    assert 'max-width: 600px' in data and 'prefers-color-scheme: dark' in data,name
    for src in re.findall(r'(?:src|srcset)="([^"]+)"',data):
        local=src.removeprefix('https://raw.githubusercontent.com/rainbowyuyu/rainbowyuyu/main/').split('?')[0]
        assert (ROOT/local).is_file(),(name,local)
before=snapshot()
status=digest(ROOT/'assets/profile/activity-status.json')
subprocess.run([sys.executable,str(ROOT/'scripts/generate_readme.py')],cwd=ROOT,check=True)
assert snapshot()==before,'Regeneration changed output'
assert status==digest(ROOT/'assets/profile/activity-status.json'),'Design generation changed freshness'
print(json.dumps({'projects':7,'svg_components':len(files),'languages':2,'themes':2,'responsive_layouts':2,'initial_visible_projects':3,'additional_projects':4,'idempotent':True,'activity_status_unchanged':True},indent=2))
