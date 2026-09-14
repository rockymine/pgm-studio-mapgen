"""Redmarl — a CTW board cut into a red marl gully.

Each team's ground is offset to its own flank, so the dry red watercourse between them runs corner
to corner and the two sides come onto it from opposite ends. The wool is fetched out of the enemy's
dyehouse, carried down into the gully and back up the far bank to a plinth at your own back.

A wool board is judged on how much of its bounding box is land — `fill-ratio`, band [0.201, 0.542],
which no destroy board is asked — and that is what decides this plan's shape rather than any
preference: half the box is void, and the void is the two corners each team's bank does not reach.
The neck of gully floor between them is the only ground both teams stand on.

Four grounds meet on it and each is stated by the one instrument that can state it:

  the marl bank      an area mark at 26 with two dunes pushed up behind the dyehouses
  the apron          an area mark at 23, narrower than the bank, with one low swell in it
  the brink          an area mark at 21 held to its edge, so the gully is a face and not a grade
  the gully neck     an area mark at 17 whose ring wanders six blocks either side of the plan's
                     straight z, which is what stops the frontline reading as a ruled line

and the watercourse itself is a line mark with a narrow tread, so the band either side of it lofts
back to the floor rather than walling itself.

Two descents a team, and both are authored rather than graded: a built washing stair between two
revetments, and a slumped marl slip at the neck's own corner. Under rot_180 a team's slip is on the
flank opposite its enemy's, so the gully is crossed on the diagonal.

The pale built family — smooth sandstone, stone brick — appears only where somebody built it, and
every place it meets the marl it meets it over a face: the yards stand a course proud of the bank,
the revetments are walls, and the gully's own theme change follows the channel's break of slope.
Nothing pale is laid flush on red ground.
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
                    "surface": APRON, "observerY": 62},
        "pieces": [
            # The back row: two dyehouses with the spawn between them, so both are on somebody's
            # journey out of the door, and each wool marker sits at its room's FAR side -- which
            # is what buys the 30 blocks WL2 wants out of a 28-block spawn piece (ST10 caps that
            # piece at 30 x 20).                            blocks x -52..16, z -104..-88
            {"id": "dye-w",  "role": "wool-room", "rect": [-13, -26, 5, 4], "surface": BANK},
            {"id": "yard",   "role": "spawn",     "rect": [ -8, -26, 7, 4], "surface": BANK},
            {"id": "dye-e",  "role": "wool-room", "rect": [ -1, -26, 5, 4], "surface": BANK},
            # the bank the row stands on                    blocks x -52..16, z -88..-64
            {"id": "bank",   "role": "piece",     "rect": [-13, -22, 17, 6], "surface": BANK},
            # the apron, quarried back off both flanks      blocks x -44..-4, z -64..-44
            {"id": "apron",  "role": "piece",     "rect": [-11, -16, 10, 5], "surface": APRON},
            # the brink, the lip over the gully             blocks x -44..4,  z -44..-24
            {"id": "brink",  "role": "piece",     "rect": [-11, -11, 12, 5], "surface": BRINK},
            # the neck: the gully floor, and the one piece both teams stand on. Each team's brink
            # docks on its own half of it, so the two sides come on at opposite corners.
            #                                               blocks x -24..24, z -24..24
            {"id": "strand", "role": "piece",     "rect": [ -6,  -6, 12, 12], "surface": FLOOR},
        ],
        # the build zone over the neck and the two brinks that dock on it
        "zones": [{"id": "gully", "rect": [-11, -7, 22, 14], "kind": "build"}],
        "placements": {
            # yard's corner is (-32, -104): the point is (-18, -99) and the room x -26..-10,
            # which leaves each iron cube its 3 x 3 and two blocks of air to the shell
            "spawns": [{"id": "spawn-1", "piece": "yard", "at": [14, 5], "facing": "back",
                        "footprint": [6, 3, 16, 10]}],
            "iron": [{"id": "iron-1", "piece": "yard", "at": [3, 8]},
                     {"id": "iron-2", "piece": "yard", "at": [26, 8]}],
            # dye-w's corner is (-52, -104) and dye-e's is (-4, -104); both markers stand at the
            # far side of their room, 30 blocks from the spawn and 60 from each other
            "wools": [{"id": "wool-1", "piece": "dye-w", "at": [4, 8],
                       "footprint": [2, 2, 16, 12]},
                      {"id": "wool-2", "piece": "dye-e", "at": [16, 8],
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
BRICK = solid(45)
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
            (cell(31, 6, SANDSTONE, BRICK_STONE, SMOOTH, HARDCLAY), 1), (HARDCLAY, 1))},
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
         "ring": [[-54, -106], [-30, -104], [-4, -106], [18, -103],
                  [17, -64], [-6, -61], [-30, -64], [-54, -62]]},
        {"id": "apron-pan", "kind": "area", "h": APRON, "bevel": 4,
         "ring": [[-46, -66], [-28, -63], [-10, -66], [-2, -63],
                  [-3, -43], [-20, -41], [-38, -44], [-46, -42]]},
        # held to its edge -- a small bevel is what makes the lip a lip. West of x = -24 its own
        # south edge fronts void, which is the promontory the gully has cut back behind.
        {"id": "brink-pan", "kind": "area", "h": BRINK, "bevel": 2,
         "ring": [[-46, -46], [-28, -43], [-10, -46], [6, -43],
                  [5, -26], [-12, -22], [-30, -26], [-46, -23]]},
        # the neck. Its north edge wanders six blocks either side of the plan's z = -24, which is
        # what keeps the frontline off a ruled line; the ring reaches past the centre so its own
        # mirror overlaps it and the floor is continuous across z = 0.
        {"id": "gully-pan", "kind": "area", "h": FLOOR, "bevel": 1,
         "ring": [[-26, -26], [-12, -20], [2, -27], [16, -20], [26, -25],
                  [26, 4], [10, 8], [-6, 2], [-20, 7], [-26, 3]]},
        # the watercourse, running the neck's diagonal. A narrow tread and the rest of the band
        # lofts, so it is a channel cut in the floor and not a trench walled down both sides; its
        # own mirror comes up the other diagonal and the two meet at the centre.
        {"id": "channel", "kind": "line", "h": CHANNEL, "r": 6, "tread": 2,
         "points": [[-26, -14], [-14, -8], [-2, -2]]},
        # a side braid joining it off the slip's foot
        {"id": "braid", "kind": "line", "h": 15.5, "r": 4, "tread": 1,
         "points": [[-24, -13], [-20, -9], [-15, -5]]},
    ]


def pushes():
    """Added to the solved surface after the marks, so each is kept off ground a mark had to
    arrive at: the yards, the stair's head and foot, and the lip."""
    return [
        {"id": "dune-w", "ring": [[-52, -86], [-40, -84], [-36, -74], [-46, -66], [-52, -70]],
         "amount": 3.0, "falloff": 11, "crown": 2.4, "roughness": 1.5, "seed": 4},
        {"id": "dune-e", "ring": [[0, -86], [16, -84], [18, -72], [6, -66], [-2, -74]],
         "amount": 2.4, "falloff": 10, "crown": 2.0, "roughness": 1.3, "seed": 11},
        {"id": "swell", "ring": [[-38, -62], [-26, -60], [-20, -52], [-30, -46], [-40, -52]],
         "amount": 1.6, "falloff": 14, "crown": 0.6, "roughness": 1.0, "seed": 21},
        # a bar in the bed: cover on the one piece of ground both teams fight over
        {"id": "bar", "ring": [[-8, -14], [6, -12], [10, -4], [-2, 0], [-12, -6]],
         "amount": 1.7, "falloff": 8, "crown": 1.2, "roughness": 0.9, "seed": 31},
    ]


