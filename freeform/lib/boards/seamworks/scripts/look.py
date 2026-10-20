"""Seamworks' looks: what every block of every asset is made of, asked by the asset functions in `assets.py` by
role. `LOOK` is the board's; `PANELS` and `BUILDINGS` hold the palettes the asset sheet compares side by side.

The rock of the cuts is stone and andesite with cobblestone under a third, and a cut floor is stone, andesite and
gravel a third each. The board's look, chosen on the sheet: the crust is gravel ash, gravel and andesite with soot
patches of black clay; the panels are dark steel, dark prismarine plates on polished andesite ribs under a smooth
stone cap, which stands apart from both the grey rock and the red brick; the works are brick, nether brick at the
corners and base, smooth stone at each storey's band, the sills and the cornice."""
import numpy as np

import plan as P
from pgmvox import B
from pgmvox.geom.noise import fbm

W, H = P.W, P.H


def _sym(f):
    return (f + f[::-1, ::-1]) / 2


def _field(cell, seed, octaves=3):
    f = _sym(fbm((W, H), cell, octaves, seed=seed))
    return (f - f.min()) / (f.max() - f.min())


ROCK_A = _field(5, 11)                    # patches about five across
ROCK_B = _field(4, 12)
ASH = _field(5, 21)
WEAR = _field(6, 31)
STEP = _field(4, 41) * 2 - 1              # the wander of a flight's step edges, -1 to 1


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


# ---- the panels: the steel lining the cuts, by role: plate, rib (every third block), cap (the top course), edge ------
PANELS = {
    "iron": {"plate": (B.IRON_BLOCK, 0), "rib": (B.DSLAB, 0), "cap": (B.DSLAB, 0), "edge": (B.DSLAB, 0)},
    "plate steel": {"plate": (B.STONE, 6), "rib": (B.DSLAB, 0), "cap": (B.IRON_BLOCK, 0), "edge": (B.DSLAB, 0)},
    "rust": {"plate": [((B.RED_SANDSTONE, 2), 3), ((B.STONE, 2), 1)], "rib": (B.STONE, 1), "cap": (B.DSLAB, 0),
             "edge": (B.STONE, 1)},
    "patina": {"plate": (B.PRISMARINE, 2), "rib": (B.PRISMARINE, 1), "cap": (B.DSLAB, 0), "edge": (B.PRISMARINE, 1)},
    "steel and verdigris": {"plate": (B.STONE, 6), "rib": (B.PRISMARINE, 2), "cap": (B.DSLAB, 0),
                            "edge": (B.PRISMARINE, 2)},
    "dark steel": {"plate": (B.PRISMARINE, 2), "rib": (B.STONE, 6), "cap": (B.DSLAB, 0), "edge": (B.STONE, 6)},
}

# ---- the crust: the ash on everything above the cuts, as noise stops [patch, ground, ground, patch] ----------------
CRUSTS = {
    "clay ash": [(B.STAINED_CLAY, 7), (B.STAINED_CLAY, 9), (B.STAINED_CLAY, 9), (B.STAINED_CLAY, 15)],
    "gravel ash": [(B.STAINED_CLAY, 15), (B.GRAVEL, 0), (B.GRAVEL, 0), (B.STONE, 5)],
    "cinder": [(B.DIRT, 1), (B.GRAVEL, 0), (B.STONE, 5), (B.COBBLE, 0)],
}

