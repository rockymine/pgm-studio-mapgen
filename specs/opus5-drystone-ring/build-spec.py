#!/usr/bin/env python3
"""Drystone Ring — a CTW board with a raider's high road over the ring.

Adapted from the composed board `players=8 symmetry=mirror_z seed=183` (hub `bar`,
frontline `none`, wool `donut`).  The composed board rings its wool room with a five-piece
donut and offers the attack two ways round the hole, both of them the same forty-five-block
walk down a ten-block corridor, and leaves 125 blocks of the ring's west end on nobody's
route at all.  Here the north bar is widened at its west end and tapered at its east, and a
causeway is walked out seven blocks above it: forty blocks of open deck with a ramp at each
end and no way off in between, which is the third way in and the only quick one.

Writes opus5-drystone-ring.plan.json and opus5-drystone-ring.finish.json beside this file.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SLUG = "opus5-drystone-ring"

CELL = 5
MOOR_Y, GARTH_Y = 12, 14
DECK_Y = 18            # the deck's own course, so a player stands on it at 19

# ---------------------------------------------------------------- materials
def s(i, d=0):  return {"kind": "solid", "id": i, "data": d}
GRASS, DIRT, COARSE, PODZOL = s(2), s(3, 0), s(3, 1), s(3, 2)
GRAVEL, STONE, ANDESITE, DIORITE = s(13), s(1, 0), s(1, 5), s(1, 3)
POL_ANDESITE, COBBLE, MOSSY_COBBLE = s(1, 6), s(4), s(48)
GRANITE, CLAY, BRICK, CHISELED = s(1, 1), s(82), s(98, 0), s(98, 3)
SPRUCE_PLANK, SPRUCE_LOG = s(5, 1), s(17, 1)

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
# ground family: a cold dark moor — podzol and coarse dirt under a taiga tint.
# built family: drystone cobble.  accent: the causeway's spruce timber.
MOOR_FLAT     = depth([(cell(27, 16, [GRASS, PODZOL, COARSE]), 1), (DIRT, 2), (COARSE, 1)], GRAVEL)
MOOR_SHOULDER = depth([(PODZOL, 1), (COARSE, 1), (DIRT, 2)], GRAVEL)
MOOR_FACE     = depth([(GRAVEL, 2), (CLAY, 1), (ANDESITE, 2)], DIORITE)

THEME_MOOR = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void", "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": GRAVEL},
    "surface": {"enabled": True, "depth": 3,
                "material": slope([(MOOR_FLAT, 20), (MOOR_SHOULDER, 14), (MOOR_FACE, 56)], GRAVEL)},
    "wallEnabled": True,
    "wall": runs([(COARSE, 1), (DIRT, 2), (GRAVEL, 2), (CLAY, 2), (ANDESITE, 3),
                  (DIORITE, 2)], POL_ANDESITE),
    # the strip under the causeway is painted out of this bucket, because one column
    # resolves one band stack and ground under a slab falls in the fill
    "fill": cell(7, 10, [ANDESITE, DIORITE, GRAVEL], jitter=35, warp=5, rise=5),
}

# the garth behind the spawn: the same moor two blocks up, walled and grazed
THEME_GARTH = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "drop", "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": COBBLE},
    "surface": {"enabled": True, "depth": 3,
                "material": depth([(cell(37, 11, [GRASS, COARSE]), 1), (DIRT, 2)], GRAVEL)},
    "wallEnabled": True,
    "wall": {"kind": "wallRun", "runs": [
        {"material": COBBLE, "width": 2}, {"material": MOSSY_COBBLE, "width": 1},
        {"material": ANDESITE, "width": 3}, {"material": GRAVEL, "width": 2}]},
    "fill": cell(9, 10, [ANDESITE, DIORITE], jitter=30, warp=4, rise=4),
}

# the scalded ground the lanes are worn to, used as a brush and nowhere else
THEME_SCALD = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void", "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": GRAVEL},
    "surface": {"enabled": True, "depth": 2,
                "material": depth([(cell(47, 8, [COARSE, GRAVEL, PODZOL]), 1), (DIRT, 1)], GRAVEL)},
    "wallEnabled": True,
    "wall": runs([(GRAVEL, 2), (ANDESITE, 3), (DIORITE, 2)], POL_ANDESITE),
    "fill": cell(7, 10, [ANDESITE, DIORITE], jitter=35, warp=5, rise=5),
}

# ---------------------------------------------------------------- the plan
PLAN = {
    "plan": 2,
    "meta": {"name": "Drystone Ring",
             "notes": "CTW. One wool a team, ringed by a drystone donut. Two ways round "
                      "the hole on the ground and one over it: a causeway seven blocks up "
                      "with a ramp at each end and no way off between them."},
    "globals": {"cell": CELL, "symmetry": "mirror_z", "maxPlayers": 8,
                "surface": MOOR_Y, "observerY": 44},
    "pieces": [
        {"id": "hub", "role": "piece", "rect": [-2, 2, 5, 4], "surface": MOOR_Y},
        {"id": "spawn-t1", "role": "piece", "rect": [1, 6, 2, 2], "surface": GARTH_Y},
        {"id": "spawn-room", "role": "spawn", "rect": [1, 8, 3, 2], "surface": GARTH_Y},
        # the stem, tapered to a ten-by-fifteen throat: everything that reaches the ring
        # from the hub comes through it
        {"id": "stem", "role": "piece", "rect": [-4, 3, 2, 3], "surface": MOOR_Y},
        # the north bar, widened from ten blocks to fifteen at its west end so the causeway
        # over it leaves a lane beside rather than covering the whole corridor, and left at
        # ten at its east end, which is the taper
        {"id": "bar-w", "role": "piece", "rect": [-12, 2, 3, 3], "surface": MOOR_Y},
        # the corner the ring turns at stays ten blocks deep: widened it is a cul-de-sac
        # no journey enters, which is what nine per cent of this board's ground was
        {"id": "bar-nw", "role": "piece", "rect": [-14, 3, 2, 2], "surface": MOOR_Y},
        {"id": "bar-e", "role": "piece", "rect": [-9, 3, 5, 2], "surface": MOOR_Y},
        {"id": "stub-e", "role": "piece", "rect": [-6, 5, 2, 3], "surface": MOOR_Y},
        {"id": "stub-w", "role": "piece", "rect": [-14, 5, 2, 3], "surface": MOOR_Y},
        {"id": "south-bar", "role": "piece", "rect": [-12, 8, 8, 2], "surface": MOOR_Y},
        {"id": "wool-room", "role": "wool-room", "rect": [-14, 8, 2, 2], "surface": MOOR_Y},
    ],
    "zones": [{"id": "mid-band", "rect": [-2, -2, 5, 4], "holes": []}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn-room", "at": [5, 5], "facing": "front",
                    "footprint": [1, 1, 8, 8]}],
        "wools": [{"id": "wool-1", "piece": "wool-room", "at": [5, 5]}],
        "iron": [{"id": "iron-1", "piece": "spawn-room", "at": [13, 5]}],
        "destroyables": [], "cores": [],
    },
    "walls": [], "boxes": [],
}

# ---------------------------------------------------------------- the relief
# The ring is corridors, so most of it is stated flat: a rolling relief inside a ten-block
# lane is ground nobody can fight on.  What rolls is the wide west end, the yard the wool
# room stands in and the hub the crossing lands on.
RELIEF = {"team": {
    "base": MOOR_Y, "reach": 12, "step": 1, "landform": "rolling",
    "grain": {"amplitude": 1.1, "scale": 14, "seed": 5},
    "marks": [
        # the two lanes of the ring, flat to their edges and carrying no tread
        {"id": "bar-flat", "kind": "area", "h": MOOR_Y, "bevel": 2,
         "ring": [[-46, 14], [-19, 14], [-19, 26], [-46, 26]]},
        {"id": "south-flat", "kind": "area", "h": MOOR_Y, "bevel": 2,
         "ring": [[-61, 39], [-19, 39], [-19, 51], [-61, 51]]},
        # only the strip the crossing lands on is pinned; the hub's back half rolls up
        # to the garth behind it
        {"id": "hub-flat", "kind": "area", "h": MOOR_Y, "bevel": 2,
         "ring": [[-11, 9], [16, 9], [16, 21], [-11, 21]]},
        {"id": "hub-brow", "kind": "point", "at": [1, 26], "r": 5, "h": 16},
        # the ramp off the causeway's far end lands here, so the ground it lands on is
        # stated rather than left to whatever the push behind it does
        {"id": "stub-flat", "kind": "area", "h": MOOR_Y, "bevel": 2,
         "ring": [[-72, 24], [-58, 24], [-58, 41], [-72, 41]]},
        # the knott on the wide west end, which is what the causeway is walked past
        {"id": "knott", "kind": "point", "at": [-58, 17], "r": 5, "h": 17},
        {"id": "garth-flat", "kind": "area", "h": GARTH_Y, "tread": 4, "bevel": 2,
         "ring": [[4, 29], [21, 29], [21, 51], [4, 51]]},
    ],
    "pushes": [
        # the swell on the wide west end, north of the ring's turn
        {"id": "rigg", "ring": [[-60, 10], [-50, 9], [-44, 13], [-50, 17], [-60, 16]],
         "amount": 3, "falloff": 9, "crown": 1.7, "roughness": 1, "seed": 11},
    ],
}}

# ---------------------------------------------------------------- authored shapes
RAMP_MAT = cell(61, 6, [COBBLE, ANDESITE, MOSSY_COBBLE], jitter=30, warp=4, rise=3)

ADD_SHAPES = [
    # up onto the causeway, off the hub and across the stem: fourteen blocks for seven
    {"id": "ramp-up", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": DECK_Y + 1, "height_mode": "level", "skirt": 0,
     "keepClear": True, "relief_scope": "exclude", "material": RAMP_MAT, "group": "team",
     "vertices": [[-22, 16], [-8, 16], [-8, 22], [-22, 22]],
     "anchor_heights": [DECK_Y + 1, MOOR_Y, MOOR_Y, DECK_Y + 1]},
    # and down off its far end onto the west stub, ten blocks from the wool room's door
    {"id": "ramp-down", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": DECK_Y + 1, "height_mode": "level", "skirt": 0,
     "keepClear": True, "relief_scope": "exclude", "material": RAMP_MAT, "group": "team",
     "vertices": [[-68, 16], [-62, 16], [-62, 30], [-68, 30]],
     "anchor_heights": [DECK_Y + 1, DECK_Y + 1, MOOR_Y, MOOR_Y]},
    # a drystone wall along the south lane's outer edge: a polyline, so four points draw
    # as a curve rather than a chain of chords
    {"id": "drystone", "type": "polyline", "operation": "add", "override": True,
     "vertices": [[-56, 49], [-44, 48], [-32, 49], [-22, 47]],
     "radius": 1.0, "stroke_edge": "solid", "stroke_seed": 7,
     "floor": 0, "base_height": 2, "skirt": 0, "height_mode": "raise",
     "keepClear": True, "material": cell(63, 4, [COBBLE, MOSSY_COBBLE, ANDESITE], rise=3),
     "group": "team"},
    # the lanes worn bare where the ring is walked: brushes, so each states a height_mode
    # and is a scope candidate at all
    {"id": "scald-bar", "type": "polygon", "operation": "add", "height_mode": "raise",
     "base_height": 0, "skirt": 0, "theme": "scald", "group": "team",
     "vertices": [[-44, 21], [-30, 20], [-22, 22], [-30, 25], [-42, 25]]},
    {"id": "scald-south", "type": "polygon", "operation": "add", "height_mode": "raise",
     "base_height": 0, "skirt": 0, "theme": "scald", "group": "team",
     "vertices": [[-56, 43], [-40, 42], [-26, 44], [-30, 47], [-48, 47]]},
]

# ---------------------------------------------------------------- the second storey
# The causeway: forty blocks of deck on spruce trestles, standing seven blocks over the
# north bar with a ramp at each end and nothing in between.  A made thing, so it is
# painted over its own span and the lane under it keeps its own column.
DECK_MAT = cell(53, 7, [SPRUCE_PLANK, COBBLE, ANDESITE], jitter=25, warp=4, rise=2)
POST_MAT = cell(57, 4, [SPRUCE_LOG, COBBLE], jitter=25, warp=3, rise=3)

def post(pid, x0, z0):
    return {"id": pid, "type": "rectangle", "operation": "add", "keepClear": True,
            "min_x": x0, "max_x": x0 + 2, "min_z": z0, "max_z": z0 + 2,
            "floor": 0, "base_height": DECK_Y - MOOR_Y + 1, "material": POST_MAT}

POSTS = [post(f"trestle-{i}-{j}", x, z)
         for i, x in enumerate((-58, -48, -38, -28))
         for j, z in enumerate((17, 20))]

DECK = [{"id": "causey", "type": "rectangle", "operation": "add", "keepClear": True,
         "min_x": -62, "max_x": -22, "min_z": 16, "max_z": 22,
         "floor": 0, "base_height": 1, "material": DECK_MAT}]

RAIL = [{"id": "causey-rail-n", "type": "rectangle", "operation": "add", "keepClear": True,
         "min_x": -62, "max_x": -22, "min_z": 16, "max_z": 17,
         "floor": 0, "base_height": 1, "material": SPRUCE_LOG}]

ADD_LAYERS = [
    {"id": "trestles", "name": "Causeway trestles", "base_y": MOOR_Y - 1, "kind": "made",
     "part_of": "causeway", "shapes": POSTS,
     "groups": [{"id": "trestles", "name": "trestles", "mirrors": True,
                 "shapeIds": [p["id"] for p in POSTS]}]},
    {"id": "causey", "name": "The causeway", "base_y": DECK_Y, "kind": "made",
     "part_of": "causeway", "shapes": DECK,
     "groups": [{"id": "causey", "name": "causey", "mirrors": True, "shapeIds": ["causey"]}]},
    {"id": "causey-rail", "name": "Causeway rail", "base_y": DECK_Y + 1, "kind": "made",
     "part_of": "causeway", "shapes": RAIL,
     "groups": [{"id": "causey-rail", "name": "rail", "mirrors": True,
                 "shapeIds": ["causey-rail-n"]}]},
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
        "spruce-tall": {"kind": "tree", "form": "template", "species": "spruce", "height": 14},
        "spruce-low": {"kind": "tree", "form": "template", "species": "spruce", "height": 10},
    },
    "props": [
        {"id": "ring-road", "kind": "stroke", "seed": 5, "layer": "ground",
         "points": [[8, 36], [2, 28], [-8, 22], [-18, 20]],
         "radius": 2, "style": "solid", "claimsGround": False,
         "material": cell(15, 5, [GRAVEL, ANDESITE, COBBLE])},
        # No building. `POST …/sketch/seats` answers eight house seats on the whole board
        # at 11x9 and none of them on this team's own ground; an eight-player ring is
        # ten-block corridors, and every footprint tried on the hub refuses `DR-PASS`
        # because the spawn march takes half of it. What is built here is the causeway
        # and the drystone wall.
        tree("bar-1", "spruce-tall", -56, 12), tree("bar-2", "spruce-low", -48, 13),
        tree("west-1", "spruce-tall", -52, 11), tree("west-2", "spruce-low", -58, 15),
        tree("ring-1", "spruce-tall", -27, 30),
        tree("south-1", "spruce-low", -26, 44), tree("south-2", "spruce-tall", -36, 45),
        tree("south-3", "spruce-low", -45, 42),
        boulder("erratic-s", -22, 33, 2, 3, 42),
        {"id": "ling", "kind": "flora", "seed": 13, "layer": "ground",
         "points": [[-72, 8], [22, 8], [22, 52], [-72, 52]],
         "spec": {"points": 5200, "coverage": 0.19, "scale": 25, "octaves": 3,
                  "fernShare": 0.36, "flowerShare": 0.04, "flowerScale": 13, "tallShare": 0.04}},
    ],
}

FINISH = {
    "themes": {"moor": THEME_MOOR, "garth": THEME_GARTH, "scald": THEME_SCALD},
    "mapTheme": "moor",
    "biome": {"kind": "solid", "id": 5},        # Taiga: grass #86b783, a cold green
    "themeByHeight": {str(GARTH_Y): "garth"},
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
