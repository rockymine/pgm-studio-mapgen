"""Generate Sandreach: red's half, made and grown, then blue's as its half turn; then the objectives.

    python3 gen.py <build-dir>

    the made        every cell of the blueprint in Brittlebush's grammar (pgmvox.brittle on pgmvox.grammar), read
                    against the grown ground beside it: a face is as deep as the drop to the meadow under it, and
                    a made edge level with grown ground is a seam; the spawn's and the wool's houses stacked of
                    whole cells, the wool on a square of its colour, the redstone line before its door
    the grown       the meadow and the island, painted by their slope: grass on the gentle ground, coarse dirt where
                    it steepens, sandstone where it is a face; two courses of dirt under the grass, then sandstone
                    in beds; an underside hanging under every column, deepest inland, flush against the made ground
                    where the meadow meets it; acacias to the outside of each, none where a player lands or leaves
"""
import random
import sys

import numpy as np

import plan as P
from pgmvox import B, World, props, terrain, trees
from pgmvox.brittle import CELL, build, house
from pgmvox.orient import turn_world
from pgmvox.shapes import edge_depth

cells, team = P.cells()
X, Z = P.grid()
w = World(P.X_MIN, P.Z_MIN, X.shape[0], X.shape[1], sy=64)
rng = random.Random(f"{P.BOARD}/ground")
red = [c for c, t in team.items() if t == 0]

# the grown ground, red's: the meadow and the island, kept out of the made
made = P.made_mask(X, Z, cells)
m1, H1 = P.meadow(X, Z, cells)
m2, H2 = P.island(X, Z)
m2 &= ~made
GROWN = m1 | m2
H = np.where(m1, H1, np.where(m2, H2, -1))
grown = {(int(X[i, k]), int(Z[i, k])): int(H[i, k]) for i, k in np.argwhere(GROWN)}

# 1. the made: the blueprint, read against the grown beside it
build(w, cells, only=red, rng=rng, dye=P.DYES[0], fill=P.fill, grown=grown)
wx0, wz0, wx1, wz1 = P.WOOL_BOX
for x in range(wx0, wx1 + 1):
    for z in range(wz0, wz1 + 1):
        for y in range(P.WOOL + 1, P.WOOL + 20):
            w.set(x, y, z, B.AIR)
cx, cz = wx0 // CELL, wz0 // CELL
house(w, [[(cx, cz), (cx + 1, cz), (cx, cz + 1), (cx + 1, cz + 1)], [(cx, cz), (cx + 1, cz), (cx, cz + 1)],
          [(cx + 1, cz)]], P.WOOL, 4, door=((cx + 1, cz + 1), "s"))         # red keeps the yellow wool
props.wool_chests(w, (cx * CELL + 1, cz * CELL + 1, (cx + 2) * CELL - 2, (cz + 2) * CELL - 2), P.WOOL, "s")
fx, _, fz = P.WOOL_AT
for x in range(fx - 1, fx + 2):
    for z in range(fz - 1, fz + 2):
        w.set(x, P.WOOL, z, B.WOOL, 4)
for x in range(wx0, wx1 + 1):                                             # the redstone line before its door
    w.set(x, P.WOOL + 1, wz1 + 1, *((B.REDSTONE_TORCH, 5) if x in (wx0, wx1) else (B.REDSTONE_WIRE, 15)))
sx0, sz0, sx1, sz1 = P.SPAWN_BOX
for x in range(sx0, sx1 + 1):
    for z in range(sz0, sz1 + 1):
        for y in range(P.YARD + 1, P.YARD + 20):
            w.set(x, y, z, B.AIR)
kx, kz = sx0 // CELL, sz0 // CELL
house(w, [[(kx, kz), (kx + 1, kz), (kx, kz + 1), (kx + 1, kz + 1)], [(kx, kz), (kx + 1, kz)], [(kx, kz)]],
      P.YARD, P.DYES[0], door=[((kx, kz + 1), "s"), ((kx + 1, kz + 1), "s")], cobwebs=False, floor_block=None)
mx, my, mz = P.SPAWN_AT
for y in range(P.YARD + 22, P.YARD + 25):                                # the team's wool floating over the spawn
    w.set(mx, y, mz, B.WOOL, P.DYES[0])

