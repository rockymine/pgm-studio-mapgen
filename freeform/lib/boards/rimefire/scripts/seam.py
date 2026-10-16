"""The seam: the ravine's floor, its stairs and the three bridges over it.

North of the seam's centre line everything is the fire half's (lava in the foot, dark oak, jack-o'-lanterns); south of it
the ice half's (a frozen stream, spruce, sea lanterns). A bridge changes skin at its middle.
"""
import numpy as np

from pgmvox import B, rng
from pgmvox.core.orient import stair as stair_data

import land as LND

FLOOR = LND.FLOOR
LEVEL = LND.LEVEL


def put(w, x, y, z, blk):
    w.set(x, y, z, *blk) if isinstance(blk, tuple) else w.set(x, y, z, blk)


def ford_near(x, side, g):
    """True where the lava channel is broken for a stair's foot: x within 5 of a north stair's start (side north)."""
    for name, pts in g["ramps"]:
        south = "(south)" in name
        if south == (side == "south") and abs(x - pts[0][0]) < 5.5:
            return True
    return False


def floor(w, g):
    """The seam's floor: an obsidian line down the middle, a walkway of cobble and gravel either side of it, a lava
    stream under the north wall and a frozen stream under the south one, and slag or rime beyond them."""
    H, d, hw, south, land = g["H"], g["d"], g["hw"], g["south"], g["land"]
    X = g["X"]
    r = rng("rimefire", "seam-floor")
    sx, sz = H.shape
    n = {"lava": 0, "ice": 0}
    for i in range(sx):
        for k in range(sz):
            if not (land[i, k] and g["seam"][i, k]) or d[i, k] >= hw[i, k] - 0.4:
                continue
            x, z = int(X[i, k]), int(g["Z"][i, k])
            dd = d[i, k]
            top = FLOOR
            # clear the column above the floor and rebuild the floor at FLOOR
            ytop = max(int(H[i, k]), FLOOR) + 3
            w.ids[i, FLOOR:ytop + 1, k] = 0
            w.dat[i, FLOOR:ytop + 1, k] = 0
            lo = max(1, min(int(H[i, k]), FLOOR) - 30)
            under = w.ids[i, lo:FLOOR, k]
            under[under == 0] = B.STONE
            if dd < 1.1:
                blk = (B.OBSIDIAN, 0)
            elif dd < 3.3:
                blk = [(B.COBBLE, 0), (B.GRAVEL, 0), (B.STONE, 5), (B.GRAVEL, 0)][int(r.integers(4))]
            elif dd < 5.7 and not ford_near(x, "south" if south[i, k] else "north", g):
                blk = None
            else:
                if south[i, k]:
                    blk = [(B.PACKED_ICE, 0), (B.GRAVEL, 0), (B.STONE, 5), (B.PACKED_ICE, 0)][int(r.integers(4))]
                else:
                    blk = [(B.NETHERRACK, 0), (B.DIRT, 1), (B.NETHERRACK, 0), (B.GRAVEL, 0)][int(r.integers(4))]
            if blk is not None:
                w.set(x, FLOOR, z, *blk)
            else:                                                  # the stream: a channel one block down
                bed = (B.NETHERRACK, 0) if not south[i, k] else (B.GRAVEL, 0)
                w.set(x, FLOOR - 2, z, *bed)
                if south[i, k]:
                    w.set(x, FLOOR - 1, z, B.ICE)
                    n["ice"] += 1
                else:
                    w.set(x, FLOOR - 1, z, B.LAVA)
                    n["lava"] += 1
    return n


def road_surface(w, g, f, cold_at, pts, width, seed, clear=3):
    """A path: every column within width/2 of the polyline takes a block of its half's path tone."""
    from pgmvox.geom import shapes
    X, Z, H = g["X"], g["Z"], g["H"]
    d, _ = shapes.polyline(X, Z, pts)
    r = np.random.default_rng(seed)
    on = (d <= width / 2) & g["land"] & ~g["seam_floor"]
    n = 0
    for i, k in np.argwhere(on):
        x, z, y = int(X[i, k]), int(Z[i, k]), int(H[i, k])
        if cold_at[i, k]:
            blk = [(B.STONE, 5), (B.GRAVEL, 0), (B.COBBLE, 0), (B.STONE, 5), (B.GRAVEL, 0)][int(r.integers(5))]
        else:
            blk = [(B.STONE, 1), (B.DIRT, 1), (B.GRAVEL, 0), (B.STONE, 1), (B.DIRT, 1), (B.BRICK, 0)][int(r.integers(6))]
        w.set(x, y, z, *blk)
        for yy in range(y + 1, y + 1 + clear):
            if w.id(x, yy, z) in (B.SNOW_LAYER, B.TALLGRASS, B.FLOWER, B.DEADBUSH):
                w.set(x, yy, z, B.AIR)
        n += 1
    return n


