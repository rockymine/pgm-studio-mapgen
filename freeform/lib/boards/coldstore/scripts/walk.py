"""Read Coldstore back from the built world: footing and water; what a spawn reaches on foot; each team's walk to its
own wool monuments, to its own seals and to the enemy's, bridging; with every seal blown and its screen opened, the
walk to the enemy's wool and home with it; and the air over every island.

    python3 walk.py <build-dir>
"""
import sys

import numpy as np

import layout as L
import objectives as P
import rooms
from pgmvox import B, World
from pgmvox.play.objectives import Spawn, Wool
from pgmvox.read import audit
from pgmvox.read.walk import MoveRules, nearest, walk

w = World.load(sys.argv[1])
O = P.objectives()
print(f"footing problems: {len(audit.footing(w))}; water against air: {len(audit.loose_water(w))}")

X, Z = w.grid()
inside = (np.abs(X + 0.5) < -L.OUTER_U - 1) & (np.abs(Z + 0.5) < L.OUTER_V - 1)
foot = MoveRules(max_drop=3, jumps=False, kill_y=L.FLOOR)
built = MoveRules(max_drop=3, jumps=False, kill_y=L.FLOOR, build=(inside, (L.TOP + 1, L.CEIL)))
spawns = {o.team: o.at for o in O.of(Spawn)}
wools = O.of(Wool)


def case_face(team_keeping, north):
    """The air just off a seal's glass case, on the void, at the capsule's middle height."""
    u, v = L.CASE_U + 1, (L.MONUMENT[2] + L.MONUMENT[3]) // 2
    y = (L.MONUMENT[4] + L.MONUMENT[5]) // 2
    if north:
        v = -1 - v
    if team_keeping == "red-team":
        u = -1 - u
    return (u, y, v)


reach = {}
for team, at in spawns.items():
    d0 = walk(w.ids, [at], w.x0, w.z0, foot)
    reach[team] = d0
    n = int((d0 >= 0).sum())
    print(f"{team}: on foot from its spawn a player reaches {n} places")
    for o in wools:
        if o.team == team:
            print(f"  to its {o.color} monument, on foot: {nearest(d0, w.x0, w.z0, *o.slot, r=1)}")
    d1 = walk(w.ids, [at], w.x0, w.z0, built)
    for keeper in spawns:
        for north in (False, True):
            f = case_face(keeper, north)
            n = nearest(d1, w.x0, w.z0, *f, r=2)
            print(f"  to {'its own' if keeper == team else 'the enemy'}'s {'north' if north else 'south'} seal, "
                  f"bridging: {n}")

open_w = World.load(sys.argv[1])
for sid, door in P.seals():
    for p in door:
        open_w.set(*p, B.AIR)
for p in rooms.monument() + rooms.case():
    for fu in (False, True):
        for fv in (False, True):
            u, y, v = p
            open_w.set(-1 - u if fu else u, y, -1 - v if fv else v, B.AIR)
for team, at in spawns.items():
    d = walk(open_w.ids, [at], w.x0, w.z0, built)
    for o in wools:
        if o.team != team:
            continue
        there = nearest(d, w.x0, w.z0, *o.found[:1], o.found[1], o.found[2], r=1)
        back = walk(open_w.ids, [(o.found[0], o.found[1] + 1, o.found[2])], w.x0, w.z0, built)
        home = nearest(back, w.x0, w.z0, *o.slot, r=1)
        print(f"{team}, every seal blown: spawn to the {o.color} wool {there}, the wool home to its monument {home}")

print("air over each island's ground (its deck or the drift on it), least and most:")
for k, (u0, u1, v0, v1) in enumerate(L.ISLANDS):
    clear = []
    for u in range(u0, u1 + 1):
        for v in range(v0, v1 + 1):
            y = L.TOP + 1
            while w.id(u, y, v) in (B.SNOW, B.PACKED_ICE):
                y += 1
            y0 = y
            while w.id(u, y, v) in (B.AIR, B.SNOW_LAYER):
                y += 1
            clear.append(y - y0)
    print(f"  island {k} u {u0}..{u1} v {v0}..{v1}: {min(clear)} to {max(clear)}")

print("\nthe match's phases, blue's spawn to red's south wool, the seal and its screen walled as the door:")
from pgmvox.read import late                                                  # noqa: E402
seal = [(-1 - u, y, v) for u, y, v in rooms.monument() + rooms.case() + rooms.screen_door()]
target = [o for o in wools if o.color == "purple"][0]
drifts = {B.SNOW, B.SNOW_LAYER, B.PACKED_ICE, B.ICE, B.GRAVEL}
got = late.phases(w, spawns["blue-team"], (target.found[0], target.found[1] + 1, target.found[2]), inside, L.CEIL,
                  door=seal, breakable=drifts, low=L.TOP + 1)
print(late.table([("blue to red's south wool", got)]))
got = late.phases(open_w, spawns["blue-team"], (target.found[0], target.found[1] + 1, target.found[2]), inside,
                  L.CEIL, door=seal, breakable=drifts, low=L.TOP + 1)
print(late.table([("the same, the seal blown", got)]))
