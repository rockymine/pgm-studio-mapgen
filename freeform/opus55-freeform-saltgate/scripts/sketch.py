"""Saltgate's plan, drawn from the raster before anything is built:

1. THE BOARD — every column by what it is and how high: the sea and the ships, the beach, the wall and its towers,
   the yard, the town's terraces, the houses (closed), the magazines, the citadel wall, the courtyard and the keep.
   Gates are drawn in the colour of the stage whose fall opens them; the ladders, the culvert, the objectives and
   every spawn, labelled by team and stage.
2. A SECTION down the middle, at true scale: the flagship, the beach, the gate under the wall, the yard, the three
   terraces, the citadel's gate and the keep with the banner in it.
3. THE STAGES — the checker's walks.

    python3 sketch.py <out.png>
"""
import contextlib
import io
import sys

from PIL import Image, ImageDraw

import plan as P
import plan_check as C

S = 8
W, H = P.NX * S, P.NZ * S
R = C.R
KN = {v: k for k, v in P.KINDS.items()}
BASE = {"sea": (40, 90, 160), "beach": (220, 205, 150), "street": (175, 170, 160), "wall": (95, 90, 85),
        "rampart": (130, 125, 115), "tower": (80, 75, 70), "house": (165, 85, 60), "stair": (150, 140, 120),
        "ladder": (150, 110, 60), "gate": (0, 0, 0), "deck": (140, 100, 60), "pier": (120, 90, 55),
        "court": (190, 185, 170), "magazine": (110, 60, 50), "keep": (70, 65, 75), "floor": (200, 190, 170),
        "cover": (90, 110, 70)}
STAGE = {"warmup": (240, 240, 60), "A": (240, 140, 40), "B": (220, 60, 200)}
TEAM = {"attackers": (210, 50, 50), "defenders": (50, 90, 220)}


def px(x, z, oy=0):
    return ((x - P.X_MIN) * S, oy + (z - P.Z_MIN) * S)


def board(d, oy):
    for i in range(P.NX):
        for j in range(P.NZ):
            x, z = i + P.X_MIN, j + P.Z_MIN
            k, h = KN[R.K[i, j]], R.H[i, j]
            c = STAGE[R.gate[(x, z)]] if k == "gate" else BASE[k]
            if k in ("street", "court", "beach", "rampart"):
                f = 0.8 + (h - 20) / 40.0
                c = tuple(min(255, int(v * f)) for v in c)
            a, b = px(x, z, oy)
            d.rectangle([a, b, a + S - 1, b + S - 1], fill=c)
            if R.U[i, j] >= 0:
                d.rectangle([a + 2, b + 2, a + S - 3, b + S - 3], outline=(80, 80, 80))
    for (x, z), r in R.stair.items():
        a, b = px(x, z, oy)
        dx, dz = {"+x": (1, 0), "-x": (-1, 0), "+z": (0, 1), "-z": (0, -1)}[r]
        cx, cy = a + S / 2, b + S / 2
        d.line([(cx - dx * 3, cy - dz * 3), (cx + dx * 3, cy + dz * 3)], fill=(30, 30, 30), width=2)
    q = [tuple(v + S / 2 for v in px(x, z, oy)) for x, z, _ in P.CULVERT["pts"]]
    for (a, b), (c, e) in zip(q, q[1:]):
        for t in range(0, 10, 2):
            d.line([(a + (c - a) * t / 10, b + (e - b) * t / 10), (a + (c - a) * (t + 1) / 10, b + (e - b) * (t + 1) / 10)],
                   fill=(120, 60, 200), width=3)
    x0, x1, z0, z1 = P.CONTROL["box"]
    a, b = px(x0, z0, oy)
    c, e = px(x1 + 1, z1 + 1, oy)
    d.rectangle([a, b, c, e], outline=(255, 140, 0), width=3)
    d.text((a + 2, b + 2), "A: SEA GATE", fill=(0, 0, 0))
    for m in P.MAGAZINES:
        x, y, z = m["monument"]
        a, b = px(x, z, oy)
        d.rectangle([a - 2, b - 2, a + S + 2, b + S + 2], fill=(20, 20, 30), outline=(255, 255, 255))
        d.text((a - 30, b - 16), "B: " + m["key"], fill=(255, 255, 255))
    wx, wy, wz = P.WOOL["at"]
    a, b = px(wx, wz, oy)
    d.rectangle([a - 2, b - 2, a + S + 2, b + S + 2], fill=(150, 60, 200), outline=(255, 255, 255))
    d.text((a + 12, b - 4), "C: the banner", fill=(255, 255, 255))
    mx, my, mz = P.WOOL["monument"]
    a, b = px(mx, mz, oy)
    d.rectangle([a, b, a + S, b + S], outline=(150, 60, 200), width=2)
    for team, st in P.SPAWNS.items():
        for stage, (x, y, z, yaw) in st.items():
            a, b = px(x, z, oy)
            d.ellipse([a - 7, b - 7, a + 7, b + 7], fill=TEAM[team], outline=(255, 255, 255))
            d.text((a - 3, b - 6), stage, fill=(255, 255, 255))
    for x, z, t in ((-44, -70, "THE SHIPS 24"), (-44, -45, "BEACH 21-22"), (-44, -34, "SEA WALL, walk 28"),
                    (-42, -25, "YARD 22"), (-44, -17, "terrace 22"), (-44, -6, "terrace 26"), (-44, 8, "terrace 30"),
                    (-44, 24, "CITADEL WALL 44"), (-44, 30, "COURTYARD 34"), (-11, 45, "KEEP")):
        a, b = px(x, z, oy)
        d.text((a, b), t, fill=(0, 0, 0))
    d.text((6, oy + 4), "1. THE BOARD — gates in the colour of what opens them: yellow the warm-up, orange the Sea Gate's fall, magenta the Powder Stores';"
           " culvert violet; spawns by team (red attack, blue defend) and stage", fill=(255, 255, 255))


