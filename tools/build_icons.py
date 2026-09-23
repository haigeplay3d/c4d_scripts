"""Build original geometric SVG/PNG/TIF script icons. Requires Pillow.

Run from any directory: python tools/build_icons.py
Writes only the 13 declared icon assets and the preview sheet; no C4D API calls.
SVG and raster outputs share the same primitives, not generated bitmap edits.
"""
from pathlib import Path
import math
import os
import json
import hashlib
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets' / 'icons'
INK, ACCENT, BLUE = '#A4B8CC', '#FFB454', '#45C5D5'
PURPLE = '#AC94F4'
SCALE = 8


class Icon:
    def __init__(self):
        self.image = Image.new('RGBA', (64*SCALE,64*SCALE))
        self.draw = ImageDraw.Draw(self.image)
        self.svg = []

    def line(self, points, color=INK, width=3):
        points = list(points)
        self.draw.line([(round(x*SCALE),round(y*SCALE)) for x,y in points],
                       fill=color, width=round(width*SCALE), joint='curve')
        for x,y in (points[0],points[-1]):
            radius=width*SCALE/2
            self.draw.ellipse((x*SCALE-radius,y*SCALE-radius,x*SCALE+radius,y*SCALE+radius),fill=color)
        data=' '.join(f'{x:g},{y:g}' for x,y in points)
        self.svg.append(f'<polyline points="{data}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')

    def polygon(self, points, color=INK, fill=None, width=3):
        points=list(points)
        if fill:
            self.draw.polygon([(round(x*SCALE),round(y*SCALE)) for x,y in points],fill=fill)
            data=' '.join(f'{x:g},{y:g}' for x,y in points)
            self.svg.append(f'<polygon points="{data}" fill="{fill}"/>')
        if color: self.line(points+[points[0]],color,width)

    def circle(self, x, y, radius, color=INK, fill=None, width=3):
        box=((x-radius)*SCALE,(y-radius)*SCALE,(x+radius)*SCALE,(y+radius)*SCALE)
        if fill:self.draw.ellipse(box,fill=fill)
        if color:
            # Match SVG centered stroke by drawing the outer and inner boundary.
            pts=[(x+radius*math.cos(t*math.tau/128),y+radius*math.sin(t*math.tau/128)) for t in range(129)]
            self.draw.line([(round(a*SCALE),round(b*SCALE)) for a,b in pts],fill=color,width=round(width*SCALE),joint='curve')
        self.svg.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill or "none"}" stroke="{color or "none"}" stroke-width="{width}"/>')

    def box(self,x,y,w,h,color=INK,fill=None,width=3):
        self.polygon([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],color,fill,width)

    def arrow(self,a,b,color=ACCENT,width=3,head=5):
        self.line([a,b],color,width)
        theta=math.atan2(b[1]-a[1],b[0]-a[0])
        left=(b[0]-head*math.cos(theta-.65),b[1]-head*math.sin(theta-.65))
        right=(b[0]-head*math.cos(theta+.65),b[1]-head*math.sin(theta+.65))
        self.line([left,b,right],color,width)

    def finish(self, folder, stem):
        ASSETS.mkdir(parents=True,exist_ok=True)
        text='<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 64 64">\n'+'\n'.join(self.svg)+'\n</svg>\n'
        (ASSETS/(stem+'.svg')).write_text(text,encoding='utf-8')
        raster=self.image.resize((128,128),Image.Resampling.LANCZOS)
        raster.save(ASSETS/(stem+'.png'))
        raster.save(ROOT/'c4d_scripts'/folder/('HG_'+stem+'.tif'),compression='raw')
        return raster


