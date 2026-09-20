"""Potsherd — a DTC board on a terracotta brickfield.

Each team's core stands in the open at the head of its own kiln yard, on the lip of a terrace with
the clay pit cut seven blocks below it, and the drying-shed rows behind. An attacker crosses the
brickfield in the middle, drops into the pit or goes round its rim, and has to come up the haul
road under the core to reach it.

Four grounds meet on it and each is stated by the one instrument that can state it:

  the shed rows      an area mark at 25, where the sheds stand and the spawn is
  the kiln terrace   an area mark at 24 carrying the cores and the two bottle kilns
  the clay pit       an area mark at 17 with a bench mark at 20 inside it, because a worked pit
                     is stepped and one pan is a hole
  the brickfield     an area mark at 20 across the middle, the one ground both teams stand on

The pit's walls are the board's argument. `wallOnTerrainFaces` puts a run of stained clay courses
on every exposed riser, so the cut face reads as bedded clay — orange over brown over white — and
that is the only place the pale band appears. Every theme boundary on this board lies on a break
of slope or on a built riser: the pit floor meets the terrace over a seven-block face, and the
works ground stands a course proud of the clay wherever it is laid.

Four ways off the pit floor a team, and every one is authored rather than graded: the haul road
from the terrace, a step out to the brickfield, and a step off each rim.
"""

import json, math, os, sys

SLUG = "opus5-potsherd"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "sculpt"))
import props

CELL = 4
SHEDS = 25           # the drying-shed rows and the camp
TERRACE = 24         # the kiln terrace, and the lip the core stands on
RIM = 23             # the unquarried clay either side of the pit
FIELD = 20           # the brickfield in the middle
BENCH = 20           # the worked bench inside the pit
PIT = 17             # the pit floor


# ── the plan: the arrangement, and nothing else ──────────────────────────────────────────────
def plan():
    return {
        "plan": 2,
        "meta": {"name": "Potsherd"},
        "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 16,
                    "surface": FIELD, "observerY": 60},
        "pieces": [
            # the shed rows                                blocks x -52..52, z -96..-76
            {"id": "works",   "role": "piece", "rect": [-13, -24, 26, 5], "surface": SHEDS},
            # the camp standing in them. 28 x 20 blocks, because ST10 caps a spawn piece at
            # 30 x 20 and the piece is what the protection is cut from.
            {"id": "camp",    "role": "spawn", "rect": [ -4, -24,  7, 5], "surface": SHEDS},
            # the kiln terrace, which the core stands at the front of
            #                                              blocks x -52..52, z -76..-52
            {"id": "terrace", "role": "piece", "rect": [-13, -19, 26, 6], "surface": TERRACE},
            # the clay pit, cut into it, and the unquarried clay either side
            #                                              blocks x -36..36, z -52..-32
            {"id": "pit",     "role": "piece", "rect": [ -9, -13, 18, 5], "surface": PIT},
            {"id": "rim-w",   "role": "piece", "rect": [-13, -13,  4, 5], "surface": RIM},
            {"id": "rim-e",   "role": "piece", "rect": [  9, -13,  4, 5], "surface": RIM},
            # the brickfield                               blocks x -52..52, z -32..-12
            {"id": "field",   "role": "piece", "rect": [-13,  -8, 26, 5], "surface": FIELD},
            # and its middle, the one piece both teams stand on
            #                                              blocks x -44..44, z -12..12
            {"id": "mid",     "role": "piece", "rect": [-11,  -3, 22, 6], "surface": FIELD},
        ],
        "zones": [{"id": "brickfield", "rect": [-11, -5, 22, 10], "kind": "build"}],
        "placements": {
            # camp's corner is (-16, -96): the point is (-2, -86) and the room x -10..6,
            # which leaves each iron cube its 3 x 3 and two blocks of air to the shell
            "spawns": [{"id": "spawn-1", "piece": "camp", "at": [14, 10], "facing": "back",
                        "footprint": [6, 3, 16, 14]}],
            "iron": [{"id": "iron-1", "piece": "camp", "at": [3, 10]},
                     {"id": "iron-2", "piece": "camp", "at": [25, 10]}],
            # terrace's corner is (-52, -76), so the core is at (-34, -60): out in the open
            # between the two kiln yards and clear of the lip's own grade, and thirty-four off
            # the centre line, which is what puts the far flank on somebody's journey
            "cores": [{"id": "core-1", "piece": "terrace", "at": [18, 16], "lava": 3,
                       "lavaHeight": 3, "float": 6, "leak": 5, "name": "The Kiln Core"}],
            "destroyables": [],
            "wools": [],
        },
    }


