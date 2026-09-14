"""Redmarl — a CTW board cut into a red marl gully.

Each team's dyehouses stand on its own bank above a dry red watercourse. The wool is fetched out of
the enemy's dyehouse, carried down into the gully and back up onto your own bank to a plinth at your
back, so every carry crosses the one piece of ground both teams can reach.

Four grounds meet on it and each is stated by the one instrument that can state it:

  the marl bank      an area mark at 26 with two dunes pushed up behind the dyehouses
  the apron          an area mark at 23, with one low swell so the open ground is not a table
  the brink          an area mark at 21 held to its edge, so the gully is a face and not a grade
  the gully floor    an area mark at 17 whose ring wanders eight blocks either side of the plan's
                     straight z, which is what stops the frontline reading as a ruled line

and the watercourse itself is a line mark with a narrow tread, so the band either side of it lofts
back to the floor rather than walling itself.

Three descents a team, and every one of them is authored rather than graded: a built washing stair
at the centre between two revetments, and a slumped marl slip on the west flank. Under rot_180 a
team's slip is on the flank opposite its enemy's, so the gully is crossed on the diagonal.

The pale built family — smooth sandstone, stone brick — appears only where somebody built it, and
every place it meets the marl it meets it over a face: the dye yards stand a course proud of the
bank, the revetments are walls, and the gully's own theme change follows the channel's break of
slope. Nothing pale is laid flush on red ground.
"""

import json, os, sys

SLUG = "opus5-redmarl"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "sculpt"))
import props

CELL = 4
BANK = 26            # the marl bank the dyehouses and the spawn stand on
YARD = 27            # the built yards under them, one course proud of the bank
APRON = 23           # the open ground the tracks cross
BRINK = 21           # the lip above the gully
FLOOR = 17           # the gully floor
CHANNEL = 14.5       # the dry watercourse cut into it


# ── the plan: the arrangement, and nothing else ──────────────────────────────────────────────
def plan():
    return {
        "plan": 2,
        "meta": {"name": "Redmarl"},
        "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 20,
                    "surface": APRON, "observerY": 60},
        "pieces": [
            # the bank                                            blocks x -64..64, z -96..-72
            {"id": "bank",   "role": "piece",     "rect": [-16, -24, 32, 6], "surface": BANK},
            # the two dyehouses on it. 20 x 16 blocks each: a protection region is at most
            # 20 x 30 (ST10) and the piece is what the protection is cut from.
            {"id": "dye-w",  "role": "wool-room", "rect": [-15, -23,  5, 4], "surface": BANK},
            {"id": "dye-e",  "role": "wool-room", "rect": [ 10, -23,  5, 4], "surface": BANK},
            # the spawn, between them, so both dyehouses are on somebody's journey out of the door
            {"id": "yard",   "role": "spawn",     "rect": [ -3, -23,  6, 4], "surface": BANK},
            # the apron                                           blocks x -64..64, z -72..-48
            {"id": "apron",  "role": "piece",     "rect": [-16, -18, 32, 6], "surface": APRON},
            # the brink                                           blocks x -64..64, z -48..-28
            {"id": "brink",  "role": "piece",     "rect": [-16, -12, 32, 5], "surface": BRINK},
            # the gully floor, the one piece both teams stand on  blocks x -64..64, z -28..28
            {"id": "strand", "role": "piece",     "rect": [-16,  -7, 32, 14], "surface": FLOOR},
        ],
        # the gully is the build zone: there is ground under all of it, so nothing has to be
        # bridged -- what is built there is cover, and a fourth way up somebody makes
        "zones": [{"id": "gully", "rect": [-16, -7, 32, 14], "kind": "build"}],
        "placements": {
            # yard's minimum corner is (-12, -92), so the point is (0, -87) and the room
            # x -8..8, z -89..-79: a 20 x 14 protection, inside ST10's 20 x 30
            "spawns": [{"id": "spawn-1", "piece": "yard", "at": [12, 5], "facing": "back",
                        "footprint": [4, 3, 16, 10]}],
            "iron": [{"id": "iron-1", "piece": "yard", "at": [4, 8]},
                     {"id": "iron-2", "piece": "yard", "at": [20, 8]}],
            # dye-w's corner is (-60, -92) and dye-e's is (40, -92)
            "wools": [{"id": "wool-1", "piece": "dye-w", "at": [10, 8],
                       "footprint": [2, 2, 16, 12]},
                      {"id": "wool-2", "piece": "dye-e", "at": [10, 8],
                       "footprint": [2, 2, 16, 12]}],
            "destroyables": [],
            "cores": [],
        },
    }


