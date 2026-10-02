"""A hunters' camp in a spruce clearing, given room: the two tents face the fire across an open ring of log seats,
the hide rack stands on a knoll to the north-east under its spruce, firewood and stores sit at the clearing's
edge, a gravel path comes in from the south, and the smugglers' stash is dug under the green tent."""
from kit import Chunk


def tent(c, x0, z0, length, wool, along="z", y=0):
    """A five-wide ridge tent, open at its far end, its ridge pole running on past both ends."""
    def at(u, dy, v, block):
        x, z = (x0 + u, z0 + v) if along == "z" else (x0 + v, z0 + u)
        c.set(x, y + dy, z, block)
    for v in range(length):
        at(0, 0, v, wool); at(4, 0, v, wool)
        at(1, 1, v, wool); at(3, 1, v, wool)
        at(2, 2, v, wool)
        for u in (1, 2, 3):
            at(u, -1, v, "3:1")
    for u in (1, 2, 3):
        at(u, 0, 0, wool)
    at(2, 1, 0, wool)
    at(2, 2, -1, "85"); at(2, 2, length, "85")
    at(2, 0, length, "85"); at(2, 1, length, "85")
    at(0, 0, length, "85"); at(4, 0, length, "85")          # guy pegs


def build():
    c = Chunk("camp", "Hunters' Camp", "forest",
              "Two canvas tents across a fire with a spit and log seats, a hide rack on a spruce knoll, firewood "
              "and stores at the clearing's edge, and a stash dug under the green tent.", size=32)
    # landform: a spruce knoll to the north-east, a low ridge along the west, a shallow dip for the path
    c.hill(24, 8, 8, 3)
    c.raise_poly([(0, 0), (7, 0), (5, 6), (3, 12), (2, 15), (0, 15)], 1)
    c.raise_poly([(0, 0), (4, 0), (2, 7), (0, 9)], 2)
    c.raise_poly([(28, 18), (32, 16), (32, 30), (29, 30)], 1)

    # the white tent, facing south toward the fire
    tent(c, 7, 4, 6, "35:0")
    c.set(8, 0, 5, "26:2"); c.set(8, 0, 4, "26:10")
    c.set(10, 0, 5, "54:3")
    c.set(9, 0, 7, "171:12"); c.set(9, 0, 8, "171:12")
    # the green tent, facing west toward the fire
    tent(c, 20, 19, 5, "35:13", along="x")
    c.set(23, 0, 20, "26:3"); c.set(24, 0, 20, "26:11")
    c.set(23, 0, 22, "54:4")

    # the fire: netherrack set into the ground, a ring of stones, a spit on two forks
    fx, fz = 15, 15
    c.set(fx, -1, fz, "87"); c.set(fx, 0, fz, "51")
    for dx, dz in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        c.set(fx + dx, 0, fz + dz, "44:3")
    for dx, dz in ((-1, -1), (1, 1), (-1, 1), (1, -1)):
        c.set(fx + dx, -1, fz + dz, "4")
    for dx in range(-3, 4):
        for dz in range(-3, 4):
            if 2 < abs(dx) + abs(dz) <= 4:
                c.set(fx + dx, -1, fz + dz, "3:1" if (dx * 3 + dz) % 2 else "13")
    c.box(fx - 2, 0, fz, fx - 2, 1, fz, "85"); c.box(fx + 2, 0, fz, fx + 2, 1, fz, "85")
    c.box(fx - 2, 2, fz, fx + 2, 2, fz, "85")
    c.set(fx, 1, fz, "162:4")
    # log seats round the ring
    c.set(11, 0, 14, "17:9"); c.set(11, 0, 15, "17:9"); c.set(11, 0, 16, "17:9")
    c.set(14, 0, 19, "17:5"); c.set(15, 0, 19, "17:5")
    c.set(19, 0, 12, "17:1")

    # firewood stack and chopping block at the clearing's east edge
    c.box(23, 0, 13, 25, 2, 14, "17:5")
    for x in (23, 24, 25):
        c.set(x, 3, 13, "126:1"); c.set(x, 3, 14, "126:1")
    c.set(22, 0, 16, "17:1"); c.set(22, 1, 16, "69:5")
    c.set(23, 0, 16, "17:5"); c.set(24, 0, 17, "17:9")

    # the hide rack on the knoll's top
    top = 3
    c.box(22, top, 8, 22, top + 1, 8, "188"); c.box(26, top, 8, 26, top + 1, 8, "188")
    c.box(22, top + 2, 8, 26, top + 2, 8, "188")
    c.set(23, top + 1, 8, "35:12"); c.set(25, top + 1, 8, "35:1")

    # stores beside the white tent
    c.set(12, 0, 4, "170:0"); c.set(12, 1, 4, "170:4"); c.set(13, 0, 4, "54:3")
    c.set(14, 0, 4, "17:0"); c.set(14, 1, 4, "17:0"); c.set(15, 0, 4, "118:3")

    # a gravel path in from the south bridge, winding to the fire
    for z in range(19, 32):
        bend = 0 if z > 26 else (-1 if z > 22 else 0)
        for x in (15 + bend, 16 + bend, 17 + bend):
            c.set(x, -1, z, "13" if (x + z) % 3 else "3:1")
    c.prop("hand-cart", 3, 0, 18)
    c.prop("scarecrow", 25, 0, 27, 0)
    c.prop("lantern-post", 13, 0, 27)

    # the smugglers' stash under the green tent, open on the east face, down a ladder shaft
    c.lower(24, 22, 31, 28, -9)
    c.roof(25, 22, 31, 28, -4, 0)
    c.roof(24, 23, 24, 28, -4, 0)
    for y in range(-8, 0):
        c.set(24, y, 22, "65:5")
    c.set(24, -1, 22, "96:8")
    c.box(24, -9, 22, 31, -9, 28, "5:1")
    for x in (26, 29):
        c.box(x, -8, 22, x, -5, 22, "17:1"); c.box(x, -8, 28, x, -5, 28, "17:1")
        c.box(x, -5, 23, x, -5, 27, "17:9")
    c.set(31, -8, 28, "54:4"); c.set(30, -8, 28, "54:4")
    c.set(28, -8, 28, "17:0"); c.set(28, -7, 28, "17:0")
    c.set(31, -8, 22, "46"); c.set(31, -7, 22, "46"); c.set(30, -8, 22, "46")
    c.set(28, -6, 25, "89")
    c.set(27, -8, 23, "170:0"); c.set(27, -7, 23, "170:4")
    c.box(28, -8, 26, 28, -6, 26, "188")

    c.tree(26, 5, "tiny-spruce-4")
    c.tree(5, 27, "tall-spruce-2")
    c.boulder(20, 4, 3, "angular")
    c.boulder(4, 13, 3)
    c.cover([(0, 0), (32, 0), (32, 32), (0, 32)], coverage=0.4, fernShare=0.5, flowerShare=0.08)
    return c
