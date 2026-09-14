#!/usr/bin/env python3
"""Basaltmere — a capture board in a black bowl with one mere in it.

Writes opus5-basaltmere.plan.json and opus5-basaltmere.finish.json beside this file.

The board is a bowl 90 blocks across and 190 long, terraced in three steps down to a
strand that is mostly under water.  The one hill stands on a basalt stack in the middle
of the mere, and it has no back: two causeways arrive dry off each team's bench and two
shingle spits arrive wet out of the water, one in every quadrant, so a team holding the
pad is holding a place that can be entered from every side at once.

The darkness is the rock's own and not a shadow: the face bands are coal block and black
stained clay, and the only green on the board is the weed on the drowned shelf, which is
where a player stands when they are in the water.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SLUG = "opus5-basaltmere"

# ---------------------------------------------------------------- materials
def s(i, d=0):  return {"kind": "solid", "id": i, "data": d}

STONE, ANDESITE, POLISHED = s(1, 0), s(1, 5), s(1, 6)
COBBLE, GRAVEL, CLAY = s(4), s(13), s(82)
COAL_BLOCK, COAL_ORE = s(173), s(16)
BLACK_CLAY, GRAY_CLAY, GREEN_CLAY = s(159, 15), s(159, 7), s(159, 13)
MOSSY_COBBLE, MOSSY_BRICK, BRICK, CRACKED = s(48), s(98, 1), s(98, 0), s(98, 2)
DARK_PRISMARINE = s(168, 2)
DIRT, COARSE, PODZOL, GRASS = s(3, 0), s(3, 1), s(3, 2), s(2)

def depth(bands, beyond):
    return {"kind": "layered", "axis": "depth",
            "stack": {"ending": "handOver",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]},
            "beyond": beyond}

def slope(bands, beyond):
    """A thickness on the slope axis is a span of degrees, so one stack finishes the pan,
    the shoulder and the face of the same bowl."""
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

def style(name, footing=None, **patch):
    st = json.load(open(os.path.join(REPO, "tools", "styles", name + ".json")))
    st.setdefault("foundation", {})["footing"] = footing
    st.update(patch)
    return st

def watch_shell():
    """The watch hut, forked twice. HS3 reads the half-course slab as the roof body's own
    material and the shell steps andesite in a stone-brick slab, so the body becomes stone
    brick; HS9 wants a laid-log course under a beam and this shell has masonry walls, so
    the beams go rather than the walls changing. A building with no beams states
    `block: -1`; `beams: null` is not a shape the house style reads, and the store
    answers 500 on it rather than a refusal."""
    st = style("hoar-watch")
    st["roof"]["body"] = {"kind": "solid", "id": 98, "data": 0}
    st["beams"]["block"] = -1
    return st

# ---------------------------------------------------------------- themes
# The bowl's own stone, finished by the angle it stands at.  The incline read wants
# roughly two thirds of the ground under twenty degrees on a terraced board, so the bands
# cut at 18 and 32: grit pan, broken shoulder, black face.
BOWL_PAN      = depth([(cell(11, 15, [GRAVEL, COAL_ORE, GRAY_CLAY]), 1), (ANDESITE, 2)], STONE)
BOWL_SHOULDER = depth([(cell(13, 9, [COBBLE, ANDESITE, COAL_ORE]), 1), (STONE, 2)], STONE)
BOWL_FACE     = depth([(cell(17, 7, [COAL_BLOCK, BLACK_CLAY, ANDESITE], rise=6), 2),
                       (ANDESITE, 2)], STONE)

THEME_BASALT = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": GRAVEL},
    "surface": {"enabled": True, "depth": 3,
                "material": slope([(BOWL_PAN, 18), (BOWL_SHOULDER, 14), (BOWL_FACE, 58)], STONE)},
    "wallEnabled": True,
    # the columnar banding a basalt riser shows when it is cut: black over black over grey
    "wall": {"kind": "wallRun", "runs": [
        {"material": BLACK_CLAY, "width": 2}, {"material": COAL_BLOCK, "width": 3},
        {"material": ANDESITE, "width": 2}, {"material": COBBLE, "width": 3}]},
    "fill": cell(3, 11, [STONE, ANDESITE], jitter=35, warp=5, rise=5),
}

# the drowned shelf: the one green on the board, and it is under the water
THEME_WEED = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": GRAVEL},
    "surface": {"enabled": True, "depth": 3,
                "material": slope([
                    (depth([(cell(23, 13, [MOSSY_COBBLE, GREEN_CLAY, DARK_PRISMARINE]), 1),
                            (GRAVEL, 2), (CLAY, 1)], ANDESITE), 20),
                    (depth([(cell(29, 9, [GRAVEL, COBBLE, MOSSY_COBBLE]), 1),
                            (GRAVEL, 2)], ANDESITE), 70)], ANDESITE)},
    "wallEnabled": True,
    "wall": runs([(GRAVEL, 2), (CLAY, 2), (ANDESITE, 4)], STONE),
    "fill": cell(3, 11, [STONE, ANDESITE], jitter=35, warp=5, rise=5),
}

# the stack the hill stands on: the blackest thing on the board, and it has a face
THEME_STACK = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "drop",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": BLACK_CLAY},
    "surface": {"enabled": True, "depth": 3,
                "material": slope([
                    (depth([(cell(31, 7, [COAL_BLOCK, BLACK_CLAY, ANDESITE], rise=5), 1),
                            (ANDESITE, 2)], STONE), 22),
                    (depth([(cell(37, 5, [COAL_BLOCK, BLACK_CLAY]), 2),
                            (ANDESITE, 2)], STONE), 68)], STONE)},
    "wallEnabled": True,
    "wall": {"kind": "wallRun", "runs": [
        {"material": COAL_BLOCK, "width": 4}, {"material": BLACK_CLAY, "width": 2},
        {"material": ANDESITE, "width": 2}]},
    "fill": cell(3, 9, [ANDESITE, STONE], jitter=35, warp=5, rise=5),
}

# ---------------------------------------------------------------- the plan
# Three surfaces, three shapes, and the arrangement is the bowl: the strand under the
# water, the bench over it, the spawn one course above that.  Nothing is cut up so a
# theme has somewhere to hang -- each of the three is a terrace a player stands on.
CELL = 5
STRAND, BRINK, STAITH = 10, 14, 15
PLAN = {
    "plan": 2,
    "meta": {"name": "Basaltmere",
             "notes": "KotH. A black bowl with one mere in it; the hill is a basalt stack "
                      "in the water, entered from all four quadrants."},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 20,
                "surface": BRINK, "observerY": 62},
    "pieces": [
        # the strand crosses the centre and is its own image, which is what makes the
        # middle one continuous sheet of ground rather than two halves and a gap
        {"id": "strand", "role": "piece", "rect": [-9, -6, 18, 12], "surface": STRAND},
        {"id": "brink",  "role": "piece", "rect": [-9,  6, 18,  5], "surface": BRINK},
        {"id": "bield",  "role": "piece", "rect": [-6, 11, 12,  4], "surface": BRINK},
        {"id": "staith", "role": "spawn", "rect": [-3, 15,  6,  4], "surface": STAITH},
    ],
    # building is allowed over the water and nowhere else: the mere is the one place a
    # player may make ground, which is what makes bridging to the stack a decision
    "zones": [{"id": "deep", "rect": [-9, -6, 18, 12], "kind": "build", "holes": []}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "staith", "at": [15, 12],
                    "facing": "front", "footprint": [9, 6, 12, 12]}],
        "iron":   [{"id": "iron-1", "piece": "staith", "at": [18.5, 2.5]}],
        "wools": [], "destroyables": [], "cores": [],
    },
    "walls": [], "boxes": [],
}

# ---------------------------------------------------------------- the relief
# Authored on the +z half and folded by rot_180, except the pan, whose ring is its own
# rot_180 image so both groups solve the same mere floor and agree across the centre.
# The shore wanders between z 18 and z 34 rather than running along the seam between two
# plan rectangles: a rim that is a rectangle's own edge reads as a ruler laid across the
# board, and the mark is what decides where the water stops, not the piece.
PAN_RING = [[-41, -3], [-33, -21], [-22, -31], [-8, -24], [4, -34], [19, -27], [33, -18],
            [41, 3], [33, 21], [22, 31], [8, 24], [-4, 34], [-19, 27], [-33, 18]]

RELIEF = {"*": {
    "base": BRINK, "reach": 0, "step": 1,
    "grain": {"amplitude": 1.5, "scale": 12, "seed": 7},
    "marks": [
        # the mere floor: flat to its own outline, because a pan is what it is
        {"id": "pan", "kind": "area", "h": STRAND, "bevel": 5, "ring": PAN_RING},
        # the bench over the water, rolling rather than a table
        {"id": "bench", "kind": "area", "h": 15, "bevel": 4, "tread": 4,
         "ring": [[-44, 33], [-24, 30], [-4, 32], [18, 30], [44, 34],
                  [44, 62], [20, 66], [-2, 64], [-22, 66], [-44, 62]]},
        # the shelf the spawn hall stands on, one bench further back
        {"id": "howe-flat", "kind": "area", "h": 16, "bevel": 4, "tread": 5,
         "ring": [[-28, 70], [-8, 68], [12, 69], [28, 70], [28, 94], [-28, 94]]},
        # a lower apron on the east bench, so the two flanks are not the same ground
        {"id": "apron", "kind": "area", "h": 13, "bevel": 3,
         "ring": [[14, 34], [30, 32], [42, 37], [42, 50], [28, 54], [16, 48]]},
    ],
    "pushes": [
        # the crag on the west bench: the one thing on this board taller than the stack.
        # amount/falloff 7/16 = 0.44 and crown over the ring's half-width 3.5/8 = 0.44,
        # which is the agreement RL6 reads.
        {"id": "crag", "ring": [[-42, 36], [-30, 33], [-20, 40], [-24, 52], [-38, 54]],
         "amount": 7, "falloff": 16, "crown": 3.5, "roughness": 1, "seed": 5},
        # a low swell behind the bench so the back is not one plane either
        {"id": "howe", "ring": [[-14, 62], [2, 60], [10, 68], [-4, 72]],
         "amount": 3, "falloff": 10, "crown": 1.8, "roughness": 1, "seed": 9},
    ],
}}

# ---------------------------------------------------------------- authored shapes
# The stack and the four ways onto it.  Every ring here is its own rot_180 image about
# (-0.5, -0.5) -- the centre the compiler fans about -- or is authored once and fanned.
STACK_RING = [[-12, -3], [-9, -10], [-1, -13], [7, -11], [12, -4],
              [11, 2], [8, 9], [0, 12], [-8, 10], [-13, 3]]
STACK_TOP = 16

ADD_SHAPES = [
    # the stack: a shape and not a mark, because the whole point of it is the face.
    # `exclude` takes the footprint out of the solve, so the mere floor and the stack
    # top meet at one instead of the relief ramping the water up to it.
    {"id": "stack", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": STACK_TOP, "relief_scope": "exclude", "skirt": 0,
     # the mere is drawn over the stack and a pool cuts every column inside its outline
     # down to the water line: `keepClear` is what says these columns are drawn to be
     # something, and it is the difference between an island and a carved-out hole
     "keepClear": True,
     "theme": "stack", "group": "team", "vertices": STACK_RING},

    # the dry way on: a causeway off each bench, arriving at the stack's shoulder.  A
    # flight is stated rather than graded -- level, anchored, its own material, skirt 0 --
    # and it runs 35 blocks for a rise of 2.
    {"id": "causeway", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": BRINK, "height_mode": "level", "skirt": 0,
     "relief_scope": "exclude", "keepClear": True, "group": "team",
     "material": cell(41, 6, [STONE, COBBLE, ANDESITE], rise=4),
     "vertices": [[-36, 34], [-28, 34], [-5, 8], [-12, 3]],
     "anchor_heights": [BRINK, BRINK, STACK_TOP, STACK_TOP]},

    # the wet way on: a shingle spit that breaks the surface, so a swimmer walks out of
    # the water rather than climbing a face.  6 of rise over 20 of run.
    {"id": "spit", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": STRAND, "height_mode": "level", "skirt": 0,
     "relief_scope": "exclude", "keepClear": True, "group": "team",
     "material": cell(43, 5, [GRAVEL, COBBLE, ANDESITE], rise=4),
     # it starts on the east flank's dry strand rather than in open water, which is what
     # makes the flank a route: the coverage read counts a journey, not a possibility
     "vertices": [[41, 9], [41, -1], [9, -5], [10, 6]],
     "anchor_heights": [STRAND, STRAND, STACK_TOP, STACK_TOP]},

    # two beaches down off each bench: without them the bowl's inner face is a four-block
    # scarp the whole way round and the water is a trap rather than a route
    {"id": "beach-w", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": BRINK, "height_mode": "level", "skirt": 0,
     "relief_scope": "exclude", "keepClear": True, "group": "team",
     "material": cell(47, 5, [GRAVEL, COBBLE], rise=4),
     "vertices": [[-24, 42], [-14, 42], [-14, 26], [-24, 26]],
     "anchor_heights": [BRINK, BRINK, STRAND, STRAND]},
    {"id": "beach-e", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": BRINK, "height_mode": "level", "skirt": 0,
     "relief_scope": "exclude", "keepClear": True, "group": "team",
     "material": cell(53, 5, [GRAVEL, COBBLE], rise=4),
     "vertices": [[22, 40], [32, 40], [32, 26], [22, 26]],
     "anchor_heights": [BRINK, BRINK, STRAND, STRAND]},
]

# ---------------------------------------------------------------- the crown
# A broken ring wall round the pad, with a gate on each of the four approaches: the hill
# has a face to fight over and no side that is the back of it.  `made` keeps SK10's pair
# walk and SK11's reachability walk off a solid standing in a hill.
import math

def annulus(cx, cz, outer, thickness, points=48):
    ring = [(cx + outer * math.cos(2 * math.pi * i / points),
             cz + outer * math.sin(2 * math.pi * i / points)) for i in range(points)]
    inner = [(cx + (outer - thickness) * math.cos(2 * math.pi * i / points),
              cz + (outer - thickness) * math.sin(2 * math.pi * i / points))
             for i in range(points - 1, -1, -1)]
    return [[round(x, 2), round(z, 2)] for x, z in ring + [ring[0]] + inner + [inner[0]]]

CROWN_BLACK = cell(59, 6, [COAL_BLOCK, BLACK_CLAY, ANDESITE], rise=5)
crown_shapes = [{"id": "crown-wall", "type": "polygon", "operation": "add",
                 "floor": STACK_TOP, "base_height": 4, "keepClear": True,
                 "material": CROWN_BLACK,
                 "vertices": annulus(-0.5, -0.5, 10.5, 2)}]
# one gate per quadrant, on the bearing its approach arrives from
# one gate on each approach: the two causeways come in on the diagonals, the two
# spits straight along x
for i, (bearing, width) in enumerate([(90, 7), (135, 7), (270, 7), (315, 7)]):
    a = math.radians(bearing)
    dx, dz = math.sin(a), -math.cos(a)
    px, pz = -0.5 + dx * 9.5, -0.5 + dz * 9.5
    nx, nz = -dz, dx
    reach = 4
    crown_shapes.append({
        "id": f"crown-gate-{i}", "type": "polygon", "operation": "add", "override": True,
        "floor": STACK_TOP, "base_height": 1, "keepClear": True, "material": CROWN_BLACK,
        "vertices": [[round(px + nx * width / 2 - dx * reach, 2), round(pz + nz * width / 2 - dz * reach, 2)],
                     [round(px - nx * width / 2 - dx * reach, 2), round(pz - nz * width / 2 - dz * reach, 2)],
                     [round(px - nx * width / 2 + dx * reach, 2), round(pz - nz * width / 2 + dz * reach, 2)],
                     [round(px + nx * width / 2 + dx * reach, 2), round(pz + nz * width / 2 + dz * reach, 2)]]})

ADD_LAYERS = [{"id": "crown", "name": "crown", "base_y": 0, "kind": "made",
               "part_of": "crown", "shapes": crown_shapes,
               "groups": [{"id": "crown-body", "name": "crown", "mirrors": False,
                           "shapeIds": [x["id"] for x in crown_shapes]}]}]

# ---------------------------------------------------------------- dressing
TREES = json.load(open(os.path.join(HERE, "trees.json")))
STYLES = {k: {"kind": "tree", "form": "copied", "body": v["body"]} for k, v in TREES.items()}
STYLES["watch"] = {"kind": "house", "shell": watch_shell()}

def tree(pid, st, x, z):
    return {"id": pid, "kind": "tree", "style": st, "x": x, "z": z, "layer": "ground"}

def boulder(pid, x, z, r, h, seed):
    # boulders are stone: stone, cobblestone, andesite and nothing else, whatever the
    # board is painted in
    return {"id": pid, "kind": "boulder", "x": x, "z": z, "radius": r, "height": h,
            "seed": seed, "layer": "ground",
            "material": cell(seed, 7, [STONE, COBBLE, ANDESITE], rise=4)}

PROPS = [
    # the mere, its outline its own rot_180 image so the two shores match.  The level is
    # the strand's own height, so the water stands flush with the shelf it drowns and a
    # player walks in rather than dropping in.
    {"id": "mere", "kind": "water", "seed": 61, "layer": "ground", "shape": "pool",
     "points": [[-38, -3], [-31, -19], [-20, -28], [-8, -21], [3, -31], [18, -25],
                [31, -17], [38, 3], [31, 19], [20, 28], [8, 21], [-3, 31], [-18, 25],
                [-31, 17]],
     "radius": 3, "depth": 3, "shore": 3, "shoreWander": True, "edge": 0.55,
     # the bed and the beach are the board's own grit, not the sand a pool lays by default:
     # one pale fringe round a black mere is the whole board's value thrown away
     "bank": cell(73, 7, [GRAVEL, COBBLE, MOSSY_COBBLE, COAL_ORE], rise=3),
     "level": STRAND},
    # the way out of the spawn, down the bench and onto the west causeway
    {"id": "trod", "kind": "stroke", "seed": 5, "layer": "ground",
     "points": [[-2, 80], [-10, 72], [-18, 62], [-26, 48], [-32, 36]],
     "radius": 2, "style": "solid", "claimsGround": True,
     "material": cell(67, 5, [GRAVEL, ANDESITE, COBBLE], rise=4)},
    # one building a side: a watch hut on the crag's shoulder, where a lookout belongs
    {"id": "watch", "kind": "house", "seed": 311, "layer": "ground",
     "style": "watch", "front": "posZ",
     "wings": [{"corners": [[18, 40], [26, 48]]}]},
]

# scrub in the lee of the crag and along the back bench, and nowhere near the water:
# nothing grows on a basalt strand
for i, (x, z) in enumerate([(-40, 46), (-38, 54), (-28, 58), (-8, 56), (12, 66),
                            (14, 52), (34, 50), (40, 38), (-22, 70), (20, 70)]):
    PROPS.append(tree(f"scrub-{i}", ["scrub-a", "scrub-b"][i % 2], x, z))

# fallen blocks under the crag and out on the strand: stone, and the ones in the water
# are what a swimmer aims for
for i, (x, z, r, h) in enumerate([(-38, 42, 3, 4), (-33, 48, 2, 3), (-10, 50, 2, 3),
                                  (8, 46, 2, 2), (34, 34, 2, 3), (38, 44, 3, 4),
                                  (-43, 22, 2, 2), (-6, 44, 2, 2)]):
    PROPS.append(boulder(f"fall-{i}", x, z, r, h, 71 + i))

PROPS.append(
    # cover over the benches only, and thin: a bowl of black rock is not a meadow
    {"id": "ling", "kind": "flora", "seed": 13, "layer": "ground",
     "points": [[-45, 32], [45, 32], [45, 95], [-45, 95]],
     "spec": {"points": 2600, "coverage": 0.14, "scale": 24, "octaves": 3,
              "fernShare": 0.3, "flowerShare": 0.03, "flowerScale": 12, "tallShare": 0.03}})

DRESSING = {"styles": STYLES, "props": PROPS}

# ---------------------------------------------------------------- the finish
FINISH = {
    "themes": {"basalt": THEME_BASALT, "weed": THEME_WEED, "stack": THEME_STACK},
    "mapTheme": "basalt",
    # Deep ocean, so the mere reads blue-black rather than the peat-murk of a moss and the
    # two boards do not share a water colour
    "biome": {"kind": "solid", "id": 24},
    "themeByHeight": {str(STRAND): "weed"},
    "addLayers": ADD_LAYERS,
    "addShapes": ADD_SHAPES,
    "relief": RELIEF,
    "roomStyles": {"spawn": style("sb-spawn")},
    "dressing": DRESSING,
    # one hill, stated absolutely: a compiled intent carries no symmetry, so nothing
    # downstream fans this and one entry is one hill
    "controlPoints": [{"name": "The Stack", "anchor": {"x": 0, "z": 0}, "size": 9,
                       "points": 1, "captureTime": "6s"}],
    "scoreLimit": 750,
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
