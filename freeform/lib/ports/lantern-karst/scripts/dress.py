"""What stands on the islands of Lantern Karst, on red's half (gen.py turns it onto blue's): the paint of the
floors, the paths, the joins, the pavilions (the Pavilion of Arrival and its lantern towers, the Gate, the Bell
Rock's bell house, the Pillar Shrine, the Tea Store), the bedrock wall, and the dressing (tea, stone lanterns,
pines, ferns, iron, banners).

Pavilions are spruce and dark oak: dark oak log posts, white panels (white stained clay) banded in jade
(prismarine bricks), hip roofs of dark oak stairs (the studio's RoofField) with their corners turned up.
Lanterns are glowstone. Red and blue appear only on the teams' banners.
"""
import numpy as np

import plan  # noqa: F401  (puts the library on the path)

from pgmvox import B, noise
from pgmvox import build as BLD
from pgmvox import facade as F
from pgmvox import route
from pgmvox.orient import stair as stair_data

DARK_LOG = (B.LOG2, 1)
SPRUCE_LOG = (B.LOG, 1)
WHITE = (B.STAINED_CLAY, 0)
JADE = (B.PRISMARINE, 1)
DO_PLANK = (B.PLANKS, 5)
DO_SLAB = (B.WOOD_SLAB, 5)
SP_PLANK = (B.PLANKS, 1)
SB = (B.STONEBRICK, 0)
PAVE = [(B.STONEBRICK, 0), (B.STONE, 6), (B.STONE, 5), (B.STONE, 0)]
PATH = ((B.DIRT, 0), (B.DIRT, 1), (B.PLANKS, 1))
TEA = (B.LEAVES, 3 | 4)


class Ground:
    """The plan's floors over the world, red's half: what the dressing asks of a column."""

    def __init__(self, R, w):
        self.R, self.w = R, w
        self.floor = np.where(R.piece == R.kinds["void"], -1, R.floor)
        self.piece = R.piece
        self.red = R.Z < 0
        self.land = (self.piece != R.kinds["void"]) & self.red

    def at(self, x, z):
        return int(self.floor[self.R.ix(x), self.R.iz(z)])

    def key(self, x, z):
        return self.R.names[int(self.piece[self.R.ix(x), self.R.iz(z)])]

    def on_land(self, x, z):
        return self.R.inside(x, z) and bool(self.land[self.R.ix(x), self.R.iz(z)])


