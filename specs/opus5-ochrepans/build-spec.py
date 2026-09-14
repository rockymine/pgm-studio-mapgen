"""Ochrepans — a KotH board on an ochre salt-works.

Three square pads, and none of them is a hill. The middle one is sunk four blocks in a walled
evaporation yard; the other two stand four blocks up on the raised pan banks out on either flank.
A board where every sightline is broken by a pan wall rather than by a rise, which is why the
relief here is the quietest of the four and the structure the loudest.

The ground is stated four ways and each by the one instrument that can state it:

  the salt flat      base 22, with low heaps of harvested salt pushed up on it
  the pans           sixteen square area marks one block down, so every pan edge is a bench and
                     the pale crust inside it never meets the ochre on flat ground
  the yard           one area mark at 18, walled, with four gates cut through the wall and a
                     flight down through each
  the pan banks      one area mark at 26 — stated once, because its own rot_180 image is the
                     other bank — with two ramps up onto each

The wall is the board's argument. It is a polyline shape out of the relief's solve, three courses
proud of the flat and seven above the yard floor, so it cannot be climbed and cannot be seen over;
the four gates are the only ways in, and each one is an authored flight rather than a graded seam.
The three points are then three different problems: the sump is held from above, the banks from
below.
"""

import json, os, sys

SLUG = "opus5-ochrepans"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "sculpt"))
import props

CELL = 4
FLAT = 22            # the salt flat: the board's own surface
PAN = 21             # a pan floor, one block down, so its rim is a bench and not a wall
YARD = 18            # the sunk evaporation yard at the centre
BANK = 26            # the raised pan banks out on the flanks
STEAD = 23           # the works stead, where a team enters
WALL_TOP = 25        # the yard wall: three courses proud of the flat, seven above the yard


# ── the plan: one works and two steads, and everything else authored downstream ──────────────
def plan():
    return {
        "plan": 2,
        "meta": {"name": "Ochrepans"},
        "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 16,
                    "surface": FLAT, "observerY": 62},
        "pieces": [
            # The works: two rectangles and nothing more, because a capture board's shape is its
            # pans and its walls, and a plan cut into a piece per pan is a plan whose paint
            # follows the cutting. It is two rather than one only because LN2 measures a piece's
            # longest side and bands it at 110 blocks; 152 in one run is a lane with no junction.
            #                              blocks x -52..52, z -76..-28 (and its image, 28..76)
            {"id": "works-n", "role": "piece", "rect": [-13, -19, 26, 12], "surface": FLAT},
            # the middle, which is its own image        blocks x -52..52, z -28..28
            {"id": "works-mid", "role": "piece", "rect": [-13, -7, 26, 14], "surface": FLAT},
            # the stead behind it. 28 x 20 blocks, inside ST10's 30 x 20.
            #                                              blocks x -16..12, z -96..-76
            {"id": "stead", "role": "spawn", "rect": [-4, -24, 7, 5], "surface": STEAD},
        ],
        "placements": {
            # stead's corner is (-16, -96): the point is (-2, -86) and the room x -10..6
            "spawns": [{"id": "spawn-1", "piece": "stead", "at": [14, 10], "facing": "back",
                        "footprint": [6, 3, 16, 14]}],
            "iron": [{"id": "iron-1", "piece": "stead", "at": [3, 10]},
                     {"id": "iron-2", "piece": "stead", "at": [25, 10]}],
            "wools": [], "destroyables": [], "cores": [],
        },
    }


