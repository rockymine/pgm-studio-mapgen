"""Read Blastworks back from the built world: footing and water; each team's walks on foot to its own monument and
box; bridging to the enemy's box (its roof door and its side door) and to the middle's TNT; with the enemy's doors
blown, to the wool in the box and home; and the match's phases for the box with its two doors as the door.

    python3 walk.py <build-dir>
"""
import sys

import numpy as np

import layout as L
import objectives as P
import parts
from pgmvox import B, World
from pgmvox.play.objectives import Spawn, Wool
from pgmvox.read import audit, late
from pgmvox.read.walk import MoveRules, nearest, walk

w = World.load(sys.argv[1])
O = P.objectives()
print(f"footing problems: {len(audit.footing(w))}; water against air: {len(audit.loose_water(w))}")
zone = (w.ids[:, 1:, :] != 0).any(axis=1)                  # the void rule: over ground, or in a build zone
for x0, z0, x1, z1 in L.ZONES + [parts.image(r) for r in L.ZONES]:
    zone[x0 - w.x0:x1 - w.x0 + 1, z0 - w.z0:z1 - w.z0 + 1] = True
foot = MoveRules(max_drop=3, jumps=False, kill_y=1)
built = MoveRules(max_drop=3, jumps=False, kill_y=1, build=(zone, (1, L.MAX_BUILD)))
spawns = {o.team: o.at for o in O.of(Spawn)}


def places(team):
    """The roof door's middle and the side door's face on the void, for a team's own side."""
    tx0, tz0, tx1, tz1, _, ty1 = L.ROOF_DOOR
    sx0, sz0, sx1, sz1, sy0, _ = L.SIDE_DOOR
    out = {"roof door": ((tx0 + tx1) // 2, ty1 + 1, (tz0 + tz1) // 2),
           "side door": (sx1 + 1, sy0 + 1, (sz0 + sz1) // 2)}
    if team == "red-team":
        out = {k: P.image(v) for k, v in out.items()}
    return out


for team, at in spawns.items():
    d0 = walk(w.ids, [at], w.x0, w.z0, foot)
    d1 = walk(w.ids, [at], w.x0, w.z0, built)
    print(f"{team}: on foot from its spawn a player reaches {int((d0 >= 0).sum())} places")
    for o in O.of(Wool):
        if o.team == team:
            print(f"  to its {o.color} monument, on foot: {nearest(d0, w.x0, w.z0, *o.slot, r=1)}")
    for name, p in places(team).items():
        print(f"  to its own {name}, on foot: {nearest(d0, w.x0, w.z0, *p, r=2)}")
    enemy = [t for t in spawns if t != team][0]
    for name, p in places(enemy).items():
        print(f"  to the enemy's {name}, bridging: {nearest(d1, w.x0, w.z0, *p, r=2)}")
    print(f"  to the middle's TNT, bridging: {nearest(d1, w.x0, w.z0, -1, L.MID_H + 1, -1, r=2)}")

open_w = World.load(sys.argv[1])
doors = []
for (x0, z0, x1, z1, y0, y1) in (L.ROOF_DOOR, L.SIDE_DOOR):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            for y in range(y0, y1 + 1):
                doors += [(x, y, z), P.image((x, y, z))]
for name, keep in (("roof door blown", L.ROOF_DOOR), ("side door blown", L.SIDE_DOOR)):
    ww = World.load(sys.argv[1])
    x0, z0, x1, z1, y0, y1 = keep
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            for y in range(y0, y1 + 1):
                ww.set(*P.image((x, y, z)), B.AIR)
    o = [o for o in O.of(Wool) if o.team == "blue-team" and o.color == "orange"][0]
    d = walk(ww.ids, [spawns["blue-team"]], w.x0, w.z0, built)
    back = walk(ww.ids, [(o.found[0], o.found[1] + 1, o.found[2])], w.x0, w.z0, built)
    print(f"blue, red's {name}: spawn to the orange wool {nearest(d, w.x0, w.z0, *o.found, r=1)}, "
          f"home with it {nearest(back, w.x0, w.z0, *o.slot, r=1)}")

print("\nthe match's phases, blue's spawn to red's box wool, both its doors walled as the door:")
o = [o for o in O.of(Wool) if o.team == "blue-team" and o.color == "orange"][0]
goal = (o.found[0], o.found[1] + 1, o.found[2])
red_doors = [p for p in doors if p[0] >= 0]
rows = [("doors standing", late.phases(w, spawns["blue-team"], goal, zone, L.MAX_BUILD, door=red_doors,
                                       breakable=set(), low=1))]
for p in red_doors:
    open_w.set(*p, B.AIR)
rows.append(("both doors blown", late.phases(open_w, spawns["blue-team"], goal, zone, L.MAX_BUILD, door=red_doors,
                                             breakable=set(), low=1)))
print(late.table(rows))
