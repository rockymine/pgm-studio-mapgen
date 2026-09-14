#!/usr/bin/env python3
"""Slakemoss — a destroy-the-core board in a hall the moss and the water took back.

Writes opus5-slakemoss.plan.json and opus5-slakemoss.finish.json beside this file.

Each team's core stands on a dry plinth inside a ruined chapter house at the back of its
own side.  Between the two of them the nave is roofless and its floor is under water, with
the arcade still standing down either bank — so the short way to the enemy's core is
straight up the middle, wading, in the open, with nothing overhead; and the long way is
round the fen on either flank, dry and slow and out of sight.

The green is the moss on the stone and the fen round it, and it is the board's own colour
rather than a tint: mossy cobble, mossy brick, podzol and peat water under a swamp sky.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SLUG = "opus5-slakemoss"

# ---------------------------------------------------------------- materials
def s(i, d=0):  return {"kind": "solid", "id": i, "data": d}

GRASS, DIRT, COARSE, PODZOL = s(2), s(3, 0), s(3, 1), s(3, 2)
STONE, ANDESITE, COBBLE, GRAVEL, CLAY = s(1, 0), s(1, 5), s(4), s(13), s(82)
MOSSY_COBBLE, MOSSY_BRICK, STONE_BRICK, CRACKED, CHISELED = s(48), s(98, 1), s(98, 0), s(98, 2), s(98, 3)
GREEN_CLAY, GRAY_CLAY, BLACK_CLAY, BROWN_CLAY = s(159, 13), s(159, 7), s(159, 15), s(159, 12)
DARK_PRISMARINE, COAL_ORE = s(168, 2), s(16)


def depth(bands, beyond):
    return {"kind": "layered", "axis": "depth",
            "stack": {"ending": "handOver",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]},
            "beyond": beyond}


def slope(bands, beyond):
    """A span of degrees per band, so one stack finishes the fen's flat, the bank it breaks
    at and the cut face under it without a plan piece for each."""
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


def style(name, footing=None, beams=True):
    """A shipped preset, forked. `beams=False` states `block: -1`, the house style's own
    word for a building whose storeys meet without log ends: HS9 refuses beams over walls
    carrying no laid-log course, and `beams: null` is not a shape the style reads at all."""
    st = json.load(open(os.path.join(REPO, "tools", "styles", name + ".json")))
    st.setdefault("foundation", {})["footing"] = footing
    if not beams and isinstance(st.get("beams"), dict):
        st["beams"]["block"] = -1
    return st


# ---------------------------------------------------------------- themes
# The fen: peat under a thin green skin, finished by the angle it stands at rather than by
# the piece it stands on.
FEN_FLAT     = depth([(cell(11, 15, [GRASS, PODZOL, COARSE]), 1), (DIRT, 2), (CLAY, 1)], GRAVEL)
FEN_SHOULDER = depth([(cell(13, 9, [COARSE, PODZOL, GRAVEL]), 1), (DIRT, 2)], GRAVEL)
FEN_FACE     = depth([(cell(17, 7, [MOSSY_COBBLE, GRAVEL, COBBLE], rise=5), 2),
                      (GRAVEL, 2)], ANDESITE)

THEME_FEN = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": COARSE},
    "surface": {"enabled": True, "depth": 3,
                "material": slope([(FEN_FLAT, 16), (FEN_SHOULDER, 14), (FEN_FACE, 60)], GRAVEL)},
    "wallEnabled": True,
    "wall": runs([(PODZOL, 1), (DIRT, 2), (CLAY, 2), (GRAVEL, 2), (MOSSY_COBBLE, 2),
                  (ANDESITE, 3)], STONE),
    "fill": cell(7, 11, [STONE, ANDESITE], jitter=35, warp=5, rise=5),
}

# the nave: the floor of a hall that has been under water long enough to be a pond bed
THEME_SLAKE = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": GRAVEL},
    "surface": {"enabled": True, "depth": 3,
                "material": slope([
                    (depth([(cell(23, 13, [MOSSY_COBBLE, DARK_PRISMARINE, GREEN_CLAY]), 1),
                            (GRAVEL, 2), (CLAY, 1)], ANDESITE), 18),
                    (depth([(cell(29, 9, [COARSE, GRAVEL, MOSSY_COBBLE]), 1),
                            (CLAY, 2)], ANDESITE), 72)], ANDESITE)},
    "wallEnabled": True,
    "wall": runs([(COARSE, 1), (CLAY, 2), (GRAVEL, 2), (MOSSY_COBBLE, 2), (ANDESITE, 3)], STONE),
    "fill": cell(7, 11, [STONE, ANDESITE], jitter=35, warp=5, rise=5),
}

# the paved ground of the ruin itself: the one built ground on the board, and the moss is
# what tells it apart from the stone of a quarry
THEME_GARTH = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "drop",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": MOSSY_BRICK},
    "surface": {"enabled": True, "depth": 3,
                "material": slope([
                    (depth([(cell(31, 9, [MOSSY_COBBLE, MOSSY_BRICK, CRACKED, GRASS]), 1),
                            (COBBLE, 2)], STONE), 18),
                    (depth([(cell(37, 7, [CRACKED, COBBLE, MOSSY_COBBLE]), 1),
                            (COBBLE, 2)], STONE), 72)], STONE)},
    "wallEnabled": True,
    "wall": {"kind": "wallRun", "runs": [
        {"material": MOSSY_BRICK, "width": 3}, {"material": CRACKED, "width": 2},
        {"material": MOSSY_COBBLE, "width": 3}, {"material": GRAVEL, "width": 2}]},
    "fill": cell(7, 11, [STONE, COBBLE], jitter=35, warp=5, rise=5),
}

# ---------------------------------------------------------------- the plan
# Four surfaces, one course apart, and each is a place: the drowned nave, the fen round it,
# the paved court the ruin stands in, and the frater the team spawns out of.
CELL = 5
SLAKE, FEN, GARTH, FRATER = 13, 14, 15, 16
PLAN = {
    "plan": 2,
    "meta": {"name": "Slakemoss",
             "notes": "DTC. A ruined hall taken back by moss and water: a core a team on a "
                      "dry plinth in the chapter house, the nave between them under water."},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 20,
                "surface": FEN, "observerY": 62},
    "pieces": [
        # the nave crosses the centre and is its own image, so the water in it is one sheet
        {"id": "nave",    "role": "piece", "rect": [-9, -7, 18, 14], "surface": SLAKE},
        {"id": "fen",     "role": "piece", "rect": [-9,  7, 18,  5], "surface": FEN},
        {"id": "court",   "role": "piece", "rect": [-7, 12, 14,  4], "surface": GARTH},
        {"id": "frater",  "role": "spawn", "rect": [-3, 16,  6,  4], "surface": FRATER},
    ],
    # the one place a player may make ground is the water: bridging the nave is what the
    # short way costs
    "zones": [{"id": "nave-zone", "rect": [-4, -7, 8, 14], "kind": "build", "holes": []}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "frater", "at": [15, 12],
                    "facing": "front", "footprint": [9, 6, 12, 12]}],
        "iron":   [{"id": "iron-1", "piece": "frater", "at": [18.5, 2.5]}],
        "wools": [], "destroyables": [],
        # the core rides no plan piece: it stands on a plinth inside the chapter house,
        # which is an authored shape, so `piece: ""` addresses it from the symmetry centre
        "cores": [{"id": "core-1", "piece": "", "at": [-14, 56],
                   "lava": 3, "lavaHeight": 3, "float": 6, "leak": 5}],
    },
    "walls": [], "boxes": [],
}

# ---------------------------------------------------------------- the relief
RELIEF = {"*": {
    "base": FEN, "reach": 0, "step": 1,
    "grain": {"amplitude": 1.7, "scale": 13, "seed": 7},
    "marks": [
        # the nave floor, flat to its own outline because a flagged floor is what it was.
        # The ring is its own rot_180 image, so both groups solve the same floor and agree
        # across the middle.
        {"id": "floor", "kind": "area", "h": SLAKE, "bevel": 4,
         "ring": [[-40, -6], [-33, -24], [-16, -33], [2, -31], [18, -26], [32, -17],
                  [39, 5], [32, 23], [15, 32], [-3, 30], [-19, 25], [-33, 16]]},
        # the fen that grew over the hall's outer court, rolling
        {"id": "fen-flat", "kind": "area", "h": 15, "bevel": 4, "tread": 4,
         "ring": [[-44, 36], [-22, 33], [0, 35], [22, 33], [44, 37],
                  [44, 62], [22, 66], [0, 64], [-22, 66], [-44, 62]]},
        # the court the ruin stands in, flat to its edge because it is paved
        # stated at the court's own surface: a mark a course above it meets the spawn
        # room's own pad on a three-block step, and RL3 reads that as a wall
        {"id": "court-flat", "kind": "area", "h": GARTH, "bevel": 3, "tread": 4,
         "ring": [[-34, 66], [-12, 64], [10, 65], [34, 66], [34, 98], [-34, 98]]},
        # the reedbed on the east flank, a hand lower than the fen: the slow dry way round
        {"id": "reeds", "kind": "area", "h": 14, "bevel": 3,
         "ring": [[16, 38], [34, 35], [44, 42], [42, 56], [24, 60], [14, 50]]},
    ],
    "pushes": [
        # the spoil bank on the west flank, which is what a hall's own rubble becomes.
        # amount/falloff 6/14 = 0.43, crown over the ring's half-width 3.0/7 = 0.43.
        {"id": "bank", "ring": [[-44, 38], [-30, 35], [-22, 42], [-26, 56], [-42, 58]],
         "amount": 6, "falloff": 14, "crown": 3.0, "roughness": 1, "seed": 5},
        # east of the court, clear of the spawn's own pad: a push over it meets the room
        # mark on a step and RL3 reads that as a wall
        {"id": "howe", "ring": [[10, 64], [26, 62], [32, 70], [16, 74]],
         "amount": 3, "falloff": 10, "crown": 1.7, "roughness": 1, "seed": 11},
    ],
}}

# ---------------------------------------------------------------- authored shapes
ADD_SHAPES = [
    # the plinth the core stands on: dry ground inside the chapter house, a shape rather
    # than a mark because the whole point of it is that it has a face and the lava that
    # leaks off it runs down to the court rather than standing in the water
    {"id": "plinth", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": 17, "relief_scope": "exclude", "skirt": 0, "keepClear": True,
     "theme": "garth", "group": "team",
     "vertices": [[-23, 49], [-12, 47], [-4, 53], [-5, 64], [-14, 68], [-24, 61]]},
    # the stair up onto it, stated rather than graded: level, anchored, its own material,
    # and run at four times its rise
    # two ways up onto it, so the core is not behind one stair: the processional from the
    # court, and a broken ramp off the fen on the west
    {"id": "plinth-stair", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": 15, "height_mode": "level", "skirt": 0,
     "relief_scope": "exclude", "keepClear": True, "group": "team",
     "material": cell(41, 6, [MOSSY_COBBLE, COBBLE, CRACKED], rise=4),
     "vertices": [[-20, 78], [-12, 78], [-10, 62], [-18, 62]],
     "anchor_heights": [15, 15, 17, 17]},
    {"id": "plinth-ramp", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": 15, "height_mode": "level", "skirt": 0,
     "relief_scope": "exclude", "keepClear": True, "group": "team",
     "material": cell(45, 6, [MOSSY_COBBLE, GRAVEL, COBBLE], rise=4),
     "vertices": [[-34, 46], [-34, 56], [-22, 55], [-22, 47]],
     "anchor_heights": [15, 15, 17, 17]},
    # the two slipways off the fen into the nave, so the water is a route and not a moat
    {"id": "slip-w", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": FEN, "height_mode": "level", "skirt": 0,
     "relief_scope": "exclude", "keepClear": True, "group": "team",
     "material": cell(43, 5, [GRAVEL, COBBLE, MOSSY_COBBLE], rise=4),
     "vertices": [[-34, 42], [-26, 42], [-26, 26], [-34, 26]],
     "anchor_heights": [FEN + 1, FEN + 1, SLAKE, SLAKE]},
    {"id": "slip-e", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": FEN, "height_mode": "level", "skirt": 0,
     "relief_scope": "exclude", "keepClear": True, "group": "team",
     "material": cell(47, 5, [GRAVEL, COBBLE, MOSSY_COBBLE], rise=4),
     "vertices": [[12, 40], [20, 40], [20, 24], [12, 24]],
     "anchor_heights": [FEN + 1, FEN + 1, SLAKE, SLAKE]},
]

# ---------------------------------------------------------------- the ruin
# Written in the sketch's own shapes rather than stamped: an annulus is one even-odd
# polygon, so a wall costs one shape and no subtract -- and `kind: "made"` keeps SK10's
# pair walk and SK11's reachability walk off a solid standing in a hill.
RUIN_STONE = cell(59, 7, [MOSSY_COBBLE, MOSSY_BRICK, CRACKED, COBBLE], rise=5)


def annulus(cx, cz, outer, thickness, points=48):
    ring = [(cx + outer * math.cos(2 * math.pi * i / points),
             cz + outer * math.sin(2 * math.pi * i / points)) for i in range(points)]
    inner = [(cx + (outer - thickness) * math.cos(2 * math.pi * i / points),
              cz + (outer - thickness) * math.sin(2 * math.pi * i / points))
             for i in range(points - 1, -1, -1)]
    return [[round(x, 2), round(z, 2)] for x, z in ring + [ring[0]] + inner + [inner[0]]]


CHAPTER = (-14, 56)
chapter_shapes = [{"id": "chapter-wall", "type": "polygon", "operation": "add",
                   "floor": 17, "base_height": 8, "keepClear": True,
                   "material": RUIN_STONE,
                   "vertices": annulus(CHAPTER[0], CHAPTER[1], 8.5, 2)}]
# three breaches in the wall, on the three sides an attacker can arrive from: the nave,
# the west bank and the stair up from the court
for i, (bearing, width) in enumerate([(180, 8), (270, 7), (30, 7)]):
    a = math.radians(bearing)
    dx, dz = math.sin(a), -math.cos(a)
    px, pz = CHAPTER[0] + dx * 7.5, CHAPTER[1] + dz * 7.5
    nx, nz = -dz, dx
    chapter_shapes.append({
        "id": f"chapter-breach-{i}", "type": "polygon", "operation": "add",
        "override": True, "floor": 17, "base_height": 1, "keepClear": True,
        "material": RUIN_STONE,
        "vertices": [[round(px + nx * width / 2 - dx * 4, 2), round(pz + nz * width / 2 - dz * 4, 2)],
                     [round(px - nx * width / 2 - dx * 4, 2), round(pz - nz * width / 2 - dz * 4, 2)],
                     [round(px - nx * width / 2 + dx * 4, 2), round(pz - nz * width / 2 + dz * 4, 2)],
                     [round(px + nx * width / 2 + dx * 4, 2), round(pz + nz * width / 2 + dz * 4, 2)]]})

# the arcade down the nave's two banks: discs never touch, so a colonnade is one layer.
arcade_shapes = []
# ten blocks between piers and three blocks across: closer than that is a wall down the
# nave rather than an arcade, and the route read walks it as a barrier every six blocks
for i, z in enumerate(range(2, 34, 10)):
    for side, x in ((0, -21), (1, 21)):
        arcade_shapes.append({
            "id": f"pier-{i}-{side}", "type": "circle", "operation": "add",
            "center_x": x, "center_z": z, "radius": 1.5,
            "floor": 13, "base_height": 9, "keepClear": True, "material": RUIN_STONE})

ADD_LAYERS = [
    {"id": "chapter", "name": "chapter house", "base_y": 0, "kind": "made",
     "part_of": "chapter", "shapes": chapter_shapes,
     "groups": [{"id": "chapter-body", "name": "chapter house", "mirrors": True,
                 "shapeIds": [x["id"] for x in chapter_shapes]}]},
    {"id": "arcade", "name": "arcade", "base_y": 0, "kind": "made",
     "part_of": "arcade", "shapes": arcade_shapes,
     "groups": [{"id": "arcade-body", "name": "arcade", "mirrors": True,
                 "shapeIds": [x["id"] for x in arcade_shapes]}]},
]

# ---------------------------------------------------------------- dressing
TREES = json.load(open(os.path.join(HERE, "trees.json")))
STYLES = {k: {"kind": "tree", "form": "copied", "body": v["body"]} for k, v in TREES.items()}
STYLES["cot"] = {"kind": "house", "shell": style("hoar-store", beams=False)}


def tree(pid, st, x, z):
    return {"id": pid, "kind": "tree", "style": st, "x": x, "z": z, "layer": "ground"}


def boulder(pid, x, z, r, h, seed):
    # boulders are stone: stone, cobblestone, andesite, whatever the board is painted in
    return {"id": pid, "kind": "boulder", "x": x, "z": z, "radius": r, "height": h,
            "seed": seed, "layer": "ground",
            "material": cell(seed, 7, [STONE, COBBLE, ANDESITE], rise=4)}


PROPS = [
    # the water in the nave.  Its outline is its own rot_180 image and its level is the
    # nave floor's own height, so the sheet stands flush with the flags it drowns and a
    # player wades in rather than dropping in.  It is drawn clear of the arcade and the
    # slipways, both of which are keepClear, because a pool empties every column inside
    # its outline down to its own line.
    {"id": "slake", "kind": "water", "seed": 21, "layer": "ground", "shape": "pool",
     "points": [[-19, -5], [-15, -22], [-2, -29], [10, -26], [17, -13],
                [18, 4], [14, 21], [1, 28], [-11, 25], [-17, 12]],
     "radius": 3, "depth": 2, "shore": 2, "shoreWander": True, "edge": 0.5,
     "bank": cell(73, 7, [GRAVEL, COARSE, MOSSY_COBBLE, CLAY], rise=3),
     "level": SLAKE},
    # the way out of the frater door, down the court and round to the chapter stair
    {"id": "trod", "kind": "stroke", "seed": 5, "layer": "ground",
     "points": [[-2, 84], [-9, 81], [-16, 80]],
     "radius": 2, "style": "solid", "claimsGround": True,
     "material": cell(67, 5, [GRAVEL, MOSSY_COBBLE, COBBLE], rise=3)},
    # one building a side: the store that outlasted the hall, on the court's east
    {"id": "cot", "kind": "house", "seed": 311, "layer": "ground",
     "style": "cot", "front": "posZ",
     "wings": [{"corners": [[14, 70], [22, 78]]}]},
]

# the carr: alder and scrub round the fen's edge and out on the reedbed, and none of it
# inside the ruin, where a hall's own floor is what a player reads
for i, (x, z) in enumerate([(-40, 52), (-34, 44), (28, 44), (36, 52), (24, 56),
                            (30, 64), (-32, 62), (6, 60), (20, 64), (-28, 74)]):
    PROPS.append(tree(f"carr-{i}", ["carr-tall", "carr-dense", "scrub-a", "scrub-b"][i % 4], x, z))

# fallen masonry: stone, and only stone, whatever colour the ruin is painted
for i, (x, z, r, h) in enumerate([(-38, 44, 3, 4), (-4, 38, 2, 3), (4, 46, 2, 3),
                                  (-30, 70, 2, 3), (10, 54, 2, 2), (26, 34, 3, 4)]):
    PROPS.append(boulder(f"fall-{i}", x, z, r, h, 71 + i))

PROPS.append(
    # cover over the fen and the court, fern-heavy and both gameplay numbers kept low
    {"id": "sedge", "kind": "flora", "seed": 13, "layer": "ground",
     "points": [[-45, 33], [45, 33], [45, 98], [-45, 98]],
     "spec": {"points": 3600, "coverage": 0.2, "scale": 24, "octaves": 3,
              "fernShare": 0.46, "flowerShare": 0.03, "flowerScale": 12, "tallShare": 0.05}})

DRESSING = {"styles": STYLES, "props": PROPS}

# ---------------------------------------------------------------- the finish
FINISH = {
    "themes": {"fen": THEME_FEN, "slake": THEME_SLAKE, "garth": THEME_GARTH},
    "mapTheme": "fen",
    # Swampland: murky green water and an olive grass tint, which is what makes the fen
    # read as peat rather than as a lawn
    "biome": {"kind": "solid", "id": 6},
    "themeByHeight": {str(SLAKE): "slake", str(GARTH): "garth", str(FRATER): "garth"},
    "addLayers": ADD_LAYERS,
    "addShapes": ADD_SHAPES,
    "relief": RELIEF,
    "roomStyles": {"spawn": style("sb-spawn", beams=False)},
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