# ── what it is made of ───────────────────────────────────────────────────────────────────────
# Three tone families, named before anything is painted:
#   ground  hardened clay and stained clay -- mid-value warm orange-brown, the middle of this run
#   built   brick and sandstone, which is nearer the clay than any pale stone would be
#   accent  whitewashed birch on the sheds, and the white course in the pit's bedding
def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}

def cell(seed, size, *palette):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": 2, "warp": 3,
            "palette": list(palette), "rise": 0}

def depth_stack(*bands):
    return {"kind": "layered", "axis": "depth",
            "stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]}}

def by_slope(*bands):
    """One stack finishing the pan, the shoulder and the cut face of the same clay. A thickness on
    the slope axis is a span of degrees, which is the only axis that tells a pit wall from a pan."""
    return {"kind": "layered", "axis": "slope",
            "stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]}}


HARDCLAY = solid(172)
CLAY_ORANGE = solid(159, 1)
CLAY_BROWN = solid(159, 12)
CLAY_WHITE = solid(159, 0)
CLAY_YELLOW = solid(159, 4)
CLAY_RED = solid(159, 14)
RAW_CLAY = solid(82)
BRICK = solid(45)
BRICK_STONE = solid(98)
SANDSTONE = solid(24)
SMOOTH = solid(24, 2)
CHIS = solid(24, 1)
GRASS = solid(2)
GRAVEL = solid(13)
DIRT = solid(3)
COARSE = solid(3, 1)
STONE = solid(1)
COBBLE = solid(4)
ANDESITE = solid(1, 5)
BIRCH = solid(5, 2)
BIRCH_LOG = solid(17, 2)

# The terrace is baked clay gone over to orange in patches, at a brush wide enough to read as
# patches rather than speckle. The shoulder is the worked clay with silt in it. The face is the
# bedding the pit is cut through, which is the whole reason this board has a pit in it.
TERRACE_TOP = cell(21, 12, HARDCLAY, CLAY_ORANGE, HARDCLAY, COARSE)
SHOULDER_TOP = cell(23, 9, COARSE, HARDCLAY, CLAY_BROWN, HARDCLAY)


def clay_theme():
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void",
        # the pit's cut walls get their bedding from the wall bucket, and this board has more
        # exposed riser than any other in the run -- which is what the bedding is for
        "wallOnTerrainFaces": True,
        "rim": {"material": CLAY_ORANGE, "depth": 1, "enabled": True},
        "surface": {"depth": 4, "enabled": True, "material": by_slope(
            (depth_stack((TERRACE_TOP, 1), (HARDCLAY, 2), (SANDSTONE, 1)), 12),
            (depth_stack((SHOULDER_TOP, 1), (HARDCLAY, 1), (CLAY_BROWN, 2)), 16),
            (depth_stack((CLAY_BROWN, 2), (CLAY_ORANGE, 1), (HARDCLAY, 1)), 62))},
        # the beds, in courses: orange over brown over white over yellow. The white is the only
        # pale band on the board and it appears on a cut face and nowhere else.
        "wall": {"kind": "wallRun", "runs": [
            {"material": CLAY_ORANGE, "width": 2},
            {"material": CLAY_BROWN, "width": 3},
            {"material": CLAY_WHITE, "width": 1},
            {"material": CLAY_YELLOW, "width": 2},
            {"material": HARDCLAY, "width": 3}]},
        "wallEnabled": True,
        "fill": {"kind": "voronoi", "seed": 17, "cellSize": 15, "rise": 7, "bands": [
            {"material": HARDCLAY, "depth": 2}, {"material": CLAY_BROWN, "depth": 1}]},
    }


def pit_theme():
    """The dug floor: raw clay, spoil and the gravel under it. Duller and darker than the terrace,
    and every edge of it lies at the foot of a face rather than across flat ground."""
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void",
        "wallOnTerrainFaces": False,
        "rim": {"material": CLAY_BROWN, "depth": 1, "enabled": True},
        "surface": {"depth": 3, "enabled": True, "material": depth_stack(
            (cell(29, 8, RAW_CLAY, CLAY_BROWN, COARSE, GRAVEL), 1),
            (CLAY_BROWN, 1), (HARDCLAY, 1))},
        "wall": {"kind": "wallRun", "runs": [
            {"material": CLAY_BROWN, "width": 2}, {"material": CLAY_YELLOW, "width": 1}]},
        "wallEnabled": True,
        "fill": {"kind": "voronoi", "seed": 19, "cellSize": 13, "rise": 6, "bands": [
            {"material": HARDCLAY, "depth": 2}, {"material": CLAY_BROWN, "depth": 1}]},
    }


