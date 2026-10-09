"""Generate Claywork from the plan: red's half block for block, then blue's as its mirror (pgmvox.orient.turn_world,
red's stained clay recoloured blue), then the objectives stamped for both teams.

    python3 gen.py <build-dir>

Every column of land is laid the same way, from the top down:

    the surface     one block, painted by the piece it belongs to: a checker of three-by-three paces in clay, stone
                    and double stone slab, each level its own pair, a stone-brick border on every edge
    the ground      eleven more blocks: stone, with andesite and gravel through it; on a face over the void,
                    dressed stone: a cornice, sunk panels of the team's stained clay with a quartz diamond between
                    stone-brick pilasters, and a plinth of polished andesite
    the base        two of bedrock, then a band of the team's stained clay on the faces, then bedrock to y 1,
                    broken on the faces by a lattice of obsidian and black wool
    y 0             block 36 under every column of land and every build zone: building is allowed only over it

Then what stands on the ground: the broad steps' stair nosings, the arrows in the team's wool, the arches, the
parapets, the bedrock walls (bedrock to the floor of the world) with their defence chests, the Kilns with their roofs,
chimneys and gear, the Gatehouse's walls, its iron and its spawn carpet, the statues; and what is cut into it: the
Undercroft, its well and pool, the balconies and the ladders.
"""
import sys

import numpy as np

import plan as P
from pgmvox import B, World, rng
from pgmvox.props import DEFENCE, ROOM_GEAR, laid
from pgmvox.objectives import Wool
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


def inside(x, z):
    return P.X_MIN <= x <= P.X_MAX and P.Z_MIN <= z <= P.Z_MAX


def is_land(x, z):
    return inside(x, z) and land[R.ix(x), R.iz(z)]


def normal(x, z):
    """The one side of a face cell that looks onto the void, or None at a corner or inside the land."""
    out = [(dx, dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)) if not is_land(x + dx, z + dz)]
    return out[0] if len(out) == 1 else None


PANEL, PILASTER = 6, 2                                            # a face's bay: a sunk panel, then a pilaster
BAY = PANEL + PILASTER


def bay(x, z, h, n):
    """Where a face cell falls in its run of face at one height: 'pilaster', 'panel' with the panel's column
    (0..PANEL-1), or 'ashlar' in a run too short for a bay or past the last one. The bays are centred on the run."""
    ax, az = -n[1], n[0]                                          # along the face
    i0, i1 = 0, 0
    while True:
        a, b = x - ax * (i0 + 1), z - az * (i0 + 1)
        if normal(a, b) != n or surface(a, b)[0] != h or U.kind(a, b) != "none":
            break
        i0 += 1
    while True:
        a, b = x + ax * (i1 + 1), z + az * (i1 + 1)
        if normal(a, b) != n or surface(a, b)[0] != h or U.kind(a, b) != "none":
            break
        i1 += 1
    length, pos = i0 + i1 + 1, i0
    bays = (length - PILASTER) // BAY
    if bays < 1:
        return "ashlar", 0
    q = pos - (length - (bays * BAY + PILASTER)) // 2
    if q < 0 or q >= bays * BAY + PILASTER:
        return "ashlar", 0
    if q % BAY < PILASTER:
        return "pilaster", 0
    return "panel", q % BAY - PILASTER


DIAMOND = {(a, b) for a in range(PANEL) for b in range(5) if abs(a - (PANEL - 1) / 2) + abs(b - 2) <= 1.5}


