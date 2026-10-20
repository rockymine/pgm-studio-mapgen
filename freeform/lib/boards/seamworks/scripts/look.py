"""Seamworks' looks: what every block of every asset is made of, asked by the asset functions in `assets.py` by
role. `LOOK` is the board's; `PANELS`, `CRUSTS` and `BUILDINGS` hold the palettes the asset sheet compares side by
side.

The rock of the cuts is stone and andesite with cobblestone under a third, and a cut floor is a noise mix of the
same stones, so the floor players walk on is told apart from the ash above it. What the board's look is, and why,
is `PLAN.md`'s."""
import numpy as np

import plan as P
from pgmvox import B
from pgmvox.core.orient import stair as stair_data_
from pgmvox.geom.noise import fbm

W, H = P.W, P.H


def _sym(f):
    return (f + f[::-1, ::-1]) / 2


def _field(cell, seed, octaves=3):
    f = _sym(fbm((W, H), cell, octaves, seed=seed))
    return (f - f.min()) / (f.max() - f.min())


ROCK_A = _field(5, 11)                    # patches about five across
ROCK_B = _field(4, 12)
FLOOR_A = _field(5, 13)
FLOOR_B = _field(4, 14)
ASH = _field(16, 21, 4)                   # the crust's patches, large and coherent
ASH_FINE = _field(4, 22)
WEAR = _field(6, 31)
STEP = _field(4, 41) * 2 - 1              # the wander of a flight's step edges, -1 to 1
PATCH = _field(4, 51)


def _at(f, x, z):
    return f[x % W, z % H]


def _hash(x, y, z):
    return ((x * 73856093) ^ (y * 19349663) ^ (z * 83492791)) % 1000 / 1000


def pick(spec, x, y, z):
    """A block from a palette entry: a block, or [(block, weight), ...] drawn by the block's position."""
    if isinstance(spec, tuple):
        return spec
    r = _hash(x, y, z) * sum(wt for _, wt in spec)
    for block, wt in spec:
        r -= wt
        if r < 0:
            return block
    return spec[-1][0]


# ---- the panels: a frame round every panel so each plane reads, and an infill whose pattern may change from one
# panel to the next. A pattern is a function of the block's place on its panel: along, up, its length and rise ------
STEEL = (B.PRISMARINE, 2)
FRAME = (B.STONE, 6)


def _framed(info):
    return info["along"] < 1 or info["along"] >= info["length"] - 1 or info["up"] < 1 or info["up"] >= info["rise"] - 1


def _plain(info, x, y, z):
    return STEEL


def _courses(info, x, y, z):
    return FRAME if int(info["up"]) % 4 == 0 else STEEL


def _crossed(info, x, y, z):
    on = int(info["along"]) % 3 == 0 if info["shade"] == 0 else int(info["up"]) % 3 == 0
    return FRAME if on else STEEL


def _diagonal(info, x, y, z):
    on = int(info["along"]) % 3 == 0 if info["shade"] == 0 else (int(info["along"]) + int(info["up"])) % 4 == 0
    return FRAME if on else STEEL


def _broken_by(block):
    def pattern(info, x, y, z):
        return block if _at(PATCH, x + int(info["up"]) * 3, z + int(info["along"])) > 0.66 else STEEL
    return pattern


def _weathered(block):
    def pattern(info, x, y, z):
        if _at(PATCH, x + int(info["up"]) * 3, z + int(info["along"])) > 0.7:
            return block
        return _crossed(info, x, y, z)
    return pattern


PANELS = {"framed": _plain, "framed courses": _courses, "crossed": _crossed, "crossed and diagonal": _diagonal,
          "broken by green clay": _broken_by((B.STAINED_CLAY, 13)),
          "broken by green wool": _broken_by((B.WOOL, 13)),
          "crossed, weathered by green clay": _weathered((B.STAINED_CLAY, 13)),
          "crossed, weathered by green wool": _weathered((B.WOOL, 13))}

