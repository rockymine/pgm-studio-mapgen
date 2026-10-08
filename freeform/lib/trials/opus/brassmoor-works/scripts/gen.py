"""Generate Brassmoor Works from the plan: red's half (z < 0) is built and turned half a circle onto blue's; the
crane island, the smog and the build markers are laid over both; then the objectives are stamped.

Every deck is its plan floor at its height, exactly, so the gaps the plan measured are the gaps in the world.

The look, decided in the report's plan section and made here:
    decks    a built floor: stone brick, polished andesite, andesite and stone, a quarter each in cells of three
    built    red brick with stone brick pilasters and iron-barred windows; iron and spruce for the machines
    under    girders of stone brick and brick under every deck, iron hanging at their crossings, piers into the smog
    accent   hazard stripes of yellow and black clay on every edge a bridge leaves from; the teams' banners

    python3 gen.py <build-dir>
"""
import math
import sys
import time

import numpy as np

import plan as P
import common as C
from pgmvox import B, World, rng

from pgmvox import terrain as T
from pgmvox.objectives import Wool
from pgmvox.orient import ladder as ladder_data, stair as stair_data, turn_world

t0 = time.time()
R = P.build()
w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=112)
X, Z = w.grid()
r_ = rng(P.BOARD, "works")
DECK = [(B.STONEBRICK, 0), (B.STONE, 6), (B.STONE, 5), (B.STONE, 0)]
SPAWN_FLOOR = [(B.STONE, 6), (B.STONE, 4), (B.STONEBRICK, 0), (B.STONE, 6)]
SLAG = [(B.COAL_BLOCK, 0), (B.STAINED_CLAY, 15), (B.COBBLE, 0), (B.STAINED_CLAY, 7)]
assert (w.sx, w.sz) == R.H.shape
land = R.piece != R.kinds["void"]
red = Z < 0
zone = P.zone_mask(R)


def floor_of(x, z):
    return int(R.floor[x - w.x0, z - w.z0])


def piece_of(x, z):
    return R.names[int(R.piece[x - w.x0, z - w.z0])]


# ---- the decks and what holds them up ------------------------------------------------------------------------
for i, k in np.argwhere(land & red):
    x, z = int(X[i, k]), int(Z[i, k])
    h, key = int(R.floor[i, k]), R.names[int(R.piece[i, k])]
    cls = P.PIECE[key][2]
    blk = C.cell_pick(x, z, SPAWN_FLOOR if cls == "spawn" else SLAG if cls == "islet" else DECK, 3, 1)
    w.set(x, h, z, *blk)
    w.set(x, h - 1, z, B.STONEBRICK)
    girder = (x % 6 == 0) or (z % 6 == 0)
    edge = any(not land[i + dx, k + dz] for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))
               if 0 <= i + dx < w.sx and 0 <= k + dz < w.sz)
    if girder or edge:
        w.set(x, h - 2, z, B.BRICK)
        w.set(x, h - 3, z, *((B.STONEBRICK, 0) if edge else (B.BRICK, 0)))
    if x % 6 == 0 and z % 6 == 0:
        for y in range(h - 7, h - 3):
            w.set(x, y, z, B.IRON_BARS)
for key, _, cls, (x0, z0, x1, z1), h in P.PIECES:            # piers from each deck's corners into the smog
    if key == "crane":
        continue
    for x, z in ((x0 + 1, z0 + 1), (x1 - 1, z0 + 1), (x0 + 1, z1 - 1), (x1 - 1, z1 - 1)):
        if land[x - w.x0, z - w.z0]:
            for y in range(P.SMOG_Y[0] + 2, h - 3):
                w.set(x, y, z, *((B.STONEBRICK, 0) if y % 7 else (B.STONEBRICK, 3)))
# the stairs between floors
for (x, z), rises in R.stair.items():
    if z < 0 and R.kind(x, z) == "stair":
        w.set(x, R.h(x, z), z, B.STONEBRICK_STAIRS, stair_data(rises))
        w.set(x, R.h(x, z) - 1, z, B.STONEBRICK)
