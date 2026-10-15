"""Check Coldbore's plan before a block is placed: each team's walks to the cores and the wools, the leak's
clearance, the rock over every room, the fissure's gaps, and every approach to a core. One line a measure, the
value then its target.

    python3 plan_check.py > ../renders/plan-check.txt
"""
import itertools
import math

import numpy as np

import land
import plan as P
from pgmvox.plan import graph as G

R = P.raster()
R_open = P.raster(opened=True)
LINKS = P.links()
RULES = G.PlanRules(jumps=False, max_drop=4)


def hatch_links():
    """The leak opens the hatch: the well's floor drops into the vault's pool. Both halves."""
    out = []
    for x, z in [(-1, 55)]:
        a = P.node(x, z, P.L1 - 1)
        b = P.node(x, z, P.L2 - 2)
        out.append((a, b, 6, "hatch"))
        xa, za = P.SYM.point(x, z)
        out.append((P.node(xa, za, P.L1 - 1), P.node(xa, za, P.L2 - 2), 6, "hatch"))
    return out


E = G.graph(R, P.WALK, extra=LINKS, rules=RULES)
E_open = G.graph(R_open, P.WALK, extra=LINKS + hatch_links(), rules=RULES)

O = P.objectives()
spawn = {"red": [P.node(P.SPAWN_AT[0], P.SPAWN_AT[2], P.TOP - 1)]}
bx, bz = P.SYM.point(P.SPAWN_AT[0], P.SPAWN_AT[2])
spawn["blue"] = [P.node(bx, bz, P.TOP - 1)]


def ring(box, feet):
    """The floor cells round a box's footprint a player strikes it from."""
    return [P.node(x, z, feet - 1) for x in range(box.x0 - 2, box.x1 + 3) for z in range(box.z0 - 2, box.z1 + 3)
            if not (box.x0 - 1 <= x <= box.x1 + 1 and box.z0 - 1 <= z <= box.z1 + 1)]


def image_nodes(nodes):
    return [(*P.SYM.point(n[0], n[1]),) + tuple(n[2:]) for n in nodes]


core_red = ring(P.CORE, P.L1)
core_blue = image_nodes(core_red)
wool_red = [P.node(P.WOOL_AT[0] + dx, P.WOOL_AT[2] + dz, P.L2 - 1) for dx in (-1, 0) for dz in (-1, 0)]
mon_red = [P.node(P.MONUMENT[0] + dx, P.MONUMENT[2] + dz, P.TOP - 1) for dx in (-1, 1) for dz in (-1, 1)]
mon_blue = image_nodes(mon_red)

rows = []


def row(value, what, target, ok):
    rows.append((value, what, target, ok))
    mark = "" if ok is None else ("ok  " if ok else "MISS")
    print(f"{mark:4s} {value:>8} {what:58s} {target}")


Dr, pr = G.dijkstra(E, spawn["red"])
Db, pb = G.dijkstra(E, spawn["blue"])
own = G.route(Dr, pr, core_red)[0]
enemy = G.route(Db, pb, core_red)[0]
row(f"{own:.0f}", "red's walk to its own reactor", "40 to 90 (GO4)", 40 <= own <= 90)
row(f"{enemy:.0f}", "blue's walk to red's reactor", "85 to 150 (GO3)", 85 <= enemy <= 150)
row(f"{enemy / own:.2f}", "the reactor's walks, enemy over own", "3 to 4 (GO1)", 3 <= enemy / own <= 4)
mirror = G.route(Db, pb, core_blue)[0]
row(f"{mirror:.0f}", "blue's walk to its own reactor", f"equal to red's {own:.0f}", abs(mirror - own) < 0.5)

Dbo, pbo = G.dijkstra(E_open, spawn["blue"])
to_wool = G.route(Dbo, pbo, wool_red)[0]
row(f"{to_wool:.0f}", "blue's walk to red's wool once the reactor leaks", "reached", math.isfinite(to_wool))
Dw, pw = G.dijkstra(E_open, wool_red)
home = G.route(Dw, pw, mon_blue)[0]
row(f"{home:.0f}", "the wool carried from red's vault to blue's monument", "reached", math.isfinite(home))
cost, by, path = G.measure(Dw, pw, E_open, mon_blue)
row(", ".join(f"{k} {v:.0f}" for k, v in sorted(by.items())), "  how that carry divides", "", None)
sealed = G.route(Db, pb, wool_red)[0]
row("sealed" if not math.isfinite(sealed) else f"{sealed:.0f}", "red's wool before the leak", "sealed",
    not math.isfinite(sealed))

