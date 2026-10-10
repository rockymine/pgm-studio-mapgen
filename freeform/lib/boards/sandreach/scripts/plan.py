"""Sandreach: capture the wool for two teams of twelve, one wool each, on a board that is made and grown at once.

The made ground is Brittlebush's grammar on a grid of five-block cells: a plaza in the middle, neutral and parted
from both sides by a cell of build zone, a lane climbing by stair cells to each spawn's yard and its house, a spine
west to the wool's terrace and its house, a landing under the terrace toward the middle. The grown ground is terrain
painted by its slope: a meadow hillside east of each spawn, falling away south into hanging rock, and a floating
island off each wool's approach. The two meet as the author's ruling has them meet: the made ground is cut out of
the grown and they meet at a made face, dressed; the height between them is a stair cell set into a notch of the
yard, never a graded slope.

The board is red's half (z < 0) turned a half turn about the middle for blue's (x, z) -> (-1 - x, -1 - z).

    cells()         the made blueprint, both halves: ({cell: Cell}, {cell: 0 red, 1 blue})
    meadow(), island()      the grown ground, red's: (mask, heights) over the world's grid
    objectives()    two teams; each keeps one wool in its house and takes the other's to its monument, and
                    keeps an emerald monument on its meadow that the other team destroys
"""
import os
import sys
from dataclasses import replace

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
import numpy as np  # noqa: E402

from pgmvox import brittle as BR  # noqa: E402
from pgmvox import B, noise  # noqa: E402
from pgmvox.objectives import Box, Destroyable, Objectives, Observer, Spawn, Teams, Wool  # noqa: E402
from pgmvox.plan import Symmetry  # noqa: E402

BOARD = "sandreach"
SYM = Symmetry("rot_180")
CELL = BR.CELL
X_MIN, X_MAX = -75, 74                     # 150 by 200: the void round the land is the world's edge
Z_MIN, Z_MAX = -100, 99
PLAZA, LANE, YARD, WOOL = 12, 15, 18, 21   # the made levels, three apart
MAX_BUILD = 40
TEAMS = [("red-team", "Red", "red", 12), ("blue-team", "Blue", "blue", 12)]
DYES = [14, 11]


def _rect(out, cx0, cx1, cz0, cz1, kind, y, section, **kw):
    for cx in range(cx0, cx1 + 1):
        for cz in range(cz0, cz1 + 1):
            out[(cx, cz)] = BR.Cell(kind, y, section=section, name=section, **kw)