# ── what it is made of ───────────────────────────────────────────────────────────────────────
# Three tone families, named before anything is painted:
#   ground  yellow ochre -- sand, sandstone and yellow stained clay, the highest-value of the run
#   crust   the salt itself: white and light grey clay, and it appears inside a pan and nowhere
#           else, which is what the one-block rim is for
#   built   sandstone ashlar, chiselled and smooth, on the walls and the yard flags
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
    """One stack finishing the flat, the bank's shoulder and the yard's cut face. A thickness on
    the slope axis is a span of degrees, and on a board this flat it is the only axis on which
    the little relief there is can be told from the rest."""
    return {"kind": "layered", "axis": "slope",
            "stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]}}


SAND = solid(12)
SANDSTONE = solid(24)
SMOOTH = solid(24, 2)
CHIS = solid(24, 1)
CLAY_YELLOW = solid(159, 4)
CLAY_WHITE = solid(159, 0)
CLAY_SILVER = solid(159, 8)
CLAY_ORANGE = solid(159, 1)
HARDCLAY = solid(172)
COARSE = solid(3, 1)
DIRT = solid(3)
GRAVEL = solid(13)
STONE = solid(1)
COBBLE = solid(4)
ANDESITE = solid(1, 5)
ACACIA = solid(5, 4)
ACACIA_LOG = solid(162)
BRICK = solid(45)

FLAT_TOP = cell(21, 11, SAND, CLAY_YELLOW, SAND, HARDCLAY)
SHOULDER_TOP = cell(23, 8, CLAY_YELLOW, COARSE, SAND, CLAY_ORANGE)


def ochre_theme():
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void",
        # the pan rims and the yard's cut face are the only risers on this board, and they are
        # exactly what wants a course on it
        "wallOnTerrainFaces": True,
        "rim": {"material": CHIS, "depth": 1, "enabled": True},
        "surface": {"depth": 4, "enabled": True, "material": by_slope(
            (depth_stack((FLAT_TOP, 1), (HARDCLAY, 2), (SANDSTONE, 1)), 10),
            (depth_stack((SHOULDER_TOP, 1), (SAND, 1), (SANDSTONE, 2)), 18),
            (depth_stack((SANDSTONE, 2), (CLAY_ORANGE, 1), (SANDSTONE, 1)), 62))},
        "wall": {"kind": "wallRun", "runs": [
            {"material": SANDSTONE, "width": 2},
            {"material": CLAY_YELLOW, "width": 1},
            {"material": SANDSTONE, "width": 2},
            {"material": CHIS, "width": 1}]},
        "wallEnabled": True,
        "fill": {"kind": "voronoi", "seed": 17, "cellSize": 15, "rise": 7, "bands": [
            {"material": SANDSTONE, "depth": 2}, {"material": SMOOTH, "depth": 1}]},
    }


def crust_theme():
    """What is left in a pan when the brine has gone. The palest ground in the run, and it lies
    only inside a pan -- so every edge of it stands at the foot of a one-block bench rather than
    running across the flat, which is the whole reason the pans are cut at all."""
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void",
        "wallOnTerrainFaces": False,
        "rim": {"material": CLAY_YELLOW, "depth": 1, "enabled": True},
        "surface": {"depth": 3, "enabled": True, "material": depth_stack(
            (cell(29, 6, CLAY_WHITE, CLAY_SILVER, SAND, CLAY_WHITE), 1),
            (SAND, 1), (SANDSTONE, 1))},
        "wall": {"kind": "wallRun", "runs": [
            {"material": CLAY_YELLOW, "width": 1}, {"material": SANDSTONE, "width": 2}]},
        "wallEnabled": True,
        "fill": {"kind": "voronoi", "seed": 19, "cellSize": 12, "rise": 6, "bands": [
            {"material": SANDSTONE, "depth": 2}, {"material": SMOOTH, "depth": 1}]},
    }


def works_theme():
    """The walls, the gates and the yard flags: sandstone ashlar. It is the flat's own rock,
    dressed -- so the built family is a shade off the ground rather than against it, and what
    separates them is the course it stands proud by."""
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop",
        "wallOnTerrainFaces": True,
        "rim": {"material": CHIS, "depth": 1, "enabled": True},
        "surface": {"depth": 2, "enabled": True, "material": depth_stack(
            (cell(31, 5, SMOOTH, SANDSTONE, CHIS, SMOOTH), 1), (SANDSTONE, 1))},
        "wall": {"kind": "wallRun", "runs": [
            {"material": SMOOTH, "width": 3},
            {"material": CHIS, "width": 1},
            {"material": SANDSTONE, "width": 2}]},
        "wallEnabled": True,
        "fill": solid(24, 2),
    }


# ── the works, as a grid ─────────────────────────────────────────────────────────────────────
# The pans, stated in the stated half alone: the expander mirrors every mark, so eight drawn here
# are sixteen on the board. Two rows of four, twenty by fourteen blocks each, on six-block banks.
PAN_COLUMNS = [(-48, -30), (-24, -4), (2, 22), (28, 46)]
PAN_ROWS = [(-62, -50), (-46, -36)]