def dress(x, z, h):
    """A face over the void, under the surface: a cornice, a frame, a panel sunk one block between pilasters with
    the team's clay and a quartz diamond at its back, and a plinth; the lattice and the stripe below are the base's."""
    n = normal(x, z)
    if n is None or U.kind(x, z) != "none" or not is_land(x - n[0], z - n[1]):
        kind = "pilaster"
    else:
        kind, col = bay(x, z, h, n)
    for y in range(h - P.GROUND + 1, h):
        d = h - y                                                  # 1 the cornice .. 11 the plinth's foot
        if d >= 9:
            w.set(x, y, z, *ANDESITE)
        elif kind == "pilaster":
            w.set(x, y, z, B.STONEBRICK, 3 if d in (2, 8) else 0)
        elif kind == "panel" and 3 <= d <= 7:
            w.set(x, y, z, B.AIR)
            back = (B.QUARTZ, 1) if (col, d - 3) in DIAMOND else (B.STAINED_CLAY, RED)
            w.set(x - n[0], y, z - n[1], *back)
        else:
            w.set(x, y, z, B.STONEBRICK, 2 if r.random() < 0.08 else 0)


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
for i, k in np.argwhere(near_void):
    x, z = int(X[i, k]), int(Z[i, k])
    h, kind = surface(x, z)
    if red(x, z) and kind not in ("stone",):
        dress(x, z, h)
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

# 3. arrows set into the surface in the team's wool (a truer blue than blue clay), pointing the way forward: a chevron three deep, centred on its
# lane (a lane an even number wide has its centre between two blocks, and the chevron is six wide there, else five)


def arrow(cx, cz, d):
    dx, dz = {"n": (0, -1), "s": (0, 1), "e": (1, 0), "w": (-1, 0)}[d]
    across = cx if dx == 0 else cz
    half = 0.5 if across != int(across) else 0.0
    offsets = [s + half for s in range(-3 if half else -2, 3)]
    for s in offsets:
        for t in (0, 1):
            back = t - int(abs(s))
            if dx == 0:                                          # across + s is whole: both are halves or neither
                ax, az = round(cx + s), round(cz + dz * back)
            else:
                ax, az = round(cx + dx * back), round(cz + s)
            if not is_land(ax, az):
                continue
            h, kind = surface(ax, az)
            if kind not in ("steps", "neck"):
                w.set(ax, h, az, B.WOOL, RED)


ARROWS = [(-0.5, -87, "s"),                      # the Gatehouse, down the Spawn Steps
          (-27, -58.5, "w"), (-41, -58.5, "w"),  # the Court and the Arcade, out to the Walk
          (-66.5, -44, "n"), (-66.5, -57, "n"),  # up the Walk to the wall and the Kiln
          (-23.5, -24, "n"),                     # the Forecourt to the Grand Steps' flight
          (-66.5, -22, "n"),                     # the Apron, into the Walk
          (-0.5, -22, "s")]                      # the Forecourt, toward the band
for cx, cz, d in ARROWS:
    arrow(cx, cz, d)
    if P.mx(cx) != cx:
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

# 6. the bedrock walls across the Walks, three over the floor and bedrock all the way down to the world's floor, so
# nothing tunnels under them; two defence chests set into the face the Kiln's side looks at
for i, k in np.argwhere(R.mask("barrier")):
    x, z = int(X[i, k]), int(Z[i, k])
    if red(x, z):
        for y in range(1, int(R.floor[i, k]) + P.WALL["height"] + 1):
            w.set(x, y, z, B.BEDROCK)
for x0, x1 in ((P.WALL["x0"], P.WALL["x1"]), (P.mx(P.WALL["x1"]), P.mx(P.WALL["x0"]))):
    lane = x1 - x0 + 1
    face = P.WALL["z0"]                                              # the north face, toward the Kiln
    stand = int(R.floor[R.ix(x0), R.iz(face - 1)]) + 1               # where a defender stands before it
    for n in (1, 2):
        cx = x0 + n * lane // 3
        w.chest(cx, stand, face, laid(DEFENCE), facing=2)
        w.set(cx, stand + 1, face, B.AIR)                            # room for the lid; the column behind is bedrock

# 7. the Kilns: a brick hall on a stone-brick plinth, pilasters every four with windows of iron between them on the
# faces over the void, a frieze of the team's clay, a cornice, a hipped roof of brick stairs, a chimney with embers
# at its top; inside, the wool on a dais, lamps in the pilasters, and two chests of gear against the back wall


