#!/usr/bin/env python3
"""Build light project-cover counterparts without changing approved dark artwork.

Requirements: Python 3.10+, Node.js, sharp.
Usage: python scripts/generate_cover_themes.py [--sharp-module /path/to/sharp]
The existing SVG is the composition source. Explicit light-theme drawing roles
are used instead of raster inversion or image filters. Embedded logos are kept.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'assets/showcase'
PROJECTS = {
    'physcast': ('#7eb2c9', '#2f6b85'),
    'omniforge': ('#dbaf6c', '#856019'),
    'wiscomper': ('#aaa1ef', '#6553a6'),
    'ai-engineer': ('#6ebaf0', '#236e9d'),
    'ai-revolution': ('#dcc08c', '#84641f'),
    'science-studio': ('#74d5c7', '#14786b'),
    'manim': ('#7bc7b8', '#256f60'),
}

# Neutral paper and a single supporting surface; project hue is reserved for
# the concept drawing and headline accent. Text remains readable on each panel.
LIGHT_ROLES = {
    '#171d21': '#f6f8fa', '#242d33': '#f6f8fa',
    '#1a2227': '#eaeef2', '#262f35': '#ffffff',
    '#202b30': '#f7f9fb', '#252f34': '#f7f9fb',
    '#20282c': '#f7f9fb', '#172327': '#f7f9fb',
    '#f3f4ee': '#202b33', '#e6ecea': '#202b33',
    '#b9c4c6': '#45555f', '#9daeb2': '#45555f',
    '#bcc8c9': '#45555f', '#c5d0d0': '#45555f',
    '#c5d8d4': '#354851', '#aeb9bc': '#45555f',
    '#98aaaf': '#586973', '#9cacb2': '#586973',
    '#afc1c7': '#586973', '#7d929a': '#586973',
    '#819a9e': '#586973', '#91a9b2': '#586973',
    '#b4c4cb': '#637785', '#81939a': '#a4b1bb',
    '#50636c': '#c6d0d8', '#52636a': '#bac7d0',
    '#495961': '#c6d0d8', '#475c63': '#c6d0d8',
    '#4d6268': '#c6d0d8', '#64757b': '#9cabb5',
    '#566467': '#9cabb5', '#53616a': '#9cabb5',
    '#52616b': '#9cabb5', '#53666d': '#9cabb5',
    '#c7dbe1': '#6793a7', '#dfc49a': '#936f35',
    '#c49adb': '#7f5597', '#e4c17d': '#956c1c',
    '#f2ecdf': '#ede9df',
}

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def make_light(slug: str, source: str) -> str:
    marks: list[str] = []
    def protect(match: re.Match) -> str:
        marks.append(match.group(0))
        return f'<!-- PROJECT_MARK_{len(marks)-1} -->'
    canvas = re.sub(r'<svg x="77".*?</svg>', protect, source, flags=re.S)
    colors = dict(LIGHT_ROLES)
    colors[PROJECTS[slug][0]] = PROJECTS[slug][1]
    canvas = re.sub(r'#[0-9a-fA-F]{6}', lambda m: colors.get(m.group().lower(), m.group()), canvas)
    # Keep the approved fine-grid composition, but omit the dark-version glow.
    canvas = re.sub(r'<ellipse[^>]+fill="url\(#glow\)"[^>]*/>', '', canvas)
    canvas = canvas.replace('fill="url(#bg)"', 'fill="#f6f8fa"')
    canvas = canvas.replace('project cover"', 'project cover — light theme"', 1)
    for i, mark in enumerate(marks):
        # Two original marks use pale strokes. A compact slate mounting tile
        # preserves those assets while making their silhouette legible on paper.
        mount = '<rect x="69" y="74" width="80" height="80" rx="17" fill="#202b33"/>' if slug in ('omniforge', 'science-studio') else ''
        canvas = canvas.replace(f'<!-- PROJECT_MARK_{i} -->', mount + mark)
    ET.fromstring(canvas)
    assert all(mark in canvas for mark in marks), 'Original logo changed'
    return canvas

RENDER_JS = r'''
const fs = require('node:fs');
const sharp = require(process.argv[1]);
const jobs = JSON.parse(fs.readFileSync(0,'utf8'));
(async () => {
  for (const job of jobs) {
    await sharp(job.source, {density:100}).resize(1600,800)
      .webp({quality:94, alphaQuality:100}).toFile(job.output);
    const metadata = await sharp(job.output).metadata();
    if (metadata.width !== 1600 || metadata.height !== 800 || !metadata.hasAlpha)
      throw new Error('Unexpected dimensions or missing transparency: '+job.output);
  }
})().catch(error => { console.error(error.message); process.exit(1); });
'''

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sharp-module', default='sharp', help='sharp package name or absolute module directory')
    parser.add_argument('--svg-only', action='store_true', help='Write SVGs without rendering or updating the manifest')
    args = parser.parse_args()
    originals = {p: digest(p.read_bytes()) for slug in PROJECTS for p in
                 (ART/f'{slug}.webp', ART/f'{slug}-cover.svg', ART/f'{slug}-original.webp')}
    jobs = []
    for slug in PROJECTS:
        source = ART/f'{slug}-cover.svg'
        output = ART/f'{slug}-cover-light.svg'
        output.write_text(make_light(slug, source.read_text(encoding='utf-8')), encoding='utf-8', newline='\n')
        jobs.append({'source':str(output), 'output':str(ART/f'{slug}-light.webp')})
    if not args.svg_only:
        subprocess.run(['node','-e',RENDER_JS,args.sharp_module], input=json.dumps(jobs).encode(), cwd=ROOT, check=True)
        manifest_path = ROOT/'assets/catalog/manifest.json'
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        for entry in manifest['assets']:
            slug = entry['id']
            if slug not in PROJECTS:
                continue
            light = ART/f'{slug}-light.webp'
            svg = ART/f'{slug}-cover-light.svg'
            entry['theme_variants'] = {
                'dark': {'asset': entry['asset'], 'svg_source':entry['svg_source'],
                         'bytes':entry['bytes'], 'sha256':entry['sha256'], 'accent':PROJECTS[slug][0]},
                'light': {'asset':light.relative_to(ROOT).as_posix(),
                          'svg_source':svg.relative_to(ROOT).as_posix(),
                          'width':1600, 'height':800, 'bytes':light.stat().st_size,
                          'sha256':digest(light.read_bytes()), 'svg_sha256':digest(svg.read_bytes()),
                          'accent':PROJECTS[slug][1], 'ground':'#f6f8fa', 'ink':'#202b33',
                          'corner_transparency':True},
            }
            entry['theme_notes'] = 'Matching light and dark compositions retain the original logo and project hue. Light cover uses explicit neutral surfaces and contrast-adjusted ink; no image inversion or filter. Pale original OmniForge and Science Studio marks sit on compact slate mounting tiles.'
        manifest['theme_generator'] = 'scripts/generate_cover_themes.py'
        manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    assert all(digest(p.read_bytes()) == value for p,value in originals.items()), 'Approved artwork was changed'
    print(f'Generated {len(PROJECTS)} light counterparts; original dark artwork and logos preserved.')

if __name__ == '__main__':
    main()
