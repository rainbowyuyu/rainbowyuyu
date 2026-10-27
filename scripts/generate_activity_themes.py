#!/usr/bin/env python3
"""Create display-only themes from saved metric SVGs, preserving data and dates."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from activity_card_renderer import FILES, render_card, snapshot_from_svg

ROOT = Path(__file__).resolve().parents[1]
PALETTES = {
    'light': {
        '#0b111d':'#edf1f4', '#223149':'#d5dde4', '#2b3b51':'#c3cfd8',
        '#e9f1f8':'#202b33', '#d8e6f2':'#202b33', '#9dafc4':'#465967', '#6e859f':'#5c6e7b',
        '#6ce9c4':'#19775f', '#69b5ff':'#246caa', '#a894ff':'#6851a3', '#f6c467':'#885c13',
        '#f08bb7':'#a43a6b', '#89d8e3':'#1d7884', '#74dfbd':'#19775f', '#79dfbf':'#19775f',
        '#b09cff':'#6851a3', '#b7a2ff':'#6851a3', '#87a8ff':'#396db4',
        '#172439':'#dfe7e9', '#1b2b40':'#dfe7e9', '#1f5d57':'#b1d3c7',
        '#2e8b75':'#71ae96', '#48bd99':'#3b8b70', '#77efd0':'#16624a',
        '#777':'#52616d', '#666':'#52616d', '#959da5':'#657887', '#58a6ff':'#246caa',
        '#8b949e':'#657887', '#c9d1d9':'#52616d', '#d2a8ff':'#7652a4', '#56d364':'#237b46',
    },
    'dark': {
        '#0b111d':'#1c242c', '#223149':'#35424e', '#2b3b51':'#35424e',
        '#e9f1f8':'#eef2f4', '#d8e6f2':'#e1e8ed', '#9dafc4':'#b8c4ce', '#6e859f':'#9cabb8',
        '#777':'#bdc8d1', '#666':'#bdc8d1', '#959da5':'#9cabb8', '#0366d6':'#87baf1',
        '#cb2431':'#f38b97', '#106cbc':'#87baf1', '#8b949e':'#9cabb8', '#d1d5da':'#3b4854',
    },
}

def themed_svg(source: str, theme: str) -> str:
    """Recolour presentation only; never alter text, geometry, metadata or dates."""
    palette = PALETTES[theme]
    result = re.sub(r'#[0-9a-fA-F]{3,8}\b', lambda m: palette.get(m.group().lower(), m.group()), source)
    if '<foreignObject' in result:
        # Archived metrics use XHTML/CSS instead of a native SVG background.
        ink = '#202b33' if theme == 'light' else '#eef2f4'
        muted = '#52616d' if theme == 'light' else '#b8c4ce'
        accent = '#246caa' if theme == 'light' else '#87baf1'
        surface = '#edf1f4' if theme == 'light' else '#1c242c'
        result = re.sub(r'(<svg\b[^>]*>)', lambda m: m.group(1) + f'<rect width="100%" height="100%" rx="12" fill="{surface}"/>', result, count=1)
        style = f'<style>svg{{color:{muted}}}.items-wrapper{{color:{muted}}}h2,h3{{color:{ink}}}.blue{{color:{accent}}}</style>'
        at = result.rfind('</svg>')
        result = result[:at] + style + result[at:]
    ET.fromstring(result)
    return result

def generate_metric_themes(root: Path = ROOT) -> list[str]:
    outputs = []
    for source in sorted((root / 'github-metrics').glob('*.svg')):
        if source.stem.endswith(('-light', '-dark')):
            continue
        raw = source.read_text(encoding='utf-8')
        saved = snapshot_from_svg(raw, source.name, source.parent) if source.name in FILES else None
        if saved is not None:
            # Native snapshots own both themes; a restyle retains source time/data.
            source.write_text(render_card(saved, 'dark'), encoding='utf-8', newline='\n')
        for theme in ('light', 'dark'):
            target = source.with_name(source.stem + '-' + theme + '.svg')
            result = render_card(saved, theme) if saved is not None else themed_svg(raw, theme)
            target.write_text(result, encoding='utf-8', newline='\n')
            outputs.append(target.relative_to(root).as_posix())
    return outputs

if __name__ == '__main__':
    print(f'Generated {len(generate_metric_themes())} themed metric images from existing snapshots; no API request or freshness change.')
