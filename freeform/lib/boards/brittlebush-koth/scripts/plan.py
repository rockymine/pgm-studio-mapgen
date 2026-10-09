"""Brittlebush KotH: a king-of-the-hill board for four teams in the Brittlebush style, laid out as a blueprint of cells.

Five hills: the dais in the middle, and one on each border, on the island between two neighbouring spawns. Each
team spawns in its keep with sixteen leaves to bridge with, and takes a leaf and a golden apple for every kill;
golden apples also grow on the four inner islands, reached by bridging, and arrows on the four landings by the
middle.

Every piece is made of cells five blocks a side, and a cell is one of a handful of pieces:

    flat      level ground at one of six levels, three blocks apart (7, 10, 13, 16, 19, 22)
    stair     a ramp one cell long that climbs one level, three blocks in five, in half steps of a stone-brick
              slab and a stone-brick block in turn; every change of level is one of these
    keep      a team's spawn, flat at the top level
    gap       void a player may build over, cobwebs on the floor of the void where it meets the open void
    water     void with water at its foot, which marks it: no cobwebs
    void      nothing

No flat piece runs more than three cells, fifteen blocks, before a stair or a gap. A piece one cell wide is laid
in sand; a piece with two cells by two in it is laid with the sandstone, birch and grass inlay, and may carry a
tree. Cacti and dead bushes stand only on sand.

The board is four quadrants, one a team, each its neighbour turned a quarter about the middle; and each quadrant is
its own mirror across its diagonal, so a team's two neighbours meet it the same way. QUADRANT draws red's, the
north-west, from the corner (a 0, b 0) to the middle (a 12, b 12): only the cells on or above the diagonal
(a >= b), the rest being their mirror.

    plan()          the raster: every block's floor and kind, the underfloors as the base and decks as storey 1
    cells()         the blueprint itself: {(cx, cz): (kind, level, rises, team)}
    objectives()    the four teams, their spawns and the five hills
    APPLES, ARROWS  where the golden apples and the arrows grow
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
import numpy as np  # noqa: E402

from pgmvox.objectives import Box, Hill, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.plan import Raster  # noqa: E402

BOARD = "brittlebush-koth"
CELL = 5
N = 13                                     # cells from a quadrant's outer corner to the middle
X_MIN, X_MAX = -N * CELL, N * CELL - 1     # -65 .. 64
Z_MIN, Z_MAX = X_MIN, X_MAX
LEVEL = {0: 7, 1: 10, 2: 13, 3: 16, 4: 19, 5: 22}  # a level's floor block
MAX_BUILD = 44

# red's quadrant, the cells on or above its diagonal, row b from the outer edge, a from the diagonal to the middle.
# fN flat at level N; KN the keep;
# s< s> s^ sv a stair rising west, east, north (toward b 0) or south; ww a gap; ~~ water; .. void
QUADRANT = [
    # a: 0   1   2   3   4   5   6   7   8   9   10  11  12
    "K5 K5 K5 .. f4 f4 f4 .. f3 f3 f3 ww f2",          # b 0  the keep; the orchard; the terrace; a border hill
    "   K5 K5 s< f4 f4 f4 s< f3 f3 f3 s< f2",          # b 1  two cells of stair down out of the keep, and on, to
    "      K5 s< f4 f4 f4 s< f3 f3 f3 s< f2",          # b 2  the island and its hill between red and blue
    "         .. s^ s^ .. .. .. .. .. .. ..",          # b 3  down from the orchard into the yard
    "            f3 f3 f3 s< f2 f2 f2 ww f2",          # b 4  the yard; down to the arbour; an inner island, apples
    "               f3 f3 s< f2 f2 f2 ww f2",          # b 5
    "                  ~~ ~~ f2 f2 f2 ww f2",          # b 6  the pond between the yard and the arbours
    "                     ~~ .. s^ s^ .. ..",          # b 7  up from the inner court onto the arbour
    "                        f1 f1 f1 .. ..",          # b 8  the inner court
    "                           f1 f1 s< f0",          # b 9  down to a landing on the border, its arrows
    "                              f1 s< f0",          # b 10
    "                                 ~~ sv",          # b 11 up from the landing onto the dais
    "                                    f1",          # b 12 the dais, a quarter of it: the middle hill
]
TEAMS = [("red-team", "Red", "red"), ("blue-team", "Blue", "blue"), ("green-team", "Green", "green"),
         ("yellow-team", "Yellow", "yellow")]
NAMES = {"keep": "the Keep", "tower": "the Tower"}
FLIP = {"<": "^", "^": "<", ">": "v", "v": ">"}            # across the diagonal (a, b) -> (b, a)
TURN = {"^": ">", ">": "v", "v": "<", "<": "^"}            # a quarter turn clockwise: north becomes east
STEP = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}


def _quadrant():
    """Red's quadrant in full: {(a, b): token}."""
    q = {}
    for b, row in enumerate(QUADRANT):
        toks = row.split()
        assert len(toks) == N - b, f"row b {b} has {len(toks)} cells, not {N - b}"
        for j, t in enumerate(toks):
            a = b + j
            q[(a, b)] = t
            if a != b:
                q[(b, a)] = ("s" + FLIP[t[1]]) if t[0] == "s" else t
    return q


