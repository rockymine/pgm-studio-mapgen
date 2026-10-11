"""Generate Penstock: red's half (x < 0) is carved out of one block of concrete and painted, then mirrored onto
blue's (x -> -1 - x) and recoloured.

    python3 gen.py <build-dir>

The order is the station's: the mass; the spaces carved out of it; the decks, flights and tunnels put back
into them; the shafts cut through everything to the void; then the paint, read off which faces of the mass
are exposed; then the furniture — cover, rails, the dais, the generators, the boxes, the spawn.
"""
import math
import sys
import time

import numpy as np

import plan as P
from mc import World, B
from mirror import mirror_world

TEAM = 14                                   # red's colour; blue's half is recoloured to 11 after the mirror
CONCRETE = (B.DSLAB, 8)                    # smooth stone, all faces: the station's concrete
DARK = (B.STAINED_CLAY, 9)                  # cyan, which reads dark grey: base courses and beams
WHITE = (B.QUARTZ, 0)
SMOOTH = (B.STONE, 0)                       # plain stone: the field of the floors
POL_AND = (B.STONE, 6)
SEA = (169, 0)
BARS = (B.IRON_BARS, 0)
HAZ_Y, HAZ_K = (B.STAINED_CLAY, 4), (B.STAINED_CLAY, 15)
SB_STAIRS = B.STONEBRICK_STAIRS


def box_fill(w, x0, x1, z0, z1, y0, y1, blk):
    w.fill(x0, y0, z0, x1, y1, z1, *blk)


def carve(w, x0, x1, z0, z1, y0, y1):
    w.fill(x0, y0, z0, x1, y1, z1, B.AIR)


def space_of(x, z, y):
    """Which planned space a cell of air belongs to, for the paint."""
    for s in P.SPACES:
        x0, x1, z0, z1 = s["box"]
        if x0 <= x <= x1 and z0 <= z <= z1 and s["floor"] < y < s["ceil"]:
            return s["key"]
    return None


# ---- the mass and the carving ---------------------------------------------------------------------------------
def mass(w):
    box_fill(w, P.X_MIN, -1, P.Z_MIN, P.Z_MAX, P.MASS_BOTTOM, P.ROOF, CONCRETE)
    # the underside steps in toward the middle, a dam's foot rather than a brick
    for k in range(1, 5):
        y = P.MASS_BOTTOM - k
        box_fill(w, P.X_MIN + 3 * k, -1, P.Z_MIN + 3 * k, P.Z_MAX - 3 * k, y, y, CONCRETE)


def spaces(w):
    for s in P.SPACES:
        x0, x1, z0, z1 = s["box"]
        carve(w, x0, x1, z0, z1, s["floor"] + 1, s["ceil"] - 1)
    # doorways from the corridors and pump rooms into the hall, through both long walls
    for x0, x1 in P.DOORS:
        for z in (-37, 36):
            carve(w, x0, x1, z, z, 21, 24)
    # the corridors open into the gallery at their west ends (x -44 is gallery); nothing to cut
    # the spawn's two doors, in its front wall at x -56
    for f in P.FLIGHTS:
        if f["key"].startswith("exit"):
            _, _, z0, z1 = f["box"]
            carve(w, -56, -56, z0, z1, 25, 28)
    for f in P.FLIGHTS:                                       # the niches before the walk's flights
        if f["key"].startswith("walk"):
            _, _, z0, z1 = f["box"]
            carve(w, P.NICHE[0], P.NICHE[1], z0, z1, 21, 23)
    # the score boxes' alcoves, behind the gallery's back wall
    for b in P.BOXES:
        z0, z1 = b["z"]
        carve(w, P.BOX_X[0], -56, z0, z1, P.BOX_FLOOR + 1, P.BOX_FLOOR + 3)
        box_fill(w, P.BOX_X[0], -56, z0, z1, 20, P.BOX_FLOOR, CONCRETE)


def decks(w):
    for d in P.DECKS + P.LANDINGS:
        x0, x1, z0, z1 = d["box"]
        box_fill(w, x0, x1, z0, z1, d["y"], d["y"], CONCRETE)


