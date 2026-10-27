"""Self-contained hand-painted assets; text and data stay editable SVG."""
import base64
from functools import lru_cache
from pathlib import Path

ART = Path(__file__).resolve().parents[1] / 'assets/profile/studio'


@lru_cache(maxsize=20)
def image_uri(name):
    mime = 'image/jpeg' if name.endswith('.jpg') else 'image/png'
    return 'data:' + mime + ';base64,' + base64.b64encode((ART / name).read_bytes()).decode('ascii')


def illustration(name, x, y, width, height, moving=False):
    cls = ' class="studio-float"' if moving else ''
    return f'<image{cls} x="{x}" y="{y}" width="{width}" height="{height}" href="{image_uri(name)}" preserveAspectRatio="xMidYMid meet"/>'


def star(x, y, color, size=7, delay=0):
    return f'<path class="studio-star" style="animation-delay:{delay}s;transform-origin:{x}px {y}px" d="M{x} {y-size}q1 {size-1} {size} {size}q-{size-1} 1 -{size} {size}q-1 -{size-1} -{size} -{size}q{size-1} -1 {size} -{size}Z" fill="{color}"/>'


MOTION = '''.studio-float{animation:studio-float 6s ease-in-out infinite}
.studio-star{animation:studio-twinkle 4s ease-in-out infinite}
@keyframes studio-float{50%{transform:translateY(-3px)}}
@keyframes studio-twinkle{50%{opacity:.35;transform:scale(.8)}}
@media(prefers-reduced-motion:reduce){.studio-float,.studio-star{animation:none!important}}'''
