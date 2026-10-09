"""Generate Claywork from the plan: red's half block for block, then blue's as its mirror (pgmvox.orient.turn_world,
red's stained clay recoloured blue), then the objectives stamped for both teams.

    python3 gen.py <build-dir>

Every column of land is laid the same way, from the top down:

    the surface     one block, painted by the piece it belongs to: a checker of three-by-three paces in clay, stone
                    and double stone slab, each level its own pair, a stone-brick border on every edge
    the ground      eleven more blocks: stone, with andesite and gravel through it
    the base        two of bedrock, then a band of the team's stained clay on the faces, then bedrock to y 1,
                    broken on the faces by a lattice of obsidian and black wool
    y 0             block 36 under every column of land and every build zone: building is allowed only over it

Then what stands on the ground: the broad steps' stair nosings, the arrows, the arches, the parapets, the Kilns,
the Gatehouse's walls, the statues and the Rostrum's column, the bedrock walls; and what is cut into it: the
Undercroft, its well, the balconies and the ladders.
"""
import sys

import numpy as np

import plan as P
from pgmvox import B, World, rng
from pgmvox.orient import ladder, stair, turn_world

R = P.plan()
U = R.storeys[1]
w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=64)
r = rng(P.BOARD, "ground")
VOID = R.kinds["void"]
X, Z = w.grid()
RED = 14                                        # red stained clay; the mirror recolours it blue (11)

# the surface pairs, level by level: (a, b) for the checker's two paces
CLAY, STONE, DSLAB, SMOOTH = (B.CLAY, 0), (B.STONE, 0), (B.DSLAB, 0), (B.DSLAB, 8)
BRICK, ANDESITE = (B.STONEBRICK, 0), (B.STONE, 6)
PAIRS = {"front": (CLAY, STONE), "apron": (CLAY, STONE), "steps": (BRICK, BRICK),
         "hub": (STONE, CLAY), "wing": (STONE, CLAY), "rostrum": (DSLAB, STONE), "walk": (DSLAB, STONE),
         "neck": (BRICK, BRICK), "spawn": (DSLAB, CLAY), "terrace": (DSLAB, CLAY), "kiln": (SMOOTH, CLAY),
         "under": (BRICK, (B.STONEBRICK, 2)), "stone": (ANDESITE, ANDESITE)}


def red(x, z):
    return z < 0


def surface(x, z):
    """The column's top and its piece: the first storey over the Undercroft, else the ground floor before walls."""
    i, k = R.ix(x), R.iz(z)
    if U.K[i, k] != U.kinds["none"]:
        return int(U.H[i, k]), U.kind(x, z)
    return int(R.floor[i, k]), [n for n, v in R.kinds.items() if v == R.piece[i, k]][0]


land = R.piece != VOID
near_void = np.zeros(land.shape, bool)                        # land beside void: the faces and the borders
for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
    sh = np.roll(np.roll(~land, dx, 0), dz, 1)
    near_void |= land & sh
near_void[0, :] |= land[0, :]
near_void[-1, :] |= land[-1, :]


