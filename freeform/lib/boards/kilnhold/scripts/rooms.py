"""The bunker's inside: every room and passage carved from the rock, lined in its own style, and what stands in each.

    build(w)      carve, line and furnish red's bunker; returns what it made, for the checks
"""
import numpy as np

import kit
import plan as P
from kit import (AIR, ANDESITE, BARS, BLACK, BROWN, COBBLE, COAL, GLOW, GREY, IRON, LAVA, LOG_DARK, LOG_DARK_X,
                 LOG_DARK_Z, OAK_DARK, ORANGE, PAND, RCHISEL, RSMOOTH, RSANDSTONE, SB, SBCHISEL, SBCRACK, SEA, STONE,
                 TEAM_CARPET, TEAM_WOOL, WATER, put)
from pgmvox import B


def floor_set(x, z, size=3):
    """Four close tones laid a cell each: the built floor of the gate level."""
    return kit.pick([SB, PAND, ANDESITE, STONE], kit.cell_key(x, z, size))


# ---------------------------------------------------------------------------------------------------------------
# styles: a function of (x, y, z, face) to the block lining that cell; the tag says what the cell is in the room
# ---------------------------------------------------------------------------------------------------------------
def tag_at(I, x, y, z):
    return I.tag[x - I.w.x0, y, z - I.w.z0]


def style_muster(I):
    S = P.GATE

    def s(x, y, z, face):
        u = x + 0.5
        if face == "floor":
            if abs(u) < 1.01:
                return TEAM_WOOL                                  # the aisle, spine door to the far wall
            if abs(abs(u) - 4.5) < 0.6 or z in (-93, -81):
                return RSMOOTH if (z + x) % 2 == 0 else PAND
            return kit.pick([PAND, STONE, PAND, ANDESITE], kit.cell_key(x, z, 2))
        if face == "ceil":
            if z % 4 == 0:
                return OAK_DARK
            return GLOW if (x % 4 == 0 and z % 4 == 2) else SB
        dy = y - (S + 1)
        tag = tag_at(I, x, y, z)
        if tag == 1:                                              # a post: dark oak, with a chiselled foot
            return SBCHISEL if dy == 0 else LOG_DARK
        if tag == 2:                                              # an alcove's walls
            return BLACK if dy < 4 else SB
        if dy == 0:
            return PAND
        if dy in (3, 4):
            return TEAM_WOOL                                      # the stripe round the hall
        if dy == 7:
            return RSMOOTH
        return SB
    return s


def style_spine(I):
    S = P.GATE

    def s(x, y, z, face):
        if face == "floor":
            return PAND if (x + z) % 2 else SB
        if face == "ceil":
            return GLOW if (z % 3 == 0 and x in (-1, 0)) else SB
        dy = y - (S + 1)
        if dy == 2:
            return RSMOOTH
        return SBCHISEL if dy == 0 else SB
    return s


def style_gate_hall(I):
    S = P.GATE

    def s(x, y, z, face):
        u = x + 0.5
        tag = tag_at(I, x, y, z)
        if face == "floor":
            if abs(u) < 1.01 and z <= -56:
                return TEAM_WOOL                                  # the aisle from the gate to the spine
            if abs(abs(u) - 11.0) < 0.6 or z in (-55, -74):
                return RSMOOTH
            return floor_set(x, z)
        if face == "ceil":
            if z % 5 == 0:
                return OAK_DARK                                   # cross beams
            if x % 5 == 2 and z % 5 == 2:
                return SEA
            return SB
        dy = y - (S + 1)
        if tag == 1:                                              # a pilaster: chiselled, capital and foot
            return SBCHISEL if dy in (0, 1, 8, 9) else SB
        if tag == 2:                                              # a recessed panel, lit by a slit
            return GLOW if dy == 7 else BLACK
        if dy <= 1:
            return PAND
        if dy == 8:
            return RSMOOTH
        if dy == 9:
            return SBCHISEL
        return SB
    return s


