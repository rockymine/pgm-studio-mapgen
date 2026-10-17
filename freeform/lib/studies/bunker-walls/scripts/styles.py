"""The segments, floors and faces of the bunker study, stated in segments.py's grammar.

    ANDESITE_SEG   the author's segment: a cobble L (top fading left to right, right leg fading up into cobble wall)
                   over a polished-andesite L, a stone-brick slab over nether brick, andesite fading up to stone
    CROSS_SEG      the author's segment with a gray-wool cross in its core
    DOTS_SEG       the author's segment with two obsidian studs in its core
    DARK_SEG       the same peels: coal on top, black wool down the right, an obsidian L, the slab over gray wool,
                   a bedrock core with a row of cyan clay one under its top
    SLIT_SEG       a bedrock frame round columns of iron bars over gray glass, alternating with bedrock
"""
from segments import (Peel, Segment, Solid, Fade, Bitmap, Checker, Courses, COBBLE, COBBLE_WALL, POL_ANDESITE,
                      ANDESITE, STONE, NETHER_BRICK, BEDROCK, OBSIDIAN, GRAY_WOOL, LIGHT_GRAY_WOOL, CLAY,
                      CYAN_CLAY, GRAY_GLASS, IRON_BARS, TOP_SLAB, COAL, BLACK_WOOL)

# the author's segment, colour by colour
BLUE = Fade(((COBBLE, 0.0), (COBBLE_WALL, 1.0)), axis="along", noise=0.55)       # left cobble, right wall
ORANGE = Fade(((COBBLE, 0.0), (COBBLE_WALL, 1.0)), axis="along", noise=0.55)     # bottom cobble, top wall
RED = Solid(POL_ANDESITE)
GREEN = Solid(TOP_SLAB["stonebrick"], back=NETHER_BRICK)
YELLOW = Fade(((ANDESITE, 0.0), (STONE, 1.0)), axis="v", noise=0.9)

L_PEELS = (Peel("top", BLUE), Peel("right", ORANGE), Peel("top", RED), Peel("left", RED), Peel("top", GREEN))

ANDESITE_SEG = Segment(L_PEELS, core=YELLOW, name="andesite")

CROSS = (".#.", "###", ".#.")
DOTS = ("#", ".", ".", "#")
CROSS_SEG = Segment(L_PEELS, core=Bitmap(CROSS, Solid(GRAY_WOOL), YELLOW), name="cross")
DOTS_SEG = Segment(L_PEELS, core=Bitmap(DOTS, Solid(OBSIDIAN), YELLOW), name="dots")

# the dark family: the author's peels in coal, black wool and obsidian over a bedrock core banded in cyan clay
DARK_SEG = Segment((Peel("top", Solid(COAL)), Peel("right", Solid(BLACK_WOOL)), Peel("top", Solid(OBSIDIAN)),
                    Peel("left", Solid(OBSIDIAN)), Peel("top", Solid(TOP_SLAB["stonebrick"], back=GRAY_WOOL))),
                   core=Courses((Solid(BEDROCK), Solid(CYAN_CLAY)), Solid(BEDROCK)), name="dark")

# a bedrock frame, and inside it iron bars over gray glass alternating with bedrock, column by column
BARS = Solid(IRON_BARS, back=GRAY_GLASS)
SLIT_SEG = Segment((Peel("top", Solid(BEDROCK)), Peel("left", Solid(BEDROCK)), Peel("right", Solid(BEDROCK)),
                    Peel("bottom", Solid(BEDROCK))), core=Solid(BEDROCK),
                   overlays=(lambda s, t, w, h: BARS if 0 < s < w - 1 and 0 < t < h - 1 and s % 2 == 1 else None,),
                   name="slit")

SEGMENTS = [ANDESITE_SEG, CROSS_SEG, DOTS_SEG, DARK_SEG, SLIT_SEG]

# floors: a one-block rim on two sides and a three-by-three core, four a side, laid on a grid counted from FLOOR_AT
FLOOR_MODULE = 4
FLOOR_AT = (12, 8)
FLOOR_GRID = Segment((Peel("top", Solid(STONE)), Peel("left", Solid(STONE))),
                     core=Checker(CLAY, LIGHT_GRAY_WOOL), name="floor-grid")
FLOOR_MORTAR = Segment((Peel("top", Checker(CLAY, LIGHT_GRAY_WOOL)), Peel("left", Checker(CLAY, LIGHT_GRAY_WOOL))),
                       core=Checker(STONE, ANDESITE, FLOOR_MODULE, FLOOR_AT), name="floor-mortar")
FLOOR_RING = Segment((Peel("top", Checker(CLAY, LIGHT_GRAY_WOOL)), Peel("left", Checker(CLAY, LIGHT_GRAY_WOOL))),
                     core=Bitmap(("...", ".#.", "..."), Solid(STONE), Solid(ANDESITE)), name="floor-ring")
FLOORS = [FLOOR_GRID, FLOOR_MORTAR, FLOOR_RING]

# the lofted retaining wall: cobble at the foot, up through polished andesite and andesite to stone
LOFT = Fade(((COBBLE, 0.0), (POL_ANDESITE, 0.3), (ANDESITE, 0.62), (STONE, 1.0)), axis="v", noise=0.9)
