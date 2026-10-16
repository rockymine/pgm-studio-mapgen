"""Read Rimeburn back from the built world: each team walks from its spawn, with the seam bridged, to every goal;
the Vent is walked end to end; nothing stands over the void outside the lands and the seam; every block has
footing; no water stands against air; and each objective checks itself.

    python3 walk.py <build-dir>
"""
import sys

import numpy as np

import land as LD
import plan as P
from pgmvox import World
from pgmvox.play.objectives import Core, Destroyable, Spawn
from pgmvox.read import audit
from pgmvox.read import walk as WK

w = World.load(sys.argv[1])
X, Z = w.grid()
sx0, sz0, sx1, sz1 = P.SEAM
seam = (X >= sx0) & (X <= sx1) & (Z >= sz0) & (Z <= sz1)
O = P.objectives()
spawns = {s.team: (s.at[0], s.at[1], s.at[2]) for s in O.of(Spawn)}
print("Rimeburn, read back from the built world\n")
print(f"{'walk (moves)':<46} {'Frost':>7} {'Ember':>7}")
rules = WK.MoveRules(kill_y=P.KILL_Y, build=(seam, (30, 50)))
alone = WK.MoveRules(kill_y=P.KILL_Y)
dist = {t: WK.walk(w.ids, [p], w.x0, w.z0, rules) for t, p in spawns.items()}
home = {t: WK.walk(w.ids, [p], w.x0, w.z0, alone) for t, p in spawns.items()}
goals = [g for g in O.items if isinstance(g, (Core, Destroyable))]


def at_goal(d, g):
    """The fewest moves to stand within two blocks of a goal's footprint, at any height up to its top."""
    b = g.box
    sub = d[b.x0 - 2 - w.x0:b.x1 + 3 - w.x0, P.KILL_Y:b.y1 + 1, b.z0 - 2 - w.z0:b.z1 + 3 - w.z0]
    got = sub[sub >= 0]
    return int(got.min()) if got.size else None


for g in goals:
    own = g.team
    enemy = P.TEAMS.other(own)
    a = at_goal(home[own], g)
    b = at_goal(dist[enemy], g)
    print(f"{g.name:<22} own spawn, on foot{'':<6} {str(a):>7}")
    print(f"{'':<22} enemy spawn, bridging{'':<3} {str(b):>7}")
# the Vent: from its mouth on the cliff face to the hollow, on foot
for team, pts in (("frost", LD.VENT), ("ember", [(*LD.SYM.point(x, z), y) for x, y, z in LD.VENT])):
    if team == "frost":
        (mx, my, mz), (ex, ey, ez) = pts[0], pts[-1]
    else:
        (mx, mz, my), (ex, ez, ey) = pts[0], pts[-1]
    inward = -1 if team == "frost" else 1                       # a block in from the cliff face
    d = WK.walk(w.ids, [(mx, my, mz + inward)], w.x0, w.z0, alone)
    print(f"the Vent, {team}: mouth to the hollow floor, moves {WK.nearest(d, w.x0, w.z0, ex, ey, ez, 2)}")
land = np.zeros((w.sx, w.sz), bool)
Xl, Zl, H, lm, water, surface = LD.build()
land[:] = lm
wide = land.copy()
from scipy import ndimage  # noqa: E402
wide = ndimage.binary_dilation(land, iterations=3)
stand = WK.no_stand_above(w, P.KILL_Y, ~seam, wide)
print(f"\nplaces to stand over the kill height off the lands and the seam: {len(stand)}", stand[:8])
foot = audit.footing(w)
print(f"blocks with no footing: {len(foot)}", foot[:6])
loose = audit.loose_water(w)
print(f"water against air: {len(loose)}", loose[:6])
problems = O.check(w)
print(f"objectives with a problem: {len(problems)}")
for p in problems:
    print("  ", p)
