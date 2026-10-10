"""Draw every shape the Riftwater port's code names, by the kind of geometry it is written as, over its ground."""
import os; D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, "out"); ROOT = os.path.abspath(os.path.join(D, *[".."] * 5))
import sys, os, pickle, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "freeform/lib/ports/riftwater/scripts")); sys.path.insert(0, os.path.join(ROOT, "freeform/lib"))
import plan as P
from pgmvox import noise
from pgmvox.noise import spline
h = pickle.load(open(f"{OUT}/stack.pkl", "rb")); land = h["land"]
S = 5; X0, Z0 = P.X_MIN, P.Z_MIN
base = np.array(Image.open(f"{OUT}/img/spoil.png").convert("L").convert("RGB")).astype(float)
base = base * 0.55 + 255 * 0.45
im = Image.fromarray(base.astype(np.uint8)).resize((land.shape[0] * S, land.shape[1] * S), Image.NEAREST)
d = ImageDraw.Draw(im)
sys.path.insert(0, D); from style import KIND as C
px = lambda x, z: ((x - X0 + 0.5) * S, (z - Z0 + 0.5) * S)
def ellipse(c, rx, rz, kind="ell", w=3):
    (x, z) = c; a, b = px(x - rx, z - rz), px(x + rx, z + rz); d.ellipse([a, b], outline=C[kind], width=w)
    d.ellipse([px(x, z)[0] - 3, px(x, z)[1] - 3, px(x, z)[0] + 3, px(x, z)[1] + 3], fill=C[kind])
def path(pts, kind="line", w=3):
    d.line([px(x, z) for x, z in pts], fill=C[kind], width=w, joint="curve")
def poly(pts, kind="poly", w=3):
    d.polygon([px(x, z) for x, z in pts], outline=C[kind], width=w)
marks = []
def mark(n, x, z, kind):
    X, Y = px(x, z); d.rounded_rectangle([X - 10, Y - 9, X + 10, Y + 9], 4, fill=(255, 255, 255), outline=C[kind], width=2)
    d.text((X, Y), str(n), fill=(20, 20, 20), anchor="mm", font=FONT); marks.append(n)
try: FONT = ImageFont.truetype("DejaVuSans-Bold.ttf", 12)
except OSError: FONT = ImageFont.load_default()
# noise lines: the outline's four edges and the ridge's foot and crest — one offset per row, no points
edge = land & ~np.pad(land, 1, constant_values=False)[1:-1, 2:] | land & ~np.pad(land, 1, constant_values=False)[1:-1, :-2] \
     | land & ~np.pad(land, 1, constant_values=False)[2:, 1:-1] | land & ~np.pad(land, 1, constant_values=False)[:-2, 1:-1]
for i, k in zip(*np.nonzero(edge)):
    d.rectangle([i * S, k * S, i * S + S - 1, k * S + S - 1], fill=C["noise"])
sh = land.shape; zs = np.arange(P.Z_MIN, P.Z_MAX + 1)
foot = noise.line(sh, "z", 24, seed=40, amp=4, base=-100)[0]
d.line([px(float(x), float(z)) for x, z in zip(foot, zs)], fill=C["noise"], width=2)
# axis bands: the westfall
d.line([px(-114, P.Z_MIN), px(-114, P.Z_MAX)], fill=C["band"], width=2)
# polylines (splined): river, routes, spit, spurs
path(spline(P.RIVER, 0.5), w=5)
for r in P.ROUTES: path(spline(r["pts"], 1.0), w=2)
path([(-92, 30), (-86, 24), (-83, 21)], w=3)
path([(-114, -68), (-98, -74), (-82, -80)], w=3); path([(-114, 70), (-100, 76), (-88, 82)], w=3)
# polygons and rectangles
poly([(-76, -53), (-56, -53), (-56, -34), (-76, -34)])
poly(P.NORTH_WOOD)
x0, z0, x1, z1 = P.FIELD; poly([(x0, z0), (x1, z0), (x1, z1), (x0, z1)])
# circles and ellipses: centre and radii
ellipse((-44, -78), 16, 11)                       # chapel hill (Gauss, soft: one radius drawn)
ellipse((-84, 20), 12.5, 9.5)                     # pond
ellipse((-97, -7), 12, 9.5)                       # spawn shoulder
ellipse((-66, -44), 11, 11); ellipse((-66, 48), 9, 9)   # monument levels
ellipse((-66, 48), 8.5, 8.5, w=2)                 # the green
ellipse((-22, 74), 16, 20)                        # knoll
ellipse((-74, 22), 4, 4, w=2)                     # outlet
ellipse((-50, 38), 10.5, 10.5)                    # sinkhole
ellipse((-101, 79), 7, 5.6)                       # spoil
for n, (x, z, k) in enumerate([(-44, -92 + 6, "ell"), (-84, 8, "ell"), (-97, -19, "ell"), (-66, -58, "ell"), (-66, 61, "ell"),
                               (-22, 56, "ell"), (-50, 26, "ell"), (-101, 71, "ell"), (-60, 9, "line"), (-48, -48, "line"),
                               (-90, 26, "line"), (-100, -76, "line"), (-62, -36, "poly"), (-112, -80, "poly"), (-40, 57, "poly"),
                               (-104, 0, "noise"), (-12, -80, "noise"), (-117, 40, "band")], 1):
    mark(n, x, z, k)
im.save(f"{OUT}/img/overlay.png"); print(im.size, len(marks))
