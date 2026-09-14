#!/usr/bin/env python3
"""Peatgarth — a DTM board on a worked peat moss.

Writes opus5-peatgarth.plan.json and opus5-peatgarth.finish.json beside this file.

The board is a lane 80 blocks across and 200 long, tapering from a full-width
frontline to the works behind each spawn.  A 20-block void seam runs the whole
width and is bridged by a build zone.  One destroyable a team stands on a
stripped peat bench twelve blocks west of the centre line, with four different
ways onto it: open moor from the front, the bench's own south ramp, a flooded
cutting on the east flank that arrives below it, and the knott on the east front
that arrives above.  The ground is finished by its angle, not by its height.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SLUG = "opus5-peatgarth"

# ---------------------------------------------------------------- materials
def s(i, d=0):  return {"kind": "solid", "id": i, "data": d}
GRASS, DIRT, COARSE, PODZOL = s(2), s(3, 0), s(3, 1), s(3, 2)
GRAVEL, STONE, ANDESITE, POLISHED = s(13), s(1, 0), s(1, 5), s(1, 6)
COBBLE, BRICK, CHISELED, CLAY = s(4), s(98, 0), s(98, 3), s(82)

def depth(bands, beyond):
    return {"kind": "layered", "axis": "depth",
            "stack": {"ending": "handOver",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]},
            "beyond": beyond}

def slope(bands, beyond):
    """A thickness on the slope axis is a span of degrees, so one stack finishes
    the flat, the shoulder and the face of the same hill."""
    return {"kind": "layered", "axis": "slope",
            "stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]},
            "beyond": beyond}

def runs(bands, beyond):
    return {"kind": "layered", "axis": "depth",
            "stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]},
            "beyond": beyond}

def cell(seed, size, palette, jitter=40, warp=6, rise=0):
    p = {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter,
         "warp": warp, "palette": palette}
    if rise: p["rise"] = rise
    return p

def house_shell(name):
    """A room style forked into a house prop. `beams: null` is legal in a room style and is
    not a shape the house prop reads: the store answers 500 on it rather than a refusal, so
    a building with no log ends states `block: -1`."""
    st = style(name)
    if not isinstance(st.get("beams"), dict):
        st["beams"] = {"block": -1, "data": 0, "reach": 1, "any": True}
    return st


def style(name, footing=None):
    """A shipped preset, forked.  Footing is null by default and that is the answer:
    over a plate of one course it is a rim round a building with no foundation."""
    st = json.load(open(os.path.join(REPO, "tools", "styles", name + ".json")))
    st.setdefault("foundation", {})["footing"] = footing
    return st

# ---------------------------------------------------------------- themes
# ground: black peat and olive moor grass.  built: grey stone.  accent: dark water.
# The incline read over the built board gives 36% under 10 degrees, 24% in the
# teens, 22% in the twenties, 13% in the thirties and 6% at 40 or steeper, so the
# bands cut at 22 and 34 to make the moor about two thirds and the rock an eighth.
MOOR_FLAT     = depth([(cell(31, 17, [GRASS, PODZOL]), 1), (DIRT, 2), (COARSE, 1)], GRAVEL)
MOOR_SHOULDER = depth([(COARSE, 1), (DIRT, 2)], GRAVEL)
MOOR_FACE     = depth([(DIRT, 2), (GRAVEL, 2)], ANDESITE)

THEME_MOSS = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": GRAVEL},
    "surface": {"enabled": True, "depth": 3,
                "material": slope([(MOOR_FLAT, 22), (MOOR_SHOULDER, 12), (MOOR_FACE, 56)], GRAVEL)},
    "wallEnabled": True,
    "wall": runs([(COARSE, 1), (DIRT, 3), (GRAVEL, 2), (CLAY, 2), (ANDESITE, 4)], STONE),
    "fill": cell(7, 11, [STONE, ANDESITE], jitter=35, warp=5, rise=5),
}

# the flooded cutting: the trench floor the water stands in, and its sides
THEME_CUTTING = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": DIRT},
    "surface": {"enabled": True, "depth": 3,
                "material": depth([(cell(19, 13, [COARSE, DIRT]), 1), (DIRT, 2), (CLAY, 1)], GRAVEL)},
    "wallEnabled": True,
    "wall": runs([(DIRT, 2), (CLAY, 2), (GRAVEL, 3)], ANDESITE),
    "fill": cell(7, 11, [STONE, ANDESITE], jitter=35, warp=5, rise=5),
}

# the works: the stone stage at the head of the tramway.  Grey against brown peat.
THEME_WORKS = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "drop",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": CHISELED},
    "surface": {"enabled": True, "depth": 3,
                "material": depth([(cell(43, 9, [POLISHED, ANDESITE]), 1), (STONE, 2)], COBBLE)},
    "wallEnabled": True,
    "wall": {"kind": "wallRun", "runs": [
        {"material": BRICK, "width": 2}, {"material": ANDESITE, "width": 3},
        {"material": COBBLE, "width": 2}, {"material": GRAVEL, "width": 3}]},
    "fill": cell(7, 11, [STONE, COBBLE], jitter=35, warp=5, rise=5),
}

# ---------------------------------------------------------------- the plan
CELL, SURFACE = 5, 13
PLAN = {
    "plan": 2,
    "meta": {"name": "Peatgarth",
             "notes": "DTM. A worked peat moss: one monument a team on a stripped bench, "
                      "the hags open to the sky between the sides."},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 20,
                "surface": SURFACE, "observerY": 56},
    "pieces": [
        {"id": "fore",   "role": "piece", "rect": [-8,  2, 16, 7], "surface": SURFACE},
        {"id": "garth",  "role": "piece", "rect": [-6,  9, 12, 7], "surface": SURFACE},
        {"id": "stage",  "role": "piece", "rect": [-6, 16,  3, 4], "surface": SURFACE + 1},
        {"id": "staith", "role": "spawn", "rect": [-3, 16,  6, 4], "surface": SURFACE + 1},
    ],
    "zones": [{"id": "pass", "rect": [-8, -2, 16, 4], "kind": "build", "holes": []}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "staith", "at": [15, 12],
                    "facing": "front", "footprint": [9, 6, 12, 12]}],
        "iron":   [{"id": "iron-1", "piece": "staith", "at": [18.5, 2.5]}],
        "wools": [],
        "destroyables": [{"id": "mon-1", "piece": "", "at": [-12, 52],
                          "style": "cube-3", "float": 4,
                          "name": "Peat Store", "materials": "ender stone"}],
        "cores": [],
    },
    "walls": [], "boxes": [],
}

# ---------------------------------------------------------------- the relief
# Authored on the +z half; rot_180 folds it onto the other.  The bench carries no
# bevel, because the whole point of it is that it has a face.
RELIEF = {"*": {
    "base": SURFACE, "reach": 0, "step": 1,
    "grain": {"amplitude": 1.9, "scale": 15, "seed": 5},
    "marks": [
        {"id": "moor-flat", "kind": "area", "h": 14, "bevel": 3,
         "ring": [[-36, 13], [-18, 11], [0, 12], [18, 11], [36, 14],
                  [34, 34], [16, 40], [-2, 38], [-20, 40], [-36, 36]]},
        {"id": "back-flat", "kind": "area", "h": 14, "bevel": 4, "tread": 5,
         "ring": [[-28, 72], [-10, 70], [10, 71], [28, 72], [28, 96], [-28, 96]]},
        # the flooded cutting east of it: the way in from below
        {"id": "hag-e", "kind": "area", "h": 11, "bevel": 2,
         "ring": [[9, 48], [18, 46], [26, 50], [27, 60], [21, 68], [12, 66], [8, 57]]},
        # a dry peat hag on the west front: a second way in from below
        {"id": "hag-w", "kind": "area", "h": 12, "bevel": 2,
         "ring": [[-34, 18], [-26, 16], [-20, 21], [-21, 29], [-28, 32], [-34, 28]]},
    ],
    "pushes": [
        # the knott on the east front: the way in from above.  amount/falloff 0.33
        # and crown over the ring's half-width 3.3/10 = 0.33 — RL6 wants them to agree.
        {"id": "knott", "ring": [[14, 16], [26, 14], [34, 20], [33, 31], [22, 34], [15, 29]],
         "amount": 6, "falloff": 18, "crown": 3.3, "roughness": 1, "seed": 3},
        # a low rise on the west front, so the moor is not one plane
        {"id": "rigg", "ring": [[-36, 30], [-26, 31], [-24, 39], [-32, 42]],
         "amount": 3, "falloff": 9, "crown": 1.7, "roughness": 1, "seed": 11},
    ],
}}

# ---------------------------------------------------------------- authored shapes
ADD_SHAPES = [
    # the stripped bench the monument stands on.  It is a shape and not a mark
    # because the whole point of a cut peat bench is that it has a face: exclude
    # takes the footprint out of the solve and the two tiers meet at one.
    {"id": "bench", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": 19, "relief_scope": "exclude", "skirt": 0, "group": "team",
     "theme": "works", "keepClear": True,
     "vertices": [[-26, 46], [-16, 43], [-4, 45], [0, 53], [-2, 64],
                  [-12, 68], [-22, 66], [-27, 57]]},
    # the tramway ramp up the bench's south face: a flight, stated rather than
    # graded, a material rather than a theme, run at nearly three times its rise
    {"id": "bench-ramp", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": 14, "height_mode": "level", "skirt": 0,
     "relief_scope": "exclude", "keepClear": True, "material": ANDESITE,
     "vertices": [[-24, 31], [-15, 31], [-15, 45], [-24, 45]],
     "anchor_heights": [14, 14, 19, 19], "group": "team"},
    # bare peat scalded off the bench where it is walked
    {"id": "bench-scald", "type": "polygon", "operation": "add",
     "floor": 0, "base_height": 19, "theme": "cutting", "group": "team",
     "vertices": [[-22, 50], [-10, 48], [-6, 57], [-15, 63], [-23, 59]]},
]

# ---------------------------------------------------------------- dressing
def tree(pid, st, x, z):
    return {"id": pid, "kind": "tree", "style": st, "x": x, "z": z, "layer": "ground"}

def boulder(pid, x, z, r, h, seed):
    return {"id": pid, "kind": "boulder", "x": x, "z": z, "radius": r, "height": h,
            "seed": seed, "layer": "ground",
            "material": cell(seed, 7, [STONE, COBBLE, ANDESITE])}

DRESSING = {
    "styles": {
        # drowned spruce: the only trees a peat moss carries, and they stand in a stand
        "spruce-tall":  {"kind": "tree", "form": "template", "species": "spruce", "height": 15},
        "spruce-short": {"kind": "tree", "form": "template", "species": "spruce", "height": 10},
        # the same shell the spawn hall is built from, so the two buildings at the head
        # of the tramway are one family rather than two styles eleven blocks apart. A
        # house prop reads `beams` and a null is not a shape it reads, so a building with
        # none states `block: -1`.
        "peat-store":   {"kind": "house", "shell": house_shell("sb-spawn")},
    },
    "props": [
        # the water fills the cutting the relief already dug, so the two agree:
        # its outline is the hag's own ring and its level is two under that ground
        {"id": "cut-e", "kind": "water", "seed": 21, "layer": "ground", "shape": "pool",
         "points": [[9, 48], [18, 46], [26, 50], [27, 60], [21, 68], [12, 66], [8, 57]],
         "radius": 2, "depth": 2, "shore": 2, "shoreWander": False, "edge": 0.4, "level": 9},
        # the way out of the spawn and down to the ramp, drawn before the scenery
        {"id": "tramway", "kind": "stroke", "seed": 5, "layer": "ground",
         "points": [[-8, 79], [-14, 70], [-18, 58], [-19, 46], [-19, 34]],
         "radius": 2, "style": "solid", "claimsGround": True,
         "material": cell(9, 5, [GRAVEL, ANDESITE, COBBLE])},
        # the peat store on the stone stage: one building, standing where the
        # tramway ends, and not in the family the ground under it is painted in
        {"id": "store", "kind": "house", "seed": 485, "layer": "ground",
         "style": "peat-store", "front": "posZ",
         "wings": [{"corners": [[-30, 70], [-20, 82]]}]},
        # the holt on the east front: cover to within a few blocks of the moor
        tree("holt-1", "spruce-tall", 12, 20), tree("holt-2", "spruce-short", 19, 16),
        tree("holt-3", "spruce-tall", 8, 27), tree("holt-4", "spruce-short", 21, 33),
        tree("holt-5", "spruce-tall", 16, 31), tree("holt-6", "spruce-short", 28, 18),
        tree("holt-7", "spruce-tall", 4, 17),
        # a few drowned ones standing in the cutting's shallows
        tree("cut-1", "spruce-short", 6, 45), tree("cut-2", "spruce-tall", 29, 66),
        # boulders on the knott: stone, and only stone
        boulder("knott-1", 24, 22, 3, 4, 41), boulder("knott-2", 30, 27, 2, 3, 42),
        boulder("knott-3", 18, 27, 2, 3, 43),
        # ground cover over the whole board: the shape is the board, the patchiness
        # the field's, and both gameplay numbers kept low
        {"id": "ling", "kind": "flora", "seed": 13, "layer": "ground",
         "points": [[-40, 8], [40, 8], [40, 98], [-40, 98]],
         "spec": {"points": 5200, "coverage": 0.2, "scale": 26, "octaves": 3,
                  "fernShare": 0.34, "flowerShare": 0.05, "flowerScale": 14, "tallShare": 0.04}},
    ],
}

FINISH = {
    "themes": {"moss": THEME_MOSS, "cutting": THEME_CUTTING, "works": THEME_WORKS},
    "mapTheme": "moss",
    "biome": {"kind": "solid", "id": 6},       # Swampland: grass #6a7039, murky water
    "addShapes": ADD_SHAPES,
    # the coast, the frontline included, drawn rather than left over from the plan's
    # rectangles.  The bend only ever moves a point inward, so the strait can only widen.
    "bendShapes": {"fore-13": {"k": 0.24, "wander": 4, "step": 8, "seed": 5}},
    "relief": RELIEF,
    "roomStyles": {"spawn": style("sb-spawn")},
    "dressing": DRESSING,
    "authors": ["Opus 5"],
    "created": "2026-09-14",
    "voidEnforcement": True,
}

def main():
    json.dump(PLAN,   open(os.path.join(HERE, SLUG + ".plan.json"),   "w"), indent=1)
    json.dump(FINISH, open(os.path.join(HERE, SLUG + ".finish.json"), "w"), indent=1)
    print("wrote", SLUG + ".plan.json", "and", SLUG + ".finish.json")

if __name__ == "__main__":
    main()
