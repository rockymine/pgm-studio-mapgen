"""Generate Claywork from the plan: red's half block for block, then blue's as its mirror (pgmvox.orient.turn_world,
red's stained clay recoloured blue), then the objectives stamped for both teams.

    python3 gen.py <build-dir>

The land is spoken in the grammar (pgmvox.grammar) in the Claywork style (pgmvox.clay): every piece cut into
sections about nine blocks a side, both wings alike, outlined and laid each in its own fill, its neighbours in
another; a face's inlaid bays centred on the sections over it; the flights of steps their own stepped sections; the
arrows laid into the sections they point out of. Under it all, twelve of ground, the team's band and the lattice on
the faces, bedrock to y 1, and block 36 under every column of land and every build zone.

Then what stands on the ground: the arches, the parapets, the bedrock walls (bedrock to the floor of the world) with
their defence chests, the Kilns with their roofs, chimneys and gear, the Gatehouse's walls, its iron and its spawn
carpet, the statues; and what is cut into it: the Undercroft, its well and pool, the balconies and the ladders.
"""
import sys

import numpy as np

import plan as P
from pgmvox import B, World, clay, rng
from pgmvox import grammar as Gm
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

CLAY, STONE, DSLAB, SMOOTH = clay.CLAY, clay.STONE, clay.DSLAB, clay.SMOOTH
BRICK, ANDESITE, DIORITE = clay.BRICK, clay.ANDESITE, clay.DIORITE


def red(x, z):
    return z < 0


def surface(x, z):
    """The column's top and its piece: the first storey over the Undercroft, else the ground floor before walls."""
    i, k = R.ix(x), R.iz(z)
    if U.K[i, k] != U.kinds["none"]:
        return int(U.H[i, k]), U.kind(x, z)
    return int(R.floor[i, k]), [n for n, v in R.kinds.items() if v == R.piece[i, k]][0]


land = R.piece != VOID
near_void = np.zeros(land.shape, bool)                        # land beside void: the faces and the band
for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
    sh = np.roll(np.roll(~land, dx, 0), dz, 1)
    near_void |= land & sh
near_void[0, :] |= land[0, :]
near_void[-1, :] |= land[-1, :]

# 1. the land of red's half in the grammar (pgmvox.grammar, spoken in pgmvox.clay): every piece cut into sections
# about nine blocks a side, both wings alike, each outlined and laid in its own fill; the flights of steps their
# own sections, stepped; the arrows laid into the section each points out of. A face's bays are centred on the
# sections over it, so the inlaid panels answer the floor's cut.
STYLE = clay.style(dye=RED, rng=r, faced=lambda x, z: bool(near_void[R.ix(x), R.iz(z)]))
CUT = {"front": (7, 2), "apron": (2, 2), "rostrum": (4, 1), "hub": (7, 3), "spawn": (3, 2), "terrace": (1, 1),
       "wing": (3, 1), "kiln": (1, 1)}
# a piece's sections alternate between two fills, like the cells of a checker, so neighbours never match
FILLS = {"front": ("paving", "squares"), "apron": ("squares", "inlay"), "rostrum": ("paving", "paving"),
         "hub": ("checker", "inlay"), "spawn": ("inlay", "squares"), "terrace": ("inlay", "inlay"),
         "wing": ("inlay", "squares"), "kiln": ("squares", "squares"), "walk": ("squares", "paving")}
ARROWS = [(-27, -58.5, "w"),                     # the Court, out toward the Arcade
          (-23.5, -24, "n"),                     # the Forecourt to the Grand Steps' flight
          (-0.5, -22, "s"),                      # the Forecourt, toward the band
          (-1, -85, "s"),                        # the Gatehouse's front, down the Spawn Steps
          (-41, -58, "w"),                       # the Arcade, out to the Walk
          (-66, -44, "n"), (-66, -58, "n"),      # up the Walk to the wall and the Kiln
          (-62, -22, "n")]                       # the Apron, toward the Walk
TOP = {}
for i, k in np.argwhere(land):
    x, z = int(X[i, k]), int(Z[i, k])
    if red(x, z):
        TOP[(x, z)] = surface(x, z)


def runs(cols):
    """A set of columns as boxes, a run along z in each column x."""
    out = []
    for x in sorted({c[0] for c in cols}):
        zs = sorted(z for a, z in cols if a == x)
        start = zs[0]
        for p, q in zip(zs, zs[1:] + [None]):
            if q != p + 1:
                out.append((x, start, x, p))
                start = q
    return tuple(out)


def mirrored(box):
    x0, z0, x1, z1 = box
    return P.mx(x1), z0, P.mx(x0), z1


SECS = []


def add(cols, y, name, fill=None, tags=(), tops=()):
    motifs = []
    for ax, az, d in ARROWS:
        for px, dd in ((int(np.floor(ax)), d), (P.mx(int(np.floor(ax))), {"w": "e", "e": "w"}.get(d, d))):
            if (px, int(np.floor(az))) in cols and not any(m[1] == (("d", dd),) for m in motifs):
                motifs.append(("arrow", (("d", dd),)))
                fill = "plate"
    SECS.append(Gm.Section(runs(cols), y, name, fill, frozenset(tags), tuple(motifs[:1]), tuple(tops)))


