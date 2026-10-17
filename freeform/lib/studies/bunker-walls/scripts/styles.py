"""The segments, floors and faces of the bunker study, stated in segments.py's grammar.

    ANDESITE_SEG   the author's segment: a cobble L (top fading left to right, right leg fading up into cobble wall)
                   over a polished-andesite L, a stone-brick slab over nether brick, andesite fading up to stone
    OBSIDIAN_SEG   the same peels in the dark family: gray wool, obsidian, a nether-brick slab over cyan clay, bedrock
    SLIT_SEG       bedrock framing gray wool, two slits of iron bars over gray glass
    CROSS_SEG      the author's segment with a gray-wool cross in its core
    DOTS_SEG       the author's segment with two obsidian studs in its core
    FRAMED_SEG     a bedrock ring round the dark Ls, the slot over cyan clay
"""
from segments import (Peel, Segment, Solid, Fade, Bitmap, Checker, slit, COBBLE, COBBLE_WALL, POL_ANDESITE,
                      ANDESITE, STONE, NETHER_BRICK, BEDROCK, OBSIDIAN, GRAY_WOOL, LIGHT_GRAY_WOOL, CLAY,
                      CYAN_CLAY, GRAY_GLASS, IRON_BARS, DSLAB, SMOOTH_DSLAB, TOP_SLAB)

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

# the dark family
DARK_TOP = Solid(GRAY_WOOL)
DARK_L = Solid(OBSIDIAN)
DARK_SLOT = Solid(TOP_SLAB["nether"], back=CYAN_CLAY)
DARK_CORE = Solid(BEDROCK)
OBSIDIAN_SEG = Segment((Peel("top", DARK_TOP), Peel("right", DARK_TOP), Peel("top", DARK_L), Peel("left", DARK_L),
                        Peel("top", DARK_SLOT)), core=DARK_CORE, name="obsidian")

FRAMED_SEG = Segment((Peel("top", Solid(BEDROCK)), Peel("left", Solid(BEDROCK)), Peel("right", Solid(BEDROCK)),
                      Peel("bottom", Solid(BEDROCK)), Peel("top", DARK_TOP), Peel("right", DARK_TOP),
                      Peel("top", DARK_SLOT)), core=DARK_L, name="framed")

BARS = Solid(IRON_BARS, back=GRAY_GLASS)
SLIT_SEG = Segment((Peel("top", Solid(BEDROCK)), Peel("left", Solid(BEDROCK)), Peel("right", Solid(BEDROCK)),
                    Peel("bottom", Solid(BEDROCK))), core=Solid(GRAY_WOOL),
                   overlays=(slit(lambda w: {w // 2 - 1, w // 2} if w >= 6 else {w // 2}, 2, 4, BARS),), name="slit")

SEGMENTS = [ANDESITE_SEG, CROSS_SEG, DOTS_SEG, OBSIDIAN_SEG, FRAMED_SEG, SLIT_SEG]

# floors: the same peels laid flat, in the light family
FLOOR_L = Segment((Peel("top", Solid(STONE)), Peel("right", Solid(STONE)), Peel("top", Solid(LIGHT_GRAY_WOOL)),
                   Peel("left", Solid(LIGHT_GRAY_WOOL))), core=Solid(CLAY), name="floor-l")
FLOOR_GRID = Segment((Peel("top", Solid(STONE)), Peel("left", Solid(STONE))),
                     core=Checker(CLAY, LIGHT_GRAY_WOOL), name="floor-grid")
FLOOR_PLATE = Segment((Peel("top", Solid(DSLAB)), Peel("left", Solid(DSLAB))),
                      core=Bitmap(("##", "##"), Solid(SMOOTH_DSLAB), Solid(CLAY)), name="floor-plate")
FLOORS = [FLOOR_L, FLOOR_GRID, FLOOR_PLATE]

# the lofted retaining wall: cobble at the foot, up through polished andesite and andesite to stone
LOFT = Fade(((COBBLE, 0.0), (POL_ANDESITE, 0.3), (ANDESITE, 0.62), (STONE, 1.0)), axis="v", noise=0.9)
