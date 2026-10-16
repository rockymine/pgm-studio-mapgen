"""The two seasons Thawline is made of, and the one way every place is built twice.

**The ground is one; the season is per half.** Every place is written once, in Frost's coordinates, through a
`Side`. Frost's side writes it where it is drawn, in Frost's materials; Ember's writes its image under the half turn,
(x, z) -> (-1 - x, -1 - z), each block's data turned with it, in Ember's. So the two halves are the same ground and
the same buildings, block for block, and differ only in what they are made of.

**A material is named by its role, never by its block.** `side.m("wall")` is stone brick in Frost and brick in
Ember; a place asks for a role, and the palette answers for the season.

**The season also runs across each half.** `depth` is how far a column lies from the Thawline, 0 at the rift and
1 at the board's back. Frost's front is autumn under the first snow and its back deep winter; Ember's front still
carries a frost in the shade and its back is a charcoal burners' country, burnt and burning.
"""
import numpy as np

from pgmvox.core.blocks import B
from pgmvox.core.orient import turn_data

ICE_PLAINS, MESA, SAVANNA = 12, 37, 35

PALETTES = {
    "frost": {
        # built: grey stone and spruce, a dark roof under snow, cold light
        "wall": [(B.STONEBRICK, 0), (B.STONEBRICK, 0), (B.STONE, 6)],
        "wall_dark": (B.STONE, 6),
        "trim": (B.STONEBRICK, 3),
        "plinth": (B.STONE, 6),
        "stair": B.STONEBRICK_STAIRS,
        "slab": (B.SLAB, 5),
        "planks": (B.PLANKS, 1),
        "log": (B.LOG, 1),
        "fence": (B.SPRUCE_FENCE, 0),
        "wood_stair": B.SPRUCE_STAIRS,
        "wood_slab": (B.WOOD_SLAB, 1),
        "roof": (B.PLANKS, 5),
        "light": (B.SEA_LANTERN, 0),
        "beacon": (B.SEA_LANTERN, 0),
        "accent": (B.PACKED_ICE, 0),
        "glass": (B.STAINED_GLASS, 3),
        "pane": (B.STAINED_PANE, 3),
        "team_clay": (B.STONE, 4),
        "floor": [(B.STONEBRICK, 0), (B.STONE, 6), (B.STONE, 5), (B.STONE, 0)],
        "inlay": (B.QUARTZ, 0),
        "inlay2": (B.STONE, 4),
        "path": [(B.GRAVEL, 0), (B.STONE, 5), (B.COBBLE, 0)],
        "yard": (B.HAY, 0),
        "dome": [(B.COBBLE, 0), (B.STONE, 5), (B.STONE, 0), (B.STONE, 5)],
        "dome_core": (B.PACKED_ICE, 0),
        "spire": [(B.PACKED_ICE, 0)],
        "spire_cap": (B.SEA_LANTERN, 0),
        "banner": 12,                                   # light blue, in the banner's own numbering
    },
    "ember": {
        # built: brick and acacia, red roofs, warm light and open fire
        "wall": [(B.BRICK, 0), (B.BRICK, 0), (B.STONE, 2)],
        "wall_dark": (B.BRICK, 0),
        "trim": (B.RED_SANDSTONE, 1),
        "plinth": (B.STONE, 2),
        "stair": B.BRICK_STAIRS,
        "slab": (B.SLAB, 4),
        "planks": (B.PLANKS, 4),
        "log": (B.LOG2, 1),
        "fence": (B.DARK_OAK_FENCE, 0),
        "wood_stair": B.DARK_OAK_STAIRS,
        "wood_slab": (B.WOOD_SLAB, 5),
        "roof": (B.BRICK, 0),
        "light": (B.GLOWSTONE, 0),
        "beacon": (B.NETHERRACK, 0),
        "accent": (B.COAL_BLOCK, 0),
        "glass": (B.STAINED_GLASS, 1),
        "pane": (B.STAINED_PANE, 1),
        "team_clay": (B.STAINED_CLAY, 1),
        "floor": [(B.STONE, 2), (B.STONE, 1), (B.STONE, 2), (B.STONE, 1)],
        "inlay": (B.BRICK, 0),
        "inlay2": (B.RED_SANDSTONE, 2),
        "path": [(B.DIRT, 1), (B.DIRT, 0), (B.PLANKS, 1)],
        "yard": (B.PUMPKIN, 0),
        "dome": [(B.DIRT, 1), (B.DIRT, 2), (B.DIRT, 1), (B.DIRT, 0)],
        "dome_core": (B.COAL_BLOCK, 0),
        "spire": [(B.COAL_BLOCK, 0), (B.STAINED_CLAY, 15), (B.OBSIDIAN, 0)],
        "spire_cap": (B.NETHERRACK, 0),
        "banner": 14,                                   # orange
    },
}