def works_theme():
    """The kiln yards and the haul road: laid brick with sandstone flags. Brick is the clay this
    board is made of, fired -- so the built family sits a shade off the ground rather than
    against it, and what separates them is the course it stands proud by."""
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop",
        "wallOnTerrainFaces": True,
        "rim": {"material": CHIS, "depth": 1, "enabled": True},
        "surface": {"depth": 2, "enabled": True, "material": depth_stack(
            (cell(31, 6, BRICK, SANDSTONE, BRICK, BRICK_STONE), 1), (BRICK, 1))},
        "wall": {"kind": "wallRun", "runs": [
            {"material": BRICK, "width": 3},
            {"material": SANDSTONE, "width": 1},
            {"material": BRICK, "width": 2}]},
        "wallEnabled": True,
        "fill": solid(45),
    }


def sward_theme():
    """A seat of soil for a tree, and the only green on the board. The Desert tint puts grass at straw, so a patch of grass on
    dry ground reads as scrub holding on rather than as a lawn; the cell carries the ground's own
    top block as well, so the patch feathers out instead of ending on a line. A copied tree body
    wants soil under it, and stained clay is not soil."""
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void",
        "wallOnTerrainFaces": False,
        "rim": {"material": COARSE, "depth": 1, "enabled": True},
        "surface": {"depth": 3, "enabled": True, "material": depth_stack(
            (cell(61, 6, GRASS, COARSE, COARSE, GRASS), 1), (DIRT, 2), (HARDCLAY, 1))},
        "wall": {"kind": "wallRun", "runs": [
            {"material": DIRT, "width": 2}, {"material": COARSE, "width": 1}]},
        "wallEnabled": True,
        "fill": {"kind": "voronoi", "seed": 23, "cellSize": 11, "rise": 5, "bands": [
            {"material": HARDCLAY, "depth": 2}, {"material": CLAY_BROWN, "depth": 1}]},
    }


def patch(name, cx, cz, radius, seed):
    """One sward patch: a seven-point ring with the radius wobbled per point, so a seat of soil is
    a shape the ground could have made rather than a disc somebody stamped."""
    ring = []
    for step in range(7):
        angle = 2 * math.pi * step / 7
        wobble = radius * (0.72 + 0.28 * ((seed * (step + 3) * 37) % 11) / 10.0)
        ring.append([round(cx + wobble * math.cos(angle)),
                     round(cz + wobble * math.sin(angle))])
    return {"id": name, "type": "polygon", "operation": "add", "height_mode": "raise",
            "base_height": 0, "skirt": 0, "vertices": ring, "theme": "sward"}


