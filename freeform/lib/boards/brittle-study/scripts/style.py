"""The Brittlebush look, read off Brittlebush I and II (CommunityMaps ctw/brittlebush, ctw/brittlebush_ii) and
written as functions a board can call. STYLE.md beside this folder says what each one copies and how it was read.

    face(w, x, z, h, inward, panel)      the five courses under a platform's edge
    base(w, x, z, h)                     the stone and bedrock under a surface, the obsidian sheet at y 1 and 2
    kerbed_bed(w, box, y, rng)           a sandstone-kerbed bed of grass, bushes and alliums
    sand_field(w, cells, y, rng)         sand with sandstone pebbles, cacti and dead bushes
    striped_path(w, box, y, along)       stone brick and stone-brick slab in alternate rows
    tier(w, plate, base_y, top, dye)     one storey of a tiered tower: black clay walls, birch panels, a band in
                                         the wool's colour, a plate with the same edge as the ground
    heart(w, cx, y, z, dye)              the wool's heart in pixel art, outlined in black wool
"""
from pgmvox import B
from pgmvox.orient import stair

DARK_OAK_SLAB = (B.WOOD_SLAB, 5)
SPRUCE_PLANKS = (B.PLANKS, 1)
BLACK_CLAY = (B.STAINED_CLAY, 15)
OPP = {"n": "s", "s": "n", "e": "w", "w": "e"}


def face(w, x, z, h, inward, panel=False):
    """A platform's edge, top down: an upside-down spruce stair whose full side is inward, so its top is flush and
    its underside steps back; brick; a dark-oak slab, which leaves a groove; an upside-down dark-oak stair; black
    clay. A panel swaps the brick and the dark oak for three birch stairs under the black clay: a light inset."""
    w.set(x, h, z, B.SPRUCE_STAIRS, stair(inward, upside_down=True))
    if panel:
        w.set(x, h - 1, z, *BLACK_CLAY)
        w.set(x, h - 2, z, B.BIRCH_STAIRS, stair(inward))
        w.set(x, h - 3, z, B.BIRCH_STAIRS, stair(inward))
        w.set(x, h - 4, z, B.BIRCH_STAIRS, stair(inward, upside_down=True))
    else:
        w.set(x, h - 1, z, B.BRICK)
        w.set(x, h - 2, z, *DARK_OAK_SLAB)
        w.set(x, h - 3, z, B.DARK_OAK_STAIRS, stair(inward, upside_down=True))
        w.set(x, h - 4, z, *BLACK_CLAY)


def base(w, x, z, h, fill=(B.STONE, 0), depth=4):
    """Under a surface at h: depth courses of stone, then bedrock, an obsidian sheet at y 1 and 2, bedrock at 0."""
    for y in range(h - depth, h):
        w.set(x, y, z, *fill)
    for y in range(3, h - depth):
        w.set(x, y, z, B.BEDROCK)
    w.set(x, 2, z, B.OBSIDIAN)
    w.set(x, 1, z, B.OBSIDIAN)
    w.set(x, 0, z, B.BEDROCK)


def kerbed_bed(w, box, y, rng, tree=None):
    """A bed of grass inside a kerb of sandstone stairs rising toward its middle, sandstone at the corners; tall
    grass, alliums and low bushes of birch leaves in it, and a birch tree at (tree) if given."""
    x0, z0, x1, z1 = box
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            ring = x in (x0, x1) or z in (z0, z1)
            corner = x in (x0, x1) and z in (z0, z1)
            if corner:
                w.set(x, y, z, B.SANDSTONE)
            elif ring:
                d = "e" if x == x0 else "w" if x == x1 else "s" if z == z0 else "n"
                w.set(x, y, z, B.SANDSTONE_STAIRS, stair(d))
            else:
                w.set(x, y, z, B.GRASS)
                c = rng.random()
                if c < 0.08:
                    w.set(x, y + 1, z, B.LEAVES, 2 | 4)
                elif c < 0.30:
                    w.set(x, y + 1, z, B.TALLGRASS, 1)
                elif c < 0.36:
                    w.set(x, y + 1, z, B.FLOWER, 2)
    if tree:
        tx, tz = tree
        top = y + 6
        for yy in range(y + 1, top):
            w.set(tx, yy, tz, B.LOG, 2)
        for yy in range(top - 2, top + 2):
            r = 2 if yy < top + 1 else 1
            for dx in range(-r, r + 1):
                for dz in range(-r, r + 1):
                    if abs(dx) + abs(dz) <= r + (1 if yy < top else 0) and w.get(tx + dx, yy, tz + dz)[0] == B.AIR:
                        w.set(tx + dx, yy, tz + dz, B.LEAVES, 2 | 4)


