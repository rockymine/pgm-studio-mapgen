"""Generate Saltgate from the plan: every column built to the floor the checker walked, its top and its body by
kind, then what a raster cannot hold — the ships and their sails, the gatehouse and the walk over it, the
siege ladders, the culvert, the closed houses, the powder stores with their monuments, the citadel's gate and
posterns, the courtyard's buildings, the keep with the banner in it, the gates that open by stage, the cover.

    python3 gen.py <build-dir>

Every gate is a block that the match's triggers fill with air when its stage falls: iron bars across a door or a
passage, a fence across a gangplank. `GATE_REGIONS` lists their boxes for map.xml.
"""
import random
import sys
import time

import numpy as np

import house
import plan as P
from mc import World, B

R = P.build()
K = P.KINDS
KN = {v: k for k, v in K.items()}
BASE_Y = 6
SEA_FLOOR = 13
rng = random.Random(9)

SBRICK, MOSSY, CRACKED, CHISELED = (B.STONEBRICK, 0), (B.STONEBRICK, 1), (B.STONEBRICK, 2), (B.STONEBRICK, 3)
COBBLE, MOSSY_COBBLE, ANDESITE, POL_ANDESITE = (B.COBBLE, 0), (B.MOSSY, 0), (B.STONE, 5), (B.STONE, 6)
STONE, GRAVEL, SAND, SANDSTONE = (B.STONE, 0), (B.GRAVEL, 0), (B.SAND, 0), (B.SANDSTONE, 0)
SPRUCE, DARK_OAK, SPRUCE_LOG, DARK_LOG = (B.PLANKS, 1), (B.PLANKS, 5), (B.LOG, 1), (B.LOG2, 1)
BRICK = (B.BRICK, 0)
STAIR_DATA = {"+x": 0, "-x": 1, "+z": 2, "-z": 3}
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
RED, BLUE, PURPLE = 14, 11, 10


def kind(x, z):
    i, j = P.ix(x), P.iz(z)
    if not (0 <= i < P.NX and 0 <= j < P.NZ):
        return "sea"
    return KN[R.K[i, j]]


def h(x, z):
    return int(R.H[P.ix(x), P.iz(z)])


def pick(choices, weights):
    return rng.choices(choices, weights)[0]


def masonry(y, sea_side=False):
    """The town's stone: stone brick, mossy and cracked low down and toward the sea."""
    if y < 24 or sea_side:
        return pick([SBRICK, MOSSY, CRACKED], [50, 30, 20])
    return pick([SBRICK, CRACKED, MOSSY], [75, 15, 10])


def paving(x, z, k):
    if k == "beach":
        return SAND
    if k == "court":
        return pick([POL_ANDESITE, SBRICK, ANDESITE], [50, 30, 20])
    if k == "rampart":
        return pick([SBRICK, CRACKED], [80, 20])
    return pick([COBBLE, ANDESITE, STONE, GRAVEL, MOSSY_COBBLE], [40, 25, 15, 10, 10])


# ---- the ground -------------------------------------------------------------------------------------------
def columns(w):
    for i in range(P.NX):
        for j in range(P.NZ):
            x, z = i + P.X_MIN, j + P.Z_MIN
            k, hh = KN[R.K[i, j]], int(R.H[i, j])
            for y in range(BASE_Y, SEA_FLOOR):
                w.set(x, y, z, *STONE)
            w.set(x, SEA_FLOOR, z, *(GRAVEL if (x * 3 + z) % 4 == 0 else SAND))
            if k in ("sea", "deck", "pier") or (k == "gate" and R.gate[(x, z)] == "warmup"):
                for y in range(SEA_FLOOR + 1, P.SEA + 1):
                    w.set(x, y, z, B.WATER)
                continue
            if k == "stair":
                if z < -50:                                               # a gangplank of spruce over the water
                    for y in range(SEA_FLOOR + 1, P.SEA + 1):
                        w.set(x, y, z, B.WATER)
                    w.set(x, hh, z, 134, STAIR_DATA[R.stair[(x, z)]])
                    continue
                for y in range(SEA_FLOOR + 1, hh):
                    w.set(x, y, z, *masonry(y))
                w.set(x, hh, z, 109, STAIR_DATA[R.stair[(x, z)]])         # stone brick stairs
                continue
            top = hh
            if k in ("house", "magazine", "keep", "tower", "wall", "cover", "ladder"):
                top = ground_under(x, z, k)
            for y in range(SEA_FLOOR + 1, top + 1):
                w.set(x, y, z, *(SANDSTONE if k == "beach" else masonry(y, sea_side=z < -28)))
            if k == "beach":
                w.set(x, top, z, *SAND)
                w.set(x, top - 1, z, *SAND)
            elif k in ("street", "court", "rampart", "floor", "gate"):
                w.set(x, top, z, *paving(x, z, k))
            if k in ("wall", "tower", "keep"):
                for y in range(top + 1, hh + 1):
                    w.set(x, y, z, *masonry(y, sea_side=z < -28))


