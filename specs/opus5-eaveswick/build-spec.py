#!/usr/bin/env python3
"""Eaveswick — a CTW board whose frontline has two storeys.

Adapted from the composed board `players=12 symmetry=mirror_z seed=61` (hub `single`,
frontline `bar`, wools `i` + `l`).  That board puts one wool on its own spawn's doorstep
(29 blocks) and walks the other out to 59, a 2.03x spread, and gives the attack a single
road for the whole of both approaches.  Here the spawn is moved to the back centre and the
two wools are hung off the hub's two ends at the same distance from it, and the frontline
is cut down seven blocks into a quay with the hub's own ground carried out over it on a
timber gallery: the defence holds the upper deck, the attack lands on the lower lane, and
the only ways between them are the two flank ramps the deck looks straight down on.

Writes opus5-eaveswick.plan.json and opus5-eaveswick.finish.json beside this file.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SLUG = "opus5-eaveswick"

CELL = 5
QUAY_Y, SHELF_Y, UPLAND_Y = 12, 16, 19
DECK_Y = 18          # the gallery's own course, so a player stands on it at 19 — the hub

# ---------------------------------------------------------------- materials
def s(i, d=0):  return {"kind": "solid", "id": i, "data": d}
GRASS, DIRT, COARSE, PODZOL = s(2), s(3, 0), s(3, 1), s(3, 2)
GRAVEL, STONE, ANDESITE, DIORITE = s(13), s(1, 0), s(1, 5), s(1, 3)
POL_DIORITE, COBBLE, CLAY = s(1, 4), s(4), s(82)
SAND, SANDSTONE, SMOOTH_SAND, CHIS_SAND = s(12), s(24, 0), s(24, 2), s(24, 1)
BRICK, CHISELED = s(98, 0), s(98, 3)
OAK_PLANK, DARK_PLANK, SPRUCE_PLANK = s(5, 0), s(5, 5), s(5, 1)
DARK_LOG, OAK_LOG = s(162, 1), s(17, 0)

def depth(bands, beyond):
    return {"kind": "layered", "axis": "depth",
            "stack": {"ending": "handOver",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]},
            "beyond": beyond}

def runs(bands, beyond):
    return {"kind": "layered", "axis": "depth",
            "stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]},
            "beyond": beyond}

def slope(bands, beyond):
    return {"kind": "layered", "axis": "slope",
            "stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]},
            "beyond": beyond}

def cell(seed, size, palette, jitter=40, warp=6, rise=0):
    p = {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter,
         "warp": warp, "palette": palette}
    if rise: p["rise"] = rise
    return p

def style(name, footing=None):
    st = json.load(open(os.path.join(REPO, "tools", "styles", name + ".json")))
    st.setdefault("foundation", {})["footing"] = footing
    return st

def house_shell(name):
    """A preset forked into a house prop: no beam over a wall with no laid log in it
    (`HS9`) and no roof slab cut from a block the roof body is not (`HS3`)."""
    st = style(name)
    st["beams"] = {"block": -1, "data": 0, "reach": 1, "any": True}
    if isinstance(st.get("roof"), dict):
        st["roof"]["slab"], st["roof"]["slabData"] = -1, 0
    return st

# ---------------------------------------------------------------- themes
# ground family: a pale river terrace — sand, gravel and grey-green turf.
# built family: dark oak timber.  accent: the quay's wet sandstone.
UP_FLAT     = depth([(cell(23, 14, [GRASS, COARSE]), 1), (DIRT, 2), (GRAVEL, 1)], SANDSTONE)
UP_SHOULDER = depth([(COARSE, 1), (GRAVEL, 2)], SANDSTONE)
UP_FACE     = depth([(GRAVEL, 2), (SANDSTONE, 2)], SMOOTH_SAND)

THEME_UPLAND = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void", "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": GRAVEL},
    "surface": {"enabled": True, "depth": 3,
                "material": slope([(UP_FLAT, 18), (UP_SHOULDER, 14), (UP_FACE, 58)], GRAVEL)},
    "wallEnabled": True,
    "wall": runs([(COARSE, 1), (GRAVEL, 2), (SANDSTONE, 3), (SMOOTH_SAND, 2),
                  (DIORITE, 3)], POL_DIORITE),
    "fill": cell(7, 12, [DIORITE, POL_DIORITE], jitter=35, warp=5, rise=5),
}

# the west shelf: the same terrace one step down, grazed rather than built on
THEME_HOLM = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void", "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": GRAVEL},
    "surface": {"enabled": True, "depth": 3,
                "material": slope([(depth([(cell(33, 12, [GRASS, PODZOL]), 1), (DIRT, 2)], GRAVEL), 20),
                                   (depth([(COARSE, 1), (DIRT, 2)], GRAVEL), 14),
                                   (depth([(GRAVEL, 2), (SANDSTONE, 1)], SMOOTH_SAND), 56)], GRAVEL)},
    "wallEnabled": True,
    "wall": runs([(COARSE, 1), (DIRT, 2), (GRAVEL, 3), (SANDSTONE, 3)], POL_DIORITE),
    "fill": cell(9, 11, [DIORITE, POL_DIORITE], jitter=35, warp=5, rise=5),
}

# the quay: the lower lane, and the floor under the gallery.  Its `fill` is what the
# covered half of it is painted with, because one column resolves one band stack and
# ground under a slab falls in the fill bucket.
THEME_QUAY = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void", "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": GRAVEL},
    "surface": {"enabled": True, "depth": 3,
                "material": depth([(cell(43, 9, [SAND, GRAVEL, SANDSTONE]), 1),
                                   (SAND, 1), (SANDSTONE, 2)], SMOOTH_SAND)},
    "wallEnabled": True,
    "wall": runs([(GRAVEL, 1), (SANDSTONE, 2), (SMOOTH_SAND, 2), (CHIS_SAND, 1),
                  (DIORITE, 3)], POL_DIORITE),
    "fill": cell(11, 9, [GRAVEL, SANDSTONE, ANDESITE], jitter=30, warp=4, rise=4),
}

# ---------------------------------------------------------------- the plan
PLAN = {
    "plan": 2,
    "meta": {"name": "Eaveswick",
             "notes": "CTW. A three-tier river terrace: the frontline is a quay seven "
                      "blocks down, and the hub's ground is carried out over it on a "
                      "timber gallery. Two wools, one off each end of the hub."},
    "globals": {"cell": CELL, "symmetry": "mirror_z", "maxPlayers": 12,
                "surface": UPLAND_Y, "observerY": 50},
    "pieces": [
        # the frontline, cut down seven blocks into a quay and widened from twenty blocks
        # to forty so the gallery over it has two flanks rather than one
        {"id": "quay", "role": "piece", "rect": [-4, 2, 8, 6], "surface": QUAY_Y},
        {"id": "hub", "role": "piece", "rect": [-4, 8, 8, 3], "surface": UPLAND_Y},
        {"id": "spawn-t1", "role": "piece", "rect": [-2, 11, 4, 1], "surface": UPLAND_Y},
        {"id": "spawn-room", "role": "spawn", "rect": [-2, 12, 4, 2], "surface": UPLAND_Y},
        # the west wool on a grazed shelf one step down off the hub's west end
        {"id": "wool-a-t1", "role": "piece", "rect": [-8, 8, 4, 2], "surface": SHELF_Y},
        {"id": "wool-a-room", "role": "wool-room", "rect": [-10, 8, 2, 2], "surface": SHELF_Y},
        # the east wool on the upland itself, its lane mouth from the quay barred by an
        # approach wall so the attack has to come the long way round the hub
        {"id": "wool-b-t1", "role": "piece", "rect": [4, 6, 4, 4], "surface": UPLAND_Y},
        {"id": "wool-b-room", "role": "wool-room", "rect": [8, 8, 2, 2], "surface": UPLAND_Y},
    ],
    "zones": [{"id": "mid-band", "rect": [-4, -2, 8, 4], "holes": []}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn-room", "at": [10, 5], "facing": "front",
                    "footprint": [1, 1, 10, 8]}],
        "wools": [{"id": "wool-1", "piece": "wool-a-room", "at": [5, 5]},
                  {"id": "wool-2", "piece": "wool-b-room", "at": [5, 5]}],
        "iron": [{"id": "iron-1", "piece": "spawn-room", "at": [15, 5]}],
        "destroyables": [], "cores": [],
    },
    # the one instrument the composer never emits: `walls` is always []
    "walls": [{"a": "quay", "b": "wool-b-t1"}],
    "boxes": [],
}

# ---------------------------------------------------------------- the relief
# Two flats are stated rather than solved — the quay, because the gallery stands on it and
# the crossing lands on it, and the hub's own apron, because that is where the deck lands.
# Everything behind them rolls.
RELIEF = {"team": {
    "base": UPLAND_Y, "reach": 14, "step": 1, "landform": "rolling",
    "grain": {"amplitude": 1.3, "scale": 15, "seed": 5},
    "marks": [
        {"id": "quay-flat", "kind": "area", "h": QUAY_Y, "bevel": 2,
         "ring": [[-21, 9], [21, 9], [21, 41], [-21, 41]]},
        {"id": "hub-apron", "kind": "area", "h": UPLAND_Y, "bevel": 2,
         "ring": [[-21, 39], [21, 39], [21, 50], [-21, 50]]},
        # the knoll the east wool stands behind, and the rise behind the spawn
        {"id": "knoll", "kind": "point", "at": [32, 44], "r": 5, "h": 23},
        {"id": "back", "kind": "point", "at": [-2, 63], "r": 6, "h": 22},
    ],
    "pushes": [
        {"id": "swell", "ring": [[22, 34], [36, 33], [46, 38], [44, 48], [32, 52], [22, 48]],
         "amount": 3, "falloff": 10, "crown": 1.7, "roughness": 1, "seed": 11},
        {"id": "holm-swell", "ring": [[-44, 42], [-32, 41], [-22, 45], [-30, 52], [-42, 51]],
         "amount": 2, "falloff": 8, "crown": 1.2, "roughness": 1, "seed": 13},
    ],
}}

# ---------------------------------------------------------------- authored shapes
RAMP_MAT = cell(61, 6, [SANDSTONE, SMOOTH_SAND, GRAVEL], jitter=30, warp=4, rise=3)

ADD_SHAPES = [
    # the two flank ramps: the only ways between the quay and the upland, and the deck
    # looks straight down both of them. Fourteen blocks of run for seven of rise.
    {"id": "ramp-w", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": UPLAND_Y, "height_mode": "level", "skirt": 0,
     "keepClear": True, "relief_scope": "exclude", "material": RAMP_MAT, "group": "team",
     "vertices": [[-20, 26], [-14, 26], [-14, 41], [-20, 41]],
     "anchor_heights": [QUAY_Y, QUAY_Y, UPLAND_Y, UPLAND_Y]},
    {"id": "ramp-e", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": UPLAND_Y, "height_mode": "level", "skirt": 0,
     "keepClear": True, "relief_scope": "exclude", "material": RAMP_MAT, "group": "team",
     "vertices": [[14, 26], [20, 26], [20, 41], [14, 41]],
     "anchor_heights": [QUAY_Y, QUAY_Y, UPLAND_Y, UPLAND_Y]},
    # the step off the hub onto the west shelf: three blocks over twelve
    {"id": "ramp-holm", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": UPLAND_Y, "height_mode": "level", "skirt": 0,
     "keepClear": True, "relief_scope": "exclude", "material": RAMP_MAT, "group": "team",
     "vertices": [[-26, 42], [-14, 42], [-14, 48], [-26, 48]],
     "anchor_heights": [SHELF_Y, UPLAND_Y, UPLAND_Y, SHELF_Y]},
    # a drift of bare sand where the quay meets the water's edge: a brush, so it states a
    # height_mode and is a scope candidate at all
    {"id": "strand", "type": "polygon", "operation": "add", "height_mode": "raise",
     "base_height": 0, "skirt": 0, "theme": "quay", "group": "team",
     "vertices": [[-18, 10], [-4, 9], [10, 11], [18, 15], [6, 19], [-8, 18], [-17, 15]]},
]

# ---------------------------------------------------------------- the second storey
# The gallery: the hub's own ground carried out over the quay on posts.  It is a made
# thing, so it is painted over its own span and the lane under it keeps its own paint.
DECK_MAT = cell(53, 8, [DARK_PLANK, SPRUCE_PLANK], jitter=25, warp=4, rise=2)
POST_MAT = cell(57, 5, [DARK_LOG, OAK_LOG], jitter=25, warp=3, rise=3)

def post(pid, x0, z0):
    return {"id": pid, "type": "rectangle", "operation": "add", "keepClear": True,
            "min_x": x0, "max_x": x0 + 2, "min_z": z0, "max_z": z0 + 2,
            "floor": 0, "base_height": DECK_Y - QUAY_Y, "material": POST_MAT}

POSTS = [post(f"post-{i}-{j}", x, z)
         for i, x in enumerate((-12, -5, 3, 10))
         for j, z in enumerate((27, 32, 37))]

DECK = [{"id": "deck", "type": "rectangle", "operation": "add", "keepClear": True,
         "min_x": -14, "max_x": 15, "min_z": 26, "max_z": 41,
         "floor": 0, "base_height": 1, "material": DECK_MAT}]

# the rail along the deck's outer edge, on its own layer because a layer holds one span
# per column and the rail stands on the deck it would otherwise contest
RAIL = [{"id": "rail-s", "type": "rectangle", "operation": "add", "keepClear": True,
         "min_x": -14, "max_x": 15, "min_z": 26, "max_z": 27,
         "floor": 0, "base_height": 1, "material": DARK_LOG}]

ADD_LAYERS = [
    {"id": "posts", "name": "Gallery posts", "base_y": QUAY_Y, "kind": "made",
     "part_of": "gallery", "shapes": POSTS,
     "groups": [{"id": "posts", "name": "posts", "mirrors": True,
                 "shapeIds": [p["id"] for p in POSTS]}]},
    {"id": "deck", "name": "The gallery", "base_y": DECK_Y, "kind": "made",
     "part_of": "gallery", "shapes": DECK,
     "groups": [{"id": "deck", "name": "deck", "mirrors": True, "shapeIds": ["deck"]}]},
    {"id": "rail", "name": "Gallery rail", "base_y": DECK_Y + 1, "kind": "made",
     "part_of": "gallery", "shapes": RAIL,
     "groups": [{"id": "rail", "name": "rail", "mirrors": True, "shapeIds": ["rail-s"]}]},
]

# ---------------------------------------------------------------- dressing
def tree(pid, st, x, z):
    return {"id": pid, "kind": "tree", "style": st, "x": x, "z": z, "layer": "ground"}

def boulder(pid, x, z, r, h, seed):
    return {"id": pid, "kind": "boulder", "x": x, "z": z, "radius": r, "height": h,
            "seed": seed, "layer": "ground",
            "material": cell(seed, 6, [STONE, COBBLE, ANDESITE])}

DRESSING = {
    "styles": {
        "oak-broad": {"kind": "tree", "form": "template", "species": "oak", "height": 10},
        "birch-thin": {"kind": "tree", "form": "template", "species": "birch", "height": 12},
        "warehouse": {"kind": "house", "shell": house_shell("hoar-store")},
    },
    "props": [
        {"id": "quay-road", "kind": "stroke", "seed": 5, "layer": "ground",
         "points": [[0, 58], [4, 50], [8, 44], [17, 36], [17, 26]],
         "radius": 2, "style": "solid", "claimsGround": False,
         "material": cell(15, 5, [GRAVEL, ANDESITE, COBBLE])},
        # the wharf shed, on the one stretch of quay the seats read leaves free — it is
        # the cover the crossing lands beside, and it is timber on a sand terrace
        {"id": "wharf-shed", "kind": "house", "seed": 521, "layer": "ground",
         "style": "warehouse", "front": "negZ",
         "wings": [{"corners": [[-11, 10], [0, 19]]}]},
        tree("holm-1", "oak-broad", -28, 42), tree("holm-2", "birch-thin", -12, 45),
        tree("holm-3", "oak-broad", -16, 48),
        tree("knoll-1", "birch-thin", 26, 42), tree("knoll-2", "oak-broad", 30, 48),
        tree("knoll-3", "birch-thin", 18, 51),
        tree("wharf-1", "oak-broad", -18, 14), tree("wharf-2", "birch-thin", 15, 17),
        tree("wharf-3", "oak-broad", -4, 22),
        boulder("erratic-e", 12, 21, 2, 3, 41), boulder("erratic-w", -19, 20, 2, 3, 42),
        {"id": "ling", "kind": "flora", "seed": 13, "layer": "ground",
         "points": [[-52, 8], [52, 8], [52, 72], [-52, 72]],
         "spec": {"points": 5600, "coverage": 0.17, "scale": 26, "octaves": 3,
                  "fernShare": 0.3, "flowerShare": 0.06, "flowerScale": 14, "tallShare": 0.04}},
    ],
}

FINISH = {
    "themes": {"upland": THEME_UPLAND, "holm": THEME_HOLM, "quay": THEME_QUAY},
    "mapTheme": "upland",
    "biome": {"kind": "solid", "id": 3},        # Extreme Hills: grass #8ab689, a pale turf
    "themeByHeight": {str(QUAY_Y): "quay", str(SHELF_Y): "holm"},
    "addShapes": ADD_SHAPES,
    "addLayers": ADD_LAYERS,
    "relief": RELIEF,
    "roomStyles": {"spawn": style("showcase-hall"), "wool": style("showcase-cage")},
    "dressing": DRESSING,
    "authors": ["Opus 5"],
    "created": "2026-09-16",
}


def main():
    json.dump(PLAN,   open(os.path.join(HERE, SLUG + ".plan.json"),   "w"), indent=1)
    json.dump(FINISH, open(os.path.join(HERE, SLUG + ".finish.json"), "w"), indent=1)
    print("wrote", SLUG + ".plan.json", "and", SLUG + ".finish.json")


if __name__ == "__main__":
    main()
