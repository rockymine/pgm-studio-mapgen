"""Generate Riad from the plan's two rasters: every column built to the floor the checker walked, the roofs over
the arcades, then what a raster cannot hold — the Cistern's tower, its caged water columns and its landings,
the trees, the pavilions, the spawn terraces' canopies, the posts' beacons and the flag's banner — and the
palace's paint.

    python3 gen.py <build-dir>

The rasters are the whole board already (they were drawn with their mirror), so nothing is mirrored here
except the pieces built by hand, which are built for blue and mirrored for red.
"""
import random
import sys
import time

import numpy as np
from scipy import ndimage

import plan as P
from mc import World, B

R = P.build()
K = P.KINDS
KN = {v: k for k, v in K.items()}
G, LOW = P.G, P.LOW

SANDSTONE, CHISELED, SMOOTH = (B.SANDSTONE, 0), (B.SANDSTONE, 1), (B.SANDSTONE, 2)
RED, RED_CHISELED, RED_SMOOTH = (B.RED_SANDSTONE, 0), (B.RED_SANDSTONE, 1), (B.RED_SANDSTONE, 2)
QUARTZ, QUARTZ_CHISELED, QUARTZ_PILLAR = (B.QUARTZ, 0), (B.QUARTZ, 1), (B.QUARTZ, 2)
TERRACOTTA = (B.HARDENED_CLAY, 0)
ORANGE_CLAY, CYAN_CLAY, WHITE_CLAY = (B.STAINED_CLAY, 1), (B.STAINED_CLAY, 9), (B.STAINED_CLAY, 0)
PRISMARINE, PRISMARINE_BRICK, DARK_PRISMARINE = (168, 0), (168, 1), (168, 2)
SEA_LANTERN = (169, 0)
BEACON = (138, 0)
GOLD = (B.GOLD_BLOCK, 0)
HEDGE = (B.LEAVES, 4)                                # oak leaves, no decay
CAGE = (B.STAINED_PANE, 3)                           # light-blue glass
SANDSTONE_STAIRS, RED_STAIRS = 128, 180
QUARTZ_SLAB = (B.SLAB, 7)
STAIR_DATA = {"+x": 0, "-x": 1, "+z": 2, "-z": 3}
rng = random.Random(7)


def team_wool(z):
    """Red holds the north, blue the south; the middle band, |z| <= 16, belongs to nobody."""
    if z < -16:
        return (B.WOOL, 14)
    if z > 16:
        return (B.WOOL, 11)
    return QUARTZ


def dye(team):
    return {"red": 1, "blue": 4}[team]


def kind(x, z):
    i, j = P.ix(x), P.iz(z)
    if not (0 <= i < P.NX and 0 <= j < P.NZ):
        return "void"
    return KN[R.K[i, j]]


def height(x, z):
    i, j = P.ix(x), P.iz(z)
    if not (0 <= i < P.NX and 0 <= j < P.NZ):
        return -1
    return int(R.H[i, j])


N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
N8 = N4 + ((1, 1), (1, -1), (-1, 1), (-1, -1))

# ---- the board's underside: an inverted ziggurat, a course deeper for every block in from the edge ----------
SOLIDMASK = R.K != K["void"]
DIST = ndimage.distance_transform_cdt(SOLIDMASK, metric="chessboard")
OUTER = ndimage.label(~SOLIDMASK)[0]
OUTER_IDS = set(np.unique(np.concatenate([OUTER[0, :], OUTER[-1, :], OUTER[:, 0], OUTER[:, -1]]))) - {0}


def base_y(x, z):
    d = int(DIST[P.ix(x), P.iz(z)])
    return max(3, 15 - d)


def is_outer_void(x, z):
    i, j = P.ix(x), P.iz(z)
    if not (0 <= i < P.NX and 0 <= j < P.NZ):
        return True
    return R.K[i, j] == K["void"] and OUTER[i, j] in OUTER_IDS


# ---- the paint --------------------------------------------------------------------------------------------
def body(x, y, z, top):
    """A column's body: red sandstone in courses with terracotta every fourth, and in the top three blocks of a
    face that stands over a sunken garden, a band of chiseled sandstone under the team's colour."""
    if y == top - 1 and top == G:
        return team_wool(z) if abs(z) > 16 else CHISELED
    if y == top - 2 and top == G:
        return CHISELED
    if y % 4 == 0:
        return TERRACOTTA
    return RED


