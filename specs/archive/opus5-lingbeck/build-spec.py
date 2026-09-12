#!/usr/bin/env python3
"""Lingbeck — the plan and the finish.

A capture-the-wool board whose one idea is a cut. A beck runs in a five-course gill straight through
each team's ground from the frontline to the spawn's own doorstep, and the two wools sit on opposite
banks of it. Every rotation between them is a crossing, and there are exactly three: round the head,
over the brig, or down through the water at the ford.

The gill is also the best covered approach on the board and the worst place to be caught in.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-lingbeck"

MOSS, BED = 12, 7            # the bank and the beck's bed; a top block is h - 1

plan = {
    "plan": 2,
    "meta": {"name": "Lingbeck"},
    "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 24, "surface": MOSS, "observerY": 46},
    "pieces": [
        {"id": "moss",  "role": "piece",     "rect": [-11, 4, 14, 4], "surface": MOSS},
        # The hub is ONE piece and the gill is cut out of it downstream. A piece at a lower surface
        # enclosed by pieces at a higher one is not a cut: the compiler traces one outline for the
        # component, the taller add wins every column, and the low piece never appears in the world
        # — measured here, where a transect across the gill read 11 12 12 13 13 14 straight over it.
        {"id": "hub",   "role": "piece",     "rect": [-11, 8, 14, 8], "surface": MOSS},
        # barn, house, byre across the back, one wool on each bank, the spawn between them
        {"id": "barn",  "role": "wool-room", "rect": [-11, 16, 5, 3], "surface": MOSS},
        {"id": "stell", "role": "spawn",     "rect": [-6, 16, 4, 4],  "surface": MOSS},
        {"id": "byre",  "role": "wool-room", "rect": [-2, 16, 5, 3],  "surface": MOSS},
    ],
    "zones": [{"id": "mire", "rect": [-11, -4, 22, 8], "kind": "build"}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "stell", "at": [10, 10], "facing": "front",
                    "footprint": [6, 3, 8, 14]}],
        "iron":   [{"id": "iron-1", "piece": "stell", "at": [2, 10]},
                   {"id": "iron-2", "piece": "stell", "at": [18, 10]}],
        # WL9 reads the two spawn-wool walks over the PIECE graph, so a void notch between the spawn
        # and a room is a detour the straight line does not show: 22 and 38 against a 1.232 cap. The
        # three pieces abut, and the two markers are pushed out to the same distance from the door.
        "wools": [{"id": "wool-1", "piece": "barn", "at": [5, 12], "footprint": [2, 2, 13, 11]},
                  {"id": "wool-2", "piece": "byre", "at": [20, 12], "footprint": [10, 2, 13, 11]}],
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
DARKOAK, BRICK = solid(5, 5), solid(45)

def cell_(seed, size, palette, rise=0, jitter=2, warp=2):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp,
            "palette": palette, "rise": rise}

def stack(bands, ending="handOver"):
    return {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}

def layered(bands, axis="depth", ending="handOver"):
    return {"kind": "layered", "axis": axis, "stack": stack(bands, ending)}

ROCK_BODY = cell_(71, 9, [STONE, ANDESITE, STONE, COBBLE], rise=5)
BANK_FACE = cell_(72, 6, [GRAVEL, COARSE, STONE, ANDESITE], rise=3)
WAY = cell_(73, 5, [DIRT, COARSE, SPRUCE])       # a peat track: three close browns

LING_SURFACE = layered([
    (24, layered([(1, GRASS), (2, DIRT), (1, COARSE)])),
    (16, layered([(1, COARSE), (2, DIRT)])),
    (50, cell_(74, 7, [STONE, ANDESITE, GRAVEL], rise=3)),
], axis="slope")

themes = {
    "ling": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": cell_(75, 7, [STONE, ANDESITE, COBBLE],
                                                                  rise=3)},
        "surface": {"enabled": True, "depth": 4, "material": LING_SURFACE},
        "wall":    cell_(75, 7, [STONE, ANDESITE, COBBLE], rise=3),
        "wallEnabled": True,
        "fill":    ROCK_BODY,
    },
    # The gill. Its WALL is what a player standing in the beck looks at, so that is where the work
    # goes: a cut bank of gravel and coarse earth over the rock it is cut into.
    "heugh": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": COARSE},
        "surface": {"enabled": True, "depth": 2,
                    "material": cell_(76, 5, [GRAVEL, ANDESITE, COBBLE])},
        "wall":    BANK_FACE, "wallEnabled": True,
        "fill":    ROCK_BODY,
    },
    # peat: a splotch stated on a shape, where the moss is wet. Three close browns and no grass in
    # the pattern with them, so it reads as a different ground rather than as a mottle of this one.
    "myre": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": COARSE},
        "surface": {"enabled": True, "depth": 3,
                    "material": layered([(1, cell_(77, 6, [COARSE, DIRT, GRAVEL])), (2, DIRT)])},
        "wall":    BANK_FACE, "wallEnabled": True,
        "fill":    ROCK_BODY,
    },
}

STEP_MATERIAL = cell_(78, 4, [STONEBRICK, COBBLE, ANDESITE], rise=2)

# ── what the plan cannot state ───────────────────────────────────────────────────────────────────
def poly(id_, ring, **kw):
    return dict(id=id_, type="polygon", operation="add", group="team",
                vertices=[[x, z] for x, z in ring], **kw)


def ramp(id_, x_top, x_foot, z0, z1):
    """One bank of the ford: a tilted quad falling a course a block from the moss into the bed.
    The vertices are ordered so the anchors run along X, which is the way the ground has to fall."""
    return {"id": id_, "type": "polygon", "operation": "add", "override": True, "keepClear": True,
            "group": "team", "floor": 0, "base_height": MOSS, "material": BANK_FACE,
            "height_mode": "level", "skirt": 0,
            "vertices": [[x_top, z0], [x_top, z1], [x_foot, z1], [x_foot, z0]],
            "anchor_heights": [MOSS, MOSS, BED, BED]}


add_shapes = [
    # The gill, as an OVERRIDE add: override moves a shape into the second pass, where it overwrites
    # the column it lands on outright, which is the only thing that beats a taller ordinary add.
    {"id": "gill", "type": "rectangle", "operation": "add", "override": True, "group": "team",
     "min_x": -25, "min_z": 40, "max_x": -15, "max_z": 76,
     "floor": 0, "base_height": BED, "theme": "heugh",
     "height_mode": "level", "skirt": 0},
    # its south mouth, ramping out of the moss into the bed, so the gill is a route in as well as a
    # place to fall into
    {"id": "gill-mouth", "type": "polygon", "operation": "add", "override": True, "group": "team",
     "keepClear": True, "floor": 0, "base_height": MOSS, "theme": "heugh",
     "height_mode": "level", "skirt": 0,
     "vertices": [[-24, 34], [-16, 34], [-16, 46], [-24, 46]],
     "anchor_heights": [MOSS, MOSS, BED, BED]},
    # the ford: one ramp down each bank, and the beck's own bed between them
    ramp("ford-w", -30, -25, 46, 56),
    ramp("ford-e", -10, -15, 46, 56),
    # two patches of peat, where a moss is wet
    poly("myre-s", [(-46, 26), (-30, 24), (-22, 30), (-32, 38), (-46, 34)], theme="myre",
         floor=0, base_height=MOSS),
    poly("myre-e", [(0, 46), (14, 44), (20, 52), (10, 58), (-2, 54)], theme="myre",
         floor=0, base_height=MOSS),
]

# The brig is a SECOND LAYER, not an override add on the ground. A layer holds one span per column,
# so a deck written onto the ground layer would move that column's only span up and take the beck's
# bed with it — a lid, not a bridge (showcase/12-underpass measures exactly this). A slab at
# base_y 10 leaves the bed at y0..y6, six courses of air, and the deck flush with both banks.
add_layers = [{
    # base_y 11 and one course thick, lapping ONE block onto each bank. A layer's span is inclusive
    # of its top, so an upper layer sitting exactly at the lower one's top shares that course and is
    # the ordinary seam; two courses of overlap is SK10 — the two build as one mass and the gap the
    # layers were drawn to have is not in the world.
    "id": "brig", "name": "The Brig", "base_y": MOSS - 1,
    "shapes": [{"id": "brig-deck", "type": "rectangle", "operation": "add", "keepClear": True,
                "min_x": -25, "min_z": 62, "max_x": -15, "max_z": 68,
                "floor": 0, "base_height": 1, "material": STEP_MATERIAL}],
    "groups": [{"id": "brig", "mirrors": True, "shapeIds": ["brig-deck"]}],
}]

# ── the relief ───────────────────────────────────────────────────────────────────────────────────
def area(id_, x0, z0, x1, z1, h, **kw):
    return dict(id=id_, kind="area", h=h, ring=[[x0, z0], [x1, z0], [x1, z1], [x0, z1]], **kw)

relief = {
    "team": {
        "base": MOSS, "reach": 26, "step": 1, "landform": "plain",
        "grain": {"amplitude": 1, "scale": 15, "seed": 3},
        "marks": [
            area("landing", -55, 20, 15, 26, MOSS),
            {"id": "how-w",  "kind": "point", "at": [-48, 34], "r": 5, "h": MOSS + 4},
            {"id": "how-e",  "kind": "point", "at": [8, 36],   "r": 5, "h": MOSS + 5},
            {"id": "swang",  "kind": "point", "at": [-46, 64], "r": 5, "h": MOSS - 3},
            {"id": "rigg",   "kind": "point", "at": [10, 64],  "r": 5, "h": MOSS + 4},
            # Both banks are pinned FLAT at the ford and at the brig. A ramp's top anchor is an
            # absolute height, so where the relief leaves the bank two blocks above it the crossing
            # arrives at a step — measured, a BARRIER +3 at the ford's east head.
            area("ford-pad", -34, 44, -6, 58, MOSS),
            area("brig-pad", -34, 59, -6, 71, MOSS),
            area("back", -55, 78, 15, 100, MOSS),
        ],
        "pushes": [],
    }
}

# ── the bastle ───────────────────────────────────────────────────────────────────────────────────
# Three families: the ground is verdant over grey stone, so what is built is grey stone laid in
# courses under a dark timber roof — and the accent is brick, which appears once, at the plinth.
def bastle_style(storeys, roof_body):
    return {
        "foundation": {"plate": {"stack": stack([(1, BRICK)], "repeat"), "extent": 1},
                       "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                                   "inlayInset": 2, "isPlain": True},
                       "footing": None},
        "roof": {"form": "gable", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
                 "ridgeCap": True, "hole": False,
                 "body": roof_body, "verge": LAID_SPRUCE, "gable": SPRUCE,
                 "gableWindows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0,
                                  "data": 0, "sill": 1, "width": 1, "height": 1, "spacing": 3}},
        "wall": {"stack": stack([(1, STONEBRICK)], "repeat"), "extent": 5},
        "post": SPRUCE_LOG,
        "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                    "sill": 2, "width": 2, "height": 2, "spacing": 3},
        "storeys": storeys,
        "porch": None, "front": None,
        "beams": {"block": 17, "data": 1, "reach": 1, "any": True},
        "doorway": {"door": "air", "head": {"form": "none", "block": 53, "fill": "upperSlab",
                                            "fillBlock": 126, "fillData": 1}, "width": 2, "height": 3},
    }


BYRE_STOREY = {
    "clear": 5, "post": SPRUCE_LOG, "deck": None,
    "wall": {"stack": stack([(2, cell_(79, 3, [COBBLE, ANDESITE])), (3, STONEBRICK)], "repeat"),
             "extent": 5},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 2, "width": 1, "height": 2, "spacing": 4},
}
LOFT_STOREY = {
    "clear": 4, "post": SPRUCE_LOG, "deck": None,
    "wall": {"stack": stack([(3, SPRUCE), (1, LAID_SPRUCE)], "repeat"), "extent": 4},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 1, "width": 2, "height": 2, "spacing": 4},
}
bastle = bastle_style([BYRE_STOREY, LOFT_STOREY], DARKOAK)
shieling = bastle_style([dict(BYRE_STOREY, clear=4)], DARKOAK)

# ── what stands on it ────────────────────────────────────────────────────────────────────────────
trees = json.load(open(os.path.join(HERE, "trees.json")))
tree_styles = {name: {"kind": "tree", "form": "copied", "body": trees[name]["body"]}
               for name in ("birch-3", "birch-7", "birch-9", "holt-2", "holt-4", "fir-3")}

props = [
    # The beck, in TWO reaches, and only the southern one carries water. A channel reads the surface
    # TOP, and on a stacked board that is the maximum over every layer — so the brig's own deck reads
    # as the bed under it and the water line cannot hold across the jump. Measured: at (-20, 63) and
    # (-20, 67) the transect answers ground 12, which is the deck five courses over the bed.
    # The northern reach lays its gravel and coarse earth and stands dry, which is what a beck above
    # a sink actually looks like; it is kept for the bed it paints rather than for water it does not
    # carry, and the map says so rather than claiming a stream it has not got.
    {"id": "beck-south", "kind": "water", "seed": 11, "radius": 2.5, "depth": 2, "form": "stream",
     "edge": 0.8, "shore": 2, "shoreWander": True,
     "points": [[-20, 41], [-20, 48], [-20, 55], [-20, 60]],
     "bank": {"kind": "voronoi", "seed": 12, "cellSize": 5, "rise": 0, "bands": [
         {"material": GRAVEL, "depth": 1}, {"material": COARSE, "depth": 1},
         {"material": ANDESITE, "depth": 2}]}},
    {"id": "beck-north", "kind": "water", "seed": 13, "radius": 2.5, "depth": 2, "form": "stream",
     "edge": 0.8, "shore": 2, "shoreWander": True,
     "points": [[-20, 70], [-20, 73], [-20, 75]],
     "bank": {"kind": "voronoi", "seed": 12, "cellSize": 5, "rise": 0, "bands": [
         {"material": GRAVEL, "depth": 1}, {"material": COARSE, "depth": 1},
         {"material": ANDESITE, "depth": 2}]}},
    # the peat track: door -> down the east bank -> the moss -> the lip of the mire. One line.
    {"id": "track", "kind": "stroke", "seed": 81, "radius": 2, "style": "solid", "coverage": 1.0,
     "claimsGround": True, "pave": WAY,
     "points": [[-13, 86], [-8, 72], [-4, 56], [-6, 40], [-8, 26]]},
    # and the branch to the brig, which is the only reason to walk west off it
    {"id": "brig-way", "kind": "stroke", "seed": 82, "radius": 2, "style": "solid", "coverage": 1.0,
     "claimsGround": True, "pave": WAY,
     "points": [[-6, 64], [-13, 65], [-27, 65], [-38, 68], [-44, 76]]},
    # the bastle: a two-storey stone house on the east bank above the brig, because somebody who
    # owned a crossing built a house that watched it
    {"id": "bastle", "kind": "house", "seed": 801, "front": "negX", "style": "bastle",
     "wings": [{"corners": [[2, 48], [14, 58]], "spec": {"ridge": "alongX"}},
               {"corners": [[5, 59], [11, 65]], "spec": {"storeysHigh": 1, "ridge": "alongZ"}}]},
]
# Four trees. A shaw of three in the lee of the west how, where the ground shelters and the sheep do
# not go, and one thorn standing at the ford — which is a thing that really is planted at a crossing.
# The gill's own banks are the road's and the ford's, and a tree three blocks off a road is declined
# anyway (DR-ROAD), so the wood went where there was room for one rather than where the story wanted.
for i, (x, z, style) in enumerate([(-38, 40, "birch-3"), (-44, 50, "birch-7"), (-30, 34, "holt-2"),
                                   (-13, 56, "fir-3")]):
    props.append({"id": f"shaw-{i}", "kind": "tree", "seed": 950 + i, "x": x, "z": z, "style": style})

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-12",
    "themes": themes,
    "mapTheme": "ling",
    "biome": {"kind": "solid", "id": 5},
    "relief": relief,
    "addShapes": add_shapes,
    "addLayers": add_layers,
    "roomStyles": {"spawn": bastle, "wool": shieling},
    "dressing": {"styles": dict(tree_styles, bastle={"kind": "house", "shell": bastle}),
                 "props": props},
}

json.dump(plan,   open(os.path.join(HERE, f"{SLUG}.plan.json"),   "w"), indent=1)
json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")
