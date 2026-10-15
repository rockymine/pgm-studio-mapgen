"""Every shape the caldera recipe names, drawn by the kind of geometry it is written as (the Riftwater page's key:
pink circle or ellipse, orange rectangle, purple noise-defined line, grey band), twice: as the code writes it, and as
the bent ruler measures it. Writes overlay-written.png, overlay-measured.png and overlay.json."""
import base64
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
sys.path.insert(0, os.path.join(HERE, *[".."] * 6, "analysis", "freeform-vs-studio", "pages", "riftwater-layers", "make"))
import round2 as R                                                          # noqa: E402
from volcanoes import noise, grid                                            # noqa: E402
from pgmvox.geom.shapes import ellipse_distance                             # noqa: E402
from style import KIND, hypso, shade                                        # noqa: E402

S = 3
_, X, Z = grid()
N = X.shape[0]
X0, Z0 = int(X[0, 0]), int(Z[0, 0])
H = R.caldera_lake(X, Z)
Xw, Zw = R.warp(X, Z, 210, big=12, small=4)
try:
    FONT = ImageFont.truetype("DejaVuSans-Bold.ttf", 13)
except OSError:
    FONT = ImageFont.load_default()


def base():
    """The finished ground, greyed and lightened so the shapes read over it."""
    rgb = hypso(np.clip(H + 26, 36, 82)) * shade(H)
    grey = rgb.mean(-1, keepdims=True).repeat(3, -1)
    img = grey * 0.5 + 255 * 0.5
    big = np.repeat(np.repeat(img, S, 0), S, 1)
    return Image.fromarray(np.clip(big, 0, 255).astype(np.uint8).transpose(1, 0, 2))


px = lambda x, z: ((x - X0 + 0.5) * S, (z - Z0 + 0.5) * S)                   # noqa: E731


def ellipse_pts(c, r, stretch, angle, n=240):
    """The rim of r_at's ellipse: r across, r * stretch along, turned `angle` degrees."""
    a = np.radians(angle)
    t = np.linspace(0, 2 * np.pi, n)
    u, v = r * np.cos(t), r * stretch * np.sin(t)
    return [(c[0] + ui * np.cos(a) - vi * np.sin(a), c[1] + ui * np.sin(a) + vi * np.cos(a)) for ui, vi in zip(u, v)]


def contour(d, field, level, colour, width=2):
    """Paint the cells where `field` crosses `level`: the shape as actually measured."""
    inside = field < level
    edge = np.zeros_like(inside)
    edge[:-1] |= inside[:-1] != inside[1:]
    edge[:, :-1] |= inside[:, :-1] != inside[:, 1:]
    for i, k in zip(*np.nonzero(edge)):
        x, y = i * S, k * S
        d.rectangle([x, y, x + S + width - 2, y + S + width - 2], fill=colour)


def dashed(d, pts, colour, width=2, on=6, off=5):
    pts = [px(x, z) for x, z in pts]
    run, draw = 0.0, True
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        seg = np.hypot(x2 - x1, y2 - y1)
        if draw:
            d.line([(x1, y1), (x2, y2)], fill=colour, width=width)
        run += seg
        if run > (on if draw else off):
            run, draw = 0.0, not draw


def dot(d, c, colour):
    x, y = px(*c)
    d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=colour, outline=(255, 255, 255))


def mark(d, n, x, z, kind):
    cx, cy = px(x, z)
    d.rounded_rectangle([cx - 11, cy - 10, cx + 11, cy + 10], 4, fill=(255, 255, 255), outline=KIND[kind], width=2)
    d.text((cx, cy), str(n), fill=(20, 20, 20), anchor="mm", font=FONT)


def lumps_placed():
    """Replay lumps()'s draws to learn which slump blocks it placed and where."""
    dc = R.r_at(Xw, Zw, (0, 0), 0.82, 30) * (1 + 0.1 * noise.fbm(X.shape, 40, 3, seed=9))
    mask = (dc < 48) & (dc > 30)
    rng = np.random.default_rng(13)
    out = []
    for _ in range(26):
        x, z = rng.uniform(-50, 50), rng.uniform(-45, 45)
        if not mask[150 + int(x), 150 + int(z)]:
            continue
        rx = rng.uniform(3, 8)
        rz = rx * rng.uniform(0.5, 1.0)
        ang = rng.uniform(0, 180)
        rng.uniform(3, 8)
        out.append((x, z, rx, rz, ang))
    return out, dc


