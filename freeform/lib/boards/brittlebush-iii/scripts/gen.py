"""Generate Brittlebush III from its studio plan: red's part block for block in the Brittlebush style
(pgmvox.brittle), its spawn house and its wool's tower with the wool's heart over it, then turned a quarter three
times for blue, green and yellow, each turn moving the team's colours and the wool's colours on a team; then the
monuments and the wools.

    python3 gen.py <build-dir>

    the ground      every cell of the plan as pgmvox.brittle lays it: the cap on every edge and stair side, the
                    birch panels, frames, sand and grass, the stairs of slab and block, the decks and the hollows
                    and pillars under them, the water zones' water, the bare zones' cobwebs toward the void
    the spawn       a house of black clay over the spawn's footprint, two storeys, its door toward the lane, the
                    team's band under its plates; a stack of the team's wool floating high over it
    the wool        a tower of three storeys over the wool's footprint, its door onto the ground in front, the wool's
                    colour in its bands, and the wool's heart floating over it
"""
import random
import sys

import numpy as np

import plan as P
from pgmvox import B, World
from pgmvox.brittle import CELL, build, heart, tower
from pgmvox.orient import turn_world

cells, team = P.cells()
lo, hi = P.extent(cells)
w = World(lo, lo, hi - lo + 1, hi - lo + 1, sy=64)
rng = random.Random(f"{P.BOARD}/ground")
red = [c for c, t in team.items() if t == 0]

# 1. red's part: the ground, the spawn's house and mark, the wool's tower and heart
build(w, cells, only=red, rng=rng, dye=P.DYES[0])
sx0, sz0, sx1, sz1 = P.SPAWN_BOX
tower(w, P.SPAWN_BOX, P.SPAWN_Y, [(6, 0), (4, 1)], P.DYES[0],
      door=(P.SPAWN_DOOR, (sz0 + 2, sz1 - 2) if P.SPAWN_DOOR in "ew" else (sx0 + 2, sx1 - 2)))
x, _, z = P.SPAWN_AT
for y in range(P.SPAWN_Y + 20, P.SPAWN_Y + 23):
    w.set(x, y, z, B.WOOL, P.DYES[0])
wx0, wz0, wx1, wz1 = P.WOOL_BOX
top, (hx, hz) = tower(w, P.WOOL_BOX, P.WOOL_Y, [(6, 0), (5, 1), (4, 2)], P.KEEP_DYES[0],
                      door=("s", (wx0 + 3, wx1 - 3)))
heart(w, hx, top + 8, hz, P.KEEP_DYES[0], facing="s", hang=top + 1)
for mx, mz in P.MONUMENTS:                                        # room over the monuments' slots
    for y in range(P.SPAWN_Y + 1, P.SPAWN_Y + 5):
        w.set(mx, y, mz, B.AIR)

# 2. the other three, each the last turned a quarter clockwise, its team's and its wool's colours moved on
for k in range(1, 4):
    mask = np.zeros((w.sx, w.sz), bool)
    for (cx, cz), t in team.items():
        if t == k - 1:
            mask[cx * CELL - w.x0:(cx + 1) * CELL - w.x0, cz * CELL - w.z0:(cz + 1) * CELL - w.z0] = True
    recolour = {}
    for a, b in ((P.DYES[k - 1], P.DYES[k]), (P.KEEP_DYES[k - 1], P.KEEP_DYES[k])):
        for bid in (B.WOOL, B.STAINED_CLAY, B.STAINED_PANE, B.STAINED_GLASS, B.CARPET):
            recolour[(bid, a)] = (bid, b)
    turn_world(w, "cw", mask, recolour=recolour)

P.objectives().stamp(w)
w.save(sys.argv[1], "Brittlebush III", (0, 50, 0))
print(f"saved: {int(np.count_nonzero(w.ids))} blocks, {len(w.tiles)} tile entities")
