#!/usr/bin/env python3
"""Grykefell — the plan and the finish.

A destroy-the-monument board on a limestone pavement fell. One idea: the ground itself is the cover.
Limestone weathers into clints and grikes, so the fell is bare pale rock almost everywhere and the
green is in the few sheltered shelves that hold soil — which means every piece of cover on this board
is a step in the rock rather than a thing standing on it.

One monument a team, out in the open on a scoured slab, and the four quarters around it are four
different ways in (`approaches.md`): a birch hag to walk through on the west, a scar to drop off on
the east, a dry gill to come up out of on the south-west, and open pavement to cross on the south.

The plan is two pieces and a build zone. Everything that is a shape of ground is in the relief, and
what the ground is finished with is decided by its ANGLE — one `layered` stack on the slope axis —
rather than by which piece it is on.
"""
import json, os, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-grykefell"
API = os.environ.get("PGM_STUDIO_API", "http://localhost:7894").rstrip("/")
API = API[:-4].rstrip("/") if API.endswith("/api") else API

SHORE, FELL, SLAB, BROW, BIELD = 22, 25, 27, 31, 27   # a top block is h - 1

# ── the plan ─────────────────────────────────────────────────────────────────────────────────────
# Two pieces at one surface and one build zone across the whole width. The land ends at z 10 and its
# own rot_180 image begins at z -10, so the gap between the two teams is 20 blocks of void with a
# build slice over it: a crossing an attacker pays for, never a corridor a defender stands in.
plan = {
    "plan": 2,
    "meta": {"name": "Grykefell"},
    "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 24, "surface": 24, "observerY": 58},
    "pieces": [
        {"id": "fell",  "role": "piece", "rect": [-8, 2, 16, 15], "surface": 24},
        {"id": "bield", "role": "spawn", "rect": [-3, 17, 6, 3],  "surface": 25},
    ],
    "zones": [{"id": "sound", "rect": [-8, -4, 16, 8], "kind": "build"}],
    "placements": {
        # the hall sits back in its piece: 18 x 10 inside a 30 x 15 spawn ground, so the apron in
        # front of the door is the piece's own and the iron cubes have the ring WX8 needs
        "spawns": [{"id": "spawn-1", "piece": "bield", "at": [15, 7], "facing": "front",
                    "footprint": [6, 2, 18, 10]}],
        "iron":   [{"id": "iron-1", "piece": "bield", "at": [2, 7]},
                   {"id": "iron-2", "piece": "bield", "at": [28, 7]}],
        # the monument stands 14 blocks off the centre line on purpose: a goal on the axis gives the
        # board two journeys down its middle and leaves both flanks dead (`coverage`)
        "destroyables": [{"id": "destroyable-1", "piece": "fell", "at": [60, 44],
                          "style": "pillar-2", "float": 4, "name": "The Cairn"}],
        "cores": [], "wools": [],
    },
    "walls": [], "boxes": [],
}

# ── materials ────────────────────────────────────────────────────────────────────────────────────
def solid(i, d=0):  return {"kind": "solid", "id": i, "data": d}

STONE, DIORITE, POL_DIORITE, ANDESITE = solid(1), solid(1, 3), solid(1, 4), solid(1, 5)
COBBLE, GRAVEL, STONEBRICK, CHISELLED = solid(4), solid(13), solid(98), solid(98, 3)
GRASS, DIRT, COARSE = solid(2), solid(3), solid(3, 1)
SPRUCE_LOG, SPRUCE_PLANK, HAY = solid(17, 1), solid(5, 1), solid(170)
STONE_SLAB = solid(44, 0)
LAID_SPRUCE = {"kind": "laidLog", "id": 17, "data": 1}


