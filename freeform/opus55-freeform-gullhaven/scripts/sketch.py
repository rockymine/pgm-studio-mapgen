"""Gullhaven's plan, drawn from the raster before anything is built, in three panels:

1. THE ISLAND — every column by what it is and how high, hill-shaded: the sea, the beach, the grass, the town's
   terraces, the quay, the ravine and its stream, the ramps and stairs, the bridge, the houses and landmarks
   (closed), the cover, the trees; the caves under it dashed; the spawn points.
2. THE READS — what the checker says: each spawn's nearest neighbour on foot and how many other spawns it sees;
   the open ground, shaded by how far it is from anything to stand behind.
3. TWO SECTIONS at true scale — west to east across the Headland, the Ravine and the Town, and north to south
   across the Town, the Harbour and the basin.

    python3 sketch.py <out.png>
"""
import contextlib
import io
import math
import sys

import numpy as np
from PIL import Image, ImageDraw

import plan as P
import plan_check as C

S = 7
W, H = P.NX * S, P.NZ * S
R = C.R
KN = {v: k for k, v in P.KINDS.items()}
BASE = {"sea": (40, 90, 160), "grass": (110, 160, 80), "beach": (220, 205, 150), "rock": (130, 130, 130),
        "street": (175, 165, 150), "quay": (150, 140, 125), "ramp": (200, 180, 120), "ravine": (125, 115, 95),
        "stream": (70, 130, 200), "house": (170, 80, 60), "cover": (90, 90, 90), "tree": (30, 90, 30),
        "pier": (140, 105, 60), "landmark": (230, 230, 230)}


def px(x, z, oy=0):
    return ((x - P.X_MIN) * S, oy + (z - P.Z_MIN) * S)


def shade():
    Hf = R.H.astype(float)
    gx = np.gradient(Hf, axis=0)
    gz = np.gradient(Hf, axis=1)
    return np.clip(1.0 - 0.10 * (gx + gz), 0.55, 1.25)


def island(d, oy, dim=1.0):
    sh = shade()
    for i in range(P.NX):
        for j in range(P.NZ):
            k = KN[R.K[i, j]]
            h = R.H[i, j]
            c = BASE[k]
            if k in ("grass", "street", "quay", "ramp", "ravine", "beach"):
                t = (h - 24) / 16.0
                c = tuple(int(v * (0.8 + 0.35 * t)) for v in c)
            c = tuple(max(0, min(255, int(v * sh[i, j] * dim))) for v in c)
            a, b = px(i + P.X_MIN, j + P.Z_MIN, oy)
            d.rectangle([a, b, a + S - 1, b + S - 1], fill=c)
            if R.U[i, j] >= 0:
                d.rectangle([a + 1, b + 2, a + S - 2, b + S - 3], fill=(150, 100, 50))


