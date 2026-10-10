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
    """Three ships lying broadside to the beach, bow to the east. The hull is the deck's outline carried down to a
    keel: each course below the deck is a little shorter and narrower than the one above, so the sides curve in
    under the water. Dark oak strakes with a band of spruce at the waterline; a bulwark round the deck with a rail
    on it, rising at the bow and the stern; a stern cabin with windows and a railed roof; a bowsprit; a mast or
    two with red sails and a pennant; the gangplank's head amidships on the landward side, fenced until the
    warm-up ends."""
    for ship in P.SHIPS:
        cx, zc, a = ship["cx"], ship["zc"], ship["length"] / 2.0
        deck = set(P.ship_deck(ship))
        # the hull, course by course from the deck down to the keel
        for y in range(P.SEA - 4, 25):
            d = 24 - y
            shrink_l = 1.0 - 0.18 * (d / 10.0) ** 2
            shrink_w = 1.0 - 0.55 * (d / 10.0) ** 1.6
            for x in range(int(cx - a) - 1, int(cx + a) + 2):
                u = x + 0.5 - (cx + 0.5)
                if abs(u) > a * shrink_l:
                    continue
                hw = P.half_width(ship, u / shrink_l) * shrink_w
                for z in range(zc - 5, zc + 6):
                    if abs(z - zc) <= hw:
                        if y == 24:
                            blk = SPRUCE if (x, z) in deck and abs(z - zc) < hw - 0.9 else DARK_OAK
                        elif y in (P.SEA, P.SEA + 1):
                            blk = SPRUCE
                        elif y < P.SEA - 1 and abs(z - zc) < 0.6:
                            blk = DARK_LOG                                  # the keel
                        else:
                            blk = DARK_OAK
                        w.set(x, y, z, *blk)
        # the bulwark: a course of planks and a rail round the deck's edge, higher at the ends
        for x, z in deck:
            edge = any((x + dx, z + dz) not in deck for dx, dz in N4)
            if not edge:
                continue
            u = x + 0.5 - (cx + 0.5)
            if abs(x - cx) <= 1 and z > zc:
                continue                                            # the gangplank's opening
            w.set(x, 25, z, *DARK_OAK)
            w.set(x, 26, z, B.DARK_OAK_FENCE)
            if abs(u) > 0.7 * a:
                w.set(x, 26, z, *DARK_OAK)
                w.set(x, 27, z, B.DARK_OAK_FENCE)
        # the stern cabin, with windows, and its railed roof
        for x, z in deck:
            u = x + 0.5 - (cx + 0.5)
            if u < -0.62 * a:
                edge = any((x + dx, z + dz) not in deck or (x + dx + 0.5 - (cx + 0.5)) >= -0.62 * a for dx, dz in N4)
                for y in range(25, 29):
                    win = edge and y == 26 and (x + z) % 2 == 0
                    w.set(x, y, z, *((B.PANE, 0) if win else DARK_OAK))
                w.set(x, 29, z, *SPRUCE)
                if edge:
                    w.set(x, 30, z, B.DARK_OAK_FENCE)
        # the bowsprit
        bx = int(cx + a)
        for k in range(0, 6):
            w.set(bx + k, 26 + k // 2, zc, *DARK_LOG)
        w.set(bx + 6, 29, zc, B.DARK_OAK_FENCE)
        # the masts, the yards, the sails and the pennants
        for mu in ship["masts"]:
            mx = cx + mu
            top = 40 if len(ship["masts"]) == 1 or mu > 0 else 37
            for y in range(25, top):
                w.set(mx, y, zc, *DARK_LOG)
            for dz in range(-5, 6):
                w.set(mx, top - 2, zc + dz, B.LOG2, 9)                # the yard, along z
            for y in range(28, top - 2):
                spread = 5 - max(0, (top - 3 - y) // 4)
                for dz in range(-spread, spread + 1):
                    stripe = (top - 3 - y) % 4 == 0
                    w.set(mx + 1, y, zc + dz, B.WOOL, 0 if stripe else RED)
            w.set(mx, top, zc, B.FENCE)
            for k in range(1, 4):
                w.set(mx - k, top, zc, B.WOOL, RED)
        # the gangplank's head and its warm-up fence
        gx = cx
        for x in range(gx - 1, gx + 2):
            for z in (-56, -55, -54):
                for y in range(P.SEA - 1, 24):
                    w.set(x, y, z, *DARK_OAK)
                w.set(x, 24, z, *SPRUCE)
            w.set(x, 25, -55, B.DARK_OAK_FENCE)
            w.set(x, 26, -55, B.DARK_OAK_FENCE)


def palm(w, x, y, z, lean, seed):
    """A palm: a jungle-wood trunk that leans as it rises, and a crown of two crosses of leaves laid one over the
    other, the second turned an eighth, each arm drooping at its tip."""
    r = random.Random(seed)
    import math
    tall = r.randint(7, 9)
    lx, lz = lean
    px, pz = x, z
    for k in range(1, tall + 1):
        f = (k / tall) ** 1.6
        px, pz = x + round(lx * f), z + round(lz * f)
        w.set(px, y + k, pz, B.LOG, 3)
    top = y + tall
    w.set(px, top + 1, pz, B.LEAVES, 7)
    turn = r.random() * 0.4
    for i in range(8):
        ang = turn + i * math.pi / 4
        dx, dz = math.cos(ang), math.sin(ang)
        length = 5 if i % 2 == 0 else 4
        for k in range(1, length + 1):
            yy = top + 1 - max(0, k - 2)                                  # level, then drooping toward the tip
            w.set(px + round(dx * k), yy, pz + round(dz * k), B.LEAVES, 7)


def palms(w):
    for n, (x, z) in enumerate(P.PALMS):
        lean = [(2, 1), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1), (1, 2), (2, 2), (-2, 2)][n % 9]
        palm(w, x, h_ground(x, z), z, lean, n + 1)


def h_ground(x, z):
    hs = [h(x + dx, z + dz) for dx, dz in N4 if kind(x + dx, z + dz) == "beach"]
    return min(hs) if hs else 22


def landing(w):
    """The landing stage: spruce planks on log posts, over the water, a fence along its seaward edge and ends but
    for the three gangplanks, a lantern on a post at each."""
    gaps = {s["cx"] + d for s in P.SHIPS for d in (-1, 0, 1)}
    for x in range(-36, 36):
        for z in range(-50, -46):
            w.set(x, 21, z, *SPRUCE)
            if x % 4 == 0 and z in (-50, -47):
                for y in range(SEA_FLOOR + 1, 21):
                    w.set(x, y, z, *SPRUCE_LOG)
        if x not in gaps:
            w.set(x, 22, -50, B.SPRUCE_FENCE)
    for z in range(-50, -46):
        w.set(-36, 22, z, B.SPRUCE_FENCE)
        w.set(35, 22, z, B.SPRUCE_FENCE)
    for s in P.SHIPS:
        for x in (s["cx"] - 2, s["cx"] + 2):
            w.set(x, 22, -50, B.SPRUCE_FENCE)
            w.set(x, 23, -50, B.SPRUCE_FENCE)
            w.set(x, 24, -50, B.GLOWSTONE)


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
    """The powder stores: brick, low and vaulted, iron-barred windows, a monument of obsidian hung three blocks over a stone plinth in
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
        w.set(mx, f, mz, *CHISELED)                       # the plinth is the floor's own course: nothing stands under
        w.set(mx, my, mz, B.OBSIDIAN)                     # the monument, which hangs three blocks over it (my = f + 4)
        w.set(mx, my + 1, mz, B.OBSIDIAN)
        for dx, dz in N4:
            w.set(mx + dx, f, mz + dz, B.SLAB, 5)
        w.set(mx, f + 6, mz, B.GLOWSTONE)


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


def crates(w):
    """Crates, barrels and sacks against the houses' walls along the streets: a stack of one or two in a few
    places, never on a stair, by a door or gate, or near a spawn."""
    r = random.Random(21)
    keep_clear = set()
    for (x, z) in list(R.stair) + list(R.gate):
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                keep_clear.add((x + dx, z + dz))
    for st in P.SPAWNS.values():
        for (sx, sy, sz, _) in st.values():
            for dx in range(-3, 4):
                for dz in range(-3, 4):
                    keep_clear.add((int(sx) + dx, int(sz) + dz))
    for i in range(1, P.NX - 1):
        for j in range(1, P.NZ - 1):
            x, z = i + P.X_MIN, j + P.Z_MIN
            if kind(x, z) not in ("street", "court") or (x, z) in keep_clear or not (-19 <= z <= 60):
                continue
            if not any(kind(x + dx, z + dz) in ("house", "magazine") for dx, dz in N4):
                continue
            if r.random() > 0.07:
                continue
            f = h(x, z)
            if w.id(x, f + 1, z) != B.AIR:
                continue
            stack = 1 if r.random() < 0.6 else 2
            for y in range(f + 1, f + 1 + stack):
                w.set(x, y, z, *r.choice([SPRUCE, (B.HAY, 0), SPRUCE_LOG, (B.PLANKS, 0), (B.LOG, 12)]))


def flag(w, x, y, z, height, colour, along="x", length=5, drop=3):
    """A flagpole of fence on the wall's top with a flag of wool flying from it, its far edge ragged."""
    for k in range(height):
        w.set(x, y + k, z, B.FENCE)
    top = y + height - 1
    for u in range(1, length + 1):
        for v in range(drop):
            if u == length and v == drop - 1:
                continue
            fx, fz = (x + u, z) if along == "x" else (x, z + u)
            w.set(fx, top - v, fz, B.WOOL, colour)


def flags(w):
    """The defenders' blue over the keep, on the citadel wall and on the sea wall's towers."""
    flag(w, -1, 51, 52, 10, BLUE, length=7, drop=4)
    for x in (-40, -22, 20, 38):
        flag(w, x, 45, 24, 5, BLUE)
    for x, z in ((-28, -30), (26, -30), (-46, -30), (44, -30)):
        flag(w, x, 34, z, 5, BLUE, along="z", length=4, drop=3)


def keep_detail(w):
    """The keep's faces: a chiseled course at 42 and under the battlements, windows of dark glass two high every
    four blocks on the upper storey with a sill under each, arrow slits two high on the lower, and a canopy of stone brick stairs over the door."""
    x0, x1, z0, z1 = -12, 11, 44, 60
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if not (x in (x0, x1) or z in (z0, z1)):
                continue
            for y in (42, 50):
                w.set(x, y, z, *CHISELED)
            run = x if z in (z0, z1) else z
            corner = x in (x0, x1) and z in (z0, z1)
            if corner:
                continue
            ix_, iz_ = (0 if x not in (x0, x1) else (1 if x == x0 else -1)), (0 if z not in (z0, z1) else (1 if z == z0 else -1))
            if run % 4 == 0:
                for y in (45, 46):
                    w.set(x, y, z, B.STAINED_PANE, 15)                # dark glass, the room behind unlit
                    w.set(x + ix_, y, z + iz_, B.WOOL, 15)
                w.set(x, 44, z, 109, 2 if z == z1 else 3) if z in (z0, z1) else w.set(x, 44, z, *CHISELED)
            if run % 4 == 2 and not (-2 <= x <= 1 and z == z0):
                w.set(x, 38, z, B.STAINED_PANE, 15)
                w.set(x, 39, z, B.STAINED_PANE, 15)
                w.set(x + ix_, 38, z + iz_, B.WOOL, 15)
                w.set(x + ix_, 39, z + iz_, B.WOOL, 15)
    for x in range(-3, 3):
        w.set(x, 40, z0 - 1, 109, 6)                            # the canopy over the door, stone brick stairs


def smoke(w):
    """Smoke from some of the town's chimneys: white glass, two by two where it leaves the chimney, swelling into a
    long balloon as the wind carries it east and a little north, curving as it goes."""
    import math
    r = random.Random(31)
    tops = []
    xs, ys, zs = np.nonzero(w.ids == B.COBBLE_WALL)
    for i, y, k in zip(xs, ys, zs):
        tops.append((int(i) + w.x0, int(y), int(k) + w.z0))
    r.shuffle(tops)
    for (x, y, z) in tops[: max(1, int(len(tops) * 0.3))]:
        length = r.randint(12, 18)
        bend = r.uniform(-0.6, 0.6)
        for s in range(length * 3):
            t = s / 3.0
            f = t / length
            cx = x + 0.5 + t * 0.95
            cz = z + 0.5 - t * 0.25 + bend * (t ** 2) / length
            cy = y + 1.5 + t * 0.55 + 1.2 * math.sin(f * math.pi) * 0.5
            rad = 0.75 + 1.25 * math.sin(f * math.pi * 0.9) ** 1.5      # two by two at the chimney, swelling
            if cy + rad >= w.sy - 1:
                break
            for bx in range(int(cx - rad) - 1, int(cx + rad) + 2):
                for by in range(int(cy - rad * 0.8) - 1, int(cy + rad * 0.8) + 2):
                    for bz in range(int(cz - rad) - 1, int(cz + rad) + 2):
                        dx, dy, dz = bx + 0.5 - cx, (by + 0.5 - cy) / 0.8, bz + 0.5 - cz
                        if dx * dx + dy * dy + dz * dz <= rad * rad and w.id(bx, by, bz) == B.AIR:
                            w.set(bx, by, bz, 95, 0)


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
    keep_detail(w)
    flags(w)
    cover(w)
    palms(w)
    crates(w)
    spawns_dress(w)
    smoke(w)
    w.biome[:, :] = 1
    return w


def main(build):
    t0 = time.time()
    w = make()
    w.save(build, "Saltgate", (0, 50, 0))
    print(f"generated and saved {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
