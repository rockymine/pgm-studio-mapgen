"""Read Seamworks back: from each spawn, the walk to its own flag's three posts and monument, and to the other
team's, with the other team's spawn closed as PGM closes it; every block's footing; every objective's own check.

    python3 walk.py <build-dir>
"""
import sys

import plan as P
from mapxml import OBJECTIVES, spawn_box
from pgmvox import World, B
from pgmvox.read import audit, walk

YS = P.YS
w = World.load(sys.argv[1])


def turn(p):
    return (P.W - 1 - p[0], p[1], P.H - 1 - p[2])


def closed(box):
    ids = w.ids.copy()
    ids[box.x0 - w.x0:box.x1 - w.x0 + 1, box.y0:box.y1 + 1, box.z0 - w.z0:box.z1 - w.z0 + 1] = B.STONE
    return ids


home = (P.SPAWN_AT[0], YS - 8, P.SPAWN_AT[1])
posts = [(name, (x, YS + d, z)) for name, (x, z), d in P.FLAG_POSTS]
monument = (P.MONUMENT[0], P.monument_y() - 3, P.MONUMENT[1])
for team, start, other_box in (("red", home, spawn_box.image(P.SYM)), ("blue", turn(home), spawn_box)):
    d = walk.walk(closed(other_box), [start], w.x0, w.z0)
    mine = (lambda p: p) if team == "red" else turn
    theirs = turn if team == "red" else (lambda p: p)
    print(f"{team}, from its spawn (moves; a block walked is one):")
    for side, f in (("own", mine), ("enemy", theirs)):
        for name, p in posts:
            print(f"  {side} flag at the {name}: {walk.nearest(d, w.x0, w.z0, *f(p), 2)}")
        print(f"  {side} monument, standing on the crust under it: {walk.nearest(d, w.x0, w.z0, *f(monument), 3)}")
print("footing problems:", len(audit.footing(w)))
problems = OBJECTIVES.check(w)
print("objectives with a problem:", len(problems))
for p in problems:
    print("  ", p)