def draw(measured):
    im = base()
    d = ImageDraw.Draw(im)
    fx, fz = (Xw, Zw) if measured else (X, Z)
    c, isle = (0, 0), (-18, 14)
    theta = np.arctan2(fz, fx)
    d0 = R.r_at(fx, fz, c, 0.9, 30)
    # grey bands: where the gullies run (70 to 135 out) and the notch's wedge
    for r in (70, 135):
        if measured:
            contour(d, d0, r, KIND["band"], 1)
        else:
            dashed(d, ellipse_pts(c, r, 0.9, 30), KIND["band"])
    wedge = np.abs(np.angle(np.exp(1j * (theta - 2.3)))) < 0.25
    band = (d0 > 30) & (d0 < 80)
    contour(d, np.where(wedge & band, 0, 1), 0.5, KIND["band"], 2)
    # purple: the gully grooves, a line wherever the noisy phase crosses a whole number
    phi = theta * 30 / (2 * np.pi) + (0.9 * noise.fbm(X.shape, 50, 3, seed=8) if measured else 0)
    whole = np.floor(phi)
    cross = np.zeros(phi.shape, bool)                                      # where the phase crosses a whole number
    cross[:-1] |= whole[:-1] != whole[1:]
    cross[:, :-1] |= whole[:, :-1] != whole[:, 1:]
    for i, k in zip(*np.nonzero(cross & (d0 > 70) & (d0 < 135))):
        d.rectangle([i * S, k * S, i * S + S, k * S + S], fill=KIND["noise"])
    # pink: the cone's foot, the caldera's two cliffs, the island and its crater
    dc = R.r_at(fx, fz, c, 0.82, 30) * ((1 + 0.1 * noise.fbm(X.shape, 40, 3, seed=9)) if measured else 1)
    ir = R.r_at(fx, fz, isle, 0.75, 70)
    shapes = [(d0, c, 145, 0.9, 30, 3), (dc, c, 42, 0.82, 30, 3), (dc, c, 58, 0.82, 30, 3),
              (ir, isle, 17, 0.75, 70, 3), (ir, isle, 4, 0.75, 70, 2)]
    for field, centre, r, stretch, ang, w in shapes:
        if measured:
            contour(d, field, r, KIND["ell"], w)
        else:
            d.line([px(*p) for p in ellipse_pts(centre, r, stretch, ang)], fill=KIND["ell"], width=w)
    for r in (30, 48):                                                     # where slump blocks may land
        if measured:
            contour(d, dc, r, (232, 140, 180), 1)
        else:
            dashed(d, ellipse_pts(c, r, 0.82, 30), (232, 140, 180), 1)
    dot(d, c, KIND["ell"])
    dot(d, isle, KIND["ell"])
    # orange: the box slump blocks are drawn in
    a, b = px(-50, -45), px(50, 45)
    d.rectangle([a, b], outline=KIND["poly"], width=2)
    placed, _ = lumps_placed()
    for x, z, rx, rz, ang in placed:                                       # each placed block: a small ellipse
        d.line([px(*p) for p in ellipse_pts((x, z), rx, rz / rx, ang, 60)], fill=KIND["ell"], width=2)
    for n, (x, z, kind) in enumerate([(0, -145 * 0.9 - 4, "ell"), (36, 21, "ell"), (-50, -29, "ell"),
                                      (-18, 14 - 20, "ell"), (-8, 26, "ell"), (50, 45, "poly"),
                                      (-75, 70, "band"), (110, -40, "noise")], 1):
        mark(d, n, x, z, kind)
    return im, len(placed)


def main():
    out = {}
    for measured, name in ((False, "written"), (True, "measured")):
        im, placed = draw(measured)
        path = os.path.join(HERE, f"overlay-{name}.png")
        im.save(path, optimize=True)
        out[name] = "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()
    out["placed"] = placed
    json.dump(out, open(os.path.join(HERE, "overlay.json"), "w"))
    print("placed slump blocks", placed, "bytes", os.path.getsize(os.path.join(HERE, "overlay.json")))


if __name__ == "__main__":
    main()