def cell_(seed, size, palette, rise=0):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": max(1, size // 3),
            "warp": max(1, size // 4), "palette": palette, "rise": rise}


def stack(bands, ending="handOver"):
    return {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}


def layered(bands, axis="depth", ending="handOver"):
    return {"kind": "layered", "axis": axis, "stack": stack(bands, ending)}


# The pavement, at three angles. A limestone pavement is bare where it is flat — the soil washed into
# the grikes long ago — so the flat band is rock and the green is stated as patches, not sampled.
CLINTS = cell_(11, 9, [STONE, DIORITE])            # the flat slabs: two blocks, a texture
SHELF  = cell_(12, 6, [COBBLE, GRAVEL])            # broken ground on a shoulder
FACE   = cell_(13, 8, [STONE, ANDESITE], rise=4)   # the exposed riser: a rise is what
                                                   # gives a face grain instead of stripes (PT4)
BODY   = cell_(14, 9, [STONE, POL_DIORITE], rise=5)  # the rock nobody sees until a face is cut

FELL_SURFACE = layered([
    (12, layered([(1, CLINTS), (2, COBBLE)])),      # under 12 degrees: pavement
    (16, layered([(1, SHELF), (2, GRAVEL)])),       # 12-28: broken shoulder
    (62, FACE),                                     # over 28: bare rock
], axis="slope")

themes = {
    "fell": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": CHISELLED},
        "surface": {"enabled": True, "depth": 4, "material": FELL_SURFACE},
        "wall":    FACE, "wallEnabled": True,
        "fill":    BODY,
    },
    # the sheltered shelves: the only green on the board, and it is stated as patches
    "turf": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": COARSE},
        "surface": {"enabled": True, "depth": 4,
                    "material": layered([(1, cell_(15, 8, [GRASS, COARSE])), (3, DIRT)])},
        "wall":    FACE, "wallEnabled": True,
        "fill":    BODY,
    },
    # scree at the foot of the scar: broken rock, and it is stone
    "scree": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": ANDESITE},
        "surface": {"enabled": True, "depth": 3,
                    "material": layered([(1, cell_(16, 5, [COBBLE, ANDESITE])), (2, GRAVEL)])},
        "wall":    FACE, "wallEnabled": True,
        "fill":    BODY,
    },
}

# ── the relief ───────────────────────────────────────────────────────────────────────────────────
# An area mark's ring is a SHAPE, and a rectangle looks like one: four-vertex marks build mesas with
# square sides that read as squares in the heightmap. Every pad here is a lobed ring.
import math


def lobe(cx, cz, radii, tilt=0.0):
    n = len(radii)
    return [[round(cx + r * math.cos(tilt + 2 * math.pi * i / n), 1),
             round(cz + r * math.sin(tilt + 2 * math.pi * i / n), 1)]
            for i, r in enumerate(radii)]


relief = {
    "team": {
        "base": FELL, "reach": 0, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 1, "scale": 16, "seed": 7},
        "marks": [
            # the shore: flat right to the edge, because a bridge has to land on something level
            {"id": "apron", "kind": "area", "h": SHORE, "bevel": 3,
             "ring": lobe(0, 18, [41, 35, 39, 34, 41, 35, 39, 34], 0.2)},
            # the scoured slab the Cairn stands on: open ground, and the one thing on the board a
            # player can see across
            {"id": "slab", "kind": "area", "h": SLAB, "bevel": 4,
             "ring": lobe(20, 54, [18, 15, 17, 14, 19, 15, 16, 14], 0.4)},
            # the spawn's ground, a little above the fell and graded into it
            {"id": "bield-floor", "kind": "area", "h": BIELD, "bevel": 4,
             "ring": lobe(0, 92, [26, 22, 25, 20, 26, 22, 25, 20], 0.1)},
            # the dry gill: limestone swallows its own water, so this is a groove in the rock rather
            # than a beck. It is the approach from BELOW — a player walks up it out of sight.
            {"id": "gill", "kind": "line", "r": 8, "tread": 2,
             "points": [[-36, 74], [-30, 60], [-24, 44], [-18, 30]],
             "h": [26, 24, 22, 21]},
            # the scar: an escarpment on the east flank, high on the +z (spawn) side because the lip
            # is traced with x increasing. Five blocks over three is a drop, not a path: the approach
            # from ABOVE, and one way.
            {"id": "scar", "kind": "scarp", "points": [[16, 72], [27, 69], [38, 68]],
             "high": BROW, "low": SLAB - 1, "face": 3, "band": 7},
        ],
        "pushes": [
            # the hag: the knoll the birches stand on. The two gradients agree — 6/9 up the skirt and
            # 6/9 to the crown — so it is a hill rather than a wall with a hill on top (`RL6`).
            {"id": "hag", "ring": lobe(-26, 62, [11, 9, 10, 8, 11, 9, 10, 8], 0.3),
             "amount": 6, "falloff": 9, "crown": 6, "roughness": 1.5, "seed": 3},
            # a low rigg on the east shore, so the pavement is not one plane down to the water
            {"id": "rigg", "ring": lobe(30, 30, [9, 7, 8, 7, 9, 7, 8, 7], 0.6),
             "amount": 4, "falloff": 6, "crown": 4, "roughness": 1, "seed": 4},
        ],
    }
}