def marks():
    """In solve order: the flat is the base, the pans are cut into it, the bank is raised off it
    and the yard sunk through it last, because the yard is the thing nothing else may overwrite."""
    out = []
    for at, (x0, x1) in enumerate(PAN_COLUMNS):
        for row, (z0, z1) in enumerate(PAN_ROWS):
            out.append({"id": f"pan-{at}-{row}", "kind": "area", "h": PAN, "bevel": 1,
                        "ring": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]})
    # The west pan bank, drawn wholly in the stated half. The relief is solved for z <= 0 and
    # rotated onto the rest, so a mark centred on the centre line is built on one side of it and
    # not the other: a ring from z -19 to 19 gave a bank from z -19 to -1 and a seven-block fall
    # at z 0, which `transect x=-45` read as `DROP -7 at (-45, 0)` and the pad sitting on the seam
    # answered as `ground 61 degrees from level`. Off the centre line, its own image is the east
    # bank and the two stand diagonally opposite -- which is what gives each team a near pad.
    out.append({"id": "bank-w", "kind": "area", "h": BANK, "bevel": 3,
                "ring": [[-52, -30], [-42, -32], [-32, -29], [-30, -18],
                         [-32, -8], [-42, -6], [-52, -8]]})
    # The evaporation yard, sunk. Its ring is its own mirror, so it is drawn once and stays one.
    out.append({"id": "yard", "kind": "area", "h": YARD, "bevel": 1,
                "ring": [[-22, -22], [0, -23], [22, -22], [23, 0],
                         [22, 22], [0, 23], [-22, 22], [-23, 0]]})
    return out


def pushes():
    """Heaps of harvested salt, raked up off the flat between the pans. Low, because a capture
    board whose middle is a wall does not want a hill beside it as well."""
    return [
        {"id": "heap-w", "ring": [[-30, -78], [-20, -76], [-16, -70], [-24, -66], [-32, -70]],
         "amount": 2.2, "falloff": 10, "crown": 1.0, "roughness": 1.3, "seed": 4},
        {"id": "heap-e", "ring": [[24, -80], [36, -78], [38, -70], [28, -66], [20, -72]],
         "amount": 1.8, "falloff": 9, "crown": 0.8, "roughness": 1.1, "seed": 11},
        {"id": "heap-mid", "ring": [[-8, -54], [6, -52], [10, -44], [-2, -40], [-12, -46]],
         "amount": 1.6, "falloff": 11, "crown": 0.7, "roughness": 1.0, "seed": 21},
    ]


