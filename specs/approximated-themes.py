#!/usr/bin/env python3
"""Terrain themes approximated from the palettes Grok stated in prose.

Grok named a theme on every layout shape and never wrote a themes registry, so nothing resolved and all
three boards paint with the built-in default. What he did state is a palette: a block-id table in
grok-ridge/THEME.md, and one line per Sandscar README. These are those palettes written as real
TerrainTheme documents. The block ids are his; the bucket structure — which block is rim, which is
surface, which is the exposed riser, how deep each band runs — is not stated anywhere and is mine.
"""

def solid(i, d=0):
    return {"kind": "solid", "id": i, "data": d}


def voronoi(seed, cell, palette):
    return {"kind": "voronoi", "seed": seed, "cellSize": cell, "palette": palette}


def layered(*pairs):
    return {"kind": "layered", "layers": [{"material": m, "thickness": t} for m, t in pairs]}


def theme(rim, rim_depth, surface, surface_depth, wall, fill, rim_edges="drop"):
    return {
        "bedrock": {"relative": True, "value": 7},
        "rimEdges": rim_edges,
        "wallOnTerrainFaces": True,
        "rim": {"material": rim, "depth": rim_depth, "enabled": True},
        "surface": {"material": surface, "depth": surface_depth, "enabled": True},
        "wall": wall,
        "wallEnabled": True,
        "fill": fill,
    }


# ── Grok Ridge — THEME.md: andesite 1:5 body, stone brick 98:0/98:1/98:3 base and trim,
#    spruce log 17:1 posts, "path mix: stone brick + andesite + cobble", "cool gray ridge stone".
RIDGE_STONE = theme(
    rim=solid(98, 3),                                             # chiselled stone brick edge
    rim_depth=2,
    surface=voronoi(1, 5, [solid(98, 0), solid(1, 5), solid(4)]),  # his stated path mix, as the ground
    surface_depth=3,
    wall=layered((solid(1, 5), 3), (solid(1, 0), 2)),              # andesite riser over stone
    fill=solid(1),
)

# The crest reads lighter, the way THEME.md's cottage floor and trim do: mossy brick over the same body.
RIDGE_CREST = theme(
    rim=solid(98, 1),
    rim_depth=2,
    surface=voronoi(2, 4, [solid(98, 0), solid(98, 1), solid(1, 6)]),
    surface_depth=3,
    wall=layered((solid(1, 6), 2), (solid(1, 5), 3)),
    fill=solid(1),
)

# ── Sandscar — README: "sandstone + endstone + birch + brick roofs".
SANDSCAR_DESERT = theme(
    rim=solid(24, 1),                                             # chiselled sandstone lip
    rim_depth=2,
    surface=voronoi(3, 5, [solid(24, 0), solid(121, 0), solid(12, 0)]),   # sandstone · end stone · sand
    surface_depth=3,
    wall=layered((solid(24, 2), 2), (solid(24, 0), 3)),           # smooth sandstone riser over sandstone
    fill=solid(24, 0),
)

# The savanna half of Sandscar Complex's stated desert→savanna progression.
SANDSCAR_SAVANNA = theme(
    rim=solid(24, 1),
    rim_depth=1,
    surface=layered((voronoi(4, 6, [solid(2, 0), solid(3, 1), solid(12, 0)]), 1), (solid(3, 0), 2)),
    surface_depth=3,
    wall=layered((solid(3, 1), 1), (solid(24, 0), 2), (solid(1, 0), 2)),
    fill=solid(1),
)

# The pit floor, one band below the desert: end stone showing through where the ground is cut deepest.
SANDSCAR_PIT = theme(
    rim=solid(24, 2),
    rim_depth=2,
    surface=voronoi(5, 4, [solid(121, 0), solid(24, 0), solid(121, 0)]),
    surface_depth=3,
    wall=layered((solid(121, 0), 2), (solid(24, 2), 3)),
    fill=solid(24, 0),
)

REGISTRY = {
    "grok-ridge": ({"ridge-stone": RIDGE_STONE, "ridge-crest": RIDGE_CREST}, "ridge-stone"),
    "sandscar": ({"sandscar-desert": SANDSCAR_DESERT}, "sandscar-desert"),
    "sandscar-complex": ({"desert": SANDSCAR_DESERT, "savanna": SANDSCAR_SAVANNA, "pit": SANDSCAR_PIT},
                         "desert"),
}


def assign(slug, shape):
    """Which theme a compiled shape takes. Grok named his themes on his own shape ids, which the compile
    does not produce, so the assignment is by the one property both documents share: the height the piece
    stands at. The bands are the ones his own names describe."""
    top = (shape.get("floor") or 0) + (shape.get("base_height") or 0)
    if slug == "grok-ridge":
        return "ridge-crest" if top >= 27 else "ridge-stone"
    if slug == "sandscar-complex":
        if top <= 37:
            return "pit"
        return "desert" if top <= 41 else "savanna"
    return None