# ── what the plan cannot state ───────────────────────────────────────────────────────────────────
STEP_MATERIAL = cell_(17, 4, [STONEBRICK, COBBLE, ANDESITE], rise=2)


def flight(id_, ring, low, high):
    """A stair is one polygon with a height per vertex, run at least twice the rise, sheer-sided and
    kept clear. It is made, so it takes a material rather than a theme, and it is the same stone the
    whole way up whatever it joins."""
    return {"id": id_, "type": "polygon", "operation": "add", "override": True, "keepClear": True,
            "group": "team", "floor": 0, "base_height": high, "material": STEP_MATERIAL,
            "height_mode": "level", "skirt": 0,
            "vertices": [[x, z] for x, z in ring],
            "anchor_heights": [low, low, high, high]}


def patch(id_, ring, theme):
    """A paint patch on solved ground. It has to declare a height_mode or ShapeScopeOwners never makes
    it a candidate and it paints nothing in silence; a raise of 0 sits flush at the median ground."""
    return {"id": id_, "type": "polygon", "operation": "add", "group": "team",
            "height_mode": "raise", "base_height": 0, "skirt": 0,
            "vertices": [[x, z] for x, z in ring], "theme": theme}


add_shapes = [
    # the one way up the scar: a flight cut into the re-entrant at its west end, 14 blocks of run for
    # 5 courses. Without it the scar is a one-way drop from the spawn side and the east flank is only
    # ever left, never entered.
    flight("scar-steps", [(6, 66), (14, 66), (14, 80), (6, 80)], SLAB - 1, BROW),
    # turf: the shelves that hold soil. Every one of them is somewhere the rock lies flat and out of
    # the weather, which is the answer to "why here".
    patch("turf-hag",  lobe(-26, 62, [14, 11, 13, 10, 14, 11, 13, 10], 0.3), "turf"),
    patch("turf-gill", [(-34, 70), (-26, 62), (-20, 46), (-14, 32), (-22, 30), (-28, 46), (-36, 62)],
          "turf"),
    patch("turf-rigg", lobe(30, 30, [13, 10, 12, 9, 13, 10, 12, 9], 0.2), "turf"),
    # scree: the broken rock the scar sheds, in a tongue at its foot
    patch("scree-scar", [(14, 64), (28, 61), (39, 60), (39, 54), (26, 55), (16, 58)], "scree"),
]

