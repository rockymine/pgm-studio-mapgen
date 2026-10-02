"""A hunters' camp in a spruce clearing: two canvas tents, a fire with a spit, log seats, a firewood stack and
a hide rack, stores, a cart and a straw dummy."""
from kit import Chunk


def tent(c, x0, z0, length, wool, along="z"):
    """A five-wide ridge tent, open at its far end, its ridge pole running on past both ends."""
    def at(u, y, v, block):
        x, z = (x0 + u, z0 + v) if along == "z" else (x0 + v, z0 + u)
        c.set(x, y, z, block)
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


def build():
    c = Chunk("camp", "Hunters' Camp", "forest",
              "Two canvas tents round a fire with a spit, log seats, a firewood stack, a hide rack and a straw dummy.")
    # a low rise in the north-east
    c.raise_(11, 0, 15, 4, 1)
    c.raise_(13, 0, 15, 2, 2)

    tent(c, 1, 1, 5, "35:0")
    c.set(2, 0, 2, "26:2"); c.set(2, 0, 1, "26:10")        # bed, head to the back
    c.set(4, 0, 2, "54:3")
    c.set(3, 0, 3, "171:12")
    tent(c, 9, 10, 4, "35:13", along="x")                    # a green tent facing west
    c.set(12, 0, 12, "26:3"); c.set(13, 0, 12, "26:11")

    # the fire: netherrack set into the ground, a ring of stones, a spit on two forks
    fx, fz = 7, 7
    c.set(fx, -1, fz, "87"); c.set(fx, 0, fz, "51")
    for dx, dz in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        c.set(fx + dx, 0, fz + dz, "44:3")
    for dx, dz in ((-1, -1), (1, 1), (-1, 1), (1, -1)):
        c.set(fx + dx, -1, fz + dz, "4")
    c.box(fx - 2, 0, fz, fx - 2, 1, fz, "85"); c.box(fx + 2, 0, fz, fx + 2, 1, fz, "85")
    c.box(fx - 2, 2, fz, fx + 2, 2, fz, "85")
    c.set(fx, 1, fz, "162:4")                                # a log roasting on the spit
    # log seats
    c.set(4, 0, 6, "17:9"); c.set(4, 0, 7, "17:9")
    c.set(7, 0, 10, "17:5"); c.set(8, 0, 10, "17:5")
    c.set(10, 0, 5, "17:1")
    # firewood stack and chopping block
    c.box(12, 1, 6, 14, 2, 7, "17:5")
    c.box(12, 0, 6, 14, 0, 7, "17:5")
    c.set(12, 3, 6, "126:1"); c.set(13, 3, 6, "126:1"); c.set(14, 3, 6, "126:1")
    c.set(11, 0, 8, "17:1"); c.set(11, 1, 8, "69:5")
    # a rack of hides
    c.box(12, 1, 2, 12, 2, 2, "188"); c.box(14, 1, 2, 14, 2, 2, "188")
    c.box(12, 3, 2, 14, 3, 2, "188")
    c.set(13, 2, 2, "35:12")
    # stores by the white tent
    c.set(6, 0, 1, "170:0"); c.set(7, 0, 1, "54:3"); c.set(8, 0, 1, "17:0"); c.set(8, 1, 1, "17:0")
    c.set(9, 0, 1, "118:3"); c.set(6, 1, 1, "170:4")
    # a gravel path in from the south bridge
    for z in range(10, 16):
        for x in (7, 8, 9):
            if (x + z) % 3:
                c.set(x, -1, z, "13")
            else:
                c.set(x, -1, z, "3:1")
    c.prop("hand-cart", 1, 0, 10)
    c.prop("scarecrow", 13, 1, 14, 0)
    c.prop("lantern-post", 6, 0, 14)

    # a smugglers' stash under the green tent, cut open on the east face, reached down a ladder shaft
    c.lower(12, 11, 15, 14, -9)
    c.roof(13, 11, 15, 14, -4, 0)
    c.roof(12, 12, 12, 14, -4, 0)
    for y in range(-8, 0):
        c.set(12, y, 11, "65:5")
    c.set(12, -1, 11, "96:8")
    c.box(12, -9, 11, 15, -9, 14, "5:1")
    c.set(15, -8, 14, "54:4"); c.set(14, -8, 14, "54:4")
    c.set(13, -8, 14, "17:0"); c.set(13, -7, 14, "17:0")
    c.set(15, -8, 11, "46"); c.set(15, -7, 11, "46")
    c.set(14, -5, 12, "89")
    c.set(14, -8, 12, "170:0")
    c.box(13, -8, 13, 13, -6, 13, "188")
    c.tree(3, 13, "tiny-spruce-2")
    c.tree(14, 9, "tiny-spruce-4")
    c.boulder(13, 2, 3, "angular")
    c.boulder(2, 8, 3)
    c.cover([(0, 0), (16, 0), (16, 16), (0, 16)], coverage=0.4, fernShare=0.5, flowerShare=0.08)
    return c
