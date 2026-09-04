#!/usr/bin/env python3
"""Write the two authored documents for `opus5-interchange`.

    python3 specs/opus5-interchange/build-spec.py

The board is a four-storey building rather than a landscape, so its geometry is a few hundred
rectangles whose coordinates are arithmetic on a handful of levels. Those levels are named once
here and every shape is written from them, which is the only way the four storeys can be kept from
drifting a course apart: a slab's floor, the wall that carries it and the ramp that reaches it are
three statements of one number.

Output: `opus5-interchange.plan.json` and `opus5-interchange.finish.json` beside this file.
"""
import json, os, copy

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-interchange"

# ── the levels ────────────────────────────────────────────────────────────────────────────────
# A layer holds one span per column, so every storey is `floor` + thickness inside its own layer.
# Read down the page: the world reads the same way.
CELL = 4
UNDER_FLOOR = 0                    # the undercroft slab: blocks 0..5, stood on at y6
UNDER_H = 6
BASIN_H = 3                        # the drained basin: blocks 0..2, stood on at y3 — three down
UNDER_WALL_H = 12                  # undercroft walls meet the concourse's underside at y12
CONC_FLOOR = 12                    # the concourse: blocks 12..17, stood on at y18
CONC_H = 6
CONC_TOP = CONC_FLOOR + CONC_H     # 18
WALL_H = 14                        # a room wall: blocks 12..25, eight courses over the concourse
PARAPET_H = 18                     # the spine's walls: blocks 12..29, over its own roof
ROOF_FLOOR = 26                    # the spine's roof: blocks 26..27
ROOF_H = 2
CATWALK_FLOOR = 24                 # the catwalk: blocks 24..25, stood on at y26
CATWALK_H = 2
CATWALK_TOP = CATWALK_FLOOR + CATWALK_H     # 26
DECK_FLOOR = 34                    # the car deck: blocks 34..37, stood on at y38
DECK_H = 4
DECK_TOP = DECK_FLOOR + DECK_H     # 38

# ── the frame ─────────────────────────────────────────────────────────────────────────────────
X_EDGE = 56                        # the complex's outer skin
Z_PLAZA, Z_APRON, Z_COURT, Z_APPROACH, Z_BACK = 16, 40, 100, 112, 124


# ── materials ─────────────────────────────────────────────────────────────────────────────────
def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


def checker(size, even, odd):
    return {"kind": "checker", "size": size, "even": even, "odd": odd}


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
    return {"kind": "voronoi", "seed": seed, "cellSize": cell_size, "rise": 0,
            "bands": [{"material": m, "thickness": t} for m, t in bands]}


def theme(surface, wall, fill, rim=None, rim_depth=1, surface_depth=3,
          rim_edges="drop", wall_on_faces=True, bedrock=1):
    """One paintable recipe. `rim=None` turns the lip off, which is what an interior wants:
    a rim caps every fall with a band, and inside a building every fall is a step somebody made."""
    return {
        "bedrock": {"relative": False, "value": bedrock},
        "rimEdges": rim_edges,
        "wallOnTerrainFaces": wall_on_faces,
        "rim": {"material": rim or solid(155, 0), "depth": rim_depth, "enabled": rim is not None},
        "surface": {"material": surface, "depth": surface_depth, "enabled": True},
        "wall": wall,
        "wallEnabled": True,
        "fill": fill,
    }


def glass_theme(data):
    """A pane wall or a pane floor: one block, every bucket, no lip. A stained-glass shape is
    terrain the light goes through, which is the whole reason to draw one."""
    pane = solid(95, data)
    return theme(surface=pane, wall=pane, fill=pane, rim=None,
                 surface_depth=8, rim_edges="void", wall_on_faces=True, bedrock=1)


STONE = solid(1, 0)
ANDESITE = solid(1, 5)
POLISHED_ANDESITE = solid(1, 6)
STONE_BRICK = solid(98, 0)
CRACKED_BRICK = solid(98, 2)
SLAB = solid(43, 8)
QUARTZ = solid(155, 0)
GRASS = solid(2, 0)
DIRT = solid(3, 0)
PODZOL = solid(3, 2)
COBBLE = solid(4, 0)
MOSSY = solid(48, 0)
GRAVEL = solid(13, 0)
OAK = solid(5, 0)
BIRCH = solid(5, 2)
HARDENED = solid(172, 0)
PRISMARINE = solid(168, 0)
PRISM_BRICK = solid(168, 1)
DARK_PRISM = solid(168, 2)
CLAY_WHITE = solid(159, 0)
CLAY_ORANGE = solid(159, 1)
CLAY_LTBLUE = solid(159, 3)
CLAY_YELLOW = solid(159, 4)
CLAY_GRAY = solid(159, 7)
CLAY_LTGRAY = solid(159, 8)
CLAY_CYAN = solid(159, 9)
CLAY_BROWN = solid(159, 12)
CLAY_GREEN = solid(159, 13)
CLAY_LIME = solid(159, 5)
CLAY_BLACK = solid(159, 15)