# ---- the works, by role ------------------------------------------------------------------------------------------------
_BUILT_FLOOR = [((B.STONEBRICK, 0), 1), ((B.STONE, 6), 1), ((B.STONE, 5), 1), ((B.STONE, 0), 1)]
BUILDINGS = {
    "brick works": {"wall": (B.BRICK, 0), "corner": (B.NETHER_BRICK, 0), "band": (B.DSLAB, 0),
                    "base": (B.NETHER_BRICK, 0), "cornice": (B.DSLAB, 0), "parapet": (B.NETHER_BRICK, 0),
                    "roof": (B.DSLAB, 0), "skylight": (B.GLASS, 0), "window": (B.IRON_BARS, 0),
                    "sill": (B.DSLAB, 0), "floor": _BUILT_FLOOR, "light": (B.GLOWSTONE, 0),
                    "jamb": (B.NETHER_BRICK, 0), "lintel": (B.DSLAB, 0), "stack": (B.BRICK, 0),
                    "cap": (B.NETHER_BRICK, 0)},
    "brick and timber": {"wall": (B.BRICK, 0), "corner": (B.LOG, 1), "band": (B.LOG, 1 | 4), "base": (B.STONEBRICK, 0),
                         "cornice": (B.PLANKS, 1), "parapet": (B.SPRUCE_FENCE, 0), "roof": (B.PLANKS, 1),
                         "skylight": (B.GLASS, 0), "window": (B.PANE, 0), "sill": (B.PLANKS, 1),
                         "floor": _BUILT_FLOOR, "light": (B.GLOWSTONE, 0), "jamb": (B.LOG, 1), "lintel": (B.LOG, 1 | 4),
                         "stack": (B.BRICK, 0), "cap": (B.STONEBRICK, 0)},
    "sandstone concrete": {"wall": (B.SANDSTONE, 2), "corner": (B.SANDSTONE, 0), "band": (B.BRICK, 0),
                           "base": (B.BRICK, 0), "cornice": (B.BRICK, 0), "parapet": (B.SANDSTONE, 2),
                           "roof": (B.DSLAB, 0), "skylight": (B.GLASS, 0), "window": (B.IRON_BARS, 0),
                           "sill": (B.DSLAB, 1), "floor": _BUILT_FLOOR, "light": (B.GLOWSTONE, 0),
                           "jamb": (B.BRICK, 0), "lintel": (B.BRICK, 0), "stack": (B.BRICK, 0),
                           "cap": (B.SANDSTONE, 2)},
}
# the hazard frame stays available as a door's look
HAZARD = [(B.STAINED_CLAY, 4), (B.STAINED_CLAY, 15)]


class Look:
    """Every asset's blocks: the ground as stated above, the panels and works from a palette each."""

    def __init__(self, panels="iron", building="brick works", crust="clay ash", hazard=False):
        self.panels_name, self.building_name = panels, building
        self.C = CRUSTS[crust]
        self.P = PANELS[panels]
        self.Bd = BUILDINGS[building]
        self.hazard = hazard

    # the ground
    def rock(self, x, y, z):
        a = _at(ROCK_A, x, z) * 0.7 + ((x * 7 + y * 13 + z * 5) % 11) / 11 * 0.3
        if _at(ROCK_B, x + y * 3, z + y * 2) > 0.72:
            return (B.COBBLE, 0)
        return (B.STONE, 5) if a < 0.42 else (B.STONE, 0)

    def crust(self, x, z):
        v = _at(ASH, x, z)
        if v < 0.22:
            return self.C[0]
        if v > 0.8:
            return self.C[3]
        return self.C[1] if _hash(x, 0, z) < 0.5 else self.C[2]

    def cut_floor(self, x, z):
        k = ((x // 3) * 7 + (z // 3) * 13 + (x // 3) * (z // 3)) % 3
        return [(B.STONE, 5), (B.GRAVEL, 0), (B.STONE, 0)][k]

    tunnel_floor = cut_floor

    def lump(self, x, z, v):
        return (B.COBBLE, 0) if v == 2 else (B.SLAB, 3)

    def stair(self, x, z, data):
        return (B.STONEBRICK_STAIRS, data)

    def spoil(self, x, y, z):
        return [(B.DIRT, 1), (B.DIRT, 0)][(x * 3 + z + y) % 2]

    def seam(self, x, y, z):
        return (B.NETHERRACK, 0)

    # the made things
    def panel(self, x, y, z, role, shade):
        return pick(self.P[role], x, y, z)

    def plate(self, x, y, z, role):
        return (B.IRON_BLOCK, 0) if role == "plate" else (B.DSLAB, 0)

    def building(self, x, y, z, role):
        return pick(self.Bd[role], x, y, z)

    def door(self, x, y, z, role):
        if self.hazard:
            return HAZARD[(y + x + z) % 2]
        return pick(self.Bd[role], x, y, z)

    def chimney(self, x, y, z, role):
        return pick(self.Bd[role], x, y, z)

    def timber(self, role):
        return (B.SPRUCE_FENCE, 0) if role == "post" else (B.PLANKS, 1)

    def light(self):
        return (B.GLOWSTONE, 0)


LOOK = Look(panels="dark steel", building="brick works", crust="gravel ash")


def paint_rock(w, look=LOOK):
    """Every block of plain stone in the world turned into the rock set, course by course."""
    xs = np.arange(w.x0, w.x0 + w.sx) % W
    zs = np.arange(w.z0, w.z0 + w.sz) % H
    XI, ZI = np.meshgrid(xs, zs, indexing="ij")
    a0 = ROCK_A[XI, ZI] * 0.7
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