def cell_pick(x, z, choices, size=3, salt=0):
    h = ((x // size) * 73856093) ^ ((z // size) * 19349663) ^ (salt * 83492791)
    return choices[(h & 0x7fffffff) % len(choices)]


# ---- the floors -----------------------------------------------------------------------------------------
def paved(g, x, z):
    k = g.key(x, z)
    cls = {"neck-w", "neck-e", "sp-front", "sp-mid", "sp-back", "bar", "road", "store", "pillar", "bell"}
    if k in cls:
        return True
    if k == "hub":
        dx, dz = max(-8 - x, x - 7, 0), max(-66 - z, z + 51, 0)
        return 1 <= max(dx, dz) <= 3
    return False


# The paths: every walk a player makes, spawn to the front, to each wool room and out to every bridging edge,
# wandering two and a half blocks either side over fourteen, easing to nothing at their ends.
STROKES = [
    [(-14.5, -79), (-16, -70), (-26, -66.5), (-50, -66.5), (-86, -66.5)],
    [(-60, -66.5), (-86, -66.5), (-87.5, -96)],
    [(-37.5, -74), (-37.5, -96)],
    [(13.5, -79), (16, -70), (30, -71), (44, -72), (50, -72)],
    [(16, -70), (22, -55), (30, -44.5), (50, -44.5)],
    [(-14.5, -79), (-18, -60), (-19.5, -40), (-19.5, -38)],
    [(13.5, -79), (17, -60), (18.5, -40), (18.5, -38)],
    [(-19.5, -27), (-19.5, -13)], [(18.5, -27), (18.5, -13)],
]


def wander(pts, amp=2.5, period=14.0, ease=6.0):
    """A stroke resampled a block at a time and bent sideways by a sine that eases to nothing at its ends."""
    dense = []
    for a, b in zip(pts, pts[1:]):
        n = max(1, int(np.hypot(b[0] - a[0], b[1] - a[1])))
        dense += [(a[0] + (b[0] - a[0]) * t / n, a[1] + (b[1] - a[1]) * t / n) for t in range(n)]
    dense.append(pts[-1])
    d = np.array(dense)
    s = np.arange(len(d))
    e = np.minimum(1, np.minimum(s, len(d) - 1 - s) / ease)
    tan = np.gradient(d, axis=0)
    nrm = np.stack([-tan[:, 1], tan[:, 0]], 1)
    nrm /= np.maximum(1e-9, np.linalg.norm(nrm, axis=1))[:, None]
    return [tuple(p) for p in d + nrm * (amp * np.sin(2 * np.pi * s / period) * e)[:, None]]


def paint(w, g, rng):
    """The top of every land column: paths (route.pave over the plan's floors), built floors paved in cells of
    three, the rest grass with about 7% in coarse-dirt patches."""
    X, Z = w.grid()
    H = np.where(g.land, g.floor, -1)
    for k, pts in enumerate(STROKES):
        route.pave(w, H, X, Z, wander(pts), width=3.4, surface=PATH, weights=(1, 1, 1), clear=0, seed=k)
    patch = noise.fbm(H.shape, 5, 2, seed=21)
    cut = np.percentile(patch[g.land], 93)
    for i, k in np.argwhere(g.land):
        x, z, h = int(X[i, k]), int(Z[i, k]), int(H[i, k])
        if paved(g, x, z):
            w.set(x, h, z, *cell_pick(x, z, PAVE))
        elif w.id(x, h, z) == B.GRASS and patch[i, k] > cut:
            w.set(x, h, z, B.DIRT, 1)


def joins(w, g, R, walls):
    """The plan's stair flights, their retaining walls, and a row of slabs on the low side of every one-block
    step between pieces."""
    for (x, z), d in R.stair.items():
        if z < 0:
            w.set(x, R.h(x, z), z, B.STONEBRICK_STAIRS, stair_data(d))
    for x, z in walls:
        h = g.at(x, z)
        w.set(x, h, z, *SB)
        w.set(x, h - 1, z, *SB)
    n = 0
    for i, k in np.argwhere(g.land):
        x, z = int(R.X[i, k]), int(R.Z[i, k])
        h = int(g.floor[i, k])
        if (x, z) in R.stair:
            continue
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if g.on_land(x + dx, z + dz) and g.at(x + dx, z + dz) == h + 1 and (x + dx, z + dz) not in R.stair \
                    and w.id(x, h + 1, z) == B.AIR:
                w.set(x, h + 1, z, B.SLAB, 5)
                n += 1
                break
    return n


# ---- the parts -----------------------------------------------------------------------------------------
def posts(w, x0, z0, x1, z1, y0, y1, step=4, log=DARK_LOG):
    for x in sorted(set(range(x0, x1 + 1, step)) | {x1}):
        for z in (z0, z1):
            w.column(x, z, y0, y1, *log)
    for z in sorted(set(range(z0, z1 + 1, step)) | {z1}):
        for x in (x0, x1):
            w.column(x, z, y0, y1, *log)


def roof(w, box, base_y, overhang=1, upturn=True):
    """A hip roof of dark oak over a wall line: the studio's RoofField laid as its stamper lays it, the four
    corners of the eave turned up a block (upside-down stairs) as a pavilion's are."""
    f = BLD.RoofField("hip", box, overhang=overhang, base_y=base_y)
    BLD.lay_roof(w, f, DO_PLANK, B.DARK_OAK_STAIRS, DO_SLAB)
    if upturn:
        x0, z0, x1, z1 = box[0] - overhang, box[1] - overhang, box[2] + overhang, box[3] + overhang
        for x, z, rises in ((x0, z0, "s"), (x1, z0, "s"), (x0, z1, "n"), (x1, z1, "n")):
            w.set(x, f.crown(x, z) + 1, z, B.DARK_OAK_STAIRS, stair_data(rises, upside_down=True))
    return f


def eave(w, x0, z0, x1, z1, y):
    """A skirt of eave: two courses of dark oak stairs stepping up and in."""
    for k in range(2):
        a, b, c, d = x0 + k, z0 + k, x1 - k, z1 - k
        for x in range(a, c + 1):
            w.set(x, y + k, b, B.DARK_OAK_STAIRS, stair_data("s"))
            w.set(x, y + k, d, B.DARK_OAK_STAIRS, stair_data("n"))
        for z in range(b + 1, d):
            w.set(a, y + k, z, B.DARK_OAK_STAIRS, stair_data("e"))
            w.set(c, y + k, z, B.DARK_OAK_STAIRS, stair_data("w"))


def panel_walls(w, box, y0, y1, open_sides=(), windows=True, post_every=4):
    """White panels between dark oak posts, a jade band one course up, panes for windows, sides in open_sides
    ("n", "s", "w", "e") left open below the head: facade.extrude over the box, patterns in order of
    precedence. A pattern is not told which way its face looks, so the face numbers are read from
    facade.faces first."""
    x0, z0, x1, z1 = box
    cells = F.rect_cells(x0, z0, x1, z1)
    runs, _ = F.faces(cells)
    side = {n: {(1, 0): "e", (-1, 0): "w", (0, 1): "s", (0, -1): "n"}[normal] for n, (normal, _) in enumerate(runs)}
    pats = [
        lambda s, run, t, h, n: ("accent", (B.AIR, 0)) if side[n] in open_sides and 0 < s < run - 1 and t <= 3
        else None,
        lambda s, run, t, h, n: ("accent", DARK_LOG) if s % post_every == post_every - 1 else None,
        lambda s, run, t, h, n: ("accent", JADE) if t == 1 else None,
    ]
    if windows:
        pats.append(F.windows(4, 2, 3))
    pats.append(lambda s, run, t, h, n: ("accent", WHITE))
    F.extrude(w, cells, y0, y1, faces_=pats, fill=False)
    for x, z in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
        w.column(x, z, y0, y1, *DARK_LOG)


def lanterns_under(w, x0, z0, x1, z1, y):
    for x, z in ((x0 - 1, z0 - 1), (x1 + 1, z0 - 1), (x0 - 1, z1 + 1), (x1 + 1, z1 + 1)):
        w.set(x, y, z, B.DARK_OAK_FENCE)
        w.set(x, y - 1, z, B.GLOWSTONE)


def toro(w, x, y, z):
    """A stone lantern on a floor at y: a chiselled foot, a wall post, the light, a slab cap."""
    w.set(x, y + 1, z, B.STONEBRICK, 3)
    w.set(x, y + 2, z, B.COBBLE_WALL, 0)
    w.set(x, y + 3, z, B.GLOWSTONE)
    w.set(x, y + 4, z, B.SLAB, 5)


def pine(w, x, y, z, height):
    """A karst pine on a floor at y: a spruce trunk in cones of leaves shrinking to a point."""
    w.column(x, z, y + 1, y + height, *SPRUCE_LOG)
    r = 3 if height >= 9 else 2
    for yy in range(y + 3, y + height + 1, 2):
        rr = max(1, round(r * (1 - (yy - y - 3) / max(1, height - 2)) + 0.4))
        for dx in range(-rr, rr + 1):
            for dz in range(-rr, rr + 1):
                if abs(dx) + abs(dz) <= rr + (rr > 1) and (dx or dz) and w.id(x + dx, yy, z + dz) == B.AIR:
                    w.set(x + dx, yy, z + dz, B.LEAVES, 1 | 4)
    w.column(x, z, y + height + 1, y + height + 2, B.LEAVES, 1 | 4)


def tea(w, g, x0, z0, x1, z1, axis="z"):
    """Rows of tea, one high, a walking gap of two between rows: facade.stripes laid by facade.carpet, kept to
    grass (a carpet lays one course, so each cell is checked against the floor under it)."""
    rows = F.stripes(3, 1, TEA, axis)

    def field(c):
        if not g.on_land(c.x, c.z):
            return None
        h = g.at(c.x, c.z)
        return rows(c) if h + 1 == y and w.id(c.x, h, c.z) == B.GRASS else None
    ys = {g.at(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1) if g.on_land(x, z)}
    for h in ys:
        y = h + 1
        F.carpet(w, x0, z0, x1, z1, y, field)


def entrance_line(w, cells, y):
    """A wool room's entrance marker: a redstone line on the room's last row, a redstone torch at either end."""
    for k, (x, z) in enumerate(cells):
        w.set(x, y, z, *((B.REDSTONE_TORCH, 5) if k in (0, len(cells) - 1) else (B.REDSTONE_WIRE, 0)))


def iron(w, cx, y, cz):
    w.fill(cx - 1, y + 1, cz - 1, cx + 1, y + 3, cz + 1, B.IRON_BLOCK)


def banner_post(w, x, y, z, rot=0):
    """A team banner (red's, base 1) on a spruce pole; gen.py recolours the turned copy on blue's half."""
    w.column(x, z, y + 1, y + 3, B.SPRUCE_FENCE)
    w.banner(x, y + 4, z, 1, rot=rot)


# ---- the places ----------------------------------------------------------------------------------------
def spawn(w, g, rng):
    """The Pavilion of Arrival, the pool, the outcrop, the two lantern towers, the tea beds, the iron, the stone
    lanterns at the exits, the monuments' jade frames."""
    x0, z0, x1, z1, y = -8, -119, 7, -112, 74
    w.fill(x0, y, z0, x1, y, z1, *SP_PLANK)
    panel_walls(w, (x0, z0, x1, z1), y + 1, y + 4, open_sides=("s", "e", "w"))
    eave(w, x0 - 1, z0 - 1, x1 + 1, z1 + 1, y + 5)
    w.fill(x0 + 1, y + 5, z0 + 1, x1 - 1, y + 5, z1 - 1, *SP_PLANK)
    panel_walls(w, (x0 + 1, z0 + 1, x1 - 1, z1 - 1), y + 6, y + 8, post_every=3)
    roof(w, (x0, z0, x1, z1), y + 9)
    lanterns_under(w, x0 - 1, z0 - 1, x1 + 1, z1 + 1, y + 8)
    banner_post(w, -9, y, -111, rot=0)
    banner_post(w, 8, y, -111, rot=0)
    for x in range(-13, -5):                                 # the pool, a block deep, stepping stones across
        for z in range(-108, -101):
            if ((x + z) % 5 == 0 and z in (-106, -103)) or (x == -10 and z % 2 == 0):
                w.set(x, 72, z, B.STONE, 6)
            else:
                w.set(x, 72, z, B.WATER)
                w.set(x, 71, z, B.DIRT)
                if rng.random() < 0.12:
                    w.set(x, 73, z, B.LILY)
    for x in range(-14, -4):
        for z in (-109, -101):
            w.set(x, 72, z, B.STONE, 5)
    for x in range(6, 12):                                   # the outcrop: a karst knuckle with a pine on it
        for z in range(-108, -101):
            hh = int(4.2 - 0.55 * np.hypot(x - 8.5, z + 104.5) + rng.random())
            for yy in range(73, 73 + max(0, hh)):
                w.set(x, yy, z, *((B.MOSSY, 0) if rng.random() < 0.3 else (B.STONE, 5 if rng.random() < 0.5 else 0)))
    pine(w, 8, 76, -105, 8)
    for tx in (-20, 16):                                     # the lantern towers at the Monument Terrace's ends
        a, b, c, d = tx, -96, tx + 3, -93
        w.fill(a, 71, b, c, 72, d, *SB)
        posts(w, a, b, c, d, 73, 77, step=3)
        w.fill(a + 1, 77, b + 1, c - 1, 77, d - 1, B.GLOWSTONE)
        for x in range(a + 1, c):
            w.set(x, 74, b, B.DARK_OAK_FENCE)
            w.set(x, 74, d, B.DARK_OAK_FENCE)
        for z in range(b + 1, d):
            w.set(a, 74, z, B.DARK_OAK_FENCE)
            w.set(c, 74, z, B.DARK_OAK_FENCE)
        roof(w, (a, b, c, d), 78)
    tea(w, g, -12, -97, -7, -92, "x")
    tea(w, g, 6, -97, 11, -92, "x")
    iron(w, -15, 72, -104)
    iron(w, 14, 72, -104)
    for x in (-20, -9, 8, 19):
        toro(w, x, 70, -87)
    for mx in (-4, 3):                                       # the monuments' frames; the slot is the objective's
        w.fill(mx - 1, 70, -90, mx + 1, 70, -88, *JADE)
        for dx, dz in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            w.set(mx + dx, 71, -89 + dz, B.SLAB, 5)


def gate(w):
    y = 65
    for x in (-9, 8):
        for z in (-35, -30):
            w.column(x, z, y + 1, y + 6, *DARK_LOG)
    for x in range(-10, 10):
        for z in (-35, -30):
            w.set(x, y + 7, z, *(DARK_LOG if x in (-9, 8) else DO_PLANK))
    for x in range(-8, 8):
        w.set(x, y + 6, -35, *JADE)
        w.set(x, y + 6, -30, *JADE)
    roof(w, (-10, -35, 9, -30), y + 8)
    lanterns_under(w, -11, -36, 10, -29, y + 7)
    for x in (-24, -14, 13, 23):
        toro(w, x, y, -37)


def bell_rock(w):
    """The bell house, built whole across the axis; the turn of red's half rebuilds the south half the same."""
    y = 68
    for x, z in ((-4, -4), (3, -4), (-4, 3), (3, 3)):
        w.column(x, z, y + 1, y + 5, *DARK_LOG)
    for x in range(-4, 4):
        w.set(x, y + 6, -4, *DO_PLANK)
        w.set(x, y + 6, 3, *DO_PLANK)
    for z in range(-4, 4):
        w.set(-4, y + 6, z, *DO_PLANK)
        w.set(3, y + 6, z, *DO_PLANK)
    roof(w, (-4, -4, 3, 3), y + 7)
    for x, z in ((-1, -1), (0, -1), (-1, 0), (0, 0)):
        w.set(x, y + 5, z, B.FENCE)
        w.column(x, z, y + 3, y + 4, B.GOLD_BLOCK)


def shrine(w, wool_at):
    """The Pillar Shrine: four posts, a beam ring, a hip roof; the wool's jade plinth; an entrance line on every
    side, since every side faces the pit's build zone."""
    x0, z0, x1, z1, y = -66, -97, -59, -90, 74
    for x, z in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
        w.column(x, z, y + 1, y + 5, *DARK_LOG)
    for x in range(x0, x1 + 1):
        w.set(x, y + 6, z0, *DO_PLANK)
        w.set(x, y + 6, z1, *DO_PLANK)
    for z in range(z0, z1 + 1):
        w.set(x0, y + 6, z, *DO_PLANK)
        w.set(x1, y + 6, z, *DO_PLANK)
    roof(w, (x0, z0, x1, z1), y + 7)
    lanterns_under(w, x0 - 1, z0 - 1, x1 + 1, z1 + 1, y + 6)
    wx, _, wz = wool_at
    w.fill(wx - 1, y, wz - 1, wx + 1, y, wz + 1, *JADE)
    for cells in ([(x, z0) for x in range(x0 + 1, x1)], [(x, z1) for x in range(x0 + 1, x1)],
                  [(x0, z) for z in range(z0 + 1, z1)], [(x1, z) for z in range(z0 + 1, z1)]):
        entrance_line(w, cells, y + 1)


GEAR = [(0, "minecraft:iron_chestplate", 1, 0), (1, "minecraft:iron_leggings", 1, 0),
        (2, "minecraft:iron_boots", 1, 0), (3, "minecraft:iron_helmet", 1, 0),
        (4, "minecraft:golden_apple", 2, 0), (5, "minecraft:arrow", 32, 0)]


def store(w, wool_at, door=(51, 62)):
    """The Tea Store: a course of stone brick under spruce, white and jade panels between posts above, the door
    the road's width less two, a double eave and a clerestory under a hip roof; chests of better gear, the wool
    on a jade shelf at the back."""
    x0, z0, x1, z1, y = 47, -110, 66, -97, 70
    ring = [(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1) if x in (x0, x1) or z in (z0, z1)]
    for x, z in ring:
        w.set(x, y + 1, z, *SB)
        w.column(x, z, y + 2, y + 3, *SP_PLANK)
    panel_walls(w, (x0, z0, x1, z1), y + 4, y + 7, post_every=5)
    for x in range(door[0], door[1] + 1):
        w.column(x, z1, y + 1, y + 4, B.AIR)
        w.set(x, y + 5, z1, *DARK_LOG)
    w.fill(x0 + 1, y + 8, z0 + 1, x1 - 1, y + 8, z1 - 1, *DO_PLANK)
    eave(w, x0 - 2, z0 - 2, x1 + 2, z1 + 2, y + 8)
    w.fill(x0 + 2, y + 9, z0 + 2, x1 - 2, y + 9, z1 - 2, *DO_PLANK)
    panel_walls(w, (x0 + 3, z0 + 3, x1 - 3, z1 - 3), y + 10, y + 11, windows=False)
    roof(w, (x0 + 3, z0 + 3, x1 - 3, z1 - 3), y + 12)
    lanterns_under(w, x0 - 2, z0 - 2, x1 + 2, z1 + 2, y + 7)
    for x in (52, 56, 61):
        w.set(x, y + 7, (z0 + z1) // 2, B.GLOWSTONE)
    for x in range(x0 + 1, x1):
        if x % 2 == 0 and not 54 <= x <= 58:
            w.set(x, y + 1, z0 + 1, B.HAY, 0)
    wx, _, wz = wool_at
    for dx in (-1, 0, 1):
        w.set(wx + dx, y + 1, wz - 1, *JADE)
    w.chest(x0 + 1, y + 1, (z0 + z1) // 2 + 1, GEAR, facing=5)
    w.chest(x1 - 1, y + 1, (z0 + z1) // 2 + 1, GEAR, facing=4)
    entrance_line(w, [(x, z1) for x in range(door[0], door[1] + 1)], y + 1)


def store_wall(w, g, wall):
    """Two thick, the road's width: three courses of bedrock and one of cobweb, crossed by building."""
    for x in range(wall["x0"], wall["x1"] + 1):
        for z in range(wall["z0"], wall["z1"] + 1):
            h = g.at(x, z)
            w.column(x, z, h + 1, h + wall["height"], B.BEDROCK)
            w.set(x, h + wall["height"] + 1, z, B.COBWEB)


def lanes(w, g, rng):
    """Tea along the Long Terrace and the hub's flanks, lanterns along the lanes, pines at the Arms' ends and
    the hub's corners, mats of drying tea on the Drying Floor, ferns on the Ledges."""
    tea(w, g, -88, -73, -46, -71, "z")
    for x in range(-88, -34, 10):
        toro(w, x, 66, -60)
    for z in range(-42, -80, -9):
        for x in (50, 63):
            toro(w, x, g.at(x, z), z)
    tea(w, g, 33, -40, 46, -39, "z")
    tea(w, g, -30, -74, -16, -69, "z")
    tea(w, g, 15, -74, 29, -69, "z")
    tea(w, g, -30, -48, -16, -42, "x")
    tea(w, g, 15, -48, 29, -42, "x")
    for x, z in ((-12, -70), (11, -70), (-12, -47), (11, -47)):
        toro(w, x, 66, z)
    mats = lambda c: (B.CARPET, 13 if ((c.x - 33) // 4) % 2 else 12) if (c.x - 33) % 4 < 3 else None  # noqa: E731
    for xa, xb in ((33, 37), (38, 43), (44, 47)):            # one carpet per course of the Drying Floor's ramp
        F.carpet(w, xa, -78, xb, -76, g.at(xa, -78) + 1, mats)
    for x in (-27, -12, 11, 26):
        toro(w, x, 64, -25)
    for x, z in ((-91, -93), (-34, -93), (-29, -76), (28, -76), (-90, -71)):
        pine(w, x, g.at(x, z), z, int(rng.integers(8, 12)))
    for x in range(-75, -49):
        for z in range(-82, -75):
            if g.on_land(x, z) and g.key(x, z).startswith("ledge") and rng.random() < 0.15:
                w.set(x, 47, z, B.TALLGRASS, 2)


def ferns(w, g, rng):
    """Ferns and grass on about 6% of the grass, never within two of a rim a bridger leaves from."""
    from pgmvox.shapes import edge_depth
    ed = edge_depth(g.land)
    X, Z = w.grid()
    n = 0
    for i, k in np.argwhere(g.land & (ed > 1)):
        x, z, h = int(X[i, k]), int(Z[i, k]), int(g.floor[i, k])
        if w.id(x, h, z) != B.GRASS or w.id(x, h + 1, z) != B.AIR:
            continue
        r = rng.random()
        if r < 0.035:
            w.set(x, h + 1, z, B.TALLGRASS, 2)
        elif r < 0.045 and w.id(x, h + 2, z) == B.AIR:
            w.set(x, h + 1, z, B.DOUBLE_PLANT, 3)
            w.set(x, h + 2, z, B.DOUBLE_PLANT, 8)
        elif r < 0.06:
            w.set(x, h + 1, z, B.TALLGRASS, 1)
        else:
            continue
        n += 1
    return n