def shapes():
    """The wall, its four gates and the ramps onto the banks. Every one of them is out of the
    relief's solve, so each arrives at the height it was drawn at rather than at the height the
    ground around it happened to reach."""
    out = []

    ashlar = {"kind": "layered", "axis": "depth", "stack": {
        "ending": "repeat", "bands": [
            {"material": CHIS, "thickness": 1},
            {"material": SMOOTH, "thickness": 2},
            {"material": SANDSTONE, "thickness": 4}]}}

    # The yard wall, four runs, every one of them drawn in the stated half: the north wall either
    # side of its gate, and both side walls from the north corner down to the gate gap. Their
    # rot_180 images are the south wall and the far halves of the two side walls, so each side is
    # walled from z -26 to 26 with a sixteen-block gate gap across the centre.
    wall_runs = [
        ("wall-n-w", [[-26, -26], [-18, -26], [-10, -26], [-6, -26]]),
        ("wall-n-e", [[6, -26], [10, -26], [18, -26], [26, -26]]),
        ("wall-w", [[-26, -26], [-26, -21], [-26, -15], [-26, -9]]),
        ("wall-e", [[26, -26], [26, -21], [26, -15], [26, -9]]),
    ]
    for name, points in wall_runs:
        out.append({"id": name, "type": "polyline", "operation": "add",
                    "radius": 1.5, "stroke_edge": "solid", "base_height": WALL_TOP,
                    "relief_scope": "exclude", "keepClear": True,
                    "vertices": points, "material": ashlar})

    # The gates: a flight through each gap, from the flat down onto the yard floor. Twelve blocks
    # of run against four of rise, a material rather than a theme, and sheer-sided because a gate
    # graded into its wall is a ramp with a wall beside it and not a gate.
    flagging = {"kind": "cell", "seed": 37, "cellSize": 5, "jitter": 1, "warp": 2,
                "palette": [SMOOTH, CHIS, SMOOTH, SANDSTONE], "rise": 3}
    out.append({"id": "gate-n", "type": "polygon", "operation": "add",
                "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
                "keepClear": True, "floor": 0,
                "vertices": [[-5, -31], [5, -31], [5, -19], [-5, -19]],
                "anchor_heights": [FLAT, FLAT, YARD, YARD], "material": flagging})
    # The two side gates, both drawn in the stated half for the same reason the bank is; their
    # images complete each gate on the far side of the centre line.
    out.append({"id": "gate-w", "type": "polygon", "operation": "add",
                "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
                "keepClear": True, "floor": 0,
                "vertices": [[-31, -8], [-31, 0], [-19, 0], [-19, -8]],
                "anchor_heights": [FLAT, FLAT, YARD, YARD], "material": flagging})
    out.append({"id": "gate-e", "type": "polygon", "operation": "add",
                "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
                "keepClear": True, "floor": 0,
                "vertices": [[19, -8], [19, 0], [31, 0], [31, -8]],
                "anchor_heights": [YARD, YARD, FLAT, FLAT], "material": flagging})

    # The ramps onto the banks. One drawn north of the west bank and one south of it, so each
    # bank ends up with a ramp at either end once the images are in.
    scree = {"kind": "cell", "seed": 39, "cellSize": 6, "jitter": 2, "warp": 3,
             "palette": [COARSE, SAND, CLAY_YELLOW, GRAVEL], "rise": 2}
    out.append({"id": "bank-ramp-n", "type": "polygon", "operation": "add",
                "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
                "keepClear": True, "floor": 0,
                "vertices": [[-46, -36], [-38, -36], [-38, -26], [-46, -26]],
                "anchor_heights": [FLAT, FLAT, BANK, BANK], "material": scree})
    out.append({"id": "bank-ramp-s", "type": "polygon", "operation": "add",
                "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
                "keepClear": True, "floor": 0,
                "vertices": [[-46, -12], [-38, -12], [-38, -2], [-46, -2]],
                "anchor_heights": [BANK, BANK, FLAT, FLAT], "material": scree})

    # Two free-standing pan walls out on the flat, where a sightline from the stead to the yard
    # would otherwise run the length of the board. They are the same wall as the yard's and stand
    # on the same ground, which is what keeps them from reading as ornament.
    for name, points in (("brake-w", [[-34, -34], [-28, -32], [-22, -34]]),
                         ("brake-e", [[22, -34], [28, -32], [34, -34]])):
        out.append({"id": name, "type": "polyline", "operation": "add",
                    "radius": 1.5, "stroke_edge": "solid", "base_height": WALL_TOP,
                    "relief_scope": "exclude", "keepClear": True,
                    "vertices": points, "material": ashlar})

    # The crust in each pan: a brush states a height_mode or it is never a candidate for the paint
    # at all, and a raise of zero sits flush on ground a mark already pinned level. The ring is
    # inset a block from the pan's own, so the rim keeps the flat's ochre and the change of
    # material stands at the foot of the bench rather than on top of it.
    for at, (x0, x1) in enumerate(PAN_COLUMNS):
        for row, (z0, z1) in enumerate(PAN_ROWS):
            out.append({"id": f"crust-{at}-{row}", "type": "polygon", "operation": "add",
                        "height_mode": "raise", "base_height": 0, "skirt": 0,
                        "theme": "crust",
                        "vertices": [[x0 + 1, z0 + 1], [x1 - 1, z0 + 1],
                                     [x1 - 1, z1 - 1], [x0 + 1, z1 - 1]]})

    # The yard's own floor, flagged: the middle pad stands on it and it is the one ground on this
    # board that is entirely somebody's work.
    out.append({"id": "yard-floor", "type": "polygon", "operation": "add",
                "height_mode": "raise", "base_height": 0, "skirt": 0, "theme": "works",
                "vertices": [[-20, -20], [0, -21], [20, -20], [21, 0],
                             [20, 20], [0, 21], [-20, 20], [-21, 0]]})
    return out


