"""Restyle upstream 3D rainbow SVG without changing geometry or contribution data."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def generate_rainbow_contributions(root=ROOT):
    folder = root / 'profile-3d-contrib'
    source = (folder / 'profile-night-rainbow.svg').read_text(encoding='utf-8')
    outputs = []
    for theme in ('light', 'dark'):
        dark = theme == 'dark'
        raw = source.replace('#00000f', '#151b20' if dark else '#fbfcfd')
        raw = re.sub(r'(<svg\b[^>]*)(>)', r'\1 role="img" aria-labelledby="rainbow-title rainbow-description"\2<title id="rainbow-title">Rainbow contribution landscape</title><desc id="rainbow-description">GitHub contribution history, repository languages and public activity. Column geometry and values follow the saved upstream snapshot; the rainbow is decorative.</desc>', raw, count=1)
        raw = raw.replace('#eeeeff', '#ecf1f4' if dark else '#25323d')
        raw = raw.replace('#aaaaaa', '#a8b6c3' if dark else '#627381')
        raw = raw.replace('rgb(255,200,55)', '#c9a5e0' if dark else '#8760a4')
        # The same spatial rainbow phase remains; colours are softer in daylight.
        if not dark:
            def daylight(match):
                rgb = [int(match.group(i)) for i in range(1, 4)]
                return 'rgb('+', '.join(str(round(v*.74+255*.26)) for v in rgb)+')'
            raw = re.sub(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', daylight, raw)
        # Base fills make reduced-motion and paused versions real rainbow stills.
        def base_colour(match):
            name, body = match.group(1), match.group(2)
            keyframe = re.search(r'@keyframes '+re.escape(name)+r'\{0\.00%\{fill:([^}]+)\}', raw)
            fill = f'fill:{keyframe.group(1)};' if keyframe else ''
            return '.'+name+'{'+fill+body+'}'
        raw = re.sub(r'\.(rb-l\d-(?:top|left|right))\{([^}]+)\}', base_colour, raw)
        # Frame-by-frame reduced-motion fallback uses the saved phase per tile.
        def freeze_tile(match):
            tag = match.group(0)
            cls = re.search(r'class="(rb-l\d-(?:top|left|right))"', tag)
            phase = re.search(r'animation-delay:\s*(-?[\d.]+)s', tag)
            if not cls:
                return tag
            keys = re.search(r'@keyframes '+re.escape(cls.group(1))+r'\{(.*?)(?=\n|$)', raw)
            if not keys:
                return tag
            colors = re.findall(r'([\d.]+)%\{fill:rgb\((\d+),\s*(\d+),\s*(\d+)\)\}', keys.group(1))
            t = (-float(phase.group(1)) % 10)/10*100 if phase else 0
            for a,b in zip(colors,colors[1:]):
                if float(a[0]) <= t <= float(b[0]):
                    f=(t-float(a[0]))/(float(b[0])-float(a[0]))
                    c=[round(int(a[i])+(int(b[i])-int(a[i]))*f) for i in (1,2,3)]
                    return tag.replace('style="', 'style="fill:rgb('+','.join(map(str,c))+');', 1)
            return tag
        raw = re.sub(r'<(?:path|polygon|rect)\b[^>]*class="rb-l[^>]*>', freeze_tile, raw)
        raw = raw.replace('</svg>', '<style>@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}</style></svg>')
        ET.fromstring(raw)
        for static in (False, True):
            result = raw
            suffix = '-static' if static else ''
            if static:
                result = re.sub(r'<(?:animate|animateTransform|animateMotion|set)\b[^>]*(?:/>|>.*?</(?:animate|animateTransform|animateMotion|set)>)','',result,flags=re.S)
                result = result.replace('</svg>','<style>*{animation:none!important;transition:none!important}</style></svg>')
            path=folder/f'profile-rainbow-{theme}{suffix}.svg'
            path.write_text(result,encoding='utf-8',newline='\n')
            outputs.append(path.relative_to(root).as_posix())
    return outputs


if __name__ == '__main__':
    print('\n'.join(generate_rainbow_contributions()))
