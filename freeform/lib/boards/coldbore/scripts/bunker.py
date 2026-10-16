"""Red's station inside the mountain: every room, corridor and ramp carved and lined, the gate's facade in the west
buttress and the generator house in the east, the reactor hall with its balcony, gantry and ramp, the pit under
the core, the vault and its blast door, the gallery over the fissure, and the store whose ceiling fell in.

The built family is the station's: stone and stone brick inside, a dark nether-brick front at the gate and at
the generator house alike, iron for what is machinery, yellow-and-black hazard bands at its
thresholds; the vault alone is white quartz, a clean room.
"""
import numpy as np
from scipy import ndimage

import land
import plan as P
from pgmvox import B
from pgmvox.core import orient
from pgmvox.geom import noise

FLOOR = [(B.STONEBRICK, 0), (B.STONE, 6), (B.STONE, 5), (B.STONE, 0)]       # a quarter each, in cells of three
HAZARD = [(B.STAINED_CLAY, 4), (B.STAINED_CLAY, 15)]
TEAM = (B.STAINED_CLAY, 14)                                                 # red; blue's image recolours it
BOX = dict(x0=-66, x1=48, y0=36, y1=104, z0=0, z1=99)                      # red's station lies inside this
RUBBLE = [(B.COBBLE, 0), (B.STONE, 5), (B.STONEBRICK, 2), (B.GRAVEL, 0), (B.STONE, 0), (B.STONEBRICK, 0)]


