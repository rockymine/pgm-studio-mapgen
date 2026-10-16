"""Read Kilnhold back from the built world: each spawn walked on foot to every objective and to the places the plan
names, red's and blue's walks compared (the board is its own half turn, so they must agree), every objective
checked, and every block's footing.

    python3 walk.py <build-dir>
"""
import sys
import time

import numpy as np

import plan as P
from pgmvox import World
from pgmvox.core import blocks as K
from pgmvox.read import audit, walk

t0 = time.time()
w = World.load(sys.argv[1])
rules = walk.MoveRules(max_drop=3, jumps=False)
SYM = P.SYM


def turned(x, y, z):
    nx, nz = SYM.point(x, z)
    return int(nx), y, int(nz)


def reach(dist, x, y, z, r=1):
    n = walk.nearest(dist, w.x0, w.z0, x, y, z, r)
    return None if n is None else int(n)


def show(n):
    return "NOT REACHED" if n is None else f"{n}"


red, blue = P.SPAWN, turned(*P.SPAWN)
dist = {}
for team, start in (("red", red), ("blue", blue)):
    dist[team] = walk.walk(w.ids, [start], w.x0, w.z0, rules)

# red's places: (name, (x, y of the feet, z))
bx, bz = P.BEACON_AT
px, pz = P.PUMP_AT
fx, fy, fz = P.FLAG_POST
PLACES = [
    ("Muster Hall, the far wall", (0, P.GATE + 1, -93)),
    ("Gate Hall, the capture dais", (0, P.GATE + 2, -62)),
    ("Gate Hall, the west gallery, level part", (-14, P.MEZ + 1, -60)),
    ("the loft across the nave", (0, P.MEZ + 1, -56)),
    ("Crown, the west ramp's trench, mid", (-30, P.CROWN + 1, -56)),
    ("Crown Beacon, the deck beside it", (bx, P.CROWN + 1, bz + 4)),
    ("Crown Beacon, under it", (bx, P.CROWN + 1, bz)),
    ("Pump Hall Monument, under it", (px, P.DEEP + 1, pz)),
    ("Pump Hall, the rim of the sump", (px, P.DEEP + 1, pz + 8)),
    ("Turbine Hall, the flag", (fx, fy, fz)),
    ("Turbine Hall, the drum's walkway", (42, P.DEEP + 1, -62)),
    ("Cross Gallery, the middle", (0, P.DEEP + 1, -68)),
    ("the Workshop", (-24, P.GATE + 1, -86)),
    ("the Command Post", (23, P.GATE + 1, -86)),
    ("the Cooling Tower's court", (-46, P.PIT + 1, -38)),
    ("the Quarry Pit's floor", (45, P.PIT + 1, -40)),
    ("the Apron", (0, P.APRON + 1, -40)),
    ("the west ramp's top, on the Crown", (-46, P.CROWN + 1, -56)),
    ("the east ramp's top, on the Crown", (45, P.CROWN + 1, -56)),
    ("the Crater's shelf", (0, 60, -9)),
    ("the west lane, mid", (-52, P.FIELD + 1, -12)),
]
print("walks on foot, no jumps, a drop of at most three; moves from each spawn")
print(f"{'place (red side)':45s} {'from red':>10s} {'from blue':>10s}")
rows = {}
for name, (x, y, z) in PLACES:
    a = reach(dist["red"], x, y, z, 2)
    b = reach(dist["blue"], x, y, z, 2)
    rows[name] = (a, b)
    print(f"{name:45s} {show(a):>10s} {show(b):>10s}")
print(f"[{time.time() - t0:.0f}s]")

# the mirrored places must read the same from the other spawn
bad = 0
for name, (x, y, z) in PLACES:
    tx, ty, tz = turned(x, y, z)
    a = reach(dist["blue"], tx, ty, tz, 2)
    b = rows[name][0]
    if a != b:
        bad += 1
        print(f"  asymmetry: {name}: red reaches it in {show(b)}, blue reaches its image in {show(a)}")
print(f"places where the half turn disagrees: {bad}")

# the ratios the studio's goal rules look at
print()
print("each goal: the walk from its own spawn and from the enemy's")
for name in ("Crown Beacon, under it", "Pump Hall Monument, under it", "Turbine Hall, the flag",
             "Gate Hall, the capture dais"):
    own, enemy = rows[name]
    ratio = "-" if not own or not enemy else f"{enemy / own:.2f}"
    print(f"  {name:40s} own {show(own):>6s}   enemy {show(enemy):>6s}   enemy/own {ratio}")

# with running jumps on
jr = walk.MoveRules(max_drop=3, jumps=True)
dj = walk.walk(w.ids, [red], w.x0, w.z0, jr)
print()
print("with running jumps on, from red's spawn:")
for name in ("Crown Beacon, under it", "Pump Hall Monument, under it", "Turbine Hall, the flag"):
    x, y, z = dict(PLACES)[name]
    print(f"  {name:40s} {show(reach(dj, x, y, z, 2))}")

# the standing places no spawn reaches, by region of the board
st, _ = walk.standing(w.ids)
reached = (dist["red"] >= 0) | (dist["blue"] >= 0)
cells = st & ~reached
cells[:, :16, :] = False
print()
print(f"places to stand that neither spawn reaches on foot: {int(cells.sum())} of {int(st.sum())}")
cols = np.argwhere(cells.any(axis=1))
if len(cols):
    xs, zs = cols[:, 0] + w.x0, cols[:, 1] + w.z0
    print(f"  over x {xs.min()}..{xs.max()}, z {zs.min()}..{zs.max()}")

problems = P.objectives().check(w)
print()
print("objectives with a problem:", len(problems))
for p in problems:
    print("  ", p)
f = audit.footing(w)
print("footing problems:", len(f))
kinds = {}
for x, y, z, why in f:
    kinds.setdefault(why, []).append((x, y, z))
for why, c in sorted(kinds.items(), key=lambda kv: -len(kv[1])):
    print(f"   {len(c):5d}  {why}  e.g. {c[:3]}")
print(f"[{time.time() - t0:.0f}s]")
