"""The grammar's showcase: one specimen plan spoken in five styles, side by side, and a gallery of the marks and
floor fields every style shares. No objectives and no match: it is a swatch book.

    python3 gen.py <build-dir>

    the specimen    a terrace at 28 with a show wall to the north, a ledge at 24, a flight of steps up to the terrace,
                    a loggia (a deck at 28 over a passage at 20, pillars under its open edges), a plaza at 20 cut into
                    six sections, a front court at 16 cut into four; every edge to the void a deep face
    the styles      Brittlebush and Claywork as their boards speak them, and Terra, Marble and Foundry, west to east;
                    each specimen's sections carry its own fills, an arrow up the flight, the team's word and a glyph
    the gallery     south of them, a floor of twenty-four sections, each a floor field or a mark in a frame, before a
                    wall that carries the alphabet, the digits and every glyph
"""
import os
import sys
from dataclasses import replace

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox import B, World, rng  # noqa: E402
from pgmvox.built import facade  # noqa: E402
from pgmvox.grammar import brittle, clay, foundry, marble, marks, terra  # noqa: E402
from pgmvox.grammar import rules as G  # noqa: E402

BOARD = "grammar-showcase"
WIDTH, DEPTH, GAP = 48, 46, 16                      # a specimen's footprint, and the void between two
RED = 14
TERRACE, LEDGE, PLAZA, FRONT = 28, 24, 20, 16


def _brittle():
    """Brittlebush's style with a deck: stone under the deck, the floor sand on sand, the pillar its dark oak."""
    from pgmvox.core.orient import stair

    def deck(w, x, z, h, floor):
        for y in range(h - 3, h):
            w.set(x, y, z, B.STONE)
        for y in range(floor + 1, h - 3):
            w.set(x, y, z, B.AIR)
        brittle.ground(w, x, z, floor)
        w.set(x, floor, z, B.SAND)

    def pillar(w, x, z, top, bottom, side):
        for n, y in enumerate(range(top, bottom - 1, -1)):
            w.set(x, y, z, *((B.PLANKS, 5) if n % 3 == 0 else (B.DARK_OAK_STAIRS, stair(G.OPP[side],
                                                                                            upside_down=n % 3 == 2))))
    return replace(brittle.STYLE, deck=deck, pillar=pillar, params={**brittle.STYLE.params, "deck_depth": 4},
                   fills={**brittle.STYLE.fills,
                          "flight": marks.flight((B.SLAB, 5), B.STONEBRICK_STAIRS)})


def _claywork():
    """Claywork's style with a deck of stone brick over its floor of smooth slab, and pillars of chiseled brick."""
    style = clay.style(dye=RED, rng=rng(BOARD, "claywork"))

    def deck(w, x, z, h, floor):
        for y in range(h - 3, h):
            w.set(x, y, z, *clay.BRICK)
        for y in range(floor + 1, h - 3):
            w.set(x, y, z, B.AIR)
        style.body(w, x, z, floor)
        w.set(x, floor, z, *clay.SMOOTH)

    def pillar(w, x, z, top, bottom, side):
        for y in range(bottom, top + 1):
            w.set(x, y, z, *((B.STONEBRICK, 3) if y in (bottom, top) else clay.BRICK))
    faces = {**style.faces, "deck": G.Face([clay.BRICK, clay.BRICK, clay.ANDESITE], floor=1)}
    return replace(style, faces=faces, deck=deck, pillar=pillar, params={**style.params, "deck_depth": 3})


