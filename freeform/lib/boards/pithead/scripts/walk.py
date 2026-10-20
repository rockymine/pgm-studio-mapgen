"""Read Pithead back: from each spawn, the walk to its own monuments, its own frontline, and to each wool it keeps
with the defence walls standing and with them opened, the other team's spawn closed as PGM closes it; every block's
footing; every objective's own check.

    python3 walk.py <build-dir>
"""
import sys

import numpy as np

import plan as P
from mapxml import OBJECTIVES, spawn_box
from pgmvox import B, World
from pgmvox.play.objectives import Wool
from pgmvox.read import audit, walk

YS = P.YS
w = World.load(sys.argv[1])


def turn(p):
    return (P.W - 1 - p[0], p[1], P.H - 1 - p[2])


def closed(box, open_walls=False):
    ids = w.ids.copy()
    ids[box.x0 - w.x0:box.x1 - w.x0 + 1, box.y0:box.y1 + 1, box.z0 - w.z0:box.z1 - w.z0 + 1] = B.STONE
    if open_walls:
        walls = ids == B.BEDROCK
        walls[:, :YS, :] = False
        ids[walls] = B.AIR
    return ids


home = (P.SPAWN_AT[0], YS + 2, P.SPAWN_AT[1])
wools = OBJECTIVES.of(Wool)
for team, start, other_box in (("red", home, spawn_box.image(P.SYM)), ("blue", turn(home), spawn_box)):
    print(f"{team}, from its spawn (moves; a block walked is one):")
    for label, opened in (("walls standing", False), ("walls opened", True)):
        d = walk.walk(closed(other_box, opened), [start], w.x0, w.z0)
        for wool in wools:
            short = wool.team.split("-")[0]
            if short == team:
                if not opened:
                    print(f"  own monument for {wool.color}: {walk.nearest(d, w.x0, w.z0, *wool.slot, 2)}")
            else:
                print(f"  {wool.color} wool it keeps, {label}: {walk.nearest(d, w.x0, w.z0, *wool.found, 2)}")
    front = (50, YS - 2, 146) if team == "red" else turn((50, YS - 2, 146))
    print(f"  its frontline's edge over the middle: {walk.nearest(d, w.x0, w.z0, *front, 2)}")
# the middle crossed by bridging the build zones at the islands' and frontlines' levels
zone = np.zeros((w.sx, w.sz), bool)
for x0, z0, x1, z1 in P.BUILD + [(*P.RC(b[2:]), *P.RC(b[:2])) for b in P.BUILD]:
    zone[x0 - w.x0:x1 - w.x0 + 1, z0 - w.z0:z1 - w.z0 + 1] = True
d = walk.walk(closed(spawn_box.image(P.SYM)), [home], w.x0, w.z0,
              walk.MoveRules(build=(zone, (YS - 3, YS - 2)), kill_y=P.KILL_Y))
island = (57, YS - 3, 125)
print("red, bridging the middle:")
print(f"  its own island: {walk.nearest(d, w.x0, w.z0, *island, 2)}")
print(f"  blue's island: {walk.nearest(d, w.x0, w.z0, *turn(island), 2)}")
print(f"  blue's frontline: {walk.nearest(d, w.x0, w.z0, *turn((50, YS - 2, 146)), 2)}")
print("footing problems:", len(audit.footing(w)))
problems = OBJECTIVES.check(w)
print("objectives with a problem:", len(problems))
for p in problems:
    print("  ", p)
