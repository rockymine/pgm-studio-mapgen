"""The segments, floors and faces of the bunker study, stated in segments.py's grammar.

    ANDESITE_SEG   the author's segment: a cobble L (top fading left to right, right leg fading up into cobble wall)
                   over a polished-andesite L, a stone-brick slab over nether brick, andesite fading up to stone
    STRIPE_*_SEG   the author's segment, its core stone on top, a stripe of obsidian or gray wool, the fade under it
    GRAY_CYAN_SEG  the author's segment, its core stone on top, a row of cyan clay, gray wool under it
    DARK_SEG       the same peels: coal on top, black wool down the right, an obsidian L, a nether-brick slab
                   over gray wool,
                   a bedrock core with a row of cyan clay one under its top
    SLIT_SEG       a bedrock frame round columns of iron bars over gray glass, alternating with bedrock
"""
from segments import (Peel, Segment, Solid, Fade, Courses, COBBLE, COBBLE_WALL, POL_ANDESITE,
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

# the same peels, the core in rows like the dark segment's: read down from its top, the rest under them
STRIPE_OBSIDIAN_SEG = Segment(L_PEELS, core=Courses((Solid(STONE), Solid(OBSIDIAN)), YELLOW), name="stripe-obsidian")
STRIPE_GRAY_SEG = Segment(L_PEELS, core=Courses((Solid(STONE), Solid(GRAY_WOOL)), YELLOW), name="stripe-gray")
GRAY_CYAN_SEG = Segment(L_PEELS, core=Courses((Solid(STONE), Solid(CYAN_CLAY)), Solid(GRAY_WOOL)), name="gray-cyan")

# the dark family: the author's peels in coal, black wool and obsidian over a bedrock core banded in cyan clay
DARK_SEG = Segment((Peel("top", Solid(COAL)), Peel("right", Solid(BLACK_WOOL)), Peel("top", Solid(OBSIDIAN)),
                    Peel("left", Solid(OBSIDIAN)), Peel("top", Solid(TOP_SLAB["nether"], back=GRAY_WOOL))),
                   core=Courses((Solid(BEDROCK), Solid(CYAN_CLAY)), Solid(BEDROCK)), name="dark")

# a bedrock frame, and inside it iron bars over gray glass alternating with bedrock, column by column
BARS = Solid(IRON_BARS, back=GRAY_GLASS)
SLIT_SEG = Segment((Peel("top", Solid(BEDROCK)), Peel("left", Solid(BEDROCK)), Peel("right", Solid(BEDROCK)),
                    Peel("bottom", Solid(BEDROCK))), core=Solid(BEDROCK),
                   overlays=(lambda s, t, w, h: BARS if 0 < s < w - 1 and 0 < t < h - 1 and s % 2 == 1 else None,),
                   name="slit")

SEGMENTS = [ANDESITE_SEG, STRIPE_OBSIDIAN_SEG, STRIPE_GRAY_SEG, GRAY_CYAN_SEG, DARK_SEG, SLIT_SEG]

# floors: tiles four a side, each lined on two edges and filled in two pieces, both L-shaped where they can be
FLOOR_MODULE = 4
FLOOR_L = Segment((Peel("top", Solid(CLAY)), Peel("left", Solid(LIGHT_GRAY_WOOL)), Peel("top", Solid(ANDESITE)),
                   Peel("left", Solid(ANDESITE))), core=Solid(STONE), name="floor-l")
FLOOR_BAR = Segment((Peel("top", Solid(CLAY)), Peel("left", Solid(LIGHT_GRAY_WOOL)), Peel("right", Solid(ANDESITE))),
                    core=Solid(STONE), name="floor-bar")
FLOOR_DARK = Segment((Peel("top", Solid(COBBLE)), Peel("left", Solid(ANDESITE)), Peel("top", Solid(CYAN_CLAY)),
                      Peel("left", Solid(CYAN_CLAY))), core=Solid(GRAY_WOOL), name="floor-dark")
FLOORS = [FLOOR_L, FLOOR_BAR, FLOOR_DARK]

# the lofted retaining wall: cobble at the foot, up through polished andesite and andesite to stone
LOFT = Fade(((COBBLE, 0.0), (POL_ANDESITE, 0.3), (ANDESITE, 0.62), (STONE, 1.0)), axis="v", noise=0.9)