def flights(w):
    """Solid stairs: each column of the flight filled from the floor below to its step, a stair block on top."""
    for f in P.FLIGHTS:
        x0, x1, z0, z1 = f["box"]
        cells = range(x0, x1 + 1) if f["axis"] == "x" else range(z0, z1 + 1)
        order = list(cells) if f["step"] > 0 else list(cells)[::-1]
        base = 20
        for k, c in enumerate(order):
            y = min(f["y0"] + k, f["y1"])
            data = (0 if f["step"] > 0 else 1) if f["axis"] == "x" else (2 if f["step"] > 0 else 3)
            if f["axis"] == "x":
                box_fill(w, c, c, z0, z1, base, y - 1, CONCRETE)
                for z in range(z0, z1 + 1):
                    w.set(c, y, z, SB_STAIRS, data)
            else:
                box_fill(w, x0, x1, c, c, base, y - 1, CONCRETE)
                for x in range(x0, x1 + 1):
                    w.set(x, y, c, SB_STAIRS, data)


def tunnels(w):
    tf = P.TUNNEL_FLOOR
    for t in P.TUNNELS:
        z0, z1 = t["z"]
        a, b = P.TUNNEL_RUN
        carve(w, a, b, z0, z1, tf + 1, tf + 4)
        # down from the gallery: the first step at 19, descending east to the tunnel floor
        d0, d1 = P.TUNNEL_DOWN
        for k, x in enumerate(range(d0, d1 + 1)):
            y = 19 - k
            carve(w, x, x, z0, z1, y + 1, 20)
            carve(w, x, x, z0, z1, y + 1, y + 4)
            if y > tf:
                for z in range(z0, z1 + 1):
                    w.set(x, y, z, SB_STAIRS, 1)            # ascending west, back up to the gallery
        # up into the hall: rising east from 15 to 19, the hall floor at 20 beyond
        u0, u1 = P.TUNNEL_UP
        for k, x in enumerate(range(u0, u1 + 1)):
            y = tf + 1 + k
            carve(w, x, x, z0, z1, y + 1, 20)
            for z in range(z0, z1 + 1):
                w.set(x, y, z, SB_STAIRS, 0)
        # rails round the hall-floor opening of the up-stair, so its sides are a wall rather than a drop
        for x in range(u0, u1 + 1):
            for z in (z0 - 1, z1 + 1):
                w.set(x, 21, z, *BARS)


def shafts(w):
    for s in P.SHAFTS:
        x0, x1, z0, z1 = s["box"]
        carve(w, x0, x1, z0, z1, 0, 20)
        # hazard stripes round the lip, rails on the two long sides only
        for x in range(x0 - 1, x1 + 2):
            for z in range(z0 - 1, z1 + 2):
                if not (x0 <= x <= x1 and z0 <= z <= z1):
                    w.set(x, 20, z, *(HAZ_Y if (x + z) % 2 == 0 else HAZ_K))
        for x in range(x0, x1 + 1):
            w.set(x, 21, z0 - 1, *BARS)
            w.set(x, 21, z1 + 1, *BARS)


# ---- paint ------------------------------------------------------------------------------------------------
TEAM_SPACES = ("spawn", "gallery", "corridor-0", "corridor-1")


