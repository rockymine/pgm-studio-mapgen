"""What stands on the islands of Lantern Karst, on red's half: the paint of the floors, the tea, the stone
lanterns, the spruce, and the pavilions — the Pavilion of Arrival and its towers, the Gate, the Bell Rock's
bell house, the Pillar Shrine and the Tea Store — with the monuments and the Store's bedrock wall.

Pavilions are spruce and dark oak: dark oak log posts, white panels (white stained clay) banded in jade
(prismarine), dark oak stair roofs that turn up at the corners. Lanterns are glowstone. Red and blue appear only
on the teams' banners of wool; no lacquer red.
"""
import numpy as np

import geometry as G
import plan as P
import terrain as T
from mc import B

DARK_LOG = (B.LOG2, 1)
SPRUCE_LOG = (B.LOG, 1)
WHITE = (B.STAINED_CLAY, 0)
JADE = (168, 1)              # prismarine bricks
DARK_JADE = (168, 2)
PRISMARINE = (168, 0)
DO_STAIRS = B.DARK_OAK_STAIRS
DO_SLAB = (B.WOOD_SLAB, 5)
DO_PLANK = (B.PLANKS, 5)
SP_PLANK = (B.PLANKS, 1)
SB = (B.STONEBRICK, 0)


def floor_y(F, x, z):
    return int(F.H[T.ix(x), T.iz(z)])


def on_land(F, x, z):
    return 0 <= T.ix(x) < T.NX and 0 <= T.iz(z) < T.NZ and F.H[T.ix(x), T.iz(z)] >= 0


# ---- the floors' paint ---------------------------------------------------------------------------------
# Three families, named before painting: the ground is grass on the islands' stone; the built is a paved floor of
# stone brick, polished andesite, andesite and stone (a quarter each in cells of three) under dark oak, spruce,
# white and jade; the accent is the tea's bright green and the lanterns' glowstone.
PAVE = [(B.STONEBRICK, 0), (B.STONE, 6), (B.STONE, 5), (B.STONE, 0)]
PATH = [(B.DIRT, 0), (B.DIRT, 1), (B.PLANKS, 1)]          # solid, one soft tone, a third each