def ground_block(x, z, h):
    """The ground's top. The court: smooth sandstone with a lattice of red on the diagonals and a ring of
    chiseled quartz round the Cistern. The gardens: grass. Everywhere else smooth sandstone ruled every five
    blocks in red. Wherever the ground stands over a lower neighbour its edge is quartz."""
    if any(height(x + dx, z + dz) < h - 1 and kind(x + dx, z + dz) not in ("void", "water", "stair")
           for dx, dz in N4):
        return QUARTZ
    if h == LOW:
        return (B.GRASS, 0)
    if abs(x) <= 17 and abs(z) <= 16 or (-19 <= x <= -18 and abs(z) <= 16):
        if max(abs(x), abs(z)) == 7:
            return QUARTZ_CHISELED
        if (abs(x) + abs(z)) % 6 == 0 or abs(abs(x) - abs(z)) % 6 == 0:
            return RED_SMOOTH
        return SMOOTH
    if abs(x) <= 8 and 17 <= abs(z) <= 36:                   # the lane: quartz coping along the canal
        return QUARTZ_CHISELED if abs(x) == 3 else SMOOTH
    if x % 5 == 0 or z % 5 == 0:
        return RED_SMOOTH
    return SMOOTH


# ---- the columns ------------------------------------------------------------------------------------------
def columns(w):
    for i in range(P.NX):
        for j in range(P.NZ):
            x, z = i + P.X_MIN, j + P.Z_MIN
            k, h = KN[R.K[i, j]], int(R.H[i, j])
            if k == "void":
                continue
            b0 = base_y(x, z)
            if k == "bridge":
                for y in range(h - 1, h + 1):
                    w.set(x, y, z, *RED_SMOOTH)
                w.set(x, h, z, *(QUARTZ if x % 2 == 0 else SMOOTH))
                w.set(x, h - 2, z, RED_STAIRS, 4 if abs(z) == 0 else (6 if z < 0 else 7))
                continue
            if k == "post" and x < -30:                     # the Mirador's pad, hung over the void
                for y in range(h - 5, h + 1):
                    w.set(x, y, z, *(RED_CHISELED if y == h - 2 else RED_SMOOTH))
                w.set(x, h, z, *QUARTZ_CHISELED)
                continue
            if k == "stone" and h <= G and any(kind(x + dx, z + dz) == "void" for dx, dz in N4):
                for y in range(b0 - 6, h):                  # a stepping stone: a pillar out of the void
                    w.set(x, y, z, *(RED_CHISELED if y % 3 == 0 else RED_SMOOTH))
                w.set(x, h, z, *QUARTZ_CHISELED)
                continue
            landing = k == "floor" and h == 22 and abs(x) <= 6 and abs(z) <= 1
            if k in ("water", "swim", "cage") or landing:
                sump = (x, z) in P.SUMP or k in ("swim", "cage")
                floor = P.CISTERN["sump"] if sump else P.CISTERN["floor"]
                for y in range(b0, floor):
                    w.set(x, y, z, *body(x, y, z, floor))
                w.set(x, floor, z, *(SEA_LANTERN if (x + z) % 4 == 0 and not sump else PRISMARINE_BRICK))
                top = h if k == "swim" else P.CISTERN["water"]           # the landings are built in cistern()
                for y in range(floor + 1, top + 1):
                    w.set(x, y, z, B.WATER)
                if k == "cage":
                    for y in range(P.CISTERN["water"] + 1, h + 1):
                        w.set(x, y, z, *CAGE)
                continue
            if k == "canal":
                for y in range(b0, G - 1):
                    w.set(x, y, z, *body(x, y, z, G - 1))
                w.set(x, G - 1, z, *(SEA_LANTERN if z % 5 == 0 and x == 0 else PRISMARINE))
                w.set(x, G, z, B.WATER)
                continue
            floor_h = h
            if k in ("hedge", "tree", "column", "ladder", "wall"):
                floor_h = G if abs(x) <= 13 and k == "column" else (
                    LOW if (k in ("hedge", "tree", "ladder", "wall") and _sunk(x, z)) else G)
            for y in range(b0, floor_h + 1):
                w.set(x, y, z, *body(x, y, z, floor_h))
            if k in ("floor", "spawn"):
                w.set(x, h, z, *ground_block(x, z, h))
                if h == G + 2 and k == "spawn":
                    w.set(x, h, z, *(team_wool(z) if (x + z) % 2 == 0 and abs(x) <= 9 else QUARTZ))
                    w.set(x, h - 1, z, *team_wool(z))
            elif k == "stair":
                w.set(x, h, z, SANDSTONE_STAIRS, STAIR_DATA[R.stair[(x, z)]])
            elif k == "stone":
                for y in range(floor_h + 1, h):
                    w.set(x, y, z, *CHISELED)
                w.set(x, h, z, *QUARTZ_CHISELED)
            elif k == "hedge":
                w.set(x, floor_h, z, *(SMOOTH if floor_h == G else (B.GRASS, 0)))
                for y in range(floor_h + 1, floor_h + 3):
                    w.set(x, y, z, *HEDGE)
            elif k == "column":
                w.set(x, G, z, *SMOOTH)
                for y in range(G + 1, h):
                    w.set(x, y, z, *QUARTZ_PILLAR)
            elif k in ("ladder", "tree", "wall"):
                w.set(x, floor_h, z, *(SMOOTH if floor_h == G else (B.GRASS, 0)))
            elif k == "post":
                pass                                        # the towers: built in towers()


