"""Props: small built things that dress a place, each with the way it faces and what it is made of as parameters.

    stall(w, x, y, z, "e", awning=14)          # a market stall on a floor at y, its counter toward the east
    stalls(w, cells, y, "e")                   # a row of them along an edge, a pace apart, colours in turn
    lamp(w, x, y, z)                           # a lamp post on a floor at y
    lamps(w, path, H, X, Z, every=12)          # lamp posts beside a route, sides in turn
    brazier(w, x, y, z)                        # a post on a stone footing with a light on top
    rubble(w, x, y, z, rng)                    # a low heap of loose stone
    w.chest(x, y, z, laid(DEFENCE), facing=2)  # a chest laid out as a pattern, here a defence chest
    wool_chests(w, (x0, z0, x1, z1), y, "s")   # the studio's wool-room loot, two chests in each inner corner
    defence_chests(w, [(x, z) ...], y, "s")    # the studio's defence chests set into a wall's face, lids opened

A prop is placed on a floor: y is the floor block, and it stands from y + 1. Each returns the cells it stands on,
so a board can claim them and keep a route or a scatter off them.
"""
import math

from .blocks import B
from .orient import NAMES, vec

AWNINGS = (14, 4, 11, 13)                      # red, yellow, blue, green: a row of stalls takes them in turn


def stall(w, x, y, z, facing="e", awning=14, stripe=0, post=(B.FENCE, 0), goods=None, chest=True):
    """A market stall three by three on the floor at y, its counter on the side it faces: fence posts at the
    corners two high, a striped wool awning over them (awning and stripe the dyes), a slab counter at the front
    with goods on it (default a pumpkin or a melon) and a chest behind. Returns its cells."""
    fx, fz = vec(facing)
    rx, rz = -fz, fx                                           # across the stall
    cells = []

    def at(u, v):                                              # u back to front (0..2), v across (-1..1)
        return x + fx * (u - 1) + rx * v, z + fz * (u - 1) + rz * v
    for u in (0, 2):
        for v in (-1, 1):
            px, pz = at(u, v)
            for yy in (1, 2):
                w.set(px, y + yy, pz, *post)
    for u in range(3):
        for v in (-1, 0, 1):
            px, pz = at(u, v)
            w.set(px, y + 3, pz, B.WOOL, stripe if v == 0 else awning)
            cells.append((px, pz))
    cx, cz = at(2, 0)
    w.set(cx, y + 1, cz, B.WOOD_SLAB, 1 | 8)                   # the counter, an upper slab
    g = goods if goods is not None else ((B.PUMPKIN, 3) if (x + z) % 2 else (B.MELON, 0))
    w.set(cx, y + 2, cz, *g)
    if chest:
        bx, bz = at(1, 0)
        w.chest(bx, y + 1, bz, [], facing={"n": 2, "s": 3, "w": 4, "e": 5}[NAMES[(fx, fz)]])
    return cells


def stalls(w, line, y, facing="e", every=5, awnings=AWNINGS, stripe=0):
    """A row of stalls along a line of cells [(x, z), ...] on a floor at y, one every `every` cells, each facing
    the same way, their awnings taking `awnings` in turn. Returns every cell they stand on."""
    cells = []
    for i, (x, z) in enumerate(line[1:-1:every] if len(line) > 2 else line):
        cells += stall(w, x, y, z, facing, awnings[i % len(awnings)], stripe)
    return cells


def lamp(w, x, y, z, height=3, post=(B.FENCE, 0), light=(B.GLOWSTONE, 0), cap=(B.WOOD_SLAB, 5)):
    """A lamp post on the floor at y: a post `height` high, a light on it and a slab cap. Returns its cell."""
    for yy in range(1, height + 1):
        w.set(x, y + yy, z, *post)
    w.set(x, y + height + 1, z, *light)
    if cap:
        w.set(x, y + height + 2, z, *cap)
    return [(x, z)]



# A chest is laid out as a picture: three rows of nine slots, one letter a slot, a legend saying what each letter
# holds. A row is filled the same from either end, so the heavy stacks balance across the chest, the rare things sit in
# the middle, and the tools are centred rather than left at the end of a run of planks.
DEFENCE = (["PSCERECSP",
            "PSEKRKESP",
            "PSCERECSP"],
           {"P": ("minecraft:planks", 64, 5), "S": ("minecraft:planks", 32, 1), "C": ("minecraft:crafting_table", 16, 0),
            "E": ("minecraft:end_stone", 16, 0), "R": ("minecraft:redstone_block", 16, 0),
            "K": ("minecraft:iron_pickaxe", 1, 0, [(32, 2)])})
"""A defence chest for a team's line: dark-oak planks at the ends, spruce inside them, crafting tables and end
stone toward the middle, a column of redstone blocks down the centre, and two Efficiency II iron pickaxes either
side of it."""