def section(d, top, band, fixed):
    d.rectangle([0, top, W, top + band], fill=(215, 228, 240))
    lo, hi = P.Z_MIN, P.Z_MAX
    s = (W - 20) / (hi - lo + 1)
    py = lambda y: top + band - 10 - (y - 10) * s
    sx = lambda u: 10 + (u - lo) * s
    for z in range(lo, hi + 1):
        i, j = P.ix(fixed), P.iz(z)
        k, h = KN[R.K[i, j]], R.H[i, j]
        if k == "sea":
            d.rectangle([sx(z), py(P.SEA + 1), sx(z + 1) - 1, py(13)], fill=BASE["sea"])
            continue
        c = STAGE[R.gate[(fixed, z)]] if k == "gate" else BASE[k]
        if k in ("magazine", "keep"):
            d.rectangle([sx(z), py(h + 1), sx(z + 1) - 1, py(10)], fill=c)
        else:
            d.rectangle([sx(z), py(h + 1), sx(z + 1) - 1, py(10)], fill=c)
        if R.U[i, j] >= 0:
            d.rectangle([sx(z), py(R.U[i, j] + 1), sx(z + 1) - 1, py(R.U[i, j])], fill=BASE["rampart"])
    for y in range(10, 54, 4):
        d.text((W - 22, py(y) - 6), str(y), fill=(90, 90, 90))
    d.text((10, top + 4), f"2. NORTH TO SOUTH at x = {fixed}, true scale: the flagship, the beach, the gate under the wall walk, the yard, "
           "the terraces, the citadel's gate, the courtyard and the keep", fill=(0, 0, 0))


def main(out):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        lines = C.main()
    band = 46 * 4
    T = 13 * len(lines) + 30
    im = Image.new("RGB", (W, H + band + T + 10), (0, 0, 0))
    d = ImageDraw.Draw(im)
    board(d, 0)
    section(d, H + 4, band, 0)
    y = H + band + 12
    d.text((10, y), "3. THE STAGES — walks on the plan, in blocks, from each team's spawn for that stage", fill=(255, 255, 255))
    y += 18
    for ln in lines:
        d.text((10, y), ln[:130], fill=(230, 230, 230))
        y += 13
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1])