def kiln(x0, z0, x1, z1, d0, d1):
    top = P.WOOL + P.ROOM_H                                          # the cornice course
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            ring = x in (x0, x1) or z in (z0, z1)
            if not ring:
                continue
            along = (z - z0) if x in (x0, x1) else (x - x0)
            corner = x in (x0, x1) and z in (z0, z1)
            pilaster = corner or along % 4 == 0
            door = z == z1 and d0 <= x <= d1
            for y in range(P.WOOL + 1, top):
                v = y - P.WOOL                                       # 1 the plinth .. ROOM_H-1 the frieze
                if door and v <= 4:
                    b = (B.AIR, 0)
                elif door:
                    b = (B.STAINED_CLAY, RED)                        # the lintel
                elif v == 1:
                    b = BRICK
                elif pilaster:
                    b = (B.GLOWSTONE, 0) if v == 3 and not corner else (B.STONEBRICK, 3 if v == P.ROOM_H - 1 else 0)
                elif v == P.ROOM_H - 1:
                    b = (B.STAINED_CLAY, RED)                        # the frieze
                elif v in (2, 3) and along % 4 == 2 and z != z1:
                    b = (B.IRON_BARS, 0)                             # a window, on the three faces over the void
                else:
                    b = (B.BRICK, 0)
                w.set(x, y, z, *b)
            w.set(x, top, z, *BRICK)                                 # the cornice
    for x in (d0 - 1, d1 + 1):                                       # the door's jambs in the team's clay
        for y in range(P.WOOL + 1, P.WOOL + 5):
            w.set(x, y, z1, B.STAINED_CLAY, RED)
    w.set(d0, P.WOOL + 4, z1, B.STONEBRICK_STAIRS, stair("e", upside_down=True))
    w.set(d1, P.WOOL + 4, z1, B.STONEBRICK_STAIRS, stair("w", upside_down=True))
    for x in range(x0 + 1, x1):                                      # the ceiling's lamps hang under the roof
        for z in range(z0 + 1, z1):
            if (x - x0) % 4 == 2 and (z - z0) % 4 == 2:
                w.set(x, top, z, B.GLOWSTONE)
            else:
                w.set(x, top, z, B.AIR)
    # the hipped roof: a ring of brick stairs a course, each one in from the last, rising to a ridge
    k = 0
    while x0 + k <= x1 - k and z0 + k <= z1 - k:
        y = top + 1 + k
        a0, a1, b0, b1 = x0 + k, x1 - k, z0 + k, z1 - k
        for x in range(a0, a1 + 1):
            for z in range(b0, b1 + 1):
                edge = [d for d, on in (("e", x == a0), ("w", x == a1), ("s", z == b0), ("n", z == b1)) if on]
                if not edge:
                    continue
                if a1 - a0 <= 1:                                     # the ridge: two stairs back to back
                    w.set(x, y, z, B.BRICK_STAIRS, stair("e" if x == a0 else "w"))
                elif b1 - b0 <= 1:
                    w.set(x, y, z, B.BRICK_STAIRS, stair("s" if z == b0 else "n"))
                else:
                    w.set(x, y, z, B.BRICK_STAIRS, stair(edge[0]))
        k += 1
    # the chimney, at the back, four by four and hollow, its top a ring of stone brick over embers
    cx = (x0 + x1) // 2
    for x in range(cx - 1, cx + 3):
        for z in range(z0 + 2, z0 + 6):
            shell = x in (cx - 1, cx + 2) or z in (z0 + 2, z0 + 5)
            for y in range(top + 1, P.MAX_BUILD + 1):
                if shell:
                    w.set(x, y, z, *(BRICK if y >= P.MAX_BUILD - 1 else (B.BRICK, 0)))
                elif y == P.MAX_BUILD - 1:
                    w.set(x, y, z, B.GLOWSTONE)
                else:
                    w.set(x, y, z, B.AIR)
    # the gear: two chests against the back wall, either side of the middle
    for x in (cx - 3, cx + 4):
        w.chest(x, P.WOOL + 1, z0 + 1, laid(ROOM_GEAR), facing=3)


