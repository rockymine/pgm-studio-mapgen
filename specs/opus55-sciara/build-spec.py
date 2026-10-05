"""Sciara — two hill villages on the flank of a volcano, each defending a core on its threshing floor.

Writes `opus55-sciara.plan.json` and `opus55-sciara.refinement.json`. Every coordinate is red's unit, on the
z < 0 half; the rot_180 symmetry fans the plan and the `team` group to blue.

Heights a player stands on, red's half:
  village yard and piazza   34   made ground, excluded from the relief
  the aia (core terrace)    31   made ground, the core on a paved threshing circle in the middle of it
  upper olive terrace       28   made ground, west of the aia
  lower olive terrace       25   made ground, in front of the upper one
  the open slope            27 → 22   relief, pinned at the aia's front and at the ravine lip
  the sciara                a push down the east flank, its crest a little over the core's casing
  the cava                  a sunk quarry pit in front of the aia, six under the slope
"""
import json, os

SLUG = "opus55-sciara"
HERE = os.path.dirname(os.path.abspath(__file__))


def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data} if data else {"kind": "solid", "id": block}


GRASS, DIRT, STONE, COBBLE, GRAVEL = 2, 3, 1, 4, 13
CLAY, HARD_CLAY, COAL_BLOCK, BRICK = 159, 172, 173, 45

# --- materials -------------------------------------------------------------------------------------------

def over_dirt(top):
    """One course of `top` over two of dirt, read down from the surface."""
    return {"kind": "layered", "axis": "depth", "stack": {"ending": "repeat", "bands": [
        {"material": top, "thickness": 1}, {"material": solid(DIRT), "thickness": 2}]}}


LAVA_ROCK = {"kind": "cell", "seed": 11, "cellSize": 2, "jitter": 1, "warp": 1,
             "palette": [solid(CLAY, 15), solid(CLAY, 15), solid(CLAY, 7), solid(COAL_BLOCK)], "rise": 2}

MATERIALS = {
    # the lava stone: black and grey stained clay with coal block as its grain — the rock the whole
    # mountain is made of, so it is the wall, the fill and the steepest band of every theme
    "lava-rock": LAVA_ROCK,
    "worn": {"kind": "cell", "seed": 5, "cellSize": 2, "jitter": 1, "warp": 1,
             "palette": [solid(DIRT), solid(DIRT, 1)]},
    # the sciara's own top: the lava stone as ground, grey clay patches at one end, coal at the other.
    # A named material is stated inline where another named material holds it: the store keeps a `use`
    # nested inside `materials` unresolved, and every read of the board then refuses it.
    "sciara-top": {"kind": "noise", "seed": 23, "scale": 3, "octaves": 2, "stops": [
        solid(CLAY, 7), LAVA_ROCK, LAVA_ROCK, solid(COAL_BLOCK)]},
    # the village floor: granite, polished granite, hardened clay and brick, a quarter each
    "paving": {"kind": "cell", "seed": 3, "cellSize": 3, "jitter": 1, "warp": 1,
               "palette": [solid(STONE, 1), solid(STONE, 2), solid(HARD_CLAY), solid(BRICK)]},
}


def theme(surface, surface_depth=1, rim_top=None):
    """A theme whose wall, fill and steepest ground are the lava stone. Where `rim_top` is stated the rim
    caps every edge with it one course deep, so a terrace face is lava stone up to its top course rather
    than the surface's soil."""
    rim = ({"material": rim_top, "depth": 1} if rim_top
           else {"material": {"use": "lava-rock"}, "enabled": False})
    return {"rim": rim,
            "surface": {"material": surface, "depth": surface_depth},
            "wall": {"use": "lava-rock"},
            "fill": {"use": "lava-rock"}}


THEMES = {
    # the countryside: savanna grass, worn earth where it leans, lava stone where it stands up
    "campagna": theme({"kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
        {"material": over_dirt(solid(GRASS)), "thickness": 34},
        {"material": over_dirt({"use": "worn"}), "thickness": 14},
        {"material": {"use": "lava-rock"}, "thickness": 42}]}}, 3, solid(GRASS)),
    "sciara": theme({"use": "sciara-top"}, 2),
    "borgo": theme({"use": "paving"}, 2),
}

# --- the plan --------------------------------------------------------------------------------------------

