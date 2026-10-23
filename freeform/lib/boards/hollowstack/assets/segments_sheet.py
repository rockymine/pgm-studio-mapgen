"""The segment sheet: every piece of the kit laid once in each style, in a block of rock, then walked and measured.

    python3 segments_sheet.py <build-dir>

Prints whether the far end of each style is reached on foot, and every place a player stands inside the pieces
with fewer than three blocks of air over it, or fewer than four (a jump there meets the ceiling).
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox import World, B                                                            # noqa: E402
from pgmvox.built import segments as S                                                 # noqa: E402
from pgmvox.read.walk import MoveRules, nearest, standing, walk                         # noqa: E402


def plan():
    p = S.Plan()
    L0 = [((0, 1), (1, 1)), ((1, 1), (2, 1)), ((1, 1), (1, 0)), ((2, 1), (2, 2)), ((2, 2), (3, 2)),
          ((2, 2), (1, 2)), ((2, 2), (2, 3)), ((1, 2), (0, 2)), ((2, 3), (3, 3)), ((3, 3), (4, 3))]
    for a, b in L0:
        p.link((*a, 0), (*b, 0))
    p.link((3, 2, 0), (4, 2, 0))                            # into the stair's foot
    p.stair((4, 2, 0), "e")                                 # up into (5, 2, 1)
    p.link((5, 2, 1), (6, 2, 1))
    p.link((6, 2, 1), (6, 1, 1))
    p.room("hall", 7, 0, 8, 1, 1, "hall")
    p.link((6, 1, 1), (7, 1, 1))
    p.room("library", 5, 3, 6, 4, 0, "library")
    p.link((4, 3, 0), (5, 3, 0))
    p.shaft(0, 2, 0, 1, "w")
    p.link((0, 2, 1), (0, 3, 1))
    p.link((0, 3, 1), (1, 3, 1))
    p.port((0, 1, 0), "w", "arch")
    return p


def lay(w, x0, kit, seed):
    g = S.Grid(x0, 20, 2)
    p = plan()
    S.lay(w, g, p, kit, np.random.default_rng(seed))
    return g, p


if __name__ == "__main__":
    w = World(-4, -4, 110, 40, 64)
    w.ids[:, 1:48, :] = B.STONE
    w.ids[:, 0, :] = B.BEDROCK
    out = {}
    for x0, kit, seed in ((2, S.DUNGEON, 1), (56, S.MINE, 2)):
        out[kit["name"]] = (lay(w, x0, kit, seed), x0)
    w.ids[:, 47, :] = B.GRASS
    st, _ = standing(w.ids)
    for name, ((g, p), x0) in out.items():
        sx, sy, sz = g.centre(0, 1, 0)
        d = walk(w.ids, [(sx, sy, sz)], w.x0, w.z0, MoveRules(max_drop=3, jumps=False))
        for label, c in (("the hall up the stair", (7, 0, 1)), ("the library", (5, 3, 0)),
                         ("the shaft's top", (1, 3, 1)), ("the dead end", (1, 0, 0))):
            print(f"{name:8} {label:22} {nearest(d, w.x0, w.z0, *g.centre(*c), r=1)}")
        low3, low4 = [], []
        taken = p.taken()
        for c in taken:
            cx, cy, cz = g.corner(*c)
            for x in range(cx, cx + g.cell):
                for z in range(cz, cz + g.cell):
                    for y in range(cy + 1, cy + g.height):
                        if not st[x - w.x0, y, z - w.z0] or d[x - w.x0, y, z - w.z0] < 0:
                            continue
                        clear = 0
                        while w.ids[x - w.x0, y + clear, z - w.z0] in (B.AIR, B.TORCH, B.RAIL, B.LADDER, B.COBWEB):
                            clear += 1
                        if clear < 3:
                            low3.append((x, y, z, clear))
                        elif clear < 4:
                            low4.append((x, y, z))
        print(f"{name:8} places with under three of air: {len(low3)} {low3[:6]}; with three: {len(low4)}")
    w.save(sys.argv[1], "segments", (0, 60, 0))