HOUSE_STYLES = {
    # the library's house: ground storey and upper walls, posts and laid courses of log, gable, roof, door, window
    "frost": dict(ground=[(B.STONEBRICK, 0), (B.STONEBRICK, 0), (B.STONE, 6)], upper=[(B.PLANKS, 1)], post=1,
                  gable=(B.PLANKS, 1), floor=(B.PLANKS, 1), roof=(B.PLANKS, 5), stair=None,
                  slab=None, door=B.SPRUCE_DOOR, window=(B.STAINED_PANE, 3), chimney=(B.STONEBRICK, 0),
                  chimney_cap=(B.COBBLE_WALL, 0)),
    "ember": dict(ground=[(B.BRICK, 0)], upper=[(B.PLANKS, 4)], post=0, gable=(B.PLANKS, 4), floor=(B.PLANKS, 5),
                  roof=(B.PLANKS, 5), stair=B.DARK_OAK_STAIRS, slab=(B.WOOD_SLAB, 5), door=B.DARK_OAK_DOOR,
                  window=(B.STAINED_PANE, 1), chimney=(B.BRICK, 0), chimney_cap=(B.NETHER_FENCE, 0)),
}


class Side:
    """One half's way of building: where a Frost coordinate lands, how a block's data turns, and the palette."""

    def __init__(self, name):
        self.name = name
        self.ember = name == "ember"
        self.pal = PALETTES[name]
        self.house = HOUSE_STYLES[name]

    def c(self, x, z):
        """A block in Frost's coordinates, on this side."""
        return (-1 - x, -1 - z) if self.ember else (x, z)

    def p(self, x, z):
        """A point between blocks (a centre, a heading's origin) on this side: the half turn about the board's middle."""
        return (-x, -z) if self.ember else (x, z)

    def heading(self, h):
        return (h + 180) % 360 if self.ember else h

    def dir(self, d):
        return {"n": "s", "s": "n", "e": "w", "w": "e"}[d] if self.ember else d

    def data(self, bid, d):
        return turn_data(bid, d, "half") if self.ember else d

    def m(self, role, rng=None):
        v = self.pal[role]
        if isinstance(v, list):
            return v[int(rng.integers(len(v)))] if rng is not None else v[0]
        return v

    def set(self, w, x, y, z, bid, d=0):
        """Set a block given in Frost's coordinates and Frost's facing."""
        x, z = self.c(x, z)
        w.set(x, y, z, bid, self.data(bid, d))

    def get(self, w, x, y, z):
        x, z = self.c(x, z)
        return w.get(x, y, z)


SIDES = (Side("frost"), Side("ember"))


def depth_field(X, Z, rng_noise):
    """How far each column lies from the Thawline toward its own back, 0 at the rift and 1 at the board's back,
    bent by noise so the season's edges wander rather than run along a row."""
    d = (np.abs(Z + 0.5) - 6) / 92
    return np.clip(d + 0.06 * rng_noise, 0, 1)
