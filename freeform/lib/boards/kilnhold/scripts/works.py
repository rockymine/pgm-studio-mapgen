"""What is built on the outside of the bunker, in red's half: the facade and its bastions, the apron, the cooling
tower and the quarry pit, the two ramps to the Crown, and the roof deck.

    build(w, L)   lay all of it; returns what it made, for the checks
"""
import math

import numpy as np

import kit
import plan as P
from kit import (AIR, ANDESITE, BARS, BLACK, BROWN, COBBLE, COAL, GLOW, GREY, IRON, LAVA, LOG_DARK, OAK_DARK, ORANGE, PAND,
                 RCHISEL, RSMOOTH, RSANDSTONE, SB, SBCHISEL, SBCRACK, SEA, STONE, TEAM_WOOL, put, fill)
from pgmvox import B

WALL = (B.COBBLE_WALL, 0)


def paving(x, z):
    """The made ground's four tones, laid a cell each."""
    return kit.pick([SB, PAND, ANDESITE, STONE], kit.cell_key(x, z, 3))


# ---------------------------------------------------------------------------------------------------------------
def road(w, cells, clear=6, rail=True, surface=None):
    """Lay a ramp's floor cells [(x, z, y, slab)] over the ground: fill under the rising run, cut the ground over it,
    face the cut and the fill in stone brick, a low wall on the open side. Returns the cells' surface y by column."""
    cols = {(x, z): (y, slab) for x, z, y, slab in cells}
    for (x, z), (y, slab) in cols.items():
        ground = w.top(x, z)
        for yy in range(max(ground + 1, 1), y):
            put(w, x, yy, z, SB)
        for yy in range(y + 1, y + clear + 1):
            if w.id(x, yy, z) != B.AIR:
                w.set(x, yy, z, B.AIR, 0)
    for (x, z), (y, slab) in cols.items():
        edge = any((x + dx, z + dz) not in cols for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        blk = RSMOOTH if edge else (surface(x, z) if surface else kit.pick([SB, PAND, ANDESITE, PAND], kit.cell_key(x, z, 2)))
        if slab:
            put(w, x, y, z, (B.SLAB, 0 if blk != RSMOOTH else 0))
            if blk == RSMOOTH:
                put(w, x, y, z, (B.RED_SANDSTONE_SLAB, 0))
        else:
            put(w, x, y, z, blk)
    for (x, z), (y, slab) in cols.items():
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, z + dz)
            if n in cols:
                continue
            nt = w.top(*n)
            if nt > y:                                       # a cut: face it as high as the ground stands, to a wall
                for yy in range(y + 1, min(nt, y + clear) + 1):
                    put(w, n[0], yy, n[1], SB if yy % 4 else SBCHISEL)
            else:                                            # a fill: face it from the ground, a low wall on top
                for yy in range(nt + 1, y + 1):
                    put(w, n[0], yy, n[1], SB if (y - yy) % 4 else SBCHISEL)
                if rail and y - nt >= 2:
                    put(w, n[0], y + 1, n[1], WALL)
    return cols


