"""Read Cinderfall back from the built world: each spawn walked to its own core's plinth and to the enemy's, the
ridge and its beacon (ladder to the top), the vent tube from the pit to the blowhole, how much of the island's land
is reached, every objective checked, every block's footing.

    python3 walk.py <build-dir>

The walk opens doors (pgmvox.walk's PASSABLE has none), takes a drop of at most three and no running jumps.
"""
import sys

import numpy as np

import plan as P
from pgmvox import World, audit, walk
from pgmvox import blocks as K

w = World.load(sys.argv[1])
ids = w.ids.copy()
ids[np.isin(ids, sorted(K.DOORS))] = 0
ids[np.isin(ids, (K.B.LAVA, K.B.LAVA_FLOW))] = 0                 # lava is not ground: the library walk reads every block it does
KILL = 48                                                          # not call passable as solid. Nothing under the ravine's shore
rules = walk.MoveRules(max_drop=3, jumps=False, kill_y=KILL)       # is a place: a fall into the lava is a death
O = P.objectives()
L = P.land()


def reach(d, x, y, z, r=2):
    n = walk.nearest(d, w.x0, w.z0, x, y, z, r)
    return "not reached" if n is None else f"{n}"


problems = O.check(w)
print(f"objectives with a problem (Objectives.check): {len(problems)}")
for p in problems:
    print("   ", p)
foot = audit.footing(w)
print(f"footing problems (audit.footing): {len(foot)}")
for f in foot[:8]:
    print("   ", f)
cx, cz = P.CORE_AT
red = P.SPAWN
blue = (int(P.SYM.point(red[0], red[2])[0]), red[1], int(P.SYM.point(red[0], red[2])[1]))
for team, start in (("red", red), ("blue", blue)):
    d = walk.walk(ids, [start], w.x0, w.z0, rules)
    own = (cx, cz) if team == "red" else tuple(int(v) for v in P.SYM.point(cx, cz))
    other = tuple(int(v) for v in P.SYM.point(*own))
    print(f"{team} spawn at {start}: {int((d >= 0).sum())} places reached")
    print(f"  to its own core's plinth, its edge: {reach(d, own[0] + (5 if team == 'blue' else -5), P.PLINTH_Y + 1, own[1], 2)}")
    print(f"  to the pit's rim (the plinth's centre is lava): {reach(d, own[0] + (4 if team == 'blue' else -4), P.PLINTH_Y + 1, own[1], 1)}")
    print(f"  to the enemy's plinth, its edge: {reach(d, other[0] + (5 if team == 'red' else -5), P.PLINTH_Y + 1, other[1], 2)}")
    bx0, bz0, bx1, bz1 = P.BEACON
    if team == "red":
        print(f"  to the beacon's door: {reach(d, (bx0 + bx1) // 2, P.BEACON_Y + 1, bz1 + 1, 1)}")
        print(f"  to the beacon's top (by its ladder): {reach(d, (bx0 + bx1) // 2, P.BEACON_Y + 13, (bz0 + bz1) // 2, 2)}")
    reached = (d.max(axis=1) >= 0) & L.land
    print(f"  land columns reached: {int(reached.sum())} of {int(L.land.sum())} "
          f"({reached.sum() / L.land.sum():.0%}; the rest: the lava, sheer faces, and the tube's ceiling)")
(px, pz), py, _ = P.PIT
d = walk.walk(ids, [(px, py + 1, pz)], w.x0, w.z0, walk.MoveRules(max_drop=3, jumps=False))
(bx, bz), by, _ = P.BLOWHOLE
print(f"from the Cinder Pit's floor {(px, py + 1, pz)}:")
print(f"  to the blowhole's floor: {reach(d, bx, by + 1, bz, 1)}")
print(f"  out of the blowhole onto the plain: {reach(d, bx - 9, P.at(L, bx - 9, bz) + 1, bz, 2)}")
print(f"  to red's plinth through the tube: {reach(d, cx - 5, P.PLINTH_Y + 1, cz, 2)}")

# the ravine: the bridge on foot, and the hop chains with running jumps
bridge_a = (P.BRIDGE_X[0] - 1, P.BRIDGE_Y + 1, -1)
bridge_b = (P.BRIDGE_X[1] + 2, P.BRIDGE_Y + 1, -1)
d = walk.walk(ids, [bridge_a], w.x0, w.z0, rules)
print(f"from the bridgehead {bridge_a} on foot:")
print(f"  across the Slag Bridge to the far head {bridge_b}: {reach(d, *bridge_b, 1)}")
print(f"  onto the keystone's top (0, {P.BRIDGE_Y + 1}, 0): {reach(d, 0, P.BRIDGE_Y + 1, 0, 1)}")
jump_rules = walk.MoveRules(max_drop=3, jumps=True, max_gap=3, kill_y=KILL)
chain = P.CHAIN
first, last = chain[0], chain[-1]
for name, a, b in (("north", first, last), ("south", (-1 - last[0], -1 - last[1], last[2], last[3], last[4]),
                                            (-1 - first[0], -1 - first[1], first[2], first[3], first[4]))):
    d = walk.walk(ids, [(a[0], a[3] + 1, a[1])], w.x0, w.z0, jump_rules)
    print(f"the {name} hop chain, running jumps of up to 3, from the west shore stack {(a[0], a[3] + 1, a[1])}:")
    print(f"  to the east shore stack {(b[0], b[3] + 1, b[1])}: {reach(d, b[0], b[3] + 1, b[1], 2)}")
    d = walk.walk(ids, [(a[0], a[3] + 1, a[1])], w.x0, w.z0, rules)
    print(f"  the same on foot, no jumps: {reach(d, b[0], b[3] + 1, b[1], 2)}")
# the shore stairs down to each shore, from the plain above
for name, top, shore in (("north", (-30, 63, -45), (-5, 48, -45)), ("south", (-38, 59, 36), (-12, 48, 31))):
    d = walk.walk(ids, [top], w.x0, w.z0, rules)
    print(f"the {name} shore stair, from {top} down to the shore {shore}: {reach(d, *shore, 2)}")

# the ravine splits the board: with both bridge spans and the keystone's cap taken out, the walk to the enemy's plinth
# goes round the ravine's dry ends
cut = ids.copy()
cut[P.BRIDGE_X[0] - 1 - w.x0:P.BRIDGE_X[1] + 2 - w.x0, P.BRIDGE_Y - 2:P.BRIDGE_Y + 4, P.BRIDGE_Z[0] - 1 - w.z0:P.BRIDGE_Z[1] + 2 - w.z0] = 0
d = walk.walk(cut, [red], w.x0, w.z0, rules)
other = tuple(int(v) for v in P.SYM.point(cx, cz))
print(f"red spawn to the enemy's plinth, its edge, with the bridge taken out (round the ravine's ends): "
      f"{reach(d, other[0] + 5, P.PLINTH_Y + 1, other[1], 2)}")