# ── what it is made of ───────────────────────────────────────────────────────────────────────
# Three tone families, named before anything is painted:
#   ground  red sand, hardened clay and red sandstone -- the deepest and most saturated of the run
#   built   smooth sandstone and stone brick, pale, and only where somebody built it
#   accent  the dye itself: red and orange stained clay, inside the vats and nowhere else
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
    """One stack finishing the flat, the shoulder and the cut face of the same marl. A thickness
    on the slope axis is a span of degrees, which is the only axis that tells a bank from a pan."""
    return {"kind": "layered", "axis": "slope",
            "stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]}}


RED_SAND = solid(12, 1)
RED_STONE = solid(179)
RED_SMOOTH = solid(179, 2)
RED_CHIS = solid(179, 1)
HARDCLAY = solid(172)
CLAY_RED = solid(159, 14)
CLAY_ORANGE = solid(159, 1)
CLAY_BROWN = solid(159, 12)
SAND = solid(12)
SANDSTONE = solid(24)
SMOOTH = solid(24, 2)
CHIS = solid(24, 1)
GRAVEL = solid(13)
DIRT = solid(3)
COARSE = solid(3, 1)
STONE = solid(1)
COBBLE = solid(4)
ANDESITE = solid(1, 5)
BRICK_STONE = solid(98)
ACACIA = solid(5, 4)
ACACIA_LOG = solid(162)

# The flat is red sand gone over to bare hardened clay in patches, at a brush wide enough to read
# as patches rather than speckle. The shoulder is the clay alone with coarse silt in it. The face
# is bedded red sandstone, which is what the banks of this gully are cut in.
MARL_TOP = cell(21, 12, RED_SAND, HARDCLAY, RED_SAND, CLAY_BROWN)
MARL_SHOULDER = cell(23, 9, HARDCLAY, RED_SAND, COARSE, HARDCLAY)


def marl_theme():
    """The board's own ground. Everything about it is stated on the slope axis, because a board
    finished by height paints the gully and the bank the same colour from above."""
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void",
        # the gully's cut banks get their bedding from the wall bucket; the whole board's red
        # family means a riser the grain throws up reads as more of the same rock
        "wallOnTerrainFaces": True,
        "rim": {"material": RED_SMOOTH, "depth": 1, "enabled": True},
        "surface": {"depth": 4, "enabled": True, "material": by_slope(
            (depth_stack((MARL_TOP, 1), (HARDCLAY, 2), (RED_STONE, 1)), 12),
            (depth_stack((MARL_SHOULDER, 1), (HARDCLAY, 1), (RED_STONE, 2)), 16),
            (depth_stack((RED_STONE, 2), (RED_SMOOTH, 1), (RED_STONE, 1)), 62))},
        # the cut banks: bedding planes, which is the whole reason this board has a gully in it
        "wall": {"kind": "wallRun", "runs": [
            {"material": RED_STONE, "width": 3},
            {"material": RED_SMOOTH, "width": 1},
            {"material": RED_STONE, "width": 2},
            {"material": RED_CHIS, "width": 1}]},
        "wallEnabled": True,
        "fill": {"kind": "voronoi", "seed": 17, "cellSize": 15, "rise": 7, "bands": [
            {"material": RED_SMOOTH, "depth": 2}, {"material": RED_STONE, "depth": 1}]},
    }


def wash_theme():
    """What the water left in the bed: paler than the marl, and stated only on the channel's own
    pans, so every edge of it lies on a break of slope rather than across flat ground."""
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void",
        "wallOnTerrainFaces": False,
        "rim": {"material": SANDSTONE, "depth": 1, "enabled": True},
        "surface": {"depth": 3, "enabled": True, "material": depth_stack(
            (cell(29, 8, SAND, GRAVEL, RED_SAND, COARSE), 1), (SAND, 1), (SANDSTONE, 1))},
        "wall": {"kind": "wallRun", "runs": [
            {"material": SANDSTONE, "width": 2}, {"material": RED_STONE, "width": 1}]},
        "wallEnabled": True,
        "fill": {"kind": "voronoi", "seed": 19, "cellSize": 13, "rise": 6, "bands": [
            {"material": RED_STONE, "depth": 2}, {"material": SANDSTONE, "depth": 1}]},
    }