# ---- the crust: one ground with patches inset in it, as noise stops [core, rim, ground ...] --------------------------
# a core is sunk a block; the ground is a fine mix of its own blocks
CRUSTS = {
    "soot and charred boards": {"core": [((B.STAINED_CLAY, 15), 7), ((B.PLANKS, 5), 3)],
                                "rim": [((B.DIRT, 1), 1), ((B.DIRT, 2), 1)],
                                "ground": [(B.GRAVEL, 0), (B.STONE, 5), (B.GRAVEL, 0)]},
    "soot and coal": {"core": [((B.STAINED_CLAY, 15), 6), ((B.COAL_BLOCK, 0), 4)],
                      "rim": [((B.DIRT, 1), 1), ((B.DIRT, 0), 1)],
                      "ground": [(B.GRAVEL, 0), (B.STONE, 5), (B.GRAVEL, 0)]},
    "gravel ash": {"core": (B.STAINED_CLAY, 15), "rim": (B.GRAVEL, 0),
                   "ground": [(B.GRAVEL, 0), (B.STONE, 5), (B.GRAVEL, 0)]},
    "badlands and soot": {"core": [((B.STAINED_CLAY, 15), 7), ((B.PLANKS, 5), 3)],
                          "rim": [((B.DIRT, 1), 1), ((B.DIRT, 2), 1)],
                          "ground": [(B.SAND, 1), (B.RED_SANDSTONE, 0), (B.SAND, 1), (B.RED_SANDSTONE, 0), (B.STAINED_CLAY, 1)]},
}
DEEP, SOOT, RIM = 0.24, 0.38, 0.47         # where a patch's deep core, its core and its rim end on the patch field

# ---- the overburden: the orange ground the cuts were dug through, in beds that follow the crust, over the stone the
# diggers struck and left. Its thickness wanders between five and eight blocks ------------------------------------------
RED_SANDSTONE_DOUBLE = 181                # the double red sandstone slab; data 8 is smooth on every face
BEDS = [(B.RED_SANDSTONE, 0), (RED_SANDSTONE_DOUBLE, 8), (B.RED_SANDSTONE, 0), (B.HARDENED_CLAY, 0),
        (RED_SANDSTONE_DOUBLE, 8), (B.RED_SANDSTONE, 0), (B.STAINED_CLAY, 1)]
OVER = _field(12, 61)
BED_WOBBLE = _field(9, 62)

# ---- the works, by role ------------------------------------------------------------------------------------------------
_BUILT_FLOOR = [((B.STONEBRICK, 0), 1), ((B.STONE, 6), 1), ((B.STONE, 5), 1), ((B.STONE, 0), 1)]


