"""Read Crucible back from the built world: what red's spawn reaches on foot, what an attacker who has bridged the
rift reaches by each approach to the crucible and to the cold store, the carry home, the crucible's leak clearance,
the objectives' own checks and every block's footing. One line a measure; red's half is read, blue's is its image.

    python3 walk.py <build-dir> > ../renders/walks.txt
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

import land  # noqa: E402
import plan as P  # noqa: E402
from pgmvox import B, World  # noqa: E402
from pgmvox.read import audit, walk  # noqa: E402

w = World.load(sys.argv[1])
SAFE = walk.MoveRules(max_drop=4, kill_y=P.KILL_Y)            # no fall a player would take damage from
FREE = walk.MoveRules(kill_y=P.KILL_Y)                         # any drop


def feet(x, z):
    col = w.ids[x - w.x0, :, z - w.z0]
    solid = np.nonzero((col != 0) & ~np.isin(col, [B.LAVA, B.LAVA_FLOW, B.CARPET, B.RAIL]))[0]
    return int(solid.max()) + 1


def reach(dist, x, y, z, r=2):
    return walk.nearest(dist, w.x0, w.z0, x, y, z, r)


def show(value, what, ok=None):
    mark = "" if ok is None else ("ok  " if ok else "MISS")
    print(f"{mark:4s} {str(value):>8} {what}")


def img(p):
    x, z = P.SYM.point(p[0], p[2])
    return (int(x), p[1], int(z))


core = P.CORE
ring = [(x, P.L1, z) for x in range(core.x0 - 2, core.x1 + 3) for z in range(core.z0 - 2, core.z1 + 3)
        if not (core.x0 - 1 <= x <= core.x1 + 1 and core.z0 - 1 <= z <= core.z1 + 1)]


def to_core(dist, cells=ring):
    got = [d for d in (reach(dist, *c, r=0) for c in cells) if d is not None]
    return min(got) if got else None


spawn = [P.SPAWN_AT]
d_safe = walk.walk(w.ids, spawn, w.x0, w.z0, SAFE)
d_free = walk.walk(w.ids, spawn, w.x0, w.z0, FREE)
print("== red's spawn, on foot ==")
show(to_core(d_safe), "moves from red's spawn to the floor round its own crucible, no fall over four",
     to_core(d_safe) is not None)
show(to_core(d_free), "  the same, any drop (off the loggia)", None)
store = P.STORE
places = [("the pour room's monument", (P.MONUMENT[0], P.L0, P.MONUMENT[2] - 1)),
          ("the loggia", (22, P.L0, 59)),
          ("the loading gate, outside", (-30, 0, 55)),
          ("the loading hall", (-31, P.L0, 70)),
          ("the furnace hall", (15, P.L1, 68)),
          ("the slag run's west end", (-40, P.L1, 65)),
          ("the cold store's passage", (-36, P.L2, 80)),
          ("the haul ramp's top", (19, 48, 34)),
          ("the gantry's deck", (30, P.GANTRY["y"] + 1, 45)),
          ("the cone's vent", (land.CONE[0] + 2, 0, land.CONE[1])),
          ("the sinkhole's floor", (-6, 42, 30)),
          ("the tip's end", (-12, 0, 6)),
          ("the flank cave's mouth", (P.FLANK[0][0], P.FLANK[0][1], P.FLANK[0][2])),
          ("the flank cave's chamber", (P.CAVE_CHAMBERS[0][0], P.CAVE_CHAMBERS[0][1], P.CAVE_CHAMBERS[0][2]))]
for name, at in places:
    x, y, z = at
    if y == 0:
        y = feet(x, z)
    got = reach(d_safe, x, y, z, r=3)
    show(got, f"moves from red's spawn to {name}", got is not None)
inside = [(x, P.L2, z) for x in range(store.x0 + 2, store.x1, 4) for z in (store.z0 + 2, store.z1 - 2)]
got = min([d for d in (reach(d_safe, *p, r=1) for p in inside) if d is not None], default=None)
show(got, "moves from red's spawn into its own cold store (the room rule keeps red out; the walk does not)", None)

# an attacker who has bridged the rift: blue standing on red's rim
print("== blue, landed on red's rim ==")
r = land.rim()
rim = []
for x in range(-60, 60, 3):
    z = int(np.ceil(r[x - land.X0])) + 1
    rim.append((x, feet(x, z), z))
d_rim = walk.walk(w.ids, rim, w.x0, w.z0, FREE)
d_rim_safe = walk.walk(w.ids, rim, w.x0, w.z0, SAFE)
got = to_core(d_rim_safe)
show(got, "moves from red's rim to red's crucible, no fall over four", got is not None)


def by(name, entry, target, rules=SAFE, around=None):
    a = reach(d_rim_safe, *entry, r=2)
    d_entry = walk.walk(w.ids, [entry], w.x0, w.z0, rules)
    b = target(d_entry)
    show(None if a is None or b is None else a + b, f"  by {name}", a is not None and b is not None)


ramp_top = (19, feet(19, 34), 34)
tube_mouth = (-5, P.TUBE[0][1], P.TUBE[0][2])
gantry_end = (P.GANTRY["x1"], P.GANTRY["y"] + 1, 45)
gate_out = (-30, feet(-30, 55), 55)
loggia_end = (31, feet(31, 56), 56)
by("the haul ramp (around)", ramp_top, to_core)
by("the lava tube from the sinkhole (below)", tube_mouth, to_core, FREE)
over = [(x, P.GANTRY["y"] + 1, 45) for x in range(core.x0, core.x1 + 1)]
by("the cone's shoulder onto the gantry (above), to the girder over the crucible", gantry_end,
   lambda d: to_core(d, over))
by("the loading gate and the slag run into the furnace hall (through)", gate_out, to_core)
by("the loggia's end and the furnace ramp (through)", loggia_end, to_core)

print("== the cold store ==")
door = (-36, P.L2, 81)
got = reach(d_rim_safe, *door, r=2)
show(got, "moves from red's rim to the cold store's door", got is not None)
flank = (P.FLANK[0][0], P.FLANK[0][1], P.FLANK[0][2])
by("the loading gate, the loading ramp, the slag run and the deep ramp", gate_out,
   lambda d: reach(d, *door, r=2))
by("the pit, the furnace hall, the slag run and the deep ramp", ramp_top, lambda d: reach(d, *door, r=2))
west = (-46, P.L2, 89)
by("the flank cave from the west spur to the store's west door", flank, lambda d: reach(d, *west, r=2))
wool = P.WOOL_AT
d_wool = walk.walk(w.ids, [(wool[0] + 2, P.L2, wool[2])], w.x0, w.z0, SAFE)
home = img((P.MONUMENT[0], P.L0, P.MONUMENT[2] - 1))
# the carry: the wool to red's rim, then (bridged) from blue's rim to blue's monument
d_brim = walk.walk(w.ids, [img(p) for p in rim], w.x0, w.z0, SAFE)
a = min([d for d in (reach(d_wool, *p, r=1) for p in rim) if d is not None], default=None)
b = reach(d_brim, *home, r=2)
show(None if a is None or b is None else f"{a}+{b}", "the wool carried from red's store to red's rim, then from "
     "blue's rim to blue's monument", a is not None and b is not None)

print("== the crucible ==")
x0, x1, z0, z1 = core.x0 - 15, core.x1 + 15, core.z0 - 15, core.z1 + 15
sub = w.ids[x0 - w.x0:x1 - w.x0 + 1, :P.LEAK_Y + 1, z0 - w.z0:z1 - w.z0 + 1]
near = int(np.isin(sub, [B.LAVA, B.LAVA_FLOW]).sum())
show(near, f"lava within 15 of red's crucible at or under its leak line y {P.LEAK_Y}", near == 0)
under = [(x, z) for x in range(core.x0, core.x1 + 1) for z in range(core.z0, core.z1 + 1)]
gap = min(core.y0 - 1 - max(y for y in range(core.y0) if w.id(x, y, z) != B.AIR) for x, z in under)
fl = max(max(y for y in range(core.y0) if w.id(x, y, z) != B.AIR) for x, z in under)
show(gap, "blocks of air under the crucible (it floats)", gap >= 3)
show(fl + 1, f"where lava let out lands: y {fl + 1}, the leak line {P.LEAK_Y}", fl + 1 <= P.LEAK_Y)
lava = np.isin(w.ids, [B.LAVA])
air = w.ids == 0
loose = np.zeros_like(lava)
loose[:-1] |= lava[:-1] & air[1:]
loose[1:] |= lava[1:] & air[:-1]
loose[:, :, 1:] |= lava[:, :, 1:] & air[:, :, :-1]
loose[:, :, :-1] |= lava[:, :, :-1] & air[:, :, 1:]
loose[:, 1:] |= lava[:, 1:] & air[:, :-1]
show(int(loose.sum()), "still lava with air beside or under it (runs once a block by it changes)", None)
for i, y, k in np.argwhere(loose)[:8]:
    print(f"       at ({i + w.x0}, {y}, {k + w.z0})")

print("== the build ==")
problems = P.objectives().check(w)
show(len(problems), "objectives with a problem", not problems)
for p in problems:
    print("      ", p)
fall = audit.footing(w)
show(len(fall), "blocks that would fall or hang on nothing", None)
kinds = {}
for x, y, z, *_ in fall:
    k = int(w.ids[x - w.x0, y, z - w.z0])
    kinds[k] = kinds.get(k, 0) + 1
for k, n in sorted(kinds.items(), key=lambda t: -t[1])[:6]:
    print(f"       id {k}: {n}")