x0, z0, x1, z1 = P.KILN
d0, d1 = P.KILN_DOOR
kiln(x0, z0, x1, z1, d0, d1)
kiln(P.mx(x1), z0, P.mx(x0), z1, P.mx(d1), P.mx(d0))
for o in P.objectives().of(Wool):                                    # the wool's dais: chiseled stone brick
    fx, fy, fz = o.found
    if fz < 0:
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                w.set(fx + dx, fy - 1, fz + dz, *((B.QUARTZ, 1) if (dx, dz) == (0, 0) else (B.STONEBRICK, 3)))

# 8. the Gatehouse, open to the sky: walls round its back and sides on a plinth, stone-brick pilasters every four
# with lamps, clay between them and windows of iron, a frieze of the team's clay, a cornice and battlements; posts in
# the team's clay at its front corners; two cubes of iron, which grow back; the team's carpet where they spawn
x0, z0, x1, z1 = P.PIECE["spawn"][2]
for x in range(x0, x1 + 1):
    for z in range(z0, z1 + 1):
        if not (x in (x0, x1) or z == z0):
            continue
        along = (z - z0) if x in (x0, x1) else (x - x0)
        corner = x in (x0, x1) and z == z0
        pilaster = corner or along % 4 == 0 or (x in (x0, x1) and z == z1)
        for y in range(P.SPAWN + 1, P.SPAWN + 8):
            v = y - P.SPAWN
            if v == 1:
                b = BRICK
            elif v == 7:
                b = BRICK if (x + z) % 2 == 0 or pilaster else (B.AIR, 0)    # battlements
            elif v == 6:
                b = BRICK
            elif pilaster:
                b = (B.SEA_LANTERN, 0) if v == 4 and not corner else (B.STONEBRICK, 3 if v == 5 else 0)
            elif v == 5:
                b = (B.STAINED_CLAY, RED)
            elif v in (2, 3) and along % 4 == 2:
                b = (B.IRON_BARS, 0)
            else:
                b = CLAY
            w.set(x, y, z, *b)
for x in (x0, x1):                                                   # the front posts
    for y in range(P.SPAWN + 1, P.SPAWN + 8):
        w.set(x, y, z1, B.STAINED_CLAY, RED)
    w.set(x, P.SPAWN + 8, z1, B.SEA_LANTERN)
for ix0, iz0 in P.IRON:
    for a in (ix0, P.mx(ix0 + P.IRON_SPAN - 1)):
        for x in range(a, a + P.IRON_SPAN):
            for z in range(iz0, iz0 + P.IRON_SPAN):
                for y in range(P.SPAWN + 1, P.SPAWN + 1 + P.IRON_SPAN):
                    w.set(x, y, z, B.IRON_BLOCK)
sx, sy, sz = P.SPAWN_AT
for x in range(sx - 3, sx + 3):                                      # six by five, the team's colour, a white heart
    for z in range(sz - 2, sz + 3):
        w.set(x, sy, z, B.CARPET, 0 if (x in (sx - 1, sx) and z == sz) else RED)

# 9. the statues: a figure on a plinth, facing the way forward, its belt, crest and plinth's top in the team's clay,
# lamps at the plinth's corners; one on each Statue Terrace and one on the Rostrum