# what each style lays where: the terrace's two halves, the ledge, the plaza's six, the front's four; a plaza
# section that carries a mark is laid in the style's calmest fill, so the mark reads
STYLES = [
    ("brittlebush", _brittle(), {"terrace": ["bed", "sand"], "ledge": ["sand"],
                                 "plaza": ["sand", "sand", "bed", "grass", "sand", "sand"],
                                 "front": ["bed", "sand", "sand", "bed"]}),
    ("claywork", _claywork(), {"terrace": ["squares", "inlay"], "ledge": ["paving"],
                               "plaza": ["plate", "plate", "inlay", "checker", "plate", "plate"],
                               "front": ["inlay", "squares", "checker", "paving"]}),
    ("terra", terra.style(dye=RED), {"terrace": ["kilim", "tiles"], "ledge": ["court"],
                                     "plaza": ["plain", "plain", "zigzag", "court", "plain", "plain"],
                                     "front": ["zigzag", "court", "tiles", "kilim"]}),
    ("marble", marble.style(dye=RED), {"terrace": ["medallion", "medallion"], "ledge": ["grid"],
                                       "plaza": ["plain", "plain", "rings", "star", "plain", "plain"],
                                       "front": ["rings", "grid", "grid", "medallion"]}),
    ("foundry", foundry.style(dye=RED), {"terrace": ["plates", "lanes"], "ledge": ["lanes"],
                                         "plaza": ["plain", "plain", "hazard", "sector", "plain", "plain"],
                                         "front": ["sector", "plates", "hazard", "sector"]}),
]
# the marks in each style's own block: the team's word and a glyph on the plaza, an arrow up toward the flight
MARK = {"brittlebush": (B.WOOL, RED), "claywork": (B.WOOL, RED), "terra": (B.STAINED_CLAY, 12),
        "marble": marble.DARK, "foundry": foundry.COAL}


def specimen(ox, oz, name, style, fills):
    """The specimen's sections at (ox, oz), its flight's tops and the columns its show wall stands on."""
    def box(x0, z0, x1, z1):
        return ox + x0, oz + z0, ox + x1, oz + z1

    def pick(key, i):
        f = fills[key][i % len(fills[key])]
        return f
    mark = MARK[name]
    secs = []
    for i, s in enumerate(G.split(box(0, 0, WIDTH - 1, 11), 2, 1, TERRACE, f"{name}-terrace")):
        secs.append(replace(s, fill=pick("terrace", i)))
    secs.append(G.Section((box(0, 12, 17, 19),), LEDGE, f"{name}-ledge", pick("ledge", 0)))
    x0, z0, x1, z1 = box(18, 12, 29, 19)
    tops = tuple(((x, z), TERRACE - (z - z0)) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1))
    secs.append(G.Section(((x0, z0, x1, z1),), PLAZA + 1, f"{name}-flight", style.fills["flight"], tops=tops))
    secs.append(G.Section((box(30, 12, WIDTH - 1, 19),), TERRACE, f"{name}-loggia", pick("terrace", 0),
                          tags=frozenset({f"under-{PLAZA}"})))
    plaza = G.split(box(0, 20, WIDTH - 1, 35), 3, 2, PLAZA, f"{name}-plaza")
    motifs = {f"{name}-plaza-0-0": (("arrow", (("d", "e"), ("block", mark))),),
              f"{name}-plaza-2-0": (("arrow", (("d", "w"), ("block", mark))),),
              f"{name}-plaza-0-1": (("word", (("text", "RED"), ("block", mark))),),
              f"{name}-plaza-2-1": (("glyph", (("name", "eye"), ("block", mark), ("up", "n"))),)}
    for i, s in enumerate(plaza):
        secs.append(replace(s, fill=pick("plaza", i), motifs=motifs.get(s.name, ())))
    for i, s in enumerate(G.split(box(0, 36, WIDTH - 1, DEPTH - 1), 4, 1, FRONT, f"{name}-front")):
        secs.append(replace(s, fill=pick("front", i)))
    show = {(x, oz) for x in range(ox, ox + WIDTH)}
    return secs, show


