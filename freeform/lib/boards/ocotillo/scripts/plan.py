"""Ocotillo: a capture-the-wool board for four teams in the Brittlebush style, laid out as a blueprint of cells.

Every piece is made of cells five blocks a side, and a cell is one of a handful of pieces:

    flat      level ground at one of five levels, three blocks apart (7, 10, 13, 16, 19)
    stair     a ramp one cell long that climbs one level, three blocks in five, in half steps of a stone-brick
              slab and a stone-brick block in turn; every change of level is one of these
    stacked   a deck one level over an underfloor: the underfloor is covered ground a player walks under the deck
    keep      a team's spawn, flat at the top level
    tower     a team's wool room, a tower of narrow storeys on its yard
    gap       void a player may build over, marked by cobwebs on the floor of the void
    water     void with water at its foot, marked by cobwebs too
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
    objectives()    the four teams, their spawns and the four wools, each captured by the other three
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
import numpy as np  # noqa: E402

from pgmvox.objectives import Box, Objectives, Observer, Spawn, Teams, Wool  # noqa: E402
from pgmvox.plan import Raster  # noqa: E402

BOARD = "ocotillo"
CELL = 5
N = 13                                     # cells from a quadrant's outer corner to the middle
X_MIN, X_MAX = -N * CELL, N * CELL - 1     # -65 .. 64
Z_MIN, Z_MAX = X_MIN, X_MAX
LEVEL = {1: 7, 2: 10, 3: 13, 4: 16, 5: 19}  # a level's floor block
MAX_BUILD = 40

# red's quadrant, the cells on or above its diagonal, row b from the outer edge, a from the diagonal to the middle.
# fN flat at level N; kN a deck at N over an underfloor at N-1; KN the keep; TN the tower's yard floor;
# s< s> s^ sv a stair rising west, east, north (toward b 0) or south; ww a gap; ~~ water; .. void
QUADRANT = [
    # a: 0   1   2   3   4   5   6   7   8   9   10  11  12
    "K5 K5 K5 .. f4 f4 f4 .. .. .. .. f2 ww",          # b 0  the keep; the orchard; a post on the border
    "   K5 K5 s< f4 f4 f4 s< f3 f3 s< f2 ww",          # b 1  down the wing: orchard, the sand walk, the post
    "      K5 .. f4 f4 f4 .. ww ww .. f2 ww",          # b 2  a gap from the walk to the arbour
    "         .. .. s^ .. .. ww ww .. .. ..",          # b 3  down from the orchard into the tower's yard
    "            f3 f3 f3 k3 k3 k3 .. .. ..",          # b 4  the yard; the arbour, a deck over a covered walk
    "               T3 T3 k3 k3 k3 s> f4 ww",          # b 5  the tower; up from the arbour to the lookout
    "                  T3 k3 k3 k3 .. .. ..",          # b 6
    "                     .. f2 s^ .. .. ..",          # b 7  into the covered walk; up onto the deck
    "                        f2 f2 .. .. ..",          # b 8  the inner court
    "                           f2 f2 .. ..",          # b 9
    "                              f2 s< f1",          # b 10 down to a landing on the border
    "                                 ~~ sv",          # b 11 up from the landing onto the dais
    "                                    f2",          # b 12 the dais, a quarter of it
]
TEAMS = [("red-team", "Red", "red"), ("blue-team", "Blue", "blue"), ("green-team", "Green", "green"),
         ("yellow-team", "Yellow", "yellow")]
WOOLS = {"red-team": "pink", "blue-team": "light_blue", "green-team": "lime", "yellow-team": "orange"}
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
    # a stair climbs from the level of the cell on its low side
    for c, (kind, level, d, team) in list(out.items()):
        if kind == "stair":
            dx, dz = STEP[d]
            low = out.get((c[0] - dx, c[1] - dz))
            out[c] = (kind, low[1] if low and low[1] else None, d, team)
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
    """A team's tower, as its four cells."""
    out = []
    for a, b in ((5, 5), (6, 5), (5, 6), (6, 6)):
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


def objectives():
    """Four teams; each spawns in its keep and keeps its own wool in its tower, which the other three capture."""
    O = Objectives(Teams(*[t + (10,) for t in TEAMS]))
    for i, (team, *_) in enumerate(TEAMS):
        x, z = spawn_cell(i)
        box = keep_box(i)
        O.add(Spawn(team, (x, LEVEL[5] + 1, z), yaw=[315, 45, 135, 225][i], kit="spawn-kit",
                    area=Box(box[0], 0, box[1], box[2], 127, box[3]), protect=True), mirror=False)
    for i, (keeper, *_) in enumerate(TEAMS):
        x0, z0, x1, z1 = tower_box(i)
        cx, cz = (x0 + x1) // 2, (z0 + z1) // 2
        for j, (taker, *_) in enumerate(TEAMS):
            if taker == keeper:
                continue
            sx, sz = spawn_cell(j)
            O.add(Wool(taker, WOOLS[keeper], slot=(sx + [-3, 0, 3][(j - i) % 4 - 1], LEVEL[5] + 1, sz + 3),
                       found=(cx, LEVEL[3] + 1, cz), room=Box(x0, LEVEL[3] + 1, z0, x1, LEVEL[3] + 6, z1)),
                  mirror=False)
    O.add(Observer((0, 40, 0)), mirror=False)
    return O
