"""One hill and one crater, each over four kinds of area: an ellipse, the same ellipse warped, a lasso polygon,
the polygon with a ragged rim. The ops are pgmvox's own; only the distance they read changes."""
import os; D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, "out"); ROOT = os.path.abspath(os.path.join(D, *[".."] * 5))
import os, sys, json, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, D); sys.path.insert(0, os.path.join(ROOT, "freeform/lib"))
from pgmvox import landform as LF, shapes
from pgmvox.noise import fbm
from style import relief, outline, KIND
N, S = 64, 5
X, Z = np.meshgrid(np.arange(N, dtype=float), np.arange(N, dtype=float), indexing="ij")
ground = 48.3 + 0.4 * fbm((N, N), 14, 2, seed=3)
everywhere = np.ones((N, N), bool)
C, RX, RZ = (32, 32), 20, 14
LASSO = [(10, 30), (16, 14), (30, 9), (40, 17), (52, 12), (57, 26), (49, 38), (54, 52), (38, 55), (30, 44), (17, 50)]

def ellipse():
    """0 at the centre, 1 on the rim; the rim is RX blocks out along the long axis."""
    return shapes.ellipse_distance(X, Z, C, RX, RZ, angle=25), float(RX)

def warped(strength=1.0):
    """The ellipse's distance read at shifted coordinates (domain warp), with lobes around its rim and fine
    noise: still a centre and radii, no longer a circle."""
    wx, wz = (7 * strength * fbm((N, N), 18, 2, seed=s) for s in (11, 12))
    e = shapes.ellipse_distance(X + wx, Z + wz, C, RX, RZ, angle=25)
    th = np.arctan2(Z - C[1], X - C[0])
    lobes = 1 + 0.18 * strength * np.sin(3 * th + 0.7) + 0.08 * strength * np.sin(5 * th + 2.1)
    return e / lobes + 0.10 * strength * fbm((N, N), 6, 2, seed=13), float(RX)

def polygon(rough=0.0):
    """The lasso measured inward from its rim: 1 on the rim, 0 at the deepest point; the rim `rough` blocks
    ragged."""
    signed = np.where(shapes.inside(X, Z, LASSO), -1, 1) * shapes.edge_distance(X, Z, LASSO)
    inside = signed + rough * 3 * fbm((N, N), 5, 2, seed=21) < 0
    d = shapes.distance_in(inside, "euclid")
    return np.where(inside, 1 - d / d.max(), 9.0), float(d.max())

cols = [("Ellipse", ellipse()), ("Ellipse, verbeult", warped()), ("Polygon (Lasso, 11 Punkte)", polygon()),
        ("Polygon, rauer Rand", polygon(1.0))]
tiles = []
for label, op in (("Hügel", "mound"), ("Krater", "crater")):
    for col, (title, (e, r)) in enumerate(cols):
        H = LF.mound(ground, e, 9.0, power=1.6) if op == "mound" else LF.crater(ground, e * r, 39, r, flat=1.5, slope=9 / (r - 1.5))
        H = np.round(H)
        img = outline(relief(H, everywhere, s=S, step=1, major=5), e < 1, S, tint=0.0)
        im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8).transpose(1, 0, 2)); dr = ImageDraw.Draw(im)
        if col >= 2:
            pts = [((x + .5) * S, (z + .5) * S) for x, z in LASSO]
            dr.line(pts + pts[:1], fill=KIND["poly"], width=2)
            for x, y in pts: dr.ellipse([x - 4, y - 4, x + 4, y + 4], fill=KIND["poly"], outline=(255, 255, 255))
        else:
            cx, cz = (C[0] + .5) * S, (C[1] + .5) * S
            dr.ellipse([cx - 4, cz - 4, cx + 4, cz + 4], fill=KIND["ell"], outline=(255, 255, 255))
        name = f"form-{op}-{col}"; im.save(f"{OUT}/img/{name}.png")
        tiles.append(dict(row=label, col=title, img=name, top=int(H.max()), low=int(H.min())))
json.dump(tiles, open(f"{OUT}/forms.json", "w")); print([(t["row"], t["col"], t["low"], t["top"]) for t in tiles])
