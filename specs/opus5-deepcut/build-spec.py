#!/usr/bin/env python3
"""Write the two authored documents for `opus5-deepcut`.

    python3 specs/opus5-deepcut/build-spec.py

**A small destroy-the-monument board, 72 x 128, in a chalk quarry.** One pit takes the middle of the
board and is worked down in **benches**; the plateau at either end carries a spawn. Standing in the
pit, one to a team and under its own rim, is a **witness pillar** — the spire of unquarried chalk a
quarry leaves where it has stopped cutting — with the monument four blocks over its crown. Water has
come up in the sump at the bottom.

**The idea this board is for: the terracing that ruins a hillside is what a quarry bench *is*.**
`opus5-tarnfell` came out as stacked plateaus with vertical faces and had to be rebuilt; here that is
the design, and it is asked for by one knob rather than by drawing thirty marks. The relief solves a
smooth bowl — `base` at the rim, one `area` mark holding the sump at the bottom — and `step` snaps
the finished surface to a quantum, so the bowl comes out as concentric benches with a riser between
each. `stairs` then cuts a way up out of every place the terracing stranded, which is what keeps a
worked pit walkable without making it stop being terraced.

The two spires are **`relief_scope: "exclude"`** shapes: excluded cells leave the field entirely, so
the relaxation bends round them as it bends round the void and each keeps its own drawn column — a
flat crown on vertical sides, which is a spire and cannot be made from a mark. Neither is joined to
anything. The pit is a build zone and reaching a monument means bridging to it.

The faces are painted with **`wallRun`**: stripes wrapping the perimeter, constant up a column, so
they stand vertical. A weathered cliff bands horizontally (`opus5-kiln-row`) and a **cut** face is
scored vertically by the saw, and the two boards say so in the same bucket with two materials.

Output: `opus5-deepcut.plan.json` and `opus5-deepcut.finish.json` beside this file.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-deepcut"

# ── the frame ─────────────────────────────────────────────────────────────────────────────────
CELL = 2
BOARD_X, BOARD_Z = 36, 64           # 72 x 128 blocks

RIM_Y = 40                          # the plateau the pit was cut into
FLOOR_Y = 16                        # the working floor at the bottom of the benches
SUMP_Y = 12                         # and the sump in the neck between the two faces
STEP = 4                            # the bench quantum: every level here is a multiple of it
CROWN_Y = 28                        # the two spires' flat tops
LAND_H = 38

RIM_Z = 40                          # where the plateau breaks off into the pit
SPAWN_RECT = (-8, 42, 8, 58)

# **The floor is a dumbbell, not a bowl.** A pit whose floor is a disc in the middle of the board
# puts both monuments the same distance from both spawns; two lobes, each worked back under its own
# team's rim and joined by a neck through the seam, is how a quarry with two faces actually reads and
# is what puts a goal near the team that defends it. The lobe is authored once and the fan draws the
# other, so the floor comes out as a Z through the board.
LOBE = (-25, 14, 1, 34)
NECK = (-9, -14, 9, 14)
SUMP = (-7, -6, 7, 6)
PILLAR = (-13, 30)                  # the witness pillar, in the lobe under its own team's rim
PILLAR_R = 4


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


def wall_run(*pairs):
    """Stripes wrapping the outer perimeter, each so many arc cells wide and constant up a column —
    so on a face they stand vertical. What a saw leaves, rather than what weather does."""
    return {"kind": "wallRun", "runs": [{"material": m, "width": w} for m, w in pairs]}


STONE = solid(1, 0)
DIORITE = solid(1, 3)
POLISHED_DIORITE = solid(1, 4)
ANDESITE = solid(1, 5)
GRASS = solid(2, 0)
DIRT = solid(3, 0)
COARSE = solid(3, 1)
COBBLE = solid(4, 0)
GRAVEL = solid(13, 0)
CLAY = solid(82, 0)
QUARTZ = solid(155, 0)
CHISELLED_QUARTZ = solid(155, 1)
PILLAR_QUARTZ = solid(155, 2)
CLAY_WHITE = solid(159, 0)
CLAY_LGREY = solid(159, 8)
CLAY_GREY = solid(159, 7)
COAL_BLOCK = solid(173, 0)

# The saw's own pattern: four widths that do not divide into each other, so the cycle round a face
# never falls back into step with the corners.
SAWN = wall_run((QUARTZ, 3), (CLAY_WHITE, 5), (CLAY_LGREY, 2), (QUARTZ, 4),
                (DIORITE, 1), (CLAY_WHITE, 7), (POLISHED_DIORITE, 2))


def theme(surface, wall, fill, surface_depth=3, rim=None, rim_edges="void", bedrock=1):
    return {
        "bedrock": {"relative": False, "value": bedrock},
        "rimEdges": rim_edges,
        "wallOnTerrainFaces": True,
        "rim": {"material": rim or STONE, "depth": 1, "enabled": rim is not None},
        "surface": {"material": surface, "depth": surface_depth, "enabled": True},
        "wall": wall,
        "wallEnabled": True,
        "fill": fill,
    }


THEMES = {
    # the benches: broken chalk underfoot, and the cut face beside them
    "bench": theme(
        surface=layered(stack((voronoi(11, 6, [(CLAY_LGREY, 1), (QUARTZ, 2), (CLAY_WHITE, 1)]), 2),
                              (CLAY_WHITE, 2))),
        wall=SAWN, fill=CLAY_WHITE, surface_depth=3),

    # the sump: what has washed to the bottom, and it is grey
    "sump": theme(
        surface=layered(stack((voronoi(12, 5, [(CLAY_GREY, 1), (CLAY_LGREY, 2), (GRAVEL, 1)]), 2),
                              (CLAY, 1), (CLAY_WHITE, 2))),
        wall=SAWN, fill=CLAY_WHITE, surface_depth=3),

    # the plateau the pit was cut into: the only green on the board, and it is what makes the pit
    # read as something taken out of somewhere
    "downs": theme(
        surface=layered(stack((noise(13, 10, 3, [GRASS, GRASS, COARSE]), 1), (DIRT, 2),
                              (CLAY_WHITE, 3))),
        wall=SAWN, fill=CLAY_WHITE, surface_depth=3),
}

# ── the shapes ────────────────────────────────────────────────────────────────────────────────
_ids = {}


def sid(prefix):
    _ids[prefix] = _ids.get(prefix, 0) + 1
    return f"{prefix}{_ids[prefix]}"


def rect(prefix, x0, z0, x1, z1, theme_key, floor=0, height=LAND_H, scope=None):
    shape = {"id": sid(prefix), "type": "rectangle", "operation": "add",
             "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1,
             "floor": floor, "base_height": height, "theme": theme_key}
    if scope:
        shape["relief_scope"] = scope
    return shape


def circle(prefix, cx, cz, radius, theme_key, floor=0, height=LAND_H, scope=None):
    shape = {"id": sid(prefix), "type": "circle", "operation": "add",
             "center_x": cx, "center_z": cz, "radius": radius,
             "floor": floor, "base_height": height, "theme": theme_key}
    if scope:
        shape["relief_scope"] = scope
    return shape


shapes = [
    # paint scopes
    rect("t", -BOARD_X, RIM_Z, BOARD_X, BOARD_Z, "downs"),
    rect("t", SUMP[0] - 3, SUMP[1] - 3, SUMP[2] + 3, SUMP[3] + 3, "sump"),
    # the witness pillar. `exclude` takes its cells out of the relief entirely, so the bowl is
    # solved as if it were a hole and the shape keeps the column it was drawn with: a flat crown
    # on vertical sides. A mark cannot make one — every mark is a constraint the relaxation then
    # smooths through.
    circle("spire", PILLAR[0], PILLAR[1], PILLAR_R, "bench", height=CROWN_Y, scope="exclude"),
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


MARKS = [
    # Four statements and nothing else: the plateau, the two floors, the sump. Every bench between
    # them is the step quantum rather than a mark, which is the whole of why this board is thirty
    # marks shorter than the landscape that taught it.
    area("downs", -BOARD_X, RIM_Z + 1, BOARD_X, BOARD_Z, RIM_Y),
    area("lobe", *LOBE, FLOOR_Y),
    area("neck", *NECK, FLOOR_Y),
    area("sump", *SUMP, SUMP_Y),

    # the haul road, down the west wall into this team's own face, so the stone had a way out and
    # the team that defends the face has the short way onto it
    line("haul", [(-30, 44), (-29, 36), (-25, 28), (-22, 22)],
         [RIM_Y, 32, 24, FLOOR_Y], 4),

    # two shoulders left uncut, so the pit is not an oval
    point("shoulder-e", 33, 26, 34, 6),
    point("shoulder-w", -33, -2, 32, 6),
]

RELIEF = {"*": {
    "base": RIM_Y, "reach": 26,
    # **The one knob this board is about.** The surface snaps to a four-block quantum, which turns
    # the solved bowl into concentric benches with a four-course riser between them; `stairs` then
    # cuts a way up out of every place that stranded, so the pit stays walkable without stopping
    # being terraced. `RIM_Y` and `SUMP_Y` are both multiples of it, so neither is rounded away.
    "step": STEP, "stairs": True,
    "grain": {"amplitude": 0.8, "scale": 9, "seed": 5},
    "marks": MARKS,
}}


# ── what stands on it ─────────────────────────────────────────────────────────────────────────
def tree(ident, x, z, species, height, seed):
    return {"id": ident, "kind": "tree", "seed": seed, "x": x, "z": z,
            "form": "template", "species": species, "height": height}


def boulder(ident, x, z, size, seed, form="angular", mossy=False):
    return {"id": ident, "kind": "boulder", "seed": seed, "x": x, "z": z,
            "form": form, "size": size, "mossy": mossy,
            "rock": voronoi(14, 4, [(CLAY_LGREY, 1), (QUARTZ, 1), (CLAY_WHITE, 1)])}


def flora(ident, ring, coverage, seed, scale=9, fern=0.1, flower=0.3, tall=0.06):
    return {"id": ident, "kind": "flora", "seed": seed,
            "points": [[x, z] for x, z in ring],
            "spec": {"coverage": coverage, "scale": scale, "octaves": 2, "fernShare": fern,
                     "flowerShare": flower, "flowerScale": 6, "tallShare": tall}}


def stroke(ident, points, radius, pave, style="worn", coverage=0.4, route=False, seed=1):
    out = {"id": ident, "kind": "path", "seed": seed, "style": style, "radius": radius,
           "coverage": coverage, "pave": pave}
    if route:
        out["route"] = True
    out["points"] = [[x, z] for x, z in points]
    return out


HAUL = voronoi(21, 4, [(COARSE, 1), (CLAY_LGREY, 1), (GRAVEL, 1)])

props = [
    # the water that has come up in the bottom of it
    # The water fills whatever is level, so the **pan** is the size of the pool: an `area` mark at
    # the sump's own level, small, with the working floor four courses over it all round.
    {"id": "the-sump", "kind": "water", "seed": 5, "form": "natural",
     "points": [[-5, -3], [0, -4], [5, -2], [4, 3], [-1, 4], [-5, 2], [-5, -3]],
     "radius": 3.0, "depth": 2, "edge": 0.8, "shore": 3, "shoreWander": True,
     "bank": voronoi(15, 4, [(CLAY, 1), (CLAY_LGREY, 1), (GRAVEL, 1)])},

    # spoil: what did not go on the lorry, tipped on the benches
    boulder("spoil-a", -28, 18, 3.0, 61, form="angular"),
    boulder("spoil-b", 24, 30, 2.6, 62, form="angular"),
    boulder("spoil-c", -31, 12, 2.2, 63, form="outcrop"),
    boulder("spoil-d", 6, 20, 2.4, 64, form="angular"),
    boulder("spoil-e", 30, 6, 2.0, 65, form="outcrop"),
    boulder("spoil-f", -33, 21, 2.8, 66, form="cairn"),

    # the downs above it, which is the only place anything grows
    tree("thorn-a", -16, 54, "birch", 7, 201),
    tree("thorn-b", 22, 48, "birch", 6, 202),
    tree("thorn-c", 30, 58, "oak", 8, 203),
    tree("thorn-d", -30, 60, "oak", 7, 204),
    flora("downs-turf", [(-34, RIM_Z + 2), (34, RIM_Z + 2), (34, 62), (-34, 62)], 0.42, 81,
          scale=9, fern=0.14, flower=0.3, tall=0.14),
    # and a thin fringe on the top bench, where the turf is falling in
    flora("lip-turf", [(-34, 34), (34, 34), (34, RIM_Z), (-34, RIM_Z)], 0.12, 82,
          scale=6, fern=0.05, flower=0.2, tall=0.04),

    # the haul road, and a wash of grit along the second bench
    stroke("haul-road", [(-28, 50), (-30, 44), (-29, 36), (-25, 28), (-22, 22), (-12, 16), (0, 8)],
           3.0, HAUL, style="solid", coverage=1.0, route=True, seed=31),
    stroke("bench-grit", [(-34, 30), (-16, 34), (4, 32), (22, 36)], 3.4,
           voronoi(22, 4, [(CLAY_LGREY, 1), (GRAVEL, 1)]), style="worn", coverage=0.45, seed=32),
    stroke("lip-wash", [(-34, RIM_Z - 1), (0, RIM_Z), (34, RIM_Z - 1)], 4.0, CLAY_WHITE,
           style="worn", coverage=0.3, seed=33),
]


# ── the plan ──────────────────────────────────────────────────────────────────────────────────
def cells(x0, z0, x1, z1):
    return [x0 // CELL, z0 // CELL, (x1 - x0) // CELL, (z1 - z0) // CELL]


plan = {
    "plan": 1,
    "meta": {"name": "Deepcut"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 16, "surface": FLOOR_Y},
    "pieces": [
        {"id": "pit", "role": "piece", "rect": cells(-BOARD_X, 0, BOARD_X, RIM_Z),
         "surface": FLOOR_Y + 8},
        {"id": "rim-s", "role": "piece", "rect": cells(-BOARD_X, RIM_Z, BOARD_X, SPAWN_RECT[1]),
         "surface": RIM_Y},
        {"id": "rim-w", "role": "piece",
         "rect": cells(-BOARD_X, SPAWN_RECT[1], SPAWN_RECT[0], BOARD_Z), "surface": RIM_Y},
        {"id": "camp", "role": "spawn", "rect": cells(*SPAWN_RECT), "surface": RIM_Y},
        {"id": "rim-n", "role": "piece",
         "rect": cells(SPAWN_RECT[0], SPAWN_RECT[3], SPAWN_RECT[2], BOARD_Z), "surface": RIM_Y},
        {"id": "rim-e", "role": "piece",
         "rect": cells(SPAWN_RECT[2], SPAWN_RECT[1], BOARD_X, BOARD_Z), "surface": RIM_Y},
    ],
    # The pit floor either side of the sump: what a player may build on, which on this board is how
    # a monument is reached at all.
    "zones": [{"id": "pit-floor", "rect": cells(-BOARD_X, -18, BOARD_X, 18), "holes": []}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "camp", "at": [4, 4], "facing": "front"}],
        "destroyables": [
            {"id": "destroyable-1", "at": [PILLAR[0] / CELL, PILLAR[1] / CELL],
             "style": "pillar-3", "materials": "obsidian", "float": 4,
             "name": "The Witness"},
        ],
    },
}

finish = {
    "authors": ["Opus 5"],
    "addShapes": shapes,
    "relief": RELIEF,
    "themes": THEMES,
    "mapTheme": "bench",
    "roomStyles": {"cage": None, "spawn": "@dc-cabin"},
    "dressing": {"props": props},
}


def write():
    if RIM_Y % STEP or SUMP_Y % STEP or FLOOR_Y % STEP:
        raise SystemExit("the rim and the sump have to be multiples of the step, or both are rounded")
    with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as handle:
        json.dump(plan, handle, indent=1)
    with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as handle:
        json.dump(finish, handle, indent=1)
    kinds = {}
    for prop in props:
        kinds[prop["kind"]] = kinds.get(prop["kind"], 0) + 1
    benches = (RIM_Y - FLOOR_Y) // STEP
    print(f"board {2 * BOARD_X} x {2 * BOARD_Z}  rim y{RIM_Y}  floor y{FLOOR_Y}  sump y{SUMP_Y}  "
          f"step {STEP} -> {benches} benches  spire crown y{CROWN_Y} at {PILLAR}")
    print(f"shapes {len(shapes)} · marks {len(MARKS)} · themes {len(THEMES)} · "
          f"props {len(props)} {kinds}")


if __name__ == "__main__":
    write()
