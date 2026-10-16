"""Check Crucible's plan before a block is placed: each team's walks to the crucibles and the wools, every approach
to a crucible and to a cold store, the leak's clearance, the rock over every room, the rift's crossings and the
ramps' grades. One line a measure, the value then its target.

    python3 plan_check.py > ../renders/plan-check.txt
"""
import itertools
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

import land  # noqa: E402
import plan as P  # noqa: E402
from pgmvox.plan import graph as G  # noqa: E402

R = P.raster()
H = np.round(land.heights()).astype(int)


def rim_z(x):
    """Red's rim in column x: the first z from the middle whose ground stands at 44 or over."""
    return next((z for z in range(0, 30) if H[x - land.X0, z - land.Z0] >= 44), None)


def crossings():
    """Per x, the rift's crossing straight across: (red's rim z, blue's rim z)."""
    out = {}
    for x in range(land.X0 + 4, land.X1 - 3):
        zr, zi = rim_z(x), rim_z(-1 - x)
        if zr is not None and zi is not None:
            out[x] = (zr, -1 - zi)
    return out


CROSS = crossings()


def links():
    out = []
    for x, (zr, zb) in CROSS.items():
        a = P.node(R, x, zr, int(H[x - land.X0, zr - land.Z0]))
        b = P.node(R, x, zb, int(H[x - land.X0, zb - land.Z0]))
        if a and b:
            out += [(a, b, zr - zb, "bridge"), (b, a, zr - zb, "bridge")]
    return out


LINKS = links()
RULES = G.PlanRules(jumps=False, max_drop=4, diagonals=True)
E = G.graph(R, P.WALK, extra=LINKS, rules=RULES)
rows = []


def row(value, what, target, ok):
    rows.append((value, what, target, ok))
    mark = "" if ok is None else ("ok  " if ok else "MISS")
    print(f"{mark:4s} {value:>10} {what:62s} {target}")


def nodes(cells):
    return [n for n in (P.node(R, x, z, h) for x, z, h in cells) if n]


def image(cells):
    return [(*(int(v) for v in P.SYM.point(x, z)), h) for x, z, h in cells]


c = P.CORE
core_red = [(x, z, P.L1 - 1) for x in range(c.x0 - 2, c.x1 + 3) for z in range(c.z0 - 2, c.z1 + 3)
            if not (c.x0 - 1 <= x <= c.x1 + 1 and c.z0 - 1 <= z <= c.z1 + 1)]
wx, _, wz = P.WOOL_AT
wool_red = [(wx + dx, wz + dz, P.L2 - 1) for dx in (-2, 2) for dz in (-2, 2)]
mx, my, mz = P.MONUMENT
mon_red = [(mx + dx, mz + dz, P.L0 - 1) for dx in (-1, 0, 1) for dz in (-1, 1)]
spawn_red = nodes([(P.SPAWN_AT[0], P.SPAWN_AT[2], P.SPAWN_AT[1] - 1)])
spawn_blue = nodes(image([(P.SPAWN_AT[0], P.SPAWN_AT[2], P.SPAWN_AT[1] - 1)]))

Dr, pr = G.dijkstra(E, spawn_red)
Db, pb = G.dijkstra(E, spawn_blue)
own = G.route(Dr, pr, nodes(core_red))[0]
enemy = G.route(Db, pb, nodes(core_red))[0]
row(f"{own:.0f}", "red's walk to its own crucible", "40 to 90 (GO4)", 40 <= own <= 90)
row(f"{enemy:.0f}", "blue's walk to red's crucible, the rift bridged", "85 to 150 (GO3)", 85 <= enemy <= 150)
row(f"{enemy / own:.2f}", "the crucible's walks, enemy over own", "3 to 4 (GO1)", 3 <= enemy / own <= 4)
mirror = G.route(Db, pb, nodes(image(core_red)))[0]
row(f"{mirror:.0f}", "blue's walk to its own crucible", f"equal to red's {own:.0f}", abs(mirror - own) < 0.5)
sx, sz = P.SPAWN_AT[0], P.SPAWN_AT[2]
ex, ez = P.SYM.point(sx, sz)
cx, cz = (c.x0 + c.x1 + 1) / 2, (c.z0 + c.z1 + 1) / 2
ang = math.degrees(abs(math.atan2(cx - sx, cz - sz) - math.atan2(ex - sx, ez - sz)))
ang = min(ang, 360 - ang)
row(f"{ang:.0f}", "degrees the crucible stands off the line from red's spawn to blue's", "20 or over (corpus 42)",
    ang >= 20)
home = G.route(Dr, pr, nodes(mon_red))[0]
row(f"{home:.0f}", "red's walk from its spawn to its own monument", "under 40", home < 40)
to_wool = G.route(Db, pb, nodes(wool_red))[0]
row(f"{to_wool:.0f}", "blue's walk to red's wool, the rift bridged", "reached", math.isfinite(to_wool))
Dw, pw = G.dijkstra(E, nodes(wool_red))
cost, by, path = G.measure(Dw, pw, E, nodes(image(mon_red)))
row(f"{cost:.0f}", "the wool carried from red's store to blue's monument", "reached", math.isfinite(cost))
row(", ".join(f"{k} {v:.0f}" for k, v in sorted(by.items())), "  how that carry divides", "", None)
row(f"{to_wool / enemy:.2f}", "blue's walk to red's wool over its walk to red's crucible", "over 1: the wool deeper",
    to_wool > enemy)