# ── the themes, one per area ──────────────────────────────────────────────────────────────────
# Each area names two families and no more: a structural one and an accent. The glass panes are
# the third thing every area shares, and they are the only place a colour is stated as itself.
THEMES = {
    # the ordinary ground the map opens on: grass, with paving that rings in from the coast
    "plaza": theme(
        surface=layered(stack((COBBLE, 1), (STONE_BRICK, 3), (SLAB, 2), ending="handOver"),
                        axis="inward", beyond=layered(stack((GRASS, 1), (DIRT, 2)))),
        wall=layered(stack((STONE_BRICK, 3), (ANDESITE, 2), (COBBLE, 1))),
        fill=STONE, rim=QUARTZ, rim_edges="void", surface_depth=3),

    # the spine: the corridor everything else opens off, and the only ordinary interior
    "spine": theme(
        surface=layered(stack((checker(4, CLAY_LTGRAY, CLAY_WHITE), 1), (STONE_BRICK, 2))),
        wall=layered(stack((CLAY_WHITE, 4), (CLAY_LTGRAY, 1))),
        fill=STONE, rim=None, surface_depth=3),
    "w-spine": theme(
        surface=SLAB,
        wall=layered(stack((CLAY_WHITE, 3), (CLAY_LTGRAY, 1), (CLAY_WHITE, 4))),
        fill=CLAY_WHITE, rim=None, surface_depth=1),

    # the stair hall: grey concrete under a deck, with the one warm colour on the map
    "hall": theme(
        surface=layered(stack((checker(8, POLISHED_ANDESITE, ANDESITE), 1), (ANDESITE, 2))),
        wall=layered(stack((CLAY_GRAY, 4), (CLAY_ORANGE, 1))),
        fill=STONE, rim=None, surface_depth=3),
    "w-hall": theme(
        surface=CLAY_ORANGE,
        wall=layered(stack((CLAY_GRAY, 5), (CLAY_ORANGE, 1), (CLAY_GRAY, 2))),
        fill=CLAY_GRAY, rim=None, surface_depth=1),
    "stair": theme(
        surface=layered(stack((POLISHED_ANDESITE, 1), (ANDESITE, 1), (CLAY_ORANGE, 1))),
        wall=layered(stack((ANDESITE, 1), (CLAY_ORANGE, 1), (ANDESITE, 4))),
        fill=ANDESITE, rim=None, surface_depth=3),

    # the corridor of doors: an office floor, warm and brown, repeating down its length
    "doors": theme(
        surface=layered(stack((checker(6, OAK, solid(5, 5)), 1), (CLAY_BROWN, 2))),
        wall=layered(stack((CLAY_BROWN, 4), (CLAY_YELLOW, 1))),
        fill=HARDENED, rim=None, surface_depth=3),
    "w-doors": theme(
        surface=OAK,
        wall=layered(stack((CLAY_BROWN, 2), (CLAY_YELLOW, 1), (CLAY_BROWN, 5))),
        fill=CLAY_BROWN, rim=None, surface_depth=1),

    # The garden court: the most familiar thing on the board, and the one with a sky. The turf is
    # mown in six-block squares — plain grass against a three-way mottle of grass, lime and green —
    # which is the same instrument as the pool's tile and the deck's bays at a third size, and reads
    # as a lawn somebody laid out rather than one that grew. `boundary` rims it where it meets a
    # wall, so every lawn has a planted edge without a shape drawn for one.
    "garden": theme(
        surface=layered(stack(
            (checker(6, GRASS, noise(53, 4, 2, [CLAY_LIME, CLAY_GREEN, CLAY_LIME])), 1),
            (DIRT, 2))),
        wall=layered(stack((CLAY_GREEN, 3), (MOSSY, 1), (COBBLE, 2))),
        fill=STONE, rim=CLAY_GREEN, rim_edges="boundary", surface_depth=3),

    # the approach outside the court's north wall: the same three greens, unmown — no squares, only
    # the mottle, so the lawn inside the wall reads as the deliberate one
    "verge": theme(
        surface=layered(stack((noise(54, 11, 3, [GRASS, GRASS, CLAY_LIME]), 1),
                              (noise(55, 9, 2, [DIRT, DIRT, PODZOL]), 2))),
        wall=layered(stack((CLAY_GREEN, 2), (MOSSY, 1), (COBBLE, 3))),
        fill=STONE, rim=MOSSY, rim_edges="void", surface_depth=3),
    "w-garden": theme(
        surface=MOSSY,
        wall=layered(stack((CLAY_GREEN, 4), (MOSSY, 1), (CLAY_GREEN, 3))),
        fill=CLAY_GREEN, rim=None, surface_depth=1),

    # the car deck: a hectare of slab, marked out in bays nobody parked in
    "deck": theme(
        surface=layered(stack((checker(16, SLAB, CLAY_LTGRAY), 1), (SLAB, 1), (STONE, 2))),
        wall=layered(stack((CLAY_LTGRAY, 2), (SLAB, 1), (CLAY_LTGRAY, 5))),
        fill=STONE, rim=CLAY_LTGRAY, rim_edges="void", surface_depth=4),

    # the pool: the only room on the board that was built to hold something, and does not
    "pool": theme(
        surface=layered(stack((checker(2, CLAY_WHITE, CLAY_LTGRAY), 1), (CLAY_WHITE, 2))),
        wall=layered(stack((CLAY_CYAN, 3), (PRISM_BRICK, 1))),
        fill=HARDENED, rim=PRISM_BRICK, rim_edges="drop", surface_depth=3),
    "basin": theme(
        surface=layered(stack((noise(17, 7, 2, [CLAY_LTBLUE, CLAY_LTBLUE, CLAY_CYAN]), 1),
                              (PRISMARINE, 1))),
        wall=layered(stack((PRISM_BRICK, 1), (DARK_PRISM, 1), (PRISMARINE, 4))),
        fill=PRISMARINE, rim=None, surface_depth=2),
    "w-pool": theme(
        surface=PRISM_BRICK,
        wall=layered(stack((CLAY_CYAN, 4), (CLAY_WHITE, 1), (CLAY_CYAN, 3))),
        fill=CLAY_CYAN, rim=None, surface_depth=1),

    # the service level: what is under a building, and reads like it
    "service": theme(
        surface=layered(stack((voronoi(5, 5, [(CRACKED_BRICK, 1), (STONE_BRICK, 1), (GRAVEL, 1)]), 1),
                              (STONE, 2))),
        wall=layered(stack((CLAY_GRAY, 3), (CLAY_BLACK, 1), (CRACKED_BRICK, 2))),
        fill=STONE, rim=None, surface_depth=3),
    "w-service": theme(
        surface=CRACKED_BRICK,
        wall=layered(stack((CLAY_BLACK, 2), (CLAY_GRAY, 4), (CRACKED_BRICK, 2))),
        fill=CLAY_GRAY, rim=None, surface_depth=1),

    # the outer skin, seen from outside the complex and from the void
    "skin": theme(
        surface=QUARTZ,
        wall=layered(stack((HARDENED, 3), (STONE_BRICK, 2), (CLAY_LTGRAY, 1), (HARDENED, 6))),
        fill=HARDENED, rim=None, surface_depth=1),

    # the pool's lane markings: the basin's own thickness, so only the paint changes
    "lane": theme(surface=DARK_PRISM, wall=DARK_PRISM, fill=PRISMARINE, rim=None, surface_depth=2),

    "glass-cyan": glass_theme(9),
    "glass-green": glass_theme(13),
    "glass-yellow": glass_theme(4),
    "glass-gray": glass_theme(8),
    "glass-orange": glass_theme(1),
}


