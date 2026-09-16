#!/usr/bin/env python3
"""Crossdyke — a CTW board whose middle is a two-storey causeway over a limestone reef.

Adapted from the composed board `players=8 symmetry=rot_180 seed=10` (hub `bar`,
frontline `none`, wools `i`).  The composer's twenty-block mid band is replaced by a
fifty-block crossing carrying a real island: a reef five blocks below the banks, with a
masonry causeway standing seven blocks over it.  The high road is the causeway — bridge
fifteen, walk twenty in the open, bridge fifteen.  The low road is the reef itself —
bridge down to either flank, walk under the deck out of sight, and climb one of the two
flights that come up on the deck's far half.

Writes opus5-crossdyke.plan.json and opus5-crossdyke.finish.json beside this file.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SLUG = "opus5-crossdyke"

CELL, SURFACE, REEF_Y = 5, 14, 9
DECK_TOP, DECK_FLOOR = 15, 6          # deck occupies y15; floor 6 over the layer's base_y 9

# ---------------------------------------------------------------- materials
def s(i, d=0):  return {"kind": "solid", "id": i, "data": d}
GRASS, DIRT, COARSE, PODZOL = s(2), s(3, 0), s(3, 1), s(3, 2)
GRAVEL, STONE, ANDESITE, DIORITE = s(13), s(1, 0), s(1, 5), s(1, 3)
POLISHED_AND, COBBLE, CLAY = s(1, 6), s(4), s(82)
BRICK, MOSSY_BRICK, CRACKED, CHISELED = s(98, 0), s(98, 1), s(98, 2), s(98, 3)
MOSSY_COBBLE, SAND = s(48), s(12)

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
    """A thickness on the slope axis is a span of degrees, so one stack finishes the
    flat, the shoulder and the face of the same ground."""
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
    """A preset forked into a house prop. Two of the shipped presets carry a beam over a
    wall with no laid log in it (`HS9`) and a roof slab cut from a different block than the
    roof body (`HS3`); a house prop states neither rather than carrying both in."""
    st = style(name)
    st["beams"] = {"block": -1, "data": 0, "reach": 1, "any": True}
    if isinstance(st.get("roof"), dict):
        st["roof"]["slab"], st["roof"]["slabData"] = -1, 0
    return st

# ---------------------------------------------------------------- themes
# ground family: green limestone moor.  built family: pale grey masonry.
# accent: the reef's wet grey shingle, which is neither.
MOOR_FLAT     = depth([(cell(31, 14, [GRASS, COARSE]), 1), (DIRT, 2), (COARSE, 1)], GRAVEL)
MOOR_SHOULDER = depth([(COARSE, 1), (DIRT, 2)], GRAVEL)
MOOR_FACE     = depth([(GRAVEL, 2), (CLAY, 1)], ANDESITE)

THEME_MOOR = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void", "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": GRAVEL},
    "surface": {"enabled": True, "depth": 3,
                "material": slope([(MOOR_FLAT, 20), (MOOR_SHOULDER, 14), (MOOR_FACE, 56)], GRAVEL)},
    "wallEnabled": True,
    "wall": runs([(COARSE, 1), (DIRT, 2), (GRAVEL, 2), (CLAY, 2), (ANDESITE, 4)], DIORITE),
    # never plain stone: a fill of 1:0 hands the whole column to whatever is drawn over it
    "fill": cell(7, 12, [ANDESITE, DIORITE], jitter=35, warp=5, rise=5),
}

REEF_FLAT     = depth([(cell(17, 9, [GRAVEL, ANDESITE, COBBLE]), 1), (GRAVEL, 1), (ANDESITE, 2)], DIORITE)
REEF_SHOULDER = depth([(COBBLE, 1), (ANDESITE, 2)], DIORITE)
REEF_FACE     = depth([(ANDESITE, 2), (DIORITE, 2)], STONE)

THEME_REEF = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void", "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": GRAVEL},
    "surface": {"enabled": True, "depth": 3,
                "material": slope([(REEF_FLAT, 22), (REEF_SHOULDER, 16), (REEF_FACE, 52)], DIORITE)},
    "wallEnabled": True,
    "wall": runs([(GRAVEL, 1), (ANDESITE, 3), (DIORITE, 2), (COBBLE, 2)], STONE),
    "fill": cell(9, 11, [ANDESITE, DIORITE], jitter=35, warp=5, rise=5),
}

# the quay and the wool yard: made ground, so it wears courses rather than a field
THEME_QUAY = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "drop", "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": CHISELED},
    "surface": {"enabled": True, "depth": 3,
                "material": depth([(cell(43, 8, [BRICK, POLISHED_AND]), 1), (BRICK, 2)], COBBLE)},
    "wallEnabled": True,
    "wall": {"kind": "wallRun", "runs": [
        {"material": BRICK, "width": 2}, {"material": ANDESITE, "width": 3},
        {"material": COBBLE, "width": 2}, {"material": GRAVEL, "width": 3}]},
    "fill": cell(11, 9, [BRICK, COBBLE], jitter=30, warp=4, rise=4),
}

# ---------------------------------------------------------------- the plan
# Every piece of the composed board moved three cells further from the centre line, which
# is what buys the middle room to hold an island with two fifteen-block hops either side
# of it.  The hub is split in two so its north-west flank can be bitten out, and the wool
# spur is re-hung off the east half.
PLAN = {
    "plan": 2,
    "meta": {"name": "Crossdyke",
             "notes": "CTW. One wool a team behind a limestone moor; the middle is a reef "
                      "with a causeway over it, and the two storeys are two crossings."},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 8,
                "surface": SURFACE, "observerY": 44},
    "pieces": [
        {"id": "bank-w",    "role": "piece",     "rect": [-5, 5, 4, 3]},
        {"id": "bank-e",    "role": "piece",     "rect": [-1, 5, 4, 4]},
        {"id": "spawn-t1",  "role": "piece",     "rect": [-6, 6, 1, 2]},
        {"id": "spawn-room", "role": "spawn",    "rect": [-9, 6, 3, 2]},
        {"id": "wool-t1",   "role": "piece",     "rect": [1, 9, 2, 2]},
        {"id": "wool-room", "role": "wool-room", "rect": [1, 11, 2, 2]},
        # the mid island the composer does not place: five blocks below the banks, its own
        # landmass, stamped once because it lies on the symmetry centre
        {"id": "reef",      "role": "piece",     "rect": [-5, -2, 10, 4],
         "surface": REEF_Y, "mirrors": False},
    ],
    # one zone per crossing rather than one band over the middle: the island is between them
    "zones": [
        {"id": "cross-n", "rect": [-5, 2, 10, 3], "holes": []},
        {"id": "cross-s", "rect": [-5, -5, 10, 3], "holes": []},
    ],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn-room", "at": [5, 5], "facing": "right",
                    "footprint": [1, 1, 8, 8]}],
        "wools":  [{"id": "wool-1", "piece": "wool-room", "at": [5, 5]}],
        "iron":   [{"id": "iron-1", "piece": "spawn-room", "at": [13, 5]}],
        "destroyables": [], "cores": [],
    },
    "walls": [], "boxes": [],
}

# ---------------------------------------------------------------- the relief
# Two grounds, one relief each, and they never meet: the moor is grown and the reef is a
# shelf.  The quay and the wool yard are taken out of the moor's solve so that made ground
# and grown ground meet at a face rather than being graded into one another.
RELIEF = {
    "team": {
        "base": SURFACE, "reach": 16, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 1.5, "scale": 17, "seed": 5},
        "marks": [
            # the apron the bridges land on: flat to its edge, and no tread on it
            {"id": "shore", "kind": "area", "h": 14, "bevel": 2,
             "ring": [[-26, 25], [16, 25], [16, 32], [-26, 32]]},
            {"id": "knoll-w", "kind": "point", "at": [-18, 37], "r": 5, "h": 19},
            {"id": "knoll-e", "kind": "point", "at": [9, 41], "r": 4, "h": 18},
            # the two flats that have to be flat: the spawn's ground and the wool's.
            # Both carry a tread, because each would otherwise meet the moor on a wall.
            {"id": "spawn-flat", "kind": "area", "h": 17, "tread": 4, "bevel": 2,
             "ring": [[-46, 27], [-24, 27], [-24, 43], [-46, 43]]},
            {"id": "wool-flat", "kind": "area", "h": 16, "tread": 4, "bevel": 2,
             "ring": [[3, 46], [17, 46], [17, 66], [3, 66]]},
        ],
        "pushes": [
            # one long swell across the back of the moor, so the bank is not a plane
            {"id": "swell", "ring": [[-24, 36], [-12, 34], [2, 36], [10, 41], [2, 47],
                                     [-12, 46], [-22, 43]],
             "amount": 3, "falloff": 9, "crown": 1.7, "roughness": 1, "seed": 11},
        ],
    },
    # the reef: nearly flat, two low humps, and the flights excluded from the solve
    "neutral": {
        "base": REEF_Y, "reach": 8, "step": 1, "landform": "plain",
        "grain": {"amplitude": 0.7, "scale": 11, "seed": 3},
        "marks": [
            {"id": "hump-w", "kind": "point", "at": [-17, 4], "r": 4, "h": 11},
            {"id": "hump-e", "kind": "point", "at": [17, -4], "r": 4, "h": 11},
        ],
        "pushes": [],
    },
}

# ---------------------------------------------------------------- authored shapes
ADD_SHAPES = [
    # the quay: made ground along the moor's front edge, excluded from the solve so that it
    # meets the moor behind it at a face rather than being graded into it
    {"id": "quay", "type": "polygon", "operation": "add", "override": True, "keepClear": True,
     "floor": 0, "base_height": 14, "height_mode": "level", "skirt": 0,
     "relief_scope": "exclude", "theme": "quay", "group": "team",
     "vertices": [[-26, 25], [16, 25], [16, 30], [6, 30], [4, 33], [-8, 33], [-10, 30],
                  [-26, 30]]},
    # the two flights set into the quay's own face, each cut into a re-entrant of it
    {"id": "quay-stair-w", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": 14, "height_mode": "level", "skirt": 0, "keepClear": True,
     "relief_scope": "exclude", "material": BRICK, "group": "team",
     "vertices": [[-10, 30], [-8, 30], [-8, 37], [-10, 37]],
     "anchor_heights": [14, 14, 17, 17]},
    {"id": "quay-stair-e", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": 14, "height_mode": "level", "skirt": 0, "keepClear": True,
     "relief_scope": "exclude", "material": BRICK, "group": "team",
     "vertices": [[4, 30], [6, 30], [6, 37], [4, 37]],
     "anchor_heights": [14, 14, 17, 17]},
    # a worn patch of bare moor where the two flights come up — a splotch, not a pattern
    # a brush, so it declares a height_mode: a one-course add under solved ground is never
    # a scope candidate and paints nothing at all, in silence
    {"id": "scald", "type": "polygon", "operation": "add", "height_mode": "raise",
     "base_height": 0, "skirt": 0, "theme": "reef", "group": "team",
     "vertices": [[-12, 33], [-1, 32], [7, 35], [5, 40], [-6, 41], [-13, 38]]},
    # the two flights off the reef onto the causeway deck.  Each runs eighteen blocks for a
    # seven-block rise and comes up on the far half of the deck from the bank it faces.
    {"id": "reef-stair-e", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": 9, "height_mode": "level", "skirt": 0, "keepClear": True,
     "relief_scope": "exclude", "material": BRICK, "layer": "ground", "group": "neutral",
     "vertices": [[6, 10], [13, 10], [13, -8], [6, -8]],
     "anchor_heights": [9, 9, DECK_TOP, DECK_TOP]},
    {"id": "reef-stair-w", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": 9, "height_mode": "level", "skirt": 0, "keepClear": True,
     "relief_scope": "exclude", "material": BRICK, "layer": "ground", "group": "neutral",
     "vertices": [[-13, -10], [-6, -10], [-6, 8], [-13, 8]],
     "anchor_heights": [9, 9, DECK_TOP, DECK_TOP]},
]

# ---------------------------------------------------------------- the second storey
# The causeway: a made thing, so it is painted over its own span and nothing below it is
# repainted.  Eight piers stand on the reef, the deck runs the island's whole depth, and a
# kerb along both edges says which way a player may fall off.
DECK_MAT = cell(53, 7, [BRICK, POLISHED_AND, CHISELED], jitter=30, warp=4, rise=3)
PIER_MAT = cell(57, 5, [COBBLE, ANDESITE, MOSSY_COBBLE], jitter=30, warp=4, rise=3)

def pier(pid, x0, z0):
    return {"id": pid, "type": "rectangle", "operation": "add", "keepClear": True,
            "min_x": x0, "max_x": x0 + 2, "min_z": z0, "max_z": z0 + 2,
            "floor": 0, "base_height": DECK_FLOOR, "material": PIER_MAT}

PIERS = [pier(f"pier-w{n}", -6, z) for n, z in enumerate((-10, -5, 1, 6))] \
      + [pier(f"pier-e{n}", 4, z) for n, z in enumerate((-10, -5, 1, 6))]

DECK = [{"id": "deck", "type": "rectangle", "operation": "add", "keepClear": True,
         "min_x": -6, "max_x": 6, "min_z": -10, "max_z": 10,
         "floor": 0, "base_height": 1, "material": DECK_MAT}]

# the kerb is broken where each flight comes up off the reef, so the low road has a way
# on rather than a two-block climb at the parapet
KERB = [
    {"id": "kerb-e", "type": "rectangle", "operation": "add", "keepClear": True,
     "min_x": 5, "max_x": 6, "min_z": -5, "max_z": 10,
     "floor": 0, "base_height": 1, "material": CHISELED},
    {"id": "kerb-w", "type": "rectangle", "operation": "add", "keepClear": True,
     "min_x": -6, "max_x": -5, "min_z": -10, "max_z": 5,
     "floor": 0, "base_height": 1, "material": CHISELED},
]

def made(layer_id, name, base_y, shapes):
    return {"id": layer_id, "name": name, "base_y": base_y,
            "kind": "made", "part_of": "causeway", "shapes": shapes,
            "groups": [{"id": layer_id, "name": layer_id, "mirrors": False,
                        "shapeIds": [sh["id"] for sh in shapes]}]}

# bottom-up, because the painter walks the stack in document order
ADD_LAYERS = [
    made("piers", "Causeway piers", REEF_Y, PIERS),
    made("deck", "Causeway deck", DECK_TOP, DECK),
    made("kerb", "Causeway kerb", DECK_TOP + 1, KERB),
]

# ---------------------------------------------------------------- dressing
def tree(pid, st, x, z):
    return {"id": pid, "kind": "tree", "style": st, "x": x, "z": z, "layer": "ground"}

def boulder(pid, x, z, r, h, seed, layer="ground"):
    """Granite, because the reef it stands on is gravel, cobble and andesite and a rock
    cut from the ground's own tones reads as that ground standing up (`DR-TONE`)."""
    return {"id": pid, "kind": "boulder", "x": x, "z": z, "radius": r, "height": h,
            "seed": seed, "layer": layer,
            "material": cell(seed, 6, [s(1, 1), STONE, s(1, 2)])}

