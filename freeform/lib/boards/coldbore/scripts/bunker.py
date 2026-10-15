"""Red's station under the cliff: every room, corridor and flight carved and lined, the facade standing out of the
cliff, the stair core, the drop, the vent ladder, the reactor's well and hatch, the vault and its pool, the
blast door, the gallery over the fissure and the culvert up to the snow.

The built family is the station's: stone and stone brick inside, a dark nether-brick front outside, iron for what
is machinery, yellow-and-black hazard bands at its thresholds; the vault alone is white quartz, a clean room.
"""
import numpy as np
from scipy import ndimage

import land  # noqa: F401
import plan as P
from pgmvox import B
from pgmvox.core import orient
from pgmvox.volume import under

FLOOR = [(B.STONEBRICK, 0), (B.STONE, 6), (B.STONE, 5), (B.STONE, 0)]       # a quarter each, in cells of three
HAZARD = [(B.STAINED_CLAY, 4), (B.STAINED_CLAY, 15)]
TEAM = (B.STAINED_CLAY, 14)                                                 # red; blue's image recolours it
BOX = dict(x0=-36, x1=40, y0=24, y1=112, z0=0, z1=99)                      # red's bunker lies inside this


def floor_block(x, z):
    h = (x // 3 * 73856093) ^ (z // 3 * 19349663)
    return FLOOR[h % 4]


def hazard(x, y, z):
    return HAZARD[((x + z + y) // 2) % 2]


def grid():
    b = BOX
    xs, ys, zs = np.arange(b["x0"], b["x1"] + 1), np.arange(b["y0"], b["y1"] + 1), np.arange(b["z0"], b["z1"] + 1)
    return xs, ys, zs


def mask_of(boxes):
    """A boolean volume over BOX holding every (x0, x1, y0, y1, z0, z1) inclusive box."""
    xs, ys, zs = grid()
    m = np.zeros((len(xs), len(ys), len(zs)), bool)
    for x0, x1, y0, y1, z0, z1 in boxes:
        m[max(0, x0 - xs[0]):x1 - xs[0] + 1, max(0, y0 - ys[0]):y1 - ys[0] + 1, max(0, z0 - zs[0]):z1 - zs[0] + 1] = True
    return m


def space_boxes():
    """Every carved air box of red's station: rooms and corridors, flights, the gallery, the shafts."""
    out = {}
    for s in P.SPACES:
        out[s.name] = [(s.x0, s.x1, s.feet, s.feet + s.h - 1, s.z0, s.z1)]
    for f in P.FLIGHTS:
        out[f.name] = [(x, x, feet, feet + f.h - 1, z, z) for x, z, feet in f.cells()]
    g = P.GALLERY
    out["gallery"] = [(x, x, g["feet"], g["feet"] + g["h"] - 1, z, z) for x, z in P.gallery_cells()]
    sh = P.SHAFT
    out["stair core"] = [(sh["x0"] + 1, sh["x1"] - 1, P.L2, P.TOP + 4, sh["z0"] + 1, sh["z1"] - 1)]
    out["doors"] = [(x, x, feet, feet + 3, z, z) for x, z, feet in P.DOORS]
    d = P.DROP
    out["drop shaft"] = [(d["x0"], d["x1"], P.L1 + 9, P.TOP + 2, d["z0"], d["z1"])]
    lad = P.LADDER
    out["vent shaft"] = [(lad["x"], lad["x"] + 1, P.L1 + 9, lad["top"], lad["z0"], lad["z1"])]
    out["gate"] = [(P.GATE["x0"], P.GATE["x1"], P.L0, P.L0 + P.GATE["h"] - 1, P.GATE["z"], P.GATE["z"])]
    return out


def place(w, xs, ys, zs, m, block):
    """Write `block` (or a function of x, y, z) at every True of a mask over BOX."""
    for i, j, k in np.argwhere(m):
        x, y, z = int(xs[i]), int(ys[j]), int(zs[k])
        b = block(x, y, z) if callable(block) else block
        if b is not None:
            w.set(x, y, z, *b)


def carve_and_line(w):
    """Carve every space, then line what rock touches the air: a floor, walls and a ceiling by the space they
    face. Returns the air mask over BOX, for what is laid afterwards."""
    xs, ys, zs = grid()
    boxes = space_boxes()
    air = mask_of([b for v in boxes.values() for b in v])
    struct = ndimage.generate_binary_structure(3, 1)
    b = BOX
    solid = w.ids[b["x0"] - w.x0:b["x1"] - w.x0 + 1, b["y0"]:b["y1"] + 1, b["z0"] - w.z0:b["z1"] - w.z0 + 1] != 0
    f = P.FACADE
    front = mask_of([(f["x0"], f["x1"], f["y0"], f["y1"], f["z0"], f["z1"])])
    shell = ndimage.binary_dilation(air, struct) & ~air & (solid | front)    # only what is rock or the facade
    # the facade first: a mass of nether brick standing out of the cliff, the rooms cut into it after
    place(w, xs, ys, zs, front & ~air, facade_block)
    # walls, floors and ceilings by which way the air lies from them
    below_air = np.zeros_like(air); below_air[:, :-1, :] = air[:, 1:, :]       # air over it: a floor
    above_air = np.zeros_like(air); above_air[:, 1:, :] = air[:, :-1, :]       # air under it: a ceiling
    vault = next(s for s in P.SPACES if s.name == "vault")
    vmask = mask_of([(vault.x0 - 1, vault.x1 + 1, vault.feet - 1, vault.feet + vault.h, vault.z0 - 1, vault.z1 + 1)])

    def line(x, y, z):
        i, j, k = x - xs[0], y - ys[0], z - zs[0]
        if front[i, j, k] and not air[i, j, k] and y > f["y0"]:
            return None                                           # the facade keeps its own faces
        if vmask[i, j, k]:
            return vault_block(x, y, z, below_air[i, j, k], above_air[i, j, k])
        if below_air[i, j, k]:
            return floor_block(x, z)
        if above_air[i, j, k]:
            return (B.SEA_LANTERN, 0) if x % 6 == 0 and z % 6 == 0 else (B.DSLAB, 0)
        return wall_block(x, y, z)
    place(w, xs, ys, zs, shell, line)
    place(w, xs, ys, zs, air, (B.AIR, 0))
    return air


def wall_block(x, y, z):
    if (x + z) % 6 == 0:
        return (B.STONEBRICK, 0)                                  # pilasters
    if y in (P.L0, P.L1, P.L2):
        return (B.STONE, 6)                                       # the skirting at the feet
    if y in (P.L0 + 4, P.L1 + 4, P.L2 + 4) and (x + z) % 6 in (2, 3, 4):
        return hazard(x, y, z)
    return (B.STONE, 0)


def vault_block(x, y, z, is_floor, is_ceiling):
    if is_floor:
        return (B.QUARTZ, 0) if (x + z) % 4 else (B.STONE, 4)
    if is_ceiling:
        return (B.SEA_LANTERN, 0) if x % 5 == 0 and z % 5 == 0 else (B.QUARTZ, 0)
    return (B.QUARTZ, 2) if (x + z) % 5 == 0 else (B.QUARTZ, 0)


def facade_block(x, y, z):
    f = P.FACADE
    if y == f["y1"]:
        return (B.NETHER_FENCE, 0) if (x + z) % 2 else (B.SLAB, 6)    # the parapet
    if y == f["y1"] - 1 or y == P.L0 + 9:
        return (B.STONEBRICK, 0)                                  # courses round the mass
    if y == f["y1"] - 3:
        return TEAM                                               # the team's band
    if (x - f["x0"]) % 4 == 0 and z == f["z0"]:
        return (B.STONEBRICK, 0)                                  # ribs down the front
    return (B.NETHER_BRICK, 0)


def gate(w):
    """The gate's frame: hazard bands round the opening, iron jambs, and slits under the parapet."""
    g, f = P.GATE, P.FACADE
    z = g["z"]
    for x in range(g["x0"] - 2, g["x1"] + 3):
        for y in range(g["feet"] - 1, g["feet"] + g["h"] + 2):
            inside = g["x0"] <= x <= g["x1"] and g["feet"] <= y < g["feet"] + g["h"]
            if not inside:
                w.set(x, y, z, *hazard(x, y, z))
    for x in (g["x0"] - 1, g["x1"] + 1):
        for y in range(g["feet"], g["feet"] + g["h"]):
            w.set(x, y, z + 1, B.IRON_BLOCK)
    for x in range(f["x0"] + 2, f["x1"] - 1, 4):
        if not g["x0"] - 2 <= x <= g["x1"] + 2:
            for y in (P.L0 + 11, P.L0 + 12):
                w.set(x, y, z, B.IRON_BARS)


def wings(w):
    """Blast walls splaying out from the facade's front corners onto the forecourt, falling from six courses at
    the facade to three at their ends, and a concrete visor over the gate."""
    f, g = P.FACADE, P.GATE
    for side in (-1, 1):
        x0 = f["x0"] if side < 0 else f["x1"]
        for t in range(8):
            x, z = x0 + side * t, f["z0"] - 1 - t
            height = 6 - t * 3 // 8
            for dx in (0, side):
                for y in range(land.GROUND + 1, land.GROUND + 1 + height):
                    w.set(x + dx, y, z, *((B.STAINED_CLAY, 4 if (y + t) % 2 else 15) if y == land.GROUND + 1
                                          else (B.NETHER_BRICK, 0)))
                w.set(x + dx, land.GROUND + 1 + height, z, B.STONEBRICK)
    for x in range(g["x0"] - 3, g["x1"] + 4):
        for z in range(g["z"] - 3, g["z"]):
            w.set(x, g["feet"] + g["h"] + 1, z, B.SLAB, 13 if z > g["z"] - 3 else 5)


def flights(w):
    """Stairs on every flight: each step's block faces the way the flight climbs."""
    for f in P.FLIGHTS:
        cells = f.cells()
        up = "n" if f.feet_at(f.z1) < f.feet_at(f.z0) and f.z1 > f.z0 or \
            f.feet_at(f.z1) > f.feet_at(f.z0) and f.z1 < f.z0 else "s"
        for x, z, feet in cells:
            w.set(x, feet - 1, z, B.STONEBRICK_STAIRS, orient.stair(up))
            w.set(x, feet - 2, z, B.STONEBRICK)


def stair_core(w):
    """The shaft: a solid core of polished andesite, the stair climbing the ring round it a block a step, lit
    from the core."""
    sh = P.SHAFT
    for x in range(sh["x0"] + 2, sh["x1"] - 1):
        for z in range(sh["z0"] + 2, sh["z1"] - 1):
            for y in range(P.L2 - 1, P.TOP + 4):
                lit = (y - P.L2) % 6 == 3 and (x in (sh["x0"] + 2, sh["x1"] - 2) or z in (sh["z0"] + 2, sh["z1"] - 2))
                w.set(x, y, z, B.SEA_LANTERN if lit else B.STONE, 0 if lit else 6)
    steps = P.helix()
    for (x, z, feet), nxt in zip(steps, steps[1:] + [None]):
        d = "n"
        if nxt is not None:
            dx, dz = nxt[0] - x, nxt[1] - z
            d = {(1, 0): "e", (-1, 0): "w", (0, 1): "s", (0, -1): "n"}[(dx, dz)]
        w.set(x, feet - 1, z, B.STONEBRICK_STAIRS, orient.stair(d))


def drop(w):
    """The drop's pool at the foot of the shaft, three deep and flush with the drop room's floor."""
    d = P.DROP
    for x in range(d["x0"], d["x1"] + 1):
        for z in range(d["z0"], d["z1"] + 1):
            for y in range(d["water_top"] - d["water_depth"] + 1, d["water_top"] + 1):
                w.set(x, y, z, B.WATER)
            w.set(x, d["water_top"] - d["water_depth"], z, B.SEA_LANTERN)


def ladder(w):
    lad = P.LADDER
    for z in range(lad["z0"], lad["z1"] + 1):
        for y in range(lad["bottom"], lad["top"] + 1):
            w.set(lad["wall_x"], y, z, B.STONEBRICK)
            w.set(lad["x"], y, z, B.LADDER, orient.ladder("w"))


def reactor(w):
    """The reactor's hall: the well under the core, its hatch, the hazard ring round the well's mouth, iron
    columns at its corners, and the cradle the core hangs in from the ceiling."""
    wl, hatch, c = P.WELL, P.HATCH, P.CORE
    for x in range(wl.x0, wl.x1 + 1):
        for z in range(wl.z0, wl.z1 + 1):
            for y in range(wl.y0, wl.y1 + 1):
                w.set(x, y, z, B.AIR)
            w.set(x, hatch.y0, z, B.BEDROCK)
    for x in range(wl.x0 - 1, wl.x1 + 2):
        for z in range(wl.z0 - 1, wl.z1 + 2):
            if not (wl.x0 <= x <= wl.x1 and wl.z0 <= z <= wl.z1):
                w.set(x, P.L1 - 1, z, *hazard(x, 0, z))
    for x, z in ((wl.x0 - 2, wl.z0 - 2), (wl.x1 + 2, wl.z0 - 2), (wl.x0 - 2, wl.z1 + 2), (wl.x1 + 2, wl.z1 + 2)):
        for y in range(P.L1, P.L1 + P.HALL_H):
            w.set(x, y, z, B.IRON_BLOCK if (y - P.L1) % 4 else B.STONEBRICK, 0)
    for x, z in ((c.x0, c.z0), (c.x1, c.z0), (c.x0, c.z1), (c.x1, c.z1)):
        for y in range(c.y1 + 1, P.L1 + P.HALL_H):
            w.set(x, y, z, B.IRON_BARS)
    # coolant lines along the ceiling from the well to the walls
    for z in range(44, 67, 4):
        for x in range(-12, 12):
            if not (c.x0 - 1 <= x <= c.x1 + 1 and c.z0 - 1 <= z <= c.z1 + 1):
                w.set(x, P.L1 + P.HALL_H - 1, z, B.COBBLE_WALL)
    # consoles along the east wall: iron cabinets with lamps over them
    for z in range(46, 64, 3):
        w.set(11, P.L1, z, B.IRON_BLOCK)
        w.set(11, P.L1 + 1, z, B.REDSTONE_LAMP)


def vault(w):
    """The cooling vault: the pool under the hatch lit from its floor, a quartz rim and rails round it, racks
    of spent rods along the walls, and the blast door in its east wall."""
    p = P.POOL
    for x in range(p["x0"] - 1, p["x1"] + 2):
        for z in range(p["z0"] - 1, p["z1"] + 2):
            edge = not (p["x0"] <= x <= p["x1"] and p["z0"] <= z <= p["z1"])
            for y in range(p["y0"] - 1, p["y1"] + 1):
                if edge or y == p["y0"] - 1:
                    w.set(x, y, z, (B.SEA_LANTERN if (not edge and (x + z) % 3 == 0) else B.PRISMARINE), 0)
                else:
                    w.set(x, y, z, B.WATER)
            if edge:
                w.set(x, P.L2 - 1, z, B.QUARTZ, 2 if (x + z) % 2 else 0)
                if (x + z) % 7 and not (x == p["x1"] + 1 and p["z0"] + 3 <= z <= p["z0"] + 6):
                    w.set(x, P.L2, z, B.IRON_BARS)
    vault_space = next(s for s in P.SPACES if s.name == "vault")
    for x in (vault_space.x0, vault_space.x1):
        for z in range(vault_space.z0 + 2, vault_space.z1 - 1, 3):
            for y in range(P.L2, P.L2 + 4):
                w.set(x, y, z, B.QUARTZ, 2)
            w.set(x, P.L2 + 4, z, B.SEA_LANTERN)
    d = P.VAULT_DOOR
    for x in range(d.x0, d.x1 + 1):
        for y in range(d.y0, d.y1 + 1):
            for z in range(d.z0, d.z1 + 1):
                w.set(x, y, z, B.BEDROCK)
    for y in range(d.y0, d.y1 + 2):
        for z in (d.z0 - 1, d.z1 + 1):
            w.set(d.x1 + 1, y, z, *hazard(0, y, z))


def gallery(w):
    """The bore's service gallery on the fissure: a jib over the edge with its cable hanging into the crack,
    broken rails along the lip and pipe racks along the back wall."""
    cells = P.gallery_cells()
    lips = {}
    for x, z in cells:
        lips[x] = min(z, lips.get(x, z))
    for x, z in lips.items():
        if x % 5 and (x * 7) % 3:
            w.set(x, P.L2, z, B.NETHER_FENCE)
    xs_ = sorted(lips)
    for x in (xs_[0] - 1, xs_[-1] + 1):                           # a frame round the mouth in the fissure's wall
        z = lips[xs_[0] if x < 0 else xs_[-1]]
        for zz in range(z - 1, z + 2):
            for y in range(P.L2 - 1, P.L2 + P.HALL_H + 1):
                if w.id(x, y, zz) != B.AIR:
                    w.set(x, y, zz, B.NETHER_BRICK)
    for x in range(xs_[0] - 1, xs_[-1] + 2):
        z = lips.get(x, lips[xs_[0]])
        for zz in range(z - 1, z + 2):
            if w.id(x, P.L2 + P.HALL_H, zz) != B.AIR:
                w.set(x, P.L2 + P.HALL_H, zz, *hazard(x, 0, zz))
    jib_x = -6
    z0 = lips[jib_x]
    for z in range(z0 - 6, z0 + 4):
        w.set(jib_x, P.L2 + P.HALL_H - 2, z, B.IRON_BLOCK)
    for y in range(P.L2 + 2, P.L2 + P.HALL_H - 2):
        w.set(jib_x, y, z0 - 6, B.FENCE)
    for x in range(P.GALLERY["x0"], P.GALLERY["x1"] + 1, 3):
        for y in (P.L2 + 6, P.L2 + 9):
            w.set(x, y, P.GALLERY["z1"], B.IRON_BARS)


def culvert(w):
    """The collapsed culvert from the barracks up to the snow: a cave's tube, its floor rubble and gravel."""
    under.tunnel(w, P.CULVERT, ground=None, cover=0)
    for x, y, z, r in P.CULVERT[:2]:
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                if w.id(x + dx, y, z + dz) == B.AIR and w.id(x + dx, y - 1, z + dz) not in (B.AIR,):
                    w.set(x + dx, y - 1, z + dz, B.GRAVEL)


SUPPLY = [(0, "minecraft:arrow", 32, 0), (4, "minecraft:cooked_beef", 8, 0), (8, "minecraft:golden_apple", 1, 0)]


def furnish(w):
    """What each room is for: racks and supply chests in the armoury, bunks in the barracks, pipework and a
    pump in the turn hall."""
    arm = next(s for s in P.SPACES if s.name == "armoury")
    for z in range(arm.z0 + 1, arm.z1, 2):                      # weapon racks along the west wall
        for y in range(arm.feet, arm.feet + 3):
            w.set(arm.x0, y, z, B.IRON_BARS)
    w.chest(arm.x0 + 1, arm.feet, arm.z0, SUPPLY, facing=3)
    w.chest(arm.x0 + 3, arm.feet, arm.z0, SUPPLY, facing=3)
    bar = next(s for s in P.SPACES if s.name == "barracks")
    for x in range(bar.x0 + 1, bar.x1, 3):                      # bunks along both long walls, head to the wall
        for z, head, foot in ((bar.z0, bar.z0, bar.z0 + 1), (bar.z1, bar.z1, bar.z1 - 1)):
            facing = 2 if head == bar.z0 else 0
            for y in (bar.feet, bar.feet + 3):
                w.set(x, y, head, B.BED, facing | 8)
                w.set(x, y, foot, B.BED, facing)
            for zz in (head, foot):
                w.set(x, bar.feet + 2, zz, B.WOOD_SLAB, 13)
    turn = next(s for s in P.SPACES if s.name == "turn hall")
    for x in range(turn.x0 + 1, turn.x1, 4):                    # pipes down the back wall into a manifold
        for y in range(turn.feet, turn.feet + turn.h - 1):
            w.set(x, y, turn.z1, B.COBBLE_WALL)
    for x in range(turn.x0 + 1, turn.x1):
        w.set(x, turn.feet + 2, turn.z1, B.IRON_BLOCK)
    w.set(turn.x0 + 2, turn.feet, turn.z1 - 1, B.CAULDRON)
    w.set(turn.x1 - 2, turn.feet, turn.z1 - 1, B.CAULDRON)


def build(w):
    air = carve_and_line(w)
    gate(w)
    wings(w)
    flights(w)
    stair_core(w)
    drop(w)
    ladder(w)
    reactor(w)
    vault(w)
    gallery(w)
    culvert(w)
    furnish(w)
    return air
