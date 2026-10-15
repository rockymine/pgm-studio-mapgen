"""The Segment style for pgmvox.grammar.rules, read off CommunityMaps ctw/segment: a paved deck of grey slab and
clay, a brick line down every piece, cyan rims with bollards, and faces moulded in cobblestone walls over a band
sunk in the wool's colour.

    STYLE = segment.style(dye=5)        # dye: the wool colour of the side, laid in the sunk band

    the body        stone, bedrock to y 1, block 36 at y 0
    the edge        cyan clay at the rim, a cobblestone wall for a moulding, grey wool, a band sunk a block into
                    the wool's colour, a brick slab over it, a nether-brick slab, nether brick and obsidian at the
                    foot; on the rim a bollard three wide in every six, a cobblestone wall under a quartz slab
    the flank       the bullnose: cyan clay, a brick stair upright over one upside down, a cobblestone wall, brick,
                    a nether-brick slab
    the outline     cyan clay
    the fills       street (a stone kerb, a one-block checker of double slab and clay, a line of bricks two wide
                    down the long axis), plaza (the checker without the line), cross (the line both ways)
    the deck        the bullnose over nether brick, four of air under it, the street's slab for a floor
    the pillar      a cobblestone wall, iron bars between its ends
"""
from pgmvox.core.blocks import B
from pgmvox.core.orient import stair
from pgmvox.grammar import marks
from pgmvox.grammar import rules as G

CYAN, SLAB, CLAY, STONE = (B.STAINED_CLAY, 9), (B.DSLAB, 0), (B.CLAY, 0), (B.STONE, 0)
BRICK, WALL, GREY = (B.BRICK, 0), (B.COBBLE_WALL, 0), (B.WOOL, 7)
QZ_SLAB, BRICK_SLAB, NB_SLAB, NB = (B.SLAB, 7), (B.SLAB, 4), (B.SLAB, 6), (B.NETHER_BRICK, 0)


def _up(inward):
    return B.BRICK_STAIRS, stair(inward)


def _down(inward):
    return B.BRICK_STAIRS, stair(inward, upside_down=True)


def style(dye=5):
    """Segment's blocks for the grammar; `dye` is the wool colour the sunk band carries."""
    band = (B.STAINED_CLAY, dye)

    def body(w, x, z, h):
        for y in range(4, h):
            w.set(x, y, z, *STONE)
        for y in range(1, min(4, h)):
            w.set(x, y, z, B.BEDROCK)
        w.set(x, 0, z, 36)

    edge = G.Face([CYAN, WALL, GREY, G.Sunk(band), G.Course(BRICK_SLAB, back=band), NB_SLAB, NB, (B.OBSIDIAN, 0)],
                  floor=1, crest=lambda s, run: [WALL, QZ_SLAB] if (s + 3) % 6 < 3 and 0 < s < run - 1 else None)
    flank = G.Face([CYAN, _up, _down, WALL, BRICK, NB_SLAB], floor=1)
    deck_face = G.Face([CYAN, _up, _down, NB], floor=1)

    def deck(w, x, z, h, floor):
        for y in range(h - 3, h):
            w.set(x, y, z, *NB)
        for y in range(floor + 1, h - 3):
            w.set(x, y, z, B.AIR)
        body(w, x, z, floor)
        w.set(x, floor, z, *SLAB)

    def pillar(w, x, z, top, bottom, side):
        for y in range(bottom, top + 1):
            w.set(x, y, z, *(WALL if y in (bottom, top) else (B.IRON_BARS, 0)))

    def paving(line):
        """A stone kerb, the checker inside it, and the brick line two wide down the long axis, across, or both."""
        def f(c):
            if c.edge == 0:
                return STONE
            long_x = c.hw >= c.hh
            on = {"long": [abs(c.v) < 1 if long_x else abs(c.u) < 1],
                  "cross": [abs(c.v) < 1, abs(c.u) < 1], "none": []}[line]
            if any(on):
                return BRICK if (c.x + c.z) % 2 else (B.BRICK_STAIRS, stair("n", upside_down=True))
            return SLAB if (c.x + c.z) % 2 else CLAY
        return f

    fills = {"street": marks.field(paving("long"), name="street"), "plaza": marks.field(paving("none"), name="plaza"),
             "cross": marks.field(paving("cross"), name="cross"),
             "flight": marks.flight(SLAB, B.STONEBRICK_STAIRS, cheek=CYAN)}
    return G.Style("segment", body=body, faces={"edge": edge, "flank": flank, "deck": deck_face}, seam=CYAN,
                   fills=fills, choose=lambda sec, lot: ["street"], params={"dye": dye, "deck_depth": 4,
                                                                            "pillar_every": 6},
                   deck=deck, pillar=pillar)