def _cells_of(blocks, size):
    """A pattern of `blocks` an equal share each, in cells about `size` across."""
    def pattern(x, y, z):
        k = (x // size) * 7 + (z // size) * 13 + (y // size) * 5 + (x // size) * (z // size)
        return blocks[k % len(blocks)]
    return pattern


def _courses(a, b):
    """Two blocks in alternate courses."""
    return lambda x, y, z: a if y % 2 else b


ROOF_BLOCKS = [(B.DSLAB, 0), (B.DSLAB, 8), (B.WOOL, 8)]
BUILDINGS = {
    "brick works": {"wall": (B.BRICK, 0), "window band": (B.HARDENED_CLAY, 0),
                    "corner": _courses((B.NETHER_BRICK, 0), (B.STAINED_CLAY, 15)),
                    "band": _cells_of([(B.DSLAB, 0), (B.DSLAB, 8)], 2), "base": (B.NETHER_BRICK, 0),
                    "cornice": (B.DSLAB, 0), "parapet": (B.SLAB, 6), "roof": _cells_of(ROOF_BLOCKS, 2),
                    "inset": B.BRICK_STAIRS, "skylight": (B.GLASS, 0),
                    "window": (B.IRON_BARS, 0), "sill": (B.DSLAB, 0), "floor": _BUILT_FLOOR,
                    "light": (B.GLOWSTONE, 0), "jamb": (B.NETHER_BRICK, 0), "lintel": (B.DSLAB, 0)},
}
CHIMNEY = {"stack": (B.STONEBRICK, 0), "ring": (B.STONE, 6), "crown": (B.COBBLE_WALL, 0),
           "smoke": [((B.STAINED_GLASS, 8), 3), ((B.STAINED_GLASS, 7), 2), ((B.GLASS, 0), 1)]}


class Look:
    """Every asset's blocks: the ground as stated above, the panels, crust and works from a palette each."""

    def __init__(self, panels="framed", building="brick works", crust="soot and charred boards"):
        self.panels_name, self.building_name, self.crust_name = panels, building, crust
        self.pattern = PANELS[panels]
        self.C = CRUSTS[crust]
        self.Bd = BUILDINGS[building]

    # the ground
    def rock(self, x, y, z):
        a = _at(ROCK_A, x, z) * 0.7 + ((x * 7 + y * 13 + z * 5) % 11) / 11 * 0.3
        if _at(ROCK_B, x + y * 3, z + y * 2) > 0.72:
            return (B.COBBLE, 0)
        return (B.STONE, 5) if a < 0.42 else (B.STONE, 0)

    def crust(self, x, z):
        v = _at(ASH, x, z)
        if v < SOOT:
            return pick(self.C["core"], x, 0, z)
        if v < RIM:
            return pick(self.C["rim"], x, 0, z)
        g = self.C["ground"]
        return g[min(int(_at(ASH_FINE, x, z) * len(g)), len(g) - 1)]

    def sunk(self, x, z):
        """How many blocks lower the crust lies here: two in a soot patch's deep core, one in the rest of its core."""
        v = _at(ASH, x, z)
        return 2 if v < DEEP else 1 if v < SOOT else 0

    def thickness(self, x, z):
        """How deep the orange ground runs under the crust before the stone."""
        return 5 + int(_at(OVER, x, z) * 3.99)

    def overburden(self, x, y, z, depth):
        """The orange ground `depth` blocks under the crust's top, in beds about two blocks deep."""
        bed = int((depth + _at(BED_WOBBLE, x, z) * 1.6) / 1.7)
        return BEDS[bed % len(BEDS)]

    def cut_floor(self, x, z):
        if _at(FLOOR_B, x, z) > 0.8:
            return (B.COBBLE, 0)
        v = _at(FLOOR_A, x, z)
        return (B.STONE, 5) if v < 0.4 else (B.STONE, 0) if v < 0.78 else (B.STONE, 6)

    tunnel_floor = cut_floor

    def lump(self, x, z, v):
        return (B.COBBLE, 0) if v == 2 else (B.SLAB, 3)

    def stair(self, x, z, data):
        return (B.STONEBRICK_STAIRS, data)

    def spoil(self, x, y, z):
        """What the cuts threw out, heaped: the crust's soot, black clay and charred boards in coarse dirt and podzol."""
        return pick([((B.STAINED_CLAY, 15), 4), ((B.PLANKS, 5), 2), ((B.DIRT, 1), 2), ((B.DIRT, 2), 2)], x, y, z)

    def seam(self, x, y, z):
        return (B.NETHERRACK, 0)

    # the made things
    def panel(self, x, y, z, info):
        return FRAME if _framed(info) else self.pattern(info, x, y, z)

    def plate(self, x, y, z, role):
        return (B.IRON_BLOCK, 0) if role == "plate" else (B.DSLAB, 0)

    def building(self, x, y, z, role):
        spec = self.Bd[role]
        return spec(x, y, z) if callable(spec) else pick(spec, x, y, z)

    def inset(self, x, y, z, inward, upside_down):
        """A stair set into a wall, its full half inward, so the wall's face steps back half a block."""
        return (self.Bd["inset"], stair_data_(inward, upside_down))

    def door(self, x, y, z, role):
        return pick(self.Bd[role], x, y, z)

    def chimney(self, x, y, z, role):
        return pick(CHIMNEY[role], x, y, z)

    def timber(self, role):
        return (B.SPRUCE_FENCE, 0) if role == "post" else (B.PLANKS, 1)

    def hut(self, x, y, z, role, up=None):
        if role == "roof":
            return (B.DARK_OAK_STAIRS, stair_data_(up))
        return {"post": (B.LOG2, 1), "wall": (B.PLANKS, 1), "gable": (B.PLANKS, 1), "ridge": (B.WOOD_SLAB, 5),
                "window": (B.IRON_BARS, 0), "table": (B.CRAFTING, 0)}[role]

    def dais(self, x, y, z, role, up=None):
        if role == "step":
            return (B.STONEBRICK_STAIRS, stair_data_(up))
        return {"deck": (B.STONEBRICK, 0), "plinth": (B.STONE, 6), "post": (B.NETHER_FENCE, 0),
                "canopy": (B.SLAB, 5 | 8), "light": (B.GLOWSTONE, 0)}[role]

    def roof_kit(self, x, y, z, role):
        return {"body": (B.DSLAB, 8), "grille": (B.IRON_BARS, 0), "fan": (151, 0), "pipe": (B.COBBLE_WALL, 0),
                "cap": (B.SLAB, 0), "footing": (B.STONE, 6), "mast": (B.IRON_BARS, 0), "arm": (B.IRON_BARS, 0),
                "tip": (B.REDSTONE_BLOCK, 0), "lamp": (B.REDSTONE_TORCH, 5)}[role]

    def rim(self, team):
        return (B.STAINED_CLAY, 14) if team == 0 else (B.STAINED_CLAY, 11)

    def light(self):
        return (B.GLOWSTONE, 0)


LOOK = Look(panels="crossed, weathered by green wool", crust="badlands and soot")


BAND_EVERY = 8                            # blocks from one dark bed to the next through the stone
BAND_WOBBLE = _field(14, 71)
BAND_GAPS = _field(6, 72)


def paint_rock(w, look=LOOK):
    """Every block of plain stone in the world turned into the rock set, course by course, with its thin beds."""
    xs = np.arange(w.x0, w.x0 + w.sx) % W
    zs = np.arange(w.z0, w.z0 + w.sz) % H
    XI, ZI = np.meshgrid(xs, zs, indexing="ij")
    a0 = ROCK_A[XI, ZI] * 0.7
    lean = P.CRUST[np.clip(np.arange(w.x0, w.x0 + w.sx), 0, W - 1)][:, np.clip(np.arange(w.z0, w.z0 + w.sz), 0, H - 1)] * 0.6
    for y in range(1, w.sy):
        layer = w.ids[:, y, :]
        stone = (layer == B.STONE) & (w.dat[:, y, :] == 0)
        if not stone.any():
            continue
        grain = ((XI * 7 + y * 13 + ZI * 5) % 11) / 11 * 0.3
        b = ROCK_B[(XI + y * 3) % W, (ZI + y * 2) % H]
        cob = stone & (b > 0.72)
        andesite = stone & ~cob & (a0 + grain < 0.42)
        w.ids[:, y, :][cob] = B.COBBLE
        w.dat[:, y, :][andesite] = 5
        # thin beds through the stone, leaning a little with the crust and broken where the noise is low: a dark bed
        # of cyan clay and, between those, a pale bed of clay
        level = y - lean + BAND_WOBBLE[XI, ZI] * 2.2
        whole = BAND_GAPS[(XI + y * 5) % W, ZI] > 0.3
        if y + 1 < w.sy:
            whole &= w.ids[:, y + 1, :] != B.AIR             # a bed shows in a face, never on a rock's top
        dark = stone & whole & (np.mod(level, BAND_EVERY) < 1)
        pale = stone & whole & (np.abs(np.mod(level, BAND_EVERY) - BAND_EVERY / 2) < 0.5)
        w.ids[:, y, :][dark] = B.STAINED_CLAY
        w.dat[:, y, :][dark] = 9
        w.ids[:, y, :][pale] = B.CLAY
        w.dat[:, y, :][pale] = 0