def cisterns():
    """Four brine cisterns on the flat between the yard and the banks, stone-lined and three
    courses proud. They are stated as two rot_180 pairs rather than mirrored, because a made
    layer carries its own group and the expander is not asked to fan it."""
    made = []
    lining = {"kind": "cell", "seed": 57, "cellSize": 4, "jitter": 1, "warp": 2,
              "palette": [SMOOTH, SANDSTONE, CHIS, SANDSTONE], "rise": 3}
    brine = {"kind": "cell", "seed": 59, "cellSize": 3, "jitter": 1, "warp": 1,
             "palette": [CLAY_SILVER, CLAY_WHITE, CLAY_SILVER, SMOOTH], "rise": 2}
    for at, (cx, cz) in enumerate([(-14, -32), (14, 32)]):
        layer = props.ring_wall(f"cistern-{at}", cx, cz, outer=5, thickness=1, floor=FLAT,
                                height=3, theme=None, inner_floor=None,
                                name=f"Cistern {at}", mirrors=False)
        inner = layer.pop("layout")
        layer["shapes"] = inner["shapes"]
        layer["groups"] = inner["groups"]
        layer["kind"] = "made"
        layer["part_of"] = "saltworks"
        for shape in layer["shapes"]:
            shape.pop("theme", None)
            shape["material"] = lining
        layer["shapes"].append({"id": f"cistern-{at}-brine", "type": "circle",
                                "operation": "add", "center_x": cx, "center_z": cz,
                                "radius": 3.5, "floor": FLAT, "base_height": 1,
                                "keepClear": True, "override": True, "material": brine})
        layer["groups"][0]["shapeIds"].append(f"cistern-{at}-brine")
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


def salt_house():
    """The spawn hall: sandstone to the sill and acacia above it, acacia posts at the corners and
    a beam course of laid log where the storey changes -- a beam has to be the end of something.
    No footing: over a plate one course deep it is a rim round a building with no foundation. The
    roof slab is the roof body's own material (HS3) and the door head's stair and its fill are
    one material (HS4)."""
    return {
        "foundation": {"plate": band((SMOOTH, 1)), "surface": PLAIN_SURFACE, "footing": None},
        "roof": {"form": "hip", "pitch": 1, "slab": 44, "slabData": 1, "overhang": 1,
                 "ridgeCap": True, "hole": False,
                 "body": SANDSTONE, "verge": {"kind": "laidLog", "id": 162, "data": 0},
                 "gable": ACACIA,
                 "gableWindows": window("pane", 102, width=1, height=2, sill=1, spacing=3)},
        "wall": band((SANDSTONE, 4), (ACACIA, 4)),
        "post": ACACIA_LOG,
        "windows": window("pane", 102, width=2, height=2, sill=3, spacing=4),
        "storeys": [
            {"clear": 5, "wall": band((SANDSTONE, 2), (ACACIA, 4)), "post": ACACIA_LOG,
             "windows": window("pane", 102, width=2, height=2, sill=3, spacing=4),
             "surface": PLAIN_SURFACE, "deck": None, "headroom": 5},
        ],
        "porch": None, "front": None,
        "beams": {"block": 162, "data": 0, "reach": 1, "any": False},
        "doorway": {"door": "air", "width": 2, "height": 3,
                    "head": {"form": "arched", "block": 128, "fill": "upperSlab",
                             "fillBlock": 44, "fillData": 1}},
    }


def pan_house():
    """The salters' sheds on the flat: one style, and the plots differ in height and footprint and
    in nothing else, which is what makes three buildings a row rather than three ideas."""
    shell = salt_house()
    shell["wall"] = band((SANDSTONE, 2), (ACACIA, 3))
    shell["storeys"] = []
    shell["roof"] = dict(shell["roof"], form="hip", pitch=1, overhang=2, ridgeCap=False)
    shell["windows"] = window("pane", 102, width=2, height=2, sill=2, spacing=3)
    return {"kind": "house", "shell": shell}