def style_gate_passage(I):
    S = P.GATE

    def s(x, y, z, face):
        if face == "floor":
            return PAND if abs(x + 0.5) > 1 else TEAM_WOOL
        if face == "ceil":
            return OAK_DARK if z % 3 == 0 else SB
        dy = y - (S + 1)
        if dy == 0:
            return PAND
        if dy == 5:
            return RSMOOTH
        return SBCHISEL if z in (-53, -48) else SB
    return s


def style_workshop(I):
    S = P.GATE

    def s(x, y, z, face):
        if face == "floor":
            return kit.pick([STONE, COBBLE, ANDESITE, STONE], kit.cell_key(x, z, 2))
        if face == "ceil":
            return OAK_DARK if x % 4 else LOG_DARK_Z
        dy = y - (S + 1)
        if tag_at(I, x, y, z) == 1:
            return LOG_DARK
        if dy == 0:
            return COBBLE
        if dy == 4:
            return ORANGE
        return kit.pick([ANDESITE, STONE, ANDESITE, COBBLE], kit.cell_key(x, y, 2) + z)
    return s


def style_command(I):
    S = P.GATE

    def s(x, y, z, face):
        if face == "floor":
            return kit.pick([PAND, SB], kit.cell_key(x, z, 2))
        if face == "ceil":
            return OAK_DARK if z % 3 else SB
        dy = y - (S + 1)
        if tag_at(I, x, y, z) == 1:
            return LOG_DARK
        if dy in (1, 2, 3):
            return (B.BOOKSHELF, 0)
        if dy == 0:
            return OAK_DARK
        if dy == 4:
            return RSMOOTH
        return SB
    return s


def style_turbine(I):
    S = P.DEEP
    cx, cz = P.TURBINE_AT

    def s(x, y, z, face):
        u, v = x + 0.5 - (cx + 0.5), z + 0.5 - (cz + 0.5)
        if face == "floor":
            r = np.hypot(u, v)
            if 5.0 <= r < 7.5:
                return None                                        # the moat is cut by the furnishing
            if abs(r - 8.5) < 0.6:
                return ORANGE
            return kit.pick([BLACK, GREY, BLACK, BLACK], kit.cell_key(x, z, 3))
        if face == "ceil":
            return GLOW if (x % 4 == 0 and z % 4 == 0) else (BLACK if (x + z) % 3 else GREY)
        dy = y - (S + 1)
        tag = tag_at(I, x, y, z)
        if tag == 1:
            return COAL if dy not in (0, 9, 4) else ORANGE
        if dy == 0 or dy == 9:
            return ORANGE
        if dy == 4:
            return SBCRACK
        return kit.pick([BLACK, GREY, BLACK, SB], kit.cell_key(x, y, 2) + z)
    return s


def style_pump(I):
    S = P.DEEP
    cx, cz = P.PUMP_AT

    def s(x, y, z, face):
        u, v = x + 0.5 - (cx + 0.5), z + 0.5 - (cz + 0.5)
        if face == "floor":
            if np.hypot(u, v) < 7.5:
                return None
            return kit.pick([RSANDSTONE, BROWN, RSMOOTH, RSANDSTONE], kit.cell_key(x, z, 3))
        if face == "ceil":
            return SEA if (x % 4 == 0 and z % 4 == 1) else RSMOOTH
        dy = y - (S + 1)
        tag = tag_at(I, x, y, z)
        if tag == 1:
            return RCHISEL if dy in (0, 9) else RSMOOTH
        if dy == 0:
            return BROWN
        if dy == 5:
            return ORANGE
        return RSANDSTONE if dy % 4 else RSMOOTH
    return s