# ── the barn ─────────────────────────────────────────────────────────────────────────────────────
# Three families named before painting: the ground is PALE GREY rock, so what is built is dry-stone
# walling under a slate roof with spruce posts, and the accent is STRAW — the one warm thing on the
# board, and it appears twice rather than once.
def barn_style(storeys):
    return {
        "foundation": {"plate": {"stack": stack([(1, COBBLE)], "repeat"), "extent": 1},
                       "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                                   "inlayInset": 2, "isPlain": True},
                       "footing": None},
        "roof": {"form": "gable", "pitch": 2, "slab": 44, "slabData": 5, "overhang": 1,
                 "ridgeCap": True, "hole": False,
                 "body": STONEBRICK, "verge": LAID_SPRUCE, "gable": SPRUCE_PLANK,
                 "gableWindows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0,
                                  "data": 0, "sill": 1, "width": 1, "height": 1, "spacing": 3}},
        "wall": {"stack": stack([(1, COBBLE)], "repeat"), "extent": 5},
        "post": SPRUCE_LOG,
        "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                    "sill": 2, "width": 1, "height": 2, "spacing": 4},
        "storeys": storeys,
        "porch": None, "front": None,
        "beams": {"block": 17, "data": 1, "reach": 1, "any": True},
        "doorway": {"door": "air", "head": {"form": "none", "block": 53, "fill": "upperSlab",
                                            "fillBlock": 126, "fillData": 1}, "width": 2, "height": 3},
    }


BYRE_STOREY = {
    "clear": 4, "post": SPRUCE_LOG, "deck": None,
    "wall": {"stack": stack([(3, cell_(18, 4, [COBBLE, STONE])), (1, HAY)], "repeat"), "extent": 4},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 2, "width": 1, "height": 2, "spacing": 4},
}
LOFT_STOREY = {
    "clear": 3, "post": SPRUCE_LOG, "deck": None,
    "wall": {"stack": stack([(2, SPRUCE_PLANK), (1, LAID_SPRUCE)], "repeat"), "extent": 3},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 1, "width": 1, "height": 1, "spacing": 4},
}
barn = barn_style([BYRE_STOREY, LOFT_STOREY])
laithe = barn_style([dict(BYRE_STOREY, clear=4)])

# ── what stands on it ────────────────────────────────────────────────────────────────────────────
# The birches are copied bodies out of the studio's own library, so a hag is the trees somebody grew
# rather than the vanilla stamp. Row 13 of the tree showcase is the birch row.
BIRCHES = ["tree-showcase-r13-%d" % n for n in (1, 3, 5, 7, 9)]


def library_tree(name):
    with urllib.request.urlopen(f"{API}/api/tree-styles") as handle:
        index = {row["name"]: row["id"] for row in json.load(handle)}
    with urllib.request.urlopen(f"{API}/api/tree-styles/{index[name]}") as handle:
        style = json.load(handle)
    return {"kind": "tree", "form": "copied", "body": style["body"]}


def path(id_, points, radius, pave, style="solid", coverage=1.0, seed=0, claims=True):
    return {"id": id_, "kind": "stroke", "seed": seed, "radius": radius, "style": style,
            "coverage": coverage, "claimsGround": claims, "pave": pave, "points": points}


# a path is three blocks a reader cannot quite tell apart, and on hard ground that is gravel,
# andesite and cobblestone
WAY = cell_(19, 5, [GRAVEL, ANDESITE, COBBLE])

BOULDER = {"kind": "boulder", "form": "outcrop", "size": 4, "mossy": False,
           "rock": cell_(20, 4, [STONE, COBBLE, ANDESITE], rise=2)}