def works_theme():
    """The dyers' own ground: smooth sandstone flags with stone brick in them. Pale, and out of
    the marl's family on purpose -- so it stands a course proud of the bank wherever it is laid,
    and every edge of it is a built riser rather than a change of colour on flat ground."""
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop",
        "wallOnTerrainFaces": True,
        "rim": {"material": CHIS, "depth": 1, "enabled": True},
        "surface": {"depth": 2, "enabled": True, "material": depth_stack(
            (cell(31, 6, SMOOTH, BRICK_STONE, SMOOTH, SANDSTONE), 1), (SANDSTONE, 1))},
        "wall": {"kind": "wallRun", "runs": [
            {"material": SANDSTONE, "width": 2},
            {"material": CHIS, "width": 1},
            {"material": SMOOTH, "width": 2}]},
        "wallEnabled": True,
        "fill": solid(24, 2),
    }


# ── the ground, as four things that meet ─────────────────────────────────────────────────────
def marks():
    """In solve order: a later mark wins a contested cell, so the three terraces are stated from
    the back forward and the gully last, cutting its own edge through the brink."""
    return [
        {"id": "bank-pan", "kind": "area", "h": BANK, "bevel": 4,
         "ring": [[-63, -99], [-34, -97], [-4, -99], [28, -96], [62, -98],
                  [61, -74], [30, -71], [0, -73], [-30, -70], [-62, -73]]},
        {"id": "apron-pan", "kind": "area", "h": APRON, "bevel": 4,
         "ring": [[-63, -73], [-30, -70], [2, -72], [34, -69], [62, -72],
                  [61, -49], [28, -47], [-2, -50], [-32, -47], [-62, -50]]},
        # held to its edge -- a small bevel is what makes the lip a lip
        {"id": "brink-pan", "kind": "area", "h": BRINK, "bevel": 2,
         "ring": [[-63, -50], [-30, -47], [2, -50], [34, -47], [62, -50],
                  [62, -30], [30, -27], [0, -31], [-30, -28], [-62, -31]]},
        # the gully. Its north edge wanders eight blocks either side of the plan's z = -28, which
        # is what keeps the frontline off a ruled line; the ring reaches past the centre so its
        # own mirror overlaps it and the floor is continuous across z = 0.
        {"id": "gully-pan", "kind": "area", "h": FLOOR, "bevel": 1,
         "ring": [[-64, -30], [-48, -25], [-34, -31], [-18, -24], [-2, -30],
                  [14, -23], [30, -29], [46, -23], [64, -27],
                  [64, 6], [40, 4], [16, 8], [-10, 3], [-36, 7], [-64, 2]]},
        # the watercourse. A narrow tread and the rest of the band lofts, so it is a channel cut
        # in the floor rather than a trench with a wall down both sides. Its own mirror comes up
        # the other arm of the S and the two nearly meet at the centre, leaving a bar between.
        {"id": "channel", "kind": "line", "h": CHANNEL, "r": 7, "tread": 2,
         "points": [[-66, -18], [-46, -10], [-26, -16], [-6, -6], [-1, -2]]},
        # a side braid joining it off the west slip's foot
        {"id": "braid", "kind": "line", "h": 15.5, "r": 4, "tread": 1,
         "points": [[-54, -26], [-46, -18], [-38, -11]]},
    ]


def pushes():
    """Added to the solved surface after the marks, so each is kept off ground a mark had to
    arrive at: the yards, the stair's head and foot, and the lip."""
    return [
        {"id": "dune-w", "ring": [[-62, -97], [-48, -95], [-42, -86], [-50, -76], [-62, -80]],
         "amount": 3.2, "falloff": 11, "crown": 2.5, "roughness": 1.6, "seed": 4},
        {"id": "dune-e", "ring": [[44, -98], [60, -96], [62, -84], [52, -76], [42, -85]],
         "amount": 2.4, "falloff": 10, "crown": 2.0, "roughness": 1.3, "seed": 11},
        {"id": "swell", "ring": [[8, -70], [34, -67], [42, -57], [20, -52], [4, -60]],
         "amount": 1.8, "falloff": 13, "crown": 1.5, "roughness": 1.0, "seed": 21},
        # a bar in the bed: cover on the one piece of ground both teams fight over
        {"id": "bar", "ring": [[-14, -17], [6, -15], [10, -6], [-8, -4], [-18, -10]],
         "amount": 1.7, "falloff": 8, "crown": 1.2, "roughness": 0.9, "seed": 31},
    ]


