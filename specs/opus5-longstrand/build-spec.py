#!/usr/bin/env python3
"""Longstrand — the plan and the finish.

Adapted from a composed board:
    GET /api/compose?players=20&symmetry=mirror_z  seed 12
    composerVersion markers-in-blocks-1, cell 5, score 4.173
    structure: hub twin · frontline bar · wools l, donut

What the composer gave: a 95 x 230 board — the longest thing in the browse — with a five-piece
donut wool deep at one end, a second wool sitting level with the frontline at the other, and one
plain twenty-block mid band across the middle. The near wool stood 108 blocks from the door that
had to raid it and the deep one 157: a raid and a walk-in, on the same board.

What this board does with it. The donut is kept — it is the one body the composer draws that a
player has to make a decision about — but it is pulled forward and shrunk to a ring of dune round a
fifteen-block blowout, and the near wool is taken off the front and set on the open strand opposite
it at the same depth, so the two raids are 195 and 188 blocks. The frontline bar is cut in two and
becomes a pair of headlands with a notch between them. And the mid, which arrived as one band, is
three stepping stones at a ten-block grain with a water lane down the west flank that opens
forty-five minutes in: four crossings where there was one, and the last of them arrives late.

The one idea: a sand spit — flat, pale and open nearly everywhere, with one dune ring on it that
you have to walk round.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-longstrand"

STRAND = 10                    # the base; a top block is surface - 1

plan = {
    "plan": 2,
    "meta": {"name": "Longstrand"},
    "globals": {"cell": 5, "symmetry": "mirror_z", "maxPlayers": 20, "surface": STRAND,
                "observerY": 42},
    "pieces": [
        # THE FRONT. The composer draws one 55 x 25 bar; this is that bar, trimmed at both ends to
        # exactly the ground the two crossings land on and nothing more — the dead-share read named
        # its outer thirty blocks as ground no journey passes. The notch that splits it into two
        # headlands is cut in the LAYOUT, one vertex at a time, where G5's hop band cannot see it.
        {"id": "front-bar", "role": "piece", "rect": [-7, 3, 12, 3]},
        # the isthmus: twenty-five blocks wide and fifteen long, which is the whole of what makes
        # this board long rather than merely large
        {"id": "neck",      "role": "piece", "rect": [-3, 6, 5, 3]},
        {"id": "hub",       "role": "piece", "rect": [-6, 9, 12, 2]},
        {"id": "lonning",   "role": "piece", "rect": [-2, 11, 4, 7]},
        {"id": "spawn-t1",   "role": "piece", "rect": [-2, 18, 4, 2]},
        {"id": "spawn-room", "role": "spawn", "rect": [-1, 20, 2, 3]},
        # THE DUNE — the composer's donut, pulled forward off the board's far end and shrunk to a
        # ring round a fifteen-block blowout, with the wool room on the ring's far corner so that
        # both arms are somebody's road. A hole is never scenery and nothing fills this one.
        {"id": "dune-w",  "role": "piece", "rect": [3, 11, 2, 7]},
        {"id": "dune-n",  "role": "piece", "rect": [5, 11, 3, 2]},
        {"id": "dune-s",  "role": "piece", "rect": [5, 16, 3, 2]},
        {"id": "dune-e",  "role": "piece", "rect": [8, 11, 2, 7]},
        {"id": "wool-a-room", "role": "wool-room", "rect": [10, 16, 2, 2]},
        # and the other wool on the open strand opposite it, at the same depth and reached over
        # ground with nothing on it. Its lane hangs off the HUB and not off the spawn's own lonning
        # — five blocks of void between them — so the defender comes down to the hub and back out,
        # which is what brings the two wools' own walks to 118 and 100 instead of 118 and 79.
        {"id": "strand-w",    "role": "piece",     "rect": [-6, 11, 3, 3]},
        {"id": "wool-b-t1",   "role": "piece",     "rect": [-9, 12, 3, 4]},
        {"id": "wool-b-room", "role": "wool-room", "rect": [-11, 14, 2, 3]},
        # THE TWO STONES, twenty blocks apart and ten off each front — every hop on this board
        # inside G5's 10-to-20 band, which three stones in a row cannot be: the diagonal from a
        # front's inner corner to the far stone is 22 whatever the spacing.
        {"id": "stone-w", "role": "piece", "rect": [-5, -1, 3, 2], "mirrors": False},
        {"id": "stone-e", "role": "piece", "rect": [2, -1, 3, 2], "mirrors": False},
    ],
    # Five build zones and a water lane. One flush zone per side of each stone, which is what BZ11
    # asks for on a mid with islands in it; one more across the twenty blocks between the stones, so
    # a player who takes one stone can work along the chain instead of going back.
    "zones": [
        {"id": "hop-w-n", "rect": [-5, 1, 3, 2], "holes": []},
        {"id": "hop-w-s", "rect": [-5, -3, 3, 2], "holes": []},
        {"id": "hop-e-n", "rect": [2, 1, 3, 2], "holes": []},
        {"id": "hop-e-s", "rect": [2, -3, 3, 2], "holes": []},
        {"id": "hop-mid", "rect": [-2, -1, 4, 2], "holes": []},
        # THE TIDE — a water lane down the west flank, closed at the first tick and open
        # forty-five minutes in. It is a fourth crossing that arrives late, and it can never be the
        # connection the lint reads this board as joined by, which is why the five above exist.
        {"id": "tide", "rect": [-7, -3, 2, 6], "holes": [], "kind": "water-lane"},
    ],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn-room", "at": [5, 7], "facing": "front"}],
        "wools": [{"id": "wool-1", "piece": "wool-a-room", "at": [5, 5]},
                  {"id": "wool-2", "piece": "wool-b-room", "at": [5, 5]}],
        "iron": [], "destroyables": [], "cores": [],
    },
    "walls": [],
    "boxes": [],
}


# ── materials ────────────────────────────────────────────────────────────────────────────────────
# Three families. The GROUND is pale and warm — sand, sandstone, marram turf. What is BUILT is dark
# oak over stone brick, which is the only dark thing on the board and reads from the far headland.
# The ACCENT is prismarine: the two stones in the middle and the sea-marks on them, and nowhere else.
def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


GRASS, DIRT, COARSE = solid(2), solid(3), solid(3, 1)
SAND, SANDSTONE, SMOOTH_SANDSTONE = solid(12), solid(24), solid(24, 2)
GRAVEL, STONE, COBBLE = solid(13), solid(1), solid(4)
STONEBRICK, DARKOAK, DARKOAK_LOG = solid(98), solid(5, 5), solid(162, 1)
LAID_DARKOAK = {"kind": "laidLog", "id": 162, "data": 1}
PRISMARINE, DARK_PRISMARINE = solid(168), solid(168, 2)


def cell_(seed, size, palette, rise=0, jitter=2, warp=2):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp,
            "palette": palette, "rise": rise}


def stack(bands, ending="handOver"):
    return {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}


def layered(bands, axis="depth", ending="handOver"):
    return {"kind": "layered", "axis": axis, "stack": stack(bands, ending)}


DUNE_BODY = cell_(61, 9, [SANDSTONE, SAND, SANDSTONE, SMOOTH_SANDSTONE], rise=5)
DUNE_FACE = cell_(62, 7, [SAND, SANDSTONE, GRAVEL], rise=4)
BOARDS = cell_(63, 5, [DARKOAK, DARKOAK_LOG])          # the staithe's decking
TRACK = cell_(64, 5, [SAND, GRAVEL, COARSE])           # the way over the strand

# The strand finished by its ANGLE. Flat sand is bound by marram and reads green; the blown face of
# a dune is bare sand; only the eroded scarp shows the rock under it. Three bands, cut at 20 and 38
# degrees, because a dune's own angle of repose is about 34 and the cut has to fall either side.
STRAND_SURFACE = layered([
    (20, layered([(1, GRASS), (1, COARSE), (2, SAND)])),   # the marram-bound flat
    (18, layered([(1, SAND), (3, SAND)])),                 # the blown face
    (52, DUNE_FACE),                                       # the eroded scarp
], axis="slope")

STRATA = layered([(2, SANDSTONE), (1, SAND), (3, SANDSTONE), (1, GRAVEL), (2, SMOOTH_SANDSTONE)])

themes = {
    "strand": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": DUNE_FACE},
        "surface": {"enabled": True, "depth": 4, "material": STRAND_SURFACE},
        "wall": STRATA, "wallEnabled": True,
        "fill": DUNE_BODY,
    },
    # the two stones in the middle: tide-washed rock, and the one cold thing on a warm board
    "skear": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": DARK_PRISMARINE},
        "surface": {"enabled": True, "depth": 2,
                    "material": cell_(65, 6, [PRISMARINE, DARK_PRISMARINE, COBBLE])},
        "wallEnabled": True,
        "wall": {"kind": "wallRun", "runs": [
            {"material": DARK_PRISMARINE, "width": 3},
            {"material": STONE, "width": 2},
        ]},
        "fill": cell_(66, 7, [STONE, COBBLE], rise=4),
    },
    # the staithe: the plank-and-stone landing the spawn hall stands on, and the one made ground
    "staithe": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": DARKOAK_LOG},
        "surface": {"enabled": True, "depth": 2, "material": BOARDS},
        "wallEnabled": True,
        "wall": {"kind": "wallRun", "runs": [
            {"material": STONEBRICK, "width": 3},
            {"material": DARKOAK_LOG, "width": 2},
        ]},
        "fill": DUNE_BODY,
    },
}

STEP = cell_(67, 4, [STONEBRICK, COBBLE, SANDSTONE], rise=2)
FENCE = cell_(68, 4, [DARKOAK_LOG, DARKOAK], rise=2)

STRAND_TOP, STAITHE = 10, 12


def pad(id_, ring, height, theme=None, scope="exclude"):
    shape = {"id": id_, "type": "polygon", "operation": "add", "group": "team",
             "floor": 0, "base_height": height, "height_mode": "level", "skirt": 0,
             "relief_scope": scope,
             "vertices": [[x, z] for x, z in ring],
             "anchor_heights": [height] * len(ring)}
    if theme:
        shape["theme"] = theme
    return shape


def flight(id_, ring, anchors, top, group="team"):
    return {"id": id_, "type": "polygon", "operation": "add", "override": True, "keepClear": True,
            "group": group, "floor": 0, "base_height": top, "material": STEP,
            "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
            "vertices": [[x, z] for x, z in ring], "anchor_heights": list(anchors)}


def groyne(id_, points, top, radius=1, group="team"):
    """A timber groyne as a POLYLINE — the rasterizer splines its points before offsetting the band,
    so four clicked points draw as a curve. A polyline states its bounds rather than the points a
    height is stated at, so it takes one base_height and no anchor_heights."""
    return {"id": id_, "type": "polyline", "operation": "add", "override": True, "keepClear": True,
            "group": group, "floor": 0, "base_height": top, "material": FENCE,
            "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
            "radius": radius, "stroke_edge": "solid",
            "vertices": [[x, z] for x, z in points]}


add_shapes = [
    # THE STAITHE — the one piece of made ground, a plank-and-stone landing at the head of the
    # lonning with the spawn hall on it, flat to its edge and out of the solve.
    pad("staithe", [(-13, 88), (2, 87), (3, 116), (-13, 117)], STAITHE, theme="staithe"),
    # the ramp down off it onto the strand: twelve blocks of run for two of rise
    flight("staithe-ramp", [(-8, 76), (-2, 76), (-2, 88), (-8, 88)],
           [STRAND_TOP, STRAND_TOP, STAITHE, STAITHE], STAITHE),
    # two groynes running off the headland into the tide, which is what a strand this long has on it
    groyne("groyne-w", [(-30, 16), (-31, 8), (-28, 2), (-30, -4)], STRAND_TOP + 3),
    groyne("groyne-e", [(20, 16), (22, 9), (19, 3), (21, -3)], STRAND_TOP + 3),
]

# ── the relief ───────────────────────────────────────────────────────────────────────────────────
relief = {
    # No marks and two pushes. A mark is a constraint honoured exactly; a push is the only thing
    # that builds a landform, and a push is added to the surface the marks solved — so a board that
    # states both gets the mark's height with the push's on top of it.
    "team": {
        "base": STRAND_TOP, "reach": 0, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 1, "scale": 19, "seed": 21},
        # one mark, and it is the one WX11 asks for by name: a spawn whose floor stands two courses
        # over the ground beside it fills that face in bedrock, which is a wall nobody drew. Neither
        # push reaches this corner of the board, so the mark is not lifted by one.
        "marks": [{"id": "staithe-bench", "kind": "area", "h": 12,
                   "ring": [[-16, 84], [6, 83], [7, 120], [-16, 120]]}],
        "pushes": [
            # THE DUNE: the ring the composer drew as a donut, made of sand. Its ring is the four
            # arms' own outline and its two gradients agree — 7 over a falloff of 10 is 0.70 a block
            # outside, and a crown of 6 over a half-width of about 9 is 0.67 inside — so the
            # landform has no step at its own outline and the blowout in the middle is a hole in a
            # hill rather than a hole in a table.
            {"id": "dune", "amount": 7, "crown": 6, "falloff": 10, "roughness": 3, "seed": 22,
             "ring": [(18, 58), (34, 56), (48, 60), (48, 84), (33, 89), (18, 86)],
             "amounts": [6, 7, 7, 6, 7, 6]},
            # THE BANK: a low swell over the west strand, so the open wool is not approached across
            # a table. Half the dune's lift and half its reach.
            {"id": "bank", "amount": 4, "crown": 3, "falloff": 7, "roughness": 2, "seed": 23,
             "ring": [(-36, 60), (-20, 58), (-18, 72), (-34, 76)],
             "amounts": [4, 4, 3, 4]},
        ],
    },
    # the two stones are their own group and nothing on a group that does not mirror is mirrored for
    # it, so each mark is stated once and lies on ground that is its own mirror_z image
    "neutral": {
        "base": 11, "reach": 5, "step": 1, "landform": "plain",
        "grain": {"amplitude": 0, "scale": 8, "seed": 24},
        "marks": [
            {"id": "skear-w", "kind": "area", "h": 11,
             "ring": [[-25, -5], [-10, -5], [-10, 5], [-25, 5]]},
            {"id": "skear-e", "kind": "area", "h": 11,
             "ring": [[10, -5], [25, -5], [25, 5], [10, 5]]},
        ],
        "pushes": [],
    },
}


# ── the hall and the net-house ───────────────────────────────────────────────────────────────────
def hall(wall_stack, storeys):
    return {
        "foundation": {"plate": {"stack": stack([(1, STONEBRICK)], "repeat"), "extent": 1},
                       "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                                   "inlayInset": 2, "isPlain": True},
                       "footing": None},
        "roof": {"form": "hip", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
                 "ridgeCap": True, "hole": False,
                 "body": STONEBRICK, "verge": LAID_DARKOAK, "gable": DARKOAK,
                 "gableWindows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0,
                                  "data": 0, "sill": 1, "width": 1, "height": 1, "spacing": 3}},
        "wall": {"stack": wall_stack, "extent": 5},
        "post": DARKOAK_LOG,
        "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                    "sill": 2, "width": 2, "height": 2, "spacing": 3},
        "storeys": storeys,
        "porch": None, "front": None,
        "beams": {"block": 162, "data": 1, "reach": 1, "any": True},
        "doorway": {"door": "air", "head": {"form": "none", "block": 53, "fill": "upperSlab",
                                            "fillBlock": 126, "fillData": 1},
                    "width": 2, "height": 3},
    }


GROUND_STOREY = {
    "clear": 5, "post": DARKOAK_LOG, "deck": None,
    "wall": {"stack": stack([(3, cell_(69, 3, [STONEBRICK, COBBLE])), (2, DARKOAK)], "repeat"),
             "extent": 5},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 2, "width": 2, "height": 2, "spacing": 3},
}
UPPER_STOREY = {
    "clear": 4, "post": DARKOAK_LOG, "deck": None,
    "wall": {"stack": stack([(3, DARKOAK), (1, LAID_DARKOAK)], "repeat"), "extent": 4},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 1, "width": 1, "height": 2, "spacing": 4},
}

hythe = hall(stack([(1, DARKOAK)], "repeat"), [GROUND_STOREY, UPPER_STOREY])
nethouse = hall(stack([(1, DARKOAK)], "repeat"), [dict(GROUND_STOREY, clear=6)])

# ── what stands on the board ─────────────────────────────────────────────────────────────────────
trees = json.load(open(os.path.join(HERE, "trees.json")))
# the lifted bodies in this file are in the reader's own {foot, body} shape; a dressing style is a
# discriminated PropStyle, and a bare body there is a 500 rather than a 400 because the parse throws
# before any gate reads it
tree_styles = {name: {"kind": "tree", "form": "copied", "body": trees[name]["body"]}
               for name in ("pine-1", "pine-3", "pine-5", "scrub-1", "scrub-3")}

props = [
    # the way over the strand: the hall's door, down the ramp, along the lonning to the hub, and out
    # to the front. One line, both ends attached, running TO a door.
    {"id": "way", "kind": "stroke", "seed": 71, "radius": 2, "style": "solid", "coverage": 1.0,
     "claimsGround": True, "pave": TRACK,
     "points": [[-5, 100], [-5, 84], [-3, 66], [-2, 50], [-4, 36]]},
    # and the lane out to the open wool, which ends at its door
    {"id": "strand-lane", "kind": "stroke", "seed": 72, "radius": 2, "style": "solid",
     "coverage": 1.0, "claimsGround": True, "pave": TRACK,
     "points": [[-14, 52], [-22, 60], [-32, 68], [-38, 76]]},
    # ground cover: ONE shape over the whole board, the patchiness left to the density field, and
    # both gameplay numbers low — tall grass hides a player in front of an objective nobody chose
    {"id": "marram", "kind": "flora", "seed": 73,
     "points": [[-48, 20], [26, 20], [58, 60], [40, 112], [-48, 112]],
     "spec": {"coverage": 0.24, "scale": 28, "octaves": 3, "fernShare": 0.15,
              "flowerShare": 0.04, "flowerScale": 16, "tallShare": 0.05}},
]

# ONE building beside the two stamped rooms, standing where POST …/sketch/seats says a 9 x 7
# footprint may stand rather than where it looked right: a net-house on the dune's north-east
# shoulder, the only built thing on the ring. The seats mask cannot answer DR-WAY, DR-CROSS or
# DR-SLOPE — those three read the built world — and the first seat this house took, on the front
# bar, sent the lateral way 23 blocks further round and was declined for it.
props += [
    {"id": "nethouse-1", "kind": "house", "seed": 611, "front": "negZ", "style": "nethouse",
     "wings": [{"corners": [[41, 55], [49, 61]], "spec": {"ridge": "alongX", "storeysHigh": 1}}]},
]
# pines and scrub in the lee of the dune and along the strand, every position read off the same
# seats mask rather than guessed and then declined
for i, (x, z, style) in enumerate([(-25, 20, "scrub-1"), (10, 27, "scrub-3"), (25, 54, "pine-1"),
                                   (35, 63, "pine-3"), (-48, 90, "pine-5")]):
    props.append({"id": f"pine-{i}", "kind": "tree", "seed": 640 + i, "x": x, "z": z,
                  "style": style})

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-16",
    "themes": themes,
    "mapTheme": "strand",
    # the two stones are their own shapes, and a theme registered and not on a shape paints nothing
    "themeById": {"stone-w-10": "skear", "stone-e-10": "skear"},
    "biome": {"kind": "solid", "id": 35},
    # THE OUTLINE, ONE POINT AT A TIME. The compile hands back one 36-vertex ring for the whole team
    # unit and a rectangle for the blowout. Read down the ring as the compile emitted it:
    #   0 (-50,70)  1 (-40,70)  2 (-40,60)  3 (-30,60)  4 (-30,45)  5 (-15,45)  6 (-15,30)
    #   7 (-35,30)  8 (-35,15)  9 (25,15)  10 (25,30)  11 (10,30)  12 (10,45)  13 (30,45)
    #  14 (30,55)  15 (50,55)  16 (50,80)  17 (60,80)  18 (60,90)  19 (15,90)  20 (15,55)
    #  21 (10,55)  22 (10,100) 23 (5,100)  24 (5,115)  25 (-5,115) 26 (-5,100) 27 (-10,100)
    #  28 (-10,55) 29 (-15,55) 30 (-15,70) 31 (-30,70) 32 (-30,80) 33 (-40,80) 34 (-40,85)
    #  35 (-50,85)
    # An insert names the edge LEAVING the vertex it states and every index above it moves, so the
    # list runs back to front and five inserts on one edge are stated in reverse.
    "editShapes": {
        "dune-e-10": [
            # THE WEST GARTH. The composed wool room has ground on one side and a bedrock plinth on
            # the other three — a stamped room fills its piece and fills downward in bedrock.
            {"index": 35, "x": -56, "z": 90},
            {"index": 34, "x": -42, "z": 92},
            # THE EAST GARTH, at the dune ring's far corner, the same fault and the same answer
            {"index": 19, "x": 22, "z": 96},
            {"index": 18, "x": 64, "z": 97},
            {"index": 17, "x": 67, "z": 76},
            {"index": 16, "x": 52, "z": 72},
            # the front's east nose, pushed out and broken
            {"index": 9, "x": 28, "z": 13},
            # THE BAY. The composer draws the front as one 55 x 25 bar and the plan keeps it that
            # way, because splitting it into two headlands puts a 22-block diagonal between one
            # headland and the far stone and G5's hop band tops out at 20. So the split is cut HERE,
            # into the compiled outline, where the plan tier cannot see it: a scalloped bay eight
            # blocks deep that the middle of the crossing aims at and neither stone reaches.
            {"after": 8, "x": 10, "z": 16},
            {"after": 8, "x": 6, "z": 22},
            {"after": 8, "x": 0, "z": 24},
            {"after": 8, "x": -6, "z": 23},
            {"after": 8, "x": -12, "z": 16},
            # the front's west nose
            {"index": 8, "x": -38, "z": 13},
            # and the west flank of the hub, drawn back so the lane off it reads as a neck
            {"index": 4, "x": -27, "z": 47},
            {"index": 3, "x": -33, "z": 58},
            {"index": 0, "x": -56, "z": 66},
        ],
        # the two stones, rectangles in the plan and tide-worn rock in the world
        "stone-w-10": [
            {"after": 0, "x": -18, "z": -8},
            {"after": 2, "x": -7, "z": 0},
            {"after": 4, "x": -18, "z": 8},
            {"after": 6, "x": -28, "z": 0},
        ],
        "stone-e-10": [
            {"after": 0, "x": 18, "z": -8},
            {"after": 2, "x": 28, "z": 0},
            {"after": 4, "x": 18, "z": 8},
            {"after": 6, "x": 7, "z": 0},
        ],
    },
    # THE BLOWOUT IS NOT SCENERY. The donut's middle compiles to a subtract, which is the board's own
    # statement of its negative space: it may be redrawn but never filled. This one is rounded off
    # and opened a block on every side — the sand blown out of the middle of a dune ring.
    "shapePropsById": {
        "void-1-cut": {"vertices": [[28, 64], [37, 64], [41, 68], [41, 77],
                                    [37, 81], [28, 81], [24, 77], [24, 68]]},
    },
    # the roughener. `in` on every coast, because the hops across the mid are measured from these
    # shores and the studio's outward bloat would eat them: bent in, a ten-block hop reads twelve
    # to fourteen, which is still inside G5's band.
    "bendShapes": {"dune-e-10": {"wander": 2.0, "step": 11, "seed": 27, "side": "in"},
                   "stone-w-10": {"wander": 1.2, "step": 6, "seed": 28, "side": "in"},
                   "stone-e-10": {"wander": 1.2, "step": 6, "seed": 29, "side": "in"}},
    "relief": relief,
    "addShapes": add_shapes,
    "roomStyles": {"spawn": hythe, "wool": nethouse},
    "dressing": {"styles": dict(tree_styles, nethouse={"kind": "house", "shell": nethouse}),
                 "props": props},
}


if __name__ == "__main__":
    json.dump(plan,   open(os.path.join(HERE, f"{SLUG}.plan.json"),   "w"), indent=1)
    json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
    print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")