# ── shapes ────────────────────────────────────────────────────────────────────────────────────
_ids = {}


def sid(prefix):
    _ids[prefix] = _ids.get(prefix, 0) + 1
    return f"{prefix}{_ids[prefix]}"


def box(prefix, x0, z0, x1, z1, floor, height, theme_key=None, op="add"):
    shape = {"id": sid(prefix), "type": "rectangle", "operation": op,
             "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1,
             "floor": floor, "base_height": height}
    if theme_key:
        shape["theme"] = theme_key
    return shape


def ramp(prefix, x0, z0, x1, z1, floor, high, low, along="z", theme_key=None):
    """A wedge: a rectangle whose thickness runs from `high` at its low-coordinate edge to `low`
    at the other. The vertices are wound so the two heights land on the right pair, and the
    heights are block thicknesses over `floor`, which is what makes a ramp between two storeys
    arithmetic rather than a guess."""
    verts = [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]
    if along == "z":
        heights = [high, high, low, low]
    else:
        heights = [high, low, low, high]
    shape = {"id": sid(prefix), "type": "polygon", "operation": "add",
             "vertices": verts, "anchor_heights": heights,
             "floor": floor, "base_height": max(high, low)}
    if theme_key:
        shape["theme"] = theme_key
    return shape


# ══ the ground layer, over the compiled concourse ═════════════════════════════════════════════
# Everything here stands at CONC_FLOOR. A wall is not a shape on top of the floor — a layer keeps
# one span per column and the taller add wins it outright — so a wall is the same slab, thicker.
ground = []

