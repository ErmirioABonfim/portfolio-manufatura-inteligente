from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

W, H = 960, 540
BG = "#071016"
PANEL = "#0d1b24"
GRID = "#17303a"
WHITE = "#f4f7f5"
MUTED = "#9fb0b6"
GREEN = "#75efc0"
BLUE = "#3b82f6"
RED = "#ef4444"
YELLOW = "#fbbf24"

def font(size, bold=False):
    filenames = ["DejaVuSans-Bold.ttf", "Arial Bold.ttf"] if bold else ["DejaVuSans.ttf", "Arial.ttf"]
    roots = [
        Path("/usr/share/fonts/truetype/dejavu"),
        Path("/Library/Fonts"),
        Path.home() / "Library/Fonts",
        Path("C:/Windows/Fonts"),
    ]
    for root in roots:
        for filename in filenames:
            try:
                return ImageFont.truetype(str(root / filename), size)
            except OSError:
                pass
    for filename in filenames:
        try:
            return ImageFont.truetype(filename, size)
        except OSError:
            pass
    return ImageFont.load_default()

def text(draw, xy, value, size, fill=WHITE, bold=False, anchor=None):
    draw.text(xy, value, font=font(size, bold), fill=fill, anchor=anchor)

def worker(draw, x, y, scale=1.0, vest=GREEN, helmet=YELLOW):
    # Stylized worker, deliberately illustrative rather than photorealistic.
    r = int(18 * scale)
    draw.ellipse((x-r, y-r-78*scale, x+r, y+r-78*scale), fill="#b9c7cb")
    draw.pieslice((x-r-3, y-r-85*scale, x+r+3, y+r-67*scale), 180, 360, fill=helmet)
    draw.polygon([(x-30*scale,y-55*scale),(x+30*scale,y-55*scale),(x+43*scale,y+38*scale),(x-43*scale,y+38*scale)], fill="#203743")
    draw.polygon([(x-24*scale,y-49*scale),(x+24*scale,y-49*scale),(x+31*scale,y+18*scale),(x-31*scale,y+18*scale)], fill=vest)
    draw.rectangle((x-28*scale,y-42*scale,x-20*scale,y+12*scale), fill="#dce7e8")
    draw.rectangle((x+20*scale,y-42*scale,x+28*scale,y+12*scale), fill="#dce7e8")
    draw.line((x-23*scale,y+36*scale,x-32*scale,y+95*scale), fill="#8da0a6", width=max(3,int(9*scale)))
    draw.line((x+23*scale,y+36*scale,x+32*scale,y+95*scale), fill="#8da0a6", width=max(3,int(9*scale)))
    draw.rectangle((x-45*scale,y+91*scale,x-20*scale,y+100*scale), fill="#1b2e37")
    draw.rectangle((x+20*scale,y+91*scale,x+45*scale,y+100*scale), fill="#1b2e37")

def bbox(draw, box, color=GREEN):
    x1,y1,x2,y2=box
    width=3
    draw.rectangle(box, outline=color, width=width)
    l=22
    for a,b,cx,cy in [(x1,y1,x1+l,y1),(x1,y1,x1,y1+l),(x2,y1,x2-l,y1),(x2,y1,x2,y1+l),(x1,y2,x1+l,y2),(x1,y2,x1,y2-l),(x2,y2,x2-l,y2),(x2,y2,x2,y2-l)]:
        draw.line((a,b,cx,cy), fill=color, width=6)

def label(draw, x, y, value, color=BLUE):
    bb=draw.textbbox((0,0),value,font=font(15,True))
    w=bb[2]-bb[0]+18
    draw.rectangle((x,y,x+w,y+28), fill=color)
    text(draw,(x+9,y+6),value,15,WHITE,True)

