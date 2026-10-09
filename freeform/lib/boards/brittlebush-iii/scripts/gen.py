"""Generate Brittlebush III from its studio plan: red's part block for block in the Brittlebush style
(pgmvox.brittle), its spawn's house and its wool's house, each stacked of whole cells, then turned a quarter three
times for blue, green and yellow, each turn moving the team's colours and the wool's colours on a team; then the
monuments and the wools.

    python3 gen.py <build-dir>

    the ground      every cell of the plan as pgmvox.brittle lays it: the cap on every edge and stair side, the
                    birch panels, frames, sand and grass, the stairs of slab and block, the decks and the hollows
                    and pillars under them, the water zones' water, the bare zones' cobwebs toward the void
    the spawn       a house of three storeys of whole cells over the spawn's piece: two by two, the two back
                    cells, one cell; doors onto the lane and toward the monuments, the keep's floor inside, a beacon
                    under the team's glass on top, and a stack of the team's wool floating high over it
    the wool        a house of three storeys of whole cells over the wool's piece (pgmvox.brittle.house): two by
                    two, an L, one cell; its door onto the ground in front, the wool on a square of its colour, a
                    beacon on top shining through glass of the wool's colour
"""
import random
import sys

import numpy as np

import plan as P
from pgmvox import B, World
from pgmvox.brittle import CELL, build, house
from pgmvox.orient import turn_world

cells, team = P.cells()
lo, hi = P.extent(cells)
w = World(lo, lo, hi - lo + 1, hi - lo + 1, sy=64)
rng = random.Random(f"{P.BOARD}/ground")
red = [c for c, t in team.items() if t == 0]

# 1. red's part: the ground, the spawn's house and mark, the wool's house
build(w, cells, only=red, rng=rng, dye=P.DYES[0])
sx0, sz0, sx1, sz1 = P.SPAWN_PIECE
for x in range(sx0, sx1 + 1):
    for z in range(sz0, sz1 + 1):
        for y in range(P.SPAWN_Y + 1, P.SPAWN_Y + 20):
            w.set(x, y, z, B.AIR)
house(w, P.SPAWN_LAYERS, P.SPAWN_Y, P.DYES[0], door=P.SPAWN_DOORS, cobwebs=False, floor_block=None)
x, _, z = P.SPAWN_AT
for y in range(P.SPAWN_Y + 22, P.SPAWN_Y + 25):
    w.set(x, y, z, B.WOOL, P.DYES[0])
wx0, wz0, wx1, wz1 = P.WOOL_BOX
for x in range(wx0, wx1 + 1):                                     # the bed and its birch off the wool's piece
    for z in range(wz0, wz1 + 1):
        for y in range(P.WOOL_Y + 1, P.WOOL_Y + 20):
            w.set(x, y, z, B.AIR)
house(w, P.WOOL_LAYERS, P.WOOL_Y, P.KEEP_DYES[0], door=P.WOOL_DOOR)
fx, _, fz = P.WOOL_AT
for x in range(fx - 1, fx + 2):                                   # the wool stands on a square of its colour
    for z in range(fz - 1, fz + 2):
        w.set(x, P.WOOL_Y, z, B.WOOL, P.KEEP_DYES[0])
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
