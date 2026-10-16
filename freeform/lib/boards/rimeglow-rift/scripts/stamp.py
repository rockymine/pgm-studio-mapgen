"""A building is stated once in the north half's coordinates and written twice: through a `Stamp` that leaves it
where it is (Rime, in winter's materials) or turns it half way round the board (Ember, in autumn's). The turn carries
every block's facing with it; the palette carries the materials."""
import numpy as np

from pgmvox import B
from pgmvox.core.orient import door as door_data, stair as stair_data, turn_data, torch as torch_data
from pgmvox.core.orient import ladder as ladder_data

AIR = (B.AIR, 0)

# name -> (Rime, Ember). A block is (id, data); a stair or door family is an id.
PAL = {
    "wall": ((B.STONEBRICK, 0), (B.NETHER_BRICK, 0)),
    "wall_b": ((B.STONE, 5), (B.RED_SANDSTONE, 2)),
    "wall_c": ((B.COBBLE, 0), (B.STAINED_CLAY, 12)),
    "plinth": ((B.STONEBRICK, 2), (B.RED_SANDSTONE, 1)),
    "log": ((B.LOG, 1), (B.LOG2, 1)),
    "plank": ((B.PLANKS, 1), (B.PLANKS, 5)),
    "plank_b": ((B.PLANKS, 5), (B.PLANKS, 4)),
    "slab": ((B.WOOD_SLAB, 1), (B.WOOD_SLAB, 5)),
    "roof": ((B.PLANKS, 1), (B.PLANKS, 4)),
    "roof_slab": ((B.WOOD_SLAB, 1), (B.WOOD_SLAB, 4)),
    "fence": ((B.SPRUCE_FENCE, 0), (B.DARK_OAK_FENCE, 0)),
    "glass": ((B.STAINED_GLASS, 3), (B.STAINED_GLASS, 1)),
    "pane": ((B.STAINED_PANE, 3), (B.STAINED_PANE, 1)),
    "light": ((B.SEA_LANTERN, 0), (B.GLOWSTONE, 0)),
    "stone": ((B.STONE, 0), (B.STONE, 1)),
    "slab_stone": ((B.SLAB, 5), (B.RED_SANDSTONE_SLAB, 0)),
    "post": ((B.COBBLE_WALL, 0), (B.NETHER_FENCE, 0)),
    "pave_a": ((B.STONE, 6), (B.STONE, 2)),
    "pave_b": ((B.STONE, 5), (B.BRICK, 0)),
    "pave_c": ((B.STONEBRICK, 0), (B.STONE, 1)),
    "pave_d": ((B.COBBLE, 0), (B.HARDENED_CLAY, 0)),
    "hot": ((B.PACKED_ICE, 0), (B.STAINED_CLAY, 1)),
    "accent": ((B.PACKED_ICE, 0), (B.HAY, 0)),
    "rock": ((B.STONE, 0), (B.HARDENED_CLAY, 0)),
    "pressure": ((B.PACKED_ICE, 0), (B.OBSIDIAN, 0)),
    "menhir": ((B.STONE, 5), (B.COAL_BLOCK, 0)),
}
STAIRS = {
    "roof": (B.SPRUCE_STAIRS, B.ACACIA_STAIRS),
    "wall": (B.STONEBRICK_STAIRS, B.NETHER_STAIRS),
    "trim": (B.COBBLE_STAIRS, B.RED_SANDSTONE_STAIRS),
    "plank": (B.SPRUCE_STAIRS, B.DARK_OAK_STAIRS),
}
DOORS = (B.SPRUCE_DOOR, B.DARK_OAK_DOOR)


class Stamp:
    def __init__(self, w, south=False):
        self.w, self.south = w, bool(south)

    # ---- coordinates and writing -----------------------------------------------------------------------
    def xz(self, x, z):
        return (-1 - x, -1 - z) if self.south else (x, z)

    def block(self, key):
        if isinstance(key, str):
            return PAL[key][int(self.south)]
        return key

    def set(self, x, y, z, key, d=None):
        """One block; `key` is a palette name or an (id, data); `d` overrides the data."""
        if isinstance(key, int):
            blk = (key, 0 if d is None else d)
        else:
            blk = self.block(key)
            if d is not None:
                blk = (blk[0], d)
        px, pz = self.xz(x, z)
        bid, dat = blk
        if self.south:
            dat = turn_data(bid, dat, "half")
        self.w.set(px, y, pz, bid, dat)

    def get(self, x, y, z):
        px, pz = self.xz(x, z)
        return self.w.get(px, y, pz)

    def fill(self, x0, y0, z0, x1, y1, z1, key):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for z in range(min(z0, z1), max(z0, z1) + 1):
                for y in range(min(y0, y1), max(y0, y1) + 1):
                    self.set(x, y, z, key)

    def clear(self, x0, y0, z0, x1, y1, z1):
        self.fill(x0, y0, z0, x1, y1, z1, AIR)

    def hollow(self, x0, y0, z0, x1, y1, z1, key, top=None, bottom=None):
        """A box of walls, floor and roof optional, hollow inside."""
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                for y in range(y0, y1 + 1):
                    edge = x in (x0, x1) or z in (z0, z1)
                    if edge:
                        self.set(x, y, z, key)
                    elif y == y0 and bottom is not None:
                        self.set(x, y, z, bottom)
                    elif y == y1 and top is not None:
                        self.set(x, y, z, top)
                    else:
                        self.set(x, y, z, AIR)

    def stair(self, x, y, z, family, rises, upside=False):
        bid = STAIRS[family][int(self.south)]
        self.set(x, y, z, (bid, stair_data(rises, upside)))

    def door(self, x, y, z, facing):
        bid = DOORS[int(self.south)]
        self.set(x, y, z, (bid, door_data(facing)))
        self.set(x, y + 1, z, (bid, door_data(facing, upper=True)))

    def torch(self, x, y, z, on_wall=None):
        self.set(x, y, z, (B.TORCH, torch_data(on_wall)))

    def ladder(self, x, y, z, on_wall):
        self.set(x, y, z, (B.LADDER, ladder_data(on_wall)))

    def log(self, x, y, z, axis=None, key="log"):
        """A log lying along `axis` ("x" or "z") or standing upright."""
        bid, dat = self.block(key)
        self.set(x, y, z, (bid, (dat & 3) | {"x": 4, "z": 8, None: 0}[axis]))

    def banner(self, x, y, z, base, patterns=(), wall_facing=None, rot=0):
        """A banner (dye numbering 0 black .. 15 white); under the turn a wall banner faces the other way."""
        px, pz = self.xz(x, z)
        if self.south:
            wall_facing = {2: 3, 3: 2, 4: 5, 5: 4}.get(wall_facing, wall_facing)
            rot = (rot + 8) % 16
        self.w.banner(px, y, pz, base, patterns, wall_facing, rot)

    def column(self, x, z, y0, y1, key):
        for y in range(y0, y1 + 1):
            self.set(x, y, z, key)

    def foot(self, H, x, z, y, key="rock", under=None):
        """Fill down from y - 1 to the ground at (x, z), so a building never hangs."""
        px, pz = self.xz(x, z)
        g = int(H[px - self.w.x0, pz - self.w.z0])
        if g <= 0:
            return
        for yy in range(g, y):
            blk = self.block(key) if under is None else under
            if self.get(x, yy, z)[0] in (0, B.SNOW_LAYER, B.SNOW, B.GRASS, B.CARPET, B.TALLGRASS) or yy >= g:
                self.set(x, yy, z, blk)