def ground_under(x, z, k):
    """The floor a solid thing stands on: the lowest walkable neighbour's height within two blocks, or its own
    height for the walls and towers, which are built to the top."""
    if k in ("wall", "tower"):
        return h(x, z)
    if k == "keep":
        return 34
    if k == "ladder":
        return 22
    hs = [h(x + dx, z + dz) for dx in range(-3, 4) for dz in range(-3, 4)
          if kind(x + dx, z + dz) in ("street", "court", "beach", "floor", "stair")]
    return min(hs) if hs else h(x, z)


def ships(w):
    """Three ships: hulls of dark oak from the water to a spruce deck at 24, raised ends, a mast with a red sail,
    rails round the deck but at the gangplank."""
    for x0, x1 in ((-30, -22), (-6, 5), (21, 29)):
        z0, z1 = -66, -56
        cx = (x0 + x1) / 2
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                edge = x in (x0, x1) or z in (z0, z1)
                for y in range(P.SEA - 2, 24):
                    w.set(x, y, z, *DARK_OAK)
                w.set(x, 24, z, *(DARK_OAK if edge else SPRUCE))
                gang = abs(x - (x0 + x1) // 2) <= 1 and z == z1
                if edge and not gang:
                    w.set(x, 25, z, B.DARK_OAK_FENCE)
        for x in range(x0, x1 + 1):                                  # the stern raised
            for z in range(z0, z0 + 3):
                w.set(x, 25, z, *DARK_OAK)
                if z == z0 or x in (x0, x1):
                    w.set(x, 26, z, B.DARK_OAK_FENCE)
        mx, mz = int(cx), (z0 + z1) // 2
        for y in range(25, 40):
            w.set(mx, y, mz, *DARK_LOG)
        for y in range(29, 38):
            for dx in range(-4, 5):
                if abs(dx) <= 4 - (y - 29) // 3:
                    w.set(mx + dx, y, mz + 1, B.WOOL, RED)
        for dx in range(-5, 6):
            w.set(mx + dx, 38, mz + 1, B.LOG2, 5)                    # the yard, along x
        w.set(mx, 40, mz, B.WOOL, RED)
        gx = (x0 + x1) // 2                                          # the gangplank's middle, as the plan has it
        for x in range(gx - 1, gx + 2):                              # the gangplank's gate: a fence, warm-up
            w.set(x, 25, -55, B.DARK_OAK_FENCE)
            w.set(x, 26, -55, B.DARK_OAK_FENCE)
            w.set(x, 24, -55, *SPRUCE)
            w.set(x, 24, -54, *SPRUCE)


def landing(w):
    """The landing stage: spruce planks on log posts, over the water."""
    for x in range(-36, 36):
        for z in range(-50, -46):
            w.set(x, 21, z, *SPRUCE)
            if x % 4 == 0 and z in (-50, -47):
                for y in range(SEA_FLOOR + 1, 21):
                    w.set(x, y, z, *SPRUCE_LOG)


def sea_wall(w):
    """Crenellations along the walk's sea edge and the towers' tops; the gatehouse's arch and the walk over its
    passage; blue banners of wool hung down the wall's face; the siege ladders."""
    for x in range(P.X_MIN, P.X_MAX + 1):
        if kind(x, -31) in ("rampart",) or (-3 <= x <= 2):
            if x % 2 == 0:
                w.set(x, 29, -31, *SBRICK)
    for x in range(-3, 3):                                        # the passage, its arch and the walk over it
        for z in range(-31, -28):
            for y in range(23, 28):
                w.set(x, y, z, B.AIR)
            w.set(x, 28, z, *SBRICK)
        w.set(x, 27, -31, *CHISELED)
        w.set(x, 27, -29, *CHISELED)
    for x in (-4, 3):
        for y in range(23, 29):
            w.set(x, y, -32, *CHISELED)
    for i in range(P.NX):                                         # the towers' crenellations
        for j in range(P.NZ):
            x, z = i + P.X_MIN, j + P.Z_MIN
            if kind(x, z) == "tower" and any(kind(x + dx, z + dz) != "tower" for dx, dz in N4) and (x + z) % 2 == 0:
                w.set(x, h(x, z) + 1, z, *SBRICK)
    for x in (-8, 7):                                             # the siege ladders
        for y in range(23, 29):
            w.set(x, y, -32, B.LADDER, 2)
    for x in (-20, -12, 11, 19):                                  # blue hangings down the face
        for y in range(23, 28):
            w.set(x, y, -32, B.WOOL, BLUE)


def culvert(w):
    """The drain under the wall: two wide, three high, stone brick round it, a little water in its floor."""
    pts = P.CULVERT["pts"]
    for (ax, az, ay), (bx, bz, by) in zip(pts, pts[1:]):
        n = int(max(abs(bx - ax), abs(bz - az), abs(by - ay)) * 3) + 1
        for s in range(n + 1):
            t = s / n
            cx, cz, cy = ax + (bx - ax) * t, az + (bz - az) * t, int(round(ay + (by - ay) * t))
            for x in (int(round(cx)) - 1, int(round(cx))):
                for z in (int(round(cz)),):
                    for y in range(cy + 1, cy + 4):
                        w.set(x, y, z, B.AIR)
                    w.set(x, cy, z, *MOSSY_COBBLE)
    for x in (-15, -14):                                          # the grates' frames at either mouth
        w.set(x, 25, -36, *CHISELED)
        w.set(x, 25, -22, *CHISELED)


def houses(w):
    for n, (x0, x1, z0, z1) in enumerate(P.HOUSES + P.COURT_BUILDINGS):
        f = ground_under(x0, z0, "house")
        spec = dict(cx=(x0 + x1 + 1) / 2, cz=(z0 + z1 + 1) / 2, heading=0, L=x1 - x0 + 1, W=z1 - z0 + 1,
                    floor=f, storeys=2 if (x1 - x0) > 6 else 1,
                    style=["stone", "plaster", "town"][n % 3] if n < len(P.HOUSES) else "stone",
                    door=1 if n % 2 else -1)
        house.build(w, spec, ground_at=lambda x, z: f, rng=np.random.default_rng(n + 11))


def magazines(w):
    """The powder stores: brick, low and vaulted, iron-barred windows, a monument of obsidian on a stone plinth in
    the middle of the hall, and iron bars across both doors until the Sea Gate falls."""
    for m in P.MAGAZINES:
        x0, x1, z0, z1 = m["box"]
        f = m["floor"]
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                edge = x in (x0, x1) or z in (z0, z1)
                for y in range(f + 1, f + 8):
                    if edge:
                        w.set(x, y, z, *BRICK)
                    else:
                        inner = min(x - x0, x1 - x, z - z0, z1 - z)
                        roof = f + 5 + min(inner, 2)
                        w.set(x, y, z, *(BRICK if y >= roof else (B.AIR, 0)))
                w.set(x, f, z, *(SBRICK if not edge else BRICK))
            for z in (z0, z1):
                if (x - x0) % 3 == 1:
                    w.set(x, f + 3, z, B.IRON_BARS)
        for dx0, dx1, dz0, dz1 in m["doors"]:
            for x in range(dx0, dx1 + 1):
                for z in range(dz0, dz1 + 1):
                    for y in range(f + 1, f + 4):
                        w.set(x, y, z, B.IRON_BARS)
                    w.set(x, f + 4, z, *CHISELED)
        mx, my, mz = m["monument"]
        w.set(mx, my - 1, mz, *CHISELED)
        w.set(mx, my, mz, B.OBSIDIAN)
        w.set(mx, my + 1, mz, B.OBSIDIAN)
        for dx, dz in N4:
            w.set(mx + dx, my - 1, mz + dz, B.SLAB, 5)
        w.set(mx, f + 5, mz, B.GLOWSTONE)


def citadel(w):
    """The citadel wall's crenellations; its gate, a passage under an arch with a portcullis of iron bars until both
    powder stores fall; the posterns, plain doors two wide; blue hangings on the wall's town face."""
    for x in range(P.X_MIN, P.X_MAX + 1):
        if x % 2 == 0:
            w.set(x, 45, 23, *SBRICK)
    for (x0, x1, fl) in ((-3, 2, 30), (36, 37, 30), (-38, -37, 30)):
        for x in range(x0, x1 + 1):
            for z in range(23, 26):
                for y in range(fl + 1, fl + (6 if x0 == -3 else 4)):
                    w.set(x, y, z, B.AIR)
                w.set(x, fl + (6 if x0 == -3 else 4), z, *CHISELED)
    for x in range(-3, 3):                                        # the portcullis
        for y in range(31, 36):
            w.set(x, y, 22, B.IRON_BARS)
    for x in (-30, -16, 15, 29):
        for y in range(33, 41):
            w.set(x, y, 22, B.WOOL, BLUE)


def keep(w):
    """The keep: stone brick to 50 with corner turrets to 55 and crenellations; the treasury inside at 34, lit, its
    roof at 41, the banner on a pedestal; iron bars across the front door's passage and the side door until both
    powder stores fall."""
    x0, x1, z0, z1 = -12, 11, 44, 60
    for x in range(x0 + 1, x1):                                  # its solid mass over the treasury and the doors
        for z in range(z0 + 1, z1):
            for y in range(41, 51):
                w.set(x, y, z, *SBRICK)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            if edge and (x + z) % 2 == 0:
                w.set(x, 51, z, *SBRICK)
    for cx, cz in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
        for x in range(cx - 1, cx + 2):
            for z in range(cz - 1, cz + 2):
                for y in range(44, 55):
                    w.set(x, y, z, *SBRICK)
                if (x + z) % 2 == 0:
                    w.set(x, 55, z, *SBRICK)
    for x in range(-8, 8):
        for z in range(48, 58):
            for y in range(35, 41):
                w.set(x, y, z, B.AIR)
            if (x % 4 == 0) and (z % 4 == 0):
                w.set(x, 41, z, B.GLOWSTONE)
    for x in range(-2, 2):                                        # the front door's passage
        for z in range(44, 48):
            for y in range(35, 39):
                w.set(x, y, z, B.AIR)
            w.set(x, 39, z, *CHISELED)
        for y in range(35, 39):
            w.set(x, y, 44, B.IRON_BARS)
    for x in range(8, 12):                                        # the side door
        for z in range(51, 54):
            for y in range(35, 38):
                w.set(x, y, z, B.AIR)
    for z in range(51, 54):
        for y in range(35, 38):
            w.set(11, y, z, B.IRON_BARS)
    wx, wy, wz = P.WOOL["at"]
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            w.set(wx + dx, wy - 1, wz + dz, *CHISELED)
    w.set(wx, wy, wz, B.WOOL, PURPLE)
    for x in (-6, 5):
        for y in range(36, 40):
            w.set(x, y, 57, B.WOOL, BLUE)


def wool_monument(w):
    """The banner's monument in the Sea Gate's yard: a frame of chiseled stone brick and purple glass round the
    slot the banner goes in."""
    mx, my, mz = P.WOOL["monument"]
    w.set(mx, my - 1, mz, *CHISELED)
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            if (dx, dz) != (0, 0):
                w.set(mx + dx, my - 1, mz + dz, *CHISELED)
                if abs(dx) + abs(dz) == 2:
                    w.set(mx + dx, my, mz + dz, 95, PURPLE)
    w.set(mx, my + 2, mz, 95, PURPLE)


def cover(w):
    """Beached boats and rocks on the sand; carts and crates in the yard and the courtyard."""
    for x0, x1, z0, z1, tall in P.COVER:
        f = ground_under(x0, z0, "cover")
        beach = kind(x0 - 1, z0) == "beach" or kind(x1 + 1, z1) == "beach"
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                for y in range(f + 1, f + 1 + tall):
                    if beach:
                        b = (DARK_OAK if (x + z) % 3 else SPRUCE) if (x1 - x0) >= 2 else pick([STONE, MOSSY_COBBLE, ANDESITE], [50, 30, 20])
                    else:
                        b = pick([SPRUCE_LOG, (B.HAY, 0), SPRUCE, (B.LOG, 13)], [30, 30, 20, 20])
                    w.set(x, y, z, *b)


def spawns_dress(w):
    """Each spawn's ground in its team's colour: red on the flagship's deck, blue in the town square."""
    for team, st in P.SPAWNS.items():
        col = RED if team == "attackers" else BLUE
        for stage, (x, y, z, yaw) in st.items():
            for dx in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    w.set(int(x - 0.5) + dx, int(y) - 1, int(z - 0.5) + dz, B.WOOL, col)


GATE_REGIONS = {
    # stage -> boxes (x0, y0, z0, x1, y1, z1) inclusive, filled with air when it falls
    "warmup": [((a + b) // 2 - 1, 25, -55, (a + b) // 2 + 1, 26, -55) for a, b in ((-30, -22), (-6, 5), (21, 29))],
    "A": [(dx0, P.MAGAZINES[k]["floor"] + 1, dz0, dx1, P.MAGAZINES[k]["floor"] + 3, dz1)
          for k in range(2) for dx0, dx1, dz0, dz1 in P.MAGAZINES[k]["doors"]],
    "B": [(-3, 31, 22, 2, 35, 22), (-2, 35, 44, 1, 38, 44), (11, 35, 51, 11, 37, 53)],
}


def make():
    w = World(P.X_MIN, P.Z_MIN, P.NX, P.NZ, sy=64)
    columns(w)
    landing(w)
    ships(w)
    sea_wall(w)
    culvert(w)
    houses(w)
    magazines(w)
    citadel(w)
    keep(w)
    wool_monument(w)
    cover(w)
    spawns_dress(w)
    w.biome[:, :] = 1
    return w


def main(build):
    t0 = time.time()
    w = make()
    w.save(build, "Saltgate", (0, 50, 0))
    print(f"generated and saved {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