PLAN = {
    "plan": 2,
    "meta": {"name": "Sciara"},
    "globals": {"cell": 4, "symmetry": "rot_180", "maxPlayers": 20, "surface": 22,
                # over the build ceiling (y49), so the platform is no stepping stone in the ravine
                "observerY": 60},
    "pieces": [
        {"id": "spawn", "role": "spawn", "rect": [-5, -29, 6, 5], "surface": 34},
        {"id": "back-w", "rect": [-12, -29, 7, 5], "surface": 34},
        {"id": "back-e", "rect": [1, -29, 11, 5], "surface": 34},
        {"id": "flank", "rect": [-12, -24, 24, 21], "surface": 22},
        # the lane behind the village, so its houses keep a passage to the coast
        {"id": "back-lane", "rect": [-12, -31, 24, 2], "surface": 34},
    ],
    "zones": [{"id": "ravine", "rect": [-12, -3, 24, 3]}],
    "placements": {
        # the hall and its marker as POST /plan/room answers them for a 16 × 12 building
        "spawns": [{"id": "spawn-0", "piece": "spawn", "at": [11, 10], "facing": "back",
                    "footprint": [3, 4, 16, 12]}],
        "cores": [{"id": "core-0", "piece": "", "at": [10, -64], "name": "Aia Core"}],
    },
}

# --- made ground -----------------------------------------------------------------------------------------

YARD, AIA, UPPER, LOWER = 34, 31, 28, 25
SLOPE_TOP, LIP = 27, 22          # the open slope, pinned at the aia's front and at the ravine lip
VERGE = 31                       # the ground in front of the yard


def made(shape_id, vertices, height, theme_id="campagna"):
    """A terrace: ground that is made rather than grown, out of the relief, meeting it at a face."""
    return {"id": shape_id, "type": "polygon", "operation": "add", "base_height": height,
            "relief_scope": "exclude", "theme": theme_id, "vertices": vertices}


def flight(shape_id, foot, head, low, high):
    """A stair from ground standing at `low` to ground standing at `high`: `foot` and `head` are each a
    pair of corners, and the run between them is twice the rise. Anchors sit half a riser past the first
    and last tread so every tread comes out two blocks deep."""
    return {"id": shape_id, "type": "polygon", "operation": "add", "height_mode": "level", "skirt": 0,
            "keepClear": True, "material": solid(STONE, 6),  # polished andesite treads
            "vertices": [foot[0], foot[1], head[1], head[0]],
            "anchor_heights": [low + 0.5, low + 0.5, high + 0.5, high + 0.5]}


SHAPES = [
    # the piazza the spawn opens onto, notched where the stair down to the aia is set into it
    made("piazza", [[-24, -100], [18, -100], [18, -80], [11, -80], [11, -86], [6, -86], [6, -80],
                    [-24, -80]], YARD, "borgo"),
    flight("stair-piazza", [[6, -80], [11, -80]], [[6, -86], [11, -86]], AIA, YARD),

    # the aia's terrace, notched on its west side for the stair up from the olives and on its front
    # for the stair up from the open slope
    made("aia", [[-6, -80], [26, -80], [26, -48], [23, -48], [23, -56], [18, -56], [18, -48],
                 [-6, -48], [-6, -57], [0, -57], [0, -62], [-6, -62]], AIA),
    {"id": "aia-floor", "type": "circle", "operation": "add", "center_x": 10, "center_z": -64,
     "radius": 8, "base_height": AIA, "relief_scope": "exclude", "theme": "borgo"},
    flight("stair-olive", [[-6, -62], [-6, -57]], [[0, -62], [0, -57]], UPPER, AIA),
    flight("stair-front", [[18, -48], [23, -48]], [[18, -56], [23, -56]], SLOPE_TOP, AIA),

    # the two olive terraces, the upper notched for the stair up from the lower, the lower for the stair
    # up from the lip
    made("olive-upper", [[-47, -76], [-6, -76], [-6, -48], [-25, -48], [-25, -54], [-30, -54],
                         [-30, -48], [-47, -48]], UPPER),
    flight("stair-olives", [[-30, -48], [-25, -48]], [[-30, -54], [-25, -54]], LOWER, UPPER),
    made("olive-lower", [[-47, -48], [-6, -48], [-6, -22], [-17, -22], [-17, -28], [-22, -28],
                         [-22, -22], [-47, -22]], LOWER),
    flight("stair-lip", [[-22, -22], [-17, -22]], [[-22, -28], [-17, -28]], LIP, LOWER),

    # down from the yard's west end to the ground in front of it, and on down to the olives
    flight("stair-yard", [[-40, -90], [-35, -90]], [[-40, -96], [-35, -96]], VERGE, YARD),
    flight("stair-grove", [[-40, -76], [-35, -76]], [[-40, -82], [-35, -82]], UPPER, VERGE),

    # paint over relief ground: the sciara down the east flank and the cava pit, each drawn at the
    # landmass's own height so it forms the surface and the relief settles the height
    {"id": "sciara-flow", "type": "polygon", "operation": "add", "base_height": LIP, "theme": "sciara",
     "vertices": [[0, 0], [1, 0], [1, 1]]},
    {"id": "cava-floor", "type": "polygon", "operation": "add", "base_height": LIP, "theme": "sciara",
     "vertices": [[0, 0], [1, 0], [1, 1]]},
]