def flat_piece(key, box, h, nx, nz, fills):
    copies = [(box, False)] if box[0] <= -1 <= box[2] - 1 else [(box, False), (mirrored(box), True)]
    for b, mir in copies:
        xs, zs = Gm._cuts(b[0], b[2], nx), Gm._cuts(b[1], b[3], nz)
        for i, (a0, a1) in enumerate(xs):
            for j, (c0, c1) in enumerate(zs):
                cols = {(x, z) for x in range(a0, a1 + 1) for z in range(c0, c1 + 1) if TOP.get((x, z)) == (h, key)}
                if cols:
                    ii = nx - 1 - i if mir else i
                    add(cols, h, f"{key}-{ii}-{j}", fills[(ii + j) % 2])


def flight(key, box, rise):
    copies = [box] if box[0] <= -1 <= box[2] - 1 else [box, mirrored(box)]
    for b in copies:
        cols = {(x, z) for x in range(b[0], b[2] + 1) for z in range(b[1], b[3] + 1)
                if (x, z) in TOP and TOP[(x, z)][1] == key}
        tops = [((x, z), TOP[(x, z)][0]) for x, z in sorted(cols)]
        add(cols, min(h for _, h in tops), f"{key}-flight", "flight", tags=(f"rise-{rise}",), tops=tops)


for key, _, box, rule in P.PIECES:
    if key == "walk":
        for sub, rr in P.WALK_FLOORS:
            if isinstance(rr, tuple):
                flight("walk", sub, rr[4])
            else:
                flat_piece("walk", sub, rr, 1, 3, FILLS["walk"])
    elif isinstance(rule, tuple):
        flight(key, box, rule[4])
    else:
        flat_piece(key, box, rule, *CUT[key], FILLS[key])
for b, h in P.STONES:                                           # the stepping stones, plain
    for bb in (b, mirrored(b)):
        add({(x, z) for x in range(bb[0], bb[2] + 1) for z in range(bb[1], bb[3] + 1)}, h, "stone", "flat")
covered = {c for sec in SECS for c in sec.columns()}
left = {c for c in TOP if c not in covered}
for c in sorted(left):                                           # the well's floor and the landing: a checker
    if c in left:
        comp, todo = set(), [c]
        while todo:
            p = todo.pop()
            if p in comp or p not in left or TOP[p] != TOP[c]:
                continue
            comp.add(p)
            todo += [(p[0] + 1, p[1]), (p[0] - 1, p[1]), (p[0], p[1] + 1), (p[0], p[1] - 1)]
        left -= comp
        add(comp, TOP[c][0], f"{TOP[c][1]}-rest", "checker")
GROUND = Gm.Ground(SECS)
FLIGHTS = {n for n, s in enumerate(SECS) if s.fill == "flight"}
Gm.lay(w, GROUND, STYLE, rng=r, face_of=lambda x, z: "flank" if GROUND.owner[(x, z)] in FLIGHTS else "edge")
zones = P.band_mask(R)
for i, k in np.argwhere(zones):
    if red(int(X[i, k]), int(Z[i, k])):
        w.ids[i, 0, k] = 36


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


def hipped(x0, z0, x1, z1, y0, stairs=B.BRICK_STAIRS):
    """A hipped roof over x0..x1, z0..z1: a ring of stairs a course from y0, each one in from the last, rising
    to a ridge of stairs back to back."""
    k = 0
    while x0 + k <= x1 - k and z0 + k <= z1 - k:
        y = y0 + k
        a0, a1, b0, b1 = x0 + k, x1 - k, z0 + k, z1 - k
        for x in range(a0, a1 + 1):
            for z in range(b0, b1 + 1):
                edge = [d for d, on in (("e", x == a0), ("w", x == a1), ("s", z == b0), ("n", z == b1)) if on]
                if not edge:
                    continue
                if a1 - a0 <= 1:
                    w.set(x, y, z, stairs, stair("e" if x == a0 else "w"))
                elif b1 - b0 <= 1:
                    w.set(x, y, z, stairs, stair("s" if z == b0 else "n"))
                else:
                    w.set(x, y, z, stairs, stair(edge[0]))
        k += 1


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
    hipped(x0, z0, x1, z1, top + 1)
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

# 9b. the well's canopy: a brick roof on four stilts of stone brick at the pit's corners, a beam of slabs between
# them, sea lanterns over the stilts; open on every side, so the drop and the Court's sight lines stay as they were
hx0, hz0, hx1, hz1 = P.HOLE
cx0, cz0, cx1, cz1 = hx0 - 1, hz0 - 1, hx1 + 1, hz1 + 1
beam = P.HUB + P.CANOPY
for x in (cx0, cx1):
    for z in (cz0, cz1):
        for y in range(P.HUB + 1, beam):
            w.set(x, y, z, B.STONEBRICK, 3 if y == beam - 1 else 0)
for x in range(cx0, cx1 + 1):
    for z in range(cz0, cz1 + 1):
        if x in (cx0, cx1) or z in (cz0, cz1):
            corner = x in (cx0, cx1) and z in (cz0, cz1)
            w.set(x, beam, z, *((B.SEA_LANTERN, 0) if corner else (B.SLAB, 5 | 8)))
hipped(cx0, cz0, cx1, cz1, beam + 1)

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
    w.set(x, P.UNDER, z, *(BRICK if ((x // 3) + (z // 3)) % 2 == 0 else (B.STONEBRICK, 2)))
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