ROOM_GEAR = (["A...H...A",
              "W.FCGLF.W",
              "A...B...A"],
             {"A": ("minecraft:arrow", 16, 0), "W": ("minecraft:planks", 32, 0), "F": ("minecraft:cooked_beef", 8, 0),
              "H": ("minecraft:iron_helmet", 1, 0), "C": ("minecraft:iron_chestplate", 1, 0),
              "G": ("minecraft:golden_apple", 2, 0), "L": ("minecraft:iron_leggings", 1, 0),
              "B": ("minecraft:iron_boots", 1, 0)})
"""The gear in a wool room: a set of iron armour down the middle around two golden apples, food either side, and
arrows and planks at the four ends."""


SPEED_POTION = 8194                            # 1.8 Potion of Swiftness, Speed I for 3:00
WOOL_CHEST_LOW = (["PPPPPPPPP", "SSSSSSSSS", "GGGGGGGGG"],
                  {"P": ("minecraft:planks", 16, 0), "S": ("minecraft:potion", 1, SPEED_POTION),
                   "G": ("minecraft:golden_apple", 16, 0)})
WOOL_CHEST_HIGH = (["LLLLLLLLL", "BBBBBBBBB", "PPPPPPPPP"],
                   {"L": ("minecraft:diamond_leggings", 1, 0), "B": ("minecraft:bow", 1, 0, [(48, 1), (51, 1)]),
                    "P": ("minecraft:planks", 16, 0)})
"""The studio's wool-room loot (its WoolChests stamper), for the attackers who reach the room: the lower chest a row
each of planks, Speed potions and golden apples by sixteen; the upper a row each of diamond leggings, Power I
Infinity bows and planks."""


def wool_chests(w, box, floor, door="s"):
    """The studio's wool-room loot: two chests stacked in each inner corner of the room whose inside is
    box = (x0, z0, x1, z1), on the floor at `floor`. Every chest opens along the axis of the room's door wall
    `door` ("n", "s", "e" or "w"), away from the corner's wall on that axis, so none fronts a wall. Returns the
    corners."""
    x0, z0, x1, z1 = box
    corners = [(x0, z0), (x1, z0), (x0, z1), (x1, z1)]
    for x, z in corners:
        if door in "ns":
            facing = 3 if z == z0 else 2           # opens south off the north wall, north off the south
        else:
            facing = 5 if x == x0 else 4           # opens east off the west wall, west off the east
        w.chest(x, floor + 1, z, laid(WOOL_CHEST_LOW), facing=facing)
        w.chest(x, floor + 2, z, laid(WOOL_CHEST_HIGH), facing=facing)
    return corners


def studio_defence():
    """The studio's defence chest (its DefenseChest stamper), slot by slot: dark-oak planks in twelve half stacks,
    spruce in seven, crafting tables in four, a half stack each of end stone and redstone blocks, and two
    Efficiency II iron pickaxes; 27 slots, a full chest."""
    stacks = [("minecraft:planks", 5)] * 12 + [("minecraft:planks", 1)] * 7 + [("minecraft:crafting_table", 0)] * 4 + \
        [("minecraft:end_stone", 0), ("minecraft:redstone_block", 0)]
    items = [(k, i, 32, d) for k, (i, d) in enumerate(stacks)]
    items += [(25, "minecraft:iron_pickaxe", 1, 0, [(32, 2)]), (26, "minecraft:iron_pickaxe", 1, 0, [(32, 2)])]
    return items


def defence_chests(w, cells, y, facing="s"):
    """The studio's defence chests set into a wall: a chest at each (x, z) of the wall's face at y, the player's
    standing height on the approach, opening toward `facing` ("n", "s", "e", "w"), and the block over it carved to
    air so its lid opens. The column behind each chest is left as it was, so the wall still stands whole."""
    data = {"n": 2, "s": 3, "w": 4, "e": 5}[facing]
    for x, z in cells:
        w.chest(x, y, z, studio_defence(), facing=data)
        w.set(x, y + 1, z, B.AIR)
    return list(cells)


def laid(layout, symmetric=True):
    """The items of a chest drawn as rows of letters: (rows, legend) -> [(slot, id, count, damage[, ench])]. '.' is
    an empty slot. symmetric asks that every row be filled the same from either end; a pair such as a chestplate and
    leggings may mirror each other."""
    rows, legend = layout
    items = []
    for r, row in enumerate(rows):
        if len(row) != 9:
            raise ValueError(f"a chest row is nine slots: {row!r}")
        filled = [c != "." for c in row]
        if symmetric and filled != filled[::-1]:
            raise ValueError(f"row {r} is not filled the same from either end: {row!r}")
        for col, c in enumerate(row):
            if c != ".":
                items.append((r * 9 + col,) + tuple(legend[c]))
    return items


def brazier(w, x, y, z, post=(B.NETHER_FENCE, 0), light=(B.GLOWSTONE, 0), height=2, base=(B.COBBLE_WALL, 0)):
    """A post on a stone footing, a light on top, standing on the floor at y."""
    w.set(x, y + 1, z, *base)
    for k in range(2, height + 1):
        w.set(x, y + k, z, *post)
    w.set(x, y + height + 1, z, *light)


