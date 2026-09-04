#!/usr/bin/env python3
"""Mootgate — a walled market town on each side of a void crossing, built as placed things.

Writes opus5-mootgate.plan.json and opus5-mootgate.finish.json for tools/drive.py.

The board is a lane: two towns 80 blocks wide, 76 deep, facing each other across a 28-block
build zone over void. Each town keeps a wool in its moot hall — a stamped wool-room whose shell
is a full HouseStyle — and the enemy has to come through one of three gates, up a street plan,
across the market square and over the Moot Green to reach it. The captured wool goes home to
the market cross.

Everything a player sees inside the walls is a placed thing: 18 house props per side over five
house styles, seven paved routes, a stone town wall and its stair flights authored as terrain
shapes, and a market square painted as a splotch rather than paved as a road.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-mootgate"

# ── materials ────────────────────────────────────────────────────────────────────────────────
# `kind` is read positionally and must be the first key of every material object (TL2).


def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


def noise(seed, scale, octaves, first, second, rise=0):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": octaves,
            "stops": [first, second], "rise": rise}


def voronoi(seed, cell_size, bands, rise=0):
    return {"kind": "voronoi", "seed": seed, "cellSize": cell_size, "rise": rise,
            "bands": [{"material": material, "thickness": thickness}
                      for material, thickness in bands]}


def checker(size, even, odd):
    return {"kind": "checker", "size": size, "even": even, "odd": odd}


def laid_log(block, data=0):
    return {"kind": "laidLog", "id": block, "data": data}


def layered(bands, axis="depth"):
    return {"kind": "layered", "axis": axis,
            "stack": {"bands": [{"material": material, "thickness": thickness}
                                for material, thickness in bands],
                      "ending": "repeat"}}


def stack(bands, extent):
    return {"stack": {"bands": [{"material": material, "thickness": thickness}
                                for material, thickness in bands],
                      "ending": "repeat"},
            "extent": extent}


GRASS = solid(2, 0)
DIRT = solid(3, 0)
COARSE = solid(3, 1)
STONE = solid(1, 0)
ANDESITE = solid(1, 5)
COBBLE = solid(4, 0)
MOSSY_COBBLE = solid(48, 0)
GRAVEL = solid(13, 0)
STONEBRICK = solid(98, 0)
MOSSYBRICK = solid(98, 1)
CHISELBRICK = solid(98, 3)
BRICK = solid(45, 0)
PLASTER = solid(159, 0)          # white stained clay — whitewash, a stated colour on a wall
SPRUCE = solid(5, 1)
BIRCH = solid(5, 2)
DARKOAK = solid(5, 5)
OAKLOG = solid(17, 0)
SPRUCELOG = solid(17, 1)
DARKOAKLOG = solid(162, 1)

# ── the three themes ─────────────────────────────────────────────────────────────────────────
# ground: grass over dirt over stone.  built: the town wall's stone brick.  hard standing: the
# square and the worn yards, a two-block grey.  Nothing else is painted; the buildings carry the
# rest, which is the point of the board.


def theme(surface_material, surface_depth, wall_material, fill_material,
          rim_material=None, rim_depth=1):
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void",
        "wallOnTerrainFaces": True,
        "rim": {"material": rim_material or STONE, "depth": rim_depth,
                "enabled": rim_material is not None},
        "surface": {"material": surface_material, "depth": surface_depth, "enabled": True},
        "wall": wall_material,
        "wallEnabled": True,
        "fill": fill_material,
    }


THEMES = {
    # The vale: one ground for the whole board, and the only one the relief solves through.
    # The rim is on because every edge of this board is a made edge — land over void.
    "vale": theme(
        layered([(GRASS, 1), (DIRT, 3)]), 4,
        layered([(DIRT, 2), (COBBLE, 1), (STONE, 8)]),
        voronoi(19, 11, [(STONE, 3), (ANDESITE, 1), (STONE, 4)], rise=6),
        rim_material=STONE, rim_depth=1),

    # Hard standing: the market square and the worn yards. Two greys of one shade at a brush
    # three times the size of the thing it dresses, so it reads as trodden ground, not static.
    "cobbles": theme(
        layered([(noise(23, 11, 2, GRAVEL, COBBLE), 2), (COARSE, 2)]), 3,
        layered([(COBBLE, 2), (STONE, 6)]),
        solid(1, 0)),

    # The rampart: the town wall, its stair flights, the gate towers, the market cross and the
    # wool stone. One family, weathered by a two-block field at a wall-sized period.
    "rampart": theme(
        noise(29, 9, 2, STONEBRICK, MOSSYBRICK), 2,
        noise(31, 7, 2, STONEBRICK, MOSSYBRICK),
        solid(4, 0)),
}

# ── the house styles ─────────────────────────────────────────────────────────────────────────
# Three families, named before anything was painted: the ground is green and grey (grass, dirt,
# gravel, cobble); the buildings are whitewash and dark timber over a cobble plinth, roofed in
# brick and shingle; the accent is the civic stone brick of the wall, the moot hall and the
# market cross.  No building is walled in the ground's own family.


def window(form, block, data=0, sill=2, width=2, height=2, spacing=3, host=-1, host_data=0):
    return {"form": form, "block": block, "hostBlock": host, "hostData": host_data,
            "data": data, "sill": sill, "width": width, "height": height, "spacing": spacing}


NO_WINDOW = window("none", 102)


def storey(clear, wall, post, windows, headroom=None, deck=None):
    return {"clear": clear, "wall": wall, "post": post, "windows": windows,
            "surface": {"field": None, "border": None, "borderWidth": 1,
                        "inlay": None, "inlayInset": 2, "isPlain": True},
            "deck": deck, "headroom": headroom if headroom is not None else clear}


def foundation(plate_material, extent, footing=None):
    return {"plate": stack([(plate_material, 1)], extent),
            "surface": {"field": None, "border": None, "borderWidth": 1,
                        "inlay": None, "inlayInset": 2, "isPlain": True},
            "footing": footing}


def roof(form, body, verge, gable=None, pitch=1, slab=-1, slab_data=0, overhang=1,
         ridge_cap=True, hole=False, gable_windows=None):
    return {"form": form, "pitch": pitch, "slab": slab, "slabData": slab_data,
            "overhang": overhang, "ridgeCap": ridge_cap, "hole": hole,
            "body": body, "verge": verge, "gable": gable,
            "gableWindows": gable_windows or NO_WINDOW}


def doorway(door, head_block, fill_block, fill_data, width=2, height=3, form="arched"):
    return {"door": door,
            "head": {"form": form, "block": head_block, "fill": "upperSlab",
                     "fillBlock": fill_block, "fillData": fill_data},
            "width": width, "height": height}


# The croft: one storey, whitewash between dark posts on a cobble plinth, shingled in spruce.
CROFT = {
    "foundation": foundation(COBBLE, 2, footing=COBBLE),
    "roof": roof("gable", SPRUCE, DARKOAK, gable=PLASTER,
                 gable_windows=window("open", 102, sill=1, width=1, height=1, spacing=3)),
    "wall": stack([(COBBLE, 1), (PLASTER, 4)], 5),
    "post": DARKOAKLOG,
    "windows": window("pane", 102, sill=2, width=2, height=2, spacing=3),
    "storeys": [storey(4, stack([(COBBLE, 1), (PLASTER, 3)], 4), DARKOAKLOG,
                       window("pane", 102, sill=2, width=2, height=2, spacing=3))],
    "porch": None,
    "front": None,
    "beams": {"block": -1, "data": 0, "reach": 1, "any": False},
    "doorway": doorway("air", 164, 126, 5),
}

# The townhouse: two storeys, a stone ground floor under a half-timbered jetty, brick roof.
TOWNHOUSE = {
    "foundation": foundation(STONEBRICK, 2, footing=COBBLE),
    "roof": roof("gable", BRICK, DARKOAK, gable=PLASTER,
                 gable_windows=window("open", 102, sill=1, width=1, height=1, spacing=3)),
    "wall": stack([(COBBLE, 2), (PLASTER, 3)], 5),
    "post": DARKOAKLOG,
    "windows": window("pane", 102, sill=2, width=2, height=2, spacing=3),
    "storeys": [
        storey(4, stack([(COBBLE, 2), (STONEBRICK, 2)], 4), DARKOAKLOG,
               window("arched", 109, sill=2, width=2, height=2, spacing=3)),
        storey(4, stack([(PLASTER, 1), (checker(1, PLASTER, DARKOAK), 3)], 4), DARKOAKLOG,
               window("pane", 102, sill=1, width=2, height=2, spacing=3)),
    ],
    "porch": None,
    "front": None,
    "beams": {"block": 162, "data": 1, "reach": 1, "any": True},
    "doorway": doorway("air", 164, 126, 5),
}

# The store: a granary, one tall windowless volume under a shed roof, boarded in spruce with a
# laid-log eaves course.
STORE = {
    "foundation": foundation(STONEBRICK, 2, footing=None),
    "roof": roof("shed", DARKOAK, SPRUCE, gable=SPRUCE, overhang=1, ridge_cap=False),
    "wall": stack([(STONEBRICK, 2), (SPRUCE, 4), (laid_log(17, 1), 1)], 7),
    "post": SPRUCELOG,
    "windows": NO_WINDOW,
    "storeys": [storey(6, stack([(STONEBRICK, 2), (SPRUCE, 4), (laid_log(17, 1), 1)], 7),
                       SPRUCELOG,
                       window("slabBanded", 44, data=5, sill=4, width=2, height=3, spacing=5))],
    "porch": None,
    "front": None,
    "beams": {"block": -1, "data": 0, "reach": 1, "any": False},
    "doorway": doorway("air", 134, 126, 1, width=3, height=4),
}

# The forge: low, brick over cobble, hip roof stepped in brick slab, with an open working porch.
FORGE = {
    "foundation": foundation(COBBLE, 2, footing=COBBLE),
    "roof": roof("hip", BRICK, DARKOAK, gable=None, pitch=1, slab=44, slab_data=4,
                 overhang=1, ridge_cap=False),
    "wall": stack([(COBBLE, 2), (BRICK, 3)], 5),
    "post": STONEBRICK,
    "windows": window("slabBanded", 44, data=5, sill=2, width=2, height=3, spacing=4),
    "storeys": [storey(4, stack([(COBBLE, 2), (BRICK, 2)], 4), STONEBRICK,
                       window("slabBanded", 44, data=5, sill=2, width=2, height=3, spacing=4))],
    "porch": {"depth": 2, "inset": 1, "edge": None, "roof": "shed", "railBlock": 0},
    "front": None,
    "beams": {"block": -1, "data": 0, "reach": 1, "any": False},
    "doorway": doorway("air", 108, 44, 4, width=3, height=4),
}

# The stall: a market shed, one low course of whitewash under a shingle lean-to over a railed
# deck. The smallest thing this board can say — DR-SIZE stops anything under 5x5.
STALL = {
    "foundation": foundation(COBBLE, 1, footing=None),
    "roof": roof("shed", SPRUCE, DARKOAK, gable=PLASTER, overhang=1, ridge_cap=False),
    "wall": stack([(PLASTER, 3)], 3),
    "post": OAKLOG,
    "windows": window("open", 102, sill=1, width=2, height=2, spacing=2),
    "storeys": [storey(3, stack([(PLASTER, 3)], 3), OAKLOG,
                       window("open", 102, sill=1, width=2, height=2, spacing=2))],
    "porch": {"depth": 2, "inset": 0, "edge": None, "roof": "shed", "railBlock": 85},
    "front": None,
    "beams": {"block": -1, "data": 0, "reach": 1, "any": False},
    "doorway": doorway("air", 164, 126, 5, width=2, height=3),
}

# The moot hall: the wool room's own shell. Civic stone brick, arched windows, a hip roof stepped
# in stone-brick slab, and cobweb in all four doorways, which is what the room's break rule takes.
HALL = {
    "foundation": foundation(STONEBRICK, 3, footing=STONEBRICK),
    "roof": roof("hip", BRICK, STONEBRICK, gable=None, pitch=1, slab=44, slab_data=4,
                 overhang=1, ridge_cap=False),
    "wall": stack([(STONEBRICK, 2), (MOSSYBRICK, 1), (STONEBRICK, 3)], 6),
    "post": CHISELBRICK,
    "windows": window("arched", 109, sill=3, width=2, height=3, spacing=4),
    "storeys": [storey(5, stack([(STONEBRICK, 2), (MOSSYBRICK, 1), (STONEBRICK, 2)], 5),
                       CHISELBRICK,
                       window("arched", 109, sill=3, width=2, height=3, spacing=4))],
    "porch": None,
    "front": None,
    "beams": {"block": -1, "data": 0, "reach": 1, "any": False},
    "doorway": doorway("web", 109, 44, 5, width=3, height=4),
}

# The barracks: the spawn cube. Cobble to head height under stone brick, gable roof in shingle.
BARRACKS = {
    "foundation": foundation(STONEBRICK, 2, footing=COBBLE),
    "roof": roof("gable", SPRUCE, DARKOAK, gable=STONEBRICK,
                 gable_windows=window("open", 102, sill=1, width=1, height=1, spacing=3)),
    "wall": stack([(COBBLE, 2), (STONEBRICK, 4)], 6),
    "post": DARKOAKLOG,
    "windows": window("arched", 109, sill=2, width=2, height=3, spacing=4),
    "storeys": [storey(5, stack([(COBBLE, 2), (STONEBRICK, 3)], 5), DARKOAKLOG,
                       window("arched", 109, sill=2, width=2, height=3, spacing=4))],
    "porch": None,
    "front": None,
    "beams": {"block": -1, "data": 0, "reach": 1, "any": False},
    "doorway": doorway("air", 109, 44, 5, width=3, height=4),
}

# ── the plan ─────────────────────────────────────────────────────────────────────────────────
# cell 2, so a cell rect [x, z, w, h] covers blocks [2x .. 2(x+w)) x [2z .. 2(z+h)).
CELL = 2
SURFACE = 14

PIECES = [
    # the field between the crossing and the town gate — no-man's land, and the only wood
    {"id": "field", "role": "piece", "rect": [-20, 7, 40, 6]},
    # the town: one piece under the whole walled area, so the street plan is dressing, not plan
    {"id": "town", "role": "piece", "rect": [-20, 13, 40, 22], "surface": 15},
    {"id": "back-w", "role": "piece", "rect": [-20, 35, 4, 7], "surface": 15},
    {"id": "moot", "role": "wool-room", "rect": [-16, 35, 9, 7], "surface": 15},
    {"id": "mid-back", "role": "piece", "rect": [-7, 35, 15, 7], "surface": 15},
    {"id": "barrack", "role": "spawn", "rect": [8, 35, 8, 7], "surface": 15},
    {"id": "back-e", "role": "piece", "rect": [16, 35, 4, 7], "surface": 15},
    # the strip behind the wall, so both rooms have land on all four sides
    {"id": "rear", "role": "piece", "rect": [-20, 42, 40, 3], "surface": 15},
]

ZONES = [
    {"id": "crossing", "rect": [-20, -7, 40, 14], "holes": []},
]

PLAN = {
    "plan": 2,
    "meta": {"name": "Mootgate"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 24, "surface": SURFACE},
    "pieces": PIECES,
    "zones": ZONES,
    "placements": {
        # `at` and `footprint` are blocks from the piece's minimum corner (plan version 2).
        "spawns": [{"id": "spawn-1", "piece": "barrack", "at": [8, 7], "facing": "left",
                    "footprint": [2, 3, 12, 8]}],
        "wools": [{"id": "wool-1", "piece": "moot", "at": [9, 7], "footprint": [3, 3, 12, 8]}],
        "iron": [],
        "destroyables": [],
        "cores": [],
    },
    "walls": [],
    "boxes": [],
}

# ── the town, in blocks ──────────────────────────────────────────────────────────────────────
# The town runs x -40..40, z 26..90; the wall ring stands three blocks thick inside it, with the
# main gate and two posterns cut through its front face.  Every made thing here is terrain: an
# override add that owns its column, stands out of the relief and is ground the dressing pass
# must leave alone.
WALL_TOP = 23          # base_height, so the wall walk's top block is y22 over ground at y14
TOWER_TOP = 27
GROUND_TOP = 16        # the foot of a flight, one step up off the town's own surface


def made(shape_id, min_x, min_z, max_x, max_z, height, theme_id="rampart"):
    return {"id": shape_id, "type": "rectangle", "operation": "add", "override": True,
            "keepClear": True, "min_x": min_x, "min_z": min_z, "max_x": max_x, "max_z": max_z,
            "floor": 0, "base_height": height, "height_mode": "level", "skirt": 0,
            "relief_scope": "exclude", "theme": theme_id}


def flight(shape_id, min_x, max_x, high_z, low_z, high, low, theme_id="rampart"):
    """A stair as one tilted quad. The run is at least twice the rise or it walks as a wall."""
    return {"id": shape_id, "type": "polygon", "operation": "add", "override": True,
            "keepClear": True,
            "vertices": [[min_x, high_z], [max_x, high_z], [max_x, low_z], [min_x, low_z]],
            "anchor_heights": [high, high, low, low],
            "floor": 0, "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
            "theme": theme_id}


def patch(shape_id, min_x, min_z, max_x, max_z, theme_id):
    """A splotch: one course, no override, so the taller add keeps the height and the smallest
    themed shape covering a cell keeps the colour."""
    return {"id": shape_id, "type": "rectangle", "operation": "add",
            "min_x": min_x, "min_z": min_z, "max_x": max_x, "max_z": max_z,
            "floor": 0, "base_height": 1, "theme": theme_id}


ADD_SHAPES = []

# The town wall — a ring three blocks thick with three gaps cut in its front face.  A rectangle
# covers [min, max), so wall-w owns x -36..-34 and the first free column inside it is x -33.
ADD_SHAPES += [
    made("wall-s-w", -36, 29, -24, 32, WALL_TOP),
    made("wall-s-cw", -18, 29, -5, 32, WALL_TOP),
    made("wall-s-ce", 5, 29, 18, 32, WALL_TOP),
    made("wall-s-e", 24, 29, 36, 32, WALL_TOP),
    made("wall-w", -36, 29, -33, 88, WALL_TOP),
    made("wall-e", 33, 29, 36, 88, WALL_TOP),
    made("wall-n", -36, 85, 36, 88, WALL_TOP),
    # the gate towers, four courses over the wall walk, flanking the main gate
    made("tower-w", -9, 27, -5, 35, TOWER_TOP),
    made("tower-e", 5, 27, 9, 35, TOWER_TOP),
]

# Two flights onto the wall walk, one either side of the main gate: 16 blocks of run for 7
# courses of rise, which is the 2:1 a flight has to keep to walk at all.
ADD_SHAPES += [
    flight("stair-w", -11, -7, 33, 49, WALL_TOP, GROUND_TOP),
    flight("stair-e", 7, 11, 33, 49, WALL_TOP, GROUND_TOP),
]

# The market cross: three steps and a shaft at the middle of the square, and the wool stone
# beside it — the block a captured wool is carried home to.
ADD_SHAPES += [
    made("cross-1", -3, 47, 4, 54, 16),
    made("cross-2", -2, 48, 3, 53, 17),
    made("cross-3", -1, 49, 2, 52, 18),
    made("cross-shaft", 0, 50, 1, 51, 25),
    made("wool-stone", 7, 47, 10, 50, 16),
    # the town well: a ring two courses proud round one open column
    made("well-n", -5, 56, -2, 57, 17),
    made("well-s", -5, 58, -2, 59, 17),
    made("well-w", -5, 57, -4, 58, 17),
    made("well-e", -3, 57, -2, 58, 17),
]

# The hard standing: the square, the avenue the moot hall's doors open onto — which has to be
# paint rather than paving, because a route laid in a door's approach is declined — and four
# worn yards.
ADD_SHAPES += [
    patch("sq-market", -11, 47, 11, 61, "cobbles"),
    patch("sq-moot", -31, 61, -15, 73, "cobbles"),
    patch("yard-gate", -9, 33, 9, 40, "cobbles"),
    patch("yard-w", -33, 41, -25, 46, "cobbles"),
    patch("yard-e", 20, 41, 31, 46, "cobbles"),
    patch("yard-n", -12, 62, 14, 71, "cobbles"),
]

# ── the relief ───────────────────────────────────────────────────────────────────────────────
# Nearly flat, which is what a board made of placed things needs: the town is one course over the
# field so the wall's footing reads, and the only shape in the ground is two knolls and a hollow
# in the field, where the fighting before the gate happens.
RELIEF = {
    "*": {
        "base": SURFACE,
        "reach": 24,
        "step": 1,
        "stairs": False,
        "grain": {"amplitude": 0.6, "scale": 17, "seed": 7},
        "marks": [
            {"id": "town-pad", "kind": "area",
             "ring": [[-40, 27], [40, 27], [40, 90], [-40, 90]], "h": 15},
            {"id": "knoll-w", "kind": "point", "at": [-31, 21], "h": 17, "r": 8},
            {"id": "mere-pan", "kind": "point", "at": [-33, 20], "h": 12, "r": 5},
            {"id": "swell-e", "kind": "point", "at": [37, 20], "h": 16, "r": 6},
        ],
    }
}

# ── the dressing ─────────────────────────────────────────────────────────────────────────────
# The recipes are stated once in the registry and every placement names one, which is what makes
# repainting a whole street of houses one edit rather than eighteen.
#
# Three numbers this board was re-laid against, all read off 06-claims.txt and the declines of
# the first build: two buildings need FOUR blocks between footprints (a roof overhang each and a
# block of structure clearance); a footprint may not include a keepClear column, so a house
# stands two blocks off the town wall's inner face; and a wing is at least 4x4 (HP2) inside a
# building that is at least 5x5 (DR-SIZE).

PAVE = noise(21, 9, 2, COBBLE, GRAVEL)

STYLES = {
    "croft": {"kind": "house", "shell": CROFT},
    "townhouse": {"kind": "house", "shell": TOWNHOUSE},
    "store": {"kind": "house", "shell": STORE},
    "forge": {"kind": "house", "shell": FORGE},
    "stall": {"kind": "house", "shell": STALL},
    "oak-med": {"kind": "tree", "form": "template", "species": "oak", "height": 9},
    "oak-tall": {"kind": "tree", "form": "template", "species": "oak", "height": 12},
    "birch": {"kind": "tree", "form": "template", "species": "birch", "height": 8},
    "erratic": {"kind": "boulder", "form": "angular", "size": 2.4, "mossy": True,
                "rock": noise(33, 6, 1, STONE, COBBLE, rise=3)},
    "erratic-big": {"kind": "boulder", "form": "outcrop", "size": 3.2, "mossy": True,
                    "rock": noise(33, 6, 1, STONE, COBBLE, rise=3)},
}


def house(prop_id, style, corners, front, seed, extra_wings=None, spec=None):
    wings = [{"corners": corners, **({"spec": spec} if spec else {})}]
    for wing_corners, wing_spec in (extra_wings or []):
        wings.append({"corners": wing_corners, "spec": wing_spec})
    return {"id": prop_id, "kind": "house", "seed": seed, "front": front,
            "style": style, "wings": wings}


def route(prop_id, points, radius, seed, style="solid", pave=None, is_route=True,
          coverage=1.0):
    return {"id": prop_id, "kind": "stroke", "seed": seed, "style": style, "radius": radius,
            "coverage": coverage, "pave": pave or PAVE, "claimsGround": is_route, "points": points}


def tree(prop_id, style, x, z, seed):
    return {"id": prop_id, "kind": "tree", "seed": seed, "x": x, "z": z, "style": style}


def boulder(prop_id, style, x, z, seed):
    return {"id": prop_id, "kind": "boulder", "seed": seed, "x": x, "z": z, "style": style}


# The routes go down first: a building may end a road and never stand across one.  Four streets
# and no more — the square, the moot avenue and the yards are paint, and the town reads as three
# gates feeding three lanes into one cross street.
STROKES = [
    route("st-gate", [[0, 22], [0, 28], [0, 34], [0, 42]], 2.5, 101),
    route("st-market", [[-28, 44], [-10, 44], [10, 44], [28, 44]], 2.5, 102),
    route("st-postern-w", [[-21, 22], [-21, 30], [-21, 37], [-21, 43]], 2.0, 103),
    route("st-postern-e", [[21, 22], [21, 30], [21, 37], [21, 43]], 2.0, 104),
]

HOUSES = [
    # the row inside the front wall, fronting Market Row
    house("h-south-a", "croft", [[-32, 34], [-26, 40]], "posZ", 11),
    house("h-south-b", "townhouse", [[-17, 34], [-13, 40]], "posZ", 12),
    house("h-south-d", "croft", [[13, 34], [17, 40]], "posZ", 14),
    house("h-south-f", "forge", [[25, 34], [31, 40]], "posZ", 16),
    # the west quarter: a cottage along the wall, and the granary — an L of hall and wing
    house("h-west-g", "croft", [[-32, 47], [-28, 60]], "posX", 21),
    house("h-granary", "store", [[-23, 47], [-15, 56]], "negX", 22,
          extra_wings=[([[-23, 57], [-19, 61]], {"ridge": "alongZ"})],
          spec={"ridge": "alongX"}),
    # the east quarter: the inn, an L turned the other way, and a cottage along the wall
    house("h-inn", "townhouse", [[12, 47], [18, 56]], "negX", 23,
          extra_wings=[([[19, 50], [22, 56]], {"ridge": "alongX"})],
          spec={"ridge": "alongZ"}),
    house("h-east-k", "croft", [[27, 47], [31, 58]], "negX", 24),
    # the market stalls on the square, either side of the cross
    house("h-stall-a", "stall", [[-11, 48], [-7, 52]], "posX", 31),
    house("h-stall-b", "stall", [[-11, 56], [-7, 60]], "posX", 32),
    house("h-stall-c", "stall", [[3, 56], [7, 60]], "negX", 33),
    # the back of the town, between the moot hall's green and the barracks' apron
    house("h-reeve", "townhouse", [[-3, 64], [5, 70]], "negZ", 41),
    house("h-back-e", "croft", [[22, 62], [29, 68]], "negZ", 42),
    house("h-guild", "townhouse", [[12, 62], [18, 68]], "negZ", 43),
    # outside the walls: a steading, the tithe barn, a wayside chapel and a cot
    house("h-steading", "store", [[-17, 18], [-11, 25]], "posX", 51),
    house("h-barn", "store", [[24, 17], [30, 24]], "negX", 52),
    house("h-chapel", "croft", [[4, 18], [8, 24]], "negX", 53),
    house("h-cot", "croft", [[13, 18], [17, 24]], "negX", 54),
]

WATER = [
    # the mere in the hollow west of the road, the one place on the board water can stand
    {"id": "w-mere", "kind": "water", "seed": 61, "shape": "pool",
     "points": [[-36, 18], [-32, 17], [-30, 21], [-33, 24], [-37, 23]],
     "radius": 2.0, "depth": 2.0},
]

BOULDERS = [
    boulder("b-field-a", "erratic", -26, 17, 71),
    boulder("b-field-b", "erratic", -6, 20, 72),
    boulder("b-field-c", "erratic-big", 36, 24, 73),
    boulder("b-berm-w", "erratic", -38, 36, 74),
    boulder("b-berm-e", "erratic", 38, 36, 75),
    boulder("b-berm-e2", "erratic", 38, 68, 76),
    boulder("b-berm-w2", "erratic", -38, 68, 78),
]

TREES = [
    tree("t-wood-a", "oak-tall", -26, 24, 81),
    tree("t-wood-b", "oak-med", -30, 25, 82),
    tree("t-wood-c", "birch", -6, 25, 83),
    tree("t-wood-d", "oak-med", -12, 15, 84),
    tree("t-field-w", "birch", -20, 15, 93),
    tree("t-field-c", "oak-med", 17, 15, 94),
    tree("t-hedge-a", "birch", 34, 17, 85),
    tree("t-hedge-b", "oak-med", 31, 27, 86),
    tree("t-hedge-c", "birch", 12, 15, 87),
    tree("t-berm-w", "oak-med", -38, 50, 88),
    tree("t-berm-w2", "birch", -38, 64, 89),
    tree("t-berm-e", "oak-med", 38, 50, 90),
    tree("t-berm-e2", "oak-med", 38, 80, 97),
    tree("t-green-a", "oak-tall", -32, 64, 91),
    tree("t-green-b", "oak-med", -14, 65, 92),
    tree("t-yard-n", "oak-tall", 9, 65, 98),
]

FLORA = [
    {"id": "fl-field", "kind": "flora", "seed": 95,
     "points": [[-40, 14], [40, 14], [40, 28], [-40, 28]],
     "spec": {"coverage": 0.32, "scale": 12, "octaves": 2, "fernShare": 0.10,
              "flowerShare": 0.18, "flowerScale": 13, "tallShare": 0.20}},
    {"id": "fl-green", "kind": "flora", "seed": 96,
     "points": [[-33, 61], [-13, 61], [-13, 84], [-33, 84]],
     "spec": {"coverage": 0.22, "scale": 11, "octaves": 2, "fernShare": 0.06,
              "flowerShare": 0.22, "flowerScale": 10, "tallShare": 0.06}},
]

PROPS = WATER + STROKES + HOUSES + BOULDERS + TREES + FLORA

FINISH = {
    "created": "2026-09-03",
    "authors": ["Opus 5"],
    "mapTheme": "vale",
    "themes": THEMES,
    "relief": RELIEF,
    "addShapes": ADD_SHAPES,
    "roomStyles": {"cage": HALL, "spawn": BARRACKS},
    "dressing": {"props": PROPS, "styles": STYLES},
}


def main():
    with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as handle:
        json.dump(PLAN, handle, indent=1)
    with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as handle:
        json.dump(FINISH, handle, indent=1)
    kinds = {}
    for prop in PROPS:
        kinds[prop["kind"]] = kinds.get(prop["kind"], 0) + 1
    print(f"{SLUG}: {len(PIECES)} pieces, {len(ADD_SHAPES)} shapes, "
          f"{len(THEMES)} themes, {len(STYLES)} recipes, {len(PROPS)} props {kinds}")


if __name__ == "__main__":
    main()
