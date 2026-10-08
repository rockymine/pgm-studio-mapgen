"""Copperline's plan, drawn from the raster before anything is built:

1. THE BOARD - every column by what it is, shaded by height; the two bridges over the gorge; the track rail by
   rail in its leg's colour, sloped rails marked, the bumpers between legs, each cart where it starts and each
   leg's end; the connectors (ladder, gantry, adit) dashed; every spawn, labelled by team and stage.
2. THE TRACK UNROLLED - the rails' heights one after another, A, B and C, at true scale, with the ground either
   side of the line under it: where the cart climbs and what stands over it.
3. THE LEGS - the checker's trace and walks.

    python3 sketch.py <out.png>
"""
import contextlib
import io
import sys

from PIL import Image, ImageDraw

import plan as P
import plan_check as C

S = 7
W, H = P.NX * S, P.NZ * S
R = C.R
KN = P.KN
BASE = {"rock": (95, 90, 85), "yard": (150, 140, 120), "street": (180, 175, 160), "ground": (120, 160, 90),
        "house": (165, 85, 60), "track": (110, 100, 90), "bed": (140, 130, 115), "stair": (150, 140, 120),
        "river": (50, 100, 170), "floor": (205, 195, 175), "wall": (70, 65, 60), "gate": (0, 0, 0),
        "heap": (70, 60, 60), "platform": (200, 180, 140), "cover": (90, 110, 70), "bumper": (230, 230, 230)}
LEG = {"A": (240, 150, 30), "B": (230, 60, 200), "C": (40, 200, 220)}
STAGE = {"warmup": (240, 240, 60), "A": LEG["A"], "B": LEG["B"]}
TEAM = {"attackers": (210, 50, 50), "defenders": (50, 90, 220)}


def px(x, z, oy=0):
    return ((x - P.X_MIN) * S, oy + (z - P.Z_MIN) * S)


def shade(c, h):
    f = 0.75 + (h - 24) / 50.0
    return tuple(max(0, min(255, int(v * f))) for v in c)


def dashed(d, a, b, col, width=3):
    for t in range(0, 20, 2):
        d.line([(a[0] + (b[0] - a[0]) * t / 20, a[1] + (b[1] - a[1]) * t / 20),
                (a[0] + (b[0] - a[0]) * (t + 1) / 20, a[1] + (b[1] - a[1]) * (t + 1) / 20)], fill=col, width=width)