def shapes():
    """What the plan cannot state: the yards the buildings stand on, the three descents into the
    gully, the revetments holding the stair, and the pans the channel left."""
    out = []

    # The three yards. relief_scope exclude takes each footprint out of the solve, and a course
    # above the bank makes the meeting a riser rather than a change of colour on flat ground.
    for name, ring in (
            ("yard-dye-w", [[-63, -94], [-52, -96], [-39, -94], [-36, -84],
                            [-38, -74], [-52, -71], [-63, -75]]),
            ("yard-dye-e", [[37, -94], [50, -96], [63, -94], [62, -75],
                            [50, -71], [37, -74], [35, -84]]),
            ("yard-spawn", [[-15, -93], [0, -95], [15, -93], [16, -80],
                            [1, -76], [-14, -78], [-16, -84]])):
        out.append({"id": name, "type": "polygon", "operation": "add",
                    "base_height": YARD, "relief_scope": "exclude", "keepClear": True,
                    "theme": "works", "vertices": ring})

    # The washing stair: level, sheer-sided, out of the relief's solve so it arrives where it was
    # told. Fourteen blocks of run against four of rise, and a material rather than a theme --
    # a stair is a thing somebody built and a theme is a place.
    out.append({"id": "wash-stair", "type": "polygon", "operation": "add",
                "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
                "keepClear": True, "floor": 0,
                "vertices": [[-9, -32], [9, -32], [9, -18], [-9, -18]],
                "anchor_heights": [BRINK, BRINK, FLOOR, FLOOR],
                "material": {"kind": "cell", "seed": 37, "cellSize": 6, "jitter": 1, "warp": 2,
                             "palette": [SMOOTH, BRICK_STONE, SMOOTH, SANDSTONE], "rise": 3}})

    # The revetments either side of it. Out of the solve, so they hold the height they were drawn
    # at while the ground falls away under them: a course proud at the head, four at the foot.
    for side, xs in (("w", -11), ("e", 10)):
        out.append({"id": f"revet-{side}", "type": "polyline", "operation": "add",
                    "radius": 1, "stroke_edge": "solid", "base_height": BRINK + 1,
                    "relief_scope": "exclude", "keepClear": True,
                    "vertices": [[xs, -34], [xs, -29], [xs, -23], [xs, -17]],
                    "material": {"kind": "layered", "axis": "depth", "stack": {
                        "ending": "repeat", "bands": [
                            {"material": CHIS, "thickness": 1},
                            {"material": SANDSTONE, "thickness": 4}]}}})

    # The west slip: the bank slumped into the gully. Same arithmetic as the stair and the
    # opposite material -- red scree, so it reads as ground giving way rather than as masonry.
    # Under rot_180 a team's own slip is on the flank opposite its enemy's.
    out.append({"id": "slip-w", "type": "polygon", "operation": "add",
                "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
                "keepClear": True, "floor": 0,
                "vertices": [[-57, -35], [-40, -32], [-38, -15], [-55, -17]],
                "anchor_heights": [BRINK, BRINK, FLOOR, FLOOR],
                "material": {"kind": "cell", "seed": 39, "cellSize": 7, "jitter": 2, "warp": 3,
                             "palette": [RED_SAND, HARDCLAY, COARSE, RED_STONE], "rise": 2}})

    # A bench jutting over the gully on the east flank: brink height, out of the solve, so its
    # three open sides are faces. Somewhere to shoot the floor from, and no way down off it.
    out.append({"id": "bench-e", "type": "polygon", "operation": "add",
                "base_height": BRINK, "relief_scope": "exclude", "keepClear": False,
                "vertices": [[38, -33], [56, -31], [58, -21], [40, -23]]})

    # The pads the vats stand on, so the made layer over them lands on ground of a known height.
    for name, ring in (("pad-w", [[-42, -68], [-27, -70], [-24, -58], [-38, -55], [-44, -61]]),
                       ("pad-e", [[24, -66], [39, -68], [44, -60], [34, -53], [22, -57]])):
        out.append({"id": name, "type": "polygon", "operation": "add",
                    "base_height": APRON, "relief_scope": "exclude", "keepClear": True,
                    "theme": "works", "vertices": ring})

    # Where the channel widens, the ground the water left. A brush states a height_mode or it is
    # never a candidate for the paint at all; a raise of zero sits flush and changes no height.
    for name, ring in (("wash-w", [[-58, -22], [-44, -16], [-36, -9],
                                   [-44, -5], [-58, -11], [-63, -17]]),
                       ("wash-mid", [[-30, -20], [-16, -14], [-10, -6],
                                     [-20, -2], [-32, -8], [-35, -15]]),
                       ("wash-bar", [[-6, -11], [6, -9], [9, -2],
                                     [-2, 1], [-10, -4]])):
        out.append({"id": name, "type": "polygon", "operation": "add",
                    "height_mode": "raise", "base_height": 0, "skirt": 0,
                    "vertices": ring, "theme": "wash"})
    return out