def rubble(w, x, y, z, rng, r=1.6, blocks=((B.STONE, 5), (B.COBBLE, 0), (B.STONE, 0), (B.GRAVEL, 0)),
           supported=True):
    """A heap of loose stone r across on the floor at y, its blocks drawn from rng. It fills only air and low
    plants, and with `supported` only where the block below is ground, so no stone hangs over air or water."""
    loose = (B.AIR, B.TALLGRASS, B.DEADBUSH)
    R = int(math.ceil(r))
    for dx in range(-R, R + 1):
        for dz in range(-R, R + 1):
            d = math.hypot(dx, dz) + rng.uniform(-0.4, 0.4)
            if d <= r:
                top = int(round((r - d) * 0.9)) + (1 if rng.random() < 0.5 else 0)
                for k in range(1, max(1, top) + 1):
                    if w.id(x + dx, y + k, z + dz) in loose and \
                            (not supported or w.id(x + dx, y + k - 1, z + dz) not in loose + (B.WATER,)):
                        w.set(x + dx, y + k, z + dz, *blocks[int(rng.integers(len(blocks)))])


def lamps(w, path, H, X, Z, every=12, post=(B.NETHER_FENCE, 0), light=(B.GLOWSTONE, 0), height=2, side=3.0, start=6):
    """Lamp posts beside a route every `every` blocks from `start`, `side` blocks off it, on alternate sides, each on
    the ground H gives under it (where H is above 0). Returns the posts' cells."""
    from .shapes import length, point_at
    total = length(path)
    s, n = start, 0
    out = []
    while s < total:
        (px, pz), (hx, hz) = point_at(path, s)
        nx, nz = -hz, hx
        sg = 1 if n % 2 == 0 else -1
        x, z = int(round(px + sg * side * nx)), int(round(pz + sg * side * nz))
        i, k = x - int(X[0, 0]), z - int(Z[0, 0])
        if 0 <= i < H.shape[0] and 0 <= k < H.shape[1] and H[i, k] > 0:
            y = int(H[i, k])
            for t in range(1, height + 1):
                w.set(x, y + t, z, *post)
            w.set(x, y + height + 1, z, *light)
            out.append((x, z))
        s += every
        n += 1
    return out


def crop_field(w, box, y, crops, rng, rows=9, ditch=4, tilt=0.0, ripe=(0.15, (4, 8)), fence="w", gate=None):
    """A field over `box` (x0, z0, x1, z1) laid on a plane at y, tilting `tilt` blocks a block along z: farmland
    in strips `rows` rows deep taking `crops` in turn, a water ditch in row `ditch` of every strip, a grass edge,
    the ground cleared over it and filled with dirt under it. Of the wheat, a share `ripe[0]` drawn from rng is at
    an age in `ripe[1]` instead. A fence runs along the `fence` side ("w" or "e") with a gate in row `gate` (the
    middle where None)."""
    x0, z0, x1, z1 = box
    gate = (z0 + z1) // 2 if gate is None else gate
    fx = x0 if fence == "w" else x1
    for z in range(z0, z1 + 1):
        crop = crops[((z - z0) // rows) % len(crops)]
        wet = ditch is not None and (z - z0) % rows == ditch
        yz = y + int(round((z - (z0 + z1) / 2) * tilt))
        for x in range(x0, x1 + 1):
            g = w.top(x, z)
            for yy in range(yz + 1, g + 3):
                w.set(x, yy, z, B.AIR)
            for yy in range(min(g, yz) - 2, yz):
                w.set(x, yy, z, B.DIRT)
            if wet and x0 < x < x1:
                w.set(x, yz, z, B.WATER)
            elif x in (x0, x1) or z in (z0, z1):
                w.set(x, yz, z, B.GRASS)
            else:
                w.set(x, yz, z, B.FARMLAND, 7)
                c = crop if not (crop[0] == B.WHEAT and rng.random() < ripe[0]) else \
                    (B.WHEAT, int(rng.integers(*ripe[1])))
                w.set(x, yz + 1, z, *c)
        w.set(fx, yz + 1, z, *((B.FENCE_GATE, 1) if z == gate else (B.FENCE, 0)))


def scarecrow(w, x, z, facing="n"):
    """A scarecrow on the ground at (x, z): two fence posts, a hay body with fence arms across `facing`, a pumpkin
    head."""
    from .orient import vec
    y = w.top(x, z)
    for yy, blk in ((1, (B.FENCE, 0)), (2, (B.FENCE, 0)), (3, (B.HAY, 0)), (4, (B.PUMPKIN, 3))):
        w.set(x, y + yy, z, *blk)
    fx, fz = vec(facing)
    w.set(x - fz, y + 3, z + fx, B.FENCE)
    w.set(x + fz, y + 3, z - fx, B.FENCE)

