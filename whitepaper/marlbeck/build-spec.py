#!/usr/bin/env python3
"""Write Marlbeck's two authored documents.

The plan is the board — two pieces, a spawn, a monument and the build zone over the strait.
The finish is everything a plan cannot state: the shape of the ground, what it is painted with,
and what stands on it.

    python3 build-spec.py            writes marlbeck.plan.json and marlbeck.finish.json

The board is 108 x 256 blocks under rot_180, so everything here is authored for team 0 — the half
at negative Z — and the compiler fans it onto the other.
"""
import json, os, math

HERE = os.path.dirname(os.path.abspath(__file__))

# ── blocks, by the numeric ids the terrain palette takes ───────────────────────────────────────
GRASS, DIRT, STONE, COBBLE = (2, 0), (3, 0), (1, 0), (4, 0)
COARSE, PODZOL = (3, 1), (3, 2)
GRAVEL, ANDESITE, SAND = (13, 0), (1, 5), (12, 0)
MOSSY, STONEBRICK, LOG = (48, 0), (98, 0), (17, 1)


def solid(block):
    return {"kind": "solid", "id": block[0], "data": block[1]}


def depth_stack(*courses):
    """A material read downward: (block, thickness) pairs, the last one handing over to the fill."""
    return {"kind": "layered", "axis": "depth", "beyond": solid(STONE),
            "stack": {"ending": "handOver",
                      "bands": [{"thickness": t, "material": solid(b)} for b, t in courses]}}


def slope_stack(*bands):
    """The band axis that tells a hillside from a meadow: each thickness is a span of DEGREES."""
    return {"kind": "layered", "axis": "slope", "from": 0,
            "stack": {"ending": "repeat",
                      "bands": [{"thickness": deg, "material": m} for m, deg in bands]}}


# ── the one ground theme, banded by the angle of the ground rather than by its height ───────────
MOOR = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": solid(COBBLE)},
    "surface": {"enabled": True, "depth": 4, "material": slope_stack(
        # 0-24 deg — the moor itself: grass over two courses of soil
        (depth_stack((GRASS, 1), (DIRT, 2)), 24),
        # 24-40 deg — the shoulder where the fell begins to lean
        (depth_stack((COARSE, 1), (DIRT, 2)), 16),
        # 40-90 deg — the face of the scarp, which is rock
        (depth_stack((STONE, 2), (ANDESITE, 2)), 50))},
    "fill": {"kind": "voronoi", "seed": 11, "cellSize": 14, "rise": 0,
             "bands": [{"depth": 2, "material": solid(STONE)},
                       {"depth": 1, "material": solid(ANDESITE)}]},
    "wall": depth_stack((STONE, 3), (ANDESITE, 3)),
}

# ── two patches: ground somebody chose, not ground a sampler rolled ─────────────────────────────
FLASH = {                                              # the wet ground either side of the beck
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void", "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": solid(COBBLE)},
    "surface": {"enabled": True, "depth": 3, "material": depth_stack((PODZOL, 1), (COARSE, 1), (DIRT, 1))},
    "fill": solid(STONE),
    "wall": depth_stack((COARSE, 2), (DIRT, 2)),
}
WORKINGS = {                                           # the marl pit the monument stands over
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void", "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": solid(COBBLE)},
    "surface": {"enabled": True, "depth": 3, "material": depth_stack((GRAVEL, 1), (ANDESITE, 2))},
    "fill": solid(STONE),
    "wall": depth_stack((ANDESITE, 2), (STONE, 3)),
}


def ring(cx, cz, rx, rz, n=14):
    """A closed ring of n points around a centre — an ellipse, so a patch is not a rectangle."""
    return [[round(cx + rx * math.cos(2 * math.pi * i / n), 1),
             round(cz + rz * math.sin(2 * math.pi * i / n), 1)] for i in range(n)]


# ── the plan: the board ────────────────────────────────────────────────────────────────────────
plan = {
    "plan": 2,
    "meta": {"name": "Marlbeck"},
    "globals": {"cell": 2, "symmetry": "rot_180", "maxPlayers": 16, "surface": 20, "observerY": 78},
    "pieces": [
        {"id": "camp", "role": "spawn", "rect": [-7, -64, 14, 6], "surface": 21},
        {"id": "moor", "role": "piece", "rect": [-21, -58, 42, 50], "surface": 20},
    ],
    "zones": [{"id": "crossing", "rect": [-21, -8, 42, 16]}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "camp", "at": [14, 6], "facing": "back",
                    "footprint": [4, 1, 20, 10]}],
        "destroyables": [{"id": "dt-marl", "piece": "moor", "at": [30, 49], "style": "pillar-3",
                          "materials": "obsidian", "float": 4, "name": "The Marlstone"}],
    },
}