# the paint of each room, stated as a shape the same thickness as the floor it repaints: within a
# layer the smallest themed shape wins a cell, so a floor colour needs no geometry of its own
ground += [
    box("t", -44, 44, -12, 80, CONC_FLOOR, CONC_H, "hall"),        # the stair hall
    box("t", 12, 44, 52, 80, CONC_FLOOR, CONC_H, "doors"),         # the corridor of doors
    box("t", -8, 40, 8, 100, CONC_FLOOR, CONC_H, "spine"),         # the spine
    box("t", -52, 84, 52, 96, CONC_FLOOR, CONC_H, "garden"),       # the garden court
    box("t", -28, 100, 28, Z_APPROACH, CONC_FLOOR, CONC_H, "verge"),   # the approach to it
    box("t", -8, Z_APPROACH, 8, Z_BACK, CONC_FLOOR, CONC_H, "verge"),  # and the arrivals yard
    box("t", 56, 59, 62, 68, CONC_FLOOR, CONC_H, "skin"),          # the balcony over the void
]
# The two glass floors. The core's is the drained pool's ceiling, sixteen blocks over the monument
# standing in it; the hall's sits directly under the car deck's own pane, so the three storeys read
# as one shaft — the deck, the concourse, and the service level under both.
ground += [
    box("gl", 26, 58, 38, 66, CONC_FLOOR, CONC_H, "glass-cyan"),
    box("gl", -30, 56, -22, 64, CONC_FLOOR, CONC_H, "glass-gray"),
]

# the complex's outer skin
ground += [
    box("w", -X_EDGE, 40, -52, 100, CONC_FLOOR, WALL_H, "skin"),           # west face
    box("w", 52, 40, X_EDGE, 59, CONC_FLOOR, WALL_H, "skin"),              # east face, south of
    box("w", 52, 68, X_EDGE, 100, CONC_FLOOR, WALL_H, "skin"),             # …and north of the slot
    box("w", -52, 96, -8, 100, CONC_FLOOR, WALL_H, "skin"),                # north face, west
    box("w", 8, 96, 52, 100, CONC_FLOOR, WALL_H, "skin"),                  # …and east of the gate
    box("w", -52, 40, -44, 44, CONC_FLOOR, WALL_H, "skin"),                # south face, west
    box("w", -32, 40, -8, 44, CONC_FLOOR, WALL_H, "skin"),
    box("w", 8, 40, 52, 44, CONC_FLOOR, WALL_H, "skin"),
]
# the balcony: a three-wide slot through the east face onto a platform over nothing
ground += [box("bal", X_EDGE, 59, 62, 68, CONC_FLOOR, CONC_H, "skin")]

# The spine's own walls, carried a storey past its roof so the roof is a slot rather than a route,
# and run the whole length of the complex — including across the garden court, which the spine
# therefore crosses without opening onto. Three doors in sixty blocks: one west into the stair
# hall and two east into the loop. The court is reached by going the long way round.
# A run of `(z0, z1, theme)`: a theme of None is the gap a door is. Written as a run rather than as
# rectangles because the thing that matters about this wall is where it stops, three times in sixty
# blocks, and a run says that on one line.
SPINE_WEST = [(40, 56, "w-spine"), (56, 62, None), (62, 70, "w-spine"),
              (70, 78, "glass-green"), (78, 84, "w-spine"),
              (84, 96, "glass-green"), (96, 100, "w-spine")]
SPINE_EAST = [(40, 48, "w-spine"), (48, 54, "glass-yellow"), (54, 58, None),
              (58, 66, "w-spine"), (66, 72, "glass-yellow"), (72, 76, None),
              (76, 84, "w-spine"), (84, 96, "glass-green"), (96, 100, "w-spine")]
for x0, x1, run in ((-12, -8, SPINE_WEST), (8, 12, SPINE_EAST)):
    for z0, z1, key in run:
        if key is not None:
            ground.append(box("w", x0, z0, x1, z1, CONC_FLOOR, PARAPET_H, key))

# the corridor of doors: a ring around a sealed core, with a door only in the core's north face
ground += [
    box("w", 22, 54, 26, 70, CONC_FLOOR, WALL_H, "w-doors"),               # core, west
    box("w", 38, 54, 42, 70, CONC_FLOOR, WALL_H, "w-doors"),               # core, east
    box("w", 26, 54, 38, 58, CONC_FLOOR, WALL_H, "w-doors"),               # core, south
    box("w", 26, 66, 30, 70, CONC_FLOOR, WALL_H, "w-doors"),               # core, north-west…
    box("w", 34, 66, 38, 70, CONC_FLOOR, WALL_H, "w-doors"),               # …and north-east
]
# the doors the corridor is named for: a repeating rank of glass panels down its west leg
for k, z0 in enumerate(range(46, 78, 8)):
    ground.append(box("gl", 20, z0, 22, z0 + 4, CONC_FLOOR, WALL_H, "glass-yellow"))
    ground.append(box("w", 20, z0 + 4, 22, z0 + 8, CONC_FLOOR, WALL_H, "w-doors"))

