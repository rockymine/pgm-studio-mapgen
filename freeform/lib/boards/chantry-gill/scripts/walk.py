"""Read Chantry Gill back from the built world: footing and water, each team's walk on foot to its own monuments,
and the walk to the enemy's with the build zone between the teams standable (a player bridging it); then the ways
the plan names, walked through their waypoints: the adit, the chimney, the brig and the timber bridge.

    python3 walk.py <build-dir>
"""
import sys

import numpy as np

import layout as L
import objectives as P
from pgmvox import World
from pgmvox.read import audit
from pgmvox.read.walk import MoveRules, nearest, walk
from pgmvox.play.objectives import Destroyable, Spawn

w = World.load(sys.argv[1])
O = P.objectives()
print(f"footing problems: {len(audit.footing(w))}; water against air: {len(audit.loose_water(w))}")
spawns = {o.team: o.at for o in O.of(Spawn)}
mons = O.of(Destroyable)
X = np.arange(w.x0, w.x0 + w.sx)[:, None] + 0 * np.arange(w.sz)[None, :]
Z = np.arange(w.z0, w.z0 + w.sz)[None, :] + 0 * np.arange(w.sx)[:, None]
zone = (Z >= -14) & (Z <= 13)
foot = MoveRules(max_drop=3, jumps=False)
built = MoveRules(max_drop=3, jumps=False, build=(zone, (30, 60)))


def under(m):
    b = m.box
    return (b.x0, b.y0 - 3, b.z0)                                  # the floor under the floating monument


for team, at in spawns.items():
    d0 = walk(w.ids, [at], w.x0, w.z0, foot)
    d1 = walk(w.ids, [at], w.x0, w.z0, built)
    for m in mons:
        x, y, z = under(m)
        own = m.team == team
        d = nearest(d0 if own else d1, w.x0, w.z0, x, y, z, r=2)
        print(f"{team:9} to {m.id:10} ({'own' if own else 'enemy'}, {'on foot' if own else 'bridging the zone'}): "
              f"{d if d is not None else 'not reached'}")


def via(points, rules):
    """Moves through the points in order, each leg walked from the last point: None where a leg is not reached."""
    total = 0
    for a, b in zip(points, points[1:]):
        d = walk(w.ids, [a], w.x0, w.z0, rules)
        n = nearest(d, w.x0, w.z0, *b, r=2)
        if n is None:
            return None, (a, b)
        total += n
    return total, None


ground = lambda x, z: w.top(x, z) + 1                                    # noqa: E731
WAYS = {
    "brig, east bank over the gill to the square": [(45, ground(45, 38), 38), (-14, 43, 55)],
    "adit, gill floor to the crypt": [(32, 35, 60), (41, 35, 74), (-8, 33, 74)],
    "ladder, crypt up into the nave": [(-8, 33, 74), (-8, 45, 72)],
    "chimney, shelter up onto the bench": [(43, 35, 75), (52, 51, 78)],
    "timber bridge, spawn to the bench": [P.SPAWN_AT, (54, 51, 82)],
}
for name, pts in WAYS.items():
    n, leg = via(pts, MoveRules(max_drop=3, jumps=False))
    print(f"way {name}: {n if n is not None else f'broken between {leg[0]} and {leg[1]}'}")
