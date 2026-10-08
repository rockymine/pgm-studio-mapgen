"""Generate Calcite from the plan's raster: every column built to the floor the checker walked, then the things
a raster cannot hold — the Spring and its tunnels under the lava, the spawn tunnels, the spawns, the pads, the
hills' wool, the derricks — and the quarry's paint and its team colours.

    python3 gen.py <build-dir>

The raster is the whole board already (it was drawn with its turned twin), so nothing is mirrored here; the
underground pieces are built for red and turned for blue.
"""
import sys
import time

import numpy as np

import plan as P
from mc import World, B

R = P.build()
K = P.KINDS
QSTAIRS = 156                                        # quartz stairs: every made step in the quarry is one stone
DIORITE, POL_DIORITE, STONE, ANDESITE, POL_ANDESITE = (B.STONE, 3), (B.STONE, 4), (B.STONE, 0), (B.STONE, 5), (B.STONE, 6)
QUARTZ = (B.QUARTZ, 0)
GLASS = (B.GLASS, 0)
SLIME = (165, 0)
STAIR_DATA = {"+x": 0, "-x": 1, "+z": 2, "-z": 3}
TF = P.TUNNEL_FLOOR


def team_of(x):
    """Red holds the west half, blue the east: the colour a block takes on each team's side."""
    return 14 if x < 0 else 11