# the wall between the complex and the garden court, with the three ways through it
ground += [
    box("w", -52, 80, -40, 84, CONC_FLOOR, WALL_H, "w-garden"),
    box("w", -28, 80, -12, 84, CONC_FLOOR, WALL_H, "w-garden"),
    box("w", 12, 80, 28, 84, CONC_FLOOR, WALL_H, "w-garden"),
    box("w", 40, 80, 52, 84, CONC_FLOOR, WALL_H, "w-garden"),
]

# the hole the down ramp falls through, and two light wells over the service level
ground += [
    box("cut", -40, 60, -32, 76, CONC_FLOOR, 40, None, op="subtract"),
    box("cut", -26, 66, -18, 74, CONC_FLOOR, 40, None, op="subtract"),
    box("cut", 42, 60, 48, 68, CONC_FLOOR, 40, None, op="subtract"),
]

# the ramp to the car deck, in the open slot beside the hall it rises out of
ground += [ramp("up", -52, 48, -44, 80, CONC_FLOOR,
                high=DECK_TOP - CONC_FLOOR, low=CONC_TOP - CONC_FLOOR, theme_key="stair")]

GROUND_IDS = [s["id"] for s in ground]


# ══ the undercroft ════════════════════════════════════════════════════════════════════════════
# Everything is at floor 0. The fill outside the hollow is what the concourse stands on; inside
# it, a wall is again the same slab run up to the concourse's underside.
under = []
# what holds the board up, drawn to the plan's own outline so the plinth is never wider than the deck
under += [
    box("uf", -36, 0, 36, Z_PLAZA, UNDER_FLOOR, UNDER_WALL_H, "skin"),
    box("uf", -X_EDGE, Z_PLAZA, X_EDGE, 48, UNDER_FLOOR, UNDER_WALL_H, "skin"),
    box("uf", -X_EDGE, 48, -48, 92, UNDER_FLOOR, UNDER_WALL_H, "skin"),
    box("uf", 48, 48, X_EDGE, 92, UNDER_FLOOR, UNDER_WALL_H, "skin"),
    box("uf", -X_EDGE, 92, X_EDGE, Z_COURT, UNDER_FLOOR, UNDER_WALL_H, "skin"),
    box("uf", -28, Z_COURT, 28, Z_APPROACH, UNDER_FLOOR, UNDER_WALL_H, "skin"),
    box("uf", -8, Z_APPROACH, 8, Z_BACK, UNDER_FLOOR, UNDER_WALL_H, "skin"),
]
# the service level: one floor, two solid plant rooms, and the ring corridor they leave
under += [
    box("us", -48, 48, 8, 92, UNDER_FLOOR, UNDER_H, "service"),
    box("uw", -40, 52, -12, 60, UNDER_FLOOR, UNDER_WALL_H, "w-service"),
    box("uw", -40, 80, -12, 88, UNDER_FLOOR, UNDER_WALL_H, "w-service"),
    box("uw", 4, 48, 8, 68, UNDER_FLOOR, UNDER_WALL_H, "w-pool"),      # the pool's west wall…
    box("uw", 4, 76, 8, 92, UNDER_FLOOR, UNDER_WALL_H, "w-pool"),      # …with its one doorway
]
# the pool hall: a deck clamped around a basin four blocks below it, and steps back out
under += [
    box("pd", 8, 48, 16, 92, UNDER_FLOOR, UNDER_H, "pool"),
    box("pd", 40, 48, 48, 92, UNDER_FLOOR, UNDER_H, "pool"),
    box("pd", 16, 48, 40, 56, UNDER_FLOOR, UNDER_H, "pool"),
    box("pd", 16, 84, 40, 92, UNDER_FLOOR, UNDER_H, "pool"),
    box("pb", 16, 56, 40, 84, UNDER_FLOOR, BASIN_H, "basin"),
    box("pl", 22, 58, 25, 82, UNDER_FLOOR, BASIN_H, "lane"),
    box("pl", 31, 58, 34, 82, UNDER_FLOOR, BASIN_H, "lane"),
    ramp("ps", 24, 56, 32, 62, UNDER_FLOOR, high=UNDER_H, low=BASIN_H, theme_key="basin"),
]
# The ramp down from the stair hall, under the hole cut for it. Twenty cells for twelve courses:
# a slope of one course a cell builds as treads of two, and a two-block rise is a block a player
# has to place to climb it, so a stair that is meant to be walked back up runs at about a half.
under += [ramp("dn", -40, 60, -32, 80, UNDER_FLOOR,
               high=CONC_TOP, low=UNDER_H, theme_key="stair")]

UNDER_IDS = [s["id"] for s in under]


# ══ the catwalk, the car deck and the spine's roof ════════════════════════════════════════════
catwalk = [box("cw", -44, 66, -32, 70, CATWALK_FLOOR, CATWALK_H, "stair")]

deck = [
    box("dk", -44, 44, -8, 84, DECK_FLOOR, DECK_H, "deck"),
    box("dg", -30, 56, -22, 64, DECK_FLOOR, DECK_H, "glass-gray"),     # a pane over the hall
]