# ---------------------------------------------------------------------------------------------------------------
def facade(w):
    """The gatehouse: a wall of stone brick on the rock's face, pilasters stepped out, panels sunk behind them,
    bands inset, a portal frame round the gate, bastions at both ends."""
    Y0, top = P.APRON, P.FACADE_TOP
    x0, x1 = -20, 19
    fill(w, x0, Y0, -53, x1, top, -48, SB)
    fill(w, x0, Y0, -48, x1, Y0 + 1, -48, PAND)               # plinth
    for x in range(x0, x1 + 1):
        put(w, x, 70, -48, RSMOOTH)                            # bands, flush
        put(w, x, 74, -48, SBCHISEL)
        put(w, x, top, -48, PAND)
    piers = [(-19, -18), (-14, -13), (-10, -9)]                # pilasters stepped out a block
    piers += [(-1 - b, -1 - a) for a, b in piers]
    for a, b in piers:
        for y in range(Y0, top):
            for x in range(a, b + 1):
                put(w, x, y, -47, SBCHISEL if y in (Y0, Y0 + 1, top - 2, top - 1) else SB)
        for x in range(a, b + 1):
            put(w, x, top, -47, PAND)
    panels = [(-17, -15), (-12, -11)]                          # panels sunk between them, lit by a slit
    panels += [(-1 - b, -1 - a) for a, b in panels]
    for a, b in panels:
        for x in range(a, b + 1):
            for y in range(67, 73):
                put(w, x, y, -48, AIR)
                put(w, x, y, -49, kit.GREY if False else SBCRACK)
            put(w, x, 72, -49, GLOW)
            put(w, x, 66, -48, PAND)
    for xa, xb in ((-8, -6), (5, 7)):                          # the portal frame stands out two blocks
        for y in range(Y0, top - 1):
            for x in range(xa, xb + 1):
                for z in (-47, -46):
                    put(w, x, y, z, SB if y % 4 else SBCHISEL)
    for x in range(-8, 8):
        for y in range(74, top):
            for z in (-47, -46):
                put(w, x, y, z, RSMOOTH if y == 75 else SB if y != top - 1 else SBCHISEL)
    for x in (-7, 6):
        for y in (70, 66):
            pass
        w.banner(x, 71, -45, 1, [("bo", 0)], wall_facing=3)
    for x in range(x0, x1 + 1):                                # merlons along the top
        if x % 2 == 0:
            put(w, x, top + 1, -48, SB)
    for xa, xb in ((-27, -21), (20, 26)):                      # bastions at both ends
        fill(w, xa, Y0, -52, xb, top + 4, -44, SB)
        for x in range(xa, xb + 1):
            put(w, x, Y0 + 1, -44, PAND)
            put(w, x, 70, -44, RSMOOTH)
            put(w, x, top, -44, RSMOOTH)
            if x % 2 == 0:
                put(w, x, top + 5, -44, SB)
        for x in (xa + 1, xa + 3, xa + 5):
            for y in (72, 73, 74):
                put(w, x, y, -44, AIR)
                put(w, x, y, -45, BLACK if y != 74 else GLOW)
        for x in (xa, xb):
            for y in range(Y0, top + 4):
                put(w, x, y, -44, SBCHISEL if y in (Y0, Y0 + 1, top + 3) else SB)


def apron(w, L):
    ax0, ax1, az0, az1 = P.APRON_BOX
    S = P.APRON
    for x in range(ax0, ax1 + 1):
        for z in range(az0, az1 + 1):
            border = x in (ax0, ax1) or z == az1
            if border:
                put(w, x, S, z, PAND)
            elif abs(x + 0.5) < 3.1:
                put(w, x, S, z, PAND if (z % 6) else RSMOOTH)         # the way in, ribbed
            elif abs(x + 0.5) in (14.5, 15.5) or z == az0 + 1:
                put(w, x, S, z, RSMOOTH)
            else:
                put(w, x, S, z, paving(x, z))
            # the edge column faces the drop
            if border:
                ground = int(L.H[x - P.X_MIN, z - P.Z_MIN]) if False else None
    # facing on the retaining sides: south and the two ends down to the field
    for x in range(ax0, ax1 + 1):
        for z in range(az0, az1 + 1):
            if x in (ax0, ax1) or z == az1:
                for y in range(P.FIELD - 3, S):
                    put(w, x, y, z, SB if (S - y) % 4 else SBCHISEL)
    # two ramps down to the field, one at each end of the south edge: three blocks over six cells, four wide; the
    # edge between them is a retaining wall, so a way to the gate runs the apron's length
    for xa, xb in ((-25, -22), (21, 24)):
        cells = kit.ramp_cells((xa, xb), (az1, az1 + 6), "+z", S, flat=0, fall=True, level=P.FIELD)
        road(w, cells, clear=4, rail=True, surface=paving)
    # heat grilles: lava under bars, a block of brick between them and the way
    for gx0 in (-13, 8):
        for x in range(gx0, gx0 + 5):
            for z in range(-42, -37):
                put(w, x, S, z, BARS)
                put(w, x, S - 1, z, LAVA)
                put(w, x, S - 2, z, LAVA)
                put(w, x, S - 3, z, kit.OBSIDIAN)
        for x in range(gx0 - 1, gx0 + 6):
            for z in (-43, -37):
                put(w, x, S, z, RSMOOTH)
        for z in range(-42, -37):
            put(w, gx0 - 1, S, z, RSMOOTH)
            put(w, gx0 + 5, S, z, RSMOOTH)


