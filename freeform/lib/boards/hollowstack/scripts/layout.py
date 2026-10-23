"""Hollowstack's numbers, in blue's half (x >= 0); red's are their image under the half turn.

Every storey is stated here once: the chasm's face, the ground of the Tops, the floors of the Workings, the
Underwood, the Undercroft and the Deep, the segment grids, the rooms and the wells.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox.plan.raster import Symmetry                                                # noqa: E402

SYM = Symmetry("half")
X0, Z0, SX, SZ, SY = -96, -28, 192, 56, 128
FACE = 12                      # the chasm's face: the first x of rock, x -12 to 11 the void between the walls
BACK = 95
SIDE = 26                      # the walls reach z -26 to 25, a ragged edge over the void at the board's sides

TOPS = 96                      # the Tops' ground at the brink; it rises to the keep's hill at KEEP_Y
KEEP_Y = 100
KEEP = (76, -12, 94, 11)       # the keep's levelled hill, x0, z0, x1, z1

WORKINGS = dict(x0=18, y0=82, z0=-20, cols=14, rows=8)              # the mine's grid: one level, floor y 82
UNDERCROFT = dict(x0=18, y0=34, z0=-20, cols=14, rows=8)            # the dungeon's grid: floors y 34 and 40
CELL, STOREY = 5, 6

UNDERWOOD = dict(cx=37, cz=0, rx=29, rz=19, roof=60, dome=17)      # the cavern: its plan ellipse and roof
UNDERWOOD_FLOORS = dict(mouth=56, spur=58, pond=51, water=53, mid=54, court=52, back=59, high=61)
DEEP = dict(floor=14, lava=13, pool=12)

LIGHT_WELL = (37, -9, 2.5)     # from the Tops into the Underwood's pond
ROOT_WELL = (27, 9, 2.4)       # from the Underwood's spur down to the Deep's pool
GATEHOUSE = (6, 4)             # the Undercroft's shaft column that rises into the Underwood's court
DEEP_SHAFT = (13, 7)           # the Undercroft's shaft column down into the Deep's grotto
KEEP_WELL = (13, 3)            # the shaft column from the Undercroft up through the Workings into the keep's yard
POSTERN_LEVEL = 4              # the keep well's door into the Underwood's back, y 58
WORKINGS_LEVEL = 8             # the Workings are the Undercroft's grid eight storeys up
VAULT = (10, 5, 12, 7)         # the Vault's cells in the Undercroft, two storeys high
PLUNGE = (61, -8, 1.6)         # a drop from the keep's hillside into a pool at the Underwood's back

SHRINE = dict(x0=13, z0=-5, x1=22, z1=5, floor=57)                 # the Grove Shrine's spur
SPAWN = (82, KEEP_Y + 1, 4)
MONUMENTS = [(79, KEEP_Y + 1, -7), (79, KEEP_Y + 1, 7)]


def cell_box(grid, i, j, level=0):
    """A grid cell's corner block (x, y, z)."""
    return grid["x0"] + i * CELL, grid["y0"] + level * STOREY, grid["z0"] + j * CELL