def cell_pick(x, z, choices, size=3, salt=0):
    h = ((x // size) * 73856093) ^ ((z // size) * 19349663) ^ (salt * 83492791)
    return choices[(h & 0x7fffffff) % len(choices)]


# ---- the paint: one rock, cut in courses, and a team band in every face -----------------------------------
def wall_rock(x, y, z):
    """The quarry's cut faces: diorite and polished diorite in courses, a darker course of stone every fifth,
    a drill line of andesite every fourth column; and a band of the team's colour in the Bench's face (y 15)
    and in the quarry wall above the Bench (y 22), so a player knows whose side of the bowl they are on."""
    if y in (15, 22):
        return (B.STAINED_CLAY, team_of(x))
    if (x + z) % 4 == 0 and y % 7 not in (0, 1):
        return ANDESITE
    band = y % 5
    if band == 0:
        return STONE
    if band in (1, 3):
        return POL_DIORITE
    return DIORITE


# each ground its own tone, three blocks a third each in cells of three: the Ledge grey, the Bench white
FLOORS = {13: [ANDESITE, POL_ANDESITE, STONE], 14: [POL_ANDESITE, STONE, POL_DIORITE],
          17: [DIORITE, POL_DIORITE, STONE], 20: [POL_DIORITE, DIORITE, QUARTZ], 21: [QUARTZ, POL_DIORITE, DIORITE]}


def floor_block(x, z, kind, h):
    if kind == K["spawn"]:
        return (B.STAINED_CLAY, team_of(x)) if (x // 2 + z // 2) % 2 == 0 else QUARTZ
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
                for y in range(1, P.LAVA_Y - 1):
                    w.set(x, y, z, *STONE)
                for y in range(P.LAVA_Y - 1, P.LAVA_Y + 1):
                    w.set(x, y, z, B.LAVA)
                continue
            for y in range(1, h + 1):
                w.set(x, y, z, *wall_rock(x, y, z))
            if k == K["wall"]:
                w.set(x, h, z, *POL_DIORITE)
                continue
            if k == K["stair"]:
                w.set(x, h, z, QSTAIRS, STAIR_DATA[R.stair[(x, z)]])
            else:
                w.set(x, h, z, *floor_block(x, z, k, h))


def trims(w):
    """The team's colour along every edge of the Bench and the Ledge where the ground drops away, and on the
    spawn terraces' lip: a line a player can read from across the bowl."""
    for i in range(1, P.NX - 1):
        for j in range(1, P.NZ - 1):
            k, h = R.K[i, j], R.H[i, j]
            if k not in (K["floor"], K["spawn"]) or h not in (13, 17, 21):
                continue
            drop = any(R.H[i + di, j + dj] <= h - 2 and R.K[i + di, j + dj] != K["stair"]
                       for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if drop:
                x, z = i + P.X_MIN, j + P.Z_MIN
                w.set(x, h, z, B.STAINED_CLAY, team_of(x))


# ---- carving -----------------------------------------------------------------------------------------------
def carve(w, cells, axis, half, height=2):
    """A tunnel through the rock: for each (x, z, floor) a slice `2*half+1` wide across `axis` (the axis the
    slice spans), `height` of air over a stone brick floor. Where the slice lies under the lava, its roof is
    glass with the lava standing on it, and its sides are glass against the lava."""
    for x, z, f in cells:
        for o in range(-half, half + 1):
            cx, cz = (x + o, z) if axis == "x" else (x, z + o)
            under_lava = R.K[P.ix(cx), P.iz(cz)] == K["lava"]
            w.set(cx, f, cz, B.STONEBRICK, 0)
            for y in range(f + 1, f + 1 + height):
                w.set(cx, y, cz, B.AIR)
            if under_lava:
                w.set(cx, f + 1 + height, cz, *GLASS)
                for y in range(f + 2 + height, P.LAVA_Y + 1):
                    w.set(cx, y, cz, B.LAVA)
        for o in (-half - 1, half + 1):
            cx, cz = (x + o, z) if axis == "x" else (x, z + o)
            if R.K[P.ix(cx), P.iz(cz)] == K["lava"]:
                for y in range(f, f + 2 + height):
                    w.set(cx, y, cz, *GLASS)


def stairs_on(w, cells, axis, half, rises):
    for x, z, f in cells:
        for o in range(-half, half + 1):
            cx, cz = (x + o, z) if axis == "x" else (x, z + o)
            w.set(cx, f, cz, QSTAIRS, STAIR_DATA[rises])


def turn(cells):
    return [(*P.rot(x, z), f) for x, z, f in cells]


def turned(r):
    return {"+x": "-x", "-x": "+x", "+z": "-z", "-z": "+z"}[r]


def mirror_x(cells):
    return [(-1 - x, z, f) for x, z, f in cells]


def both_turns(w, cells, axis, half, rises=None, height=2, step_cells=None):
    for cs, r in ((cells, rises), (turn(cells), turned(rises) if rises else None)):
        carve(w, cs, axis, half, height)
        if r:
            sc = step_cells(cs) if step_cells else cs
            stairs_on(w, sc, axis, half, r)


# ---- the Spring and its tunnels -----------------------------------------------------------------------------
def spring(w):
    """The room under the Middle; two stairwells down into it from the apron, each met head-on by the apron's
    band; the tunnel north (and turned, south) under the lava, the fork, the branches on under the Ledge, and the
    trenches the raster carries up onto the Ledge."""
    sp = P.SPRING
    f = sp["floor"]
    x0, x1, z0, z1 = sp["box"]
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            w.set(x, f, z, *cell_pick(x, z, [POL_ANDESITE, (B.STONEBRICK, 0)], 2))
            for y in range(f + 1, sp["ceil"]):
                w.set(x, y, z, B.AIR)
    for x, z in ((-1, -1), (0, -1), (-1, 0), (0, 0)):
        w.set(x, f, z, B.GOLD_BLOCK)
    for x in (x0, x1):
        for z in (z0, z1):
            w.set(x, sp["ceil"] - 1, z, 169, 0)
    # the west stairwell: in the apron's west band, running north from the band's south end, down to the
    # room's floor, then a short passage east into the room. Its top is met by two cells of apron in line.
    well = [(-8, z, 14 - (7 - z)) for z in range(6, 2, -1)]           # 13 at z 6 .. 10 at z 3
    passage = [(-8, z, f) for z in (2, 1)] + [(x, 1, f) for x in range(-7, -4)]
    for cells, axis, r in ((well, "x", "+z"), (passage[:2], "x", None), (passage[2:], "z", None)):
        for cs, rr in ((cells, r), (turn(cells), turned(r) if r else None)):
            for x, z, fl in cs:
                for o in ((-1, 0) if axis == "x" else (-1, 0, 1)):
                    cx, cz = (x + o, z) if axis == "x" else (x, z + o)
                    w.set(cx, fl, cz, B.STONEBRICK, 0)
                    top = 14 if rr else fl + 2
                    for y in range(fl + 1, top + 1):
                        w.set(cx, y, cz, B.AIR)
                    if rr:
                        w.set(cx, fl, cz, QSTAIRS, STAIR_DATA[rr])
    # north out of the room: two steps down to the tunnel's floor, then under the island and the lava
    down = [(-1, -5, f), (-1, -6, f - 1)]                              # stairs at 9 and 8; the tunnel at 7 beyond
    run = [(-1, z, TF) for z in range(-7, -12, -1)]
    fork = [(x, -12, TF) for x in range(-7, 7)]
    br_e = [(6, z, TF) for z in range(-13, -24, -1)]
    br_w = mirror_x(br_e)
    both_turns(w, down, "x", 1, "+z", height=3)
    both_turns(w, run, "x", 1)
    both_turns(w, fork, "z", 1)
    both_turns(w, br_e, "x", 1)
    both_turns(w, br_w, "x", 1)
    # the trenches' feet: the corridor under the Ledge at the tunnel's floor, three wide, meeting the raster's
    # stairs at x 8 (and -9)
    for cs in ([(x, -22, TF) for x in (5, 6, 7)], [(x, -22, TF) for x in (-8, -7, -6)]):
        both_turns(w, cs, "z", 1)


def spawn_tunnels(w):
    """Red's tunnel: from the spawn terrace's north edge, down a straight stair inside the wall to the Ledge's
    level, on to the Ledge's north-west corner; blue's is its turn."""
    down = [(-46, z, 22 - (-6 - z)) for z in range(-7, -15, -1)]       # stairs 21 at -7 .. 14 at -14
    flat = [(-46, z, 13) for z in range(-15, -22, -1)]
    along = [(x, -21, 13) for x in range(-45, -29)]
    both_turns(w, down, "x", 1, "+z", height=3)
    both_turns(w, flat, "x", 1, height=3)
    both_turns(w, along, "z", 1, height=3)
    for x in range(-44, -30, 5):
        for (a, b) in ((x, -23), P.rot(x, -23)):
            w.set(a, 15, b, 169, 0)


# ---- the made things on the surface -------------------------------------------------------------------------
def spawns(w):
    """The spawn terraces: a roof at 26 over the back half, the team's colour in the floor, the lintel and two
    banners on the wall behind."""
    for (x0, x1, z0, z1) in ((-49, -42, -6, 5), R._rot(-49, -42, -6, 5)):
        c = team_of(x0)
        back = list(range(x0, x0 + 4)) if x0 < 0 else list(range(x1 - 3, x1 + 1))
        for x in back:
            for z in range(z0, z1 + 1):
                w.set(x, 26, z, *POL_DIORITE)
        lint = back[-1] if x0 < 0 else back[0]
        for z in range(z0, z1 + 1):
            w.set(lint, 25, z, B.STAINED_CLAY, c)
        wallx = x0 - 1 if x0 < 0 else x1 + 1
        for z in (z0 + 1, z1 - 1):
            for y in range(22, 26):
                w.set(wallx, y, z, B.WOOL, c)
        for z in (z0 + 3, z1 - 3):
            w.set((x0 + x1) // 2, 25, z, 169, 0)


def hills(w):
    """The hills' tops: polished diorite inside a ring of white wool, which takes the holder's colour."""
    for hd in P.HILLS:
        x0, x1, z0, z1 = hd["box"]
        y = hd["y"]
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                ring = x in (x0, x1) or z in (z0, z1)
                w.set(x, y, z, *((B.WOOL, 0) if ring else POL_DIORITE))


def pads(w):
    for pd in P.PADS:
        x0, x1, z0, z1, y = pd["cells"]
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                for a, b in ((x, z), P.rot(x, z)):
                    w.set(a, y, b, *SLIME)


def arrows(w):
    for x, y, z in P.ARROWS_AT:
        bx, bz, by = int(np.floor(x)), int(np.floor(z)), int(y) - 1
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                w.set(bx + dx, by, bz + dz, *POL_ANDESITE)
        w.set(bx, by, bz, B.DISPENSER, 1)


def pillars(w):
    """The parkour and the diagonal steps: columns of quartz out of the lava, capped in polished diorite."""
    for i in range(P.NX):
        for j in range(P.NZ):
            if R.K[i, j] != K["floor"] or R.H[i, j] != 14:
                continue
            x, z = i + P.X_MIN, j + P.Z_MIN
            if -9 <= x <= 8 and -9 <= z <= 8:
                continue
            for y in range(1, 14):
                if w.id(x, y, z) not in (B.AIR, B.GLASS, B.LAVA, B.STONEBRICK):
                    w.set(x, y, z, *QUARTZ)
            w.set(x, 14, z, *POL_DIORITE)


def derricks(w):
    """Timber derricks on the quarry wall's top at the bowl's four corners: a mast, a jib over the Bench, a
    hanging block. Landmarks, out of play."""
    for (cx, cz, dx, dz) in ((-39, -35, 1, 1), (38, -35, -1, 1)):
        for (x, z, ddx, ddz) in ((cx, cz, dx, dz), (*P.rot(cx, cz), -dx, -dz)):
            for y in range(P.WALL_Y + 1, P.WALL_Y + 12):
                w.set(x, y, z, B.LOG2, 1)
            for k in range(1, 8):
                w.set(x + ddx * k, P.WALL_Y + 11 - k // 3, z + ddz * k, B.DARK_OAK_FENCE)
            for y in range(P.WALL_Y + 4, P.WALL_Y + 9):
                w.set(x + ddx * 7, y, z + ddz * 7, B.FENCE)
            w.set(x + ddx * 7, P.WALL_Y + 3, z + ddz * 7, *POL_ANDESITE)


def rails(w):
    """Iron bars along the causeways' sides over the lava, where a fall is not the point."""
    for x in range(-23, -11):
        for z in (-3, 2):
            for a, b in ((x, z), P.rot(x, z)):
                w.set(a, 14, b, B.IRON_BARS)


def make():
    w = World(P.X_MIN, P.Z_MIN, P.NX, P.NZ, sy=64)
    columns(w)
    trims(w)
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
    w.save(build, "Calcite", (0, 40, 0))
    print(f"generated and saved {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