def unit():
    """Red's made cells: (cx, cz) -> Cell, every section a rectangle."""
    u = {}
    # the plaza in the middle, red's half of it: three sections two cells by three
    _rect(u, -3, -2, -3, -1, "flat", PLAZA, "plaza-w")
    _rect(u, -1, 0, -3, -1, "flat", PLAZA, "plaza-m")
    _rect(u, 1, 2, -3, -1, "flat", PLAZA, "plaza-e")
    # the plaza is neutral ground: a cell of build zone parts it from each team's lane, three blocks up, so the
    # middle is reached by building and the far side by building again. Up from the lane: a stair, the yard
    _rect(u, -2, -1, -8, -5, "flat", LANE, "lane-w")
    _rect(u, 0, 1, -8, -5, "flat", LANE, "lane-e")
    _rect(u, -1, 0, -9, -9, "stair", LANE, "stair", rises="n")
    _rect(u, -3, -2, -12, -10, "flat", YARD, "yard-sw")
    _rect(u, -1, 0, -12, -10, "flat", YARD, "yard-s")
    _rect(u, 1, 2, -12, -10, "flat", YARD, "yard-se")
    _rect(u, -3, -2, -14, -13, "flat", YARD, "yard-nw")
    _rect(u, 1, 2, -14, -13, "flat", YARD, "yard-ne")
    _rect(u, -1, 0, -14, -13, "keep", YARD, "keep")
    # a notch in the yard's east face, and a stair down it onto the meadow: the made meets the grown at a flight
    _rect(u, 3, 3, -12, -12, "stair", LANE, "stair", rises="w")
    # west: the spine, a stair up to the wool's terrace, the wool's house and the bar before it
    _rect(u, -6, -4, -12, -10, "flat", YARD, "spine")
    _rect(u, -7, -7, -12, -11, "stair", YARD, "stair", rises="w")
    _rect(u, -11, -10, -15, -14, "flat", WOOL, "wool")
    _rect(u, -11, -10, -13, -13, "flat", WOOL, "wool-front")
    _rect(u, -9, -8, -15, -13, "flat", WOOL, "terrace-n")
    _rect(u, -11, -8, -12, -11, "flat", WOOL, "terrace-s")
    # under the terrace, toward the middle: a stair down to the landing, the attackers' way in
    _rect(u, -9, -8, -10, -10, "stair", YARD, "stair", rises="n")
    _rect(u, -11, -8, -9, -8, "flat", YARD, "landing")
    # the build zones: every void cell in the band across the middle, and round the island off the landing
    for cx in range(-13, 13):
        for cz in range(-7, 0):
            if (cx, cz) not in u:
                u[(cx, cz)] = BR.Cell("gap")
    for cx in range(-13, -6):
        for cz in range(-8, -7):
            if (cx, cz) not in u:
                u[(cx, cz)] = BR.Cell("gap")
    return u


def cells():
    """Both halves: red's unit and its half turn, blue's sections named apart so no section crosses the middle."""
    u = unit()
    out, team = dict(u), {c: 0 for c in u}
    for c, v in BR.turn_cells(u, 2).items():
        if c not in out:
            out[c] = replace(v, section=v.section + "'") if v.section else v
            team[c] = 1
    return out, team


# how a rectangle is filled where the shape rule would not choose: the middle and the corridors open grass, a birch
# only in the yard's back corners, to the outside of the spawn
FILL = {"plaza-w": "grass", "plaza-m": "sand", "plaza-e": "grass", "lane-w": "grass", "lane-e": "sand",
        "yard-sw": "grass", "yard-s": "sand", "yard-se": "grass", "spine": "grass", "landing": "sand",
        "terrace-s": "grass", "terrace-n": "sand", "wool-front": "sand"}


def fill(piece, cs):
    s = (cs[piece[0]].section or "").rstrip("'")
    return FILL.get(s)


# ---- the grown ground, red's -------------------------------------------------------------------------------
def grid():
    xs = np.arange(X_MIN, X_MAX + 1)
    zs = np.arange(Z_MIN, Z_MAX + 1)
    return np.meshgrid(xs, zs, indexing="ij")


def made_mask(X, Z, cs, pad=0):
    """The columns of made land, grown ground kept out of them."""
    m = np.zeros(X.shape, bool)
    for (cx, cz), c in cs.items():
        if c.kind in BR.LAND:
            m |= (X >= cx * CELL - pad) & (X < cx * CELL + CELL + pad) & (Z >= cz * CELL - pad) & \
                (Z < cz * CELL + CELL + pad)
    return m


STAIR_FOOT = (20, 24, -60, -56)            # the meadow stair's foot: x0, x1, z0, z1, laid level at LANE
EMERALD_AT, EMERALD_Y = (40, -64), 21      # red's emerald monument: its middle column, and the ground under it