props = [
    # the ways, drawn before the scenery: the spine from the door to the slab and on to the shore,
    # and a second road down the west flank so the board has two journeys rather than one. A path
    # is solid and three blocks a reader cannot quite tell apart.
    path("way", [[0, 86], [8, 76], [16, 66], [20, 58]], 2, WAY, seed=41),
    path("way-shore", [[20, 44], [12, 36], [6, 26], [2, 20]], 2, WAY, seed=42),
    path("way-west", [[-6, 86], [-12, 74], [-15, 58], [-18, 42], [-20, 28]], 2, WAY, seed=43),
    # the spur to the barn's door: a road ends at a door or it says the board was assembled
    path("way-barn", [[9, 31], [14, 30]], 2, WAY, seed=44),
    # the barn: a byre with a loft over it and a low cross wing, at the head of the shore road on
    # the south-east, where the rigg gives it a shelf to stand on. It is off the spawn door's own
    # approach (DR-KEEP), out of the Cairn's ten-block keep-out (OB19), and out of the wood.
    {"id": "barn", "kind": "house", "seed": 601, "front": "negX", "style": "barn",
     "wings": [{"corners": [[22, 24], [33, 34]], "spec": {"ridge": "alongZ"}},
               {"corners": [[16, 26], [21, 31]], "spec": {"storeysHigh": 1, "ridge": "alongX"}}]},
    # ground cover: ONE shape, the whole board, and two numbers kept low. The patchiness is the
    # density field's and it is better at it than a hand-drawn polygon.
    {"id": "sward", "kind": "flora", "seed": 900,
     "points": [[-38, 12], [38, 12], [38, 98], [-38, 98]],
     "spec": {"coverage": 0.22, "scale": 26, "octaves": 3, "fernShare": 0.3,
              "flowerShare": 0.06, "flowerScale": 14, "tallShare": 0.05}},
]
# the hag: seven birches on the knoll and its shoulders, thrown rather than latticed and ten apart —
# a copied body is wider than a template, and `DR-CLAIM` is footprint overlap rather than a standoff.
# No road runs through a wood.
for i, (x, z) in enumerate([(-36, 40), (-34, 58), (-36, 76), (-30, 68), (-24, 46),
                            (-26, 30)]):
    props.append({"id": f"birk-{i}", "kind": "tree", "seed": 700 + i, "x": x, "z": z,
                  "style": BIRCHES[i % len(BIRCHES)]})
# erratics: stone, cobblestone and andesite and nothing else, each standing where the pavement gives
# it a reason — along the slab's rim, at the gill's mouth, and on the open shore
for i, (x, z) in enumerate([(-6, 40), (34, 60), (-12, 22), (-8, 62), (-34, 22), (-30, 52)]):
    props.append(dict(BOULDER, id=f"erratic-{i}", kind="boulder", seed=800 + i, x=x, z=z,
                      size=4 if i % 2 == 0 else 3))

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-13",
    "themes": themes,
    "mapTheme": "fell",
    # Extreme hills tints grass #8ab689 — a grey-green that agrees with pale limestone, where Plains
    # would put a summer meadow through it
    "biome": {"kind": "solid", "id": 3},
    "editShapes": {"bield-24": [
        # the frontline, west to east: headland, bay, headland, bay, headland
        {"after": 0, "x": -32, "z": 12}, {"after": 1, "x": -24, "z": 18},
        {"after": 2, "x": -15, "z": 14}, {"after": 3, "x": -6, "z": 10},
        {"after": 4, "x": 4, "z": 12},   {"after": 5, "x": 13, "z": 17},
        {"after": 6, "x": 23, "z": 18},  {"after": 7, "x": 32, "z": 12},
        # the east coast
        {"after": 9, "x": 38, "z": 26},  {"after": 10, "x": 35, "z": 44},
        {"after": 11, "x": 39, "z": 62}, {"after": 12, "x": 36, "z": 76},
        # and the west
        {"after": 15, "x": -37, "z": 70}, {"after": 16, "x": -39, "z": 52},
        {"after": 17, "x": -36, "z": 34}, {"after": 18, "x": -38, "z": 20},
    ]},
    "relief": relief,
    "addShapes": add_shapes,
    "roomStyles": {"spawn": laithe},
    "dressing": {"styles": dict({name: library_tree(name) for name in BIRCHES},
                                barn={"kind": "house", "shell": barn}),
                 "props": props},
}

json.dump(plan,   open(os.path.join(HERE, f"{SLUG}.plan.json"),   "w"), indent=1)
json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")