def make_icons():
    result=[]
    def save(icon,folder,title,stem=None):
        stem=stem or folder
        result.append((stem,title,icon.finish(folder,stem)))

    i=Icon()
    i.polygon([(10,10),(52,10),(52,36),(29,36),(18,46),(18,36),(10,36)],BLUE)
    i.line([(19,19),(43,19)],INK);i.line([(19,27),(35,27)],INK)
    i.box(36,43,14,12,ACCENT)
    save(i,'AnnotationFromName','Name annotation')

    i=Icon()
    for y in (10,26,42):
        i.box(13,y,38,12,INK,width=2.5)
        i.circle(20,y+6,3.5,None,ACCENT)
        i.line([(34,y+6),(44,y+6)],INK,2)
    save(i,'C4D_BatchDisableBasicEnabled','Disable all generators')

    i=Icon()
    i.polygon([(12,11),(28,11),(33,26),(23,41),(29,53),(13,53),(8,40),(18,25)],BLUE)
    i.line([(10,39),(25,39)],INK,2);i.line([(17,25),(31,25)],INK,2)
    i.circle(47,36,9,INK,width=2.5);i.line([(47,24),(47,35)],ACCENT,3.5)
    save(i,'DeformerToggle','Deformer visibility')

    i=Icon()
    i.box(22,8,20,17,INK, width=2.5)
    i.line([(26,12),(38,21)],ACCENT);i.line([(38,12),(26,21)],ACCENT)
    i.line([(32,27),(32,35)],INK,2.5)
    i.line([(13,42),(13,35),(51,35),(51,42)],INK,2.5)
    i.line([(32,35),(32,42)],INK,2.5)
    for x in (7,26,45):i.box(x,43,12,11,BLUE,width=2.5)
    save(i,'DeleteNulls','Remove null / retain children')

    i=Icon()
    i.box(20,20,24,24,BLUE)
    i.line([(9,23),(9,9),(23,9)],INK);i.line([(41,55),(55,55),(55,41)],INK)
    i.arrow((26,38),(48,16),ACCENT,3,6)
    i.arrow((38,26),(16,48),ACCENT,3,6)
    save(i,'FigureScale','Scale to target size')

    i=Icon()
    i.box(9,15,38,32,BLUE)
    i.arrow((14,10),(42,10),INK,2.5,4)
    i.arrow((4,43),(4,20),INK,2.5,4)
    i.box(35,35,20,18,ACCENT,fill='#253546')
    i.line([(40,35),(40,29),(44,25),(47,25),(51,29),(51,35)],ACCENT)
    i.circle(45,43,2,None,ACCENT)
    save(i,'PlaneLockRatio','Lock plane proportions')

    i=Icon()
    i.polygon([(9,22),(21,15),(33,22),(21,29)],INK)
    i.line([(9,22),(9,35),(21,42),(33,35),(33,22)],INK)
    i.line([(21,29),(21,42)],INK,2)
    i.polygon([(36,32),(47,26),(57,32),(47,38)],BLUE)
    i.line([(36,32),(36,45),(47,51),(57,45),(57,32)],BLUE)
    i.line([(47,38),(47,51)],BLUE,2)
    i.arrow((28,9),(50,19),ACCENT,3,5)
    save(i,'PositionWorldFollow','Copy world transform')

    i=Icon()
    for x,y,c in ((15,25,BLUE),(32,41,ACCENT),(49,20,PURPLE)):
        i.line([(x,10),(x,54)],INK,2.5)
        i.box(x-6,y-5,12,10,c,fill='#253546')
    save(i,'PresetsByHaigeC4D','Personal preferences','presetsbyhaigec4d')

    i=Icon()
    i.circle(32,32,16,BLUE, width=3);i.circle(32,32,7,INK,width=2.5)
    for a,b in [((32,13),(32,4)),((51,32),(60,32)),((32,51),(32,60)),((13,32),(4,32))]:i.arrow(a,b,ACCENT,2.5,4)
    save(i,'RadialStretch','Radial ring stretch')

    i=Icon()
    for x,y,c in ((23,22,BLUE),(43,27,PURPLE),(30,43,ACCENT)):
        i.circle(x,y,11,c,fill='#253546',width=3)
        i.line([(x-5,y-4),(x-2,y-6)],c,2)
    i.circle(48,48,2,None,INK);i.circle(53,42,2,None,INK)
    save(i,'RandomColorStandardMaterial','Random standard material')

    i=Icon()
    i.arrow((15,49),(15,10),INK,2.5,4);i.arrow((15,49),(54,49),INK,2.5,4)
    for x in (28,40,52):
        for y in (13,25,37):i.circle(x,y,1.5,None,BLUE)
    i.circle(30,34,4,ACCENT,width=2.5)
    i.arrow((35,31),(40,25),ACCENT,2.5,4)
    i.box(37,22,6,6,None,ACCENT)
    save(i,'RoundXYZ','Round position / angle')

    i=Icon()
    i.box(10,10,44,44,BLUE)
    for v in (21,32,43):
        i.line([(v,10),(v,54)],INK,2)
        i.line([(10,v),(54,v)],INK,2)
    i.box(32,21,11,11,ACCENT,fill=ACCENT,width=2)
    save(i,'SquareSegementsForPlane','Square plane segments')

    i=Icon()
    i.polygon([(8,20),(25,10),(42,20),(25,30)],BLUE)
    i.line([(8,29),(25,39),(35,33)],INK)
    i.line([(8,38),(25,48),(31,44)],INK)
    i.polygon([(37,33),(47,28),(57,38),(46,51),(34,40)],ACCENT,fill='#253546')
    i.circle(46,35,2,None,ACCENT)
    save(i,'TagsSameColor','Layer color to icons')
    return result


