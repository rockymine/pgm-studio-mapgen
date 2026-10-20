"""Seamworks, a gray map: the plan every other script reads. Plan x is world x and plan y is world z; one unit is a
block. Team red's half is stated here and team blue's is its half turn about the board's middle.

Depths are blocks below the surface: a floor at depth -10 has its walking level ten blocks under the crust's."""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

import numpy as np  # noqa: E402

from pgmvox.geom.noise import fbm  # noqa: E402
from pgmvox.plan.raster import Symmetry  # noqa: E402

W, H = 300, 140
YS = 48                                  # the surface's walking level; its top block is YS - 1
SEAM_Y = YS - 20                         # the seam's lava, under every plated strip
LIP = 2                                  # how far a panel's top stands over the ground behind it
CRUST_RISE = (-2, 5)                     # the crust's height about YS, low and high, in whole blocks
SYM = Symmetry("half", axis=(149.5, 69.5))


def R(p):
    return (W - p[0], H - p[1])


def _crust():
    """The crust's height about YS for every column of the board, indexed [x, z]: smooth noise, made symmetric under
    the half turn and stretched to CRUST_RISE."""
    f = fbm((W, H), 30, 5, seed=7, gain=0.62)
    f = (f + f[::-1, ::-1]) / 2
    f = (f - f.min()) / (f.max() - f.min())
    lo, hi = CRUST_RISE
    return np.floor(lo + f * (hi - lo + 1)).clip(lo, hi).astype(int)


CRUST = _crust()


def ground(x, z):
    """The walking level of the crust at a column: YS plus its noise; YS off the board."""
    return YS + int(CRUST[x, z]) if 0 <= x < W and 0 <= z < H else YS


# ---- the cuts: each edge tagged by what holds it. P panels, R raw rock, B a building's face, T a tunnel mouth,
# O open to the next cut, C a panel wall that gave way --------------------------------------------------------------
RED = [((40, 26), 'C'), ((44, 8), 'R'), ((118, 6), 'R'), ((124, 3), 'P'), ((190, 5), 'B'), ((190, 13), 'T'),
         ((190, 21), 'R'), ((187, 29), 'P'), ((147, 28), 'B'), ((147, 48), 'O'), ((138, 48), 'P'), ((138, 28), 'P'),
         ((100, 28), 'R'), ((100, 32), 'P'), ((56, 32), 'P'), ((60, 50), 'R'),
         ((124, 50), 'R'), ((124, 54), 'O'), ((124, 68), 'R'), ((118, 98), 'R'), ((84, 98), 'P'), ((74, 102), 'T'),
         ((64, 103), 'P'), ((54, 106), 'P'), ((28, 112), 'B'), ((28, 100), 'P'), ((44, 94), 'R'), ((40, 72), 'R'),
         ((30, 66), 'B'), ((30, 42), 'B'), ((40, 42), 'B')]
_MID_HALF = [((124, 68), 'O'), ((124, 54), 'R'), ((130, 48), 'P'), ((138, 48), 'O'), ((147, 48), 'B'),
             ((160, 48), 'R'), ((160, 55), 'R'), ((165, 56), 'R'), ((167, 63), 'R'), ((172, 64), 'R'),
             ((174, 70), 'R')]
MIDDLE = _MID_HALF + [(R(p), t) for p, t in _MID_HALF]
PASSAGE = [((18, 66), 'B'), ((26, 66), 'P'), ((25, 77), 'P'), ((18, 90), 'B'), ((10, 90), 'P'), ((17, 77), 'P')]


def turned(cut):
    return [(R(p), t) for p, t in cut]


CUTS = [RED, turned(RED), MIDDLE, PASSAGE, turned(PASSAGE)]

# ---- undug rock standing in the cuts ------------------------------------------------------------------------------
RIB1 = [(66, 15), (102, 14), (104, 18), (99, 20.5), (68, 20)]
RIB2 = [(116, 14), (144, 13), (146, 17), (118, 19)]
MESA = [(92, 60), (110, 58), (112, 72), (108, 74), (110, 86), (94, 88), (90, 74)]
KNUCKLE = [(50, 62), (58, 60), (60, 70), (52, 72)]
_ROCK_HALF = [RIB1, RIB2, MESA, KNUCKLE]
ROCKS = _ROCK_HALF + [[R(p) for p in r] for r in _ROCK_HALF]
# the rock the middle's stepped faces were cut into, left standing between the middle and the quarries
_MASS_HALF = [(160, 48), (160, 55), (165, 56), (167, 63), (172, 64), (174, 70), (176, 72), (182, 42), (178, 36), (160, 34)]
STANDING = ROCKS + [_MASS_HALF, [R(p) for p in _MASS_HALF]]