def _sunk(x, z):
    """Whether a solid thing stands in a sunken garden: its neighbours' ground is the low ground."""
    hs = [height(x + dx, z + dz) for dx, dz in N8 if kind(x + dx, z + dz) in ("floor", "stair", "stone")]
    return bool(hs) and min(hs) == LOW


def parapets(w):
    """Round the board's outer edge, a parapet of red sandstone, crenellated with quartz slabs and inlaid with
    the team's wool every fourth block. Not beside the Mirador's bridge, not behind the Minaret's garden and
    not round the void holes: there the drop is the point; and not beside a spawn terrace, where it would be
    the step a player climbs back by."""
    for i in range(P.NX):
        for j in range(P.NZ):
            if R.K[i, j] == K["void"]:
                continue
            x, z = i + P.X_MIN, j + P.Z_MIN
            k, h = KN[R.K[i, j]], int(R.H[i, j])
            if k not in ("floor", "hedge", "tree") or h not in (G, LOW):
                continue
            if x <= -30 and abs(z) <= 7 or x >= 40 and abs(z) <= 13:
                continue
            if abs(x) <= 15 and abs(z) >= 44:
                continue                                    # a parapet by a spawn terrace would be a step onto it
            if not any(is_outer_void(x + dx, z + dz) for dx, dz in N4):
                continue
            w.set(x, h + 1, z, *(team_wool(z) if (x + z) % 4 == 0 and abs(z) > 16 else RED_SMOOTH))
            if (x + z) % 2 == 0:
                w.set(x, h + 2, z, *QUARTZ_SLAB)


def hole_rims(w):
    """The void holes' rims in chiseled quartz, so the edge reads before the fall."""
    for i in range(P.NX):
        for j in range(P.NZ):
            x, z = i + P.X_MIN, j + P.Z_MIN
            if KN[R.K[i, j]] != "floor":
                continue
            if any(kind(x + dx, z + dz) == "void" and not is_outer_void(x + dx, z + dz) for dx, dz in N4):
                w.set(x, int(R.H[i, j]), z, *QUARTZ_CHISELED)


def arcades(w):
    """The arcades: a roof of orange terracotta edged in the team's wool over quartz columns, and between each
    pair of columns an arch of upside-down sandstone stairs."""
    for i in range(P.NX):
        for j in range(P.NZ):
            if R.UK[i, j] != P.UKINDS["roof"]:
                continue
            x, z = i + P.X_MIN, j + P.Z_MIN
            u = int(R.U[i, j])
            edge = any(R.UK[i + di, j + dj] != P.UKINDS["roof"] for di, dj in N4)
            w.set(x, u, z, *(team_wool(z) if edge else ORANGE_CLAY))
    for sz in (1, -1):
        for xc in (-13, -9, 9, 13):
            for zc in range(18, 38, 4):
                a, b = sz * (zc + 1), sz * (zc + 3)
                w.set(xc, 23, a, SANDSTONE_STAIRS, 7 if sz > 0 else 6)
                w.set(xc, 23, b, SANDSTONE_STAIRS, 6 if sz > 0 else 7)


def tree(w, x, y, z, kind_="oak"):
    """A vanilla tree: a trunk of four to six, two wide layers of leaves with ragged corners, a narrow crown."""
    log, leaf = ((B.LOG, 0), (B.LEAVES, 4)) if kind_ == "oak" else ((B.LOG, 2), (B.LEAVES, 6))
    rng = random.Random(x * 1000 + abs(z))                  # a tree and its mirror grow alike
    t = rng.randint(5, 6)                                   # the leaves start over a player's head
    top = y + t
    for yy in range(y + 1, top + 1):
        w.set(x, yy, z, *log)
    for yy in (top - 2, top - 1):
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                if abs(dx) == 2 and abs(dz) == 2 and rng.random() < 0.6:
                    continue
                if (dx, dz) != (0, 0) and w.id(x + dx, yy, z + dz) == B.AIR:
                    w.set(x + dx, yy, z + dz, *leaf)
    for yy in (top, top + 1):
        for dx in range(-1, 2):
            for dz in range(-1, 2):
                if abs(dx) == 1 and abs(dz) == 1 and (yy == top + 1 or rng.random() < 0.5):
                    continue
                if w.id(x + dx, yy, z + dz) == B.AIR:
                    w.set(x + dx, yy, z + dz, *leaf)


