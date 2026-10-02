"""What a chunk is built from: its ground, its made blocks and its dressing, all in chunk-local coordinates.

A chunk is a 16 x 16 column whose terrain tops out at world y `BASE - 1`, so local y 0 is the first course a
build stands on and local y 31 the last. Negative local y is underground. x runs east and z south, 0..15.

* **Ground** is sketch shapes on the board's ground layer: the chunk's own block, raised parts (`raise_`), lowered
  parts (`lower`, an override so it cuts under the chunk's top) and, for a cave or a tunnel, a roof on the
  `upper` layer floating over a void.
* **Blocks** are made blocks, `(id, data)` per cell, compiled into `made` layers. A block inside the ground wins
  its cell, which is how a vault is lined or an ore shows on a cut face.
* **Dressing** is the studio's own trees, boulders, ground cover and water, which seat on the ground.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prop-showcase"))
from catalogue import parse, place as place_prop, PROPS  # noqa: E402

BASE = 24          # world y of local y 0
PROP = {p.name: p for p in PROPS}

# ---------------------------------------------------------------------------------------------------------
# Materials


def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


def noise(seed, *stops, scale=4):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": 2, "rise": 3, "stops": list(stops)}


def strata(top, soil, soil_depth, rock, deep):
    """The cut face of a chunk read by world height: bedrock, a deep band with ore, rock, soil and the top."""
    return {"kind": "layered", "axis": "height", "from": 0, "beyond": rock,
            "stack": {"ending": "handOver", "bands": [
                {"material": solid(7), "thickness": 1},
                {"material": deep, "thickness": BASE - 2 - soil_depth - 6},
                {"material": rock, "thickness": 6},
                {"material": soil, "thickness": soil_depth},
                {"material": top, "thickness": 1}]}}


ORE_STONE = noise(11, solid(1), solid(16), solid(1, 5), solid(1), solid(15), solid(1), solid(4), solid(16),
                  solid(1), solid(1, 5), solid(13), solid(1), solid(21), solid(1), solid(56), solid(1, 6), scale=2)
STONE = noise(12, solid(1), solid(1), solid(1, 5), solid(1), solid(4), solid(1), scale=4)


def theme(top, soil, soil_depth=4, rock=None, deep=None, rim=None, surface=None):
    """A chunk's theme: `top` on the surface, the strata down the cut sides, stone inside."""
    rock = rock or STONE
    deep = deep or ORE_STONE
    surface = surface or {"kind": "layered", "stack": {"ending": "repeat", "bands": [
        {"material": top, "thickness": 1}, {"material": soil, "thickness": 3}]}}
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "boundary",
        "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": rim or top},
        "surface": {"enabled": True, "depth": 4, "material": surface},
        "wall": strata(top, soil, soil_depth, rock, deep),
        "wallEnabled": True,
        "fill": strata(soil, soil, soil_depth, rock, deep),
    }


THEMES = {
    "grass": theme(solid(2), solid(3)),
    "forest": theme(solid(2), solid(3), surface={"kind": "layered", "stack": {"ending": "repeat", "bands": [
        {"material": noise(21, solid(2), solid(2), solid(3, 2), solid(2), solid(3, 1)), "thickness": 1},
        {"material": solid(3), "thickness": 3}]}}),
    "snow": theme(solid(80), solid(3), rock=noise(13, solid(1), solid(4), solid(1, 5), solid(1))),
    "sand": theme(solid(12), solid(24), soil_depth=6,
                  rock=noise(14, solid(24), solid(24, 2), solid(24), solid(179))),
    "rock": theme(noise(15, solid(1), solid(4), solid(1, 5), solid(13), solid(1)), solid(1, 5), soil_depth=2),
    "mud": theme(noise(16, solid(2), solid(3, 2), solid(2), solid(82)), solid(3, 1)),
    "sea-floor": theme(solid(12), solid(12), soil_depth=3, rock=solid(24)),
    "plank": {"bedrock": {"relative": False, "value": 1}, "rimEdges": "boundary", "wallOnTerrainFaces": True,
              "rim": {"enabled": True, "depth": 1, "material": solid(98)},
              "surface": {"enabled": True, "depth": 1, "material": solid(98)},
              "wall": solid(98), "wallEnabled": True, "fill": solid(1)},
}