def turn_cell(cx, cz, d=None):
    """A cell and a direction a quarter turn clockwise about the middle: (x, z) -> (-1 - z, x) in blocks."""
    return (-1 - cz, cx), (TURN[d] if d else None)


def cells():
    """The blueprint: {(cx, cz): (kind, level, rises, team)}, cx and cz in cells, -13 .. 12. A stair's level is
    the level it climbs from; rises is the side it climbs toward."""
    out = {}
    kinds = {"K": "keep", "T": "tower", "f": "flat", "k": "stacked", "s": "stair", "w": "gap", "~": "water",
             ".": "void"}
    for (a, b), t in _quadrant().items():
        kind = kinds[t[0]]
        level = int(t[1]) if t[1].isdigit() else None
        rises = t[1] if kind == "stair" else None
        c, d = (a - N, b - N), rises
        for team, *_ in TEAMS:
            out[c] = (kind, level, d, team)
            c, d = turn_cell(*c, d)
    # a stair climbs one level to the cell on its high side, from the cell on its low side (a stacked cell's
    # underfloor, when the stair runs down under its deck)
    for c, (kind, level, d, team) in list(out.items()):
        if kind == "stair":
            dx, dz = STEP[d]
            high = out.get((c[0] + dx, c[1] + dz))
            out[c] = (kind, high[1] - 1 if high and high[1] else None, d, team)
    return out


def cell_box(cx, cz):
    return cx * CELL, cz * CELL, cx * CELL + CELL - 1, cz * CELL + CELL - 1


KINDS = ["void", "gap", "water", "sand", "inlay", "stair", "under", "deck", "keep", "tower"]
COLOURS = {"void": (34, 38, 52), "gap": (70, 66, 60), "water": (60, 110, 190), "sand": (226, 208, 150),
           "inlay": (150, 175, 105), "stair": (150, 150, 155), "under": (120, 95, 70), "deck": (140, 100, 60),
           "keep": (210, 190, 160), "tower": (40, 34, 30)}
WALK_KINDS = {"sand", "inlay", "stair", "under", "deck", "keep", "tower"}


def themes(C):
    """Each flat cell's theme: 'inlay' if its piece (the flat cells joined to it at its level) holds two cells by
    two, else 'sand'."""
    flat = {c for c, v in C.items() if v[0] == "flat"}
    seen, theme = set(), {}
    for c in flat:
        if c in seen:
            continue
        comp, todo = set(), [c]
        while todo:
            p = todo.pop()
            if p in comp or p not in flat or C[p][1] != C[c][1]:
                continue
            comp.add(p)
            todo += [(p[0] + 1, p[1]), (p[0] - 1, p[1]), (p[0], p[1] + 1), (p[0], p[1] - 1)]
        seen |= comp
        square = any({(x, z), (x + 1, z), (x, z + 1), (x + 1, z + 1)} <= comp for x, z in comp)
        for p in comp:
            theme[p] = "inlay" if square else "sand"
    return theme


