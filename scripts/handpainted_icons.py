"""Shared watercolor icon and brush components for README, site and daily cards."""
from pathlib import Path
import base64
from functools import lru_cache
ROOT=Path(__file__).resolve().parents[1]
ICONS=ROOT/'assets/components/icons'
TOOL_ICONS={
 'Python':'python','PyTorch':'pytorch','MATLAB':'matlab','OpenFAST / FAST.Farm':'openfast','LaTeX':'latex',
 'C':'c','C++':'cpp','TypeScript':'typescript','Three.js':'threejs','Docker':'docker','Git':'git','MySQL':'mysql',
 'Manim':'manim','Blender':'blender','Photoshop':'photoshop','Premiere':'premiere','After Effects':'after-effects',
 'Audition':'audition','Java':'java','GitHub':'github','Markdown':'markdown',
 'Adaptive Agents':'toolbox','FEM':'threejs','Topology Optimization':'compass','Multimodal AI':'compass','Canvas 2D':'notebook',
 'Geometry':'threejs','Optimization':'compass','AI Education':'notebook','Visual Narratives':'film',
 'Experiments':'toolbox','Science Communication':'notebook','Video Tools':'film','Motion':'activity','Creative Coding':'manim'}
@lru_cache(maxsize=64)
def data_uri(name):
 return 'data:image/png;base64,'+base64.b64encode((ICONS/(name+'.png')).read_bytes()).decode('ascii')
def painted_icon(name,x,y,size):
 return f'<image x="{x}" y="{y}" width="{size}" height="{size}" href="{data_uri(name)}"/>'
def brush_divider(x,y,width,height=40,fish=False):
 return f'<image x="{x}" y="{y}" width="{width}" height="{height}" preserveAspectRatio="none" href="{data_uri("divider-fish" if fish else "divider-brush")}"/>'