def style_cross(I):
    S = P.DEEP

    def s(x, y, z, face):
        if face == "floor":
            return kit.pick([BLACK, GREY, BLACK], kit.cell_key(x, z, 2)) if abs(z + 68.5) > 0.6 else ORANGE
        if face == "ceil":
            return GLOW if (x % 6 == 0 and z in (-69, -68)) else SB
        dy = y - (S + 1)
        if tag_at(I, x, y, z) == 1:
            return LOG_DARK if dy not in (0, 4) else SBCHISEL
        if dy == 0:
            return ORANGE
        if dy in (2, 3):
            return IRON if (x % 2) else SB
        return SB
    return s


def style_descent(I):
    S = P.GATE

    def s(x, y, z, face):
        if face in ("floor", "ramp"):
            return TEAM_WOOL if (abs(z + 60.5) < 0.6 and x % 6 in (0, 1)) else (SB if face == "ramp" and x % 2 else PAND)
        if face == "ceil":
            return OAK_DARK if x % 6 == 0 else SB
        return SBCHISEL if x % 6 == 0 else (ORANGE if (y - S) % 9 == 0 else SB)
    return s


def style_culvert(I):
    def s(x, y, z, face):
        if face in ("floor", "ramp"):
            return GREY if (x + z) % 2 else BLACK
        if face == "ceil":
            return LOG_DARK_X if z % 6 == 0 else BLACK
        return COBBLE if (y + x) % 5 else ANDESITE
    return s


def style_crown_ramp(I):
    def s(x, y, z, face):
        if face in ("floor", "ramp"):
            return PAND if x % 2 else SB
        if face == "ceil":
            return OAK_DARK if x % 5 == 0 else SB
        return SBCHISEL if x % 5 == 0 else SB
    return s


STYLES = (("muster", style_muster), ("spine", style_spine), ("gate_hall", style_gate_hall),
          ("gate_passage", style_gate_passage), ("workshop", style_workshop), ("command", style_command),
          ("turbine", style_turbine), ("pump", style_pump), ("cross", style_cross), ("descent", style_descent),
          ("culvert", style_culvert), ("crown_ramp", style_crown_ramp))


# ---------------------------------------------------------------------------------------------------------------
def build(w):
    I = kit.Interior(w)
    made = {}
    for name, style in STYLES:
        I.styles[I.index(name)] = style(I)
    for name, (x0, x1, z0, z1, floor, h) in P.ROOMS.items():
        if name != "shrine":
            I.box(name, x0, x1, z0, z1, floor, h)
    I.box("gate_passage", -5, 4, -53, -46, P.GATE, 8)
    x0, x1, z0, z1, floor, h = P.ROOMS["shrine"]
    I.box("turbine", x0, x1, z0, z1, floor, h)
    for nm in ("workshop_door", "command_door"):
        pa = P.PASSAGES[nm]
        I.box("spine", *pa["x"], *pa["z"], pa["floor"], pa["h"])
    pa = P.PASSAGES["cross"]
    I.box("cross", *pa["x"], *pa["z"], pa["floor"], pa["h"])
    for nm in ("culvert_w", "culvert_e"):
        pa = P.PASSAGES[nm]
        for x0, x1, z0, z1 in pa["parts"]:
            I.box("culvert", x0, x1, z0, z1, pa["floor"], pa["h"])
    # the ramps: descents fall from the gate floor to the deep floor over sixteen cells and run level to the halls;
    # the crown ramps rise from the gallery's floor to the Crown
    for nm, run, fall, floor, level, style in (
            ("descent_w", "-x", True, P.GATE, P.DEEP, "descent"), ("descent_e", "+x", True, P.GATE, P.DEEP, "descent"),
            ("crown_ramp_w", "-x", False, P.MEZ, P.CROWN, "crown_ramp"),
            ("crown_ramp_e", "+x", False, P.MEZ, P.CROWN, "crown_ramp")):
        pa = P.PASSAGES[nm]
        cells = kit.ramp_cells(pa["x"], pa["z"], run, floor, flat=0, fall=fall, level=level)
        I.ramp(style, cells, pa["h"])
        made[nm] = cells
    dress_carves(I)
    made["lined"] = I.line()
    furnish(w, I, made)
    return I, made