def vats():
    """The dye vats: two stone-lined rings on each apron pad, one holding red liquor and one
    orange -- the two colours the dyehouses behind them send out. They stand where the sightline
    across the apron wants breaking, and they are the only stained clay on the board."""
    made = []
    plan_vats = [("vat-w", -33, -62, CLAY_RED), ("vat-e", 33, -60, CLAY_ORANGE)]
    lining = {"kind": "cell", "seed": 57, "cellSize": 4, "jitter": 1, "warp": 2,
              "palette": [BRICK_STONE, SANDSTONE, BRICK_STONE, COBBLE], "rise": 0}
    for name, cx, cz, liquor in plan_vats:
        layer = props.ring_wall(name, cx, cz, outer=6, thickness=1, floor=APRON, height=3,
                                theme=None, inner_floor=None, name=f"Vat {name[-1]}",
                                mirrors=False)
        inner = layer.pop("layout")
        layer["shapes"] = inner["shapes"]
        layer["groups"] = inner["groups"]
        layer["kind"] = "made"
        layer["part_of"] = "dyeworks"
        for shape in layer["shapes"]:
            shape.pop("theme", None)
            shape["material"] = lining
        # the liquor itself: one course inside the ring, laid over the wall's own floor
        layer["shapes"].append({"id": f"{name}-liquor", "type": "circle", "operation": "add",
                                "center_x": cx, "center_z": cz, "radius": 4.5,
                                "floor": APRON, "base_height": 1, "keepClear": True,
                                "override": True, "material": liquor})
        layer["groups"][0]["shapeIds"].append(f"{name}-liquor")
        made.append(layer)
    return made


# ── what a team walks out of, and what it fetches ────────────────────────────────────────────
def band(*bands):
    return {"stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]},
            "extent": sum(t for _m, t in bands)}

def window(form, block, width=1, height=2, sill=2, spacing=4, data=0):
    return {"form": form, "block": block, "hostBlock": -1, "hostData": 0, "data": data,
            "sill": sill, "width": width, "height": height, "spacing": spacing}

PLAIN_SURFACE = {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                 "inlayInset": 2, "isPlain": True}


def guild_hall():
    """The spawn hall. Hardened clay to the sill and acacia above it, acacia posts at the corners
    and a beam course of laid log where the storey changes -- a beam has to be the end of
    something. No footing: over a plate one course deep it is a rim round a building with no
    foundation. It is of the bank's own family, because a pale hall on red ground with nothing
    under it is the change of material this board is most exposed to."""
    return {
        "foundation": {"plate": band((RED_STONE, 1)), "surface": PLAIN_SURFACE, "footing": None},
        "roof": {"form": "gable", "pitch": 1, "slab": 182, "slabData": 0, "overhang": 1,
                 "ridgeCap": True, "hole": False,
                 "body": HARDCLAY, "verge": {"kind": "laidLog", "id": 162, "data": 0},
                 "gable": ACACIA,
                 "gableWindows": window("pane", 102, width=1, height=2, sill=1, spacing=3)},
        "wall": band((HARDCLAY, 3), (ACACIA, 4)),
        "post": ACACIA_LOG,
        "windows": window("pane", 102, width=2, height=2, sill=3, spacing=4),
        "storeys": [
            {"clear": 5, "wall": band((HARDCLAY, 3), (ACACIA, 3)), "post": ACACIA_LOG,
             "windows": window("pane", 102, width=2, height=2, sill=3, spacing=4),
             "surface": PLAIN_SURFACE, "deck": None, "headroom": 5},
        ],
        "porch": None, "front": None,
        "beams": {"block": 162, "data": 0, "reach": 1, "any": False},
        "doorway": {"door": "air", "width": 2, "height": 3,
                    "head": {"form": "arched", "block": 134, "fill": "upperSlab",
                             "fillBlock": 182, "fillData": 0}},
    }