# every approach to red's reactor, each walked with the others taken away
APPROACHES = {
    "the gate (through)": [P.node(x, 46, P.L0 - 1) for x in range(P.GATE["x0"], P.GATE["x1"] + 1)],
    "the vent ladder (above)": [P.node(P.LADDER["x"], P.LADDER["z0"], P.L1 - 1)],
    "the deep gallery (below)": [P.node(x, z, P.L2 - 1) for x, z in P.gallery_cells() if z == min(
        zz for xx, zz in P.gallery_cells() if xx == x)],
    "the culvert (around)": [P.node(-31, 56, P.L1 - 1)],
}
for name, entry in APPROACHES.items():
    a = G.route(Db, pb, entry)[0]
    De, pe = G.dijkstra(E, entry)
    b = G.route(De, pe, core_red)[0]
    row(f"{a + b:.0f}", f"blue to red's reactor by {name}", "reached", math.isfinite(a + b))

# the leak: no lava within 15 blocks of the core's footprint at or under the leak height but the well's own
H, X, Z = land.heights()
lava_cols = [(int(x), int(z)) for x, z, h in zip(X.ravel(), Z.ravel(), H.ravel()) if h <= land.LAVA]
for x, top, z, r in P.LAVA_PONDS:
    lava_cols += [(x + dx, z + dz) for dx in range(-4, 5) for dz in range(-4, 5) if math.hypot(dx, dz) <= r]
lava_cols += [P.SYM.point(x, z) for x, z in lava_cols]


def gap(box, x, z):
    return max(box.x0 - x, 0, x - box.x1) + 0, max(box.z0 - z, 0, z - box.z1)


near = min(max(gap(P.CORE, x, z)) for x, z in lava_cols)
row(near, "blocks from red's core to the nearest lava under the leak height", "over 15", near > 15)
row(P.LEAK_Y, "the leak height (the core's lowest block less its leak)", f"the well's floor at {P.WELL.y0} or over",
    P.WELL.y0 <= P.LEAK_Y)

# rock over every room: the surface over its ceiling, and the space over it
top = np.round(H).astype(int)
worst = []
for s in P.SPACES:
    f = P.FACADE
    under_roof = lambda x, z: f["x0"] <= x <= f["x1"] and f["z0"] <= z <= f["z1"] and s.feet == P.L0
    cells = [(x, z) for x, z in s.cells() if not under_roof(x, z)]      # the facade's roof covers its own
    if not cells:
        continue
    ceil = s.feet + s.h
    cover = min(int(top[x - land.X0, z - land.Z0]) - ceil for x, z in cells)
    worst.append((cover, s.name))
cover, name = min(worst)
row(cover, f"rock over the shallowest room ({name})", "at least 3", cover >= 3)
for a, b in itertools.combinations(P.SPACES, 2):
    ox = min(a.x1, b.x1) - max(a.x0, b.x0)
    oz = min(a.z1, b.z1) - max(a.z0, b.z0)
    if ox >= 0 and oz >= 0:
        lo, hi = sorted((a, b), key=lambda s: s.feet)
        between = hi.feet - 1 - (lo.feet + lo.h)
        if between < 0 and lo.feet != hi.feet:
            row(between, f"rock between {lo.name} and {hi.name}", "at least 3", False)
        elif lo.feet != hi.feet and between < 3:
            row(between, f"rock between {lo.name} and {hi.name}", "at least 3", between >= 3)

# the fissure's gaps
bridges = [c for a, b, c, t in LINKS if t == "bridge"]
deep = [c for a, b, c, t in LINKS if t == "deep bridge"]
row(min(bridges), "the narrowest surface crossing of the fissure", "16 or more", min(bridges) >= 16)
row(f"{np.median(bridges):.0f}", "the median surface crossing", "", None)
row(min(deep), "the narrowest crossing between the galleries, at depth", "8 or more", min(deep) >= 8)