def statue(c0, c1, cz, floor):
    """A figure whose middle is the columns c0..c1 (one or two), standing at z cz on the floor at floor."""
    for x in range(c0 - 2, c1 + 3):
        for z in range(cz - 2, cz + 3):
            corner = x in (c0 - 2, c1 + 2) and z in (cz - 2, cz + 2)
            w.set(x, floor + 1, z, *((B.SEA_LANTERN, 0) if corner else BRICK))
            edge = x in (c0 - 2, c1 + 2) or z in (cz - 2, cz + 2)
            w.set(x, floor + 2, z, *((B.SLAB, 5) if edge else (B.STAINED_CLAY, RED)))
    f = floor + 3
    for v in range(3):                                               # the legs
        for x in (c0 - 1, c1 + 1):
            w.set(x, f + v, cz, B.QUARTZ, 2)
    for x in range(c0 - 1, c1 + 2):                                  # the belt
        w.set(x, f + 3, cz, B.STAINED_CLAY, RED)
    for v in range(4, 7):                                            # the body, two deep
        for x in range(c0 - 1, c1 + 2):
            for z in (cz - 1, cz):
                w.set(x, f + v, z, B.QUARTZ, 0)
    for v in range(3, 7):                                            # the arms
        for x in (c0 - 2, c1 + 2):
            w.set(x, f + v, cz, B.QUARTZ, 2)
    head = (c0 - 1, c1 + 1) if c0 == c1 else (c0, c1)                # three wide over a body of three, else two
    for v in range(7, 9):                                            # the head
        for x in range(head[0], head[1] + 1):
            for z in (cz - 1, cz):
                w.set(x, f + v, z, B.QUARTZ, 1)
    for x in range(c0, c1 + 1):                                      # a crest on the helm in the team's clay
        for z in (cz - 1, cz):
            w.set(x, f + 9, z, B.STAINED_CLAY, RED)


for x, z in ((-11, -75),):
    statue(x, x, z, P.SPAWN)
    statue(P.mx(x), P.mx(x), z, P.SPAWN)
statue(-1, 0, -35, P.HUB)

# 10. the Undercroft: the passage carved three high under the Court and the Arcades, a roof three thick over it, lit;
# the well's floor a pool to land in; the ladders up the Walks' faces
for i, k in np.argwhere(R.mask("under")):
    x, z = int(X[i, k]), int(Z[i, k])
    if not red(x, z):
        continue
    for y in range(P.UNDER + 1, P.UNDER + 1 + P.UNDER_CLEAR):
        w.set(x, y, z, B.AIR)
    for y in range(P.UNDER + 1 + P.UNDER_CLEAR, P.HUB):              # the roof: no gravel over the passage
        if w.get(x, y, z)[0] == B.GRAVEL:
            w.set(x, y, z, *STONE)
    w.set(x, P.UNDER, z, *paint(x, z, P.UNDER, "under"))
    if U.kind(x, z) != "none" and x % 6 == 0:                     # a light in the passage's back wall
        w.set(x, P.UNDER + 2, P.PASSAGE[3] + 1, B.GLOWSTONE)
hx0, hz0, hx1, hz1 = P.HOLE
for x in range(hx0 + 1, hx1):
    for z in range(hz0 + 1, hz1):
        w.set(x, P.UNDER, z, B.WATER)                             # the pool, the drop's landing
        w.set(x, P.UNDER - 1, z, *BRICK)
lx, lz = P.LADDER
for x, side in ((lx, "w"), (P.mx(lx), "e")):
    for y in range(P.UNDER + 1, P.HUB + 1):
        w.set(x, y, lz, B.LADDER, ladder(side))

# 11. blue's half: red's in a mirror, its stained clay blue; then the objectives for both
turn_world(w, "mirror_z", Z < 0, recolour={(B.STAINED_CLAY, RED): (B.STAINED_CLAY, 11), (B.CARPET, RED): (B.CARPET, 11),
                                             (B.WOOL, RED): (B.WOOL, 11)})
P.objectives().stamp(w)
w.save(sys.argv[1], "Claywork", (0, 50, 0))
print(f"saved: {int(np.count_nonzero(w.ids))} blocks, {len(w.tiles)} tile entities")