def trees(w):
    for i in range(P.NX):
        for j in range(P.NZ):
            if KN[R.K[i, j]] == "tree":
                x, z = i + P.X_MIN, j + P.Z_MIN
                y = LOW if _sunk(x, z) else G
                tree(w, x, y, z, "birch" if (x * 7 + z * 3) % 3 == 0 else "oak")


def flowers(w):
    """Flowers in the sunken gardens' grass, a few in every bed."""
    for i in range(P.NX):
        for j in range(P.NZ):
            x, z = i + P.X_MIN, j + P.Z_MIN
            if KN[R.K[i, j]] == "floor" and R.H[i, j] == LOW and w.get(x, LOW, z) == (B.GRASS, 0):
                r = rng.random()
                if r < 0.06:
                    w.set(x, LOW + 1, z, B.FLOWER, rng.choice((0, 3, 8, 6)))
                elif r < 0.09:
                    w.set(x, LOW + 1, z, B.DANDELION, 0)
                elif r < 0.16:
                    w.set(x, LOW + 1, z, B.TALLGRASS, 1)


def cistern(w):
    """The Cistern's tower: red sandstone banded in chiseled, a quartz top, a beacon in it and the flag's banner
    on it. Its landings: a bridge east and west off the tower, two under its top, arched over the pool so a
    swimmer passes under."""
    for x in range(-1, 2):
        for z in range(-1, 2):
            for y in range(P.CISTERN["sump"], 25):
                w.set(x, y, z, *(RED_CHISELED if y % 3 == 0 else RED_SMOOTH))
            w.set(x, 24, z, *QUARTZ_CHISELED)
    w.set(0, 24, 0, *BEACON)
    w.banner(0, 25, 0, 5, patterns=[("bo", 15), ("mc", 15)], rot=0)   # purple, a white border and a roundel
    for sx in (-1, 1):
        for a in range(2, 7):
            x = a * sx
            for z in range(-1, 2):
                w.set(x, 22, z, *(QUARTZ_CHISELED if z == 0 else SMOOTH))
                w.set(x, 21, z, *RED_SMOOTH)
                w.set(x, 20, z, B.AIR)
        for z in range(-1, 2):                              # an arch's shoulders where the landing meets the rim
            w.set(6 * sx, 20, z, RED_STAIRS, 4 + (1 if sx > 0 else 0))


def minaret(w):
    """The Minaret: a pillar five over its garden, banded, a quartz top with a beacon in it, and a ladder up
    each face. Paths of smooth sandstone cross the garden to it."""
    for x in range(21, 43):
        for z in (-1, 0, 1):
            if w.get(x, LOW, z) == (B.GRASS, 0):
                w.set(x, LOW, z, *SMOOTH)
    for z in range(-13, 14):
        for x in (29, 30, 31):
            if w.get(x, LOW, z) == (B.GRASS, 0):
                w.set(x, LOW, z, *SMOOTH)
    top = LOW + 5
    for x in range(29, 32):
        for z in range(-1, 2):
            for y in range(LOW + 1, top + 1):
                w.set(x, y, z, *(QUARTZ_CHISELED if y == top else (RED_CHISELED if y == LOW + 3 else RED_SMOOTH)))
    w.set(30, top, 0, *BEACON)
    for (x, z), facing in (((30, -2), 2), ((30, 2), 3), ((28, 0), 4), ((32, 0), 5)):
        for y in range(LOW + 1, top + 1):
            w.set(x, y, z, B.LADDER, facing)
    w.set(-42, 24, 0, *BEACON)


