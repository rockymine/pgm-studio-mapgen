"""Lantern Pass's plan, drawn from the raster before anything is built, the lane laid on its side (the boathouse at
the left, the bell at the right):

1. THE BOARD — every column by what it is, shaded by height; awnings and roofs hatched over what they cover; the
   walkways either side with their side-swap rows; the fastest route (white) and the safest (yellow).
2. SIGHT — every cell a runner can stand on, coloured by the share of the walkways that see it: dark where
   hidden, red where seen from everywhere.
3. THE LONG SECTION — the lane's floor along its middle and the walkways' height over it, true scale.
4. THE CHECK — the checker's numbers, section by section.

    python3 sketch.py <out.png>
"""
import contextlib
import io
import sys

from PIL import Image, ImageDraw

import plan as P
import plan_check as C

S = 3
W, H = P.NZ * S + 20, P.NX * S
R = C.R
BASE = {"void": (18, 18, 24), "plank": (165, 125, 75), "street": (175, 170, 160), "grass": (105, 155, 75),
        "paddy": (90, 150, 170), "bund": (130, 165, 85), "stair": (200, 190, 170), "bamboo": (60, 120, 50),
        "cover": (120, 90, 60), "house": (170, 60, 50), "water": (45, 95, 165), "bridge": (190, 150, 90),
        "pillar": (150, 150, 150), "stone": (185, 180, 170), "walk": (110, 105, 120), "swap": (230, 180, 60),
        "wall": (60, 55, 65), "gate": (240, 240, 60), "floor": (200, 170, 120)}


def px(x, z, oy):
    return (10 + (z - P.Z_MIN) * S, oy + (P.X_MAX - x) * S)


def shade(c, h):
    f = 0.7 + (h - 18) / 70.0
    return tuple(max(0, min(255, int(v * f))) for v in c)


def board(d, oy, routes):
    for i in range(P.NX):
        for j in range(P.NZ):
            x, z = i + P.X_MIN, j + P.Z_MIN
            k = P.KN[R.K[i, j]]
            c = BASE[k] if k == "void" else shade(BASE[k], R.H[i, j])
            a, b = px(x, z, oy)
            d.rectangle([a, b, a + S - 1, b + S - 1], fill=c)
            if R.C[i, j] >= 0:
                d.line([(a, b + S - 1), (a + S - 1, b)], fill=(240, 240, 240))
    for name, col in (("fastest", (255, 255, 255)), ("safest", (255, 220, 40))):
        pts = [px(i + P.X_MIN, j + P.Z_MIN, oy) for i, j in routes[name]]
        pts = [(a + S / 2, b + S / 2) for a, b in pts]
        d.line(pts, fill=col, width=1)
    for key, name, z0, z1 in P.SECTIONS:
        a, b = px(P.LANE[1], z0, oy)
        d.line([(a, oy), (a, oy + H)], fill=(90, 90, 90))
        d.text((a + 3, oy + 2), f"{key} {name}", fill=(255, 255, 255))
    bx0, bx1, bz0, bz1 = P.BELL["box"]
    a, b = px(bx1, bz0, oy)
    c, e = px(bx0, bz1, oy)
    d.rectangle([a, b, c + S, e + S], outline=(255, 60, 60), width=2)
    hx0, hx1, hz0, hz1 = P.HEAL["box"]
    a, b = px(hx1, hz0, oy)
    c, e = px(hx0, hz1, oy)
    d.rectangle([a, b, c + S, e + S], outline=(80, 255, 120), width=2)


def sight(d, oy):
    d.rectangle([0, oy, W, oy + H], fill=(18, 18, 24))
    for i in range(P.NX):
        for j in range(P.NZ):
            a, b = px(i + P.X_MIN, j + P.Z_MIN, oy)
            k = P.KN[R.K[i, j]]
            if C.walkable(i, j):
                v = C.VIS[i, j]
                c = (int(40 + 215 * v), int(40 + 40 * (1 - v)), int(60 * (1 - v)))
            elif k in ("walk", "swap"):
                c = (110, 105, 120)
            elif k == "void":
                continue
            else:
                c = (70, 70, 70)
            d.rectangle([a, b, a + S - 1, b + S - 1], fill=c)


def long_section(d, top, band):
    d.rectangle([0, top, W, top + band], fill=(215, 228, 240))
    py = lambda y: top + band - 8 - (y - 10) * S
    hw = C.HW
    for j in range(P.NZ):
        z = j + P.Z_MIN
        a = 10 + j * S
        i = P.ix(0)
        hh = max((R.H[P.ix(x), j] for x in range(P.LANE[0], P.LANE[1] + 1) if R.K[P.ix(x), j] != 0), default=None)
        if hh is not None:
            d.rectangle([a, py(hh + 1), a + S - 1, py(10)], fill=(150, 140, 120))
        d.rectangle([a, py(hw[j] + 1), a + S - 1, py(hw[j])], fill=(110, 105, 120))
    for y in range(20, 64, 10):
        d.text((2, py(y) - 6), str(y), fill=(80, 80, 80))
    d.text((40, top + 4), "3. THE LONG SECTION, true scale: the lane's highest floor (brown) and the walkways (grey) over it",
           fill=(0, 0, 0))


def main(out):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        lines, routes = C.main()
    band = 60 * S
    T = 14 * len(lines) + 30
    im = Image.new("RGB", (W, 2 * H + band + T + 70), (0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((10, 4), "1. THE BOARD - the lane between the two walkways (side-swap rows yellow); awnings and roofs hatched; "
           "the fastest route white, the safest yellow; the bell red, the shrine green", fill=(255, 255, 255))
    board(d, 20, routes)
    d.text((10, H + 26), "2. SIGHT - each cell a runner can stand on by the share of the walkways within forty blocks that "
           "see it: dark hidden, red seen from everywhere", fill=(255, 255, 255))
    sight(d, H + 42)
    long_section(d, 2 * H + 46, band)
    y = 2 * H + band + 54
    d.text((10, y), "4. THE CHECK - blocks walked and blocks in sight (weighted by how much of the walkways see them), "
           "seconds at a Speed I sprint", fill=(255, 255, 255))
    y += 18
    for ln in lines:
        d.text((10, y), ln, fill=(230, 230, 230))
        y += 14
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1])