def paint(x, z, h, kind):
    """The top block of a column: the level's checker in three-by-three paces, stone brick on a piece's edge."""
    i, k = R.ix(x), R.iz(z)
    if near_void[i, k] and kind not in ("stone", "under"):
        return BRICK
    a, b = PAIRS.get(kind, (STONE, STONE))
    return a if ((x // 3) + (z // 3)) % 2 == 0 else b


def column(x, z):
    """Surface, ground, base and the block-36 marker for one column of land."""
    i, k = R.ix(x), R.iz(z)
    h, kind = surface(x, z)
    w.set(x, h, z, *paint(x, z, h, kind))
    for y in range(h - P.GROUND + 1, h):
        c = r.random()
        w.set(x, y, z, *((B.STONE, 5) if c < 0.12 else (B.GRAVEL, 0) if c < 0.15 else STONE))
    base = h - P.GROUND                                           # the top of the base: two of bedrock, the stripe
    for y in range(1, base + 1):
        w.set(x, y, z, B.BEDROCK)
    stripe = base - 2
    if near_void[i, k] and stripe >= 1:
        w.set(x, stripe, z, B.STAINED_CLAY, RED)                  # the team's band, flush with the face
        for y in range(1, stripe):                                # the lattice on the faces below the stripe
            u = x + z
            if (u + y) % 8 == 0:
                w.set(x, y, z, B.OBSIDIAN)
            elif (u - y) % 8 == 0:
                w.set(x, y, z, B.WOOL, 15)
    w.set(x, 0, z, 36)


# 1. the land of red's half, and block 36 under the build zones
for i, k in np.argwhere(land):
    x, z = int(X[i, k]), int(Z[i, k])
    if red(x, z):
        column(x, z)
zones = P.band_mask(R)
for i, k in np.argwhere(zones):
    if red(int(X[i, k]), int(Z[i, k])):
        w.ids[i, 0, k] = 36

# 2. the broad steps' nosings: a stone-brick stair on the lower tread's last row before each rise
for i, k in np.argwhere(land):
    x, z = int(X[i, k]), int(Z[i, k])
    if not red(x, z) or R.kind(x, z) not in ("steps", "neck", "walk"):
        continue
    h = int(R.floor[i, k])
    for dx, dz, d in ((0, -1, "n"), (0, 1, "s")):
        a, b = x + dx, z + dz
        if R.inside(a, b) and R.kind(a, b) in ("steps", "neck", "walk", "hub", "spawn", "kiln", "front", "apron") \
                and int(R.floor[R.ix(a), R.iz(b)]) == h + 1:
            w.set(x, h + 1, z, B.STONEBRICK_STAIRS, stair(d))

# 3. arrows set into the surface, in quartz, pointing the way forward (a chevron five wide and two deep)


def arrow(cx, cz, d):
    dx, dz = {"n": (0, -1), "s": (0, 1), "e": (1, 0), "w": (-1, 0)}[d]
    px, pz = -dz, dx
    for s in range(-2, 3):
        for t in (0, 1):
            ax, az = cx + dx * (t - abs(s)) + px * s, cz + dz * (t - abs(s)) + pz * s
            h, kind = surface(ax, az)
            if R.kind(ax, az) != "void" and kind not in ("steps", "neck"):
                w.set(ax, h, az, B.QUARTZ, 0)


for cx, cz, d in ((0, -86, "s"), (-24, -50, "w"), (-44, -56, "w"), (-66, -44, "n"), (-66, -60, "n"),
                  (-23, -24, "n"), (-62, -22, "n"), (0, -22, "s")):
    arrow(cx, cz, d)
    arrow(P.mx(cx), cz, {"w": "e", "e": "w"}.get(d, d))

# 4. the arches: stone-brick legs on the way's edges, a beam two high, upside-down stairs under its ends
for name, axis, (a, b), at in P.ARCHES:
    for sign in (1, -1):
        lo, hi = (a, b) if sign > 0 else (P.mx(b), P.mx(a))
        cells = [(s, at) if axis == "x" else (at, s) for s in range(lo, hi + 1)]
        floor = max(int(R.floor[R.ix(x), R.iz(z)]) if U.kind(x, z) == "none" else U.h(x, z) for x, z in cells)
        top = floor + P.ARCH_CLEAR + 1
        for n, (x, z) in enumerate(cells):
            if n in (0, len(cells) - 1):
                for y in range(int(R.floor[R.ix(x), R.iz(z)]) + 1 if U.kind(x, z) == "none" else U.h(x, z) + 1,
                               top + 2):
                    w.set(x, y, z, *BRICK)
            else:
                w.set(x, top, z, *BRICK)
                w.set(x, top + 1, z, B.SLAB, 5)
        for n, rise in ((1, "w" if axis == "x" else "n"), (len(cells) - 2, "e" if axis == "x" else "s")):
            x, z = cells[n]
            w.set(x, top - 1, z, B.STONEBRICK_STAIRS, stair({"w": "e", "e": "w", "n": "s", "s": "n"}[rise],
                                                            upside_down=True))

# 5. the parapets: two high of stone brick along the Statue Terraces and the Rostrum
for i, k in np.argwhere(R.mask("parapet")):
    x, z = int(X[i, k]), int(Z[i, k])
    if red(x, z):
        h = int(R.floor[i, k])
        w.set(x, h + 1, z, *BRICK)
        w.set(x, h + 2, z, B.SLAB, 5)

# 6. the bedrock walls across the Walks, three high
for i, k in np.argwhere(R.mask("barrier")):
    x, z = int(X[i, k]), int(Z[i, k])
    if red(x, z):
        for y in range(int(R.floor[i, k]) + 1, int(R.floor[i, k]) + P.WALL["height"] + 1):
            w.set(x, y, z, B.BEDROCK)

# 7. the Kilns: clay walls with stone-brick corners, a double-slab roof with glowstone, a door framed in red,
# the wool on the floor (stamped with the objectives) and two chests of gear against the back wall
for sign in (1, -1):
    x0, z0, x1, z1 = P.KILN
    d0, d1 = P.KILN_DOOR
    if sign < 0:
        x0, x1, d0, d1 = P.mx(x1), P.mx(x0), P.mx(d1), P.mx(d0)
    top = P.WOOL + P.ROOM_H
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            ring = x in (x0, x1) or z in (z0, z1)
            corner = x in (x0, x1) and z in (z0, z1)
            if ring and not (z == z1 and d0 <= x <= d1):
                for y in range(P.WOOL + 1, top):
                    w.set(x, y, z, *(BRICK if corner or y == top - 1 else CLAY))
            elif ring:                                           # the doorway: open four high, a red lintel over it
                for y in range(P.WOOL + 1, P.WOOL + 5):
                    w.set(x, y, z, B.AIR)
                for y in range(P.WOOL + 5, top):
                    w.set(x, y, z, B.STAINED_CLAY, RED)
            w.set(x, top, z, *((B.GLOWSTONE, 0) if (x - x0) % 4 == 2 and (z - z0) % 4 == 2 else DSLAB))
    for x in (d0 - 1, d1 + 1):                                    # the door's jambs in red
        for y in range(P.WOOL + 1, P.WOOL + 5):
            w.set(x, y, z1, B.STAINED_CLAY, RED)
    cx = (x0 + x1) // 2
    for x in (cx - 3, cx + 3):
        w.chest(x, P.WOOL + 1, z0 + 1, [(0, "minecraft:iron_chestplate", 1, 0), (1, "minecraft:iron_leggings", 1, 0),
                                       (2, "minecraft:golden_apple", 2, 0), (3, "minecraft:arrow", 32, 0)], facing=3)

# 8. the Gatehouse: walls round its back and sides five high with windows, posts at its front corners
x0, z0, x1, z1 = P.PIECE["spawn"][2]
for x in range(x0, x1 + 1):
    for z in range(z0, z1 + 1):
        if x in (x0, x1) or z == z0:
            for y in range(P.SPAWN + 1, P.SPAWN + 6):
                window = y in (P.SPAWN + 2, P.SPAWN + 3) and (x + z) % 4 == 0 and not (x in (x0, x1) and z == z0)
                w.set(x, y, z, *((B.IRON_BARS, 0) if window else BRICK if y == P.SPAWN + 5 else CLAY))
for x in (x0, x1):
    for y in range(P.SPAWN + 1, P.SPAWN + 7):
        w.set(x, y, z1, B.STAINED_CLAY, RED)

# 9. the statues on the Statue Terraces and the column on the Rostrum: a plinth, a quartz column, a lantern


def statue(cx, cz, floor, height):
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            w.set(cx + dx, floor + 1, cz + dz, *BRICK)
            w.set(cx + dx, floor + 2, cz + dz, B.SLAB, 5)
    for y in range(floor + 2, floor + 2 + height):
        w.set(cx, y, cz, B.QUARTZ, 2)
    w.set(cx, floor + 2 + height, cz, B.SEA_LANTERN)


for x, z in ((-11, -75), (10, -75)):
    statue(x, z, P.SPAWN, 4)
statue(-1, -35, P.HUB, 6)
statue(0, -35, P.HUB, 6)

# 10. the Undercroft: the passage carved under the Court and the Arcades, lit; the well's floor with a pool in it
# to break the fall; the ladders up the Walks' faces
for i, k in np.argwhere(R.mask("under")):
    x, z = int(X[i, k]), int(Z[i, k])
    if not red(x, z):
        continue
    for y in range(P.UNDER + 1, P.HUB):
        w.set(x, y, z, B.AIR)
    w.set(x, P.UNDER, z, *paint(x, z, P.UNDER, "under"))
    if U.kind(x, z) != "none" and x % 6 == 0:                     # a light in the passage's back wall
        w.set(x, P.UNDER + 2, P.PASSAGE[3] + 1, B.GLOWSTONE)
hx0, hz0, hx1, hz1 = P.HOLE
for x in range(hx0 + 4, hx1 - 3):
    for z in range(hz0 + 4, hz1 - 3):
        w.set(x, P.UNDER, z, B.WATER)                             # a pool, the drop's landing
lx, lz = P.LADDER
for x, side in ((lx, "w"), (P.mx(lx), "e")):
    for y in range(P.UNDER + 1, P.HUB + 1):
        w.set(x, y, lz, B.LADDER, ladder(side))

# 11. blue's half: red's in a mirror, its stained clay blue; then the objectives for both
turn_world(w, "mirror_z", Z < 0, recolour={(B.STAINED_CLAY, RED): (B.STAINED_CLAY, 11)})
P.objectives().stamp(w)
w.save(sys.argv[1], "Claywork", (0, 50, 0))
print(f"saved: {int(np.count_nonzero(w.ids))} blocks, {len(w.tiles)} tile entities")
