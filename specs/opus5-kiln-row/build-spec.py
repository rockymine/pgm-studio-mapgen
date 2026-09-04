#!/usr/bin/env python3
"""Write the two authored documents for `opus5-kiln-row`.

    python3 specs/opus5-kiln-row/build-spec.py

**A small capture-the-wool board, 72 x 128, in a mesa.** A dry wadi runs down the middle of it and a
banded bluff stands over each end. On the bluff's shelf sits a row of four **apartment blocks** —
sandstone and terracotta under a brick roof, three storeys, the end ones open to the sky — with the
spawn behind the row at one end and the wool room behind it at the other. One ramp comes down off
each shelf into the wadi, and the wadi floor is the only ground both teams share.

**The idea this board is for: a mesa's strata live in the `wall` bucket, because a mesa is a cliff.**
There is no material that bands by world height, and there does not need to be one: the wall bucket's
`layered` stack is read by depth **from the top of the face it is painting**, so on a board whose
drops all start from one shelf, banding by depth *is* banding by altitude. One `STRATA` stack is the
wall material of every theme here, so every cut face on the board — the bluff, the ramp's sides, the
channel's bank — reads as the same rock in the same order, and nothing else on the board does.

The face itself is a **`scarp`** mark: a polyline with a height either side of it and a stated width
for the drop between, so the cliff is drawn where a line is drawn rather than found between two
plateaus that happened to meet.

Output: `opus5-kiln-row.plan.json` and `opus5-kiln-row.finish.json` beside this file.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-kiln-row"

# ── the frame ─────────────────────────────────────────────────────────────────────────────────
CELL = 2
BOARD_X, BOARD_Z = 36, 64           # 72 x 128 blocks

WADI_Y = 10                         # the floor both teams share
SHELF_Y = 20                        # the terrace the row stands on
CREST_Y = 27                        # the bluff top behind the spawn
LAND_H = 18

BLUFF_Z = 30                        # where the shelf breaks off into the wadi
ROW_Z = (32, 41)                    # the apartment row's own depth on the shelf
SHELF_Z = 44                        # behind the row: the spawn and the wool room
RAMP_X = 26                         # the two ways down off each shelf, one at either end

# The two rooms stand at the ends of the shelf rather than in the middle of it, because **the ground
# in front of a door is kept clear** and a building standing in it is declined `DR-KEEP`. With the
# rooms at the ends, the clear column their approaches take is the ends too, and the forty blocks
# between them is where the row goes.
SPAWN_RECT = (20, 44, 36, 60)
WOOL_RECT = (-36, 44, -20, 60)


# ── materials ─────────────────────────────────────────────────────────────────────────────────
def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


def stack(*pairs, ending="repeat"):
    return {"bands": [{"material": m, "thickness": t} for m, t in pairs], "ending": ending}


def layered(band_stack, axis="depth", beyond=None):
    out = {"kind": "layered", "axis": axis, "stack": band_stack}
    if beyond is not None:
        out["beyond"] = beyond
    return out


def noise(seed, scale, octaves, stops):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": octaves, "stops": stops}


def voronoi(seed, cell_size, bands):
    """A Worley diagram: bands are **depths inward from a cell boundary**, measured against the
    `F2 - F1` gap, and are not weights. The loop stops one short — **the last band takes the whole
    rest of the cell whatever depth it states** — so the material a player sees most of is the one
    written *last*, and everything before it is veining along the boundaries. Written the other way
    round, a wadi of sand with a seventh of gravel comes out as a gravel bed with sand along the
    cracks."""
    return {"kind": "voronoi", "seed": seed, "cellSize": cell_size, "rise": 0,
            "bands": [{"material": m, "thickness": t} for m, t in bands]}


SAND = solid(12, 0)
RED_SAND = solid(12, 1)
GRAVEL = solid(13, 0)
SANDSTONE = solid(24, 0)
SMOOTH_SANDSTONE = solid(24, 2)
CHISELLED_SANDSTONE = solid(24, 1)
RED_SANDSTONE = solid(179, 0)
SMOOTH_RED_SANDSTONE = solid(179, 2)
TERRACOTTA = solid(172, 0)
CLAY_WHITE = solid(159, 0)
CLAY_ORANGE = solid(159, 1)
CLAY_BROWN = solid(159, 12)
CLAY_RED = solid(159, 14)
BRICK = solid(45, 0)
END_STONE = solid(121, 0)
STONE = solid(1, 0)
COARSE = solid(3, 1)

# **The strata.** Read down from the top of whatever face is being painted, and used as the wall
# material of every theme on this board — so the bluff, the ramp's cheeks and the channel's bank are
# all one rock in one order, and the banding is the only place these colours appear.
STRATA = layered(stack(
    (CLAY_WHITE, 2),
    (CLAY_ORANGE, 3),
    (TERRACOTTA, 2),
    (CLAY_RED, 2),
    (CLAY_BROWN, 3),
    (CLAY_ORANGE, 4),
    (RED_SANDSTONE, 3),
    (SANDSTONE, 6),
))


def theme(surface, wall, fill, surface_depth=3, rim=None, rim_edges="void", bedrock=1):
    return {
        "bedrock": {"relative": False, "value": bedrock},
        "rimEdges": rim_edges,
        "wallOnTerrainFaces": True,
        "rim": {"material": rim or SANDSTONE, "depth": 1, "enabled": rim is not None},
        "surface": {"material": surface, "depth": surface_depth, "enabled": True},
        "wall": wall,
        "wallEnabled": True,
        "fill": fill,
    }


THEMES = {
    # the wadi floor: dry sand braided with gravel where water last ran
    "wadi": theme(
        surface=layered(stack((voronoi(11, 7, [(GRAVEL, 1), (RED_SAND, 2), (SAND, 1)]), 2),
                              (SANDSTONE, 2))),
        wall=STRATA, fill=SANDSTONE, surface_depth=3),

    # the shelf the row stands on: baked ground, redder than the wadi
    "shelf": theme(
        surface=layered(stack((noise(12, 9, 3, [RED_SAND, SAND, TERRACOTTA]), 1),
                              (RED_SANDSTONE, 1), (SANDSTONE, 2))),
        wall=STRATA, fill=SANDSTONE, surface_depth=3),

    # the bluff top behind the spawn: the caprock, which is what kept the mesa standing
    "crest": theme(
        surface=layered(stack((voronoi(13, 6, [(CLAY_ORANGE, 1), (RED_SAND, 2), (TERRACOTTA, 1)]), 2),
                              (RED_SANDSTONE, 2))),
        wall=STRATA, fill=SANDSTONE, surface_depth=3),
}

# ── the shapes ────────────────────────────────────────────────────────────────────────────────
_ids = {}


def sid(prefix):
    _ids[prefix] = _ids.get(prefix, 0) + 1
    return f"{prefix}{_ids[prefix]}"


def rect(prefix, x0, z0, x1, z1, theme_key, floor=0, height=LAND_H):
    return {"id": sid(prefix), "type": "rectangle", "operation": "add",
            "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1,
            "floor": floor, "base_height": height, "theme": theme_key}


# Paint scopes only: the relief has already solved every height, so a shape added here changes which
# theme owns its cells and nothing else.
shapes = [
    rect("t", -BOARD_X, BLUFF_Z, BOARD_X, 60, "shelf"),
    rect("t", -BOARD_X, 60, BOARD_X, BOARD_Z, "crest"),
]


# ── the relief ────────────────────────────────────────────────────────────────────────────────
def point(ident, x, z, h, r):
    return {"id": ident, "kind": "point", "at": [x, z], "h": h, "r": r}


def line(ident, points, heights, width):
    return {"id": ident, "kind": "line", "points": [[x, z] for x, z in points],
            "h": heights, "r": width}


def area(ident, x0, z0, x1, z1, h):
    return {"id": ident, "kind": "area",
            "ring": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]], "h": h}


def scarp(ident, points, high, low, face, band):
    """A drop drawn as a line rather than found between two plateaus. The mark pins `high` on one
    side of the polyline and `low` on the other, holds each for `band` blocks, and leaves `face`
    blocks unpinned between them — so the grade of the cliff is `(high - low) / face` and the
    relaxation builds exactly that."""
    return {"id": ident, "kind": "scarp", "points": [[x, z] for x, z in points],
            "high": high, "low": low, "face": face, "band": band}


MARKS = [
    # the bluff, drawn past both edges of the board so the face is cut by the frame
    scarp("bluff", [(-44, 31), (-14, 29), (16, 30), (44, 28)], SHELF_Y, WADI_Y + 1, 4, 9),
    # and the low back-bluff behind the spawn, so the shelf is a shelf rather than a plateau
    scarp("caprock", [(-44, 61), (0, 60), (44, 61)], CREST_Y, SHELF_Y, 2, 4),

    # the shelf itself, level, because a terrace of flats is built on one
    area("shelf", -BOARD_X, 33, BOARD_X, 60, SHELF_Y),

    # the wadi: shallow, dry, and braided
    point("pan-w", -24, 8, WADI_Y - 1, 5),
    point("pan-e", 20, 16, WADI_Y, 5),
    point("bar-w", -8, 20, WADI_Y + 2, 4),
    point("bar-e", 30, 6, WADI_Y + 1, 4),
    # the channel the water last ran down, two courses under the floor either side of it
    line("channel", [(-34, 4), (-12, 13), (8, 3), (30, 12)], [WADI_Y - 2], 4),

    # the two ways down off the shelf, cut through the bluff after the scarp so they win their cells
    line("ramp-e", [(RAMP_X, 16), (RAMP_X, 26), (RAMP_X, 36)], [WADI_Y, 15, SHELF_Y], 4),
    line("ramp-w", [(-RAMP_X, 16), (-RAMP_X, 26), (-RAMP_X, 36)], [WADI_Y, 15, SHELF_Y], 4),
]

RELIEF = {"*": {"base": WADI_Y, "reach": 20, "step": 1, "stairs": False,
                "grain": {"amplitude": 0.7, "scale": 11, "seed": 5},
                "marks": MARKS}}


# ── what stands on it ─────────────────────────────────────────────────────────────────────────
def tree(ident, x, z, species, height, seed):
    return {"id": ident, "kind": "tree", "seed": seed, "x": x, "z": z,
            "form": "template", "species": species, "height": height}


def house(ident, x, z, width, depth, style, seed, front="negZ"):
    return {"id": ident, "kind": "house", "seed": seed, "front": front,
            "wings": [{"corners": [[x, z], [x + width, z + depth]]}], "style": style}


def boulder(ident, x, z, size, seed, form="angular", mossy=False):
    return {"id": ident, "kind": "boulder", "seed": seed, "x": x, "z": z,
            "form": form, "size": size, "mossy": mossy,
            "rock": voronoi(14, 5, [(TERRACOTTA, 1), (RED_SANDSTONE, 2), (SANDSTONE, 1)])}


def flora(ident, ring, coverage, seed, scale=9, fern=0.05, flower=0.3, tall=0.05):
    return {"id": ident, "kind": "flora", "seed": seed,
            "points": [[x, z] for x, z in ring],
            "spec": {"coverage": coverage, "scale": scale, "octaves": 2, "fernShare": fern,
                     "flowerShare": flower, "flowerScale": 6, "tallShare": tall}}


def stroke(ident, points, radius, pave, style="worn", coverage=0.4, route=False, seed=1):
    out = {"id": ident, "kind": "stroke", "seed": seed, "style": style, "radius": radius,
           "coverage": coverage, "pave": pave}
    if route:
        out["route"] = True
    out["points"] = [[x, z] for x, z in points]
    return out


TRACK = voronoi(21, 4, [(RED_SAND, 1), (COARSE, 1), (GRAVEL, 1)])

props = [
    # the row: four blocks along the front of the shelf, the two ends open to the sky and the two
    # in the middle under brick. Nine deep, which is the depth the studio's desert house is drawn at.
    house("flat-a", -18, ROW_Z[0], 9, 9, "@kr-deck", 11),
    house("flat-b", -4, ROW_Z[0], 9, 9, "@kr-block", 12),
    house("flat-c", 9, ROW_Z[0], 9, 9, "@kr-deck", 13),

    # and one more standing at the foot of the bluff, in the wadi, where the ramp comes down
    house("kiln", 14, 12, 8, 7, "@kr-block", 15, front="posZ"),

    # rock fallen off the bluff, which is where rock at the foot of a bluff comes from
    boulder("scree-a", -20, 26, 2.6, 61, form="angular"),
    boulder("scree-b", 2, 24, 2.2, 62, form="outcrop"),
    boulder("scree-c", -33, 22, 2.0, 63, form="angular"),
    boulder("scree-d", 16, 24, 2.4, 64, form="outcrop"),
    boulder("scree-e", -6, 6, 1.8, 65, form="round"),
    boulder("crest-a", -8, 62, 2.8, 66, form="cairn"),
    boulder("crest-b", 10, 62, 2.4, 67, form="outcrop"),

    # acacia along the channel, which is the only place anything grows
    tree("acacia-a", -14, 4, "acacia", 8, 201),
    tree("acacia-b", -2, 14, "acacia", 7, 202),
    tree("acacia-c", 22, 4, "acacia", 8, 203),
    tree("acacia-d", -28, 8, "acacia", 6, 204),

    flora("scrub-wadi", [(-34, 0), (34, 0), (34, 28), (-34, 28)], 0.14, 81,
          scale=7, fern=0.02, flower=0.24, tall=0.04),
    flora("scrub-shelf", [(-34, 33), (34, 33), (34, 60), (-34, 60)], 0.08, 82,
          scale=9, fern=0.02, flower=0.3, tall=0.02),
]

props += [
    # the row's own street, and the ramp off the end of it
    stroke("street", [(-RAMP_X, 37), (-14, 44), (0, 45), (14, 44), (RAMP_X, 37)], 2.6, TRACK,
           style="solid", coverage=1.0, route=True, seed=31),
    stroke("ramp-track-e", [(RAMP_X, 37), (RAMP_X, 26), (RAMP_X + 1, 16), (20, 10)], 2.4, TRACK,
           coverage=0.9, route=True, seed=32),
    stroke("ramp-track-w", [(-RAMP_X, 37), (-RAMP_X, 26), (-RAMP_X - 1, 16), (-20, 10)], 2.4, TRACK,
           coverage=0.9, route=True, seed=36),
    # and the braid down the wadi, which is paint rather than a route
    stroke("braid-a", [(-34, 6), (-12, 15), (8, 5), (30, 14)], 3.0,
           voronoi(22, 5, [(GRAVEL, 1), (SAND, 4)]), style="worn", coverage=0.3, seed=33),
    stroke("braid-b", [(-32, 14), (-10, 5), (10, 16), (32, 4)], 2.2,
           voronoi(23, 4, [(GRAVEL, 1), (RED_SAND, 3)]), style="worn", coverage=0.22, seed=34),
    # a wash of red sand up the bluff's foot, so the join is not a drawn line
    stroke("foot-wash", [(-36, 24), (-12, 26), (12, 25), (36, 27)], 5.0, RED_SAND,
           style="worn", coverage=0.3, seed=35),
]


# ── the plan ──────────────────────────────────────────────────────────────────────────────────
def cells(x0, z0, x1, z1):
    return [x0 // CELL, z0 // CELL, (x1 - x0) // CELL, (z1 - z0) // CELL]


plan = {
    "plan": 1,
    "meta": {"name": "Kiln Row"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 16, "surface": WADI_Y},
    "pieces": [
        # The wadi, the row's shelf, and the back of the shelf split so the two rooms abut ground
        # rather than nest inside a piece — a nested room has no seam and answers `WX6`.
        {"id": "wadi", "role": "piece", "rect": cells(-BOARD_X, 0, BOARD_X, BLUFF_Z),
         "surface": WADI_Y},
        {"id": "row", "role": "piece", "rect": cells(-BOARD_X, BLUFF_Z, BOARD_X, SHELF_Z),
         "surface": SHELF_Y},
        {"id": "wool-room", "role": "wool-room", "rect": cells(*WOOL_RECT), "surface": SHELF_Y},
        {"id": "shelf-wn", "role": "piece",
         "rect": cells(WOOL_RECT[0], WOOL_RECT[3], WOOL_RECT[2], BOARD_Z), "surface": SHELF_Y},
        {"id": "shelf-m", "role": "piece",
         "rect": cells(WOOL_RECT[2], SHELF_Z, SPAWN_RECT[0], BOARD_Z), "surface": SHELF_Y},
        {"id": "camp", "role": "spawn", "rect": cells(*SPAWN_RECT), "surface": SHELF_Y},
        {"id": "shelf-en", "role": "piece",
         "rect": cells(SPAWN_RECT[0], SPAWN_RECT[3], SPAWN_RECT[2], BOARD_Z), "surface": SHELF_Y},
    ],
    # The wadi floor, which is where the two halves meet and the only ground worth building on.
    "zones": [{"id": "mid-band", "rect": cells(-BOARD_X, -14, BOARD_X, 14), "holes": []}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "camp", "at": [4, 4], "facing": "front"}],
        "wools": [{"id": "wool-1", "piece": "wool-room", "at": [4, 4]}],
    },
}

finish = {
    "authors": ["Opus 5"],
    "addShapes": shapes,
    "relief": RELIEF,
    "themes": THEMES,
    "mapTheme": "wadi",
    "roomStyles": {"cage": "@kr-vault", "spawn": "@kr-gate"},
    "dressing": {"props": props},
}


def write():
    with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as handle:
        json.dump(plan, handle, indent=1)
    with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as handle:
        json.dump(finish, handle, indent=1)
    kinds = {}
    for prop in props:
        kinds[prop["kind"]] = kinds.get(prop["kind"], 0) + 1
    print(f"board {2 * BOARD_X} x {2 * BOARD_Z}  wadi y{WADI_Y}  shelf y{SHELF_Y}  crest y{CREST_Y}")
    print(f"shapes {len(shapes)} · marks {len(MARKS)} · themes {len(THEMES)} · "
          f"props {len(props)} {kinds}")


if __name__ == "__main__":
    write()
