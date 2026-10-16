"""Read Coldbore back from the built world: what each spawn reaches on foot, whether the core is in sight from the
spawn room's door, what an attacker who has bridged the fissure reaches by each approach, that the vault is
sealed until the leak, where lava stands near a core, the objectives' own checks, and every block's footing. One
line a measure; red's half is read, blue's is its image.

    python3 walk.py <build-dir> > ../renders/walks.txt
"""
import sys

import numpy as np

import land
import plan as P
from pgmvox import B, World
from pgmvox.read import audit
from pgmvox.read import walk

w = World.load(sys.argv[1])
RULES = walk.MoveRules(max_drop=4, kill_y=P.KILL_Y)              # no fall a player would take damage from
FREE = walk.MoveRules(kill_y=P.KILL_Y)                          # any drop: into the pit, down the fallen ceiling


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


core, pit = P.CORE, P.PIT
mz, mx = (pit.z0 + pit.z1) // 2, (pit.x0 + pit.x1) // 2
faces = [(pit.x0 - 2, P.L1, mz), (pit.x1 + 2, P.L1, mz), (mx, P.L1, pit.z0 - 2), (mx, P.L1, pit.z1 + 2)]


def to_core(dist):
    got = [reach(dist, *f) for f in faces]
    got = [g for g in got if g is not None]
    return min(got) if got else None


def sight(eye, target):
    """True when nothing but air, a pane or a bar stands between eye and target, the core's own blocks aside."""
    clear = {B.AIR, B.IRON_BARS, B.PANE, B.NETHER_FENCE, B.LADDER, B.SNOW_LAYER}
    a, b = np.array(eye, float), np.array(target, float)
    for t in np.linspace(0, 1, 400):
        x, y, z = (int(np.floor(c)) for c in a + (b - a) * t)
        if core.x0 <= x <= core.x1 and core.y0 <= y <= core.y1 and core.z0 <= z <= core.z1:
            return True
        if w.id(x, y, z) not in clear:
            return False
    return True


spawn = [P.SPAWN_AT]
d_spawn = walk.walk(w.ids, spawn, w.x0, w.z0, FREE)
d_safe = walk.walk(w.ids, spawn, w.x0, w.z0, RULES)
own = to_core(d_safe)
show(own, "moves from red's spawn to its own reactor, no fall over four blocks", own is not None)
door = next(s for s in P.SPACES if s.name == "spawn door")
top_face = [(x + 0.5, core.y1 + 0.9, z + 0.5) for x in (core.x0, (core.x0 + core.x1) // 2, core.x1)
            for z in (core.z0, (core.z0 + core.z1) // 2, core.z1)]
seen = [(door.x0 + 0.5, P.L0 + 1.62, z + 0.5) for z in range(door.z0, door.z1 + 1)]
n_seen = sum(any(sight(e, t) for t in top_face) for e in seen)
show(f"{n_seen} of {len(seen)}", "cells of the spawn room's door the core's top is in sight from (one corner from "
     "the spawn)", n_seen > 0)
places = [("the balcony's monument", (P.MONUMENT[0], P.L0, P.MONUMENT[2] - 1)),
          ("the gate", (P.GATE["x0"] + 2, P.L0, P.GATE["z"] - 2)),
          ("the armoury", (-56, P.L0, 69)),
          ("the generator house", (34, P.L0, 55)),
          ("the garage's court", (34, P.L0, 46)),
          ("the collapsed store", (24, P.L1, 44)),
          ("the gallery's lip", (0, P.L2, 30)),
          ("the vault's door", (23, P.L2, 77)),
          ("the yard, up the spiral stair", (P.YARD["x0"] + 10, P.TOP, P.YARD["z1"] - 4))] + \
         [(f"the cave chamber at x {x}", (x + 3, fy, z + 3)) for x, fy, z, *_ in P.CHAMBERS]
for name, at in places:
    got = reach(d_safe, *at, r=3)
    show(got, f"moves from red's spawn to {name}", got is not None)
vault = next(s for s in P.SPACES if s.name == "vault")
inside = [(x, P.L2, z) for x in range(vault.x0 + 2, vault.x1, 4) for z in (vault.z0 + 2, vault.z1 - 2)]
sealed = all(reach(d_spawn, *p, r=1) is None for p in inside)
show("sealed" if sealed else "OPEN", "red's vault from red's spawn before the leak", sealed)

# an attacker who has bridged the fissure: from red's rim, and from red's gallery lip
c, half = land.fissure_line()
rim = []
for x in range(-12, 12):
    z = int(np.ceil(c[x - land.X0] + half[x - land.X0])) + 2
    rim.append((x, feet(x, z), z))
d_rim = walk.walk(w.ids, rim, w.x0, w.z0, FREE)
got = to_core(d_rim)
show(got, "moves from red's rim (bridged across) to red's reactor, any way", got is not None)
rh = P.ROOF_HOLE
for name, entry in [("the gate", (P.GATE["x0"] + 2, P.L0, P.GATE["z"] - 2)),
                    ("the generator house", (P.GARAGE["x0"] + 2, P.L0, P.GARAGE["z"] - 2)),
                    ("the fallen ceiling", (rh["x0"] - 3, feet(rh["x0"] - 3, rh["z0"] + 2), rh["z0"] + 2))]:
    d_entry = walk.walk(w.ids, [entry], w.x0, w.z0, FREE)
    a, b = reach(d_rim, *entry, r=2), to_core(d_entry)
    show(None if a is None or b is None else a + b, f"  by {name}", a is not None and b is not None)
lip = [(x, P.L2, z) for x, z in P.gallery_cells() if abs(x) < 4][:6]
d_lip = walk.walk(w.ids, lip, w.x0, w.z0, FREE)
got = to_core(d_lip)
show(got, "moves from red's gallery lip (bridged across at depth) to red's reactor", got is not None)
got = reach(walk.walk(w.ids, [(rh["x0"] + 2, P.L1, rh["z1"] + 4)], w.x0, w.z0, RULES),
            rh["x0"] - 3, feet(rh["x0"] - 3, rh["z0"] + 2), rh["z0"] + 2, r=3)
show(got, "moves from the store's floor back up the rubble to the snow (a drop in; out takes blocks)", None)

# the leak: lava under the leak height within fifteen blocks of the core's footprint, and loose lava anywhere
x0, x1, z0, z1 = core.x0 - 15, core.x1 + 15, core.z0 - 15, core.z1 + 15
sub = w.ids[x0 - w.x0:x1 - w.x0 + 1, :P.LEAK_Y + 1, z0 - w.z0:z1 - w.z0 + 1]
near = int(np.isin(sub, [B.LAVA, B.LAVA_FLOW]).sum())
show(near, "lava blocks within 15 of red's core at or under its leak height", near == 0)
under = w.ids[pit.x0 - w.x0:pit.x1 - w.x0 + 1, pit.y0:core.y0, pit.z0 - w.z0:pit.z1 - w.z0 + 1]
show(int((under != 0).sum()), "blocks between the core and the pit's floor, the cradle's ladder aside",
     int(((under != 0) & (under != B.LADDER)).sum()) == 0)
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
