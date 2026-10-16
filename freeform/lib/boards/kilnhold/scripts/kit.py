"""Kilnhold's blocks and the small things every part of the build uses: block names, stairs and slabs by facing,
and a carve-and-line engine for the bunker's interior.

The palette keeps three tone families apart. The ground is ash: black and grey stained clay, with scoria of red
sandstone and orange clay where the earth is hot. What is built is bone concrete: stone brick, polished andesite,
andesite and stone, with dark oak for timber and iron for machinery. The accents are hazard orange (red sandstone
and orange clay), the glow of lava and glowstone, and each team's wool.
"""
import numpy as np

import plan  # noqa: F401  (puts the library on the path)
from pgmvox import B
from pgmvox.core import orient

# ground and rock
STONE, ANDESITE, PAND, COBBLE = (B.STONE, 0), (B.STONE, 5), (B.STONE, 6), (B.COBBLE, 0)
BLACK, GREY = (B.STAINED_CLAY, 15), (B.STAINED_CLAY, 7)
ORANGE, RSAND, RSANDSTONE = (B.STAINED_CLAY, 1), (B.SAND, 1), (B.RED_SANDSTONE, 0)
RSMOOTH, RCHISEL = (B.RED_SANDSTONE, 2), (B.RED_SANDSTONE, 1)
COAL, OBSIDIAN, GRAVEL = (B.COAL_BLOCK, 0), (B.OBSIDIAN, 0), (B.GRAVEL, 0)
# built
SB, SBCRACK, SBCHISEL = (B.STONEBRICK, 0), (B.STONEBRICK, 2), (B.STONEBRICK, 3)
IRON, BARS = (B.IRON_BLOCK, 0), (B.IRON_BARS, 0)
OAK_DARK, LOG_DARK = (B.PLANKS, 5), (B.LOG2, 1)
LOG_DARK_X, LOG_DARK_Z = (B.LOG2, 1 | 4), (B.LOG2, 1 | 8)
GLOW, SEA = (B.GLOWSTONE, 0), (B.SEA_LANTERN, 0)
BROWN = (B.STAINED_CLAY, 12)
# team colours: wool, carpet and glass turn with the half turn into blue's
TEAM_WOOL, TEAM_CARPET, TEAM_GLASS = (B.WOOL, 14), (B.CARPET, 14), (B.STAINED_GLASS, 14)
RECOLOUR = {(B.WOOL, 14): (B.WOOL, 11), (B.CARPET, 14): (B.CARPET, 11), (B.STAINED_GLASS, 14): (B.STAINED_GLASS, 11),
            (B.STAINED_PANE, 14): (B.STAINED_PANE, 11)}
LAVA, WATER = (B.LAVA, 0), (B.WATER, 0)
AIR = (B.AIR, 0)

SLAB_STONE, SLAB_BRICK, SLAB_COBBLE = (B.SLAB, 0), (B.SLAB, 5), (B.SLAB, 3)
SLAB_UP = 8


def stairs(block_id, rises, upside_down=False):
    """A stair of `block_id` climbing toward `rises` ('e', 'w', 's', 'n')."""
    return (block_id, orient.stair(rises, upside_down))


SB_STAIR = lambda rises, up=False: stairs(B.STONEBRICK_STAIRS, rises, up)   # noqa: E731
COB_STAIR = lambda rises, up=False: stairs(B.COBBLE_STAIRS, rises, up)      # noqa: E731
RS_STAIR = lambda rises, up=False: stairs(B.RED_SANDSTONE_STAIRS, rises, up)  # noqa: E731


def put(w, x, y, z, blk):
    w.set(x, y, z, blk[0], blk[1])


def fill(w, x0, y0, z0, x1, y1, z1, blk):
    w.fill(x0, y0, z0, x1, y1, z1, blk[0], blk[1])


def pick(blocks, key):
    """One of `blocks` by an integer key: a pattern of several close tones laid by position."""
    return blocks[key % len(blocks)]


