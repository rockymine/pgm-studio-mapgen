"""A stack of giant books, spines out, rising from the street in steps: each book one block thick, its cover a
colour, its pages a cream edge at the front. The stack climbs east; a book at each step lies a block further along."""
from mc import B

NAME = "The Book Stack"
KIND = "structure"

COVERS = [14, 11, 13, 4, 10, 9, 12, 1, 14, 11, 13]      # red, blue, green, yellow, purple, cyan, brown, orange
PAGES = (B.QUARTZ, 0)
SPINE = (B.STAINED_CLAY, 0)
SPINE_ROOF = (B.WOOL, 0)


def build(c):
    # the stack: book k lies at height k, its west end stepped one block further east than the book below
    for k in range(0, 11):
        x0 = k
        x1 = 10
        cover = (B.WOOL, COVERS[k % len(COVERS)])
        c.fill(x0, k, 1, x1, k, 9, *cover)
        # the pages, a cream edge at the east end of each book
        c.fill(x1, k, 1, x1, k, 9, *PAGES)
        # the spine, a band of darker cover along the back
        c.fill(x0, k, 1, x1 - 1, k, 1, B.WOOL, 15)
        c.fill(x0, k, 9, x1 - 1, k, 9, cover[0], cover[1])

    # a reading chamber hollowed in the middle of the stack, two blocks up, entered through a gap in its west wall
    c.fill(5, 4, 3, 8, 5, 7, B.AIR)
    c.fill(5, 6, 3, 8, 6, 7, *SPINE_ROOF)
    for y in (4, 5):
        for z in (3, 4, 6, 7):
            c.set(4, y, z, *SPINE_ROOF)
    c.set(4, 4, 5, B.AIR)
    c.set(4, 5, 5, B.AIR)
    # a bookmark ribbon hanging from the top book's end
    c.set(10, 10, 5, B.WOOL, 14)