def dress_carves(I):
    """Pilasters, posts, panels and alcoves: carve-outs and carve-ins, before the lining is laid."""
    S, D = P.GATE, P.DEEP
    # muster hall: posts every four along both walls, alcoves between them, three deep and four high
    x0, x1, z0, z1, _, h = P.ROOMS["muster"]
    for z in range(z0 + 1, z1, 4):
        for xx in (x0, x1):
            I.keep(xx, xx, S + 1, S + h, z, z, tag=1)
    for zc in (-91, -83):
        for xa, xb in ((x0 - 3, x0 - 1), (x1 + 1, x1 + 3)):
            I.carve("muster", xa, xb, S + 1, S + 4, zc - 1, zc + 1, tag=2)
    # gate hall: pilasters on the north and south walls, panels sunk between them
    x0, x1, z0, z1, _, h = P.ROOMS["gate_hall"]
    for xc in (-13, -9, -5, 4, 8, 12):
        I.keep(xc, xc + 1, S + 1, S + h, z0, z0, tag=1)
    for xc in (-13, -9, 8, 12):
        I.keep(xc, xc + 1, S + 1, S + h, z1, z1, tag=1)
    for xc in (-11, -7, 6, 10):
        I.carve("gate_hall", xc, xc, S + 4, S + 8, z0 - 1, z0 - 1, tag=2)
        I.carve("gate_hall", xc, xc, S + 4, S + 8, z1 + 1, z1 + 1, tag=2)
    for zc in (-72, -68):
        I.carve("gate_hall", x0 - 1, x0 - 1, S + 8, S + 9, zc, zc + 1, tag=2)
        I.carve("gate_hall", x1 + 1, x1 + 1, S + 8, S + 9, zc, zc + 1, tag=2)
    # workshop and command post: posts along the long walls
    for nm in ("workshop", "command"):
        x0, x1, z0, z1, _, h = P.ROOMS[nm]
        for z in range(z0 + 2, z1, 4):
            I.keep(x0, x0, S + 1, S + h, z, z, tag=1)
            I.keep(x1, x1, S + 1, S + h, z, z, tag=1)
    # pump hall and turbine hall: piers on the walls
    for nm, wall_x in (("pump", "w"), ("turbine", "e")):
        x0, x1, z0, z1, _, h = P.ROOMS[nm]
        for z in range(z0 + 1, z1, 4):
            xx = x0 if wall_x == "w" else x1
            if nm == "turbine" and -71 <= z <= -63:
                continue                                           # the shrine's mouth
            I.keep(xx, xx, D + 1, D + h, z, z + 1, tag=1)
        for x in range(x0 + 2, x1 - 1, 4):
            I.keep(x, x + 1, D + 1, D + h, z0, z0, tag=1)
    # cross gallery: ribs every six
    xa, xb = P.PASSAGES["cross"]["x"]
    za, zb = P.PASSAGES["cross"]["z"]
    for x in range(xa + 2, xb, 6):
        I.keep(x, x, D + 1, D + 5, za, za, tag=1)
        I.keep(x, x, D + 1, D + 5, zb, zb, tag=1)


def banner(w, x, y, z, facing):
    """A wall banner in the team's colour with a black border."""
    w.banner(x, y, z, 1, [("bo", 0)], wall_facing=facing)


def furnish(w, I, made):
    for xc in (-13, -9, -5, 4, 8, 12):
        banner(w, xc, P.GATE + 6, -73, 3)                         # on the gate hall's north pilasters
    for x in (-8, -4, 4, 7):
        banner(w, x, P.GATE + 5, -94, 3)                          # on the muster hall's far wall
    gate_hall(w, made)
    muster(w, made)
    turbine(w, made)
    pump(w, made)
    pump_props(w)
    workshop(w, made)
    command(w, made)