def dyehouse():
    """The wool room: taller than the hall and lit through stained glass, which is what says from
    the far bank that the thing being fetched is in there. Stone brick to the sill because it
    stands in water, and the same acacia above it as everything else on the bank."""
    shell = guild_hall()
    shell["foundation"] = {"plate": band((BRICK_STONE, 1)), "surface": PLAIN_SURFACE,
                           "footing": None}
    shell["wall"] = band((BRICK_STONE, 4), (ACACIA, 5))
    shell["windows"] = window("pane", 160, width=2, height=3, sill=2, spacing=3, data=1)
    shell["storeys"] = [
        {"clear": 6, "wall": band((BRICK_STONE, 2), (ACACIA, 4)), "post": ACACIA_LOG,
         "windows": window("pane", 160, width=2, height=2, sill=2, spacing=3, data=14),
         "surface": PLAIN_SURFACE, "deck": None, "headroom": 6},
    ]
    shell["roof"] = dict(shell["roof"], form="gable", pitch=1, overhang=2, ridgeCap=True,
                         body=BRICK_STONE, gable=ACACIA)
    return shell


def drying_shed():
    """One style, and the two plots differ in height and footprint and in nothing else, which is
    what makes two buildings a row rather than two ideas."""
    shell = guild_hall()
    shell["wall"] = band((HARDCLAY, 2), (ACACIA, 3))
    shell["storeys"] = []
    shell["roof"] = dict(shell["roof"], form="hip", pitch=1, overhang=1, ridgeCap=False)
    shell["windows"] = window("pane", 102, width=1, height=2, sill=2, spacing=3)
    return {"kind": "house", "shell": shell}


