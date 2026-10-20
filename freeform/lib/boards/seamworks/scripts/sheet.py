"""Seamworks' asset sheet: every asset the map is built from, lined up on a flat crust, through the same functions
the map uses, so each look can be judged on its own before it is applied. The first row holds the panel palettes on
one cut, the second the building palettes on one building, the third the rest in the board's look.

    python3 sheet.py <build-dir> [<renders-dir>]
"""
import math
import os
import random
import sys

import numpy as np

import plan as P  # noqa: I001  (plan puts the library on the path)
import assets as A
import look as L
from pgmvox import B, World
from pgmvox.built import props
from pgmvox.read import render

YS = 30
w = World(-2, -2, 520, 230, sy=YS + 46)
floors = {}                                   # (x, z) -> walking level of cut floor


def ground(x, z):
    return YS


def is_floor(x, z):
    return (x, z) in floors


def feet(x, z):
    return floors[(x, z)]


def keep_none(x, z):
    return False


# a flat crust over rock
for x in range(w.x0, w.x0 + w.sx):
    for z in range(w.z0, w.z0 + w.sz):
        w.column(x, z, 0, 0, B.BEDROCK)
        w.column(x, z, 1, YS - 2, B.STONE)
        A.lay_crust(w, x, z, ground, L.LOOK)
L.paint_rock(w)


def cut(poly, depth, look, tags=None):
    """A cut to `depth` under the crust: its floor, and panels on every edge tagged P (all edges when no tags)."""
    cells = A.poly_cells(poly)
    for x, z in cells:
        floors[(x, z)] = YS + depth
        w.column(x, z, YS + depth - 1, YS + 30, B.AIR)
        w.set(x, YS + depth - 1, z, *look.cut_floor(x, z))
    tags = tags or "P" * len(poly)
    quads = []
    rng = random.Random(len(poly) * 7 + depth)
    for i, tag in enumerate(tags):
        if tag != "P":
            continue
        a, b = poly[i], poly[(i + 1) % len(poly)]
        n = P.outward(a, b, poly)
        length = math.hypot(b[0] - a[0], b[1] - a[1])
        ux, uz = (b[0] - a[0]) / length, (b[1] - a[1]) / length
        lean = rng.uniform(10, 14)
        for j, (s0, s1) in enumerate(P.panel_runs(a, b, rng)):
            l0 = lean + rng.uniform(-1.5, 1.5)
            quads.append(((a[0] + ux * s0, a[1] + uz * s0), (a[0] + ux * s1, a[1] + uz * s1), n,
                          (l0, l0 + rng.uniform(-1.5, 1.5)), j % 2))
    A.panels(w, quads, lambda a, b, n: YS + depth, lambda a, b, n, base: YS + P.LIP - base, is_floor, keep_none,
             ground, look)
    return cells


SHOTS = []


def shot(name, box, yaw=210, pitch=28):
    SHOTS.append(dict(out=name, box=box, yaw=yaw, pitch=pitch, fov=55, w=1100, h=760))


# ---- row one: the panel palettes on one cut with an inside corner, an outside corner, a rock face and a ladder -------
for k, name in enumerate(L.PANELS):
    look = L.Look(panels=name)
    x0, z0 = 4 + k * 62, 4
    poly = [(x0, z0), (x0 + 30, z0), (x0 + 30, z0 + 12), (x0 + 18, z0 + 12), (x0 + 18, z0 + 24), (x0, z0 + 24)]
    cut(poly, -10, look, "PPPPRP")
    A.ladder_bay(w, x0 + 8, z0, "n", YS - 10, ground, look)
    # a corner of brick works beside them, to judge the steel against the buildings it stands with
    hut = [(x0 + 2, z0 + 15), (x0 + 10, z0 + 15), (x0 + 10, z0 + 22), (x0 + 2, z0 + 22)]
    A.building(w, hut, YS - 10, [(A.poly_cells(hut), P.storeys_below(-10) + 1, ((x0 + 3, z0 + 16), "w"))],
               L.Look(building="brick works"))
    w.sign(x0 + 33, YS, z0 + 2, ["panels", name])
    shot(f"panels-{name.replace(' ', '-')}.png", (x0 - 2, YS - 11, z0 - 3, x0 + 32, YS + 3, z0 + 26))

# ---- row two: the building palettes on one works building, two sections, in a cut eight deep -------------------------
for k, name in enumerate(L.BUILDINGS):
    look = L.Look(building=name)
    x0, z0 = 4 + k * 82, 50
    pit = [(x0, z0), (x0 + 44, z0), (x0 + 44, z0 + 40), (x0, z0 + 40)]
    cut(pit, -8, look, "RRRR")
    hall = [(x0 + 4, z0 + 4), (x0 + 30, z0 + 4), (x0 + 30, z0 + 14), (x0 + 38, z0 + 14), (x0 + 38, z0 + 28),
            (x0 + 4, z0 + 28)]
    tall = {(x, z) for x in range(x0 + 4, x0 + 30) for z in range(z0 + 4, z0 + 16)}
    low = {(x, z) for x in range(x0 + 4, x0 + 38) for z in range(z0 + 16, z0 + 28)} | \
          {(x, z) for x in range(x0 + 30, x0 + 38) for z in range(z0 + 14, z0 + 16)}
    below = P.storeys_below(-8)
    A.building(w, hall, YS - 8, [(tall, below + 3, ((x0 + 5, z0 + 5), "w")),
                                 (low, below + 2, ((x0 + 36, z0 + 26), "e"))], look, skylights=True)
    A.door(w, [(x, z0 + 27) for x in range(x0 + 14, x0 + 17)], YS - 8, look)
    A.door(w, [(x0 + 37, z) for z in range(z0 + 20, z0 + 23)], YS - 8, look)
    A.chimney(w, (x0 + 8, z0 + 7, x0 + 10, z0 + 9), 9, look)
    A.chimney(w, (x0 + 33, z0 + 18, x0 + 34, z0 + 19), 5, look, plume=7)
    w.sign(x0 + 46, YS, z0 + 2, ["works", name])
    shot(f"works-{name.replace(' ', '-')}.png", (x0 - 1, YS - 9, z0 - 1, x0 + 45, YS + 22, z0 + 41), yaw=200, pitch=22)