roofs = [
    box("rf", -8, 40, 8, 100, ROOF_FLOOR, ROOF_H, "w-spine"),
    box("rg", -8, 58, 8, 66, ROOF_FLOOR, ROOF_H, "glass-orange"),      # one pane over the spine
]


def island(ident, name, shapes, mirrors=True):
    return {"id": ident, "name": name, "mirrors": mirrors,
            "shapeIds": [s["id"] for s in shapes]}


# ── the plan ──────────────────────────────────────────────────────────────────────────────────
# Cells, not blocks: a cell is CELL blocks and the frame is the symmetry centre.
def cells(x0, z0, x1, z1):
    return [x0 // CELL, z0 // CELL, (x1 - x0) // CELL, (z1 - z0) // CELL]


plan = {
    "plan": 1,
    "meta": {"name": "Interchange"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 24, "surface": CONC_TOP},
    "pieces": [
        {"id": "plaza",   "role": "piece", "rect": cells(-36, 0, 36, Z_PLAZA), "surface": CONC_TOP},
        {"id": "apron",   "role": "piece", "rect": cells(-X_EDGE, Z_PLAZA, X_EDGE, Z_APRON),
         "surface": CONC_TOP},
        {"id": "complex", "role": "piece", "rect": cells(-X_EDGE, Z_APRON, X_EDGE, Z_COURT),
         "surface": CONC_TOP},
        {"id": "approach", "role": "piece", "rect": cells(-28, Z_COURT, 28, Z_APPROACH),
         "surface": CONC_TOP},
        {"id": "arrivals", "role": "spawn", "rect": cells(-8, Z_APPROACH, 8, Z_BACK),
         "surface": CONC_TOP},
    ],
    "zones": [],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "arrivals", "at": [2, 2], "facing": "front"}],
        "destroyables": [
            # Absolute cells from the centre: three of the five stand on ground the plan has no
            # rectangle for, and a goal that names no piece is the one marker kind that may.
            # `layer` is which storey the goal stands on: a stacked board has a surface per layer, and a
            # thing stated for a hall lands on the deck roofing it unless it says which one it meant.
            {"id": "destroyable-1", "at": [30 / CELL, 78 / CELL], "style": "pillar-1", "layer": "under",
             "materials": "obsidian", "float": 3, "name": "The Deep End"},        # the drained basin
            {"id": "destroyable-2", "at": [-38 / CELL, 68 / CELL], "style": "pillar-2", "layer": "catwalk",
             "materials": "obsidian", "float": 2, "name": "The Catwalk"},         # dark, under the car deck
            {"id": "destroyable-3", "at": [34 / CELL, 62 / CELL], "style": "pillar-1", "layer": "ground",
             "materials": "obsidian", "float": 4, "name": "The Back Office"},     # roofed by nothing
            {"id": "destroyable-4", "at": [-26 / CELL, 50 / CELL], "style": "pillar-2", "layer": "deck",
             "materials": "obsidian", "float": 4, "name": "Level 4"},             # forty by thirty-six of slab
            {"id": "destroyable-5", "at": [24 / CELL, 90 / CELL], "style": "pillar-2", "layer": "ground",
             "materials": "obsidian", "float": 4, "name": "The Court"},           # the one anybody finds first
        ],
    },
}

# ── the two things that keep appearing ────────────────────────────────────────────────────────
# A kiosk and a cairn, in the same relation to each other, in seven rooms that share nothing else:
# the plaza, the apron, the approach, the corridor of doors, the pool hall, the garden court twice
# and the car deck. Each entry is `(name, x, z, layer, cairn dx, cairn dz)` — the offset is per site
# because the ground around each one is a different shape.
KIOSK_SITES = [
    ("kiosk-plaza", -22, 4, "ground", 10, 4),
    ("kiosk-apron", 18, 24, "ground", 10, 4),
    ("kiosk-approach", -20, 102, "ground", 10, 4),
    ("kiosk-doors", 44, 44, "ground", 2, 10),
    ("kiosk-pool", 9, 50, "under", 1, 10),
    ("kiosk-court-w", -50, 86, "ground", 8, 2),
    ("kiosk-court-e", 44, 86, "ground", -4, 8),
    ("kiosk-hall", -20, 72, "ground", -6, 2),
    ("kiosk-deck", -14, 60, "deck", -8, 8),
]


def kiosk(name, x, z, layer):
    prop = {"id": name, "kind": "house", "seed": 7, "front": "negZ",
            "wings": [{"corners": [[x, z], [x + 5, z + 5]]}], "style": "@interchange-kiosk"}
    if layer != "ground":
        prop["layer"] = layer
    return prop


def cairn(name, x, z, layer, seed):
    prop = {"id": name, "kind": "boulder", "seed": seed, "x": x, "z": z,
            "form": "cairn", "size": 2.0, "mossy": False,
            "rock": voronoi(3, 4, [(ANDESITE, 2), (POLISHED_ANDESITE, 1), (CLAY_LTGRAY, 1)])}
    if layer != "ground":
        prop["layer"] = layer
    return prop