# ── the finish: the ground, its paint, and what stands on it ───────────────────────────────────
finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-06",

    "relief": {"*": {
        # `reach` is what leaves ground alone. At 0 every mark decides the whole surface and the board
        # is nothing but transition — RL5, "graded everywhere and nowhere to stand". At 45 a cell more
        # than 45 blocks from any mark falls back to `base`, which is the moor.
        "base": 20, "reach": 45, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 1.4, "scale": 24, "seed": 7},
        "marks": [
            # The break of slope down the east side: high fell, low moor, a face between them.
            # `band` holds 8 blocks either side at its own height, so both the top and the foot are flat.
            {"id": "fell", "kind": "scarp", "high": 32, "low": 20, "face": 7, "band": 8,
             "points": [[22, -114], [25, -100], [23, -84], [20, -68],
                        [22, -52], [25, -38], [23, -26]]},
            # The beck's bed. The tread is what is held flat — 8 either side, so the water's 14-block
            # width sits inside ground that is already level and its carve has nothing left to dig.
            {"id": "beck", "kind": "line", "r": 11, "tread": 8, "h": 16,
             "points": [[-42, -46], [-28, -43], [-16, -42], [-6, -44]]},
            # The shelf the monument stands on — bevelled, so it is ground rather than a pad.
            {"id": "shelf", "kind": "area", "h": 24, "bevel": 5,
             "ring": ring(-12, -67, 17, 13)},
        ],
        "pushes": [
            # The west flank lifts, so the two ways past the monument are not the same walk. The ring
            # is kept clear of the spawn camp: a room is rigid, and ground lifted against one leaves a
            # step at its door.
            {"id": "west-rise", "ring": ring(-26, -104, 11, 10), "amount": 7,
             "falloff": 10, "roughness": 2.5, "crown": 1.5, "seed": 3},
        ],
    }},

    "themes": {"moor": MOOR, "flash": FLASH, "workings": WORKINGS},
    "mapTheme": "moor",

    # Splotches beat patterns: a patch is a shape with a theme of its own.
    "addShapes": [
        {"id": "flash-w", "type": "polygon", "operation": "add", "theme": "flash",
         "vertices": ring(-28, -44, 13, 7)},
        {"id": "flash-e", "type": "polygon", "operation": "add", "theme": "flash",
         "vertices": ring(20, -45, 11, 6)},
        {"id": "pit", "type": "polygon", "operation": "add", "theme": "workings",
         "vertices": ring(-12, -67, 12, 9)},
    ],

    "dressing": {"props": [
        # A stated `level` is what stops the carve. Absent, the water line is the LOWEST surface the
        # channel crosses and every column over it is emptied down to it — DR-BANK, a straight-sided
        # wall eight courses tall where the bed ran across a slope.
        {"id": "beck-water", "kind": "water", "shape": "channel", "form": "natural",
         "level": 18, "depth": 3, "radius": 11, "edge": 0.4, "shore": 3, "shoreWander": False,
         "points": [[-42, -46], [-28, -43], [-16, -42], [-6, -44]],
         "bank": {"kind": "voronoi", "seed": 6, "cellSize": 6, "rise": 0,
                  "bands": [{"depth": 1, "material": solid(GRAVEL)},
                            {"depth": 1, "material": solid(COARSE)},
                            {"depth": 2, "material": solid(DIRT)}]}},

        # The haul road off the camp down to the workings: a stroke repaints, it does not raise.
        {"id": "haul", "kind": "stroke", "seed": 2, "style": "solid", "radius": 2.5, "coverage": 1.0,
         "points": [[0, -114], [-2, -104], [-6, -94], [-10, -84], [-12, -76]],
         "pave": {"kind": "cell", "seed": 8, "cellSize": 4, "jitter": 55, "warp": 1, "rise": 0,
                  "palette": [solid(GRAVEL), solid(COBBLE), solid(GRAVEL)]}},

        # A wood on the west rise and three boulders along the fell. Every one is placed clear of the
        # channel that claims its cells and of the goal's own clearance ring.
        *[{"id": f"t{i}", "kind": "tree", "seed": 100 + i, "x": x, "z": z,
           "form": "template", "species": "birch", "height": 9 + (i % 4)}
          for i, (x, z) in enumerate([(-33, -101), (-27, -97), (-35, -93), (-29, -89),
                                      (-37, -85), (-31, -81), (-24, -95), (-38, -99)])],
        *[{"id": f"b{i}", "kind": "boulder", "seed": 500 + i, "x": x, "z": z,
           "form": "angular", "size": 2.6, "mossy": True,
           "rock": {"kind": "voronoi", "seed": 3, "cellSize": 4, "rise": 0,
                    "bands": [{"depth": 2, "material": solid(STONE)},
                              {"depth": 1, "material": solid(ANDESITE)},
                              {"depth": 1, "material": solid(MOSSY)}]}}
          for i, (x, z) in enumerate([(30, -96), (33, -74), (27, -22)])],

        # Heath under the wood: flora is coverage over a ring, not a scatter over the board.
        {"id": "fl-heath", "kind": "flora", "seed": 31,
         "points": ring(-30, -94, 12, 11, 9),
         "spec": {"coverage": 0.32, "scale": 10, "octaves": 2,
                  "fernShare": 0.6, "flowerShare": 0.1, "flowerScale": 11, "tallShare": 0.2}},
    ]},

    "roomStyles": {"spawn": "@showcase-hall"},
    "biome": {"kind": "solid", "id": 4},
}

for name, doc in (("marlbeck.plan.json", plan), ("marlbeck.finish.json", finish)):
    with open(os.path.join(HERE, name), "w") as handle:
        json.dump(doc, handle, indent=1)
        handle.write("\n")
    print(f"wrote {name}")
