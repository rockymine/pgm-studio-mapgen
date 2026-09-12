#!/usr/bin/env python3
"""Heftfold — the plan and the finish.

A capture-the-wool board, laid out on the composer's own skeleton and then given the three things a
composed board does not have: an island in the middle, a team site that is split rather than one
rectangle, and two wools the spawn stands between instead of behind.

The one idea: made ground meeting grown ground. Each side is an open hill pasture at y11 and a
drystone-walled farm terrace at y16, and the whole board is the question of how you get up the four
feet between them. The two yards are split by a lane of pasture that runs from the pass to the spawn
door, so a defender who commits to one yard has to come back down to reach the other.

In the middle, on the saddle, the fold: a walled sheepfold that is nobody's, open toward each team.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-heftfold"

LEY, GARTH, SADDLE = 12, 17, 14          # the three surfaces; a top block is surface - 1

# ── the plan ─────────────────────────────────────────────────────────────────────────────────────
# Seven pieces at three surfaces. The pasture and the lane are one surface so they fuse into ONE
# terrain shape, and the two yards and their two rooms are a second. A piece earns its place here by
# being a room or a corridor: the fold, the ground a bridge lands on, the lane, the two yards, the
# two rooms, the spawn. The board's SHAPE is the relief's.
plan = {
    "plan": 2,
    "meta": {"name": "Heftfold"},
    "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 24, "surface": LEY, "observerY": 48},
    "pieces": [
        # the sheepfold on the saddle: centred on the origin, so it is its own rot_180 image and is
        # stated once. It is the island the composer's own middle does not have.
        {"id": "fold",    "role": "piece",     "rect": [-3, -2, 6, 4],   "surface": SADDLE,
         "mirrors": False},
        {"id": "pasture", "role": "piece",     "rect": [-11, 4, 14, 4],  "surface": LEY},
        {"id": "garth",   "role": "piece",     "rect": [-11, 8, 10, 6],  "surface": GARTH},
        {"id": "lane",    "role": "piece",     "rect": [-1, 8, 4, 6],    "surface": LEY},
        # barn, house, byre in a row across the back: the spawn stands BETWEEN its two wools rather
        # than behind both, so neither is the one nobody walks to. One is up in the walled yard and
        # one is down on the lane, so the two approaches differ in ground and not in distance.
        {"id": "barn",    "role": "wool-room", "rect": [-11, 14, 4, 3],  "surface": GARTH},
        {"id": "stell",   "role": "spawn",     "rect": [-7, 14, 6, 3],   "surface": GARTH},
        {"id": "byre",    "role": "wool-room", "rect": [-1, 14, 4, 3],   "surface": GARTH},
    ],
    # one zone for the whole middle: several over one crossing is a stitch a player reads as a
    # patchwork (BZ11). It is wider than either pasture's face because the board is SHIFTED, and the
    # extra width docks the mirrored image at its corner — the case BZ9 is written to pass.
    "zones": [{"id": "pass", "rect": [-11, -4, 22, 8], "kind": "build"}],
    "placements": {
        # the footprint is pulled off the piece edge on both flanks, because WX8's iron cube needs
        # its own 3x3 plus two blocks of clear air in the ring between the shell and the piece
        "spawns": [{"id": "spawn-1", "piece": "stell", "at": [15, 8], "facing": "front",
                    "footprint": [6, 3, 18, 9]}],
        "iron":   [{"id": "iron-1", "piece": "stell", "at": [2, 7]},
                   {"id": "iron-2", "piece": "stell", "at": [28, 7]}],
        "wools": [{"id": "wool-1", "piece": "barn", "at": [5, 10],
                   "footprint": [2, 2, 16, 11]},
                  {"id": "wool-2", "piece": "byre", "at": [15, 10],
                   "footprint": [2, 2, 16, 11]}],
        "destroyables": [], "cores": [],
    },
    "walls": [], "boxes": [],
}

# ── materials ────────────────────────────────────────────────────────────────────────────────────
def solid(i, d=0):  return {"kind": "solid", "id": i, "data": d}

GRASS, DIRT, COARSE = solid(2), solid(3), solid(3, 1)
STONE, ANDESITE, COBBLE, GRAVEL = solid(1), solid(1, 5), solid(4), solid(13)
STONEBRICK, SPRUCE, SPRUCE_LOG = solid(98), solid(5, 1), solid(17, 1)
LAID_SPRUCE = {"kind": "laidLog", "id": 17, "data": 1}
OAK, DARKOAK, BRICK = solid(5, 0), solid(5, 5), solid(45)

def cell_(seed, size, palette, rise=0, jitter=2, warp=2):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp,
            "palette": palette, "rise": rise}

def stack(bands, ending="handOver"):
    return {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}

def layered(bands, axis="depth", ending="handOver"):
    return {"kind": "layered", "axis": axis, "stack": stack(bands, ending)}

ROCK_BODY = cell_(11, 9, [STONE, ANDESITE, STONE, COBBLE], rise=5)
ROCK_FACE = cell_(12, 7, [STONE, ANDESITE, COBBLE], rise=3)
SETTS = cell_(13, 5, [COBBLE, STONE, GRAVEL])        # the yard, three close greys
TRACK = cell_(14, 5, [DIRT, COARSE, SPRUCE])         # the drove road, three close browns

# the hill finished by its angle: turf, then the worn shoulder, then the rock the sheep keep bare
LEY_SURFACE = layered([
    (26, layered([(1, GRASS), (2, DIRT), (1, COARSE)])),
    (16, layered([(1, COARSE), (2, DIRT)])),
    (48, ROCK_FACE),
], axis="slope")

themes = {
    "ley": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": ROCK_FACE},
        "surface": {"enabled": True, "depth": 4, "material": LEY_SURFACE},
        "wall":    ROCK_FACE, "wallEnabled": True,
        "fill":    ROCK_BODY,
    },
    # The made ground — an intake: walled grassland, not a car park. What is BUILT about it is its
    # edge, so the rim is the coping of the retaining wall and the wall is that wall's own face,
    # striped along the perimeter. A wallRun varies along the arc, which is the one thing nothing
    # sampled from the plane can do, and the one thing a retaining wall needs.
    "garth": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": STONEBRICK},
        "surface": {"enabled": True, "depth": 4,
                    "material": layered([(1, GRASS), (2, DIRT), (1, COARSE)])},
        "wallEnabled": True,
        "wall": {"kind": "wallRun", "runs": [
            {"material": STONEBRICK, "width": 2},
            {"material": COBBLE,     "width": 3},
            {"material": ANDESITE,   "width": 2},
            {"material": COBBLE,     "width": 4},
        ]},
        "fill": ROCK_BODY,
    },
    # The yard: the few blocks of the intake that are actually paved, because somebody walks there
    # every day. A splotch, stated on a shape, rather than a pattern sprinkled over the whole
    # terrace — if the answer to "why is it here" is "the noise put it there", it is not an answer.
    "yard": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": STONEBRICK},
        "surface": {"enabled": True, "depth": 2, "material": SETTS},
        "wallEnabled": True,
        "wall": {"kind": "wallRun", "runs": [
            {"material": STONEBRICK, "width": 2},
            {"material": COBBLE,     "width": 3},
            {"material": ANDESITE,   "width": 2},
        ]},
        "fill": ROCK_BODY,
    },
}

STEP_MATERIAL = cell_(16, 4, [STONEBRICK, COBBLE, ANDESITE], rise=2)
WALL_MATERIAL = cell_(17, 4, [COBBLE, STONE, ANDESITE], rise=2)

# ── what the plan cannot state ───────────────────────────────────────────────────────────────────
def poly(id_, ring, **kw):
    return dict(id=id_, type="polygon", operation="add", group="team",
                vertices=[[x, z] for x, z in ring], **kw)


def flight(id_, ring, low, high):
    """A flight is one polygon with a height per vertex: the first two at the foot, the last two at
    the head. The run is twice the rise or better, which is what separates a stair from a wall."""
    return {"id": id_, "type": "polygon", "operation": "add", "override": True, "keepClear": True,
            "group": "team",
            "floor": 0, "base_height": high, "material": STEP_MATERIAL,
            "height_mode": "level", "skirt": 0,
            "vertices": [[x, z] for x, z in ring],
            "anchor_heights": [low, low, high, high]}


def wall(id_, x0, z0, x1, z1, top=SADDLE + 4):
    """A length of drystone: terrain, so it says so with keepClear or a road will repaint its top."""
    return {"id": id_, "type": "rectangle", "operation": "add", "override": True, "keepClear": True,
            "group": "team",
            "floor": 0, "base_height": top, "material": WALL_MATERIAL,
            "height_mode": "level", "skirt": 0,
            "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1}


# The fold's own walls. Authored on one side of the origin and fanned, so the ring comes out with a
# gap in the middle of BOTH ends and each team walks in the same way its enemy does.
add_shapes = [
    # The fold's own walls. Authored on one side of the origin and fanned, so the ring comes out with
    # a gap in the middle of BOTH ends and each team walks in the same way its enemy does.
    wall("fold-w-se", 4, 7, 15, 9),
    wall("fold-w-sw", -15, 7, -4, 9),
    wall("fold-w-e", 13, -9, 15, 9),
    # three flights: up off the pasture into the yard, up off the lane into the yard, and down out of
    # the yard to the byre's own door. Each is on a line somebody actually walks, and each has run to
    # spare over its rise, which is what separates a stair from a wall.
    flight("gate",  [(-30, 36), (-22, 36), (-22, 46), (-30, 46)], LEY, GARTH),
    flight("wicket", [(-5, 48), (-5, 56), (-15, 56), (-15, 48)], LEY, GARTH),
    flight("byre-gate", [(0, 62), (12, 62), (12, 72), (0, 72)], LEY, GARTH),
    # the two patches of the intake that are paved: the ground the steading stands on, and the
    # working yard the three back buildings open onto
    poly("yard-house", [(-54, 40), (-34, 40), (-34, 62), (-40, 64), (-54, 60)], theme="yard",
         floor=0, base_height=GARTH, relief_scope="exclude"),
    poly("yard-back", [(-54, 63), (-24, 63), (-6, 66), (14, 66), (14, 70), (-54, 70)],
         theme="yard", floor=0, base_height=GARTH, relief_scope="exclude"),
]

# ── the relief ───────────────────────────────────────────────────────────────────────────────────
def area(id_, x0, z0, x1, z1, h, **kw):
    return dict(id=id_, kind="area", h=h, ring=[[x0, z0], [x1, z0], [x1, z1], [x0, z1]], **kw)

relief = {
    "team": {
        "base": LEY, "reach": 28, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 1, "scale": 14, "seed": 6},
        "marks": [
            # the ground a bridge lands on, flat to its own coast
            area("haugh", -55, 20, 15, 26, LEY),
            # and the hill above it: summits at a small radius, with the relaxation between them.
            # The one flat thing on the pasture is the gate's own approach, because a stair has to
            # arrive somewhere level or it is a stair onto a slope.
            {"id": "how-w",     "kind": "point", "at": [-50, 37], "r": 4, "h": LEY + 6},
            {"id": "how-e",     "kind": "point", "at": [10, 36],  "r": 4, "h": LEY + 4},
            {"id": "sike",      "kind": "point", "at": [-16, 35], "r": 5, "h": LEY - 2},
            area("gate-foot", -34, 30, -18, 40, LEY, bevel=3),
            {"id": "lane-s",    "kind": "point", "at": [6, 46],   "r": 4, "h": LEY + 1},
            area("lane-head", -4, 54, 15, 68, LEY + 1),
        ],
        "pushes": [],
    },
    # the saddle is its own group, and nothing on a non-fanned group is mirrored for it, so every
    # mark on it has to be its own image about the origin. One area centred there is exactly that.
    "neutral": {
        "base": SADDLE, "reach": 12, "step": 1, "landform": "plain",
        "grain": {"amplitude": 1, "scale": 9, "seed": 7},
        "marks": [area("saddle", -15, -10, 15, 10, SADDLE)],
        "pushes": [],
    },
}

# ── the hall, the barn, and the one house style behind both ──────────────────────────────────────
# Three families named before anything was painted: the ground is verdant over grey stone, so what is
# BUILT is timber and the accent is brick. Every roof on the board is a gable at pitch one — a shed
# is the one form this board does not use.
def hall_style(wall_stack, storeys):
    return {
        "foundation": {"plate": {"stack": stack([(1, COBBLE)], "repeat"), "extent": 1},
                       "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                                   "inlayInset": 2, "isPlain": True},
                       # a footing is null by default for a reason: it rings the building in a second
                       # material nobody asked for
                       "footing": None},
        "roof": {"form": "gable", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
                 "ridgeCap": True, "hole": False,
                 # HS3: a bare log on a verge stands every block on end; a laid one takes the ridge
                 "body": BRICK, "verge": LAID_SPRUCE, "gable": SPRUCE,
                 "gableWindows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0,
                                  "data": 0, "sill": 1, "width": 1, "height": 1, "spacing": 3}},
        "wall": {"stack": wall_stack, "extent": 5},
        "post": SPRUCE_LOG,
        "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                    "sill": 2, "width": 2, "height": 2, "spacing": 3},
        "storeys": storeys,
        "porch": None, "front": None,
        # beams run out past the corners where two storeys meet, so the upper wall carries a course
        # of laid log for them to be the end of
        "beams": {"block": 17, "data": 1, "reach": 1, "any": True},
        "doorway": {"door": "air", "head": {"form": "none", "block": 53, "fill": "upperSlab",
                                            "fillBlock": 126, "fillData": 1}, "width": 2, "height": 3},
    }


GROUND_STOREY = {
    "clear": 5, "post": SPRUCE_LOG, "deck": None,
    "wall": {"stack": stack([(2, cell_(18, 3, [COBBLE, ANDESITE])), (3, SPRUCE)], "repeat"),
             "extent": 5},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 2, "width": 2, "height": 2, "spacing": 3},
}
UPPER_STOREY = {
    "clear": 4, "post": SPRUCE_LOG, "deck": None,
    "wall": {"stack": stack([(3, SPRUCE), (1, LAID_SPRUCE)], "repeat"), "extent": 4},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 1, "width": 1, "height": 2, "spacing": 4},
}

steading = hall_style(stack([(1, SPRUCE)], "repeat"), [GROUND_STOREY, UPPER_STOREY])
outbarn = hall_style(stack([(1, SPRUCE)], "repeat"), [dict(GROUND_STOREY, clear=6)])

# ── what stands on the board ─────────────────────────────────────────────────────────────────────
trees = json.load(open(os.path.join(HERE, "trees.json")))
tree_styles = {name: {"kind": "tree", "form": "copied", "body": trees[name]["body"]}
               for name in ("fir-1", "fir-3", "fir-5", "holt-2", "holt-4")}

props = [
    # the drove road: door -> yard -> gate -> pasture -> the lip of the pass. One line, both ends
    # attached, and it runs TO the doors rather than through anything.
    {"id": "drove", "kind": "stroke", "seed": 31, "radius": 2, "style": "solid", "coverage": 1.0,
     "claimsGround": True, "pave": SETTS,
     "points": [[-19, 72], [-23, 62], [-26, 52], [-26, 45]]},
    {"id": "drove-down", "kind": "stroke", "seed": 32, "radius": 2, "style": "solid",
     "coverage": 1.0, "claimsGround": True, "pave": TRACK,
     "points": [[-26, 38], [-25, 30], [-16, 24], [-6, 21]]},
    # the yard road, running from the house door to the barn door and stopping at it
    {"id": "yard", "kind": "stroke", "seed": 33, "radius": 2, "style": "solid", "coverage": 1.0,
     "claimsGround": True, "pave": SETTS,
     "points": [[-20, 76], [-30, 76], [-38, 75], [-45, 75]]},
    # and the lane, from the wicket down to the byre's own door
    {"id": "lonnin", "kind": "stroke", "seed": 34, "radius": 2, "style": "solid", "coverage": 1.0,
     "claimsGround": True, "pave": TRACK,
     "points": [[-2, 48], [4, 56], [6, 66], [6, 76]]},
    # the steading: a two-storey hall with a single-storey cross wing, standing in the yard
    {"id": "steading", "kind": "house", "seed": 501, "front": "posZ", "style": "steading",
     # HP3 caps a placed building at 192 blocks of wing, so a 14x10 hall takes a 7x7 cross wing and
     # no more. The hall's ridge runs ALONG the shared edge and the wing's INTO it, which is what
     # keeps HJ4 off a hall that is nearly square.
     "wings": [{"corners": [[-50, 42], [-38, 51]], "spec": {"ridge": "alongX"}},
               {"corners": [[-47, 52], [-41, 58]], "spec": {"storeysHigh": 1, "ridge": "alongZ"}}]},
    # One authored house and no more. The yard already stands three buildings — the steading, the
    # spawn hall and the barn the wool sits in — and a fourth is a farm nobody could run.
]
# a shelterbelt behind the yard, which is what a hill farm plants and where it plants it
for i, (x, z) in enumerate([(-36, 22), (-8, 44), (-36, 60), (4, 40), (10, 30)]):
    props.append({"id": f"shelter-{i}", "kind": "tree", "seed": 600 + i, "x": x, "z": z,
                  "style": ["fir-1", "fir-3", "fir-5", "holt-2", "holt-4"][i]})

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-12",
    "themes": themes,
    "mapTheme": "ley",
    "themeById": {"barn-17": "garth"},
    "biome": {"kind": "solid", "id": 1},
    # A terrace meets the tier below at a FACE, which is `exclude`: `hold` lets the ground ramp up to
    # meet the shape, and then there is no five feet to climb and no reason for a stair.
    "shapePropsById": {"barn-17": {"relief_scope": "exclude"}},
    # The grown ground gets a drawn coast, one point at a time; the made ground stays rectilinear
    # because a retaining wall is a straight thing — except where it is set back round the gateway,
    # which is the one place the boundary between the two is allowed to be interesting.
    "editShapes": {
        "barn-12": [{"after": 0, "x": -42, "z": 24}, {"after": 1, "x": -28, "z": 18},
                    {"after": 2, "x": -12, "z": 25}, {"after": 3, "x": 2, "z": 19},
                    {"after": 5, "x": 12, "z": 46}, {"after": 10, "x": -51, "z": 31}],
        "barn-17": [{"after": 0, "x": -33, "z": 40}, {"after": 1, "x": -33, "z": 46},
                    {"after": 2, "x": -19, "z": 46}, {"after": 3, "x": -19, "z": 40}],
    },
    "relief": relief,
    "addShapes": add_shapes,
    # The key is `wool`, not `cage`: SketchRoomStyles carries `wool` and `spawn`, and a key it does
    # not know is dropped in silence — the room then stamps the built-in bedrock box and nothing says
    # so. (tools/README.md and drive.py both document it as `cage`.)
    "roomStyles": {"spawn": steading, "wool": outbarn},
    "dressing": {"styles": dict(tree_styles,
                                steading={"kind": "house", "shell": steading},
                                outbarn={"kind": "house", "shell": outbarn}),
                 "props": props},
}

json.dump(plan,   open(os.path.join(HERE, f"{SLUG}.plan.json"),   "w"), indent=1)
json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")
