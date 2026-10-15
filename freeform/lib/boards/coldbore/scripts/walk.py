"""Read Coldbore back from the built world: what each spawn reaches on foot, what an attacker who has bridged the
fissure reaches by each approach, that the vault is sealed until the leak, where lava stands near a core, the
objectives' own checks, and every block's footing. One line a measure; red's half is read, blue's is its image.

    python3 walk.py <build-dir> > ../renders/walks.txt
"""
import math
import sys

import numpy as np

import land
import plan as P
from pgmvox import B, World
from pgmvox.read import audit
from pgmvox.read import walk

w = World.load(sys.argv[1])
RULES = walk.MoveRules(max_drop=4, kill_y=P.KILL_Y)              # no fall a player would take damage from
FREE = walk.MoveRules(kill_y=P.KILL_Y)                          # any drop, the drop shaft's pool included


def feet(x, z):
    """Where a player stands on a column: one over its highest block that is not air or a snow layer."""
    col = w.ids[x - w.x0, :, z - w.z0]
    solid = np.nonzero((col != 0) & (col != B.SNOW_LAYER))[0]
    return int(solid.max()) + 1


def reach(dist, x, y, z, r=2):
    return walk.nearest(dist, w.x0, w.z0, x, y, z, r)


def show(value, what, ok=None):
    mark = "" if ok is None else ("ok  " if ok else "MISS")
    print(f"{mark:4s} {str(value):>8} {what}")


core = P.CORE
faces = [(core.x0 - 2, P.L1, (core.z0 + core.z1) // 2), (core.x1 + 2, P.L1, (core.z0 + core.z1) // 2),
         ((core.x0 + core.x1) // 2, P.L1, core.z0 - 2), ((core.x0 + core.x1) // 2, P.L1, core.z1 + 2)]


def to_core(dist):
    got = [reach(dist, *f) for f in faces]
    got = [g for g in got if g is not None]
    return min(got) if got else None


spawn = [P.SPAWN_AT]
d_spawn = walk.walk(w.ids, spawn, w.x0, w.z0, FREE)
own = to_core(d_spawn)
show(own, "moves from red's spawn to its own reactor, the drop taken", own is not None)
d_safe = walk.walk(w.ids, spawn, w.x0, w.z0, RULES)
safe = to_core(d_safe)
show(safe, "the same without any fall over four blocks (the stair)", safe is not None)
for name, at in [("the gallery's lip", (0, P.L2, 14)), ("the turn hall", (0, P.L1, 95)), ("the barracks", (-23, P.L1, 56)),
                 ("the armoury", (-20, P.L0, 65)), ("the forecourt", (0, P.L0, 38)),
                 ("the culvert's mouth", (-46, P.L0, 30))] + \
        [(f"the cave chamber at x {x}", (x + 3, fy, z + 3)) for x, fy, z, *_ in P.CHAMBERS]:
    got = reach(d_safe, *at, r=3)
    show(got, f"moves from red's spawn to {name}", got is not None)
vault_inside = [(x, P.L2, z) for x in range(-9, 9, 3) for z in (47, 63)]
sealed = all(reach(d_spawn, *p, r=1) is None for p in vault_inside)
show("sealed" if sealed else "OPEN", "red's vault from red's spawn before the leak", sealed)

# an attacker who has bridged the fissure: from red's rim at the bridge stub, and from red's gallery lip
c, half = land.fissure_line()
rim = [(x, feet(x, int(np.ceil(c[x - land.X0] + half[x - land.X0])) + 2),
        int(np.ceil(c[x - land.X0] + half[x - land.X0])) + 2) for x in range(-12, 12)]
d_rim = walk.walk(w.ids, rim, w.x0, w.z0, FREE)
got = to_core(d_rim)
show(got, "moves from red's rim (bridged across) to red's reactor, any way", got is not None)
for name, entry in [("the gate", (0, P.L0, 46)), ("the vent ladder", (P.LADDER["x"], P.L1, P.LADDER["z0"])),
                    ("the culvert", (-45, feet(-45, 31), 31))]:
    d_entry = walk.walk(w.ids, [entry], w.x0, w.z0, FREE)
    a, b = reach(d_rim, *entry, r=2), to_core(d_entry)
    show(None if a is None or b is None else a + b, f"  by {name}", a is not None and b is not None)
lip = [(x, P.L2, z) for x, z in P.gallery_cells() if abs(x) < 4][:6]
d_lip = walk.walk(w.ids, lip, w.x0, w.z0, FREE)
got = to_core(d_lip)
show(got, "moves from red's gallery lip (bridged across at depth) to red's reactor", got is not None)

# the leak: lava under the leak height within fifteen blocks of the core's footprint, and loose lava anywhere
x0, x1, z0, z1 = core.x0 - 15, core.x1 + 15, core.z0 - 15, core.z1 + 15
sub = w.ids[x0 - w.x0:x1 - w.x0 + 1, :P.LEAK_Y + 1, z0 - w.z0:z1 - w.z0 + 1]
near = int(np.isin(sub, [B.LAVA, B.LAVA_FLOW]).sum())
show(near, "lava blocks within 15 of red's core at or under its leak height", near == 0)
lava = np.isin(w.ids, [B.LAVA, B.LAVA_FLOW])
air = w.ids == 0
loose = np.zeros_like(lava)
loose[1:] |= lava[1:] & air[:-1]
loose[:-1] |= lava[:-1] & air[1:]
loose[:, :, 1:] |= lava[:, :, 1:] & air[:, :, :-1]
loose[:, :, :-1] |= lava[:, :, :-1] & air[:, :, 1:]
loose[:, 1:] |= lava[:, 1:] & air[:, :-1]
show(int(loose.sum()), "lava blocks beside air or over it, which run once a block next to them changes", None)

problems = P.objectives().check(w)
show(len(problems), "objectives with a problem", not problems)
for p in problems:
    print("      ", p)
fall = audit.footing(w)
show(len(fall), "blocks that would fall or hang on nothing", None)
kinds = {}
for x, y, z, *_ in fall:
    kinds[int(w.ids[x - w.x0, y, z - w.z0])] = kinds.get(int(w.ids[x - w.x0, y, z - w.z0]), 0) + 1
for k, n in sorted(kinds.items(), key=lambda t: -t[1])[:6]:
    print(f"       id {k}: {n}")