# ---------------------------------------------------------------------------------------------------------------
def tower(w, L):
    tx, tz = P.TOWER
    for x in range(int(tx) - 12, int(tx) + 12):
        for z in range(int(tz) - 12, int(tz) + 12):
            u, v = x + 0.5 - tx, z + 0.5 - tz
            r = math.hypot(u, v)
            ground = w.top(x, z)
            north = -v / max(r, 1e-6)
            h = int(round(76 + 6 * north + 2.0 * math.sin(math.atan2(v, u) * 5.0)))
            if P.TOWER_R_IN <= r <= P.TOWER_R_OUT:
                for y in range(max(ground, P.PIT) + 1, h + 1):
                    blk = SB if y % 6 else SBCRACK
                    if y == 68:
                        blk = ORANGE
                    put(w, x, y, z, blk)
            elif P.TOWER_R_OUT < r <= P.TOWER_R_OUT + 1.0:
                ang = math.degrees(math.atan2(v, u)) % 360
                if min(ang % 30, 30 - ang % 30) < 7:               # a rib every thirty degrees
                    for y in range(ground + 1, h - 3):
                        put(w, x, y, z, SB if y % 5 else SBCHISEL)
            elif P.TOWER_R_IN - 1.0 <= r < P.TOWER_R_IN:
                for y in range(P.PIT + 1, ground + 1):
                    put(w, x, y, z, SB if (ground - y) % 4 else SBCHISEL)
    # the south door, the culvert's arch and a break each side, cut through the ring
    for x in range(-48, -44):
        for z in range(-30, -26):
            for y in range(63, 71):
                put(w, x, y, z, AIR)
    for x in range(-48, -44):
        for z in range(-47, -42):
            for y in range(P.PIT + 1, P.PIT + 7):
                put(w, x, y, z, AIR)
    for zc in (-37, -36):
        for xa in (int(tx - 9), int(tx + 8)):
            for x in range(xa - 1, xa + 3):
                for y in range(63, 68):
                    if w.id(x, y, zc) != B.AIR:
                        put(w, x, y, zc, AIR)


def pit(w, L):
    x0, x1, z0, z1 = P.PIT_BOX
    S = P.PIT
    # face the walls the relief leaves: the rim cells round the pit, stone brick from the floor up
    for x in range(x0 - 1, x1 + 2):
        for z in range(z0 - 1, z1 + 1):
            inside = x0 <= x <= x1 and z0 <= z <= z1
            if inside:
                continue
            ground = w.top(x, z)
            for y in range(S + 1, ground + 1):
                put(w, x, y, z, SB if (ground - y) % 4 else SBCHISEL)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            put(w, x, S, z, kit.pick([GREY, BLACK, GREY, COBBLE], kit.cell_key(x, z, 2)))
    for x in range(44, 48):
        for z in range(-47, -43):
            for y in range(S + 1, S + 7):
                put(w, x, y, z, AIR)


