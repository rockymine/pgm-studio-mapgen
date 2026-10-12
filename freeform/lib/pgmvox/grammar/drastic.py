"""The Drastic style for pgmvox.grammar.rules, read off CommunityMaps ctw/drastic_change_ii: white quartz faces under
a nether-brick rim, a groove in the side's colour, portholes ringed in stairs, and meadows inside a quartz kerb
streaked with chiseled quartz.

    STYLE = drastic.style(dye=14)       # dye: the side's colour, in the groove and the body's foot

    the body        andesite, two courses of the side's clay at its foot, block 36 at y 0
    the edge        an upside-down nether-brick stair at the rim, chiseled quartz, a groove sunk into the side's
                    colour, a quartz slab, quartz, an upside-down quartz stair for a cove, a nether-brick slab; every
                    third bay of five a porthole: a ring of quartz stairs round three of dark hole
    the outline     nether brick
    the fills       meadow (a quartz kerb; grass streaked on the diagonal with chiseled quartz, birch-leaf bushes,
                    grass and orchids), court (quartz, chiseled at its ring)
    the deck        quartz over nether brick, four of air, the floor quartz
    the pillar      pillar quartz, its ends chiseled
"""
from pgmvox.core.blocks import B
from pgmvox.core.orient import stair
from pgmvox.grammar import marks
from pgmvox.grammar import rules as G

QZ, CHIS, PILLAR, QZ_SLAB = (B.QUARTZ, 0), (B.QUARTZ, 1), (B.QUARTZ, 2), (B.SLAB, 7)
NB, NB_SLAB, ANDESITE = (B.NETHER_BRICK, 0), (B.SLAB, 6), (B.STONE, 5)
BAY = 5
LEFT = {"n": "e", "s": "w", "e": "s", "w": "n"}       # a face's left end, seen from outside, by its inward side


def _rim(inward):
    return B.NETHER_STAIRS, stair(inward, upside_down=True)


def _cove(inward):
    return B.QUARTZ_STAIRS, stair(inward, upside_down=True)


def _toward(end, upside_down):
    """A quartz stair in the face, solid toward the bay's `end` ("lo" or "hi")."""
    def f(inward):
        lo = {"n": "w", "s": "w", "e": "n", "w": "n"}[inward]
        return B.QUARTZ_STAIRS, stair(lo if end == "lo" else G.OPP[lo], upside_down=upside_down)
    return f


def style(dye=14):
    """Drastic's blocks for the grammar; `dye` is the side's colour."""
    side = (B.STAINED_CLAY, dye)

    def body(w, x, z, h):
        for y in range(3, h):
            w.set(x, y, z, *ANDESITE)
        for y in range(1, min(3, h)):
            w.set(x, y, z, *side)
        w.set(x, 0, z, 36)

    hole = G.Sunk(NB)
    plain = [_rim, CHIS, G.Sunk(side), QZ_SLAB, QZ, _cove, NB_SLAB]
    frame = [_rim, CHIS, NB, QZ, QZ, NB, NB_SLAB]

    def porthole(pos):
        """Three wide: stairs at its four corners, quartz at the middle of its top and foot, dark hole inside."""
        if pos == 2:
            return [_rim, CHIS, QZ, hole, hole, QZ, NB_SLAB]
        end = "lo" if pos == 1 else "hi"
        return [_rim, CHIS, _toward(end, True), hole, hole, _toward(end, False), NB_SLAB]

    edge = G.Face(plain, G.Accent(BAY, frame=frame, inner=porthole, every=3, min_air=7), floor=1)
    deck_face = G.Face([_rim, CHIS, NB], floor=1)

    def deck(w, x, z, h, floor):
        w.set(x, h - 1, z, *QZ)
        w.set(x, h - 2, z, *NB)
        for y in range(floor + 1, h - 2):
            w.set(x, y, z, B.AIR)
        body(w, x, z, floor)
        w.set(x, floor, z, *QZ)

    def pillar(w, x, z, top, bottom, s):
        for y in range(bottom, top + 1):
            w.set(x, y, z, *(CHIS if y in (bottom, top) else PILLAR))

    def meadow(w, lot, rng):
        x0, z0, x1, z1 = lot.box
        for x, z in lot.cols:
            ring = min(x - x0, x1 - x, z - z0, z1 - z)
            if ring == 0:
                w.set(x, lot.y, z, *QZ)
                continue
            streak = (x - z) % 6 in (0, 1) and (x + z) // 3 % 3 == 0
            if streak:
                w.set(x, lot.y, z, *CHIS)
                continue
            w.set(x, lot.y, z, B.GRASS)
            c = rng.random()
            if c < 0.07:
                w.set(x, lot.y + 1, z, B.LEAVES, 2 | 4)
            elif c < 0.25:
                w.set(x, lot.y + 1, z, B.TALLGRASS, 1)
            elif c < 0.28:
                w.set(x, lot.y + 1, z, B.FLOWER, 1)
        return True

    fills = {"meadow": meadow,
             "court": marks.field(lambda c: CHIS if c.edge == 0 else None, under=QZ, name="court"),
             "flight": marks.flight(QZ, B.QUARTZ_STAIRS, cheek=NB)}
    return G.Style("drastic", body=body, faces={"edge": edge, "deck": deck_face}, seam=NB, fills=fills,
                   choose=lambda sec, lot: ["meadow"], params={"dye": dye, "deck_depth": 3, "pillar_every": 6},
                   deck=deck, pillar=pillar)
