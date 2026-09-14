#!/usr/bin/env python3
"""Mirkholt — a capture-the-wool board in a wood you cannot see across.

Writes opus5-mirkholt.plan.json and opus5-mirkholt.finish.json beside this file.

Each side is a wood shifted onto its own diagonal, so the board's other two quarters are
void and the two sides face each other across one 20-block strait.  A hollow way runs the
length of each wood, sunk four blocks under the floor and roofed by the canopy, and it
delivers a raider straight to the crossing.  The brow stands over it, and it is the only
ground the whole run is visible from.  So a wool run is a choice between the lane, which is
blind both ways, and the brow, where you are the one thing moving that anybody can see.

Neither wool room stands beside the spawn.  Each sits at the far end of its own terrain
spur running off the island -- the west room down a 25-block lane out of the back band, the
east room down a 25-block lane south off the garth -- so reaching one is a commitment and
not a step sideways out of the door.  The lanes are bare ground: void either side, nothing
planted on them, and the emptiness is what makes the room a place.

The clearings the rooms stand in are the one lit ground on the board; everything else is
dark-oak trunk, leaf litter and moss under a roofed-forest tint.
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
# The side is SHIFTED west, which is what puts the void in the board: each team's wood runs
# from its own back corner down to a toe at the strait, and rot_180 lays the other team's
# across the opposite diagonal.  What neither of them fills -- the two far quarters -- is
# the board's device rather than its margin, and it is what keeps the fill ratio inside the
# band a wool board is measured in (G8).
#
# **Each wool room is the far end of a spur, never a neighbour of the spawn.** A room butted
# onto the spawn passes every gate there is -- WL2's text asks for a different lane and only
# its distance clause is implemented, and WL6 has no term at all -- and is still wrong: the
# room has to be walked to. So the back band is spawn, then a 25-block lane, then the room
# (opus5-coinfall's camp -> run -> plinth), and the second room hangs off the garth on a
# lane of its own running south into what was void.
CELL = 5
SIKE, HOLT, BROW, GARTH = 13, 14, 15, 16
PLAN = {
    "plan": 2,
    "meta": {"name": "Mirkholt",
             "notes": "CTW. A dark wood on a shifted diagonal: one hollow way a side runs "
                      "from the garth down to the strait, and each wool room stands at the "
                      "end of its own bare lateral lane off the back."},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 24,
                "surface": HOLT, "observerY": 66},
    "pieces": [
        # The frontline band, and the one piece on this board that is NOT offset. Under
        # rot_180 a front spanning [a, b] is faced by one spanning [-b, -a], so the two are
        # opposite each other only where the edge is symmetric about x = 0: this piece runs
        # x -35..35 and its image x -36..34. The rest of the unit stays on the diagonal,
        # which is what keeps the void in the board.
        {"id": "toe",   "role": "piece", "rect": [ -7,  3, 14,  2], "surface": SIKE},
        # the wood, 45 blocks deep, which is what this board is named for. Everything
        # behind it is pared to the bone instead, because three soft terms read the
        # distance from the front to the rooms and the wood is not what pays for them.
        {"id": "holt",  "role": "piece", "rect": [-10,  5,  9,  9], "surface": HOLT},
        {"id": "brow",  "role": "piece", "rect": [-10, 14,  8,  1], "surface": BROW},
        {"id": "garth", "role": "piece", "rect": [ -8, 15, 15,  2], "surface": GARTH},
        # the back row: cage | lane | apron | lane | cage, so each room is the far end of
        # its own 25-block lateral lane and the two are as far from the front as each other
        # centred on the front rather than hung off one end of it, so the two rooms are
        # the same distance from the frontline (WL10's ratio)
        {"id": "west-cage", "role": "wool-room", "rect": [-11, 17, 3, 3], "surface": GARTH},
        {"id": "west-lane", "role": "piece",     "rect": [ -8, 17, 5, 3], "surface": GARTH},
        {"id": "apron",     "role": "piece",     "rect": [ -3, 17, 5, 3], "surface": GARTH},
        {"id": "east-lane", "role": "piece",     "rect": [  2, 17, 5, 3], "surface": GARTH},
        {"id": "east-cage", "role": "wool-room", "rect": [  7, 17, 3, 3], "surface": GARTH},
        # the spawn behind the apron: off both lane roots, sharing an edge with neither
        # room, and joined along an edge rather than at a corner (PC-C)
        {"id": "lodge",     "role": "spawn",     "rect": [ -3, 20, 5, 3], "surface": GARTH},
    ],
    # exactly the band between the two frontlines and no wider than they are: 30 blocks of
    # gap, spanned end to end, with nothing over land and nothing over void
    "zones": [{"id": "strait", "rect": [-7, -3, 14, 6], "kind": "build", "holes": []}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "lodge", "at": [12, 10],
                    "facing": "front", "footprint": [6, 3, 13, 11]}],
        "iron":   [{"id": "iron-1", "piece": "lodge", "at": [3, 8]},
                   {"id": "iron-2", "piece": "lodge", "at": [22, 8]}],
        "wools":  [{"id": "wool-1", "piece": "west-cage", "at": [5, 7],
                    "footprint": [2, 2, 11, 11]},
                   {"id": "wool-2", "piece": "east-cage", "at": [10, 7],
                    "footprint": [2, 2, 11, 11]}],
        "destroyables": [], "cores": [],
    },
    "walls": [], "boxes": [],
}

# The ground this side actually has, as blocks, so nothing downstream is placed over void.
GROUND_RECTS = [(-35, 15, 35, 25), (-50, 25, -5, 70), (-50, 70, -10, 75),
                (-40, 75, 35, 85), (-55, 85, -40, 100), (-40, 85, -15, 100),
                (-15, 85, 10, 100), (10, 85, 35, 100), (35, 85, 50, 100),
                (-15, 100, 10, 115)]

# The two lanes, kept bare: a lane is a way to walk and not a place to dress, and a wood is
# exactly the board that will grow into one if it is allowed to.
LANES = [(-40, 85, -15, 100), (10, 85, 35, 100)]


def on_ground(x, z, inset=4):
    """True where the +z side has ground under (x, z), with a margin off its edge. A prop
    outside it is DR-SITE and a tree on the lip of a void reads as one growing out of air."""
    return any(x0 + inset <= x <= x1 - inset and z0 + inset <= z <= z1 - inset
               for x0, z0, x1, z1 in GROUND_RECTS)


def on_lane(x, z, margin=3):
    return any(x0 - margin <= x <= x1 + margin and z0 - margin <= z <= z1 + margin
               for x0, z0, x1, z1 in LANES)


# ---------------------------------------------------------------- the relief
# The hollow way runs from the garth down through the wood to the toe, so the lane arrives
# at the strait rather than stopping short of it.
HOLLOW = [[-26, 81], [-20, 71], [-16, 53], [-14, 38], [-10, 24], [-2, 18]]

RELIEF = {"*": {
    "base": HOLT, "reach": 0, "step": 1,
    "grain": {"amplitude": 2.1, "scale": 14, "seed": 5},
    "marks": [
        # the wood's floor, rolling, drawn inside the ground it actually has
        {"id": "floor", "kind": "area", "h": 14, "bevel": 4,
         "ring": [[-48, 28], [-34, 27], [-20, 28], [-8, 30], [-8, 53], [-14, 63],
                  [-32, 67], [-48, 64]]},
        # the wet flat the whole front drains to: the one band on this board that runs the
        # same x range as the enemy's
        {"id": "strandflat", "kind": "area", "h": 13, "bevel": 3,
         "ring": [[-34, 17], [-18, 15], [0, 18], [16, 16], [34, 17],
                  [34, 23], [14, 25], [-2, 22], [-20, 24], [-34, 23]]},
        # the hollow way: a line whose band is flat down the middle and lofts to the wood
        # either side, so the lane has banks and not walls
        # reach 9 rather than 12: a 24-block band through a 40-block wood leaves no wood,
        # and a hollow way's banks are steep anyway
        {"id": "hollow", "kind": "line", "r": 9, "tread": 1,
         "h": [14, 11, 10, 10, 11, 12], "points": HOLLOW},
        # the garth and the back band, flat to their own edge because they are cut ground
        {"id": "glade", "kind": "area", "h": 16, "bevel": 3, "tread": 4,
         "ring": [[-38, 78], [-18, 76], [0, 77], [18, 77], [33, 78], [48, 87],
                  [48, 98], [-53, 98], [-53, 87]]},
        # the ground the spawn hall stands on, one piece behind the back row
        {"id": "bield", "kind": "area", "h": 16, "bevel": 2, "tread": 3,
         "ring": [[-13, 98], [8, 98], [8, 113], [-13, 113]]},
    ],
    "pushes": [
        # the brow west of the hollow way: the one ground the run is visible from.
        # amount/falloff 7/16 = 0.44, crown over the ring's half-width 2.6/6 = 0.44.
        {"id": "brow-rise", "ring": [[-49, 34], [-41, 32], [-39, 56], [-47, 60]],
         "amount": 7, "falloff": 16, "crown": 1.8, "roughness": 1, "seed": 3},
        # a swell on the garth so the back is not one table.  It is kept off both lanes: a
        # lane may step or ramp, but it should do it because the author said so.
        {"id": "howe", "ring": [[-8, 76], [4, 75], [10, 82], [-2, 84]],
         "amount": 3, "falloff": 10, "crown": 1.7, "roughness": 1, "seed": 11},
    ],
}}

# ---------------------------------------------------------------- authored shapes
ADD_SHAPES = [
    # the threshold out of the garth and down into the wood: a made edge, which is what a
    # boundary between two grounds of different value needs to be
    {"id": "glade-gate", "type": "polygon", "operation": "add", "override": True,
     "floor": 0, "base_height": 16, "height_mode": "level", "skirt": 0,
     "relief_scope": "exclude", "keepClear": True, "group": "team",
     "material": cell(43, 5, [COBBLE, MOSSY_COBBLE, GRAVEL], rise=4),
     "vertices": [[-18, 81], [-10, 81], [-10, 69], [-18, 69]],
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


def near_course(points, x, z, within):
    """Distance from a drawn course. A trunk stands off a road by three blocks and a road
    is three wide, so a tree inside six of a centreline is DR-ROAD."""
    best = 1e9
    for (ax, az), (bx, bz) in zip(points, points[1:]):
        dx, dz = bx - ax, bz - az
        span = dx * dx + dz * dz
        t = 0.0 if span == 0 else max(0.0, min(1.0, ((x - ax) * dx + (z - az) * dz) / span))
        best = min(best, ((x - ax - t * dx) ** 2 + (z - az - t * dz) ** 2) ** 0.5)
    return best < within


TROD = [[8, 102], [2, 96], [-4, 90], [-10, 82]]

PROPS = [
    # the lane's own floor, painted wet rather than dug: a channel that states no level
    # still empties every column over its own line
    {"id": "lane", "kind": "stroke", "seed": 21, "layer": "ground",
     "points": HOLLOW, "radius": 2, "style": "worn", "claimsGround": True,
     "material": cell(77, 7, [COARSE, GRAVEL, MOSSY_COBBLE, PODZOL], rise=3)},
    # the trod out of the spawn door and across the garth into the wood.  It does not run
    # down either spur: a lane is walked, not paved.
    {"id": "trod", "kind": "stroke", "seed": 5, "layer": "ground",
     "points": TROD, "radius": 2, "style": "solid", "claimsGround": True,
     "material": cell(67, 5, [GRAVEL, COARSE, COBBLE], rise=3)},
    # one building on this side: a charcoal burner's hut on the garth, which is why there
    # is a clearing in the trees at all
    {"id": "hut", "kind": "house", "seed": 311, "layer": "ground",
     "style": "hut", "front": "posZ",
     "wings": [{"corners": [[14, 76], [22, 84]]}]},
]

# stone, and only stone -- and none of it on a spur: a big boulder is exactly what a bare
# lane must not have
BOULDERS = [(8, 20, 2, 2), (18, 22, 2, 2), (-34, 79, 3, 4), (28, 79, 2, 3)]
for i, (x, z, r, h) in enumerate(BOULDERS):
    PROPS.append(boulder(f"stone-{i}", x, z, r, h, 71 + i))

KEEP_OFF = [(14, 76, 22, 84, 8),         # the charcoal burner's hut
            (-18, 69, -10, 81, 3)]       # the threshold out of the clearing
KEEP_OFF += [(x - r, z - r, x + r, z + r, 4) for x, z, r, _ in BOULDERS]
# the rooms and the ground in front of the spawn door
# the rooms, and the ground in front of the spawn door, which reaches well south
KEEP_OFF += [(-53, 87, -42, 98, 7), (37, 87, 48, 98, 7), (-9, 87, 4, 114, 7)]

# A fine lattice, taken greedily: dense enough that two crowns close over the hollow way
# and open enough that no tree is declined for standing in another's footprint.  The two
# spurs are excluded outright.
CANOPY = ["mirk-tall-a", "mirk-tall-b", "mirk-giant"]
DENSE = ["mirk-dense-a", "mirk-dense-b"]
SCRUB = ["scrub-a", "scrub-b"]

planted = []
count = 0
for row, z in enumerate(range(17, 87, 3)):
    for col, x in enumerate(range(-48, 36, 3)):
        jx = ((row * 7 + col * 13) % 7) - 3
        jz = ((row * 11 + col * 5) % 7) - 3
        px, pz = x + jx, z + jz
        # five blocks off the edge, not two: a copied crown is nine to seventeen blocks
        # across and DR-SITE reads the footprint, not the trunk
        if not on_ground(px, pz, 5):
            continue
        if on_lane(px, pz):
            continue
        # seven from the centreline, not six: the stroke wanders, so the road cell can lie
        # a block or two off the line it was drawn on and DR-ROAD measures the cell
        if near_course(HOLLOW, px, pz, 7) or near_course(TROD, px, pz, 7):
            continue
        if any(x0 - m <= px <= x1 + m and z0 - m <= pz <= z1 + m
               for x0, z0, x1, z1, m in KEEP_OFF):
            continue
        # A wood 35 blocks wide with a lane down it holds a great many small trees and a
        # few large ones, so the mix is one canopy giant in six, three dense crowns and two
        # of scrub -- and how close the next trunk may stand is the tree's own size.
        rank = (row * 3 + col) % 6
        kind = (CANOPY[row % 3] if rank == 0 else
                DENSE[rank % 2] if rank < 4 else SCRUB[rank % 2])
        room = 10 if rank == 0 else (9 if rank < 4 else 7)
        if any((px - ax) ** 2 + (pz - az) ** 2 < max(room, other) ** 2
               for ax, az, other in planted):
            continue
        planted.append((px, pz, room))
        PROPS.append(tree(f"holt-{count}", kind, px, pz))
        count += 1

# Ground cover, fern-heavy because that is what grows under a closed canopy, in two
# polygons rather than one: neither reaches a lane, and a lane is not dressed.
PROPS.append(
    {"id": "understorey", "kind": "flora", "seed": 13, "layer": "ground",
     "points": [[-50, 15], [35, 15], [35, 68], [-50, 68]],
     "spec": {"points": 3200, "coverage": 0.22, "scale": 22, "octaves": 3,
              "fernShare": 0.52, "flowerShare": 0.03, "flowerScale": 12, "tallShare": 0.06}})
PROPS.append(
    {"id": "backcover", "kind": "flora", "seed": 17, "layer": "ground",
     "points": [[-50, 68], [35, 68], [35, 85], [-50, 85]],
     "spec": {"points": 1400, "coverage": 0.2, "scale": 22, "octaves": 3,
              "fernShare": 0.5, "flowerShare": 0.04, "flowerScale": 12, "tallShare": 0.05}})

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