# ---- floor depths: the cut's own depth, then zones laid over it in order. A zone is (polygon, depth) or
# (polygon, (low point, low depth), (high point, high depth)): a ramp or a flight of stairs --------------------------
CUT_DEPTH = {0: -10, 1: -10, 2: -13, 3: -8, 4: -8}
_ZONES_HALF = [
    ([(26, 44), (84, 44), (84, 60), (92, 60), (90, 74), (94, 88), (88, 99), (74, 104), (54, 107), (44, 94), (26, 94)], -8),
    ([(36, 26), (57, 26), (57, 44), (36, 44)], ((48, 26), -10), ((48, 38), -8)),          # the link, a ramp
    ([(83.6, 44), (97, 44), (97, 60), (83.6, 60)], ((97, 52), -10), ((84, 52), -8)),      # north of the mesa, a ramp
    ([(65.6, 2), (104.4, 2), (104.4, 15), (65.6, 16)], -12),                              # the sump's trough
    ([(61.6, 4), (66, 4), (66, 16), (61.6, 16)], ((66, 10), -12), ((61.6, 10), -10)),     # its stairs, both ends
    ([(104, 3), (108.4, 3), (108.4, 15), (104, 15)], ((104, 10), -12), ((108.4, 10), -10)),
    ([(28, 96), (56, 96), (56, 116), (28, 116)], ((30, 108), -11), ((50, 101), -8)),      # the side cut, a ramp
    ([(8, 60), (28, 60), (28, 80), (8, 80)], -8),                                         # the passage's landing
    ([(6, 80), (28, 80), (28, 88), (6, 88)], ((16, 88), -11), ((16, 80), -8)),            # its stairs
    ([(4, 88), (28, 88), (28, 92), (4, 92)], -11),
    ([(136, 43), (149, 43), (149, 48.8), (136, 48.8)], ((142, 48.8), -13), ((142, 43), -10)),   # the slot's stairs
    ([(117, 50), (130, 50), (130, 70), (117, 70)], ((130, 60), -13), ((117, 60), -10)),   # the throat, a ramp
]


def _turn_zone(z):
    if len(z) == 2:
        return ([R(p) for p in z[0]], z[1])
    return ([R(p) for p in z[0]], (R(z[1][0]), z[1][1]), (R(z[2][0]), z[2][1]))


ZONES = _ZONES_HALF + [_turn_zone(z) for z in _ZONES_HALF]

# ---- buildings: polygon, floor depth, roof height over the surface --------------------------------------------------
HALL = [(6, 20), (30, 20), (30, 26), (40, 26), (40, 42), (30, 42), (30, 66), (16, 66), (16, 60), (6, 60)]
BOILER = [(4, 90), (20, 90), (20, 100), (28, 100), (28, 112), (22, 112), (22, 124), (4, 124)]
WINCH = [(190, 1), (206, 1), (206, 13), (190, 13)]
PUMP = [(147, 31), (160, 31), (160, 48), (147, 48)]
STOREY = 5                               # a storey's floor slab and four of air
# each building's floor depth, and its sections: a rectangle (x0, z0, x1, z1) of the cells it covers, its storeys
# over the crust, and the cell of its ladder with the side of the wall it hangs on. Under the crust a building has
# as many storeys as its cut is deep, so a section's storeys are those plus the ones it shows above ground
_BUILDINGS_HALF = [
    ("hall", HALL, -8, [((6, 20, 30, 42), 3, ((28, 21), "n")), ((30, 26, 40, 42), 2, ((38, 27), "n")),
                        ((6, 42, 30, 66), 2, ((28, 64), "s"))]),
    ("boiler house", BOILER, -11, [((4, 90, 14, 124), 3, ((5, 91), "w")), ((14, 90, 28, 124), 2, ((26, 101), "e"))]),
    ("winch house", WINCH, -10, [((190, 1, 198, 13), 3, ((191, 2), "n")), ((198, 1, 206, 13), 2, ((204, 2), "n"))]),
    ("pump house", PUMP, -13, [((147, 31, 154, 48), 3, ((148, 32), "w")), ((154, 31, 160, 48), 2, ((158, 32), "e"))]),
]


def storeys_below(depth):
    """The storeys a building has under the surface level: every one whose floor lies below it."""
    return math.ceil(-depth / STOREY)


def _turn_section(sec):
    (x0, z0, x1, z1), n, ((lx, lz), side) = sec
    return ((W - x1, H - z1, W - x0, H - z0), n, ((W - 1 - lx, H - 1 - lz), turn_dir(side)))


def turn_dir(d):
    return {"n": "s", "s": "n", "e": "w", "w": "e"}[d]