# ── the ground, as four things that meet ─────────────────────────────────────────────────────
def marks():
    """In solve order: a later mark wins a contested cell, so the terraces are stated from the
    back forward, the pit cut through them, and the bench laid on the pit's own floor."""
    return [
        {"id": "works-pan", "kind": "area", "h": SHEDS, "bevel": 3,
         "ring": [[-54, -99], [-28, -97], [0, -99], [26, -96], [54, -98],
                  [53, -76], [26, -73], [-2, -76], [-28, -73], [-54, -75]]},
        {"id": "terrace-pan", "kind": "area", "h": TERRACE, "bevel": 4,
         "ring": [[-54, -78], [-28, -75], [0, -78], [26, -75], [54, -77],
                  [53, -52], [26, -49], [-4, -53], [-30, -50], [-54, -52]]},
        # the unquarried clay either side of the pit, held to its edge so the pit's side walls
        # are faces and not grades
        {"id": "rim-w-pan", "kind": "area", "h": RIM, "bevel": 2,
         "ring": [[-54, -54], [-42, -51], [-34, -54], [-33, -32], [-42, -29], [-54, -32]]},
        {"id": "rim-e-pan", "kind": "area", "h": RIM, "bevel": 2,
         "ring": [[33, -54], [42, -51], [54, -54], [54, -32], [42, -29], [34, -32]]},
        {"id": "field-pan", "kind": "area", "h": FIELD, "bevel": 4,
         "ring": [[-54, -34], [-28, -31], [0, -35], [28, -31], [54, -34],
                  [54, -10], [28, -7], [0, -11], [-28, -7], [-54, -10]]},
        # the middle, reaching past the centre so its own mirror overlaps it
        {"id": "mid-pan", "kind": "area", "h": FIELD, "bevel": 3,
         "ring": [[-46, -14], [-20, -11], [8, -15], [34, -11], [46, -14],
                  [46, 5], [20, 8], [-8, 4], [-34, 8], [-46, 5]]},
        # the pit. Its lip wanders five blocks either side of the plan's straight z, which is what
        # keeps the frontline the board's best-defended edge off a ruled line.
        {"id": "pit-pan", "kind": "area", "h": PIT, "bevel": 1,
         "ring": [[-34, -50], [-20, -46], [-4, -51], [12, -45], [28, -50], [34, -45],
                  [33, -35], [16, -31], [0, -36], [-16, -32], [-30, -36], [-35, -42]]},
        # and the bench worked into its west end: a pit is dug in steps, and a single pan is a
        # hole rather than a quarry
        {"id": "bench-pan", "kind": "area", "h": BENCH, "bevel": 1,
         "ring": [[-33, -49], [-22, -46], [-14, -49], [-13, -39], [-22, -35], [-32, -38]]},
    ]


def pushes():
    """Added to the solved surface after the marks, so each is kept off ground a mark had to
    arrive at: the core's lip, the haul road's head and foot, and the sheds."""
    return [
        # spoil, thrown out of the pit onto the terrace behind it
        {"id": "spoil-w", "ring": [[-52, -60], [-44, -58], [-40, -54], [-48, -52], [-53, -55]],
         "amount": 2.6, "falloff": 12, "crown": 1.1, "roughness": 1.4, "seed": 4},
        {"id": "spoil-e", "ring": [[30, -70], [44, -68], [48, -58], [38, -54], [28, -60]],
         "amount": 2.2, "falloff": 11, "crown": 0.9, "roughness": 1.2, "seed": 11},
        # a low swell across the brickfield, so the middle is not a table
        {"id": "swell", "ring": [[-30, -18], [-10, -15], [4, -10], [-8, -4], [-28, -8]],
         "amount": 1.6, "falloff": 8, "crown": 0.7, "roughness": 0.9, "seed": 21},
        # and the heap the sheds stand behind
        {"id": "heap", "ring": [[14, -94], [30, -92], [32, -82], [20, -78], [12, -86]],
         "amount": 2.0, "falloff": 12, "crown": 0.8, "roughness": 1.1, "seed": 31},
    ]


