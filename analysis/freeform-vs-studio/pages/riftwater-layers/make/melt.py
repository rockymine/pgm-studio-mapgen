"""Forms melting into each other: two hills of one layer, a hill on the ground, a crater in a hill, each meeting
hard (max or min) and through a smooth max or min whose width k is how far the seam is rounded."""
import os; D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, "out"); ROOT = os.path.abspath(os.path.join(D, *[".."] * 5))
import sys, json, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, D); sys.path.insert(0, os.path.join(ROOT, "freeform/lib"))
from pgmvox import landform as LF, shapes
from pgmvox.noise import fbm
from style import relief, outline
N, S = 64, 5
X, Z = np.meshgrid(np.arange(N, dtype=float), np.arange(N, dtype=float), indexing="ij")
ground = 48.3 + 1.6 * fbm((N, N), 24, 2, seed=5) + 0.6 * fbm((N, N), 8, 2, seed=6)
everywhere = np.ones((N, N), bool)

def smin(a, b, k):
    """The lower of a and b, rounded over a seam k wide; k = 0 is the plain min."""
    if k <= 0: return np.minimum(a, b)
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)
def smax(a, b, k): return -smin(-a, -b, k)
def merge(ra, rb, p):
    """Two rises over the same ground, joined by their p-norm: p = 0 stands for the plain max; a lower p fills
    the saddle between them, and where neither rises nothing changes."""
    if p == 0: return np.maximum(ra, rb)
    return (np.maximum(ra, 0) ** p + np.maximum(rb, 0) ** p) ** (1 / p)

A, B = shapes.ellipse_distance(X, Z, (24, 34), 14, 11), shapes.ellipse_distance(X, Z, (40, 30), 13, 10, angle=30)
hill = shapes.ellipse_distance(X, Z, (32, 32), 22, 17, angle=15)
pit = shapes.ellipse_distance(X, Z, (40, 32), 9, 8)
rows = [
    ("Zwei Hügel, eine Ebene", "Anstieg: max der beiden, dann p-Norm", [0, 3, 1.6],
     lambda p: ground + merge(LF.mound(ground, A, 9.0, power=1.6) - ground, LF.mound(ground, B, 8.0, power=1.6) - ground, p), [A, B]),
    ("Hügel auf welligem Grund", "Boden: max(Grund, Hügel)", [0, 4, 8],
     lambda k: smax(ground, np.where(hill < 1, 40 + 17 * (1 - np.clip(hill, 0, 1) ** 1.6), -100), k), [hill]),
    ("Krater im Hügel", "Boden: min(Hügel, Schüssel)", [0, 4, 8],
     lambda k: smin(LF.mound(ground, hill, 10.0, power=1.6), 44 + 1.0 * np.maximum(0, pit * 9 - 2), k), [hill, pit]),
]
def label_of(row, k):
    if k == 0: return "hart"
    return (f"p = {k}" if row == 0 else f"k = {k}").replace(".", ",")
tiles, profiles = [], {}
for label, how, ks, make, areas in rows:
    lines = []
    for col, k in enumerate(ks):
        H = np.round(make(k))
        img = relief(H, everywhere, s=S, step=1, major=5)
        for e in areas: img = outline(img, e < 1, S, tint=0.0)
        im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8).transpose(1, 0, 2)); dr = ImageDraw.Draw(im)
        y = (32 + .5) * S; dr.line([(0, y), (N * S, y)], fill=(255, 255, 255), width=1)
        name = f"melt-{len(profiles)}-{col}"; im.save(f"{OUT}/img/{name}.png")
        tiles.append(dict(row=label, col=label_of(len(profiles), k), img=name, how=how))
        lines.append([int(v) for v in H[:, 32]])
    profiles[label] = dict(ground=[round(float(v), 1) for v in ground[:, 32]], lines=lines,
                           cols=[label_of(len(profiles), k) for k in ks])
json.dump(dict(tiles=tiles, profiles=profiles, headers=["hart", "weicher", "am weichsten"]), open(f"{OUT}/melt.json", "w"))
print(len(tiles))
