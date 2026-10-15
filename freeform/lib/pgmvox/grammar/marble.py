"""The Marble style for pgmvox.grammar.rules: a temple's quartz over diorite, its insets dark prismarine and lit.

    STYLE = marble.style(dye=14)
    grammar.lay(w, ground, STYLE, face_of=...)

    the body        polished diorite four courses under the floor, diorite under that, bedrock to y 1, block 36 at y 0
    the edge        ten courses: an upside-down quartz stair at the rim, chiseled quartz, quartz, a band of dark
                    prismarine, quartz to the foot; every bay of six, two engaged columns of pillar quartz, their
                    capitals and bases thrown out a block, over a panel sunk into prismarine bricks with a sea
                    lantern at its heart
    the show face   fourteen courses of quartz fluted in dark prismarine, a word inlaid flush over the flutes
    the outline     chiseled quartz
    the fills       medallion (a diamond of rings in quartz and prismarine on diorite, a lantern at its heart), star
                    (an eight-pointed star of dark prismarine on quartz in a band), rings (round rings of quartz and
                    diorite), grid (quartz in a chiseled frame lined in dark prismarine, crossed by prismarine bars
                    every four along its long side), plain (quartz in chiseled quartz, under a mark)
    the flight      stairs of quartz between cheeks of chiseled quartz
    the deck        an entablature of three courses, chiseled over quartz, over five of air; the floor under it
                    prismarine bricks
    the pillar      a column of pillar quartz, its base and capital chiseled
"""
from pgmvox.built import facade
from pgmvox.core.blocks import B
from pgmvox.core.orient import stair
from pgmvox.grammar import marks
from pgmvox.grammar import rules as G

QUARTZ, CHISELED, PILLAR = (B.QUARTZ, 0), (B.QUARTZ, 1), (B.QUARTZ, 2)
DARK, BRICKS, PRISM = (B.PRISMARINE, 2), (B.PRISMARINE, 1), (B.PRISMARINE, 0)
DIORITE, POLISHED = (B.STONE, 3), (B.STONE, 4)
LANTERN = (B.SEA_LANTERN, 0)
BAY = 6                                           # a column, a panel four wide, a column


def _rim(inward):
    return B.QUARTZ_STAIRS, stair(inward, upside_down=True)


def _foot(inward):
    return B.QUARTZ_STAIRS, stair(inward)


def style(dye=14):
    """Marble's blocks for the grammar; `dye` is the team's colour, worn by its marks."""
    def body(w, x, z, h):
        for y in range(max(1, h - 4), h):
            w.set(x, y, z, *POLISHED)
        for y in range(4, h - 4):
            w.set(x, y, z, *DIORITE)
        for y in range(1, min(4, h)):
            w.set(x, y, z, B.BEDROCK)
        w.set(x, 0, z, 36)

    plain = [_rim, CHISELED, QUARTZ, DARK, QUARTZ, QUARTZ, QUARTZ, QUARTZ, QUARTZ, CHISELED]
    column = [_rim, G.Course(CHISELED, out=_rim)] + [PILLAR] * 7 + [G.Course(CHISELED, out=_foot)]

    def panel(pos):
        mid = pos in (2, 3)
        return [_rim, CHISELED, QUARTZ, DARK] + [G.Sunk(BRICKS), G.Sunk(LANTERN if mid else BRICKS),
                                                  G.Sunk(LANTERN if mid else BRICKS), G.Sunk(BRICKS)] + \
            [QUARTZ, CHISELED]

    edge = G.Face(plain, G.Accent(BAY, frame=column, inner=panel, every=1, min_air=10, align="section"), floor=1)
    show = G.Face([_rim, CHISELED] + [QUARTZ] * 12, floor=1, pattern=(
        facade.word(8, "MARBLE", DARK, inset=False),
        facade.flutes(3, 1, 1, 6, DARK),
        lambda s, run, t, h, n: ("accent", DARK) if t == 7 else None))
    flank = G.Face(plain, floor=1)
    deck_face = G.Face([_rim, CHISELED, QUARTZ], floor=1)

    def deck(w, x, z, h, floor):
        w.set(x, h - 1, z, *CHISELED)
        w.set(x, h - 2, z, *QUARTZ)
        for y in range(floor + 1, h - 2):
            w.set(x, y, z, B.AIR)
        body(w, x, z, floor)
        w.set(x, floor, z, *BRICKS)

    def pillar(w, x, z, top, bottom, side):
        for y in range(bottom, top + 1):
            w.set(x, y, z, *(CHISELED if y in (bottom, top) else PILLAR))

    fills = {
        "medallion": marks.field(facade.first_of(
            facade.border(1, DARK), facade.medallion(0.0, 0.15, LANTERN), facade.medallion(0.15, 0.4, DARK),
            facade.medallion(0.4, 0.55, QUARTZ), facade.medallion(0.55, 0.7, PRISM)), under=POLISHED,
            name="medallion"),
        "star": marks.field(facade.first_of(facade.border(1, CHISELED), facade.border(2, DARK),
                                            facade.star(2.2, DARK)), under=QUARTZ, name="star"),
        "rings": marks.field(facade.first_of(facade.border(1, QUARTZ),
                                             facade.rings(1.5, [QUARTZ, DIORITE, DARK, DIORITE])), name="rings"),
        "grid": marks.field(facade.first_of(facade.border(1, CHISELED), facade.border(1, DARK, at=1),
                                            lambda c: PRISM if abs(c.u if c.hw >= c.hh else c.v) % 4 < 1
                                            and min(c.hw, c.hh) > 1 else None),
                            under=QUARTZ, name="grid"),
        "plain": marks.field(facade.border(1, CHISELED), under=QUARTZ, name="plain"),
        "flight": marks.flight(QUARTZ, B.QUARTZ_STAIRS, cheek=CHISELED),
    }
    return G.Style(
        "marble",
        body=body,
        faces={"edge": edge, "show": show, "flank": flank, "deck": deck_face},
        seam=CHISELED,
        fills=fills,
        choose=lambda sec, lot: ["grid"],
        params={"dye": dye, "deck_depth": 3, "pillar_every": 5},
        deck=deck,
        pillar=pillar)