def plan():
    """The raster. A stacked cell's underfloor is the base raster and its deck is storey 1; a stair's rows climb
    a block every two rows (the half steps rounded down), so the plan walk climbs it as a player does."""
    C = cells()
    T = themes(C)
    R = Raster((X_MIN, X_MAX), (Z_MIN, Z_MAX), KINDS, base_h=0, base_kind="void")
    up = R.storey(1)
    for (cx, cz), (kind, level, d, team) in C.items():
        x0, z0, x1, z1 = cell_box(cx, cz)
        if kind in ("void", "gap", "water"):
            R.rect(x0, x1, z0, z1, 0, kind)
            continue
        if kind == "stair":
            lo = LEVEL[level]
            dx, dz = STEP[d]
            for x in range(x0, x1 + 1):
                for z in range(z0, z1 + 1):
                    r = (x - x0) if dx > 0 else (x1 - x) if dx < 0 else (z - z0) if dz > 0 else (z1 - z)
                    R.cell(x, z, lo + 1 + r // 2 if r < 4 else lo + 3, "stair")   # 4 rows of half steps, a top row
            continue
        h = LEVEL[level]
        if kind == "stacked":
            R.rect(x0, x1, z0, z1, LEVEL[level - 1], "under")
            for x in range(x0, x1 + 1):
                for z in range(z0, z1 + 1):
                    up.cell(x, z, h, "deck")
            continue
        R.rect(x0, x1, z0, z1, h, {"flat": T.get((cx, cz), "sand")}.get(kind, kind))
    R.cells = C
    R.themes = T
    return R


def mask(R, kind):
    return R.mask(kind)


def spawn_cell(team_index):
    """The middle of a team's keep, in blocks: red's is cell (1, 1) of its quadrant, the others its turns."""
    c = (1 - N, 1 - N)
    for _ in range(team_index):
        c, _ = turn_cell(*c)
    x0, z0, _, _ = cell_box(*c)
    return x0 + 2, z0 + 2


def tower_cells(team_index):
    """A team's tower, its landmark, as its four cells."""
    out = []
    for a, b in ((6, 6), (7, 6), (6, 7), (7, 7)):
        c = (a - N, b - N)
        for _ in range(team_index):
            c, _ = turn_cell(*c)
        out.append(c)
    return out


def keep_cells(team_index):
    """A team's keep, as its nine cells."""
    out = []
    for a in range(3):
        for b in range(3):
            c = (a - N, b - N)
            for _ in range(team_index):
                c, _ = turn_cell(*c)
            out.append(c)
    return out


def keep_box(team_index):
    return _box(keep_cells(team_index))


def _box(cs):
    xs, zs = [], []
    for c in cs:
        x0, z0, x1, z1 = cell_box(*c)
        xs += [x0, x1]
        zs += [z0, z1]
    return min(xs), min(zs), max(xs), max(zs)


def tower_box(team_index):
    return _box(tower_cells(team_index))


def _turned_box(box, k):
    """A box (x0, z0, x1, z1) in blocks, turned k quarters clockwise about the middle."""
    x0, z0, x1, z1 = box
    for _ in range(k):
        x0, z0, x1, z1 = -1 - z1, x0, -1 - z0, x1
    return x0, z0, x1, z1


def _turned_point(x, z, k):
    for _ in range(k):
        x, z = -1 - z, x
    return x, z


# the hills, square pads on the floor: the dais at 7, and the island at 10 between red's and blue's spawns turned to
# the other three borders; the order of the border hills follows the teams (north, east, south, west)
HILL_Y = LEVEL[2]                          # the border hills' floor; the Dais stands at LEVEL[1]
CENTRE_HILL = (-5, -5, 4, 4)
BORDER_HILL = (-5, -63, 4, -54)
HILLS = [("centre", "the Dais", CENTRE_HILL, 2, LEVEL[1])] + \
        [(f"{side}", f"the {side.title()} Island", _turned_box(BORDER_HILL, k), 1, HILL_Y)
         for k, side in enumerate(("north", "east", "south", "west"))]
# what grows where: golden apples on the inner islands, arrows on the landings, each between two neighbours
APPLES = [_turned_point(-0.5, -38, k) for k in range(4)]
ARROWS = [_turned_point(-0.5, -15.5, k) for k in range(4)]


def objectives():
    """Four teams, each spawning in its keep and facing the middle; the five hills, the dais worth two."""
    O = Objectives(Teams(*[t + (10,) for t in TEAMS]))
    for i, (team, *_) in enumerate(TEAMS):
        x, z = spawn_cell(i)
        box = keep_box(i)
        O.add(Spawn(team, (x, LEVEL[5] + 1, z), yaw=[315, 45, 135, 225][i], kit="spawn-kit",
                    area=Box(box[0], 0, box[1], box[2], 127, box[3]), protect=True), mirror=False)
    for hid, name, (x0, z0, x1, z1), points, y in HILLS:
        O.add(Hill(hid, name, Box(x0, y, z0, x1, y, z1), points=points, capture_time="5s"), mirror=False)
    O.add(Observer((0, 40, 0)), mirror=False)
    return O
