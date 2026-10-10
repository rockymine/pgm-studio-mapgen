"""A hill and a crater on rolling ground, as pgmvox makes them and with a soft edge: the op's change to the ground
weighted down to nothing over the outer share of its area, so its edge meets the ground without a kink."""
import os; D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, "out"); ROOT = os.path.abspath(os.path.join(D, *[".."] * 5))
import sys, json, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, D); sys.path.insert(0, os.path.join(ROOT, "freeform/lib"))
from pgmvox import landform as LF, shapes
from pgmvox.noise import fbm, smoothstep
from style import relief, outline, KIND
N, S = 64, 5
X, Z = np.meshgrid(np.arange(N, dtype=float), np.arange(N, dtype=float), indexing="ij")
ground = 48.3 + 1.6 * fbm((N, N), 24, 2, seed=5) + 0.6 * fbm((N, N), 8, 2, seed=6)
everywhere = np.ones((N, N), bool)
C, RX, RZ, BAND = (32, 32), 20, 15, 0.35

def soft(H, shaped, e, band=BAND):
    """The op's change to the ground, in full inside, eased to nothing over the outer `band` of the area."""
    return H + (shaped - H) * smoothstep(1.0, 1.0 - band, e)

def area(rough):
    return shapes.ellipse_distance(X, Z, C, RX, RZ, angle=20) + rough * 0.14 * fbm((N, N), 6, 2, seed=13)

cols = [("wie jetzt", 0.0, False), ("weicher Rand", 0.0, True), ("weicher und rauer Rand", 1.0, True)]
tiles, profiles = [], {}
for label, op in (("Hügel", "mound"), ("Krater", "crater")):
    lines = []
    for col, (title, rough, smooth) in enumerate(cols):
        e = area(rough)
        shaped = LF.mound(ground, e, 9.0, power=1.6) if op == "mound" else LF.crater(ground, e * RX, 40, RX, flat=2, slope=8 / (RX - 2))
        H = np.round(soft(ground, shaped, e) if smooth else shaped)
        img = outline(relief(H, everywhere, s=S, step=1, major=5), e < 1, S, tint=0.0)
        im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8).transpose(1, 0, 2)); dr = ImageDraw.Draw(im)
        y = (C[1] + .5) * S; dr.line([(0, y), (N * S, y)], fill=(255, 255, 255), width=1)
        name = f"soft-{op}-{col}"; im.save(f"{OUT}/img/{name}.png")
        tiles.append(dict(row=label, col=title, img=name))
        lines.append([int(v) for v in H[:, C[1]]])
    profiles[label] = dict(ground=[round(float(v), 1) for v in ground[:, C[1]]], lines=lines, cols=[c[0] for c in cols])
json.dump(dict(tiles=tiles, profiles=profiles), open(f"{OUT}/soft.json", "w"))
print(len(tiles))