# ---- the crusts, side by side on the flat ----------------------------------------------------------------------------
for k, name in enumerate(L.CRUSTS):
    look = L.Look(crust=name)
    x0, z0 = 4 + k * 46, 168
    for x in range(x0, x0 + 40):
        for z in range(z0, z0 + 40):
            w.column(x, z, YS - 2, YS - 1, *look.rock(x, YS - 2, z))
            A.lay_crust(w, x, z, ground, look)
    w.sign(x0 + 1, YS, z0 - 1, ["crust", name])
    shot(f"crust-{name.replace(' ', '-')}.png", (x0, YS - 3, z0, x0 + 40, YS + 1, z0 + 40), yaw=200, pitch=50)

# ---- row three: the rest in the board's look -----------------------------------------------------------------------------
look = L.LOOK
# a worn floor with a flight up out of it whose step edges wander
x0, z0 = 4, 120
cells = cut([(x0, z0), (x0 + 34, z0), (x0 + 34, z0 + 26), (x0, z0 + 26)], -8, look, "RRPR")
flight = set()
for x, z in list(cells):
    if x >= x0 + 20:
        t = (x + .5 - (x0 + 20)) / 14 + L._at(L.STEP, x, z) * 1.4 / 14
        floors[(x, z)] = YS - 8 + int(round(min(max(t, 0), 1) * 6))
        flight.add((x, z))
        w.column(x, z, floors[(x, z)] - 1, YS + 30, B.AIR)
        w.column(x, z, YS - 9, floors[(x, z)] - 1, *look.rock(x, YS - 9, z))
        w.set(x, floors[(x, z)] - 1, z, *look.cut_floor(x, z))
A.stairs(w, flight, feet, is_floor, lambda x, z: (1, 0), look)
A.wear(w, [c for c in cells if c not in flight and c[0] > x0 + 1 and c[1] > z0 + 1 and c[1] < z0 + 24], feet,
       lambda x, z: 2 if L._at(L.WEAR, x, z) > 0.8 else 1 if L._at(L.WEAR, x, z) > 0.62 else 0, look)
shot("ground-floor-and-flight.png", (x0 - 1, YS - 9, z0 - 1, x0 + 35, YS + 2, z0 + 27))

# a plated seam across a cut, three plates gone
x0 = 48
cut([(x0, z0), (x0 + 30, z0), (x0 + 30, z0 + 26), (x0, z0 + 26)], -10, look, "PRPR")
A.plated_strip(w, (x0 + 15, z0 + 1), (x0 + 15, z0 + 25), 10, [6, 6, 6, 6], {(1, 0), (1, 1), (2, 1)}, feet, is_floor,
               YS - 22, look)
shot("seam-plated-strip.png", (x0 - 1, YS - 23, z0 - 1, x0 + 31, YS + 3, z0 + 27))

# spoil slumped through a wall that gave way, one panel lying on it
x0 = 92
cut([(x0, z0), (x0 + 30, z0), (x0 + 30, z0 + 26), (x0, z0 + 26)], -10, look, "RRRP")
A.crust_hollow(w, A.poly_cells([(x0 - 6, z0 + 6), (x0, z0 + 4), (x0, z0 + 20), (x0 - 5, z0 + 18)]), ground, look)
A.spoil(w, [(x0, z0 + 4), (x0 + 12, z0 + 6), (x0 + 14, z0 + 13), (x0 + 11, z0 + 21), (x0, z0 + 20)],
        [(x0 - 0.5, z0 + 6), (x0 - 0.5, z0 + 18)], 5, feet, is_floor, look)
A.fallen_panel(w, (x0 + 0.4, z0 + 7), (x0 + 0.4, z0 + 15), (1, 0.15), 11, 3, 1, YS - 10, is_floor, look)
shot("spoil-and-fallen-panel.png", (x0 - 7, YS - 11, z0 - 1, x0 + 31, YS + 3, z0 + 27))

# a drift into the rock, a stall and a lamp at its mouth
x0 = 136
cut([(x0, z0), (x0 + 26, z0), (x0 + 26, z0 + 26), (x0, z0 + 26)], -8, look, "PRPP")
A.bore(w, [(x0 + 26, z0 + 13), (x0 + 50, z0 + 13)], YS - 8, YS - 8, is_floor, look)
for i, z in enumerate((z0 + 5, z0 + 11)):
    props.stall(w, x0 + 3, YS - 9, z, "e", awning=[12, 8][i], stripe=0)
props.lamp(w, x0 + 20, YS - 9, z0 + 4, height=3, post=(B.NETHER_FENCE, 0), cap=(B.SLAB, 3))
shot("town-drift-stall-lamp.png", (x0 - 1, YS - 9, z0 - 1, x0 + 40, YS + 3, z0 + 27))

build = sys.argv[1]
w.save(build, "Seamworks assets", (10, YS, 10))
out = sys.argv[2] if len(sys.argv) > 2 else None
if out:
    os.makedirs(out, exist_ok=True)
    for s in SHOTS:
        s["out"] = os.path.join(out, s["out"])
    print(render.textured(build, SHOTS))
print("sheet built:", len(SHOTS), "shots")
