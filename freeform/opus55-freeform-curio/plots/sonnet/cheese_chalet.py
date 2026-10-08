"""A cheese-wedge chalet: pale slope with cheese-hole shafts, a rind back wall, rooms and a loft inside."""
from mc import B

NAME = "The Cheese Chalet"
KIND = "house"

SANDSTONE_STAIRS = 128


def build(c):
    X0, X1 = 1, 9
    # body: yellow clay, slope of sandstone stairs rising south (45 degrees)
    for z in range(0, 11):
        if z > 0:
            c.fill(X0, 0, z, X1, z - 1, z, B.STAINED_CLAY, 4)
        for x in range(X0, X1 + 1):
            c.set(x, z, z, SANDSTONE_STAIRS, 2)
    c.fill(X0, 0, 0, X1, 0, 0, B.STAINED_CLAY, 4)
    # rind: the tall back wall and the base edge
    c.fill(X0, 0, 10, X1, 10, 10, B.STAINED_CLAY, 1)
    for x in (X0, X1):
        c.fill(x, 0, 0, x, 0, 10, B.STAINED_CLAY, 1)
    # darker crumb speckle on the slope sides
    for z in range(1, 10):
        for x in (X0, X1):
            if (z * 3 + x) % 4 == 0:
                c.set(x, z - 1, z, B.STAINED_CLAY, 0)
    # rooms: a low back room (z 2..5) and a tall front room (z 7..9), divided at z 6
    for z in range(1, 10):
        top = z - 3
        if top >= 0:
            c.fill(2, 0, z, 8, top, z, B.AIR)
    c.fill(2, 0, 7, 8, 6, 9, B.AIR)
    c.fill(2, 0, 6, 8, 3, 6, B.STAINED_CLAY, 4)
    c.fill(3, 0, 6, 3, 1, 6, B.AIR)            # doorway between rooms
    # the loft over the last two rows and a ladder up its front edge
    c.fill(2, 3, 8, 8, 3, 9, B.PLANKS, 1)
    c.fill(6, 0, 8, 6, 2, 8, B.PLANKS, 5)
    for y in range(0, 4):
        c.set(6, y, 7, B.LADDER, 2)
    # a second way up inside: crate steps in the front room
    c.set(2, 0, 7, B.PLANKS, 1)
    c.set(2, 1, 8, B.PLANKS, 1)
    c.set(2, 0, 8, B.PLANKS, 1)
    c.set(2, 2, 9, B.PLANKS, 1)
    c.fill(2, 0, 9, 2, 1, 9, B.PLANKS, 1)
    # cheese holes on the slope: shafts into the rooms
    def shaft(xc, zc, r):
        for x in range(X0 + 1, X1):
            for z in range(1, 10):
                if (x - xc) ** 2 + (z - zc) ** 2 <= r * r:
                    c.fill(x, 0, z, x, z, z, B.AIR)
                    c.set(x, -1, z, B.STAINED_CLAY, 1)
    shaft(7, 9, 1.3)
    shaft(3, 4, 1.0)
    # holes in the cut faces: east only, in the front room, plus a west door into the back room
    def hole(x, zc, yc, r):
        for z in range(0, 11):
            for y in range(0, 11):
                if (z - zc) ** 2 + (y - yc) ** 2 <= r * r:
                    c.set(x, y, z, B.AIR)
    hole(9, 8, 4, 1.5)
    hole(1, 8, 5, 1.0)
    c.fill(1, 0, 4, 1, 1, 4, B.AIR)
    # the chalet facade: timber posts, door, windows, balcony
    for x in (X0, X1):
        c.fill(x, 0, 10, x, 10, 10, B.LOG2, 1)
    c.fill(4, 0, 10, 4, 1, 10, B.AIR)
    c.fill(3, 0, 10, 3, 2, 10, B.PLANKS, 5)
    c.fill(5, 0, 10, 6, 2, 10, B.PLANKS, 5)
    c.fill(4, 2, 10, 4, 2, 10, B.PLANKS, 5)
    c.fill(4, 0, 8, 4, 2, 8, B.PLANKS, 1)
    c.fill(8, 4, 10, 8, 5, 10, B.PANE)
    c.fill(2, 4, 10, 2, 5, 10, B.PANE)
    c.fill(4, 5, 10, 5, 6, 10, B.AIR)
    c.fill(3, 7, 10, 7, 7, 10, B.PLANKS, 5)
    c.fill(4, 8, 10, 6, 8, 10, B.PLANKS, 5)
    c.set(5, 9, 10, B.PLANKS, 5)
    # inside furniture
    c.set(7, 0, 5, B.PLANKS, 1)
    c.fill(3, 0, 4, 3, 2, 5, B.STAINED_CLAY, 4)
    c.set(8, 0, 5, B.HAY)
    c.set(8, 0, 4, B.HAY)
    c.set(7, 0, 3, B.CRAFTING)
    c.set(4, 4, 9, B.CHEST, 3)
    c.set(8, 4, 8, B.BOOKSHELF)
    c.set(8, 4, 9, B.BOOKSHELF)
    c.set(3, 4, 9, B.TORCH, 5)
    # chimney on the slope
    c.fill(6, 7, 6, 7, 7, 7, B.BRICK)
    c.fill(6, 8, 6, 7, 11, 7, B.BRICK)
    c.fill(6, 8, 6, 7, 8, 7, B.BRICK)
    # flower boxes under the windows