def dressing():
    trees = json.load(open(f"{HERE}/trees.json"))
    styles = dict(trees)
    styles["shed"] = drying_shed()
    # A boulder is stone: stone, cobblestone and andesite is the whole palette that reads as rock
    # against any ground, and on a red board a red boulder is a boulder nobody can see.
    styles["rock"] = {"kind": "boulder", "form": "angular", "size": 3.0, "mossy": False,
                      "rock": cell(53, 4, STONE, COBBLE, ANDESITE, STONE)}

    paving = cell(43, 5, HARDCLAY, COARSE, RED_SAND, HARDCLAY)
    props_out = [
        # Out of the spawn door, across the apron between the vats, and onto the stair's head.
        # Three blocks a reader cannot quite tell apart, solid, because a worn band reads as
        # litter and a path is a claim about where people walk.
        {"id": "track-out", "kind": "stroke", "seed": 41, "radius": 2, "style": "solid",
         "coverage": 1.0, "claimsGround": True, "pave": paving,
         "points": [[0, -76], [-3, -68], [-1, -58], [0, -50]]},
        {"id": "track-stair", "kind": "stroke", "seed": 42, "radius": 2, "style": "solid",
         "coverage": 1.0, "claimsGround": True, "pave": paving,
         "points": [[0, -50], [0, -42], [0, -36], [0, -33]]},
        # and the two haulage tracks to the dyehouses
        {"id": "track-dye-w", "kind": "stroke", "seed": 43, "radius": 2, "style": "solid",
         "coverage": 1.0, "claimsGround": True, "pave": paving,
         "points": [[-14, -80], [-24, -78], [-34, -80], [-40, -78]]},
        {"id": "track-dye-e", "kind": "stroke", "seed": 44, "radius": 2, "style": "solid",
         "coverage": 1.0, "claimsGround": True, "pave": paving,
         "points": [[14, -80], [24, -78], [34, -80], [40, -78]]},
        # the slip's own worn line, down onto the floor
        {"id": "track-slip", "kind": "stroke", "seed": 45, "radius": 2, "style": "solid",
         "coverage": 0.9, "claimsGround": True, "pave": paving,
         "points": [[-48, -44], [-48, -38], [-48, -30], [-47, -20]]},
        # The channel floor: not a path, so not solid -- a scoured bed reads as stones left.
        {"id": "bed", "kind": "stroke", "seed": 47, "radius": 4, "style": "stones",
         "coverage": 0.7, "claimsGround": True,
         "pave": cell(48, 6, GRAVEL, SAND, RED_SAND, COARSE),
         "points": [[-64, -18], [-46, -10], [-26, -16], [-6, -6]]},
    ]

    # Two drying sheds on the apron flanks. They are here because the flanks need a reason to be
    # walked and the sightline across the apron needs breaking, and a track runs to one's door.
    props_out.append({"id": "shed-w", "kind": "house", "seed": 501, "front": "posZ",
                      "style": "shed",
                      "wings": [{"corners": [[-58, -70], [-46, -61]], "spec": {"ridge": "alongX"}}]})
    props_out.append({"id": "shed-e", "kind": "house", "seed": 502, "front": "negZ",
                      "style": "shed",
                      "wings": [{"corners": [[48, -66], [60, -57]],
                                 "spec": {"storeysHigh": 1, "ridge": "alongX"}}]})

    # Boulders, each where the bed dropped it or where the bank has calved.
    for at, (bx, bz) in enumerate([(-30, -14), (-12, -22), (18, -18), (36, -12),
                                   (-52, -8), (24, -40), (-20, -56), (52, -88)]):
        props_out.append({"id": f"rock-{at}", "kind": "boulder", "seed": 610 + at,
                          "x": bx, "z": bz, "style": "rock"})

    # Acacia on the open ground and scrub where the dust is deepest. Every one is off a track and
    # off the yards, and none is on the gully floor, which is a bed and carries nothing tall.
    plant = [("holt-1", -30, -92), ("holt-2", 26, -90), ("holt-3", -20, -70),
             ("holt-1", 30, -76), ("holt-2", 8, -64), ("holt-3", -44, -88),
             ("scrub-1", -56, -46), ("scrub-1", 54, -44), ("scrub-1", -12, -44),
             ("scrub-1", 16, -46), ("holt-2", 58, -92), ("holt-3", -60, -64),
             ("scrub-1", 44, -34), ("scrub-1", -34, -38)]
    for at, (style, tx, tz) in enumerate(plant):
        props_out.append({"id": f"holt-{at}", "kind": "tree", "seed": 700 + at,
                          "x": tx, "z": tz, "style": style})

    # Ground cover over the whole board rather than in patches: the density field is better at
    # patchiness than a hand-drawn outline is, and both gameplay numbers stay low -- tall grass is
    # cover nobody authored, in front of an objective nobody chose.
    props_out.append({"id": "cover", "kind": "flora", "seed": 800,
                      "points": [[-68, -100], [68, -100], [68, 0], [-68, 0]],
                      "spec": {"coverage": 0.14, "scale": 30, "octaves": 3, "fernShare": 0.06,
                               "flowerShare": 0.04, "flowerScale": 18, "tallShare": 0.03}})
    return {"styles": styles, "props": props_out}


def finish():
    return {
        "authors": [{"name": "Opus 5"}],
        "created": "2026-09-14",
        # Mesa: the driest tint in the game, which pulls the acacia canopy brown rather than the
        # olive a savanna board carries. It is the one colour here a block does not state itself.
        "biome": {"kind": "solid", "id": 37},
        "themes": {"marl": marl_theme(), "wash": wash_theme(), "works": works_theme()},
        "mapTheme": "marl",
        # the board's outer edge, drawn as an edge rather than as the staircase of rectangles the
        # plan compiled to. The gully's own edge is the gully-pan mark's ring and is not bent.
        "bendShapes": {"bank-26": {"k": 0.16, "wander": 3, "step": 11, "seed": 5},
                       "apron-23": {"k": 0.18, "wander": 3, "step": 11, "seed": 9}},
        "relief": {"*": {"base": APRON, "reach": 0, "step": 1, "landform": "rolling",
                         "grain": {"amplitude": 1.1, "scale": 19, "seed": 7},
                         "marks": marks(), "pushes": pushes()}},
        "addShapes": shapes(),
        "addLayers": vats(),
        "roomStyles": {"spawn": guild_hall(), "wool": dyehouse()},
        "dressing": dressing(),
    }


if __name__ == "__main__":
    with open(f"{HERE}/{SLUG}.plan.json", "w") as handle:
        json.dump(plan(), handle, indent=2)
    with open(f"{HERE}/{SLUG}.finish.json", "w") as handle:
        json.dump(finish(), handle, indent=2)
    print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")