def overlay(d, oy):
    for t in P.TUNNELS:
        q = [tuple(v + S / 2 for v in px(x, z, oy)) for x, z, _ in t["pts"]]
        for k in range(len(q) - 1):
            (a, b), (c, e) = q[k], q[k + 1]
            n = max(2, int(max(abs(c - a), abs(e - b)) // 8))
            for s_ in range(0, n, 2):
                d.line([(a + (c - a) * s_ / n, b + (e - b) * s_ / n), (a + (c - a) * (s_ + 1) / n, b + (e - b) * (s_ + 1) / n)],
                       fill=(200, 80, 220), width=3)
    x0, x1, z0, z1 = P.GROTTO["box"]
    a, b = px(x0, z0, oy)
    c, e = px(x1 + 1, z1 + 1, oy)
    d.rectangle([a, b, c, e], outline=(200, 80, 220), width=2)
    x0, x1, z0, z1 = P.CHAPEL["box"]
    a, b = px(x0, z0, oy)
    c, e = px(x1 + 1, z1 + 1, oy)
    d.rectangle([a, b, c, e], outline=(240, 240, 240), width=2)
    for x, z, yaw in P.SPAWNS:
        a, b = px(x, z, oy)
        a += S / 2; b += S / 2
        d.ellipse([a - 5, b - 5, a + 5, b + 5], fill=(255, 220, 40), outline=(0, 0, 0))
        r = math.radians(yaw)
        d.line([(a, b), (a - 9 * math.sin(r), b + 9 * math.cos(r))], fill=(0, 0, 0), width=2)
    for x, z, yaw, y in P.CAVE_SPAWNS:
        a, b = px(x, z, oy)
        a += S / 2; b += S / 2
        d.ellipse([a - 5, b - 5, a + 5, b + 5], fill=(240, 140, 255), outline=(0, 0, 0))
    labels = [(-46, -46, "THE HEADLAND 40"), (-12, -50, "RAVINE 24"), (6, -49, "upper terrace 36"),
              (4, -29, "middle terrace 32"), (6, -11, "lower terrace 28"), (20, 9, "THE QUAY 22"),
              (-30, 30, "THE DOWNS 26-30"), (-56, 8, "COVE"), (21, 40, "basin"), (-36, -24, "grotto"),
              (-28, -40, "chapel"), (-50, -42, "lighthouse"), (-34, 22, "mill"), (-12, 25, "stones")]
    for x, z, t in labels:
        a, b = px(x, z, oy)
        d.text((a, b), t, fill=(0, 0, 0))


def reads(d, oy, lines, openness):
    island(d, oy, dim=0.45)
    mx = 10.0
    for i in range(P.NX):
        for j in range(P.NZ):
            v = openness[i, j]
            if v < 0:
                continue
            t = min(v, mx) / mx
            a, b = px(i + P.X_MIN, j + P.Z_MIN, oy)
            d.rectangle([a + 1, b + 1, a + S - 2, b + S - 2], fill=(int(60 + 195 * t), int(200 - 150 * t), 60))
    overlay(d, oy)
    d.text((6, oy + 4), "2. THE READS — walkable ground by distance to the nearest thing to stand behind (green near, red ten or more); spawns",
           fill=(255, 255, 255))


def section(d, top, band, axis, fixed, title):
    d.rectangle([0, top, W, top + band], fill=(215, 228, 240))
    lo, hi = (P.X_MIN, P.X_MAX) if axis == "x" else (P.Z_MIN, P.Z_MAX)
    s = (W - 20) / (hi - lo + 1)
    y0 = 10
    py = lambda y: top + band - 10 - (y - y0) * s
    sx = lambda u: 10 + (u - lo) * s
    for u in range(lo, hi + 1):
        i, j = (P.ix(u), P.iz(fixed)) if axis == "x" else (P.ix(fixed), P.iz(u))
        k, h = KN[R.K[i, j]], R.H[i, j]
        if k == "sea":
            d.rectangle([sx(u), py(P.SEA + 1), sx(u + 1) - 1, py(13)], fill=BASE["sea"])
            continue
        c = BASE[k]
        d.rectangle([sx(u), py(h + 1), sx(u + 1) - 1, py(y0)], fill=c)
        if R.U[i, j] >= 0:
            d.rectangle([sx(u), py(R.U[i, j] + 1), sx(u + 1) - 1, py(R.U[i, j])], fill=(150, 100, 50))
    for t in P.TUNNELS:
        for (x, z, y), (x2, z2, y2) in zip(t["pts"], t["pts"][1:]):
            for f in np.linspace(0, 1, 30):
                xx, zz, yy = x + (x2 - x) * f, z + (z2 - z) * f, y + (y2 - y) * f
                if (axis == "x" and abs(zz - fixed) < 1.6) or (axis == "z" and abs(xx - fixed) < 1.6):
                    u = xx if axis == "x" else zz
                    d.rectangle([sx(u), py(yy + 4), sx(u + 1), py(yy + 1)], fill=(240, 220, 250))
    for yy in range(y0, 52, 4):
        d.text((W - 24, py(yy) - 6), str(yy), fill=(90, 90, 90))
    d.text((10, top + 4), title, fill=(0, 0, 0))


def main(out):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        lines, openness = C.main()
    band = 46 * 6
    T = 13 * len(lines) + 12
    im = Image.new("RGB", (W, 2 * H + T + 2 * band + 12), (0, 0, 0))
    d = ImageDraw.Draw(im)
    island(d, 0)
    overlay(d, 0)
    d.text((6, 4), "1. THE ISLAND — by kind and height, hill-shaded; houses and landmarks closed (brick red, white); caves dashed (violet); spawns (yellow, ticked the way they face)",
           fill=(255, 255, 255))
    reads(d, H + 4, lines, openness)
    y = 2 * H + 10
    for ln in lines:
        d.text((10, y), ln[:150], fill=(230, 230, 230))
        y += 13
    section(d, 2 * H + T + 8, band, "x", -32, "3a. WEST TO EAST at z = -32: the Headland's cliff, the chapel and the crypt, the Ravine under the bridge, the upper terrace")
    section(d, 2 * H + T + 10 + band, band, "z", 22, "3b. NORTH TO SOUTH at x = 22: the three terraces, the stairs, the quay, the basin")
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1])
