"""Generate Calcite from the plan's raster: every column built to the floor the checker walked, then the things
a raster cannot hold — the Spring and its tunnels under the lava, the spawn tunnels, the spawns, the pads, the
hills' wool, the derricks — and the quarry's paint.

    python3 gen.py <build-dir>

The raster is the whole board already (it was drawn with its turned twin), so nothing is mirrored here; the
underground pieces are built for red and turned for blue by `both`.
"""
import sys
import time

import numpy as np

import plan as P
from mc import World, B

R = P.build()
K = P.KINDS
TEAM = 14
QSTAIRS = 156                                        # quartz stairs: every made step in the quarry is one stone
DIORITE, POL_DIORITE, STONE, ANDESITE, POL_ANDESITE = (B.STONE, 3), (B.STONE, 4), (B.STONE, 0), (B.STONE, 5), (B.STONE, 6)
QUARTZ = (B.QUARTZ, 0)
GLASS = (B.GLASS, 0)
SLIME = (165, 0)
STAIR_DATA = {"+x": 0, "-x": 1, "+z": 2, "-z": 3}


def cell_pick(x, z, choices, size=3, salt=0):
    h = ((x // size) * 73856093) ^ ((z // size) * 19349663) ^ (salt * 83492791)
    return choices[(h & 0x7fffffff) % len(choices)]


def both(x, z):
    return [(x, z), P.rot(x, z)]


# ---- the paint: one rock, cut in courses ------------------------------------------------------------------
def wall_rock(x, y, z):
    """The quarry's cut faces: diorite and polished diorite in courses, a darker course of stone every fifth,
    a drill line of andesite every fourth column."""
    if (x + z) % 4 == 0 and y % 7 not in (0, 1):
        return ANDESITE
    band = y % 5
    if band == 0:
        return STONE
    if band in (1, 3):
        return POL_DIORITE
    return DIORITE


# each ground its own tone, three blocks a third each in cells of three, so a player knows which level they
# are on by the floor: the Ledge grey, the Bench white, the Rim brightest
FLOORS = {16: [ANDESITE, POL_ANDESITE, STONE], 19: [POL_ANDESITE, STONE, POL_DIORITE],
          22: [DIORITE, POL_DIORITE, STONE], 28: [QUARTZ, POL_DIORITE, DIORITE]}


def floor_block(x, z, kind, h=22):
    if kind == K["spawn"]:
        return (B.STAINED_CLAY, TEAM if x < 0 else 11) if (x // 2 + z // 2) % 2 == 0 else QUARTZ
    choices = FLOORS.get(h) or FLOORS[min(FLOORS, key=lambda k: abs(k - h))]
    return cell_pick(x, z, choices)


# ---- the columns ------------------------------------------------------------------------------------------
def columns(w):
    for i in range(P.NX):
        for j in range(P.NZ):
            x, z = i + P.X_MIN, j + P.Z_MIN
            h, k = int(R.H[i, j]), int(R.K[i, j])
            w.set(x, 0, z, B.BEDROCK)
            if k == K["lava"]:
                for y in range(1, 7):
                    w.set(x, y, z, *STONE)
                for y in range(7, P.LAVA_Y + 1):
                    w.set(x, y, z, B.LAVA)
                continue
            for y in range(1, h + 1):
                w.set(x, y, z, *wall_rock(x, y, z))
            if k == K["wall"]:
                w.set(x, h, z, *(POL_DIORITE if h < P.WALL_Y else DIORITE))
                continue
            if k == K["stair"]:
                w.set(x, h, z, QSTAIRS, STAIR_DATA[R.stair[(x, z)]])
            else:
                w.set(x, h, z, *floor_block(x, z, k, h))


# ---- carving helpers ------------------------------------------------------------------------------------------
def carve_run(w, cells, width_axis, half, lava_glass=True):
    """A tunnel through the rock: for each (x, z, floor) a slice `2*half+1` wide across `width_axis`, air three
    high over the floor, the floor stone brick. Where the slice lies in the lava, the tunnel's walls and roof are
    glass, and the glass stands above the lava wherever the tunnel rises out of it."""
    for x, z, f in cells:
        for o in range(-half, half + 1):
            cx, cz = (x + o, z) if width_axis == "x" else (x, z + o)
            in_lava = R.K[P.ix(cx), P.iz(cz)] == K["lava"]
            for y in range(f + 1, f + 4):
                w.set(cx, y, cz, B.AIR)
            w.set(cx, f, cz, B.STONEBRICK, 0)
            if in_lava and lava_glass:
                w.set(cx, f + 4, cz, *GLASS)
                for y in range(f + 5, P.LAVA_Y + 1):
                    w.set(cx, y, cz, B.LAVA)
            elif w.id(cx, f + 4, cz) == B.AIR:
                pass
        # the tube's sides in the lava
        if lava_glass:
            for o in (-half - 1, half + 1):
                cx, cz = (x + o, z) if width_axis == "x" else (x, z + o)
                if R.K[P.ix(cx), P.iz(cz)] == K["lava"]:
                    for y in range(f, f + 5):
                        w.set(cx, y, cz, *GLASS)


def stair_run(w, cells, width_axis, half, rises):
    """Stairs on a carved run: the floor block of each cell a quartz stair rising `rises`."""
    for x, z, f in cells:
        for o in range(-half, half + 1):
            cx, cz = (x + o, z) if width_axis == "x" else (x, z + o)
            w.set(cx, f, cz, QSTAIRS, STAIR_DATA[rises])


def turned(cells):
    return [(*P.rot(x, z), f) for x, z, f in cells]


def turned_dir(r):
    return {"+x": "-x", "-x": "+x", "+z": "-z", "-z": "+z"}[r]


# ---- the Spring and its tunnels -----------------------------------------------------------------------------
def spring(w):
    """The room under the Middle: two stairwells down from the apron, the apples' plinth in the middle, and a
    glass tunnel north and south under the lava that forks and climbs a trench either side of a side hill's
    front stair."""
    f = P.SPRING["floor"]
    for x in range(-4, 4):
        for z in range(-4, 4):
            w.set(x, f, z, *cell_pick(x, z, [POL_ANDESITE, (B.STONEBRICK, 0)], 2))
            for y in range(f + 1, P.SPRING["ceil"]):
                w.set(x, y, z, B.AIR)
    for x, z in ((-1, -1), (0, -1), (-1, 0), (0, 0)):
        w.set(x, f, z, B.GOLD_BLOCK)
    for x in (-4, 3):
        for z in (-4, 3):
            w.set(x, P.SPRING["ceil"] - 1, z, 169, 0)               # sea lanterns in the corners
    # the stairwells: west, from the apron at x -9 down east into the room; and its turn, east
    west = [(x, 4, 18 - (x + 9)) for x in range(-9, -4)]            # 18 at -9 .. 14 at -5
    for cells in (west, turned(west)):
        rises = "-x" if cells is west else "+x"
        for x, z, fl in cells:
            for o in (-1, 0, 1):
                top = int(R.H[P.ix(x), P.iz(z + o)])
                # under the apron the well is open to the sky; under the rings it keeps their floors as its roof
                hi = top if top == 19 else min(fl + 3, top - 1)
                for y in range(fl + 1, hi + 1):
                    w.set(x, y, z + o, B.AIR)
        stair_run(w, cells, "z", 1, rises)
    # the tunnel north: out of the room's north wall at x -2..0, down to 6, then the fork along the lava floor
    down = [(-1, z, 13 - (-4 - z)) for z in range(-5, -12, -1)]     # 12 at -5 .. 6 at -11
    fork = [(x, -12, 6) for x in range(-7, 7)]
    up_e = [(6, z, f_) for z, f_ in ((-13, 6), (-14, 7), (-15, 8), (-16, 9), (-17, 10), (-18, 10), (-19, 10))]
    up_w = [(-7, z, f_) for _, z, f_ in up_e]
    for run, axis, rises in ((down, "x", "+z"), (fork, "z", None), (up_e, "x", "-z"), (up_w, "x", "-z")):
        for cells, r in ((run, rises), (turned(run), turned_dir(rises) if rises else None)):
            carve_run(w, cells, axis, 1)
            if r:
                # a stair wherever the floor changes from the cell before it; the room's floor is the first "before"
                prev, steps = 13, []
                for c in cells:
                    if c[2] != prev:
                        steps.append(c)
                    prev = c[2]
                stair_run(w, steps, axis, 1, r)
    # the fork's floor under the room's centre line is flat: the down-run ends on it
    # the trench above the tunnels' tops is open: the raster carries its stairs at 11 .. 16


def spawn_tunnels(w):
    """Red's tunnel: from the spawn's north wall, down inside the quarry wall to the Ledge's north-west corner;
    blue's is its turn."""
    down = [(-50, z, 28 - (-7 - z)) for z in range(-7, -20, -1)]    # 28 at -7 .. 16 at -19
    along = [(x, -21, 16) for x in range(-50, -29)]
    for cells, axis, r in ((down, "x", "+z"), (along, "z", None)):
        for cs, rr in ((cells, r), (turned(cells), turned_dir(r) if r else None)):
            carve_run(w, cs, axis, 1, lava_glass=False)
            if rr:
                stair_run(w, cs, axis, 1, rr)
    for cs in ([(-50, z, 16) for z in range(-21, -19)], turned([(-50, z, 16) for z in range(-21, -19)])):
        carve_run(w, cs, "x", 1, lava_glass=False)
    # lights along the tunnel
    for x in range(-48, -30, 5):
        for (a, b) in both(x, -23):
            w.set(a, 18, b, 169, 0)


# ---- the made things on the surface -------------------------------------------------------------------------
def spawns(w):
    """The spawn huts: cut into the wall, a roof at 33, open to the Rim, the team's colour in the floor and the
    lintel."""
    for (x0, x1, z0, z1) in ((-55, -46, -6, 5), R._rot(-55, -46, -6, 5)):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                for y in range(29, 33):
                    w.set(x, y, z, B.AIR)
                w.set(x, 33, z, *POL_DIORITE)
        lint = x1 if x0 < 0 else x0
        for z in range(z0, z1 + 1):
            w.set(lint, 32, z, B.STAINED_CLAY, TEAM if x0 < 0 else 11)
        for z in (z0 + 2, z1 - 2):
            w.set((x0 + x1) // 2, 32, z, 169, 0)


def hills(w):
    """The hills' tops: polished diorite with a ring of white wool round the edge, which turns the holder's
    colour."""
    for hd in P.HILLS:
        x0, x1, z0, z1 = hd["box"]
        y = hd["y"]
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                ring = x in (x0, x1) or z in (z0, z1)
                w.set(x, y, z, *((B.WOOL, 0) if ring else POL_DIORITE))


def pads(w):
    """Slime pads where the plan put them, and each one's twin."""
    for pd in P.PADS:
        x0, x1, z0, z1, y = pd["cells"]
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                for a, b in both(x, z):
                    w.set(a, y, b, *SLIME)


def arrows(w):
    for x, y, z in P.ARROWS_AT:
        bx, bz = int(np.floor(x)), int(np.floor(z))
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                w.set(bx + dx, 16, bz + dz, *POL_ANDESITE)
        w.set(bx, 16, bz, B.DISPENSER, 1)


def pillars(w):
    """The parkour and the diagonal steps: columns of quartz from the lava's floor, capped in polished diorite;
    where the Spring's tunnel runs under one, the column stands on the tunnel's glass."""
    for i in range(P.NX):
        for j in range(P.NZ):
            if R.K[i, j] != K["floor"]:
                continue
            x, z = i + P.X_MIN, j + P.Z_MIN
            near_lava = any(R.K[P.ix(x + dx), P.iz(z + dz)] == K["lava"] for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))
                            if 0 <= P.ix(x + dx) < P.NX and 0 <= P.iz(z + dz) < P.NZ)
            if near_lava and R.H[i, j] in (17, 18, 19) and not (-9 <= x <= 8 and -9 <= z <= 8) and not (-23 <= x <= -10 and -2 <= z <= 1) \
                    and not (9 <= x <= 22 and -2 <= z <= 1):
                for y in range(1, int(R.H[i, j])):
                    if w.id(x, y, z) not in (B.AIR, B.GLASS):
                        w.set(x, y, z, *QUARTZ)
                w.set(x, int(R.H[i, j]), z, *POL_DIORITE)


def derricks(w):
    """Timber derricks at the Rim's four corners: a mast, a jib over the bowl, a hanging block. Landmarks."""
    for (cx, cz, dx, dz) in ((-42, -38, 1, 1), (41, -38, -1, 1)):
        for (x, z, ddx, ddz) in ((cx, cz, dx, dz), (*P.rot(cx, cz), -dx, -dz)):
            for y in range(29, 41):
                w.set(x, y, z, B.LOG2, 1)
            for k in range(1, 9):
                w.set(x + ddx * k, 40 - k // 3, z + ddz * k, B.DARK_OAK_FENCE)
            for y in range(32, 37):
                w.set(x + ddx * 8, y, z + ddz * 8, B.FENCE)
            w.set(x + ddx * 8, 31, z + ddz * 8, *POL_ANDESITE)
            for a in (-1, 1):
                w.set(x + a, 29, z, B.LOG2, 1 + 4)
                w.set(x, 29, z + a, B.LOG2, 1 + 8)


def rails(w):
    """Iron bars where a fall is not the point: along the causeways' sides over the lava."""
    for x in range(-23, -12):
        for z in (-3, 2):
            for a, b in both(x, z):
                w.set(a, 17, b, B.IRON_BARS)


def make():
    w = World(P.X_MIN, P.Z_MIN, P.NX, P.NZ, sy=64)
    columns(w)
    spring(w)
    spawn_tunnels(w)
    spawns(w)
    hills(w)
    pads(w)
    arrows(w)
    pillars(w)
    derricks(w)
    rails(w)
    w.biome[:, :] = 1
    return w


def main(build):
    t0 = time.time()
    w = make()
    w.save(build, "Calcite", (0, 45, 0))
    print(f"generated and saved {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