# 2. the grown: painted by slope, soil then sandstone in beds, an underside hanging under it
deg = terrain.slope_deg(np.where(GROWN, H, 0).astype(float), GROWN)
hang = terrain.root_depth(GROWN | made, cone=2.6, flutes=3, spires=9, seed=5)       # deep where it meets the made
ed = edge_depth(GROWN)
for i, k in np.argwhere(GROWN):
    h, d = int(H[i, k]), float(deg[i, k])
    bottom = max(1, h - int(hang[i, k]) - 2)
    soil = 0 if d > 38 else 1 if d > 28 else 2
    for y in range(bottom, h):
        if y >= h - soil:
            w.ids[i, y, k], w.dat[i, y, k] = B.DIRT, 0
        else:                                                              # sandstone in beds a few thick
            band = (y + int(X[i, k]) // 23) % 7
            w.ids[i, y, k], w.dat[i, y, k] = (B.SANDSTONE, 2) if band == 0 else (B.SANDSTONE, 0)
    w.ids[i, 0, k] = 36
    if d > 38:
        top = (B.SANDSTONE, 0)
    elif d > 28 or (ed[i, k] <= 1 and d > 18):
        top = (B.DIRT, 1)
    else:
        top = (B.GRASS, 0)
    w.ids[i, h, k], w.dat[i, h, k] = top
    if top == (B.GRASS, 0) and ed[i, k] >= 2:                               # sparse cover, a few flowers
        c = rng.random()
        if c < 0.06:
            w.set(int(X[i, k]), h + 1, int(Z[i, k]), B.TALLGRASS, 1)
        elif c < 0.07:
            w.set(int(X[i, k]), h + 1, int(Z[i, k]), B.FLOWER, 2)
        elif c < 0.08:
            w.set(int(X[i, k]), h + 1, int(Z[i, k]), B.DEADBUSH)
    elif top == (B.DIRT, 1) and ed[i, k] >= 2 and rng.random() < 0.05:     # dry scrub on the coarse ground
        w.set(int(X[i, k]), h + 1, int(Z[i, k]), B.DEADBUSH)

# the emerald's plinth: smooth sandstone five by five under and round it, chiselled at the corners, clear over
ex, ez = P.EMERALD_AT
for x in range(ex - 3, ex + 4):
    for z in range(ez - 3, ez + 4):
        ring = max(abs(x - ex), abs(z - ez))
        if ring <= 2:
            corner = abs(x - ex) == 2 and abs(z - ez) == 2
            w.set(x, P.EMERALD_Y, z, B.SANDSTONE, 1 if corner else 2)
            for y in range(P.EMERALD_Y + 1, P.EMERALD_Y + 9):
                w.set(x, y, z, B.AIR)

# boulders on the grown ground: weathered lumps of sandstone and stone, sat into the grass, off the made faces, the
# stair's foot and the emerald's ground, a dozen blocks apart
def boulder(x, z, r):
    g = int(H[x - P.X_MIN, z - P.Z_MIN])
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            for dy in range(0, 3):
                if dx * dx + dz * dz + (dy * 1.6) ** 2 <= r * r + rng.random() * 1.2:
                    if not GROWN[x + dx - P.X_MIN, z + dz - P.Z_MIN]:
                        continue
                    gg = int(H[x + dx - P.X_MIN, z + dz - P.Z_MIN])
                    c = rng.random()
                    blk = (B.SANDSTONE, 0) if c < 0.45 else (B.STONE, 0) if c < 0.7 else (B.COBBLE, 0) if c < 0.85 \
                        else (B.MOSSY, 0)
                    w.set(x + dx, gg + dy, z + dz, *blk)
    return g


far = edge_depth(~made) > 6
spots = [(int(X[i, k]), int(Z[i, k])) for i, k in np.argwhere(GROWN & far & (ed >= 4)) if deg[i, k] < 25]
rng.shuffle(spots)
placed = []
for x, z in spots:
    if len(placed) >= 9:
        break
    if max(abs(x - ex), abs(z - ez)) < 9 or any(abs(x - a) + abs(z - b) < 14 for a, b in placed):
        continue
    fx0, fx1, fz0, fz1 = P.STAIR_FOOT
    if fx0 - 6 <= x <= fx1 + 6 and fz0 - 6 <= z <= fz1 + 6:
        continue
    boulder(x, z, 1.4 + rng.random() * 1.2)
    placed.append((x, z))
print(f"boulders: {len(placed)}")

# acacias to the outside of each grown piece: a handful, on gentle grass well in from the void, away from the made
# faces, off the meadow's southern brink and the island's sides that face the landing and the middle
lib = trees.kinds(trees.library())
far_made = edge_depth(~made) > 9
TREES = {"meadow": 5, "island": 2}
for name, mask, ok in (("meadow", m1, lambda x, z: z < -40), ("island", m2, lambda x, z: x < P.ISLAND[0] - 3)):
    sites = [(int(X[i, k]), int(Z[i, k])) for i, k in np.argwhere(mask & far_made & (ed >= 5) & (ed <= 10))
             if deg[i, k] < 20 and ok(int(X[i, k]), int(Z[i, k]))]
    rng.shuffle(sites)
    planted = []
    for x, z in sites:
        if len(planted) >= TREES[name]:
            break
        if any(abs(x - a) + abs(z - b) < 16 for a, b in planted) or max(abs(x - ex), abs(z - ez)) < 10 or \
                any(abs(x - a) + abs(z - b) < 6 for a, b in placed):
            continue
        t = lib["acacia"][rng.randrange(len(lib["acacia"]))]
        if trees.plant(w, x, z, t, turn=rng.randrange(4)):
            planted.append((x, z))

# 3. blue's half: red's turned a half about the middle, its colours moved on
turn_world(w, "half", Z < 0, recolour={(B.STAINED_CLAY, 14): (B.STAINED_CLAY, 11), (B.WOOL, 14): (B.WOOL, 11),
                                        (B.STAINED_GLASS, 14): (B.STAINED_GLASS, 11), (B.WOOL, 4): (B.WOOL, 1),
                                        (B.STAINED_GLASS, 4): (B.STAINED_GLASS, 1)})
P.objectives().stamp(w)
w.save(sys.argv[1], "Sandreach", (0, 50, 0))
print(f"saved: {int(np.count_nonzero(w.ids))} blocks, {len(w.tiles)} tile entities")
