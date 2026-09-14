#!/usr/bin/env python3
"""Mirkholt — a capture-the-wool board in a wood you cannot see across.

Writes opus5-mirkholt.plan.json and opus5-mirkholt.finish.json beside this file.

Each side is a wood shifted onto its own diagonal, so the board's other two quarters are
void and the two sides face each other across one 20-block strait.  A hollow way runs the
length of each wood, sunk four blocks under the floor and roofed by the canopy, and it
delivers a raider straight to the crossing.  The brow stands over it, and it is the only
ground the whole run is visible from.  So a wool run is a choice between the lane, which is
blind both ways, and the brow, where you are the one thing moving that anybody can see.

The two wool rooms stand in cut clearings at the back, and the clearings are the one lit
ground on the board: everything else is dark-oak trunk, leaf litter and moss under a
roofed-forest tint.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SLUG = "opus5-mirkholt"

# ---------------------------------------------------------------- materials
def s(i, d=0):  return {"kind": "solid", "id": i, "data": d}

GRASS, DIRT, COARSE, PODZOL = s(2), s(3, 0), s(3, 1), s(3, 2)
STONE, ANDESITE, COBBLE, GRAVEL, CLAY = s(1, 0), s(1, 5), s(4), s(13), s(82)
MOSSY_COBBLE, MOSSY_BRICK, STONE_BRICK, CRACKED = s(48), s(98, 1), s(98, 0), s(98, 2)
GREEN_CLAY, GRAY_CLAY, BLACK_CLAY, BROWN_CLAY = s(159, 13), s(159, 7), s(159, 15), s(159, 12)
COAL_ORE, DARK_OAK_PLANK = s(16), s(5, 5)

def depth(bands, beyond):
    return {"kind": "layered", "axis": "depth",
            "stack": {"ending": "handOver",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]},
            "beyond": beyond}

def slope(bands, beyond):
    """A span of degrees per band, so one stack finishes the floor of the wood, the bank of
    the hollow way and the broken face of the brow without a piece cut for each."""
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
    """A shipped preset, forked. `beams=False` states `block: -1`, which is the house
    style's own word for a building whose storeys meet without log ends: HS9 refuses beams
    over walls that carry no laid-log course, and `beams: null` is not a shape the style
    reads at all -- the store answers 500 on it rather than a refusal."""
    st = json.load(open(os.path.join(REPO, "tools", "styles", name + ".json")))
    st.setdefault("foundation", {})["footing"] = footing
    if not beams and isinstance(st.get("beams"), dict):
        st["beams"]["block"] = -1
    return st

# ---------------------------------------------------------------- themes
# The wood's floor, finished by its angle.  Leaf litter is what a dark wood's floor is made
# of, so podzol and coarse dirt carry the flat and the grass is the minority in it; the
# roofed-forest tint takes what grass there is to a deep green rather than a meadow's.
MIRK_FLAT     = depth([(cell(11, 15, [PODZOL, GRASS, COARSE]), 1), (DIRT, 2), (COARSE, 1)], GRAVEL)
MIRK_SHOULDER = depth([(cell(13, 9, [COARSE, PODZOL, DIRT]), 1), (DIRT, 2)], GRAVEL)
MIRK_FACE     = depth([(cell(17, 7, [COARSE, GRAVEL, MOSSY_COBBLE], rise=5), 2),
                       (GRAVEL, 2)], ANDESITE)

THEME_MIRK = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": COARSE},
    "surface": {"enabled": True, "depth": 3,
                "material": slope([(MIRK_FLAT, 16), (MIRK_SHOULDER, 14), (MIRK_FACE, 60)], GRAVEL)},
    "wallEnabled": True,
    "wall": runs([(PODZOL, 1), (DIRT, 3), (COARSE, 2), (GRAVEL, 2), (MOSSY_COBBLE, 2),
                  (ANDESITE, 3)], STONE),
    "fill": cell(7, 11, [STONE, ANDESITE], jitter=35, warp=5, rise=5),
}

# the sike: the wet flat at the foot of the lane, one course under the wood and the
# ground the crossing is made from -- mud, gravel and moss where the hollow way drains
THEME_SIKE = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": COARSE},
    "surface": {"enabled": True, "depth": 3,
                "material": slope([
                    (depth([(cell(23, 11, [COARSE, GRAVEL, PODZOL]), 1), (DIRT, 2),
                            (CLAY, 1)], GRAVEL), 18),
                    (depth([(cell(29, 9, [MOSSY_COBBLE, COARSE, GRAVEL], rise=4), 1),
                            (DIRT, 2)], GRAVEL), 72)], GRAVEL)},
    "wallEnabled": True,
    "wall": runs([(COARSE, 1), (DIRT, 2), (CLAY, 2), (MOSSY_COBBLE, 2), (ANDESITE, 3)], STONE),
    "fill": cell(7, 11, [STONE, ANDESITE], jitter=35, warp=5, rise=5),
}

# the clearings at the back: the one lit ground on the board, and the wall round them the
# reason the wood stops where it does
THEME_GLADE = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "drop",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": MOSSY_COBBLE},
    "surface": {"enabled": True, "depth": 3,
                "material": slope([
                    (depth([(cell(31, 13, [GRASS, GRASS, PODZOL]), 1), (DIRT, 2)], GRAVEL), 18),
                    (depth([(cell(37, 9, [COARSE, GRASS, GRAVEL]), 1), (DIRT, 2)], GRAVEL), 72)],
                    GRAVEL)},
    "wallEnabled": True,
    "wall": {"kind": "wallRun", "runs": [
        {"material": MOSSY_COBBLE, "width": 3}, {"material": COBBLE, "width": 2},
        {"material": MOSSY_BRICK, "width": 3}, {"material": GRAVEL, "width": 2}]},
    "fill": cell(7, 11, [STONE, COBBLE], jitter=35, warp=5, rise=5),
}

# ---------------------------------------------------------------- the plan
# The side is SHIFTED west, which is what puts the void in the board: each team's wood
# runs from its own back corner down to a toe at the strait, and rot_180 lays the other
# team's across the opposite diagonal.  What neither of them fills -- the two far quarters
# -- is the board's own device rather than its margin, and it is what keeps the fill ratio
# inside the band a wool board is measured in (G8).  The strait is 20 blocks, which is one
# hop, and it is 41 blocks wide, so the crossing is a decision and not a doorway.
CELL = 5
SIKE, HOLT, BROW, GARTH = 13, 14, 15, 16
PLAN = {
    "plan": 2,
    "meta": {"name": "Mirkholt",
             "notes": "CTW. A dark wood on a shifted diagonal: one hollow way a side runs "
                      "from the clearings down to the strait, and the brow over it is the "
                      "only ground the whole run is visible from."},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 24,
                "surface": HOLT, "observerY": 66},
    "pieces": [
        {"id": "holt",  "role": "piece", "rect": [-10,  2,  8, 10], "surface": HOLT},
        # the toe: the ground the crossing is made from, and the reason the two sides face
        # each other across 41 blocks of strait rather than meeting at one corner
        {"id": "toe",   "role": "piece", "rect": [ -2,  2,  6,  4], "surface": SIKE},
        {"id": "brow",  "role": "piece", "rect": [-10, 12, 14,  2], "surface": BROW},
        {"id": "garth", "role": "piece", "rect": [ -9, 14, 13,  2], "surface": GARTH},
        # cage, lodge, cage in a row: the spawn stands between its two wools rather than
        # behind both, so neither is the one nobody walks to
        {"id": "west-cage", "role": "wool-room", "rect": [-9, 16, 4, 4], "surface": GARTH},
        {"id": "lodge",     "role": "spawn",     "rect": [-5, 16, 5, 4], "surface": GARTH},
        {"id": "east-cage", "role": "wool-room", "rect": [ 0, 16, 4, 4], "surface": GARTH},
    ],
    "zones": [{"id": "strait", "rect": [-10, -4, 20, 8], "kind": "build", "holes": []}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "lodge", "at": [12, 12],
                    "facing": "front", "footprint": [6, 6, 12, 12]}],
        "iron":   [{"id": "iron-1", "piece": "lodge", "at": [3, 10]},
                   {"id": "iron-2", "piece": "lodge", "at": [22, 10]}],
        # the markers sit at the far end of each room: WL2 measures spawn-to-wool on the
        # cell lattice, so a wool a room's width nearer reads as 25 and refuses
        "wools":  [{"id": "wool-1", "piece": "west-cage", "at": [4, 10],
                    "footprint": [3, 3, 14, 14]},
                   {"id": "wool-2", "piece": "east-cage", "at": [16, 10],
                    "footprint": [3, 3, 14, 14]}],
        "destroyables": [], "cores": [],
    },
    "walls": [], "boxes": [],
}

# The ground this side actually has, as blocks, so nothing downstream is placed over void.
GROUND_RECTS = [(-50, 10, -10, 60), (-10, 10, 20, 30), (-50, 60, 20, 70),
                (-45, 70, 20, 80), (-45, 80, 20, 100)]

def on_ground(x, z, inset=4):
    """True where the +z side has ground under (x, z), with a margin off its edge. A prop
    outside it is DR-SITE and a tree on the lip of a void reads as one growing out of air."""
    return any(x0 + inset <= x <= x1 - inset and z0 + inset <= z <= z1 - inset
               for x0, z0, x1, z1 in GROUND_RECTS)

# ---------------------------------------------------------------- the relief
# The hollow way runs from the clearings down through the wood to the toe, so the lane
# arrives at the strait rather than stopping short of it.
HOLLOW = [[-40, 76], [-38, 60], [-32, 44], [-24, 30], [-14, 20], [-2, 16]]

RELIEF = {"*": {
    "base": HOLT, "reach": 0, "step": 1,
    "grain": {"amplitude": 2.1, "scale": 14, "seed": 5},
    "marks": [
        # the wood's floor, rolling, drawn inside the ground it actually has
        {"id": "floor", "kind": "area", "h": 14, "bevel": 4,
         "ring": [[-48, 14], [-34, 12], [-18, 14], [-6, 13], [17, 16], [17, 27],
                  [-8, 28], [-14, 42], [-13, 56], [-30, 58], [-48, 56]]},
        # the hollow way: a line whose band is flat down the middle and lofts to the wood
        # either side, so the lane has banks and not walls
        {"id": "hollow", "kind": "line", "r": 12, "tread": 1,
         "h": [13, 11, 10, 10, 11, 12], "points": HOLLOW},
        # the clearings, flat to their own edge because that is what a cut clearing is
        {"id": "glade", "kind": "area", "h": 16, "bevel": 3, "tread": 4,
         "ring": [[-43, 72], [-20, 70], [2, 71], [18, 73], [18, 98], [-43, 98]]},
    ],
    "pushes": [
        # the brow: the shoulder between the hollow way and the wood's eastern edge, and
        # the one ground the run is visible from.  amount/falloff 7/16 = 0.44 and the crown
        # over the ring's half-width 3.1/7 = 0.44, which is the agreement RL6 reads.
        {"id": "brow-rise", "ring": [[-24, 38], [-14, 36], [-13, 52], [-23, 54]],
         "amount": 7, "falloff": 16, "crown": 3.1, "roughness": 1, "seed": 3},
        # a swell behind the clearings so the back is not one table
        {"id": "howe", "ring": [[-16, 78], [0, 76], [8, 84], [-8, 88]],
         "amount": 3, "falloff": 10, "crown": 1.7, "roughness": 1, "seed": 11},
    ],
}}

# ---------------------------------------------------------------- authored shapes
ADD_SHAPES = [
    # the way off the brow down into the hollow way: a flight, stated rather than graded,
    # run at nearly three times its rise, with a material of its own rather than a theme
    {"id": "brow-stair", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": 14, "height_mode": "level", "skirt": 0,
     "relief_scope": "exclude", "keepClear": True, "group": "team",
     "material": cell(41, 5, [GRAVEL, COBBLE, MOSSY_COBBLE], rise=4),
     "vertices": [[-20, 46], [-14, 46], [-14, 26], [-20, 26]],
     "anchor_heights": [20, 20, 11, 11]},
    # the threshold out of the west clearing and down into the wood: a made edge, which is
    # what a boundary between two grounds of different value needs to be
    {"id": "glade-gate", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": 16, "height_mode": "level", "skirt": 0,
     "relief_scope": "exclude", "keepClear": True, "group": "team",
     "material": cell(43, 5, [COBBLE, MOSSY_COBBLE, GRAVEL], rise=4),
     "vertices": [[-28, 70], [-20, 70], [-20, 56], [-28, 56]],
     "anchor_heights": [16, 16, 14, 14]},
]

# ---------------------------------------------------------------- dressing
TREES = json.load(open(os.path.join(HERE, "trees.json")))
STYLES = {k: {"kind": "tree", "form": "copied", "body": v["body"]} for k, v in TREES.items()}
STYLES["hut"] = {"kind": "house", "shell": style("talltimber-cottage")}


def tree(pid, st, x, z):
    return {"id": pid, "kind": "tree", "style": st, "x": x, "z": z, "layer": "ground"}


def boulder(pid, x, z, r, h, seed):
    # boulders are stone: stone, cobblestone, andesite, whatever the board is painted in
    return {"id": pid, "kind": "boulder", "x": x, "z": z, "radius": r, "height": h,
            "seed": seed, "layer": "ground",
            "material": cell(seed, 7, [STONE, COBBLE, ANDESITE], rise=4)}


def near_hollow(x, z, within):
    """Distance from the hollow way's course, so the lane's own floor can be left open --
    a hollow way roofed at its edges and clear down the middle is what makes it read as a
    lane rather than as a ditch full of trees."""
    best = 1e9
    for (ax, az), (bx, bz) in zip(HOLLOW, HOLLOW[1:]):
        dx, dz = bx - ax, bz - az
        span = dx * dx + dz * dz
        t = 0.0 if span == 0 else max(0.0, min(1.0, ((x - ax) * dx + (z - az) * dz) / span))
        best = min(best, ((x - ax - t * dx) ** 2 + (z - az - t * dz) ** 2) ** 0.5)
    return best < within


TROD = [[-40, 86], [-26, 83], [-13, 83], [2, 85], [15, 87]]

PROPS = [
    # the beck in the bottom of the hollow way.  It states no level, so the line is the
    # lowest surface it crosses and the fill never rises past a column's own surface --
    # water cut into ground that was already there, which is what a lane's runnel is.
    {"id": "lane", "kind": "stroke", "seed": 21, "layer": "ground",
     "points": HOLLOW, "radius": 3, "style": "worn", "claimsGround": True,
     "material": cell(77, 7, [COARSE, GRAVEL, MOSSY_COBBLE, PODZOL], rise=3)},
    # the trod along the back of the clearings, from one room past the spawn door to the
    # other: the only lateral movement on this board that is not through the wood
    {"id": "trod", "kind": "stroke", "seed": 5, "layer": "ground",
     "points": TROD,
     "radius": 2, "style": "solid", "claimsGround": True,
     "material": cell(67, 5, [GRAVEL, COARSE, COBBLE], rise=3)},
    # one building in the wood: a charcoal burner's hut, which is why there is a clearing
    # in the trees at all
    {"id": "hut", "kind": "house", "seed": 311, "layer": "ground",
     "style": "hut", "front": "posZ",
     "wings": [{"corners": [[-46, 61], [-38, 69]]}]},
]

# The wood.  A jittered lattice over the ground this side actually has, three storeys deep
# -- tall dark-oak-trunked canopy, dense crowns, scrub -- with the hollow way's own floor
# and the door approaches left open.
CANOPY = ["mirk-tall-a", "mirk-tall-b", "mirk-giant"]
DENSE = ["mirk-dense-a", "mirk-dense-b"]
SCRUB = ["scrub-a", "scrub-b"]

count = 0
# stone, and only stone -- and all of it on the brow strip and the toe, because a wood
# 40 blocks wide with a 14-block lane down it has no room for a boulder as well as a tree
BOULDERS = [(-30, 66, 3, 4), (-6, 64, 2, 3), (8, 66, 2, 3),
            (-26, 16, 2, 3), (6, 22, 2, 2), (16, 26, 2, 2)]
for i, (x, z, r, h) in enumerate(BOULDERS):
    PROPS.append(boulder(f"stone-{i}", x, z, r, h, 71 + i))

KEEP_OFF = [(-46, 61, -38, 69, 8),       # the charcoal burner's hut
            (-20, 26, -14, 46, 2),       # the flight off the brow
            (-28, 56, -20, 70, 3)]       # the threshold out of the clearing
KEEP_OFF += [(x - r, z - r, x + r, z + r, 4) for x, z, r, _ in BOULDERS]
# the rooms and the ground in front of the spawn door: a room's own keep-out is stated by
# the compile, and a tree inside it is DR-KEEP rather than a tree
KEEP_OFF += [(-42, 72, -28, 97, 7), (3, 72, 17, 97, 7), (-19, 72, -7, 98, 7)]


def near_trod(x, z, within):
    """A trunk stands off a road by three blocks and the road is three wide, so a tree
    inside six of its centreline is DR-ROAD."""
    best = 1e9
    for (ax, az), (bx, bz) in zip(TROD, TROD[1:]):
        dx, dz = bx - ax, bz - az
        span = dx * dx + dz * dz
        t = 0.0 if span == 0 else max(0.0, min(1.0, ((x - ax) * dx + (z - az) * dz) / span))
        best = min(best, ((x - ax - t * dx) ** 2 + (z - az - t * dz) ** 2) ** 0.5)
    return best < within

# A fine lattice, taken greedily at nine blocks between trunks: dense enough that two
# crowns close over the lane and open enough that no tree is declined for standing in
# another's footprint.  Three storeys -- dark-oak-trunked canopy, dense crowns, scrub.
planted = []
count = 0
for row, z in enumerate(range(12, 100, 3)):
    for col, x in enumerate(range(-48, 22, 3)):
        jx = ((row * 7 + col * 13) % 7) - 3
        jz = ((row * 11 + col * 5) % 7) - 3
        px, pz = x + jx, z + jz
        if not on_ground(px, pz, 2):
            continue
        if near_hollow(px, pz, 7) or near_trod(px, pz, 7):
            continue
        if pz > 68 and abs(px + 13) < 15:          # the spawn's own clearing
            continue
        if pz > 76 and (abs(px + 41) < 13 or abs(px - 16) < 13):   # the wool rooms'
            continue
        if any(x0 - m <= px <= x1 + m and z0 - m <= pz <= z1 + m
               for x0, z0, x1, z1, m in KEEP_OFF):
            continue
        # A wood 36 blocks wide with a lane through it holds a great many small trees and
        # a few large ones, so the mix is one canopy giant in six, three dense crowns and
        # two of scrub -- and how close the next trunk may stand is the tree's own size.
        rank = (row * 3 + col) % 6
        kind = (CANOPY[row % 3] if rank == 0 else
                DENSE[rank % 2] if rank < 4 else SCRUB[rank % 2])
        room = 12 if rank == 0 else (9 if rank < 4 else 7)
        if any((px - ax) ** 2 + (pz - az) ** 2 < max(room, other) ** 2
               for ax, az, other in planted):
            continue
        planted.append((px, pz, room))
        PROPS.append(tree(f"holt-{count}", kind, px, pz))
        count += 1

PROPS.append(
    # ground cover: fern-heavy, because that is what grows under a closed canopy, and both
    # gameplay numbers kept low
    {"id": "understorey", "kind": "flora", "seed": 13, "layer": "ground",
     "points": [[-50, 10], [20, 10], [20, 100], [-50, 100]],
     "spec": {"points": 4200, "coverage": 0.22, "scale": 22, "octaves": 3,
              "fernShare": 0.52, "flowerShare": 0.03, "flowerScale": 12, "tallShare": 0.06}})

DRESSING = {"styles": STYLES, "props": PROPS}

# ---------------------------------------------------------------- the finish
FINISH = {
    "themes": {"mirk": THEME_MIRK, "sike": THEME_SIKE, "glade": THEME_GLADE},
    "mapTheme": "mirk",
    # Roofed Forest: the one 1.8 biome that takes grass and leaves to a genuinely dark
    # green rather than shading a meadow
    "biome": {"kind": "solid", "id": 29},
    "themeByHeight": {str(SIKE): "sike", str(GARTH): "glade"},
    "addShapes": ADD_SHAPES,
    "relief": RELIEF,
    "roomStyles": {"spawn": style("hb-spawn", beams=False),
                   "wool": style("hb-cage", beams=False)},
    "dressing": DRESSING,
    "authors": ["Opus 5"],
    "created": "2026-09-14",
    "voidEnforcement": True,
}


def main():
    json.dump(PLAN,   open(os.path.join(HERE, SLUG + ".plan.json"),   "w"), indent=1)
    json.dump(FINISH, open(os.path.join(HERE, SLUG + ".finish.json"), "w"), indent=1)
    print("wrote", SLUG + ".plan.json", "and", SLUG + ".finish.json",
          f"({count} trees on the authored half)")


if __name__ == "__main__":
    main()
