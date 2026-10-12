"""The Foundry style for pgmvox.grammar.rules: nether brick and stone brick, iron and coal, hazard bands, light
behind grilles.

    STYLE = foundry.style(dye=14)
    grammar.lay(w, ground, STYLE, face_of=...)

    the body        stone brick with cracked ones through it, a course of coal under the floor's four, bedrock to y 1,
                    block 36 at y 0
    the edge        nine courses: an upside-down nether-brick stair at the rim, nether brick, coal, stone brick, a
                    hazard band two courses high of yellow and black clay on the diagonal, stone brick, nether brick
                    at the foot; every other bay of five, two iron columns over a grille of bars lit by glowstone
                    behind it
    the show face   fourteen courses of stone brick, a word sunk in coal, slits of black glass and the hazard band
    the outline     the smooth double slab
    the fills       hazard (a border of yellow and black on the diagonal round smooth slab), plates (squares of
                    polished andesite seamed in stone brick), lanes (stripes of smooth slab and andesite along the
                    section's long side), sector (the section's number in coal on smooth slab, twice the size where it fits), plain
                    (smooth slab in andesite, under a mark)
    the flight      stone-brick stairs between cheeks of iron
    the deck        a girder of three courses, nether brick over iron, over five of air; the floor under it polished
                    andesite
    the pillar      nether brick on a chiseled stone-brick base, a capital of iron
"""
from pgmvox.built import facade
from pgmvox.core.blocks import B
from pgmvox.core.orient import stair
from pgmvox.grammar import marks
from pgmvox.grammar import rules as G

NETHER, SBRICK, CRACKED, CHISELED = (B.NETHER_BRICK, 0), (B.STONEBRICK, 0), (B.STONEBRICK, 2), (B.STONEBRICK, 3)
COAL, IRON, SMOOTH, ANDESITE = (B.COAL_BLOCK, 0), (B.IRON_BLOCK, 0), (B.DSLAB, 8), (B.STONE, 6)
YELLOW, BLACK = (B.STAINED_CLAY, 4), (B.STAINED_CLAY, 15)
BARS, GLOW = (B.IRON_BARS, 0), (B.GLOWSTONE, 0)
BAY = 5                                            # a column, a grille three wide, a column


def _rim(inward):
    return B.NETHER_STAIRS, stair(inward, upside_down=True)


def hazard(t0, t1, period=4):
    """A face pattern: yellow and black on the diagonal from course t0 to t1."""
    return lambda s, run, t, h, n: ("accent", YELLOW if (s + t) % period < period // 2 else BLACK) \
        if t0 <= t <= t1 else None


def style(dye=14):
    """Foundry's blocks for the grammar; `dye` is the team's colour, worn by its marks."""
    def body(w, x, z, h):
        for y in range(max(1, h - 4), h):
            w.set(x, y, z, *(CRACKED if (x * 7 + y * 3 + z * 5) % 11 == 0 else SBRICK))
        if h - 5 >= 1:
            w.set(x, h - 5, z, *COAL)
        for y in range(1, h - 5):
            w.set(x, y, z, B.BEDROCK)
        w.set(x, 0, z, 36)

    plain = [_rim, NETHER, COAL, SBRICK, None, None, SBRICK, CRACKED, NETHER]
    column = [_rim, IRON, IRON, IRON, IRON, IRON, IRON, IRON, NETHER]
    grille = [_rim, NETHER, COAL, G.Course(BARS, back=GLOW), G.Course(BARS, back=GLOW), G.Course(BARS, back=GLOW),
              G.Course(BARS, back=GLOW), SBRICK, NETHER]

    edge = G.Face(plain, G.Accent(BAY, frame=column, inner=grille, every=2, min_air=9), floor=1,
                  pattern=(hazard(3, 4),))
    show = G.Face([_rim, NETHER, COAL] + [SBRICK] * 11, floor=1, pattern=(
        facade.word(5, "FOUNDRY", COAL), hazard(1, 2), facade.slits(6, 5, 9),
        lambda s, run, t, h, n: ("accent", NETHER) if t in (0, 11) else None))
    flank = G.Face(plain, floor=1, pattern=(hazard(3, 4),))
    deck_face = G.Face([_rim, NETHER, IRON], floor=1)

    def deck(w, x, z, h, floor):
        w.set(x, h - 1, z, *NETHER)
        w.set(x, h - 2, z, *IRON)
        for y in range(floor + 1, h - 2):
            w.set(x, y, z, B.AIR)
        body(w, x, z, floor)
        w.set(x, floor, z, *ANDESITE)

    def pillar(w, x, z, top, bottom, side):
        for y in range(bottom, top + 1):
            w.set(x, y, z, *(CHISELED if y == bottom else IRON if y == top else NETHER))

    def sector(w, lot, rng):
        marks.field(lambda c: None, under=SMOOTH)(w, lot, rng)
        n = str(1 + lot.index % 9)
        return marks.word(w, lot, rng, n, COAL, scale=2) or marks.word(w, lot, rng, n, COAL) or True

    fills = {
        "hazard": marks.field(facade.first_of(lambda c: (YELLOW if (c.x + c.z) % 4 < 2 else BLACK)
                                              if c.edge < 2 else None), under=SMOOTH, name="hazard"),
        "plates": marks.field(lambda c: SBRICK if (c.x - c.x0) % 5 == 0 or (c.z - c.z0) % 5 == 0 else ANDESITE,
                              name="plates"),
        "lanes": marks.field(lambda c: (SMOOTH if (c.x - c.x0 if c.hw < c.hh else c.z - c.z0) % 3 else ANDESITE),
                             name="lanes"),
        "sector": sector,
        "plain": marks.field(facade.border(1, ANDESITE), under=SMOOTH, name="plain"),
        "flight": marks.flight(SBRICK, B.STONEBRICK_STAIRS, cheek=IRON),
    }
    return G.Style(
        "foundry",
        body=body,
        faces={"edge": edge, "show": show, "flank": flank, "deck": deck_face},
        seam=SMOOTH,
        fills=fills,
        choose=lambda sec, lot: ["plates"],
        params={"dye": dye, "deck_depth": 3, "pillar_every": 6},
        deck=deck,
        pillar=pillar)