BUILDINGS = _BUILDINGS_HALF + [(n, [R(p) for p in pg], d, [_turn_section(sec) for sec in secs])
                               for n, pg, d, secs in _BUILDINGS_HALF]
# doors: (building, the wall's cells as (x, z) pairs on the inside of the face), three wide and three high
_DOORS_HALF = [("hall", [(29, z) for z in range(46, 49)]), ("hall", [(29, z) for z in range(56, 59)]),
               ("hall", [(39, z) for z in range(34, 37)]), ("hall", [(x, 65) for x in range(20, 23)]),
               ("boiler house", [(27, z) for z in range(104, 107)]), ("boiler house", [(x, 90) for x in range(13, 16)]),
               ("winch house", [(190, z) for z in range(8, 11)]), ("pump house", [(x, 47) for x in range(152, 155)])]
DOORS = _DOORS_HALF + [(n, [(W - 1 - x, H - 1 - z) for x, z in cells]) for n, cells in _DOORS_HALF]

# ---- plated seams: (low end, high end, width, row lengths, missing (row, column)) ----------------------------------
_STRIPS_HALF = [((142.5, 28.4), (142.5, 48.6), 9, [4.4, 5.2, 4.8, 5.8], {(1, 0), (1, 1), (2, 1)}),
                ((80, 52.4), (70, 99.4), 10.5, [7, 6.2, 6.8, 6.4, 6.8, 6, 6.0],
                 {(1, 1), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0)})]
STRIPS = _STRIPS_HALF + [(R(a), R(b), w, rows, miss) for a, b, w, rows, miss in _STRIPS_HALF]
# the sump's plates across the north channel: (x, z, width, depth) boxes, the second and fourth gone
_SUMP_HALF = [(72, 7, 6, 8), (78, 7, 6, 8), (84, 7, 6, 8), (90, 7, 6, 8), (96, 7, 6, 8)]
SUMP_MISSING = {1, 3}
SUMP = [(_SUMP_HALF, False), ([(W - x - w, H - z - d, w, d) for x, z, w, d in _SUMP_HALF], True)]

# ---- spoil: a toe outline, a crest line, the crest's height over the floor, and the scar it slumped from ----------
_SPOIL_HALF = [dict(toe=[(40.4, 27.6), (45.5, 29), (51.5, 25.6), (53.6, 19.6), (51, 14.4), (45, 12.2), (41.6, 12.4)],
                    crest=[(39.6, 24.4), (41.6, 13.8)], peak=5,
                    scar=[(40, 26), (37.2, 24.6), (36.2, 19), (37.6, 14.6), (41, 12.8), (42.64, 14.1)]),
               dict(toe=[(145, 5.2), (149, 10.4), (156, 15.4), (166, 18.6), (176, 17.6), (184, 13.6), (188.6, 8.6),
                         (189.4, 5.6)], crest=[(150, 5.6), (186, 6)], peak=6, scar=None)]
SPOILS = _SPOIL_HALF + [dict(toe=[R(p) for p in s["toe"]], crest=[R(p) for p in s["crest"]], peak=s["peak"],
                             scar=[R(p) for p in s["scar"]] if s["scar"] else None) for s in _SPOIL_HALF]
# the panel that fell from the link's west wall: its foot on the wall line, how far it lies out, its turn off the
# wall's normal, and its height over the floor at the wall and at its far end, where it rests nearly flat
_FALLEN_HALF = [((40.4, 24.2), (42.2, 16.2), 11, 8, 3, 1)]
FALLEN = [(a, b, reach, turn, h0, h1, False) for a, b, reach, turn, h0, h1 in _FALLEN_HALF] + \
         [(R(a), R(b), reach, turn, h0, h1, True) for a, b, reach, turn, h0, h1 in _FALLEN_HALF]

# ---- the drift tunnels, the unfinished branch and its shaft --------------------------------------------------------
TUNNEL = [(69, 103), (71, 113), (88, 120.5), (110, 123)]          # forecourt -8 to the other twin cut -10
BRANCH = [(71, 113), (60, 116.5), (47, 119)]
SHAFT = (44, 119)                                                   # the ladder's cell, hung on its west wall
# ladders onto the crust and up out of the side cut: the ladder's cell and the side its wall is on
_LADDERS_HALF = [((80, 31), "s"), ((82, 50), "n"), ((40, 108), "s")]


LADDERS = _LADDERS_HALF + [((W - 1 - x, H - 1 - z), turn_dir(d)) for (x, z), d in _LADDERS_HALF]

