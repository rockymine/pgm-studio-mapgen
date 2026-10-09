"""Generate Brittlebush KotH from its blueprint: red's quadrant block for block in the Brittlebush style
(pgmvox.brittle), then turned a quarter three times for blue, green and yellow, each turn recolouring the team's
clay, wool and glass; then the five hills' pads, the spawners' marks and the objectives over the whole board.

    python3 gen.py <build-dir>

    the ground      every cell of the blueprint as pgmvox.brittle lays it: the cap on every edge, every other
                    cell's panel, frames and fields, the stairs of slab and block, the decks on their posts, the gaps'
                    cobwebs, the water
    the keep        smooth sandstone ringed in the team's clay; a line of the team's wool along its front edges; a
                    stack of the team's wool floating high over the spawn, as Brittlebush marks a spawn
    the house       in the keep's outer corner, stacked of whole cells (pgmvox.brittle.house): two by two over the
                    spawn, an L of three, the corner cell on top with a beacon under the team's glass; its doors
                    open from the spawn's cell onto the keep's yard
    the hills       a pad of white clay ten blocks square on each, cleared of the beds and trees over it
    the spawners    a mark of chiseled sandstone under each: golden apples on the inner islands, arrows on the landings
"""
import random
import sys

import numpy as np

import plan as P
from pgmvox import B, World
from pgmvox.brittle import CELL, Cell, build, house
from pgmvox.orient import turn_world

DYES = [14, 11, 13, 4]                                         # red, blue, green, yellow
RISES = {"<": "w", ">": "e", "^": "n", "v": "s"}
C = P.cells()
TEAM_IDS = [t[0] for t in P.TEAMS]


def to_cell(kind, level, d):
    if kind in ("void", "gap", "water"):
        return Cell(kind)
    if kind == "stair":
        return Cell("stair", P.LEVEL[level], rises=RISES[d])
    return Cell(kind, P.LEVEL[level])


cells = {c: to_cell(k, lv, d) for c, (k, lv, d, team) in C.items()}
team_of = {c: TEAM_IDS.index(team) for c, (k, lv, d, team) in C.items()}
w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=64)
rng = random.Random(f"{P.BOARD}/ground")
red = [c for c, t in team_of.items() if t == 0]

# 1. red's quadrant: the ground, the keep's marks and its house
build(w, cells, only=red, rng=rng, dye=DYES[0],                # birches on the back levels, open grass
      fill=lambda piece, cs: "grass" if cs[piece[0]].y < P.LEVEL[3] else None)  # toward the middle
kx0, kz0, kx1, kz1 = P.keep_box(0)
for x in range(kx0, kx1 + 1):                                  # the team's wool along the keep's two inner edges
    w.set(x, P.LEVEL[5], kz1, B.WOOL, DYES[0])
for z in range(kz0, kz1 + 1):
    w.set(kx1, P.LEVEL[5], z, B.WOOL, DYES[0])
sx, sz = P.spawn_cell(0)
for y in range(P.LEVEL[5] + 22, P.LEVEL[5] + 25):              # the stack floating over the spawn
    w.set(sx, y, sz, B.WOOL, DYES[0])
# the keep's house, stacked of whole cells in the keep's outer corner, two by two over the spawn: an L of the
# three outer cells over it, and the corner cell on top with a beacon under the team's glass; its doors open from
# the spawn's cell east and south onto the keep's yard and its two stairs
c0 = -P.N
HOUSE = [[(c0, c0), (c0 + 1, c0), (c0, c0 + 1), (c0 + 1, c0 + 1)], [(c0, c0), (c0 + 1, c0), (c0, c0 + 1)], [(c0, c0)]]
for x in range(c0 * CELL, (c0 + 2) * CELL):
    for z in range(c0 * CELL, (c0 + 2) * CELL):
        for y in range(P.LEVEL[5] + 1, P.LEVEL[5] + 20):
            w.set(x, y, z, B.AIR)
house(w, HOUSE, P.LEVEL[5], DYES[0], door=[((c0 + 1, c0 + 1), "e"), ((c0 + 1, c0 + 1), "s")], cobwebs=False,
      floor_block=None)

# 2. the other three: each the last turned a quarter clockwise, its colours moved on a team
X, Z = w.grid()
for k in range(1, 4):
    mask = np.zeros((w.sx, w.sz), bool)
    for (cx, cz), t in team_of.items():
        if t == k - 1:
            mask[cx * CELL - w.x0:(cx + 1) * CELL - w.x0, cz * CELL - w.z0:(cz + 1) * CELL - w.z0] = True
    a, b = DYES[k - 1], DYES[k]
    turn_world(w, "cw", mask, recolour={(B.WOOL, a): (B.WOOL, b), (B.STAINED_CLAY, a): (B.STAINED_CLAY, b),
                                         (B.STAINED_PANE, a): (B.STAINED_PANE, b),
                                         (B.STAINED_GLASS, a): (B.STAINED_GLASS, b), (B.CARPET, a): (B.CARPET, b)})

# 3. the hills' pads, cleared over; the spawners' marks
for hid, name, (x0, z0, x1, z1), points, hy in P.HILLS:
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            for y in range(hy + 1, hy + 10):
                w.set(x, y, z, B.AIR)
            w.set(x, hy, z, B.STAINED_CLAY, 0)
for (px, pz), y in [(p, P.LEVEL[2]) for p in P.APPLES] + [(p, P.LEVEL[0]) for p in P.ARROWS]:
    for x in (int(np.floor(px)), int(np.ceil(px))):
        for z in (int(np.floor(pz)), int(np.ceil(pz))):
            for yy in range(y + 1, y + 4):
                w.set(x, yy, z, B.AIR)
            w.set(x, y, z, B.SANDSTONE, 1)

P.objectives().stamp(w)
w.save(sys.argv[1], "Brittlebush KotH", (0, 40, 0))
print(f"saved: {int(np.count_nonzero(w.ids))} blocks, {len(w.tiles)} tile entities")
