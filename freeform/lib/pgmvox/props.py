"""Props: small built things that dress a place, each with the way it faces and what it is made of as parameters.

    stall(w, x, y, z, "e", awning=14)          # a market stall on a floor at y, its counter toward the east
    stalls(w, cells, y, "e")                   # a row of them along an edge, a pace apart, colours in turn
    lamp(w, x, y, z)                           # a lamp post on a floor at y
    w.chest(x, y, z, laid(DEFENCE), facing=2)  # a chest laid out as a pattern, here a defence chest

A prop is placed on a floor: y is the floor block, and it stands from y + 1. Each returns the cells it stands on,
so a board can claim them and keep a route or a scatter off them.
"""
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