OUTLINES = {
    "sciara-flow": {"at": [37, -63], "radius": 17, "radiusZ": 37, "points": 36, "lobes": 5,
                    "wobble": 0.18, "phase": 0.7, "turn": -6},
    "cava-floor": {"at": [14, -32], "radius": 8, "radiusZ": 7, "points": 20, "lobes": 3, "wobble": 0.2,
                   "phase": 1.3},
    "tongue": {"at": [37, -63], "radius": 8, "radiusZ": 28, "points": 32, "lobes": 5, "wobble": 0.15,
               "phase": 0.7, "turn": -6},
    "cava": {"at": [14, -32], "radius": 6, "radiusZ": 5, "points": 18, "lobes": 3, "wobble": 0.15,
             "phase": 1.3},
}

RELIEF = {"team": {
    "base": LIP, "reach": 0, "step": 1, "landform": "rolling",
    "grain": {"amplitude": 2, "scale": 32, "seed": 9},
    "marks": [
        {"id": "lip", "kind": "line", "points": [[-56, -17], [-20, -16], [12, -18], [56, -17]],
         "h": LIP, "r": 3},
        {"id": "slope-top", "kind": "line", "points": [[-6, -44], [12, -45], [32, -43]],
         "h": SLOPE_TOP, "r": 2},
        {"id": "verge", "kind": "line", "points": [[-56, -93], [-20, -92], [20, -93], [56, -93]],
         "h": VERGE, "r": 3},
    ],
    "pushes": [
        {"id": "tongue", "ring": [[0, 0], [1, 0], [1, 1]], "amount": 8, "falloff": 10, "crown": 4,
         "roughness": 0.5, "seed": 3},
        {"id": "cava", "ring": [[0, 0], [1, 0], [1, 1]], "amount": -6, "falloff": 3, "crown": 0,
         "roughness": 0.3, "seed": 4},
    ],
}}

# --- the campanile --------------------------------------------------------------------------------------

QUARTZ, QUARTZ_PILLAR = (155, 0), (155, 2)


def block_rect(shape_id, x0, z0, x1, z1, floor, height, block):
    return {"id": shape_id, "type": "rectangle", "operation": "add", "keepClear": True,
            "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1, "floor": floor, "base_height": height,
            "material": solid(*block)}


def campanile(cx, cz, foot):
    """The village's bell tower on the corner of its piazza: a quartz shaft whose four corner posts rise
    past it to frame an open belfry, under a stepped brick cap. Two made layers, because a layer keeps one
    span a column and the belfry's posts and the cap above them are two spans."""
    x0, z0, x1, z1 = cx - 2, cz - 2, cx + 3, cz + 3
    shaft, belfry = 13, 4
    body = [block_rect("campanile-shaft", x0, z0, x1, z1, foot, shaft, QUARTZ)]
    for i, (px, pz) in enumerate([(x0, z0), (x1 - 1, z0), (x0, z1 - 1), (x1 - 1, z1 - 1)]):
        body.append(block_rect(f"campanile-post-{i}", px, pz, px + 1, pz + 1, foot, shaft + belfry,
                               QUARTZ_PILLAR))
    cap_floor = foot + shaft + belfry
    cap = [block_rect(f"campanile-cap-{step}", x0 - 1 + step, z0 - 1 + step, x1 + 1 - step, z1 + 1 - step,
                      cap_floor, step + 1, (BRICK, 0)) for step in range(4)]
    return [{"id": layer_id, "name": name, "base_y": 0, "kind": "made", "part_of": "campanile",
             "shapes": shapes,
             "groups": [{"id": f"{layer_id}-body", "name": name, "mirrors": True,
                         "shapeIds": [shape["id"] for shape in shapes]}]}
            for layer_id, name, shapes in (("campanile-body", "Campanile", body),
                                           ("campanile-cap", "Campanile cap", cap))]


LAYERS = campanile(-29, -104, YARD)

# --- dressing ---------------------------------------------------------------------------------------------

def tree(prop_id, x, z, style):
    return {"id": prop_id, "kind": "tree", "x": x, "z": z, "style": style}


def track(prop_id, points, wander=2):
    """A farm track: three blocks of soft ground a third each, solid, wandering a little between its ends."""
    return {"id": prop_id, "kind": "stroke", "points": points, "radius": 1.5, "style": "solid",
            "claimsGround": True, "wander": wander, "wanderLength": 14, "pave": {"use": "track"}}