def stairs(w, g, pts, cold_at, width=3):
    """A stair on every one-block rise along a polyline."""
    from pgmvox.geom.shapes import walk_cells
    H, X, Z = g["H"], g["X"], g["Z"]
    cells = walk_cells([(int(round(x)), int(round(z))) for x, z in pts])
    n = 0
    x0, z0 = int(X[0, 0]), int(Z[0, 0])
    for (ax, az), (bx, bz) in zip(cells, cells[1:]):
        a, b = (ax - x0, az - z0), (bx - x0, bz - z0)
        if not (0 <= b[0] < H.shape[0] and 0 <= b[1] < H.shape[1]):
            continue
        dh = int(H[b]) - int(H[a])
        dx, dz = bx - ax, bz - az
        if abs(dh) != 1 or abs(dx) + abs(dz) != 1:
            continue
        up, at = ((dx, dz), (bx, bz, int(H[b]))) if dh > 0 else ((-dx, -dz), (ax, az, int(H[a])))
        for j in range(-(width // 2), width - width // 2):
            x, z = at[0] + j * abs(dz), at[1] + j * abs(dx)
            ix, iz = x - x0, z - z0
            if 0 <= ix < H.shape[0] and 0 <= iz < H.shape[1] and abs(int(H[ix, iz]) - at[2]) <= 1:
                cold = cold_at[ix, iz]
                w.set(x, at[2], z, B.COBBLE_STAIRS if cold else B.BRICK_STAIRS, stair_data(up))
                n += 1
    return n


# ---- the bridges -------------------------------------------------------------------------------------------
def rail_post(w, x, y, z, south, lit=True):
    post = B.SPRUCE_FENCE if south else B.DARK_OAK_FENCE
    w.set(x, y + 1, z, post)
    w.set(x, y + 2, z, post)
    if lit:
        if south:
            w.set(x, y + 3, z, B.SEA_LANTERN)
        else:
            w.set(x, y + 3, z, B.JACK, 0)


def timber_bridge(w, g, cx, width=4):
    """A trestle bridge on a straight line across the seam at x = cx. Its deck is at LEVEL: dark oak planks over the north
    half and spruce over the south, rails of the same wood, a lit post every six blocks, and trestle bents under it."""
    c = float(LND.centre(cx))
    half = width // 2
    x0 = int(cx) - half + (1 if width % 2 == 0 else 0)
    xs = list(range(x0, x0 + width))
    z0, z1 = int(round(c)) - 16, int(round(c)) + 16
    H, Xg = g["H"], g["X"]
    ox, oz = int(Xg[0, 0]), int(g["Z"][0, 0])
    for z in range(z0, z1 + 1):
        south = z > c
        plank = (B.PLANKS, 1) if south else (B.PLANKS, 5)
        for x in xs:
            gh = int(H[x - ox, z - oz])
            if gh >= LEVEL and abs(z - c) > 11:                 # solid ground at the deck's level: nothing to span
                continue
            w.set(x, LEVEL, z, *plank)
            for y in range(LEVEL + 1, LEVEL + 4):
                w.set(x, y, z, B.AIR)
        for x in (xs[0], xs[-1]):
            gh = int(H[x - ox, z - oz])
            if abs(z - c) > 11 and gh >= LEVEL:
                continue
            w.set(x, LEVEL + 1, z, B.SPRUCE_FENCE if south else B.DARK_OAK_FENCE)
    # a lit post every six blocks
    for z in range(z0 + 2, z1 - 1, 6):
        for x in (xs[0], xs[-1]):
            if abs(z - c) <= 11:
                rail_post(w, x, LEVEL, z, z > c)
    # trestle bents: two legs and a cross beam at each bent, down to whatever is below
    for off in (-8, -4, 0, 4, 8):
        z = int(round(c + off))
        south = z > c
        log = (B.LOG, 1) if south else (B.LOG2, 1)
        for x in (xs[0], xs[-1]):
            y = LEVEL - 1
            while y > 1 and w.id(x, y, z) in (B.AIR, B.LAVA, B.WATER, B.ICE):
                w.set(x, y, z, *log)
                y -= 1
        for x in range(xs[0], xs[-1] + 1):
            w.set(x, LEVEL - 1, z, *((B.LOG, 1 | 4) if south else (B.LOG2, 1 | 4)))
    # a gate over the middle: two posts and a lintel on the seam line
    zc = int(round(c))
    for x in (xs[0], xs[-1]):
        for y in range(LEVEL + 1, LEVEL + 6):
            w.set(x, y, zc, B.SPRUCE_FENCE if y < LEVEL + 5 else B.LOG2)
    for x in range(xs[0], xs[-1] + 1):
        w.set(x, LEVEL + 5, zc, B.LOG2, 1 | 4)
    return xs, z0, z1


def keystone(w, g, cx=-0.5, width=6):
    """The keystone: a stone bridge whose pier stands on the seam's floor with a tunnel through it, parapets of
    cobble wall and bricks, and upside-down stairs under the deck's edge."""
    c = float(LND.centre(cx))
    x0 = int(np.floor(cx - width / 2 + 0.5))
    xs = list(range(x0, x0 + width))
    z0, z1 = int(round(c)) - 15, int(round(c)) + 15
    zc = int(round(c))
    H = g["H"]
    ox, oz = int(g["X"][0, 0]), int(g["Z"][0, 0])
    r = rng("rimefire", "keystone")
    for z in range(z0, z1 + 1):
        south = z > c
        for xi, x in enumerate(xs):
            gh = int(H[x - ox, z - oz])
            if gh >= LEVEL and abs(z - c) > 11:
                continue
            edge = xi in (0, width - 1)
            w.set(x, LEVEL, z, *(((B.STONEBRICK, 0) if (z + x) % 5 else (B.STONEBRICK, 3)) if not edge else (B.STONEBRICK, 0)))
            w.set(x, LEVEL - 1, z, B.STONEBRICK, 0)
            for y in range(LEVEL + 1, LEVEL + 5):
                w.set(x, y, z, B.AIR)
            if edge:
                w.set(x, LEVEL + 1, z, B.COBBLE_WALL, 0)
            # a groove down the middle in the colour of the half it crosses
            if xi in (width // 2 - 1, width // 2) and abs(z - c) <= 12:
                w.set(x, LEVEL, z, B.QUARTZ if south else B.NETHER_BRICK, 0)
            if xi in (1, width - 2) and abs(z - c) <= 12 and z % 4 == 0:
                w.set(x, LEVEL, z, B.STONEBRICK, 3)
    # the pier
    top = LEVEL - 2
    for x in xs:
        for z in range(zc - 3, zc + 4):
            col = H[x - ox, z - oz]
            for y in range(FLOOR + 1, top + 1):
                w.set(x, y, z, B.STONEBRICK, 0 if (x + y + z) % 6 else 2)
    for x in xs:                                                # the tunnel along the seam
        for z in range(zc - 2, zc + 2):
            for y in range(FLOOR + 1, FLOOR + 5):
                w.set(x, y, z, B.AIR)
        # arch: stairs on the tunnel's lips
        w.set(x, FLOOR + 5, zc - 2, B.STONEBRICK_STAIRS, stair_data("s", True))
        w.set(x, FLOOR + 5, zc + 1, B.STONEBRICK_STAIRS, stair_data("n", True))
    # corbels under the deck's edges, either side of the pier
    for z in list(range(zc - 11, zc - 3)) + list(range(zc + 4, zc + 12)):
        for x in (xs[0], xs[-1]):
            if H[x - ox, z - oz] < LEVEL - 2:
                w.set(x, LEVEL - 2, z, B.STONEBRICK_STAIRS, stair_data("e" if x == xs[0] else "w", True))
    # braziers at both ends of the deck and at the pier: fire over the north half, ice-light over the south
    for zz in (zc - 11, zc + 11):
        for x in (xs[0], xs[-1]):
            w.set(x, LEVEL + 1, zz, B.NETHER_BRICK if zz < c else B.QUARTZ, 0)
            w.set(x, LEVEL + 2, zz, B.NETHER_BRICK if zz < c else B.QUARTZ, 0)
            w.set(x, LEVEL + 3, zz, B.GLOWSTONE if zz < c else B.SEA_LANTERN)
    return xs, z0, z1