# ---- play ----------------------------------------------------------------------------------------------------------
TEAMS = (("red-team", "Red", "red"), ("blue-team", "Blue", "blue"))
SPAWN_BOX = (7, 21, 16, 44)              # the back of the hall: x0, z0, x1, z1; the rest of the hall is open
SPAWN_AT = (11, 32)
FLAG_POSTS = [("passage", (22, 71), -8), ("boiler house", (9, 106), -11), ("forecourt", (52, 80), -8)]
MONUMENT = (109, 38)                      # its two-by-two-by-two box's corner, floating three over the crust


def monument_y():
    """The monument's lowest block: three of air over the highest crust under it."""
    return max(ground(MONUMENT[0] + i, MONUMENT[1] + k) for i in (0, 1) for k in (0, 1)) + 3
CAPTURES = 3


# ---- geometry helpers ------------------------------------------------------------------------------------------------
def pip(pt, poly):
    x, y = pt
    inside = False
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


def outward(a, b, poly):
    """The unit normal of edge a-b pointing out of the polygon, into the earth behind the wall."""
    dx, dz = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dz)
    n = (dz / length, -dx / length)
    mid = ((a[0] + b[0]) / 2 + n[0] * 0.4, (a[1] + b[1]) / 2 + n[1] * 0.4)
    return n if not pip(mid, poly) else (-n[0], -n[1])


def panel_runs(a, b, rng):
    """A wall's panels along a-b: (start, end) distances from a, each 10 to 17 long, half a block apart."""
    length = math.hypot(b[0] - a[0], b[1] - a[1])
    inset, gap = 0.35, 0.5
    runs, pos, end = [], inset, length - inset
    while end - pos > 0.5:
        rest = end - pos
        run = rng.uniform(10, 17)
        if rest - run < 7:
            run = rest if rest < 20 else rest / 2
        runs.append((pos, pos + run))
        pos += run + gap
    return runs


def panels():
    """Every panel as (base start, base end, outward normal, lean at each end in degrees, shade): a quad standing on
    the floor at its base and leaning back into the earth. The half turn gets the same panels turned."""
    out = []
    for k, cut in enumerate(CUTS):
        poly = [p for p, _ in cut]
        for i, (p, tag) in enumerate(cut):
            q = cut[(i + 1) % len(cut)][0]
            if tag not in "PC":
                continue
            a = p if tag == "P" else (p[0] + (q[0] - p[0]) * 0.68, p[1] + (q[1] - p[1]) * 0.68)
            family = {0: 0, 1: 0, 2: 2, 3: 3, 4: 3}[k]          # a cut and its half turn share their panels
            rng = random.Random(f"{family}-{i % len(_MID_HALF) if k == 2 else i}")
            n = outward(a, q, poly)
            length = math.hypot(q[0] - a[0], q[1] - a[1])
            ux, uz = (q[0] - a[0]) / length, (q[1] - a[1]) / length
            lean = rng.uniform(10, 14)
            for j, (s0, s1) in enumerate(panel_runs(a, q, rng)):
                l0 = lean + rng.uniform(-1.5, 1.5)
                l1 = l0 + rng.uniform(-1.5, 1.5)
                out.append(((a[0] + ux * s0, a[1] + uz * s0), (a[0] + ux * s1, a[1] + uz * s1), n, (l0, l1), j % 2))
    return out


# ---- the dressing: a market against the forecourt's rock, lamps along the walls, the boiler house's furnaces -------
_STALLS_HALF = [((43, 76), "e"), ((44, 82), "e"), ((45, 88), "e")]
STALLS = _STALLS_HALF + [((W - 1 - x, H - 1 - z), turn_dir(f)) for (x, z), f in _STALLS_HALF]
_LAMPS_HALF = [(33, 47), (47, 92), (58, 24), (96, 25), (132, 24), (176, 23), (112, 52), (116, 95), (150, 51)]
LAMPS = _LAMPS_HALF + [(W - 1 - x, H - 1 - z) for x, z in _LAMPS_HALF]
_FURNACES_HALF = [(5, z) for z in range(95, 104)]               # along the boiler house's west wall, facing in
FURNACES = [(c, "e") for c in _FURNACES_HALF] + [((W - 1 - x, H - 1 - z), "w") for x, z in _FURNACES_HALF]
_COAL_HALF = [(x, z) for x in range(7, 11) for z in range(117, 121)]
COAL = _COAL_HALF + [(W - 1 - x, H - 1 - z) for x, z in _COAL_HALF]
# chimneys: the boiler house's over its west body, the pump house's small stack over the slot
_CHIMNEYS_HALF = [("boiler house", (7, 113, 9, 115), 9), ("pump house", (149, 34, 150, 35), 5)]
CHIMNEYS = _CHIMNEYS_HALF + [(n, (W - 1 - x1, H - 1 - z1, W - 1 - x0, H - 1 - z0), h)
                             for n, (x0, z0, x1, z1), h in _CHIMNEYS_HALF]
