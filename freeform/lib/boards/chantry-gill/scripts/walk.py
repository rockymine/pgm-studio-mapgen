"""Read Chantry Gill back from the built world: footing and water, each team's walk on foot to its own monuments,
and the walk to the enemy's with the build zone between the teams standable (a player bridging it); then the ways
the plan names, walked through their waypoints: the adit, the chimney, the brig and the timber bridge.

    python3 walk.py <build-dir>
"""
import sys

import numpy as np

import layout as L
from layout import FLOOR as F
import objectives as P
import zone as ZN
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
zone = ZN.mask(X, Z)
ground0 = w.ids[:, 0, :] != 0
coast = [(x, z) for x, z in ZN.edges().items() if z <= ZN.CAP]
cut_off = [(x, z) for x, z in coast if not zone[x - w.x0, z - 1 - w.z0] or ground0[x - w.x0, z - 1 - w.z0]]
print(f"build zone: {len(ZN.rects())} rectangles, {int(zone.sum())} columns; front coast columns {len(coast)}, "
      f"with no zone in front of them {len(cut_off)}")
foot = MoveRules(max_drop=3, jumps=False)
built = MoveRules(max_drop=3, jumps=False, build=(zone, (F - 10, F + 20)))


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
    "brig, east bank over the gill to the square": [(45, ground(45, 38), 38), (-14, F + 3, 55)],
    "adit, gill floor to the crypt": [(32, F - 5, 60), (41, F - 5, 74), (-8, F - 7, 74)],
    "ladder, crypt up into the nave": [(-8, F - 7, 74), (-8, F + 5, 72)],
    "chimney, shelter up onto the bench": [(43, F - 5, 75), (52, F + 11, 78)],
    "timber bridge, spawn to the bench": [P.SPAWN_AT, (54, F + 11, 82)],
    "Hollin cave, front cliff to the hall": [(-39, F - 10, 18), (-22, F - 12, 38)],
    "Hollin cave, hall east into the adit": [(-22, F - 12, 38), (24, F - 14, 75)],
    "Hollin cave, hall up to the swallow hole": [(-22, F - 12, 38), (-52, ground(-52, 55), 55)],
    "tarn cave, over the water to the bench": [(60, F - 5, 47), (68, F + 2, 62), (54, F + 11, 79)],
    "side cave, east cliff into the tarn cave": [(80, F - 6, 40), (66, F - 4, 52)],
}
for name, pts in WAYS.items():
    n, leg = via(pts, MoveRules(max_drop=3, jumps=False))
    print(f"way {name}: {n if n is not None else f'broken between {leg[0]} and {leg[1]}'}")