def base_scene():
    im=Image.new("RGB",(W,H),BG)
    d=ImageDraw.Draw(im)
    # Technical grid.
    for x in range(0,W,48): d.line((x,0,x,H),fill=GRID,width=1)
    for y in range(0,H,48): d.line((0,y,W,y),fill=GRID,width=1)
    # Factory silhouettes and a restricted zone.
    d.rectangle((30,115,430,420),fill="#0b1a22",outline="#23414d",width=2)
    d.rectangle((70,170,190,360),fill="#16303b")
    d.rectangle((220,205,405,360),fill="#122832")
    d.line((70,150,405,150),fill="#31525d",width=8)
    d.rectangle((470,120,925,420),fill="#0a1820",outline="#23414d",width=2)
    for x in (500,650,800): d.line((x,145,x,370),fill="#24424d",width=7)
    d.polygon([(500,390),(710,390),(785,475),(430,475)],outline=RED,fill="#24151a")
    worker(d,260,300,1.05)
    worker(d,590,315,.98)
    worker(d,785,315,.98,vest="#d6a62c")
    text(d,(32,28),"MIS-VISION",27,GREEN,True)
    text(d,(32,64),"VISÃO COMPUTACIONAL INDUSTRIAL",14,MUTED,True)
    text(d,(928,32),"CENA CONCEITUAL",13,MUTED,True,"ra")
    return im

frames=[]
N=48
for i in range(N):
    im=base_scene(); d=ImageDraw.Draw(im)
    # scanner line, loops gently across the scene
    scan_x=int(60+(i/(N-1))*820)
    d.line((scan_x,105,scan_x,485),fill=GREEN,width=2)
    d.rectangle((scan_x-18,105,scan_x+18,485),fill="#0e2a28")
    # Restore a thin bright center after translucent-style slab.
    d.line((scan_x,105,scan_x,485),fill=GREEN,width=2)
    if i>=7:
        bbox(d,(202,178,318,410),GREEN)
    if i>=11:
        bbox(d,(535,196,645,424),GREEN)
    if i>=15:
        bbox(d,(730,196,840,424),RED if i>=28 else GREEN)
    if i>=18:
        label(d,202,145,"PESSOA 0.96",BLUE)
        label(d,535,163,"PESSOA 0.94",BLUE)
        label(d,730,163,"PESSOA 0.93",BLUE)
    if i>=22:
        label(d,205,416,"CAPACETE · COLETE · LUVAS",GREEN)
        label(d,520,430,"CAPACETE · BOTAS",GREEN)
    if i>=28:
        label(d,700,430,"LUVAS NÃO DETECTADAS",RED)
        text(d,(600,486),"EXCEÇÃO VISUAL PARA VERIFICAÇÃO",14,RED,True)
    if i>=34:
        # Event panel arrives from the right.
        p=min(1,(i-34)/8)
        x=int(W-(330*p))
        d.rectangle((x,92,x+315,262),fill=PANEL,outline="#35515c",width=2)
        text(d,(x+22,114),"EVENTO",13,GREEN,True)
        text(d,(x+22,144),"Luvas não detectadas",24,WHITE,True)
        text(d,(x+22,180),"Pessoa 03 · Área de processo",15,MUTED)
        d.line((x+22,214,x+293,214),fill="#35515c",width=1)
        text(d,(x+22,229),"Evidência pronta para análise humana",13,WHITE)
    if i>=40:
        # Transformation rail.
        d.rectangle((0,500,W,540),fill="#061016")
        stages=[("CÂMERA",70),("IA",265),("REGRA",430),("EVENTO",620),("DECISÃO",805)]
        for j,(name,x) in enumerate(stages):
            text(d,(x,520),name,13,GREEN if j<=((i-40)//2) else MUTED,True,"mm")
            if j<4: text(d,(x+96,520),"→",18,"#52666f",True,"mm")
    frames.append(im)

# Hold the final state, then make a compact optimized palette GIF.
frames.extend([frames[-1].copy() for _ in range(10)])
pal=[f.convert("P",palette=Image.Palette.ADAPTIVE,colors=128) for f in frames]
out=ASSETS/"mis-vision-showcase.gif"
pal[0].save(out,save_all=True,append_images=pal[1:],duration=90,loop=0,optimize=True,disposal=2)
frames[-1].save(ASSETS/"mis-vision-showcase-poster.png",optimize=True)
print(out, out.stat().st_size)