def gate_hall(w, made):
    S = P.GATE
    # galleries: a slab ramp up each side wall from the spine end, level to the gate end
    for side, (xa, xb) in (("w", (-15, -12)), ("e", (11, 14))):
        cells = kit.ramp_cells((xa, xb), (-73, -55), "+z", S, flat=0, fall=False, level=P.MEZ)
        inner = -12 if side == "w" else 11
        for x, z, y, slab in cells:
            if z <= -64:
                for yy in range(S + 1, y):                         # a solid wedge under the rising run
                    put(w, x, yy, z, SB)
            if slab:
                put(w, x, y, z, (B.SLAB, 5))
            else:
                put(w, x, y, z, SB if x % 2 else PAND)
            if x == inner:
                put(w, x, y + 1, z, BARS)
        for zp in (-63, -55):                                       # piers under the deck's inner edge
            for yy in range(S + 1, P.MEZ):
                put(w, inner, yy, zp, LOG_DARK)
        made[f"gallery_{side}"] = cells
    # the loft across the nave over the gate's inner end: a deck with a rail each side
    for x in range(-11, 11):
        for z in range(-58, -54):
            put(w, x, P.MEZ, z, SB if (x + z) % 2 else PAND)
        put(w, x, P.MEZ + 1, -58, BARS)
        put(w, x, P.MEZ + 1, -55, BARS)
    for x in (-5, 4):
        for yy in range(S + 1, P.MEZ):
            put(w, x, yy, -57, LOG_DARK)
    # the capture dais in the middle of the nave: two steps, the team's wool inlaid
    for x in range(-5, 5):
        for z in range(-67, -57):
            put(w, x, S, z, PAND)
    for x in range(-4, 4):
        for z in range(-66, -58):
            put(w, x, S + 1, z, SB)
    for x in range(-3, 3):
        for z in range(-65, -59):
            put(w, x, S + 1, z, TEAM_WOOL if (abs(x + 0.5) < 1.1 or abs(z + 61.5) < 1.1) else PAND)


def muster(w, made):
    S = P.GATE
    x0, x1, z0, z1, _, h = P.ROOMS["muster"]
    for z in (-92, -88, -84):
        put(w, -1, S + 7, z, GLOW)
        put(w, 0, S + 7, z, GLOW)
    for zc in (-91, -83):
        for xx, f in ((x0 - 3, 5), (x1 + 3, 4)):
            w.chest(xx, S + 1, zc, [(0, "minecraft:iron_sword", 1, 0), (1, "minecraft:bow", 1, 0),
                                    (2, "minecraft:arrow", 32, 0)], facing=f)


def turbine(w, made):
    D = P.DEEP
    cx, cz = P.TURBINE_AT
    # the moat: a ring of grated lava under bars, four walkways across it
    for x in range(cx - 9, cx + 10):
        for z in range(cz - 9, cz + 10):
            u, v = x - cx, z - cz
            r = float(np.hypot(u, v))
            if 5.0 <= r < 7.5:
                if abs(u) < 2.0 or abs(v) < 2.0:
                    put(w, x, D, z, BLACK if (x + z) % 2 else GREY)
                else:
                    put(w, x, D, z, BARS)
                    put(w, x, D - 1, z, LAVA)
                    put(w, x, D - 2, z, LAVA)
                    put(w, x, D - 3, z, kit.OBSIDIAN)
            elif r < 5.0:
                put(w, x, D, z, ORANGE if r < 1.6 else (BLACK if r < 4.0 else GREY))
    # the drum: iron and coal rings round a glowing core, a hazard band
    for x in range(cx - 4, cx + 5):
        for z in range(cz - 4, cz + 5):
            r = float(np.hypot(x - cx, z - cz))
            if r <= 3.2:
                for y in range(D + 1, D + 8):
                    ring = y - D
                    if r < 1.6:
                        blk = GLOW if ring in (3, 4) else IRON
                    elif ring in (1, 7):
                        blk = COAL
                    elif ring in (3, 4):
                        blk = ORANGE
                    else:
                        blk = IRON if ring % 2 else COAL
                    put(w, x, y, z, blk)
    for y in range(D + 8, D + 11):                                  # a pipe from the drum's crown to the ceiling
        for x in (cx, cx + 1):
            for z in (cz, cz + 1):
                put(w, x, y, z, IRON)
    # the flag dais, in the team's colour
    fx, fy, fz = P.FLAG_POST
    for x in range(fx - 2, fx + 2):
        for z in range(fz - 2, fz + 3):
            put(w, x, D + 1, z, TEAM_WOOL if (x + z) % 2 == 0 else PAND)
    made["flag_dais"] = (fx, D + 1, fz)