def dressing():
    trees = json.load(open(f"{HERE}/trees.json"))
    styles = dict(trees)
    styles["shed"] = pan_house()
    # A boulder is stone: stone, cobblestone and andesite is the whole palette that reads as rock
    # against any ground. On ochre sand a sandstone boulder is a boulder nobody can see.
    styles["rock"] = {"kind": "boulder", "form": "angular", "size": 3.0, "mossy": False,
                      "rock": cell(53, 4, STONE, COBBLE, ANDESITE, STONE)}

    paving = cell(43, 5, COARSE, SAND, CLAY_YELLOW, COARSE)
    props_out = [
        # Out of the stead door, down the middle bank between the pan rows and in at the north
        # gate. Three blocks a reader cannot quite tell apart, solid, because a worn band reads
        # as litter and a path is a claim about where people walk.
        {"id": "track-out", "kind": "stroke", "seed": 41, "radius": 2, "style": "solid",
         "coverage": 1.0, "claimsGround": True, "pave": paving,
         "points": [[-2, -76], [-2, -70], [-2, -66], [-2, -63]]},
        {"id": "track-gate", "kind": "stroke", "seed": 42, "radius": 2, "style": "solid",
         "coverage": 1.0, "claimsGround": True, "pave": paving,
         "points": [[-2, -63], [-1, -54], [0, -44], [0, -33]]},
    ]

    # Three sheds on the flat behind the pans, differing in height and footprint and nothing else.
    for at, (x0, z0, tall) in enumerate([(-50, -76, 0), (-32, -76, 1),
                                         (18, -76, 0), (36, -76, 1)]):
        props_out.append({"id": f"shed-{at}", "kind": "house", "seed": 501 + at,
                          "front": "posZ", "style": "shed",
                          "wings": [{"corners": [[x0, z0], [x0 + 11, z0 + 8]],
                                     "spec": {"storeysHigh": tall, "ridge": "alongX"}}]})

    # Boulders on the banks between the pans, where the works has not been swept.
    # All six on the one wide bank the pan rows leave between them, ten blocks apart and off
    # the road: two props inside one claim is two props the dressing pass declines.
    for at, (bx, bz) in enumerate([(-22, -48), (-8, -48), (10, -48),
                                   (24, -48), (0, -20), (14, -14)]):
        props_out.append({"id": f"rock-{at}", "kind": "boulder", "seed": 610 + at,
                          "x": bx, "z": bz, "style": "rock"})

    # Thorn at the works' edges only. A salt-works is scraped ground and carries nothing in the
    # middle of it, which is also what keeps the sightlines the walls break from growing back.
    plant = [("thorn-1", -51, -56), ("thorn-2", 51, -56),
             ("spar-1", -51, -42), ("spar-2", 51, -42)]
    for at, (style, tx, tz) in enumerate(plant):
        props_out.append({"id": f"thorn-{at}", "kind": "tree", "seed": 700 + at,
                          "x": tx, "z": tz, "style": style})

    # Ground cover, thinner than any other board in the run, because scraped ground is scraped.
    props_out.append({"id": "cover", "kind": "flora", "seed": 800,
                      "points": [[-58, -102], [58, -102], [58, 14], [-58, 14]],
                      "spec": {"coverage": 0.08, "scale": 26, "octaves": 3, "fernShare": 0.04,
                               "flowerShare": 0.03, "flowerScale": 14, "tallShare": 0.02}})
    return {"styles": styles, "props": props_out}


def finish():
    return {
        "authors": [{"name": "Opus 5"}],
        "created": "2026-09-14",
        # Savanna Plateau: a dry tint over ochre ground, and the one colour on this board a block
        # does not state for itself.
        "biome": {"kind": "solid", "id": 36},
        "themes": {"ochre": ochre_theme(), "crust": crust_theme(), "works": works_theme()},
        "mapTheme": "ochre",
        # the board's outer edge, drawn as an edge rather than as the rectangle the plan compiled
        # to. The pans and the yard keep their drawn corners, because they are cut and not coastal.
        # the compiled ground is one component named for its first piece and the surface it
        # stands at, which on this board is `stead`
        "bendShapes": {"stead-22": {"k": 0.14, "wander": 3, "step": 13, "seed": 5}},
        "relief": {"*": {"base": FLAT, "reach": 0, "step": 1, "landform": "plain",
                         "grain": {"amplitude": 0.8, "scale": 17, "seed": 7},
                         "marks": marks(), "pushes": pushes()}},
        "addShapes": shapes(),
        "addLayers": cisterns(),
        "roomStyles": {"spawn": salt_house()},
        "dressing": dressing(),
        # Three pads, every one of them stated: a compiled intent carries no symmetry and nothing
        # downstream fans a control point.
        "controlPoints": [
            {"name": "The Sump", "anchor": {"x": 0, "y": 0, "z": 0}, "size": 8, "points": 1},
            {"name": "West Pan", "anchor": {"x": -41, "y": 0, "z": -19}, "size": 8, "points": 1},
            {"name": "East Pan", "anchor": {"x": 41, "y": 0, "z": 19}, "size": 8, "points": 1},
        ],
        "scoreLimit": 750,
    }


if __name__ == "__main__":
    with open(f"{HERE}/{SLUG}.plan.json", "w") as handle:
        json.dump(plan(), handle, indent=2)
    with open(f"{HERE}/{SLUG}.finish.json", "w") as handle:
        json.dump(finish(), handle, indent=2)
    print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")