def pavilions(w):
    """The large cover in each sunken garden, built on the garden floor. West: a kiosk in red sandstone with a
    blind arch on each face and a stepped dome of terracotta capped in gold. East: a fountain house in
    terracotta banded in cyan, a basin on its roof and a jet of water."""
    for sz in (1, -1):
        Z = lambda z: sz * z
        for x in range(-28, -21):
            for z in range(24, 31):
                for y in range(LOW + 1, LOW + 10):
                    edge = x in (-28, -22) or z in (24, 30)
                    mid = x == -25 or z == 27
                    corner = x in (-28, -22) and z in (24, 30)
                    if corner:
                        b = QUARTZ_PILLAR
                    elif edge and mid and y <= LOW + 4:
                        b = RED_CHISELED if y == LOW + 4 else DARK_PRISMARINE
                    elif y == LOW + 6:
                        b = QUARTZ
                    elif y == LOW + 9:
                        b = QUARTZ_CHISELED
                    else:
                        b = RED_SMOOTH
                    w.set(x, y, Z(z), *b)
        for r, y in ((3, LOW + 10), (2, LOW + 11), (1, LOW + 12), (0, LOW + 13)):
            for x in range(-25 - r, -24 + r):
                for z in range(27 - r, 28 + r):
                    w.set(x, y, Z(z), *(ORANGE_CLAY if r else GOLD))
        for x in range(22, 29):
            for z in range(24, 31):
                for y in range(LOW + 1, LOW + 10):
                    edge = x in (22, 28) or z in (24, 30)
                    b = CYAN_CLAY if y in (LOW + 3, LOW + 7) else (QUARTZ if y == LOW + 9 else TERRACOTTA)
                    if edge and (x == 25 or z == 27) and LOW + 1 <= y <= LOW + 5:
                        b = WHITE_CLAY
                    w.set(x, y, Z(z), *b)
        for x in range(23, 28):
            for z in range(25, 30):
                w.set(x, LOW + 9, Z(z), *PRISMARINE_BRICK)
                w.set(x, LOW + 10, Z(z), B.WATER)
        for x in range(22, 29):
            for z in range(24, 31):
                if x in (22, 28) or z in (24, 30):
                    w.set(x, LOW + 10, Z(z), *QUARTZ_SLAB)
        w.set(25, LOW + 10, Z(27), *QUARTZ_PILLAR)
        w.set(25, LOW + 11, Z(27), *QUARTZ_PILLAR)
        w.set(25, LOW + 12, Z(27), B.WATER)


def porch(w):
    """The Mirador's porch: a blind arcade in its faces, its top tiled, its edges in quartz, and low stairs at
    the bridge's head either side for a little cover."""
    for x in range(-30, -19):
        for z in range(-5, 6):
            w.set(x, 24, z, *(QUARTZ if x in (-30, -20) or abs(z) == 5 else
                              (RED_SMOOTH if (x + z) % 3 == 0 else SMOOTH)))
            for y in range(G + 1, 24):
                if (x in (-30, -20) or abs(z) == 5) and (x + z) % 3 == 0:
                    w.set(x, y, z, *(RED_CHISELED if y == 23 else CHISELED))
    for z in list(range(-5, -1)) + list(range(2, 6)):
        w.set(-30, 25, z, RED_STAIRS, 1)


def spawns(w):
    """Each spawn terrace: two over the back garden with a canopy over its back half — quartz pillars, a roof of
    orange terracotta fringed in the team's wool, and the team's banners hanging under its front."""
    for team, sz in (("blue", 1), ("red", -1)):
        Z = lambda z: sz * z
        for x in range(-10, 11):
            for z in range(50, 57):
                w.set(x, 27, Z(z), *(team_wool(Z(z)) if x in (-10, 10) or z in (50, 56) else ORANGE_CLAY))
        for x in (-10, -5, 5, 10):
            for z in (50, 56):
                for y in range(23, 27):
                    w.set(x, y, Z(z), *QUARTZ_PILLAR)
        for x in (-10, 10):
            for y in range(23, 27):
                w.set(x, y, Z(53), *QUARTZ_PILLAR)
        for x in range(-9, 10):                          # a low wall at the back, over the void
            if x not in (-5, 5):
                w.set(x, 23, Z(56), *RED_SMOOTH)
        for x in (-7, -2, 3, 8):
            w.banner(x, 27, Z(49), dye(team), patterns=[("bs", 15), ("cre", 0)], wall_facing=2 if sz > 0 else 3)
        w.set(0, 27, Z(53), *(B.GLOWSTONE, 0))


def make():
    w = World(P.X_MIN - 1, P.Z_MIN - 1, P.NX + 2, P.NZ + 2, sy=48)
    columns(w)
    parapets(w)
    hole_rims(w)
    arcades(w)
    cistern(w)
    minaret(w)
    pavilions(w)
    porch(w)
    spawns(w)
    trees(w)
    flowers(w)
    w.biome[:, :] = 1
    return w


def main(build):
    t0 = time.time()
    w = make()
    w.save(build, "Riad", (0, 40, 0))
    print(f"generated and saved {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
