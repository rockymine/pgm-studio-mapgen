#!/usr/bin/env python3
"""Kettleshulme — the plan and the finish.

Adapted from a composed board:
    GET /api/compose?players=20&symmetry=rot_180  seed 23
    composerVersion markers-in-blocks-1, cell 5, score 0.0
    structure: hub double-hole · frontline twin · wools i, i

What the composer gave: a 55-block gritstone bar with two slots cut through it, a twin frontline,
and two wools of which one stood 123 blocks from the enemy's door and the other 83 — close enough
to the enemy that it was nearer to him than to its own team.

What this board does with it. The near wool is taken off the hub's flank entirely and set on its
own island, ten blocks of void from the hub and joined to it by a build zone that touches nothing
but this team's ground — the team transient-link `CT4` measures and the composer never places. The
far wool takes the flank the spawn had, the spawn goes to the back, and the two end up 138 and 143
blocks from the door that has to raid them. The mid is cut in two: a fifteen-block lane on each
flank with a declared buffer between them, so an attacker picks a side before he bridges, and the
east landing is walled.

The one idea: a coal-measure clough, dark grit and podzol, with a mill launder carried over the
hub's east slot on a deck a raider can run and a defender can shoot from.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-kettleshulme"

MOOR = 12                      # the one plan surface; a top block is surface - 1

plan = {
    "plan": 2,
    "meta": {"name": "Kettleshulme"},
    "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 20, "surface": MOOR,
                "observerY": 44},
    "pieces": [
        # the double-hole hub, as composed and shifted one cell of z so the mid is 30 blocks of void
        # rather than 20. Its two slots are the board's negative space and nothing fills them.
        {"id": "hub-nw", "role": "piece", "rect": [-6, 11, 7, 2]},
        {"id": "hub-sw", "role": "piece", "rect": [-6, 8, 7, 2]},
        {"id": "hub-w",  "role": "piece", "rect": [-6, 10, 2, 1]},
        {"id": "hub-mid", "role": "piece", "rect": [-2, 10, 3, 1]},
        {"id": "hub-ne", "role": "piece", "rect": [1, 11, 4, 2]},
        {"id": "hub-se", "role": "piece", "rect": [1, 8, 4, 2]},
        {"id": "hub-e",  "role": "piece", "rect": [3, 10, 2, 1]},
        # the frontline: the composer draws the east tip 10 blocks wide, which FR9 reads as a funnel
        {"id": "front-bar", "role": "piece", "rect": [-6, 5, 10, 3]},
        {"id": "front-w",   "role": "piece", "rect": [-4, 3, 3, 2]},
        {"id": "front-e",   "role": "piece", "rect": [1, 3, 3, 2]},
        # the spawn, off the hub's back rather than its west flank
        {"id": "spawn-t1",   "role": "piece", "rect": [0, 13, 3, 2]},
        {"id": "spawn-room", "role": "spawn", "rect": [0, 15, 2, 3]},
        # the far wool takes the flank the spawn had
        {"id": "wool-a-t1",   "role": "piece",     "rect": [-8, 9, 2, 2]},
        {"id": "wool-a-room", "role": "wool-room", "rect": [-10, 9, 2, 2]},
        # THE ISLAND. The near wool is cut off the hub and left ten blocks of void away: nothing
        # walks to it, and the only way across is a build zone this team owns.
        {"id": "wool-b-t1",   "role": "piece",     "rect": [7, 9, 2, 2]},
        {"id": "wool-b-room", "role": "wool-room", "rect": [9, 9, 2, 2]},
        # the strip of void between the two crossings, declared rather than left to be inferred.
        # It is centred on the origin, so it is its own rot_180 image and is stated once.
        {"id": "sike", "role": "buffer", "rect": [-1, -3, 2, 6], "mirrors": False},
    ],
    # THE MID, CUT IN TWO. One fifteen-block lane on each flank with ten blocks of void between
    # them: an attacker commits to a side of the board before he lays a block, and the two landings
    # are different ground — the east one is behind a wall.
    "zones": [
        {"id": "crossing-w", "rect": [-4, -3, 3, 6], "holes": []},
        {"id": "crossing-e", "rect": [1, -3, 3, 6], "holes": []},
        # THE OWN BRIDGE. Every interfacing component of this zone touches one team's islands and
        # no other — the hub and that team's own wool island — which is what CT4 calls a team
        # transient-link and BZ5 the defender-egress bridge. It is a lane a defender owns.
        {"id": "own-bridge", "rect": [5, 9, 2, 2], "holes": []},
        # zones are NOT fanned by the plan's symmetry — the compile writes back exactly the rects
        # stated — so the other team's bridge is authored as this one's rot_180 image by hand.
        {"id": "own-bridge-2", "rect": [-7, -11, 2, 2], "holes": []},
    ],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn-room", "at": [5, 7], "facing": "front"}],
        "wools": [{"id": "wool-1", "piece": "wool-a-room", "at": [5, 5]},
                  {"id": "wool-2", "piece": "wool-b-room", "at": [5, 5]}],
        "iron": [], "destroyables": [], "cores": [],
    },
    # the east lane's landing is walled and the west lane's is not, so the two crossings ask for
    # different things. PL13 keeps a wall off a wool room's own edge; this one is a frontline seam.
    "walls": [{"a": "front-e", "b": "front-bar"}],
    "boxes": [],
}


# ── materials ────────────────────────────────────────────────────────────────────────────────────
# Three families. The GROUND is dark — millstone grit, podzol, coal in the body of the rock. What is
# BUILT is red brick, which is the one warm thing on the board and reads from the far bank. The
# ACCENT is pale oak: the launder, the mill's frame, the cottage gables.
def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


GRASS, DIRT, COARSE, PODZOL = solid(2), solid(3), solid(3, 1), solid(3, 2)
STONE, ANDESITE, COBBLE, GRAVEL = solid(1), solid(1, 5), solid(4), solid(13)
COAL_ORE = solid(16)
BRICK, OAK, OAK_LOG = solid(45), solid(5, 0), solid(17, 0)
LAID_OAK = {"kind": "laidLog", "id": 17, "data": 0}
STONEBRICK = solid(98)


def cell_(seed, size, palette, rise=0, jitter=2, warp=2):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp,
            "palette": palette, "rise": rise}


def stack(bands, ending="handOver"):
    return {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}


def layered(bands, axis="depth", ending="handOver"):
    return {"kind": "layered", "axis": axis, "stack": stack(bands, ending)}


# the body of the edge, and the face it presents. Cells wider than they are tall, so a cut reads as
# bedded rock; the coal is in the FILL, where nobody sees it until a wall is cut.
GRIT_BODY = cell_(31, 9, [ANDESITE, STONE, COAL_ORE, ANDESITE], rise=5)
GRIT_FACE = cell_(32, 7, [ANDESITE, COBBLE, GRAVEL], rise=4)
SETTS = cell_(33, 5, [COBBLE, ANDESITE, GRAVEL])       # the mill yard, three close darks
TRACK = cell_(34, 5, [GRAVEL, COARSE, PODZOL])         # the pack road, three close browns

# the clough finished by its ANGLE. The cuts are at 26 and 40 degrees: under GET …/incline this
# board stands mostly flat with its edge between 30 and 40, so the shoulder band is what the edge's
# own brow wears and the face band is the edge itself.
CLOUGH_SURFACE = layered([
    # a surfacing block is exactly one course and what is under it is soil (PT1), so podzol tops
    # the shoulder band rather than lying under the turf
    (26, layered([(1, GRASS), (2, DIRT), (1, COARSE)])),       # the moor turf
    (14, layered([(1, PODZOL), (2, DIRT), (1, COARSE)])),      # the brow, worn to the leaf litter
    (50, GRIT_FACE),                                           # the edge
], axis="slope")

STRATA = layered([(2, ANDESITE), (1, GRAVEL), (3, STONE), (1, COBBLE), (2, ANDESITE)])

themes = {
    "clough": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": GRIT_FACE},
        "surface": {"enabled": True, "depth": 4, "material": CLOUGH_SURFACE},
        "wall": STRATA, "wallEnabled": True,
        "fill": GRIT_BODY,
    },
    # the mill yard: made ground, and its FACE is where its paint goes — a wallRun stripes along the
    # perimeter, which is the one thing nothing sampled from the plane can do and the one thing a
    # retaining wall needs.
    "yard": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": BRICK},
        "surface": {"enabled": True, "depth": 2, "material": SETTS},
        "wallEnabled": True,
        "wall": {"kind": "wallRun", "runs": [
            {"material": BRICK, "width": 3},
            {"material": COBBLE, "width": 2},
            {"material": ANDESITE, "width": 3},
        ]},
        "fill": GRIT_BODY,
    },
    # the launder: the one storey on the board, and it is timber because a launder is
    "launder": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop", "wallOnTerrainFaces": False,
        "rim": {"enabled": True, "depth": 1, "material": OAK_LOG},
        # a wall and a fill sample a volume, so each states a rise — without one every block of a
        # column resolves alike and the face reads as vertical stripes (PT4)
        "surface": {"enabled": True, "depth": 2, "material": cell_(35, 4, [OAK, OAK_LOG])},
        "wallEnabled": True, "wall": cell_(36, 5, [OAK_LOG, OAK], rise=3),
        "fill": cell_(37, 5, [OAK_LOG, OAK], rise=3),
    },
}

STEP = cell_(38, 4, [STONEBRICK, COBBLE, ANDESITE], rise=2)   # every stair on the board, one stone
WALLING = cell_(39, 4, [COBBLE, ANDESITE, STONE], rise=2)     # every drystone wall, one stone

# ── the shapes the plan cannot state ─────────────────────────────────────────────────────────────
MOOR_TOP, YARD, DECK_Y = 12, 16, 16


def pad(id_, ring, height, theme=None, scope="exclude"):
    shape = {"id": id_, "type": "polygon", "operation": "add", "group": "team",
             "floor": 0, "base_height": height, "height_mode": "level", "skirt": 0,
             "relief_scope": scope,
             "vertices": [[x, z] for x, z in ring],
             "anchor_heights": [height] * len(ring)}
    if theme:
        shape["theme"] = theme
    return shape


def flight(id_, ring, anchors, top, group="team", layer=None):
    """A flight: one polygon, a height per vertex, at least twice the run as rise, excluded from the
    relief because a relief graded across the seam would delete the boundary the flight states."""
    shape = {"id": id_, "type": "polygon", "operation": "add", "override": True, "keepClear": True,
             "group": group, "floor": 0, "base_height": top, "material": STEP,
             "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
             "vertices": [[x, z] for x, z in ring], "anchor_heights": list(anchors)}
    if layer:
        shape["layer"] = layer
    return shape


def wall_line(id_, points, top, radius=1, group="team"):
    return {"id": id_, "type": "polyline", "operation": "add", "override": True, "keepClear": True,
            "group": group, "floor": 0, "base_height": top, "material": WALLING,
            "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
            "radius": radius, "stroke_edge": "solid",
            "vertices": [[x, z] for x, z in points]}


add_shapes = [
    # THE MILL YARD — the board's one piece of made ground, cut flat at 16 and taken out of the
    # solve, so the hub meets it at a four-block face with a retaining wall on it. Its outline is
    # inside the hub's north bar on every side, because a shape that hangs over the void builds a
    # plinth of bedrock there and nothing declines it.
    pad("yard", [(-15, 57), (-2, 56), (9, 57), (10, 63), (-4, 64), (-15, 63)], YARD, theme="yard"),
    # the two ways up onto it, one from each end of the bar: ten blocks of run for four of rise
    flight("rake-w", [(-25, 58), (-15, 58), (-15, 62), (-25, 62)], [MOOR_TOP, YARD, YARD, MOOR_TOP],
           YARD),
    flight("rake-e", [(10, 58), (20, 58), (20, 62), (10, 62)], [YARD, MOOR_TOP, MOOR_TOP, YARD],
           YARD),
    # the yard's own wall, along the brow of the face
    wall_line("yard-wall", [(-15, 56), (-2, 55), (9, 56)], YARD + 2),
    # the drystone head-dyke along the back of the hub, which is where the moor stops being grazed
    wall_line("head-dyke", [(-28, 66), (-14, 68), (2, 67), (18, 69)], MOOR_TOP + 2),
]

# ── the launder: the board's second storey ───────────────────────────────────────────────────────
# A timber deck at y16, five courses over the hub's own top, carried out of the mill yard and
# across the east slot on piers. It is a way OUT and not a way back: a raider runs it and drops off
# its south end onto the hub's front bar, and coming back he goes round. `kind: "made"` paints it
# over its own span rather than from the bedrock course, and keeps SK10's pair walk and SK11's
# reachability walk off it.
launder_layer = {
    "id": "launder", "name": "Launder", "base_y": DECK_Y, "kind": "made", "part_of": "launder",
    "groups": [{"id": "launder", "name": "Launder", "mirrors": True,
                "shapeIds": ["launder-deck", "launder-kerb-w", "launder-kerb-e"]}],
    "shapes": [
        # the kerbs are three blocks wide, not one: a shape whose every column touches the void is
        # all edge, so the rim and the wall are the only buckets that ever paint it and the theme's
        # own surface lands nowhere on the board (SK23)
        {"id": "launder-deck", "type": "rectangle", "operation": "add", "theme": "launder",
         "min_x": 4, "min_z": 45, "max_x": 14, "max_z": 58, "floor": 0, "base_height": 1},
        {"id": "launder-kerb-w", "type": "rectangle", "operation": "add", "theme": "launder",
         "min_x": 4, "min_z": 45, "max_x": 7, "max_z": 58, "floor": 0, "base_height": 2},
        {"id": "launder-kerb-e", "type": "rectangle", "operation": "add", "theme": "launder",
         "min_x": 11, "min_z": 45, "max_x": 14, "max_z": 58, "floor": 0, "base_height": 2},
    ],
}

# ── the relief ───────────────────────────────────────────────────────────────────────────────────
relief = {
    # NO marks and one push. A mark is a constraint honoured exactly; a push is the only thing that
    # builds a landform, and a push is added to the surface the marks solved — so a board that
    # states both gets the mark's height with the push's on top of it. The flat this board needs is
    # the mill yard, and that is stated as made ground where it can be walked on.
    "team": {
        "base": MOOR_TOP, "reach": 0, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 1, "scale": 15, "seed": 12},
        "marks": [],
        "pushes": [
            # THE EDGE: the gritstone brow the frontline stands on, so the two teams look at each
            # other across the clough from two edges rather than over a flat. Its south lip is the
            # coast itself, which is what makes the drop into the mid a face and not a slope; its
            # skirt dies at z 49, which leaves the hub, the yard and both wools on level ground.
            # The two gradients are made to agree, which RL6 reads back off the built field: 6 over
            # a falloff of 9 is 0.67 a block outside the ring, and a crown of 11 over this ring's
            # own half-width — about 17, which the read answers and no arithmetic here predicts —
            # is 0.66 inside it.
            {"id": "edge", "amount": 6, "crown": 11, "falloff": 9, "roughness": 2, "seed": 13,
             "ring": [(-28, 17), (-8, 15), (8, 15), (19, 18), (17, 34), (-4, 38), (-26, 35)],
             "amounts": [6, 7, 7, 6, 5, 6, 6]},
        ],
    },
}

# ── the mill, and the two cottages beside it ─────────────────────────────────────────────────────
def hall(wall_stack, storeys):
    return {
        "foundation": {"plate": {"stack": stack([(1, COBBLE)], "repeat"), "extent": 1},
                       "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                                   "inlayInset": 2, "isPlain": True},
                       "footing": None},
        "roof": {"form": "gable", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
                 "ridgeCap": True, "hole": False,
                 "body": STONEBRICK, "verge": LAID_OAK, "gable": OAK,
                 "gableWindows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0,
                                  "data": 0, "sill": 1, "width": 1, "height": 1, "spacing": 3}},
        "wall": {"stack": wall_stack, "extent": 5},
        "post": OAK_LOG,
        "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                    "sill": 2, "width": 2, "height": 2, "spacing": 3},
        "storeys": storeys,
        "porch": None, "front": None,
        "beams": {"block": 17, "data": 0, "reach": 1, "any": True},
        "doorway": {"door": "air", "head": {"form": "none", "block": 53, "fill": "upperSlab",
                                            "fillBlock": 126, "fillData": 1},
                    "width": 2, "height": 3},
    }


GROUND_STOREY = {
    "clear": 5, "post": OAK_LOG, "deck": None,
    "wall": {"stack": stack([(4, cell_(40, 3, [BRICK, COBBLE])), (1, LAID_OAK)], "repeat"),
             "extent": 5},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 2, "width": 2, "height": 2, "spacing": 3},
}
UPPER_STOREY = {
    "clear": 4, "post": OAK_LOG, "deck": None,
    "wall": {"stack": stack([(3, BRICK), (1, LAID_OAK)], "repeat"), "extent": 4},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 1, "width": 1, "height": 2, "spacing": 4},
}

mill = hall(stack([(1, BRICK)], "repeat"), [GROUND_STOREY, UPPER_STOREY])
cot = hall(stack([(1, BRICK)], "repeat"), [dict(GROUND_STOREY, clear=6)])

# ── what stands on the board ─────────────────────────────────────────────────────────────────────
trees = json.load(open(os.path.join(HERE, "trees.json")))
tree_styles = {name: trees[name] for name in ("birk-1", "birk-2", "birk-3", "roundel-1")}

props = [
    # the pack road: the spawn door, over the hub's back, onto the mill yard by the west rake and
    # down onto the front bar. One line, both ends attached, running TO a door.
    {"id": "packway", "kind": "stroke", "seed": 51, "radius": 2, "style": "solid", "coverage": 1.0,
     "claimsGround": True, "pave": TRACK,
     "points": [[5, 72], [-4, 68], [-14, 64], [-20, 60]]},
    # and the lane to the far wool, which ends at its door
    {"id": "wool-lane", "kind": "stroke", "seed": 52, "radius": 2, "style": "solid",
     "coverage": 1.0, "claimsGround": True, "pave": TRACK,
     "points": [[-22, 58], [-26, 52], [-33, 50], [-38, 50]]},
    # ground cover: ONE shape over the whole board, the patchiness left to the density field, and
    # both gameplay numbers low — tall grass hides a player in front of an objective nobody chose.
    {"id": "ling", "kind": "flora", "seed": 53,
     "points": [[-52, 18], [24, 18], [56, 46], [40, 90], [-52, 78]],
     "spec": {"coverage": 0.20, "scale": 24, "octaves": 3, "fernShare": 0.35,
              "flowerShare": 0.05, "flowerScale": 12, "tallShare": 0.04}},
]

# NO third building. A 9 x 7 cottage on the front bar leaves under eight blocks of passable ground on
# both of its long sides, because the bar is fifteen deep — DR-PASS says so and it is right: a board
# already standing a spawn hall, two wool rooms and a launder has nowhere a fourth thing belongs.
# birches down the clough and along the head-dyke, every position read off the same seats mask
# every one of these is at least eight blocks inside a run of the seats mask and at least fifteen
# from any room, because the dressing pass seats a prop a block or three off the position stated and
# judges it at every image of its orbit — a cell at the edge of a legal run is nudged out of one
for i, (x, z, style) in enumerate([(-20, 24, "birk-1"), (-3, 32, "birk-2"), (14, 32, "birk-3"),
                                   (-8, 48, "roundel-1"), (-27, 64, "birk-1")]):
    props.append({"id": f"birk-{i}", "kind": "tree", "seed": 660 + i, "x": x, "z": z,
                  "style": style})

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-16",
    "themes": themes,
    "mapTheme": "clough",
    "biome": {"kind": "solid", "id": 6},
    # THE OUTLINE, ONE POINT AT A TIME. The compile hands back one 22-vertex ring for the team mass
    # and a four-vertex rectangle for the island. Read down the ring as the compile emitted it:
    #   0 (-50,45)  1 (-30,45)  2 (-30,25)  3 (-20,25)  4 (-20,15)  5 (-5,15)  6 (-5,25)
    #   7 (5,25)    8 (5,15)    9 (20,15)  10 (20,40)  11 (25,40)  12 (25,65)  13 (15,65)
    #  14 (15,75)  15 (10,75)  16 (10,90)  17 (0,90)   18 (0,65)   19 (-30,65)  20 (-30,55)
    #  21 (-50,55)
    # An insert names the edge LEAVING the vertex it states and every index above it moves, so the
    # list runs back to front and the run prints where each point landed.
    "editShapes": {
        "front-bar-12": [
            # THE WEST GARTH. The composed wool room has ground on one side and a bedrock plinth on
            # the other three — a stamped room fills its piece and fills downward in bedrock.
            {"index": 21, "x": -54, "z": 61},
            {"index": 20, "x": -32, "z": 62},
            # THE SPAWN YARD, the same fault at the other end of the board
            {"index": 18, "x": -8, "z": 70},
            {"index": 17, "x": -9, "z": 95},
            {"index": 16, "x": 19, "z": 95},
            {"index": 15, "x": 20, "z": 76},
            {"index": 14, "x": 17, "z": 70},
            # THE EDGE. The frontline is the high ground on this board and its lip is the coast, so
            # the two noses are pushed out and broken and the brow between them pulled back into a
            # V — the ground an attacker lands on is a headland, not the end of a rectangle.
            {"index": 11, "x": 25, "z": 43},
            {"index": 10, "x": 26, "z": 30},
            {"index": 9, "x": 24, "z": 17},
            {"index": 8, "x": 7, "z": 18},
            {"index": 7, "x": 4, "z": 31},
            {"index": 6, "x": -4, "z": 31},
            {"index": 5, "x": -7, "z": 18},
            {"index": 4, "x": -24, "z": 17},
            {"index": 3, "x": -27, "z": 30},
            {"index": 2, "x": -33, "z": 34},
            # and the west garth's north side, which the ring reaches last
            {"after": 0, "x": -36, "z": 39},
            {"index": 0, "x": -54, "z": 40},
        ],
        # THE ISLAND — a rectangle in the plan and a skerry in the world, with ground round the room
        # on all four sides and its west shore left where the plan drew it so the hop stays ten
        # blocks (G5's band) rather than shrinking under it.
        "wool-b-room-12": [
            {"after": 0, "x": 45, "z": 40},
            {"index": 2, "x": 61, "z": 48},
            {"after": 2, "x": 60, "z": 59},
            {"index": 4, "x": 48, "z": 63},
            {"index": 5, "x": 36, "z": 59},
            {"index": 0, "x": 35, "z": 48},
        ],
    },
    # the roughener, over the coasts at once. `out` on the mass is the studio's own slight bloat;
    # `in` on the island holds the plan's footprint, because the ten blocks between it and the hub
    # are the hop G5 measures and a bloated shore would eat them.
    "bendShapes": {"front-bar-12": {"wander": 2.5, "step": 9, "seed": 17, "side": "out"},
                   "wool-b-room-12": {"wander": 1.5, "step": 7, "seed": 18, "side": "in"}},
    "relief": relief,
    "addShapes": add_shapes,
    "addLayers": [launder_layer],
    "roomStyles": {"spawn": mill, "wool": cot},
    "dressing": {"styles": tree_styles,
                 "props": props},
}


if __name__ == "__main__":
    json.dump(plan,   open(os.path.join(HERE, f"{SLUG}.plan.json"),   "w"), indent=1)
    json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
    print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")