def paint(w):
    """Read every exposed face of the mass and paint it by what it faces: floors, walls, ceilings."""
    ids = w.ids
    solid = (ids != B.AIR)
    air = ~solid
    x0 = w.x0
    for i in range(0, -x0):                              # red's half only
        x = x0 + i
        for k in range(w.sz):
            z = w.z0 + k
            col = ids[i, :, k]
            for y in range(P.MASS_BOTTOM - 4, P.ROOF + 1):
                if col[y] != CONCRETE[0] or w.dat[i, y, k] != CONCRETE[1]:
                    continue
                up = y + 1 < w.sy and air[i, y + 1, k]
                down = y > 0 and air[i, y - 1, k]
                side = any(0 <= i + di < w.sx and 0 <= k + dk < w.sz and air[i + di, y, k + dk]
                           for di, dk in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                if up:
                    w.set(x, y, z, *floor_block(x, y, z))
                elif down and not side:
                    w.set(x, y, z, *ceiling_block(x, y, z))
                elif side:
                    w.set(x, y, z, *wall_block(x, y, z, i, k, air))


def floor_block(x, y, z):
    sp = space_of(x, z, y + 1)
    if y == 27:                                          # decks: steel grating look
        return (B.STAINED_CLAY, 9) if (x + z) % 2 else POL_AND
    if sp == "hall":
        if x % 6 == 0 or z % 6 == 0:
            return POL_AND
        if x <= -38:                                    # the team's end of the hall: a band of its colour
            return (B.STAINED_CLAY, TEAM) if (x + z) % 4 == 0 else SMOOTH
        return SMOOTH
    if sp == "spawn":
        return (B.STAINED_CLAY, TEAM) if (x // 2 + z // 2) % 2 == 0 else WHITE
    if sp in ("gallery",) or (sp and sp.startswith("corridor")):
        if z % 4 == 0:
            return (B.STAINED_CLAY, TEAM)
        return SMOOTH if (x + z) % 3 else POL_AND
    if sp and sp.startswith("pumps"):
        return POL_AND if (x + z) % 2 else SMOOTH
    if y == P.TUNNEL_FLOOR:
        return (B.STONEBRICK, 0)
    if y < 0 or sp is None and y < 14:
        return CONCRETE
    return SMOOTH


def ceiling_block(x, y, z):
    if (x % 6 == 0 and z % 6 == 0):
        return SEA
    if x % 6 == 0:
        return DARK                                      # the beams
    return CONCRETE


def wall_block(x, y, z, i, k, air):
    # which space the face looks into, and how high above its floor this course is
    sp, fl = None, 20
    for di, dk in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ii, kk = i + di, k + dk
        if 0 <= ii and 0 <= kk < air.shape[2] and ii < air.shape[0] and air[ii, y, kk]:
            xx, zz = x + di, z + dk
            for s in P.SPACES:
                a, b, c, d = s["box"]
                if a <= xx <= b and c <= zz <= d and s["floor"] < y < s["ceil"]:
                    sp, fl = s["key"], s["floor"]
            break
    h = y - fl
    if y < 20:
        return (B.STONEBRICK, 0) if (x + z + y) % 5 else (B.STONEBRICK, 2)       # the tunnels: brick-lined
    if h == 1:
        return DARK
    if h == 2 and sp in TEAM_SPACES:
        return (B.STAINED_CLAY, TEAM)
    if h == 2:
        return WHITE
    if sp in ("hall", "gallery") and y >= P.ROOF - 2:
        return DARK
    if (x % 6 == 0) or (z % 6 == 0):
        return (B.STONEBRICK, 0) if h > 2 else DARK                              # pilasters
    if sp in TEAM_SPACES and h == 5 and (x + z) % 3 == 0:
        return (B.STAINED_CLAY, TEAM)                                             # a second, broken band
    return CONCRETE


# ---- furniture --------------------------------------------------------------------------------------------
def rails(w):
    """Iron bars along every deck edge that drops to a floor, except where a flight or another deck meets it."""
    deck = np.zeros((w.sx, w.sz), bool)
    for d in P.DECKS + P.LANDINGS:
        x0, x1, z0, z1 = d["box"]
        deck[x0 - w.x0:x1 - w.x0 + 1, z0 - w.z0:z1 - w.z0 + 1] = True
    deck[-w.x0:, :] = deck[:-w.x0, :][::-1, :]          # the mirror, so the gantry's red half sees its partner
    for i in range(0, -w.x0):
        for k in range(w.sz):
            if not deck[i, k]:
                continue
            x, z = w.x0 + i, w.z0 + k
            for di, dk in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ii, kk = i + di, k + dk
                if not (0 <= ii < w.sx and 0 <= kk < w.sz) or deck[ii, kk]:
                    continue
                if w.id(x + di, 27, z + dk) != B.AIR or w.id(x + di, 26, z + dk) != B.AIR:
                    continue
                # a flight arriving here is a way on, not a drop
                if w.id(x + di, 26, z + dk) in (SB_STAIRS,):
                    continue
                if w.id(x, 28, z) == B.AIR:
                    w.set(x, 28, z, *BARS)
    # the flights' tops: clear the bar where a flight's last step meets a deck or landing
    for f in P.FLIGHTS:
        x0, x1, z0, z1 = f["box"]
        if f["y1"] == 26:
            xe = x1 + 1 if f["step"] > 0 else x0 - 1
            for z in range(z0, z1 + 1):
                if w.id(xe, 28, z) == B.IRON_BARS:
                    w.set(xe, 28, z, B.AIR)
    # the landings join the catwalks on their wall side: open that edge
    for L in P.LANDINGS:
        x0, x1, z0, z1 = L["box"]
        ze = z0 if z0 < 0 else z1
        for x in range(x0, x1 + 1):
            w.set(x, 28, ze, B.AIR)


def dais(w):
    """The Exciter: a dais two high with steps all round, a ring of sea lanterns, the diamond spawner's plinth."""
    for r, y in ((5, 21), (4, 22)):
        for x in range(-1 - r, 0):
            for z in range(-1 - r, r + 1):
                if max(abs(x + 0.5), abs(z + 0.5)) <= r + 0.5:
                    w.set(x, y, z, *(POL_AND if y == 21 else WHITE))
    for z in range(-5, 5):
        w.set(-6, 21, z, B.SLAB, 8 + 0)                                        # a slab skirt to step onto
    for x in range(-6, 0):
        for z in (-6, 5):
            w.set(x, 21, z, B.SLAB, 8 + 0)
    for x, z in ((-1, -1), (-1, 0)):
        w.set(x, 22, z, *SEA)
    for x, z in ((-4, -4), (-4, 3)):
        for y in range(23, 27):
            w.set(x, y, z, *BARS)


def generators(w):
    """Two turbine housings a side: a drum four high, a domed cap, a dark band round its waist. Cover."""
    for cx, cz in P.GENERATORS:
        for x in range(int(cx - 6), int(cx + 7)):
            for z in range(int(cz - 6), int(cz + 7)):
                d = math.hypot(x - cx, z - cz)
                if d <= P.GEN_R:
                    for y in range(21, 25):
                        w.set(x, y, z, *(DARK if y == 23 else CONCRETE if d > P.GEN_R - 1.2 else WHITE))
                    if d <= P.GEN_R - 1.5:
                        w.set(x, 25, z, *WHITE)
                    if d <= 1.2:
                        w.set(x, 26, z, *SEA)


def cover(w):
    """Crates and low walls in the hall and the gallery: places to stand behind and to heal."""
    def crate(x, z, h=2):
        for dx in (0, 1):
            for dz in (0, 1):
                for y in range(21, 21 + h):
                    w.set(x + dx, y, z + dz, *((B.LOG, 1) if (dx + dz + y) % 2 else (B.PLANKS, 1)))

    def low_wall(x0, x1, z0, z1, h=2):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                for y in range(21, 21 + h):
                    w.set(x, y, z, *((B.STONEBRICK, 0) if y < 20 + h else (B.SLAB, 5)))
                w.set(x, 20 + h, z, B.SLAB, 5)
                for y in range(21, 20 + h):
                    w.set(x, y, z, B.STONEBRICK, 0)
    # the hall
    for z in (-8, 6):
        crate(-36, z)
    crate(-30, -2, 3); crate(-30, 0, 2)
    low_wall(-20, -20, -6, -1, 2); low_wall(-20, -20, 0, 5, 2)
    low_wall(-8, -5, -22, -22, 2); low_wall(-8, -5, 21, 21, 2)
    crate(-14, -32 + 6); crate(-14, 24)
    low_wall(-34, -31, -26, -26, 3); low_wall(-34, -31, 25, 25, 3)
    # the gallery
    for z in (-26, 25, -14, 13):
        crate(-48, z)
    low_wall(-50, -47, -2, -2, 2); low_wall(-50, -47, 1, 1, 2)
    # the pump rooms: two pumps each, drums of iron bars round a core
    for zc in (-42, 41):
        for xc in (-12, -6):
            for y in range(21, 24):
                w.set(xc, y, zc, *DARK)
                for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    w.set(xc + dx, y, zc + dz, *BARS)
            w.set(xc, 24, zc, B.SLAB, 5)


def boxes(w):
    """The score boxes: an alcove behind the gallery's back wall, lined in the team's glass, lit, and guarded
    by cobweb — a curtain in the doorway, or a strip on the floor before it."""
    for b in P.BOXES:
        z0, z1 = b["z"]
        xa, xb = P.BOX_X
        for x in range(xa, xb + 1):
            for z in range(z0, z1 + 1):
                w.set(x, P.BOX_FLOOR, z, B.GOLD_BLOCK if (x + z) % 2 else B.STAINED_CLAY, 4 if (x + z) % 2 == 0 else 0)
                w.set(x, P.BOX_FLOOR + 4, z, *SEA)
        for x in range(xa - 1, xb + 1):
            for y in range(P.BOX_FLOOR + 1, P.BOX_FLOOR + 4):
                for z in (z0 - 1, z1 + 1):
                    w.set(x, y, z, 95, TEAM)
        for z in range(z0, z1 + 1):
            for y in range(P.BOX_FLOOR + 1, P.BOX_FLOOR + 4):
                w.set(xa - 1, y, z, 95, TEAM)
        # a frame round the opening in the back wall, so it reads from the spawn's doors
        for z in range(z0 - 1, z1 + 2):
            w.set(-56, P.BOX_FLOOR + 4, z, *HAZ_Y if z % 2 else HAZ_K)
        for y in range(P.BOX_FLOOR, P.BOX_FLOOR + 4):
            w.set(-56, y, z0 - 1, *HAZ_Y if y % 2 else HAZ_K)
            w.set(-56, y, z1 + 1, *HAZ_Y if y % 2 else HAZ_K)
        if b["guard"] == "door":
            for z in range(z0, z1 + 1):
                for y in (P.BOX_FLOOR + 1, P.BOX_FLOOR + 2):
                    w.set(-56, y, z, B.COBWEB)
        else:
            for x in (-55, -54):
                for z in range(z0, z1 + 1):
                    w.set(x, 21, z, B.COBWEB)


def spawn(w):
    """The Gatehouse: the shop counter at the back, banners, windows over the gallery either side of each door."""
    # the counter where the shopkeeper stands
    for z in range(-9, -3):
        w.set(-66, 25, z, B.DARK_OAK_STAIRS, 1 | 4) if z not in (-7, -6) else None
    for z in (-9, -4):
        w.set(-66, 25, z, B.PLANKS, 5)
    w.set(-69, 27, -7, B.WOOL, TEAM); w.set(-69, 28, -7, B.WOOL, TEAM)
    # windows in the front wall over the gallery: iron bars between and beside the doors
    for z in list(range(-4, 4)) + list(range(-11, -9)) + list(range(9, 11)):
        for y in (26, 27):
            if w.id(-56, y, z) != B.AIR:
                w.set(-56, y, z, *BARS)
    # windows in the back wall's flanks over the score boxes' approach
    for z in list(range(-30, -14)) + list(range(13, 29)):
        if z % 3 == 0:
            for y in (25, 26):
                pass
    # banners of the team on the side walls
    for z in (-10, 9):
        for x in (-64, -60):
            w.set(x, 28, z, B.WOOL, TEAM); w.set(x, 29, z, B.WOOL, TEAM)
    # lights
    for x in (-66, -60):
        for z in (-6, 5):
            w.set(x, 31, z, *SEA)


def windows_and_roof(w):
    """High windows in the outer walls and strips of skylight over the hall."""
    for x in range(P.X_MIN + 3, -1):
        if x % 6 == 3:
            for y in range(30, 34):
                for z in (P.Z_MIN, P.Z_MAX):
                    if w.id(x, y, z) != B.AIR:
                        w.set(x, y, z, B.PANE, 0)
    for x in range(-40, -1):
        if x % 6 in (2, 3):
            for z in range(-30, 30):
                w.set(x, P.ROOF, z, B.GLASS)
    # the roof's top: smooth stone with a parapet of dark
    for x in range(P.X_MIN, 0):
        for z in range(P.Z_MIN, P.Z_MAX + 1):
            if w.id(x, P.ROOF, z) == CONCRETE[0] and w.dat[x - w.x0, P.ROOF, z - w.z0] == CONCRETE[1]:
                w.set(x, P.ROOF, z, *SMOOTH)
    for x in range(P.X_MIN, 0):
        for z in (P.Z_MIN, P.Z_MAX):
            w.set(x, P.ROOF + 1, z, *DARK)
    for z in range(P.Z_MIN, P.Z_MAX + 1):
        w.set(P.X_MIN, P.ROOF + 1, z, *DARK)


def exterior(w):
    """Buttresses down the outer walls, so the station reads as a dam's powerhouse from the void."""
    for x in range(P.X_MIN + 2, -1, 8):
        for z in (P.Z_MIN - 1, P.Z_MAX + 1):
            for y in range(P.MASS_BOTTOM - 2, P.ROOF + 1):
                w.set(x, y, z, *DARK)
                w.set(x + 1, y, z, *DARK)
    for z in range(P.Z_MIN + 4, P.Z_MAX - 3, 8):
        for y in range(P.MASS_BOTTOM - 2, P.ROOF + 1):
            w.set(P.X_MIN - 1, y, z, *DARK)


def penstocks_overhead(w):
    """The station's pipes, made visible: a penstock runs under the roof from the gallery wall to each generator,
    and drops into it. Dark pipe banded with quartz every six; high over the play, out of the way of the decks."""
    for cx, cz in P.GENERATORS:
        r = 2.4
        yc = 32.5
        for x in range(-55, int(cx) + 1):
            band = (x % 6 == 0)
            for y in range(29, 36):
                for z in range(int(cz - 3), int(cz + 4)):
                    d = math.hypot(y - yc, z - cz)
                    if d <= r:
                        w.set(x, y, z, *((B.QUARTZ, 0) if band else DARK))
        # the drop into the housing: an elbow over the generator, down to its dome
        for y in range(26, 31):
            for x in range(int(cx - 2), int(cx + 3)):
                for z in range(int(cz - 2), int(cz + 3)):
                    if math.hypot(x - cx, z - cz) <= 1.8:
                        w.set(x, y, z, *((B.QUARTZ, 0) if y == 28 else DARK))


def crane(w):
    """An overhead crane across the hall at x -32: a beam on the walls at 33, a trolley, a hook hanging."""
    for z in range(-36, 36):
        w.set(-32, 33, z, *DARK); w.set(-31, 33, z, *DARK)
        w.set(-32, 34, z, B.SLAB, 5 + 8); w.set(-31, 34, z, B.SLAB, 5 + 8)
    for z in (-6, -5, 4, 5):
        pass
    for x in (-33, -32, -31, -30):
        for z in (-2, -1, 0, 1):
            w.set(x, 32, z, *((B.STAINED_CLAY, 4) if (x + z) % 2 else HAZ_K))
    for y in range(28, 32):
        w.set(-32, y, -1, B.FENCE)
    w.set(-32, 27, -1, B.IRON_BLOCK); w.set(-32, 26, -1, B.ANVIL)


def floor_rings(w):
    """Rings round the Exciter in quartz and dark, and a hazard ring round each generator's foot."""
    for x in range(-20, 0):
        for z in range(-20, 20):
            d = math.hypot(x + 0.5, z + 0.5)
            if w.id(x, 20, z) in (B.STONE, B.DSLAB) and w.id(x, 21, z) == B.AIR:
                if 8.5 <= d < 9.5:
                    w.set(x, 20, z, B.QUARTZ, 0)
                elif 12.5 <= d < 13.5:
                    w.set(x, 20, z, *DARK)
    for cx, cz in P.GENERATORS:
        for x in range(int(cx - 7), int(cx + 8)):
            for z in range(int(cz - 7), int(cz + 8)):
                d = math.hypot(x - cx, z - cz)
                if P.GEN_R + 0.3 <= d < P.GEN_R + 1.3 and w.id(x, 21, z) == B.AIR:
                    w.set(x, 20, z, *(HAZ_Y if (x + z) % 2 == 0 else HAZ_K))


def murals(w):
    """The team's colour, large: diagonal bands on the gallery's back wall over the spawn, on the deck's edge,
    and a chevron on the hall floor at the team's end pointing at the enemy."""
    for z in range(-36, 36):
        for y in range(29, 35):
            if w.id(-56, y, z) not in (B.AIR, B.IRON_BARS) and w.id(-55, y, z) == B.AIR:
                w.set(-56, y, z, *(((B.STAINED_CLAY, TEAM) if (y + z) % 6 < 3 else (B.QUARTZ, 0))))
    for z in range(-30, 30):
        w.set(-44, 27, z, B.STAINED_CLAY, TEAM)
    for z in range(-12, 12):
        for x in range(-42, -34):
            k = x + 42 - abs(z + 0.5) * 0.6
            if 0 <= k % 6 < 2 and w.id(x, 21, z) == B.AIR and w.id(x, 20, z) != B.AIR:
                w.set(x, 20, z, B.STAINED_CLAY, TEAM)


def make():
    w = World(P.X_MIN - 2, P.Z_MIN - 2, (P.X_MAX - P.X_MIN + 1) + 4, (P.Z_MAX - P.Z_MIN + 1) + 4, sy=P.Y_TOP)
    mass(w)
    spaces(w)
    decks(w)
    flights(w)
    tunnels(w)
    paint(w)
    shafts(w)
    rails(w)
    dais(w)
    generators(w)
    cover(w)
    boxes(w)
    spawn(w)
    windows_and_roof(w)
    exterior(w)
    penstocks_overhead(w)
    crane(w)
    floor_rings(w)
    murals(w)
    mirror_world(w)
    blue = np.zeros((w.sx, 1, w.sz), bool); blue[-w.x0:, :, :] = True
    for bid in (B.STAINED_CLAY, B.WOOL, 95, B.STAINED_PANE):
        m = (w.ids == bid) & (w.dat == TEAM) & blue
        w.dat[m] = 11
    w.biome[:, :] = 1
    return w


def main(build):
    t0 = time.time()
    w = make()
    w.save(build, "Penstock", (0, 40, 0))
    print(f"generated and saved {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