# each approach, walked from blue's spawn through its entry
gx = (-33, -28)
APPROACH_CORE = {
    "the haul ramp, round the pit (around)": [(x, z, H[x - land.X0, z - land.Z0]) for x, z in ((19, 34), (20, 34))],
    "the lava tube from the sinkhole (below)": [(-6, 30, 41), (-5, 31, 41)],
    "the cone onto the gantry (above)": [(P.GANTRY["x1"], z, P.GANTRY["y"])
                                         for z in range(P.GANTRY["z0"], P.GANTRY["z1"] + 1)],
    "the loading gate and the slag run (through)": [(x, 59, P.L0 - 1) for x in range(gx[0], gx[1] + 1)],
}
over = [(x, z, P.GANTRY["y"]) for x in range(c.x0, c.x1 + 1) for z in range(P.GANTRY["z0"], P.GANTRY["z1"] + 1)]
for name, entry in APPROACH_CORE.items():
    a = G.route(Db, pb, nodes(entry))[0]
    De, pe = G.dijkstra(E, nodes(entry))
    b = G.route(De, pe, nodes(over if "above" in name else core_red))[0]
    row(f"{a + b:.0f}", f"blue to red's crucible by {name}", "reached", math.isfinite(a + b))
APPROACH_WOOL = {
    "the loading gate, the loading ramp and the deep ramp": [(x, 59, P.L0 - 1) for x in range(gx[0], gx[1] + 1)],
    "the pit's doors, the furnace hall and the deep ramp": [(16, 59, P.L1 - 1), (24, 59, P.L1 - 1)],
    "the flank cave from the west spur": [(P.FLANK[1][0] + dx, P.FLANK[1][2] + dz, P.FLANK[1][1] - 1)
                                          for dx in (-1, 0, 1) for dz in (-1, 0, 1)],
}
for name, entry in APPROACH_WOOL.items():
    a = G.route(Db, pb, nodes(entry))[0]
    De, pe = G.dijkstra(E, nodes(entry))
    b = G.route(De, pe, nodes(wool_red))[0]
    row(f"{a + b:.0f}", f"blue to red's wool by {name}", "reached", math.isfinite(a + b))

# the leak: the floor under the crucible is where its lava lands, and no lava of the land near it
fl = P.PIT["floor"]
row(fl + 1, "where the crucible's lava lands (on the pit's floor)", f"at or under the leak line {P.LEAK_Y}",
    fl + 1 <= P.LEAK_Y)
row(c.y0 - fl - 1, "blocks of air between the pit's floor and the crucible", "3 or over (it floats)",
    c.y0 - fl - 1 >= 3)
X, Z = land.grid()
lava_cols = [(int(x), int(z)) for x, z, h in zip(X.ravel(), Z.ravel(), H.ravel()) if h <= land.LAVA]
lava_cols += [(int(X[i, k]), int(Z[i, k])) for i, k in np.argwhere(land.lava_channel())]


def gap(box, x, z):
    return max(box.x0 - x, 0, x - box.x1, box.z0 - z, z - box.z1)


near = min(gap(c, x, z) for x, z in lava_cols)
row(near, "blocks from red's crucible to the nearest lava of the land", "over 15", near > 15)

# rock over every room, and between rooms stacked over each other
worst = []
for s in P.SPACES:
    if s.style in ("loggia", "door", "gate"):
        continue
    cells = [(x, z) for x, z in s.cells() if not (58 <= z <= 61)]
    if cells:
        cover = min(int(H[x - land.X0, z - land.Z0]) - (s.feet + s.h) for x, z in cells)
        worst.append((cover, s.name))
cover, name = min(worst)
row(cover, f"rock over the shallowest room ({name})", "2 or over", cover >= 2)
for a, b in itertools.combinations(P.SPACES, 2):
    ox = min(a.x1, b.x1) - max(a.x0, b.x0)
    oz = min(a.z1, b.z1) - max(a.z0, b.z0)
    if ox >= 0 and oz >= 0 and a.feet != b.feet:
        lo, hi = sorted((a, b), key=lambda s: s.feet)
        between = hi.feet - 1 - (lo.feet + lo.h)
        row(between, f"rock between {lo.name} and {hi.name}", "2 or over", between >= 2)

# the rift
gaps = [zr - zb - 1 for zr, zb in CROSS.values()]
row(min(gaps), "the narrowest crossing of the rift, rim to rim", "16 or more", min(gaps) >= 16)
row(f"{np.median(gaps):.0f}", "the median crossing", "", None)
t = P.TIP
tip_gap = min(t["z0"] - CROSS[x][1] - 1 for x in range(t["x0"], t["x1"] + 1))
row(tip_gap, "the crossing from the tip's end to the far rim", "12 or more", tip_gap >= 12)

# the ramps
for r in P.RAMPS:
    worst = 0.0
    for leg in r.legs:
        run = (leg.x1 - leg.x0) if leg.axis == "x" else (leg.z1 - leg.z0)
        if leg.feet0 != leg.feet1:
            worst = max(worst, abs(leg.feet0 - leg.feet1) / run)
    row(f"1 in {1 / worst:.1f}", f"the steepest leg of {r.name}", "1 in 2 or gentler", worst <= 0.55)