def sand_field(w, cells, y, rng):
    """Sand, with upside-down sandstone stairs lying on it as pebbles, cacti one to three high clear of anything
    beside them, and dead bushes."""
    cells = list(cells)
    taken = set(cells)
    for x, z in cells:
        w.set(x, y, z, B.SAND)
    for x, z in cells:
        c = rng.random()
        if c < 0.05:
            w.set(x, y, z, B.SANDSTONE_STAIRS, stair("nsew"[int(rng.random() * 4)], upside_down=True))
        elif c < 0.065:
            w.set(x, y + 1, z, B.DEADBUSH)
        elif c < 0.085:
            clear = all((x + dx, z + dz) in taken and w.get(x + dx, y + 1, z + dz)[0] == B.AIR
                        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if clear:
                for yy in range(y + 1, y + 2 + int(rng.random() * 3)):
                    w.set(x, yy, z, B.CACTUS)


def striped_path(w, box, y, along="x"):
    """A grey path in rows across its length: stone brick, then a stone-brick slab half a block lower, in turn."""
    x0, z0, x1, z1 = box
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            k = x if along == "x" else z
            w.set(x, y, z, *((B.STONEBRICK, 0) if k % 2 == 0 else (B.SLAB, 5)))


def tier(w, plate, base_y, top, dye, door=None, panels=True):
    """One storey of a tiered tower. Its plate (x0, z0, x1, z1) is the floor of the storey above, at top, and
    overhangs the walls by one: an upside-down spruce-stair rim, spruce planks, upside-down dark-oak stairs under
    the rim as brackets. The walls stand one in from the plate's edge, black clay from base_y + 1, a band of the
    wool's colour two under the plate, brick under the plate; birch-stair panels two high on each wall every
    three; a door (x0, x1) three high in the south wall."""
    x0, z0, x1, z1 = plate
    a0, b0, a1, b1 = x0 + 1, z0 + 1, x1 - 1, z1 - 1
    for x in range(a0, a1 + 1):
        for z in range(b0, b1 + 1):
            if not (x in (a0, a1) or z in (b0, b1)):
                continue
            along = z if x in (a0, a1) else x
            out = "w" if x == a0 else "e" if x == a1 else "n" if z == b0 else "s"
            corner = x in (a0, a1) and z in (b0, b1)
            for y in range(base_y + 1, top):
                v = top - y
                if door and z == b1 and door[0] <= x <= door[1] and y <= base_y + 3:
                    w.set(x, y, z, B.AIR)
                elif v == 1:
                    w.set(x, y, z, B.BRICK)
                elif v == 2:
                    w.set(x, y, z, B.WOOL, dye)
                elif panels and not corner and along % 3 == 1 and v in (3, 4) and top - base_y >= 5:
                    w.set(x, y, z, B.BIRCH_STAIRS, stair(OPP[out], upside_down=(v == 3)))
                else:
                    w.set(x, y, z, *BLACK_CLAY)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            ring = x in (x0, x1) or z in (z0, z1)
            if ring:
                inward = "e" if x == x0 else "w" if x == x1 else "s" if z == z0 else "n"
                w.set(x, top, z, B.SPRUCE_STAIRS, stair(inward, upside_down=True))
                if not (x in (x0, x1) and z in (z0, z1)):
                    w.set(x, top - 1, z, B.DARK_OAK_STAIRS, stair(inward, upside_down=True))
            else:
                w.set(x, top, z, *SPRUCE_PLANKS)


HEART = [".XX.XX.",
         "XXXXXXX",
         "XXXXXXX",
         ".XXXXX.",
         "..XXX..",
         "...X..."]


def heart(w, cx, y, z, dye):
    """The wool's heart, seven wide and six high in the wool, outlined in black wool and backed by it, standing
    upright facing south with its bottom at y; a pane of the wool's colour hangs it from below."""
    rows = len(HEART)
    filled = {(i - 3, rows - 1 - j) for j, row in enumerate(HEART) for i, c in enumerate(row) if c == "X"}
    outline = {(u + du, v + dv) for u, v in filled for du in (-1, 0, 1) for dv in (-1, 0, 1)} - filled
    for u, v in filled | outline:
        w.set(cx + u, y + v + 1, z, *((B.WOOL, dye) if (u, v) in filled else (B.WOOL, 15)))
        w.set(cx + u, y + v + 1, z - 1, B.WOOL, 15)
