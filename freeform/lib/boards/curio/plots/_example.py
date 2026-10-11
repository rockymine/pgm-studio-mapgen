"""An example plot: a cottage with a ladder to its roof and a lean-to behind it. Not in the square."""
from mc import B

NAME = "The Example Cottage"
KIND = "house"


def build(c):
    c.fill(2, 0, 2, 8, 3, 7, B.PLANKS, 1)                      # the walls, hollowed below
    c.fill(3, 0, 3, 7, 3, 6, B.AIR)
    c.set(5, 0, 2, B.AIR); c.set(5, 1, 2, B.AIR)               # the doorway
    c.fill(1, 4, 1, 9, 4, 8, B.WOOD_SLAB, 1)                   # the flat roof
    c.fill(4, 5, 4, 6, 5, 5, B.COBBLE)                         # the chimney breast, a step up
    c.fill(5, 6, 4, 5, 7, 4, B.COBBLE)                         # the stack, climbed from the breast
    for y in range(0, 5):
        c.set(9, y, 4, B.LADDER, 5)                            # the ladder up the east wall
    c.fill(3, 0, 8, 7, 1, 10, B.HAY)                           # bales stacked behind
