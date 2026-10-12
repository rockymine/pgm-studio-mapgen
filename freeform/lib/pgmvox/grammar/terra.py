"""The Terra style for pgmvox.grammar.rules: a mesa built on, red sandstone over banded terracotta.

    STYLE = terra.style(dye=14)
    grammar.lay(w, ground, STYLE, face_of=...)

    the body        the mesa's own strata by height, whatever the rim: terracotta, orange, white, yellow, brown,
                    red, in bands of two; block 36 at y 0
    the edge        eight courses: an upside-down red-sandstone stair at the rim, smooth red sandstone, terracotta
                    with a band of orange and one of white; every bay of seven, two pilasters of chiseled red
                    sandstone that stand out a block over a niche sunk into brown, arched at its head
    the show face   fourteen courses of terracotta under a chiseled band, a word sunk in brown, a row of white steps
                    under it
    the outline     brown clay, so the sections read as cut
    the fills       tiles (two-block checker of white and orange), zigzag (chevrons of white on orange pointing up
                    the board), kilim (stepped bands of the strata's colours), court (red sand in a frame of
                    terracotta and white, a yellow diamond at its heart), plain (smooth red sandstone in terracotta,
                    under a mark)
    the flight      stairs of red sandstone between cheeks of chiseled
    the deck        three courses of terracotta over five of air, the floor under it red sandstone on the strata
    the pillar      a chiseled red-sandstone base and capital, its shaft smooth
"""
from pgmvox.built import facade
from pgmvox.core.blocks import B
from pgmvox.core.orient import stair
from pgmvox.grammar import marks
from pgmvox.grammar import rules as G

TERRA = (B.HARDENED_CLAY, 0)
SMOOTH, CHISELED, RED = (B.RED_SANDSTONE, 2), (B.RED_SANDSTONE, 1), (B.RED_SANDSTONE, 0)
RED_SAND = (B.SAND, 1)
STRATA = [TERRA, TERRA, (B.STAINED_CLAY, 1), (B.STAINED_CLAY, 1), TERRA, (B.STAINED_CLAY, 0), (B.STAINED_CLAY, 4),
          TERRA, TERRA, (B.STAINED_CLAY, 12), (B.STAINED_CLAY, 14), TERRA]
BROWN, ORANGE, WHITE, YELLOW = (B.STAINED_CLAY, 12), (B.STAINED_CLAY, 1), (B.STAINED_CLAY, 0), (B.STAINED_CLAY, 4)
BAY = 7                                           # a pilaster, a niche five wide, a pilaster


def _rim(inward):
    return B.RED_SANDSTONE_STAIRS, stair(inward, upside_down=True)


def style(dye=14):
    """Terra's blocks for the grammar; `dye` is the team's colour, worn by its marks."""
    strata = G.bands(STRATA)

    def body(w, x, z, h):
        for y in range(1, h):
            w.set(x, y, z, *strata(x, y, z))
        w.set(x, 0, z, 36)

    plain = [_rim, SMOOTH, TERRA, (B.STAINED_CLAY, 1), TERRA, TERRA, (B.STAINED_CLAY, 0), TERRA]
    pilaster = [_rim, G.Course(CHISELED, out=_rim)] + [G.Course(SMOOTH, out=SMOOTH)] * 5 + \
        [G.Course(CHISELED, out=lambda inward: (B.RED_SANDSTONE_STAIRS, stair(inward)))]

    def niche(pos):
        """Five wide: an arch of upside-down stairs springing from the pilasters, the niche under it sunk into
        brown, its sill smooth."""
        head = [_rim, SMOOTH]
        if pos in (1, BAY - 2):                       # the springers, solid toward their pilaster
            toward = ({"n": "w", "s": "w", "e": "n", "w": "n"} if pos == 1 else
                      {"n": "e", "s": "e", "e": "s", "w": "s"})
            arch = [lambda inward: (B.RED_SANDSTONE_STAIRS, stair(toward[inward], upside_down=True))]
        else:
            arch = [G.Sunk(BROWN)]
        return head + arch + [G.Sunk(BROWN)] * 4 + [SMOOTH]

    edge = G.Face(plain, G.Accent(BAY, frame=pilaster, inner=niche, every=1, min_air=9, align="section"), floor=1)
    show = G.Face([_rim, SMOOTH, CHISELED] + [TERRA] * 10 + [SMOOTH], floor=1, pattern=(
        facade.word(6, "TERRA", BROWN), facade.glyph_row(0, ["step"], WHITE, spacing=7, inset=False)))
    flank = G.Face(plain, floor=1)
    deck_face = G.Face([_rim, SMOOTH, TERRA], floor=1)

    def deck(w, x, z, h, floor):
        for y in range(h - 2, h):
            w.set(x, y, z, *TERRA)
        for y in range(floor + 1, h - 2):
            w.set(x, y, z, B.AIR)
        w.set(x, floor, z, *RED)
        for y in range(1, floor):
            w.set(x, y, z, *strata(x, y, z))
        w.set(x, 0, z, 36)

    def pillar(w, x, z, top, bottom, side):
        for y in range(bottom, top + 1):
            w.set(x, y, z, *(CHISELED if y in (bottom, top) else SMOOTH))

    fills = {
        "tiles": marks.field(facade.first_of(facade.border(1, SMOOTH), facade.tiles(2, WHITE, ORANGE)),
                             name="tiles"),
        "zigzag": marks.field(facade.first_of(facade.border(1, TERRA), facade.chevrons(6, 2, WHITE, "n")),
                              under=ORANGE, name="zigzag"),
        "kilim": marks.field(facade.first_of(facade.border(1, BROWN),
                                             facade.kilim_steps(2, [TERRA, (B.STAINED_CLAY, 1), (B.STAINED_CLAY, 0),
                                                                    (B.STAINED_CLAY, 4)])), name="kilim"),
        "court": marks.field(facade.first_of(facade.border(1, TERRA), facade.border(1, WHITE, at=1),
                                             facade.medallion(0, 0.45, YELLOW)), under=RED_SAND, name="court"),
        "plain": marks.field(facade.border(1, TERRA), under=SMOOTH, name="plain"),
        "flight": marks.flight(SMOOTH, B.RED_SANDSTONE_STAIRS, cheek=CHISELED),
    }
    return G.Style(
        "terra",
        body=body,
        faces={"edge": edge, "show": show, "flank": flank, "deck": deck_face},
        seam=BROWN,
        fills=fills,
        choose=lambda sec, lot: ["court", "tiles"],
        params={"dye": dye, "deck_depth": 3, "pillar_every": 6},
        deck=deck,
        pillar=pillar)