def shapes():
    """What the plan cannot state: the kiln yards, the haul road down into the pit, and the three
    steps back out of it."""
    out = []

    # The two kiln yards, a course proud of the terrace so the meeting is a riser rather than a
    # change of colour on flat ground. The kilns stand on them, and they are what the core has
    # behind it. Nothing is laid under the core itself: it stands on bare clay at the lip, which
    # is what puts it in the open.
    for name, ring in (("yard-kiln-w", [[-53, -76], [-46, -76], [-39, -76],
                                        [-38, -71], [-40, -66], [-47, -65], [-53, -69]]),
                       ("yard-kiln-e", [[-23, -76], [-16, -76], [-9, -76],
                                        [-8, -71], [-10, -66], [-17, -65], [-23, -69]])):
        out.append({"id": name, "type": "polygon", "operation": "add",
                    "base_height": TERRACE + 1, "relief_scope": "exclude", "keepClear": True,
                    "theme": "works", "vertices": ring})

    # The haul road: level, sheer-sided, out of the relief's solve so it arrives where it was
    # told. Twenty-two blocks of run against seven of rise, and a material rather than a theme --
    # a road is a thing somebody built and a theme is a place.
    out.append({"id": "haul", "type": "polygon", "operation": "add",
                "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
                "keepClear": True, "floor": 0,
                "vertices": [[6, -56], [20, -56], [20, -34], [6, -34]],
                "anchor_heights": [TERRACE, TERRACE, PIT, PIT],
                "material": {"kind": "cell", "seed": 37, "cellSize": 6, "jitter": 1, "warp": 2,
                             "palette": [BRICK, COARSE, BRICK, SANDSTONE], "rise": 3}})

    # The revetments either side of its head, holding the terrace back off the road. Out of the
    # solve, so they keep the height they were drawn at while the ground falls away under them.
    for side, xs in (("w", 4), ("e", 22)):
        out.append({"id": f"revet-{side}", "type": "polyline", "operation": "add",
                    "radius": 1, "stroke_edge": "solid", "base_height": TERRACE + 1,
                    "relief_scope": "exclude", "keepClear": True,
                    "vertices": [[xs, -57], [xs, -50], [xs, -43], [xs, -36]],
                    "material": {"kind": "layered", "axis": "depth", "stack": {
                        "ending": "repeat", "bands": [
                            {"material": CHIS, "thickness": 1},
                            {"material": BRICK, "thickness": 4}]}}})

    # The step out of the pit onto the brickfield, and one off each rim, so the pit is not a trap
    # and the flanks are not a wall. Each is graded ground rather than masonry -- spoil trodden
    # down, in the clay's own family.
    scree = {"kind": "cell", "seed": 39, "cellSize": 7, "jitter": 2, "warp": 3,
             "palette": [COARSE, HARDCLAY, CLAY_BROWN, GRAVEL], "rise": 2}
    out.append({"id": "pit-step", "type": "polygon", "operation": "add",
                "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
                "keepClear": True, "floor": 0,
                "vertices": [[-24, -38], [-12, -38], [-12, -24], [-24, -24]],
                "anchor_heights": [PIT, PIT, FIELD, FIELD], "material": scree})
    # and the step off the worked bench onto the pit floor, which two marks pinning their bands
    # exactly would otherwise leave as one three-block cell of wall (RL3)
    out.append({"id": "bench-step", "type": "polygon", "operation": "add",
                "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
                "keepClear": True, "floor": 0,
                "vertices": [[-16, -48], [-16, -40], [-8, -40], [-8, -48]],
                "anchor_heights": [BENCH, BENCH, PIT, PIT], "material": scree})
    for side, (x0, x1) in (("w", (-48, -38)), ("e", (38, 48))):
        out.append({"id": f"rim-step-{side}", "type": "polygon", "operation": "add",
                    "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
                    "keepClear": True, "floor": 0,
                    "vertices": [[x0, -37], [x1, -37], [x1, -25], [x0, -25]],
                    "anchor_heights": [RIM, RIM, FIELD, FIELD], "material": scree})

    # Where the spoil has been raked back over the pit floor, the ground the digging left. A brush
    # states a height_mode or it is never a candidate for the paint at all; a raise of zero sits
    # flush on ground a mark already pinned and changes no height. Each of these lies inside the
    # pit, so its edge is the pit's own wall and not a line drawn across flat clay.
    out.append({"id": "pit-floor", "type": "polygon", "operation": "add",
                "height_mode": "raise", "base_height": 0, "skirt": 0, "theme": "pit",
                "vertices": [[-33, -49], [-20, -45], [-4, -50], [12, -44], [27, -49], [33, -44],
                             [32, -36], [16, -32], [0, -37], [-16, -33], [-29, -37], [-34, -42]]})

    # The sward: a seat of soil under every tree the author found standing on hardened or stained
    # clay. A brush states a height_mode or it is never a candidate for the paint at all, and a
    # raise of zero sits flush on ground a mark already pinned.
    for at, (px, pz, pr) in enumerate([(44, -78, 6), (44, -64, 6), (-38, -80, 6),
                                       (24, -16, 6), (-8, -18, 6), (46, -42, 6)]):
        out.append(patch(f"sward-{at}", px, pz, pr, 3 + at))
    return out


