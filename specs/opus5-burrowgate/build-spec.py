#!/usr/bin/env python3
"""Burrowgate — a CTW board whose defence rotates underground.

Adapted from the composed board `players=12 symmetry=rot_180 seed=65` (hub `twin`,
frontline `bar`, wools `i` + `l`).  The composed board hangs one wool off the hub's west
end and walks the other out along a twenty-five-block dog-leg east: the attacker's walks
are 129 and 175 blocks, a ratio of 1.36, and the defender's 30 and 48.  Here both wools
sit on sunken shelves ten blocks below the hub, the east one is cut off its spur and
bridged back over a team-only crossing, and a gallery runs the whole length of the hub
between the two shelves — the defence's own rotation, roofed by the ground the attack is
fighting over.

Writes opus5-burrowgate.plan.json and opus5-burrowgate.finish.json beside this file.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SLUG = "opus5-burrowgate"

CELL = 5
HUB_Y, FRONT_Y, SPAWN_Y, SHELF_Y = 16, 15, 17, 11
SLAB_FLOOR = 15          # the hill's turf is a slab from y15; its body is the layer under
ROCK_TOP = 14            # the rock fills y1..y14, so the slab rests on it with no gap
GALLERY_SOLE = 10        # under the lane the rock stops at y10, leaving y11..y14 to walk

# ---------------------------------------------------------------- materials
def s(i, d=0):  return {"kind": "solid", "id": i, "data": d}
GRASS, DIRT, COARSE, PODZOL = s(2), s(3, 0), s(3, 1), s(3, 2)
GRAVEL, STONE, ANDESITE, GRANITE = s(13), s(1, 0), s(1, 5), s(1, 1)
POL_GRANITE, DIORITE, COBBLE = s(1, 2), s(1, 3), s(4)
TERRACOTTA, RED_SAND, SANDSTONE = s(172), s(12, 1), s(24)
BRICK, MOSSY_BRICK, CHISELED = s(98, 0), s(98, 1), s(98, 3)
MOSSY_COBBLE, PLANKS_SPRUCE, LOG_SPRUCE = s(48), s(5, 1), s(17, 1)

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
# ground family: dry ochre hill, grass coming to meet terracotta on a Mesa tint.
# built family: dark spruce and andesite.  accent: the gallery's damp cobble.
FELL_FLAT     = depth([(cell(29, 15, [GRASS, COARSE, PODZOL]), 1), (DIRT, 2), (COARSE, 1)], GRAVEL)
FELL_SHOULDER = depth([(COARSE, 1), (TERRACOTTA, 2)], GRAVEL)
FELL_FACE     = depth([(TERRACOTTA, 2), (GRANITE, 2)], STONE)

THEME_FELL = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void", "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": GRAVEL},
    "surface": {"enabled": True, "depth": 3,
                "material": slope([(FELL_FLAT, 18), (FELL_SHOULDER, 14), (FELL_FACE, 58)], GRAVEL)},
    "wallEnabled": True,
    "wall": runs([(COARSE, 1), (TERRACOTTA, 3), (GRANITE, 2), (RED_SAND, 1), (SANDSTONE, 2)], STONE),
    "fill": cell(7, 12, [GRANITE, POL_GRANITE], jitter=35, warp=5, rise=5),
}

# the two shelves: a cut floor of gravel and terracotta, ten blocks under the fell
THEME_SHELF = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void", "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": GRAVEL},
    "surface": {"enabled": True, "depth": 3,
                "material": depth([(cell(19, 10, [GRAVEL, COARSE, TERRACOTTA]), 1),
                                   (TERRACOTTA, 2)], SANDSTONE)},
    "wallEnabled": True,
    "wall": runs([(GRAVEL, 1), (TERRACOTTA, 3), (SANDSTONE, 2), (GRANITE, 3)], STONE),
    "fill": cell(9, 11, [GRANITE, POL_GRANITE], jitter=35, warp=5, rise=5),
}

# the hill's body: the rock the gallery is driven through, and the rock its own
# flanks show where the turf slab ends. Strata, not a built revetment.
THEME_ROCK = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "drop", "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": GRAVEL},
    "surface": {"enabled": True, "depth": 2,
                "material": depth([(cell(41, 7, [GRAVEL, COBBLE, ANDESITE]), 1),
                                   (ANDESITE, 1)], GRANITE)},
    "wallEnabled": True,
    "wall": runs([(TERRACOTTA, 2), (SANDSTONE, 2), (GRANITE, 3), (ANDESITE, 2),
                  (POL_GRANITE, 3)], POL_GRANITE),
    "fill": cell(11, 9, [GRANITE, ANDESITE], jitter=30, warp=4, rise=4),
}

# ---------------------------------------------------------------- the plan
PLAN = {
    "plan": 2,
    "meta": {"name": "Burrowgate",
             "notes": "CTW. Two wools on sunken shelves under a hill; a gallery runs the "
                      "length of the hub between them, and the east shelf is an island "
                      "its own team bridges to."},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 12,
                "surface": HUB_Y, "observerY": 48},
    "pieces": [
        # the hub, deepened from ten blocks to twenty so the gallery under it has a roof
        # wide enough to be a place and the two ramps have somewhere to run
        {"id": "hub-bar", "role": "piece", "rect": [-1, 8, 7, 4], "surface": HUB_Y},
        {"id": "hub-w",   "role": "piece", "rect": [-1, 6, 2, 2], "surface": HUB_Y},
        {"id": "hub-e",   "role": "piece", "rect": [3, 6, 2, 2],  "surface": HUB_Y},
        {"id": "spawn-t1", "role": "piece", "rect": [0, 12, 1, 2], "surface": SPAWN_Y},
        {"id": "spawn-room", "role": "spawn", "rect": [1, 12, 3, 2], "surface": SPAWN_Y},
        # the west shelf: five blocks under the hub, running the hub's whole depth so the
        # gallery's mouth is as wide as the gallery, and lengthened west so the two wools
        # sit comparably far from the spawn
        {"id": "wool-a-t1", "role": "piece", "rect": [-6, 8, 5, 4], "surface": SHELF_Y},
        {"id": "wool-a-room", "role": "wool-room", "rect": [-8, 9, 2, 2], "surface": SHELF_Y},
        # the east shelf, and the room cut off it onto its own island fifteen blocks out:
        # only this team's own crossing reaches it, which is `CT4`'s team transient-link
        {"id": "wool-b-t1", "role": "piece", "rect": [6, 8, 2, 4], "surface": SHELF_Y},
        {"id": "wool-b-room", "role": "wool-room", "rect": [7, 3, 2, 2], "surface": SHELF_Y},
        # the frontline, widened east so it meets the hub's east prong and the walk to the
        # east wool is not the whole way round the hub
        {"id": "front", "role": "piece", "rect": [-3, 2, 7, 4], "surface": FRONT_Y},
    ],
    "zones": [
        {"id": "mid-band", "rect": [-3, -2, 6, 4], "holes": []},
        # the team's own crossing to its east wool: every side of it touches only this
        # team's ground, which is what makes it a transient link rather than a mid stone
        {"id": "b-link", "rect": [6, 4, 3, 5], "holes": []},
    ],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn-room", "at": [5, 5], "facing": "front",
                    "footprint": [1, 1, 8, 8]}],
        "wools": [{"id": "wool-1", "piece": "wool-a-room", "at": [5, 5]},
                  {"id": "wool-2", "piece": "wool-b-room", "at": [5, 5]}],
        "iron": [{"id": "iron-1", "piece": "spawn-room", "at": [13, 5]}],
        "destroyables": [], "cores": [],
    },
    "walls": [], "boxes": [],
}

# ---------------------------------------------------------------- the relief
# One group, one relief.  The hill rolls; the two shelves, the two ramps and the two flats
# that have to be flat are stated out of it, so that cut ground and grown ground meet at a
# face rather than being graded into each other.
RELIEF = {"team": {
    "base": HUB_Y, "reach": 12, "step": 1, "landform": "rolling",
    "grain": {"amplitude": 1.2, "scale": 16, "seed": 5},
    "marks": [
        # the frontline is fought over, so it is flat to its edge and carries no tread
        # the landing apron the crossing arrives on is flat to its edge and carries no
        # tread; the front's back half is left to roll, so the walk up to the hub has cover
        {"id": "front-flat", "kind": "area", "h": FRONT_Y, "bevel": 2,
         "ring": [[-16, 9], [21, 9], [21, 20], [-16, 20]]},
        {"id": "front-knoll-w", "kind": "point", "at": [-9, 26], "r": 4, "h": 19},
        {"id": "front-knoll-e", "kind": "point", "at": [13, 25], "r": 4, "h": 18},
        # the hub's north strip is where both flights arrive, so it is stated at exactly
        # the height they are cut to; its tread grades it into the rolling half behind
        # the hub is the ground the match is fought over and the gallery's roof, so it is
        # stated flat over its whole footprint and carries no tread: a tread here would
        # grade the two flights' heads into the hillside and leave nowhere to stand
        {"id": "hub-flat", "kind": "area", "h": HUB_Y, "bevel": 2,
         "ring": [[-6, 37], [31, 37], [31, 61], [-6, 61]]},
    ],
    "pushes": [
        # one swell over the gallery's roof, so the hill is not a plate
        # a swell across the front's back half, so the ground between the apron and the
        # hub is something to come up rather than a plane
        {"id": "brow", "ring": [[-14, 22], [0, 21], [16, 24], [14, 30], [0, 31], [-14, 29]],
         "amount": 3, "falloff": 9, "crown": 1.7, "roughness": 1, "seed": 7},
    ],
}}

# ---------------------------------------------------------------- authored shapes
# The two ramps off the hub down onto the shelves, cut into the hill's north face.  Each
# is a flight rather than a graded seam: level, skirt 0, a material rather than a theme,
# twelve blocks of run for five of rise, and its footprint taken out of the relief.
RAMP_MAT = cell(61, 6, [COBBLE, ANDESITE, BRICK], jitter=30, warp=4, rise=3)

ADD_SHAPES = [
    {"id": "ramp-w", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": HUB_Y, "height_mode": "level", "skirt": 0, "keepClear": True,
     "relief_scope": "exclude", "material": RAMP_MAT, "group": "team",
     "vertices": [[-5, 40], [9, 40], [9, 48], [-5, 48]],
     "anchor_heights": [SHELF_Y, HUB_Y, HUB_Y, SHELF_Y]},
    {"id": "ramp-e", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": HUB_Y, "height_mode": "level", "skirt": 0, "keepClear": True,
     "relief_scope": "exclude", "material": RAMP_MAT, "group": "team",
     "vertices": [[16, 40], [30, 40], [30, 48], [16, 48]],
     "anchor_heights": [HUB_Y, SHELF_Y, SHELF_Y, HUB_Y]},
    # a worn patch on the crest between the two ramp heads: a brush, so it states a
    # height_mode and is a scope candidate at all
    {"id": "scuff", "type": "polygon", "operation": "add", "height_mode": "raise",
     "base_height": 0, "skirt": 0, "theme": "shelf", "group": "team",
     "vertices": [[9, 41], [16, 40], [19, 44], [16, 47], [10, 47], [7, 44]]},
]

# ---------------------------------------------------------------- the second storey
# The gallery, drawn as the complement of the space rather than cut with a subtract: the
# rock fills the hill's body to y14 everywhere the hub stands except along the lane, where
# it stops at y10 and the four courses over it are the way through.  The hub's own ground
# is a slab from y15, which is the gallery's roof.
def rock(pid, x0, z0, x1, z1, top=ROCK_TOP):
    return {"id": pid, "type": "rectangle", "operation": "add", "theme": "rock",
            "min_x": x0, "max_x": x1, "min_z": z0, "max_z": z1,
            "floor": 1, "base_height": top}

UNDER = [
    rock("rock-crest", 9, 40, 16, 48),      # between the two ramp strips
    rock("rock-north", -5, 48, 30, 50),     # the gallery's north wall
    rock("rock-south", -5, 56, 30, 60),     # its south wall
    rock("rock-sole", -5, 50, 30, 56, GALLERY_SOLE),   # the floor: four courses of air over it
    rock("rock-prong-w", -5, 30, 5, 40),
    rock("rock-prong-e", 15, 30, 25, 40),
]

ADD_LAYERS = [
    {"id": "under", "name": "The gallery", "base_y": 0, "below": True,
     "shapes": UNDER,
     "groups": [{"id": "under", "name": "under", "mirrors": True,
                 "shapeIds": [sh["id"] for sh in UNDER]}]},
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
        "pine-tall": {"kind": "tree", "form": "template", "species": "spruce", "height": 13},
        "pine-low": {"kind": "tree", "form": "template", "species": "spruce", "height": 9},
        "steading": {"kind": "house", "shell": house_shell("hoar-steading")},
        "blockhouse": {"kind": "house", "shell": house_shell("sb-blockhouse-lo")},
    },
    "props": [
        {"id": "ridge-road", "kind": "stroke", "seed": 5, "layer": "ground",
         "points": [[11, 62], [13, 53], [14, 45], [10, 36], [2, 28]],
         "radius": 2, "style": "solid", "claimsGround": False,
         "material": cell(15, 5, [GRAVEL, ANDESITE, COBBLE])},
        # the steading at the west shelf's gallery mouth: the store the tunnel serves, on
        # one of the 116 seats `POST …/sketch/seats` answers for an 11x9 footprint
        {"id": "steading", "kind": "house", "seed": 417, "layer": "ground",
         "style": "steading", "front": "posX",
         "wings": [{"corners": [[-18, 50], [-7, 59]]}]},
        # a blockhouse on the landing apron: the only cover where the crossing arrives
        {"id": "blockhouse", "kind": "house", "seed": 418, "layer": "ground",
         "style": "blockhouse", "front": "negZ",
         "wings": [{"corners": [[8, 10], [19, 19]]}]},
        tree("holt-1", "pine-tall", -25, 44), tree("holt-2", "pine-low", -18, 47),
        tree("holt-3", "pine-tall", -25, 55), tree("holt-4", "pine-low", -27, 58),
        tree("holt-5", "pine-tall", 31, 44), tree("holt-6", "pine-low", 36, 48),
        tree("holt-7", "pine-tall", 34, 57),
        tree("front-1", "pine-low", -10, 25), tree("front-2", "pine-tall", 12, 28),
        boulder("erratic-w", -13, 45, 3, 4, 41), boulder("erratic-e", 37, 43, 2, 3, 42),
        {"id": "ling", "kind": "flora", "seed": 13, "layer": "ground",
         "points": [[-44, 8], [48, 8], [48, 72], [-44, 72]],
         "spec": {"points": 5600, "coverage": 0.18, "scale": 26, "octaves": 3,
                  "fernShare": 0.32, "flowerShare": 0.05, "flowerScale": 14, "tallShare": 0.04}},
    ],
}

FINISH = {
    "themes": {"fell": THEME_FELL, "shelf": THEME_SHELF, "rock": THEME_ROCK},
    "mapTheme": "fell",
    "biome": {"kind": "solid", "id": 37},       # Mesa: grass #90814d, so the greens are dry
    "themeByHeight": {str(SHELF_Y): "shelf"},
    # the hub's ground is a slab from y10, which is what leaves the gallery room under it;
    # the shelves are stated out of the solve so they meet the hill at a face
    "shapePropsByHeight": {str(HUB_Y): {"floor": SLAB_FLOOR},
                           str(SHELF_Y): {"relief_scope": "exclude"}},
    "addShapes": ADD_SHAPES,
    "addLayers": ADD_LAYERS,
    "relief": RELIEF,
    "roomStyles": {"spawn": style("showcase-hall"), "wool": style("showcase-cage")},
    "dressing": DRESSING,
    "authors": ["Opus 5"],
    "created": "2026-09-15",
}


def main():
    json.dump(PLAN,   open(os.path.join(HERE, SLUG + ".plan.json"),   "w"), indent=1)
    json.dump(FINISH, open(os.path.join(HERE, SLUG + ".finish.json"), "w"), indent=1)
    print("wrote", SLUG + ".plan.json", "and", SLUG + ".finish.json")


if __name__ == "__main__":
    main()