props = []
for k, (name, x, z, layer, dx, dz) in enumerate(KIOSK_SITES):
    props.append(kiosk(name, x, z, layer))
    props.append(cairn(name.replace("kiosk", "cairn"), x + dx, z + dz, layer, 500 + k))

# the garden court: the one place on the board where anything grows
props += [
    # The court, planted. Two lawns either side of the crossing, each with its kiosk, its cairn, an
    # oak or three and ground cover over the lot — the one place on the board where anything grows,
    # and the reason it is the room a player believes before they notice the rest.
    {"id": "court-turf-w", "kind": "flora", "seed": 41,
     "points": [[-51, 84], [-13, 84], [-13, 96], [-51, 96]],
     "spec": {"coverage": 0.55, "scale": 9, "octaves": 3, "fernShare": 0.14,
              "flowerShare": 0.3, "flowerScale": 7, "tallShare": 0.16}},
    {"id": "court-turf-e", "kind": "flora", "seed": 43,
     "points": [[13, 84], [51, 84], [51, 96], [13, 96]],
     "spec": {"coverage": 0.55, "scale": 9, "octaves": 3, "fernShare": 0.14,
              "flowerShare": 0.3, "flowerScale": 7, "tallShare": 0.16}},
    {"id": "court-oak-1", "kind": "tree", "seed": 111, "x": -29, "z": 87,
     "form": "template", "species": "oak", "height": 9},
    {"id": "court-oak-2", "kind": "tree", "seed": 112, "x": -22, "z": 94,
     "form": "template", "species": "oak", "height": 11},
    {"id": "court-oak-3", "kind": "tree", "seed": 113, "x": -15, "z": 87,
     "form": "template", "species": "oak", "height": 8},
    {"id": "court-oak-4", "kind": "tree", "seed": 114, "x": 38, "z": 94,
     "form": "template", "species": "oak", "height": 10},
    {"id": "court-birch-1", "kind": "tree", "seed": 101, "x": -40, "z": 95,
     "form": "template", "species": "birch", "height": 9},
    # one oak in the middle of the car deck, which is the only thing up there that is alive
    {"id": "deck-oak", "kind": "tree", "seed": 104, "x": -12, "z": 80,
     "form": "template", "species": "oak", "height": 11, "layer": "deck"},
    # The approach, outside the court's north wall: the same species again, spaced the way an
    # avenue is rather than the way a wood is, so the walk in reads as somebody's planting scheme.
    # It is twelve blocks deep between a spawn door's keep-out and a wall, so it holds three.
    {"id": "approach-oak-1", "kind": "tree", "seed": 121, "x": -26, "z": 110,
     "form": "template", "species": "oak", "height": 10},
    {"id": "approach-oak-2", "kind": "tree", "seed": 122, "x": 26, "z": 110,
     "form": "template", "species": "oak", "height": 10},
    {"id": "approach-birch", "kind": "tree", "seed": 102, "x": 14, "z": 103,
     "form": "template", "species": "birch", "height": 8},
    {"id": "approach-turf", "kind": "flora", "seed": 44,
     "points": [[-27, 101], [27, 101], [27, 111], [-27, 111]],
     "spec": {"coverage": 0.45, "scale": 10, "octaves": 2, "fernShare": 0.1,
              "flowerShare": 0.28, "flowerScale": 8, "tallShare": 0.12}},
    # the plaza, outdoors and ordinary — more of it planted, none of it patterned
    {"id": "plaza-oak-1", "kind": "tree", "seed": 105, "x": 26, "z": 6,
     "form": "template", "species": "oak", "height": 10},
    {"id": "plaza-oak-2", "kind": "tree", "seed": 106, "x": -8, "z": 12,
     "form": "template", "species": "oak", "height": 9},
    {"id": "plaza-oak-3", "kind": "tree", "seed": 107, "x": 12, "z": 14,
     "form": "template", "species": "oak", "height": 11},
    {"id": "plaza-oak-4", "kind": "tree", "seed": 108, "x": -30, "z": 10,
     "form": "template", "species": "oak", "height": 9},
    {"id": "apron-oak-1", "kind": "tree", "seed": 109, "x": 40, "z": 26,
     "form": "template", "species": "oak", "height": 10},
    {"id": "apron-oak-2", "kind": "tree", "seed": 110, "x": -44, "z": 32,
     "form": "template", "species": "oak", "height": 11},
    {"id": "apron-oak-3", "kind": "tree", "seed": 115, "x": -28, "z": 22,
     "form": "template", "species": "oak", "height": 9},
    {"id": "apron-oak-4", "kind": "tree", "seed": 116, "x": 8, "z": 34,
     "form": "template", "species": "oak", "height": 10},
    {"id": "plaza-turf", "kind": "flora", "seed": 42,
     "points": [[-34, 2], [34, 2], [34, 14], [-34, 14]],
     "spec": {"coverage": 0.38, "scale": 12, "octaves": 2, "fernShare": 0.08,
              "flowerShare": 0.24, "flowerScale": 9, "tallShare": 0.08}},
    {"id": "apron-turf", "kind": "flora", "seed": 45,
     "points": [[-54, 18], [54, 18], [54, 38], [-54, 38]],
     "spec": {"coverage": 0.32, "scale": 14, "octaves": 2, "fernShare": 0.08,
              "flowerShare": 0.2, "flowerScale": 11, "tallShare": 0.06}},
    # the road in: spawn to the court crossing to the plaza, drawn before the scenery
    {"id": "road-in", "kind": "path", "seed": 3, "style": "solid", "radius": 3.0,
     "coverage": 1.0, "route": True,
     "pave": voronoi(6, 3, [(SLAB, 2), (STONE_BRICK, 1), (COBBLE, 1)]),
     "points": [[0, 120], [0, 106], [0, 92], [0, 78], [0, 56], [0, 30], [0, 6]]},
    # The markings. A stroke repaints the surface it crosses and adds no block, so it is the only
    # way to draw a line on a floor — and none of these states `route`, because a route claims its
    # cells against the props and nothing here is a way through that a kiosk must keep off.
    # the traffic worn into the corridor's ring, which goes round the core because nothing else can
    {"id": "worn-doors", "kind": "path", "seed": 13, "style": "worn", "radius": 2.0,
     "coverage": 0.55, "pave": voronoi(8, 3, [(CLAY_LTGRAY, 2), (GRAVEL, 1)]),
     "points": [[17, 46], [17, 76], [47, 76], [47, 50], [30, 47], [17, 47]]},
    # and the track worn across the car deck, which is the only thing up there that says anyone came
    {"id": "worn-deck", "kind": "path", "seed": 14, "style": "worn", "radius": 2.0,
     "coverage": 0.5, "pave": voronoi(9, 3, [(CLAY_LTGRAY, 2), (GRAVEL, 1)]),
     "points": [[-12, 58], [-24, 62], [-30, 76], [-42, 78]]},
    # two spurs off the court's own gates, which are the only ways onto either lawn
    {"id": "road-court-w", "kind": "path", "seed": 4, "style": "worn", "radius": 2.0,
     "coverage": 0.85, "route": True,
     "pave": voronoi(7, 3, [(GRAVEL, 2), (COBBLE, 1)]),
     "points": [[-34, 80], [-34, 92]]},
    {"id": "road-court-e", "kind": "path", "seed": 5, "style": "worn", "radius": 2.0,
     "coverage": 0.85, "route": True,
     "pave": voronoi(7, 3, [(GRAVEL, 2), (COBBLE, 1)]),
     "points": [[34, 80], [34, 92]]},
]