def kilns():
    """Two bottle kilns on the terrace, one each side of the core and set back from it, so they
    frame the approach rather than stand in it. The pair is drawn once and fanned, so each team's
    core is framed by its own two. A tapered tower is nested annuli whose tops rise inward, which is
    one layer and not a stack of block soup."""
    made = []
    brickwork = {"kind": "cell", "seed": 57, "cellSize": 5, "jitter": 1, "warp": 2,
                 "palette": [BRICK, CLAY_BROWN, BRICK, CLAY_ORANGE], "rise": 4}
    for kiln_id, cx, cz in (("kiln-w", -46, -70), ("kiln-e", -16, -70)):
        layer = props.tapered_tower(kiln_id, cx, cz, base_radius=6, top_radius=3, thickness=2,
                                    floor=TERRACE + 1, height=15, theme=None,
                                    name=f"Kiln {kiln_id[-1]}")
        inner = layer.pop("layout")
        layer["shapes"] = inner["shapes"]
        layer["groups"] = inner["groups"]
        layer["kind"] = "made"
        layer["part_of"] = "kilns"
        for shape in layer["shapes"]:
            shape.pop("theme", None)
            shape["material"] = brickwork
        made.append(layer)
    return made


# ── what a team walks out of ─────────────────────────────────────────────────────────────────
def band(*bands):
    return {"stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]},
            "extent": sum(t for _m, t in bands)}

def window(form, block, width=1, height=2, sill=2, spacing=4, data=0):
    return {"form": form, "block": block, "hostBlock": -1, "hostData": 0, "data": data,
            "sill": sill, "width": width, "height": height, "spacing": spacing}

PLAIN_SURFACE = {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                 "inlayInset": 2, "isPlain": True}


def potters_hall():
    """The spawn hall. Brick to the sill and whitewashed birch above it, birch posts at the
    corners and a beam course of laid log where the storey changes -- a beam has to be the end of
    something. No footing: over a plate one course deep it is a rim round a building with no
    foundation. The roof slab is the roof body's own material (HS3) and the door head's stair and
    its fill are one material (HS4)."""
    return {
        "foundation": {"plate": band((BRICK, 1)), "surface": PLAIN_SURFACE, "footing": None},
        "roof": {"form": "gable", "pitch": 1, "slab": 44, "slabData": 4, "overhang": 1,
                 "ridgeCap": True, "hole": False,
                 "body": BRICK, "verge": {"kind": "laidLog", "id": 17, "data": 2},
                 "gable": BIRCH,
                 "gableWindows": window("pane", 102, width=1, height=2, sill=1, spacing=3)},
        "wall": band((BRICK, 4), (BIRCH, 4)),
        "post": BIRCH_LOG,
        "windows": window("pane", 102, width=2, height=2, sill=3, spacing=4),
        "storeys": [
            {"clear": 5, "wall": band((BRICK, 2), (BIRCH, 4)), "post": BIRCH_LOG,
             "windows": window("pane", 102, width=2, height=2, sill=3, spacing=4),
             "surface": PLAIN_SURFACE, "deck": None, "headroom": 5},
        ],
        "porch": None, "front": None,
        "beams": {"block": 17, "data": 2, "reach": 1, "any": False},
        "doorway": {"door": "air", "width": 2, "height": 3,
                    "head": {"form": "arched", "block": 108, "fill": "upperSlab",
                             "fillBlock": 44, "fillData": 4}},
    }


