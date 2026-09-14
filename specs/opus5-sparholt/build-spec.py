#!/usr/bin/env python3
"""Sparholt — a king-of-the-hill board that is an alabaster-cutting works, on two storeys.

Nothing on this board is raised. The three points are all sunk, and the structure is what the works
is made of rather than what the ground does: there is no relief in it beyond the two loading banks a
yard of cut stone would actually have.

  the yard        one paved deck at y24 over the whole works, four courses thick
  the cutting shed  the centre point, inside a roofed shed entered by four doors — but the roof is a
                  ring and the pad under it is open to the sky through the louvre, so the objective is
                  visible from above and from every door rather than buried
  the two sawpits the flank points, eight courses down: the yard deck simply is not there over them,
                  because the storey below is
  the undercroft  a tramway running as a rectangle round the middle at y16, joining the two pits
                  without passing under the shed — the core of rock inside the ring is solid

The second storey is stated the way `showcase/20-undercroft` states one: the ground slab is thinned to
its top four courses and a `below` layer carries the rock under it, banded round the tramway rather
than cut out of it. Every shape on this board is an add. The pits are then not holes anybody dug —
they are the two places the deck was never laid, and the tramway is what a player finds at the bottom.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-sparholt"

YARD, DECK_FLOOR, ADIT, SILL = 24, 20, 16, 26     # deck top, deck floor, tramway floor, bank top
# What the deck actually stands at once the relief has solved, read off the built world at
# (0, 20) and (17, -14): an anchor states a thickness from the shape's floor, so a ramp that has
# to arrive at the deck is cut to the height the deck is, not to the height the plan asked for.
DECK_TOP = 26

# ── the plan ─────────────────────────────────────────────────────────────────────────────────────
# Three pieces on the +z half; rot_180 makes the board. The works band is stated from the centre
# line out, so its image meets it there and the cutting shed straddles it.
plan = {
    "plan": 2,
    "meta": {"name": "Sparholt"},
    "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 24, "surface": YARD,
                "observerY": 56},
    "pieces": [
        {"id": "works", "role": "piece", "rect": [-8,  0, 16, 4], "surface": YARD},
        {"id": "yard",  "role": "piece", "rect": [-8,  4, 16, 8], "surface": YARD},
        {"id": "lodge", "role": "spawn", "rect": [-3, 12,  6, 3], "surface": YARD + 1},
    ],
    "zones": [],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "lodge", "at": [15, 7], "facing": "front",
                    "footprint": [6, 3, 18, 9]}],
        "iron": [{"id": "iron-1", "piece": "lodge", "at": [2, 7]},
                 {"id": "iron-2", "piece": "lodge", "at": [28, 7]}],
        "wools": [], "destroyables": [], "cores": [],
    },
    "walls": [], "boxes": [],
}

# ── materials ────────────────────────────────────────────────────────────────────────────────────
def solid(i, d=0):  return {"kind": "solid", "id": i, "data": d}

QUARTZ, Q_CHISEL, Q_PILLAR = solid(155, 0), solid(155, 1), solid(155, 2)
WHITE_CLAY, PALE_CLAY, GREY_CLAY = solid(159, 0), solid(159, 8), solid(159, 7)
STONE, ANDESITE, POLISHED = solid(1), solid(1, 5), solid(1, 6)
STONEBRICK, CHISELLED, CRACKED = solid(98), solid(98, 3), solid(98, 2)
COBBLE, GRAVEL = solid(4), solid(13)
IRON = solid(42)                                   # the saw frames and the tramway rails
BIRCH_LOG, BIRCH_PLANK = solid(17, 2), solid(5, 2)
Q_SLAB, Q_STAIR = 44, 156
LAID_BIRCH = {"kind": "laidLog", "id": 17, "data": 2}


def cell_(seed, size, palette, rise=0):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": max(1, size // 3),
            "warp": max(1, size // 4), "palette": palette, "rise": rise}


def stack(bands, ending="handOver"):
    return {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}


def layered(bands, axis="depth", ending="handOver"):
    return {"kind": "layered", "axis": axis, "stack": stack(bands, ending)}


PAVING = cell_(51, 6, [QUARTZ, WHITE_CLAY, PALE_CLAY, QUARTZ])    # alabaster, laid in courses
WORN   = cell_(52, 4, [PALE_CLAY, GREY_CLAY, QUARTZ])             # where the tramway is dragged over
SAWN   = cell_(53, 5, [Q_CHISEL, Q_PILLAR, QUARTZ], rise=3)       # a cut face: the kerf is visible

themes = {
    # the deck. A works yard is flat by construction, so the surface stack is on `depth` and the
    # board's structure is built rather than graded — but the wall bucket is a sawn face, because
    # every vertical on this board is a face somebody cut.
    "yard": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": Q_CHISEL},
        "surface": {"enabled": True, "depth": 3,
                    "material": layered([(1, PAVING), (2, cell_(54, 8, [QUARTZ, STONE]))])},
        "wall":    SAWN, "wallEnabled": True,
        "fill":    cell_(55, 9, [QUARTZ, STONE], rise=4),
    },
    # the loading banks: the strip along each end where cut block is stacked before it goes out.
    # Worn pale clay rather than fresh quartz, and its wall is the bank's own sawn edge.
    "bank": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": GREY_CLAY},
        "surface": {"enabled": True, "depth": 3,
                    "material": layered([(1, WORN), (2, cell_(56, 7, [PALE_CLAY, STONE]))])},
        "wall":    cell_(57, 5, [Q_PILLAR, Q_CHISEL, GREY_CLAY], rise=3), "wallEnabled": True,
        "fill":    cell_(58, 9, [STONE, QUARTZ], rise=4),
    },
    # the rock the works stands in: never seen except where the pits open it, and given a fill that
    # is not plain stone so the storey above cannot hand its whole column to whatever is drawn over it
    "rock": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": ANDESITE},
        "surface": {"enabled": True, "depth": 2, "material": cell_(59, 9, [STONE, ANDESITE])},
        "wall":    cell_(60, 7, [STONE, ANDESITE, COBBLE], rise=4), "wallEnabled": True,
        "fill":    cell_(61, 11, [STONE, POLISHED], rise=5),
    },
    # the tramway floor: iron-grey, the one place on the board that is not pale
    "adit": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": CHISELLED},
        "surface": {"enabled": True, "depth": 2,
                    "material": layered([(1, cell_(62, 4, [STONEBRICK, CRACKED, ANDESITE, IRON])),
                                         (1, STONEBRICK)])},
        "wall":    cell_(63, 6, [STONEBRICK, ANDESITE, CRACKED], rise=3), "wallEnabled": True,
        "fill":    cell_(64, 9, [STONE, ANDESITE], rise=4),
    },
}

# ── the relief: two loading banks, and nothing else ──────────────────────────────────────────────
def lobe(cx, cz, radii, tilt=0.0):
    n = len(radii)
    return [[round(cx + r * math.cos(tilt + 2 * math.pi * i / n), 1),
             round(cz + r * math.sin(tilt + 2 * math.pi * i / n), 1)]
            for i, r in enumerate(radii)]


relief = {
    "team": {
        "base": YARD, "reach": 0, "step": 1, "landform": "flat",
        "grain": {"amplitude": 0, "scale": 24, "seed": 1},
        "marks": [
            # the loading bank: two courses over the deck, along the yard behind the works. It is the
            # only rise on the board and it is a built bench, not a landform — which is why it has a
            # bevel of 1 and a straight-sided ring rather than a lobe.
            {"id": "bank", "kind": "area", "h": SILL, "bevel": 1,
             "ring": [[-34, 52], [34, 52], [34, 40], [22, 37], [-22, 37], [-34, 40]]},
            # the spawn apron, level with the bank so the door does not open onto a step
            {"id": "apron", "kind": "area", "h": SILL, "bevel": 1,
             "ring": lobe(0, 66, [22, 18, 21, 16, 22, 18, 21, 16], 0.1)},
        ],
        "pushes": [],
    }
}

# ── the works ────────────────────────────────────────────────────────────────────────────────────
PIT_W, PIT_E = -26, 26          # the two sawpits, on the tramway's west and east legs
SHED = 15                       # the cutting shed's half-span


def rect(id_, x0, z0, x1, z1, *, floor=None, span=None, theme=None, material=None,
         mode="level", height=None, layer=None, group=None, extra=None):
    shape = {"id": id_, "type": "rectangle", "operation": "add",
             "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1}
    if floor is not None:  shape["floor"] = floor
    if span is not None:   shape["base_height"] = span
    if theme:              shape["theme"] = theme
    if material:           shape["material"] = material
    if mode:               shape["height_mode"] = mode
    if height is not None: shape["base_height"] = height
    if layer:              shape["layer"] = layer
    if group:              shape["group"] = group
    if extra:              shape.update(extra)
    return shape


def sink(id_, x0, z0, x1, z1, depth, theme):
    """A dish in the deck: the top comes down and the courses under it stay ground."""
    return {"id": id_, "type": "rectangle", "operation": "add", "group": "team",
            "height_mode": "sink", "base_height": depth, "skirt": 0, "theme": theme,
            "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1}


def unlaid(id_, x0, z0, x1, z1):
    """The deck is not laid over these columns. A `sink` will not do it — a sink brings the top down
    and writes ground the whole way to the shape's floor, which fills the storey underneath — so the
    pit is a `subtract` over exactly the deck's four courses. What is left in the column is the
    tramway's own void, already open from y16, and the floor a player lands on is eight down."""
    return {"id": id_, "type": "rectangle", "operation": "subtract", "group": "team",
            "floor": DECK_FLOOR, "base_height": YARD - DECK_FLOOR,
            "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1}


def ramp(id_, x0, x1, z_high, z_low, material):
    """The way down into a pit, cut in the deck beside it rather than in it: `SK13` reads a subtract
    as the board's negative space and refuses any add that fills it, so a stair inside the pit is not
    available at any floor below the deck. Seventeen blocks of run for eight of fall."""
    return {"id": id_, "type": "polygon", "operation": "add", "override": True, "keepClear": True,
            "group": "team", "floor": 0, "base_height": YARD, "material": material,
            "height_mode": "level", "skirt": 0,
            "vertices": [[x0, z_high], [x1, z_high], [x1, z_low], [x0, z_low]],
            "anchor_heights": [DECK_TOP, DECK_TOP, ADIT, ADIT]}


TREAD = cell_(68, 4, [Q_CHISEL, STONEBRICK, POLISHED], rise=2)

add_shapes = [
    # the two sawpits. They are the flank points, and they are the only two places the deck stops.
    unlaid("pit-w", PIT_W - 6, -7, PIT_W + 6, 7),
    unlaid("pit-e", PIT_E - 6, -7, PIT_E + 6, 7),
    # and the way into each: ONE ramp is stated and its rot_180 image is the other pit's. Two, one
    # per pit, land in each other's columns — the image of a ramp cut beside the west pit is a ramp
    # beside the east one, running the other way — and two opposed ramps in one set of columns
    # resolve to a V with its floor four courses over the pit.
    ramp("ramp-e", PIT_E - 11, PIT_E - 7, -13, 7, TREAD),
    # the shed's plinth: one course proud of the deck, which is what makes the doorways read as
    # doorways rather than as gaps between walls
    rect("plinth", -SHED, -SHED, SHED, SHED, mode="raise", height=1, theme="bank", group="team",
         extra={"skirt": 0}),
    # the centre pad, one course into the plinth and open to the sky through the roof's louvre
    sink("shed-pad", -6, -6, 6, 6, 1, "bank"),
]

# ── the second storey ────────────────────────────────────────────────────────────────────────────
# The rock is stated over every column the board has and the tramway is the shorter span inside it,
# which is the whole technique: a storey drawn as its rooms leaves the ground above it floating.
RING_X, RING_Z, CORE_X, CORE_Z = 32, 20, 20, 12

under = {
    "id": "under", "name": "Undercroft", "base_y": 0, "below": True,
    "shapes": [
        rect("rock-n", -44, -80, 44, -RING_Z, floor=0, span=DECK_FLOOR, theme="rock", mode=None),
        rect("rock-s", -44, RING_Z, 44, 80, floor=0, span=DECK_FLOOR, theme="rock", mode=None),
        rect("rock-w", -44, -RING_Z, -RING_X, RING_Z, floor=0, span=DECK_FLOOR, theme="rock",
             mode=None),
        rect("rock-e", RING_X, -RING_Z, 44, RING_Z, floor=0, span=DECK_FLOOR, theme="rock",
             mode=None),
        # the core: solid rock under the cutting shed, which is what "without passing the middle"
        # means — the tramway is a rectangle round this and there is no way through it
        rect("rock-core", -CORE_X, -CORE_Z, CORE_X, CORE_Z, floor=0, span=DECK_FLOOR, theme="rock",
             mode=None),
        # the tramway: four shorter spans making one rectangle. Four courses of headroom under the
        # deck's own floor, and the two pits are where it comes out into daylight.
        rect("adit-n", -RING_X, -RING_Z, RING_X, -CORE_Z, floor=0, span=ADIT, theme="adit",
             mode=None),
        rect("adit-s", -RING_X, CORE_Z, RING_X, RING_Z, floor=0, span=ADIT, theme="adit", mode=None),
        rect("adit-w", -RING_X, -CORE_Z, -CORE_X, CORE_Z, floor=0, span=ADIT, theme="adit",
             mode=None),
        rect("adit-e", CORE_X, -CORE_Z, RING_X, CORE_Z, floor=0, span=ADIT, theme="adit", mode=None),
        # the two steps at the ramp feet. A ramp is an add on the deck's own layer and an override
        # add cannot put its top below that layer's floor, so it arrives at y20 and the pit floor is
        # y16: these close the four courses between as two scrambles. They stand under the pit's
        # subtract rather than in it — an add whose top stops at or below a hole's floor is the
        # ground under the void, which is the one add `SK13` allows there.
        rect("step-e", CORE_X, -3, CORE_X + 2, 3, floor=0, span=ADIT + 2, theme="adit", mode=None),
        rect("step-w", -CORE_X - 2, -3, -CORE_X, 3, floor=0, span=ADIT + 2, theme="adit",
             mode=None),
    ],
    "groups": [{"id": "under", "mirrors": False,
                "shapeIds": ["rock-n", "rock-s", "rock-w", "rock-e", "rock-core",
                             "adit-n", "adit-s", "adit-w", "adit-e",
                             "step-e", "step-w"]}],
}

# ── the cutting shed, and the saw frames ─────────────────────────────────────────────────────────
# A made layer is out of the stacking rules and painted over its own span, and `kind: "made"` keeps
# `SK10`'s pair walk and `SK11`'s reachability walk off it: a wall standing on a deck has no gap to
# lose and its roof is not a stair somebody forgot.
def bar(id_, x0, z0, x1, z1, floor, height, material):
    """One block of a built thing: a span of `height` courses whose base sits `floor` courses over
    the layer's own `base_y`."""
    return {"id": id_, "type": "rectangle", "operation": "add", "floor": floor,
            "base_height": height, "material": material,
            "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1}


# a `cell` painting a vertical resolves one block per column without a rise, which reads
# as stripes (`PT4`): a rise is the vertical period that gives a face its grain.
WALL = cell_(65, 5, [QUARTZ, WHITE_CLAY, Q_PILLAR], rise=3)
DOOR = 4                      # half-width of each doorway

shed_wall = {
    "id": "shed", "name": "Cutting shed", "base_y": YARD + 1, "kind": "made", "part_of": "shed",
    "seat": "ground",
    "shapes": [
        bar("shed-n-a", -SHED, -SHED, -DOOR, -SHED + 2, 0, 6, WALL),
        bar("shed-n-b",  DOOR, -SHED,  SHED, -SHED + 2, 0, 6, WALL),
        bar("shed-s-a", -SHED,  SHED - 2, -DOOR,  SHED, 0, 6, WALL),
        bar("shed-s-b",  DOOR,  SHED - 2,  SHED,  SHED, 0, 6, WALL),
        bar("shed-w-a", -SHED, -SHED + 2, -SHED + 2, -DOOR, 0, 6, WALL),
        bar("shed-w-b", -SHED,  DOOR, -SHED + 2,  SHED - 2, 0, 6, WALL),
        bar("shed-e-a",  SHED - 2, -SHED + 2,  SHED, -DOOR, 0, 6, WALL),
        bar("shed-e-b",  SHED - 2,  DOOR,  SHED,  SHED - 2, 0, 6, WALL),
        # the door heads: a lintel over each opening, so a doorway is a hole in a wall rather than
        # the wall stopping
        bar("lintel-n", -DOOR, -SHED, DOOR, -SHED + 2, 4, 2, CHISELLED),
        bar("lintel-s", -DOOR,  SHED - 2, DOOR,  SHED, 4, 2, CHISELLED),
        bar("lintel-w", -SHED, -DOOR, -SHED + 2, DOOR, 4, 2, CHISELLED),
        bar("lintel-e",  SHED - 2, -DOOR, SHED, DOOR, 4, 2, CHISELLED),
        # the corner posts, which carry the roof ring
        bar("post-nw", -SHED, -SHED, -SHED + 2, -SHED + 2, 0, 8, Q_PILLAR),
        bar("post-ne",  SHED - 2, -SHED,  SHED, -SHED + 2, 0, 8, Q_PILLAR),
        bar("post-sw", -SHED,  SHED - 2, -SHED + 2,  SHED, 0, 8, Q_PILLAR),
        bar("post-se",  SHED - 2,  SHED - 2,  SHED,  SHED, 0, 8, Q_PILLAR),
    ],
    "groups": [{"id": "shed", "mirrors": False,
                "shapeIds": ["shed-n-a", "shed-n-b", "shed-s-a", "shed-s-b", "shed-w-a",
                             "shed-w-b", "shed-e-a", "shed-e-b", "lintel-n", "lintel-s",
                             "lintel-w", "lintel-e", "post-nw", "post-ne", "post-sw", "post-se"]}],
}

# the roof: a ring of birch-framed slab over the walls, open in the middle. The louvre is what keeps
# the centre objective visible from the yard and from above — a shed roofed across is a goal nobody
# can see, and that is a different board.
roof = {
    "id": "shed-roof", "name": "Shed roof", "base_y": YARD + 9, "kind": "made", "part_of": "shed",
    "shapes": [
        bar("roof-n", -SHED - 1, -SHED - 1,  SHED + 1, -6, 0, 1, BIRCH_PLANK),
        bar("roof-s", -SHED - 1,  6,  SHED + 1,  SHED + 1, 0, 1, BIRCH_PLANK),
        bar("roof-w", -SHED - 1, -6, -6,  6, 0, 1, BIRCH_PLANK),
        bar("roof-e",  6, -6,  SHED + 1,  6, 0, 1, BIRCH_PLANK),
        # the ridge beams, laid over the roof so the shed reads as framed rather than lidded
        bar("beam-w", -11, -SHED - 1, -9, SHED + 1, 0, 2, LAID_BIRCH),
        bar("beam-e",   9, -SHED - 1, 11, SHED + 1, 0, 2, LAID_BIRCH),
    ],
    "groups": [{"id": "roof", "mirrors": False,
                "shapeIds": ["roof-n", "roof-s", "roof-w", "roof-e", "beam-w", "beam-e"]}],
}

# the saw frames: three iron gantries over the west pit and three over the east, which is what tells
# a player at fifty blocks which two holes in the deck are the ones worth standing in
frames = {
    "id": "frames", "name": "Saw frames", "base_y": YARD + 1, "kind": "made", "part_of": "frames",
    "shapes": [], "groups": [{"id": "frames", "mirrors": False, "shapeIds": []}],
}
for side, cx in (("w", PIT_W), ("e", PIT_E)):
    for n, dz in enumerate((-6, 0, 6)):
        for m, dx in enumerate((-8, 8)):
            frames["shapes"].append(bar(f"leg-{side}{n}{m}", cx + dx - 1, dz - 1, cx + dx + 1,
                                        dz + 1, 0, 5, IRON))
        frames["shapes"].append(bar(f"span-{side}{n}", cx - 9, dz - 1, cx + 9, dz + 1, 4, 1, IRON))
frames["groups"][0]["shapeIds"] = [s["id"] for s in frames["shapes"]]

# the block stacks on the loading bank: sawn alabaster waiting to go out, three to a side
stacks = {
    "id": "stacks", "name": "Block stacks", "base_y": SILL, "kind": "made", "part_of": "stacks",
    "shapes": [], "groups": [{"id": "stacks", "mirrors": False, "shapeIds": []}],
}
for n, (x, z, h) in enumerate([(-28, -46, 4), (-14, -44, 3), (2, -46, 5), (16, -43, 3),
                               (28, -46, 4), (-22, -49, 2), (10, -49, 2),
                               (28, 46, 4), (14, 44, 3), (-2, 46, 5), (-16, 43, 3),
                               (-28, 46, 4), (22, 49, 2), (-10, 49, 2)]):
    stacks["shapes"].append(bar(f"stack-{n}", x - 3, z - 3, x + 3, z + 3, 0, h,
                                cell_(70 + n, 3, [Q_CHISEL, QUARTZ, Q_PILLAR, PALE_CLAY], rise=2)))
stacks["groups"][0]["shapeIds"] = [s["id"] for s in stacks["shapes"]]

# ── the lodge ────────────────────────────────────────────────────────────────────────────────────
def works_style(storeys):
    return {
        "foundation": {"plate": {"stack": stack([(1, Q_CHISEL)], "repeat"), "extent": 1},
                       "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                                   "inlayInset": 2, "isPlain": True},
                       "footing": STONEBRICK},
        "roof": {"form": "gable", "pitch": 1, "slab": Q_SLAB, "slabData": 7, "overhang": 1,
                 "ridgeCap": True, "hole": False,
                 "body": QUARTZ, "verge": LAID_BIRCH, "gable": BIRCH_PLANK,
                 "gableWindows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0,
                                  "data": 0, "sill": 1, "width": 1, "height": 1, "spacing": 3}},
        "wall": {"stack": stack([(4, cell_(66, 4, [QUARTZ, WHITE_CLAY, PALE_CLAY], rise=3)),
                                 (1, Q_PILLAR)], "repeat"), "extent": 5},
        "post": Q_PILLAR,
        "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                    "sill": 2, "width": 2, "height": 2, "spacing": 4},
        "storeys": storeys,
        "porch": None, "front": None,
        "beams": {"block": 17, "data": 2, "reach": 1, "any": True},
        "doorway": {"door": "air", "head": {"form": "none", "block": 53, "fill": "upperSlab",
                                            "fillBlock": Q_SLAB, "fillData": 7},
                    "width": 2, "height": 3},
    }


FLOOR_STOREY = {
    "clear": 5, "post": Q_PILLAR, "deck": None,
    "wall": {"stack": stack([(2, STONEBRICK), (3, WHITE_CLAY)], "repeat"), "extent": 4},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 2, "width": 2, "height": 2, "spacing": 4},
}
LOFT_STOREY = {
    "clear": 3, "post": BIRCH_LOG, "deck": None,
    "wall": {"stack": stack([(2, PALE_CLAY), (1, LAID_BIRCH)], "repeat"), "extent": 3},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 1, "width": 1, "height": 1, "spacing": 4},
}
lodge = works_style([FLOOR_STOREY, LOFT_STOREY])
shed_house = works_style([dict(FLOOR_STOREY, clear=4)])