# ── the finish ────────────────────────────────────────────────────────────────────────────────
finish = {
    "authors": ["Opus 5"],
    # the compiled outline is one shape at the plan's own surface: lift it off the ground so the
    # whole board becomes a slab with a basement under it
    "shapePropsByHeight": {str(CONC_TOP): {"floor": CONC_FLOOR, "base_height": CONC_H}},
    "themeByHeight": {str(CONC_TOP): "plaza"},
    "addShapes": ground,
    "addLayers": [
        # first in the stack, because the painter walks it in order and each storey paints its whole
        # column: a storey listed after one that stands over it never sees a stone block again
        {"id": "under", "name": "Service level", "base_y": 0, "below": True,
         "shapes": under, "islands": [island("under", "Service level", under)]},
        {"id": "catwalk", "name": "Catwalk", "base_y": 0,
         "shapes": catwalk, "islands": [island("catwalk", "Catwalk", catwalk)]},
        {"id": "roofs", "name": "Spine roof", "base_y": 0,
         "shapes": roofs, "islands": [island("roofs", "Spine roof", roofs)]},
        {"id": "deck", "name": "Car deck", "base_y": 0,
         "shapes": deck, "islands": [island("deck", "Car deck", deck)]},
    ],
    "themes": THEMES,
    "mapTheme": "plaza",
    "roomStyles": {"cage": None, "spawn": "@interchange-spawn"},
    "dressing": {"props": props},
    "voidEnforcement": True,
}


def write():
    with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as handle:
        json.dump(plan, handle, indent=1)
    with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as handle:
        json.dump(finish, handle, indent=1)
    print(f"plan: {len(plan['pieces'])} pieces, "
          f"{len(plan['placements']['destroyables'])} goals")
    print(f"finish: ground {len(ground)} shapes · under {len(under)} · "
          f"catwalk {len(catwalk)} · roofs {len(roofs)} · deck {len(deck)} · "
          f"{len(THEMES)} themes · {len(props)} props")


if __name__ == "__main__":
    write()