def drying_shed():
    """One style, and the four plots differ in height and footprint and in nothing else, which is
    what makes four buildings a row rather than four ideas. Open-sided in fact, low and long."""
    shell = potters_hall()
    shell["wall"] = band((BRICK, 2), (BIRCH, 3))
    shell["storeys"] = []
    shell["roof"] = dict(shell["roof"], form="hip", pitch=1, overhang=2, ridgeCap=False)
    shell["windows"] = window("pane", 102, width=3, height=2, sill=2, spacing=2)
    return {"kind": "house", "shell": shell}


def dressing():
    trees = json.load(open(f"{HERE}/trees.json"))
    styles = dict(trees)
    styles["shed"] = drying_shed()
    # A boulder is stone: stone, cobblestone and andesite is the whole palette that reads as rock
    # against any ground, and on a clay board a clay-coloured boulder is one nobody can see.
    styles["rock"] = {"kind": "boulder", "form": "angular", "size": 3.0, "mossy": False,
                      "rock": cell(53, 4, STONE, COBBLE, ANDESITE, STONE)}

    paving = cell(43, 5, COARSE, HARDCLAY, BRICK, COARSE)
    props_out = [
        # Out of the camp door, along the shed row, down onto the terrace past the kilns and onto
        # the haul road's head. Three blocks a reader cannot quite tell apart, solid, because a
        # worn band reads as litter and a path is a claim about where people walk.
        {"id": "track-out", "kind": "stroke", "seed": 41, "radius": 2, "style": "solid",
         "coverage": 1.0, "claimsGround": True, "pave": paving,
         "points": [[-2, -77], [-5, -70], [-9, -64], [-13, -60]]},
        # west along the terrace, in front of the kiln yards, to the core
        {"id": "track-core", "kind": "stroke", "seed": 43, "radius": 2, "style": "solid",
         "coverage": 1.0, "claimsGround": True, "pave": paving,
         "points": [[-13, -60], [-20, -58], [-27, -58], [-33, -59]]},
        # and east to the haul road's head, then down it
        {"id": "track-haul", "kind": "stroke", "seed": 42, "radius": 2, "style": "solid",
         "coverage": 1.0, "claimsGround": True, "pave": paving,
         "points": [[-13, -60], [-2, -58], [6, -57], [12, -55]]},
        {"id": "track-road", "kind": "stroke", "seed": 45, "radius": 2, "style": "solid",
         "coverage": 1.0, "claimsGround": True, "pave": paving,
         "points": [[12, -55], [12, -48], [13, -40], [13, -35]]},
        # the barrow run out of the pit onto the brickfield
        {"id": "track-step", "kind": "stroke", "seed": 44, "radius": 2, "style": "solid",
         "coverage": 0.9, "claimsGround": True, "pave": paving,
         "points": [[-18, -40], [-18, -34], [-18, -28], [-20, -22]]},
        # The drying rows: green brick laid out on the brickfield in courses. Not a road -- so
        # not solid -- and the one thing on this board that says what the middle is for.
        {"id": "rows-w", "kind": "stroke", "seed": 47, "radius": 3, "style": "stones",
         "coverage": 0.8, "claimsGround": True,
         "pave": cell(48, 4, BRICK, HARDCLAY, BRICK, CLAY_ORANGE),
         "points": [[-44, -26], [-30, -24], [-16, -26], [-4, -23]]},
        {"id": "rows-e", "kind": "stroke", "seed": 49, "radius": 3, "style": "stones",
         "coverage": 0.8, "claimsGround": True,
         "pave": cell(50, 4, BRICK, HARDCLAY, BRICK, CLAY_ORANGE),
         "points": [[8, -20], [22, -18], [36, -21], [48, -18]]},
    ]

    # The shed rows: four plots in a line either side of the camp, differing in height and
    # footprint and in nothing else.
    for at, (x0, z0, tall) in enumerate([(-50, -94, 0), (-32, -94, 1),
                                         (18, -94, 0), (36, -94, 1)]):
        props_out.append({"id": f"shed-{at}", "kind": "house", "seed": 501 + at,
                          "front": "posZ", "style": "shed",
                          "wings": [{"corners": [[x0, z0], [x0 + 11, z0 + 8]],
                                     "spec": {"storeysHigh": tall, "ridge": "alongX"}}]})

    # Boulders: the stone that came out of the clay, left where the digging left it.
    for at, (bx, bz) in enumerate([(-26, -42), (-4, -44), (28, -42), (2, -44),
                                   (-48, -16), (30, -26), (-30, -80), (40, -80)]):
        props_out.append({"id": f"rock-{at}", "kind": "boulder", "seed": 610 + at,
                          "x": bx, "z": bz, "style": "rock"})

    # Birch on the terrace and the shed rows, a roundel where the spoil has grassed over. None in
    # the pit, which is worked ground and carries nothing tall.
    plant = [("birk-1", -48, -56), ("birk-2", 44, -78), ("birk-3", 4, -66),
             ("birk-1", 48, -70), ("roundel-1", -46, -40), ("birk-2", 44, -64),
             ("birk-3", -38, -80), ("roundel-1", 30, -74), ("birk-1", -40, -20),
             ("birk-2", 24, -16), ("birk-3", -8, -18), ("roundel-1", 46, -42)]
    for at, (style, tx, tz) in enumerate(plant):
        props_out.append({"id": f"birk-{at}", "kind": "tree", "seed": 700 + at,
                          "x": tx, "z": tz, "style": style})

    # Ground cover over the whole board rather than in patches: the density field is better at
    # patchiness than a hand-drawn outline is, and both gameplay numbers stay low -- tall grass is
    # cover nobody authored, in front of an objective nobody chose.
    props_out.append({"id": "cover", "kind": "flora", "seed": 800,
                      "points": [[-58, -102], [58, -102], [58, 14], [-58, 14]],
                      "spec": {"coverage": 0.12, "scale": 28, "octaves": 3, "fernShare": 0.05,
                               "flowerShare": 0.03, "flowerScale": 16, "tallShare": 0.03}})
    return {"styles": styles, "props": props_out}