DRESSING = {
    "styles": {
        "oak-broad": {"kind": "tree", "form": "template", "species": "oak", "height": 9},
        "birch-thin": {"kind": "tree", "form": "template", "species": "birch", "height": 11},
        # the watch-house: the one building on the board, and it is not grey
            },
    "props": [
        # the way out of the spawn and down to the quay, drawn before anything is scattered
        {"id": "quay-road", "kind": "stroke", "seed": 5, "layer": "ground",
         "points": [[-30, 35], [-22, 34], [-14, 34], [-9, 33]],
         "radius": 2, "style": "solid", "claimsGround": True,
         "material": cell(15, 5, [GRAVEL, ANDESITE, COBBLE])},
        {"id": "wool-road", "kind": "stroke", "seed": 6, "layer": "ground",
         "points": [[4, 33], [7, 40], [10, 48], [10, 55]],
         "radius": 2, "style": "solid", "claimsGround": False,
         "material": cell(15, 5, [GRAVEL, ANDESITE, COBBLE])},
        # the holt behind the west bank: cover on the flank the road does not use
        # the holt on the moor behind the quay, in the one stretch the seats read leaves
        # free of the spawn march, the wool approach and the road standoffs
        # No building. `POST …/sketch/seats` answers four house seats on the whole board at
        # 7x7 and every one of them is on the mid island: between the spawn march, the wool
        # approach and the two roads, an eight-player team side has no room for one. What
        # this board is built out of is the quay, its two flights and the causeway.
        tree("holt-1", "oak-broad", 11, 30), tree("holt-2", "birch-thin", 11, 35),
        tree("holt-3", "oak-broad", -3, 33), tree("holt-4", "birch-thin", -1, 38),
        tree("holt-5", "oak-broad", -4, 43),
        # No boulders. The only ground with room for one is the reef, and a rock on a reef
        # of gravel, cobble and andesite is that ground standing up (`DR-TONE`) whatever
        # stone it is cut from — stone, cobble and andesite being the whole rock palette.
        {"id": "ling", "kind": "flora", "seed": 13, "layer": "ground",
         "points": [[-47, 24], [18, 24], [18, 67], [-47, 67]],
         "spec": {"points": 3600, "coverage": 0.18, "scale": 24, "octaves": 3,
                  "fernShare": 0.3, "flowerShare": 0.06, "flowerScale": 13, "tallShare": 0.04}},
    ],
}

FINISH = {
    "themes": {"moor": THEME_MOOR, "reef": THEME_REEF, "quay": THEME_QUAY},
    "mapTheme": "moor",
    "biome": {"kind": "solid", "id": 1},        # Plains: grass #91bd59 against grey masonry
    "themeById": {"reef-9": "reef"},
    "addShapes": ADD_SHAPES,
    "addLayers": ADD_LAYERS,
    # the moor's coast drawn rather than left as the plan's staircase of rectangles
    "bendShapes": {"bank-e-14": {"k": 0.22, "wander": 3, "step": 9, "seed": 5, "side": "in"}},
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