# hazard stripes on every edge a bridge leaves from: deck cells beside a build zone
for i, k in np.argwhere(land & red):
    if any(0 <= i + dx < w.sx and 0 <= k + dz < w.sz and zone[i + dx, k + dz]
           for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))):
        x, z = int(X[i, k]), int(Z[i, k])
        if R.kind(x, z) not in ("stair", "roomwall", "barrier"):
            w.set(x, floor_of(x, z), z, B.STAINED_CLAY, 4 if ((x + z) // 2) % 2 else 15)
print(f"decks {time.time() - t0:.1f}s")


# ---- the wool rooms: brick halls with pilasters and barred windows -----------------------------------------------
def room(key):
    rm = P.ROOMS[key]
    x0, z0, x1, z1 = rm["box"]
    f = P.PIECE[key][4]
    top = f + rm["height"]
    # facade.extrude finds no faces on a wall one block thick (every cell is open on two sides, so a corner):
    # the walls are laid here, a stone brick pilaster every fourth block, barred windows between
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if not (x in (x0, x1) or z in (z0, z1)):
                continue
            run = (x - x0) if z in (z0, z1) else (z - z0)
            corner = x in (x0, x1) and z in (z0, z1)
            for y in range(f + 1, top):
                t = y - f
                if corner or run % 4 == 0:
                    blk = (B.STONEBRICK, 0)
                elif 3 <= t <= 6 and run % 4 == 2:
                    blk = (B.IRON_BARS, 0)
                else:
                    blk = (B.BRICK, 0)
                w.set(x, y, z, *blk)
    for x in range(x0, x1 + 1):                                 # the roof: stone brick slabs on a brick course
        for z in range(z0, z1 + 1):
            w.set(x, top, z, B.BRICK)
            w.set(x, top + 1, z, *((B.SLAB, 5) if (x in (x0, x1) or z in (z0, z1)) else (B.AIR, 0)))
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
            for y in range(f + 1, top):
                w.set(x, y, z, B.AIR)
    for x in range(x0, x1 + 1):                                 # the doors, two high and open
        for z in range(z0, z1 + 1):
            if P.door_at(rm, x, z):
                for y in range(f + 1, f + 4):
                    w.set(x, y, z, B.AIR)
                w.set(x, f + 4, z, B.STONEBRICK, 0)
    return f, top


f, top = room("boiler")
for x, z in ((-76, -88), (-76, -87), (-77, -88), (-77, -87)):   # the boiler's chimney through the roof
    for y in range(f + 1, top + 18):
        w.set(x, y, z, B.BRICK)
for x, z in ((-77, -88),):
    w.set(x, top + 18, z, B.AIR)
for x in range(-77, -69):                                       # the boilers: iron drums and fireboxes along the back
    for y in (f + 1, f + 2):
        w.set(x, y, -89, B.IRON_BLOCK if x % 3 else B.FURNACE, 3)
w.chest(-65, f + 1, -88, [(0, "minecraft:iron_chestplate", 1, 0), (1, "minecraft:arrow", 32, 0),
                          (2, "minecraft:golden_apple", 1, 0)], facing=4)
f, top = room("tower")
for dx in (-4, 4):                                              # the tank's legs on the roof and the tank itself
    for dz in (-4, 4):
        for y in range(top + 1, top + 6):
            w.set(68 + dx, y, -80 + dz, B.LOG, 1)
for x in range(62, 75):
    for z in range(-86, -73):
        d = math.hypot(x - 68, z - (-80))
        for y in range(top + 6, top + 13):
            if d <= 5.5:
                w.set(x, y, z, *((B.PLANKS, 1) if d > 4.6 or y == top + 6 else (B.WATER, 0)))
        if d <= 5.5:
            w.set(x, top + 13, z, *((B.SPRUCE_STAIRS, 0) if d > 4.6 else (B.PLANKS, 1)))
for x in range(61, 65):                                         # pumps and pipes along the back wall
    w.set(x, f + 1, -87, B.IRON_BLOCK if x % 2 else B.CAULDRON)
w.chest(74, f + 1, -86, [(0, "minecraft:iron_chestplate", 1, 0), (1, "minecraft:arrow", 32, 0),
                         (2, "minecraft:golden_apple", 1, 0)], facing=4)

# ---- the bedrock lines: three bedrock and a web, across each lane --------------------------------------------
for key, wl in P.WALLS.items():
    fl = P.PIECE[key][4]
    for x in range(wl["x0"], wl["x1"] + 1):
        for z in range(wl["z0"], wl["z1"] + 1):
            for y in range(fl + 1, fl + 4):
                w.set(x, y, z, B.BEDROCK)
            w.set(x, fl + 4, z, B.COBWEB)

# ---- the Gatehouse: a canopy over the spawn's back half, banners, the spawn's iron --------------------------------
x0, z0, x1, z1 = P.PIECE["gate"][3]
for x in (x0 + 1, x1 - 1, (x0 + x1) // 2, (x0 + x1) // 2 + 1):
    for z in (z0 + 1, z0 + 8):
        for y in range(71, 77):
            w.set(x, y, z, B.STONEBRICK, 0 if y < 76 else 3)
for x in range(x0, x1 + 1):
    for z in range(z0, z0 + 10):
        w.set(x, 77, z, *((B.SLAB, 5) if (x + z) % 2 else (B.SLAB, 0)))
for x in (x0 + 1, x1 - 1):
    w.banner(x, 75, z0 + 9, 1, wall_facing=3)
for x in (x0 + 3, x1 - 3):                                       # the iron a spawn may mine and that grows back
    w.set(x, 71, z0 + 4, B.IRON_BLOCK)
    w.set(x, 71, z0 + 5, B.IRON_BLOCK)

# ---- the Yard: rails, two wagons for cover, a lip round the pit -----------------------------------------------
for z in (-62, -64):
    for x in range(-26, 26):
        if R.kind(x, z) == "yard":
            w.set(x, 67, z, B.RAIL, 1)
for wx, wz in ((-20, -63), (12, -63)):                           # a wagon: spruce sides, iron frame, open top
    for x in range(wx, wx + 6):
        for y in (67, 68, 69):
            w.set(x, y, wz - 1, *((B.PLANKS, 1) if y < 69 else (B.WOOD_SLAB, 1)))
            w.set(x, y, wz + 1, *((B.PLANKS, 1) if y < 69 else (B.WOOD_SLAB, 1)))
        w.set(x, 67, wz, B.IRON_BLOCK)
    for y in (67, 68):
        w.set(wx - 1, y, wz, B.PLANKS, 1); w.set(wx + 6, y, wz, B.PLANKS, 1)
px0, pz0, px1, pz1 = P.PIT
for x in range(px0 - 1, px1 + 2):
    for z in range(pz0 - 1, pz1 + 2):
        if (x in (px0 - 1, px1 + 1) or z in (pz0 - 1, pz1 + 1)) and R.kind(x, z) == "yard":
            w.set(x, 67, z, B.COBBLE_WALL)
for x in range(px0, px1 + 1):                                     # the turntable's girder across the pit
    w.set(x, 65, (pz0 + pz1) // 2, B.IRON_BARS)

# ---- the Gantry: a crane gantry over the west lane, legs on its edges ---------------------------------------------
gx0, gz0, gx1, gz1 = P.PIECE["gantry"][3]
for x in range(gx0 + 6, gx1, 10):
    for z in (gz0, gz1):
        for y in range(67, 76):
            w.set(x, y, z, B.IRON_BLOCK if y in (67, 75) else B.IRON_BARS)
    for z in range(gz0, gz1 + 1):
        w.set(x, 76, z, B.IRON_BLOCK)
for x in range(gx0 + 6, gx1 - 3):
    for z in (gz0, gz1):
        w.set(x, 76, z, B.IRON_BLOCK)
for y in range(70, 76):                                           # the hook hanging from the trolley
    w.set(-40, y, -79, B.FENCE if y > 70 else B.IRON_BLOCK)

# ---- the Spur: buffers at its head, sleepers along it; the Quays: bollards and crates ------------------------------
for z in range(-81, -73, 2):
    for x in range(30, 52, 3):
        w.set(x, 65, z, B.RAIL, 1)
for qx0, qx1 in ((-28, -17), (16, 27)):
    for z in range(-54, -14, 8):
        for x in (qx0, qx1):
            w.set(x, 65, z, B.COBBLE_WALL)
    for cz in (-44, -28):                                          # crate stacks: small cover, two and three high
        cx = qx0 + 3 if cz == -44 else qx1 - 4
        for dx in range(2):
            for dz in range(2):
                for y in range(65, 67 + (dx + dz) % 2):
                    w.set(cx + dx, y, cz + dz, B.PLANKS if y % 2 else B.LOG, 1)
# the islets' heaps
for key in ("slag", "coal"):
    kx0, kz0, kx1, kz1 = P.PIECE[key][3]
    cx, cz = (kx0 + kx1) / 2, (kz0 + kz1) / 2
    for x in range(kx0, kx1 + 1):
        for z in range(kz0, kz1 + 1):
            hh = int(2.2 - math.hypot(x - cx, z - cz) * 0.8)
            for y in range(65, 65 + max(0, hh)):
                w.set(x, y, z, *(SLAG[(x + y + z) % 4] if key == "slag" else (B.COAL_BLOCK, 0)))
print(f"works {time.time() - t0:.1f}s")

# ---- blue's half, then the crane on the middle island, the smog and the markers ------------------------------------
turn_world(w, "half", red, recolour={(B.WOOL, 14): (B.WOOL, 11)}, banners={1: 4})
for i, k in np.argwhere(R.piece == R.kinds["crane"]):
    x, z = int(X[i, k]), int(Z[i, k])
    w.set(x, 66, z, *C.cell_pick(x, z, DECK, 3, 1))
    w.set(x, 65, z, B.STONEBRICK)
    w.set(x, 64, z, B.BRICK if (x + z) % 2 else B.STONEBRICK)
for y in range(67, 88):                                           # the crane's tower, iron, open inside
    for x in (-2, 1):
        for z in (-2, 1):
            w.set(x, y, z, B.IRON_BLOCK if y % 5 == 2 else B.IRON_BARS)
for x in range(-14, 13):                                          # its jib along x, the cab at its root
    w.set(x, 88, -1, B.IRON_BLOCK if x in (-2, 1) else B.IRON_BARS)
    w.set(x, 88, 0, B.IRON_BLOCK if x in (-2, 1) else B.IRON_BARS)
for x in (-1, 0):
    for z in (-1, 0):
        for y in (85, 86, 87):
            w.set(x, y, z, B.PLANKS if y < 87 else B.WOOD_SLAB, 1)
for y in range(80, 88):
    w.set(-12, y, 0, B.FENCE)
for x in range(-2, 2):
    for z in range(-2, 2):
        for y in range(30, 64):
            if x in (-2, 1) and z in (-2, 1):
                w.set(x, y, z, B.STONEBRICK)
T.cloud_deck(w, P.SMOG_Y[0] + 6, seed=17, materials=((B.STAINED_GLASS, 8), (B.WOOL, 8)))
w.ids[:, 0, :][land | zone] = 36                                  # block 36: a player may build over this column
w.biome[:, :] = 1
O = P.objectives()
O.stamp(w)
w.save(sys.argv[1], "Brassmoor Works", (0, 96, 0))
print(f"saved {time.time() - t0:.1f}s: {int(np.count_nonzero(w.ids))} blocks, {len(w.tiles)} tile entities")