def finish():
    return {
        "authors": [{"name": "Opus 5"}],
        "created": "2026-09-14",
        # Desert: no green tint at all, which is what a brickfield wants. It is the one colour
        # here a block does not state for itself.
        "biome": {"kind": "solid", "id": 2},
        "themes": {"clay": clay_theme(), "pit": pit_theme(), "works": works_theme(),
                   "sward": sward_theme()},
        "mapTheme": "clay",
        # the board's outer edge, drawn as an edge rather than as the staircase of rectangles the
        # plan compiled to. The pit's own lip is the pit-pan mark's ring and is not bent.
        "bendShapes": {"camp-25": {"k": 0.16, "wander": 3, "step": 12, "seed": 5},
                       "camp-24": {"k": 0.18, "wander": 3, "step": 12, "seed": 9},
                       "camp-20": {"k": 0.16, "wander": 3, "step": 12, "seed": 13}},
        "relief": {"*": {"base": FIELD, "reach": 0, "step": 1, "landform": "plain",
                         "grain": {"amplitude": 1.0, "scale": 18, "seed": 7},
                         "marks": marks(), "pushes": pushes()}},
        "addShapes": shapes(),
        "addLayers": kilns(),
        "roomStyles": {"spawn": potters_hall()},
        "dressing": dressing(),
    }


if __name__ == "__main__":
    with open(f"{HERE}/{SLUG}.plan.json", "w") as handle:
        json.dump(plan(), handle, indent=2)
    with open(f"{HERE}/{SLUG}.finish.json", "w") as handle:
        json.dump(finish(), handle, indent=2)
    print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")