def shapes():
    """What the plan cannot state: the yards the buildings stand on, the two descents into the
    gully, the revetments holding the stair, and the pans the channel left."""
    out = []

    # The three yards, one per building, with three blocks of marl left between them so they read
    # as three works on a bank rather than one platform. relief_scope exclude takes each footprint
    # out of the solve, and a course above the bank makes every meeting a riser rather than a
    # change of colour on flat ground -- which is the one thing this palette cannot get away with.
    for name, ring in (
            ("yard-dye-w", [[-53, -104], [-44, -106], [-33, -103], [-32, -96],
                            [-34, -88], [-44, -86], [-53, -90]]),
            ("yard-spawn", [[-29, -103], [-19, -105], [-9, -103], [-8, -96],
                            [-10, -89], [-19, -87], [-29, -90]]),
            ("yard-dye-e", [[-4, -104], [6, -106], [16, -103], [17, -96],
                            [15, -88], [6, -86], [-4, -90]])):
        out.append({"id": name, "type": "polygon", "operation": "add",
                    "base_height": YARD, "relief_scope": "exclude", "keepClear": True,
                    "theme": "works", "vertices": ring})

    # The washing stair: level, sheer-sided, out of the relief's solve so it arrives where it was
    # told. Sixteen blocks of run against four of rise, and a material rather than a theme --
    # a stair is a thing somebody built and a theme is a place.
    out.append({"id": "wash-stair", "type": "polygon", "operation": "add",
                "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
                "keepClear": True, "floor": 0,
                "vertices": [[-6, -36], [2, -36], [2, -20], [-6, -20]],
                "anchor_heights": [BRINK, BRINK, FLOOR, FLOOR],
                "material": {"kind": "cell", "seed": 37, "cellSize": 6, "jitter": 1, "warp": 2,
                             "palette": [SMOOTH, BRICK_STONE, SMOOTH, SANDSTONE], "rise": 3}})

    # The revetments either side of it. Out of the solve, so they hold the height they were drawn
    # at while the ground falls away under them: a course proud at the head, four at the foot.
    for side, xs in (("w", -8), ("e", 3)):
        out.append({"id": f"revet-{side}", "type": "polyline", "operation": "add",
                    "radius": 1, "stroke_edge": "solid", "base_height": BRINK + 1,
                    "relief_scope": "exclude", "keepClear": True,
                    "vertices": [[xs, -37], [xs, -31], [xs, -25], [xs, -19]],
                    "material": {"kind": "layered", "axis": "depth", "stack": {
                        "ending": "repeat", "bands": [
                            {"material": CHIS, "thickness": 1},
                            {"material": SANDSTONE, "thickness": 4}]}}})

    # The slip at the neck's west corner: the bank slumped into the gully. Same arithmetic as the
    # stair and the opposite material -- red scree, so it reads as ground giving way rather than
    # as masonry. Under rot_180 a team's own slip is on the flank opposite its enemy's, so the
    # two sides come onto the neck at opposite corners and the crossing is a diagonal.
    out.append({"id": "slip-w", "type": "polygon", "operation": "add",
                "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
                "keepClear": True, "floor": 0,
                "vertices": [[-24, -38], [-16, -36], [-15, -18], [-23, -20]],
                "anchor_heights": [BRINK, BRINK, FLOOR, FLOOR],
                "material": {"kind": "cell", "seed": 39, "cellSize": 7, "jitter": 2, "warp": 3,
                             "palette": [RED_SAND, HARDCLAY, COARSE, RED_STONE], "rise": 2}})

    # The pads the vats stand on, so the made layer over them lands on ground of a known height.
    for name, ring in (("pad-w", [[-41, -61], [-33, -63], [-26, -58],
                                  [-28, -49], [-37, -48], [-42, -54]]),
                       ("pad-e", [[-20, -59], [-12, -61], [-5, -56],
                                  [-7, -47], [-16, -46], [-21, -52]])):
        out.append({"id": name, "type": "polygon", "operation": "add",
                    "base_height": APRON, "relief_scope": "exclude", "keepClear": True,
                    "theme": "works", "vertices": ring})

    # Where the channel widens, the ground the water left. A brush states a height_mode or it is
    # never a candidate for the paint at all; a raise of zero sits flush and changes no height.
    # Every one of these lies along the channel, so its edge is a break of slope and not a line
    # drawn across flat red ground.
    for name, ring in (("wash-w", [[-25, -19], [-15, -13], [-9, -6],
                                   [-17, -2], [-25, -8]]),
                       ("wash-mid", [[-11, -11], [-1, -7], [4, 0],
                                     [-5, 4], [-13, -3]])):
        out.append({"id": name, "type": "polygon", "operation": "add",
                    "height_mode": "raise", "base_height": 0, "skirt": 0,
                    "vertices": ring, "theme": "wash"})
    return out


