"""Generate Riad from the plan's two rasters: every column built to the floor the checker walked, the roofs and
decks over them, then what a raster cannot hold — the Cistern's tower and its caged water columns, the
spawn houses' rooms, the posts' beacons and the flag's banner — and the palace's paint.

    python3 gen.py <build-dir>

The rasters are the whole board already (they were drawn with their mirror), so nothing is mirrored here
except the pieces built by hand, which are built for blue and mirrored for red.
"""
import sys
import time

import plan as P
from mc import World, B

R = P.build()
K = P.KINDS
KN = {v: k for k, v in K.items()}
G = P.G
BASE_Y = 6                                           # the board's underside: it floats over the void

SANDSTONE, CHISELED, SMOOTH = (B.SANDSTONE, 0), (B.SANDSTONE, 1), (B.SANDSTONE, 2)
RED, RED_CHISELED, RED_SMOOTH = (B.RED_SANDSTONE, 0), (B.RED_SANDSTONE, 1), (B.RED_SANDSTONE, 2)
QUARTZ, QUARTZ_CHISELED, QUARTZ_PILLAR = (B.QUARTZ, 0), (B.QUARTZ, 1), (B.QUARTZ, 2)
TERRACOTTA = (B.HARDENED_CLAY, 0)
PRISMARINE, PRISMARINE_BRICK, DARK_PRISMARINE = (168, 0), (168, 1), (168, 2)
SEA_LANTERN = (169, 0)
BEACON = (138, 0)
HEDGE = (B.LEAVES, 4)                                # oak, no decay
CYPRESS = (B.LEAVES, 5)                              # spruce, no decay
CAGE = (B.STAINED_PANE, 3)                           # light blue glass
SANDSTONE_STAIRS = 128
STAIR_DATA = {"+x": 0, "-x": 1, "+z": 2, "-z": 3}
FENCE = B.ACACIA_FENCE
PURPLE = 10


def team_clay(z):
    """Red holds the north, blue the south; the middle band, |z| <= 16, belongs to nobody."""
    if z < -16:
        return (B.WOOL, 14)
    if z > 16:
        return (B.WOOL, 11)
    return QUARTZ


def dye(team):
    return {"red": 1, "blue": 4}[team]


def k_at(x, z):
    i, j = P.ix(x), P.iz(z)
    if not (0 <= i < P.NX and 0 <= j < P.NZ):
        return "void"
    return KN[R.K[i, j]]


def h_at(x, z):
    return int(R.H[P.ix(x), P.iz(z)])


# ---- the paint --------------------------------------------------------------------------------------------
def in_garden(x, z):
    return 17 <= abs(z) <= 36 and 14 <= abs(x) <= 36 or (18 <= x <= 42 and abs(z) <= 16)