def gallery(ox, oz):
    """Twenty-four sections, eight by three, each a floor field or a mark in a frame of polished andesite, on smooth
    slab at 20; behind them a wall four deep and twelve high carrying the alphabet, the digits and the glyphs."""
    FRAME, FLOOR, INK = (B.STONE, 6), (B.DSLAB, 8), (B.STAINED_CLAY, 15)
    TEAM, GOLD, LIGHT = (B.WOOL, RED), (B.GOLD_BLOCK, 0), (B.SEA_LANTERN, 0)

    def framed(f):
        return marks.field(facade.first_of(facade.border(1, FRAME), f), under=FLOOR)

    def mark(kind, **params):
        def fill(w, lot, rng):
            framed(lambda c: None)(w, lot, rng)
            return marks.MOTIFS[kind](w, lot, rng, **params) or True
        return fill
    fields = [
        framed(facade.stripes(4, 2, INK)), framed(facade.stripes(4, 2, INK, axis="z")),
        framed(facade.diagonal(6, 3, TEAM)), framed(facade.chevrons(6, 2, TEAM, "n")),
        framed(facade.tiles(2, INK, FLOOR)), framed(facade.rings(1.5, [INK, FLOOR, TEAM, FLOOR])),
        framed(facade.rings(1, [INK, FLOOR], square=True)), framed(facade.star(4.2, GOLD)),
        framed(facade.first_of(facade.medallion(0, 0.25, LIGHT), facade.medallion(0.25, 0.55, TEAM),
                               facade.medallion(0.55, 0.7, INK))),
        framed(facade.first_of(facade.corners(4, TEAM, inset=4), facade.medallion(0, 0.3, INK))),
        framed(facade.cross(1.5, (B.PRISMARINE, 0))), framed(facade.diamonds(6, 2.2, INK)),
        framed(facade.kilim_steps(2, [INK, FLOOR, TEAM, FLOOR])),
        framed(facade.first_of(facade.border(2, TEAM, at=2), facade.border(1, INK, at=4))),
        mark("arrow", d="n", block=TEAM), mark("arrow", d="e", block=TEAM),
        mark("word", text="PGM", block=INK), mark("word", text="CTW", block=TEAM),
        mark("glyph", name="eye", block=INK), mark("glyph", name="key", block=INK),
        mark("glyph", name="sun", block=GOLD), mark("glyph", name="gate", block=INK),
        mark("glyph", name="cross", block=TEAM, scale=2), mark("word", text="7", block=INK, scale=2),
    ]
    secs = []
    for n, s in enumerate(G.split((ox, oz + 4, ox + 8 * 14 - 1, oz + 4 + 3 * 13 - 1), 8, 3, PLAZA, "gallery")):
        secs.append(replace(s, fill=fields[n]))
    secs.append(G.Section(((ox, oz, ox + 8 * 14 - 1, oz + 3),), PLAZA + 12, "gallery-wall", "flat"))
    wall = {(x, oz + 3) for x in range(ox, ox + 8 * 14)}
    return secs, wall


def gallery_style():
    """Plain stone for the gallery: smooth slab floors and a wall of smooth stone whose face carries every letter and
    glyph, inset in black clay."""
    INK = (B.STAINED_CLAY, 15)

    def body(w, x, z, h):
        for y in range(1, h):
            w.set(x, y, z, *(B.STONE, 0))
        w.set(x, 0, z, 36)
    letters = G.Face([(B.DSLAB, 8)] + [(B.STONE, 0)] * 12 + [(B.STONE, 6)], floor=1, pattern=(
        facade.word(7, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", INK),
        facade.glyph_row(1, list(facade.GLYPHS), INK, spacing=12),
        lambda s, run, t, h, n: ("accent", (B.STONE, 6)) if t in (0, 6, 13) else None))
    plain = G.Face([(B.DSLAB, 8)] + [(B.STONE, 0)] * 6 + [(B.STONE, 6)], floor=1)
    return G.Style("gallery", body=body, faces={"edge": plain, "letters": letters}, seam=(B.STONE, 6),
                   fills={"flat": marks.field(lambda c: (B.DSLAB, 8))}, choose=lambda sec, lot: ["flat"])


def main(build):
    r = rng(BOARD, "ground")
    span = len(STYLES) * WIDTH + (len(STYLES) - 1) * GAP
    w = World(-8, -8, span + 16, 130, sy=48)
    for k, (name, style, fills) in enumerate(STYLES):
        secs, show = specimen(k * (WIDTH + GAP), 0, name, style, fills)
        ground = G.Ground(secs)
        flight = {c for s in secs if s.name.endswith("flight") for c in s.columns()}

        def face_of(x, z, style=style, show=show, flight=flight):
            if (x, z) in show and "show" in style.faces:
                return "show"
            if (x, z) in flight and "flank" in style.faces:
                return "flank"
            return "edge"
        loggia = [n for n, s in enumerate(secs) if G.under(s) is not None]
        G.lay(w, ground, style, only=[n for n in range(len(secs)) if n not in loggia], rng=r, face_of=face_of)
        G.lay(w, ground, style, only=loggia, rng=r)
    secs, wall = gallery((span - 8 * 14) // 2, DEPTH + 24)
    G.lay(w, G.Ground(secs), gallery_style(), rng=r, face_of=lambda x, z: "letters" if (x, z) in wall else "edge")
    w.save(build, "Grammar Showcase", (0, 40, 0))
    import numpy as np
    print(f"saved: {int(np.count_nonzero(w.ids))} blocks")


if __name__ == "__main__":
    main(sys.argv[1])
