"""A lattice radio mast with a hut at its foot: a plank hut with a raised doorway on the west and a flat roof, a stone
mast rising out of the hut's east side with cross-braces, a ladder up its west face and a dish on the top."""
from mc import B

NAME = "The Radio Mast"
KIND = "structure"

PLANK = (B.PLANKS, 1)          # spruce boards
STONE = (B.STONEBRICK, 0)
BRACE = (B.IRON_BLOCK, 0)
ROOF = (B.STAINED_CLAY, 8)     # light grey tiles
DISH = (B.WOOL, 0)


def build(c):
    # the hut: spruce walls four high, a roof of grey tiles, hollowed inside with a doorway two blocks up
    c.fill(1, 0, 3, 5, 4, 7, *PLANK)
    c.fill(1, 5, 3, 5, 5, 7, *ROOF)
    c.fill(2, 1, 4, 4, 3, 6, B.AIR)
    c.fill(1, 2, 5, 1, 3, 5, B.AIR)                 # the doorway, on the west, two blocks up
    c.fill(2, 2, 5, 2, 3, 5, B.AIR)
    c.set(0, 0, 5, B.SPRUCE_STAIRS, 0)               # the stair up to the doorway
    c.set(0, 0, 4, B.SPRUCE_STAIRS, 0)               # the hut's skirt, on the west, closed off by stairs
    c.set(0, 0, 6, B.SPRUCE_STAIRS, 0)
    # a window of glass on the hut's north wall
    c.set(3, 2, 3, *PLANK)
    # the mast: a stone spine two blocks thick, rising from the hut's east side to the sky
    c.fill(7, 0, 5, 8, 19, 6, *STONE)
    # cross-braces of iron, every four blocks, reaching out to each side
    for y in (4, 8, 12, 16):
        c.fill(8, y, 5, 9, y, 6, *BRACE)
    # the dish on the mast's east side near the top
    c.fill(10, 18, 5, 10, 20, 6, *DISH)
    # a ladder up the mast's west face, from the hut's roof to the top
    for y in range(0, 20):
        c.set(6, y, 5, B.LADDER, 4)