def ground_block(x, z):
    """The ground's top: the court tiled in smooth sandstone and red sandstone in a 3 x 3 check, with a ring of
    chiseled quartz round the Cistern; the gardens grass, edged in smooth sandstone; the back gardens and the
    balconies smooth sandstone ruled every six blocks in red. The carrier's line is a band of purple clay."""
    if abs(z) == P.CARRIER_LINE and abs(x) <= 36:
        return (B.WOOL, PURPLE)
    if max(abs(x), abs(z)) == 7:
        return QUARTZ_CHISELED
    if abs(x) <= 17 and abs(z) <= 16 or (-19 <= x <= -18 and abs(z) <= 16):
        return SMOOTH if ((x + 1) // 3 + (z + 1) // 3) % 2 == 0 else RED_SMOOTH
    if in_garden(x, z):
        edge = any(k_at(x + dx, z + dz) not in ("floor", "ladder") or not in_garden(x + dx, z + dz)
                   for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        return SMOOTH if edge else (B.GRASS, 0)
    if x % 6 == 0 or z % 6 == 0:
        return RED_SMOOTH
    return SMOOTH


def body(x, y, z):
    """Below the ground: red sandstone in courses, a course of terracotta every fourth."""
    if y % 4 == 0:
        return TERRACOTTA
    return RED


# ---- the columns ------------------------------------------------------------------------------------------
def columns(w):
    for i in range(P.NX):
        for j in range(P.NZ):
            x, z = i + P.X_MIN, j + P.Z_MIN
            k, h = KN[R.K[i, j]], int(R.H[i, j])
            if k == "void":
                continue
            if k in ("bridge",):
                for y in range(h - 1, h + 1):
                    w.set(x, y, z, *RED_SMOOTH)
                w.set(x, h, z, *(QUARTZ if x % 2 == 0 else SMOOTH))
                w.set(x, h - 2, z, B.SLAB, 9)              # a sandstone slab under the deck, top half
                continue
            if k == "post" and x < -30:                     # the Mirador's pad, hung over the void
                for y in range(h - 4, h + 1):
                    w.set(x, y, z, *RED_CHISELED if y == h - 2 else RED_SMOOTH)
                w.set(x, h, z, *QUARTZ_CHISELED)
                continue
            if k in ("water", "swim", "cage"):
                cistern = abs(x) <= 6 and abs(z) <= 6
                floor = P.CISTERN["floor"] if cistern else h - 3
                for y in range(BASE_Y, floor):
                    w.set(x, y, z, *body(x, y, z))
                w.set(x, floor, z, *(SEA_LANTERN if cistern and (x + z) % 4 == 0 else PRISMARINE_BRICK))
                top = h if k != "cage" else P.CISTERN["water"]
                for y in range(floor + 1, top + 1):
                    w.set(x, y, z, B.WATER)
                if k == "cage":
                    for y in range(P.CISTERN["water"] + 1, h + 1):
                        w.set(x, y, z, *CAGE)
                continue
            if k == "canal":
                for y in range(BASE_Y, G):
                    w.set(x, y, z, *body(x, y, z))
                w.set(x, G - 1, z, *(SEA_LANTERN if z % 6 == 0 and x == 0 else PRISMARINE))
                w.set(x, G, z, B.WATER)
                continue
            top = G if k in ("hedge", "column", "ladder") else h
            for y in range(BASE_Y, top + 1):
                w.set(x, y, z, *body(x, y, z))
            if k in ("floor", "spawn"):
                w.set(x, h, z, *ground_block(x, z))
            elif k == "stair":
                w.set(x, h, z, SANDSTONE_STAIRS, STAIR_DATA[R.stair[(x, z)]])
                for y in range(G + 1, h):
                    w.set(x, y, z, *SMOOTH)
            elif k == "stone":
                for y in range(G + 1, h):
                    w.set(x, y, z, *CHISELED)
                w.set(x, h, z, *QUARTZ_CHISELED)
            elif k == "hedge":
                w.set(x, G, z, *SMOOTH)
                if h >= G + 5:                              # a cypress
                    for y in range(G + 1, h + 1):
                        w.set(x, y, z, *CYPRESS)
                    w.set(x, h + 1, z, *CYPRESS)
                elif 10 <= abs(x) <= 12 and 10 <= abs(z) <= 12:
                    w.set(x, G + 1, z, *RED_SMOOTH)             # the court's planters: a box, leaves in it
                    w.set(x, G + 2, z, *HEDGE)
                else:
                    for y in range(G + 1, h + 1):
                        w.set(x, y, z, *HEDGE)
            elif k == "column":
                for y in range(G + 1, h):
                    w.set(x, y, z, *QUARTZ_PILLAR)
            elif k == "ladder":
                w.set(x, G, z, *SMOOTH)
            elif k == "wall":
                for y in range(G, h + 1):
                    w.set(x, y, z, *RED_SMOOTH)
            elif k == "post":
                pass                                        # the towers: built in towers()


def edges(w):
    """A fence along the board's edge where it drops to the void, on a coping of the team's clay — except
    beside the Mirador's bridge and behind the Minaret, where the void is the point."""
    for i in range(P.NX):
        for j in range(P.NZ):
            if R.K[i, j] != K["void"]:
                continue
            x, z = i + P.X_MIN, j + P.Z_MIN
            if x <= -30 and abs(z) <= 7 or x >= 43 and abs(z) <= 16:
                continue
            near = [(x + dx, z + dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))]
            if not any(k_at(a, b) in ("floor", "spawn", "hedge", "stair") and h_at(a, b) == G for a, b in near):
                continue
            for y in range(BASE_Y + 2, G):
                w.set(x, y, z, *body(x, y, z))
            w.set(x, G, z, *team_clay(z))
            w.set(x, G + 1, z, FENCE)


def roofs(w):
    """The arcades' roofs: terracotta over the walks, a course of red sandstone along their edges, and the
    quartz columns' capitals under them."""
    for i in range(P.NX):
        for j in range(P.NZ):
            if R.UK[i, j] != P.UKINDS["roof"]:
                continue
            x, z = i + P.X_MIN, j + P.Z_MIN
            u = int(R.U[i, j])
            edge = any(R.UK[i + di, j + dj] != P.UKINDS["roof"] for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            w.set(x, u, z, *(team_clay(z) if edge else (B.STAINED_CLAY, 1)))


def towers(w):
    """The posts' towers. The Cistern's rises from the pool's floor, red sandstone banded in chiseled, a beacon
    in its top and the flag's banner on it. The Minaret's rises from the garden with a ladder on each face."""
    for x in range(-1, 2):
        for z in range(-1, 2):
            for y in range(P.CISTERN["floor"], 25):
                w.set(x, y, z, *(RED_CHISELED if y % 4 == 0 else RED_SMOOTH))
            w.set(x, 24, z, *QUARTZ_CHISELED)
    w.set(0, 24, 0, *BEACON)
    w.banner(0, 25, 0, 5, patterns=[("bo", 15), ("mc", 15)], rot=0)   # purple, a white border and a roundel
    for x in range(29, 32):
        for z in range(-1, 2):
            for y in range(G + 1, 26):
                w.set(x, y, z, *(QUARTZ_CHISELED if y in (21, 25) else (RED_CHISELED if y == 23 else RED_SMOOTH)))
    w.set(30, 25, 0, *BEACON)
    for (x, z), facing in (((30, -2), 2), ((30, 2), 3), ((28, 0), 4), ((32, 0), 5)):
        for y in range(G + 1, 26):
            w.set(x, y, z, B.LADDER, facing)
    w.set(-42, 24, 0, *BEACON)


def spawn_house(w, team, sgn):
    """The spawn house: a solid block of red sandstone banded in the team's clay; inside it the patio at the
    ground with the pool, its ceiling the deck at 32; on the deck, the room a player spawns into, walled,
    lit, and floored in the team's check, with the hole over the pool. Built for blue; red is its mirror."""
    clay = (B.WOOL, 14 if team == "red" else 11)

    def S(x, y, z, b):
        w.set(x, y, sgn * z, *b)
    for x in range(-9, 10):
        for z in range(45, 59):
            for y in range(G + 1, 38):
                b = clay if y in (24, 30, 36) else (RED_CHISELED if y == 33 else RED_SMOOTH)
                S(x, y, z, b)
    # the patio, under the deck
    for x in range(-7, 8):
        for z in range(46, 57):
            for y in range(G + 1, 32):
                S(x, y, z, (B.AIR, 0))
            if not (-2 <= x <= 2 and 47 <= z <= 51):
                S(x, G, z, clay if (x // 2 + z // 2) % 2 == 0 else QUARTZ)
    for x in (-9, -8, 8, 9):                                  # the doors
        for z in range(50, 55):
            for y in range(G + 1, G + 4):
                S(x, y, z, (B.AIR, 0))
            S(x, G, z, SMOOTH)
            S(x, G + 4, z, RED_CHISELED)
    # the deck and the room on it
    for x in range(-7, 8):
        for z in range(46, 57):
            hole = -2 <= x <= 2 and 47 <= z <= 51
            S(x, 32, z, (B.AIR, 0) if hole else (clay if (x + z) % 2 == 0 else QUARTZ))
            for y in range(33, 37):
                S(x, y, z, (B.AIR, 0))
            S(x, 37, z, (B.GLOWSTONE, 0) if x % 4 == 0 and z % 4 == 0 else RED_SMOOTH)
    for x in range(-3, 4):                                    # a quartz lip round the hole
        for z in range(46, 53):
            if not (-2 <= x <= 2 and 47 <= z <= 51) and -7 <= x <= 7:
                S(x, 32, z, QUARTZ_CHISELED)
    # the team's banners on the house's front and either side of each door
    for x in (-5, 0, 5):
        w.banner(x, 34, sgn * 44, dye(team), patterns=[("bs", 15)], wall_facing=2 if sgn > 0 else 3)
    for x, facing in ((-10, 4), (10, 5)):
        for z in (49, 55):
            w.banner(x, G + 3, sgn * z, dye(team), wall_facing=facing)


def screens(w):
    """The screen walls in front of each spawn door: red sandstone, the team's clay through them."""
    for sgn, team in ((1, "blue"), (-1, "red")):
        clay = (B.WOOL, 14 if team == "red" else 11)
        for x in (-13, 13):
            for z in range(44, 58):
                for y in range(G + 1, 26):
                    w.set(x, y, sgn * z, *(clay if y in (22, 25) else RED_SMOOTH))


def kiosks(w):
    """The large cover: the west garden's kiosk, in red sandstone under a quartz dome; the east garden's
    fountain house, in terracotta with a quartz cornice and a fountain on its roof."""
    for sgn in (1, -1):
        for x in range(-28, -21):
            for z in range(24, 31):
                for y in range(G + 1, 27):
                    edge = x in (-28, -22) or z in (24, 30)
                    arch = edge and (x in (-26, -24) or z in (26, 28)) and G + 1 <= y <= G + 3
                    w.set(x, y, sgn * z, *(RED_CHISELED if arch else (QUARTZ if y == 26 else RED_SMOOTH)))
        for r, y in ((2, 27), (1, 28), (0, 29)):
            for x in range(-25 - r, -24 + r):
                for z in range(27 - r, 28 + r):
                    w.set(x, y, sgn * z, *QUARTZ)
        for x in range(22, 29):
            for z in range(24, 31):
                for y in range(G + 1, 27):
                    w.set(x, y, sgn * z, *(QUARTZ if y in (23, 26) else TERRACOTTA))
        for x in range(23, 28):
            for z in range(25, 30):
                w.set(x, 26, sgn * z, *PRISMARINE_BRICK)
        w.set(25, 27, sgn * 27, *QUARTZ_PILLAR)
        w.set(25, 28, sgn * 27, B.WATER)


def porch(w):
    """The Mirador's porch: a parapet of red sandstone stairs along its west lip either side of the bridge,
    and its edge to the court picked out in chiseled quartz."""
    for z in range(-5, 6):
        w.set(-20, 24, z, *QUARTZ_CHISELED)
    for z in list(range(-5, -1)) + list(range(2, 6)):
        w.set(-30, 25, z, 180, 1)                           # red sandstone stairs, low cover at the bridge's head


def make():
    w = World(P.X_MIN - 1, P.Z_MIN - 1, P.NX + 2, P.NZ + 2, sy=48)
    columns(w)
    edges(w)
    roofs(w)
    towers(w)
    spawn_house(w, "blue", 1)
    spawn_house(w, "red", -1)
    screens(w)
    kiosks(w)
    porch(w)
    w.biome[:, :] = 1
    return w


def main(build):
    t0 = time.time()
    w = make()
    w.save(build, "Riad", (0, 40, 0))
    print(f"generated and saved {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
