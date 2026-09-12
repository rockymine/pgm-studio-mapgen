#!/usr/bin/env python3
"""Glassmere — the plan and the finish.

A destroy-the-core board on the two snowbound shores of a mere whose middle never freezes. One idea:
everything about the board is white and flat and readable except the one black gulf across it, and the
whole of an attack is the decision to start bridging where everybody can see you do it.

The ground is stated as ONE shape and its shape is the relief's. What varies is the angle: snow lies
on the flat and on the shoulder, and a crag face holds none — which is a `layered` stack on the slope
axis and not a theme per piece.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-glassmere"

APRON, SHELF, FELL, CRAG, BIELD = 14, 20, 24, 34, 18   # relief heights; a top block is h - 1

# ── the plan ─────────────────────────────────────────────────────────────────────────────────────
# Two pieces at one surface: the shore the whole match is played on, and the bield the team comes out
# of. A destroy board is a lane rather than a square, and the two sides are joined by a build zone
# over void spanning the width — never by land, so the crossing is a decision and not a corridor.
plan = {
    "plan": 2,
    "meta": {"name": "Glassmere"},
    "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 12, "surface": 14, "observerY": 56},
    "pieces": [
        {"id": "shore", "role": "piece", "rect": [-8, 4, 16, 15], "surface": 14},
        {"id": "bield", "role": "spawn", "rect": [-3, 19, 6, 3],  "surface": 14},
    ],
    "zones": [{"id": "gulf", "rect": [-8, -4, 16, 8], "kind": "build"}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "bield", "at": [15, 7], "facing": "front",
                    "footprint": [6, 2, 18, 10]}],
        "iron":   [{"id": "iron-1", "piece": "bield", "at": [2, 7]},
                   {"id": "iron-2", "piece": "bield", "at": [28, 7]}],
        # a core states its interior — a casing size and a wall thickness are two numbers that can
        # contradict each other, and `lava` cannot. The float and the leak pair, so both or neither.
        "cores": [{"id": "core-1", "piece": "shore", "at": [46, 36], "lava": 3, "lavaHeight": 3,
                   "float": 6, "leak": 5, "name": "The Beacon"}],
        "destroyables": [], "wools": [],
    },
    "walls": [], "boxes": [],
}

# ── materials ────────────────────────────────────────────────────────────────────────────────────
def solid(i, d=0):  return {"kind": "solid", "id": i, "data": d}

SNOW, ICE, PACKED = solid(80), solid(79), solid(174)
GRASS, DIRT, COARSE = solid(2), solid(3), solid(3, 1)
STONE, ANDESITE, COBBLE, GRAVEL = solid(1), solid(1, 5), solid(4), solid(13)
STONEBRICK, DARKOAK, SPRUCE_LOG = solid(98), solid(5, 5), solid(17, 1)
LAID_SPRUCE = {"kind": "laidLog", "id": 17, "data": 1}
WHITECLAY = solid(159, 0)

def cell_(seed, size, palette, rise=0, jitter=2, warp=2):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp,
            "palette": palette, "rise": rise}

def stack(bands, ending="handOver"):
    return {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}

def layered(bands, axis="depth", ending="handOver"):
    return {"kind": "layered", "axis": axis, "stack": stack(bands, ending)}

FELL_BODY = cell_(21, 9, [STONE, ANDESITE, STONE, COBBLE], rise=5)
CRAG_FACE = cell_(22, 7, [STONE, ANDESITE, COBBLE], rise=3)
WAY = cell_(23, 5, [GRAVEL, ANDESITE, COBBLE])     # a stony way, swept clear

# Snow lies on the flat and on the shoulder and a crag face holds none. One stack on the slope axis
# says all three; a height band would paint the crag white from above whatever stands under it.
# PT1: a surfacing block is exactly one course thick and what is under it is soil, so grass may only
# ever be the TOP band of a stack. Snow over grass over dirt is refused; snow over dirt is not.
FELL_SURFACE = layered([
    (14, layered([(1, SNOW), (2, DIRT)])),                             # under 14 degrees: lying snow
    (16, layered([(1, cell_(24, 7, [SNOW, GRASS, SNOW])), (2, DIRT)])),  # 14-30: scoured in patches
    (60, CRAG_FACE),                                                   # over 30: bare rock
], axis="slope")

themes = {
    "fell": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": CRAG_FACE},
        "surface": {"enabled": True, "depth": 4, "material": FELL_SURFACE},
        "wall":    CRAG_FACE, "wallEnabled": True,
        "fill":    FELL_BODY,
    },
}

STEP_MATERIAL = cell_(26, 4, [STONEBRICK, COBBLE, ANDESITE], rise=2)

# ── the shore, painted solid first and freckled afterwards ───────────────────────────────────────
# The edge of a ground is DRAWN and never sampled: a fractal between snow and ice reads as static.
# So the ice is a solid band laid right at the water, and the transition is a second, wider stroke
# over it at low coverage — a scatter of the two grounds into each other rather than a third ground
# laid along the join. `worn` is the one style that spends its coverage; `rough` fills its band solid.
ICE_BAND = {"kind": "layered", "axis": "depth",
            "stack": stack([(1, cell_(27, 6, [ICE, PACKED, ICE])), (2, PACKED)])}
FRECKLE = cell_(28, 5, [SNOW, ICE])

def stroke(id_, points, radius, pave, style="solid", coverage=1.0, seed=0, claims=False):
    return {"id": id_, "kind": "stroke", "seed": seed, "radius": radius, "style": style,
            "coverage": coverage, "claimsGround": claims, "pave": pave, "points": points}


# ── the relief ───────────────────────────────────────────────────────────────────────────────────
def area(id_, x0, z0, x1, z1, h, **kw):
    return dict(id=id_, kind="area", h=h, ring=[[x0, z0], [x1, z0], [x1, z1], [x0, z1]], **kw)

relief = {
    "team": {
        "base": APRON, "reach": 30, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 1, "scale": 15, "seed": 4},
        "marks": [
            # the frozen apron: flat to the water, because a shore is flat and because a bridge has
            # to land somewhere level
            area("apron", -40, 18, 40, 30, APRON),
            # the shelf the Beacon stands on, and the ground a defence forms on
            area("shelf", -30, 46, 20, 66, SHELF, bevel=5),
            # the crag on the west flank: the one place on the board with a view of the whole gulf
            {"id": "crag",   "kind": "point", "at": [-30, 78], "r": 5, "h": CRAG},
            {"id": "brow",   "kind": "point", "at": [-34, 38], "r": 4, "h": FELL + 2},
            {"id": "rigg",   "kind": "point", "at": [30, 44],  "r": 4, "h": FELL},
            {"id": "slack",  "kind": "point", "at": [26, 74],  "r": 5, "h": SHELF - 2},
            area("bield-floor", -18, 92, 18, 110, BIELD),
        ],
        "pushes": [],
    }
}

# ── what the plan cannot state ───────────────────────────────────────────────────────────────────
def flight(id_, ring, low, high):
    return {"id": id_, "type": "polygon", "operation": "add", "override": True, "keepClear": True,
            "group": "team", "floor": 0, "base_height": high, "material": STEP_MATERIAL,
            "height_mode": "level", "skirt": 0,
            "vertices": [[x, z] for x, z in ring],
            "anchor_heights": [low, low, high, high]}

add_shapes = [
    # one flight off the apron onto the shelf, on the line the way already takes
    flight("brae", [(2, 34), (10, 34), (10, 46), (2, 46)], APRON, SHELF),
]

# ── the bothy ────────────────────────────────────────────────────────────────────────────────────
# Three families named before painting: the ground is BRIGHT (snow) over grey stone, so what is built
# is grey stone laid in courses and the accent is dark timber — which is the one thing on this board
# that reads at all from across the mere.
def bothy_style(storeys):
    return {
        "foundation": {"plate": {"stack": stack([(1, COBBLE)], "repeat"), "extent": 1},
                       "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                                   "inlayInset": 2, "isPlain": True},
                       "footing": None},
        "roof": {"form": "gable", "pitch": 2, "slab": -1, "slabData": 0, "overhang": 1,
                 "ridgeCap": True, "hole": False,
                 "body": DARKOAK, "verge": LAID_SPRUCE, "gable": DARKOAK,
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


LOW_STOREY = {
    "clear": 5, "post": SPRUCE_LOG, "deck": None,
    "wall": {"stack": stack([(2, cell_(29, 3, [COBBLE, ANDESITE])), (3, STONEBRICK)], "repeat"),
             "extent": 5},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 2, "width": 2, "height": 2, "spacing": 3},
}
UPPER_STOREY = {
    "clear": 4, "post": SPRUCE_LOG, "deck": None,
    "wall": {"stack": stack([(3, STONEBRICK), (1, LAID_SPRUCE)], "repeat"), "extent": 4},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 1, "width": 1, "height": 2, "spacing": 4},
}
bothy = bothy_style([LOW_STOREY, UPPER_STOREY])
hut = bothy_style([dict(LOW_STOREY, clear=4)])

# ── what stands on it ────────────────────────────────────────────────────────────────────────────
trees = json.load(open(os.path.join(HERE, "trees.json")))
tree_styles = {name: {"kind": "tree", "form": "copied", "body": trees[name]["body"]}
               for name in ("fir-1", "fir-2", "fir-3", "fir-4", "fir-5")}

BOULDER = {"kind": "boulder", "form": "outcrop", "size": 4, "mossy": False,
           "rock": cell_(31, 4, [STONE, COBBLE, ANDESITE], rise=2)}

props = [
    # the ice, laid SOLID at the water's edge
    stroke("rime", [[-40, 22], [-18, 20], [4, 23], [24, 19], [40, 22]], 5, ICE_BAND, seed=41),
    # and the transition over it: wider, worn, and thin, so the two grounds freckle into each other
    stroke("rime-edge", [[-40, 28], [-16, 26], [6, 29], [26, 25], [40, 28]], 7, FRECKLE,
           style="worn", coverage=0.34, seed=42),
    # the way: door -> the Beacon -> the brae -> the shore. One line, attached at both ends.
    stroke("way", [[0, 100], [-2, 88], [2, 74], [6, 62], [6, 50]], 2, WAY, seed=43, claims=True),
    stroke("way-down", [[6, 46], [6, 38], [4, 30], [2, 24]], 2, WAY, seed=44, claims=True),
    stroke("way-crag", [[2, 74], [-12, 76], [-24, 70], [-28, 58], [-22, 52]], 2, WAY, seed=45,
           claims=True),
    # the bothy: a two-storey hall with a low cross wing, set back on the shelf's west end well clear
    # of the Beacon's own ground (OB19 keeps a prop ten blocks off a goal's marker and four off its
    # structure, and it is raised at the export with nothing earlier predicting it)
    {"id": "bothy", "kind": "house", "seed": 601, "front": "posX", "style": "bothy",
     "wings": [{"corners": [[-26, 50], [-14, 60]], "spec": {"ridge": "alongZ"}},
               {"corners": [[-13, 53], [-7, 59]], "spec": {"storeysHigh": 1, "ridge": "alongX"}}]},
]
for i, (x, z) in enumerate([(-26, 44), (-28, 90), (-34, 84), (30, 50), (20, 70)]):
    props.append({"id": f"fir-{i}", "kind": "tree", "seed": 700 + i, "x": x, "z": z,
                  "style": ["fir-1", "fir-2", "fir-3", "fir-4", "fir-5"][i]})
for i, (x, z) in enumerate([(-33, 72), (-8, 66), (-33, 48), (24, 34), (-14, 34)]):
    props.append(dict(BOULDER, id=f"scar-{i}", kind="boulder", seed=800 + i, x=x, z=z,
                      size=4 if i % 2 == 0 else 3))

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-12",
    "themes": themes,
    "mapTheme": "fell",
    # a cold biome, so the grass under the snow tints to the ice rather than fighting it
    "biome": {"kind": "solid", "id": 12},
    "editShapes": {"bield-14": [
        {"after": 0, "x": -30, "z": 13}, {"after": 1, "x": -16, "z": 21},
        {"after": 2, "x": 0, "z": 12},  {"after": 3, "x": 15, "z": 20},
        {"after": 4, "x": 29, "z": 14},
        {"after": 6, "x": 36, "z": 50}, {"after": 7, "x": 38, "z": 76},
        {"after": 14, "x": -37, "z": 72}, {"after": 15, "x": -35, "z": 44},
    ]},
    "relief": relief,
    "addShapes": add_shapes,
    "roomStyles": {"spawn": hut},
    "dressing": {"styles": dict(tree_styles, bothy={"kind": "house", "shell": bothy}),
                 "props": props},
}

json.dump(plan,   open(os.path.join(HERE, f"{SLUG}.plan.json"),   "w"), indent=1)
json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")