def cell_pick(x, z, choices, size=3, salt=0):
    h = ((x // size) * 73856093) ^ ((z // size) * 19349663) ^ (salt * 83492791)
    return choices[(h & 0x7fffffff) % len(choices)]


def paved(F, i, j):
    """The pieces and the parts of pieces that are built floors."""
    k, kind = F.key[i, j], F.kind[i, j]
    if kind == "spawn" or k in ("bar", "road", "store", "pillar", "bell"):
        return True
    if k == "hub":
        x, z = int(T.XS[i]), int(T.ZS[j])
        dx = max(-8 - x, x - 7, 0); dz = max(-66 - z, z + 51, 0)
        return 1 <= max(dx, dz) <= 3
    return False


# The paths: every walk a player makes, spawn to the front, to each wool room and out to every bridging edge.
# A stroke wanders three blocks either side over about fourteen, easing to nothing at its ends.
STROKES = [
    [(-14.5, -79), (-16, -70), (-26, -66.5), (-50, -66.5), (-86, -66.5)],          # west exit to the Long Terrace
    [(-60, -66.5), (-86, -66.5), (-87.5, -96)],                                      # along it to the Far Arm
    [(-37.5, -74), (-37.5, -96)],                                                     # the Near Arm
    [(13.5, -79), (16, -70), (30, -71), (44, -72), (50, -72)],                       # east exit over the Drying Floor
    [(16, -70), (22, -55), (30, -44.5), (50, -44.5)],                                # down to the Tea Rows
    [(-14.5, -79), (-18, -60), (-19.5, -40), (-19.5, -38)],                          # west side of the hub to the front
    [(13.5, -79), (17, -60), (18.5, -40), (18.5, -38)],                              # east side of the hub to the front
    [(-19.5, -27), (-19.5, -13)], [(18.5, -27), (18.5, -13)],                        # down the Stairs to the band
]


def path_mask(F):
    m = np.zeros(F.land.shape, bool)
    for pts in STROKES:
        dense = []
        for a, b in zip(pts, pts[1:]):
            L = max(1, int(np.hypot(b[0] - a[0], b[1] - a[1])))
            for t in range(L):
                dense.append((a[0] + (b[0] - a[0]) * t / L, a[1] + (b[1] - a[1]) * t / L))
        dense.append(pts[-1])
        dense = np.array(dense)
        n = len(dense)
        s = np.arange(n)
        ease = np.minimum(1, np.minimum(s, n - 1 - s) / 6.0)
        d = np.gradient(dense, axis=0)
        nrm = np.stack([-d[:, 1], d[:, 0]], 1)
        nrm /= np.maximum(1e-9, np.linalg.norm(nrm, axis=1))[:, None]
        bent = dense + nrm * (2.5 * np.sin(2 * np.pi * s / 14.0) * ease)[:, None]
        for px, pz in bent:
            for dx in range(-2, 3):
                for dz in range(-2, 3):
                    if dx * dx + dz * dz <= 2.3:
                        i, j = T.ix(int(round(px)) + dx), T.iz(int(round(pz)) + dz)
                        if 0 <= i < T.NX and 0 <= j < T.NZ:
                            m[i, j] = True
    return m & F.land


def paint(w, F, rng):
    """The top block of every land column: built floors paved, paths solid, the rest grass with small patches
    of coarse dirt (about five blocks across, capped)."""
    pm = path_mask(F)
    patch = np.zeros(F.land.shape)
    from noise import fbm
    patch = fbm(F.land.shape, 5, 2, seed=21)
    hi_cut = np.percentile(patch[F.land], 93)            # about 7% of the grass in coarse-dirt patches
    for i, j in zip(*np.nonzero(F.land)):
        x, z, h = int(T.XS[i]), int(T.ZS[j]), int(F.H[i, j])
        if paved(F, i, j):
            top = cell_pick(x, z, PAVE)
        elif pm[i, j]:
            top = cell_pick(x, z, PATH, salt=1)
        elif patch[i, j] > hi_cut:
            top = (B.DIRT, 1)
        else:
            top = (B.GRASS, 0)
        w.set(x, h, z, *top)


# ---- small things ----------------------------------------------------------------------------------------
def toro(w, x, y, z):
    """A stone lantern: a stone brick foot, a cobble wall post, the light, a slab cap."""
    w.set(x, y + 1, z, B.STONEBRICK, 3)
    w.set(x, y + 2, z, B.COBBLE_WALL, 0)
    w.set(x, y + 3, z, B.GLOWSTONE)
    w.set(x, y + 4, z, B.SLAB, 5)


def spruce(w, x, y, z, height, rng):
    """A karst pine: a spruce trunk with layered cones of leaves that shrink to a point."""
    for k in range(1, height + 1):
        w.set(x, y + k, z, *SPRUCE_LOG)
    r = 3 if height >= 9 else 2
    yy = y + 3
    while yy < y + height + 1:
        rr = max(1, round(r * (1 - (yy - y - 3) / max(1, height - 2)) + 0.4))
        for dx in range(-rr, rr + 1):
            for dz in range(-rr, rr + 1):
                if abs(dx) + abs(dz) <= rr + (rr > 1) and (dx or dz) and w.id(x + dx, yy, z + dz) == B.AIR:
                    w.set(x + dx, yy, z + dz, B.LEAVES, 1 | 4)
        yy += 2
    w.set(x, y + height + 1, z, B.LEAVES, 1 | 4)
    w.set(x, y + height + 2, z, B.LEAVES, 1 | 4)


def tea_rows(w, F, x0, z0, x1, z1, along_x=True):
    """Rows of tea: jungle leaves one high, a walking gap between rows."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            row = (z if along_x else x) % 3
            if row == 0 and on_land(F, x, z):
                h = floor_y(F, x, z)
                if w.id(x, h + 1, z) == B.AIR and w.id(x, h, z) == B.GRASS:
                    w.set(x, h + 1, z, B.LEAVES, 3 | 4)


def banner_post(w, x, y, z, rot):
    """A team banner on a spruce pole (wool colour 14 here; the rotation recolours blue's)."""
    w.set(x, y + 1, z, B.SPRUCE_FENCE)
    w.set(x, y + 2, z, B.SPRUCE_FENCE)
    w.set(x, y + 3, z, B.SPRUCE_FENCE)
    w.set(x, y + 4, z, B.WOOL, 14)
    w.set(x, y + 5, z, B.WOOL, 14)


# ---- roofs and pavilions ---------------------------------------------------------------------------------
def hip_roof(w, x0, z0, x1, z1, y, upturn=True, cap=DO_PLANK):
    """A hip roof of dark oak stairs over x0..x1, z0..z1 from y up, each course one in; the corners of the
    lowest course turned up a block."""
    k = 0
    while x0 + k <= x1 - k and z0 + k <= z1 - k:
        a, b, c, d = x0 + k, z0 + k, x1 - k, z1 - k
        yy = y + k
        if c - a <= 1 or d - b <= 1:
            for x in range(a, c + 1):
                for z in range(b, d + 1):
                    w.set(x, yy, z, *cap)
            for x in range(a, c + 1):
                for z in range(b, d + 1):
                    w.set(x, yy + 1, z, *DO_SLAB)
            break
        for x in range(a, c + 1):
            w.set(x, yy, b, DO_STAIRS, 2)
            w.set(x, yy, d, DO_STAIRS, 3)
        for z in range(b + 1, d):
            w.set(a, yy, z, DO_STAIRS, 0)
            w.set(c, yy, z, DO_STAIRS, 1)
        if k > 0:
            for x in range(a + 1, c):
                for z in range(b + 1, d):
                    w.set(x, yy - 1, z, *DO_PLANK)
        k += 1
    if upturn:
        for (cx, cz, dd) in ((x0, z0, 2), (x1, z0, 2), (x0, z1, 3), (x1, z1, 3)):
            w.set(cx, y + 1, cz, DO_STAIRS, dd | 4)


def skirt_roof(w, x0, z0, x1, z1, y):
    """A ring of eave: two courses of dark oak stairs stepping up and in, the corners turned up."""
    for k in range(2):
        a, b, c, d = x0 + k, z0 + k, x1 - k, z1 - k
        for x in range(a, c + 1):
            w.set(x, y + k, b, DO_STAIRS, 2); w.set(x, y + k, d, DO_STAIRS, 3)
        for z in range(b + 1, d):
            w.set(a, y + k, z, DO_STAIRS, 0); w.set(c, y + k, z, DO_STAIRS, 1)
    for (cx, cz, dd) in ((x0, z0, 2), (x1, z0, 2), (x0, z1, 3), (x1, z1, 3)):
        w.set(cx, y + 1, cz, DO_STAIRS, dd | 4)


def posts(w, x0, z0, x1, z1, y0, y1, step=4, log=DARK_LOG):
    xs = sorted(set(list(range(x0, x1 + 1, step)) + [x1]))
    zs = sorted(set(list(range(z0, z1 + 1, step)) + [z1]))
    for x in xs:
        for z in (z0, z1):
            for y in range(y0, y1 + 1):
                w.set(x, y, z, *log)
    for z in zs:
        for x in (x0, x1):
            for y in range(y0, y1 + 1):
                w.set(x, y, z, *log)


def panel_walls(w, x0, z0, x1, z1, y0, y1, openings=(), windows=True):
    """White panels between the posts, a jade band at the sill, panes for windows; `openings` are
    (side, a, b) spans left open, side in n s w e."""
    def opened(side, t):
        return any(s == side and a <= t <= b for s, a, b in openings)
    for x in range(x0 + 1, x1):
        for side, z in (("n", z0), ("s", z1)):
            for y in range(y0, y1 + 1):
                if w.id(x, y, z) in (B.LOG2, B.LOG):
                    continue
                if opened(side, x) and y <= y0 + 3:
                    w.set(x, y, z, B.AIR)
                    continue
                win = windows and y in (y0 + 2, y0 + 3) and x % 4 == 2
                w.set(x, y, z, *((B.PANE, 0) if win else JADE if y == y0 + 1 else WHITE))
    for z in range(z0 + 1, z1):
        for side, x in (("w", x0), ("e", x1)):
            for y in range(y0, y1 + 1):
                if w.id(x, y, z) in (B.LOG2, B.LOG):
                    continue
                if opened(side, z) and y <= y0 + 3:
                    w.set(x, y, z, B.AIR)
                    continue
                win = windows and y in (y0 + 2, y0 + 3) and z % 4 == 2
                w.set(x, y, z, *((B.PANE, 0) if win else JADE if y == y0 + 1 else WHITE))


def lanterns_under_eaves(w, x0, z0, x1, z1, y):
    for (x, z) in ((x0 - 1, z0 - 1), (x1 + 1, z0 - 1), (x0 - 1, z1 + 1), (x1 + 1, z1 + 1)):
        w.set(x, y, z, B.DARK_OAK_FENCE)
        w.set(x, y - 1, z, B.GLOWSTONE)


# ---- the places -----------------------------------------------------------------------------------------
def spawn(w, F, rng):
    """The Pavilion of Arrival, the pool, the outcrop, the two lantern towers, the tea beds, the monuments."""
    # the pavilion: two storeys over the top terrace, its hall open to the south (toward the Pool Terrace)
    x0, z0, x1, z1 = -8, -119, 7, -112
    y = 74
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            w.set(x, y, z, *SP_PLANK)
    posts(w, x0, z0, x1, z1, y + 1, y + 9)
    panel_walls(w, x0, z0, x1, z1, y + 1, y + 4, openings=(("s", x0 + 1, x1 - 1), ("e", z0 + 2, z1 - 2),
                                                             ("w", z0 + 2, z1 - 2)))
    for x in range(x0 + 1, x1):                     # the lower storey's south side is open: a rail of fence posts
        pass
    for x in range(x0 - 1, x1 + 2):                 # the skirt roof between the storeys
        w.set(x, y + 5, z0 - 1, DO_STAIRS, 2); w.set(x, y + 5, z1 + 1, DO_STAIRS, 3)
    for z in range(z0, z1 + 1):
        w.set(x0 - 1, y + 5, z, DO_STAIRS, 0); w.set(x1 + 1, y + 5, z, DO_STAIRS, 1)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if x0 < x < x1 and z0 < z < z1:
                w.set(x, y + 5, z, *SP_PLANK)
    panel_walls(w, x0 + 1, z0 + 1, x1 - 1, z1 - 1, y + 6, y + 8)
    posts(w, x0 + 1, z0 + 1, x1 - 1, z1 - 1, y + 6, y + 8, step=3)
    hip_roof(w, x0 - 1, z0 - 1, x1 + 1, z1 + 1, y + 9)
    lanterns_under_eaves(w, x0 - 1, z0 - 1, x1 + 1, z1 + 1, y + 8)
    banner_post(w, -9, y, -111, 0); banner_post(w, 8, y, -111, 0)
    # the pool, a block deep, stepping stones across; lilies
    for x in range(-13, -5):
        for z in range(-108, -101):
            if (x + z) % 5 == 0 and z in (-106, -103):
                w.set(x, 72, z, B.STONE, 6)
            elif x == -10 and z % 2 == 0:
                w.set(x, 72, z, B.STONE, 6)
            else:
                w.set(x, 72, z, B.WATER)
                w.set(x, 71, z, B.DIRT)
                if rng.random() < 0.12:
                    w.set(x, 73, z, B.LILY)
    for x in range(-14, -4):
        for z in (-109, -101):
            w.set(x, 72, z, B.STONE, 5)
    # the outcrop: a karst knuckle four high with a pine on it
    for x in range(6, 12):
        for z in range(-108, -101):
            dx, dz = x - 8.5, z + 104.5
            hh = int(4.2 - 0.55 * (dx * dx + dz * dz) ** 0.5 + rng.random())
            for yy in range(73, 73 + max(0, hh)):
                w.set(x, yy, z, *((B.MOSSY, 0) if rng.random() < 0.3 else (B.STONE, 5 if rng.random() < 0.5 else 0)))
    spruce(w, 8, 76, -105, 8, rng)
    # the lantern towers at the Monument Terrace's ends
    for tx in (-20, 16):
        a, b, c, d = tx, -96, tx + 3, -93
        for x in range(a, c + 1):
            for z in range(b, d + 1):
                w.set(x, 71, z, *SB); w.set(x, 72, z, *SB)
        posts(w, a, b, c, d, 73, 77, step=3)
        for x in range(a + 1, c):
            for z in range(b + 1, d):
                w.set(x, 77, z, B.GLOWSTONE)
        for x in range(a, c + 1):
            for z in (b, d):
                if a < x < c:
                    w.set(x, 74, z, B.DARK_OAK_FENCE)
        for z in range(b, d + 1):
            for x in (a, c):
                if b < z < d:
                    w.set(x, 74, z, B.DARK_OAK_FENCE)
        hip_roof(w, a - 1, b - 1, c + 1, d + 1, 78)
    # the tea beds either side of the monuments
    tea_rows(w, F, -12, -97, -7, -92, along_x=False)
    tea_rows(w, F, 6, -97, 11, -92, along_x=False)
    # stone lanterns at the heads of the two exits
    for x in (-20, -9, 8, 19):
        toro(w, x, 70, -87)
    # the monuments: a jade frame round an empty block, on a pedestal coloured for the wool it waits for
    for m in P.MONUMENTS:
        mx, mz = int(np.floor(m["at"][0])), int(np.floor(m["at"][1]))
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                w.set(mx + dx, 70, mz + dz, *JADE)
        w.set(mx, 70, mz, B.STAINED_CLAY, 0)            # recoloured per monument in gen.py
        for dx, dz in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            w.set(mx + dx, 71, mz + dz, B.SLAB, 5)
        w.set(mx, 71, mz, B.AIR)


def gate(w, F):
    """The gate pavilion over the Gate Terrace's middle: two pairs of posts, a beam, a roof that turns up."""
    y = 65
    for x in (-9, 8):
        for z in (-35, -30):
            for yy in range(y + 1, y + 7):
                w.set(x, yy, z, *DARK_LOG)
    for x in range(-10, 10):
        for z in (-35, -30):
            w.set(x, y + 7, z, *DARK_LOG if x in (-9, 8) else DO_PLANK)
    for z in range(-34, -30):
        for x in (-9, 8):
            w.set(x, y + 7, z, *DO_PLANK)
    for x in range(-8, 8):
        w.set(x, y + 6, -35, *JADE); w.set(x, y + 6, -30, *JADE)
    hip_roof(w, -11, -36, 10, -29, y + 8)
    for x in (-9, 8):
        for z in (-36, -29):
            pass
    lanterns_under_eaves(w, -11, -36, 10, -29, y + 7)
    for x in (-24, -14, 13, 23):
        toro(w, x, y, -37)


def bell_rock(w, F):
    """The bell house on the Bell Rock: four posts, a roof, a bell of gold under it. Built whole: the turn
    of red's half makes the same thing."""
    y = 68
    for (x, z) in ((-4, -4), (3, -4)):
        for yy in range(y + 1, y + 6):
            w.set(x, yy, z, *DARK_LOG)
    for x in range(-4, 4):
        w.set(x, y + 6, -4, *DO_PLANK)
    for z in range(-4, 0):
        w.set(-4, y + 6, z, *DO_PLANK); w.set(3, y + 6, z, *DO_PLANK)
    for x in range(-5, 5):
        for z in range(-5, 0):
            pass
    # the roof's red-half courses (z < 0); the turn completes it
    for k in range(0, 4):
        yy = y + 7 + k
        a, b = -5 + k, 4 - k
        zz = -5 + k
        for x in range(a, b + 1):
            w.set(x, yy, zz, DO_STAIRS, 2)
        for z in range(zz + 1, 0):
            w.set(a, yy, z, DO_STAIRS, 0)
            w.set(b, yy, z, DO_STAIRS, 1)
            for x in range(a + 1, b):
                w.set(x, yy - 1 if k else yy - 1, z, *DO_PLANK)
    w.set(-1, y + 5, -1, B.FENCE); w.set(0, y + 5, -1, B.FENCE)
    w.set(-1, y + 4, -1, B.GOLD_BLOCK); w.set(0, y + 4, -1, B.GOLD_BLOCK)
    w.set(-1, y + 3, -1, B.GOLD_BLOCK); w.set(0, y + 3, -1, B.GOLD_BLOCK)


def shrine(w, F):
    """The Pillar Shrine: an open shrine on the pillar's top, four posts and a roof; the wool on a jade plinth
    in the middle. Open on every side, as its approaches are."""
    x0, z0, x1, z1 = -66, -97, -59, -90
    y = 74
    for (x, z) in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
        for yy in range(y + 1, y + 6):
            w.set(x, yy, z, *DARK_LOG)
    for x in range(x0, x1 + 1):
        for z in (z0, z1):
            w.set(x, y + 6, z, *DO_PLANK)
    for z in range(z0, z1 + 1):
        for x in (x0, x1):
            w.set(x, y + 6, z, *DO_PLANK)
    hip_roof(w, x0 - 1, z0 - 1, x1 + 1, z1 + 1, y + 7)
    lanterns_under_eaves(w, x0 - 1, z0 - 1, x1 + 1, z1 + 1, y + 6)
    wx, wz = int(np.floor(P.WOOLS[0]["at"][0])), int(np.floor(P.WOOLS[0]["at"][1]))
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            w.set(wx + dx, y, wz + dz, *JADE)
    w.set(wx, y + 1, wz, B.WOOL, 5)                         # lime; blue's is recoloured in gen.py


def store(w, F):
    """The Tea Store: a stone storehouse at the head of the road, its door the road's width less two, its
    upper walls white and jade between dark oak posts, chests along the walls, the wool on a shelf at the back."""
    x0, z0, x1, z1 = 47, -100, 66, -87
    y = 70
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if x in (x0, x1) or z in (z0, z1):
                w.set(x, y + 1, z, *SB)                        # one course of stone under the timber
                for yy in range(y + 2, y + 4):
                    w.set(x, yy, z, *SP_PLANK)
    posts(w, x0, z0, x1, z1, y + 4, y + 7, step=5)
    panel_walls(w, x0, z0, x1, z1, y + 4, y + 7, windows=True)
    for x in range(51, 63):                                  # the door, open to the road, 12 wide, 4 high
        for yy in range(y + 1, y + 5):
            w.set(x, yy, z1, B.AIR)
    for x in range(51, 63):
        w.set(x, y + 5, z1, *DARK_LOG)
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
            w.set(x, y + 8, z, *DO_PLANK)
    # a double eave: a skirt two out all round, a clerestory of white and jade, and a smaller roof over it
    skirt_roof(w, x0 - 2, z0 - 2, x1 + 2, z1 + 2, y + 8)
    for x in range(x0 + 2, x1 - 1):
        for z in range(z0 + 2, z1 - 1):
            w.set(x, y + 9, z, *DO_PLANK)
    panel_walls(w, x0 + 3, z0 + 3, x1 - 3, z1 - 3, y + 10, y + 11, windows=False)
    posts(w, x0 + 3, z0 + 3, x1 - 3, z1 - 3, y + 10, y + 11, step=4)
    hip_roof(w, x0 + 2, z0 + 2, x1 - 2, z1 - 2, y + 12)
    lanterns_under_eaves(w, x0 - 2, z0 - 2, x1 + 2, z1 + 2, y + 7)
    # inside: lantern light, shelves of tea, the wool on a jade shelf at the back
    for x in (52, 56, 61):
        w.set(x, y + 7, -94, B.GLOWSTONE)
    for x in range(x0 + 1, x1):
        if x % 2 == 0 and not 54 <= x <= 58:
            w.set(x, y + 1, z0 + 1, B.HAY, 0)
    wx, wz = int(np.floor(P.WOOLS[1]["at"][0])), int(np.floor(P.WOOLS[1]["at"][1]))
    for dx in (-1, 0, 1):
        w.set(wx + dx, y + 1, wz - 1, *JADE)
    w.set(wx, y + 1, wz, B.WOOL, 4)                          # yellow; blue's recoloured
    gear = [(0, "minecraft:iron_chestplate", 1, 0), (1, "minecraft:iron_leggings", 1, 0),
            (2, "minecraft:iron_boots", 1, 0), (3, "minecraft:iron_helmet", 1, 0),
            (4, "minecraft:golden_apple", 2, 0), (5, "minecraft:arrow", 32, 0)]
    w.chest(x0 + 1, y + 1, -93, gear, facing=5)
    w.chest(x1 - 1, y + 1, -93, gear, facing=4)


def store_wall(w, F):
    """The Store's prepared line, as capture boards lay one: two thick, the road's full width, three courses of
    bedrock and one of cobweb, crossed by building over it."""
    wl = P.WALLS[0]
    for x in range(wl["x0"], wl["x1"] + 1):
        for z in (wl["z"], wl["z"] - 1):
            base = floor_y(F, x, z)
            for yy in range(base + 1, base + 4):
                w.set(x, yy, z, B.BEDROCK)
            w.set(x, base + 4, z, B.COBWEB)


def lanes(w, F, rng):
    """Stone lanterns along the lanes, tea along the Long Terrace and in the hub's flanks, pines on the
    islets and at the Arms' ends, mats of tea on the Drying Floor."""
    # the Long Terrace: tea on its north edge, lanterns on its south
    tea_rows(w, F, -88, -73, -46, -71)
    for x in range(-88, -34, 10):
        toro(w, x, 66, -60)
    # the Store Road: lanterns down both sides
    for z in range(-42, -80, -9):
        for x in (50, 63):
            toro(w, x, floor_y(F, x, z), z)
    # the Tea Rows: tea along the south edge
    tea_rows(w, F, 33, -40, 46, -39, along_x=True)
    # the hub: tea in the flanks either side of the sinkhole, lanterns at the ring's corners
    tea_rows(w, F, -30, -74, -16, -69)
    tea_rows(w, F, 15, -74, 29, -69)
    tea_rows(w, F, -30, -48, -16, -42, along_x=False)
    tea_rows(w, F, 15, -48, 29, -42, along_x=False)
    for (x, z) in ((-12, -70), (11, -70), (-12, -47), (11, -47)):
        toro(w, x, 66, z)
    # the Drying Floor: mats of drying tea in a row along its north edge, the middle left clear
    for k, x in enumerate(range(33, 48, 4)):
        for dx in range(3):
            for z in range(-78, -75):
                y = floor_y(F, x + dx, z)
                if w.id(x + dx, y + 1, z) == B.AIR:
                    w.set(x + dx, y + 1, z, B.CARPET, 13 if k % 2 else 12)
    # the frontline: lanterns at the Stairs' heads
    for x in (-27, -12, 11, 26):
        toro(w, x, 64, -25)
    # pines: on the islets, the Arms' far ends, the hub's corners
    for (x, z) in ((-91, -93), (-34, -93), (-29, -76), (28, -76), (-90, -71)):
        spruce(w, x, floor_y(F, x, z), z, int(rng.integers(8, 12)), rng)
    # the Ledges: a fern or two, a mossy stone
    for p in P.PIECES:
        if p["kind"] == "ledge":
            for x in range(int(p["poly"][0][0] + 0.5), int(p["poly"][1][0] + 0.5)):
                for z in range(int(p["poly"][0][1] + 0.5), int(p["poly"][2][1] + 0.5)):
                    if rng.random() < 0.15:
                        w.set(x, p["y"] + 1, z, B.TALLGRASS, 2)


def build(w, F, rng):
    paint(w, F, rng)
    spawn(w, F, rng)
    gate(w, F)
    bell_rock(w, F)
    shrine(w, F)
    store(w, F)
    store_wall(w, F)
    lanes(w, F, rng)