def floor_block(x, z):
    h = (x // 3 * 73856093) ^ (z // 3 * 19349663)
    return FLOOR[h % 4]


def hazard(x, y, z):
    return HAZARD[((x + z + y) // 2) % 2]


def grid():
    b = BOX
    return np.arange(b["x0"], b["x1"] + 1), np.arange(b["y0"], b["y1"] + 1), np.arange(b["z0"], b["z1"] + 1)


def mask_of(boxes):
    """A boolean volume over BOX holding every (x0, x1, y0, y1, z0, z1) inclusive box."""
    xs, ys, zs = grid()
    m = np.zeros((len(xs), len(ys), len(zs)), bool)
    for x0, x1, y0, y1, z0, z1 in boxes:
        m[max(0, x0 - xs[0]):x1 - xs[0] + 1, max(0, y0 - ys[0]):y1 - ys[0] + 1, max(0, z0 - zs[0]):z1 - zs[0] + 1] = True
    return m


def space_boxes():
    """Every carved air box of red's station: rooms and corridors, the tunnel ramps, the gallery, the gate, the
    garage door and the pit."""
    out = []
    for s in P.SPACES:
        out.append((s.x0, s.x1, s.feet, s.feet + s.h - 1, s.z0, s.z1))
    for r in P.RAMPS:
        if not r.solid:
            out += [(x, x, P.ramp_floor(f) + 1, P.ramp_floor(f) + r.h, z, z) for x, z, f in r.cells()]
    g = P.GALLERY
    out += [(x, x, g["feet"], g["feet"] + g["h"] - 1, z, z) for x, z in P.gallery_cells()]
    out.append((P.GATE["x0"], P.GATE["x1"], P.L0, P.L0 + P.GATE["h"] - 1, P.GATE["z"], P.GATE["z"]))
    ga = P.GARAGE
    out.append((ga["x0"], ga["x1"], ga["feet"], ga["feet"] + ga["h"] - 1, ga["z"], ga["z"]))
    p = P.PIT
    out.append((p.x0, p.x1, p.y0, p.y1, p.z0, p.z1))
    return out


def place(w, xs, ys, zs, m, block):
    """Write `block` (or a function of x, y, z) at every True of a mask over BOX."""
    for i, j, k in np.argwhere(m):
        x, y, z = int(xs[i]), int(ys[j]), int(zs[k])
        b = block(x, y, z) if callable(block) else block
        if b is not None:
            w.set(x, y, z, *b)


def fronts():
    f, a = P.FACADE, P.ANNEX
    return [(f["x0"], f["x1"], f["y0"], f["y1"], f["z0"], f["z1"]), (a["x0"], a["x1"], a["y0"], a["y1"], a["z0"], a["z1"])]


def carve_and_line(w):
    """Carve every space, then line what rock touches the air: a floor, walls and a ceiling by the space they
    face. Returns the air mask over BOX, for what is laid afterwards."""
    xs, ys, zs = grid()
    air = mask_of(space_boxes())
    struct = ndimage.generate_binary_structure(3, 1)
    b = BOX
    solid = w.ids[b["x0"] - w.x0:b["x1"] - w.x0 + 1, b["y0"]:b["y1"] + 1, b["z0"] - w.z0:b["z1"] - w.z0 + 1] != 0
    west, east = fronts()
    wmask, emask = mask_of([west]), mask_of([east])
    front = wmask | emask
    shell = ndimage.binary_dilation(air, struct) & ~air & (solid | front)    # only what is rock or a facade
    place(w, xs, ys, zs, wmask & ~air, facade_block)
    place(w, xs, ys, zs, emask & ~air, annex_block)
    below_air = np.zeros_like(air); below_air[:, :-1, :] = air[:, 1:, :]       # air over it: a floor
    above_air = np.zeros_like(air); above_air[:, 1:, :] = air[:, :-1, :]       # air under it: a ceiling
    vault = next(s for s in P.SPACES if s.name == "vault")
    vmask = mask_of([(vault.x0 - 1, vault.x1 + 1, vault.feet - 1, vault.feet + vault.h, vault.z0 - 1, vault.z1 + 1)])

    def line(x, y, z):
        i, j, k = x - xs[0], y - ys[0], z - zs[0]
        if front[i, j, k] and not below_air[i, j, k] and not above_air[i, j, k]:
            if not solid[i, j, k] or z == (P.FACADE["z0"] if wmask[i, j, k] else P.ANNEX["z0"]):
                return None                                       # a facade keeps its own faces
        if vmask[i, j, k]:
            return vault_block(x, y, z, below_air[i, j, k], above_air[i, j, k])
        if below_air[i, j, k]:
            return floor_block(x, z)
        if above_air[i, j, k]:
            return (B.SEA_LANTERN, 0) if x % 5 == 0 and z % 5 == 0 else (B.DSLAB, 0)
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


def annex_block(x, y, z):
    """The generator house's front, in the gate's dark style: nether brick ribbed in stone brick between its bays, a
    course of stone brick at the gate's height, a window band of bars, the team's band under a parapet of nether
    brick slabs and fence."""
    a, ga = P.ANNEX, P.GARAGE
    if y == a["y1"]:
        return (B.NETHER_FENCE, 0) if (x + z) % 2 else (B.SLAB, 6)
    if y == a["y1"] - 1 or y == P.L0 + 9:
        return (B.STONEBRICK, 0)
    if y == a["y1"] - 3:
        return TEAM
    if z == a["z0"] and y in (P.L0 + 7, P.L0 + 8) and (x - a["x0"]) % 5 and not ga["x0"] - 1 <= x <= ga["x1"] + 1:
        return (B.IRON_BARS, 0)                                   # the window band onto the court
    if (x - a["x0"]) % 5 == 0 and z == a["z0"]:
        return (B.STONEBRICK, 0)                                  # ribs between the bays
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
    """Blast walls splaying out from the facade's front corners onto the court, falling from six courses at the
    facade to three at their ends, and a concrete visor over the gate."""
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


def garage(w):
    """The generator house's door: a hazard frame, the shutter jammed a block down from the lintel, and two
    exhausts climbing the front past the coping."""
    ga, a = P.GARAGE, P.ANNEX
    z = ga["z"]
    for x in range(ga["x0"] - 1, ga["x1"] + 2):
        for y in range(ga["feet"] - 1, ga["feet"] + ga["h"] + 1):
            inside = ga["x0"] <= x <= ga["x1"] and ga["feet"] <= y < ga["feet"] + ga["h"]
            if not inside:
                w.set(x, y, z, *hazard(x, y, z))
    for x in range(ga["x0"], ga["x1"] + 1):
        w.set(x, ga["feet"] + ga["h"] - 1, z, B.IRON_TRAPDOOR, 8 | 1)
    for x in (a["x0"] + 2, a["x1"] - 2):
        for y in range(P.L0, a["y1"] + 6):
            w.set(x, y, a["z0"] - 1, B.NETHER_FENCE)
        w.set(x, a["y1"] + 6, a["z0"] - 1, B.IRON_BARS)


def ramp_step(f):
    """A ramp cell's floor block: a full block where the feet stand on a whole block, a slab where on a half."""
    return (B.STONEBRICK, 0) if f == int(f) else (B.SLAB, 5)


def ramps(w):
    """The hall's ramp stands as a wedge of stone brick against its west and south walls; the tunnel ramps get
    their half steps in their carved floors and a lamp in the ceiling every four."""
    for r in P.RAMPS:
        for x, z, f in r.cells():
            top = P.ramp_floor(f)
            if r.solid:
                for y in range(P.L1 - 1, top):
                    w.set(x, y, z, B.STONEBRICK, 0 if (x + y + z) % 7 else 2)
            w.set(x, top, z, *ramp_step(f))
            if f != int(f):
                w.set(x, top - 1, z, B.STONEBRICK)
            if not r.solid and x % 4 == 0 and z % 4 == 0:
                w.set(x, top + r.h + 1, z, B.SEA_LANTERN)
    hall = next(r for r in P.RAMPS if r.solid)
    leg = hall.legs[0]
    for z in range(leg.z0, leg.z1 + 1, 3):                       # hazard marks along the open edge of the upper leg
        f = max(c[2] for c in hall.cells() if c[0] == leg.x1 and c[1] == z)
        w.set(leg.x1, P.ramp_floor(f), z, *(HAZARD[0] if f == int(f) else (B.SLAB, 5)))


def decks(w):
    """The balcony and the gantry: a floor on a beam, on piers to the hall's floor, a rail on the open edges."""
    for d in P.DECKS:
        for x, z in d.cells():
            w.set(x, d.feet - 1, z, *floor_block(x, z))
            w.set(x, d.feet - 2, z, B.SLAB, 13)
    bal = next(d for d in P.DECKS if d.name == "balcony")
    gan = next(d for d in P.DECKS if d.name == "gantry")
    piers = [(x, bal.z0) for x in range(bal.x0 + 6, bal.x1, 6)] + [(gan.x0, z) for z in range(gan.z0, gan.z1 + 1, 4)]
    for x, z in piers:
        for y in range(P.L1, P.L0 - 1):
            w.set(x, y, z, B.IRON_BLOCK if (y - P.L1) % 5 == 4 else B.STONEBRICK)
    for x in range(bal.x0, bal.x1 + 1):
        w.set(x, P.L0 - 2, bal.z0, B.STONEBRICK)                  # the beam along the balcony's lip
        if -8 <= x < gan.x0:
            w.set(x, P.L0, bal.z0, B.NETHER_FENCE)
    for z in range(gan.z0, gan.z1 + 1):
        w.set(gan.x0, P.L0 - 2, z, B.STONEBRICK)
        w.set(gan.x0, P.L0, z, B.NETHER_FENCE)
    for x in range(gan.x0, gan.x1 + 1):
        w.set(x, P.L0, gan.z0, B.NETHER_FENCE)


def reactor(w):
    """The reactor's hall: the pit under the core with its ladder and hazard ring, iron columns at the pit's
    corners, the cradle the core hangs in, coolant lines along the ceiling and consoles on the east wall."""
    p, c = P.PIT, P.CORE
    top = P.L1 + P.HALL["h"] - 1
    for x in range(p.x0 - 1, p.x1 + 2):
        for z in range(p.z0 - 1, p.z1 + 2):
            if not (p.x0 <= x <= p.x1 and p.z0 <= z <= p.z1):
                w.set(x, P.L1 - 1, z, *hazard(x, 0, z))
    for x in range(p.x0, p.x1 + 1):
        for z in range(p.z0, p.z1 + 1):
            w.set(x, p.y0 - 1, z, B.OBSIDIAN if (x + z) % 3 else B.COAL_BLOCK)
    lx = (p.x0 + p.x1) // 2
    for y in range(p.y0, p.y1 + 1):
        w.set(lx, y, p.z1, B.LADDER, orient.ladder("s"))
    for x, z in ((p.x0 - 2, p.z0 - 2), (p.x1 + 2, p.z0 - 2), (p.x0 - 2, p.z1 + 2), (p.x1 + 2, p.z1 + 2)):
        for y in range(P.L1, top + 1):
            w.set(x, y, z, B.IRON_BLOCK if (y - P.L1) % 4 else B.STONEBRICK, 0)
    for x, z in ((c.x0, c.z0), (c.x1, c.z0), (c.x0, c.z1), (c.x1, c.z1)):
        for y in range(c.y1 + 1, top + 1):
            w.set(x, y, z, B.IRON_BARS)
    for x in range(c.x0, c.x1 + 1):                              # the cradle's yoke over the core
        for z in (c.z0, c.z1):
            w.set(x, c.y1 + 1, z, B.IRON_BLOCK if x in (c.x0, c.x1) else B.IRON_BARS)
    h = P.HALL
    for z in range(h["z0"] + 2, h["z1"], 4):                     # coolant lines from the core to the walls
        for x in range(h["x0"], h["x1"] + 1):
            if not (c.x0 - 1 <= x <= c.x1 + 1 and c.z0 - 1 <= z <= c.z1 + 1):
                w.set(x, top, z, B.COBBLE_WALL)
    for z in range(h["z0"] + 1, 69, 3):                          # consoles along the east wall
        w.set(h["x1"], P.L1, z, B.IRON_BLOCK)
        w.set(h["x1"], P.L1 + 1, z, B.REDSTONE_LAMP)


def vault(w):
    """The cooling vault: a sunk pool lit from its floor, racks of spent rods along the walls, a plinth for the
    wool, and the blast door in the west wall with hazard bands either side of it."""
    v = next(s for s in P.SPACES if s.name == "vault")
    px0, px1, pz0, pz1 = v.x0 + 4, v.x0 + 10, v.z0 + 4, v.z0 + 11
    for x in range(px0 - 1, px1 + 2):
        for z in range(pz0 - 1, pz1 + 2):
            if not (px0 <= x <= px1 and pz0 <= z <= pz1):
                w.set(x, v.feet - 1, z, B.QUARTZ, 2 if (x + z) % 2 else 0)
                if (x + z) % 4:
                    w.set(x, v.feet, z, B.IRON_BARS)
            else:
                w.set(x, v.feet - 4, z, B.SEA_LANTERN if (x + z) % 3 == 0 else B.PRISMARINE)
                for y in range(v.feet - 3, v.feet):
                    w.set(x, y, z, B.WATER)
    for x0 in (v.x0, v.x1):                                      # racks of spent rods along both long walls
        for z in range(v.z0 + 2, v.z1 - 1, 3):
            for y in range(v.feet, v.feet + 5):
                w.set(x0, y, z, B.QUARTZ, 2)
            w.set(x0, v.feet + 5, z, B.SEA_LANTERN)
    wx, _, wz = P.WOOL_AT
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            w.set(wx + dx, v.feet - 1, wz + dz, B.QUARTZ, 1)
    d = P.VAULT_DOOR
    for x in range(d.x0, d.x1 + 1):
        for y in range(d.y0, d.y1 + 1):
            for z in range(d.z0, d.z1 + 1):
                w.set(x, y, z, B.BEDROCK)
    for y in range(d.y0, d.y1 + 2):
        for z in (d.z0 - 1, d.z1 + 1):
            w.set(d.x0 - 1, y, z, *hazard(0, y, z))
            w.set(d.x1 + 1, y, z, *hazard(0, y, z))


def gallery(w):
    """The bore's service gallery on the fissure: a jib over the edge with its cable hanging into the crack,
    broken rails along the lip and pipe racks along the back wall."""
    lips = {}
    for x, z in P.gallery_cells():
        lips[x] = min(z, lips.get(x, z))
    for x, z in lips.items():
        if x % 5 and (x * 7) % 3 and w.id(x, P.L2 - 1, z) != B.AIR:
            w.set(x, P.L2, z, B.NETHER_FENCE)
    xs_ = sorted(lips)
    h = P.GALLERY["h"]
    for x in (xs_[0] - 1, xs_[-1] + 1):                           # a frame round the mouth in the fissure's wall
        z = lips[xs_[0] if x < xs_[0] else xs_[-1]]
        for zz in range(z - 1, z + 2):
            for y in range(P.L2 - 1, P.L2 + h + 1):
                if w.id(x, y, zz) != B.AIR:
                    w.set(x, y, zz, B.NETHER_BRICK)
    for x in range(xs_[0] - 1, xs_[-1] + 2):
        z = lips.get(x, lips[xs_[0]])
        for zz in range(z - 1, z + 2):
            if w.id(x, P.L2 + h, zz) != B.AIR:
                w.set(x, P.L2 + h, zz, *hazard(x, 0, zz))
    jib_x = -6
    z0 = lips[jib_x]
    for z in range(z0 - 6, z0 + 4):                               # the jib, hung from the gallery's ceiling
        w.set(jib_x, P.L2 + h - 1, z, B.IRON_BLOCK)
    for y in range(P.L2 + 2, P.L2 + h - 1):
        w.set(jib_x, y, z0 - 6, B.FENCE)
    for x in range(P.GALLERY["x0"], P.GALLERY["x1"] + 1, 3):
        for y in (P.L2 + 6, P.L2 + 9):
            w.set(x, y, P.GALLERY["z1"], B.IRON_BARS)


def collapsed_store(w, top):
    """The store under the snowfield whose ceiling fell in: the hole torn ragged to the sky, the mound of rubble
    and broken slabs under it climbing to within a drop of the hole's lip, snow drifted in on its crown, and
    the store's crates crushed along its south wall."""
    s = next(sp for sp in P.SPACES if sp.name == "collapsed store")
    rh = P.ROOF_HOLE
    cx, cz = (rh["x0"] + rh["x1"]) / 2, (rh["z0"] + rh["z1"]) / 2
    ragged = noise.fbm((14, 14), 3, 1, seed=70)
    for dx in range(-7, 7):
        for dz in range(-7, 7):
            x, z = int(cx) + dx, int(cz) + dz
            if max(abs(x - cx), abs(z - cz)) > 2.6 + 0.9 * ragged[dx + 7, dz + 7]:
                continue
            for y in range(s.feet + s.h, int(top[x - land.X0, z - land.Z0]) + 2):
                w.set(x, y, z, B.AIR)
    rng = np.random.default_rng(71)
    peak = land.GROUND - 6
    for x in range(s.x0, s.x1 + 1):
        for z in range(s.z0, s.z1 + 1):
            height = int(round(peak - np.hypot(x - cx, z - cz) - 0.6 * rng.random()))
            for y in range(s.feet, height + 1):
                w.set(x, y, z, *RUBBLE[int(rng.integers(len(RUBBLE)))])
            if height >= s.feet and max(abs(x - cx), abs(z - cz)) < 3.2:
                w.set(x, height, z, B.SNOW)
                w.set(x, height + 1, z, B.SNOW_LAYER, int(rng.integers(0, 3)))
    for x, z, axis in ((rh["x0"] - 1, rh["z1"] + 3, "x"), (rh["x1"] + 3, rh["z0"], "z")):
        for t in range(-2, 3):                                     # slabs of the fallen ceiling lying on the mound
            X, Z = (x + t, z) if axis == "x" else (x, z + t)
            y = s.feet
            while w.id(X, y, Z) != B.AIR and y < s.feet + s.h - 1:
                y += 1
            w.set(X, y, Z, B.DSLAB)
    for x in range(s.x0, s.x1 + 1, 3):                            # crates crushed along the south wall
        if w.id(x, s.feet, s.z0) == B.AIR:
            w.set(x, s.feet, s.z0, B.PLANKS, 1)
            if x % 2:
                w.set(x, s.feet + 1, s.z0, B.LOG, 1)


SUPPLY = [(0, "minecraft:arrow", 32, 0), (4, "minecraft:cooked_beef", 8, 0), (8, "minecraft:golden_apple", 1, 0)]


def furnish(w):
    """What each room is for: racks and supply chests in the armoury, benches and lockers in the spawn room, iron
    in the iron room's walls with benches to work it at, generators and their flues in the generator house."""
    arm = next(s for s in P.SPACES if s.name == "armoury")
    for z in range(arm.z0 + 1, arm.z1, 2):                      # weapon racks along the west wall
        for y in range(arm.feet, arm.feet + 3):
            w.set(arm.x0, y, z, B.IRON_BARS)
    w.chest(arm.x0 + 1, arm.feet, arm.z0, SUPPLY, facing=3)
    w.chest(arm.x0 + 3, arm.feet, arm.z0, SUPPLY, facing=3)
    sp = next(s for s in P.SPACES if s.name == "spawn room")
    for x in range(sp.x0 + 2, sp.x1 - 1, 4):                    # lockers along the north wall, benches before them
        for y in (sp.feet, sp.feet + 1):
            w.set(x, y, sp.z1, B.IRON_BLOCK)
        w.set(x, sp.feet + 2, sp.z1, B.REDSTONE_LAMP)
        w.set(x, sp.feet, sp.z1 - 2, B.STONEBRICK_STAIRS, orient.stair("n"))
    for x in range(sp.x0 + 2, sp.x1, 5):                        # the team's colour on the south wall
        w.set(x, sp.feet + 3, sp.z0 - 1, *TEAM)
    for x, y, z in P.IRON:
        w.set(x, y, z, B.IRON_BLOCK)
    ir = next(s for s in P.SPACES if s.name == "iron room")
    for z in (ir.z0 + 3, ir.z1 - 3):
        w.set(ir.x0 + 3, ir.feet, z, B.CRAFTING)
    w.set(ir.x0 + 3, ir.feet, (ir.z0 + ir.z1) // 2, B.ANVIL)
    gh = next(s for s in P.SPACES if s.name == "generator house")
    for x0 in (gh.x0 + 2, gh.x1 - 5):                           # two generators: iron and furnaces under a flue
        for x in range(x0, x0 + 4):
            for z in range(gh.z1 - 3, gh.z1 + 1):
                w.set(x, gh.feet, z, *((B.IRON_BLOCK, 0) if (x + z) % 2 else (B.FURNACE, 2)))
                w.set(x, gh.feet + 1, z, B.SLAB, 7)
        for y in range(gh.feet + 2, gh.feet + gh.h):
            w.set(x0 + 1, y, gh.z1, B.COBBLE_WALL)
    for z in range(gh.z0 + 1, gh.z1 - 4, 2):
        w.set(gh.x1, gh.feet, z, B.PLANKS, 1)


def build(w, top):
    air = carve_and_line(w)
    gate(w)
    wings(w)
    garage(w)
    ramps(w)
    decks(w)
    reactor(w)
    vault(w)
    gallery(w)
    collapsed_store(w, top)
    furnish(w)
    return air