def preview(items):
    image=Image.new('RGB',(1200,900),'#151D27');d=ImageDraw.Draw(image)
    def font(size):
        try:return ImageFont.truetype(str(Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts/segoeui.ttf'),size)
        except OSError:return ImageFont.load_default()
    d.text((32,20),'HAIGE / C4D SCRIPTS',font=font(28),fill='#E2EAF2')
    d.text((32,60),'13 function icons  |  SVG master + 128 px transparent TIFF  |  64 / 32 px previews',font=font(16),fill='#93A8BD')
    for n,(stem,title,icon) in enumerate(items):
        x=24+(n%4)*294;y=104+(n//4)*190
        d.rounded_rectangle((x,y,x+278,y+174),radius=12,fill='#202B38')
        image.paste(icon.resize((64,64),Image.Resampling.LANCZOS),(x+18,y+18),icon.resize((64,64),Image.Resampling.LANCZOS))
        small=icon.resize((32,32),Image.Resampling.LANCZOS)
        image.paste(small,(x+103,y+35),small)
        d.rounded_rectangle((x+164,y+17,x+258,y+84),radius=6,fill='#F0F3F6')
        image.paste(small,(x+195,y+35),small)
        label='HG_'+stem
        label_font=font(15)
        for size in range(15,9,-1):
            label_font=font(size)
            if d.textbbox((0,0),label,font=label_font)[2] <= 246: break
        d.text((x+16,y+106),label,font=label_font,fill='#E2EAF2')
        d.text((x+16,y+134),title,font=font(14),fill='#9DAFC1')
    image.save(ASSETS/'preview.png')


if __name__=='__main__':
    icons=make_icons()
    preview(icons)
    entries=[]
    for script in sorted((ROOT/'c4d_scripts').glob('*/*.py')):
        icon=script.with_suffix('.tif')
        if script.stem not in {'HG_'+name for name,_,_ in icons}:
            continue
        entries.append({'script':script.relative_to(ROOT).as_posix(),
                        'icon':icon.relative_to(ROOT).as_posix(),
                        'sha256':hashlib.sha256(icon.read_bytes()).hexdigest()})
    (ASSETS/'manifest.json').write_text(json.dumps(
        {'size':[128,128],'mode':'RGBA','icons':entries},indent=2),encoding='utf-8')
    print('Built',len(icons),'SVG, PNG and TIFF icons; preview:',ASSETS/'preview.png')