def board(d):
    for i in range(P.NX):
        for j in range(P.NZ):
            x, z = i + P.X_MIN, j + P.Z_MIN
            k, h = KN[R.K[i, j]], R.H[i, j]
            c = STAGE[R.gate[(x, z)]] if k == "gate" else BASE[k]
            if k not in ("rock", "house", "wall", "cover"):
                c = shade(c, h)
            a, b = px(x, z)
            d.rectangle([a, b, a + S - 1, b + S - 1], fill=c)
            if R.U[i, j] >= 0:
                d.rectangle([a, b, a + S - 1, b + S - 1], fill=(150, 110, 70))
                d.line([(a, b + S // 2), (a + S - 1, b + S // 2)], fill=(110, 80, 50))
    for leg in P.LEGS:
        cells = P.lay(leg)
        for x, z, h, dd in cells:
            a, b = px(x, z)
            d.rectangle([a + 1, b + 1, a + S - 2, b + S - 2], fill=LEG[leg["key"]])
            if 2 <= dd <= 5:
                d.rectangle([a + 2, b + 2, a + S - 3, b + S - 3], fill=(255, 255, 255))
        x, z = cells[0][:2]
        a, b = px(x, z)
        d.rectangle([a - 3, b - 3, a + S + 2, b + S + 2], outline=(255, 255, 255), width=2)
        d.text((a + 10, b - 4), f"cart {leg['key']}", fill=(255, 255, 255))
        x, z = cells[-1][:2]
        a, b = px(x, z)
        d.ellipse([a - 5, b - 5, a + S + 4, b + S + 4], outline=LEG[leg["key"]], width=3)
        d.text((a + 10, b + 2), f"{leg['key']} ends", fill=(255, 255, 255))
    for name, way, a0, b0, L in P.CONNECTORS:
        a = tuple(v + S / 2 for v in px(*a0))
        b = tuple(v + S / 2 for v in px(*b0))
        dashed(d, a, b, (255, 230, 60) if way == "above" else (160, 90, 230))
        d.text((a[0] + 6, a[1] + 2), name.replace("the ", ""), fill=(255, 255, 255))
    for team, st in P.SPAWNS.items():
        for stage, (x, y, z, yaw) in st.items():
            a, b = px(x, z)
            d.ellipse([a - 7, b - 7, a + 7, b + 7], fill=TEAM[team], outline=(255, 255, 255))
            d.text((a - 3, b - 6), stage, fill=(255, 255, 255))
    for x, z, t in ((-22, 69, "THE RAIL YARD 24"), (-34, 30, "STATION ROAD"), (-6, 49, "alley"), (5, 50, "MAIN ST"),
                    (28, 46, "SLAG HEAP to 34"), (-34, 12, "station"), (-46, 1, "THE BROW 26"),
                    (-50, -13, "THE GORGE, river 12"), (-46, -33, "THE NORTH BANK 28"), (-40, -52, "THE MINE YARD 36"),
                    (-30, -69, "MINE HALL"), (-2, -69, "lamps"), (36, -46, "ramp"), (22, -30, "depot"),
                    (37, -30, "bunks"), (29, 2, "office"), (19, 65, "shed")):
        a, b = px(x, z)
        d.text((a, b), t, fill=(255, 255, 255))
    d.text((6, 4), "1. THE BOARD - the track by leg (A orange, B magenta, C cyan; white cells sloped), bridges brown,"
           " connectors dashed (yellow above, violet below),", fill=(255, 255, 255))
    d.text((6, 16), "   gates in the colour of the leg whose end opens them (yellow the warm-up); spawns by team"
           " (red attack, blue defend) and stage", fill=(255, 255, 255))


def unrolled(d, top, band):
    d.rectangle([0, top, W, top + band], fill=(215, 228, 240))
    cells = [(leg["key"], c) for leg in P.LEGS for c in P.lay(leg)]
    s = (W - 40) / len(cells)
    py = lambda y: top + band - 14 - (y - 8) * 3.2
    for n, (key, (x, z, h, dd)) in enumerate(cells):
        u = 20 + n * s
        for side in (-2, 2):                                    # the ground either side of the line
            dx, dz = (0, 0)
            nb = cells[min(n + 1, len(cells) - 1)][1]
            pv = cells[max(n - 1, 0)][1]
            tx, tz = nb[0] - pv[0], nb[1] - pv[1]
            ox, oz = (-tz, tx) if side > 0 else (tz, -tx)
            ox, oz = (ox // max(1, abs(ox) + abs(oz)) * 3, oz // max(1, abs(ox) + abs(oz)) * 3)
            i, j = P.ix(x + ox), P.iz(z + oz)
            if C.inside(i, j):
                g = R.H[i, j] if R.U[i, j] < 0 else R.U[i, j]
                col = (150, 150, 150) if side < 0 else (120, 120, 120)
                d.line([(u, py(g)), (u + s, py(g))], fill=col, width=1)
        if R.U[P.ix(x), P.iz(z)] >= 0:
            d.rectangle([u, py(h), u + s, py(12)], fill=(150, 110, 70))
            d.rectangle([u, py(13.5), u + s, py(12)], fill=(50, 100, 170))
        else:
            d.rectangle([u, py(h), u + s, py(8)], fill=(140, 130, 115))
        d.rectangle([u, py(h + 1), u + s, py(h)], fill=LEG[key])
    for y in range(12, 40, 4):
        d.text((4, py(y) - 6), str(y), fill=(90, 90, 90))
    n0 = 0
    for leg in P.LEGS:
        n = len(P.lay(leg))
        d.text((20 + (n0 + n / 2) * s - 40, top + 20), f"{leg['key']}: {leg['name']}, {n} rails", fill=(0, 0, 0))
        n0 += n
    d.text((10, top + 4), "2. THE TRACK UNROLLED - rail after rail, A then B then C, heights at 3.2 px a block; "
           "grey lines the ground three blocks either side; the trestle over the river", fill=(0, 0, 0))


def main(out):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        lines = C.main()
    band = 120
    T = 13 * len(lines) + 30
    im = Image.new("RGB", (W, H + band + T + 10), (0, 0, 0))
    d = ImageDraw.Draw(im)
    board(d)
    unrolled(d, H + 4, band)
    y = H + band + 12
    d.text((10, y), "3. THE LEGS - the rails traced as PGM traces them; walks on the plan, in blocks, from each team's spawn for that leg",
           fill=(255, 255, 255))
    y += 18
    for ln in lines:
        d.text((10, y), ln[:150], fill=(230, 230, 230))
        y += 13
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1])
