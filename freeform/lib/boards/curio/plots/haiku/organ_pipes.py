"""A bank of church organ pipes on a wooden case, tallest in the middle. A hollow in the case is entered by a passage two
blocks up from a stair on the west; a ladder climbs the west side to a ledge on the case, and the gaps between
the pipes make nooks to stand in."""
from mc import B

NAME = "The Organ Pipes"
KIND = "structure"

CASE = (B.PLANKS, 3)            # jungle planks, the case of the organ
TIN = (B.IRON_BLOCK, 0)         # the metal pipes
BRASS = (B.GOLD_BLOCK, 0)       # the mouths
CONSOLE = (B.PLANKS, 0)

PIPES = {2: 9, 4: 13, 6: 16, 8: 11}      # pipe at each x, and the height it reaches


def build(c):
    # the case: a box of wood, five blocks high, with a hollow inside
    c.fill(1, 0, 3, 9, 5, 7, *CASE)
    c.fill(3, 1, 4, 7, 3, 6, B.AIR)
    c.fill(1, 2, 4, 2, 3, 4, B.AIR)
    c.fill(2, 2, 4, 2, 3, 4, B.AIR)
    c.set(0, 0, 4, B.OAK_STAIRS, 0)
    # the pipes: a tin column at each station, from the case's top to its height, with a brass mouth
    for x, top in PIPES.items():
        c.fill(x, 6, 4, x, top, 6, *TIN)
        c.set(x, top, 5, *BRASS)
    # the console: a bench of wood at the front, on the south side of the case
    c.fill(3, 6, 8, 7, 6, 9, *CONSOLE)
    # a ladder up the west face, from the grass to the case top
    for y in range(0, 6):
        c.set(0, y, 5, B.LADDER, 4)