def path(id_, points, radius, pave, style="solid", coverage=1.0, seed=0, claims=True):
    return {"id": id_, "kind": "stroke", "seed": seed, "radius": radius, "style": style,
            "coverage": coverage, "claimsGround": claims, "pave": pave, "points": points}


TRAM = cell_(67, 4, [POLISHED, IRON, ANDESITE, GRAVEL], rise=2)     # the surface tramway, iron on stone

props = [
    # the tramways on the deck: out of each lodge door, along the yard, and round the shed to the two
    # pit heads. They are the one iron-grey line on a pale board and they are what the eye follows.
    path("tram-spine", [[0, 66], [0, 54], [-2, 40], [-18, 26], [PIT_W, 12], [PIT_W, 8]],
         2, TRAM, seed=71),
    path("tram-east",  [[6, 64], [8, 52], [10, 40], [20, 28], [PIT_E, 14], [PIT_E, 8]],
         2, TRAM, seed=72),
    path("tram-bank",  [[-32, 46], [0, 44], [32, 46]], 2, TRAM, seed=73),
    path("tram-shed",  [[-22, 18], [-10, 18], [0, 20]], 2, TRAM, seed=74),
]

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-14",
    "themes": themes,
    "mapTheme": "yard",
    # Extreme Hills tints grass and water a cold grey-green, which suits a stone works and keeps the
    # board in the same cold family as the other three without repeating a biome
    "biome": {"kind": "solid", "id": 3},
    "relief": relief,
    # the deck is four courses standing on the rock at y20, which is what leaves the storey under it
    # somewhere to be. Lift the surface without thinning the slab and the undercroft has no room.
    "shapePropsByHeight": {str(YARD): {"floor": DECK_FLOOR, "base_height": YARD - DECK_FLOOR},
                           str(YARD + 1): {"floor": DECK_FLOOR,
                                           "base_height": YARD + 1 - DECK_FLOOR}},
    "themeByHeight": {str(YARD): "yard", str(YARD + 1): "yard"},
    "addShapes": add_shapes,
    "addLayers": [under, shed_wall, roof, frames, stacks],
    "roomStyles": {"spawn": lodge},
    "dressing": {"styles": {}, "props": props},
    "controlPoints": [
        {"name": "The Cutting Shed", "anchor": {"x": 0, "y": 0, "z": 0}, "size": 9, "points": 2},
        {"name": "West Sawpit", "anchor": {"x": PIT_W - 1, "y": 0, "z": 0}, "size": 7, "points": 1},
        {"name": "East Sawpit", "anchor": {"x": PIT_E + 1, "y": 0, "z": 0}, "size": 7, "points": 1},
    ],
    "scoreLimit": 750,
}

json.dump(plan,   open(os.path.join(HERE, f"{SLUG}.plan.json"),   "w"), indent=1)
json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json  "
      f"({len(plan['pieces'])} pieces, {len(relief['team']['marks'])} marks, "
      f"{len(add_shapes)} shapes, {len(finish['addLayers'])} layers, "
      f"{sum(len(L['shapes']) for L in finish['addLayers'])} layer shapes, {len(props)} props)")