def pump(w, made):
    D = P.DEEP
    cx, cz = P.PUMP_AT
    # the sump: a round pool of water under bars, a rim of orange clay, and the monument over it
    for x in range(cx - 9, cx + 10):
        for z in range(cz - 9, cz + 10):
            r = float(np.hypot(x - cx, z - cz))
            if r < 7.5:
                if r < 6.0:
                    put(w, x, D, z, BARS)
                    put(w, x, D - 1, z, WATER)
                    put(w, x, D - 2, z, WATER)
                    put(w, x, D - 3, z, kit.OBSIDIAN)
                else:
                    put(w, x, D, z, ORANGE)
            elif r < 8.5:
                put(w, x, D, z, RSMOOTH)


def pump_props(w):
    """Valve stands at the pump hall's corners and a pipe run along its north wall."""
    D = P.DEEP
    x0, x1, z0, z1, _, h = P.ROOMS["pump"]
    for x in range(x0 + 1, x1):
        put(w, x, D + 7, z0 + 1, IRON)
        if x % 4 == 0:
            put(w, x, D + 6, z0 + 1, BARS)
            put(w, x, D + 5, z0 + 1, BARS)
    for cx, cz in ((x0 + 2, z0 + 3), (x1 - 3, z0 + 3), (x0 + 2, z1 - 3), (x1 - 3, z1 - 3)):
        for x in range(cx, cx + 2):
            for z in range(cz, cz + 2):
                put(w, x, D + 1, z, RSMOOTH)
                put(w, x, D + 2, z, IRON if (x + z) % 2 else COAL)
        put(w, cx, D + 3, cz, BARS)
        put(w, cx + 1, D + 3, cz + 1, BARS)


def workshop(w, made):
    S = P.GATE
    x0, x1, z0, z1, _, h = P.ROOMS["workshop"]
    for x in range(x0 + 1, x1, 2):
        put(w, x, S + 1, z0, (B.FURNACE, 3))
    for x in (x0 + 3, x0 + 8):
        put(w, x, S + 1, z0 + 3, (B.ANVIL, 0))
    put(w, x0 + 5, S + 1, z0 + 5, (B.CRAFTING, 0))
    for x in range(x0 + 1, x0 + 4):
        for z in range(z1 - 2, z1):
            put(w, x, S + 1, z, IRON)
    for x in range(x0 + 9, x1 - 1):
        put(w, x, S + 1, z1 - 1, COAL)
    w.chest(x1 - 1, S + 1, z0 + 6, [(0, "minecraft:iron_pickaxe", 1, 0), (1, "minecraft:cooked_beef", 16, 0)],
            facing=4)


def command(w, made):
    S = P.GATE
    x0, x1, z0, z1, _, h = P.ROOMS["command"]
    for x in range(x0 + 5, x0 + 10):
        for z in range(z0 + 4, z0 + 9):
            put(w, x, S + 1, z, (B.WOOD_SLAB, 5))
    put(w, x0 + 7, S + 2, z0 + 6, TEAM_CARPET)
    w.chest(x0 + 1, S + 1, z0 + 6, [(0, "minecraft:golden_apple", 4, 0), (1, "minecraft:arrow", 32, 0)], facing=5)