def meadow(X, Z, cs):
    """The meadow east of red's yard: a hillside rising to the north-east, its south falling away over the void,
    its west edge the made yard's and lane's faces. (mask, H)."""
    n = noise.fbm(X.shape, 16, 3, seed=11)
    edge = np.hypot((X - 44) / 30.0, (Z + 52) / 30.0) + 0.18 * n
    m = (edge < 1.0) & (X >= 10) & (Z <= -22)
    m &= ~made_mask(X, Z, cs)
    rise = noise.smoothstep(-25, -75, Z) * 0.6 + noise.smoothstep(15, 60, X) * 0.4
    H = 11 + 13 * rise + 2.5 * noise.fbm(X.shape, 10, 2, seed=12)
    near_yard = (X < 20) & (Z <= -45)                               # under the yard's face: three or more below
    H = np.where(near_yard, np.minimum(H, YARD - 3), H)
    H = np.where((X < 15) & (Z > -45), np.minimum(H, LANE - 3), H)  # under the lane's face
    fx0, fx1, fz0, fz1 = STAIR_FOOT                                 # the stair's foot, level, and round it a
    d = np.maximum(np.maximum(fx0 - X, X - fx1), np.maximum(fz0 - Z, Z - fz1))   # gentle run out to the hill
    H = np.where(d <= 0, LANE, np.where(d < 6, LANE + (H - LANE) * d / 6.0, H))
    mx, mz = EMERALD_AT                                             # the emerald's ground, level, eased out to the hill
    d = np.maximum(np.abs(X - mx), np.abs(Z - mz))
    H = np.where(d <= 3, EMERALD_Y, np.where(d < 8, EMERALD_Y + (H - EMERALD_Y) * (d - 3) / 5.0, H))
    return m, np.round(H).astype(int)


ISLAND = (-38, -18, 12, 10)                # the island off the landing: centre, half widths


def island(X, Z):
    """The floating island off red's landing, toward the middle: a grassy top tilted toward the landing, rock where
    it is steep, a deep underside. (mask, H)."""
    cx, cz, rx, rz = ISLAND
    n = noise.fbm(X.shape, 8, 3, seed=21)
    r = np.hypot((X - cx) / rx, (Z - cz) / rz) + 0.22 * n
    m = r < 1.0
    H = 13 + 3 * noise.smoothstep(-8, -28, Z) + 2.0 * (1 - r) + 1.5 * noise.fbm(X.shape, 6, 2, seed=22)
    return m, np.round(H).astype(int)


# ---- objectives ----------------------------------------------------------------------------------------------
WOOL_BOX = (-55, -75, -46, -66)            # the wool's house, its whole piece
WOOL_AT = (-50, WOOL + 1, -71)
SPAWN_BOX = (-5, -70, 4, -61)              # the keep, under the spawn's house
SPAWN_AT = (0, YARD + 1, -66)
MONUMENT = (0, YARD + 1, -50)              # red's, in the yard's front, where red brings blue's wool


def objectives():
    """Two teams spawning in their houses; each team's wool in its house, captured by the other at its monument."""
    O = Objectives(Teams(*TEAMS), SYM)
    sx0, sz0, sx1, sz1 = SPAWN_BOX
    O.add(Spawn("red-team", SPAWN_AT, yaw=0, kit="spawn-kit", area=Box(sx0, 0, sz0, sx1, 127, sz1)))
    O.add(Observer((0, 50, 0), yaw=90), mirror=False)
    wx0, wz0, wx1, wz1 = WOOL_BOX
    room = Box(wx0 + 1, WOOL + 1, wz0 + 1, wx1 - 1, WOOL + 4, wz1 - 1)
    bx, bz = SYM.point(MONUMENT[0], MONUMENT[2])
    O.add(Wool("blue-team", "yellow", slot=(int(bx), MONUMENT[1], int(bz)), found=WOOL_AT, room=room),
          color="orange")
    ex, ez = EMERALD_AT                       # and a monument to destroy on each meadow: a cube of emerald on bedrock
    O.add(Destroyable("red-emerald", "Red Emerald", "red-team", Box(ex - 1, EMERALD_Y + 1, ez - 1, ex + 1, EMERALD_Y + 3,
                                                                    ez + 1),
                      material=(B.EMERALD_BLOCK, 0), materials="emerald block", heart=(B.BEDROCK, 0)),
          name="Blue Emerald")
    return O