MATERIALS["track"] = {"kind": "cell", "seed": 17, "cellSize": 1, "jitter": 0, "warp": 0,
                      "palette": [solid(DIRT), solid(DIRT, 1), solid(5, 1)]}   # spruce planks

DRESSING = {
    "styles": {
        "olive-a": {"library": "olive-3"}, "olive-b": {"library": "olive-7"},
        "olive-c": {"library": "olive-9"}, "olive-young": {"library": "small-olive-2"},
        "casa": {"kind": "house", "library": "brick-roofed-quartz-house"},
        "lava-erratic": {"kind": "boulder", "form": "angular", "size": 3, "rock": {"use": "lava-rock"},
                         "mossy": False},
    },
    "props": [
        # the farm tracks, flight to flight, so every stair has a way to it
        track("track-yard", [[-25, -97], [-31, -98.5], [-37.5, -97.5]], 1),
        track("track-upper", [[-37.5, -75], [-33, -67], [-27.5, -56]]),
        track("track-upper-aia", [[-31, -64], [-20, -63], [-8, -59.5]]),
        track("track-lower", [[-27.5, -47], [-25, -38], [-19.5, -30]]),
        track("track-front", [[20.5, -46], [24, -38], [21, -26], [17, -17]]),
        # the lava the mountain threw, lying where the sciara stopped
        {"id": "erratic-snout", "kind": "boulder", "x": 24, "z": -22, "style": "lava-erratic"},
        {"id": "erratic-lip", "kind": "boulder", "x": -2, "z": -30, "style": "lava-erratic"},
        # the grove: olives planted in rows along the outside of each terrace, none on the brink
        tree("olive-1", -42, -70, "olive-a"), tree("olive-2", -30, -73, "olive-b"),
        tree("olive-3", -20, -69, "olive-c"), tree("olive-4", -41, -59, "olive-b"),
        tree("olive-5", -15, -54, "olive-a"),
        tree("olive-6", -43, -42, "olive-c"), tree("olive-7", -34, -35, "olive-a"),
        tree("olive-8", -12, -38, "olive-b"), tree("olive-9", -44, -31, "olive-young"),
        # two young olives by the houses
        tree("olive-10", -44, -102, "olive-young"), tree("olive-11", 22, -90, "olive-young"),
        # the village: one style, three plots, one of them a storey taller
        {"id": "casa-west", "kind": "house", "style": "casa", "front": "posZ",
         "wings": [{"corners": [[-38, -114], [-28, -108]]}]},
        {"id": "casa-east", "kind": "house", "style": "casa", "front": "posZ",
         "wings": [{"corners": [[12, -114], [22, -107]], "spec": {"storeysHigh": 2}}]},
        {"id": "casa-tongue", "kind": "house", "style": "casa", "front": "negX",
         "wings": [{"corners": [[30, -112], [38, -104]]}]},
        # ground cover over the whole side, low and short so the ground still reads
        {"id": "cover", "kind": "flora", "points": [[-56, -120], [56, -120], [56, -8], [-56, -8]],
         "spec": {"coverage": 0.22, "scale": 9, "octaves": 2, "fernShare": 0.1, "flowerShare": 0.04,
                  "flowerScale": 7, "tallShare": 0.03, "deadBushShare": 0.15}},
    ],
}

REFINEMENT = {
    "materials": MATERIALS,
    "themes": THEMES,
    "mapTheme": "campagna",
    "biome": {"kind": "solid", "id": 35},   # Savanna: grass #bfb755, foliage #aea42a
    "shapePropsById": {"back-e-34": {"relief_scope": "exclude"}},
    "addShapes": SHAPES,
    "addLayers": LAYERS,
    "outlines": OUTLINES,
    "bendShapes": {
        "back-e-22": {"tension": 0.22, "wander": 3, "step": 9, "seed": 5, "side": "out"},
        "back-e-34": {"tension": 0.22, "wander": 2, "step": 9, "seed": 6, "side": "out"},
    },
    "relief": RELIEF,
    "roomStyles": {"spawn": {"library": "brick-roofed-quartz-house"}},
    "dressing": DRESSING,
    "authors": [{"name": "Opus 5.5", "contribution": "authored through the studio's API"}],
    "created": "2026-10-05",
}

json.dump(PLAN, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(REFINEMENT, open(os.path.join(HERE, f"{SLUG}.refinement.json"), "w"), indent=1)
print(f"wrote {SLUG}.plan.json and {SLUG}.refinement.json")