# ---------------------------------------------------------------------------------------------------------
# The chunk


class Chunk:
    def __init__(self, name, title, theme_name, blurb=""):
        self.name = name
        self.title = title
        self.theme = theme_name
        self.blurb = blurb
        self.ground = []        # (cells, height, theme, override) — height is local, surface at BASE + h - 1
        self.upper = []         # (cells, floor, top, theme) — local y
        self.blocks = {}
        self.trees = []         # (x, z, style)
        self.boulders = []      # (x, z, form, size, mossy)
        self.flora = []         # (points, spec)

    # ground ------------------------------------------------------------------------------------------------
    def raise_(self, x0, z0, x1, z1, h, theme=None):
        """Ground over the cells x0..x1, z0..z1 (inclusive) raised to local height h (top course at h - 1)."""
        self.ground.append(((x0, z0, x1, z1), h, theme or self.theme, False))

    def lower(self, x0, z0, x1, z1, h, theme=None):
        """Ground cut down to local height h (h <= 0), whatever stands over it."""
        self.ground.append(((x0, z0, x1, z1), h, theme or self.theme, True))

    def roof(self, x0, z0, x1, z1, floor, top, theme=None):
        """Ground floating over a void from local `floor` up to `top` — a cave's or a tunnel's roof."""
        self.upper.append(((x0, z0, x1, z1), floor, top, theme or self.theme))

    # blocks ------------------------------------------------------------------------------------------------
    def set(self, x, y, z, block):
        if block is None:
            self.blocks.pop((x, y, z), None)
            return
        self.blocks[(x, y, z)] = parse(block)

    def box(self, x0, y0, z0, x1, y1, z1, block, hollow=False):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1):
                    if hollow and min(x0, x1) < x < max(x0, x1) and min(z0, z1) < z < max(z0, z1) \
                            and min(y0, y1) < y < max(y0, y1):
                        continue
                    self.set(x, y, z, block)

    def walls(self, x0, y0, z0, x1, y1, z1, block):
        """Four walls round a rectangle, no floor or ceiling."""
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.set(x, y, z0, block)
                self.set(x, y, z1, block)
            for z in range(z0, z1 + 1):
                self.set(x0, y, z, block)
                self.set(x1, y, z, block)

    def clear(self, x0, y0, z0, x1, y1, z1):
        self.box(x0, y0, z0, x1, y1, z1, None)

    def disc(self, cx, cz, r, y, block, ring=None):
        """A filled disc of radius r, or a ring `ring` thick at its edge."""
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            for z in range(int(cz - r - 1), int(cz + r + 2)):
                d = math.hypot(x - cx, z - cz)
                if d <= r + 0.3 and (ring is None or d > r - ring + 0.3):
                    self.set(x, y, z, block)

    def ascii(self, x, y, z, legend, *layers):
        """ASCII layers bottom first at (x, y, z), each row a z, each column an x; `.` and ` ` are air, `~` keeps
        what is already there."""
        legend = {key: parse(value) for key, value in legend.items()}
        for dy, block in enumerate(layers):
            for dz, row in enumerate(block.strip("\n").split("\n")):
                for dx, char in enumerate(row):
                    if char in ". ":
                        continue
                    if char == "~":
                        continue
                    if char == "_":
                        self.set(x + dx, y + dy, z + dz, None)
                        continue
                    self.blocks[(x + dx, y + dy, z + dz)] = legend[char]

    def prop(self, name, x, y, z, turns=0):
        """A prop from the prop catalogue, at its origin cell, turned."""
        for (px, py, pz), block in place_prop(PROP[name], x, y, z, turns).items():
            self.blocks[(px, py, pz)] = block

    # dressing ----------------------------------------------------------------------------------------------
    def tree(self, x, z, style):
        self.trees.append((x, z, style))

    def boulder(self, x, z, size=2, form="round", mossy=True):
        self.boulders.append((x, z, form, size, mossy))

    def cover(self, points, **spec):
        self.flora.append((points, spec))