def crown_roads(w):
    made = {}
    # the west ramp: north along the rim, a landing, east and up onto the deck
    leg1 = kit.ramp_cells((-61, -58), (-49, -26), "-z", P.FIELD, flat=0)
    top1 = leg1[-1]
    landing_y = top1[2]
    landing = [(x, z, landing_y, False) for x in range(-61, -57) for z in range(-53, -49)]
    leg2 = kit.ramp_cells((-57, -46), (-53, -50), "+x", landing_y, flat=0, level=P.CROWN)
    # leg 2 begins one half block above the landing, the way a ramp begins after a flat
    deck = [(x, z, P.CROWN, False) for x in range(-48, -44) for z in range(-57, -53)]
    cells = leg1 + landing + leg2 + deck
    made["west"] = cells
    road(w, cells, clear=6)
    # the east ramp is the west's mirror across x = -0.5
    mirror = [(-1 - x, z, y, s) for x, z, y, s in cells]
    made["east"] = mirror
    road(w, mirror, clear=6)
    # tower and pit entries, the same ramp mirrored
    ent = kit.ramp_cells((-48, -45), (-34, -24), "-z", P.FIELD, flat=0, fall=True, level=P.PIT)
    road(w, ent, clear=6)
    made["tower_entry"] = ent
    ent_e = [(-1 - x, z, y, s) for x, z, y, s in ent]
    road(w, ent_e, clear=6)
    made["pit_entry"] = ent_e
    return made


def deck(w, L):
    """The Crown: a paved roof, bands every twelve blocks, a parapet along the front with the ramps' gaps, vents lit
    from below, pillboxes, a mast."""
    x0, x1, z0, z1 = P.DECK_BOX
    Y = P.CROWN
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            band = (z - z0) % 12 == 0
            seam = abs(x + 0.5) < 1.1
            if band:
                blk = RSMOOTH
            elif seam:
                blk = PAND
            else:
                blk = paving(x, z)
            put(w, x, Y, z, blk)
    # a parapet along the front edge, two high, with crenels, gaps where the ramps arrive
    gaps = [(-52, -43), (42, 51)]
    for x in range(x0, x1 + 1):
        if any(a <= x <= b for a, b in gaps):
            continue
        put(w, x, Y + 1, z1, SB)
        put(w, x, Y + 1, z1 - 0, SB)
        if x % 3 != 2:
            put(w, x, Y + 2, z1, SB)
    # the sides and back: a one-block kerb in stone brick
    for z in range(z0, z1 + 1):
        for x in (x0, x1):
            put(w, x, Y + 1, z, SB)
    for x in range(x0, x1 + 1):
        put(w, x, Y + 1, z0, SB)
    # vents: lava under bars, framed in orange
    for cx, cz in ((-22, -86), (21, -86), (-22, -66), (21, -66)):
        for x in range(cx - 1, cx + 3):
            for z in range(cz - 2, cz + 3):
                put(w, x, Y, z, BARS)
                put(w, x, Y - 1, z, LAVA)
                put(w, x, Y - 2, z, LAVA)
                put(w, x, Y - 3, z, kit.OBSIDIAN)
        for x in range(cx - 2, cx + 4):
            for z in (cz - 3, cz + 3):
                put(w, x, Y, z, RSMOOTH)
        for z in range(cz - 2, cz + 3):
            put(w, cx - 2, Y, z, RSMOOTH)
            put(w, cx + 3, Y, z, RSMOOTH)


def crater(w, L):
    """The central crater's lake: lava in a basin of obsidian, a kerb two high round it, over the shelf."""
    X, Z = w.grid()
    r = L.r
    for i, k in zip(*np.nonzero(L.land & (r < 8.0))):
        x, z = int(X[i, k]), int(Z[i, k])
        if r[i, k] < 6.2:
            for y in range(56, 60):
                w.set(x, y, z, B.LAVA, 0)
            w.set(x, 55, z, B.OBSIDIAN, 0)
        elif r[i, k] < 7.4:
            w.set(x, 59, z, B.OBSIDIAN, 0)
            w.set(x, 60, z, B.OBSIDIAN, 0)