def vats():
    """The dye vats: two stone-lined rings on the apron, one holding red liquor and one orange --
    the two colours the dyehouses behind them send out. They stand where the sightline across the
    apron wants breaking, and they are the only stained clay on the board."""
    made = []
    plan_vats = [("vat-w", -34, -55, CLAY_RED), ("vat-e", -13, -53, CLAY_ORANGE)]
    # a fill's field is sampled in the plane, so a rise is what stops a face reading as vertical
    # stripes (PT4) -- a made layer's material is resolved as a fill
    lining = {"kind": "cell", "seed": 57, "cellSize": 4, "jitter": 1, "warp": 2,
              "palette": [BRICK_STONE, SANDSTONE, BRICK_STONE, COBBLE], "rise": 3}
    for vat_id, cx, cz, liquor in plan_vats:
        layer = props.ring_wall(vat_id, cx, cz, outer=5, thickness=1, floor=APRON, height=3,
                                theme=None, inner_floor=None, name=f"Vat {vat_id[-1]}",
                                mirrors=False)
        inner = layer.pop("layout")
        layer["shapes"] = inner["shapes"]
        layer["groups"] = inner["groups"]
        layer["kind"] = "made"
        layer["part_of"] = "dyeworks"
        for shape in layer["shapes"]:
            shape.pop("theme", None)
            shape["material"] = lining
        # the liquor itself: one course inside the ring, an override add so it beats the wall
        layer["shapes"].append({"id": f"{vat_id}-liquor", "type": "circle", "operation": "add",
                                "center_x": cx, "center_z": cz, "radius": 3.5,
                                "floor": APRON, "base_height": 1, "keepClear": True,
                                "override": True, "material": liquor})
        layer["groups"][0]["shapeIds"].append(f"{vat_id}-liquor")
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
        # the slab that halves a roof course continues the body, so it is the body's own
        # material (HS3), and the door head's stair and its fill are one material too (HS4)
        "roof": {"form": "gable", "pitch": 1, "slab": 44, "slabData": 4, "overhang": 1,
                 "ridgeCap": True, "hole": False,
                 "body": BRICK, "verge": {"kind": "laidLog", "id": 162, "data": 0},
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
                    "head": {"form": "arched", "block": 108, "fill": "upperSlab",
                             "fillBlock": 44, "fillData": 4}},
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
                         body=BRICK_STONE, slab=44, slabData=5, gable=ACACIA)
    shell["doorway"] = dict(shell["doorway"],
                            head={"form": "arched", "block": 109, "fill": "upperSlab",
                                  "fillBlock": 44, "fillData": 5})
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
        # Out of the spawn door, down the bank, across the apron between the vats and onto the
        # stair's head. Three blocks a reader cannot quite tell apart, solid, because a worn band
        # reads as litter and a path is a claim about where people walk.
        {"id": "track-out", "kind": "stroke", "seed": 41, "radius": 2, "style": "solid",
         "coverage": 1.0, "claimsGround": True, "pave": paving,
         "points": [[-18, -86], [-21, -78], [-25, -70], [-26, -62]]},
        {"id": "track-apron", "kind": "stroke", "seed": 42, "radius": 2, "style": "solid",
         "coverage": 1.0, "claimsGround": True, "pave": paving,
         "points": [[-26, -62], [-22, -54], [-14, -48], [-6, -43]]},
        {"id": "track-stair", "kind": "stroke", "seed": 43, "radius": 2, "style": "solid",
         "coverage": 1.0, "claimsGround": True, "pave": paving,
         "points": [[-6, -43], [-4, -40], [-3, -37], [-3, -34]]},
        # the two haulage tracks along the bank to the dyehouses
        {"id": "track-dye-w", "kind": "stroke", "seed": 44, "radius": 2, "style": "solid",
         "coverage": 1.0, "claimsGround": True, "pave": paving,
         "points": [[-28, -86], [-35, -88], [-42, -90], [-46, -92]]},
        {"id": "track-dye-e", "kind": "stroke", "seed": 45, "radius": 2, "style": "solid",
         "coverage": 1.0, "claimsGround": True, "pave": paving,
         "points": [[-10, -86], [0, -88], [8, -90], [12, -92]]},
        # the slip's own worn line, off the apron and down onto the floor
        {"id": "track-slip", "kind": "stroke", "seed": 46, "radius": 2, "style": "solid",
         "coverage": 0.9, "claimsGround": True, "pave": paving,
         "points": [[-32, -48], [-27, -44], [-22, -40], [-20, -36]]},
        # The channel floor: not a path, so not solid -- a scoured bed reads as stones left.
        {"id": "bed", "kind": "stroke", "seed": 47, "radius": 4, "style": "stones",
         "coverage": 0.7, "claimsGround": True,
         "pave": cell(48, 6, GRAVEL, SAND, RED_SAND, COARSE),
         "points": [[-26, -14], [-14, -8], [-2, -2]]},
    ]

    # Two drying sheds on the bank. They are here because the bank needs a reason to be crossed
    # anywhere but along the track, and a sightline down it needs breaking.
    props_out.append({"id": "shed-w", "kind": "house", "seed": 501, "front": "posZ",
                      "style": "shed",
                      "wings": [{"corners": [[-48, -74], [-38, -66]], "spec": {"ridge": "alongX"}}]})
    props_out.append({"id": "shed-e", "kind": "house", "seed": 502, "front": "negZ",
                      "style": "shed",
                      "wings": [{"corners": [[0, -76], [10, -68]],
                                 "spec": {"storeysHigh": 1, "ridge": "alongX"}}]})

    # Boulders, each where the bed dropped it or where the bank has calved.
    # On the gully floor only, east of the two descents and clear of the bed's own stroke,
    # with ten blocks between any two -- a prop inside another prop's claim is a prop the
    # dressing pass declines and nothing in the world says so afterwards.
    for at, (bx, bz) in enumerate([(8, -18), (18, -10), (4, -4), (16, 4), (-8, 2), (-18, 6)]):
        props_out.append({"id": f"rock-{at}", "kind": "boulder", "seed": 610 + at,
                          "x": bx, "z": bz, "style": "rock"})

    # Acacia on the bank and scrub where the dust is deepest. Every one is off a track and off a
    # yard, and none is on the gully floor, which is a bed and carries nothing tall.
    plant = [("holt-1", -32, -70), ("holt-2", -14, -70), ("holt-3", -34, -80),
             ("holt-1", -42, -42), ("holt-2", -30, -28),
             ("scrub-1", 20, -20), ("scrub-1", -20, 16)]
    for at, (style, tx, tz) in enumerate(plant):
        props_out.append({"id": f"holt-{at}", "kind": "tree", "seed": 700 + at,
                          "x": tx, "z": tz, "style": style})

    # Ground cover over the whole board rather than in patches: the density field is better at
    # patchiness than a hand-drawn outline is, and both gameplay numbers stay low -- tall grass is
    # cover nobody authored, in front of an objective nobody chose.
    props_out.append({"id": "cover", "kind": "flora", "seed": 800,
                      "points": [[-58, -110], [24, -110], [28, 28], [-28, 28]],
                      "spec": {"coverage": 0.13, "scale": 30, "octaves": 3, "fernShare": 0.06,
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
        # the compiled ground is one component named for its first piece, with a shape per
        # surface it stands at -- `apron-26` is the bank, `apron-23` the apron itself
        "bendShapes": {"apron-26": {"k": 0.16, "wander": 3, "step": 11, "seed": 5},
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
