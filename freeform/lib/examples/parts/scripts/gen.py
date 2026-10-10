"""The parts: every building and pattern piece the library has, laid out on one flat yard to be looked at.

    row 1   one house in each of the four styles, at headings 0, 20, 45 and 90
    row 2   the six roof forms over the same walls
    row 3   a patterned mass (flutes, a glyph row, a word, courses, a parapet, a coffered underside) and three
            carpets (medallion, runner, star)
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox import B, World  # noqa: E402
from pgmvox import build as BLD  # noqa: E402
from pgmvox import facade as F  # noqa: E402
from pgmvox.shapes import rect_cells  # noqa: E402

FLOOR = 10
w = World(-12, -12, 112, 92, sy=48)
w.fill(-12, 0, -12, 99, FLOOR, 79, B.STONE)
w.fill(-12, FLOOR, -12, 99, FLOOR, 79, B.GRASS)

# row 1: the styles at four headings
for k, (style, heading) in enumerate((("town", 0), ("plaster", 20), ("brick", 45), ("stone", 90))):
    BLD.house(w, BLD.House(8 + 24 * k, 8, heading, L=11, W=7, floor=FLOOR, storeys=2, style=style,
                           jetty=style == "plaster"))

# row 2: the six roof forms, one storey, the studio's formulas
for k, form in enumerate(BLD.FORMS):
    BLD.house(w, BLD.House(6 + 16 * k, 32, 0, L=10, W=8, floor=FLOOR, storeys=1, style="town", roof=form,
                           chimney=False))

# row 3: a patterned mass held up on four piers, coffered underneath
mass = rect_cells(0, 50, 25, 61)
for x, z in ((2, 52), (22, 52), (2, 58), (22, 58)):
    F.extrude(w, rect_cells(x, z, x + 1, z + 1), FLOOR + 1, FLOOR + 6, base=F.DARK)
F.extrude(w, mass, FLOOR + 7, FLOOR + 26, base=F.concrete(5), faces_=[
    F.word(14, "PARTS", F.DARK),
    F.glyph_row(7, ["eye", "key", "sun", "gate"], F.DARK),
    F.flutes(3, 1, 1, 5),
    F.courses(5, F.DARK),
], top="parapet-slotted", bottom="coffer")

# and three carpets
WOOL = {c: (B.WOOL, d) for c, d in (("white", 0), ("orange", 1), ("magenta", 2), ("light_blue", 3), ("yellow", 4),
                                    ("lime", 5), ("pink", 6), ("cyan", 9), ("purple", 10), ("blue", 11),
                                    ("brown", 12), ("green", 13), ("red", 14), ("black", 15))}
F.carpet(w, 32, 48, 52, 64, FLOOR, F.first_of(
    F.border(1, WOOL["black"]), F.border(0, WOOL["yellow"], at=2), F.border(4, WOOL["blue"]),
    F.medallion(0.18, 0.28, WOOL["yellow"]), F.medallion(0, 0.18, WOOL["orange"]),
    F.medallion(0.28, 0.36, WOOL["blue"]), F.corners(4, WOOL["yellow"]), default=WOOL["red"]))
F.carpet(w, 58, 44, 66, 68, FLOOR, F.first_of(
    F.border(1, WOOL["brown"]), F.border(3, WOOL["orange"]), F.diamonds(10, 1.5, WOOL["cyan"]),
    F.diamonds(10, 3, WOOL["light_blue"]), F.diamonds(10, 4, WOOL["orange"]), default=WOOL["blue"]))
F.carpet(w, 72, 46, 92, 66, FLOOR, F.first_of(
    F.border(1, WOOL["black"]), F.border(0, WOOL["magenta"], at=2), F.border(4, WOOL["purple"]),
    F.star(4, WOOL["yellow"]), F.star(6, WOOL["white"]), F.cross(0.6, WOOL["light_blue"]), default=WOOL["blue"]))

w.save(sys.argv[1], "Parts", (40, FLOOR + 1, 40))
print("generated")
