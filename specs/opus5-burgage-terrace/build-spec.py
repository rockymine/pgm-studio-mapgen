#!/usr/bin/env python3
"""Burgage Terrace — the plan and the finish.

A destroy board whose one idea is a boundary: made ground meets grown ground along one notched edge,
six courses tall, and everything the map is about happens at that edge. Above it a market terrace with
a row of burgage plots and the monument standing at its lip; below it a water meadow; between them a
retaining wall striped diagonally in the town's own colour, with two flights cut into it.

The two sides are joined by a build zone over void, and in the middle of it the stump of the old
bridge — an island that is nobody's and halves both hops.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-burgage-terrace"

HOLM, BURGAGE, PIER = 12, 18, 14      # relief heights; a top block is h - 1

plan = {
    "plan": 2,
    "meta": {"name": "Burgage Terrace"},
    "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 16, "surface": HOLM, "observerY": 52},
    "pieces": [
        # the bridge stump: centred on the origin, so it is its own rot_180 image
        {"id": "pier",    "role": "piece", "rect": [-3, -2, 6, 4],  "surface": PIER,
         "mirrors": False},
        {"id": "holm",    "role": "piece", "rect": [-8, 4, 16, 6],  "surface": HOLM},
        {"id": "terrace", "role": "piece", "rect": [-8, 10, 16, 8], "surface": BURGAGE},
        {"id": "bar",     "role": "spawn", "rect": [-3, 18, 6, 4],  "surface": BURGAGE},
    ],
    "zones": [{"id": "ford", "rect": [-8, -4, 16, 8], "kind": "build"}],
    "placements": {
        # ST10 caps a protection region at 20x30 and ST9 the building on it at 20x20; the ring
        # between the two is what WX8's iron cubes need, two blocks of clear air and their own 3x3
        "spawns": [{"id": "spawn-1", "piece": "bar", "at": [15, 10], "facing": "front",
                    "footprint": [6, 3, 18, 14]}],
        "iron":   [{"id": "iron-1", "piece": "bar", "at": [2, 10]},
                   {"id": "iron-2", "piece": "bar", "at": [28, 10]}],
        "destroyables": [{"id": "destroyable-1", "piece": "terrace", "at": [36, 9],
                          "style": "pillar-3", "materials": "obsidian", "float": 2,
                          "name": "The Market Cross"}],
        "cores": [], "wools": [],
    },
    "walls": [], "boxes": [],
}

# ── materials ────────────────────────────────────────────────────────────────────────────────────
def solid(i, d=0):  return {"kind": "solid", "id": i, "data": d}

GRASS, DIRT, COARSE = solid(2), solid(3), solid(3, 1)
STONE, ANDESITE, COBBLE, GRAVEL = solid(1), solid(1, 5), solid(4), solid(13)
STONEBRICK, CHISELLED = solid(98), solid(98, 3)
SAND, SANDSTONE = solid(12), solid(24)
SPRUCE, OAK, DARKOAK = solid(5, 1), solid(5, 0), solid(5, 5)
OAK_LOG, SPRUCE_LOG = solid(17, 0), solid(17, 1)
LAID_OAK = {"kind": "laidLog", "id": 17, "data": 0}
BRICK, HARDCLAY = solid(45), solid(172)

def cell_(seed, size, palette, rise=0, jitter=2, warp=2):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp,
            "palette": palette, "rise": rise}

def stack(bands, ending="handOver"):
    return {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}

def layered(bands, axis="depth", ending="handOver"):
    return {"kind": "layered", "axis": axis, "stack": stack(bands, ending)}

ROCK_BODY = cell_(51, 9, [STONE, ANDESITE, STONE, COBBLE], rise=5)
ROCK_FACE = cell_(52, 7, [STONE, ANDESITE, COBBLE], rise=3)
SETTS = cell_(53, 5, [STONEBRICK, ANDESITE, COBBLE])
WAY = cell_(54, 5, [GRAVEL, ANDESITE, COBBLE])

HOLM_SURFACE = layered([
    (22, layered([(1, GRASS), (2, DIRT), (1, COARSE)])),
    (18, layered([(1, COARSE), (2, DIRT)])),
    (50, ROCK_FACE),
], axis="slope")

themes = {
    "holm": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": ROCK_FACE},
        "surface": {"enabled": True, "depth": 4, "material": HOLM_SURFACE},
        "wall":    ROCK_FACE, "wallEnabled": True,
        "fill":    ROCK_BODY,
    },
    # The made ground. Its face is the town's, so it is STRIPED rather than sampled — a wallDiagonal
    # shears its runs by height, so they climb the retaining wall at a slope instead of standing
    # upright, and one of the runs is a teamTint: the town wears the colour of whoever holds it.
    "burgage": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": CHISELLED},
        "surface": {"enabled": True, "depth": 2, "material": SETTS},
        "wallEnabled": True,
        "wall": {"kind": "wallDiagonal", "slope": 2, "runs": [
            {"material": STONEBRICK, "width": 4},
            {"material": {"kind": "teamTint", "blockId": 159, "neutral": solid(159, 8)}, "width": 1},
            {"material": COBBLE, "width": 3},
            {"material": ANDESITE, "width": 2},
        ]},
        "fill": ROCK_BODY,
    },
    # the silt the river left, drawn as two splotches rather than sprinkled over the whole meadow
    "silt": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": SANDSTONE},
        "surface": {"enabled": True, "depth": 3,
                    "material": layered([(1, cell_(55, 7, [SAND, GRAVEL, SAND])), (2, SANDSTONE)])},
        "wall":    ROCK_FACE, "wallEnabled": True,
        "fill":    ROCK_BODY,
    },
}

STEP_MATERIAL = cell_(56, 4, [STONEBRICK, COBBLE, ANDESITE], rise=2)

# ── what the plan cannot state ───────────────────────────────────────────────────────────────────
def poly(id_, ring, **kw):
    return dict(id=id_, type="polygon", operation="add", group="team",
                vertices=[[x, z] for x, z in ring], **kw)


def flight(id_, ring, low, high):
    return {"id": id_, "type": "polygon", "operation": "add", "override": True, "keepClear": True,
            "group": "team", "floor": 0, "base_height": high, "material": STEP_MATERIAL,
            "height_mode": "level", "skirt": 0,
            "vertices": [[x, z] for x, z in ring],
            "anchor_heights": [low, low, high, high]}


add_shapes = [
    # Two flights, each with sixteen blocks of run for six courses: one down out of the market place
    # onto the meadow, one at the terrace's east end. They are made things, so they carry a material
    # rather than a theme and they say keepClear, or a road repaints their top course.
    flight("market-steps", [(-20, 40), (-12, 40), (-12, 56), (-20, 56)], HOLM, BURGAGE),
    flight("east-steps", [(20, 40), (28, 40), (28, 56), (20, 56)], HOLM, BURGAGE),
    # the silt: two splotches at the water's edge, where a river used to put it
    poly("silt-w", [(-38, 20), (-24, 18), (-16, 24), (-26, 30), (-36, 28)], theme="silt",
         floor=0, base_height=HOLM),
    poly("silt-e", [(6, 19), (22, 18), (32, 23), (24, 29), (10, 27)], theme="silt",
         floor=0, base_height=HOLM),
]

# ── the relief ───────────────────────────────────────────────────────────────────────────────────
def area(id_, x0, z0, x1, z1, h, **kw):
    return dict(id=id_, kind="area", h=h, ring=[[x0, z0], [x1, z0], [x1, z1], [x0, z1]], **kw)

relief = {
    "team": {
        "base": HOLM, "reach": 26, "step": 1, "landform": "plain",
        "grain": {"amplitude": 1, "scale": 13, "seed": 8},
        "marks": [
            # a water meadow is flat, and that is the point of it: the terrace above has to be
            # looking down on something
            area("holm-flat", -40, 18, 40, 30, HOLM),
            {"id": "how-w",  "kind": "point", "at": [-33, 40], "r": 5, "h": HOLM + 3},
            {"id": "how-e",  "kind": "point", "at": [33, 38],  "r": 5, "h": HOLM + 2},
            {"id": "swang",  "kind": "point", "at": [2, 40],   "r": 5, "h": HOLM - 1},
        ],
        "pushes": [],
    },
    "neutral": {
        "base": PIER, "reach": 10, "step": 1, "landform": "plain",
        "marks": [area("pier-top", -15, -10, 15, 10, PIER)],
        "pushes": [],
    },
}

# ── the burgage row ──────────────────────────────────────────────────────────────────────────────
# Three families: the ground is verdant over grey stone and the terrace is grey stone laid in courses,
# so what is BUILT on it is timber over a brick plinth and the accent is the hardened clay of the
# upper storeys. One style, three buildings, and they differ in height and footprint rather than in
# material — which is what makes a row read as one town.
def burgage_style(storeys, roof_body):
    return {
        "foundation": {"plate": {"stack": stack([(1, BRICK)], "repeat"), "extent": 1},
                       "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                                   "inlayInset": 2, "isPlain": True},
                       "footing": None},
        "roof": {"form": "gable", "pitch": 2, "slab": -1, "slabData": 0, "overhang": 1,
                 "ridgeCap": True, "hole": False,
                 "body": roof_body, "verge": LAID_OAK, "gable": HARDCLAY,
                 "gableWindows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0,
                                  "data": 0, "sill": 1, "width": 1, "height": 1, "spacing": 3}},
        "wall": {"stack": stack([(1, HARDCLAY)], "repeat"), "extent": 5},
        "post": OAK_LOG,
        "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                    "sill": 2, "width": 2, "height": 2, "spacing": 3},
        "storeys": storeys,
        "porch": None, "front": None,
        "beams": {"block": 17, "data": 0, "reach": 1, "any": True},
        "doorway": {"door": "air", "head": {"form": "none", "block": 53, "fill": "upperSlab",
                                            "fillBlock": 126, "fillData": 0}, "width": 2, "height": 3},
    }


SHOP = {
    "clear": 5, "post": OAK_LOG, "deck": None,
    "wall": {"stack": stack([(2, cell_(57, 3, [BRICK, HARDCLAY])), (3, HARDCLAY)], "repeat"),
             "extent": 5},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 2, "width": 2, "height": 2, "spacing": 3},
}
# the storey above: timber over the shop, with a course of LAID oak for the beams to be the end of.
# A log checker in the same log as the posts would read as one mass; this is a different statement.
SOLAR = {
    "clear": 4, "post": OAK_LOG, "deck": None,
    "wall": {"stack": stack([(3, OAK), (1, LAID_OAK)], "repeat"), "extent": 4},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 1, "width": 2, "height": 2, "spacing": 4},
}
ATTIC = {
    "clear": 3, "post": OAK_LOG, "deck": None,
    "wall": {"stack": stack([(2, OAK), (1, LAID_OAK)], "repeat"), "extent": 3},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 1, "width": 1, "height": 1, "spacing": 4},
}

plot_tall = burgage_style([SHOP, SOLAR, ATTIC], DARKOAK)      # three storeys: the merchant's
plot_low = burgage_style([SHOP, SOLAR], BRICK)                # two: the rest of the row
gatehouse = burgage_style([SHOP, SOLAR], DARKOAK)

# ── what stands on it ────────────────────────────────────────────────────────────────────────────
trees = json.load(open(os.path.join(HERE, "trees.json")))
tree_styles = {name: {"kind": "tree", "form": "copied", "body": trees[name]["body"]}
               for name in ("holt-1", "holt-2", "holt-4", "birch-3", "birch-7")}

props = [
    # the road: door -> the market place -> the steps -> the meadow -> the water. One line, both ends
    # attached, and it runs TO the buildings rather than through any of them.
    {"id": "gate-road", "kind": "stroke", "seed": 61, "radius": 2, "style": "solid",
     "coverage": 1.0, "claimsGround": True, "pave": SETTS,
     "points": [[0, 96], [-6, 82], [-12, 66], [-16, 53]]},
    {"id": "holm-road", "kind": "stroke", "seed": 62, "radius": 2, "style": "solid",
     "coverage": 1.0, "claimsGround": True, "pave": WAY,
     "points": [[-16, 34], [-12, 28], [-4, 23], [4, 19]]},
    # the burgage row: three plots along the terrace's back, all one style, differing in height and
    # footprint. A row of buildings IS the boundary here — it is what a terrace is for.
    {"id": "plot-a", "kind": "house", "seed": 701, "front": "negZ", "style": "plot_tall",
     "wings": [{"corners": [[10, 58], [21, 68]], "spec": {"ridge": "alongZ"}}]},
    {"id": "plot-b", "kind": "house", "seed": 702, "front": "negZ", "style": "plot_low",
     "wings": [{"corners": [[26, 58], [37, 67]], "spec": {"ridge": "alongZ"}}]},
    {"id": "plot-c", "kind": "house", "seed": 703, "front": "negZ", "style": "plot_low",
     "wings": [{"corners": [[-32, 58], [-20, 67]], "spec": {"ridge": "alongX"}},
               {"corners": [[-29, 68], [-23, 74]], "spec": {"storeysHigh": 1, "ridge": "alongZ"}}]},
]
for i, (x, z, style) in enumerate([(-34, 44, "holt-1"), (30, 44, "holt-2"), (10, 30, "birch-3"),
                                   (-28, 26, "birch-7"), (16, 34, "holt-4")]):
    props.append({"id": f"lime-{i}", "kind": "tree", "seed": 900 + i, "x": x, "z": z,
                  "style": style})

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-12",
    "themes": themes,
    "mapTheme": "holm",
    # the terrace wears the town's paint; without this it takes the map default and the whole idea of
    # the board — made ground meeting grown ground — is invisible
    "themeById": {"bar-18": "burgage", "pier-14": "burgage"},
    "biome": {"kind": "solid", "id": 4},
    # The terrace meets the meadow at a FACE, not a ramp: `hold` would let the relief bring the
    # meadow up to it, and then there is no six courses and no reason for a flight.
    "shapePropsById": {"bar-18": {"relief_scope": "exclude"}},
    # And the boundary between made and grown ground is not a straight line. Two re-entrants where
    # the flights come up and one salient between them, cut into the terrace's own front edge one
    # point at a time; the meadow's seaward coast is drawn the same way.
    "editShapes": {
        # Each re-entrant is exactly the flight that fills it, so the stair is SET INTO the wall
        # rather than leaning on it; between them the terrace pushes a salient out over the meadow.
        "bar-18": [{"after": 0, "x": -20, "z": 50}, {"after": 1, "x": -20, "z": 56},
                   {"after": 2, "x": -12, "z": 56}, {"after": 3, "x": -12, "z": 50},
                   {"after": 4, "x": 2, "z": 50},   {"after": 5, "x": 6, "z": 44},
                   {"after": 6, "x": 20, "z": 50},  {"after": 7, "x": 20, "z": 56},
                   {"after": 8, "x": 28, "z": 56},  {"after": 9, "x": 28, "z": 50}],
        # An insert names the edge LEAVING that vertex, so the index to give is the one before the
        # edge wanted — after 8 here is the board's own back edge and folds the ring, not its west
        # flank. The first build did exactly that and put ten blocks of void inside the meadow.
        "bar-12": [{"after": 0, "x": -30, "z": 14}, {"after": 1, "x": -16, "z": 22},
                   {"after": 2, "x": 0, "z": 13},   {"after": 3, "x": 16, "z": 21},
                   {"after": 4, "x": 29, "z": 15},
                   {"after": 6, "x": 36, "z": 36},
                   {"after": 9, "x": -36, "z": 34}],
    },
    "relief": relief,
    "addShapes": add_shapes,
    "roomStyles": {"spawn": gatehouse},
    "dressing": {"styles": dict(tree_styles,
                                plot_tall={"kind": "house", "shell": plot_tall},
                                plot_low={"kind": "house", "shell": plot_low}),
                 "props": props},
}

json.dump(plan,   open(os.path.join(HERE, f"{SLUG}.plan.json"),   "w"), indent=1)
json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")
