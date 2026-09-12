#!/usr/bin/env python3
"""Blackden Sough — the plan and the finish.

A gritstone edge with a drainage sough driven under it. An attacker who bridges the gap lands on the
shelf and has three ways at the Blackden Stone: up the one nick the edge leaves open, over the edge
on placed blocks, or through the sough — six courses of headroom in the dark, coming out on the
dale floor behind the edge.

The board is written bottom-up, because a stacked one has to be:

    y  0..17   the sough's floor, and the rock either side of it   (layer `under`, below the ground)
    y 18..23   the passage's own air — six courses of headroom
    y 24..     the moor: one shape, its shape entirely in the relief

The rock is stated as ADDS banded round the corridor and never as a subtract — a subtract is a claim
about the whole stack, and the moor over it would fill what the storey below called void (SK13). The
bands are clipped out of the moor's OWN drawn outline, so nothing of the storey below stands out past
the coast as a ledge over the void.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-blackden-sough"

# ── the board ────────────────────────────────────────────────────────────────────────────────────
CELL = 5
MOOR = (-35, 15, 35, 100)          # the authored half's ground, in blocks
STELL = (-15, 100, 15, 120)        # the spawn piece
GROUND_FLOOR = 24                  # the moor's underside, which is the sough's ceiling
ROCK_TOP = 24                      # the rock spans [0, 24): top block y23, flush under the moor
SOUGH_TOP = 18                     # the corridor floor spans [0, 18): top block y17, walked at y18

SOUGH_X = (-24, -18)               # six columns
SOUGH_Z = (20, 72)                 # head of the north flight to head of the south one
STAIR_N = (34, 20)                 # foot at the portal, head out on the shelf
STAIR_S = (58, 72)                 # foot at the portal, head out on the dale

SHELF, CREST, DALE = 28, 40, 32     # relief heights; a top block is h - 1

# ── authoring geometry ───────────────────────────────────────────────────────────────────────────
# The compiled ring is the plan's rectangles walked as a staircase; the coast is drawn by moving into
# it one point at a time (POST .../vertices), which is the one edit that leaves every OTHER point
# exactly where the plan put it. The rock under the moor has to wear the same outline or it stands
# out past the coast as a ledge over the void, so the outline is stated ONCE here and the storey
# below is clipped out of it. Every coast point stays NORTH of the sough's own z-band, so each clip
# cuts a band once on each side and never walks the clip line twice.
COMPILED_RING = [(-35, 15), (35, 15), (35, 100), (15, 100), (15, 120), (-15, 120), (-15, 100), (-35, 100)]

COAST = [
    (-35, 15),                                            # the compile's own NW corner
    (-26, 19), (-13, 13), (2, 19), (16, 12), (28, 17),    # the coast, drawn
    (35, 15),                                             # its NE corner
    (30, 42), (32, 74),                                   # the east flank, pulled in
    (35, 100), (15, 100), (15, 120), (-15, 120), (-15, 100), (-35, 100),
    (-31, 76), (-33, 44),                                 # the west flank
]


def vertex_ops(compiled, drawn):
    """The ordered inserts that take `compiled` to `drawn`, in the indices each one sees."""
    ops, pos, nxt = [], 0, 1
    assert tuple(drawn[0]) == tuple(compiled[0])
    for point in drawn[1:]:
        if nxt < len(compiled) and tuple(point) == tuple(compiled[nxt]):
            nxt += 1
        else:
            ops.append({"after": pos, "x": point[0], "z": point[1]})
        pos += 1
    assert nxt == len(compiled), "every compiled vertex must survive, in order"
    return ops


def clip(poly, axis, bound, keep_above):
    """Sutherland-Hodgman against one axis-aligned half-plane, exact on the intersection."""
    def f(p):
        return (p[axis] - bound) if keep_above else (bound - p[axis])

    out = []
    for i, a in enumerate(poly):
        b = poly[(i + 1) % len(poly)]
        fa, fb = f(a), f(b)
        if fa >= 0:
            out.append(a)
        if (fa >= 0) != (fb >= 0):
            t = fa / (fa - fb)
            out.append((round(a[0] + (b[0] - a[0]) * t), round(a[1] + (b[1] - a[1]) * t)))
    return out


def band(poly, x0=None, x1=None, z0=None, z1=None):
    """The part of `poly` inside the stated bounds, or None where nothing is left."""
    for bound, axis, above in ((x0, 0, True), (x1, 0, False), (z0, 1, True), (z1, 1, False)):
        if bound is not None:
            poly = clip(poly, axis, bound, above)
            if not poly:
                return None
    dedup = []
    for point in poly:
        if not dedup or point != dedup[-1]:
            dedup.append(point)
    if len(dedup) > 1 and dedup[0] == dedup[-1]:
        dedup.pop()
    return dedup if len(dedup) >= 3 else None


def rect(id_, x0, z0, x1, z1, **kw):
    return dict(id=id_, type="rectangle", operation="add", min_x=x0, min_z=z0, max_x=x1, max_z=z1, **kw)


def poly(id_, ring, **kw):
    return dict(id=id_, type="polygon", operation="add", vertices=[[x, z] for x, z in ring], **kw)


# ── the plan ─────────────────────────────────────────────────────────────────────────────────────
# Two pieces at one surface, so they fuse into ONE terrain shape and the board's shape is the
# relief's rather than the piece list's. The Stone sits at (12, 62): fifty blocks from its own door
# and a hundred and seventy-four from the enemy's, which is GO1's band with the walk's climb to
# spare, and twelve blocks off the centre line so the dale is crossed rather than run down.
plan = {
    "plan": 2,
    "meta": {"name": "Blackden Sough"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 12, "surface": 28, "observerY": 62},
    "pieces": [
        {"id": "moor",  "role": "piece", "rect": [-7, 3, 14, 17], "surface": 28},
        {"id": "stell", "role": "spawn", "rect": [-3, 20, 6, 4],  "surface": 28},
    ],
    "zones": [{"id": "crossing", "rect": [-7, -3, 14, 6], "kind": "build"}],
    "placements": {
        # the piece is the protection region; the footprint is the hall raised on it (ST9 caps it at 20x20)
        "spawns": [{"id": "spawn-1", "piece": "stell", "at": [15, 12], "facing": "front",
                    "footprint": [8, 5, 14, 10]}],
        "iron":   [{"id": "iron-1", "piece": "stell", "at": [4, 9]},
                   {"id": "iron-2", "piece": "stell", "at": [26, 9]}],
        "destroyables": [{"id": "destroyable-1", "piece": "moor", "at": [47, 47],
                          "style": "pillar-2", "materials": "obsidian", "float": 2,
                          "name": "Blackden Stone"}],
        "cores": [], "wools": [],
    },
    "walls": [], "boxes": [],
}

# ── materials ────────────────────────────────────────────────────────────────────────────────────
def solid(i, d=0):  return {"kind": "solid", "id": i, "data": d}

GRASS, DIRT, COARSE = solid(2), solid(3), solid(3, 1)
STONE, ANDESITE, COBBLE = solid(1), solid(1, 5), solid(4)
STONEBRICK, GRAVEL, SPRUCE = solid(98), solid(13), solid(5, 1)

def cell_(seed, size, palette, rise=0, jitter=2, warp=2):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp,
            "palette": palette, "rise": rise}

def stack(bands, ending="handOver"):
    return {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}

def layered(bands, axis="depth", beyond=None, ending="handOver"):
    out = {"kind": "layered", "axis": axis, "stack": stack(bands, ending)}
    if beyond: out["beyond"] = beyond
    return out

# The body of the hill: a blob and not a stripe, so the cells are wider than they are tall.
GRIT_BODY = cell_(41, 9, [STONE, ANDESITE, STONE, COBBLE], rise=5)
# What a cut face or a scarp shows.
GRIT_FACE = cell_(42, 7, [STONE, ANDESITE, COBBLE], rise=3)

# The ground finished by its ANGLE rather than its height: one stack does the moor top, the shoulder
# and the face of the same edge, and each band carries a depth stack of its own so turf stays one
# course over its soil (PT1). Where the bands cut is read off GET .../incline.
# GET .../incline reads 43% under 10 degrees, 16% in the teens, 22% in the twenties and 9.6% at
# forty or steeper, so the cuts at 28 and 42 put three quarters under turf, a sixth on the worn
# shoulder and the last tenth on bare rock.
MOOR_SURFACE = layered([
    (28, layered([(1, GRASS), (2, DIRT), (1, COARSE)])),       # under 28 degrees: turf over soil
    (14, layered([(1, COARSE), (2, DIRT)])),                   # 28-42: the worn shoulder
    (48, GRIT_FACE),                                           # over 42: bare gritstone
], axis="slope")

themes = {
    "moor": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void",                       # a rim belongs on a made edge, and the coast is one
        "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": GRIT_FACE},
        "surface": {"enabled": True, "depth": 4, "material": MOOR_SURFACE},
        "wall":    GRIT_FACE,
        "wallEnabled": True,
        "fill":    GRIT_BODY,                     # never plain stone: the moor paints over the rock otherwise
    },
    # The rock the sough is driven through. Its WALL is what a player standing in the passage sees.
    "grit": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": False, "depth": 1, "material": GRIT_FACE},
        "surface": {"enabled": True, "depth": 2, "material": GRIT_FACE},
        "wall":    GRIT_FACE,
        "wallEnabled": True,
        "fill":    GRIT_BODY,
    },
    # The floor of the level: three close greys, which is what a stony way is made of.
    "sole": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": False, "depth": 1, "material": GRIT_FACE},
        "surface": {"enabled": True, "depth": 2, "material": cell_(51, 5, [GRAVEL, ANDESITE, COBBLE])},
        "wall":    GRIT_FACE,
        "wallEnabled": True,
        "fill":    GRIT_BODY,
    },
}

# A flight is MADE. It is one material the whole way up rather than a theme of its own, because a
# theme is a place and a stair is a thing (SK24 refuses a shape that states both).
STEP_MATERIAL = cell_(61, 4, [STONEBRICK, ANDESITE, COBBLE], rise=2)
WAY_MATERIAL = cell_(62, 5, [GRAVEL, ANDESITE, COBBLE])

# ── the hall the spawn stamps ────────────────────────────────────────────────────────────────────
# A shipped preset forked into this board's three families: the ground is turf over grey stone, so
# the building is NOT grey stone — it is timber, on a cobble plinth, under a brick roof. Spruce log
# posts at the corners and spruce beams over the storey joint, with a course of laid spruce log in
# the upper wall so the beams have something to be the end of. No footing: the plinth is the plate.
SPRUCE_LOG = {"kind": "solid", "id": 17, "data": 1}
LAID_SPRUCE = {"kind": "laidLog", "id": 17, "data": 1}
hall = {
    "foundation": {
        "plate": {"stack": stack([(1, COBBLE)], "repeat"), "extent": 1},
        "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                    "inlayInset": 2, "isPlain": True},
        "footing": None,
    },
    "roof": {"form": "gable", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
             "ridgeCap": True, "hole": False,
             # HS3: a bare log on a verge stands every block on end. A laid one takes the ridge's axis.
             "body": solid(45), "verge": LAID_SPRUCE, "gable": SPRUCE,
             "gableWindows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0,
                              "data": 0, "sill": 1, "width": 1, "height": 1, "spacing": 3}},
    "wall": {"stack": stack([(1, SPRUCE)], "repeat"), "extent": 5},
    "post": SPRUCE_LOG,
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 2, "width": 2, "height": 2, "spacing": 3},
    "storeys": [
        {"clear": 5, "post": SPRUCE_LOG, "deck": None,
         "wall": {"stack": stack([(2, cell_(81, 3, [COBBLE, ANDESITE])), (3, SPRUCE)], "repeat"),
                  "extent": 5},
         "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                     "sill": 2, "width": 2, "height": 2, "spacing": 3}},
        {"clear": 4, "post": SPRUCE_LOG, "deck": None,
         "wall": {"stack": stack([(3, SPRUCE), (1, LAID_SPRUCE)],
                                 "repeat"), "extent": 4},
         "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                     "sill": 1, "width": 1, "height": 2, "spacing": 4}},
    ],
    "porch": None, "front": None,
    "beams": {"block": 17, "data": 1, "reach": 1, "any": True},
    "doorway": {"door": "air", "head": {"form": "none", "block": 53, "fill": "upperSlab",
                                        "fillBlock": 126, "fillData": 1}, "width": 2, "height": 3},
}


# ── the storey under the moor ────────────────────────────────────────────────────────────────────
sx0, sx1 = SOUGH_X
sz0, sz1 = SOUGH_Z

rock_bands = {
    "rk-n": band(COAST, z1=sz0),                        # north of the sough's head
    "rk-s": band(COAST, z0=sz1),                        # south of its tail
    "rk-w": band(COAST, z0=sz0, z1=sz1, x1=sx0),        # west of it
    "rk-e": band(COAST, z0=sz0, z1=sz1, x0=sx1),        # east of it
}
under_shapes = [poly(k, r, floor=0, base_height=ROCK_TOP, theme="grit")
                for k, r in rock_bands.items() if r]
under_shapes.append(rect("sough", sx0, sz0, sx1, sz1, floor=0, base_height=SOUGH_TOP, theme="sole"))

# ── the two flights ──────────────────────────────────────────────────────────────────────────────
# One polygon each, cut into the moor as an override add: the anchors fall a course a block and the
# air over the treads is the shaft. `floor` is the corridor floor's own top, so a flight rests on the
# storey below rather than driving through it (SK10).
def flight(id_, x0, x1, z_foot, z_head, top):
    """The foot sits on the corridor floor; the head arrives flush with the surface it climbs to."""
    rise = top - SOUGH_TOP + 1
    return {"id": id_, "type": "polygon", "operation": "add", "override": True, "keepClear": True,
            "floor": SOUGH_TOP, "base_height": rise, "material": STEP_MATERIAL,
            "height_mode": "level", "skirt": 0,
            "vertices": [[x0, z_foot], [x1, z_foot], [x1, z_head], [x0, z_head]],
            "anchor_heights": [1, 1, rise, rise]}

add_shapes = [
    flight("mouth-n", sx0, sx1, STAIR_N[0], STAIR_N[1], SHELF - 1),   # out onto the shelf at y27
    flight("mouth-s", sx0, sx1, STAIR_S[0], STAIR_S[1], DALE - 1),    # out onto the dale at y31
]

# ── the relief ───────────────────────────────────────────────────────────────────────────────────
def area(id_, x0, z0, x1, z1, h, **kw):
    return dict(id=id_, kind="area", h=h, ring=[[x0, z0], [x1, z0], [x1, z1], [x0, z1]], **kw)

def ring(cx, cz, r, n=8):
    import math
    return [[round(cx + r * math.cos(2 * math.pi * i / n)),
             round(cz + r * math.sin(2 * math.pi * i / n))] for i in range(n)]

mx0, mz0, mx1, mz1 = MOOR

relief = {
    "team": {
        "base": 31, "reach": 34, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 2, "scale": 18, "seed": 9},
        "marks": [
            # An AREA pins a flat disc and is right only where flat is the point: the ground a bridge
            # lands on, the pan a sough discharges into, the shelf a goal stands on, the spawn's own
            # floor. Everything else is a POINT at a small radius with the relaxation between them,
            # because a wide radius is a mesa rather than a summit.
            area("shelf", mx0, 13, mx1, 22, SHELF),
            # The edge, as two scarps with an eighteen-block nick left between them. A scarp states
            # the drop outright — one face rather than the stack of two-block treads a steep
            # relaxation builds — and the nick is the one place the relaxation is allowed to ramp.
            {"id": "scarp-w", "kind": "scarp", "points": [[-35, 30], [-9, 31]],
             "high": CREST, "low": SHELF, "face": 3, "band": 4},
            {"id": "scarp-e", "kind": "scarp", "points": [[9, 31], [35, 29]],
             "high": CREST, "low": SHELF, "face": 3, "band": 4},
            {"id": "crest", "kind": "line", "r": 6, "h": CREST,
             "points": [[-35, 45], [0, 47], [35, 44]]},
            # the pan the sough's tail discharges into, which is what the south flight arrives on
            area("tail", -30, 62, -12, 84, DALE, bevel=4),
            # the shelf the Stone stands on
            area("bank", 2, 54, 24, 70, DALE, bevel=4),
            # the spawn's own floor, so the door opens on its own level
            area("apron", -17, 98, 17, 120, DALE),
            # and the dale between them, stated as summits rather than as a table. These are MARKS
            # and not pushes: a push is added to the solved surface, so one laid over a pan lowers
            # the pan, and the flight arriving on it then lands two blocks proud. Marks negotiate.
            {"id": "rig-w",  "kind": "point", "at": [-32, 68], "r": 4, "h": DALE - 2},
            {"id": "rig-e",  "kind": "point", "at": [30, 62],  "r": 5, "h": DALE + 3},
            {"id": "knowe",  "kind": "point", "at": [26, 84],  "r": 6, "h": DALE + 6},
            {"id": "slack",  "kind": "point", "at": [-4, 88],  "r": 5, "h": DALE - 3},
            {"id": "rig-n",  "kind": "point", "at": [-32, 96], "r": 5, "h": DALE},
            {"id": "howe",   "kind": "point", "at": [10, 100], "r": 5, "h": DALE + 2},
        ],
        "pushes": [],
    }
}

# ── what stands on it ────────────────────────────────────────────────────────────────────────────
# Three placement ideas and no more: the edge's own broken rock along the crest, a holt of birch in
# the shelter of the slack, and one way underfoot from the door to the Stone and on to the nick.
# Nothing is scattered: every one of them answers "why here".
trees = json.load(open(os.path.join(HERE, "trees.json")))
tree_styles = {name: {"kind": "tree", "form": "copied", "body": trees[name]["body"]}
               for name in ("birch-2", "birch-5", "birch-9", "holt-3", "holt-5")}

BOULDER = {"kind": "boulder", "form": "outcrop", "size": 4, "mossy": False,
           "rock": cell_(71, 4, [STONE, COBBLE, ANDESITE], rise=2)}
BOULDER_SMALL = dict(BOULDER, form="angular", size=3)

props = [
    # the way: door -> Stone -> the nick in the edge. Solid, because a broken track reads as litter.
    {"id": "way-dale", "kind": "stroke", "seed": 21, "radius": 2, "style": "solid",
     "coverage": 1.0, "claimsGround": True, "pave": WAY_MATERIAL,
     "points": [[0, 108], [4, 96], [10, 82], [13, 70], [12, 62]]},
    {"id": "way-nick", "kind": "stroke", "seed": 22, "radius": 2, "style": "solid",
     "coverage": 1.0, "claimsGround": True, "pave": WAY_MATERIAL,
     "points": [[12, 62], [8, 52], [3, 44], [0, 36], [0, 28]]},
]
# the edge's own broken rock: four blocks fallen to the foot of the face, where they are cover for
# whoever is trying to get up it, and two still standing on the crest above.
for i, (x, z) in enumerate([(-30, 25), (-14, 26), (16, 25), (28, 26), (-20, 38), (20, 37)]):
    props.append(dict(BOULDER if i % 2 == 0 else BOULDER_SMALL,
                      id=f"edge-rock-{i}", kind="boulder", seed=300 + i, x=x, z=z))
# the holt: birch in the slack, well clear of the Stone's own ground
# A tree claims ground with its crown, so two stand ceil((ha+hb)/4.7) apart or the later one is
# declined; and every image of the orbit is judged, which is what puts the holt clear of z 100.
for i, (x, z, style) in enumerate([(-27, 80, "birch-2"), (-16, 77, "holt-3"), (-28, 91, "holt-5"),
                                   (-17, 88, "birch-5"), (-10, 78, "birch-9")]):
    props.append({"id": f"holt-{i}", "kind": "tree", "seed": 400 + i, "x": x, "z": z, "style": style})

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-12",
    "themes": themes,
    "mapTheme": "moor",
    "biome": {"kind": "solid", "id": 3},          # extreme hills: the grey-green a gritstone moor wears
    "shapePropsById": {"moor-28": {"floor": GROUND_FLOOR}},
    "editShapes": {"moor-28": vertex_ops(COMPILED_RING, COAST)},
    "relief": relief,
    "addLayers": [{"id": "under", "name": "The Sough", "base_y": 0, "below": True,
                   "shapes": under_shapes,
                   "groups": [{"id": "under", "mirrors": True,
                               "shapeIds": [s["id"] for s in under_shapes]}]}],
    "addShapes": add_shapes,
    "roomStyles": {"spawn": hall},
    "dressing": {"styles": tree_styles, "props": props},
}

json.dump(plan,   open(os.path.join(HERE, f"{SLUG}.plan.json"),   "w"), indent=1)
json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")