def cell_key(x, z, size=3, mul=(7, 13)):
    """A stable integer for the `size`-block cell (x, z) falls in: floors of four blocks laid a cell each."""
    return (x // size) * mul[0] + (z // size) * mul[1]


class Interior:
    """The bunker's rooms and passages: space is carved as air by room, then every solid block touching a carved
    cell is a lining cell whose block comes from its room's style (a floor, a wall or a ceiling), and ramps are set
    over the floor afterwards. Pilasters are carve-outs: cells taken back out of a room, still lined by it."""

    def __init__(self, w):
        self.w = w
        self.room = np.zeros(w.ids.shape, np.uint8)
        self.tag = np.zeros(w.ids.shape, np.uint8)
        self.names = [""]
        self.styles = [None]
        self.floors = [0]
        self.surfaces = {}                  # (x, z) -> (y of the floor block, slab?) for ramp cells

    def index(self, name, style=None, floor=0):
        if name in self.names:
            return self.names.index(name)
        self.names.append(name)
        self.styles.append(style)
        self.floors.append(floor)
        return len(self.names) - 1

    def _sl(self, x0, x1, y0, y1, z0, z1):
        w = self.w
        x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); z0, z1 = sorted((z0, z1))
        return (slice(max(x0, w.x0) - w.x0, min(x1, w.x0 + w.sx - 1) - w.x0 + 1), slice(max(y0, 0), min(y1, w.sy - 1) + 1),
                slice(max(z0, w.z0) - w.z0, min(z1, w.z0 + w.sz - 1) - w.z0 + 1))

    def carve(self, name, x0, x1, y0, y1, z0, z1, tag=0):
        idx = self.index(name)
        sl = self._sl(x0, x1, y0, y1, z0, z1)
        self.room[sl] = idx
        self.tag[sl] = tag

    def keep(self, x0, x1, y0, y1, z0, z1, tag=1):
        """Cells taken back out of the carve: a pilaster or a pier, still lined by the room beside it."""
        sl = self._sl(x0, x1, y0, y1, z0, z1)
        self.room[sl] = 0
        self.tag[sl] = tag

    def box(self, name, x0, x1, z0, z1, floor, h):
        """A room: air from the cell over its floor block up `h` cells."""
        self.carve(name, x0, x1, floor + 1, floor + h, z0, z1)

    def ramp(self, name, cells, h):
        """A run of floor cells [(x, z, y_floor, slab)]: air over each from its floor up `h` (a slab's own cell is
        carved too so the wall beside it is lined to the slab's top); the surface is set after the lining."""
        for x, z, y, slab in cells:
            self.carve(name, x, x, y if slab else y + 1, y + h, z, z)
            self.surfaces[(x, z)] = (y, slab)

    def line(self):
        """Line every solid cell touching carved air with its room's style. Returns how many were lined."""
        w = self.w
        carved = self.room > 0
        w.ids[carved] = 0
        w.dat[carved] = 0
        owner = np.zeros_like(self.room)
        touch = np.zeros(carved.shape, bool)
        above = np.zeros(carved.shape, bool)
        below = np.zeros(carved.shape, bool)
        for axis in (0, 1, 2):
            for sh in (1, -1):
                src = np.roll(carved, sh, axis=axis)
                ro = np.roll(self.room, sh, axis=axis)
                # np.roll wraps: blank the wrapped slice
                sl = [slice(None)] * 3
                sl[axis] = slice(0, 1) if sh == 1 else slice(-1, None)
                src[tuple(sl)] = False
                ro[tuple(sl)] = 0
                touch |= src
                owner = np.where(src & (ro > owner), ro, owner)
                if axis == 1:
                    if sh == 1:
                        below |= src                      # the cell below is carved: this is a ceiling
                    else:
                        above |= src                      # the cell above is carved: this is a floor
        lining = touch & ~carved & (w.ids != B.AIR) & (w.ids != B.BEDROCK)
        n = 0
        for i, y, k in zip(*np.nonzero(lining)):
            x, z = i + w.x0, k + w.z0
            idx = int(owner[i, y, k])
            style = self.styles[idx]
            if style is None:
                continue
            face = "floor" if above[i, y, k] else "ceil" if below[i, y, k] else "wall"
            blk = style(x, y, z, face)
            if blk is not None:
                w.ids[i, y, k], w.dat[i, y, k] = blk
                n += 1
        for (x, z), (y, slab) in self.surfaces.items():
            idx = self.room[x - w.x0, y + (1 if not slab else 0), z - w.z0] or 0
            style = self.styles[idx] if idx else None
            blk = style(x, y, z, "ramp") if style else STONE
            if slab:
                blk = (B.SLAB, blk[1] if blk[0] == B.SLAB else 0)
            w.set(x, y, z, *blk)
        return n


def ramp_cells(xs, zs, run, start, flat=0, fall=False, level=None):
    """The floor cells of a ramp that moves half a block a cell along `run` ('+x', '-x', '+z', '-z'), `start` the y
    of the floor block at the first cell, `flat` cells flat before it begins, held at `level` once it gets there.
    Returns [(x, z, y of the floor block, slab?)] over the passage's whole width."""
    xa, xb = xs
    za, zb = zs
    sign = -1 if fall else 1
    out = []
    axis, direction = run[1], run[0]
    if axis == "x":
        order = range(xa, xb + 1) if direction == "+" else range(xb, xa - 1, -1)
    else:
        order = range(za, zb + 1) if direction == "+" else range(zb, za - 1, -1)
    for n, c in enumerate(order):
        i = max(0, n - flat)
        half = 2 * (start + 1) + sign * i                     # the surface in half blocks
        if level is not None:
            half = max(half, 2 * (level + 1)) if fall else min(half, 2 * (level + 1))
        slab = half % 2 == 1
        y = (half - 1) // 2 if slab else half // 2 - 1
        if axis == "x":
            out += [(c, z, y, slab) for z in range(za, zb + 1)]
        else:
            out += [(x, c, y, slab) for x in range(xa, xb + 1)]
    return out
